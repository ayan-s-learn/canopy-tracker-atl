import argparse
import gzip
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from pyproj import Transformer
from shapely import segmentize, transform, union_all
from shapely.geometry import Polygon, box, mapping, shape
from shapely.geometry.polygon import orient

ROOT = Path(__file__).resolve().parent
T02 = ROOT.parent / 'T02-geography'
YEARS = (2023, 2025)
TOLERANCE_M2 = 2
TO_AREA = Transformer.from_crs('OGC:CRS84', 5070, always_xy=True)
TO_LONLAT = Transformer.from_crs(5070, 'OGC:CRS84', always_xy=True)
TO_AREA_FROM_UTM = Transformer.from_crs(26916, 5070, always_xy=True)


def load(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def geography():
    sources = load(T02 / 't02-sources.json')
    snapshots = []
    for key in ('city_boundary', 'county_overlay'):
        entry = sources[key]
        path = T02 / entry['path']
        raw = path.read_bytes()
        if path.suffix == '.gz':
            raw = gzip.decompress(raw)
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError(f'T02 snapshot changed: {path.name}')
        snapshots.append(json.loads(raw)['features'])

    city_feature, = snapshots[0]
    city = valid(transform(shape(city_feature['geometry']), TO_AREA.transform, interleaved=False))
    counties = {
        f['properties']['GEOID']: city.intersection(
            valid(transform(shape(f['geometry']), TO_AREA.transform, interleaved=False)))
        for f in snapshots[1]
    }
    fulton, dekalb = counties['13121'], counties['13089']
    shared = polygonal(fulton.intersection(dekalb))
    assigned = fulton.union(dekalb)
    zones = {'Fulton': polygonal(fulton.difference(shared)),
             'DeKalb': polygonal(dekalb.difference(shared)),
             'county_unassigned': polygonal(city.difference(assigned).union(shared))}
    if abs(city.area - sources['area_check']['expected_m2']['city']) > TOLERANCE_M2:
        raise ValueError('City denominator differs from the pinned T02 check')
    return city, zones


def valid(geometry):
    if not geometry.is_valid or geometry.is_empty:
        raise ValueError('Expected nonempty, valid source geometry')
    return geometry


def catalog_polygon(rings):
    # For these snapshots the Esri rings are clockwise exteriors with no holes.
    polygons = [valid(Polygon(ring)) for ring in rings]
    if not polygons or any(p.exterior.is_ccw for p in polygons):
        raise ValueError('Unexpected catalog ring orientation')
    return union_all([transform(segmentize(p, .001), TO_AREA.transform, interleaved=False)
                      for p in polygons])


def catalog_epoch(snapshot, year, city):
    query_box = box(*map(float, parse_qs(urlsplit(snapshot['ids_url']).query)['geometry'][0].split(',')))
    if snapshot['footprint_crs'] != 'OGC:CRS84' or not query_box.covers(
            transform(city, TO_LONLAT.transform, interleaved=False)):
        raise ValueError('Catalog query envelope misses part of the City')
    if sorted(asset['OBJECTID'] for asset in snapshot['assets']) != sorted(snapshot['object_ids']):
        raise ValueError(f'{year} catalog features and ID-only query differ')
    assets = {}
    unresolved = []
    for row in snapshot['assets']:
        if row['Category'] == 2:
            continue
        if row['Category'] != 1:
            raise ValueError(f"Unexpected imagery category for {row['Name']}")
        polygon = polygonal(catalog_polygon(row['rings']).intersection(city))
        if polygon.area == 0:
            continue
        tile = row['Name']
        if tile in assets:
            raise ValueError(f'Duplicate tile name: {tile}')
        date_field = 'acquisition_date' if year == 2023 else 'QQDATE'
        from_field = (datetime.fromtimestamp(row[date_field] / 1000, timezone.utc).date()
                      if row[date_field] else None)
        from_name = re.search(r'_(\d{8})$', tile)
        date = from_field.isoformat() if from_field and from_name and (
            from_field.strftime('%Y%m%d') == from_name[1] and from_field.year == year) else None
        assets[tile] = (polygon, date)
        if date is None:
            unresolved.append(polygon)
    return assets, polygonal(union_all(unresolved))


def assign(assets):
    occupied = Polygon()
    selected = {}
    ambiguous_date = Polygon()
    by_date = defaultdict(list)
    for name, (polygon, date) in sorted(assets.items()):
        if date is None:
            continue
        selected[name] = polygon.difference(occupied)
        occupied = occupied.union(polygon)
        by_date[date].append(polygon)
    seen = Polygon()
    for polygons in by_date.values():
        footprint = union_all(polygons)
        ambiguous_date = ambiguous_date.union(seen.intersection(footprint))
        seen = seen.union(footprint)
    if abs(sum(p.area for p in selected.values()) - occupied.area) > TOLERANCE_M2:
        raise ValueError('Selected tile areas do not reconcile')
    return selected, occupied, ambiguous_date


def classify(zone, early, late, unknown):
    unresolved = zone.intersection(unknown)
    known = zone.difference(unresolved)
    return {
        'both': known.intersection(early).intersection(late),
        '2023_only': known.intersection(early).difference(late),
        '2025_only': known.intersection(late).difference(early),
        'neither': known.difference(early.union(late)),
        'unresolved': unresolved,
    }


def partitions(city, zones, masks):
    for key, zone in {**zones, 'City': city}.items():
        parts = masks[key].values()
        total = sum(part.area for part in parts)
        fused = union_all(list(parts))
        if abs(total - fused.area) > TOLERANCE_M2 or (
                fused.symmetric_difference(zone).area > TOLERANCE_M2):
            raise ValueError(f'{key} area does not reconcile')
    if abs(sum(zone.area for zone in zones.values()) - city.area) > TOLERANCE_M2:
        raise ValueError('County areas do not reconcile to the City')


def exposure_dates(city, windows, catalogs, assigned):
    results = {}
    for year, entry in load(ROOT / 'date-index.json.gz').items():
        response = entry['response']
        if response.get('error') or response.get('exceededTransferLimit') or (
                response['spatialReference']['wkid'] != 4326):
            raise ValueError(f'Incomplete exposure-date query for {year}')
        dates = defaultdict(list)
        source_pieces = []
        for feature in response['features']:
            attrs = feature['attributes']
            source_id = attrs['objectid'] if year == '2023' else attrs['FID']
            date = (datetime.fromtimestamp(attrs['date'] / 1000, timezone.utc).date().isoformat()
                    if year == '2023' else attrs['IDATE'])
            polygon = catalog_polygon(feature['geometry']['rings']).intersection(city)
            dates[date].append(polygon)
            source_pieces.append((source_id, date, polygon))
        by_date = {date: union_all(polygons) for date, polygons in sorted(dates.items())}
        footprint = union_all(list(by_date.values()))
        tile_dates = catalogs[int(year)][0]
        selected = assigned[int(year)][0]
        mismatched = union_all([
            poly.difference(by_date.get(tile_dates[name][1], Polygon())).intersection(footprint)
            for name, poly in selected.items()
        ])
        results[year] = {
            'city_m2_by_date': {date: round(p.area, 3) for date, p in by_date.items()},
            'selected_tile_date_unmatched_in_date_index_m2': round(mismatched.area, 3),
            'outside_date_index_city_m2': round(city.difference(footprint).area, 3),
            'overlapping_dates_city_m2': round(sum(p.area for p in by_date.values()) - footprint.area, 3),
            'window_intersection_m2': {
                name: {**{date: round(window.intersection(p).area, 3) for date, p in by_date.items()},
                       'outside_date_index': round(window.difference(footprint).area, 3)}
                for name, window in windows.items()
            },
            'window_source_polygons': {
                name: [{'id': source_id, 'date': date, 'area_m2': area}
                       for source_id, date, polygon in sorted(source_pieces)
                       if (area := round(window.intersection(polygon).area, 3)) > 0]
                for name, window in windows.items()
            },
        }
    return results


def polygons_only(geometry):
    if geometry.geom_type == 'Polygon' and not geometry.is_empty:
        yield orient(geometry)
    elif hasattr(geometry, 'geoms'):
        for component in geometry.geoms:
            yield from polygons_only(component)


def polygonal(geometry):
    if geometry.geom_type in ('Polygon', 'MultiPolygon'):
        return geometry
    parts = list(polygons_only(geometry))
    return union_all(parts) if parts else Polygon()


def main():
    parser = argparse.ArgumentParser(description='Rebuild T05 catalog coverage artifacts offline.')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    city, zones = geography()
    snapshot = load(ROOT / 'catalog.json')
    catalogs = {year: catalog_epoch(snapshot[str(year)], year, city) for year in YEARS}
    assigned = {year: assign(catalogs[year][0]) for year in YEARS}
    early, late = (assigned[year][1] for year in YEARS)
    unknown = polygonal(union_all([catalogs[year][1].difference(assigned[year][1]) for year in YEARS]))
    masks = {name: classify(zone, early, late, unknown) for name, zone in {**zones, 'City': city}.items()}
    partitions(city, zones, masks)
    window_features = load(ROOT / 'development-windows.geojson')['features']
    windows = {}
    for feature in window_features:
        props = feature['properties']
        area = transform(segmentize(box(*props['bbox_epsg26916']), 25),
                         TO_AREA_FROM_UTM.transform, interleaved=False)
        reservation = transform(shape(feature['geometry']), TO_AREA.transform, interleaved=False)
        if not reservation.covers(area):
            raise ValueError(f"Understated read reservation: {props['site']}")
        if area.difference(zones[props['county']]).area > TOLERANCE_M2:
            raise ValueError(f"Read window outside intended county: {props['site']}")
        for year, asset in zip(YEARS, props['tiles'], strict=True):
            footprint, date = catalogs[year][0][asset]
            if date is None or area.difference(footprint).area > TOLERANCE_M2:
                raise ValueError(f"Read window lacks dated tile coverage: {props['site']} {year}")
        windows[props['site']] = area

    areas = {}
    features = []
    for name, parts in masks.items():
        zone = city if name == 'City' else zones[name]
        areas[name] = {'total': round(zone.area, 3),
                       **{key: round(value.area, 3) for key, value in parts.items()},
                       'different_dated_tile_overlap': {
                           year: round(zone.intersection(assigned[year][2]).area, 3) for year in YEARS}}
        if name == 'City':
            continue
        for key, geometry in parts.items():
            projected = transform(geometry, TO_LONLAT.transform, interleaved=False)
            polygons = list(polygons_only(projected))
            if polygons:
                exported = {'type': 'MultiPolygon',
                            'coordinates': [mapping(p)['coordinates'] for p in polygons]}
                recovered = transform(shape(exported), TO_AREA.transform, interleaved=False)
                if not recovered.is_valid or abs(recovered.area - geometry.area) > TOLERANCE_M2:
                    raise ValueError(f'Exported mask area changed for {name} {key}')
                features.append({'type': 'Feature',
                                 'properties': {'zone': name, 'coverage': key, 'area_m2': areas[name][key]},
                                 'geometry': exported})

    output = {
        'area_crs': 'EPSG:5070',
        'tolerance_m2': TOLERANCE_M2,
        'areas_m2': areas,
        'intersecting_assets': {
            year: [{'name': name, 'tile_date': date, 'city_m2': round(geom.area, 3),
                    'selected_city_m2': round(assigned[year][0].get(name, Polygon()).area, 3)}
                   for name, (geom, date) in sorted(catalogs[year][0].items())]
            for year in YEARS},
        'exposure_date_context': exposure_dates(city, windows, catalogs, assigned),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'areas.json').write_text(json.dumps(output, indent=2) + '\n')
    mask = {'type': 'FeatureCollection', 'features': features}
    with (args.output / 'catalog-mask.geojson.gz').open('wb') as out:
        out.write(gzip.compress((json.dumps(mask, separators=(',', ':')) + '\n').encode(), mtime=0))


if __name__ == '__main__':
    main()

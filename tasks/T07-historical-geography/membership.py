import argparse
import gzip
import hashlib
import json
from datetime import date, datetime, timezone
from itertools import combinations
from pathlib import Path

from pyproj import Transformer
from shapely import intersection_all, make_valid, orient_polygons, transform, union_all
from shapely.geometry import GeometryCollection, box, mapping, shape


HERE = Path(__file__).resolve().parent
T02 = HERE.parent / 'T02-geography'
T01 = HERE.parent / 'T01-imagery'
CLASSES = {
    (True, True): 'inside_both',
    (True, False): 'first_only',
    (False, True): 'second_only',
    (False, False): 'outside_both',
}
LABELS = (*CLASSES.values(), 'unresolved')


def read_json(path, sha256=None, *, hash_uncompressed=False):
    raw = path.read_bytes()
    decoded = gzip.decompress(raw) if path.suffix == '.gz' else raw
    if sha256 and hashlib.sha256(decoded if hash_uncompressed else raw).hexdigest() != sha256:
        raise ValueError(f'Input hash mismatch: {path}')
    return json.loads(decoded)


def reproject(geometry, source, target='EPSG:5070'):
    transformer = Transformer.from_crs(source, target, always_xy=True)
    return transform(geometry, transformer.transform, interleaved=False)


def polygonal(geometry):
    if geometry.geom_type in ('Polygon', 'MultiPolygon'):
        return geometry
    if geometry.geom_type == 'GeometryCollection':
        return union_all([polygonal(part) for part in geometry.geoms])
    return GeometryCollection()


def dated_state(case, window):
    start, end = window
    earliest = case['earliest_effective_date']
    latest = case['latest_effective_date']
    if earliest and end < date.fromisoformat(earliest):
        return case['direction'] == 'deannexation'
    if latest and start >= date.fromisoformat(latest):
        return case['direction'] == 'annexation'
    return None


def classify(first, second):
    return CLASSES.get((first, second), 'unresolved')


def partition(city, census, cases, first, second):
    snapshots = [city, *census.values()]
    snapshot_union = union_all(snapshots)
    case_union = union_all([geometry for _, geometry in cases])
    domain = snapshot_union.union(case_union)
    parts = {label: [] for label in LABELS}
    parts['inside_both'].append(intersection_all(snapshots).difference(case_union))
    # Only supported event polygons can supply a positive outside finding in this evidence domain.
    overlap = union_all([a.intersection(b) for (_, a), (_, b) in combinations(cases, 2)])
    for case, geometry in cases:
        if case['disposition'] in ('apply', 'bounded'):
            core = geometry.difference(overlap)
            if case['direction'] == 'annexation':
                core = polygonal(core.intersection(city))
            state = classify(dated_state(case, first), dated_state(case, second))
            if state != 'unresolved':
                parts[state].append(core)

    covered = union_all([g for pieces in parts.values() for g in pieces])
    parts['unresolved'].append(domain.difference(covered))
    return domain, {label: polygonal(union_all(pieces)) for label, pieces in parts.items()}


def load_inputs():
    sources = read_json(HERE / 'sources.json')
    sources_t02 = read_json(T02 / 't02-sources.json')
    features_t02 = {}
    for dataset in ('city_boundary', 'county_overlay', 'annexations'):
        source = sources_t02[dataset]
        features_t02[dataset] = read_json(T02 / source['path'], source['sha256'],
                                          hash_uncompressed=True)['features']
    boundary, = features_t02['city_boundary']
    city = reproject(shape(boundary['geometry']), 'OGC:CRS84')
    counties = {
        f['properties']['GEOID']: reproject(shape(f['geometry']), 'OGC:CRS84')
        for f in features_t02['county_overlay']
    }
    census = {
        f['properties']['vintage']: reproject(shape(f['geometry']), sources['census_places']['source_crs'])
        for f in read_json(HERE / 'tiger-places.geojson.gz',
                           sources['census_places']['archived_extract']['sha256'])['features']
    }
    events = {
        f['properties']['OBJECTID']: reproject(shape(f['geometry']), 'OGC:CRS84') if f['geometry'] else None
        for f in read_json(HERE / 'city-changes.geojson',
                           sources['city_arcgis']['archived_response']['sha256'])['features']
    }
    ledger = read_json(HERE / 'effective-dates.json')
    ids = {case['city_objectid'] for case in ledger['cases'] if case['city_objectid'] is not None}
    if ids != events.keys():
        raise ValueError('The ledger must account for every archived City geometry row')
    if any(not g.is_valid for g in (city, *counties.values(), *census.values(),
                                     *(g for g in events.values() if g is not None))):
        raise ValueError('Invalid input geometry')
    return ledger, city, counties, census, events, sources_t02['area_check'], sources['t01_windows_sha256']


def t01_windows(sha256):
    samples = read_json(T01 / 't01-windows.json', sha256)['samples']
    return {
        (sample['site'], sample['year']): (
            datetime.fromtimestamp(sample['attributes'][sample['acquisition_date_field']] / 1000,
                                   timezone.utc).date(),
            reproject(box(*sample['bbox']), sample['crs']),
        )
        for sample in samples
    }


def county_areas(geometry, counties):
    fulton = geometry.intersection(counties['13121'])
    dekalb = geometry.intersection(counties['13089'])
    residual = geometry.difference(union_all(list(counties.values())))
    return {
        'total': geometry.area,
        'fulton': fulton.area,
        'dekalb': dekalb.area,
        'county_unassigned': residual.area,
        'county_overlap': fulton.intersection(dekalb).area,
    }


def validate_partition(city, counties, domain, parts, expected):
    tolerance = expected['tolerance_m2']
    if domain.symmetric_difference(union_all(list(parts.values()))).area > tolerance:
        raise ValueError('Partition does not cover the evidence domain')
    if sum(a.intersection(b).area for a, b in combinations(parts.values(), 2)) > tolerance:
        raise ValueError('Partition has overlapping membership classes')
    compare_to = expected['expected_m2']
    discovery = county_areas(city, counties)
    for county, t02_key in (
        ('total', 'city'), ('fulton', 'fulton_city_intersection'), ('dekalb', 'dekalb_city_intersection'),
        ('county_unassigned', 'city_outside_counties'), ('county_overlap', 'city_in_both_counties'),
    ):
        if abs(discovery[county] - compare_to[t02_key]) > tolerance:
            raise ValueError(f'T02 replay failed for {county}')
    return discovery


def event_areas(cases, events, city, census, first, second):
    areas = []
    for case in cases:
        geometry = events.get(case['city_objectid'])
        area = None
        if geometry is not None:
            area = {
                'total': geometry.area,
                'inside_discovery': geometry.intersection(city).area,
                'outside_discovery': geometry.difference(city).area,
                'inside_tiger': {vintage: geometry.intersection(g).area for vintage, g in census.items()},
            }
        date_lookup = None
        if case['disposition'] in ('apply', 'bounded'):
            date_lookup = classify(dated_state(case, first), dated_state(case, second))
        areas.append({'city_objectid': case['city_objectid'], 'ordinance': case['ordinance'],
                      'date_lookup': date_lookup, 'area_m2': area})
    return areas


def build(first=None, second=None):
    ledger, city, counties, census, events, expected, t01_sha256 = load_inputs()
    t01 = t01_windows(t01_sha256)
    default_first = (t01['park', 2023][0], t01['west', 2023][0])
    default_second = (t01['park', 2025][0], t01['west', 2025][0])
    first, second = first or default_first, second or default_second
    valid_from = date.fromisoformat(ledger['valid_from'])
    valid_through = date.fromisoformat(ledger['valid_through'])
    if not valid_from <= first[0] <= first[1] < second[0] <= second[1] <= valid_through:
        raise ValueError('Use ordered, nonoverlapping date ranges within the evidence period')

    cases = [(case, events[case['city_objectid']]) for case in ledger['cases']
             if case['disposition'] != 'context_only' and events.get(case['city_objectid']) is not None]
    domain, parts = partition(city, census, cases, first, second)
    discovery = validate_partition(city, counties, domain, parts, expected)
    features = []
    scopes = {'discovery': {}, 'outside_discovery': {}}
    for label, geometry in parts.items():
        for scope, piece in (('discovery', geometry.intersection(city)),
                             ('outside_discovery', geometry.difference(city))):
            piece = polygonal(piece)
            if piece.area < 1e-6:
                piece = GeometryCollection()
            scopes[scope][label] = county_areas(piece, counties)
            if piece.area:
                if not piece.is_valid:
                    raise ValueError(f'Invalid output geometry: {scope}, {label}')
                lonlat = polygonal(make_valid(reproject(piece, 'EPSG:5070', 'OGC:CRS84')))
                features.append({
                    'type': 'Feature',
                    'properties': {'scope': scope, 'membership': label, 'evidence_version': ledger['version']},
                    'geometry': mapping(orient_polygons(lonlat)),
                })
    tolerance = expected['tolerance_m2']
    for county, area in discovery.items():
        if abs(sum(row[county] for row in scopes['discovery'].values()) - area) > tolerance:
            raise ValueError(f'Discovery classifications do not reconcile for {county}')
    windows = {}
    if (first, second) == (default_first, default_second):
        for (site, year), (_, window) in t01.items():
            windows[f'{site}-{year}'] = {
                'total': window.area,
                'inside_both': window.intersection(parts['inside_both']).area,
            }
    comparisons = {}
    previous = None
    for vintage, geometry in census.items():
        comparisons[vintage] = {
            'area': geometry.area,
            'outside_discovery': geometry.difference(city).area,
            'discovery_outside_tiger': city.difference(geometry).area,
        }
        if previous is not None:
            comparisons[vintage].update(
                added_since_previous=geometry.difference(previous).area,
                removed_since_previous=previous.difference(geometry).area,
            )
        previous = geometry
    observation = {
        'evidence_version': ledger['version'],
        'first': [day.isoformat() for day in first],
        'second': [day.isoformat() for day in second],
    }
    report = {
        **observation,
        'area_crs': expected['crs'],
        'reconciliation_tolerance_m2': tolerance,
        'discovery_m2': discovery,
        'membership_m2': scopes,
        'total_historical_extent_outside_discovery_m2': None,
        'census_comparison_m2': comparisons,
        'change_geometry': event_areas(ledger['cases'], events, city, census, first, second),
        't01_windows_m2': windows,
    }
    return {'type': 'FeatureCollection', **observation, 'features': features}, report


def main():
    parser = argparse.ArgumentParser(description='Replay T07 historical membership evidence.')
    parser.add_argument('output_directory', type=Path)
    parser.add_argument('--first', nargs=2, type=date.fromisoformat, metavar=('EARLIEST', 'LATEST'))
    parser.add_argument('--second', nargs=2, type=date.fromisoformat, metavar=('EARLIEST', 'LATEST'))
    args = parser.parse_args()
    layer, report = build(args.first, args.second)
    args.output_directory.mkdir(parents=True, exist_ok=True)
    (args.output_directory / 'membership.geojson.gz').write_bytes(gzip.compress(
        (json.dumps(layer, separators=(',', ':')) + '\n').encode(), mtime=0))
    (args.output_directory / 'areas.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()

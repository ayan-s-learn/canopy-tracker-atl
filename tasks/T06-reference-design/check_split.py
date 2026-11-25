import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlsplit

from pyproj import Transformer
from shapely import orient_polygons, segmentize, transform, union_all
from shapely.geometry import box, mapping, shape

ROOT = Path(__file__).resolve().parent
INPUTS = json.loads((ROOT / 'inputs.json').read_text())
LONLAT = 'OGC:CRS84'
PROJECTION = 'EPSG:26916'
BUFFER_M = 600
BLOCK_M = 960
STRIDE_M = 1560
GRID_ORIGIN = (727200, 3727200)
CELL_M = 120
FULTON_BLOCKS = 36


def project(geometry, source, target):
    convert = Transformer.from_crs(source, target, always_xy=True)
    return transform(geometry, convert.transform, interleaved=False)


def load_source(name):
    revision, relative, expected = INPUTS['sources'][name]
    raw = (ROOT.parent / relative).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f'{relative} differs from {revision}. Review and version the split again.')
    return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)


def gt_windows(manifest):
    gt = manifest['georgia_tech']
    raster = gt['canopy_2023_download']
    window = INPUTS['gt_window']
    if raster['raster_sha256'] != window['raster_sha256'] or raster['raster_crs'] != PROJECTION:
        raise ValueError('Unexpected GT raster')
    col, row, width, height = raster['window_col_row_width_height']
    a, b, c, d, e, f = window['transform']
    if b or d or not (a > 0 and e < 0):
        raise ValueError('Expected a north-up GT raster')
    yield 'gt-2023-raster-window', box(c + a * col, f + e * (row + height),
                                      c + a * (col + width), f + e * row)

    scheme = INPUTS['gt_tile_scheme']
    ox, oy = scheme['origin']
    span = scheme['resolution'] * scheme['tile_pixels']
    for year in (2018, 2023):
        url = gt[f'rendered_{year}_tile']['query_url']
        level, row, col = map(int, urlsplit(url).path.split('/')[-3:])
        if level != scheme['level']:
            raise ValueError('GT tile level does not match the saved cache grid')
        tile = box(ox + col * span, oy - (row + 1) * span,
                   ox + (col + 1) * span, oy - row * span)
        yield f'gt-{year}-rendered-tile', project(segmentize(tile, 20), scheme['crs'], PROJECTION)

    cell = INPUTS['gt_grid_cell']
    sample = gt['grid_sample']
    if (sample['attributes']['OBJECTID'] != cell['oid']
            or sample['sha256'] != cell['response_sha256']):
        raise ValueError('Unexpected GT grid cell')
    bounds = segmentize(box(*cell['bounds_crs84']), 0.0002)
    yield 'gt-aggregate-grid-cell', project(bounds, LONLAT, PROJECTION)


def development_windows():
    reservations = load_source('reservations')
    windows = {}
    for feature in reservations['features']:
        props = feature['properties']
        reserved = project(shape(feature['geometry']), LONLAT, PROJECTION)
        native = box(*props['bbox_epsg26916'])
        if not reserved.covers(native):
            raise ValueError(f"Reservation does not cover {props['site']}")
        windows[props['site']] = (reserved, props['tiles'])

    later_reads = load_source('reads')
    if not later_reads['reservation_commit'].startswith(INPUTS['sources']['reservations'][0]):
        raise ValueError('T05 read ledger uses a different reservation')
    reads = load_source('t01')['samples'] + later_reads['samples']
    expected = sorted((site, year) for site in windows for year in (2023, 2025))
    if sorted((read['site'], read['year']) for read in reads) != expected:
        raise ValueError('Every reserved window needs both documented reads')
    for read in reads:
        reserved, tiles = windows[read['site']]
        if (read['crs'] != PROJECTION or not reserved.covers(box(*read['bbox']))
                or read['attributes']['Name'] != tiles[(read['year'] == 2025)]):
            raise ValueError(f"Unreconciled read at {read['site']}")
    return {f'naip-{site}': geom for site, (geom, _) in windows.items()}


def candidate_blocks(paired, city, exclusion):
    xmin, ymin, xmax, ymax = city.bounds
    ox, oy = GRID_ORIGIN
    west = ox + math.floor((xmin - ox) / STRIDE_M) * STRIDE_M
    south = oy + math.floor((ymin - oy) / STRIDE_M) * STRIDE_M
    choices = {county: {} for county in paired}
    for x in range(west, math.ceil(xmax), STRIDE_M):
        for y in range(south, math.ceil(ymax), STRIDE_M):
            block = box(x, y, x + BLOCK_M, y + BLOCK_M)
            if not city.covers(block) or not exclusion.disjoint(block):
                continue
            for county, coverage in paired.items():
                if coverage.covers(block):
                    choices[county][x, y] = block
                    break

    selected = list(choices['DeKalb'])
    fulton = choices['Fulton'].copy()
    if not selected or len(fulton) < FULTON_BLOCKS:
        raise ValueError('Insufficient metadata candidates for the proposed split')
    for _ in range(FULTON_BLOCKS):
        point = max(sorted(fulton), key=lambda pt: min(math.dist(pt, p) for p in selected))
        selected.append(point)
        fulton.pop(point)
    for x, y in selected:
        county = 'DeKalb' if (x, y) in choices['DeKalb'] else 'Fulton'
        yield f'{x}-{y}', county, choices[county][x, y], box(
            x + CELL_M, y + CELL_M, x + BLOCK_M - CELL_M, y + BLOCK_M - CELL_M
        )


def export_feature(kind, name, geometry, **properties):
    display = orient_polygons(project(segmentize(geometry, 40), PROJECTION, LONLAT))
    return {'type': 'Feature', 'id': name, 'geometry': mapping(display),
            'properties': {'kind': kind, **properties}}


def validate(features, city, paired):
    def layers(kind):
        for feature in features:
            if feature['properties']['kind'] == kind:
                geom = project(shape(feature['geometry']), LONLAT, PROJECTION)
                if geom.is_empty or not geom.is_valid:
                    raise ValueError(f"Invalid geometry: {feature['id']}")
                yield feature, geom

    development = union_all([g for _, g in layers('development')])
    _, exclusion = next(layers('buffered_development'))
    contexts = {f['properties']['block']: (f['properties']['county'], g)
                for f, g in layers('candidate_context')}
    cores = {f['properties']['block']: g for f, g in layers('candidate_holdout')}
    if contexts.keys() != cores.keys() or not exclusion.covers(development):
        raise ValueError('Incomplete candidate layers or development buffer')
    stats = {}
    for county in paired:
        ids = [name for name, (zone, _) in contexts.items() if zone == county]
        if not ids:
            raise ValueError(f'Candidate blocks are missing in {county}')
        stats[county] = {
            'blocks': len(ids), 'cells_before_QC': len(ids) * (BLOCK_M // CELL_M - 2)**2,
            'candidate_km2_utm': round(sum(cores[name].area for name in ids) / 1e6, 4),
        }
    for name, (county, context) in contexts.items():
        if (not city.covers(context) or not paired[county].covers(context)
                or not context.covers(cores[name]) or not exclusion.disjoint(context)
                or development.distance(context) <= BUFFER_M):
            raise ValueError(f'Candidate {name} violates City, coverage, context or separation')
    contexts_by_block = list(contexts.items())
    for i, (name, (_, context)) in enumerate(contexts_by_block):
        if any(not context.disjoint(g) for _, (_, g) in contexts_by_block[i + 1:]):
            raise ValueError(f'Overlapping context at {name}')

    context_union = union_all([g for _, g in contexts.values()])
    return {'version': INPUTS['version'], 'analysis_crs': PROJECTION, 'geojson_crs': LONLAT,
            'minimum_development_distance_m': round(development.distance(context_union), 2),
            'buffer_context_disjoint': exclusion.disjoint(context_union),
            'buffer_context_intersection_m2': exclusion.intersection(context_union).area,
            'buffer_context_distance_m': round(exclusion.distance(context_union), 2),
            'development_union_km2_utm': round(development.area / 1e6, 5),
            'buffered_development_km2_utm': round(exclusion.area / 1e6, 5),
            'by_county': stats}


def build():
    city_feature, = load_source('city')['features']
    city = project(shape(city_feature['geometry']), LONLAT, PROJECTION)
    coverage = load_source('coverage')
    paired = {
        f['properties']['zone']: project(shape(f['geometry']), LONLAT, PROJECTION)
        for f in coverage['features']
        if f['properties']['coverage'] == 'both' and f['properties']['zone'] in ('Fulton', 'DeKalb')
    }
    if set(paired) != {'Fulton', 'DeKalb'}:
        raise ValueError('Catalog overlap must include both City county portions')
    development = development_windows() | dict(gt_windows(load_source('t02')))
    # Add 1 m so the polygonal approximation and export cannot erode the 600 m guard.
    exclusion = union_all(list(development.values())).buffer(BUFFER_M + 1, quad_segs=32)
    features = [export_feature('development', name, geom) for name, geom in development.items()]
    features.append(export_feature('buffered_development', 'development-plus-buffer', exclusion,
                                   minimum_buffer_m=BUFFER_M))
    for name, county, context, core in candidate_blocks(paired, city, exclusion):
        for kind, geom in (('candidate_context', context), ('candidate_holdout', core)):
            features.append(export_feature(kind, f'{kind}-{name}', geom, block=name,
                                           county=county, bbox_epsg26916=geom.bounds))
    return {'type': 'FeatureCollection', 'version': INPUTS['version'], 'features': features}, city, paired


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path, help='Directory for regenerated artifacts')
    args = parser.parse_args()
    split, city, paired = build()
    version = json.dumps(split['version'])
    rows = ',\n'.join(json.dumps(f, separators=(',', ':')) for f in split['features'])
    split_text = f'{{"type":"FeatureCollection","version":{version},"features":[\n{rows}\n]}}\n'
    checks = validate(json.loads(split_text)['features'], city, paired)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'split.geojson').write_text(split_text)
    (args.output / 'split-check.json').write_text(json.dumps(checks, indent=2) + '\n')


if __name__ == '__main__':
    main()

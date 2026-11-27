"""Build the offline T09 reader packet from verified, previously read windows."""

import argparse
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

import numpy as np

ROOT = Path(__file__).resolve().parent
T01 = ROOT.parent / 'T01-imagery'
T05 = ROOT.parent / 'T05-paired-coverage'
T06 = ROOT.parent / 'T06-reference-design'
sys.path.insert(0, str(T05))
from check_windows import verify  # noqa: E402

YEARS = ('2023', '2025')
LAYERS = ('crown_2023', 'unknown_2023', 'crown_2025', 'unknown_2025', 'unknown_change', 'loss')
SCALE = 0.6
CORE = 200
# Fixed offsets are in 0.6 m parent pixels. The small-site cores overlap by design.
CROPS = {
    'park': ((0, 0), (12, 12)),
    'west': ((12, 0), (0, 12)),
    'kirkwood': ((0, 0), (192, 192)),
    'west-fulton': ((192, 0), (0, 192)),
}
# Interleave site mates and fixtures without encoding origin in the case ID.
ORDER = (4, 9, 0, 6, 3, 8, 5, 10, 2, 11, 7, 1)
READER_FILES = ('viewer.html', 'viewer.js', 'reader-guide.txt')


def read_json(path):
    return json.loads(path.read_bytes())


def dump_json(value):
    return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True, allow_nan=False) + '\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    return digest(path.read_bytes())


def write_assignment(path, assignment):
    path.write_text('const ASSIGNMENT = ' + dump_json(assignment).rstrip() + ';\n', encoding='utf-8')


def png(rgb):
    _, height, width = rgb.shape

    def chunk(name, data):
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data))

    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    rows = b''.join(b'\x00' + row.tobytes() for row in rgb.transpose(1, 2, 0))
    # Uncompressed DEFLATE keeps the file bytes independent of compressor tuning and release.
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IDAT', zlib.compress(rows, 0)) + chunk(b'IEND', b'')


def nominal_late(pixels):
    bands, height, width = pixels.shape
    groups = pixels.reshape(bands, height // 2, 2, width // 2, 2)
    return ((groups.sum(axis=(2, 4), dtype=np.uint16) + 2) // 4).astype(np.uint8)


def context(size):
    pad = (size - CORE) // 2
    return [pad, pad, pad + CORE, pad + CORE]


def real_pairs(old, new):
    from shapely.geometry import box

    reservations = {
        f['properties']['site']: f['properties']
        for f in read_json(T05 / 'development-windows.geojson')['features']
    }
    protected = [
        box(*f['properties']['bbox_epsg26916'])
        for f in read_json(T06 / 'split.geojson')['features'] if f['properties']['kind'] == 'candidate_context'
    ]
    if len(protected) != 40:
        raise ValueError('Expected the 40 pinned T06 protected context blocks')
    offsets = read_json(T05 / 'alignment.json')
    samples = read_json(T01 / 't01-windows.json')['samples'] + read_json(T05 / 'window-evidence.json')['samples']
    for site, corners in CROPS.items():
        pair = sorted((s for s in samples if s['site'] == site), key=lambda s: s['year'])
        reservation = reservations[site]
        bounds = reservation['bbox_epsg26916']
        if any(box(*bounds).distance(block) <= 600.001 for block in protected):
            raise ValueError(f'{site} read intersects the T06 protected context or guard')
        pixels, sources, dates = [], [], []
        for i, (sample, year, tile) in enumerate(zip(pair, YEARS, reservation['tiles'], strict=True)):
            attrs = sample['attributes']
            if (attrs['Name'] != tile or str(sample['year']) != year or sample['crs'] != 'EPSG:26916'
                    or not np.allclose(sample['bbox'], bounds, atol=1e-6, rtol=0)):
                raise ValueError(f'{site} input differs from its reserved read')
            cache = old if site in ('park', 'west') else new
            data = (cache / f'{site}-{year}.tif').read_bytes()
            native = verify(data, sample)
            expected_size = round((bounds[2] - bounds[0]) / SCALE) * (i + 1)
            if native.shape != (4, expected_size, expected_size):
                raise ValueError(f'{site} has an unexpected source pixel scale')
            pixels.append(native if i == 0 else nominal_late(native))
            date_key = 'acquisition_date' if i == 0 else 'QQDATE'
            dates.append(datetime.fromtimestamp(attrs[date_key] / 1000, UTC).date().isoformat())
            sources.append(dict(tile=tile, acquired=dates[-1], grid_bbox_epsg26916=sample['bbox'],
                                shape=sample['size'], pixel_m=SCALE / (i + 1),
                                sha256_pixels=sample['sha256_pixels_band_major'],
                                sha256_masks=sample.get('sha256_masks_band_major', 'all-valid'),
                                recorded_tiff_sha256=sample['sha256_tiff']))
        hits = [a['magnitude_m'] for a in offsets[site] if a['passes_screen']]
        registration = 'Nominal grid. Local displacement is unresolved.'
        if len(hits) == 1:
            registration += f' One screened feature showed a {hits[0]:g} m offset.'
        elif hits:
            registration += f' Window checks passed at {len(hits)} features (offsets {min(hits):g}–{max(hits):g} m).'
        else:
            registration += ' No window check passed the screening rule.'
        if site in ('west', 'west-fulton'):
            registration += ' The parent window includes mapped same-day seams in 2025.'
        size = 244 if pixels[0].shape[1] == 256 else 320
        for col, row in corners:
            if col + size > pixels[0].shape[2] or row + size > pixels[0].shape[1]:
                raise ValueError(f'{site} crop exceeds the recorded read')
            origin = [round(bounds[0] + col * SCALE, 6), round(bounds[3] - row * SCALE, 6)]
            yield (
                [image[:, row:row + size, col:col + size] for image in pixels],
                dict(dates=dates, size=size, core=context(size), registration=registration),
                dict(site=site, crop_in_parent_px=[col, row, size, size],
                     affine_epsg26916=[SCALE, 0, origin[0], 0, -SCALE, origin[1]], sources=sources,
                     screened_parent_offsets_m=hits, additional_shift_m=[0, 0]),
            )


def synthetic_pairs():
    size = 244
    y, x = np.indices((size, size))
    rng = np.random.default_rng(9206)
    # Crown centres and patch placement vary; labels stay in the owner ledger.
    designs = (
        ('stable', [(68, 68), (134, 99), (88, 165)], [], False),
        ('interior visible change', [(51, 72), (146, 115), (108, 174)], [1], False),
        ('shadow makes transition unknown', [(52, 59), (128, 130), (171, 168)], [], True),
        ('loss reaches crop boundary', [(7, 119), (88, 65), (159, 172)], [0], False),
    )
    for label, centers, removed, shadow in designs:
        texture = (3 * np.sin(x / 9) + 4 * np.cos(y / 12) + rng.integers(-8, 9, (size, size))).astype(np.int16)
        path = abs(y - 0.45 * x - 110) < 5
        background = np.array([125, 144, 108, 156])[:, None, None] + texture
        background[:, path] = np.array([170, 167, 154, 116])[:, None] + texture[path]
        early, late = background.copy(), background.copy() + 3
        for i, (cx, cy) in enumerate(centers):
            angle = np.arctan2(y - cy, x - cx)
            radius = 28 + 3 * np.cos(5 * angle) + 2 * np.sin(7 * angle)
            crown = np.hypot(x - cx, (y - cy) * 0.94) < radius
            early[:, crown] = np.array([48, 92, 46, 185])[:, None] + texture[crown]
            color = [157, 133, 113, 114] if i in removed else [52, 95, 51, 186]
            late[:, crown] = np.array(color)[:, None] + texture[crown]
        if shadow:
            patch = (x > 92) & (x + y > 202) & (x + y < 288) & (y < 175)
            late[:, patch] = late[:, patch] // 9
        yield (
            [early.astype(np.uint8), late.astype(np.uint8)],
            dict(dates=['2023-10-08', '2025-10-11'], size=size, core=context(size),
                 registration='Both observations share the nominal grid.'),
            dict(fixture=label),
        )


def blank_case(case_id):
    return dict(id=case_id, status='pending', confidence=None, reason='', crop_cutoff=False,
                active_minutes=None, masks={layer: [] for layer in LAYERS})


def build(output, t01, t05):
    pairs = list(real_pairs(t01, t05)) + list(synthetic_pairs())
    output.mkdir(mode=0o700)
    reader = output / 'reader'
    reader.mkdir()
    for name in READER_FILES:
        shutil.copyfile(ROOT / name, reader / name)
    public, private = [], {}
    for ordinal, index in enumerate(ORDER, 1):
        case_id = f'C{ordinal:02d}'
        images, info, lineage = pairs[index]
        public.append(dict(id=case_id, **info))
        private[case_id] = lineage
        for year, spectral in zip(YEARS, images, strict=True):
            for view, bands in (('rgb', [0, 1, 2]), ('nir', [3, 0, 1])):
                (reader / f'{case_id}-{year}-{view}.png').write_bytes(png(spectral[bands]))
    files = {path.name: file_hash(path) for path in sorted(reader.iterdir())}
    blank = dict(role='reader', code='', cases=[blank_case(c['id']) for c in public])
    packet = digest(dump_json(dict(cases=public, scale_m=SCALE, files=files, blank=blank)).encode())
    blank['packet'] = packet
    assignment = dict(packet=packet, scale_m=SCALE, cases=public, blank=blank)
    write_assignment(reader / 'assignment.js', assignment)
    (reader / 'blank-return.json').write_text(dump_json(blank))
    files.update({name: file_hash(reader / name) for name in ('assignment.js', 'blank-return.json')})
    ledger = dict(packet=packet, assignment=assignment, files_sha256=files, lineage=private)
    (output / 'owner-ledger.json').write_text(dump_json(ledger))
    return ledger


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='New private directory')
    parser.add_argument('t01', type=Path, help='Verified T01 TIFF directory')
    parser.add_argument('t05', type=Path, help='Verified T05 TIFF directory')
    args = parser.parse_args()
    print(build(args.output, args.t01, args.t05)['packet'])

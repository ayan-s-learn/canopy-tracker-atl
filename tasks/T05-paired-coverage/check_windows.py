import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

ROOT = Path(__file__).resolve().parent
T01 = ROOT.parent / 'T01-imagery'
SEARCH_PIXELS = 6


def fetch(url):
    return subprocess.check_output([
        'curl', '--fail', '--silent', '--show-error', '--location', '--max-time', '90',
        '--retry', '1', '--max-filesize', '8388608', url,
    ])


def verify(data, sample):
    with MemoryFile(data) as mem, mem.open() as ds:
        pixels = ds.read()
        masks = ds.read_masks()
        expected = from_bounds(*sample['bbox'], *sample['size'])
        if (ds.crs != sample['crs'] or [ds.width, ds.height] != sample['size']
                or not ds.transform.almost_equals(expected, precision=1e-6)
                or ds.count != 4 or ds.dtypes != (sample['dtype'],) * 4
                or ds.nodata != sample['nodata']
                or [[flag.name for flag in flags] for flags in ds.mask_flag_enums] != sample['mask_flags']):
            raise ValueError(f"Unexpected grid, bands or mask flags for {sample['attributes']['Name']}")
        if hashlib.sha256(pixels.tobytes()).hexdigest() != sample['sha256_pixels_band_major']:
            raise ValueError(f"Changed pixels for {sample['attributes']['Name']}")
        if 'sha256_masks_band_major' in sample:
            if hashlib.sha256(masks.tobytes()).hexdigest() != sample['sha256_masks_band_major']:
                raise ValueError(f"Changed mask for {sample['attributes']['Name']}")
        elif not np.all(masks == 255):
            raise ValueError(f"Unexpected invalid T01 pixels for {sample['attributes']['Name']}")
        return pixels


def gradients(pixels, year):
    rgb = pixels[:3].mean(axis=0)
    if year == 2025:
        height, width = rgb.shape
        rgb = rgb.reshape(height // 2, 2, width // 2, 2).mean(axis=(1, 3))
    # The two sensors have different edge sharpness even at the same pixel size.
    kernel = np.array([1, 4, 6, 4, 1]) / 16
    for axis in (0, 1):
        rgb = np.apply_along_axis(lambda line: np.convolve(line, kernel, mode='same'), axis, rgb)
    return np.stack(np.gradient(rgb))


def unit(crop):
    centered = crop - crop.mean(axis=(1, 2), keepdims=True)
    norm = np.linalg.norm(centered)
    return centered / norm if norm else centered


def align(early, late, anchor):
    col, row = anchor['pixel_xy']
    half = anchor['half_size']
    radius = SEARCH_PIXELS
    if not (radius + half <= col < early.shape[2] - radius - half
            and radius + half <= row < early.shape[1] - radius - half and early.shape == late.shape):
        raise ValueError('Alignment chip or search extends outside its paired window')
    a = unit(early[:, row-half:row+half+1, col-half:col+half+1])
    scores = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            r, c = row + dy, col + dx
            b = unit(late[:, r-half:r+half+1, c-half:c+half+1])
            scores.append((float((a * b).sum()), dx, dy))
    score, dx, dy = max(scores)
    alternative = max(s for s, x, y in scores if max(abs(x - dx), abs(y - dy)) > 1)
    return {
        **anchor, 'east_m': round(dx * .6, 2), 'north_m': round(-dy * .6, 2),
        'magnitude_m': round(float(np.hypot(dx, dy)) * .6, 2), 'score': round(score, 3),
        'runner_up_gap': round(score - alternative, 3),
        'passes_screen': score >= .65 and score - alternative >= .02 and max(abs(dx), abs(dy)) < radius,
    }


def main():
    parser = argparse.ArgumentParser(description='Verify local T05 pairs and replay stable-feature measurements.')
    parser.add_argument('t05_cache', type=Path)
    parser.add_argument('t01_cache', type=Path)
    parser.add_argument('--retrieve', action='store_true', help='Fetch fresh copies of both new pairs')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'window-evidence.json').read_text())
    old_samples = json.loads((T01 / 't01-windows.json').read_text())['samples']
    new_samples = manifest['samples']
    products = {}
    new_sites = {sample['site'] for sample in new_samples}
    for sample in old_samples + new_samples:
        site, year = sample['site'], sample['year']
        is_new = site in new_sites
        path = (args.t05_cache if is_new else args.t01_cache) / f'{site}-{year}.tif'
        if args.retrieve and is_new and not path.exists():
            live = json.loads(fetch(sample['item_url']))['attributes']
            date_field = 'acquisition_date' if year == 2023 else 'QQDATE'
            if any(live[key] != sample['attributes'][key] for key in ('OBJECTID', 'Name', date_field)):
                raise ValueError(f'Live item identity/date changed for {path.name}')
            data = fetch(sample['url'])
            pixels = verify(data, sample)
            path.parent.mkdir(parents=True, exist_ok=True)
            with TemporaryDirectory(dir=path.parent) as staging:
                staged = Path(staging) / path.name
                staged.write_bytes(data)
                path.hardlink_to(staged)
            same_tiff = hashlib.sha256(data).hexdigest() == sample['sha256_tiff']
            print(f'{path.name} retrieved and verified, byte-identical={same_tiff}', file=sys.stderr)
        else:
            pixels = verify(path.read_bytes(), sample)
        products[site, year] = gradients(pixels, year)
    measurements = {
        site: [align(products[site, 2023], products[site, 2025], anchor) for anchor in anchors]
        for site, anchors in manifest['alignment_anchors'].items()
    }
    print(json.dumps(measurements, indent=2))


if __name__ == '__main__':
    main()

"""Retrieve the four T01 development windows from the recorded public services."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from rasterio.io import MemoryFile
from rasterio.transform import from_bounds


def verify_window(data, sample):
    with MemoryFile(data) as mem, mem.open() as image:
        transform = from_bounds(*sample["bbox"], *sample["size"])
        if (image.crs != sample["crs"] or [image.width, image.height] != sample["size"]
                or not image.transform.almost_equals(transform, precision=1e-6)
                or image.dtypes != (sample["dtype"],) * 4 or image.nodata != sample["nodata"]
                or [[flag.name for flag in flags] for flags in image.mask_flag_enums]
                != sample["mask_flags"]):
            raise ValueError(f"Grid, bands or mask changed for {sample['attributes']['Name']}")
        if hashlib.sha256(image.read().tobytes()).hexdigest() != sample["sha256_pixels_band_major"]:
            raise ValueError(f"Pixel content changed for {sample['attributes']['Name']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Directory for verified GeoTIFFs (rerun to resume)")
    args = parser.parse_args()
    manifest = Path(__file__).with_name("t01-windows.json")
    samples = json.loads(manifest.read_text())["samples"]
    args.output.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        recover(sample, args.output)


def recover(sample, directory):
    path = directory / f"{sample['site']}-{sample['year']}.tif"
    if path.exists():
        data = path.read_bytes()
        same_file = hashlib.sha256(data).hexdigest() == sample["sha256_tiff"]
        if not same_file:
            verify_window(data, sample)
        print(f"{path.name}  existing TIFF verified  identical TIFF bytes={same_file}", flush=True)
        return
    # A service object ID can be reused after an imagery refresh.
    item = json.loads(fetch(sample["item_url"]))
    if item["attributes"]["Name"] != sample["attributes"]["Name"]:
        raise ValueError(f"Tile identity changed at {sample['item_url']}")
    data = fetch(sample["url"])
    verify_window(data, sample)
    # An interrupted write must not leave a partial TIFF at the resume path.
    with TemporaryDirectory(dir=directory) as staging:
        staged = Path(staging) / path.name
        staged.write_bytes(data)
        path.hardlink_to(staged)
    same_file = hashlib.sha256(data).hexdigest() == sample["sha256_tiff"]
    print(f"{path.name}  pixels verified  identical TIFF bytes={same_file}", flush=True)


def fetch(url):
    return subprocess.check_output([
        "curl", "--fail", "--silent", "--show-error", "--location",
        "--max-time", "90", "--retry", "1", "--max-filesize", "8388608", url,
    ])


if __name__ == "__main__":
    main()

"""Retrieve the four T01 development windows from the recorded public services."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import rasterio
from rasterio.io import MemoryFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Directory for verified GeoTIFFs (rerun to resume)")
    args = parser.parse_args()
    manifest = Path(__file__).resolve().parents[3] / "manifests/imagery/t01-windows.json"
    samples = json.loads(manifest.read_text())["samples"]
    args.output.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        path = args.output / f"{sample['site']}-{sample['year']}.tif"
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != sample["sha256_tiff"]:
                raise ValueError(f"Existing file differs from the archived TIFF: {path}")
            print(f"{path.name}  existing TIFF verified", flush=True)
            continue
        # A service object ID can be reused after an imagery refresh.
        item = json.loads(fetch(sample["item_url"]))
        if item["attributes"]["Name"] != sample["attributes"]["Name"]:
            raise ValueError(f"Tile identity changed at {sample['item_url']}")
        data = fetch(sample["url"])
        with MemoryFile(data) as mem, mem.open() as image:
            if (image.crs.to_string() != sample["crs"]
                    or [image.width, image.height] != sample["size"]
                    or not np.allclose(image.bounds, sample["bbox"], rtol=0, atol=1e-6)
                    or image.count != 4 or image.nodata != sample["nodata"]):
                raise ValueError(f"Grid, bands or nodata changed for {item['attributes']['Name']}")
            digest = hashlib.sha256(image.read().tobytes()).hexdigest()
        if digest != sample["sha256_pixels_band_major"]:
            raise ValueError(f"Pixel content changed for {item['attributes']['Name']}")
        with path.open("xb") as out:
            out.write(data)
        same_file = hashlib.sha256(data).hexdigest() == sample["sha256_tiff"]
        print(f"{path.name}  pixels verified  identical TIFF bytes={same_file}", flush=True)


def fetch(url):
    return subprocess.check_output([
        "curl", "--fail", "--silent", "--show-error", "--location",
        "--max-time", "90", "--retry", "1", "--max-filesize", "8388608", url,
    ])


if __name__ == "__main__":
    main()

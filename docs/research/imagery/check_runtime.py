"""Reproduce a 16 × 16 mean near-infrared raster from the T01 park fixture."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

from recover_windows import verify_window


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, help="Verified T01 park-2023.tif")
    parser.add_argument("output", type=Path, help="New output GeoTIFF path")
    args = parser.parse_args()

    manifest = Path(__file__).resolve().parents[3] / "manifests/imagery/t01-windows.json"
    sample = next(
        sample for sample in json.loads(manifest.read_text())["samples"]
        if (sample["site"], sample["year"]) == ("park", 2023)
    )
    fixture = args.fixture.read_bytes()
    if hashlib.sha256(fixture).hexdigest() != sample["sha256_tiff"]:
        verify_window(fixture, sample)

    with MemoryFile(fixture) as memory, memory.open() as source:
        means = source.read(4).reshape(16, 16, 16, 16).mean(axis=(1, 3), dtype=np.float32)
        transform = source.transform * rasterio.Affine.scale(16)
        crs = source.crs

    with MemoryFile() as memory:
        with memory.open(
            driver="GTiff", width=16, height=16, count=1, dtype="float32",
            crs=crs, transform=transform,
        ) as output:
            output.write(means, 1)
            output.set_band_description(1, "Mean near-infrared digital number")

        with memory.open() as output:
            expected_transform = from_bounds(*sample["bbox"], 16, 16)
            if (output.shape != (16, 16) or output.count != 1
                    or output.dtypes != ("float32",) or output.nodata is not None
                    or output.crs.to_string() != sample["crs"]
                    or not output.transform.almost_equals(expected_transform, precision=1e-6)):
                raise ValueError("Output GeoTIFF grid or band layout differs from the reference")

            digest = hashlib.sha256(output.read(1).astype("<f4").tobytes()).hexdigest()
            if digest != "5922297bece275f7bc3d91fb53167aab0fc1cef0429cf59755dd9922d249bdef":
                raise ValueError(f"Output pixels differ from the reference: {digest}")

        with args.output.open("xb") as output_file:
            output_file.write(memory.read())
    print(f"Verified 256 means and EPSG:26916 grid; pixel SHA-256 {digest}")


if __name__ == "__main__":
    main()

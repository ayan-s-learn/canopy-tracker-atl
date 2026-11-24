# T04 — Runtime and artifact recovery

## Brief

- **Objective:** show how a successor can reproduce a real small geospatial operation and recover its artifacts. Input: the [T01 Piedmont Park 2023 window](../T01-imagery/README.md).
- **Expected outputs:** demonstrated environment and fixture reproduction; an authorized storage round trip; recovery, retention and permission limits; a concrete storage action if the missing capability needs a human.
- **Acceptance:** open and process a real permitted raster from a fresh directory using recorded versions; verify output tolerance; copy, retrieve and hash-check a real artifact from the authorized durable path. Document disconnect, crash, reboot and deletion survival honestly; a local file or checksum alone does not establish durability. Do not deliberately restart the host to test it.
- **Limits:** 100 MiB of wheel and fixture transfers, 500 MiB of temporary space, one GitHub working branch, no paid provisioning. Shared paths reserved at launch: `requirements.txt`, the operations guide and the T04 checklist entry. Stop at a verified clean replay and remote retrieval, or a recorded blocker with resume steps.

## Result

Codex ran the checks on 2026-11-23 (America/New_York). A fresh environment built from the pinned requirements reproduced the derived near-infrared raster exactly, and a fresh HTTPS clone returned the archived copy with a matching SHA-256. This recovery path covers small shareable derivatives and records only. Before costly acquisitions or training, identify an authorized store for raw imagery and model weights, then verify a separate round trip and record retention and access there.

## Outputs and replay

### Reproduce the geospatial check

From the repository root, use CPython 3.14, curl, and a fresh directory. This ran on arm64 macOS with Python 3.14.7, Rasterio 1.4.4 (GDAL 3.10.3, PROJ 9.7.1), and NumPy 2.3.5. The [requirements file](../../requirements.txt) pins the Python packages, including dependencies. `pip check` passed. The run used about 27 MB of downloads and 136 MiB of temporary space.

```sh
repo=$PWD
run=$(mktemp -d)
python3.14 -m venv "$run/env"
"$run/env/bin/python" -m pip install --only-binary=:all: -r requirements.txt
"$run/env/bin/python" -m pip check
fixture_url=$("$run/env/bin/python" -c 'import json; print(next(s["url"] for s in json.load(open("tasks/T01-imagery/t01-windows.json"))["samples"] if (s["site"], s["year"]) == ("park", 2023)))')
curl --fail --silent --show-error --location --max-time 90 --max-filesize 1048576 \
  "$fixture_url" -o "$run/park-2023.tif"
(cd "$run" && env/bin/python "$repo/tasks/T04-runtime/check_runtime.py" park-2023.tif nir-mean.tif)
```

If the service is unavailable and the original checkout still has the T01 cache, copy `data/imagery/t01/park-2023.tif` into the run directory. The fresh download matched the [T01 input SHA-256](../T01-imagery/t01-windows.json). If the provider repackages the TIFF, the check verifies the recorded grid, bands, masks and pixel hash before using it. The check averages band 4 (near-infrared) in non-overlapping 16 × 16 blocks and writes a 16 × 16 Float32 GeoTIFF with 9.6 m pixels in EPSG:26916. It matched all 256 means exactly against a reference SHA-256 computed with independent row-by-row sums. Each affine coefficient must match the manifest-derived grid within `1e-6`. Rebuilding the TIFF checks its decoded content and grid so changes in TIFF encoding can be distinguished from changed data. NAIP imagery provided by USDA Farm Service Agency.

### Recover the archived GeoTIFF

A fresh HTTPS clone of `cbd607e` returned the 1,874-byte derived GeoTIFF. Its SHA-256 matched the output rebuilt in a fresh environment from the locked wheels. From the integrated branch, repeat with a new destination.

```sh
archive=$(mktemp -d)
git clone --depth=1 --single-branch --branch main \
  https://github.com/ayan-s-learn/canopy-tracker-atl.git "$archive/checkout"
(
  cd "$archive/checkout" || exit
  printf '%s\n' '6665d57d1016d91221278738dc49c296610c19e1052418e3fc0020efb54cf1ad  tasks/T04-runtime/t04-park-2023-nir-mean.tif' | shasum -a 256 -c
)
```

Public HTTPS reads require no repository write access. The pushed copy provides recovery after a local disconnect, crash, reboot, or deletion of local files while a remote ref retains it. Those failures were not induced. Repository deletion or removal of all retaining refs can end recovery.

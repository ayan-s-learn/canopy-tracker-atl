# Operations guide

Read the relevant section **before launching or resuming a job, handing off work, or stopping a session**. These procedures implement [AGENTS.md](../AGENTS.md); use only verified runtime capabilities, and do not assume unattended survival, notifications, usage accounting or automatic restart. [checklist.md](../checklist.md) remains the live state entry point.

## Cloud jobs, recovery, and waiting

Choose a recovery strategy appropriate to the job: rerun cheap deterministic work; checkpoint or back up expensive and irreplaceable work. Reuse tool-native logs and resumability rather than building a runner by default. Keep enough linked information to identify inputs/code, outputs, progress and how to resume or stop; document known survival limits without requiring every failure mode to be tested before useful work.

Choose validation, backup and monitoring frequency based on failure cost and available capabilities. Inspect existing work before restarting; preserve healthy jobs and useful partial results. Events, supported waits or proportionate status checks are all acceptable. Revise estimates and methods as evidence arrives within authorized resource limits; elapsed estimates alone do not require stopping a productive run.

Report completed, pending and failed work honestly; distinguish an ongoing job from a blocker or completion. Do not claim durable recovery without a verified retrieval path. Keep raw rasters, model weights, personal records, secrets and expiring signed URLs out of Git; retain provenance and retrieval instructions.

## Git publication, handoffs, and stopping

Commit at meaningful milestones and before planned stops. Stage explicit paths, inspect the diff, and exclude secrets, unrelated edits, large inputs, and temporary logs. Clearly label incomplete checkpoints and pending checks. Verify the remote contains a pushed checkpoint; report publishing failures with the local commit and recovery action.

At a stop boundary, stop launching new work, preserve partial results, update the checklist and human-action queue, and publish an honest checkpoint. A declared independent job may continue within its recorded authority and resource limits when the host supports it; an explicit instruction to stop that job overrides continuation. Stop only owned processes that should end and retain exact recovery steps. Do not describe a budget stop as successful completion.

Handoffs identify the branch and checkpoint, completed and unfinished work, checks and review status, artifact recovery locations, process ownership, blockers, and exact next actions. On resume, reconcile from those records and actual artifacts.

## T04 — Runtime and artifact recovery

Codex launched T04 on 2026-11-23 from `28643e3` on `codex/t04-reproducible-runtime`, with the environment lock, executable check, derived raster, operations guide, and checklist entry reserved for the task. The [T01 Piedmont Park 2023 window](research/imagery/T01.md) was the input. The launch limited the check to 100 MiB of wheel and fixture transfers, 500 MiB of temporary space, one GitHub working branch, and no paid provisioning. The stopping condition was a verified clean replay and remote retrieval, or a recorded blocker with resume steps.

### Reproduce the geospatial check

From the repository root, use CPython 3.14, curl, and a fresh directory. This ran on arm64 macOS with Python 3.14.7, Rasterio 1.4.4 (GDAL 3.10.3, PROJ 9.7.1), and NumPy 2.3.5. The [requirements file](../requirements.txt) pins the Python packages, including dependencies. `pip check` passed. The run used about 27 MB of downloads and 136 MiB of temporary space.

```sh
repo=$PWD
run=$(mktemp -d)
python3.14 -m venv "$run/env"
"$run/env/bin/python" -m pip install --only-binary=:all: -r requirements.txt
"$run/env/bin/python" -m pip check
fixture_url=$("$run/env/bin/python" -c 'import json; print(next(s["url"] for s in json.load(open("manifests/imagery/t01-windows.json"))["samples"] if (s["site"], s["year"]) == ("park", 2023)))')
curl --fail --silent --show-error --location --max-time 90 --max-filesize 1048576 \
  "$fixture_url" -o "$run/park-2023.tif"
(cd "$run" && env/bin/python "$repo/docs/research/imagery/check_runtime.py" park-2023.tif nir-mean.tif)
```

If the service is unavailable and the original checkout still has the T01 cache, copy `data/imagery/t01/park-2023.tif` into the run directory. The fresh download matched the [T01 input SHA-256](../manifests/imagery/t01-windows.json). If the provider repackages the TIFF, the check verifies the recorded grid, bands, masks and pixel hash before using it. The check averages band 4 (near-infrared) in non-overlapping 16 × 16 blocks and writes a 16 × 16 Float32 GeoTIFF with 9.6 m pixels in EPSG:26916. It matched all 256 means exactly against a reference SHA-256 computed with independent row-by-row sums. Each affine coefficient must match the manifest-derived grid within `1e-6`. Rebuilding the TIFF checks its decoded content and grid so changes in TIFF encoding can be distinguished from changed data. NAIP imagery provided by USDA Farm Service Agency.

### Recover the archived GeoTIFF

A fresh HTTPS clone of `cbd607e` returned the 1,874-byte derived GeoTIFF. Its SHA-256 matched the output rebuilt in a fresh environment from the locked wheels. From the integrated branch, repeat with a new destination.

```sh
archive=$(mktemp -d)
git clone --depth=1 --single-branch --branch main \
  https://github.com/ayan-s-learn/canopy-tracker-atl.git "$archive/checkout"
(
  cd "$archive/checkout" || exit
  printf '%s\n' '6665d57d1016d91221278738dc49c296610c19e1052418e3fc0020efb54cf1ad  docs/research/imagery/t04-park-2023-nir-mean.tif' | shasum -a 256 -c
)
```

Public HTTPS reads require no repository write access. The pushed copy provides recovery after a local disconnect, crash, reboot, or deletion of local files while a remote ref retains it. Those failures were not induced. Repository deletion or removal of all retaining refs can end recovery. This path is for small shareable derivatives and records. Before costly acquisitions or training, identify an authorized store for raw imagery and model weights, then verify a separate round trip and record retention and access there.

# T08 — Can a simple baseline distinguish crown loss from image displacement?

## Brief

Run an end-to-end development baseline on the four [reserved windows](../T05-paired-coverage/development-windows.geojson) at `2ac905e`. Start with the [T01](../T01-imagery/t01-windows.json) and [T05](../T05-paired-coverage/window-evidence.json) manifests. Use the [window recovery and replay commands](../T05-paired-coverage/README.md#outputs-and-replay). Use only the eight recorded rasters and their existing spatial support. Reserve this folder and ignored cache `data/imagery/t08/`.

1. Verify pixels, dates, transforms and masks. Pin one common grid and resampling rule. Record valid and unknown area by site. Reuse the [stable-feature diagnostics](../T05-paired-coverage/alignment.json). Before estimating a shift, set a rule for adequate spatial support and acceptable residuals. Where the T05 controls are sparse or disagree, attempt fresh stable-feature checks within the existing pixels. Keep controls used to fit a shift separate in space from controls used to check it. Report signed residuals in metres and rejected controls. At indexed seams, report supported and uncertain area by side. A chip spanning a seam cannot establish a correction on either side.
2. Run a reproducible, inexpensive rule for crown cover at each date, for example a vegetation index with a local texture cue to distinguish grass. Count 2023 crown becoming known 2025 noncrown as gross loss. Carry unknown at either date separately and form connected events before filtering by area. Exercise the pipeline with a same-epoch no-change pair, a copy shifted by a known offset, and an inserted crown-loss patch of known area. Record expected and observed masks and events. Preserve thresholds, connectivity, subthreshold components, edge truncation, event IDs, geometry, dates and uncertainty reasons. Start with 0.10 acre and show the effect of 0.05 and 0.25 acre. Document failures on grass, shadow and crown edges.
3. Compare the same detector on the common grid before and after any supported correction. Use the same eligible pixels for comparisons and report any area lost at the edges. Where controls support a displacement range, perturb alignment over that range and match individual candidates across shifts with a declared overlap rule. Record retained, lost, new and split/merged IDs as well as counts and area. Where support is insufficient, record the comparison as unresolved and the affected area as registration-uncertain. Report sensitivity to explicitly hypothetical shifts there, without treating those shifts as measured corrections. Inspect paired chips from flagged areas **and** apparently unchanged areas at each site using a recorded selection rule. Include misses, false alarms and ambiguous examples when observed. These are development judgments.
4. Deliver a pinned command, configuration, compact event layer and site table. Reconcile scored, unknown and excluded areas to the native TIFF footprints, excluding the 1 m reservation margin. Replay from verified inputs and compare event IDs, geometry, areas and counts within declared tolerances. Report runtime and storage. Keep imagery out of Git.

Recommend either a controlled challenger on the same inputs, a targeted development read to resolve a named failure, or stopping at the scale the imagery can support. Recommend a challenger only if the controls behave as expected and inspected examples show a detector error on registration-supported area that the challenger could address. Otherwise identify the evidence needed to interpret a change at the proposed scale. A reproducible empty queue or inconclusive result is a valid outcome. Accuracy, citywide coverage and operational yield require independent evidence.

## Progress

Owner: Codex T08, 2026-11-26 17:49 EST. Branch `task/T08-development-baseline` is stacked on AR02 (`c41c8e7`), which contains this brief. Use only the eight cached development rasters, local CPU and this folder plus the reserved ignored cache. No expanded reads.

Before estimating shifts, fix the following support rule. Partition each site by indexed exposure pair. Reuse T05's gradient-match screen. Add visually selected pavement or fixed structures. Require the smoothing, search and chip footprint to lie entirely on one side. Allocate spatially separated fit and check controls before matching. Within each side require at least three non-collinear fit controls and two independent check controls. Fit an integer-grid median translation. Each accepted fit and check residual must be within 1.2 m Euclidean distance. Restrict supported pixels to the fit convex hull on that side. Else abstain. Check sensitivity at offsets of two common-grid pixels in both axes and their diagonals on unresolved area.

Implementation and replay are complete. The documented abstentions meet the AR03 review trigger.

## Result

On 2026-11-26, the four-window baseline found 20 uncorrected candidates at or above 0.10 acre. All 235,929.60 m² of native footprint remain registration-uncertain. The control rule at `9d4755f` admitted no measured correction. Increasing the area floor to 0.25 acre leaves two far-west candidates, both still uncertain.

| Site | TIFF footprint m² | Both dates scored m² | Unknown m² | Common comparison m² | Native candidates ≥0.05 / 0.10 / 0.25 acre | Common-grid ≥0.10 acre, raw → hypothetical range |
|---|---:|---:|---:|---:|---:|---:|
| Piedmont Park | 23,592.96 | 22,861.44 | 731.52 | 22,141.44 | 0 / 0 / 0 | 0 → 0 |
| West End | 23,592.96 | 22,861.44 | 731.52 | 21,258.36 | 1 / 0 / 0 | 0 → 0–1 |
| Kirkwood | 94,371.84 | 92,706.84 | 1,665.00 | 91,253.16 | 20 / 8 / 0 | 8 → 5–10 |
| Far west Atlanta | 94,371.84 | 92,903.04 | 1,468.80 | 89,110.44 | 23 / 12 / 2 | 11 → 7–13 |

TIFF masks were valid throughout. The 2023 NAD83/UTM 16N grid has 0.6 m cells. Average each aligned 2×2 block of 2025 samples by band before classification. At each date the rule calls a cell crown when NDVI ≥0.20 and the 5×5 near-infrared population standard deviation ≥10 DN. An RGB mean below 35 DN or an incomplete texture neighborhood makes the center unknown. A known crown followed by a known noncrown contributes to gross candidate loss. Four-neighbor components form before any area filter. The first row-major pixel identifies each component within a site and scenario. Native coverage excludes the reservation margin and has zero additional spatial exclusions. Area is projected grid area at 0.36 m² per cell.

The [control ledger](controls.json) replays all 20 T05 anchors and adds 35 candidate controls. Five of the six indexed sides initially lacked enough spatially independent placements to pass even with perfect matches. Seventeen supplemental locations and roles were pinned at `a414398` before measuring them. All six sides then had at least three fit and two check placements before the correlation screen. Each displacement is the late feature position minus its early position, signed east/north in metres. Full-support overlap, a boundary crossing, a diagnostic-only role or failure of the T05 correlation screen can exclude a control. West End admitted one fit and one check on the same indexed side, with offsets (+2.4, −0.6) and (+0.6, +1.8) m. Kirkwood and Piedmont each admitted one check. Far west admitted one fit and four checks spread over two sides. The [site ledger](sites.json) reports each 2023/2025 exposure-ID pair and its supported and uncertain area using cell centers. Index polygons describe possible seams. The strip used in the four-band export remains unverified.

Each hypothetical trial samples the late mask 0 or ±2 cells in each axis, including diagonals. Intersect all trials' known cells and require every common-grid cell center in both 5×5 texture neighborhoods to lie on the same indexed side. A cell on the seam can still contain samples from both sides when its center falls on one side. The site ledger separates image-edge and internal-seam exclusions from unknown area. On the common mask Kirkwood has eight raw candidates ≥0.10 acre. Sampling two rows south and two columns east leaves five. Four raw candidates lose their match, four retain one and one new candidate appears. The [comparison ledger](comparisons.json.gz) gives counts, areas and individual links for every trial. At each floor, keep every raw/trial pair with intersection over union ≥0.10. One-to-many links mark splits, many-to-one links mark merges. The raw entry also links native IDs to the common-mask IDs. Displacements in these trials are sensitivity assumptions.

### Paired inspection

Consider aligned, nonoverlapping 32×32 tiles with ≥75% native known area. Select the largest loss count and, separately, the most prior classified crown among zero-loss tiles, breaking ties in row-major order. In all four zero-loss selections the detector assigned zero known prior crown. To inspect apparently persistent crowns as well, retain tiles outside all ≥0.10-acre events with at least 256 known prior-crown cells and select the smallest loss fraction among those cells, breaking ties by higher prior-crown count and then row-major order. The [site ledger](sites.json) gives zero-based row and column, loss pixels and known prior-crown pixels for each tile.

| Site | Flagged pair, 2023 → 2025 | Apparently unchanged pair |
|---|---|---|
| Piedmont | The mask follows a leafy edge beside dark water. Both dates show crown nearby. The apparent retreat is ambiguous at this alignment. | Lake water in both images. |
| West End | Much of the flag falls on turf beside a crown and track. A grass/shadow edge appears to trigger the crown rule. | Track and field persist despite different color and sharper lane markings. |
| Kirkwood | Dark crown or shadow in 2023 borders a brighter, differently textured crown in 2025. The flag covers visually persistent vegetation, a likely false alarm in part. | Open grass and a small light patch, with no clear crown removal. |
| Far west | Crown texture persists through the flagged patch while illumination and shadow change. This looks like a false alarm over part of the canopy. | The paved junction and verges persist. |

In the additional low-loss crown tiles, textured crowns remain visible at Piedmont and far west. West End shows a partly shaded crown beside open ground, and Kirkwood shows a crown above a verge. The scattered flags along these crowns could reflect shadow, texture or displacement. These targeted reads identified no clear missed removal. They supply neither an independent reference nor a precision or recall estimate. Registration uncertainty prevents confirming crown removal at 0.10 acre on these windows. The two candidates above 0.25 acre have the same limitation. To reopen it, target a development pair with spatially distributed stable ground features that allow fit and independent residual checks on each relevant seam side near candidate crowns. Reserve and check its full influence footprint before reading. A challenger would currently confound detector error with displacement.

## Outputs and replay

Use implementation revision `b78c7b4`, CPython 3.14.7, the [raster requirements](../../requirements.txt), SciPy 1.18.1, Shapely 2.2.0 and pyproj 3.8.0. The [config](config.json) pins the thresholds, controls and their roles. From the repository root, the replay defaults to the existing cache at `data/imagery`. If any TIFFs are missing, run the linked T05 recovery commands first, then set `imagery="$run"` in the same shell. That directory contains the recovered `t01/` and `t05/` inputs. The runner checks the archived pixels, grid, masks and reservation tile/date metadata before scoring. Source and rights details are in the T01 and T05 manifests.

```sh
(
set -eu
task=tasks/T08-development-baseline
out=$(mktemp -d)
python "$task/baseline.py" "${imagery:-data/imagery}" "$out"
python -m unittest discover -s "$task" -v
for file in sites.json controls.json; do cmp "$task/$file" "$out/$file"; done
for file in events.geojson.gz comparisons.json.gz; do
  gzip -dc "$task/$file" > "$out/reference"
  gzip -dc "$out/$file" > "$out/rebuilt"
  cmp "$out/reference" "$out/rebuilt"
done
)
```

The [event layer](events.geojson.gz) contains all 6,962 uncorrected components in WGS84, including subthreshold components. Use `area_m2` for filtering. Flags identify possible truncation at unknown or footprint edges and exposure to unresolved registration. Event replay on this host matched exactly for IDs, geometries, counts and areas. The eight cached TIFFs occupied 13,121,956 bytes. The four generated evidence files occupied about 1.36 MB. A warm local CPU run took 1.8 s, excluding input recovery and environment setup.

The [fixture ledger](fixtures.json) records expected and observed mask hashes, areas, IDs and counts. The same-epoch pair produced zero loss. A known 3-row south, 2-column west offset produced 194.04 m² of apparent loss. On the same 5,081.04 m² of supported pixels, apparent loss fell from 151.56 m² to zero after the estimated translation. Inserting a 36×36-cell loss patch returned one 466.56 m² event, retained at 0.10 acre and excluded at 0.25 acre.

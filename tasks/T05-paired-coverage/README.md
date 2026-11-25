# T05 — Where does Atlanta have a usable image pair?

## Brief

Use the [T01 dated imagery sources](../T01-imagery/README.md) and [T02 City and county snapshots](../T02-geography/README.md) at `8ac1ac9` to assess the 2023 and 2025 NAIP pair. The discovery denominator is the full 2026 City snapshot. A window can establish local readability. Tile footprints can establish only potential coverage.

- Inventory the dated assets intersecting the City. Preserve source IDs, acquisition dates or unresolved ranges, footprints, overlap selection, seamline information where available, and retrieval provenance. Produce a replayable area table and mask for both epochs together, either epoch alone, neither, and unresolved coverage. Reconcile areas to the City total within a stated tolerance, with Fulton, DeKalb and county-unassigned subtotals.
- Start with metadata and the existing Fulton windows. Before reading new pixels, push the full proposed read footprints in a versioned geometry file, then fetch the current main and task branches. Check against any published candidate or frozen holdout and its buffer, including after reference design is complete. Move conflicting windows before reading. If reference design has an active owner, agree on the reservation revision together. If no split or claim exists yet, the published windows become development exclusions. Repeat for any expanded read footprint. Attempt a dated pair in DeKalb and target any other development windows to a specific uncertainty such as a seam or a different flight date. Report bands, masks, phenology, shadow and residual alignment on stable features in ground units. Keep sample measurements local and mark unsampled catalog coverage unverified for pixel quality.
- Deliver the ledger, geometry, checks and pilot recommendation here. For a viable pilot, identify the candidate development windows by asset, extent and date, and explain which acquisition and neighborhood conditions they represent or miss. Replay one newly retrieved pair from its unsigned source and check its grid and pixel hashes, or document the acquisition/recovery failure. Estimate space for the proposed pilot from its grids and bands. If scale requires durable storage beyond the [T04 demonstration](../T04-runtime/README.md), identify the missing capacity or access before bulk acquisition.
- Stop when both county portions and the residual area are accounted for and the pilot decision or limiting source gap is reproducible. A failed county probe stays visible. Reopen the 2019–2023 alternative only for a documented recent-pair gap that compromises the pilot. Use small window reads and ignored caches under `data/`. No county mosaics, model fitting or protected-image inspection in this task. Reserve only this task folder and its cache.

## Progress

Owner and session start: Codex T05, 2026-11-24 19:14 EST. Branch `task/T05-paired-coverage` from `83509aa`. Limits: use public metadata and small development reads within 128 MiB of source transfers and 500 MiB of task cache. Reserve only this folder and `data/imagery/t05/`.

The [development reservation](development-windows.geojson) covers the full Kirkwood and far west read extents plus a 1 m margin. It also includes the previously inspected T01 windows.

Catalog accounting, reserved reads and fresh replay are complete. Independent Sol review reproduced the coverage, date overlaps, raster hashes and alignment results. Its seamline and alignment findings are incorporated below.

## Result

The two catalogs cover the entire 2026 City snapshot for both epochs. Each has 20 dated primary tiles with positive-area City intersections. Of 30 USGS and 25 USDA envelope hits, five USGS overviews were excluded and five primary tiles per epoch had no positive-area City overlap. The ID-only and feature replies agree. The footprint overlay uses EPSG:5070 and reconciles within 2 m². The [area ledger](areas.json) and [catalog mask](catalog-mask.geojson.gz) report potential coverage. Only the four windows below have verified pixels.

| City portion | Both catalogs, km² | 2023 only, 2025 only, neither, unresolved |
|---|---:|---:|
| Fulton | 329.917694 | 0 in each class |
| DeKalb | 23.445811 | 0 in each class |
| County unassigned | 0.009340 | 0 in each class |
| Full City | 353.372845 | 0 in each class |

The [catalog ledger](catalog.json) preserves unsigned requests, retrieval times, service object IDs, provider date fields and primary footprints. It assigns overlaps by ascending dated tile name in each epoch for repeatable area accounting. Pixels in the development windows were requested by explicit item ID. Different-dated catalog tiles overlap on 7.233 km² in 2023 and 2.907 km² in 2025. Missing or contradictory tile dates would leave coverage unresolved where they are the only candidate for an epoch. The sample dates are corroborated by [2023 Georgia acquisition-date polygons](https://imagery.geoplatform.gov/iipp/rest/services/NAIP/NAIP2023_CONUS_AcquisitionDates/MapServer/11) and [2025 Georgia seamlines](https://services.arcgis.com/LLVEmB8Lsae3Um4s/ArcGIS/rest/services/2025_Georgia_Image_Dates/FeatureServer/0). The selected tile dates differ from the date-index polygons over 32.363 km² and 10.543 km², respectively. The 2023 index is marked natural color, and neither index establishes the exact flight strip used in the four-band exports. Retain both sources and resolve conflicts before assigning local observation intervals. NAIP imagery provided by USDA Farm Service Agency. [T01 rights and service notes](../T01-imagery/README.md#access-and-source-selection).

Codex read the two new 307.2 m squares on November 24, 2026. The [reservation](development-windows.geojson) gives the bounds and exact asset names. After pushing `8b437f3`, the fetch showed main at `83509aa` and T05 as the only task branch. Main held the T06 brief without a published holdout or buffer. Include all four footprints in the development exclusions. The [read and replay ledger](window-evidence.json) records EPSG:26916 grids, dates, unsigned URLs, band ranges and hashes. New reads returned four nonconstant uint8 bands at 0.6 m (2023) and 0.3 m (2025). RGB and near-infrared labels come from provider band order. The TIFFs declared no nodata, and every mask pixel was valid. No pixel had all four bands equal to zero. Fresh downloads reproduced each of the four new TIFFs byte for byte and passed the grid and decoded pixel and mask checks.

| Development window | Tile dates | Observed context | Ground offset on screened features |
|---|---|---|---|
| Piedmont Park, Fulton | Oct 8, 2023 / Oct 11, 2025 | Leafy crowns, lake and paths. Shadow and visible pavement changes. | 0 of 1 passed |
| West End, Fulton | Oct 8, 2023 / Oct 11, 2025 | Running track and streets. Leafy trees and shadows around the track. | 3 of 4, 0.85–2.47 m |
| Kirkwood area, DeKalb | Oct 8, 2023 / Oct 11, 2025 | Leafy residential streets with overlapping crowns. Strong shadows and changed road markings. | 1 of 8, 0.60 m |
| Far west Atlanta, Fulton | Oct 8, 2023 / Oct 15, 2025 | Wooded residential streets with exposed pavement and changed shadow extent. | 3 of 7, 0.60–0.85 m |

Offsets are uncorrected 2025 positions relative to 2023 on a common 0.6 m grid. The [local diagnostic](alignment.json) records all accepted and rejected chips. It averages 2025 RGB 2×2, smooths both epochs, and searches signed RGB-intensity gradients within ±3.6 m. An interior peak needs correlation ≥0.65 and a ≥0.02 lead over candidates outside its one-pixel neighborhood, before rounding. Smoothing and chip placement were refined on these windows, and two far-west passes are nearby driveways. The exploratory pass counts depend on those choices and have limited spatial support. Kirkwood's single match leaves local registration uncertain. Image sharpness, shadows and crown color vary between epochs despite leafy crowns in all four windows.

Take the four windows to AR02 as a **development baseline candidate**. They cover parks, urban streets and wooded residential areas, including DeKalb and the later western flight date. They miss the October 7, 2023 exposure, between-date seams, other built forms and any designed income strata. The 2025 index shows same-day seams in West End and far west Atlanta. Registration across those seams remains unmeasured. Leave all other pixels unverified and measure stable features before using the baseline to interpret small crown changes. The current pair supports this bounded baseline, so the 2019 alternative stays closed. The four pairs require about 12.5 MiB of TIFFs. At 655,360 common-grid cells, add 5 MiB for two four-band uint8 images and 1.25 MiB for two one-byte masks. Budget about 19 MiB before headers and working arrays. The unsigned replay covers this small pilot. Bulk acquisition would need a verified raw-artifact store beyond [T04's small derivative round trip](../T04-runtime/README.md).

## Outputs and replay

Use CPython 3.14 with the [pinned raster requirements](../../requirements.txt), Shapely 2.2.0 and PyProj 3.8.0. The [compressed date-index responses](date-index.json.gz) preserve geometry and exposure attributes. From the repository root, run the following with a new output directory. The mask uses WGS84 longitude/latitude. It omits empty geometries, which are explicit as zeros in the area ledger.

```sh
run=$(mktemp -d)
python tasks/T05-paired-coverage/coverage.py "$run"
python tasks/T01-imagery/recover_windows.py "$run/t01"
python tasks/T05-paired-coverage/check_windows.py "$run/t05" "$run/t01" --retrieve > "$run/alignment.json"
python -m unittest discover -s tasks/T05-paired-coverage -v
```

Compare the rebuilt area ledger, decompressed mask and alignment JSON with the linked outputs. Use the 2 m² tolerance for the area and mask checks. The pixel replay verifies the live item ID, tile name and date before downloading and checks the recorded grid, masks and pixels. Cached raw rasters live outside Git.

## For integration

After review and merge, mark T05 complete and carry the catalog and four read windows into AR02. T06 should pin the published reservation when checking its buffer and candidate holdout.

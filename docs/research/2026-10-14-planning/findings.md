# Initial evidence and reassessment

Planning date: 2026-10-14, America/Los_Angeles. Network observations occurred on 2026-10-15 UTC. This is supporting evidence, not a second project-state file; use [checklist.md](../../../checklist.md).

## What was actually examined

Eight bounded HTTP probes, two report downloads, primary-source reading, and independent scientific review informed this plan. No training, bulk geospatial acquisition, permit collection, external communication, or deployment occurred. URLs and retrieval success are evidence about access at this time, not promises of future availability.

## E1 — Imagery catalog probe

Evidence: [script](probe_sources.py), [recorded JSON](source-probes.json). Python standard library; eight sequential requests; 30-second timeout each; 4 MiB response cap; no retries. Reproduce from repository root with:

```sh
python docs/research/2026-10-14-planning/probe_sources.py /tmp/canopy-source-probes-new.json
```

Use the authorized network-enabled executor through its inherited proxy. Do not overwrite the original observation. The JSON stores query URLs, UTC timestamps, status, response size/hash, relevant public metadata, unsigned asset URLs, and pagination state. It does not retain HTML or permit records. Hashes identify received responses; only the selected JSON fields are retained, not byte-for-byte original response bodies.

Screening rectangle: `[-84.552, 33.647, -84.289, 33.887]`, inherited from the archive. **This is not an authoritative City of Atlanta boundary or a completeness test for the whole city.**

| Query | Observed result | Permitted inference |
|---|---|---|
| Planetary Computer `naip` collection | HTTP 200; temporal extent ends 2023-12-31 | Catalog advertises no later coverage at this check |
| 2019 in rectangle | 25 items; dates 2019-09-10 through 2019-10-04; GSD 0.6 m | Plausible fallback candidate; pixels/phenology untested |
| 2021 in rectangle | 18 items; dates 2021-11-14 through 2021-11-15; GSD 0.6 m | Late-season concern is locally supported; no blanket inference about every Georgia tile |
| 2023 in rectangle | 25 items; dates 2023-10-07 through 2023-10-08; GSD 0.6 m | Archive's local September assumption is wrong for these returned items |
| 2025 in rectangle | 0 items; HTTP 200 | No matching items in this catalog/query; says nothing definitive about other distributors |
| USDA direct-download landing page | HTTP 403 | This access path failed here; dataset absence not established |
| Atlanta Accela landing page | HTTP 403 | Automated access not demonstrated; historical completeness unknown |
| Guessed ARC `/api/v3/datasets/..._0` metadata path | HTTP 404 | Endpoint guess failed; not evidence that the advertised CSV disappeared |

All four STAC searches had no next-page link. Counts refer to intersecting catalog items, including buffered footprints, not unique nonoverlapping coverage. The returned raster asset host is `naipeuwest.blob.core.windows.net`; raster bytes were **not** retrieved. The executor's observed allowlist did not list that host. T01 must establish a supported asset-access path or prepare the exact access request; a working catalog is insufficient. The collection's imagery metadata uses EPSG:26916 in these samples, supporting that CRS as a pilot candidate, subject to parcel compatibility and area checks.

The environment status reported current observations but network policy state `unknown`; `/etc/codex/network-policy.json` described restricted HTTP destinations. Initial shell network access failed until the supported network permission was enabled. Subsequent Git and STAC calls succeeded; remaining 403 responses were recorded without claiming whether provider or policy caused them. No proxy bypass was attempted.

## E2 — Georgia Tech comparison

Primary sources: [2023 final report](https://geospatial.gatech.edu/AtlantaUTC/AtlantaCanopyReport2023GT.pdf), [2018 final report](https://geospatial.gatech.edu/AtlantaUTC/2018FinalReport.pdf), and [study portal](https://geospatial.gatech.edu/AtlantaUTC/). Both PDFs were downloaded and their relevant methods, accuracy, change-review, and permit sections read directly. [Download hashes](gt-report-manifest.json) identify the versions. Raw PDFs are temporary at `/tmp/canopy-planning/` and not committed; retrieve from those URLs and compare SHA-256 to recover them. Extract with `pdftotext -layout INPUT.pdf OUTPUT.txt`. Page references below use the printed report pages.

**2023 findings (reported, not independently reproduced model performance).** Pages 18–20 describe September 24, 2023 WorldView-2 imagery (0.5 m, four bands), random forest classification across 13 quarter quads, and manual pixel edits. The three classes are tree canopy, other vegetation, and non-vegetation. A stratified 250-point check against July 2023 Google Earth imagery reports 95.6% overall accuracy; tree user/producer accuracies are 99.1%/97.4%. These are land-cover metrics. Pages 25–26 describe 500-foot grid cells, 1,057 cells crossing a one-acre change threshold, 735 remote reviews, and 385 cells selected for approximately 148 site visits. Page 15 discusses permit comparison. The report acknowledges changes split across cells can escape inspection. Section 3.5 uses a broader “over 1,000” visual-inspection count; do not conflate it with the 735-cell subset.

**2018 findings.** Pages 14–17 describe mixed-date 2018 WorldView-2 imagery, 2017 NAIP cloud fill, ISODATA classification, shadow reclassification, manual correction, and neighborhood filtering. The 250-point assessment reports 93.2% overall accuracy. Pages 23–24 use the grid review approach: 939 loss cells exceeded one acre, but loss cause qualification focused on 410 cells with at least 1.25 acres. These thresholded reviews do not constitute a probability sample of all small loss events.

**Implications for our design (our interpretation).** Borrow the explicit land-cover definitions, interpreter error review, separate treatment of shadows, and accessible map/story format. Include a random-forest baseline: GT is evidence that simpler models deserve a test, not evidence that their accuracy transfers to NAIP. Measure the cost of human correction instead of attributing the final result solely to a classifier. Avoid converting their overall accuracy into a change-detection benchmark.

Our contribution is a testable extension: reproducible detection of smaller gross-loss events, uncertainty and missing-coverage maps, explicit many-to-many parcel attribution, and auditable permit reconciliation. We cannot yet claim novelty, superior accuracy, shorter publication lag, or operational adoption. GT already studies change, uses machine learning, presents public maps, and compares permits. Do not say a quarter-acre event is absent from their underlying raster; the documented limitation concerns thresholded review and aggregation. Do not compare our gross loss directly to their net cover change.

The portal advertises a [canopy data hub](https://experience.arcgis.com/experience/a5cc602b023f42cdbbb6a1d2a35e8ec8). The dynamic page did not expose a downloadable layer in this investigation. T02 will inspect public services/rights before any contact request. GT data, if obtainable, are an external comparison with their own errors, dates, spatial support, and manual edits; they are not automatically independent truth or unrestricted training data. Targeted GT sites may inform development/error examples, never silently populate the protected probability sample.

## E3 — Other source checks

| Source | What supports the plan | Limit |
|---|---|---|
| [NOAA Georgia 2021 NAIP metadata](https://www.fisheries.noaa.gov/inport/item/68396) | Statewide acquisition 2021-10-07 to 2022-01-13; credit requested; distribution metadata | State window alone is not local phenology; no download demonstrated |
| [Earth Engine NAIP catalog](https://developers.google.com/earth-engine/datasets/catalog/USDA_NAIP_DOQQ) | Page currently ends 2023-11-17 and describes RGBN imagery | No Earth Engine account/query tested; generic page text is not per-tile resolution proof |
| [NAIP-CHM paper](https://www.nature.com/articles/s41597-026-07549-w) | Imagery-derived height includes buildings/infrastructure; mixed source dates; 96% 2022–23; ancillary model inputs | National height errors do not validate Atlanta canopy labels; local source years, rights and asset retrieval still need checks |
| [City Arborist Division](https://www.atlantaga.gov/government/departments/city-planning/nature-urban-ecology/arborist) and [city arborist guide](https://www.atlantaga.gov/home/showpublisheddocument/59680/638269295768430000) | Official indexed text describes building-permit arborist review, DDH records, and separate Parks responsibility for public trees/right-of-way | Search-index text retrieved; some direct opens returned 403. Current record coverage and historical rules not established |
| [City ordinance phase-2 summary](https://www.atlantaga.gov/home/showdocument?id=67316&t=639019965802839425) | Indexed official text says changes apply to plans submitted on/after 2026-01-01 | Direct open failed; do not back-apply these rules to 2023–25 events or infer legality |
| [ARC building-permit listing](https://opendata.atlantaregional.com/datasets/655f985f43cc40b4bf2ab7bc73d2169b/about) | Advertised 2019–24 source remains a discovery lead | Dynamic page/failed guessed endpoint did not yield a CSV or prove tree coverage |
| [Olofsson et al. 2014](https://doi.org/10.1016/j.rse.2014.02.015) | Primary publisher abstract identified: probability sampling, reference design, accuracy/area estimation with uncertainty | Full text not retrieved here; T07 must read an accessible primary manuscript before implementing estimators |
| [Roberts et al. 2017](https://doi.org/10.1111/ecog.02881) | Primary publisher abstract supports dependence-aware cross-validation | Does not prescribe NPU blocks, buffer distance, or our sample size |

The plan makes no claim about current fines, DBH thresholds, illegal removals, or guaranteed records-request cost. Those are unnecessary to establish canopy-loss feasibility. T03 must verify applicable, effective-dated rules and record semantics for the selected interval.

## Archive disposition

| Inherited choice/claim | Current disposition and reason |
|---|---|
| City plus unincorporated DeKalb | City first, including its parts in both counties; expansion needs its own jurisdiction/data/evaluation gate |
| Fixed 2023/2025, September baseline | Preferred interval only; actual baseline query is October; inspect assets and dates before commitment |
| Never use any 2021 tile | Exclude from primary pilot by default given observed late dates; retain as a possible stress test, not a forbidden source |
| Permit access solved; building CSV adequate fallback | Withdraw readiness claim. Building permits are contextual unless tree approval is evidenced; missing source coverage becomes ambiguous |
| Mandatory U-Net and 2023-only training | Baseline comparison first; same-model paired inference is a controlled candidate, not guaranteed bias cancellation |
| Height >3 m and NDVI >0.20 establish truth | Weak-label hypothesis only. Optical canopy definition need not pretend to measure exact height |
| Mandatory AROSICS/local warp | Measure residual registration; correct only with evidence, stable ground points, and before/after checks |
| 0.1 acre = 1,124 pixels; opening/compactness fixed | Physical-area threshold is provisional; at 0.6 m, 0.1 acre / 0.36 = 1,124.127 pixels, so a strict whole-pixel minimum is 1,125. Audit narrow/fragmented events |
| NPU-only split; citywide pseudo-training | Buffered geographic/acquisition blocks; exclude protected footprints from all local training and tuning |
| IoU 0.80 gate; 25 visits; preset annotation count | Replace with change-specific evaluation, justified sampling effort, and distinct historical-reference/current-field roles |
| Storm as exclusion; inferred cause as fact | Context only; retain unknown cause, record alternative explanations |
| Dollar ranges and daily sign scraping | Defer: they do not resolve the primary historical detection question and add unsupported interpretation/operations |
| Free GPU and a fixed 30-week schedule | Not established. Benchmark real inputs; retain resource and recovery gates; sequence by evidence |

## Independent review

Findings incorporated: protect geography from pseudo-training leakage, distinguish source-model overlap, evaluate both dates and nonloss, test registration rather than mandate a package, use physical event MMU before parcel splitting, separate matching from authorization, and reject inherited readiness/accuracy guarantees. Independent evidence review is recorded in [review.md](review.md).

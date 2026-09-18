# Canopy Ledger

**Problem definition, data audit, solution options, and implications for parcel-scale tree-canopy-loss detection in metro Atlanta.**

| | |
|---|---|
| Status | Scoping complete, pre-implementation |
| Last updated | 2026-09-18 |
| Supersedes | `context.md` §2 (option selection) |
| Companion | `permits-and-pixels.md` (implementation spec) |

---

## 1. The problem, stated exactly

Everything turns on one mismatch: **Atlanta measures its tree canopy at a resolution and cadence that cannot support the ordinance it is supposed to inform.**

The city's canopy assessments, produced by Georgia Tech's Center for Spatial Planning Analytics and Visualization, classify WorldView-2 satellite imagery at roughly 1.8 m into three classes, then report *change* by aggregating canopy values into grid cells of about six acres (500 ft × 500 ft) and flagging cells that gained or lost more than one acre. In the 2018 study that produced 939 loss cells and 292 gain cells citywide.

It is a good method for the question it was built to answer — how is the city doing overall — and a poor one for the question the ordinance asks: what happened on *this parcel*, and did someone have a permit for it.

### Current monitoring vs. what the ordinance needs

| | City's current method | What this project builds |
|---|---|---|
| Unit of analysis | ~6-acre grid cell (500 ft × 500 ft) | Parcel |
| Change threshold | > 1 acre per cell | ≥ 0.1 acre polygon |
| Imagery | WorldView-2, ~1.8 m, commercial | NAIP, 0.6 m, public domain |
| Cadence | ~5 years | 2 years (NAIP cycle) |
| Publication lag | ~3 years (2023 imagery → Aug 2026) | ~1–1.5 years |
| Permit reconciliation | None | Three-bucket match |
| Attribution | Neighborhood / NPU | Parcel ID + date window |

A cleared quarter-acre lot is invisible to the current method by construction. Loss cannot be tied to a parcel. Permitted cannot be separated from unpermitted.

### Problem statement

> Metro Atlanta has no method that identifies tree-canopy loss at the parcel scale, attributes it to a property and a date, and reconciles it against the tree-removal permit record — even though the city's ordinance assigns a dollar value to every inch of removed tree and a penalty to every unpermitted acre.

The consequence is that canopy loss is measured in retrospect and in aggregate. The city can say it lost roughly 150 acres a year; it cannot say which 150 acres, on whose land, in which year, with or without authorization. Enforcement therefore depends on a neighbor noticing and calling. Recompense owed on unpermitted removal cannot be estimated, so the deterrent the ordinance describes is only partly real.

### As a research question

Can a semantic-segmentation model applied to successive NAIP aerial imagery cycles detect canopy-loss patches at the parcel scale across the City of Atlanta and DeKalb County, at precision high enough to support code enforcement, and does reconciling those patches against the tree-permit record reveal a measurable volume of unpermitted clearing?

### Scope boundaries

**In scope.** City of Atlanta plus unincorporated DeKalb; two NAIP epochs; loss patches ≥ 0.1 acre; canopy defined as woody vegetation over ~3 m tall.

**Out of scope.** Canopy *gain* and net change (gain is harder and contaminated by the "false growth" problem); individual tree counting; species; exact DBH per tree; tree health.

**Deferred.** Real-time or annual monitoring — NAIP's two-year cycle cannot support it.

---

## 2. Data availability

Six inputs. Four confirmed free, one is the pivot, one is a nice-to-have.

| Input | What exactly | Access | Status | Blocker |
|---|---|---|---|---|
| NAIP imagery | Georgia, 60 cm, 4-band RGB+NIR, 2019 / 2021 / 2023 / 2025 | Planetary Computer, Earth Engine, AWS, USDA | Confirmed free | Cloud catalogs end at 2023 — see `permits-and-pixels.md` |
| Canopy labels | NAIP-CHM, 0.6 m canopy height, RMSE 2.28 m, r² 0.87 | GEE asset, COGs, GitHub weights, CC-BY 4.0 | Confirmed free | 96% derived from 2022–23 NAIP; includes buildings |
| LiDAR | Georgia statewide USGS 3DEP, ~4 pts/m², Nov 2018 – Apr 2019 | USGS, OpenTopography, NOAA; public domain | Confirmed free | Leaf-off, 7+ years old |
| Validation canopy | GT Atlanta UTC 2008/2014/2018/2023, WorldView-2, 3-class | Reports as PDF; portal advertises a "canopy hub" | Partly public | Raster download unconfirmed — email Giarrusso |
| Parcels | Fulton and DeKalb assessor polygons with land-use codes | County GIS, ARC Open Data | Routine | Boundary vintage vs. imagery date |
| Permits | Tree-removal and arborist review records | Accela, bulk CSV, sign postings, ORA request | **Solved** — see `permits-and-pixels.md` §1 | Assembly, not access |

### Two findings that shaped the plan

**Georgia NAIP is flown late, and 2021 is unusable.** The 2021 Georgia flight ran 7 October 2021 to 13 January 2022 — largely leaf-off, which for a canopy-differencing task would manufacture enormous phantom loss. The clean pair is **September 2023** against **July–October 2025**. Even within those, late-October tiles catch hardwood senescence, so pull per-quad acquisition dates from the USDA image-date services before selecting tiles.

**The permit record turned out to be accessible.** An earlier draft of this document called it the critical path most likely to sink the project. That was too pessimistic — see the companion spec. The remaining work is assembly across four systems, not acquisition.

---

## 3. Solutions

### Architecture options

#### A. Post-classification comparison — **THIS IS WHAT WE ARE DOING, defined more in permits-and-pixels.md**

Segment canopy independently in each epoch, then subtract.

- **Why.** Each mask is independently validatable, so when the change product is wrong you can tell which year was wrong. Tolerates the severe radiometric inconsistency between NAIP flight lines and years. Lets you reuse pretrained 4-band weights directly.
- **Cost.** Errors compound — two masks at 0.85 IoU do not give a change product at 0.85. Expect the change layer to be the weakest number you report, and say so.
- **Precedent.** A 2024 comparison on NAIP in two southern US cities found U-Net at 91.4% and 89.8% overall accuracy, beating SVM (~84%) and random forest (~76%).

#### B. Bi-temporal / siamese change network — stretch goal

Feed both epochs into one network with shared encoders, predict change directly.

- **Why.** Learns to ignore nuisance differences (illumination, phenology, misregistration) rather than inheriting them.
- **Cost.** Needs *change* labels, not canopy labels. Nobody has published change labels for Atlanta, so every training example is hand-digitized. Heavy annotation burden at the point in the year with least momentum.
- **Verdict.** Second-semester comparison against the differencing baseline, not the primary pipeline.

---

## Sources

- [AJC — Atlanta has lost nearly 150 acres of tree canopy a year (Aug 2026)](https://www.ajc.com/news/2026/08/atlanta-has-lost-nearly-150-acres-of-tree-canopy-a-year-study-finds/)
- [Georgia Tech ATL UTC portal](https://geospatial.gatech.edu/AtlantaUTC/) · [2018 final report](https://geospatial.gatech.edu/AtlantaUTC/2018FinalReport.pdf) — 6-acre grid cells, 939 loss cells, 93.2% accuracy, "false growth"
- [Georgia Tech News — 2023 method, random forest, Potential Planting Index](https://www.gatech.edu/news/2025/07/31/mapping-georgias-urban-forest-georgia-tech-tools-help-planners-prioritize-tree)
- [City of Atlanta — Tree Protection Ordinance statement](https://www.atlantaga.gov/Home/Components/News/News/15451/1338) · [Capital B — $140/inch, $200,000/acre](https://atlanta.capitalbnews.org/atlanta-tree-protection-ordinance-202/)
- [Rough Draft — DeKalb ordinance rewrite underway](https://roughdraftatlanta.com/2026/09/02/dekalb-tree-protection-ordinance-update/) · [DeKalb canopy report](https://www.dekalbcountyga.gov/news/dekalb-county-releases-new-urban-tree-canopy-report)
- [Pedley & Morgenroth — fine-scale canopy loss with deep learning](https://www.sciencedirect.com/science/article/pii/S2667393225000018)
- [Geomatics 2024 — U-Net vs SVM vs RF on NAIP](https://www.mdpi.com/2673-7418/4/4/22) · [NAIP canopy U-Net, Los Angeles](https://www.mdpi.com/2072-4292/18/12/1899)
- [NAIP-CHM 0.6 m canopy height model](https://www.nature.com/articles/s41597-026-07549-w) · [Georgia statewide LiDAR 2018–19](https://www.fisheries.noaa.gov/inport/item/67264)
- [California v. Ciraolo, 476 U.S. 207 (1986)](https://supreme.justia.com/cases/federal/us/476/207/)
- [Coconut Grove Spotlight — Miami canopy dispute](https://coconutgrovespotlight.com/2026/08/24/city-says-the-groves-tree-canopy-is-growing-not-all-are-convinced/)

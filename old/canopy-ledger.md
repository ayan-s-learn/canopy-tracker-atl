# Canopy Ledger

**Problem definition, data audit, solution options, and implications for parcel-scale tree-canopy-loss detection in metro Atlanta.**

| | |
|---|---|
| Status | Scoping complete, pre-implementation |
| Last updated | 2026-09-23 |
| Fact-checked | 2026-09-23 against primary sources — see §1.1 |
| Companion | `permits-and-pixels.md` (implementation spec) |

---

## 1. The problem, stated exactly

Everything turns on one mismatch: **Atlanta measures tree-canopy change at a unit of analysis and cadence that cannot support the ordinance it is supposed to inform.**

The city's canopy assessments (2008, 2014, 2018, 2023) are produced by Georgia Tech; the 2023 edition is by GT's Center for Urban Resilience and Analytics. They classify WorldView-2 satellite imagery into three classes — **0.5 m in 2023** (random forest, 95.6% overall accuracy), 6 ft / ~1.8 m in 2018 (93.2%) — then report *change* by aggregating canopy values into grid cells of about six acres (500 ft × 500 ft) and examining only cells that gained or lost more than one acre. The 2018 study produced 939 loss cells and 292 gain cells citywide. In 2023, 1,057 cells crossed the threshold; researchers inspected 735 on screen and made over 100 site visits.

**The imagery is not the gap.** GT's 2023 imagery is sharper than NAIP's 0.6 m, and GT already uses machine learning. The gap is what happens after classification: aggregation to 6-acre cells, a 1-acre floor, manual review of only the largest changes, and a 4–6 year cycle. GT's reports say so themselves (2018 and 2023, same wording): *"many areas of loss spanned multiple grid cells and subsequently were missed in these inspections where each grid cell contained loss less than 1 acre."* And on single-family redevelopment: tree removal *"often goes unnoticed because it occurs lot by lot and doesn't become apparent until an entire street or neighborhood has been redeveloped."*

It is a good method for the question it was built to answer — how is the city doing overall — and a poor one for the question the ordinance asks: what happened on *this parcel*, and did someone have a permit for it.

### Current monitoring vs. what the ordinance needs

| | City's current method | What this project builds |
|---|---|---|
| Unit of analysis | ~6-acre grid cell (500 ft × 500 ft) | Parcel |
| Change threshold | > 1 acre per cell | ≥ 0.1 acre polygon |
| Imagery | WorldView-2, 0.5 m (2023; 1.8 m in 2018), commercial | NAIP, 0.6 m, free |
| Change review | Manual — on-screen inspection of cells > 1 acre, 100+ site visits | Automated over every polygon; manual review on a validation sample |
| Cadence | 4–6 years (2008, 2014, 2018, 2023) | 2 years (NAIP cycle) |
| Publication lag | ~3 years (2023 imagery → Aug 2026) | ~1–1.5 years |
| Permit reconciliation | Manual, for inspected large-change cells only ("most of these trees were permitted … though some were locations where fines had been issued") | Automatic, every loss polygon, three-bucket match |
| Attribution | Neighborhood / NPU | Parcel ID + date window |

A cleared quarter-acre lot is invisible to the current method by construction, and GT's own reports concede that losses split across cells were missed. Loss is not tied to a parcel, and permitted is separated from unpermitted only by hand, only for the largest changes.

### Problem statement

> The City of Atlanta has no systematic method that identifies tree-canopy loss at the parcel scale, attributes it to a property and a date, and reconciles it against the tree-removal permit record — even though its ordinance charges $140 per diameter-inch of removed tree and fines unpermitted clearing up to $200,000 per acre.

The consequence is that canopy loss is measured in retrospect and in aggregate. The city can say it lost roughly 150 acres a year; it cannot say which 150 acres, on whose land, in which year, with or without authorization. Enforcement therefore depends on someone noticing. The City Auditor's 2020 audit of the Tree Trust Fund says so directly: *"Arborist staff stated that the division mainly relies on neighbors' complaints and arborists' drive-bys to identify trees that have been illegally destroyed,"* and *"based on tree canopy loss, it is likely that trees have been removed illegally without the city's knowledge. The city relies on complaint-based enforcement, which is an industry standard but unlikely to capture all cases of illegal tree removal."* It adds that the department *"could be more effective in its enforcement with more information about the total population of trees within city boundaries"* — the information this project produces. Recompense owed on undetected removal cannot be estimated, so the deterrent the ordinance describes is only partly real.

### 1.1 Verified facts (claims register)

Checked 2026-09-23 against the source listed. Repeat these figures exactly; anything not here is `[unverified]` per `AGENTS.md`.

| Claim | Figure | Source |
|---|---|---|
| Average annual canopy loss, City of Atlanta, 2008–2023 | "nearly 150 acres" a year; GT: "roughly .40 acres … per day" | AJC (Aug 2026); GT 2023 report §2.3 |
| Canopy cover, 2023 | 45.7% (39,830 acres); 46.5% in 2018; just under 48% in 2008 | GT 2023 report §2.3. SaportaReport printed 45.5% — use GT's figure |
| 2023 imagery | WorldView-2, 0.5 m pan-sharpened, 4-band, captured Sep 24, 2023; random forest; 95.6% overall accuracy | GT 2023 report §3.2–3.4 |
| 2018 imagery | WorldView-2, 6 ft pan-sharpened, Jul/Aug/Oct 2018; 2017 NAIP used under clouds; 93.2% accuracy | GT 2018 report |
| Change method | 500 ft × 500 ft (~5.75 acre) grid, ~15,800 cells; "only grid cells showing canopy change greater than 1 acre were examined" | GT 2023 report §4.4 |
| Known unpermitted removals, 2018–2023 | 5,471 trees "removed without a permit" (25% from one 22-acre site); vs 55,634 permitted for construction and 47,102 as dead/dying/hazardous | GT 2023 report §2.3, citing the City's database |
| Concentration of permitted removals | 2% of development sites removed 50% of trees permitted for removal | GT 2023 report; AJC |
| Enforcement model | complaint-based; "neighbors' complaints and arborists' drive-bys" | City Auditor, *Performance Audit: Tree Trust Fund*, Oct 2020 |
| Uncollected illegal-cutting fines | "over $2 million" assessed but uncollected, FY2009–FY2019 | City Auditor 2020 |
| Recompense | $140 per diameter-inch, effective Jan 1, 2026; inflation-indexed from 2027 `[unverified: indexing]` | Capital B (Jun 13, 2025) |
| Illegal-clearing fine | up to $200,000 per acre when the tree count cannot be determined (was $60,000); otherwise $500 first tree, $1,000 each after, plus replacement | Capital B (Jun 13, 2025); Fox 5 (Jun 11, 2025); 2020 audit for the old $60,000 |
| Report release | 2023 results publicly released Aug 2026; the city had the findings ~2 years earlier | AJC; SaportaReport |
| 2021 Georgia NAIP dates | 2021-10-07 to 2022-01-13 | NOAA InPort item 68396 |
| Resident reporting path | report to the Arborist Division with address, number of trees, and location | ATL311 KB0013006 |
| Permit search | Accela Citizen Access requires no login | Trees Atlanta, *How to Save a Tree* |

**Do not repeat:**
- The 2020 audit's "600,000 additional trees" estimate — it rests on the audit's own "0.08% canopy loss … amounting to nearly 7,000 acres," which is internally inconsistent (0.08% of the city is ~70 acres).
- The auditor's description of enforcement as current fact without the year. It predates the 2025–26 ordinance rewrite; nothing found shows the rewrite changed how violations are detected, but say "a 2020 audit."
- Any claim that the city's imagery is coarser than NAIP, that GT does not use ML, or that nobody checks permits. All three are false as of the 2023 study.

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
- **Precedent.** A 2024 comparison on free 2012 NAIP imagery in two southern US cities found U-Net best at 89.8% and 91.4% overall accuracy, ahead of SVM and random forest (Morgan et al., *Geomatics* 4(4):22; the SVM ~84% / RF ~76% figures are `[unverified]` — not in the abstract). A 2026 NAIP-only workflow (Yoo et al., Emory CS + USC, *Remote Sensing* 18(12):1899) reached **Dice 0.824** for canopy segmentation in two Los Angeles neighborhoods, with "encouraging evidence of transferability to previously unseen urban areas without retraining."

#### B. Bi-temporal / siamese change network — stretch goal

Feed both epochs into one network with shared encoders, predict change directly.

- **Why.** Learns to ignore nuisance differences (illumination, phenology, misregistration) rather than inheriting them.
- **Cost.** Needs *change* labels, not canopy labels. Nobody has published change labels for Atlanta, so every training example is hand-digitized. Heavy annotation burden at the point in the year with least momentum.
- **Verdict.** Second-semester comparison against the differencing baseline, not the primary pipeline.

---

## Sources

- [AJC — Atlanta has lost nearly 150 acres of tree canopy a year (Aug 2026)](https://www.ajc.com/news/2026/08/atlanta-has-lost-nearly-150-acres-of-tree-canopy-a-year-study-finds/)
- [Georgia Tech ATL UTC portal](https://geospatial.gatech.edu/AtlantaUTC/) · [2023 report](https://geospatial.gatech.edu/AtlantaUTC/AtlantaCanopyReport2023GT.pdf) — 0.5 m WorldView-2, >1-acre cell review, permit comparison, 5,471 unpermitted removals · [2018 final report](https://geospatial.gatech.edu/AtlantaUTC/2018FinalReport.pdf) — 6-acre grid cells, 939 loss cells, 93.2% accuracy, "false growth"
- [City Auditor — Performance Audit: Tree Trust Fund (Oct 2020)](http://www.atlaudit.org/uploads/3/9/5/8/39584481/performance_audit_-_tree_trust_fund-corrected.pdf) — complaint-based enforcement, >$2M uncollected illegal-cutting fines
- [SaportaReport — Atlanta's tree canopy hits new low](https://saportareport.com/atlantas-tree-canopy-hits-new-low/columnists/mariasmetro/maria_saporta/) · [Fox 5 — penalty increase (Jun 2025)](https://www.fox5atlanta.com/news/atlanta-could-triple-penalties-illegal-tree-removals-major-ordinance-overhaul)
- [ATL311 — reporting illegal removal on private property](https://www.atl311.com/en-US/knowledgearticle/?code=KB0013006) · [Trees Atlanta — How to Save a Tree](https://www.treesatlanta.org/resources/how-to-save-a-tree/) · [NOAA InPort — 2021 Georgia NAIP dates](https://www.fisheries.noaa.gov/inport/item/68396)
- [Georgia Tech News — 2023 method, random forest, Potential Planting Index](https://www.gatech.edu/news/2025/07/31/mapping-georgias-urban-forest-georgia-tech-tools-help-planners-prioritize-tree)
- [City of Atlanta — Tree Protection Ordinance statement](https://www.atlantaga.gov/Home/Components/News/News/15451/1338) · [Capital B — $140/inch, $200,000/acre](https://atlanta.capitalbnews.org/atlanta-tree-protection-ordinance-202/)
- [Rough Draft — DeKalb ordinance rewrite underway](https://roughdraftatlanta.com/2026/09/02/dekalb-tree-protection-ordinance-update/) · [DeKalb canopy report](https://www.dekalbcountyga.gov/news/dekalb-county-releases-new-urban-tree-canopy-report)
- [Pedley & Morgenroth — fine-scale canopy loss with deep learning](https://www.sciencedirect.com/science/article/pii/S2667393225000018)
- [Geomatics 2024 — U-Net vs SVM vs RF on NAIP](https://www.mdpi.com/2673-7418/4/4/22) · [Yoo et al. 2026 — NAIP canopy U-Net, Los Angeles](https://www.mdpi.com/2072-4292/18/12/1899)
- [NAIP-CHM 0.6 m canopy height model](https://www.nature.com/articles/s41597-026-07549-w) · [code and weights](https://github.com/smorf-ntsg/naip-chm) · [Georgia statewide LiDAR 2018–19](https://www.fisheries.noaa.gov/inport/item/67264)
- [California v. Ciraolo, 476 U.S. 207 (1986)](https://supreme.justia.com/cases/federal/us/476/207/)
- [Coconut Grove Spotlight — Miami canopy dispute](https://coconutgrovespotlight.com/2026/08/24/city-says-the-groves-tree-canopy-is-growing-not-all-are-convinced/)

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

### As an ML task

```
INPUT   NAIP 4-band tiles at t1 (Sep 2023) and t2 (Jul-Oct 2025), 60 cm
        Parcel polygons (Fulton, DeKalb)
        Tree-removal / land-disturbance permit records with dates

STAGE 1 f: tile -> binary canopy mask, per epoch
        semantic segmentation, evaluated by IoU on held-out NPUs

STAGE 2 g: (mask_t1, mask_t2) -> loss polygons >= 0.1 acre
        differencing + morphological cleanup + minimum mapping unit
        evaluated by precision/recall against hand-digitized polygons

STAGE 3 h: loss polygon -> parcel ID, area, estimated DBH-inches, cause class
        spatial join + rule layer + permit match
        evaluated by agreement with manual adjudication on a sample

OUTPUT  A ranked list of parcels with canopy loss and no matching permit,
        each carrying an area, a date window, and an estimated recompense value.
```

### Scope boundaries

**In scope.** City of Atlanta plus unincorporated DeKalb; two NAIP epochs; loss patches ≥ 0.1 acre; canopy defined as woody vegetation over ~3 m tall.

**Out of scope.** Canopy *gain* and net change (gain is harder and contaminated by the "false growth" problem); individual tree counting; species; exact DBH per tree; tree health.

**Deferred.** Real-time or annual monitoring — NAIP's two-year cycle cannot support it.

### Success criteria

| Stage | Metric | Target | Rationale |
|---|---|---|---|
| Canopy mask | IoU, spatially blocked holdout | ≥ 0.80 | Published NAIP canopy work lands at Dice ~0.82; higher-resolution work reaches 0.88 |
| Loss polygons | Precision | ≥ 0.90 | A false accusation is far costlier than a miss |
| Loss polygons | Recall | ≥ 0.70 | Matches what Pedley & Morgenroth accepted (0.81) after tuning for precision |
| Area estimate | MAE per parcel | < 15% | Tight enough that a recompense estimate is arguable |
| Reconciliation | Adjudicated sample | ≥ 50 parcels reviewed by hand | Establishes a rate, not an anecdote |
| Project | Real-world uptake | ≥ 1 agency briefed | Distinguishes a class project from a tool |

**A negative result is still a result.** If reconciliation finds that nearly all detected loss has a permit behind it, that is a publishable finding: it would mean Atlanta's canopy problem is legal clearing under a permissive ordinance rather than illegal clearing under weak enforcement, which shifts the policy recommendation entirely.

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

#### A. Post-classification comparison — **recommended**

Segment canopy independently in each epoch, then subtract.

- **Why.** Each mask is independently validatable, so when the change product is wrong you can tell which year was wrong. Tolerates the severe radiometric inconsistency between NAIP flight lines and years. Lets you reuse pretrained 4-band weights directly.
- **Cost.** Errors compound — two masks at 0.85 IoU do not give a change product at 0.85. Expect the change layer to be the weakest number you report, and say so.
- **Precedent.** A 2024 comparison on NAIP in two southern US cities found U-Net at 91.4% and 89.8% overall accuracy, beating SVM (~84%) and random forest (~76%).

#### B. Bi-temporal / siamese change network — stretch goal

Feed both epochs into one network with shared encoders, predict change directly.

- **Why.** Learns to ignore nuisance differences (illumination, phenology, misregistration) rather than inheriting them.
- **Cost.** Needs *change* labels, not canopy labels. Nobody has published change labels for Atlanta, so every training example is hand-digitized. Heavy annotation burden at the point in the year with least momentum.
- **Verdict.** Second-semester comparison against the differencing baseline, not the primary pipeline.

#### C. Height-differenced detection — partial

Compare canopy height surfaces rather than spectral masks.

- **Why.** Height is the most direct evidence a tree is gone, and it sidesteps "false growth" — scrub and pine regrowth reads as canopy to a spectral classifier but not as 10 m of height. The 2018 city study found 169 grid cells of exactly this illusory gain, roughly 500 acres.
- **Cost.** Real LiDAR exists for 2018–19 only. For 2023 and 2025 you would difference two runs of a model that predicts height from the same NAIP spectra you already used — not independent evidence.
- **Verdict.** Use height as an extra input channel and as a filter on the gain side, not as the detector.

### The benchmark

The closest published analogue is Pedley & Morgenroth's canopy-loss work in Christchurch, New Zealand: DeepLabv3+ with ResNet-101 on 7.5 cm aerial RGB plus LiDAR, reaching **F1 0.934, IoU 0.883**, with **precision 0.941 deliberately favoured over recall 0.811**, and MAE 2.81 m² at property scale. They found 14.5% of 2016 canopy gone by 2021, 74.9% of it on residential land. Note they explicitly detect loss only, not gain.

Be honest about the gap: they had 7.5 cm imagery and two LiDAR epochs at 6 and 20 points/m². You will have 60 cm imagery — eight times coarser — and one usable LiDAR epoch that predates your study window. **Their numbers are a ceiling, not a forecast.**

---

## 4. Implications

A canopy-loss detector is not a neutral map. It is an enforcement instrument pointed at private property.

### Legal — admissible, but that is not the same as sufficient

The constitutional question is settled favourably. In *California v. Ciraolo* (1986) the Supreme Court held that warrantless naked-eye observation of a fenced backyard from navigable airspace is not a search, reasoning that what any member of the public flying overhead could see carries no reasonable expectation of privacy. *Dow Chemical v. United States*, the same year, extended similar reasoning to aerial photography of an industrial site. NAIP is federal imagery already in the public domain, which is safer ground still.

The practical question differs. **A model output is an investigative lead, not evidence.** Enforcement needs a site visit, a dated record, and an inspector willing to testify. Frame the deliverable as triage — "these 40 parcels merit a look, in this order" — and you are solid. Frame it as a violation list and you have overpromised in a way a city attorney will notice.

### Equity — the tool finds loss wherever it looks hardest

The most serious risk and the one most likely to be raised by a reviewer. Canopy loss in Atlanta concentrates east, west and southwest of downtown — areas overlapping substantially with historically redlined, lower-income, majority-Black neighborhoods that also carry the city's highest heat burden. A $140-per-inch recompense bill lands very differently on a developer assembling parcels than on an elderly homeowner who took down a storm-damaged oak.

Two mitigations, both belonging in the writeup:

1. **Filter by scale and actor.** The 2023 study found half of all permitted removals happened on just 2% of sites, each clearing 100+ trees. A tool tuned to find those sites targets the actual driver and largely skips single-tree residential removal.
2. **Report performance disaggregated by neighborhood income and canopy density.** A model trained mostly on leafy north-side tiles will quietly perform worse on sparse south-side canopy, and nobody notices unless you measure it.

### Operational — detection creates work the city may not absorb

Several hundred candidate parcels a cycle handed to a handful of inspectors is a backlog, not a capability. Rank rather than list: order by estimated recompense value so the top of the list pays for the inspection time.

There is a false-positive asymmetry to design around. A missed violation costs some trees. A false accusation costs a resident an appeal, costs the agency credibility, and in a local-news cycle can kill the program. That asymmetry is why precision targets 0.90 and recall only 0.70.

### Ecological — area is a poor proxy for what was lost

The model measures canopy area. The ordinance prices diameter inches. The ecosystem cares about mature interior forest. An acre of 80-year-old hardwood and an acre of volunteer pine read nearly the same from above and are not equivalent in stormwater interception, cooling, or habitat. Giarrusso's point: regrowth on a stalled development site is not a genuine gain, and "once it's cleared, you don't get it back."

Responses: weight loss by canopy height so tall closed canopy counts for more than scrub, and **explicitly decline to report net change**, since gain and loss are not commensurable here. Reporting a net figure is how "false growth" enters the public record.

### Political — a credible number changes the argument, a shaky one ends it

Miami is the cautionary case. The city cited an AI-derived canopy assessment claiming a net gain; researchers and advocates showed the tool counted shrubs and invasives as trees, and the LiDAR-validated academic assessment became the accepted number. The lesson is not that the technique is unsound — it is that a canopy claim without independent validation will be attacked on exactly that ground, and the attack will succeed.

The upside is symmetric. DeKalb County is rewriting its tree protection ordinance now. A defensible parcel-scale loss map delivered into an active policy process is worth considerably more than the same map delivered into a vacuum.

### Limits — what this does not fix

Detection does not plant trees. Even perfect enforcement of the current ordinance does not reach the city's 50% goal, because much of the loss is legal: permitted removal under permissive zoning, which the 2025 ordinance debate left largely intact when preservation standards were deferred to a future zoning rewrite.

If reconciliation finds most loss is permitted, the honest conclusion is that **Atlanta's canopy problem is a policy-design problem wearing an enforcement costume** — and saying that clearly, with your own numbers behind it, is a stronger outcome than a slightly better IoU.

---

## 5. Open decisions

- **Geography.** City of Atlanta alone is cleaner (one ordinance, one permit system). Adding unincorporated DeKalb doubles data-access work but buys a live policy audience. *Recommendation: build on Atlanta, pitch DeKalb.*
- **Permit records.** File the Open Records Act request in week one regardless of geography. If it returns nothing usable by December, the project narrows to loss mapping without reconciliation — viable, less interesting. Know early.
- **Epoch pair.** 2023 against 2025, confirmed leaf-on per quad. Never 2021.
- **First contact.** Giarrusso's group at Georgia Tech — one conversation settles whether the canopy raster is available and what the city has said it wants between studies.

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

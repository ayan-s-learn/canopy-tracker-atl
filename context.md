# Project Context

**Everything established during scoping, including the paths not taken.**

This file is the research dossier behind `canopy-ledger.md` and `permits-and-pixels.md`. It exists so that (a) nobody has to re-derive the background, (b) a pivot to a different problem is cheap if canopy stalls, and (c) every number used in a presentation can be traced to a source.

| | |
|---|---|
| Last updated | 2026-09-18 |
| Research conducted | 2026-09-11 to 2026-09-18 |
| Method | ~60 web searches + ~90 page fetches, direct + 7 parallel research agents |

---

## 1. The assignment

A yearlong college research project: find and fix a problem relating to environmental issues affecting metro Atlanta, within three themes given by the course sponsor. The group's intended approach is an ML image-segmentation model, with USDA NAIP aerial photography suggested as the dataset.

### The three sponsor themes (verbatim summary)

1. **Maximizing urban greenspaces.** Urban land is 3% of the US but holds 80% of the population. City dwellers face poor air quality, water contamination, heat island effect, drought risk, storm vulnerability, and habitat loss. Identifying overlooked and underutilized greenspaces as potential green infrastructure and habitat is critical. Build the business case for municipalities to invest in neglected greenspaces.
2. **Improving soil health.** Soil as "brown infrastructure" — rainwater sponge and filtration system, reducing flooding and drought, decreasing surface temperatures, limiting particulate matter, supporting habitat. Urban soil is degraded by compaction, sealing, waste and contaminants, nutrient depletion. Identify green infrastructure solutions for metro Atlanta's dense acidic clay soils and demonstrate ROI at scale.
3. **Kudzu removal.** Introduced in the late 1800s as erosion control, now a noxious weed across an estimated 7M acres of the Southeast. Grows up to 1 ft/day, taproots to 6 ft. Chokes trees, breaks utility lines, decreases biodiversity, doubles nitrogen oxide emissions, worsens erosion. Control costs $200–$2,000/acre/year. Find low-impact, cost-effective removal methods and develop alternative plans for cleared fields.

### Selected direction

**Theme 1, canopy branch:** parcel-scale tree-canopy-loss detection with permit reconciliation. Selected 2026-09-11, confirmed 2026-09-18. Rationale and scoring in §2.

---

## 2. Options considered and why canopy won

Five candidate problems were scored on documented need, label availability, technical feasibility on NAIP, whether a real stakeholder would use the output, and whether a dollar case exists.

| Candidate | Theme | Need | Labels | Feasibility | Stakeholder | $ case |
|---|---|---|---|---|---|---|
| **A · Canopy loss & unpermitted clearing** | 1 (+2) | Strong | Free, abundant | High | Named, timely | $140/inch |
| B · Kudzu extent map | 3 | Inferred | Points only | Medium | Plausible | $500–2k/ac |
| C · Pervious/impervious/turf/bare-soil map | 1 + 2 | Strong | Bootstrappable | High | DWM fee | 4¢/ft²/yr |
| D · Exposed-soil / land-disturbance alerts | 2 | Indirect | Hand-digitize | Medium (timing) | Inspectors, CRK | Avoided dredging |
| E · Underutilized-greenspace candidate sites | 1 | Diffuse | Derived from C | High | Park Pride, TCF | Philly LandCare |

**Why A.** Strongest documented need, best free training labels, well-trodden technical path, a live policy window (DeKalb's ordinance rewrite), and a per-inch dollar figure to attach to every polygon.

**Why not B (kudzu), despite being the best fit to theme 3.** No public kudzu polygon map exists anywhere in Georgia to train from. Ground truth is points only, with ~100 m documented positional slop. The one prior Atlanta model scored 79.5% on independent points. No peer-reviewed deep-learning kudzu detector on aerial imagery exists — genuinely novel, but unproven. And critically: **no land manager is on record saying they need a kudzu map.** Kept as a viable second-semester experiment or added class (see §5).

---

## 3. Verified facts, with sources

Every figure here was confirmed by opening the source. Do not cite anything in §6 without re-verifying.

### Canopy and the ordinance

| Fact | Value | Source |
|---|---|---|
| Atlanta canopy 2008 | 47.9% (40,524 ac) | GT UTC baseline study |
| Atlanta canopy 2014 | 47.1% | GT UTC 2014 |
| Atlanta canopy 2018 | 46.5% (40,609 ac) | GT UTC 2018 |
| Atlanta canopy 2023 | 45.7% | GT UTC 2023 / AJC Aug 2026 |
| Annual net loss 2008–2023 | ~150 acres/year | AJC Aug 2026 |
| Council canopy goal | 50%, set 2023 | Multiple |
| Share of removals on 2% of sites | Half of all permitted removals | AJC Aug 2026 |
| Canopy on single-family land | 72–76% of city total, ~58% cover | GT UTC |
| Illegal removals, one year | 1,200+ | AJC |
| Recompense, 2026 ordinance | $140 per diameter-inch, CPI-indexed from 2027 | Capital B |
| Per-acre recompense caps | $12,500–$35,000 by zoning | Capital B |
| Illegal removal maximum | $200,000/acre | Capital B |
| Single-tree fines | $500 first, $1,000 subsequent | Capital B |
| Ordinance effective date | 1 January 2026 (passed 16 June 2025) | City of Atlanta |
| Permit trigger, private property | Trees ≥ 6 in DBH; free permits for dead/dying | ATCC |
| DeKalb canopy | 58% (2010) → 60% (2023), Eocene Environmental | DeKalb County |
| DeKalb ordinance rewrite | Underway Sept 2026 | Rough Draft Atlanta |

### The city's current monitoring method

| Fact | Value |
|---|---|
| Imagery | WorldView-2, ~1.8 m, 8-band, leaf-on |
| Classifier | ISODATA (2014/2018) → random forest (2023) |
| Classes | 3 — tree canopy / non-tree vegetation / non-vegetation |
| Change unit | ~6-acre grid cells, 500 ft × 500 ft |
| Change threshold | > 1 acre gained or lost per cell |
| 2018 result | 939 loss cells, 292 gain cells |
| Overall accuracy | 93.2% (2018), kappa 0.84; 91.8% (2014) |
| Field validation | 1,000+ visual inspections, 181 in-person visits (2018) |
| "False growth" | 169 cells (~500 ac) of scrub/pine regrowth misread as gain |
| 2023 additions | Potential Planting Index; 100+ field verification sites |
| Publication lag | 2023 imagery → report Aug 2026 (~34 months) |

### NAIP for Georgia

| Year | Acquired | GSD | Notes |
|---|---|---|---|
| 2015 | — | 1 m | 4-band |
| 2017 | ~5 Dec 2017 | 0.40 m native / 60 cm deliverable | Leaf-off |
| 2019 | 8 Sep – 20 Nov 2019 | 60 cm | Sep quads usable |
| 2021 | 7 Oct 2021 – 13 Jan 2022 | 60 cm | **Leaf-off, unusable** |
| 2023 | 12 Sep – 1 Nov 2023 | 60 cm | Best recent leaf-on |
| 2025 | 13 Jul – 16 Oct 2025 | 30 or 60 cm (GA unconfirmed) | Best available; USDA channels only |

Cadence: every two years since at least 2015, no gaps. Next expected 2027.

Catalog cutoffs: Planetary Computer ends 2023-12-31; Earth Engine ends 2023-11-17; AWS open-data buckets "2010 through 2023." The 2025 acquisitions are confirmed available through USDA channels, roughly half the states at 30 cm.

### Benchmarks from the literature

| Study | Data | Result |
|---|---|---|
| Pedley & Morgenroth (Christchurch NZ) | 7.5 cm RGB + LiDAR, DeepLabv3+/ResNet-101 | F1 0.934, IoU 0.883, precision 0.941, recall 0.811, MAE 2.81 m²; 14.5% canopy lost 2016–21, 74.9% residential; 15-day inference |
| Geomatics 2024 (Laurel MS, Georgetown TX) | NAIP 1 m and 50–60 cm | U-Net 91.4% / 89.8% OA; SVM ~84%; RF ~76% |
| Emory/USC (Los Angeles) | NAIP, U-Net + ResNet50 | Dice 0.824 |
| NAIP-CHM (CONUS) | NAIP 4-band, U-Net + CBAM/FiLM, 22.8M training pairs | RMSE 2.28 m, r² 0.87; 0.6 m output; CC-BY 4.0 |

### Legal

- *California v. Ciraolo*, 476 U.S. 207 (1986) — warrantless naked-eye aerial observation of a fenced backyard from navigable airspace is not a search. Reasoning: what any member of the public flying overhead could see carries no reasonable expectation of privacy.
- *Dow Chemical v. United States* (1986) — similar reasoning extended to aerial photography of an industrial site.
- O.C.G.A. § 50-18-71 — three business days; 10¢/page cap; staff time at lowest-paid qualified employee's prorated rate; first quarter hour free; **subsection (f) compels electronic production from databases**.

---

## 4. Wider metro Atlanta environmental context

Useful for framing, the business case, and any pivot.

### Heat

- Georgia Tech Urban Climate Lab produced Atlanta's first neighborhood heat-vulnerability assessment, July 2023, for Councilmembers Bakhtiari and Westmoreland. Highest-risk neighborhoods ~20% more likely to suffer heat illness. Citywide cool roofs plus canopy could cut heat-related hospital visits and deaths **70–80%**.
- UrbanHeatATL (GT + Spelman + West Atlanta Watershed Alliance, launched 2021): >1.5M mobile measurements. ~9°F between shaded West End streets (~90°F) and I-20 pavement (99°F) on 15 June 2022. English Avenue and Vine City hottest, lowest canopy.
- NASA Project ATLANTA: city up to 10°F hotter than rural surroundings; 17 sq mi downtown hot zone.
- Trees Atlanta surface readings, Reynoldstown: shaded sidewalk 90°F, unshaded lawn 99°F, street 138°F.
- The Nature Conservancy: tree planting could deliver 1.5°C cooling for 80,000+ residents at $3.1M/yr.
- Neither the UCL assessment nor UrbanHeatATL appears to have released a public GIS layer.

### Stormwater and soil

- Atlanta DWM is drafting an **impervious-surface stormwater fee**: ~4¢/sq ft → ~$36M/yr, against ~$200M/yr unmet need. No rate study in ~14 years; a 1999 attempt was struck down. Target: pass legislation in 2026. *An impervious fee requires parcel-level impervious mapping — directly adjacent to this project.*
- $14M Environmental Impact Bond funds six Proctor Creek GI projects targeting 55M gal/yr (~$0.25/gal capacity). $1M performance payment tied to a 6.52M-gal threshold verified Nov 2024.
- Combined sewer area is 11 sq mi of the core. Post-Development Stormwater Ordinance requires retention of the first 1 inch; ~5,200 GI practices permitted, designed for ~1.1 billion gallons.
- Atlanta DWM enforcement (cumulative ~2009–2021): 33,360 plan reviews, 245,389 site inspections, 11,255 stop-work orders, $827,861 in fines.
- Unvegetated Georgia road banks erode >350 tons/acre/yr vs ~7 on farmland. Prevention costs 10–15¢/yd³ vs $2.50–4.00/yd³ to dredge.
- Metro streams listed biota-impaired from urban runoff include Nancy Creek, North Fork Peachtree Creek, Proctor Creek, Johns Creek (Fulton); Crooked, Ivy, Level, Richland (Gwinnett); Nickajack, Olley (Cobb).
- Georgia EPD uses drones only for individual sites >400 acres. No systematic aerial screening of land clearing exists.
- UGA NARSAL: metro added impervious cover at ~55 acres/day (2001–2005). No statewide update since 2015.
- DeKalb bills stormwater by parcel impervious area (since 2004, $120/ERU/yr); Cobb started June 2026, using aerial photography for non-residential impervious.

### Greenspace and vacant land

- Center for Community Progress / Immergluck (2016): Atlanta's vacant and blighted properties cost $1.6–2.9M/yr in direct services, $55–153M in lost neighboring property value, $985K–$2.7M/yr in lost tax. No parcel count published.
- Metro Atlanta Land Bank 2022: 181 properties held ($13.6M), 188 banked, 336 parcels/interests pending; $168K/yr maintenance.
- Parking Reform Network: **25% of downtown Atlanta's developable land is parking**, vs 16% average for major metro cores. Polygons not openly downloadable.
- Trust for Public Land ParkScore 2026: Atlanta ranked 18/100, score 67.9. 84.6% within a 10-min walk (82,106 residents without). 7,024 park acres = 8.1% of the city (national median 15%). Neighborhoods of color have 16% less park space per person than the city average.
- Urban Ecology Framework (Biohabitats, 2019–20) produced recommendations; no public habitat-network GIS layer found.
- **No public land-cover map of Atlanta finer than 30 m separates turf, bare soil, impervious surface and water.** GT's product is 3 classes at ~1.8 m; ARC LandPro is 2012 parcel-level land *use*; NLCD is 30 m; the Chesapeake 1 m product does not extend to Georgia.

### Kudzu (the road not taken)

- **The "7 million acres" figure is not credible.** It traces to secondary sources with no survey behind it. Smithsonian reports the related "9 million" figure "appears to have been plucked from a small garden club publication." US Forest Service inventory finds ~227,000 acres of Southern forestland with any kudzu.
- Georgia: GFC "Dirty Dozen" reports 30,961 ac (2017) → 34,120 ac (2021), called "stable." The widely quoted 17% decline was sampling noise on ~48 FIA plots. These exclude non-forest land — roadsides, rights-of-way, vacant lots — where most metro kudzu lives.
- **No public polygon map of kudzu extent exists for Georgia or metro Atlanta.**
- Ground truth: EDDMapS holds points only, with documented ~100 m positional slop. GBIF returns ~996 occurrences in a metro bounding box, ~900 of them iNaturalist research-grade photos biased to trails and the BeltLine. Realistic usable seed count after dedup: ~600–1,000.
- Trees Atlanta treats ~500 acres of invasives annually and has named kudzu sites (South Bend Park 9.9 ac, Boulevard Crossing 1.5 ac, Chosewood, Perkerson) that likely exist as internal polygons. Worth asking.
- Control costs: goats ~$1,400–2,000/ac ($800 minimum); Roswell paid $1,300 for 33 goats × 10 days vs ~$10,000 quoted for herbicide; ORNL found ~$500–700/ac either method; USFS herbicide trials $55–173/ac chemical + $35–100/ac application. GFC cost-share pays $60/ac.
- Prior remote sensing: Jensen et al. 2020 (Sentinel-2 + AVIRIS, Atlanta) 97% internal but **79.5% external** from only 17 verified sites; Liang et al. 2020 (NAIP + LiDAR, Knox County TN) kappa 0.90 but on *early-spring "gray kudzu"* imagery, not leaf-on; Shen et al. 2021 (Sentinel-2 phenology unmixing) IoU 0.79, grassland the main confuser; Earth 2025 (Street View YOLO) mAP@50 0.46.
- Best detection season: August–September peak cover, or the post-frost "gray" signature. Main confusers: turf grass, wisteria, English ivy, Japanese honeysuckle, Chinese privet.
- **No peer-reviewed CNN segmentation of kudzu on aerial imagery exists.**

---

## 5. Stakeholders and contacts

| Who | Why they matter | Contact |
|---|---|---|
| **Tony Giarrusso**, GT School of City & Regional Planning | Ran all four Atlanta canopy studies. Associate Director, Center for Urban Resilience and Analytics. Can settle canopy-raster availability in one conversation. | Via GT planning directory |
| **Atlanta Arborist Division** | The primary user. Enforces the ordinance on private property. | `Arborist.dpcd@atlantaga.gov`, 404-330-6874, 55 Trinity Ave SW Suite 3800 |
| David Zaparanick | Arboricultural Manager | 404-330-6328 |
| **Trees Atlanta** | Runs restoration; heavy Esri GIS users; data manager James Moy. Published the TPO critique asking for a tree registry. | Via treesatlanta.org |
| **DeKalb County** | Rewriting its tree ordinance *now*. Commissioners Terry and Long Spears leading. | County commission offices |
| **Atlanta DWM** | Drafting the impervious stormwater fee — a natural second customer for a land-cover product. | atlantawatershed.org |
| Atlanta Tree Conservation Commission | Hears appeals; publishes FAQs; a natural advocate. | atlantatreecommission.com |
| Atlanta BeltLine Inc. | Tracks caliper-inch replacement with Trees Atlanta. | beltline.org |
| GT Urban Climate Lab (Brian Stone) | Heat vulnerability; potential co-analysis. | urbanclimate.gatech.edu |
| Park Pride / The Conservation Fund | Site prioritization for greening. | — |

**Precedent worth citing:** Georgia Tech's Data Science for Social Good program built parcel-level planting-prioritization and conservation web tools for Trees Atlanta and the Tree Conservation Commission in 2015 (dssgtrees.gatech.edu). A student team has done adjacent work before.

---

## 6. Explicitly unverified

Do not present any of these as established. Each is a task, not a fact.

- Whether the GT 2023 canopy **raster** downloads from the canopy hub or requires a request. The portal advertises a "canopy hub" for downloading data; the mechanism was not confirmed.
- The 2023 report's NPU-level tables and exact imagery acquisition dates.
- Georgia's 2025 NAIP ground sample distance (30 cm vs 60 cm) and whether it is ingested on any cloud catalog yet.
- Whether arborist reviews are embedded in building permit records under BB/LD prefixes since Aug 2020. **Reported, not confirmed. Test against Accela directly.**
- Whether the Tier 1 building-permits CSV contains a permit-type field that distinguishes tree or land-disturbance permits. The CSV was too large to inspect via fetch.
- Whether Accela's public search grid can be paged programmatically for Atlanta's tenant specifically.
- Arborist inspector headcount; annual violation and fine totals.
- Whether DeKalb publishes tree-permit records at all.
- Whether the Urban Ecology Framework or the heat-vulnerability assessment released GIS layers.
- Annual NPDES construction violation counts by metro county.
- EDDMapS per-county kudzu record counts (pages are JavaScript-rendered).
- Whether NASA DEVELOP's Georgia node has run an Atlanta canopy or kudzu project.

### Numbers circulating publicly that are wrong or unreliable

- **"Atlanta loses 50 acres per day"** — appears on Wikipedia, inconsistent with every primary study. The measured figure is ~150 acres/**year**.
- **Wikipedia's canopy series** (1974: 48%, 1996: 38%, 2004: 36%) conflicts with the GT studies and uses different baseline definitions. Use the GT series only.
- **"7 million acres of kudzu"** — see §4.
- **GFC's "17% kudzu decline"** — sampling noise on ~48 plots, not a trend.

---

## 7. Funding and recognition avenues

- USDA Forest Service National Urban & Community Forestry Challenge Cost-Share: $200K–$750K, universities eligible, but 2026 priority was wood utilization — weak fit.
- Georgia Forestry Commission Trees Across Georgia; Georgia Tree Council ReLeaf — small, local-partner-friendly.
- NFWF Five Star — funded Trees Atlanta's South Bend work; proven local match.
- NASA DEVELOP has a Georgia–Athens node.
- EPA Environmental Education grants — watch the next cycle.
- Note **Google Tree Canopy Lab already covers Atlanta** — a baseline to beat, not a funder. Austin's Google-assisted canopy work is a useful comparison; Miami's is a cautionary tale (see `canopy-ledger.md` §4).

---

## 8. Series of documents

| File | Purpose |
|---|---|
| `context.md` | This file — background, alternatives, verified facts, contacts |
| `canopy-ledger.md` | Problem statement, data audit, solution options, implications |
| `permits-and-pixels.md` | Permit access answer and ML implementation spec |
| `CLAUDE.md` | Working agreements and invariants for AI-assisted development |

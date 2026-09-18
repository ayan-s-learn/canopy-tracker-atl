# AGENTS.md

Working agreements for AI-assisted development on this repo. Read `context.md` for background, `canopy-ledger.md` for the problem definition, `permits-and-pixels.md` for the implementation spec.

> **Maintenance note.** Sections marked `TODO` are placeholders — fill them once the corresponding thing exists. Sections marked **STABLE** should not drift; if one becomes wrong, that is a real change to the project and deserves discussion, not a quiet edit. Suggestions for what to add over time are at the bottom.

---

## What this project is — STABLE

We detect tree-canopy loss at the parcel scale across metro Atlanta by segmenting successive USDA NAIP aerial imagery cycles, then reconcile detected loss against the City of Atlanta tree-removal permit record to surface clearing that has no permit behind it. This data will then be visualized on a public website for the project.

The city currently measures canopy change in ~6-acre grid cells with a 1-acre threshold, every ~5 years, published ~3 years late, with no permit reconciliation. We work at parcel scale, 0.1-acre threshold, on a 2-year cycle.

**One-sentence problem statement:**

> Metro Atlanta has no method that identifies tree-canopy loss at the parcel scale, attributes it to a property and a date, and reconciles it against the tree-removal permit record.

This is a yearlong 10th grade research project and the final outcome will be a website with a map that displays where illegal clearing is occuring. Deliverables are a working pipeline, a validated loss layer, and a briefing to at least one agency.

---

## Non-negotiables — STABLE

These are conclusions from scoping, not preferences. Changing one means revisiting `canopy-ledger.md`.

1. **Never use the 2021 NAIP epoch.** Georgia's 2021 flight ran 7 Oct 2021 – 13 Jan 2022 and is largely leaf-off. Differencing against it manufactures enormous phantom loss. The valid pair is 2023 (Sep) against 2025 (Jul–Oct).
2. **Always check per-quad acquisition dates before using a tile.** The statewide flight window does not apply uniformly. Late-October and later quads catch hardwood senescence.
3. **Precision over recall.** Targets are precision ≥ 0.90, recall ≥ 0.70. A false accusation against a property owner costs far more than a missed violation. Never tune the other way without a written reason.
4. **Spatially blocked evaluation only.** Group folds by NPU. Random tile splits put near-identical neighbouring tiles in train and test and inflate results by several points. Any metric produced from a random split is invalid and should not appear in a deliverable.
5. **Three buckets, never two.** Permit reconciliation emits matched / ambiguous / unmatched. Collapsing ambiguous into unmatched destroys agency trust permanently.
6. **Never publish a per-parcel dollar figure as if it were a bill.** The model measures canopy *area*; the ordinance prices *diameter inches*. Report a range with the stems-per-acre and mean-DBH assumptions printed alongside.
7. **Do not report net canopy change.** Gain and loss are not commensurable here — scrub and volunteer pine regrowth reads as canopy but is not equivalent. The city's own 2018 study found ~500 acres of this "false growth." We detect loss only.
8. **The output is triage, not evidence.** Language in every artifact: "these parcels merit inspection, in this order." Never "these parcels are in violation."
9. **Report performance disaggregated by neighborhood canopy density and income band.** A model trained mostly on dense north-side canopy will underperform on sparse south-side canopy. If we do not measure this, a reviewer will.

---

## Domain glossary

| Term | Meaning |
|---|---|
| **NAIP** | National Agriculture Imagery Program — USDA public-domain aerial imagery, 4-band RGB+NIR, 60 cm in Georgia, flown every 2 years |
| **NPU** | Neighborhood Planning Unit — Atlanta's citizen advisory districts; our unit for spatial cross-validation |
| **DBH** | Diameter at breast height — how the ordinance measures trees. Permit required at ≥ 6 in on private property |
| **Recompense** | The fee owed for removing a protected tree: $140 per diameter-inch under the ordinance effective 1 Jan 2026 |
| **MMU** | Minimum mapping unit — our 0.1-acre floor, which is 1,124 pixels at 60 cm |
| **CHM** | Canopy height model. We use NAIP-CHM, a 0.6 m CONUS product derived from 2022–23 NAIP |
| **DOQQ** | Digital Ortho Quarter Quad — NAIP's tile unit |
| **GSD** | Ground sample distance — pixel size on the ground |
| **Accela** | The permitting system the city runs. Atlanta's public tenant: `aca-prod.accela.com/ATLANTA_GA` |
| **ORA** | Georgia Open Records Act, O.C.G.A. § 50-18-71 |
| **False growth** | Scrub/pine regrowth on cleared land that a spectral classifier reads as canopy gain |

---

## Data sources and where they actually live — STABLE

| Input | Source | Gotcha |
|---|---|---|
| NAIP 2023 | Planetary Computer STAC, collection `naip` | Fine |
| **NAIP 2025** | **USDA NAIP GeoHub / EarthExplorer / NRCS Geospatial Data Gateway** | **Not in any cloud catalog.** PC ends 2023-12-31, GEE ends 2023-11-17, AWS ends 2023. Bulk download required |
| NAIP-CHM | Earth Engine asset + COGs, CC-BY 4.0 | Includes buildings — gate with NDVI |
| Georgia LiDAR | USGS 3DEP, 2018–19 | Leaf-off, 7+ years old |
| Parcels | Fulton and DeKalb county GIS | Boundary vintage vs imagery date |
| Building permits | ARC / City DCP GIS hub, 11.6 MB CSV, 2019–2024 | Ends 2024; building permits, not arborist records |
| Tree permits | Accela public grid (no login) + ORA request | See `permits-and-pixels.md` §1 |
| Sign postings | City arborist sign-postings page | Live only, no archive — scrape daily |
| GT canopy raster | Request from GT CSPAV | Validation only, never training truth |

If Georgia's 2025 NAIP arrives at 30 cm, **resample to 60 cm before differencing** or the two masks disagree for purely geometric reasons.

---

## Pipeline stages

```
P0  Acquire + verify per-quad dates
P1  Pseudo-labels: NAIP-CHM height > 3 m AND NDVI > 0.20
P2  Train U-Net (4-band) on 2023 only; fine-tune on hand-corrected tiles
P3  Co-register epochs with AROSICS, per quad, before inference
P4  Difference -> morphological opening -> MMU 1,124 px -> compactness < 60
P5  Spatial join to parcels -> classify cause -> permit match
P6  Blocked evaluation + hand-digitized validation + field checks
```

**The model is trained once, on 2023, and run frozen on both epochs.** This is deliberate: differencing two outputs of one model cancels systematic bias. Do not introduce a separately-trained 2025 model.

Radiometric augmentation (per-channel brightness, contrast, gamma) is the primary regularizer, not a nicety. NAIP radiometry varies visibly between adjacent flight lines within a single year.

---

## Repo layout

```
TODO — fill in once the structure settles. Suggested:

data/           # gitignored; raw and interim rasters
  raw/
  interim/
  processed/
notebooks/      # exploration only; nothing load-bearing
src/
  acquire/      # STAC + USDA bulk download, tile indexing
  labels/       # pseudo-label generation, annotation helpers
  models/       # architecture, training loop, inference
  change/       # co-registration, differencing, filtering
  attribute/    # parcel join, cause classification, permit match
  eval/         # blocked CV, metrics, disaggregated reporting
docs/           # canopy-ledger.md, permits-and-pixels.md, context.md
outputs/        # loss polygons, figures, tables
tests/
```

---

## Working with Claude on this repo

- **Cite or flag.** When adding a factual claim to any document, either cite a source we have verified or mark it `[unverified]`. `context.md` §6 lists what is known to be unverified and which public numbers are wrong — check it before repeating a figure.
- **Do not invent accuracy numbers or dataset properties.** If a benchmark or a dataset field is not in `context.md`, say so rather than estimating.
- **Prefer editing the existing docs over creating new ones.** The four-document structure is intentional.
- **When code and spec disagree, the spec is a hypothesis and the code is the evidence.** Update the spec.
- TODO — add: preferred Python style, whether we use type hints, test expectations, notebook hygiene rules.

---

## Suggested additions as the project develops

Things worth adding to this file later, roughly in the order they will become relevant.

**Soon**
- **Commands.** The handful of commands someone actually runs: environment setup, download, train, infer, evaluate. This is usually the highest-value section of a CLAUDE.md and it does not exist yet because the code does not.
- **Environment.** Python version, whether conda or uv or venv, how to get GDAL working (it is always the painful one), GPU expectations.
- **The chosen CRS**, once decided, stated once and referenced everywhere.
- **Where large files live** and how a new team member gets them.

**Once there is code**
- **Module map.** One line per module saying what it owns, so an AI editing `src/change/` knows not to reach into `src/models/`.
- **Test strategy.** What is actually tested — probably geometry math, tile indexing, and the permit-matching date logic, since those are where silent bugs hide.
- **Known-good reference outputs.** A small fixture area with a hand-checked expected result, so refactors can be verified.

**Once there are results**
- **Current metrics table**, with split names, updated as models improve. Prevents anyone quoting a stale number in a presentation.
- **Decisions log.** Short dated entries: what was decided, why, what was rejected. Invaluable when a reviewer asks "why 0.1 acre?" in April.
- **Failure inventory.** The specific things that went wrong and the fix, beyond the generic table in the spec.

**For the writeup**
- **Figure and table inventory** — which script generates which figure, so regenerating the deck is one command.
- **Claims register.** Every factual claim in the final paper mapped to its source or to the analysis that produced it. Start this early; reconstructing it in week 29 is miserable.
- **Stakeholder contact log.** Who was contacted, when, what they said. Both for the writeup and so two group members do not email the same person twice.

**Worth considering**
- A `SECURITY.md` or a note on handling permit data: it contains addresses tied to named property owners. Decide early whether the public repo publishes parcel-level results or only aggregates, and write that decision down here.
- A short note on **what to do if the ORA request fails**, so nobody has to re-reason it under time pressure. The fallback is Tier 5 in `permits-and-pixels.md`.

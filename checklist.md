# Canopy Tracker ATL — plan and current state

Updated **2026-11-23, America/New_York**. Integration owner: **Codex campaign lead**. Integrated scope: **T01–T04 on `main`**. Follow [AGENTS.md](AGENTS.md); necessary human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). This is the single state entry point; linked task/run records hold detail.

## Objective and current evidence

Build a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output is **inspection triage with uncertainty**, never a finding of violation.

Current direction remains **City of Atlanta first**, including its parts in both counties, with a varied pilot before regional findings. Prefer 2023→2025 if usable; investigate 2019→2023 or another justified fallback. Compare practical methods before committing to U-Net. Measure endpoint-visible loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. These methods/intervals are revisable hypotheses; [research direction](docs/research-direction.md) preserves the scientific standards and tradeoffs.

**Known:** GT already maps fine-resolution canopy, uses ML/manual corrections and compares some permits; our proposed contribution is validated smaller-event analysis and a reproducible evidence trail. T01 retrieved four-band October 2023 and October 2025 NAIP imagery at Piedmont Park and West End. The pair supports local development. Citywide coverage and registration remain open. [Sample windows and evidence](docs/research/imagery/T01.md). Public building and selected arborist records are accessible. Coverage of tree authorizations remains unverified. [T03 evidence](docs/research/permits/T03.md). These are scoped observations, not full-city readiness.

**Absent:** full study dataset, independent reference labels, measured detector accuracy, usable permit snapshot, operational pipeline, verified storage for raw imagery and model weights, and public release. **Jobs:** none running. T01 sample retrieval and review finished. Compact evidence is recorded in the repository; GT PDFs are recoverable by source URL/hash. No automated goal runtime, watcher or restart service has been established.

**Human actions:** [HA-0001](HUMAN_ACTIONS.md#ha-0001--send-the-tier-4-draft) fulfilled on owner confirmation. [HA-0002](HUMAN_ACTIONS.md#ha-0002--confirm-city-receipt-or-file-scoped-records-requests) ready to confirm City receipt or file the missing scopes.

**Next Astra project review:** [AR01 — feasibility findings and next work](docs/project-reviews.md#ar01--feasibility-findings-and-next-work), is due. The four task records below supply its evidence. Astra will define the next round and AR02 trigger. The [initial layout](docs/project-reviews.md#initial-layout--t01t04-astra-2026-10-15) covers T01–T04 only; feasibility remains unreviewed. See the [glossary](docs/glossary.md) for domain terminology.

## Ready work and ownership

Each brief specifies inputs, outputs, checks and suggested write paths. Set finite launch budgets from actual capacity/provider limits and coordinate shared resources before simultaneous jobs.

| ID | Useful next inquiry | Status / claimant | Starting evidence / next action |
|---|---|---|---|
| [T01](docs/task-contracts.md#t01--verify-candidate-imagery-intervals) | Imagery access, dates and paired samples | complete — Codex, `codex/t01-imagery` ([findings and recovery](docs/research/imagery/T01.md)) | Two 2023/2025 sample pairs read and independently checked. Fresh downloads reproduced all four TIFFs byte for byte. Both sites are in Fulton. |
| [T02](docs/task-contracts.md#t02--establish-geography-parcels-and-comparison-layers) | Jurisdiction, parcels and GT layers | complete — Codex, `codex/t02-geography`, 2026-11-23 | [Findings and replay](docs/research/geography/T02.md). Official City footprint archived, both county overlays and parcel samples checked. GT 2023 raster read. Parcel history, historical City jurisdiction and GT reuse remain open. |
| [T03](docs/task-contracts.md#t03--audit-permit-sources-and-temporal-meaning) | Permit feasibility, coverage and semantics | public-source audit complete — Codex, `codex/t03-permit-audit` | [Public-source audit and request package](docs/research/permits/T03.md). HA-0002 carries forward City receipt and historical records for standalone DDH, embedded reviews, amendments and public trees. Both county denominators remain unknown. |
| [T04](docs/task-contracts.md#t04--establish-a-minimal-reproducible-environment-and-durable-artifact-path) | Reproducible operation and durable storage | complete — Codex, `codex/t04-reproducible-runtime` | Fresh fixture replay and hash-verified GitHub retrieval of a compact derived GeoTIFF. [Checks and recovery limits](docs/operations.md#t04--runtime-and-artifact-recovery). |

A ready brief is not a scheduled job. When claiming one, record its owner, branch/checkout, write reservation, status and linked launch/evidence record here or in a reserved section.

## Future workstreams — revisable, unclaimed

These workstreams outline future questions. Astra reviews help turn the next useful work into ready briefs.

| Workstream | Useful preparation | Evidence needed for accepted results |
|---|---|---|
| Study agreement | Reconcile boundary, imagery interval and interfaces as sources become available | Versioned scope, usable inputs, honest coverage and recovery |
| Reference and evaluation | Draft protocols/tools; prepare independent component references | Protected exclusions, reviewed sampling and targets, actual references and independent reproduction |
| Preparation and detection | Inspect paired images; compare practical methods on development data | Suitable imagery, controlled comparisons and frozen versions for protected evaluation |
| Parcels and permits | Draft requests for known gaps; normalize available records and test geometry/matching | Coverage-aware relations, explicit ambiguity and complete regional accounting for regional claims |
| Public explanation | Prototype the review workflow with synthetic/development data | Supported findings, rights/handling decision and authorized publication |
| Agency use | Draft methods, briefing and feedback questions | Authorized communication and actual delivery of supported findings |
| Reproduction and maintenance | Test artifact retrieval and component reruns throughout development | Demonstrated pipeline rerun, retention/custody and correction responsibilities |
| Future direction | Assess a new interval or jurisdiction when evidence warrants | Appropriate sources, validation and authority for expansion |

## Readiness and unresolved decisions

See [research direction](docs/research-direction.md#evidence-gates-and-recoverability) for the scientific gate definitions.

| Gate | Required evidence | Current state |
|---|---|---|
| G1 — study feasible | Suitable readable paired inputs, scoped geography/source interfaces and recoverable artifacts | Unpassed; two paired sites and a current City footprint verified. Epoch-specific jurisdiction, parcel history, permit coverage, reference planning and bulk artifact recovery remain open |
| G2 — evaluation candidate selected | Controlled development evidence, reviewed protocol/reference capacity, pinned method and inputs | Unpassed; method/MMU/registration policy unchosen |
| G3 — findings validated | Appropriate independent references, uncertainty/coverage, protected evaluation and independent numerical reproduction | Unpassed; no project accuracy measurements |
| G4 — delivered and maintainable | Supported reviewable bundle, authorized public result, delivered agency briefing and tested rerun | Unpassed; no release or briefing |

Unresolved: recent-image coverage and suitability across the city; valid-area denominator; parcel history; effective-dated permit coverage; reference effort; local detection scale/registration limits; useful review yield/subgroup precision; storage for raw imagery and model weights; public detail, project license and future custodian.

## Launch ready work

Use the [task briefs](docs/task-contracts.md) and [working agreement](AGENTS.md#start-or-resume) when claiming new work.

## Next action

AR01 is due. Bring the four linked task records, the open G1 evidence gaps and HA-0002 to the review. The next imagery question is paired coverage of the official City footprint in both counties. When the City delivers records, verify their scope before interpreting permit absences.

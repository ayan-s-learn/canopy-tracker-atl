# Canopy Tracker ATL — plan and current state

Integration owner: **Codex campaign lead**. Follow [AGENTS.md](AGENTS.md); necessary human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). This is the single state entry point; each task's folder under [tasks/](tasks/) holds its brief and evidence. Only the integration owner edits this file.

## Objective and current evidence

Build a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output is **inspection triage with uncertainty**, never a finding of violation.

Current direction remains **City of Atlanta first**, including its parts in both counties, with a varied pilot before regional findings. Prefer 2023→2025 if usable; investigate 2019→2023 or another justified fallback. Compare practical methods before committing to U-Net. Measure endpoint-visible loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. These methods/intervals are revisable hypotheses; [research direction](docs/research-direction.md) preserves the scientific standards and tradeoffs.

**Known:** GT already maps fine-resolution canopy, uses ML/manual corrections and compares some permits; our proposed contribution is validated smaller-event analysis and a reproducible evidence trail. Both recent NAIP catalogs cover the full 2026 City footprint. Four sampled windows returned usable four-band pairs for development, including Kirkwood in DeKalb. Citywide pixel suitability and local registration remain open. [Coverage and sample evidence](tasks/T05-paired-coverage/README.md). Public building and selected arborist records are accessible. Coverage of tree authorizations remains unverified. [T03 evidence](tasks/T03-permits/README.md). These are scoped observations, not full-city readiness.

**Absent:** full study dataset, independent reference labels, measured detector accuracy, usable permit snapshot, operational pipeline, verified storage for raw imagery and model weights, and public release. **Jobs:** none running. Compact evidence is recorded in the repository; GT PDFs are recoverable by source URL/hash. No automated goal runtime, watcher or restart service has been established.

**Human actions:** [HA-0002](HUMAN_ACTIONS.md#ha-0002--confirm-city-receipt-or-file-scoped-records-requests) remains ready for confirmation or filing. [HA-0003](HUMAN_ACTIONS.md#ha-0003--assign-development-calibration-readers) is ready for interpreter assignment.

**Next Astra project review:** [AR03 — does the baseline warrant a method comparison?](docs/project-reviews.md#ar03--does-the-baseline-warrant-a-method-comparison) is ready. The [four-site baseline](tasks/T08-development-baseline/README.md#result) produced 20 uncorrected candidates ≥0.10 acre. None of the six exposure sides had adequate registration controls. [AR02](docs/project-reviews.md#ar02--pilot-footprint-and-reference-feasibility) reserved the T06 context blocks and selected development calibration. The eligible evaluation frame, reference protocol and staffing remain open.

## Tasks

| ID | Question | Status |
|---|---|---|
| [T01](tasks/T01-imagery/README.md) | Imagery access, dates and paired samples | complete |
| [T02](tasks/T02-geography/README.md) | Jurisdiction, parcels and GT layers | complete |
| [T03](tasks/T03-permits/README.md) | Permit feasibility, coverage and semantics | complete |
| [T04](tasks/T04-runtime/README.md) | Reproducible operation and durable storage | complete |
| [T05](tasks/T05-paired-coverage/README.md) | Where do the 2023 and 2025 assets overlap, and where has a usable pair actually been read? | complete |
| [T06](tasks/T06-reference-design/README.md) | Which geography can be protected, and how much independent reference work would the pilot require? | complete |
| [T07](tasks/T07-historical-geography/README.md) | Which parts of the City footprint have verified membership at the local image dates? | complete |
| [T08](tasks/T08-development-baseline/README.md) | Does a reproducible loss baseline survive registration checks on the four sites? | complete |
| [T09](tasks/T09-calibration-package/README.md) | Can the development assignment be delivered, returned privately and scored in a dry run? | complete |
| [T10](tasks/T10-parcel-vintages/README.md) | Which historical parcel links are supportable at the pilot sites? | ready |

## Future workstreams — revisable, unclaimed

These workstreams outline future questions. Astra reviews help turn the next useful work into ready tasks.

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
| G1 — study feasible | Suitable readable paired inputs, scoped geography/source interfaces and recoverable artifacts | Unpassed. Four paired development sites and the current City footprint are verified. Dated T07 membership supports all four pilot reservations at their tile dates. Boundary changes with missing dates or geometry, parcel history, permit coverage, reference planning and bulk artifact recovery remain open |
| G2 — evaluation candidate selected | Controlled development evidence, reviewed protocol/reference capacity, pinned method and inputs | Unpassed; method/MMU/registration policy unchosen |
| G3 — findings validated | Appropriate independent references, uncertainty/coverage, protected evaluation and independent numerical reproduction | Unpassed; no project accuracy measurements |
| G4 — delivered and maintainable | Supported reviewable bundle, authorized public result, delivered agency briefing and tested rerun | Unpassed; no release or briefing |

Unresolved: citywide pixel suitability and valid-observation area; parcel history; effective-dated permit coverage and its denominator in each county portion; Georgia Tech data reuse terms; reference effort; local detection scale/registration limits; useful review yield/subgroup precision; storage for raw imagery and model weights; public detail, project license and future custodian.

## Next action

Run AR03 with the T08 registration evidence and the requirement for spatially distributed, independent stable-ground controls. T10 can proceed on the pinned development inputs. Before any new or expanded development read, publish its full influence footprint and check disjointness against the reserved T06 context plus its 600 m guard. On City delivery under HA-0002, open a task to validate the export.

# Canopy Tracker ATL — plan and current state

Integration owner: **Codex campaign lead**. Follow [AGENTS.md](AGENTS.md); necessary human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). This is the single state entry point; each task's folder under [tasks/](tasks/) holds its brief and evidence. Only the integration owner edits this file.

## Objective and current evidence

Build a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output is **inspection triage with uncertainty**, never a finding of violation.

Current direction remains **City of Atlanta first**, including its parts in both counties, with a varied pilot before regional findings. Prefer 2023→2025 if usable; investigate 2019→2023 or another justified fallback. Compare practical methods before committing to U-Net. Measure endpoint-visible loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. These methods/intervals are revisable hypotheses; [research direction](docs/research-direction.md) preserves the scientific standards and tradeoffs.

**Known:** GT already maps fine-resolution canopy, uses ML/manual corrections and compares some permits; our proposed contribution is validated smaller-event analysis and a reproducible evidence trail. Both recent NAIP catalogs cover the full 2026 City footprint. Four sampled windows returned usable four-band pairs for development, including Kirkwood in DeKalb. Citywide pixel suitability and local registration remain open. [Coverage and sample evidence](tasks/T05-paired-coverage/README.md). Public building and selected arborist records are accessible. Coverage of tree authorizations remains unverified. [T03 evidence](tasks/T03-permits/README.md). These are scoped observations, not full-city readiness.

**Absent:** full study dataset, independent reference labels, measured detector accuracy, usable permit snapshot, operational pipeline, verified storage for raw imagery and model weights, and public release. **Jobs:** none running. Compact evidence is recorded in the repository; GT PDFs are recoverable by source URL/hash. No automated goal runtime, watcher or restart service has been established.

**Human actions:** [HA-0002](HUMAN_ACTIONS.md#ha-0002--confirm-city-receipt-or-file-scoped-records-requests) is ready: confirm City receipt or file the missing scopes.

**Next Astra project review:** [AR02 — pilot footprint and reference feasibility](docs/project-reviews.md#ar02--pilot-footprint-and-reference-feasibility) is ready with the T05 coverage ledger and four development windows, plus the [T06 candidate exclusion map](tasks/T06-reference-design/split.geojson) and [reference workload estimate](tasks/T06-reference-design/README.md#staffing-and-decision). Use AR02 to decide whether to reserve the candidate blocks, run the development baseline or a bounded imagery fallback, and select the proposed development-only calibration. Frame freeze, protocol adoption and staffing remain pending.

## Tasks

| ID | Question | Status |
|---|---|---|
| [T01](tasks/T01-imagery/README.md) | Imagery access, dates and paired samples | complete |
| [T02](tasks/T02-geography/README.md) | Jurisdiction, parcels and GT layers | complete |
| [T03](tasks/T03-permits/README.md) | Permit feasibility, coverage and semantics | complete |
| [T04](tasks/T04-runtime/README.md) | Reproducible operation and durable storage | complete |
| [T05](tasks/T05-paired-coverage/README.md) | Where do the 2023 and 2025 assets overlap, and where has a usable pair actually been read? | complete |
| [T06](tasks/T06-reference-design/README.md) | Which geography can be protected, and how much independent reference work would the pilot require? | complete |
| [T07](tasks/T07-historical-geography/README.md) | Which parts of the City footprint have verified membership at the local image dates? | ready |

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
| G1 — study feasible | Suitable readable paired inputs, scoped geography/source interfaces and recoverable artifacts | Unpassed; four paired development sites and a current City footprint verified. Epoch-specific jurisdiction, parcel history, permit coverage, reference planning and bulk artifact recovery remain open |
| G2 — evaluation candidate selected | Controlled development evidence, reviewed protocol/reference capacity, pinned method and inputs | Unpassed; method/MMU/registration policy unchosen |
| G3 — findings validated | Appropriate independent references, uncertainty/coverage, protected evaluation and independent numerical reproduction | Unpassed; no project accuracy measurements |
| G4 — delivered and maintainable | Supported reviewable bundle, authorized public result, delivered agency briefing and tested rerun | Unpassed; no release or briefing |

Unresolved: citywide pixel suitability and valid-observation area; parcel history; effective-dated permit coverage and its denominator in each county portion; Georgia Tech data reuse terms; reference effort; local detection scale/registration limits; useful review yield/subgroup precision; storage for raw imagery and model weights; public detail, project license and future custodian.

## Next action

Run AR02 with the T05 and T06 evidence and any available T07 findings. T07 can proceed independently. Before reading any new development imagery, reserve its full influence footprint and check it against the T06 candidate context plus its 600 m guard. If AR02 selects the calibration, prepare the development assignment and return package and register the staffing request in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). On City delivery under HA-0002, open a task to validate the export. Historical parcel-vintage checks remain on the parcels workstream before parcel attribution.

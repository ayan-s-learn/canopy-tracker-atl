# Canopy Tracker ATL — plan and current state

Updated **2026-10-15, America/Los_Angeles**. Integration owner: **Codex campaign lead**, coordinating through [PR #2](https://github.com/ayan-s-learn/canopy-tracker-atl/pull/2). Campaign branch: **`chore/autonomous-harness`**. Follow [AGENTS.md](AGENTS.md); necessary human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). This is the single state entry point; linked task/run records hold detail.

## Objective and current evidence

Build a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output is **inspection triage with uncertainty**, never a finding of violation.

Current direction remains **City of Atlanta first**, including its parts in both counties, with a varied pilot before regional findings. Prefer 2023→2025 if usable; investigate 2019→2023 or another justified fallback. Compare practical methods before committing to U-Net. Measure endpoint-visible loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. These methods/intervals are revisable hypotheses; [research direction](docs/research-direction.md) preserves the scientific standards and tradeoffs.

**P00 is complete:** archive/GT review, live catalog inquiry, initial plan and independent review. Evidence is in [planning findings](docs/research/2026-10-14-planning/findings.md) and [original review](docs/research/2026-10-14-planning/review.md); checkpoint `c0f4a78` preserves that version. **P01 is complete:** local agent autonomy, shared integration and detail only for ready work, as clarified by the owner; independently reviewed and merged/pushed by the Sol agent. See [D02 and review record](docs/decisions/decentralized-planning.md). No substantial pipeline implementation has begun.

**Known:** GT already maps fine-resolution canopy, uses ML/manual corrections and compares some permits; our proposed contribution is validated smaller-event analysis and a reproducible evidence trail. The saved rectangle query returned 25 October 7–8, 2023 NAIP items and no 2025 items; actual recent pixels remain unacquired. Permit access/completeness is unproven. These are scoped observations, not full-city readiness.

**Absent:** acquired research dataset, independent reference labels, measured detector accuracy, usable permit snapshot, operational pipeline, proven durable raster/model storage and public release. **Jobs:** none running; earlier metadata/report probes finished. Compact evidence is tracked; GT PDFs are recoverable by source URL/hash. No automated goal runtime, watcher or restart service has been established.

**Human actions:** none ready or blocking the first inquiries. Agents prepare concrete packages when access/storage, independent annotation, publication/communications or briefing delivery actually need a human. Do not create requests for routine local planning changes.

**Next Astra project review:** [AR01 — feasibility findings and next work](docs/project-reviews.md#ar01--feasibility-findings-and-next-work), planned after T01–T04 complete (earlier for a material blocker or change in direction). The integration owner prepares it; Astra defines the next round and AR02 trigger. No review has been held. See the [glossary](docs/glossary.md) for domain terminology.

## Ready work and ownership

The following four inquiries remain independently claimable. Each brief specifies inputs, outputs, checks and suggested write paths. Set finite launch budgets from actual capacity/provider limits and coordinate shared resources before simultaneous jobs.

| ID | Useful next inquiry | Status / claimant | Starting evidence / next action |
|---|---|---|---|
| [T01](docs/task-contracts.md#t01--verify-candidate-imagery-intervals) | Imagery access, dates and paired samples | ready — unclaimed | Saved catalog/error evidence; locate actual recent assets and read a bounded sample |
| [T02](docs/task-contracts.md#t02--establish-geography-parcels-and-comparison-layers) | Jurisdiction, parcels and GT layers | ready — unclaimed | Source leads/GT report; retrieve boundary and share it before finishing every source inquiry |
| [T03](docs/task-contracts.md#t03--audit-permit-sources-and-temporal-meaning) | Permit feasibility, coverage and semantics | ready — unclaimed | Recorded errors/official guidance; inspect accessible source metadata and diverse records |
| [T04](docs/task-contracts.md#t04--establish-a-minimal-reproducible-environment-and-durable-artifact-path) | Reproducible operation and durable storage | ready — unclaimed | Provisioned environment/permitted fixture; prove environment and storage capabilities separately |

A ready brief is not a scheduled job. When claiming one, record its owner, branch/checkout, write reservation, status and linked launch/evidence record here or in a reserved section.

## Future workstreams — revisable, unclaimed

These workstreams outline future questions. Astra reviews help turn the next useful work into ready briefs. [Earlier task sketches](docs/task-contracts.md#earlier-task-sketches) remain available as history.

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
| G1 — study feasible | Suitable readable paired inputs, scoped geography/source interfaces and recoverable artifacts | Unpassed; metadata evidence only |
| G2 — evaluation candidate selected | Controlled development evidence, reviewed protocol/reference capacity, pinned method and inputs | Unpassed; method/MMU/registration policy unchosen |
| G3 — findings validated | Appropriate independent references, uncertainty/coverage, protected evaluation and independent numerical reproduction | Unpassed; no project accuracy measurements |
| G4 — delivered and maintainable | Supported reviewable bundle, authorized public result, delivered agency briefing and tested rerun | Unpassed; no release or briefing |

Unresolved: recent-image suitability/access; valid-area denominator; parcel history; effective-dated permit coverage; reference effort; local detection scale/registration limits; useful review yield/subgroup precision; durable storage; public detail, project license and future custodian.

## Launch ready work

Read AGENTS.md and current state, claim an item, and use its [ready brief](docs/task-contracts.md). A bounded prompt is sufficient: `/goal Complete T01 under its ready brief and AGENTS.md`; substitute T02, T03 or T04 as appropriate.

## Next action

Setup reviews are complete and [PR #2](https://github.com/ayan-s-learn/canopy-tracker-atl/pull/2) is open. Next, claim T01–T04. Resume through [AGENTS.md](AGENTS.md#start-or-resume). Full delivery requires validated findings, the authorized public result, an actual agency briefing and a reproducible maintenance handoff.

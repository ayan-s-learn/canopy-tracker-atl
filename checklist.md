# Canopy Tracker ATL — plan and current state

Updated **2026-10-14, America/Los_Angeles**. Integration owner: **Codex research lead (this chat)**. Campaign branch: **`chore/autonomous-harness`**. Last revision: **`chore/decentralized-planning`**, reviewed and merged at `02d27eb`. Follow [AGENTS.md](AGENTS.md); necessary human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). This is the single state entry point; linked task/run records hold detail.

## Objective and current evidence

Build a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output is **inspection triage with uncertainty**, never a finding of violation.

Current direction remains **City of Atlanta first**, including its parts in both counties, with a varied pilot before regional findings. Prefer 2023→2025 if usable; investigate 2019→2023 or another justified fallback. Compare practical methods before committing to U-Net. Measure endpoint-visible loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. These methods/intervals are revisable hypotheses; [research direction](docs/research-direction.md) preserves the scientific standards and tradeoffs.

**P00 is complete:** archive/GT review, live catalog inquiry, initial plan and independent review. Evidence is in [planning findings](docs/research/2026-10-14-planning/findings.md) and [original review](docs/research/2026-10-14-planning/review.md); checkpoint `c0f4a78` preserves that version. **P01 is complete:** local agent autonomy, shared integration and detail only for ready work, as clarified by the owner; independently reviewed and merged/pushed by the Sol agent. See [D02 and review record](docs/decisions/decentralized-planning.md). No substantial pipeline implementation has begun.

**Known:** GT already maps fine-resolution canopy, uses ML/manual corrections and compares some permits; our proposed contribution is validated smaller-event analysis and a reproducible evidence trail. The saved rectangle query returned 25 October 7–8, 2023 NAIP items and no 2025 items; actual recent pixels remain unacquired. Permit access/completeness is unproven. These are scoped observations, not full-city readiness.

**Absent:** acquired research dataset, independent reference labels, measured detector accuracy, usable permit snapshot, operational pipeline, proven durable raster/model storage and public release. **Jobs:** none running; earlier metadata/report probes finished. Compact evidence is tracked; GT PDFs are recoverable by source URL/hash. No automated goal runtime, watcher or restart service has been established.

**Human actions:** none ready or blocking the first inquiries. Agents prepare concrete packages when access/storage, independent annotation, publication/communications or briefing delivery actually need a human. Do not create requests for routine local planning changes.

## How work is chosen and revised

Workstream owners select useful work, choose methods, split/revise local tasks and coordinate directly with affected peers within existing scope and authority. The integrator keeps shared interfaces, state, resource conflicts, evidence promotion and campaign merges coherent. It is not a permission queue for every method or batch.

Before substantive work, confirm a visible claim/write reservation and record the bounded objective, actual inputs, output/checks, resources and recovery. An established workstream reservation permits the owner to allocate its own subtasks. Keep linked evidence current; the integrator incorporates concise updates or delegates non-overlapping checklist sections. Resolve duplicate claims and shared-write conflicts before proceeding. Independent checkouts may own their Git operations; a shared checkout has one Git writer.

**Ready briefs are detailed; future work is a roadmap.** [Task briefs and sketches](docs/task-contracts.md) retain stable IDs for continuity, not a fixed sequence. Expand a sketch when it becomes useful, then state real start inputs and acceptance evidence. A compatible fixture or validated intermediate may support an early start; it cannot substitute for real-world acceptance. Pin intermediate revision/hash and producer/consumer checks even if its branch is not merged yet. Combined promotion still needs integration checks.

Revise with a short reason and impact on consumers. Preserve IDs, artifacts, unresolved checks/blockers and predecessor/successor links. `Superseded`, `not selected`, `blocked` and `waiting_for_job` are not complete. Do not silently weaken evidence standards, erase negative results, rewrite a user's active native goal or retune on protected evaluation. See [decision rights](AGENTS.md#local-decisions-and-plan-changes).

## Ready work and ownership

The following four inquiries remain independently claimable. Each links its starting evidence, expected artifact, checks and suggested write paths. **No workstream is claimed yet; no execution result exists for these items.** Owners choose justified finite launch budgets from actual capacity/provider limits; there is no project-wide two-hour default or fixed concurrency/GPU count. Coordinate the aggregate allocation and existing cost authority before simultaneous jobs.

| ID | Useful next inquiry | Status / claimant | Starting evidence / next action |
|---|---|---|---|
| [T01](docs/task-contracts.md#t01--verify-candidate-imagery-intervals) | Imagery access, dates and paired samples | ready — unclaimed | Saved catalog/error evidence; locate actual recent assets and read a bounded sample |
| [T02](docs/task-contracts.md#t02--establish-geography-parcels-and-comparison-layers) | Jurisdiction, parcels and GT layers | ready — unclaimed | Source leads/GT report; retrieve boundary and share it before finishing every source inquiry |
| [T03](docs/task-contracts.md#t03--audit-permit-sources-and-temporal-meaning) | Permit feasibility, coverage and semantics | ready — unclaimed | Recorded errors/official guidance; inspect accessible source metadata and diverse records |
| [T04](docs/task-contracts.md#t04--establish-a-minimal-reproducible-environment-and-durable-artifact-path) | Reproducible operation and durable storage | ready — unclaimed | Provisioned environment/permitted fixture; prove environment and storage capabilities separately |

A ready brief is not a scheduled job. Record the actual owner, branch/checkout, write reservation, launch bounds, evidence link and status here (or in a reserved section) when claimed. Use an existing linked record rather than duplicating logs. Check remote changes and running artifacts before resuming.

## Future workstreams — revisable, unclaimed

All IDs below are **roadmap**, not launched items with fixed dependencies or resource allocations. Owners may activate an independently useful slice or replace the breakdown with recorded successors. The sketches describe evidence needed for acceptance; proposed task grouping is not itself an acceptance condition.

| Workstream | Current questions / likely IDs | What can proceed independently | Evidence needed for accepted claims |
|---|---|---|---|
| Study agreement | [T06](docs/task-contracts.md#t06--integrate-and-freeze-the-first-study-contract-g1) | Reconcile boundary, interval and interfaces as source evidence arrives | Versioned scope, usable inputs, recovery and honest coverage |
| Reference and evaluation | [T07](docs/task-contracts.md#t07--preregister-reference-sampling-and-acceptance-design), T09–T10, T18–T20 | Protocol/tool drafts alongside acquisition; independent component reference/evaluation | Protected exclusions before contamination; reviewed sampling/targets before test; actual references and independent reproduction |
| Preparation and detection | [T08](docs/task-contracts.md#t08--build-and-assess-paired-pilot-preparation), T11–T13, T17 | Technical image QC/controls from usable samples; exploratory code before human labels | Suitable imagery, accepted development comparisons and frozen versions for protected evaluation |
| Parcels and permits | [T05](docs/task-contracts.md#t05--prepare-any-necessary-historical-records-request), T14–T16, T17L | Request drafts from known gaps; normalized batches and geometry/match fixtures | Real record/event integration, coverage-aware matching and complete regional accounting for regional claims |
| Public explanation | [T21](docs/task-contracts.md#t21--build-a-local-map-and-evidence-card-prototype), T22, T24 | Mock/development prototype and release structure before final research | Version-compatible supported findings, rights/handling decision and explicit deployment authorization |
| Agency use | [T23](docs/task-contracts.md#t23--prepare-research-report-and-agency-briefing), T25 | Methods/report drafts and concrete feedback questions early | Authorized communications; actual final briefing delivery, no invented endorsement |
| Reproduction and maintenance | [T26](docs/task-contracts.md#t26--demonstrate-rerun-and-establish-maintenance-handoff) | Artifact recovery and component reruns throughout development | Demonstrated accepted-pipeline rerun, retention/custody and correction responsibilities |
| Future direction | [T27](docs/task-contracts.md#t27--decide-the-next-interval-or-jurisdiction-deferred) | Investigate a new source/opportunity when it matters | Scope-aware go/no-go, appropriate jurisdiction/epoch validation and authority |

## Readiness and unresolved decisions

These gates describe **what may be claimed or promoted**, not a requirement to finish one global phase before starting the next. A valid partial component may advance while another is blocked; label the limitation.

| Gate | Required evidence | Current state |
|---|---|---|
| G1 — study feasible | Suitable readable paired inputs, scoped geography/source interfaces and recoverable artifacts | Unpassed; metadata evidence only |
| G2 — evaluation candidate selected | Controlled development evidence, reviewed protocol/reference capacity, pinned method and inputs | Unpassed; method/MMU/registration policy unchosen |
| G3 — findings validated | Appropriate independent references, uncertainty/coverage, protected evaluation and independent numerical reproduction | Unpassed; no project accuracy measurements |
| G4 — delivered and maintainable | Supported reviewable bundle, authorized public result, delivered agency briefing and tested rerun | Unpassed; no release or briefing |

Unresolved: recent-image suitability/access; valid-area denominator; parcel history; effective-dated permit coverage; reference effort; local detection scale/registration limits; useful review yield/subgroup precision; durable storage; public detail and future custodian. Local findings can change methods and task boundaries. A changed shared scientific assumption needs affected-owner coordination and independent review; changed public/spending/communication scope retains the working agreement's authorization requirement.

Protected geography must be reserved before training/tuning contaminates it. Freeze each relevant method/prediction frame before its model-dependent protected sample; image reference does not inherently require permit linkage. Holdout generalization is distinct from a whole-domain map survey. Incomplete permit coverage remains explicit ambiguity, never evidence of illegality. These standards survive roadmap revisions.

## First launch prompts

Use the following with the matching ready brief after claiming visible ownership and setting actual run bounds. Native `/goal` is optional; ordinary bounded prompts work too. Branch names and module paths are chosen/coordinated at launch.

```text
/goal Complete T01's imagery-feasibility inquiry. Read AGENTS.md, checklist.md,
HUMAN_ACTIONS.md and the T01 brief. Confirm your visible claim/write reservation,
choose a justified bounded method, reuse existing evidence, and coordinate
intermediates with the geography/runtime owners. Preserve checks and recovery;
record any local revision or honest blocker without weakening the objective.
```

```text
/goal Complete T02's geography/parcel inquiry under its ready brief. Read the
working agreement and current state, claim disjoint ownership, set finite
bounds, and share validated boundary/schema evidence as soon as useful.
Preserve source/vintage limits and record revisions, checks and recovery.
```

```text
/goal Complete T03's permit-source inquiry under its ready brief. Read the
working agreement and current state, confirm your claim, and choose bounded
source checks. Keep source coverage distinct from record absence; coordinate
schemas/request gaps directly with affected owners. No unauthorized contact.
Preserve evidence, limitations and the exact next action.
```

```text
/goal Complete T04's reproducibility/storage inquiry under its ready brief.
Read the working agreement and current state, reserve shared/root writes, and
choose finite fixture/setup limits. Publish checked environment/storage
intermediates separately. If a capability is missing, prepare the concrete
smallest action; do not call an unproven recovery path durable.
```

## Checkpoint and next resume

P00's scientific/evidence review remains accepted. P01 passed Sol review with no blocking findings and document checks; the Sol agent merged reviewed commit `71a1040` into `chore/autonomous-harness` at **`02d27eb`**, pushed it and verified the remote SHA. Git ownership returned to the research lead; this completion-state update follows the merge. [D02](docs/decisions/decentralized-planning.md) records the review/integration evidence. No implementation tasks have been launched during this revision.

On resume: fetch/reconcile the campaign branch, read state/HA queue, reconcile claims/jobs/artifacts, then select useful ready work. Accept supported successor tasks when the roadmap changes; do not replay completed inquiries or require all historical IDs to be executed. Full project completion still needs validated findings with honest reconciliation limits, the authorized public deliverable, an actual agency briefing and reproducible maintenance handoff. A prototype, negative feasibility result or superseded task does not fulfill those deliverables.

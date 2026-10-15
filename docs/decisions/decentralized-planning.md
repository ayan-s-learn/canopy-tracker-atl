# D02 — Local autonomy and rolling planning

Date: 2026-10-14, America/Los_Angeles. Revision branch: `chore/decentralized-planning`, based on `c0f4a78`; intended integration target: `chore/autonomous-harness`. This records a decision and its review; [checklist.md](../../checklist.md) remains the current state entry point.

## Owner's clarification

The owner supports the overall scientific direction and requested less rigid, more decentralized planning. They selected:

- Local autonomy: agents choose methods, split/revise tasks and coordinate directly, while one integrator checks shared interfaces/evidence and integrates work.
- Rolling planning: detail ready work; outline later work until evidence makes a useful next task concrete.

They authorized a subbranch, Sol review and merge. The merge target is the existing campaign branch, not `main`. This revision changes how work is organized; it does not launch the research pipeline or install a goal runtime.

## What was too rigid and what changed

| Earlier assumption | Why it would fail as the project evolves | Revised rule |
|---|---|---|
| Orchestrator owns all task selection and local decisions | Useful work waits for central attention and workstream knowledge is underused | Workstream owners select/revise local work; integrator handles shared coherence/conflicts and promotion |
| Every future ID is a detailed contract with named predecessors | Forecasts become false dependencies, even when a fixture or intermediate would suffice | Detail T01–T04; preserve later IDs as revisable sketches; distinguish starting inputs from acceptance evidence |
| Whole producer tasks/branches must finish before consumers proceed | A usable boundary, image crop or normalized batch sits idle | Pin validated intermediates, producer/consumer checks and compatibility; campaign merge is not required for an experiment |
| Fixed hours, CPU, sample counts, batch sizes and model counts months ahead | Arbitrary caps distort scientific choices or discard healthy work | Set finite evidence-based launch bounds against actual capacity; distinguish estimates from hard limits; coordinate revisions within authority |
| Integrator creates every child batch and owns every detail | Adds bookkeeping and a single coordination bottleneck | Reserve workstreams/write scopes once; owners allocate local child IDs and maintain linked evidence, retaining traceable parent completion |
| Complete final protocol before all input preparation | Blocks technical QC and tools that do not inspect protected outcomes | Reserve evaluation exclusions before contamination; final protected use needs reviewed design/frozen relevant artifacts |
| All reference/evaluation awaits integrated permit linkage | Missing records halt otherwise valid image science | Component work advances with its own accepted frame; integrated claims still require compatible joined evidence |
| Product and maintenance follow all research | Workflow and recovery problems emerge too late | Prototype and exercise recovery early; validated publication and full rerun remain separate acceptance boundaries |

The first wave still asks the same four useful questions. The scientific direction remains City of Atlanta first, conditional imagery interval, method comparison, independent validation and uncertainty-aware triage. The first plan's source observations and GT comparison are unchanged.

## Durable boundaries versus revisable choices

Keep: the owner's objective; explicit authority for spending/communications/deployment; shared-write coordination; provenance and actual recoverability; protected evaluation separation and preregistration; independent review/reproduction; coverage-aware permit ambiguity; honest completion and negative results.

Revise locally with reasons: tools, method candidates, implementation layout, investigation order, finite batch boundaries and task decomposition. Coordinate with consumers for shared schemas/input versions/resources. Consequential scientific assumption or claim changes receive independent review. Do not rewrite a frozen evaluation to fit observed results; a new hypothesis needs appropriately new evaluation evidence.

Record a material revision in the existing task/experiment record, using a separate decision record only when cross-cutting. Preserve IDs/predecessors/successors, remaining checks and blockers. `Superseded` is not success. A process needs one visible owner even when several agents can help; shared-checkout Git remains single-writer. Integrator absence does not grant extra shared writes or spending, but already reserved work can continue with recoverable handoffs.

## Future scenarios used to check the revision

| Scenario | Expected behavior |
|---|---|
| 2025 imagery remains inaccessible while older samples work | Imagery owner records a bounded alternative; geography/records work continues; shared study assumptions receive coordinated review before claims |
| One source needs a human export but public records are usable | Normalize checked public batches and prepare the request; retain partial coverage and ambiguous matches; do not wait on all records to study loss |
| Human labels are delayed | Build tools/controls and input QC without inventing validation; keep protected exclusions; performance comparisons wait for adequate references |
| A producer has a checked boundary on an unmerged branch | Consumer pins its immutable revision/hash and checks, coordinates compatibility and proceeds; integrator later verifies combined results |
| A better method changes the event schema | Owners version the schema and coordinate affected consumers; no silent replacement of shared semantics or frozen evaluated outputs |
| Actual resource needs exceed a planning estimate | Owner distinguishes estimate from hard authority limit, measures need and records/coordinates a bounded revision before exceeding it; extra spending still needs authorization |
| A task split or replacement makes old rows obsolete | Transfer unfinished checks/blockers and scope to named successors; preserve evidence and mark superseded, not complete |
| Imagery reference is ready while linkage is delayed | Evaluate the image component with its frozen frame; make no joined/permit performance claim until its own evidence is ready |
| Integrator is temporarily unavailable | Continue established nonconflicting reservations; preserve records, avoid duplicate claims/shared writes and hand off for eventual integration |

These are document-level scenario checks, not evidence that software for coordination/recovery has been implemented.

## Review and integration evidence

An independent Sol agent audited the original documents before edits. It identified central task-selection bottlenecks, false whole-task dependencies, premature numeric/resource prescriptions, fixed structural conventions and delayed product/maintenance work. The revision incorporates those findings.

The Sol agent independently reviewed the concrete diff across all seven changed documents and accepted it with **no blocking findings**. It checked that local choice/splits/child IDs/resource revisions, direct peer coordination, unmerged intermediates and future sketches are substantive changes, while protected exclusions, relevant frozen frames, independent review/reproduction, shared-write coordination and existing authority/recovery remain intact.

Checks passed: 36 active-document relative links/anchors; all 28 stable future/ready IDs retained once; four ready briefs; balanced code fences; no whitespace errors. The original archive and planning source evidence are unchanged relative to `c0f4a78`. Future scenario checks above were also reviewed. No software tests or live-data rechecks were needed for this documentation-only revision.

Reviewed commit `71a10401d4ffe43b7a2c839aaee7ce99047c0c80` was published on `chore/decentralized-planning`. The Sol reviewer took exclusive shared-checkout Git ownership, verified the campaign base had not changed, and merged with a merge commit:

- Campaign merge: **`02d27eb323aebd8ba28df060be4483ae52fdd695`** on `chore/autonomous-harness`.
- Parents: original campaign `c0f4a78e1d1b41103d93687a1a55556f6bf1146f` and reviewed subbranch `71a10401d4ffe43b7a2c839aaee7ce99047c0c80`.
- Sol pushed the campaign branch and verified `git ls-remote` returned the identical merge SHA. Working tree was clean and the merged diff passed the whitespace check. The subbranch was retained; `main` was untouched.

Git ownership then returned to the research lead for this completion-state record. P01 is accepted and integrated; the latest campaign branch includes this subsequent state update. No implementation work or automated execution service was started.

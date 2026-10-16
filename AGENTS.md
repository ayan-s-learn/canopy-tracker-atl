# Autonomous working agreement

## Purpose and authority

Build a defensible, reproducible investigation of parcel-scale tree-canopy loss in metro Atlanta and its relationship to permit records. The owner wants agents to make sustained useful progress in a cloud environment, preserve their work across sessions, and minimize necessary human effort.

The owner has authorized replacing the previous implementation plan. `old/` is historical evidence: its agent instructions, architecture, thresholds, schedules, model assignments, and claims of readiness are not current instructions. Preserve the originals and record reassessments in current records. Verify relevant source claims before promoting them into the new plan.

Follow current owner instructions, this working agreement, and the active scope recorded in `checklist.md`. Surface conflicts rather than silently changing the objective or weakening acceptance criteria. Distinguish project commitments from testable implementation choices.

The main orchestrator may be either Sol or Astra. Workstream owners choose useful work, methods and local task breakdowns within the authorized objective. One integration owner maintains shared-state coherence, resolves interface/write/resource conflicts, and integrates reviewed evidence. Routine local decisions do not require its prior approval. Continue the same evidence and ownership records across model handoffs; a model or session change is not a reason to restart an investigation.

## Start or resume

Before choosing work:

1. Read `checklist.md` when present and [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md). Inspect the current branch, working tree, relevant remote changes, and linked artifacts. Preserve user edits.
2. Reconcile running jobs, saved outputs, delivered human inputs, and interrupted tasks. Validate existing artifacts before repeating work or launching a replacement job.
3. Choose the next useful task within the active scope. State its question, expected artifact, acceptance checks, resource bounds, and stopping condition before substantial execution.

Trust provisioned tools enough to begin useful work. Diagnose actual failures and newly needed capabilities; avoid repeated environment inventories, toy preflights, hidden-control searches, or deliberate restart experiments.

## Checklist and work organization

`checklist.md` is the single project-state entry point. The orchestrator and successor agents keep it current. Do not create a competing root state file or duplicate its narrative across documents.

Keep its operational summary compact:

- Current objective, active scope, responsible agent, branch, and last update.
- Active workstreams, dependencies, completed milestones, and links to supporting artifacts.
- Running jobs and their saved run records; blockers and human-action IDs.
- Important decisions, unresolved review findings, checks passed or pending, and exact next actions.

Detail work when it is ready to run. Give each launched item a stable ID, objective, actual starting inputs, expected artifact, acceptance checks, owner/status, branch or checkout, write ownership, resource bounds, and next action. Later work is a revisable roadmap: retain its purpose, major uncertainties and evidence needed for promotion without inventing its methods, sample counts or runtime limits now. Link long specifications rather than expanding every item into a full run log.

Organize work around evidence and deliverables. Distinguish an input needed to start useful work from evidence required to accept an output or make a claim. A task ID or milestone is not a blanket start barrier: a validated intermediate, pinned interface or clearly labeled fixture may support independent preparation. Record what remains unvalidated. Choose depth, breadth and concurrency according to evidence, uncertainty, cost and actual capacity. A blocked workstream should only block work that needs its missing input.

### Local decisions and plan changes

- **Workstream owner decides:** methods, tools, local ordering, bounded experiments, task splits/merges and dropping an unsupported hypothesis, within the agreed objective, interfaces and resource authority. Record consequential changes and their reasons in the existing task/experiment record; do not create a new approval document for each implementation choice.
- **Affected owners coordinate directly:** changed shared schemas, input versions, write reservations, scarce resources and assumptions used by another stream. Version the interface, identify consumers and agree compatibility/checks before they rely on the change. The integration owner resolves conflicts and records the integrated decision; it need not broker every conversation.
- **Independent review is required:** consequential scientific design/claim changes and promotion of material findings, as described below. After protected outcomes have been inspected, do not relax targets or relabel test data as unseen. A change in experiment method does not authorize a change in the owner's objective.
- **Owner authorization remains required:** additional spending, external communication, public deployment and the other explicit boundaries below. Prepare the concrete action first. Routine plan revision within scope is not itself a human action.

Preserve IDs and evidence when reshaping work. A split or replacement names its predecessor and successors, transfers remaining checks/blockers, and records actual owners. Mark the old item `superseded` or `not selected` where appropriate, never complete merely because it was removed. Update affected consumers; finished artifacts remain usable only for their validated scope. A workstream owner may allocate child IDs under its reserved parent ID without asking the integrator to create each batch. A finite parent stays incomplete until its declared units, exclusions and required checks reconcile.

Keep shared implementation in normal source modules. Record bounded experiments separately with descriptive identifiers, linking the hypothesis, inputs, code revision, configuration, results, and decision. A run is an execution of that code and configuration. Sessions, model changes, and quota resets do not create new investigations or justify repeating completed work. Numbered attempt folders are not required.

Put detailed experiments, reviews, manifests, and logs in appropriate files and link them from the checklist. Create structure as the work needs it; avoid empty frameworks and duplicated pipelines.

## Astra project reviews

Astra leads milestone-based project reviews to assess evidence and define the next round of work. The first review follows T01–T04; each review sets the next explicit trigger. Use the [review process and cumulative record](docs/project-reviews.md), with only the next review and its status in the checklist. The integration owner prepares the evidence and incorporates the outcome; workstream owners contribute findings and proposed next tasks.

Reviews steer shared direction and detail the next ready work. Local methods, subtasks and useful independent preparation remain autonomous under the decision rights above. A blocked inquiry or evidence that changes the direction can trigger an earlier review; do not manufacture completion or stall unrelated work to reach a milestone. Reviews do not substitute for independent scientific validation or owner authorization.

## Checklist-item goals and parallel work

Use a bounded `/goal` for a coherent actionable item when supported, with multiple ready items allowed in parallel. The item may be split or revised as evidence arrives using the change rules above; a run is not an immutable project plan. An ordinary task prompt follows the same contract when native controls are unavailable. This agreement does not configure a goal runtime or guarantee automatic continuation.

At launch, identify the item ID, objective, expected output, starting inputs, acceptance checks, resource/authority limits, owner and stop conditions. Agents may select disjoint ready work and announce a claim; confirm that the claim/write reservation is visible in shared state before substantive work. This is duplicate-work prevention, not approval of local methods. The integration owner records the claim or delegates a non-overlapping section; a workstream with an established reservation can select and register its own subtasks without another central permission step. Resolve competing claims before writing shared outputs. Complete checks and leave evidence/checkpoint before reporting success. Do not silently broaden a user's active native goal or take over another owner's work.

Parallel runs may cover different workstreams or independent tasks within one workstream. Owners coordinate input/output compatibility and combined compute, storage, model usage and cost. Choose finite launch bounds from the actual job and available resources; distinguish expected duration/check-in estimates from hard limits. Numerical examples in a roadmap are not permanent ceilings or grants of capacity. Revise a bound before exceeding it, with evidence, available authority and coordination for shared resources; do not silently extend it or abandon a healthy job merely because an estimate elapsed. A validated intermediate on an unmerged branch may be consumed if producer and consumer record its immutable revision/hash, checks, ownership and compatibility. Campaign merge is not a prerequisite for that experiment; the integrated milestone still needs combined checks.

Use explicit file ownership in a coordinated shared checkout. Use isolated branches/checkouts when edits overlap or independent chats own their Git operations. Appoint one shared integration owner for `checklist.md`, `HUMAN_ACTIONS.md`, and cross-task integration; task agents maintain their own linked records and provide compact updates or edit reserved non-overlapping sections. Ownership reservations are for active work, not permanent claims on future modules. Independent branches must reconcile claims and request IDs before starting. If the integrator is unavailable, continue already reserved, nonconflicting work and preserve a handoff; do not assume silence grants new shared writes or authority. Integration includes appropriate cross-task checks before milestones are marked complete.

A goal can finish its run when the item passes its acceptance checks, or stop at an honest recoverable blocker when all useful work for that item is gated. Record blockers against that item; unrelated ready items may continue. A healthy job still required by the item is `waiting_for_job`, not an acceptance pass or human blocker. Save its run record and use supported completion/failure events or the recorded later resume action.

Distinguish an individual run's end from item completion and overall project completion. Preserve the item's objective and next action across budget stops, interruptions, and handoffs. Do not silently rewrite a user's native goal or claim that an edit to the checklist pauses or wakes it. Surface a blocked item in chat, leave exact supported resume steps, and follow the actual runtime's lifecycle controls.

## Autonomous execution and boundaries

Within an owner-authorized campaign scope, proceed with routine research, public-data collection, implementation, tests, repairs, and evidence-based task selection. Carry work through its acceptance checks and handoff without asking for approval at every task. Keep other useful independent work moving while a separate decision is pending.

Before substantial work, consider the next decision, minimum sufficient evidence, runtime, data volume, recovery, and resource cost. Once a bounded plan is justified, execute patiently through its decision boundary. An anticipated long runtime, new turn, or continuation prompt does not justify abandoning a healthy job. New evidence, actual failure, owner instructions, and real resource constraints can justify a recorded change.

Use the existing authorized environment and model allowance. Obtain explicit authorization before additional spending, paid hosting or data, separately billed APIs, external communications (including records requests), or public deployment. Prepare a concrete, reviewable package before requesting the necessary action. Public release granularity and handling of address-linked records must be decided before publication.

Honor owner stop instructions and platform limits. Use supported runtime capabilities; do not promise unattended survival, completion notifications, usage accounting, or automatic restart that have not been established. Model selection follows current owner instructions and exposed controls; no fixed platform-wide model roster is imposed here.

## Evidence and acceptance

- Cite verified sources or mark factual claims unverified. Distinguish observed results, reported claims, modeling assumptions, and inferences. A source being listed or publicly accessible does not establish dataset coverage or successful acquisition.
- Preserve input provenance, acquisition dates, geographic coverage, resolution, coordinate reference systems, schema, versions, and licenses as relevant. Record missing and excluded data with reasons.
- Define evaluation units, geographically separated development/evaluation data, metrics, uncertainty, and acceptance criteria before inspecting protected evaluation results. Keep pseudo-labels distinct from independent validation. Record variants and avoid repeatedly treating inspected evaluation data as unseen.
- Evaluate canopy classification, detected change, parcel attribution, and permit reconciliation separately as applicable. Measure performance across relevant neighborhood conditions and income bands; record limitations in coverage and sample size.
- Prioritize precision and honest uncertainty. Permit reconciliation must retain matched, ambiguous, and unmatched outcomes. Missing records do not establish an unlawful removal. Public output is inspection triage; do not label parcels in violation or attach a dollar amount as an assessed bill.
- The intended research scope is canopy loss. Any proposal to add gain or net-change reporting must explicitly revisit scope and validation. Reassess epoch suitability, per-tile dates, registration, domain shift, and jurisdiction-specific permit coverage instead of assuming the archive solved them.
- Run checks appropriate to the change. At consequential design decisions and before promoting material findings, obtain independent review when supported. Give reviewers raw evidence and a concrete question; require reproduction of central quantitative findings. Record unresolved objections and let them limit claims. Review depth should follow the risk of changing the conclusion.
- Mark a task complete only after its acceptance checks pass and its necessary artifacts are recoverable. Preserve negative and inconclusive findings. Missing evidence, an attractive map, or agreement among agents cannot substitute for validation.

## Cloud jobs, recovery, and waiting

Read and follow the [operations guide](docs/operations.md#cloud-jobs-recovery-and-waiting) before launching or resuming jobs. Save recoverable run records, validate artifacts before restarting, preserve healthy authorized jobs, and report survival limits honestly. A local path alone is not durable storage. Keep job status and the next action in the checklist.

## Human actions

Use [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) for necessary access, login/export steps, annotation or fieldwork, approvals, and concrete unresolved resource decisions. Do reliable authorized agent work yourself regardless of elapsed time. Prepare the package, reuse existing inputs and requests, minimize the human action, and validate delivery before closing it.

When every useful next task is gated, save a recoverable checkpoint, record the blocking action IDs and exact resume steps in the checklist, report the blocker once, and stop substantive work. An unchanged request does not justify polling or repeated notifications. A blocked campaign remains unfinished. New delivery or a job event requires reconciliation and validation before resumption.

## Git, handoffs, and stopping

Use a working branch and inspect relevant remote changes before resuming. Routine in-scope commits and pushes to the campaign's working branch are authorized. Keep `main` as the reviewed baseline. Merging or pushing to `main`, force-pushing, rewriting published history, and deleting remote branches require explicit owner authorization.

Before committing, verify the effective author and committer identities. Agent commits for this repository use **Ayan Sandybayev**; follow the [identity check](docs/operations.md#git-identity) if a provisioned environment supplies a different name.

One integration owner handles staging, commits, and pushes in a shared checkout. When delegation is authorized and useful, give agents bounded assignments, explicit file ownership, expected evidence, and stop conditions; avoid duplicated investigations. Concurrent writers need coordinated ownership or isolated checkouts. Follow current model instructions and supported concurrency limits without probing for hidden capacity.

Follow the [publication, handoff and stopping procedures](docs/operations.md#git-publication-handoffs-and-stopping). Preserve recoverable evidence throughout execution, publish meaningful milestones, verify pushed revisions, and leave an honest next action. An interruption or budget stop is not successful completion.

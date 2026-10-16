# Operations guide

Read the relevant section **before launching or resuming a job, handing off work, or stopping a session**. These procedures implement [AGENTS.md](../AGENTS.md); they do not grant extra authority or establish that a runner, durable store or automatic continuation exists. [checklist.md](../checklist.md) remains the live state entry point.

## Cloud jobs, recovery, and waiting

Apply these requirements to the actual download, preprocessing, training, inference, or collection job being used. These rules do not establish that a runner already implements them.

Before a long job, save a compact run record and link it from `checklist.md`:

- Purpose, run ID, owner, fixed input scope, code revision, exact command/configuration, completion and stop conditions.
- Host, working directory, task or process identity with start time, single-writer ownership, expected resources, runtime, bounded retries/timeouts, and existing cost authority.
- Output, manifest, log, and checkpoint locations; exact validation, resume, and stop commands; durable retrieval path for a new session.
- What survives a disconnect, model stop, process crash, reboot, and environment deletion. Mark unknowns explicitly. Record whether the job may continue unattended, its finite scope or runtime/cost limits, and its stop mechanism.

Validate each bounded work unit, finalize its output safely, then advance the manifest/checkpoint. Resume by validating saved units and processing only missing or failed work. Distinguish expected, complete, pending, failed, and genuinely empty units. For training, retain recoverable model/optimizer state and enough configuration to describe restart limits accurately.

The job writes its own compact progress, errors, retry/backoff state, and final exit status. Save completed units and checkpoints to an authorized durable location throughout execution, recording the last confirmed copy and any unsynced tail. A local path, checksum, terminal session, or `nohup` alone does not establish recoverability after environment loss. Keep large raw data and model artifacts out of Git; track manifests and retrieval instructions.

On handoff or continuation, reconcile actual task identity, progress, retry state, and artifacts before changing anything. Preserve healthy jobs and existing data. Stop or repair only for an owner instruction, completion boundary, substantive new evidence, demonstrated failure, or a real operational constraint. Avoid duplicate jobs and preserve partial results when changing plans.

Prefer completion/failure events and supported waits. Do useful independent tasks while a job runs. Avoid recurring model-status polling and idle busywork. A deterministic scheduled data collector can be justified by the research plan; record its schedule, ownership, retention, resource limits, and stop instructions separately from model continuation.

Record task states accurately: `active`, `waiting_for_job`, `blocked`, or `complete`, with the reason and next action. A campaign is fully blocked only when all useful authorized next work is gated. A healthy running job is ongoing work. If no completion notification exists, record that limitation and the exact later status/resume action.


## Git identity

Before the first commit in a fresh checkout or session, verify `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. For this repository, both names must be **Ayan Sandybayev**. Set `git config --local user.name "Ayan Sandybayev"` if needed; retain the verified account email. Check name overrides if the effective identity still differs. Do not rely on provisioned global defaults or rewrite published history to repair earlier attribution.

## Git publication, handoffs, and stopping

Commit at meaningful milestones and before planned stops. Stage explicit paths, inspect the diff, and exclude secrets, unrelated edits, large inputs, and temporary logs. Clearly label incomplete checkpoints and pending checks. Verify the remote contains a pushed checkpoint; report publishing failures with the local commit and recovery action.

Maintain recoverable state throughout execution rather than relying on a final saving turn. Use reliable budget signals when exposed; otherwise keep assignments bounded and checkpoint frequently without inventing remaining allowance percentages.

At a stop boundary, stop launching new work, preserve partial results, update the checklist and human-action queue, and publish an honest checkpoint. A declared independent job may continue within its recorded authority and resource limits when the host supports it; an explicit instruction to stop that job overrides continuation. Stop only owned processes that should end and retain exact recovery steps. Do not describe a budget stop as successful completion.

Handoffs identify the branch and checkpoint, completed and unfinished work, checks and review status, artifact recovery locations, process ownership, blockers, and exact next actions. On resume, reconcile from those records and actual artifacts. This agreement installs no goal runtime, watcher, scheduled agent, or automatic restart service.

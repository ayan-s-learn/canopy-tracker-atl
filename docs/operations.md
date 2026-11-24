# Operations guide

Read the relevant section **before claiming a task, launching or resuming a job, handing off work, or stopping a session**. These procedures implement [AGENTS.md](../AGENTS.md); use only verified runtime capabilities, and do not assume unattended survival, notifications, usage accounting or automatic restart. [checklist.md](../checklist.md) remains the live state entry point.

## Cloud jobs, recovery, and waiting

Choose a recovery strategy appropriate to the job: rerun cheap deterministic work; checkpoint or back up expensive and irreplaceable work. Reuse tool-native logs and resumability rather than building a runner by default. Keep enough linked information to identify inputs/code, outputs, progress and how to resume or stop; document known survival limits without requiring every failure mode to be tested before useful work.

Choose validation, backup and monitoring frequency based on failure cost and available capabilities. Inspect existing work before restarting; preserve healthy jobs and useful partial results. Events, supported waits or proportionate status checks are all acceptable. Revise estimates and methods as evidence arrives within authorized resource limits; elapsed estimates alone do not require stopping a productive run.

Report completed, pending and failed work honestly; distinguish an ongoing job from a blocker or completion. Do not claim durable recovery without a verified retrieval path. Keep raw rasters, model weights, personal records, secrets and expiring signed URLs out of Git; retain provenance and retrieval instructions. The [T04 replay](../tasks/T04-runtime/README.md#outputs-and-replay) shows how to rebuild the pinned environment and recover a small archived artifact.

## Claiming and resuming a task

1. Run `git fetch origin`, then `git switch --no-track -c task/<ID>-<slug> origin/main`, using the task folder name exactly.
2. Add a **Progress** section to the task README with an owner line giving your ID (agent name plus session start time), commit, and run `git push -u origin task/<ID>-<slug>`.
3. If the push is rejected, do not pull, rebase or force. Run `git fetch origin 'refs/heads/task/<ID>-<slug>:refs/remotes/origin/task/<ID>-<slug>'`. If no such branch exists, the failure was not a claim conflict; diagnose it. Otherwise read that branch's **Progress**, where the latest owner line is the current owner:
   - If it names you, continue on it.
   - If it ends with `Handoff: open`, or the project owner told you to take the task over, run `git switch -C task/<ID>-<slug> origin/task/<ID>-<slug>`, replace `Handoff: open` (if present) with your own owner line, commit and push. If this push is rejected, another session took the task first; choose other work.
   - Otherwise the task is taken; choose other work.
4. When stopping with work left for a later session, end **Progress** with the handoff and the line `Handoff: open`, then push.
5. The integration owner runs `git fetch --prune origin 'refs/heads/task/*:refs/remotes/origin/task/*'` at the start of each integration session.

## Git publication, handoffs, and stopping

Commit at meaningful milestones and before planned stops. Stage explicit paths, inspect the diff, and exclude secrets, unrelated edits, large inputs, and temporary logs. Clearly label incomplete checkpoints and pending checks. Verify the remote contains a pushed checkpoint; report publishing failures with the local commit and recovery action.

At a stop boundary, stop launching new work, preserve partial results, update the task's **Progress** section and any **For integration** proposals, and publish an honest checkpoint. A declared independent job may continue within its recorded authority and resource limits when the host supports it; an explicit instruction to stop that job overrides continuation. Stop only owned processes that should end and retain exact recovery steps. Do not describe a budget stop as successful completion.

Handoffs, kept in the task's **Progress** section, identify the branch and checkpoint, completed and unfinished work, checks and review status, artifact recovery locations, process ownership, blockers, and exact next actions. On resume, reconcile from those records and actual artifacts.

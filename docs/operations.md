# Operations guide

Read the relevant section **before launching or resuming a job, handing off work, or stopping a session**. These procedures implement [AGENTS.md](../AGENTS.md); use only verified runtime capabilities, and do not assume unattended survival, notifications, usage accounting or automatic restart. [checklist.md](../checklist.md) remains the live state entry point.

## Cloud jobs, recovery, and waiting

Choose a recovery strategy appropriate to the job: rerun cheap deterministic work; checkpoint or back up expensive and irreplaceable work. Reuse tool-native logs and resumability rather than building a runner by default. Keep enough linked information to identify inputs/code, outputs, progress and how to resume or stop; document known survival limits without requiring every failure mode to be tested before useful work.

Choose validation, backup and monitoring frequency based on failure cost and available capabilities. Inspect existing work before restarting; preserve healthy jobs and useful partial results. Events, supported waits or proportionate status checks are all acceptable. Revise estimates and methods as evidence arrives within authorized resource limits; elapsed estimates alone do not require stopping a productive run.

Report completed, pending and failed work honestly; distinguish an ongoing job from a blocker or completion. Do not claim durable recovery without a verified retrieval path. Keep raw rasters, model weights, personal records, secrets and expiring signed URLs out of Git; retain provenance and retrieval instructions.

## Git publication, handoffs, and stopping

Commit at meaningful milestones and before planned stops. Stage explicit paths, inspect the diff, and exclude secrets, unrelated edits, large inputs, and temporary logs. Clearly label incomplete checkpoints and pending checks. Verify the remote contains a pushed checkpoint; report publishing failures with the local commit and recovery action.

At a stop boundary, stop launching new work, preserve partial results, update the checklist and human-action queue, and publish an honest checkpoint. A declared independent job may continue within its recorded authority and resource limits when the host supports it; an explicit instruction to stop that job overrides continuation. Stop only owned processes that should end and retain exact recovery steps. Do not describe a budget stop as successful completion.

Handoffs identify the branch and checkpoint, completed and unfinished work, checks and review status, artifact recovery locations, process ownership, blockers, and exact next actions. On resume, reconcile from those records and actual artifacts.

## T04 — Runtime and artifact recovery

Codex launched T04 on 2026-11-23 from `28643e3` on `codex/t04-reproducible-runtime`. The write reservation covers the environment lock, executable check, compact derived raster, operations, and T04 checklist entry. The [T01 Piedmont Park 2023 window](research/imagery/T01.md) is the input. Use at most 100 MiB of wheel and fixture transfers, 500 MiB of temporary space, and one GitHub working branch for the recovery check. No paid provisioning. Start with the existing TIFF, then replay in a clean directory and retrieve the derived raster from the remote. Stop after both checks pass or after recording the blocked capability and resume steps.

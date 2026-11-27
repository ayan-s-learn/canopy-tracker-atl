# Human action queue

Use this queue when a necessary part of the authorized plan requires the owner or another human. Agents prepare what they can, explain the decision unlocked, and validate the result. Routine agent work and healthy long-running jobs belong in task folders and the checklist. Task agents prepare the package in their task folder and propose the action under its **For integration** section; the integration owner adds it here as soon as it sees it.

## Active actions

### HA-0002 — Confirm City receipt or file scoped records requests

- **Status / owner / task:** ready, 2026-11-23. Project owner for confirmation or filing. Validation of delivered records becomes a new task; the [T03 audit](tasks/T03-permits/README.md#next-access-action) lists the checks.
- Check whether the Gmail send already reached the designated City custodian. If so, share the acknowledgment or filing ID and scope privately. If City filing is outstanding, use the [prepared request and City routes](tasks/T03-permits/README.md#draft-for-city-custodians) for the missing Office of Buildings and Parks scopes. Reuse any existing filing for an equivalent scope.
- Allow about 10 minutes to check and file, depending on account setup. Request a quote before any paid work. Share the filing ID and covered scope privately. When the City responds, arrange private access to the export before sharing address-linked files. The validation task will verify schema, date and jurisdiction coverage, and exclusions before closing the action.

### HA-0003 — Assign development calibration readers

Ready 2026-11-27. The project owner assigns two independent interpreters (2.5 hours each) and a third adjudicator (2 hours). Their readings will test interpretation rules and workload on the 12 development exercises. No hours or spending are committed.

Use the [distribution and private return instructions](tasks/T09-calibration-package/README.md#distribution-and-return) with the scorer at `46bafa5` and the [verified packet fingerprint](tasks/T09-calibration-package/dry-run.json). First check each person's canopy and RGB/NIR experience, prior exposure and conflicts. Agree on a private handoff with each person, then give both readers the same reader ZIP separately. Readers can save drafts and resume offline in Chrome.

The coordinator verifies and archives each original by role, scores the pair, then issues flagged cases to the adjudicator. Retain both original hashes and the separate adjudication log with rationale, unresolved cases and minutes. The task instructions cover corrected returns and interrupted comparisons.

## How to use the queue

Before adding an action:

1. Check existing inputs, caches, active/fulfilled actions, and the checklist. Combine overlapping needs and avoid duplicate requests.
2. State the next task or decision it unlocks and why an agent cannot finish that part within existing authority. Request the smallest sufficient scope while preserving the planned sample and evaluation integrity.
3. Complete authorized preparation: runnable code or export instructions, annotation materials, fieldwork forms, a draft message, or a concrete resource comparison. Verify a small sample where feasible and publish the needed materials before notifying the owner. Sending a prepared message still requires authorization.
4. Specify the steps, prepared revision, required access, expected output and material effort/cost. Include unattended runtime, execution host, computer-awake requirements and disconnect behavior when the action actually involves execution; an approval-only request need not invent these fields.
5. Provide an accessible delivery path, safe stop/resume or correction steps, and agent acceptance checks. A path on the owner's device is not cloud delivery. Keep credentials out of chat, Git, archives, and logs.

The integration owner assigns stable IDs (`HA-0001`, `HA-0002`, ...). Keep each action's owner, dependencies, and linked task clear. Preserve the ID and history when correcting or closing a request.

Statuses: `ready`, `in progress`, `delivered — awaiting verification`, `needs correction`, `fulfilled`, or `closed without fulfillment`. A draft package is preparation work, not a ready request; keep it in the task folder until executable, or propose a smaller action for the actual preparation blocker.

Notify the owner when an action becomes ready or changes materially: ID, reason, branch/link, first action, hands-on time, runtime, and known cost. Full instructions stay here or in a linked tracked package. Do not nag or install a watcher for an unchanged action. Continue useful independent work while waiting.

For delivered data, check integrity, schema, expected/delivered/missing coverage, and recovery from the recorded location. Keep protected evaluation inputs separate from development analysis. For annotation or fieldwork, provide the protocol, sample assignments, uncertainty handling, and completeness checks in advance. For an approval, record the exact approved scope and limits; approval of setup is not delivery of a dataset.

If acceptance fails, keep the action active under the same ID and request the smallest precise correction. Move it to Fulfilled only after verification. Preserve cancelled/superseded actions with their reason and replacement ID; cancellation is not fulfillment.

If all useful work is blocked, follow the working agreement's [checkpoint and notification rules](AGENTS.md#human-actions).

## Action template

This template is not an active request. Replace every bracketed field before marking an action ready. Omit fields that do not apply and explain material unknowns.

### HA-NNNN — [Action]

- **Status / priority / dates:** [status, what this blocks, requested/updated].
- **Owner / task:** [responsible agent and linked task].
- **Need and scope:** [decision unlocked, why a human is needed, minimum sufficient scope and exclusions].
- **Prepared package:** [accessible link, exact revision and preparation checks].
- **Steps and delivery:** [exact actions, expected result and accessible delivery path].
- **Effort and constraints, where relevant:** [hands-on/runtime estimates, cost, access, data size, execution host and disconnect behavior].
- **Stop / correction / resume:** [safe recovery and failure-reporting instructions].
- **Acceptance / next action:** [agent checks, evaluation restrictions and next authorized work].
- **History:** [dated delivery, verification, corrections and approved scope; preserve artifact links and limitations].

## Fulfilled actions

### HA-0001 — Send the Tier 4 draft

Fulfilled for the send step on the owner's 2026-11-23 report. The owner sent the [Tier 4 draft](old/permits-and-pixels.md#tier-4--open-records-request--file-week-one) via Gmail to the Georgia arborist community. The send date and City custodian receipt are unverified. HA-0002 tracks formal filing or confirmation.

## Closed without fulfillment

None. Retain cancelled or superseded actions here with the reason and replacement ID when applicable.

# Human action queue

Use this queue when a necessary part of the authorized plan requires the owner or another human. Agents prepare what they can, explain the decision unlocked, and validate the result. Routine agent work and healthy long-running jobs belong in `checklist.md` and their run records.

## Active actions

None.

## How to use the queue

Before adding an action:

1. Check existing inputs, caches, active/fulfilled actions, and the checklist. Combine overlapping needs and avoid duplicate requests.
2. State the next task or decision it unlocks and why an agent cannot finish that part within existing authority. Request the smallest sufficient scope while preserving the planned sample and evaluation integrity.
3. Complete authorized preparation: runnable code or export instructions, annotation materials, fieldwork forms, a draft message, or a concrete resource comparison. Verify a small sample where feasible and publish the needed materials before notifying the owner. Sending a prepared message still requires authorization.
4. Specify the steps, prepared revision, required access, expected output and material effort/cost. Include unattended runtime, execution host, computer-awake requirements and disconnect behavior when the action actually involves execution; an approval-only request need not invent these fields.
5. Provide an accessible delivery path, safe stop/resume or correction steps, and agent acceptance checks. A path on the owner's device is not cloud delivery. Keep credentials out of chat, Git, archives, and logs.

Use stable IDs (`HA-0001`, `HA-0002`, ...); coordinate allocation across active project branches. Keep each action's owner, branch, dependencies, and linked checklist tasks clear. Preserve the ID and history when correcting or closing a request.

Statuses: `ready`, `in progress`, `delivered — awaiting verification`, `needs correction`, `fulfilled`, or `closed without fulfillment`. A draft package is preparation work, not a ready request; record it in the checklist until executable, or issue a smaller action for the actual preparation blocker.

Notify the owner when an action becomes ready or changes materially: ID, reason, branch/link, first action, hands-on time, runtime, and known cost. Full instructions stay here or in a linked tracked package. Do not nag or install a watcher for an unchanged action. Continue useful independent work while waiting.

For delivered data, check integrity, schema, expected/delivered/missing coverage, and recovery from the recorded location. Keep protected evaluation inputs separate from development analysis. For annotation or fieldwork, provide the protocol, sample assignments, uncertainty handling, and completeness checks in advance. For an approval, record the exact approved scope and limits; approval of setup is not delivery of a dataset.

If acceptance fails, keep the action active under the same ID and request the smallest precise correction. Move it to Fulfilled only after verification. Preserve cancelled/superseded actions with their reason and replacement ID; cancellation is not fulfillment.

If all useful work is blocked, checkpoint and name the blocking IDs and exact resume action in `checklist.md`. Do not treat a human blocker as project completion. A new delivery or job event is a reason to reconcile the saved state; unchanged blockers require no repeated polling.

## Action template

This template is not an active request. Replace every bracketed field before marking an action ready. Omit fields that do not apply and explain material unknowns.

### HA-NNNN — [Plain-language action]

- **Status / priority:** [ready; what this blocks].
- **Requested / updated:** [date and timezone].
- **Owner / branch / checklist task:** [responsible agent, branch, linked task].
- **Decision unlocked / why human action is needed:** [specific next decision and obstacle].
- **Minimum sufficient scope:** [fixed inputs or actions, existing materials reused, exclusions, missing-item handling].
- **Prepared materials / revision:** [published code, instructions, draft, sample packet, or resource options; exact revision and checks performed].
- **Hands-on / unattended time:** [estimates and basis].
- **Execution host / computer requirement:** [where work runs, awake/online requirement, disconnect behavior].
- **Cost / size / prerequisites:** [known amount or uncertainty, disk/transfer needs, accounts/access; approval limits if relevant].

**Steps**

1. [Exact starting app, website, screen, or directory and direct link.]
2. [Exact action or prepared command; define inputs and preserve existing work.]
3. [Expected progress, success message, and output or decision.]
4. [Exact accessible delivery steps and confirmation to send.]

**Stop / resume / failure:** [safe actions, saved partial work, log location, non-secret error or uncertainty to report].

**Acceptance / next action:** [files, coverage, schema, integrity or decision checks; tested retrieval/restore where relevant; exact next authorized task; evaluation restrictions].

**Progress / delivery / verification:** [dated updates, accessible artifact locations or approved scope, checks and limitations; leave empty until known].

## Fulfilled actions

None. Retain completed requests here with their IDs, dates, prepared instructions/revision, verified delivery or decision, artifact locations, limitations, and consuming tasks.

## Closed without fulfillment

None. Retain cancelled or superseded actions here with the reason and replacement ID when applicable.

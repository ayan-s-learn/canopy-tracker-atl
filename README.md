# Canopy Tracker ATL

A student research project investigating parcel-scale tree-canopy loss in metro Atlanta and reconciliation with permit records. The intended outputs are a reproducible pipeline, validated findings, a public presentation or website, and an agency briefing. Findings must communicate uncertainty and support inspection triage.

The project is being replanned. The previous implementation proposal and research documents are preserved in [old/](old/README.md). The replacement architecture, geographic coverage, data choices, and evaluation plan remain to be established by the owner-selected Astra planning agent.

## Start here

- [AGENTS.md](AGENTS.md) defines autonomous execution, evidence standards, job recovery, and handoffs.
- `checklist.md` will hold Astra's implementation plan and the current project state. It is intentionally absent until Astra creates it; successor agents maintain it as work progresses.
- [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) holds prepared requests for necessary human actions and their delivery checks.
- [Archive guide](old/README.md) identifies the preserved documents and known issues for reassessment.

## First assignment: Astra planning

Read the working agreement, inspect the archive and current repository, reassess the approach, and create `checklist.md` from the project objective down to actionable implementation tasks. Define dependencies, acceptance criteria, evidence requirements, and the first bounded execution scope. Resolve or explicitly track open questions rather than inheriting the old pipeline as the plan.

## Execute checklist items

Use one bounded `/goal` run per actionable checklist item when the runtime supports it. Each item needs a stable ID, prerequisites, an owner, acceptance checks, and evidence to leave behind. Multiple items may run in parallel when their dependencies are satisfied and their write ownership and resource use are coordinated. An ordinary bounded prompt can execute the same task when native goals are unavailable.

Replace the bracketed fields with an actual ready item before launching:

```text
/goal Complete checklist item [ID]: [task]. Read AGENTS.md, checklist.md,
and HUMAN_ACTIONS.md. Confirm prerequisites and claim ownership. Work within
the item's scope and resource limits; preserve other active work. Finish its
acceptance checks, update the shared state through its integration owner,
and publish a recoverable checkpoint. If all useful work for this item is
blocked, record the blocker and exact resume action, report BLOCKED, and stop
without marking the item complete. Preserve healthy declared background jobs.
```

Completion of an item establishes that item's accepted result. Overall project completion requires the integrated deliverables and their validation. See [AGENTS.md](AGENTS.md#checklist-item-goals-and-parallel-work) for ownership, integration, and waiting rules.

This repository provides the operating agreement. Cloud jobs, durable storage, scheduled collection, and automatic continuation require actual setup and verification when the approved work needs them.

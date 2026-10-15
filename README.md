# Canopy Tracker ATL

A student research project investigating parcel-scale tree-canopy loss in metro Atlanta and reconciliation with permit records. The intended outputs are a reproducible pipeline, validated findings, a public presentation or website, and an agency briefing. Findings must communicate uncertainty and support inspection triage.

Either Sol or Astra can serve as the main orchestrator. Workstream agents choose local methods and revise their task breakdowns; one integration owner keeps shared interfaces, evidence and repository state coherent. The previous implementation proposal and research documents are preserved in [old/](old/README.md) as historical reference.

## Start here

- [AGENTS.md](AGENTS.md) defines autonomous execution, evidence standards, job recovery, and handoffs.
- [checklist.md](checklist.md) holds the implementation plan and current project state, maintained as work progresses.
- [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) holds prepared requests for necessary human actions and their delivery checks.
- [Archive guide](old/README.md) identifies the preserved documents and known issues for reassessment.

## Execute checklist items

Detail the work that is ready to run; keep later work as revisable roadmap sketches. Use a bounded `/goal` for a coherent item when supported. Agents may choose disjoint ready work, revise local methods, split items and coordinate directly within the working agreement. Confirm visible ownership, actual starting inputs, compatible interfaces and finite resource bounds before execution. A validated intermediate can unblock work before its parent task or branch is fully integrated. Acceptance and publication still require the relevant evidence and authority. An ordinary bounded prompt works when native goals are unavailable.

Replace the bracketed fields with an actual ready item before launching:

```text
/goal Complete checklist item [ID]: [task]. Read AGENTS.md, checklist.md,
and HUMAN_ACTIONS.md. Confirm starting inputs and visible ownership. Choose
the method and finite resource bounds; preserve other active work. Revise or
split local work with a recorded reason when needed, without silently changing
this native goal or weakening evidence requirements. Finish acceptance checks,
update linked records and shared state through its integration owner,
and publish a recoverable checkpoint. If all useful work for this item is
blocked, record the blocker and exact resume action, report BLOCKED, and stop
without marking the item complete. Preserve healthy declared background jobs.
```

Completion of an item establishes that item's accepted result. Overall project completion requires the integrated deliverables and their validation. See [AGENTS.md](AGENTS.md#checklist-item-goals-and-parallel-work) for ownership, integration, and waiting rules.

This repository provides the operating agreement. Cloud jobs, durable storage, scheduled collection, and automatic continuation require actual setup and verification when the approved work needs them.

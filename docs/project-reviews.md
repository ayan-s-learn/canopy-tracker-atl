# Astra project reviews

Astra leads recurring reviews at agreed **progress milestones**, using the evidence so far to decide what to detail next. This is the cumulative review record; [checklist.md](../checklist.md) holds live task state and the next review. Reviews are agent work and do not require a human meeting unless a specific owner decision is needed. See the [glossary](glossary.md) for project terminology.

## When and how to review

1. **Trigger:** each review names the next review ID and an observable trigger, such as a defined set of inquiries completing or a development comparison becoming ready. Bring a review forward when a blocker or new evidence materially changes the next decisions. Record the reason; unfinished tasks retain their real status. No calendar schedule or automatic wakeup is implied.
2. **Prepare:** the integration owner gathers a compact packet of linked task results and revisions, passed/failed checks, coverage and uncertainty, blockers/human-action IDs, resource and recovery limits, and proposed next questions. Use existing records; do not duplicate logs or rerun completed inquiries for the meeting.
3. **Review with Astra:** inspect the evidence, challenge assumptions, decide what is supported, and choose the next bounded round of useful work. Inspect the actual files and next ready tasks, without prescribing methods, duplicating records or creating empty scaffolding. Record alternatives, consequential tradeoffs and unresolved objections. Name the actual model and review date; never label a Sol-only review as an Astra review. If Astra is unavailable, save the packet and pending status while authorized work continues; its availability is not an approval gate.
4. **Integrate:** append the outcome below, update the checklist, and create a [task folder](../AGENTS.md#task-folders) with a Brief for each ready task. Detail only work ready to launch: objective, inputs/dependencies, outputs, acceptance checks, ownership, bounds and evidence location under [AGENTS.md](../AGENTS.md). Identify parallel-ready work, follow-ups to unresolved findings, and the next review trigger. Keep later work as sketches. Integrate through the normal branch/review process, apart from the integration-only commits [AGENTS.md](../AGENTS.md#git-handoffs-and-stopping) lets the integration owner push to `main`.

Reviews guide priorities and write the next task Briefs; they add no approval gate. Workstream owners may start useful in-scope work between reviews, including coordinated work across teams, under the existing interface, evidence and authority rules. When the next trigger is reached, the integrator initiates the review at the next active session rather than waiting for a user reminder. Already authorized work and healthy jobs may continue while the review is prepared. If no active agent or supported wakeup exists, record the exact resume action rather than promising unattended review.

An Astra planning review does not itself pass a research gate. Preserve protected evaluation, independent review/reproduction and owner authority. If Astra helped design an approach, obtain a separate reviewer for the required independent challenge; agreement at a review is not quantitative validation.

## Review record

Use stable IDs (`AR01`, `AR02`, …). For each completed review, retain: date/model and contributors; triggering milestone and evidence revisions; findings and unresolved objections; decisions and reasons; next ready task IDs with linked briefs and owners or `unclaimed`; carried blockers and human actions; next review ID/trigger; integration revision. Add dated amendments rather than silently rewriting previous decisions. Pending entries must not imply a meeting occurred.

### Initial layout — T01–T04 (Astra, 2026-10-15)

- **T01:** `docs/research/imagery/` for findings and probe scripts; `manifests/imagery/` when separate source metadata is useful.
- **T02:** `docs/research/geography/` for findings and probes; `manifests/geography/` when useful.
- **T03:** `docs/research/permits/` for findings and probes; `manifests/permits/` when useful.
- **T04:** extend `docs/operations.md`; use environment files and executable checks appropriate to the chosen tooling. Defer shared code and storage layout until needed; create paths with their first artifact.

**Amended 2026-11-23:** superseded by [task folders](../AGENTS.md#task-folders); these records moved to `tasks/`.

### AR01 — Feasibility findings and next work

Held 2026-11-24 by Astra in the integration-owner session after T01–T04 completed. Evidence baseline `8ac1ac9`. The integration revision introducing this record and the three briefs is recoverable with `git log -1 --diff-filter=A --format=%H -- tasks/T05-paired-coverage/README.md`.

| Evidence reviewed | Decision and limit |
|---|---|
| [T01 window manifest](../tasks/T01-imagery/t01-windows.json). All four cached TIFF hashes matched. Both October pairs are in Fulton, with 0.6 m and 0.3 m pixels across epochs. | Retain 2023–2025 for pilot discovery. Check DeKalb, per-tile dates and measured registration before choosing pilot sites or a minimum event size. The older fallback lengthens the change interval and is warranted only if the recent pair cannot support a varied pilot. |
| [T02 geography and comparison sources](../tasks/T02-geography/t02-sources.json). The archived City, county and annexation inputs matched their hashes. The county overlay leaves 9,340 m² of City area unassigned. Recorded annexations fall on both sides of the October 2025 sample dates. | Inventory imagery across the whole dated City footprint, retaining the residual. Resolve municipal membership using local observation dates before historical attribution. Current parcels support exploratory overlap only. GT's 2023 zero value also denotes nodata, and its reuse terms remain unresolved. Exclude GT from reference truth and training in this round. |
| [T03 permit probes](../tasks/T03-permits/source-probes.json). Public sources returned building and selected arborist rows. The audit did not establish historical decision coverage for private trees or Parks records. | Keep [HA-0002](../HUMAN_ACTIONS.md#ha-0002--confirm-city-receipt-or-file-scoped-records-requests) open. Validate any delivery by authority, record family, dates and county portion before interpreting absences. Partial coverage leaves a case ambiguous. Imagery and reference preparation can proceed. |
| [T04 recovery check](../tasks/T04-runtime/README.md#recover-the-archived-geotiff). The 1,874-byte derivative matched the archived SHA-256. The four T01 originals were previously recovered from services. | Use small replayable windows now. Before costly acquisition or training, size the pilot and verify retrieval and retention in an authorized store for raw inputs or weights. Git recovery of one derivative establishes only that path. |

G1 remains open. The most consequential near-term risk is viewing new imagery before reserving development and protected geography. Begin the source inventory, split design and historical boundary work in parallel. Defer detector selection until the development comparison has a defined frame. Independent reference capacity and the eventual protected evaluation remain outstanding.

The three briefs opened unclaimed for this round are [T05 paired coverage](../tasks/T05-paired-coverage/README.md), [T06 reference design](../tasks/T06-reference-design/README.md) and [T07 historical geography](../tasks/T07-historical-geography/README.md). Revisit historical parcel vintages and split/merge evidence before interpreting parcel-level results.

### AR02 — Pilot footprint and reference feasibility

Review when T05 has reconciled paired coverage across the City and recorded a DeKalb pair or its access failure, and T06 has a versioned exclusion map and reference workload estimate. Use the available T07 membership evidence and mark any unresolved geography. Bring the review forward if either stream demonstrates that the proposed pilot or protected design is infeasible. Decide which pilot footprint and image preparation can proceed, what can be evaluated with available interpreters, and which G1 gaps still limit each claim.

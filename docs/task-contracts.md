# Ready task briefs

[checklist.md](../checklist.md) is the state entry point. [AGENTS.md](../AGENTS.md) defines decision rights and authority; [research direction](research-direction.md) defines the scientific commitments and current hypotheses. **T01–T04 are ready briefs.** Later work is outlined in the [workstream roadmap](../checklist.md#future-workstreams--revisable-unclaimed) and detailed as evidence arrives.

[Astra project reviews](project-reviews.md) use each round's evidence to detail the next ready work; AR01 follows T01–T04. Local subtasks and independent preparation can proceed between reviews. The [glossary](glossary.md) defines domain terminology.

## Rules shared by every item

Use the working agreement's [launch and parallel-work rules](../AGENTS.md#checklist-item-goals-and-parallel-work), [revision rules](../AGENTS.md#local-decisions-and-plan-changes), and [job-recovery requirements](operations.md#cloud-jobs-recovery-and-waiting). Keep each launch brief and its evidence in one linked task/experiment record, such as `docs/tasks/ID.md`. Suggested paths are conventions, not requirements.

The checklist owns live status and claims; the briefs below describe the work. Starting inputs can be validated intermediates or labeled fixtures; acceptance still requires evidence for the claimed scope. Negative findings may complete an inquiry without passing a scientific readiness gate.

## T01 — Verify candidate imagery intervals

- **Objective / starting inputs:** find a usable, accessible pair for local canopy-loss research. Start from P00's saved catalog evidence; do not repeat completed searches without a reason.
- **Suggested owner / write reservation:** imagery agent; `manifests/imagery/`, `docs/research/imagery/` and its task record, or agreed equivalents.
- **Useful output:** source/rights/date/coverage ledger, actual paired sample evidence, suitability/access limitations and a recommended interval or justified next access action.
- **Method freedom:** investigate 2023→2025 first if promising; compare 2019→2023 or another justified public pair when evidence favors it. Choose enough diverse windows to answer the next feasibility question. Metadata access, readable pixels, geographic coverage and phenology are distinct findings. Incorporate T02's boundary when available; do not wait for the entire geography inquiry to test known assets.
- **Acceptance evidence:** read actual bands/windows and validate acquisition date/range, CRS/grid/resolution, nodata, rights and source identity; document leaf/shadow/seamline concerns and missing inputs. Metadata alone cannot certify usable imagery. A documented negative inquiry can finish with bounded attempts and a concrete access package; imagery readiness remains unpassed.
- **Launch boundary:** choose a finite sample/query/download budget before collection; this is a feasibility inquiry, not a full-city acquisition. Coordinate temporary storage with T04. Preserve compact reproducible evidence immediately; declare raw sample recovery limits until durable storage is proven. Stop at sufficient decision evidence or an actual access/resource barrier.
- **Handoff / next action:** locate the official recent asset path and date metadata, using existing item IDs and recorded errors. Publish usable intermediates to the runtime/geography owners with checks; no model accuracy claim.

## T02 — Establish geography, parcels and comparison layers

- **Objective / starting inputs:** identify the real study jurisdiction and what parcel/comparison data can support. P00 supplies source leads and the GT comparison; no imagery completion is needed to start.
- **Suggested owner / write reservation:** geography agent; `manifests/geography/`, `docs/research/geography/` and its task record, or agreed equivalents.
- **Useful output:** dated official boundary, parcel source/vintage/schema matrix with representative geometry, GT access/rights findings and suitable neighborhood context leads. Record unexamined or inaccessible sources explicitly.
- **Method freedom:** prioritize the authoritative city boundary and relevant county parcel extracts; choose representative samples instead of mirroring counties. Investigate historical splits/mergers, public land and right-of-way. Follow GT's public data hub before preparing a contact request. An income context source needs a vintage and uncertainty appropriate for area-level reporting.
- **Acceptance evidence:** source IDs/terms, geometry validity, CRS/units/area checks, city versus county/mailing-address distinction, historical limitations and comparison of the old screening rectangle with the actual boundary. A discovery report may document unavailable data; it cannot certify complete historical attribution.
- **Launch boundary:** declare a finite source/extract budget using actual sizes/capacity. Stop after the current geographic decision is supportable; leave missing history/rights as scoped follow-up rather than an indefinite data hunt.
- **Handoff / next action:** retrieve and inspect the authoritative boundary, then share that validated intermediate with T01 immediately. Parcel/GT inquiries can continue separately under visible subtask ownership.

## T03 — Audit permit sources and temporal meaning

- **Objective / starting inputs:** determine what record searches can and cannot support. Start from P00's source/error evidence; imagery dates can remain candidate intervals during discovery.
- **Suggested owner / write reservation:** records agent; `docs/research/permits/`, `manifests/permits/discovery/` and its task record, or agreed equivalents.
- **Useful output:** jurisdiction × authority × record type × date coverage matrix; tested access/field semantics; redacted examples; effective-date rules and missing-source questions.
- **Method freedom:** diagnose actual access failures, discover the published export endpoint, and sample diverse records where accessible, including arborist reviews inside building records, DDH, status/amendment relationships and public/private responsibilities. Choose the sample and access route that resolve uncertainty; no broad scrape is required. Draft missing-export questions as soon as gaps are clear rather than waiting for every other stream.
- **Acceptance evidence:** distinguish landing-page access from actual records and completeness; preserve source errors and limits. Building records without tree-review evidence are context, not tree authorization. Verify relevant historical semantics from official sources. A bounded negative inquiry is valid evidence with a concrete next access action; it does not establish record absence or unlawful removal.
- **Launch boundary:** declare finite requests/sample/time limits, honor provider terms/rate limits, and stop at access barriers. Do not bypass authentication or send external communications. Do not commit owner/contact details.
- **Handoff / next action:** inspect accessible metadata and representative record families, sharing a versioned schema/coverage note with linkage and request-preparation work even before the full source inquiry closes.

## T04 — Establish a minimal reproducible environment and durable artifact path

- **Objective / starting inputs:** show how a successor can reproduce a real small geospatial operation and recover its artifacts. Use provisioned capabilities and a permitted sample, including a validated T01/T02 intermediate if available; no full-task dependency.
- **Suggested owner / write reservation:** runtime agent; environment/lock/ignore files and `docs/operations/` plus its record. Reserve root edits or isolate the checkout.
- **Useful output:** demonstrated environment/fixture reproduction, authorized storage round trip, recovery/retention/permission limits and a concrete storage action if the missing capability requires a human.
- **Method freedom:** choose the smallest maintainable environment and existing storage path that work. Containerization or a runner is justified by actual jobs, not by this task title. Runtime and storage may be separate subtasks with independently consumable outputs.
- **Acceptance evidence:** open/process a real permitted raster/vector fixture from a fresh directory using recorded versions; verify output tolerance; copy/retrieve/hash-check a real artifact from the authorized durable path. Document disconnect/crash/reboot/deletion survival honestly. A local file/checksum alone does not establish durability. Do not deliberately restart the host to test it.
- **Launch boundary:** estimate and declare finite setup/download/fixture limits from available capacity. No paid provisioning, scheduler or GPU merely for setup. A blocked storage subtask need not block environment work or other recoverable inquiry, but the entire T04 outcome remains incomplete until both checks pass.
- **Handoff / next action:** use an available permitted fixture, demonstrate the actual operation, then publish the environment and storage capabilities separately with their checks and exact retrieval/resume instructions.

## Earlier task sketches

At the owner's request, T05–T27 (including T17L) are retired as active task definitions in favor of the workstream roadmap. Their [IDs and descriptions remain in history](https://github.com/ayan-s-learn/canopy-tracker-atl/blob/f3349d7fa50ff2f884950f96d10339fa1fef63e9/docs/task-contracts.md#future-work--expand-when-useful). This is not completion: scientific and delivery requirements remain in the [research direction](research-direction.md). When new briefs are needed, record their relationship to the old sketches; do not silently reuse an old ID for unrelated work.

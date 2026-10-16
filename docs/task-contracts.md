# Ready task briefs and future roadmap

[checklist.md](../checklist.md) is the state entry point. [AGENTS.md](../AGENTS.md) defines decision rights and authority; [research direction](research-direction.md) defines the scientific commitments and current hypotheses. **T01–T04 are ready briefs. T05 onward are revisable roadmap sketches.**

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

## Future work — expand when useful

The stable IDs below preserve continuity. They describe likely outcomes and the evidence that will matter, not mandatory task boundaries. Workstream owners may activate a useful slice, combine related slices or replace a sketch after checking current state and authority. Write the short launch brief then; report its ownership/inputs/bounds to shared state. Do not leave a ready opportunity waiting for every earlier ID, and do not pretend a speculative sketch has passed acceptance checks.

## T05 — Prepare any necessary historical-records request

Prepare the smallest actionable request/export package once a concrete source gap is known, using a provisional interval if necessary. Final sending requires an exact approved scope/channel and existing authorization; delivery validation is separate. An export request need not await every imagery or parcel inquiry. Preserve coverage, cost and privacy limits; a prepared draft is not delivered data.

## T06 — Integrate and freeze the first study contract (G1)

Reconcile the current interval, region, data coverage and shared interfaces with the affected owners and independent scientific review. Version the agreement as evidence arrives; freeze a particular study/release only when needed for reproducibility. Readable suitable imagery and honest coverage/recovery are required to claim feasibility, not to begin every prototype. Missing permits limit reconciliation, not unrelated imagery work.

## T07 — Preregister reference, sampling and acceptance design

Develop the measurement/sampling protocol alongside feasibility work. Reserve protected geography and training exclusions **before local fitting, pseudo-training or tuning can contaminate it**. Before protected outcome inspection, specify estimands, inclusion probabilities, event/area rules, nonresponse, uncertainty, subgroup reporting and claim targets. Distinguish holdout-domain generalization from a full-domain map survey. Use development evidence to refine workload; review/freeze the relevant protocol before its protected use. Sample counts and staffing are not established yet.

## T08 — Build and assess paired pilot preparation

Build usable paired inputs with date/source/nodata masks and measured registration/phenology QC. A readable pair permits technical preparation before the whole reference protocol is finished; outcome-informed development still respects reserved evaluation areas. Select correction methods and batch sizes from observed errors and resources. Acceptance needs stable-feature checks, valid-area accounting and recoverable outputs, not a specific registration package.

## T09 — Prepare development reference annotation

Create clear paired-date annotation/uncertainty instructions and a usable delivery workflow. Tooling can start with labeled demonstration data; actual assignments require appropriate imagery, definitions and development/test separation. Select the packet size after effort estimates. Independently interpreted overlap and human review remain distinct from agent-assisted drafts; a ready packet is not reference truth.

## T10 — Validate development labels and reference feasibility

Check delivered IDs, dates, geometry, completeness, disagreement and adjudication; distinguish human interpretation from assisted labels. Publish accepted subsets with explicit scope rather than withholding all labels for one missing batch. Any overall reference claim still accounts for the full planned manifest and missingness. Refine development workload without inspecting protected outcomes.

## T11 — Compare inexpensive change baselines

Prepare executable baselines and controls as soon as compatible imagery/interfaces permit. A scientifically meaningful comparison needs accepted development references and protected exclusions; code running is not performance evidence. Choose a small comparison that answers the current uncertainty, including loss quality and practical cost, not a compulsory list of models or configurations. Negative results can justify a different method.

## T12 — Test one justified learned challenger (conditional)

Investigate a learned method when development evidence makes the question worthwhile. Select the architecture, variants and finite budget at launch, comparing with accepted baselines under equivalent evidence conditions. Respect protected areas, upstream-model lineage and existing resource authority. A challenger may be skipped or replaced with reasons; it is not a mandatory detour or an excuse for endless search.

## T13 — Select and freeze a method (G2)

Use independent review to select an evaluation candidate and freeze its code/configuration, relevant sampling protocol and realistic reference capacity. This binds that evaluated version, not every future experiment. Development amendments remain possible before protected use; test-guided changes require a new valid evaluation design. A useful simple method may win. Selection is not proof of achieved operational accuracy.

## T14 — Implement auditable parcel attribution

Implement/check geometry logic from an agreed event/parcel interface and explicit fixtures without waiting for a study-wide freeze. Accept real-world attribution only after integrating validated event and parcel artifacts, with area conservation, many-to-many relations, historical/boundary uncertainty and unassigned land accounted for. Crown overlap is not stem ownership; future module paths are negotiable.

## T15 — Build a versioned permit snapshot and coverage ledger

Normalize accessible source batches as their semantics/rights become known; missing export responses should block only affected coverage. Preserve source snapshots, status/record-family lineage, deduplication and privacy. Publish checked intermediates with limits. Parent acceptance reconciles its entire declared manifest, exclusions and missingness; the first successful batch does not establish complete records.

## T16 — Implement and audit three-way reconciliation

Develop matching from pinned interfaces and representative records/fixtures; integrate real events when available. Acceptance needs auditable date/location/status reasoning, edge-case checks, explicit coverage and retained ambiguity. Building-only evidence is not tree authorization. Missing-source abstention can be validated while matching performance remains unassessed; image loss remains a separate finding.

## T17 — Run the frozen detector on the accepted region

Process a finite versioned input manifest with the selected method and measured resource/recovery limits. Pilot/exploratory inference may happen earlier with its status explicit; final evaluation uses the frozen relevant outputs. Workstream owners choose/allocate disjoint batches. Parent completion reconciles all required units/exclusions, valid area, seams and duplicate events; no silent region shrinkage.

## T17L — Apply regional parcel and permit linkage

Apply accepted relation/matching logic to checked event batches, preserving every event and its lineage even when records are unavailable. Producer/consumer owners can integrate batches before all regional processing finishes. Freeze the specific joined release needed for evaluation/publication; reconcile event/area conservation, coverage and the complete declared manifest before claiming regional integration.

## T18 — Collect and seal protected reference observations

Prepare reference tools/protocols early. Make protected assignments under the reviewed design, with independent interpretation, correct inclusion probabilities, blinding and nonresponse handling. A model-dependent draw needs its **relevant frozen prediction frame**: image-only reference need not wait for permit linkage, while permit-review samples need their defined joined frame. Keep holdout generalization and full-domain map survey distinct. All required allocations and actual delivered observations must reconcile before the corresponding reference product is complete.

## T19 — Evaluate the integrated frozen system once (G3 analysis)

Evaluate available frozen components against their appropriate accepted references; image, parcel and permit evaluations need not wait for one another's missing data. Report their separate readiness and limitations. Integrated claims require compatible versions and combined evidence. Preserve the registered estimands, targets and design-consistent uncertainty; do not use test findings to tune and then present the same test as unseen. Regional totals require supported sampling, not a purposive holdout.

## T20 — Independently reproduce and challenge findings (G3 review)

Review consequential decisions as they arise and independently reproduce central calculations before promoting material claims. Inspect raw evidence, sampling, leakage, coverage and alternative explanations. Separate reviewer ownership from implementation; record unresolved objections. The required artifact is a reproducible scoped finding with its limits, not agreement among agents or a particular meeting sequence.

## T21 — Build a local map and evidence-card prototype

Explore the review workflow with clearly marked synthetic/development data and a provisional interface before all research is finished. Revise it with evidence and coordinated interface changes. Public-facing content must distinguish no data from no loss, expose dates/uncertainty/search coverage, and provide accessible explanations. Prototype acceptance is separate from approved publication of real findings.

## T22 — Assemble the reviewable public release bundle

Develop packaging and content structure early; connect only appropriately validated, version-compatible findings when preparing a release. Assemble the exact proposed public bundle with sources, coverage, rights/redaction checks, correction path and recovery. A methods/limitations release must not be presented as a validated operational system. Public detail, handling, deployment and costs need the required explicit authorization.

## T23 — Prepare research report and agency briefing

Draft methods, citations, stakeholder questions and message packages while research proceeds. Findings require accepted evidence; communication requires authorization. Credit GT and compare compatible quantities, separating endpoint-visible loss from all removals or net change. Prepare concrete feedback requests as soon as useful; do not require a finished website to seek an authorized agency conversation.

## T24 — Publish the approved website

Deploy the exact approved bundle using the authorized provider, audience and cost scope; verify the served result, correction ownership and recovery. A local build or saved artifact is not publication. An approved exploratory release can precede final operational readiness if accurately labeled; it does not complete the validated-system deliverable.

## T25 — Deliver the agency briefing and record feedback

Carry out authorized outreach/briefing and retain privacy-appropriate delivery/feedback evidence. Early authorized discussions can revise methods and product needs; the final research briefing still requires actual delivery of supported findings. Preparing slides or sending an invitation is not briefing completion, and participation is not endorsement.

## T26 — Demonstrate rerun and establish maintenance handoff

Exercise reproducibility, unit recovery and source/version drift handling as components become usable, rather than deferring maintenance until the end. Final handoff must demonstrate a representative clean rerun through the accepted pipeline, artifact retrieval and declared output tolerance, with custody/retention/correction responsibilities. Do not assume automatic continuation or next-epoch validity.

## T27 — Decide the next interval or jurisdiction (deferred)

Revisit future direction when a coverage limit, new dataset, partner need or maintenance result makes it useful. Preserve the current deliverable while comparing alternatives; no fixed calendar or compulsory completion of every other ID is needed to investigate an option. Expansion still needs jurisdiction-specific sources/validation and authority for any change beyond the agreed objective.

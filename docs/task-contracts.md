# Bounded execution contracts

Use [checklist.md](../checklist.md) for current status, claims and integration; this file specifies work. Dependencies mean **accepted outputs**, not a producer's running job. Each heading is one `/goal` item, not authorization to run the whole sequence. Read [direction](research-direction.md) and `AGENTS.md` first.

## Rules shared by every item

- **Owner/branch:** the checklist names the role and current claimant. All future items begin unclaimed. The integration owner claims/updates shared state. Use subbranch `goal/tNN-short-name` from an identified accepted campaign checkpoint for independent chats or overlapping edits. Shared-checkout agents may write only their reserved paths; only the integration owner stages/commits/pushes there. Always record actual branch/checkout and base SHA at launch.
- **Evidence:** leave `docs/tasks/TNN.md` with question, inputs and hashes, owner, base/result revision, commands/config, outputs/retrieval, checks and results, limitations, resource use, next action. Link detailed runs/manifests instead of embedding logs. Every accepted item links this record from the checklist. “Code written” alone never passes a data/evaluation task.
- **Recovery:** before a job, write and link a run record satisfying `AGENTS.md`, including finite scope, process/host, checkpoint, confirmed durable copy, exact validation/resume/stop commands and known survival limits. Stop starting units at the ceiling, preserve healthy authorized jobs as `waiting_for_job`, and checkpoint incomplete work. Reconcile existing outputs before any rerun. No unbounded retries, background services, or invented goal controls.
- **Authority:** existing environment/model allowance only; resource ceilings below are not grants of more capacity. No additional spending, external contact, login on behalf of the owner, public deployment or `main` writes without the required authorization. Follow documented source terms and access restrictions. Prepare human actions completely before marking them ready. A source/access barrier blocks only dependent work.
- **Default bound D:** one bounded session up to 2 hours, 2 CPU cores / 4 GiB RAM, 2 GiB new local artifacts, no GPU or new costs. Network collection at most 1 request/second, two connections per host, 100 requests and 1 GiB total unless a narrower/wider limit is stated below. Use provider limits when stricter. Reaching a bound is a checkpoint or justified new item proposal, not success. Long human waits use no active polling.
- **Integration:** producer schema + manifest + small permitted fixture; consumer contract check; required independent review; explicit merge/cherry-pick into `chore/autonomous-harness`; inspect combined diff/checks, then update state. Do not mark downstream items ready from unintegrated unvalidated branches. Temporary fixtures must not expose personal records or protected labels.
- **Completion:** pass the item's checks and preserve evidence remotely. A documented negative result completes a *feasibility investigation* only where stated; it does not pass the downstream feasibility gate. If otherwise gated, retain `blocked`, prerequisite/HA ID and exact resume action. No healthy job is a human blocker.

## T01 — Verify candidate imagery intervals

- **Role / prerequisites:** imagery agent; P00. Read the saved STAC probe and its bbox limits.
- **Owns / outputs:** `manifests/imagery/`, `docs/research/imagery/`, `docs/tasks/T01.md`; source/rights ledger, date/coverage index, small paired readable sample manifests, quality contact sheets where permitted, and preferred/fallback access decision. No modeling.
- **Scope / next action:** locate 2025 official Atlanta assets and acquisition/seamline metadata, inspect up to six paired windows across likely pilot conditions with 2023; if unavailable, test 2019/2023. Use the existing 2023 item IDs rather than rediscovering them. Separate metadata discovery, actual bytes, visual suitability and recoverability. Record exact additional host/account needs, including the returned COG host. Do not claim citywide completeness before T02 boundary integration.
- **Checks:** open actual bands/windows, validate CRS/transform/GSD/nodata/date/rights and checksums; document leaf/shadow/seamline issues and expected/missing inputs. No eligible pair is an acceptable negative feasibility result if attempts and a concrete smallest access action are preserved. Metadata alone cannot certify pair readiness.
- **Bound / stop:** 2 CPU / 4 GiB, 6 GiB scratch, 4 GiB transfer, 2 hours; no full-city download or GPU. If asset restrictions prevent samples, prepare the executable access package and retain uncertainty rather than bypass controls. Raw downloads remain disposable until T04 confirms storage.
- **Evidence:** sample metadata, read/inspection logs and recommended interval; no empirical accuracy claim.

## T02 — Establish geography, parcels and comparison layers

- **Role / prerequisites:** geography agent; P00.
- **Owns / outputs:** `manifests/geography/`, `docs/research/geography/`, `docs/tasks/T02.md`; dated city/jurisdiction/NPU geometry, parcel-source matrix and representative sample, GT-data discovery/rights note, income-context source candidate.
- **Scope / next action:** retrieve authoritative City of Atlanta boundary and verify its portions in both counties. Inspect Fulton/DeKalb parcel IDs, geometry, public-land/right-of-way handling, vintage/history availability and terms. Follow GT's advertised data hub to actual metadata/downloads if accessible; no contact yet. Identify an area-level income dataset with vintage and uncertainty suitable for reporting.
- **Checks:** geometry validity, CRS/unit/area sanity, stable source IDs, jurisdiction rather than mailing-address logic; enumerate missing history/coverage. Compare the archived bbox with actual boundary. GT source availability is distinct from permission and reference independence. Failure to acquire parcels is a recorded source barrier, not an assumption that they are routine.
- **Bound / stop:** 1 CPU / 2 GiB, 2 GiB scratch/transfer, 90 minutes, metadata plus representative extracts; do not mirror whole counties. Preserve usable boundary and schema evidence even if historic parcels/GT layers remain unresolved.
- **Evidence:** source manifests, small geometry checks and boundary comparison; exact dependent access requirements.

## T03 — Audit permit sources and temporal meaning

- **Role / prerequisites:** records agent; P00.
- **Owns / outputs:** `docs/research/permits/`, `manifests/permits/discovery/`, `docs/tasks/T03.md`; jurisdiction × authority × record type × date coverage matrix, terms/access note, redacted schema/example interpretations and effective-date rules ledger.
- **Scope / next action:** diagnose observed Accela/USDA-independent access failures once, discover the actual ARC export endpoint from published metadata, and inspect up to 30 representative public records if accessible (including tree reviews embedded in building records, DDH, statuses and amendments). Verify private/public-land responsibilities and historical rules from official sources. No broad scrape or communications.
- **Checks:** record-level access and field semantics demonstrated separately from landing-page reachability; building permits cannot stand in for tree approval. Include missing types/periods, source update lag, geocoding quality and parent/child records. A fully documented negative access result is an acceptable feasibility finding, with a minimal export/access proposal; completeness cannot be asserted from examples.
- **Bound / stop:** 1 CPU / 2 GiB, 0.5 GiB scratch, 250 MiB transfer, 60 requests, 90 minutes. Stop at authentication/access barriers; no CAPTCHA bypass, new account or API spending. Do not commit owner/contact details.
- **Evidence:** exact sources/errors, representative field dictionary and search-universe limits; records-request inputs for T05.

## T04 — Establish a minimal reproducible environment and durable artifact path

- **Role / prerequisites:** runtime agent; P00.
- **Owns / outputs:** environment/lock files, `.gitignore`, `docs/operations/runtime.md`, `docs/operations/storage.md`, `docs/tasks/T04.md`, tiny allowed fixture. Coordinate root-file edits on an isolated branch. No general agent scheduler.
- **Scope / next action:** use provisioned CPU and ordinary Python tools to open/reproject a small real permitted raster/vector fixture; lock the needed environment. Inspect available authorized storage from known configuration, select a path, and demonstrate upload/retrieval/hash verification of the fixture. Git may preserve compact permissible evidence; it is not a raster/model store. If no durable large-artifact path exists, prepare a concrete options/action package before long jobs.
- **Checks:** reproduce fixture output from a fresh directory and locked environment; retain command/versions and expected numeric/geometric tolerance. Document storage permissions, retrieval steps, retention and disconnect/crash/reboot/deletion survival without claiming untested guarantees. A local checksum alone does not pass durability. No deliberate host restart.
- **Bound / stop:** 2 CPU / 4 GiB, 2 GiB scratch, 1 GiB transfer, 2 hours. No GPU, container build unless genuinely needed, provisioning or paid storage. Can finish the environment portion while durability remains `blocked`; do not mark the whole item complete until the storage check passes.
- **Evidence:** lock, fixture reproduction, recorded successful restore or prepared HA with exact unblock/restore check.

## T05 — Prepare any necessary historical-records request

- **Role / prerequisites:** records agent; T01–T03 discovery accepted; a candidate interval may remain conditional.
- **Owns / outputs:** `docs/human/records-request/`, `docs/tasks/T05.md`; integration owner allocates any HA ID and edits `HUMAN_ACTIONS.md`.
- **Scope / next action:** reuse verified public inputs; prepare the smallest export request covering imagery interval plus justified validity/lookback/lag and relevant record families, including data dictionary and coverage confirmation. Include missing-system/public-tree questions only where they affect scope. Identify the verified contact/channel, expected format, delivery route and fee-approval limit; do not send. If public records suffice, document why no request is needed.
- **Checks:** concrete draft and click/submit/delivery instructions, no assertion of guaranteed free service or response completeness; privacy/minimization and delivered/missing coverage checks. Human hands-on/runtime/cost estimates labeled as estimates. Sending and any fee require authorization.
- **Bound / stop:** D, document preparation only. Completion means a ready package or evidence that none is necessary, never records delivered. Actual receipt is consumed by T15.
- **Evidence:** published package revision, allocated HA ID if needed, and exact T15 delivery-validation action.

## T06 — Integrate and freeze the first study contract (G1)

- **Role / prerequisites:** integration owner; T01–T04. Readable usable pair and recoverable sample are required, not merely completed discovery reports.
- **Owns / outputs:** `config/study.yaml`, `docs/decisions/study-scope.md`, `schemas/` initial interface definitions, `docs/tasks/T06.md`; checklist update.
- **Scope / next action:** choose interval, dated boundary, at least three separated pilot areas, candidate projected grid, data/permit coverage strata and explicit non-goals. Define interface contracts in the direction record. Integrate source IDs without copying personal fields. Name which permit types/land categories are in scope, unknown or unavailable.
- **Checks:** paired-image overlap within chosen area, sample readability/rights/date QC, spatial-unit consistency, durable manifest recovery, and no unsupported full-city claim. Independent review of interval and pilot coverage. Record fallback and excluded areas; no silently substituted epoch. Permit incompleteness may yield a loss-only pilot contract with reconciliation gate explicitly unpassed.
- **Bound / stop:** D, no regional processing. If no suitable pair or durable path, block with exact T01/T04/HA resume action; other independent items continue.
- **Evidence:** signed-off decision rationale, contract examples/checks and reviewer findings; actual frozen inputs.

## T07 — Preregister reference, sampling and acceptance design

- **Role / prerequisites:** evaluation agent; T06.
- **Owns / outputs:** `docs/protocols/evaluation.md`, `config/evaluation.yaml`, protected-footprint manifest, `docs/tasks/T07.md`.
- **Scope / next action:** read primary sampling methods, define canopy/loss/uncertainty labels, event matching/fragmentation/boundary rules, spatial buffers, development versus protected blocks, probability sampling and candidate-review estimands. Plan model-dependent strata/draw algorithm now; actual protected draws occur after freeze in T18. Both loss and nonloss must be sampled. Estimate effort and effective sample size using conservative prevalence/clustering scenarios, then refine using development pilot only.
- **Checks:** reproduce sample-size/precision calculations. Separate buffered-holdout generalization from the optional full-domain frozen-map probability survey (including development geography and labeling prior-training overlap). Every unit in a claimed population estimand needs known nonzero inclusion probability; otherwise limit estimates to the supported domain. No pseudo-training leakage into the reserved geographic holdout; design/cluster-consistent uncertainty and preregistered reference nonresponse adjustment. Specify operational precision/recall/interval-width/coverage targets, subgroup reporting rules, human budget and test-access policy. Independent methodological review; no protected labels inspected. T10 may inform an explicitly versioned amendment using development evidence only; T13 freezes the final reviewed protocol and confirmed annotation capacity before T17/T18.
- **Bound / stop:** D; at most three sampling scenarios. If reference workload is unaffordable, propose narrower claims or scope explicitly before test, not a convenient biased sample. Human-resource decisions get a prepared package.
- **Evidence:** versioned preregistration, calculations, reviewer response, protected/development spatial separation checks.

## T08 — Build and assess paired pilot preparation

- **Role / prerequisites:** imagery/preparation agent; T06, T07, T04.
- **Owns / outputs:** `src/canopy/acquire/`, `src/canopy/prepare/`, preparation tests, pilot manifests/QC report, `docs/tasks/T08.md`.
- **Scope / next action:** materialize up to six fixed paired pilot windows on the frozen grid, preserve nodata/source/date masks; test no-correction versus warranted registration on stable ground with independent checkpoints. Measure seamlines, phenology and area/parcel sensitivity to plausible residual shifts. Build only the resumable download/prepare units this needs.
- **Checks:** band/grid/date consistency, correct resampling, held-out ground residuals before/after, no edge/nodata loss artifacts; idempotent unit validation and recovery of an intentionally incomplete temporary fixture, not a live host restart. Exclude/downgrade unresolved areas with reasons. Establish usable-area mask and resource benchmark.
- **Bound / stop:** up to 4 CPU / 8 GiB, 8 GiB scratch, 4 GiB new transfer, 3 hours; no GPU. Correct at most two registration strategies beyond the uncorrected baseline. Unsuitable imagery yields no-go evidence for T06 revision, not fabricated success.
- **Evidence:** exact paired inputs/config, checkpoint residuals, visual QC, resource measurement and recovery results.

## T09 — Prepare development reference annotation

- **Role / prerequisites:** reference agent; T07, T08.
- **Owns / outputs:** `docs/human/development-annotation/`, annotation schema/tooling, development assignments, `docs/tasks/T09.md`; HA allocation by integrator.
- **Scope / next action:** prepare at most 24 initial paired development sites spanning stable/change and difficult cover conditions, a clear uncertainty rubric and independent overlap assignments. Sample sites according to the development plan; targeted failure examples are flagged. Package dates/context, optional agent draft assistance, safe delivery and correction steps.
- **Checks:** pilot two end-to-end annotation round trips using clearly marked demo labels; schema/geometry checks and instruction comprehension; independent human interpretations not anchored to model masks on the agreement subset. State expected human effort and no need for private-property entry. Protected evaluation sites stay excluded.
- **Bound / stop:** D, packet/tool preparation only; completion is a ready executable packet, not reference truth. Integrator opens a concrete HA; T10 waits for delivered labels without polling.
- **Evidence:** exact packet revision, HA ID, sample manifest, demonstrated export/import checks and annotation-time estimate basis.

## T10 — Validate development labels and reference feasibility

- **Role / prerequisites:** evaluation/reference agent; T09 and human delivery accepted for inspection.
- **Owns / outputs:** versioned development reference manifest, agreement/uncertainty report, `docs/tasks/T10.md`; large/raw labels in the authorized artifact store.
- **Scope / next action:** validate delivered IDs/geometry/dates/completeness, quantify overlap agreement and adjudicate unresolved cases with the designated human reviewer. Keep provenance distinguishing human interpretation, assisted drafts and unresolved labels. Refine workload estimates for T07 without using protected outcomes.
- **Checks:** expected/complete/missing labels accounted for; accepted ambiguous/obscured handling; labels independent enough for intended use; agreed semantic definition. Record human corrections and do not close HA until delivery checks pass. Inconsistent labels trigger smallest correction request under the same HA ID.
- **Bound / stop:** D, one delivery of the initial ≤24 sites. Waiting for humans is `blocked`, not compute. Additional annotation batches require explicit child items after demonstrated need.
- **Evidence:** label version/hash, disagreement table, adjudication history and verified consuming split IDs.

## T11 — Compare inexpensive change baselines

- **Role / prerequisites:** detection agent; T08, T10 and T07 protected exclusions.
- **Owns / outputs:** `src/canopy/detect/`, detection tests, `experiments/baseline-comparison/`, `docs/tasks/T11.md`.
- **Scope / next action:** compare a spectral/texture random forest and one accessible fixed pretrained/height-derived candidate on identical development data; retain a simple spectral threshold control. Verify model inputs, source years, rights and training overlap first. If pretrained assets are inaccessible, record it and compare the available simple methods. Evaluate paired loss and canopy per epoch, annotation effort, wall time and errors; include physical MMU/filter ablations within a predeclared small sweep.
- **Checks:** development-only tuning; deterministic masks/events and event-area thresholds; shared-model bias cancellation treated as a hypothesis; size-specific loss metrics and stable-control false positives. Show thin/fragmented/edge cases. No protected metric computed or cited.
- **Bound / stop:** 4 CPU / 8 GiB, 8 GiB artifacts, 4 hours, at most six predeclared configurations on the accepted pilot; no new GPU. Stop at comparison/decision evidence, not an indefinite accuracy chase.
- **Evidence:** inputs/labels/configs/code hashes, predictions, metrics, error gallery, measured resource and human-effort comparison; recommendation for T12 or skip.

## T12 — Test one justified learned challenger (conditional)

- **Role / prerequisites:** detection agent; T11 exposes a specific remediable failure; T13 integrator records whether this item is activated or not selected.
- **Owns / outputs:** shared detection module on an isolated branch, `experiments/learned-challenger/`, `docs/tasks/T12.md`.
- **Scope / next action:** one hypothesis, e.g. small U-Net fine-tuning improves crown/ground separation beyond RF. Compare on the same development split; use weak labels only outside protected areas and describe their errors. If both-date adaptation is tried, freeze one final procedure and test both dates. No new architecture family spree.
- **Checks:** same loss metrics/cost budget as T11, source/model license and overlap audit, recoverable model/optimizer state, baseline comparison and ablation; improvement must justify ongoing complexity. Failure/negative result is valid experiment evidence.
- **Bound / stop:** at most two variants and two seeds, 4 hours total training within an **already available authorized** accelerator or measured CPU budget, 12 GiB artifacts. No provisioned/billed GPU. If unavailable, block or retain baseline; never pretend a model trained.
- **Evidence:** experiment decision, full training/resume record, immutable weights and outputs in durable storage. A skipped task is `not selected`, not an experiment passed.

## T13 — Select and freeze a method (G2)

- **Role / prerequisites:** integration owner and independent reviewer; T11, T07; T12 completed or explicit not-selected disposition.
- **Owns / outputs:** `docs/decisions/method.md`, versioned detector/config/model manifest, `docs/tasks/T13.md`.
- **Scope / next action:** choose the simplest supported method, exact MMU/filters/abstention/ranking and registration policy; justify full-region resource estimates. Freeze before protected inference/review. Review raw examples and reproduced development comparisons, not just aggregate scores.
- **Checks:** measurement definition respected; no evaluation leakage; comparison, label quality and registration support a useful queue. Accept the final reviewed T07 revision, including sample allocation, precision lower-bound criterion, recall point target and interval-width criterion, minimum useful yield/coverage, reference nonresponse rules and confirmed human capacity. Development-driven amendments must be dated/justified before this freeze; do not presume annotation capacity exists. Independent objections resolved or constrain scope. Explicit pass/no-go/revise outcome. A no-go decision record can be complete while G2 remains unpassed.
- **Bound / stop:** D, no new model search. A material change to study scope/targets is recorded and surfaced before test; create bounded follow-up item if needed.
- **Evidence:** reproducible selection table, immutable config, independent review response and authorized inference batch budget.

## T14 — Implement auditable parcel attribution

- **Role / prerequisites:** geography agent; T06 permits fixture implementation alongside model work; final acceptance also requires the accepted T11 pilot-event artifact (or accepted T12 replacement).
- **Owns / outputs:** `src/canopy/attribute/`, attribution tests/fixtures, `docs/tasks/T14.md`.
- **Scope / next action:** construct event–parcel overlaps with jurisdiction/vintage and uncertainty, supporting one-to-many and many-to-one cases, unassigned land, parcel splits and boundary sensitivity. Ingest only needed parcel fields. Use contract fixtures until detected events exist.
- **Checks:** area conservation, no double counting, stable IDs, CRS/unit correctness, invalid geometry handling, cross-boundary and missing-history fixtures. Report crown-overlap relation rather than property-owner responsibility. Fixture pass is a checkpoint only; integrate the named accepted T11/T12 real pilot-event artifact before marking T14 complete. If waiting for that producer, record the dependency and preserve the implementation checkpoint.
- **Bound / stop:** D, ≤1,000 fixture/pilot events. No county-wide mirror or owner enrichment.
- **Evidence:** expected geometry/area fixture results, real pilot checks and unresolved parcel-vintage limits.

## T15 — Build a versioned permit snapshot and coverage ledger

- **Role / prerequisites:** records agent; T03, T06; consume T05/HA delivery if needed, not necessarily before public-source work.
- **Owns / outputs:** `src/canopy/permits/ingest*`, ingestion fixtures/tests, permit manifests and coverage ledger, `docs/tasks/T15.md`.
- **Scope / next action:** validate actual public/exported records for the fixed study interval, preserve immutable source snapshots outside public Git, normalize record families/status history/address/parcel/date fields, deduplicate and enumerate holes. Compare totals by type/month to source reports when available without treating those reports as proof of row completeness.
- **Checks:** expected/delivered coverage, source schema change detection, duplicate/status/amendment behavior, failed-versus-empty distinction, appropriate PII minimization and provenance. An unavailable-source disposition may be accepted for a deliberately limited product; it is not successful acquisition and cannot support unmatched claims.
- **Bound / stop:** first batch ≤10,000 records, 2 GiB, 3 hours, provider-rate limits. Subsequent batches get explicit manifest-backed child items if needed. Parent T15 remains incomplete until the entire fixed coverage manifest and every child batch/accepted exclusion reconcile; one batch cannot certify the whole snapshot. Access/response gaps remain linked to the existing HA.
- **Evidence:** normalization manifest, coverage matrix, source counts/hashes, redacted examples and delivery checks.

## T16 — Implement and audit three-way reconciliation

- **Role / prerequisites:** records/linkage agent; T14, T15; T06 contracts.
- **Owns / outputs:** `src/canopy/permits/match*`, match fixtures/tests, rule/config ledger, `docs/tasks/T16.md`.
- **Scope / next action:** join evidence using source-specific validity/date rules, geography, identifiers, record family and status; return explanations/candidates and preserve ambiguity. Use up to 50 development cases spanning all outcomes/coverage states. Record unknown applicability and rules that changed inside the event interval.
- **Checks:** no tree-authorization claim from building-only records; pending/expired/revoked/amended/emergency, multiple-address/parcel, incomplete-history and public-land cases; absence with unknown coverage remains ambiguous. Manual override audit and reproducible output. Prepare blinded permit-adjudication rubric for T18. If all sources unavailable, validate only abstention behavior and label matching performance unassessed.
- **Bound / stop:** D; no legal determinations or outreach. Schema integration with real pilot events required.
- **Evidence:** edge-case tests, development adjudication/errors, actual source-search limitations and initial compatible-record quality report.

## T17 — Run the frozen detector on the accepted region

- **Role / prerequisites:** pipeline agent; G2 passed (T13), T04, T08; exact finite regional input manifest approved by integration owner.
- **Owns / outputs:** regional acquisition/preparation/inference manifests, loss/quality layers, run records, `docs/tasks/T17.md`.
- **Scope / next action:** benchmark extrapolation from pilot, then process only fixed manifest units; tile overlaps/halos and seams deduplicated; record missing and unsuitable areas. Run model without inspecting protected labels. No new thresholds or implicit jurisdiction expansion.
- **Checks:** per-unit validity, expected/complete/failed/empty counts, valid-area denominator, stable event IDs, no tile-edge duplication, checksummed durable outputs and confirmed restore of one finished unit. Compare resource use to pilot estimate; central outputs reproducible within stated numerical tolerance.
- **Bound / stop:** initial batch ≤8 paired quads, 6 hours, 4 CPU / 8 GiB, 50 GiB scratch maximum within actual capacity; accelerator only if already authorized and budgeted by T13. T13 specifies smaller limits if appropriate. If region exceeds the batch, integrator creates explicit T17-BNN tasks with disjoint manifests and the same checks; parent remains incomplete until all accepted units/exclusions integrate. No indefinite “process everything” goal.
- **Evidence:** saved logs/manifests, exact resume/stop commands, last durable copy and regional coverage accounting. Healthy jobs are `waiting_for_job`.

## T17L — Apply regional parcel and permit linkage

- **Role / prerequisites:** integration/pipeline agent; T17 regional events, accepted T14/T15/T16 artifacts (or their explicit source-unavailable disposition). Partial detector batches may feed named linkage batches, but parent completion requires the fixed regional manifest.
- **Owns / outputs:** integrated event–parcel–record release tables and manifests, `docs/tasks/T17L.md`, run records. Use existing attribution/matching modules, not a second pipeline. Branch `goal/t17l-regional-linkage`.
- **Scope / next action:** apply the accepted parcel and permit rules to each frozen regional event; retain all losses regardless of permit coverage, with unmatched/ambiguous/matched semantics and provenance. Freeze the exact joined release and search-universe version for T18 sample packets and T19 evaluation.
- **Checks:** every detector event accounted for, including unassigned land and source gaps; no area/event multiplication across parcel/permit joins; full-row lineage, correct historical/jurisdiction coverage, stable IDs, schema compatibility, deterministic output and durable retrieval. If permit sources are absent, run the explicit ambiguous/unavailable path and mark matching quality unassessed; loss-only results can progress without implying permit readiness.
- **Bound / stop:** first batch ≤10,000 events, 2 CPU / 4 GiB, 2 GiB scratch, 2 hours. Create explicit disjoint manifest-backed child items if larger; parent stays incomplete until all fixed units/exclusions are reconciled. No new source scrape or threshold tuning.
- **Evidence:** detector/parcel/permit/config hashes, coverage and area-accounting checks, exact joined artifact manifest, restore and consumer checks.

## T18 — Collect and seal protected reference observations

- **Role / prerequisites:** evaluation custodian; final T07/T13 protocol, frozen T17L integrated outputs. Human delivery is required for completion, not for starting packet preparation.
- **Owns / outputs:** protected sample/assignment manifest, `docs/human/protected-reference/`, sealed reference artifact and adjudication ledger, `docs/tasks/T18.md`; HA allocated by integrator.
- **Scope / next action:** execute the preregistered seeded probability/candidate draws with explicit frame labels (geographic holdout generalization; full-domain map survey if selected; operational event review), verify inclusion probabilities, prepare date-correct imagery and record packets, blind interpreters appropriately, and validate independent human delivery. Full-domain survey may include development geography; flag prior annotation/training overlap and do not call that sample unseen geography. Reuse T09 tools; keep new references out of developer access until release evaluation. Include nonloss and uncertain areas, not only compelling clearing examples. Field observations are separately labeled present-day corroboration.
- **Checks:** complete sampled-unit accounting, independent overlap/adjudication, uncertainty labels, no replacement of difficult sites by convenient ones; missing-reference mechanism and impact stated. Sample size/strata meet T07 or claims explicitly remain unsupported. Do not treat LLM labels or selected field visits as independent truth.
- **Bound / stop:** D for preparation/QA, first delivery ≤300 units; if T07 requires more, split explicit sample-ID batches before launch without changing design. Parent T18 stays incomplete until all allocations/batches in the fixed manifest are reconciled, delivered observations verified, and missing references handled by the preregistered nonresponse procedure with resulting limits on claims. Missing labels are never silently treated as observed. Human wait is blocked under HA, no repeated reminders. A prepared packet or first batch alone is not completion.
- **Evidence:** sampling code/config/seed, inclusion probabilities, annotation provenance/agreement, correction history and final sealed hash.

## T19 — Evaluate the integrated frozen system once (G3 analysis)

- **Role / prerequisites:** evaluation agent; frozen integrated T17L release and T18 reference; final T07/T13. Missing-permit dispositions constrain matching claims.
- **Owns / outputs:** `src/canopy/evaluate/`, evaluation checks, immutable tables/figures and evaluation report, `docs/tasks/T19.md`.
- **Scope / next action:** compute the separate canopy/change/parcel/permit metrics, probability-weighted area estimates if supported, uncertainty/sensitivity, subgroup denominators, abstention/coverage and fixed-review-budget yield. Compare simple ranking and document all exclusions. Distinguish detected area, adjusted gross loss, and unknown area.
- **Checks:** estimators reproduce on a known analytical fixture; design weights/clustering handled; no zero-denominator pass; geographic-holdout and full-domain map-survey metrics remain distinct; no citywide adjusted area from a purposive holdout. Acceptance targets evaluated exactly; GT comparison labeled external and spatial/temporal support harmonized. State endpoint-visible loss, not all interval removals. No final metric used to tune. Explicit readiness table for each component and claims inventory.
- **Bound / stop:** ≤4 CPU / 8 GiB, 4 hours, fixed release/sample only. A negative result is a completed evaluation, not G3 passed. Any revision consumes a new development/test plan; no repeated test peeking.
- **Evidence:** all commands/configs, label/prediction hashes, numerical tables, intervals, failure strata and pass/fail decision.

## T20 — Independently reproduce and challenge findings (G3 review)

- **Role / prerequisites:** reviewer independent of detector/evaluation implementation; T19.
- **Owns / outputs:** `docs/reviews/release-candidate.md`, independent reproduction record, `docs/tasks/T20.md`; no quiet edits to evaluated results.
- **Scope / next action:** retrieve release inputs and run central calculations from the frozen revision in a fresh directory; inspect sample design, leakage, numerator/denominator logic, source coverage, licensing and uncertain matches. Challenge at least one plausible alternative explanation (registration/phenology/source gaps).
- **Checks:** central counts, area and metrics reproduced within declared tolerances; disagreements resolved through tracked changes and rechecks; claims bounded by evidence. Independent human/domain feedback is desirable but agent agreement is not truth. Unresolved material objections block promotion.
- **Bound / stop:** D plus ≤4 hours fixed evaluation rerun if measured need; no new training. Record unable-to-reproduce as a finding, not a waived check.
- **Evidence:** reviewer identity/role, exact reproduced values, review response and explicit G3 decision.

## T21 — Build a local map and evidence-card prototype

- **Role / prerequisites:** presentation agent; T06 interface contracts. Can run alongside research.
- **Owns / outputs:** `web/`, presentation fixtures/checks, `docs/product/review-workflow.md`, `docs/tasks/T21.md`.
- **Scope / next action:** demonstrate review tasks with clearly marked synthetic/development data: coverage/date lookup, paired evidence, uncertainty, record explanation and aggregate summary. Use independent data bundles and accessible tables; estimate payload/tile needs before adding infrastructure. Prepare a concrete public-granularity/record-handling decision package showing both aggregate and parcel-detail options.
- **Checks:** fixture no-data differs from no loss; triage language and three buckets correct; stale/partial records visible; keyboard/mobile/table alternatives; no owner names, secrets or production-looking mock claims. Local production build and interactions pass. No hosting account or deployment.
- **Bound / stop:** D, static frontend, ≤500 features/10 MiB fixture payload; do not build an authentication/backend platform without demonstrated need.
- **Evidence:** local preview/build results, workflow checks, screenshots where useful, prepared release-choice package for a later HA.

## T22 — Assemble the reviewable public release bundle

- **Role / prerequisites:** release agent; G3 decision T20, T21; any failed science gate limits release to clearly labeled methods/limitations, not validated findings.
- **Owns / outputs:** `src/canopy/release/`, versioned release manifest/bundle, `docs/releases/`, `docs/tasks/T22.md`.
- **Scope / next action:** connect accepted outputs to website, evidence cards, methods/data cards and downloads; render exact proposed public content. Apply chosen or recommended aggregate-first granularity; include reviewed examples only when permissible. Prepare hosting/retention/access/cost options and rollback plan, with a precise proposed deployment.
- **Checks:** all findings trace to accepted tables; maps show denominator/missingness/interval; license/attribution/redaction/accessibility/load checks; public bundle excludes restricted records and protected material not approved for sharing; no causal, violation, assessed-fee or unsupported performance claim. Archive exact artifact hashes and previous-version recovery.
- **Bound / stop:** D, ≤1 GiB bundle; local packaging only. Prepare HA for exact granularity/handling and deployment scope/cost if not already authorized. Package readiness is not publication approval.
- **Evidence:** reproducible build, content review, complete review URL or accessible artifact, release decision package and deployment acceptance steps.

## T23 — Prepare research report and agency briefing

- **Role / prerequisites:** research communication agent; T20; use T22 visuals when ready, but do not block report preparation on publication.
- **Owns / outputs:** `docs/briefing/`, reproducible figures/tables, claims/source index, `docs/tasks/T23.md`.
- **Scope / next action:** write a methods/results/limitations report and short briefing showing what changed, reliability at useful scales, permit-search gaps, example inspection workflow and realistic next collaboration request. Credit GT and compare only compatible quantities. Prepare contact/message and feedback questions for a relevant agency; do not send.
- **Checks:** every quantitative claim linked to a source/table/revision; observed versus inferred clear; negative results retained; audience can identify what requires inspection. No fabricated “unpermitted acreage.” Rebuild figures from release manifest; independent narrative review.
- **Bound / stop:** D, concise briefing (target ≤10 slides plus technical appendix). Human-action package includes authorized sender, audience/channel, proposed time commitment and delivery evidence.
- **Evidence:** report/deck, regenerated figures, citations, reviewed message and HA ID when ready.

## T24 — Publish the approved website

- **Role / prerequisites:** deployment owner; T22 and explicit authorization for exact public content, granularity, address-linked handling, hosting/cost and deployment. Independent science gate must permit the proposed claims.
- **Owns / outputs:** hosting configuration for the selected platform, release/deployment log, `docs/tasks/T24.md`.
- **Scope / next action:** deploy the approved immutable bundle; preserve prior version and execute smoke/access checks. No audience expansion or unapproved data added during deployment. Use provider-supported credentials and rollback.
- **Checks:** actual URL serves expected release hash/content; maps/downloads/coverage/uncertainty work; no protected fields; rollback and correction/update owner recorded. A saved artifact without an accessible deployed result does not complete this item.
- **Bound / stop:** D, only approved provider/resources. If no approval, remain blocked under HA; continue unrelated maintenance/report work.
- **Evidence:** approved scope record, URL, artifact revision, observed deployment/smoke results and recovery instructions.

## T25 — Deliver the agency briefing and record feedback

- **Role / prerequisites:** owner/designated presenter with agent preparation; T23 and authorized external communication/delivery.
- **Owns / outputs:** `docs/briefing/delivery-and-feedback.md` (minimize personal information), `docs/tasks/T25.md`.
- **Scope / next action:** execute the approved delivery/meeting route; human presents or authorizes a specific supported alternative. Capture whether the output helps inspection triage, review capacity, false-positive cost, missing record types and corrections. Convert actionable feedback into bounded follow-up proposals.
- **Checks:** evidence of an actual briefing delivered to at least one agency, with date/audience and feedback or explicit no-feedback note; sending an invitation or preparing slides is not completion. Do not claim endorsement without evidence.
- **Bound / stop:** one authorized outreach/briefing package; no repeated unsolicited contacts, automated reminders or invented acceptance. Wait on human action without polling.
- **Evidence:** delivery confirmation and documented response/limitations, with privacy-appropriate recovery path.

## T26 — Demonstrate rerun and establish maintenance handoff

- **Role / prerequisites:** maintenance agent; T20, T22. Can proceed while deployment/briefing approvals wait.
- **Owns / outputs:** `docs/operations/rerun.md`, maintenance/release checklist and actual rerun record, `docs/tasks/T26.md`.
- **Scope / next action:** from clean checkout plus recorded artifact retrieval, rerun a real pilot subset through data preparation, inference, linkage, evaluation fixture and release packaging. Exercise missing/corrupt unit handling in an isolated temporary fixture; preserve actual jobs. Define new-epoch/source-schema drift checks, update cadence, version migration, rollback, corrected findings and named future custodian.
- **Checks:** central pilot outputs reproduced/tolerances explained; resume processes missing units only; no undisclosed local state; cost/storage/retention and last confirmed backup recorded. Future epoch requires date/phenology/model-shift/reference checks, not blind scheduled inference. Unknown continuity after environment deletion stated honestly.
- **Bound / stop:** ≤4 CPU / 8 GiB, 4 hours, 10 GiB scratch, one accepted pilot subset; no scheduler/monitor unless separately justified and authorized.
- **Evidence:** exact fresh-run commands/result hashes, recovery checks, maintenance owner and handoff; unresolved operational risks restrict service claims.

## T27 — Decide the next interval or jurisdiction (deferred)

- **Role / prerequisites:** research lead; T20, T26; use T25 feedback when available, record if absent.
- **Owns / outputs:** dated expansion decision under `docs/decisions/`, proposed next bounded tasks, `docs/tasks/T27.md`.
- **Scope / next action:** compare maintaining the current product, adding an epoch, unincorporated DeKalb or another jurisdiction using acquisition feasibility, applicable records, reference effort, scientific value and maintenance cost. Reassess whether direct change models or auxiliary data address a measured limitation.
- **Checks:** evidence-based go/no-go and scope/resource/authority implications; no inherited city rules applied elsewhere; separate transfer evaluation proposed. No implementation or expansion automatically authorized by this planning item.
- **Bound / stop:** D, at most three options; defer if the core release is not credible. This optional decision is not required to call the first study delivered.
- **Evidence:** reviewed recommendation, alternatives/uncertainties and exact proposed next tasks.

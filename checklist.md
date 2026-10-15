# Canopy Tracker ATL — implementation plan and current state

Updated **2026-10-14, America/Los_Angeles**. Integration owner: **Codex research lead (this chat)**. Campaign branch: **`chore/autonomous-harness`**, planning base `817a84a`. This is the single state entry point. Follow [AGENTS.md](AGENTS.md); human actions live in [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md).

## Current objective and state

**Objective:** a reproducible, independently evaluated canopy-loss investigation with parcel/permit evidence, a public map or website, and an agency briefing. Output supports **inspection triage with uncertainty**, never a finding of violation.

**Recommended scope:** City of Atlanta first, including its parts in both counties; stratified pilot before citywide processing. Prefer 2023→2025 only after actual imagery checks; 2019→2023 is a fallback to investigate. Compare inexpensive methods before choosing U-Net. Measure endpoint-visible canopy loss, then many-to-many parcel overlap and coverage-aware three-way permit reconciliation. Public aggregates are the recommended initial presentation; publication granularity remains a decision.

**Assignment status:** P00 initial planning and review is **complete**. No substantial pipeline implementation has begun. The next campaign starts with T01–T04; later tasks become ready only after their input/authority gates. All future execution items are unclaimed. No native `/goal`, watcher or automatic restart has been installed or tested.

**What exists:** the working agreement/archive, [research direction](docs/research-direction.md), [bounded task contracts](docs/task-contracts.md), and [planning evidence](docs/research/2026-10-14-planning/findings.md). Live metadata checks and direct reading of the GT reports support the plan. **What does not exist:** an acquired geospatial dataset, validated reference labels, trained detector, measured accuracy, usable permit snapshot, operational pipeline, durable raster/model store or public release.

**Jobs / recovery:** no training, inference, collectors or background jobs running. Planning probes/report downloads finished. Full plan/evidence checkpoint **`f1863c7` was pushed and verified on the remote campaign branch**; this completion-state update follows it in branch history. Raw GT PDFs are disposable and recoverable by URL/hash. No large-artifact durability has been demonstrated; T04 owns that gate. Recover from the latest campaign branch, then reconcile actual branch/jobs/artifacts before claiming work.

**Human blockers:** none for the ready first wave; no active HA requests. Likely later needs are independent annotation, unavailable exports/storage access, publication/communications authorization and briefing delivery. Agents must prepare those packages first; see T05/T09/T18/T22/T23. No unpaid/paid capacity or external response is presumed.

## Evidence that changed the inherited plan

- **Georgia Tech already does ML, fine-resolution canopy mapping, public maps and some permit comparison.** Its one-acre criterion limits change inspection/qualification, not all pixel-level detection. Our proposed contribution is validated smaller-event analysis and a reproducible parcel/record evidence trail. [Direct report review](docs/research/2026-10-14-planning/findings.md#e2--georgia-tech-comparison-requested-by-the-owner).
- **Dates and access remain gates.** The recorded screening query returned 25 2023 NAIP items dated October 7–8 and no 2025 items. This is metadata for a rectangle, not a complete city acquisition. Accela and USDA landing probes failed here; no permit completeness claim is justified. [Probe evidence](docs/research/2026-10-14-planning/findings.md#e1--imagery-catalog-probe).
- **Independent references must precede credible findings.** No citywide pseudo-training through protected test areas; measure both epochs, change, parcel relations and record matching separately. Sample nonloss as well as detected events. GT's land-cover accuracy is not our change accuracy. [Validation decisions](docs/research-direction.md#validation-is-part-of-the-product).

## Gates, decisions and unresolved questions

| Gate | Acceptance boundary | Current state |
|---|---|---|
| G1 — study feasible | Readable suitable paired samples, jurisdiction/parcel/source contracts, recoverable artifacts and review (T06) | Pending T01–T04; imagery and record coverage unresolved |
| G2 — method selected | Controlled development comparison, reference feasibility, frozen method and independent review (T13) | No model selected; 0.1-acre floor and shared-model comparison are hypotheses |
| G3 — findings validated | Protected evaluation and independent numerical reproduction (T19–T20) | No metrics; operational targets proposed, to be fully specified before test in T07 |
| G4 — delivered and maintainable | Reviewed bundle, authorized publication, actual agency briefing and tested rerun (T22–T26) | No release, deployment or briefing yet |

D01: [initial direction and tradeoffs](docs/research-direction.md). Unresolved consequential decisions: usable recent interval; exact valid-area denominator; historical parcel availability; effective-dated permit coverage; reference-label workload; scientifically supportable MMU/registration limits; review yield and subgroup precision; durable storage; public detail and maintenance custodian. Their owners are explicit below. The archive's numeric targets, fixed architecture and readiness declarations are not accepted results. Scope/acceptance changes require a recorded rationale and review, never silent weakening after evaluation.

## Execution register

`ready` = claimable now; `queued` = prerequisites unaccepted; `conditional` = activate only by a recorded decision; `deferred` = outside the first delivery. During execution use `active`, `waiting_for_job`, `blocked`, `complete` and explicit `not selected` where appropriate. A successful investigation can produce a no-go decision; that does not pass its downstream gate.

Each ID links its scope, outputs, acceptance checks, write ownership, resource ceiling, stop conditions and next action. Common branch/evidence/recovery rules are in [task contracts](docs/task-contracts.md#rules-shared-by-every-item). Future items have **no completion evidence yet**; on acceptance add the actual `docs/tasks/TNN.md` link, checkpoint and checks to the Evidence column.

| ID | Execution item / accountable role | Prerequisites | Status / claimant | Evidence |
|---|---|---|---|---|
| P00 | Initial plan / integration owner | Current agreement + archive | complete — research lead | [Findings](docs/research/2026-10-14-planning/findings.md), [accepted review/checks](docs/research/2026-10-14-planning/review.md); `f1863c7` |
| [T01](docs/task-contracts.md#t01--verify-candidate-imagery-intervals) | Imagery access, dates and samples / imagery | P00 | ready — unclaimed | — |
| [T02](docs/task-contracts.md#t02--establish-geography-parcels-and-comparison-layers) | Boundary, parcels, GT layers / geography | P00 | ready — unclaimed | — |
| [T03](docs/task-contracts.md#t03--audit-permit-sources-and-temporal-meaning) | Permit feasibility and rules / records | P00 | ready — unclaimed | — |
| [T04](docs/task-contracts.md#t04--establish-a-minimal-reproducible-environment-and-durable-artifact-path) | Runtime and durable artifacts / runtime | P00 | ready — unclaimed | — |
| [T05](docs/task-contracts.md#t05--prepare-any-necessary-historical-records-request) | Concrete export/request package / records | T01, T02, T03 | queued — unclaimed | — |
| [T06](docs/task-contracts.md#t06--integrate-and-freeze-the-first-study-contract-g1) | Study contract, G1 / integration | T01–T04 + usable pair/storage | queued — unclaimed | — |
| [T07](docs/task-contracts.md#t07--preregister-reference-sampling-and-acceptance-design) | Evaluation preregistration / evaluation | T06 | queued — unclaimed | — |
| [T08](docs/task-contracts.md#t08--build-and-assess-paired-pilot-preparation) | Pilot data and registration / preparation | T04, T06, T07 | queued — unclaimed | — |
| [T09](docs/task-contracts.md#t09--prepare-development-reference-annotation) | Development annotation packet / reference | T07, T08 | queued — unclaimed | — |
| [T10](docs/task-contracts.md#t10--validate-development-labels-and-reference-feasibility) | Development reference QA / evaluation | T09 + human delivery | queued — unclaimed | — |
| [T11](docs/task-contracts.md#t11--compare-inexpensive-change-baselines) | Baseline comparison / detection | T07, T08, T10 | queued — unclaimed | — |
| [T12](docs/task-contracts.md#t12--test-one-justified-learned-challenger-conditional) | One learned challenger / detection | T11 + activation decision | conditional — unclaimed | — |
| [T13](docs/task-contracts.md#t13--select-and-freeze-a-method-g2) | Method freeze, G2 / integration + reviewer | T07, T11, T12 disposition | queued — unclaimed | — |
| [T14](docs/task-contracts.md#t14--implement-auditable-parcel-attribution) | Parcel attribution / geography | T06 to start; accepted T11/T12 real events to finish | queued — unclaimed | — |
| [T15](docs/task-contracts.md#t15--build-a-versioned-permit-snapshot-and-coverage-ledger) | Permit snapshot / records | T03, T06; T05 delivery if needed | queued — unclaimed | — |
| [T16](docs/task-contracts.md#t16--implement-and-audit-three-way-reconciliation) | Three-way matching / linkage | T14, T15 | queued — unclaimed | — |
| [T17](docs/task-contracts.md#t17--run-the-frozen-detector-on-the-accepted-region) | Frozen regional processing / pipeline | T04, T08, G2; fixed batch manifest | queued — unclaimed | — |
| [T17L](docs/task-contracts.md#t17l--apply-regional-parcel-and-permit-linkage) | Regional linkage and release freeze / pipeline | T17, T14, T15, T16 or explicit source limitations | queued — unclaimed | — |
| [T18](docs/task-contracts.md#t18--collect-and-seal-protected-reference-observations) | Protected reference / custodian | final T07/T13, T17L to start; human delivery to finish | queued — unclaimed | — |
| [T19](docs/task-contracts.md#t19--evaluate-the-integrated-frozen-system-once-g3-analysis) | Final evaluation / evaluation | T17L, T18, final T07/T13 | queued — unclaimed | — |
| [T20](docs/task-contracts.md#t20--independently-reproduce-and-challenge-findings-g3-review) | Independent reproduction, G3 / reviewer | T19 | queued — unclaimed | — |
| [T21](docs/task-contracts.md#t21--build-a-local-map-and-evidence-card-prototype) | Local map prototype / presentation | T06 | queued — unclaimed | — |
| [T22](docs/task-contracts.md#t22--assemble-the-reviewable-public-release-bundle) | Exact release bundle / release | T20, T21; claims constrained by G3 | queued — unclaimed | — |
| [T23](docs/task-contracts.md#t23--prepare-research-report-and-agency-briefing) | Report and briefing package / communication | T20; T22 visuals when available | queued — unclaimed | — |
| [T24](docs/task-contracts.md#t24--publish-the-approved-website) | Authorized deployment / deployment | T22 + publication/handling approval | queued — unclaimed | — |
| [T25](docs/task-contracts.md#t25--deliver-the-agency-briefing-and-record-feedback) | Actual agency briefing / owner + agent | T23 + communication/delivery authorization | queued — unclaimed | — |
| [T26](docs/task-contracts.md#t26--demonstrate-rerun-and-establish-maintenance-handoff) | Reproduction and maintenance / maintenance | T20, T22 | queued — unclaimed | — |
| [T27](docs/task-contracts.md#t27--decide-the-next-interval-or-jurisdiction-deferred) | Next epoch/jurisdiction decision / research lead | T20, T26; use T25 feedback if available | deferred — unclaimed | — |

## Parallel ownership and integration

Initial independent lanes: **T01 / T02 / T03 / T04**. Their combined ceilings are 6 CPU cores, 12 GiB RAM, 10.5 GiB scratch and 7.25 GiB transfer; these are caps, not assumed provisioned capacity. The integration owner checks actual availability and reduces concurrency if necessary. No simultaneous GPU jobs. All future resource additions require demonstrated need and existing authority or a prepared HA.

After G1: T07 reference design, T14 parcel logic, T15 records and T21 local presentation can proceed independently. Detection follows the reference/preparation chain; reconciliation follows source/parcel evidence. T23 and T26 can progress while publication/briefing approvals wait. Missing tree records do not block loss detection but prevent unsupported permit conclusions.

The integration owner alone edits this state file, allocates HA IDs, and integrates cross-cutting schemas/root configuration. Task agents reserve the paths in their contracts; overlapping work uses isolated branches/checkouts. Each handoff supplies output paths/hashes, checks, residual issues, costs, running-job identity and exact next action. Integrate schema/fixture checks before marking consumers ready. Reviewer roles must be separate from the implementation under review.

## Exact first launch prompts

After P00 is accepted, claim the following independently, substituting a real owner and actual checkout in the run record. Use native `/goal` only if supported; otherwise these are ordinary bounded task prompts. They do not launch themselves.

```text
/goal Complete T01: verify usable Atlanta imagery intervals and paired samples.
Read AGENTS.md, checklist.md, HUMAN_ACTIONS.md and the T01 contract. Claim
T01 through the integration owner; use goal/t01-imagery from the accepted
campaign checkpoint. Follow its input/write/resource limits, preserve exact
source evidence, and stop at accepted feasibility evidence or a documented
recoverable blocker. Do not begin model training or full-city acquisition.
```

```text
/goal Complete T02: establish Atlanta jurisdiction, parcel provenance and GT
comparison-layer access. Read the working agreement/state and T02 contract;
claim T02 through the integration owner on goal/t02-geography. Produce the
bounded source/geometry evidence, checks and recoverable checkpoint. Do not
assume that county boundaries, mailing addresses or current parcels describe
historical city jurisdiction or ownership.
```

```text
/goal Complete T03: audit applicable Atlanta permit sources, coverage and
effective-dated meanings. Read the working agreement/state and T03 contract;
claim T03 through the integration owner on goal/t03-permits. Preserve tested
access/field evidence and exact limits; prepare blockers if necessary. No
external communications, broad scrape or implied authorization from a
building-permit row. Complete checks and publish a recoverable checkpoint.
```

```text
/goal Complete T04: prove a minimal reproducible geospatial environment and
authorized durable artifact round trip. Read the working agreement/state and
T04 contract; claim T04 through the integration owner on goal/t04-runtime.
Use the real small fixture and exact resource bounds. If storage is absent,
prepare the smallest concrete action and keep durability blocked. Do not
provision paid services or an autonomous scheduler. Preserve checks/checkpoint.
```

## Completion and next resume

P00 checks **passed**: archive preserved; primary GT reports examined; bounded catalog observations recorded; independent evidence and final plan reviews accepted; 51 local links/anchors and 28 task contracts checked; dependency graph acyclic; script syntax, quantitative arithmetic and diff checked; full plan/evidence checkpoint pushed and remotely verified. [Detailed check/review record](docs/research/2026-10-14-planning/review.md).

At the next execution start: inspect remote branch and working tree, read this file/HA queue, reconcile claims/jobs/artifacts, claim one ready ID, and follow its contract. Do not start all tasks merely because the list exists. Initial planning completion does not complete the research project.

The first full campaign is complete only when G1–G3 support the stated findings, reconciliation limitations are evaluated honestly, T22's bundle is reviewed, T24's public result is live under authorization, T25's agency briefing is delivered, and T26's reproducible handoff passes. Any missing component remains visible; T27 is optional future direction.

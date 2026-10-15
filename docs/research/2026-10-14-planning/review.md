# Initial planning review and checks

Date: 2026-10-14 (America/Los_Angeles). Branch: `chore/autonomous-harness`; base `817a84a`. State is maintained in [checklist.md](../../../checklist.md).

## Independent evidence review — complete

Reviewer: separate Sol agent `scientific_review`, read-only, distinct from the drafting/integration owner. Questions: which inherited scientific assumptions are unsupported; what validation makes parcel-scale loss defensible; do the raw catalog/GT observations support the new direction?

Reviewer read all archive/current agreements, checked primary literature, then independently read the downloaded 2023/2018 Georgia Tech reports and recomputed the stored STAC summaries. It reproduced 25/18/25/0 returned items for 2019/2021/2023/2025; dates and GSD in the findings note match the saved JSON. It reproduced GT's reported overall accuracy arithmetic: 239/250 = 95.6% (2023), 233/250 = 93.2% (2018). It did not rerun GT's classifier, inspect NAIP pixels, or independently establish GT's confidence intervals.

Incorporated review findings:

- GT's threshold concerns inspected change cells, not the existence of smaller changes in its raster. GT already compares permits. Its net decline is not our gross-loss benchmark.
- GT's 45.7% cover and 45.5% within 2008 boundaries refer to different geographic denominators; the archive's blanket dismissal of 45.5% should not be repeated.
- October 2023 dates belong to returned NAIP items; September 24 is GT's WorldView-2 date. Late November 2021 imagery raises a testable phenology concern.
- Weak height labels and citywide pseudo-training cannot establish independent held-out accuracy. Upstream model overlap, paired dates and spatial buffers must be disclosed.
- Compare methods on loss performance/cost; registration and physical-area MMU are measured choices. Preserve narrow/fragmented real losses and unknown causes.
- Sample nonloss, weight probability estimates, account for clustering, adjudicate labels independently, and separate image/parcel/permit uncertainties.

## Independent plan review — accepted after corrections

The same separate reviewer examined the concrete checklist, task contracts and direction, with raw evidence available. It raised two material gaps and four implementation-contract issues. All were corrected and rechecked:

| Finding | Resolution |
|---|---|
| No task applied parcel/permit logic to regional outputs | T17L now owns bounded regional linkage, area/event accounting and the frozen joined artifact consumed by T18/T19 |
| Purposive geographic holdouts cannot estimate whole-city totals | Separate holdout-domain generalization from an optional full-domain frozen-map probability survey; mark development overlap and limit unsupported estimates |
| T14 had an implicit real-event dependency | Fixtures are a checkpoint; accepted T11/T12 pilot events are required before completion |
| Early protocol lacked a final version/capacity boundary | T13 accepts the final reviewed T07 version, targets, allocation, nonresponse rules and actual reference capacity before protected selection |
| First permit/reference batches could be mistaken for full completion | T15/T18 parent acceptance explicitly reconciles all fixed manifest units and required allocations |
| “Gross loss” could imply all removals between images | Define endpoint-visible cover loss, including the blind spot for removal followed by regrowth |

The reviewer also corrected the G3 task range and expansion-task reference. Follow-up review found **no remaining material scientific or dependency objection to accepting the initial plan**. Actual sample calculations, human reference capacity, readable assets, recovery and operational targets remain execution gates, not proven results. Independent agreement does not substitute for later empirical validation.

## Repository and evidence checks

- Full archive read and untouched relative to the campaign base.
- STAC probes finished; script and metadata summaries preserved. Failed HTTP probes recorded, not interpreted as missing data.
- GT PDFs downloaded/read and hashes recorded; raw PDFs not staged.
- Local Markdown paths/anchors: 51 checked successfully; all 28 execution contracts appear once in the register and contain the six required contract fields.
- Task dependency graph: reviewed independently; automated traversal of all 28 completion dependencies found no cycle, including the conditional-model disposition and T14's real-event dependency.
- Document diff and script syntax checked; source probe counts/date ranges and GT arithmetic reproduced. No production artifacts or raw PDFs staged; only public unsigned metadata is retained.
- Remote branch reconciled at `817a84a` before committing. Full plan/evidence committed as `f1863c77409c1b5a85f708cb66f397fd8fc1b004`, pushed to `chore/autonomous-harness`, and verified with `git ls-remote`. The completion-state update follows that checkpoint; retrieve the latest campaign branch on resume.

No production code/model accuracy tests are claimed. Checks are appropriate to a planning deliverable and its bounded metadata evidence script. No live data source is rerun merely to produce a green check.

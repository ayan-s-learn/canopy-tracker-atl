# Initial planning review and checks

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

# Project glossary

Plain-language meanings of terms used in the active project documents. Start with the [README](../README.md) for navigation and [checklist](../checklist.md) for current progress. These definitions explain the plan; they do not claim that the planned system already works. Define new specialist terms on first use or add them here.

## People, work and records

| Term | Meaning here |
|---|---|
| Owner | The person directing the project. A **task owner** or **workstream owner** is the agent responsible for that work, not the person who owns a parcel. |
| Agent; Sol; Astra | An AI assistant working on a task. Sol and Astra name model families. Astra leads the project reviews; a model name alone does not make its findings correct or independent. |
| Workstream | A related area of work, such as imagery, permits or evaluation. Several can proceed at once. |
| Integrator / integration owner | The agent coordinating shared files, interfaces, resource conflicts and merging reviewed results. It does not approve every local method choice. |
| Astra project review | A milestone-based discussion of evidence and next steps. It records decisions and defines the next useful round of work and review trigger. |
| Ready brief; roadmap sketch | A ready brief describes an executable task and its checks. A roadmap sketch describes possible later work whose details can change. |
| Bounded run; `/goal` | Work with a stated objective, finite resource limits and a stopping condition. `/goal` is an optional runtime command for such work; a document does not itself start or schedule it. |
| Acceptance check; gate; promotion | A check establishes whether an output meets its requirements. A gate is a group of evidence requirements for a larger claim. Promotion means accepting an output for a specified use; passing a review alone does not establish accuracy. |
| Dependency; blocker | A dependency is an input needed for some work. A blocker is a missing input, capability or decision that currently prevents that work; it need not stop other work. |
| Claim / write reservation | A visible assignment of work and files to an agent, preventing duplicate effort or conflicting edits. It is not a scientific claim. |
| Artifact; evidence packet | An artifact is a saved output, such as a dataset, report or model. A review packet links the relevant artifacts, checks, limitations and decisions needed. |
| Pipeline; evidence card | A repeatable sequence from inputs to results; and a short explanation of one candidate loss event, with images, dates, uncertainty and record-search results. |
| Interface / schema | The agreed format and meaning of information exchanged between tasks: for example, fields describing a detected loss event. |
| Branch; commit; merge | A branch keeps a line of Git work separate. A commit is a saved, identified revision. A merge combines changes. The campaign branch holds current project work; `main` remains the reviewed baseline. |
| Checkpoint; handoff | An execution checkpoint saves enough state to resume work. A handoff explains that state to the next agent. Neither means an Astra project review or successful completion. |
| `blocked`; `waiting_for_job`; `superseded` | Respectively: work cannot proceed; an ongoing job is still needed; a named replacement carries the remaining work. None means `complete`. |

## Reading the IDs

| Prefix | What it identifies |
|---|---|
| T01–T27, T17L | Stable task references in the [briefs and roadmap](task-contracts.md). Leading zeroes are formatting; T1 means T01. Numbers preserve references, not a mandatory execution order. T17L is the separate regional linkage task. |
| AR01, AR02, … | Astra project reviews in the [review record](project-reviews.md). AR01 is planned, not already held. |
| G1–G4 | Evidence gates: study feasibility, evaluation-candidate selection, validated findings, and delivery/maintenance. See the checklist for exact requirements. |
| P00, P01 | Completed planning milestones: initial research/plan and the decentralization revision. They are not research accuracy results. |
| D01, D02 | Decision records: [scientific direction](research-direction.md) and [decentralized planning](decisions/decentralized-planning.md). |
| HA-0001, … | Human-action requests tracked in [HUMAN_ACTIONS.md](../HUMAN_ACTIONS.md). |

## Imagery, land and records

| Term | Meaning here |
|---|---|
| Canopy / crown | The overhead cover of tree foliage and branches. A mapped crown does not locate its trunk or establish who owns the tree. |
| Epoch; observation interval | An image observation period and the time between two observations. Actual local acquisition dates matter more than a dataset's nominal year. |
| Endpoint-visible gross loss | Canopy visible in the first image and absent in the second, without subtracting gains elsewhere. Removal followed by regrowth between images may be invisible. |
| Parcel; attribution | A mapped land unit, and associating an event with the parcels it overlaps. One event can overlap several parcels, and one parcel can contain several events (**many-to-many**). |
| Permit reconciliation | Comparing detected events with relevant administrative records, dates and coverage. `Matched` means a compatible record was found; `ambiguous` means the evidence cannot resolve it; `unmatched` means no compatible record was found in an adequately covered, documented search. Insufficient coverage stays `ambiguous`. None is a legal ruling. |
| Inspection triage | Prioritizing candidates for human review, with evidence and uncertainty. It is not an accusation, fine or proof of unlawful removal. |
| Coverage; valid-area denominator | Where and when the inputs support analysis, and the explicitly defined area against which results are reported. Unusable or missing areas must be accounted for. |
| Raster; vector; tile / chip | A raster is a grid of pixels. Vector data represents points, lines or areas. Tiles/chips are pieces of an image used for processing. |
| Band; NIR; resolution | A band measures a range of light; NIR is near-infrared. Spatial resolution describes ground detail represented by pixels, not guaranteed positional accuracy. |
| CRS; EPSG; grid | A coordinate reference system locates map positions; EPSG numbers identify standard systems. A grid specifies pixel positions and spacing. Area calculations require suitable units and projection. |
| Registration; phenology; seamline | Alignment between images; seasonal changes such as leaf loss; and a boundary where source images are joined. Each can create apparent change unrelated to removal. |
| Mask; nodata; QC | A mask identifies included/excluded pixels; nodata marks missing observations. QC means quality control. Missing data does not mean no canopy loss. |
| Provenance; lineage; vintage | Where data came from, how it was transformed, and the date or period it represents. |
| GT; NAIP; STAC | Georgia Tech; the National Agriculture Imagery Program; and SpatioTemporal Asset Catalog, a format/API for finding geospatial assets. Finding a catalog entry is not acquiring usable pixels. |
| DDH; NPU; DBH | Dead, dying or hazardous tree records (verify the source's exact category); Atlanta Neighborhood Planning Unit; and trunk diameter at breast height. Optical canopy imagery does not directly measure DBH. |

## Methods and validation

| Term | Meaning here |
|---|---|
| Baseline; challenger; pretrained model | A practical comparison method; an alternative tested against it; and a model trained previously on other data. Prior training does not guarantee suitability here. |
| Random forest; U-Net | A model combining many decision trees; and a neural-network architecture commonly used to label image pixels. Both are candidates, not commitments. |
| Reference labels; annotation; adjudication | Independently interpreted examples used to assess predictions; the act of labeling them; and resolving disagreements. Reference observations can also be uncertain. |
| Pseudo-labels | Labels generated by a model. They can help development but are not independent validation of that model. |
| Development; protected evaluation; leakage | Data used to choose or tune methods; data reserved for evaluation; and information from evaluation influencing development, making reported performance misleading. |
| Holdout; generalization; domain shift | Reserved evaluation data; performance beyond development examples; and changes in imagery or conditions that can reduce that performance. A local holdout does not automatically support citywide totals. |
| Preregistration; freeze | Recording the evaluation plan before seeing protected results; and pinning the exact method/data versions being evaluated. Later hypotheses remain possible but need valid evaluation evidence. |
| Estimand; sampling frame | The exact quantity being estimated, such as loss area in a defined region; and the set of units from which a sample is selected. |
| Inclusion probability; strata; cluster | A unit's chance of selection; groups sampled or reported separately; and related units that must not be treated as independent observations. |
| Nonresponse; blinding | Missing reference observations; and hiding model/permit results from interpreters where appropriate to reduce bias. |
| Precision; recall; yield | The fraction of flagged events that are real; the fraction of real events detected; and how many useful candidates are produced. An empty queue cannot demonstrate useful accuracy. |
| Confidence interval / bound | A range or one-sided limit expressing statistical uncertainty under a stated sampling method and assumptions. It does not cover every possible source of error. |
| MMU | Minimum mapping unit: the smallest event area included in a stated analysis. The proposed threshold must be validated, not assumed accurate. |
| Reproduction; rerun | Independently checking a finding from its evidence; and executing the pipeline again with recorded inputs and configuration. Code running successfully is not proof of scientific validity. |
| Manifest; hash; durable storage | An inventory of expected files/work units; a content fingerprint used to check identity/integrity; and storage with verified retrieval and survival properties. A hash alone does not make a file recoverable. |

## Execution terms

| Term | Meaning here |
|---|---|
| CLI; API | A command-line interface used through typed commands; and an application programming interface used by software to request data or actions. |
| CPU; GPU; inference | General-purpose and specialized parallel processors; and running a trained model to produce predictions. Using a GPU is not a project requirement. |
| Configuration; environment lock | Recorded settings for a run; and pinned software versions needed to reproduce it. |
| Model weights; optimizer state | Learned model parameters; and training information needed to continue learning. Saving weights alone may not reproduce a training restart. |
| Retry / backoff; transactional write | Trying a failed operation again with a delay; and finalizing output so partial writes are not mistaken for completed data. Both need explicit implementation. |

The [research direction](research-direction.md) gives the measurement and validation details; the [operations guide](operations.md) gives execution and recovery procedures.

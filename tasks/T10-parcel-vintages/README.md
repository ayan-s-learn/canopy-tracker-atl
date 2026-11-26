# T10 — What parcel geometry can support the pilot at each image date?

## Brief

Use the [T02 parcel source matrix](../T02-geography/README.md#parcel-source-matrix), [T05 window extents and dates](../T05-paired-coverage/development-windows.geojson) and [T07 membership evidence](../T07-historical-geography/README.md) at `2ac905e`. Determine what historical attribution is supportable in each county portion before joining a detection to a parcel. Reserve this folder and ignored cache `data/t10/`. Work with public metadata and bounded geometry queries inside the four development windows. Start with the county archives and crosswalks. Do not query owner or address fields or inspect new imagery.

- For each county and epoch, distinguish a discoverable source, a retrieved dated polygon, and an ID crosswalk with dated predecessor/successor evidence. Record source/version, coverage, effective date or range, terms, CRS and replay path. Record where only contemporary geometry is available.
- Exercise a many-to-many overlay on a labeled synthetic loss polygon within the pilot. Use each available vintage and a contemporary comparison for the same footprint. In equal-area units reconcile the event union, covered area and unassigned pieces within a justified tolerance. Preserve ambiguous overlap, duplicate condo geometries, and ID changes where encountered. Test a split or merge on a labeled fixture if the samples contain no documented example. Keep fixture results separate from observed parcel changes.
- Return a county-by-epoch decision on which links can be dated, which can only be explored using present-day overlap, and which remain unresolved. Quantify differences where comparable shapes exist. An unsuccessful archive search ends with sources checked and the exact evidence still needed. Prepare any necessary access request for the integrator. Bound any further inquiry to the gap it would resolve.

Keep reusable checks and compact, rights-compatible evidence in this folder. Exclude identifying records and raw county extracts from Git. This task can finish independently of the detector and HA-0002.

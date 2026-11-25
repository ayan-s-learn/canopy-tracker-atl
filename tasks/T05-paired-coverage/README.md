# T05 — Where does Atlanta have a usable image pair?

## Brief

Use the [T01 dated imagery sources](../T01-imagery/README.md) and [T02 City and county snapshots](../T02-geography/README.md) at `8ac1ac9` to assess the 2023 and 2025 NAIP pair. The discovery denominator is the full 2026 City snapshot. A window can establish local readability. Tile footprints can establish only potential coverage.

- Inventory the dated assets intersecting the City. Preserve source IDs, acquisition dates or unresolved ranges, footprints, overlap selection, seamline information where available, and retrieval provenance. Produce a replayable area table and mask for both epochs together, either epoch alone, neither, and unresolved coverage. Reconcile areas to the City total within a stated tolerance, with Fulton, DeKalb and county-unassigned subtotals.
- Start with metadata and the existing Fulton windows. Before reading new pixels, push the full proposed read footprints in a versioned geometry file, then fetch the current main and task branches. Check against any published candidate or frozen holdout and its buffer, including after reference design is complete. Move conflicting windows before reading. If reference design has an active owner, agree on the reservation revision together. If no split or claim exists yet, the published windows become development exclusions. Repeat for any expanded read footprint. Attempt a dated pair in DeKalb and target any other development windows to a specific uncertainty such as a seam or a different flight date. Report bands, masks, phenology, shadow and residual alignment on stable features in ground units. Keep sample measurements local and mark unsampled catalog coverage unverified for pixel quality.
- Deliver the ledger, geometry, checks and pilot recommendation here. For a viable pilot, identify the candidate development windows by asset, extent and date, and explain which acquisition and neighborhood conditions they represent or miss. Replay one newly retrieved pair from its unsigned source and check its grid and pixel hashes, or document the acquisition/recovery failure. Estimate space for the proposed pilot from its grids and bands. If scale requires durable storage beyond the [T04 demonstration](../T04-runtime/README.md), identify the missing capacity or access before bulk acquisition.
- Stop when both county portions and the residual area are accounted for and the pilot decision or limiting source gap is reproducible. A failed county probe stays visible. Reopen the 2019–2023 alternative only for a documented recent-pair gap that compromises the pilot. Use small window reads and ignored caches under `data/`. No county mosaics, model fitting or protected-image inspection in this task. Reserve only this task folder and its cache.

## Progress

Owner and session start: Codex T05, 2026-11-24 19:14 EST. Branch `task/T05-paired-coverage` from `83509aa`. Limits: use public metadata and small development reads within 128 MiB of source transfers and 500 MiB of task cache. Reserve only this folder and `data/imagery/t05/`.

The [development reservation](development-windows.geojson) covers the full Kirkwood and far west read extents plus a 1 m margin. It also includes the previously inspected T01 windows. The DeKalb window tests readability across the county line. The other new window tests the October 15, 2025 tile date outside T01's October 11 samples.

Next: fetch the published main and task refs, check reference exclusions, then request the reserved windows if clear.

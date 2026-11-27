# T09 — Prepare a blinded development calibration

## Brief

Turn the [T06 reference and staffing proposal](../T06-reference-design/README.md#staffing-and-decision) at `2ac905e` into an assignment the owner can hand to two interpreters and a third adjudicator. Package preparation can start from T01/T05 without detector predictions, a permit delivery or interpreter commitments. Reserve this folder and ignored cache `data/imagery/t09/`.

- Assemble the same 12 exercises for each interpreter, eight contained subwindows from the four existing [development reads](../T05-paired-coverage/development-windows.geojson) and four synthetic cases. Supply only previously read context. Cover the protocol's edge, shadow/unknown, stable and visible-change decisions in the synthetic cases. Use the [T06 scoring proposal](../T06-reference-design/README.md#image-reference-and-scoring-proposal). Give both readers the same nominal grid, scale, RGB and fixed near-infrared views for each date. Record the applied transforms and registration uncertainty per case. Pin dates, scoring extent and available context. A 120 m cell with 120 m on either side needs 360 m, wider than any real development window. Flag traces cut off by the crop. Disclose any unresolved displacement in the instructions without revealing an expected disposition. Keep answer keys, predictions, records and the other reader’s answers out of the reader packet.
- Supply a working image viewer or instructions for an accessible tool, unmarked image pairs, a blank return form and a private return path. Collect per-epoch crown and unknown geometry, visible loss, edge flags, confidence, reasons and active minutes. Distinguish a completed no-loss read from a skipped or unreadable case. Keep both original returns. Give the adjudicator a separate disagreement workflow with rationale, unresolved status and time.
- From a clean directory, rebuild or recover the packet using pinned inputs, open a pair and submit two isolated synthetic returns with equal-area, disjoint loss traces and a skipped or unreadable case, then score and adjudicate them. Compare per-epoch crown overlap (IoU), symmetric-difference areas for the loss and unknown masks, disposition, and minutes per reader and adjudicator. Define expected geometry scores and missing-value treatment for the synthetic returns, including empty masks. Check units and coordinates against those expectations. Provide hashes, distribution and resume instructions. Keep raw imagery and identifiable returns outside Git. Document prior exposure and conflicts for each role before assigning readers.
- The package is complete when the integrator can reproduce that dry run and the owner can distribute and receive it with the stated tools and access. Then propose a staffing action under **For integration** with the pinned package, skill requirements and the T06 budget of 2.5 hours per reader and 2 hours for adjudication. No recruitment or paid commitment is authorized.

After staffing and delivery, actual returns can inform labeling rules and workload for the supplied context. Prevalence, missed loss and queue yield require separate probability sampling.

## Progress

Owner: Codex, 2026-11-27 09:35 EST. Branch `task/T09-calibration-package` from AR02 `c41c8e7`.

Built the offline assignment from eight pinned T01/T05 rasters and four synthetic cases. Clean retrieval, packet rebuild and private dry run passed. Next, integrate the staffing action and obtain independent reads after owner assignment.

## Result

The packet contains 12 exercises with an offline viewer and blank JSON return. Eight crops use the four T01/T05 development reads, two per site. Four synthetic scenes exercise stable cover, visible change, shadow uncertainty and loss ending at the crop. Case IDs and order are fixed and identical for both readers. The distributed files omit scenario labels, locations, source tiles and geographic transforms. Keep the owner ledger and repository out of the assignment.

The 2023 pixels stay on their EPSG:26916 0.6 m source grid. Each corresponding 2×2 block of 2025 0.3 m pixels is averaged with rounding to the nearest byte, ties up. Both years use the original byte values after that resampling, displayed as RGB and NIR/red/green. No shift is applied. Tile dates are 2023-10-08 and 2025-10-11, except far west Atlanta uses 2025-10-15. The registration notes give parent-window T05 diagnostics where available, and describe unresolved displacement in each real case. These diagnostics leave local error unbounded.

Each 200×200-pixel scoring square is 120 m across. The surrounding viewed context is 13.2 m per side at Piedmont and West End, and 36 m at Kirkwood and far west Atlanta. The two scoring squares at each site overlap by 88.36% at the smaller sites and 0.16% at the larger ones. The build checks the complete parent reads against the four pinned reservations and every T06 context block plus its 600 m guard. Scoring uses the square, retains original traces across its boundary and flags possible crop truncation. No event-size cutoff applies. This targeted exercise tests agreement and workload.

### Dry run

The [expected and reproduced result](dry-run.json) uses hand-specified geometry to test scoring. Chrome 158 also opened the offline views, drew and resumed work in two isolated sessions, downloaded both returns, displayed the original overlays in the separate adjudicator view, and exported the third return. The CLI preserved the three originals in a local private vault. Real interpreters and an owner-to-reader transfer remain pending.

For C02 each loss trace is 100 px² (36 m²) with zero intersection. The raw symmetric difference is 72 m². The 2025 unknown traces differ by 36 m², of which 18 m² overlaps one loss trace, leaving 54 m² of loss disagreement on common-known support. The early crown intersection and union are 100 px² and 400 px², giving IoU 0.25. Both late crown masks are empty on nonzero common-known support, giving IoU 1. C06 yields a completed no-loss read (0 m²) and an unreadable read (null), with null pairwise scores. The archived return hashes survive adjudication unchanged.

## Outputs and replay

Use CPython 3.14, the [pinned raster dependencies](../../requirements.txt) and Shapely 2.2.0. Fresh retrieval uses curl and access to both imagery services. The four real-source ledgers are the T01 [read ledger](../T01-imagery/t01-windows.json), T05 [read ledger](../T05-paired-coverage/window-evidence.json), [reservations](../T05-paired-coverage/development-windows.geojson) and [registration diagnostics](../T05-paired-coverage/alignment.json) at `2ac905e9472f9b900055c87380876be36571ee6b`. The T06 [split](../T06-reference-design/split.geojson) is pinned at the same revision. With a local virtual environment active, build in a private directory outside Git. Run these commands from the repository root.

```sh
python -m pip install -r requirements.txt shapely==2.2.0
umask 077
run=$(mktemp -d)
task=tasks/T09-calibration-package
python tasks/T01-imagery/recover_windows.py "$run/t01"
python tasks/T05-paired-coverage/check_windows.py "$run/t05" "$run/t01" --retrieve > /dev/null
python "$task/build_packet.py" "$run/packet" "$run/t01" "$run/t05"
python "$task/test_t09.py" "$run/packet" "$run/dry" > "$run/dry-run.json"
cmp "$run/dry-run.json" "$task/dry-run.json"
python -m unittest discover -s "$task" -v
```

Recovery retrieved all eight TIFFs byte-for-byte on 2026-11-27. Rerun retrieval into the interrupted directory to reuse verified files, or point the builder to existing caches. The two build and dry-run output paths must be new. Preserve a private copy of the reader ZIP and its owner ledger for each distributed version in case service URLs change. The ledger records the pixel and mask inputs and the SHA-256 of each distributed file.

Geometry uses polygon vertices at integer crop pixel boundaries from the top left, with x increasing rightward and y downward. The owner ledger gives a pixel-to-EPSG:26916 affine for real cases. The scorer unions rings within each layer and clips to the scoring square. It converts area using 0.36 m² per pixel². Per-date crown IoU excludes either reader's unknown for that date. Loss disagreement is reported both raw and after excluding either reader’s per-date and change-only unknown areas. The unknown differences retain the full scoring square. Completed empty masks give zero area. A completed case with zero visible loss has a separate disposition if unknown area remains. Two empty crowns yield IoU 1 when they share some known area. With zero common-known area, the corresponding IoU or common-known loss comparison is null. A skipped or unreadable return has null geometry scores. Timing totals include recorded zeroes and count missing entries separately.

### Distribution and return

1. Before assigning access, record the names and contact details privately with a role code, relevant imagery or canopy qualifications, any prior exposure to the exact imagery or known sites, and any prediction, permit, key, or other-reader exposure and conflicts. Use R01 and R02 for people who can independently trace crowns in RGB/NIR and distinguish image artifacts from change. Use A01 for a third qualified interpreter experienced in resolving imagery disagreements. Replace anyone whose prior exposure or conflicts compromise their assigned role before distribution.
2. Zip only the contents of `packet/reader/` and give the identical archive to each reader separately. Supply their role code and your direct return instructions outside the ZIP. Each reader unzips privately, opens `viewer.html` in Chrome, follows the [reader guide](reader-guide.txt) and downloads their JSON. They can resume by reopening a private draft in the same packet version. Accept the file one-to-one through the owner's existing private transfer or by direct handoff into separate owner-only folders. Confirm which route with each recipient before assignment. Keep the ZIP, owner ledger, draft files, returns and reports outside Git and shared links.
3. Keep each delivered JSON unchanged. In the replay shell, substitute the actual paths, using a vault directory accessible only to the owner. Confirm each sender through the private handoff. The commands check the assigned code, case records and geometry before archiving each original. A duplicate slot fails without replacing the first file. If a return needs correction after acceptance, retain that version privately, use a new vault for the corrected pair and regenerate adjudication against those hashes.

```sh
python "$task/score_returns.py" receive "$run/packet" "$run/vault" R01 /private/path/reader-one.json
python "$task/score_returns.py" receive "$run/packet" "$run/vault" R02 /private/path/reader-two.json
python "$task/score_returns.py" compare "$run/packet" "$run/vault" "$run/scored"
```

4. Give only A01 the contents of `scored/adjudicator/` privately. The packet includes the full traces for cases flagged by any difference in full-crop geometry or disposition, incomplete reads, low confidence or possible crop truncation. Even an off-core disagreement can call for adjudication, so A01 may see all 12 cases. Keep the comparison private. A01 records independent geometry where scorable and a rationale, resolved/unresolved status and minutes for every flagged case. Receive that JSON privately, then verify the originals and save the adjudication log separately.

```sh
python "$task/score_returns.py" receive "$run/scored" "$run/vault" A01 /private/path/adjudicator.json
python "$task/score_returns.py" finish "$run/scored" "$run/vault"
```

If no cases need adjudication, run `finish` without an A01 return. Recover an interrupted comparison by choosing a new output directory and using the same immutable vault. Keep both original returns, their comparison and the adjudication log available for the development protocol decision.

## For integration

Register a seven-person-hour staffing action for the reader packet pinned by [dry-run.json](dry-run.json). Ask the owner to assign two independent image interpreters (2.5 hours each) and a third adjudicator (2 hours), using the canopy, RGB/NIR and conflict criteria above. The coordinator can reproduce the packet and dry run before any handoff, establish the private route, and verify the two originals plus adjudication log on delivery. This unlocks a decision on the interpretation instructions and actual task time. Staffing hours remain uncommitted.

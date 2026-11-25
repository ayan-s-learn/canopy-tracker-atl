# T07 — Which areas belonged to Atlanta on the image dates?

## Brief

Start with the [dated City boundary, county overlay and annexation records](../T02-geography/README.md#municipal-footprint) and [T01 local observation dates](../T01-imagery/README.md) at `8ac1ac9`. Determine where historical municipal membership can be supported for the 2023–2025 pilot. Use the two observed dates to exercise the procedure while the imagery inventory establishes dates elsewhere.

- Check for dated official boundaries and boundary changes in both directions through the 2026 snapshot. For the seven archived annexation entries, reconcile effective dates, geometry and available ordinance evidence. Record gaps in the change history and any limits on reconstructing earlier limits from the current footprint.
- Produce a versioned boundary or uncertainty layer and an effective-date ledger. Distinguish areas inside at both dates, inside only at the first, inside only at the second, outside at both, and unresolved. Show how a local acquisition date range that straddles a change affects membership. Identify any historical areas outside the discovery footprint separately.
- Replay area accounting against the T02 discovery footprint, by county and county-unassigned area, within a stated tolerance. Exercise the dated lookup on the September and December 2025 changes around the October sample dates. Distinguish a missing geometry or unverified effective date from a measured zero-area change.
- Stop with the reproducible membership evidence available from public sources, and quantify unresolved area within the discovery footprint. Where missing historical geometry leaves the extent outside that footprint unknown, identify the missing evidence and report the extent as unknown. Reserve this task folder and its ignored cache. Historical parcel splits and permit coverage require separate evidence. No parcel-owner data, records requests or new imagery reads are needed.

## Progress

- Owner: Codex, 2026-11-25 14:02 ET. Branch: `task/T07-historical-geography`.
- Scope: public boundary and legislative evidence, archived imagery dates, and local replay. No paid data or new imagery reads.
- Status: evidence package prepared for integration review. The remaining historical coverage gaps are recorded below.

## Result

For the October 8, 2023 and October 11, 2025 tile dates, both T01 windows fall entirely in the `inside_both` area. Use this layer as historical membership evidence for pilot development and replay it with each site's local acquisition dates. The common City/Census area provides continuity evidence. The available records leave the completeness of the change history and the legal status of unverified boundaries open. [T01 sample dates](../T01-imagery/README.md) · [TIGER/Line source limits](https://www.alpha.cms.adsd.census.gov/programs-surveys/geography/technical-documentation/user-note/tiger-geo-line.html)

| Membership within the T02 discovery footprint | Fulton m² | DeKalb m² | County-unassigned m² | Total m² |
|---|---:|---:|---:|---:|
| Inside at both dates | 329,587,362 | 22,795,102 | 0 | 352,382,464 |
| Inside at the first date only | 0 | 0 | 0 | 0 |
| Inside at the second date only | 0 | 124,497 | 0 | 124,497 |
| Outside at both dates | 20 | 175,553 | 0 | 175,573 |
| Unresolved in the mapped evidence | 330,312 | 350,658 | 9,340 | 690,311 |

All five classes reconcile to T02 in EPSG:5070 within **2 m²** before rounding. The unresolved mask covers 0.20% of the discovery footprint. Outside it, the evidence domain includes 7,283,523 m² of mapped candidates, all unresolved for these dates. Most of that comes from undated or unverified City deannexation polygons. The historical municipal extent outside the discovery footprint is unknown, as is the unlocated area affected by any missing polygon. The zero for `first_only` is the measured area assigned by this replay. [Area ledger](areas.json)

- The City feature layer had 211 records. The audit mapped 21 rows selected by recent year or effective date, null annexation year, or undated deannexation status. City objects 4 and 166 list January 1, 2025 with no ordinance. Both still overlap the municipal footprint in all four TIGER vintages and the 2026 City snapshot. No matching legal removal was established. The court invalidated five older Cascade-area annexations before the study period. Four other undated deannexation rows remain unresolved. [City query and extracts](sources.json) · [City of Atlanta v. Mays](https://caselaw.findlaw.com/court/ga-supreme-court/1863180.html)
- DCA reports effective dates for all seven T02 annexations. BAS also reports the first three. Wilkinson Drive enters on October 1, 2025 under 25-O-1375, after the September 24 GIS date and before the October 11 image. Gresham Avenue enters on January 1, 2026, after both the December 10 GIS date and the October image. The replay uses the non-tax dates reported in the filings. The state map returned the same four polygons for every filing ID, so the replay uses City geometry and preserves the recorded date and ordinance discrepancies. [Effective-date ledger](effective-dates.json) · [DCA reporting guidance](https://www.georgiaplanning.com/AnnexationReportForm.pdf)
- The City GIS query also returned Sargent and Woodland in 2026 despite their historical `YEARANNEXED` values. Council adopted a further annexation, 26-O-1348, in October 2026. Its effective date and matched geometry remain unverified. The four nominal January 1 TIGER vintages contain both additions and removals. Several documented annexations appear in TIGER years later, so differences between annual polygons alone remain unresolved. [Source and ordinance receipts](sources.json) · [Census BAS coverage notes](https://www.census.gov/geographies/reference-files/time-series/geo/bas/annex.html)

## Outputs and replay

[Membership GeoJSON](membership.geojson.gz) uses longitude/latitude and carries the two inclusive date windows. Its scope field identifies the T02 footprint or mapped candidates beyond it. [Area ledger](areas.json) records EPSG:5070 totals by class and county, source differences and per-change area. A missing polygon has null area. [Sources](sources.json) pins the Atlanta-only TIGER extracts, City GIS responses, state filings and Council documents. Federal TIGER data are public domain. The City GIS item has no explicit reuse license in T02. Use the frozen input versions to reproduce the results.

Run from the repository root with Python 3.14, Shapely 2.2.0 and PyProj 3.8.0.

```sh
python tasks/T07-historical-geography/membership.py /tmp/t07-default
python tasks/T07-historical-geography/membership.py /tmp/t07-straddle --second 2025-09-29 2025-10-12
python -m unittest discover -s tasks/T07-historical-geography -v
```

The straddle replay moves 1,308 m² of Wilkinson from `second_only` to `unresolved`. The same lookup gives Gresham `outside_both` through December 31, `second_only` at January 1, and `unresolved` for a range crossing that date. The Sol reviewer independently rebuilt the defaults from the archived geometry and verified the dated scenarios and exported partition.

## For integration

On acceptance, record T07 completion in the checklist and link the membership layer. Keep the missing geometry and unverified boundary changes open under G1. Replay the layer with local acquisition dates before freezing a pilot frame or attributing historical jurisdiction.

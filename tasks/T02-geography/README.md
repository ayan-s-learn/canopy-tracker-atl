# T02 — Atlanta geography, parcels and comparison data

## Brief

- **Objective:** identify the real study jurisdiction and what parcel and comparison data can support, starting from the [P00 source findings](../P00-planning/findings.md).
- **Expected outputs:** dated official boundary; parcel source, vintage and schema matrix with representative geometry; GT access and rights findings; suitable neighborhood context leads. Record unexamined or inaccessible sources explicitly.
- **Acceptance:** source IDs and terms, geometry validity, CRS/units/area checks, city versus county/mailing-address distinction, historical limitations, and comparison of the old screening rectangle with the actual boundary. A discovery report may document unavailable data; it cannot certify complete historical attribution.
- **Limits:** 60 public data requests, 64 MiB of source transfers, 100 MiB of temporary wheel transfers and 500 MiB of scratch space. Stop once the boundary and representative geometry are usable and the remaining history and rights gaps are identified.

## Result

Codex observed these sources on 2026-11-23 (America/New_York); the [manifest](t02-sources.json) records retrieval times for fetched responses.

### Municipal footprint

Use the [dated City boundary](atlanta-city-limits-2026-11-23.geojson) for imagery coverage discovery and current City clipping. Atlanta Department of City Planning GIS returned one valid multipolygon with two parts. The native layer uses EPSG:6447 (US survey feet). The archived query returned GeoJSON in WGS84 longitude/latitude. The feature was last edited November 2, 2026, and its legal effective date is blank. The City's public open-data item gives no explicit reuse license. [City layer](https://gis.atlantaga.gov/dpcd/rest/services/OpenDataService1/FeatureServer/1) · [Open-data item](https://www.arcgis.com/home/item.html?id=3718407151454be3ab11c15526430997)

| Check | Area |
|---|---:|
| City footprint | 353.373 km² |
| City intersecting Fulton County | 329.918 km² |
| City intersecting DeKalb County | 23.446 km² |
| City outside both county polygons | 0.00934 km² |
| Old rectangle outside the City | 295.188 km² (45.51% of the rectangle) |

The old P00 rectangle contains the full snapshot in WGS84. Use the City geometry as the footprint and the Census county overlays as routing aids. Atlanta’s overlap with both county polygons is below the 2 m² check tolerance. About 9,340 m² remains outside the county union in this cross-source overlay. Keep that area in the City mask and leave its county assignment unresolved pending boundary reconciliation. Measurements use the archived GeoJSON in EPSG:5070 (equal-area, metres). [2024 TIGERweb county layer](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2024/MapServer/82)

The City annexation query returned seven annexed records from 2023 onward, including September 24 and December 10, 2025. A current footprint alone cannot establish membership on either image date. Before making historical jurisdiction claims, review the effective-dated annexation geometries and ordinances, including areas added between the two observations and areas added after the 2025 imagery. Keep those differences visible in the study footprint. [City annexations](https://gis.atlantaga.gov/dpcd/rest/services/OpenDataService1/FeatureServer/5)

### Parcel source matrix

| Source | Geometry and vintage observed | Fields for a pilot | Rights and history |
|---|---|---|---|
| [Fulton Tax Parcels, layer 0](https://gismaps.fultoncountyga.gov/arcgispub/rest/services/OpenData/Tax_Parcels/MapServer/0) | EPSG:2240, US survey feet. Both samples had `TaxYear=2027` in the live layer on November 23, 2026. Fulton says the digest dataset is provisional until midyear completion and can be corrected afterward. | `ParcelID`, `FeatureID`, `TaxYear`, `TaxDist`, `ClassCode`, `LandAcres`. | Public query. The [viewer disclaimer](https://gis.fultoncountyga.gov/Apps/propertymapviewer_EB/?dlg=Accessibility-Window) describes personal, as-is use. The [historical tax table](https://gismaps.fultoncountyga.gov/arcgispub/rest/services/Temp/GlobalSearch_Dialog/MapServer/2) has no geometry. 2023/2025 parcel polygons and an ID crosswalk remain unverified. |
| [DeKalb Tax Parcels, layer 0](https://dcgis.dekalbcountyga.gov/mapping/rest/services/TaxParcels/FeatureServer/0) | EPSG:3857, Web Mercator metres. Live snapshot with no tax-year or effective-date field in the tested schema. | `PARCELID`, `PRCLKEY`, `BUILDING`, `UNIT`, `CVTTXCD`, `CVTTXDSCRP`, `CLASSDSCRP`, `CITY`, `ACREAGE`. | Public query. [County mapping guidance](https://dekalbcountyga.gov/departments/gis/property-mapping-and-land-records) describes parcel maintenance. [Lot change procedures](https://dekalbcountyga.gov/departments/gis/lot-combinations-divisions-and-boundary-line-adjustments) document divisions, combinations and adjustments. Historical shapes and reuse terms remain unverified. |

Six point queries returned five valid polygons. The Fulton samples were a 673 m² West End parcel and a 439,742 m² polygon at Piedmont Park. The park polygon's mapped area is about 108.66 acres, while `LandAcres` is 179.4. DeKalb returned a 2,592 m² Kirkwood parcel, an East Lake polygon with about 60 m² beyond the City snapshot, and a polygon entirely outside the City snapshot with tax district `UNINCORPORATED` and site city `Atlanta`. The site city label is distinct from the source’s postal fields. Neither an address city nor a county tax district establishes legal municipal membership. Use spatial overlap for municipal assignment, preserve provider district codes as checks, and calculate physical area from geometry. Parcel IDs should carry source county and vintage. The manifest records query receipts and measurements without parcel identifiers, owner names or addresses.

A second Kirkwood point inside Atlanta returned zero DeKalb parcels and one hit in the [City/GT right-of-way proxy](https://services2.arcgis.com/I9cUOJUZvdGAJncI/arcgis/rest/services/Canopy_Data_2023_WFL1/FeatureServer/3). That proxy represents area outside parcels. Retain those pieces as unassigned and use dedicated public-land or right-of-way records to establish status. The DeKalb layer metadata says condo-unit records can repeat the same geometry. Keep possible unit links and count shared geometry once in area totals. The point samples did not test condo linkage.

The samples support a contemporary overlay pilot. For 2023/2025 attribution, look for archived county geometry and predecessor/successor IDs with effective dates, then quantify sensitivity to splits, mergers and gaps.

### Georgia Tech comparison and neighborhood context

- **2023 canopy pixels.** The Experience links to the public data hub. Its interactive map exposes the cached raster service, whose item links to a 26,384,341-byte ZIP. The download passed the archive read and Rasterio decoded a 256 × 256 Piedmont Park window. The GeoTIFF is a single UInt8 band in EPSG:26916 at about 1 m. The window contains 31,527 canopy pixels coded `1` and 34,009 pixels coded `0`, which the TIFF declares nodata. Comparing absence requires a verified coverage mask. The lineage names a 2024 City-limits clip, so the current City footprint cannot stand in for that mask. The ArcGIS item and ZIP give no explicit reuse license. Confirm training, redistribution and derivative-publication terms with Georgia Tech before those uses. [Data hub](https://city-of-atlanta-urban-tree-canopy-hub-gtmaps.hub.arcgis.com/search) · [Raster item](https://www.arcgis.com/home/item.html?id=33c5f759da6546b9ab7f28c1f7e5bdb7)
- **2018 and aggregated change.** Both epochs returned decodable rendered canopy tiles at the same map tile location. The 2018 service lists Digital Globe in its copyright field. The source class raster, coverage mask and rights to redistribute or publish derivatives remain unverified. The grid query returned a valid 5.74-acre cell with 2018/2023 canopy values. Treat the grid as aggregate comparison and the site visits as targeted examples. Neither establishes independent pixel truth or small gross-loss performance. The GT report used September 2023 WorldView-2 imagery for classification. The published 1 m product and the T01 October NAIP pair have different observation dates and pixel sizes. [GT web map](https://www.arcgis.com/home/item.html?id=4768688562b246f2a99312dab18ffce0) · [Grid layer](https://services2.arcgis.com/I9cUOJUZvdGAJncI/arcgis/rest/services/Canopy_Data_2023_WFL1/FeatureServer/7) · [Prior report findings](../P00-planning/findings.md#e2--georgia-tech-comparison)
- **Neighborhood context.** The [City NPU layer](https://gis.atlantaga.gov/dpcd/rest/services/OpenDataService1/FeatureServer/4) returned a count of 25. Use NPUs for reporting. For area income context, the 2020–2024 ACS table B19013 joined by GEOID to two sample 2024 TIGERweb block groups, one per county. The tested Fulton block group was $132,384 ± $16,769 and the DeKalb group was $101,319 ± $54,775 in 2024 dollars at 90% confidence. Preserve missing and flagged estimates and margins of error. If an interval crosses a reporting band, report uncertainty or run a sensitivity check. An ACS block-group median describes the block group and cannot identify parcel or household income. Use matching Census boundaries and avoid averaging medians across partial groups. [Census table](https://data.census.gov/table/ACSDT5Y2024.B19013) · [TIGERweb block groups](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2024/MapServer/10) · [ACS accuracy](https://www2.census.gov/programs-surveys/acs/tech_docs/accuracy/MultiyearACSAccuracyofData2024.pdf)

## Outputs and replay

The [manifest](t02-sources.json) records source IDs, bounded queries, hashes and results. The City boundary, Census county inputs and annexation response are archived alongside it. Parcel and Georgia Tech sample bytes remain external and may change when re-queried. The manifest pins the downloaded 2023 GT archive and window for replay.

Run the offline hash, geometry, date and area checks from the repository root. Tested on CPython 3.14.7 with GEOS 3.14.1 and PROJ 9.8.1. Rasterio 1.4.4 was used for the separate GT sample read.

```sh
run=$(mktemp -d)
python3.14 -m venv "$run/env"
"$run/env/bin/python" -m pip install 'shapely==2.2.0' 'pyproj==3.8.0'
"$run/env/bin/python" tasks/T02-geography/check_geography.py -v
```

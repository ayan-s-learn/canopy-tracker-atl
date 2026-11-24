# T01 — Atlanta imagery interval check

## Brief

- **Objective:** find a usable, accessible image pair for local canopy-loss research. Start from the [saved P00 NAIP catalog screen](../P00-planning/findings.md#e1--imagery-catalog-probe) and its unsigned tile URLs. Prefer 2023–2025, with 2019–2023 as fallback.
- **Acceptance:** read actual four-band windows from two dates and validate acquisition date/range, CRS/grid/resolution, nodata, rights and source identity; record them with window hashes in a compact ledger. Document leaf, shadow, alignment and seamline concerns and missing inputs before recommending an interval. Metadata alone cannot certify usable imagery.
- **Limits:** up to three development locations; twelve source/catalog lookups plus bounded tile/index/range requests; 1 GiB of imagery transfers and 2 GiB of temporary storage. No training, protected evaluation, citywide acquisition, spending or external messages. Stop at sufficient local evidence or document the failed routes and exact recovery action.

## Result

Samples were retrieved on 2026-11-22 (America/New_York); the [window manifest](t01-windows.json) records request times.

Use October 2023 to October 2025 for local development. Both services returned four distinct, nonconstant uint8 bands covering the same 153.6 m square at each site in NAD83 / UTM zone 16N (EPSG:26916). The 2023 samples are 256 × 256 at 0.6 m. The 2025 samples are 512 × 512 at 0.3 m. Each request specified source bands 0–3 in order. NAIP documents these as red, green, blue and near-infrared. The exports have undefined band labels, so band identities rely on the provider. [NAIP collection metadata](../P00-planning/source-probes.json). None of the four exports declared nodata or masked any pixels, and none contained a pixel with zeros in all four bands. Shadows and water still require interpretation.

| Development location (center, WGS84) | 2023 USGS tile and acquisition date | 2025 USDA tile and acquisition date |
|---|---|---|
| Piedmont Park, 33.787° N, 84.372° W | 3308414 SW · October 8 | 3308414 SW · October 11 |
| West End, 33.735° N, 84.423° W | 3308421 NE · October 8 | 3308421 NE · October 11 |

![Paired NAIP samples from Piedmont Park and West End](t01-windows.jpg)

At Piedmont Park, leafy crowns, a lakeshore and paths are visible in both years. Crown shadows obscure parts of the paths. In West End, the running track and adjacent street provide clearer fixed features. The 2025 images are sharper and have different colors. A shift in brightness or crown edge between dates could therefore be an imaging difference. Roads and paths line up by eye at this scale. Registration error remains unmeasured. The preview averages the 2025 RGB pixels to the display scale. Hashes use the original four-band exports.

Dates come from the tile acquisition fields, corroborated by the tile names. The timing of individual flight strips within each tile remains unverified. Use local flight dates and measure residual offsets on held-out stable ground features before interpreting small events. Both sample footprints fall entirely inside the [T02 City boundary and Fulton County overlay](../T02-geography/README.md). The DeKalb portion of Atlanta remains unsampled. Two selected locations establish sample access only. Citywide coverage, change accuracy and suitability for parcel attribution remain open. The recent pair was accessible, so the 2019 fallback was unnecessary.

An independent reviewer decoded the four original TIFFs, reproduced all file and band-major hashes, pixel ranges and mask counts, and checked the footprints and previews. The reviewer supported the local-development recommendation and identified registration, image sharpness, shadows and tile-date precision as limits.

On November 23, 2026, fresh service downloads reproduced all four original TIFFs byte for byte, including West End 2023 after the earlier HTTP 504/timeouts.

### Access and source selection

The saved planning catalog supplied the 2023 quarter-quad identifiers. A USGS index query at the park returned two overlapping 2023 tiles. We selected the quarter quad matching the 2025 tile by name. The second location uses a different quarter quad. Both locations were chosen for development before viewing their pixels. Record these footprints as inspected when defining protected geography.

The [USGS imagery index](https://index.nationalmap.gov/arcgis/rest/services/USGSNAIPImageryIndex/MapServer/0) describes the NAIP orthophotos as public domain. The [2023 USGS image service](https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer) and the [2025 USDA image service](https://apps.geo.fpac.usda.gov/geo-imagery/rest/services/naip/conus_naip/ImageServer) expose individual dated tiles. We used each tile's own image endpoint to avoid a changing default mosaic. The 2025 tile metadata explicitly permits reuse and requests credit. NAIP imagery provided by USDA Farm Service Agency.

USDA also lists [Fulton](https://nrcs.app.box.com/v/naip/file/2094469710915) and [DeKalb](https://nrcs.app.box.com/v/naip/file/2094524982359) county mosaic ZIPs of 6,393,392,971 and 1,909,801,988 bytes respectively, plus the [Georgia seamlines](https://nrcs.app.box.com/v/naip/file/2093473093347). We verified the directory entries only. The county downloads exceed the sample budget. Anonymous listing of the attempted USGS S3 bucket returned HTTP 403. An optional USGS item key-properties request returned HTTP 502. Neither failure prevented a pixel read.

## Outputs and replay

The four original service exports (2,628,338 bytes total) are preserved locally in `data/imagery/t01/` and excluded from Git. Each copy passed its whole-file hash check. The JPEG preview and JSON ledger are in this folder. The raw TIFFs have no durable copy; the retrieval below recovers them from the source services.

The [window manifest](t01-windows.json) records the original tile names, acquisition fields, service metadata, unsigned TIFF requests, native and output grids, observed nodata, band ranges and hashes. From the repository root, use curl and Python with Rasterio 1.4.4 and NumPy 2.3.5. Use a fresh directory for a full retrieval test. After an interrupted run, reuse the directory to reuse verified files, including a TIFF repackaged with the same grid, masks and pixels.

```sh
python tasks/T01-imagery/recover_windows.py /tmp/t01-recovered-windows
```

The script checks source identity, grid and SHA-256 of the four decoded uint8 bands in band-major row order. A change in TIFF packaging is reported separately. If an object ID changes, look up its recorded tile name and verify the pixels and grid before revising the manifest. Source services can retire an acquisition. Local temporary files and these retrieval checks carry no long-term retention guarantee.

# Domain glossary

Geospatial and research terms used in the [study design](research-direction.md).

| Term | Meaning |
|---|---|
| Canopy / crown | Tree cover visible from above. Crown overlap does not establish trunk location or ownership. |
| Epoch | An imagery observation period; local acquisition dates can differ within a nominal year. |
| Endpoint-visible gross loss | Canopy present in the first image and absent in the second, without subtracting gains elsewhere. Removal followed by regrowth between observations may be invisible. |
| Parcel attribution | Associating a loss event with the land parcels it overlaps, retaining overlaps with multiple parcels and unassigned areas. |
| Permit reconciliation | Comparing events with relevant records. `Matched` means a compatible record exists; `unmatched` requires an adequately covered, documented search; insufficient coverage remains `ambiguous`. These are not legal findings. |
| Valid-area denominator | The area supporting a reported measurement, with missing or unsuitable areas explicitly accounted for. |
| CRS / EPSG | Coordinate reference system / identifiers for standard coordinate systems. Projection and units determine whether area calculations are valid. |
| Registration | Spatial alignment of images. Misalignment can resemble canopy change. |
| Phenology | Seasonal vegetation changes, especially leaf emergence and loss. |
| Seamline | A boundary where source images are joined into a mosaic. |
| NIR | Near-infrared imagery, useful for distinguishing vegetation. |
| MMU | Minimum mapping unit: the smallest event area included in an analysis. |
| Estimand / sampling frame | The precise quantity being estimated / the population of units available for sampling. |
| Inclusion probability | A unit's chance of selection, needed to weight probability-sample estimates. |
| Preregistration | Recording evaluation methods and acceptance criteria before inspecting protected results. |
| Protected evaluation | Data reserved from local training and tuning. Geographic separation is needed because nearby imagery and parcels are correlated. |

## Source and local abbreviations

- **NAIP:** National Agriculture Imagery Program.
- **STAC:** SpatioTemporal Asset Catalog, used to discover geospatial assets.
- **NPU:** Atlanta Neighborhood Planning Unit.
- **DDH:** Dead, dying or hazardous tree category; verify each source's exact definition.
- **DBH:** Trunk diameter at breast height; not directly measured by overhead canopy imagery.

"""Stable-feature translation, restricted to checked exposure sides and fit hulls."""

import gzip
import json
from pathlib import Path
import sys

import numpy as np
from pyproj import Transformer
from rasterio.features import geometry_mask
from shapely import segmentize, transform as project
from shapely.geometry import MultiPoint, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
T05 = HERE.parent / "T05-paired-coverage"
sys.path.insert(0, str(T05))
import check_windows as t05  # noqa: E402


def exposure_sides(grid, shape):
    """Intersect source polygons before assigning native grid cell centers."""
    window = box(*(grid * (0, shape[0])), *(grid * (shape[1], 0)))
    layers = [("", window)]
    to_utm = Transformer.from_crs(4326, 26916, always_xy=True).transform
    for year, entry in json.loads(
        gzip.decompress((T05 / "date-index.json.gz").read_bytes())
    ).items():
        pieces = []
        for feature in entry["response"]["features"]:
            polygons = [Polygon(r) for r in feature["geometry"]["rings"]]
            if any(p.exterior.is_ccw for p in polygons):
                raise ValueError("Unexpected hole in pinned exposure snapshot")
            geom = project(
                segmentize(unary_union(polygons), 0.001), to_utm, interleaved=False
            )
            oid = feature["attributes"]["objectid" if year == "2023" else "FID"]
            for name, parent in layers:
                piece = geom.intersection(parent)
                if piece.area > 0:
                    pieces.append((f"{name}/{oid}".strip("/"), piece))
        layers = pieces
    sides = {}
    occupied = np.zeros(shape, dtype=bool)
    for name, geom in layers:
        mask = geometry_mask([geom], shape, grid, invert=True)
        if np.any(occupied & mask):
            raise ValueError("Ambiguous exposure at a cell center")
        sides[name] = (geom, mask)
        occupied |= mask
    if not occupied.all():
        raise ValueError("Incomplete indexed sides on pinned grids")
    return sides


def registration(site, pixels, grid, config, prior, sides):
    early, late = [t05.gradients(pixels[y], y) for y in (2023, 2025)]
    anchors = []
    for old, role in zip(prior, config["t05_roles"][site], strict=True):
        anchor = {k: old[k] for k in ("pixel_xy", "feature", "half_size")}
        if t05.align(early, late, anchor) != old:
            raise ValueError("T05 diagnostic replay differs")
        anchors.append((anchor, role, "T05"))
    for x, y, role, feature in config["fresh_controls"][site]:
        anchors.append(
            (dict(pixel_xy=[x, y], half_size=9, feature=feature), role, "T08")
        )
    records = []
    footprints = []
    for anchor, role, source in anchors:
        result = t05.align(early, late, anchor)
        x, y = anchor["pixel_xy"]
        # Search + binomial smoothing + gradient neighbor.
        r = anchor["half_size"] + t05.SEARCH_PIXELS + 3
        footprint = box(*(grid * (x - r, y + r + 1)), *(grid * (x + r + 1, y - r)))
        side = next(
            (k for k, (geom, _) in sides.items() if geom.covers(footprint)), None
        )
        reason = None
        if side is None:
            reason = "crosses exposure or window boundary"
        elif role == "diagnostic":
            reason = "diagnostic only"
        elif any(footprint.intersects(other) for other in footprints):
            reason = "overlaps previously allocated control support"
        else:
            footprints.append(footprint)
            if not result["passes_screen"]:
                reason = "T05 match screen"
        records.append(
            dict(
                **result,
                role=role,
                source=source,
                side=side,
                rejection=reason,
                raw_residual_east_north_m=[result["east_m"], result["north_m"]],
            )
        )
    report = {}
    supported = np.zeros(early.shape[1:], bool)
    # Values are late sampling offsets in (row, col), relative to an early cell.
    offsets = np.zeros((2, *supported.shape), dtype=int)
    for side, (_, cells) in sides.items():
        accepted = [c for c in records if c["side"] == side and c["rejection"] is None]
        fit = [c for c in accepted if c["role"] == "fit"]
        checks = [c for c in accepted if c["role"] == "check"]
        hull = MultiPoint(
            [grid * (c["pixel_xy"][0] + 0.5, c["pixel_xy"][1] + 0.5) for c in fit]
        ).convex_hull
        enough = len(fit) >= 3 and len(checks) >= 2 and hull.area > 0
        offset = None
        reason = "insufficient independent fit/check support"
        if enough:
            east, north = np.rint(
                np.median([[c["east_m"], c["north_m"]] for c in fit], axis=0) / 0.6
            ).astype(int)
            offset = [int(-north), int(east)]
            residuals = []
            for c in accepted:
                vector = np.round(
                    [c["east_m"] - east * 0.6, c["north_m"] - north * 0.6], 2
                )
                c["residual_east_north_m"] = vector.tolist()
                residuals.append(np.linalg.norm(vector))
            if max(residuals) <= 1.2 + 1e-9:
                support = geometry_mask([hull], cells.shape, grid, invert=True) & cells
                supported |= support
                offsets[:, support] = np.array(offset)[:, None]
                reason = None
            else:
                reason = "residual exceeds 1.2 m"
        report[side] = dict(
            native_m2=area(cells),
            supported_m2=area(cells & supported),
            uncertain_m2=area(cells & ~supported),
            fit_count=len(fit),
            check_count=len(checks),
            trial_sampling_offset_rc=offset,
            abstention=reason,
        )
    return records, report, supported, offsets


def area(mask):
    return round(int(np.count_nonzero(mask)) * 0.36, 2)

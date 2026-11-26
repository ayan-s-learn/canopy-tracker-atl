import argparse
import gzip
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from detector import (
    ACRE_M2,
    CROSS,
    PIXEL_M2,
    classify,
    components,
    distribution,
    event_id,
    match,
    sample_late,
)
from pyproj import Transformer
from rasterio.features import shapes
from rasterio.transform import from_bounds
from registration import HERE, T05, area, exposure_sides, registration, t05
from scipy import ndimage
from shapely import transform as project
from shapely.geometry import mapping, shape
from shapely.geometry.polygon import orient


def read(path):
    return json.loads(path.read_text())


def inputs(cache, samples, tiles):
    pixels, dates, grids = {}, {}, []
    for sample in samples:
        year = sample["year"]
        site = sample["site"]
        path = (
            cache
            / ("t01" if site in ("park", "west") else "t05")
            / f"{site}-{year}.tif"
        )
        pixels[year] = t05.verify(path.read_bytes(), sample)
        attrs = sample["attributes"]
        date = datetime.fromtimestamp(
            attrs["acquisition_date" if year == 2023 else "QQDATE"] / 1000, UTC
        ).date()
        if attrs["Name"] not in tiles or not attrs["Name"].endswith(
            date.strftime("%Y%m%d")
        ):
            raise ValueError("Tile identity or date differs from the reservation")
        dates[year] = date.isoformat()
        grids.append(from_bounds(*sample["bbox"], *sample["size"]))
    early, late = grids
    if not (
        early.almost_equals(late @ late.scale(2), precision=1e-7)
        and np.allclose([early.a, early.e], [0.6, -0.6], rtol=0, atol=1e-7)
    ):
        raise ValueError("Incompatible pair for block averaging")
    return pixels, dates, early


def features(site, cc, grid, known, supported, dates):
    labels, sizes, keys = cc
    edge = ~ndimage.binary_erosion(known, structure=CROSS, border_value=0)
    boundary = set(labels[edge])
    reg_unknown = set(labels[~supported])
    to_wgs = Transformer.from_crs(26916, 4326, always_xy=True).transform
    for geom, value in shapes(labels, mask=labels > 0, transform=grid, connectivity=4):
        i = int(value)
        polygon = shape(geom)
        # GDAL may emit self-touching rings at diagonal contacts within one component.
        if not polygon.is_valid:
            polygon = polygon.buffer(0)
        if abs(polygon.area - sizes[i] * PIXEL_M2) > 1e-5:
            raise ValueError("Component area differs from polygon area")
        projected = project(polygon, to_wgs, interleaved=False)
        if projected.geom_type == "Polygon":
            projected = orient(projected)
        yield {
            "type": "Feature",
            "id": event_id(site, keys[i], labels.shape[1]),
            "properties": {
                "site": site,
                "pixels": int(sizes[i]),
                "area_m2": round(sizes[i] * PIXEL_M2, 2),
                "first": dates[2023],
                "second": dates[2025],
                "edge_truncated_possible": i in boundary,
                "registration_uncertain": i in reg_unknown,
            },
            "geometry": mapping(projected),
        }


def scenarios(supported, offsets, sides, controls):
    shape = supported.shape
    zero = np.zeros((2, *shape), dtype=int)
    yield "raw", zero
    if supported.any():
        yield "supported_correction", offsets
        # Local bounds from signed residuals of accepted controls on each supported side.
        bounds = []
        for side, (_, cells) in sides.items():
            if (cells & supported).any():
                residuals = [
                    c["residual_east_north_m"]
                    for c in controls
                    if c["side"] == side and "residual_east_north_m" in c
                ]
                rc = np.rint(np.array(residuals)[:, [1, 0]] * [-1, 1] / 0.6).astype(int)
                bounds.append(
                    (
                        cells & supported,
                        np.minimum(0, rc.min(0)),
                        np.maximum(0, rc.max(0)),
                    )
                )
        for ri in (0, 1):
            for ci in (0, 1):
                trial = offsets.copy()
                for cells, lo, hi in bounds:
                    trial[:, cells] += np.array([(lo, hi)[ri][0], (lo, hi)[ci][1]])[
                        :, None
                    ]
                yield f"measured_bounds_{ri}{ci}", trial
    if (~supported).any():
        for dr in (-2, 0, 2):
            for dc in (-2, 0, 2):
                if dr or dc:
                    trial = offsets.copy()
                    trial[:, ~supported] = np.array([dr, dc])[:, None]
                    yield f"hypothetical_rc_{dr}_{dc}", trial


def inspect_tiles(loss, known, crown, reported):
    tiles = []
    for r in range(0, loss.shape[0], 32):
        for c in range(0, loss.shape[1], 32):
            sl = np.s_[r : r + 32, c : c + 32]
            if known[sl].sum() >= 0.75 * 1024:
                tiles.append(
                    (r, c, int(loss[sl].sum()), int((crown[sl] & known[sl]).sum()))
                )
    # Peak loss count; among zero-loss tiles prefer the most known prior crown.
    flagged = max((t for t in tiles if t[2]), key=lambda t: t[2], default=None)
    quiet = max((t for t in tiles if not t[2]), key=lambda t: t[3], default=None)
    quiet_crown = min(
        (
            t
            for t in tiles
            if t[3] >= 256 and not reported[t[0] : t[0] + 32, t[1] : t[1] + 32].any()
        ),
        key=lambda t: (t[2] / t[3], -t[3]),
        default=None,
    )
    return {
        "flagged": flagged,
        "apparently_unchanged": quiet,
        "low_loss_crown": quiet_crown,
    }


def analyze_pair(site, pixels, dates, grid, sides, prior, config):
    h, w = pixels[2023].shape[1:]
    late = pixels[2025].reshape(4, h, 2, w, 2).mean(axis=(2, 4))
    early_crown, early_known = classify(pixels[2023], config)
    late_crown, late_known = classify(late, config)
    controls, side_report, supported, offsets = registration(
        site, pixels, grid, config, prior, sides
    )
    native_known = early_known & late_known
    native_loss = native_known & early_crown & ~late_crown
    native = components(native_loss)
    side_ids = np.zeros((h, w), int)
    for i, (_, cells) in enumerate(sides.values()):
        side_ids[cells] = i
    common = np.ones((h, w), bool)
    spatial = common.copy()
    inside_all = common.copy()
    for _, (dr, dc) in scenarios(supported, offsets, sides, controls):
        source_side, inside = sample_late(side_ids, dr, dc)
        inside_all &= inside
        spatial &= inside & (side_ids == source_side)
        common &= sample_late(late_known, dr, dc)[0]
    common &= early_known & spatial
    comparisons = {}
    raw = corrected = None
    for name, (dr, dc) in scenarios(supported, offsets, sides, controls):
        candidate = components(
            common & early_crown & ~sample_late(late_crown, dr, dc)[0]
        )
        if name == "raw":
            raw = corrected = candidate
        reference = raw if name == "supported_correction" else corrected
        _, sizes, keys = candidate
        above = (
            np.flatnonzero(
                sizes[1:] * PIXEL_M2 >= min(config["floors_acres"]) * ACRE_M2
            )
            + 1
        )
        entry = {
            "totals": distribution(sizes, config["floors_acres"]),
            "candidate_m2": {
                event_id(site, keys[i], w): round(sizes[i] * PIXEL_M2, 2) for i in above
            },
        }
        if name == "raw":
            entry["native_to_common_lineage"] = match(site, native, candidate, config)
        if name != "raw":
            entry["reference"] = "raw" if reference is raw else "supported_correction"
            entry["lineage"] = match(site, reference, candidate, config)
        comparisons[name] = entry
        if name == "supported_correction":
            corrected = candidate
    summary = {
        "dates": dates,
        "native_m2": round(h * w * PIXEL_M2, 2),
        "native_excluded_m2": 0,
        "epoch_known_crown_m2": [
            area(early_known & early_crown),
            area(late_known & late_crown),
        ],
        "native_scored_m2": area(native_known),
        "native_unknown_m2": area(~native_known),
        "epoch_unknown_m2": [area(~early_known), area(~late_known)],
        "common_scored_m2": area(common),
        "comparison_spatial_excluded_m2": area(~spatial),
        "comparison_unknown_m2": area(spatial & ~common),
        "comparison_outside_image_m2": area(~inside_all),
        "comparison_seam_excluded_inside_m2": area(inside_all & ~spatial),
        "registration": side_report,
        "native_counts": distribution(native[1], config["floors_acres"]),
        "inspection_rc_loss_prior_crown": inspect_tiles(
            native_loss,
            native_known,
            early_crown,
            (native[0] != 0) & (native[1][native[0]] * PIXEL_M2 >= 0.10 * ACRE_M2),
        ),
    }
    return (
        summary,
        controls,
        comparisons,
        list(features(site, native, grid, native_known, supported, dates)),
    )


def save(path, obj):
    raw = (
        json.dumps(
            obj,
            sort_keys=True,
            indent=None if path.suffix == ".gz" else 2,
            separators=(",", ":") if path.suffix == ".gz" else None,
            allow_nan=False,
        )
        + "\n"
    ).encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".gz" else raw)


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild T08 evidence from the eight pinned windows."
    )
    parser.add_argument("imagery_cache", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=True, parents=True)
    samples = (
        read(T05.parent / "T01-imagery/t01-windows.json")["samples"]
        + read(T05 / "window-evidence.json")["samples"]
    )
    prior = read(T05 / "alignment.json")
    config = read(HERE / "config.json")
    summaries, controls, comparisons, events = {}, {}, {}, []
    for reservation in read(T05 / "development-windows.geojson")["features"]:
        props = reservation["properties"]
        site = props["site"]
        samples_here = sorted(
            (s for s in samples if s["site"] == site), key=lambda s: s["year"]
        )
        pixels, dates, grid = inputs(args.imagery_cache, samples_here, props["tiles"])
        sides = exposure_sides(grid, pixels[2023].shape[1:])
        summaries[site], controls[site], comparisons[site], fs = analyze_pair(
            site, pixels, dates, grid, sides, prior[site], config
        )

        events.extend(fs)
    save(args.output / "sites.json", summaries)
    save(args.output / "controls.json", controls)
    save(args.output / "comparisons.json.gz", comparisons)
    save(
        args.output / "events.geojson.gz",
        {"type": "FeatureCollection", "features": events},
    )


if __name__ == "__main__":
    main()

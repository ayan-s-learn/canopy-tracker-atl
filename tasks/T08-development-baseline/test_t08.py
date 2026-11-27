"""Synthetic, independent masks exercise detection, matching and translation signs."""

import unittest
from hashlib import sha256

import numpy as np
from baseline import analyze_pair, read
from detector import classify, components, distribution, event_id, match, sample_late
from rasterio.transform import from_origin
from registration import HERE, area, registration
from shapely.geometry import box


def exercise():
    config = read(HERE / "config.json")
    n = 256
    rng = np.random.default_rng(408)
    texture = rng.integers(0, 2, (n, n)) * 60
    # Stable texture across the scene, independent of the rectangular crown truth.
    visible = rng.integers(60, 161, (n, n), dtype="uint8")
    original = np.stack([visible, visible, visible, visible])
    truth = np.zeros((n, n), bool)
    truth[60:160, 65:180] = True
    original[0, truth] = 45
    original[3, truth] = (135 + texture)[truth]
    changed = original.copy()
    patch = np.zeros_like(truth)
    patch[85:121, 100:136] = True
    changed[:, patch] = original[1, patch]
    # The late image's features appear 3 rows south and 2 columns west.
    offset = (3, -2)
    shifted = np.roll(original, offset, axis=(1, 2))
    early, early_known = classify(original, config)
    if not np.array_equal(early, truth):
        raise AssertionError(
            "Synthetic early crown disagrees with its independent rectangle"
        )
    fixture_config = {
        **config,
        "fresh_controls": {
            "fixture": [
                [42, 42, "fit", "NW"],
                [210, 42, "fit", "NE"],
                [120, 209, "fit", "S"],
                [80, 105, "check", "W"],
                [177, 120, "check", "E"],
            ]
        },
        "t05_roles": {"fixture": []},
    }
    grid = from_origin(0, n * 0.6, 0.6, 0.6)
    sides = {"one": (box(0, 0, n * 0.6, n * 0.6), np.ones_like(truth))}
    records, report, support, field = registration(
        "fixture",
        {2023: original, 2025: shifted.repeat(2, 1).repeat(2, 2)},
        grid,
        fixture_config,
        [],
        sides,
    )
    if (
        not support.any()
        or not np.all(field[:, support] == np.array(offset)[:, None])
        or report["one"]["abstention"] is not None
    ):
        raise AssertionError("Registration failed to recover the known shift")
    checks = {}
    for name, late_pixels, expected, alignment in [
        ("same_epoch", original, np.zeros_like(truth), (0, 0)),
        ("shift_raw", shifted, truth & ~np.roll(truth, offset, axis=(0, 1)), (0, 0)),
        (
            "shift_raw_supported",
            shifted,
            truth & ~np.roll(truth, offset, axis=(0, 1)),
            (0, 0),
        ),
        ("shift_registered", shifted, np.zeros_like(truth), field),
        ("inserted_loss", changed, patch, (0, 0)),
    ]:
        late, known = classify(late_pixels, config)
        moved, inside = sample_late(late, *alignment)
        valid = early_known & inside & sample_late(known, *alignment)[0]
        if name in ("shift_registered", "shift_raw_supported"):
            fitted_known, fitted_inside = sample_late(known, *field)
            valid &= support & known & fitted_known & fitted_inside
        observed = early & ~moved & valid
        expected = expected & valid

        def describe(mask):
            _labels, sizes, keys = components(mask)
            return {
                "mask_sha256": sha256(mask.tobytes()).hexdigest(),
                "area_m2": area(mask),
                "events": [event_id("fixture", p, n) for p in keys[1:]],
                "floors": distribution(sizes, config["floors_acres"]),
            }

        if not np.array_equal(expected, observed):
            raise AssertionError(f"{name} loss differs from independent truth")
        checks[name] = {
            "scored_m2": area(valid),
            "expected": describe(expected),
            "observed": describe(observed),
        }
    # Run the production pair analysis. The loss rectangle is well inside the
    # common eligibility mask. Only the portion outside the fit hull should remain.
    raw_shift_loss = truth & ~np.roll(truth, offset, axis=(0, 1))
    if not (raw_shift_loss & support).any():
        raise AssertionError("Fixture lacks loss inside its supported area")
    for late_pixels, expected in [
        (original, np.zeros_like(truth)),
        (changed, patch),
        (shifted, raw_shift_loss),
    ]:
        native, _, trials, events = analyze_pair(
            "fixture",
            {2023: original, 2025: late_pixels.repeat(2, 1).repeat(2, 2)},
            {2023: "2023-10-08", 2025: "2025-10-11"},
            grid,
            sides,
            [],
            fixture_config,
        )
        expected_totals = distribution(components(expected)[1], config["floors_acres"])
        if (
            native["native_counts"] != expected_totals
            or trials["raw"]["totals"] != expected_totals
        ):
            raise AssertionError("Pair pipeline disagrees with the known raw events")
        if sorted(f["id"] for f in events) != sorted(
            event_id("fixture", p, n) for p in components(expected)[2][1:]
        ):
            raise AssertionError(
                "Archived geometry IDs differ from expected components"
            )
        if late_pixels is shifted:
            expected_corrected = distribution(
                components(raw_shift_loss & ~support)[1], config["floors_acres"]
            )
            if trials["supported_correction"]["totals"] != expected_corrected:
                raise AssertionError(
                    "Fitted correction did not remove supported displacement loss"
                )
    return {
        "fitted_sampling_offset_rc": report["one"]["trial_sampling_offset_rc"],
        "check_residuals_east_north_m": [
            c["residual_east_north_m"] for c in records if c["role"] == "check"
        ],
        "cases": checks,
    }


class BaselineChecks(unittest.TestCase):
    def test_archived_controls(self):
        self.assertEqual(exercise(), read(HERE / "fixtures.json"))

    def test_comparisons_keep_texture_neighborhoods_on_one_side(self):
        n = 64
        mid = n // 2
        early = np.full((4, n, n), 100, np.uint8)
        pixels = {2023: early, 2025: early.repeat(2, 1).repeat(2, 2)}
        grid = from_origin(0, n * 0.6, 0.6, 0.6)
        rows, cols = np.indices((n, n))
        sides = {
            "left": (box(0, 0, mid * 0.6, n * 0.6), cols < mid),
            "right": (box(mid * 0.6, 0, n * 0.6, n * 0.6), cols >= mid),
        }
        config = {
            **read(HERE / "config.json"),
            "fresh_controls": {"fixture": []},
            "t05_roles": {"fixture": []},
        }
        summary, _, _, _ = analyze_pair(
            "fixture", pixels, {2023: "2023", 2025: "2025"}, grid, sides, [], config
        )
        # Two pixels for texture and two for trial offsets at each outer and seam edge.
        eligible = (
            (rows >= 4)
            & (rows < n - 4)
            & (cols >= 4)
            & (cols < n - 4)
            & ((cols < mid - 4) | (cols >= mid + 4))
        )
        self.assertEqual(summary["common_scored_m2"], area(eligible))
        self.assertEqual(summary["native_scored_m2"], round((n - 4) ** 2 * 0.36, 2))

    def test_exact_texture_cutoff_and_unknown(self):
        config = read(HERE / "config.json")
        bands = np.full((4, 11, 11), 60, dtype=np.uint8)
        bands[3] = 100
        bands[3, 3:8, 4] = 125  # Five elevated samples in the 25-cell window: SD = 10.
        crown, known = classify(bands, config)
        self.assertTrue(crown[5, 5] and known[5, 5])
        self.assertFalse(known[1, 5])
        bands[:3, 5, 5] = 30
        self.assertFalse(classify(bands, config)[1][5, 5])
        bands[3, 5, 4] = 124
        self.assertFalse(classify(bands, config)[0][5, 5])

    def test_collinear_controls_cannot_support_a_correction(self):
        n = 512
        raster = np.random.default_rng(438).integers(50, 200, (4, n, n), dtype=np.uint8)
        pixels = {
            2023: raster,
            2025: np.roll(raster, (2, 1), axis=(1, 2)).repeat(2, 1).repeat(2, 2),
        }
        grid = from_origin(747589.8, 3739469.4, 0.6, 0.6)
        sides = {
            "side": (box(*(grid @ (0, n)), *(grid @ (n, 0))), np.ones((n, n), bool))
        }
        config = {
            "fresh_controls": {
                "fixture": [
                    [188, 75, "fit", "A"],
                    [270, 149, "fit", "B"],
                    [352, 223, "fit", "C"],
                    [80, 400, "check", "D"],
                    [420, 100, "check", "E"],
                ]
            },
            "t05_roles": {"fixture": []},
        }
        _, report, support, _ = registration("fixture", pixels, grid, config, [], sides)
        self.assertEqual(
            (report["side"]["fit_count"], report["side"]["check_count"]), (3, 2)
        )
        self.assertFalse(support.any())
        self.assertIsNone(report["side"]["trial_sampling_offset_rc"])

    def test_overlap_graph_and_diagonal_disconnect(self):
        full = np.zeros((12, 12), bool)
        full[1:4, 1:10] = True
        full[4, 10] = True
        split = full.copy()
        split[1:4, 5] = False
        split[4, 10] = False
        split[9:11, 9:11] = True
        conf = {"floors_acres": [0.00001], "match_iou_min": 0.10}
        a, b = components(full), components(split)
        forward = match("s", a, b, conf)["1e-05"]
        self.assertEqual(forward["split"], ["s-1-1"])
        self.assertEqual(forward["lost"], ["s-4-10"])
        self.assertEqual(forward["new"], ["s-9-9"])
        self.assertEqual(match("s", b, a, conf)["1e-05"]["merged"], ["s-1-1"])


if __name__ == "__main__":
    unittest.main()

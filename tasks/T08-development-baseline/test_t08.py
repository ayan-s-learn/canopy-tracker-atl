"""Synthetic, independent masks exercise detection, matching and translation signs."""

from hashlib import sha256
import unittest

import numpy as np
from rasterio.transform import from_origin
from shapely.geometry import box

from baseline import read
from detector import classify, components, distribution, event_id, match, sample_late
from registration import HERE, area, registration


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
        ("shift_registered", shifted, np.zeros_like(truth), offset),
        ("inserted_loss", changed, patch, (0, 0)),
    ]:
        late, known = classify(late_pixels, config)
        moved, inside = sample_late(late, *alignment)
        valid = early_known & inside & sample_late(known, *alignment)[0]
        if name == "shift_registered":
            valid &= support
        observed = early & ~moved & valid
        expected = expected & valid

        def describe(mask):
            labels, sizes, keys = components(mask)
            return dict(
                mask_sha256=sha256(mask.tobytes()).hexdigest(),
                area_m2=area(mask),
                events=[event_id("fixture", p, n) for p in keys[1:]],
                floors=distribution(sizes, config["floors_acres"]),
            )

        if not np.array_equal(expected, observed):
            raise AssertionError(f"{name} loss differs from independent truth")
        checks[name] = dict(
            scored_m2=area(valid),
            expected=describe(expected),
            observed=describe(observed),
        )
    return dict(
        fitted_sampling_offset_rc=report["one"]["trial_sampling_offset_rc"],
        check_residuals_east_north_m=[
            c["residual_east_north_m"] for c in records if c["role"] == "check"
        ],
        cases=checks,
    )


class BaselineChecks(unittest.TestCase):
    def test_archived_controls(self):
        self.assertEqual(exercise(), read(HERE / "fixtures.json"))

    def test_overlap_graph_and_diagonal_disconnect(self):
        full = np.zeros((12, 12), bool)
        full[1:4, 1:10] = True
        full[4, 10] = True
        split = full.copy()
        split[1:4, 5] = False
        split[4, 10] = False
        split[9:11, 9:11] = True
        conf = dict(floors_acres=[0.00001], match_iou_min=0.10)
        a, b = components(full), components(split)
        forward = match("s", a, b, conf)["1e-05"]
        self.assertEqual(forward["split"], ["s-1-1"])
        self.assertEqual(forward["lost"], ["s-4-10"])
        self.assertEqual(forward["new"], ["s-9-9"])
        self.assertEqual(match("s", b, a, conf)["1e-05"]["merged"], ["s-1-1"])


if __name__ == "__main__":
    unittest.main()

"""Four-neighbor endpoint-loss components on a common 0.6 m grid."""

import numpy as np
from scipy import ndimage

ACRE_M2 = 4046.8564224
PIXEL_M2 = 0.36
CROSS = ndimage.generate_binary_structure(2, 1)


def classify(bands, config):
    red, green, blue, nir = bands.astype("float64")
    n = config["texture_window_px"]
    # With uint8 samples or 2x2 averages these sums are exact, even at the SD threshold.
    kernel = np.ones((n, n))
    total = ndimage.correlate(nir, kernel)
    total_sq = ndimage.correlate(nir * nir, kernel)
    textured = n * n * total_sq - total * total >= (n * n * config["nir_sd_min"]) ** 2
    ndvi = (nir - red) / np.maximum(1, nir + red)
    crown = (ndvi >= config["ndvi_min"]) & textured
    dark = (red + green + blue) / 3 < config["shadow_rgb_mean_below"]
    known = ~dark
    radius = n // 2
    known[:radius] = known[-radius:] = False
    known[:, :radius] = known[:, -radius:] = False
    return crown, known


def sample_late(array, dr, dc):
    rows, cols = np.indices(array.shape)
    rows += dr
    cols += dc
    inside = (
        (rows >= 0) & (rows < array.shape[0]) & (cols >= 0) & (cols < array.shape[1])
    )
    return array[
        rows.clip(0, array.shape[0] - 1), cols.clip(0, array.shape[1] - 1)
    ], inside


def components(mask):
    labels, n = ndimage.label(mask, CROSS)
    sizes = np.bincount(labels.ravel(), minlength=n + 1)
    anchors = np.full(n + 1, mask.size, dtype=int)
    positions = np.flatnonzero(mask)
    np.minimum.at(anchors, labels.ravel()[positions], positions)
    return labels, sizes, anchors


def event_id(site, position, width):
    row, col = divmod(int(position), width)
    return f"{site}-{row}-{col}"


def distribution(sizes, floors):
    areas = sizes[1:] * PIXEL_M2
    return {
        str(acres): {
            "count": int((areas >= acres * ACRE_M2).sum()),
            "m2": round(float(areas[areas >= acres * ACRE_M2].sum()), 2),
        }
        for acres in [0, *floors]
    }


def match(site, base, trial, config):
    """Many-to-many graph at each reporting floor; IDs scoped to each scenario."""
    a, a_sizes, a_keys = base
    b, b_sizes, b_keys = trial
    overlap = (a > 0) & (b > 0)
    pairs, counts = np.unique(
        np.stack((a[overlap], b[overlap]), axis=1), axis=0, return_counts=True
    )
    edges = []
    for (left, right), n in zip(pairs, counts):
        iou = n / (a_sizes[left] + b_sizes[right] - n)
        if iou >= config["match_iou_min"]:
            edges.append((left, right, round(float(iou), 6)))

    def ids(keys, labels):
        return [event_id(site, keys[v], a.shape[1]) for v in sorted(labels)]

    report = {}
    for floor in config["floors_acres"]:
        aa = set(np.flatnonzero(a_sizes[1:] * PIXEL_M2 >= floor * ACRE_M2) + 1)
        bb = set(np.flatnonzero(b_sizes[1:] * PIXEL_M2 >= floor * ACRE_M2) + 1)
        kept = [(l, r, s) for l, r, s in edges if l in aa and r in bb]
        lhs = [l for l, _, _ in kept]
        rhs = [r for _, r, _ in kept]
        report[str(floor)] = {
            "retained_links": [
                [ids(a_keys, [l])[0], ids(b_keys, [r])[0], s] for l, r, s in kept
            ],
            "lost": ids(a_keys, aa - set(lhs)),
            "new": ids(b_keys, bb - set(rhs)),
            "split": ids(a_keys, {l for l in lhs if lhs.count(l) > 1}),
            "merged": ids(b_keys, {r for r in rhs if rhs.count(r) > 1}),
        }
    return report

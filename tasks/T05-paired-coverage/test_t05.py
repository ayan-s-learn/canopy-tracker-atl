import unittest

import numpy as np
from shapely.geometry import box

from check_windows import align
from coverage import assign, classify, partitions


class CoverageTest(unittest.TestCase):
    def test_five_coverage_classes_reconcile(self):
        city = box(0, 0, 5, 1)
        masks = classify(city, box(0, 0, 2, 1), box(1, 0, 3, 1), box(4, 0, 5, 1))
        expected = {
            '2023_only': box(0, 0, 1, 1),
            'both': box(1, 0, 2, 1),
            '2025_only': box(2, 0, 3, 1),
            'neither': box(3, 0, 4, 1),
            'unresolved': box(4, 0, 5, 1),
        }
        self.assertEqual(masks.keys(), expected.keys())
        for key in masks:
            self.assertTrue(masks[key].equals(expected[key]), key)
        partitions(city, {'Fulton': city}, {'City': masks, 'Fulton': masks})

    def test_priority_preserves_date_conflicts(self):
        a, b, unknown = box(0, 0, 2, 1), box(1, 0, 3, 1), box(2, 0, 4, 1)
        selected, coverage, conflict = assign({
            'tile-b': (b, '2025-10-15'),
            'tile-a': (a, '2025-10-11'),
            'tile-c': (unknown, None),
        })
        self.assertTrue(selected['tile-a'].equals(a))
        self.assertTrue(selected['tile-b'].equals(box(2, 0, 3, 1)))
        self.assertTrue(coverage.equals(box(0, 0, 3, 1)))
        self.assertTrue(conflict.equals(box(1, 0, 2, 1)))


class AlignmentTest(unittest.TestCase):
    def test_ground_units_and_direction(self):
        early = np.random.default_rng(14).normal(size=(2, 48, 48))
        late = np.roll(early, shift=(2, -3), axis=(1, 2))
        anchor = {'pixel_xy': [24, 24], 'half_size': 8}
        result = align(early, late, anchor)
        self.assertTrue(result['passes_screen'])
        self.assertEqual(result['east_m'], -1.8)
        self.assertEqual(result['north_m'], -1.2)

    def test_flat_features_fail_screen(self):
        pixels = np.zeros((2, 48, 48))
        anchor = {'pixel_xy': [24, 24], 'half_size': 8}
        self.assertFalse(align(pixels, pixels, anchor)['passes_screen'])


if __name__ == '__main__':
    unittest.main()

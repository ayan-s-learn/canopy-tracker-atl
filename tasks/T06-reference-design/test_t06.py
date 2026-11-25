import copy
import json
import unittest
from pathlib import Path

from shapely.geometry import box, mapping, shape

import check_split

ROOT = Path(__file__).resolve().parent


class SplitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.split, cls.city, cls.paired = check_split.build()

    def test_published_split_and_checks_replay(self):
        saved = json.loads((ROOT / 'split.geojson').read_text())
        self.assertEqual(json.loads(json.dumps(self.split)), saved)
        self.assertEqual(check_split.validate(saved['features'], self.city, self.paired),
                         json.loads((ROOT / 'split-check.json').read_text()))

    def test_reject_candidate_context_inside_exclusion(self):
        saved = copy.deepcopy(self.split)
        features = saved['features']
        context = next(f for f in features if f['properties']['kind'] == 'candidate_context')
        exclusion = next(f for f in features if f['properties']['kind'] == 'buffered_development')
        exclusion['geometry'] = mapping(
            shape(exclusion['geometry']).union(shape(context['geometry']))
        )
        with self.assertRaisesRegex(ValueError, 'violates City, coverage, context or separation'):
            check_split.validate(features, self.city, self.paired)


class ReferenceFixtureTest(unittest.TestCase):
    def test_cross_core_loss_missed_loss_and_unresolved_queue(self):
        data = json.loads((ROOT / 'synthetic-reference.json').read_text())
        ref, queue, cells, expected = (
            data[key] for key in ('reference', 'queue', 'cells', 'expected')
        )
        self.assertIn('R1', data['interpretations']['first']['A']['loss'])
        self.assertIn('R1', data['interpretations']['first']['B']['loss'])
        self.assertIn('R2', data['interpretations']['repeat']['B']['uncertain'])
        self.assertIn('R2', data['adjudication']['B'])
        self.assertLess(ref['R1']['bbox'][0], cells['B']['bbox'][0])
        self.assertEqual(queue['Q1']['bbox'][0], cells['B']['bbox'][0])
        matched = set()
        for item in queue.values():
            geom = box(*item['bbox'])
            if item['status'] == 'match':
                other = box(*ref[item['reference_id']]['bbox'])
                self.assertGreaterEqual(geom.intersection(other).area / geom.union(other).area,
                                        data['match_min_iou'])
                self.assertNotIn(item['reference_id'], matched)
                matched.add(item['reference_id'])
            elif item['status'] == 'unresolved':
                self.assertTrue(box(*ref['U1']['bbox']).covers(geom))
            else:
                self.assertTrue(all(geom.disjoint(box(*r['bbox'])) for r in ref.values()))

        weights = {}
        for identifier, item in ref.items():
            if item['status'] == 'loss':
                self.assertGreaterEqual(box(*item['bbox']).area, data['mmu_m2'])
                x, y, _, _ = item['bbox']
                owner, = [
                    cell for cell, value in cells.items()
                    if value['bbox'][0] <= x < value['bbox'][2]
                    and value['bbox'][1] <= y < value['bbox'][3]
                ]
                self.assertEqual(owner, item['anchor_cell'])
                weights[identifier] = 1 / cells[owner]['inclusion_probability']

        unresolved = sum(item['status'] == 'unresolved' for item in queue.values())
        self.assertEqual(len(weights), expected['reference_anchors'])
        self.assertEqual(len(matched), expected['matched_anchors'])
        self.assertEqual(len(matched) / len(weights), expected['unweighted_recall'])
        self.assertEqual(sum(weights[k] for k in matched) / sum(weights.values()),
                         expected['weighted_recall'])
        self.assertEqual(box(*ref['U1']['bbox']).area, expected['unknown_area_m2'])
        self.assertEqual(len(matched) / (len(queue) - unresolved),
                         expected['queue_complete_case_precision'])
        self.assertEqual([len(matched) / len(queue), (len(matched) + unresolved) / len(queue)],
                         expected['queue_precision_bounds'])


if __name__ == '__main__':
    unittest.main()

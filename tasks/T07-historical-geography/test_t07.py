import unittest
from datetime import date, datetime, timezone
from itertools import combinations

from shapely import union_all
from shapely.geometry import shape

from membership import HERE, T02, build, classify, dated_state, read_json, reproject


def days(start, end=None):
    return date.fromisoformat(start), date.fromisoformat(end or start)


class HistoricalMembershipTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.layer, cls.areas = build()
        cls.ledger = read_json(HERE / 'effective-dates.json')
        cls.cases = {row['city_objectid']: row for row in cls.ledger['cases'] if row['city_objectid'] is not None}

    def test_archived_annexations_and_city_index(self):
        archived = read_json(T02 / 'atlanta-annexations-2023-onward.json')['features']
        dates = [datetime.fromtimestamp(row['attributes']['EFF_DATE'] / 1000, timezone.utc).date().isoformat()
                 for row in archived]
        self.assertCountEqual(
            dates, [self.cases[oid]['city_gis_date'] for oid in self.ledger['t02_archive_objectids']],
        )
        source = read_json(HERE / 'sources.json')['city_arcgis']
        index = [dict(zip(source['index_columns'], row, strict=True)) for row in source['index']]
        relevant = {
            row['OBJECTID'] for row in index
            if row['YEARANNEXED'] is None or row['YEARANNEXED'] >= 2023
            or (row['EFF_DATE'] is not None and row['EFF_DATE'] >= 1672531200000)
            or (row['STATUS'] == 'Deannexed' and row['EFF_DATE'] is None)
        }
        self.assertEqual(relevant, self.cases.keys())
        for oid in (4, 166):
            self.assertEqual(self.cases[oid]['disposition'], 'unresolved')
            self.assertIsNone(self.cases[oid]['earliest_effective_date'])

    def test_reported_dates_and_ranges(self):
        first = days('2023-10-08')
        for oid, city_day, effective_day in (
            (6083, '2025-09-24', '2025-10-01'), (6721, '2025-12-10', '2026-01-01'),
        ):
            case = self.cases[oid]
            with self.subTest(oid=oid):
                early = dated_state(case, first)
                self.assertEqual(classify(early, dated_state(case, days(city_day))), 'outside_both')
                self.assertEqual(classify(early, dated_state(case, days(effective_day))), 'second_only')
                self.assertEqual(classify(early, dated_state(case, days(city_day, effective_day))), 'unresolved')
        actual = {row['city_objectid']: row for row in self.areas['change_geometry'] if row['city_objectid'] is not None}
        self.assertEqual(actual[6083]['date_lookup'], 'second_only')
        self.assertEqual(actual[6721]['date_lookup'], 'outside_both')
        self.assertEqual(actual[7041]['date_lookup'], 'outside_both')
        self.assertIsNone(dated_state(self.cases[7041], days('2026-06-24')))
        unlocated = next(row for row in self.areas['change_geometry'] if row['ordinance'] == '26-O-1348')
        self.assertIsNone(unlocated['area_m2'])

    def test_deannexation_lookup(self):
        case = {
            'direction': 'deannexation',
            'earliest_effective_date': '2025-01-01',
            'latest_effective_date': '2025-01-01',
        }
        self.assertEqual(classify(dated_state(case, days('2023-10-08')),
                                  dated_state(case, days('2025-10-11'))), 'first_only')
        self.assertIsNone(dated_state(case, days('2024-12-31', '2025-01-01')))

    def test_export_reconciles(self):
        archived_layer = read_json(HERE / 'membership.geojson.gz')
        archived_areas = read_json(HERE / 'areas.json')
        for field in ('first', 'second', 'evidence_version'):
            self.assertEqual(self.layer[field], archived_layer[field])
            self.assertEqual(self.layer[field], archived_areas[field])
        discovery_pieces = []
        all_pieces = []
        report = self.areas['membership_m2']
        tolerance = self.areas['reconciliation_tolerance_m2']
        replayed = {
            (feature['properties']['scope'], feature['properties']['membership']):
            reproject(shape(feature['geometry']), 'OGC:CRS84')
            for feature in self.layer['features']
        }
        for feature in archived_layer['features']:
            props = feature['properties']
            geometry = shape(feature['geometry'])
            self.assertTrue(geometry.is_valid)
            polygons = geometry.geoms if geometry.geom_type == 'MultiPolygon' else (geometry,)
            for polygon in polygons:
                self.assertTrue(polygon.exterior.is_ccw)
                self.assertTrue(all(not ring.is_ccw for ring in polygon.interiors))
            projected = reproject(geometry, 'OGC:CRS84')
            self.assertTrue(projected.is_valid)
            expected = replayed.pop((props['scope'], props['membership']))
            self.assertLess(projected.symmetric_difference(expected).area, tolerance)
            self.assertAlmostEqual(projected.area, report[props['scope']][props['membership']]['total'],
                                   delta=tolerance)
            all_pieces.append(projected)
            if props['scope'] == 'discovery':
                discovery_pieces.append(projected)
        self.assertFalse(replayed)
        for scope, classes in report.items():
            for label, areas in classes.items():
                for key, area in areas.items():
                    self.assertAlmostEqual(area, archived_areas['membership_m2'][scope][label][key], delta=tolerance)
        self.assertLess(sum(a.intersection(b).area for a, b in combinations(all_pieces, 2)), tolerance)
        boundary, = read_json(T02 / 'atlanta-city-limits-2026-11-23.geojson')['features']
        city = reproject(shape(boundary['geometry']), 'OGC:CRS84')
        self.assertLess(union_all(discovery_pieces).symmetric_difference(city).area, tolerance)
        for key, area in self.areas['discovery_m2'].items():
            self.assertAlmostEqual(sum(row[key] for row in report['discovery'].values()), area, delta=tolerance)
        self.assertAlmostEqual(report['discovery']['unresolved']['total'], 690310.898, delta=tolerance)
        self.assertIsNone(self.areas['total_historical_extent_outside_discovery_m2'])

    def test_sample_windows(self):
        for sample, areas in self.areas['t01_windows_m2'].items():
            with self.subTest(sample=sample):
                self.assertGreater(areas['total'], 23000)
                self.assertAlmostEqual(areas['total'], areas['inside_both'], delta=1e-6)
        self.assertEqual(len(self.areas['t01_windows_m2']), 4)


if __name__ == '__main__':
    unittest.main()

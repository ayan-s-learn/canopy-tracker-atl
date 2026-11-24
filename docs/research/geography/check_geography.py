import gzip
import hashlib
import json
import math
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pyproj import Geod, Transformer
from shapely import segmentize, transform, union_all
from shapely.geometry import box, shape


MANIFEST_DIR = Path(__file__).resolve().parents[3] / 'manifests' / 'geography'


class GeographySnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((MANIFEST_DIR / 't02-sources.json').read_bytes())

    def read_snapshot(self, name):
        source = self.sources[name]
        path = MANIFEST_DIR / source['path']
        raw = path.read_bytes()
        if path.suffix == '.gz':
            raw = gzip.decompress(raw)
        self.assertEqual(len(raw), source['bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), source['sha256'])
        return json.loads(raw)

    def test_city_and_county_areas(self):
        feature, = self.read_snapshot('city_boundary')['features']
        source = self.sources['city_boundary']
        properties = feature['properties']
        self.assertEqual(properties['OBJECTID'], source['object_id'])
        self.assertEqual(properties['GLOBALID'], source['global_id'])
        self.assertEqual(properties['NAME'], 'Atlanta')
        self.assertEqual(properties['GEOTYPE'], 'City')
        self.assertIsNone(properties['EFFECTDATE'])
        edited = datetime.fromtimestamp(properties['LAST_EDITED_DATE'] / 1000, timezone.utc)
        self.assertEqual(edited, datetime.fromisoformat(source['last_edited_utc']))

        city = shape(feature['geometry'])
        counties = {
            feature['properties']['GEOID']: shape(feature['geometry'])
            for feature in self.read_snapshot('county_overlay')['features']
        }
        self.assertEqual(set(counties), {'13089', '13121'})
        self.assertEqual(city.geom_type, 'MultiPolygon')
        self.assertEqual(len(city.geoms), 2)
        for geometry in (city, *counties.values()):
            self.assertTrue(geometry.is_valid and not geometry.is_empty)

        area_check = self.sources['area_check']
        rectangle = box(*area_check['rectangle_lonlat'])
        self.assertTrue(rectangle.covers(city))
        to_equal_area = Transformer.from_crs('OGC:CRS84', area_check['crs'], always_xy=True)
        self.assertEqual(to_equal_area.target_crs.axis_info[0].unit_name, 'metre')

        city_m = transform(city, to_equal_area.transform, interleaved=False)
        rectangle_m = transform(
            segmentize(rectangle, area_check['rectangle_segment_max_degrees']),
            to_equal_area.transform,
            interleaved=False,
        )
        fulton_m = transform(counties['13121'], to_equal_area.transform, interleaved=False)
        dekalb_m = transform(counties['13089'], to_equal_area.transform, interleaved=False)
        areas = {
            'city': city_m.area,
            'rectangle': rectangle_m.area,
            'city_outside_rectangle': city_m.difference(rectangle_m).area,
            'rectangle_outside_city': rectangle_m.difference(city_m).area,
            'fulton_city_intersection': city_m.intersection(fulton_m).area,
            'dekalb_city_intersection': city_m.intersection(dekalb_m).area,
            'city_outside_counties': city_m.difference(union_all([fulton_m, dekalb_m])).area,
            'city_in_both_counties': city_m.intersection(fulton_m).intersection(dekalb_m).area,
        }
        for name, area in areas.items():
            with self.subTest(area=name):
                self.assertTrue(
                    math.isclose(area, area_check['expected_m2'][name], rel_tol=0,
                                 abs_tol=area_check['tolerance_m2']),
                    f'{name} measured {area:,.3f} m²',
                )
        geodesic_area, _ = Geod(ellps='WGS84').geometry_area_perimeter(city)
        self.assertAlmostEqual(abs(geodesic_area), city_m.area, delta=2)

    def test_annexation_dates(self):
        response = self.read_snapshot('annexations')
        self.assertFalse(response.get('exceededTransferLimit', False))
        dates = []
        for feature in response['features']:
            self.assertEqual(feature['attributes']['STATUS'], 'Annexed')
            effective_ms = feature['attributes']['EFF_DATE']
            dates.append(datetime.fromtimestamp(effective_ms / 1000, timezone.utc).date().isoformat())
        self.assertCountEqual(dates, self.sources['annexations']['effective_dates_utc'])


if __name__ == '__main__':
    unittest.main()

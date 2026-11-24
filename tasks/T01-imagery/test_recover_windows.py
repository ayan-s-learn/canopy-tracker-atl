import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

from recover_windows import recover


class WindowRecoveryTest(unittest.TestCase):
    def test_repackaged_tiff_resumes_offline_and_detects_corruption(self):
        pixels = np.arange(16, dtype='uint8').reshape(4, 2, 2)
        bounds = [100, 200, 102, 202]

        def encode(values, compression):
            with MemoryFile() as mem:
                with mem.open(driver='GTiff', width=2, height=2, count=4, dtype='uint8',
                              crs='EPSG:26916', transform=from_bounds(*bounds, 2, 2),
                              compress=compression, photometric='MINISBLACK') as image:
                    image.write(values)
                return mem.read()

        original = encode(pixels, 'none')
        repacked = encode(pixels, 'deflate')
        self.assertNotEqual(original, repacked)
        sample = dict(site='park', year=2023, size=[2, 2], crs='EPSG:26916', bbox=bounds,
                      dtype='uint8', nodata=None, mask_flags=[['all_valid']] * 4,
                      sha256_tiff=hashlib.sha256(original).hexdigest(),
                      sha256_pixels_band_major=hashlib.sha256(pixels.tobytes()).hexdigest(),
                      attributes={'Name': 'sample'}, item_url='item', url='image')
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            with patch('recover_windows.fetch', side_effect=[
                json.dumps({'attributes': sample['attributes']}), repacked,
            ]) as fetch:
                recover(sample, target)
                recover(sample, target)
                self.assertEqual(fetch.call_count, 2)
                (target / 'park-2023.tif').write_bytes(encode(pixels + 1, 'deflate'))
                with self.assertRaisesRegex(ValueError, 'Pixel content changed'):
                    recover(sample, target)


if __name__ == '__main__':
    unittest.main()

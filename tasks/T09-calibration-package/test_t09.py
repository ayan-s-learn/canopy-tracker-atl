"""Exercise T09's score rules and replay a fixed synthetic submission on a rebuilt packet."""

from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np
from shapely.geometry import box

from build_packet import blank_case, context, dump_json, file_hash, nominal_late, read_json
from score_returns import archive, compare, finish, measure, validate_case


def ring(left, top, right, bottom):
    return [[left, top], [right, top], [right, bottom], [left, bottom]]


def complete(key, minutes, **masks):
    record = dict(blank_case(key), status='complete', confidence='high', active_minutes=minutes)
    record['masks'].update({name: [shape] for name, shape in masks.items()})
    return record


def save_return(path, assignment, code, updates):
    data = deepcopy(assignment['blank'])
    data['code'] = code
    data['cases'] = [updates.get(record['id'], dict(record, status='skipped')) for record in data['cases']]
    path.write_text(dump_json(data))


def replay(packet, run):
    assignment = read_json(packet / 'owner-ledger.json')['assignment']
    run.mkdir(mode=0o700)
    vault = run / 'vault'
    vault.mkdir(mode=0o700)
    a = complete('C02', 3.25, crown_2023=ring(80, 80, 100, 90), loss=ring(80, 80, 90, 90),
                 unknown_2025=ring(130, 80, 135, 90))
    b = complete('C02', 4.5, crown_2023=ring(90, 80, 120, 90), loss=ring(110, 80, 120, 90),
                 unknown_2025=ring(80, 80, 85, 90))
    a['reason'] = 'Synthetic shadow on the right in 2025.'
    b['reason'] = 'Synthetic shadow on the left in 2025.'
    # Other cases are deliberately skipped in both returns. The fixture injects
    # geometry to test the tool and does not interpret the rendered exercise.
    updates = (
        {'C02': a, 'C06': complete('C06', 1)},
        {'C02': b, 'C06': dict(blank_case('C06'), status='unreadable', active_minutes=2,
                              reason='Synthetic unreadable case.')},
    )
    check = unittest.TestCase()
    for code, records in zip(('R01', 'R02'), updates, strict=True):
        drop = run / code
        drop.mkdir(mode=0o700)
        source = drop / 'return.json'
        save_return(source, assignment, code, records)
        other = 'R02' if code == 'R01' else 'R01'
        with check.assertRaisesRegex(ValueError, 'Wrong packet, assigned code or role'):
            archive(source, vault, assignment, other)
        check.assertEqual(archive(source, vault, assignment, code), file_hash(source))
        with check.assertRaises(FileExistsError):
            archive(source, vault, assignment, code)
        check.assertEqual((vault / f'{code}.json').stat().st_mode & 0o777, 0o600)
        check.assertEqual(source.read_bytes(), (vault / f'{code}.json').read_bytes())

    scored = run / 'scored'
    report = compare(packet, vault, scored)
    case = report['cases']['C02']
    check.assertEqual([r['traced_loss_m2'] for r in case['readers']], [36, 36])
    check.assertEqual(case['comparison'], {
        'crown_iou': {'2023': 0.25, '2025': 1},
        'crown_common_known_m2': {'2023': 14400, '2025': 14364},
        'unknown_xor_m2': {'2023': 0, '2025': 36, 'change': 0},
        'loss_xor_m2': 72, 'loss_common_known_xor_m2': 54, 'loss_common_known_m2': 14364,
    })
    empty = report['cases']['C06']
    check.assertEqual([r['disposition'] for r in empty['readers']], ['no_loss', 'unreadable'])
    check.assertEqual([r['visible_loss_m2'] for r in empty['readers']], [0, None])
    check.assertIsNone(empty['comparison']['loss_xor_m2'])
    check.assertIsNone(report['cases']['C01']['readers'][0]['active_minutes'])
    check.assertEqual(report['minutes'], {
        'R01': {'total': 4.25, 'recorded': 2, 'missing': 10},
        'R02': {'total': 6.5, 'recorded': 2, 'missing': 10},
    })

    state = read_json(scored / 'adjudication-state.json')
    adjudicator = state['assignment']
    check.assertNotEqual(adjudicator['packet'], assignment['packet'])
    decisions = {item['id']: dict(blank_case(item['id']), status='skipped', resolution='unresolved',
                                  reason='Fixture supplied no interpretation.', active_minutes=0)
                 for item in adjudicator['cases']}
    decisions['C02'] = dict(a, resolution='resolved', reason='Fixture selects reader A.',
                           active_minutes=2.75)
    decisions['C06'] = dict(decisions['C06'], status='unreadable', active_minutes=1,
                           reason='Fixture leaves the unreadable case unresolved.')
    drop = run / 'A01'
    drop.mkdir(mode=0o700)
    source = drop / 'return.json'
    save_return(source, adjudicator, 'A01', decisions)
    sha = archive(source, vault, adjudicator, 'A01')
    final = finish(scored, vault)
    with check.assertRaises(FileExistsError):
        finish(scored, vault)
    check.assertEqual(read_json(scored / 'adjudication.json'), final)
    check.assertEqual(final['adjudication_sha256'], sha)
    check.assertEqual(final['minutes'], {'total': 3.75, 'recorded': 12, 'missing': 0})
    check.assertEqual(final['cases']['C02']['resolution'], 'resolved')
    check.assertEqual(final['cases']['C06']['resolution'], 'unresolved')
    check.assertEqual(final['original_sha256'], report['original_sha256'])
    return {
        'packet': report['packet'], 'C02': case['comparison'],
        'C06_dispositions': [r['disposition'] for r in empty['readers']],
        'C06_loss_xor_m2': empty['comparison']['loss_xor_m2'],
        'minutes': {**report['minutes'], 'A01': final['minutes']},
        'adjudication': {key: final['cases'][key]['resolution'] for key in ('C02', 'C06')},
        'reader_files': len(read_json(packet / 'owner-ledger.json')['files_sha256']),
    }


class ScoringChecks(unittest.TestCase):
    def setUp(self):
        self.item = dict(id='C01', size=244, core=context(244))

    def measure(self, a, b):
        return measure(self.item, [(r, validate_case(r, self.item, 'reader')) for r in (a, b)], 0.6)

    def test_clips_to_core_before_area_and_flags_crop(self):
        a = complete('C01', 0, loss=ring(0, 40, 32, 50), crown_2023=ring(0, 40, 32, 50))
        b = complete('C01', 1)
        measured = self.measure(a, b)
        self.assertEqual(measured['comparison']['loss_xor_m2'], 36)
        self.assertTrue(measured['readers'][0]['loss_crosses_core'])
        self.assertTrue(measured['readers'][0]['trace_touches_crop'])
        self.assertEqual(measured['readers'][0]['active_minutes'], 0)

    def test_empty_vs_missing_and_no_common_observation(self):
        empty = complete('C01', 1)
        a = complete('C01', 2, unknown_2023=ring(*self.item['core']))
        a['reason'] = 'Obscured.'
        comparison = self.measure(a, empty)['comparison']
        self.assertEqual(comparison['crown_iou'], {'2023': None, '2025': 1})
        self.assertEqual(comparison['unknown_xor_m2'], {'2023': 14400, '2025': 0, 'change': 0})
        self.assertIsNone(comparison['loss_common_known_xor_m2'])
        self.assertEqual(comparison['loss_xor_m2'], 0)
        missing = self.measure(dict(blank_case('C01'), status='skipped'), empty)
        self.assertIsNone(missing['comparison']['unknown_xor_m2']['2023'])

    def test_loss_with_no_support_from_own_crowns_flags_adjudication(self):
        trace = ring(40, 40, 50, 50)
        a = complete('C01', 1, crown_2025=trace, loss=trace)
        result = self.measure(a, a)
        self.assertIn('reader A loss conflicts with their crown traces', result['adjudication_reasons'])
        self.assertEqual(result['readers'][0]['visible_loss_m2'], 36)

    def test_persistent_crown_and_noncrown_cannot_jointly_support_loss(self):
        crown = ring(40, 40, 50, 50)
        a = complete('C01', 1, crown_2023=crown, crown_2025=crown, loss=ring(40, 40, 60, 50))
        result = self.measure(a, a)
        self.assertEqual(result['readers'][0]['traced_loss_m2'], 72)
        self.assertIn('reader A loss conflicts with their crown traces', result['adjudication_reasons'])

    def test_separate_inside_and_outside_events_do_not_cross_core(self):
        a = complete('C01', 1)
        a['masks']['loss'] = a['masks']['crown_2023'] = [ring(5, 5, 15, 15), ring(40, 40, 50, 50)]
        result = self.measure(a, a)
        self.assertFalse(result['readers'][0]['loss_crosses_core'])
        self.assertEqual(result['adjudication_reasons'], [])

    def test_transition_uncertainty_does_not_mask_either_epoch_crown(self):
        trace = ring(40, 40, 50, 50)
        a = complete('C01', 1, crown_2023=trace, unknown_change=trace)
        a['reason'] = 'Date-to-date displacement.'
        b = complete('C01', 1, crown_2023=trace, loss=trace)
        result = self.measure(a, b)
        self.assertEqual(result['comparison']['crown_iou']['2023'], 1)
        self.assertEqual(result['comparison']['loss_xor_m2'], 36)
        self.assertEqual(result['comparison']['loss_common_known_xor_m2'], 0)
        self.assertEqual(result['comparison']['unknown_xor_m2']['change'], 36)

    def test_touching_scoring_boundary_without_area_is_no_loss(self):
        a = complete('C01', 0, loss=ring(8, 40, 22, 50), crown_2023=ring(8, 40, 22, 50))
        result = self.measure(a, complete('C01', 1))['readers'][0]
        self.assertEqual(result['disposition'], 'no_loss')
        self.assertFalse(result['loss_crosses_core'])

    def test_rejects_invalid_coordinates_and_unreadable_with_geometry(self):
        a = complete('C01', 1, loss=ring(-1, 5, 20, 15))
        with self.assertRaisesRegex(ValueError, 'crop coordinates'):
            validate_case(a, self.item, 'reader')
        a['masks']['loss'] = [[[30, 30], [40, 40], [40, 30], [30, 40]]]
        with self.assertRaisesRegex(ValueError, 'self-crossing'):
            validate_case(a, self.item, 'reader')
        a['status'] = 'unreadable'
        a['masks']['loss'] = [ring(5, 5, 20, 15)]
        with self.assertRaisesRegex(ValueError, 'must leave traces'):
            validate_case(a, self.item, 'reader')

    def test_unstarted_case_requires_a_deliberate_disposition(self):
        with self.assertRaisesRegex(ValueError, 'Invalid status'):
            validate_case(blank_case('C01'), self.item, 'reader')

    def test_wrong_package_is_rejected_before_archive(self):
        assignment = dict(packet='expected', cases=[self.item])
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            source = vault / 'incoming.json'
            source.write_text(dump_json(dict(packet='unexpected', code='R01', role='reader',
                                             cases=[blank_case('C01')])))
            with self.assertRaisesRegex(ValueError, 'Wrong packet'):
                archive(source, vault, assignment, 'R01')
            self.assertFalse((vault / 'R01.json').exists())

    def test_nominal_downsampling_is_band_independent(self):
        values = np.array([[[0, 1, 200, 200], [0, 1, 200, 202]],
                           [[255, 255, 0, 0], [254, 252, 0, 1]]], dtype=np.uint8)
        np.testing.assert_array_equal(nominal_late(values), np.array([[[1, 201]], [[254, 0]]]))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(dump_json(replay(Path(sys.argv[1]), Path(sys.argv[2]))), end='')
    else:
        unittest.main()

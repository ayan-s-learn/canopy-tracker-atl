"""Archive independent T09 returns, score their agreement and prepare adjudication."""

import argparse
import math
import os
from pathlib import Path
import shutil
from stat import S_IMODE
from tempfile import TemporaryDirectory

from shapely import Polygon, box, union_all

from build_packet import LAYERS, YEARS, blank_case, digest, dump_json, file_hash, read_json, write_assignment

CODES = ('R01', 'R02', 'A01')
UNKNOWN = ('2023', '2025', 'change')


def validate(path, assignment, code):
    data = read_json(path)
    role = 'adjudicator' if code == 'A01' else 'reader'
    if not isinstance(data, dict) or (data.get('packet'), data.get('code'), data.get('role')) != (
            assignment['packet'], code, role):
        raise ValueError('Wrong packet, assigned code or role')
    cases = {item['id']: item for item in assignment['cases']}
    records = data.get('cases')
    if not isinstance(records, list) or len(records) != len(cases):
        raise ValueError('Expected exactly one record for each assigned case')
    validated = {}
    for record in records:
        key = record.get('id') if isinstance(record, dict) else None
        if not isinstance(key, str) or key not in cases or key in validated:
            raise ValueError('Unrecognized or repeated case')
        try:
            masks = validate_case(record, cases[key], role)
        except ValueError as error:
            raise ValueError(f'{key}: {error}') from error
        validated[key] = (record, masks)
    return validated


def validate_case(record, item, role):
    required = set(blank_case(item['id']))
    if role == 'adjudicator':
        required.add('resolution')
    if set(record) != required:
        raise ValueError('Record fields differ from the blank form')
    status = record['status']
    time = record['active_minutes']
    confidence = record['confidence']
    reason = record['reason']
    cutoff = record['crop_cutoff']
    if status not in ('complete', 'unreadable', 'skipped') or type(cutoff) is not bool or not isinstance(reason, str):
        raise ValueError('Invalid status, crop flag or reason')
    if time is not None and (type(time) not in (int, float) or not 0 <= time < math.inf):
        raise ValueError('Active minutes must be finite and nonnegative')
    layers = record['masks']
    if not isinstance(layers, dict) or set(layers) != set(LAYERS):
        raise ValueError('Each mask must be supplied, using [] for an empty mask')
    masks = {layer: polygons(shapes, item['size']) for layer, shapes in layers.items()}
    if status == 'complete':
        if time is None or confidence not in ('high', 'medium', 'low'):
            raise ValueError('A complete read needs confidence and active minutes')
    elif any(layers.values()) or confidence is not None or cutoff:
        raise ValueError('An unreadable or skipped return must leave traces, confidence and crop flag empty')
    if status == 'unreadable' and time is None:
        raise ValueError('An unreadable return needs active minutes')
    if (status == 'unreadable' or cutoff or any(layers[f'unknown_{period}'] for period in UNKNOWN)) and not reason.strip():
        raise ValueError('Describe unreadability, crop truncation or unknown geometry')
    if role == 'adjudicator':
        if record['resolution'] not in ('resolved', 'unresolved') or not reason.strip() or time is None:
            raise ValueError('Each disagreement needs resolution, rationale and active minutes')
        if record['resolution'] == 'resolved' and status != 'complete':
            raise ValueError('A resolved decision needs a completed reading')
    return masks


def polygons(shapes, size):
    if not isinstance(shapes, list):
        raise ValueError('Masks must be lists of polygon rings')
    parsed = []
    for points in shapes:
        if not isinstance(points, list) or len(points) < 3 or any(
                not isinstance(point, list) or len(point) != 2 or
                any(type(v) is not int or not 0 <= v <= size for v in point)
                for point in points):
            raise ValueError('Polygon vertices must be integer [column, row] crop coordinates')
        shape = Polygon(points)
        if not shape.is_valid or shape.area == 0:
            raise ValueError('A polygon is self-crossing or has zero area')
        parsed.append(shape)
    return union_all(parsed)


def archive(path, vault, assignment, code):
    if code not in CODES:
        raise ValueError('Unrecognized receipt slot')
    if vault.is_symlink() or S_IMODE(vault.stat().st_mode) & 0o077:
        raise ValueError('Use an owner-only vault directory (mode 700)')
    with TemporaryDirectory(dir=vault) as working:
        staged = Path(working) / f'{code}.json'
        staged.write_bytes(path.read_bytes())
        staged.chmod(0o600)
        validate(staged, assignment, code)
        (vault / staged.name).hardlink_to(staged)
    return file_hash(vault / staged.name)


def measure(item, readers, scale):
    def area(shape):
        return round(shape.area * scale ** 2, 6)

    core = box(*item['core'])
    crop = box(0, 0, item['size'], item['size'])
    details = []
    for record, masks in readers:
        result = {key: record[key] for key in ('status', 'active_minutes', 'confidence', 'reason', 'crop_cutoff')}
        result.update(disposition=record['status'], visible_loss_m2=None, traced_loss_m2=None,
                      unknown_m2=None, trace_touches_crop=None, loss_crosses_core=None)
        if record['status'] == 'complete':
            unknown = union_all([masks[f'unknown_{period}'] for period in UNKNOWN])
            loss = masks['loss'].intersection(core)
            visible = loss.difference(unknown)
            result.update(
                disposition=('visible_loss' if visible.area else
                             'no_visible_loss_with_unknown' if unknown.intersection(core).area else
                             'no_loss'),
                visible_loss_m2=area(visible), traced_loss_m2=area(loss),
                unknown_m2={period: area(masks[f'unknown_{period}'].intersection(core)) for period in UNKNOWN},
                trace_touches_crop=any(mask.intersects(crop.boundary) for mask in masks.values()),
                loss_crosses_core=(loss.area > 0 and masks['loss'].difference(core).area > 0),
            )
        details.append(result)

    comparison = dict(crown_iou={year: None for year in YEARS},
                      crown_common_known_m2={year: None for year in YEARS},
                      unknown_xor_m2={period: None for period in UNKNOWN},
                      loss_xor_m2=None, loss_common_known_xor_m2=None, loss_common_known_m2=None)
    if all(record['status'] == 'complete' for record, _ in readers):
        a, b = [masks for _, masks in readers]
        unknown_pairs = [a[f'unknown_{year}'].union(b[f'unknown_{year}']) for year in YEARS]
        for year, unknown in zip(YEARS, unknown_pairs, strict=True):
            known = core.difference(unknown)
            first = a[f'crown_{year}'].intersection(known)
            second = b[f'crown_{year}'].intersection(known)
            union = first.union(second).area
            comparison['crown_common_known_m2'][year] = area(known)
            if known.area:
                comparison['crown_iou'][year] = round(first.intersection(second).area / union, 9) if union else 1
            comparison['unknown_xor_m2'][year] = area(
                a[f'unknown_{year}'].symmetric_difference(b[f'unknown_{year}']).intersection(core))
        comparison['unknown_xor_m2']['change'] = area(
            a['unknown_change'].symmetric_difference(b['unknown_change']).intersection(core))
        known = core.difference(union_all(unknown_pairs + [a['unknown_change'], b['unknown_change']]))
        xor = a['loss'].symmetric_difference(b['loss']).intersection(core)
        comparison.update(loss_xor_m2=area(xor), loss_common_known_xor_m2=area(xor.intersection(known))
                          if known.area else None, loss_common_known_m2=area(known))

    # Keep disagreements in the supplied context even if their clipped score is identical.
    (_, a), (_, b) = readers
    reasons = []
    if any(record['status'] != 'complete' for record, _ in readers):
        reasons.append('incomplete read')
    if details[0]['disposition'] != details[1]['disposition']:
        reasons.append('disposition differs')
    if details[0]['crop_cutoff'] != details[1]['crop_cutoff']:
        reasons.append('crop flag differs')
    if any(detail['crop_cutoff'] or detail['trace_touches_crop'] for detail in details):
        reasons.append('possible crop truncation')
    if any(detail['confidence'] == 'low' for detail in details):
        reasons.append('low confidence')
    if any(not a[layer].equals(b[layer]) for layer in LAYERS):
        reasons.append('geometry differs')
    return dict(readers=details, comparison=comparison, adjudication_reasons=reasons)


def minutes(records):
    values = [record['active_minutes'] for record in records]
    present = [value for value in values if value is not None]
    return dict(total=sum(present), recorded=len(present), missing=len(values) - len(present))


def compare(packet, vault, output):
    ledger = read_json(packet / 'owner-ledger.json')
    assignment = ledger['assignment']
    for name, sha in ledger['files_sha256'].items():
        if file_hash(packet / 'reader' / name) != sha:
            raise ValueError(f'Reader packet file changed: {name}')
    codes = CODES[:2]
    paths = [vault / f'{code}.json' for code in codes]
    results = [validate(path, assignment, code) for path, code in zip(paths, codes, strict=True)]
    comparisons, originals, cases = {}, {}, []
    for item in assignment['cases']:
        key = item['id']
        readers = [reader[key] for reader in results]
        comparison = measure(item, readers, assignment['scale_m'])
        comparisons[key] = comparison
        if comparison['adjudication_reasons']:
            cases.append(item)
            originals[key] = [record for record, _ in readers]

    output.mkdir(mode=0o700)
    adjudication = output / 'adjudicator'
    adjudication.mkdir()
    for name in ('viewer.html', 'viewer.js', 'reader-guide.txt'):
        shutil.copyfile(packet / 'reader' / name, adjudication / name)
    for item in cases:
        for path in (packet / 'reader').glob(f"{item['id']}-*.png"):
            shutil.copyfile(path, adjudication / path.name)
    source_hashes = {code: file_hash(path) for code, path in zip(codes, paths, strict=True)}
    adjudication_id = digest(dump_json(dict(packet=assignment['packet'], originals=source_hashes)).encode())
    blank = dict(packet=adjudication_id, code='', role='adjudicator',
                 cases=[dict(blank_case(item['id']), resolution=None) for item in cases])
    adjudication_assignment = dict(packet=adjudication_id, scale_m=assignment['scale_m'],
                                   cases=cases, blank=blank, originals=originals,
                                   flags={item['id']: comparisons[item['id']]['adjudication_reasons']
                                          for item in cases})
    write_assignment(adjudication / 'assignment.js', adjudication_assignment)
    (adjudication / 'blank-return.json').write_text(dump_json(blank))
    (output / 'adjudication-state.json').write_text(dump_json(
        dict(packet=assignment['packet'], assignment=adjudication_assignment, original_sha256=source_hashes)))
    report = dict(packet=assignment['packet'], original_sha256=source_hashes, cases=comparisons,
                  minutes={code: minutes([record for record, _ in reader.values()])
                           for code, reader in zip(codes, results, strict=True)})
    (output / 'comparison.json').write_text(dump_json(report))
    return report


def finish(scored, vault):
    state = read_json(scored / 'adjudication-state.json')
    for code, sha in state['original_sha256'].items():
        if file_hash(vault / f'{code}.json') != sha:
            raise ValueError(f'Archived original changed: {code}')
    cases = state['assignment']['cases']
    source = vault / 'A01.json'
    adjudication = validate(source, state['assignment'], 'A01') if cases else {}
    report = dict(packet=state['packet'], adjudication_assignment=state['assignment']['packet'],
                  original_sha256=state['original_sha256'],
                  adjudication_sha256=file_hash(source) if cases else None,
                  minutes=minutes([record for record, _ in adjudication.values()]),
                  cases={key: record for key, (record, _) in adjudication.items()})
    with (scored / 'adjudication.json').open('x') as output:
        output.write(dump_json(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    receive = commands.add_parser('receive', help='Validate and preserve one original in a private slot')
    receive.add_argument('packet_or_comparison', type=Path)
    receive.add_argument('vault', type=Path)
    receive.add_argument('code', choices=CODES)
    receive.add_argument('return_path', type=Path)
    scoring = commands.add_parser('compare', help='Score originals and generate the adjudicator packet')
    scoring.add_argument('packet', type=Path)
    scoring.add_argument('vault', type=Path)
    scoring.add_argument('output', type=Path)
    finalize = commands.add_parser('finish', help='Verify and record the separate adjudication decisions')
    finalize.add_argument('comparison', type=Path)
    finalize.add_argument('vault', type=Path)
    args = parser.parse_args()
    os.umask(0o077)
    try:
        if args.command == 'receive':
            owner_file = 'adjudication-state.json' if args.code == 'A01' else 'owner-ledger.json'
            assignment = read_json(args.packet_or_comparison / owner_file)['assignment']
            args.vault.mkdir(mode=0o700, exist_ok=True)
            print(archive(args.return_path, args.vault, assignment, args.code))
        elif args.command == 'compare':
            report = compare(args.packet, args.vault, args.output)
            print(f"Compared {len(report['cases'])} cases")
        else:
            report = finish(args.comparison, args.vault)
            print(f"Recorded {len(report['cases'])} adjudication decisions")
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()

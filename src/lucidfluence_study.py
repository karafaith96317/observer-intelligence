"""Offline study importer and paced replay. Never grants execution authority."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def extract(text):
    """Extract complete outer JSON objects; retain duplicate occurrences and offsets."""
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        start = text.find('{', pos)
        if start < 0:
            return
        try:
            obj, size = decoder.raw_decode(text[start:])
        except ValueError:
            pos = start + 1
            continue
        if isinstance(obj, dict) and ('record_id' in obj or isinstance(obj.get('payload'), dict) and 'record_id' in obj['payload']):
            yield start, start + size, obj
        pos = start + size


def import_source(source, destination):
    raw = Path(source).read_bytes()
    text = raw.decode('utf-8')
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=True)
    (root / 'source.txt').write_bytes(raw)
    source_hash = hashlib.sha256(raw).hexdigest()
    previous = '0' * 64
    records = []
    seen = set()
    for start, end, original in extract(text):
        payload = original.get('payload', original)
        fingerprint = digest(original)
        record = {'sequence': len(records) + 1, 'previous_hash': previous,
                  'data_nature': 'SIMULATED', 'evidence_status': 'SPECULATIVE / UNVERIFIED',
                  'source_sha256': source_hash, 'source_character_range': [start, end],
                  'original_sha256': fingerprint, 'duplicate': fingerprint in seen,
                  'reported_record_id': payload['record_id'], 'original': original,
                  'anchor_status': 'NOT_ANCHORED', 'execution_permitted': False}
        record['hash'] = digest(record)
        previous = record['hash']
        seen.add(fingerprint)
        records.append(record)
    (root / 'records.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False, allow_nan=False) + '\n' for r in records))
    manifest = {'source_sha256': source_hash, 'source_bytes': len(raw), 'records': len(records),
                'unique_objects': len(seen), 'head_hash': previous, 'import_format': 1,
                'boundary': 'Conversation assertions and code are retained as source material, not verified deployments. Historical dates and hashes are unverified claims.'}
    (root / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    raw = (root / 'source.txt').read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    if source_hash != manifest['source_sha256'] or len(raw) != manifest['source_bytes']:
        raise ValueError('source mismatch')
    expected = []
    seen = set()
    previous = '0' * 64
    for line in (root / 'records.jsonl').read_text().splitlines():
        r = json.loads(line)
        h = r.pop('hash')
        if digest(r) != h or r['previous_hash'] != previous or r['sequence'] != len(expected) + 1:
            raise ValueError('chain mismatch')
        if r['data_nature'] != 'SIMULATED' or r['execution_permitted'] is not False or r['source_sha256'] != source_hash:
            raise ValueError('provenance mismatch')
        previous = h
        seen.add(r['original_sha256'])
        expected.append(r)
    extracted = list(extract(raw.decode('utf-8')))
    if len(expected) != len(extracted):
        raise ValueError('extraction count mismatch')
    for r, (start, end, obj) in zip(expected, extracted):
        if r['original'] != obj or r['source_character_range'] != [start, end] or r['original_sha256'] != digest(obj):
            raise ValueError('source binding mismatch')
    if len(expected) != manifest['records'] or len(seen) != manifest['unique_objects'] or previous != manifest['head_hash']:
        raise ValueError('manifest mismatch')
    return expected


def replay(root, limit=10, interval=1.0):
    if limit < 1 or not math.isfinite(interval) or interval < 0:
        raise ValueError('positive limit and finite nonnegative interval required')
    for index, record in enumerate(verify(root)[:limit]):
        if index:
            time.sleep(interval)
        yield {'replayed_at_utc_epoch': time.time(), 'mode': 'SIMULATED_REPLAY',
               'record_id': record['reported_record_id'], 'record_hash': digest(record),
               'tier_metrics': record['original'].get('payload', record['original']).get('tier_system_telemetry', {}),
               'execution_permitted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('import'); p.add_argument('source'); p.add_argument('destination')
    p = sub.add_parser('verify'); p.add_argument('dataset')
    p = sub.add_parser('replay'); p.add_argument('dataset'); p.add_argument('--limit', type=int, default=10); p.add_argument('--interval', type=float, default=1)
    args = parser.parse_args()
    if args.command == 'import':
        print(json.dumps(import_source(args.source, args.destination)))
    elif args.command == 'verify':
        print(json.dumps({'verified_records': len(verify(args.dataset))}))
    else:
        for event in replay(args.dataset, args.limit, args.interval):
            print(json.dumps(event), flush=True)


if __name__ == '__main__':
    main()

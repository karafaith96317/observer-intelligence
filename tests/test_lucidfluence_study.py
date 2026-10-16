import json
import tempfile
import unittest
from pathlib import Path
from src.lucidfluence_study import import_source, verify, replay


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'input.txt'
        self.source.write_text('notes\n' + json.dumps({'record_id': 'test'}))
        self.root = self.base / 'data'
        import_source(self.source, self.root)

    def test_roundtrip_boundary(self):
        self.assertEqual(len(verify(self.root)), 1)
        event = next(replay(self.root, interval=0))
        self.assertEqual(event['mode'], 'SIMULATED_REPLAY')
        self.assertIs(event['execution_permitted'], False)

    def test_source_tamper(self):
        (self.root / 'source.txt').write_text('changed')
        with self.assertRaises(ValueError): verify(self.root)

    def test_record_tamper(self):
        p = self.root / 'records.jsonl'
        obj = json.loads(p.read_text()); obj['data_nature'] = 'OBSERVED'
        p.write_text(json.dumps(obj))
        with self.assertRaises(ValueError): verify(self.root)

    def test_manifest_tamper(self):
        p = self.root / 'manifest.json'
        obj = json.loads(p.read_text()); obj['head_hash'] = 'forged'
        p.write_text(json.dumps(obj))
        with self.assertRaises(ValueError): verify(self.root)

    def test_truncation(self):
        (self.root / 'records.jsonl').write_text('')
        with self.assertRaises(ValueError): verify(self.root)

    def test_deterministic_import(self):
        other = self.base / 'other'
        import_source(self.source, other)
        self.assertEqual((other / 'records.jsonl').read_bytes(), (self.root / 'records.jsonl').read_bytes())

    def test_invalid_pacing(self):
        with self.assertRaises(ValueError): list(replay(self.root, interval=float('nan')))


if __name__ == '__main__': unittest.main()

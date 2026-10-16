import json
import tempfile
import unittest
from src.oi_monitor import Monitor, request


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.head = 'a'
        self.down = False
        self.delivery_fail = False
        self.sent = []
        def fetch(url, token=None, body=None):
            if body:
                if self.delivery_fail: raise OSError('secret URL should not be logged')
                self.sent.append(json.loads(body)); return b'OK'
            if '/branches/' in url:
                if self.down: raise OSError('offline')
                return json.dumps({'commit': {'sha': self.head}}).encode()
            return json.dumps({'workflow_runs': [{'id': 1, 'conclusion': 'failure', 'run_attempt': 1}]}).encode()
        self.fetch = fetch
        self.monitor = Monitor({'repository': 'test/repo'}, self.tmp.name, fetch)
        self.addCleanup(lambda: self.monitor.db.close())

    def test_baseline_change_and_dedup(self):
        self.monitor.poll()
        self.head = 'b'; self.monitor.poll(); self.monitor.poll()
        rows = self.monitor.db.execute('SELECT payload FROM alerts').fetchall()
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(json.loads(r[0])['execution_permitted'] is False for r in rows))

    def test_error_dedup_and_recovery(self):
        self.down = True; self.monitor.poll(); self.monitor.poll()
        self.down = False; self.monitor.poll()
        kinds = [json.loads(r[0])['kind'] for r in self.monitor.db.execute('SELECT payload FROM alerts')]
        self.assertEqual(kinds.count('collector_error'), 1)
        self.assertEqual(kinds.count('collector_recovered'), 1)

    def test_restart_persists(self):
        self.monitor.poll()
        second = Monitor({'repository': 'test/repo'}, self.tmp.name, self.fetch)
        try:
            second.poll()
            self.assertEqual(second.db.execute('SELECT count(*) FROM alerts').fetchone()[0], 1)
        finally: second.db.close()

    def test_delivery_retry(self):
        from unittest.mock import patch
        with patch.dict('os.environ', {'OI_ALERT_WEBHOOK': 'https://example.org/hook'}):
            self.delivery_fail = True; self.monitor.poll()
            self.assertEqual(self.monitor.db.execute('SELECT delivered FROM alerts').fetchone()[0], 0)
            self.delivery_fail = False; self.monitor.poll()
            self.assertEqual(len(self.sent), 1)
            self.assertEqual(self.monitor.db.execute('SELECT delivered FROM alerts').fetchone()[0], 1)

    def test_health_failure_is_not_healthy(self):
        self.monitor.config['health_url'] = 'https://health.example/status'
        original = self.monitor.fetch
        def fetch(url, **kw):
            if url.startswith('https://health.example'): raise OSError('down')
            return original(url, **kw)
        self.monitor.fetch = fetch
        self.monitor.poll()
        self.assertEqual(self.monitor.state('health:error'), 'yes')

    def test_coverage_gap(self):
        self.monitor.state('workflow_marker', 'old')
        def fetch(url, **kw):
            return json.dumps({'workflow_runs': [{'id': n, 'conclusion': 'success'} for n in range(100)]}).encode()
        self.monitor.fetch = fetch
        with self.monitor.db: self.monitor.workflows()
        row = self.monitor.db.execute('SELECT payload FROM alerts').fetchone()
        self.assertEqual(json.loads(row[0])['kind'], 'coverage_gap')

    def test_transport_guards(self):
        with self.assertRaises(ValueError): request('http://example.org')
        with self.assertRaises(ValueError): request('https://example.org', token='test')

    def test_raw_evidence_saved(self):
        self.monitor.poll()
        row = self.monitor.db.execute('SELECT raw,sha256,nature FROM observations LIMIT 1').fetchone()
        import hashlib
        self.assertEqual(hashlib.sha256(row[0]).hexdigest(), row[1])
        self.assertEqual(row[2], 'OBSERVED_API_RESPONSE')


if __name__ == '__main__': unittest.main()

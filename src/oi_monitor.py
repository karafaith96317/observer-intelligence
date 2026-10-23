"""Read-only polling monitor. API observations are not judgments of malicious intent."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import sqlite3
import threading
import time
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, token=None, body=None):
    if urlsplit(url).scheme != 'https':
        raise ValueError('HTTPS required')
    headers = {'User-Agent': 'OI-Monitor/0.1', 'Accept': 'application/vnd.github+json'}
    if token:
        if urlsplit(url).hostname != 'api.github.com':
            raise ValueError('GitHub credentials restricted to api.github.com')
        headers['Authorization'] = 'Bearer ' + token
    if body is not None:
        headers['Content-Type'] = 'application/json'
    with build_opener(NoRedirect()).open(Request(url, data=body, headers=headers), timeout=15) as response:
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError('response too large')
        return raw


class Monitor:
    def __init__(self, config, directory, fetch=request):
        self.config, self.fetch = config, fetch
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', config['repository']):
            raise ValueError('repository must be owner/name')
        for key in ('health_url',):
            if config.get(key) and urlsplit(config[key]).scheme != 'https':
                raise ValueError('HTTPS required')
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = sqlite3.connect(directory / 'monitor.sqlite3')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE IF NOT EXISTS observations (id INTEGER PRIMARY KEY, captured REAL, source TEXT, raw BLOB, sha256 TEXT, nature TEXT);
            CREATE TABLE IF NOT EXISTS alerts (key TEXT PRIMARY KEY, payload TEXT, delivered INTEGER DEFAULT 0);''')
        self.db.commit()

    def state(self, key, value=None):
        if value is None:
            row = self.db.execute('SELECT value FROM state WHERE key=?', (key,)).fetchone()
            return row[0] if row else None
        self.db.execute('INSERT OR REPLACE INTO state VALUES (?,?)', (key, value))

    def observe(self, url, raw):
        self.db.execute('INSERT INTO observations(captured,source,raw,sha256,nature) VALUES (?,?,?,?,?)',
                        (time.time(), url, raw, hashlib.sha256(raw).hexdigest(), 'OBSERVED_API_RESPONSE'))

    def alert(self, key, kind, detail):
        payload = json.dumps({'alert_id': key, 'kind': kind, 'detail': detail,
                              'captured_at_epoch': time.time(), 'execution_permitted': False})
        self.db.execute('INSERT OR IGNORE INTO alerts(key,payload) VALUES (?,?)', (key, payload))

    def check(self, name, fn):
        try:
            with self.db:
                fn()
                if self.state(name + ':error') == 'yes':
                    self.alert(name + ':recovery:' + str(time.time_ns()), 'collector_recovered', name)
                self.state(name + ':error', 'no')
        except Exception as exc:
            # Avoid logging URL-bearing exceptions, response bodies, or credentials.
            with self.db:
                if self.state(name + ':error') != 'yes':
                    self.alert(name + ':error:' + str(time.time_ns()), 'collector_error', {'collector': name, 'error_type': type(exc).__name__})
                self.state(name + ':error', 'yes')

    def github_head(self):
        base = 'https://api.github.com/repos/' + self.config['repository']
        branch = quote(self.config.get('branch', 'main'), safe='')
        url = base + '/branches/' + branch
        raw = self.fetch(url, token=os.getenv('GITHUB_TOKEN'))
        head = json.loads(raw)['commit']['sha']
        self.observe(url, raw)
        old = self.state('head')
        if old and old != head:
            self.alert('head:' + head, 'branch_head_changed', {'previous': old, 'current': head})
        self.state('head', head)

    def workflows(self):
        # Bounded recent window: gaps are explicit, not silently described as full coverage.
        url = 'https://api.github.com/repos/' + self.config['repository'] + '/actions/runs?per_page=100'
        raw = self.fetch(url, token=os.getenv('GITHUB_TOKEN'))
        data = json.loads(raw)
        self.observe(url, raw)
        runs = data['workflow_runs']
        previous = self.state('workflow_marker')
        marker = str(runs[0]['id']) if runs else ''
        if previous and previous not in {str(r['id']) for r in runs} and len(runs) == 100:
            self.alert('gap:' + marker, 'coverage_gap', 'Previous newest workflow is outside the latest 100 runs; inspect GitHub history.')
        for run in runs:
            if run.get('conclusion') in ('failure', 'timed_out', 'action_required'):
                key = 'run:' + str(run['id']) + ':' + str(run.get('run_attempt', 1)) + ':' + run['conclusion']
                self.alert(key, 'workflow_attention', {'id': run['id'], 'conclusion': run['conclusion'], 'name': run.get('name')})
        self.state('workflow_marker', marker)

    def health(self):
        url = self.config.get('health_url')
        if not url:
            return
        raw = self.fetch(url)
        self.observe(url, raw)
        # Any successful 2xx response establishes reachability only.

    def deliver(self):
        webhook = os.getenv('OI_ALERT_WEBHOOK')
        for key, payload in self.db.execute('SELECT key,payload FROM alerts WHERE delivered=0').fetchall():
            if webhook:
                try:
                    self.fetch(webhook, body=payload.encode())
                except Exception as exc:
                    print(json.dumps({'notification_delivery': 'failed', 'error_type': type(exc).__name__}), flush=True)
                    break
            else:
                print(payload, flush=True)
            with self.db:
                self.db.execute('UPDATE alerts SET delivered=1 WHERE key=?', (key,))

    def poll(self):
        for name, fn in [('github', self.github_head), ('workflows', self.workflows), ('health', self.health)]:
            self.check(name, fn)
        with self.db:
            self.state('last_poll_epoch', str(time.time()))
        self.deliver()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True)
    p.add_argument('--state-dir', required=True)
    p.add_argument('--once', action='store_true')
    args = p.parse_args()
    config = json.loads(Path(args.config).read_text())
    interval = config.get('interval_seconds', 300)
    if type(interval) is not int or interval < 30:
        p.error('interval_seconds must be an integer >= 30')
    monitor = Monitor(config, args.state_dir)
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    try:
        while not stop.is_set():
            monitor.poll()
            if args.once:
                break
            stop.wait(interval)
    finally:
        monitor.db.close()


if __name__ == '__main__':
    main()

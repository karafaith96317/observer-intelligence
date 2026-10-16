# Continuous OI monitoring

Experimental read-only collector; no actuation or threat attribution. Uses Python 3.10+ standard library. Source observations and alerts are stored separately from the LucidFluence simulation dataset. Kara Faith Sypen: project originator; OpenAI ChatGPT: implementation assistance.

## What is implemented

Every 300 seconds by default: poll a configured GitHub branch head, inspect the latest 100 workflow runs, and optionally request an HTTPS health endpoint. Successful API responses are stored as raw bytes with SHA-256, source URL, local capture time, and OBSERVED_API_RESPONSE status. This establishes what the API returned, not independent truth about attacks or people. A changed head reports previous/current SHA; it does not enumerate every intervening commit or changed file.

The first head establishes a baseline. Existing failed runs in the recent window alert on the first poll. Workflow alerts deduplicate by run, attempt, and conclusion. A collector failure alerts once per outage and recovery alerts once. HTTP errors, including rate limits, are collector failures, never interpreted as healthy. The process continues polling the other collectors. A configured health URL is considered reachable for a successful 2xx response; semantic health-body checks are not implemented.

Alerts are saved transactionally in SQLite. Without a webhook they print as JSON to stdout/journald. With OI_ALERT_WEBHOOK they POST generic JSON to your configured HTTPS receiver. This is not a Discord/Slack-specific payload. Failed delivery stays pending for the next poll. Delivery is at-least-once: a crash after receipt can resend; receivers should deduplicate alert_id. Configure the destination before starting if you want remote delivery of initial alerts. Historical stdout-delivered alerts are not automatically resent after enabling a webhook.

## Test a single poll from the repository root

```bash
python3 src/oi_monitor.py --config deploy/oi-monitor.example.json --state-dir /tmp/oi-monitor-test --once
```

For public GitHub data a token is optional. If needed, provide GITHUB_TOKEN through the host environment, with repository Contents read and Actions read access. Do not paste credentials into Git, the JSON config, or chat. GitHub connector credentials are not automatically available to the deployed Python program.

## Install on an always-on Debian/Ubuntu server with systemd

Put this repository's monitoring branch or merged code at `/opt/observer-intelligence`. Keep code root-owned and readable by the service. Then:

```bash
sudo install -d -m 755 /etc/oi-monitor
sudo install -m 644 /opt/observer-intelligence/deploy/oi-monitor.example.json /etc/oi-monitor/config.json
sudo install -m 644 /opt/observer-intelligence/deploy/oi-monitor.service /etc/systemd/system/oi-monitor.service
sudo systemctl daemon-reload
sudo systemctl enable --now oi-monitor
sudo systemctl status oi-monitor
sudo journalctl -u oi-monitor -n 50 --no-pager
```

Edit `/etc/oi-monitor/config.json` to choose branch, polling interval (integer >=30), and an optional HTTPS `health_url` that you control. Leave health_url null until an actual OI service endpoint exists. Do not use credential-bearing health URLs: source URLs and raw health responses are saved locally.

For remote alerts, create `/etc/oi-monitor/secrets.env` with `sudoedit`, restrict it with `sudo chmod 600 /etc/oi-monitor/secrets.env`, and enter the environment variables you need:

```text
GITHUB_TOKEN=your_read_only_token
OI_ALERT_WEBHOOK=https://your-controlled-receiver.example/oi
```

Restart after changes: `sudo systemctl restart oi-monitor`. Stop with `sudo systemctl disable --now oi-monitor`. Only configure webhooks you authorize to receive repository metadata and alerts. The monitor rejects HTTP and does not follow redirects, preventing credential forwarding on redirects. Webhook access tokens in the URL remain in the private environment file, not observation records.

## Operational limits

This is periodic polling, not instantaneous detection. Requests have a 15-second timeout, so cadence includes request duration. During network/API outages coverage is unavailable. Only 100 recent workflow runs are scanned per poll; if a previous marker falls outside a full window, a coverage_gap alert requests manual review. No workflows can legitimately mean an empty list. Private resources require host-side permission. Switching monitored repository/branch requires a new state directory to avoid mixing baselines.

SQLite stores last_poll_epoch for local inspection; it updates after collectors are attempted, so check collector error alerts as well. systemd restarts a crashed process but cannot alert remotely if the entire host/network is down. Use a separately hosted dead-man/heartbeat service for that requirement; none is configured by this code. There is no continuous process running merely because this code is committed.

The database grows with polling; arrange retention, disk monitoring, and backups before long-term deployment. It is not immutable or externally anchored. No intrusion-log ingestion, dependency/security-alert API, full commit/file diff, automated blocking, biometric collection, resonance measurement, or email/SMS provider integration is included. No local log or secret is pushed to GitHub by the monitor.

## Validation

```bash
python3 -m unittest discover -s tests -p test_oi_monitor.py -v
```

Offline tests cover baseline changes, deduplication, outage/recovery, restart persistence, failed webhook retry, transport credential boundaries, and raw response hashing. Use `--once` on the deployment host to verify its actual network and permissions before enabling continuous operation.

API references: https://docs.github.com/en/rest/actions/workflow-runs and https://docs.github.com/en/rest/branches/branches

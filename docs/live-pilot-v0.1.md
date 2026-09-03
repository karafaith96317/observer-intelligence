# OI Live Pilot v0.1

This is a local, dry-run-only Observer Intelligence pilot. It records a real user-supplied observation and decision run while executing no external action.

```bash
python scripts/run_live_pilot.py \
  --claim "The proposed action has sufficient evidence for a dry run" \
  --source "local://manual-observation" \
  --observation "Describe what was directly observed"
```

Records are stored locally under `.oi-live-state/` and classified `OBSERVED_TEST_RUN`. This means the software run occurred; it does not establish that the observation's interpretation is true. The state directory is intentionally not committed because it may contain sensitive inputs.

Run acceptance tests with `python -m unittest -v tests.test_live_pilot`.

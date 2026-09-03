#!/usr/bin/env python3
"""Create one real, local, non-executing OI decision record."""
import argparse, json, secrets, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from src.oi_live_pilot import Evidence, Ledger, NonceStore, authorize, reconcile, sign_token, token_payload

p = argparse.ArgumentParser()
p.add_argument("--claim", required=True); p.add_argument("--source", required=True); p.add_argument("--observation", required=True)
p.add_argument("--state-dir", default=".oi-live-state")
args = p.parse_args(); state = Path(args.state_dir); state.mkdir(parents=True, exist_ok=True)
e = Evidence("OBS-" + secrets.token_hex(4), args.source, datetime.now(timezone.utc).isoformat(), args.observation)
claim_id = "CLAIM-" + secrets.token_hex(4); rec = reconcile(claim_id, [e], [])
private = Ed25519PrivateKey.generate(); payload = token_payload(claim_id, "scope:pilot:dry-run", "local-pilot", secrets.token_hex(16),
                                                                datetime.now(timezone.utc).timestamp() + 300, [e.content_hash])
decision = authorize(rec, payload, sign_token(private, payload), private.public_key(), NonceStore(state / "nonces.sqlite3"),
                     "scope:pilot:dry-run", "local-pilot")
record = {"record_type": "OI_LIVE_PILOT_DECISION", "epistemic_classification": "OBSERVED_TEST_RUN",
          "recorded_at_utc": datetime.now(timezone.utc).isoformat(), "claim_text": args.claim,
          "evidence": {**e.__dict__, "content_hash": e.content_hash}, "reconciliation": rec, "decision": decision,
          "notice": "Dry-run only. No external action was executed."}
ledger = Ledger(state / "ledger.jsonl"); block = ledger.append(record)
print(json.dumps({"decision": decision["decision"], "block_hash": block["block_hash"], "ledger_valid": ledger.verify(), "record": record}, indent=2))

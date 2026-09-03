"""Observer Intelligence live pilot: provenance-first, dry-run only."""
from __future__ import annotations

import base64, hashlib, json, sqlite3, time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source_uri: str
    captured_at_utc: str
    payload: str
    classification: str = "OBSERVED_TEST_RUN"

    @property
    def content_hash(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class Challenge:
    observer_id: str
    target_claim_id: str
    findings: str
    counterevidence_hashes: tuple[str, ...]
    isolated_input_hashes: tuple[str, ...]


class NonceStore:
    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS consumed (nonce TEXT PRIMARY KEY, used_at REAL NOT NULL)")
        self.db.commit()

    def consume(self, nonce: str) -> bool:
        try:
            self.db.execute("INSERT INTO consumed VALUES (?, ?)", (nonce, time.time()))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False


class Ledger:
    def __init__(self, path: Path): self.path = path
    def read(self) -> list[dict]:
        if not self.path.exists(): return []
        return [json.loads(x) for x in self.path.read_text().splitlines() if x.strip()]
    def append(self, payload: dict) -> dict:
        blocks = self.read(); prev = blocks[-1]["block_hash"] if blocks else "0" * 64
        envelope = {"sequence": len(blocks) + 1, "previous_hash": prev, "payload": payload}
        block = {**envelope, "block_hash": digest(envelope)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f: f.write(json.dumps(block, sort_keys=True) + "\n")
        return block
    def verify(self) -> bool:
        prev = "0" * 64
        for i, block in enumerate(self.read(), 1):
            envelope = {"sequence": block["sequence"], "previous_hash": block["previous_hash"], "payload": block["payload"]}
            if block["sequence"] != i or block["previous_hash"] != prev or block["block_hash"] != digest(envelope): return False
            prev = block["block_hash"]
        return True


def token_payload(claim_id: str, scope: str, resource: str, nonce: str, expires: float, evidence_hashes: list[str]) -> dict:
    return {"claim_id": claim_id, "scope": scope, "resource": resource, "nonce": nonce,
            "expires": expires, "evidence_hashes": sorted(evidence_hashes)}


def sign_token(private_key: Ed25519PrivateKey, payload: dict) -> str:
    return base64.b64encode(private_key.sign(canonical(payload))).decode()


def verify_token(public_key: Ed25519PublicKey, payload: dict, signature: str) -> bool:
    try:
        public_key.verify(base64.b64decode(signature), canonical(payload)); return True
    except (InvalidSignature, ValueError): return False


def reconcile(claim_id: str, evidence: list[Evidence], challenges: list[Challenge]) -> dict:
    store = {e.content_hash for e in evidence}
    valid, rejected = [], []
    for c in challenges:
        reason = None
        if c.target_claim_id != claim_id: reason = "wrong_target"
        elif not c.counterevidence_hashes: reason = "no_counterevidence"
        elif not set(c.counterevidence_hashes).issubset(store): reason = "unknown_counterevidence"
        elif not set(c.counterevidence_hashes).issubset(set(c.isolated_input_hashes)): reason = "isolation_manifest_breach"
        (rejected if reason else valid).append({"observer_id": c.observer_id, **({"reason": reason} if reason else {"findings": c.findings})})
    state = "CONTESTED" if valid else ("SUPPORTED" if evidence else "UNRESOLVED")
    return {"claim_id": claim_id, "state": state, "evidence_hashes": sorted(store), "valid_challenges": valid, "rejected_challenges": rejected}


def authorize(rec: dict, payload: dict, signature: str, public_key: Ed25519PublicKey, nonces: NonceStore,
              required_scope: str, resource: str, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    checks = {"signature_valid": verify_token(public_key, payload, signature),
              "claim_bound": payload["claim_id"] == rec["claim_id"], "scope_exact": payload["scope"] == required_scope,
              "resource_exact": payload["resource"] == resource, "not_expired": now <= payload["expires"],
              "evidence_bound": payload["evidence_hashes"] == rec["evidence_hashes"], "state_supported": rec["state"] == "SUPPORTED"}
    allowed = all(checks.values()) and nonces.consume(payload["nonce"])
    checks["nonce_fresh"] = allowed or False
    return {"decision": "ALLOW_DRY_RUN" if allowed else "DENY", "checks": checks, "execution_attempted": False}

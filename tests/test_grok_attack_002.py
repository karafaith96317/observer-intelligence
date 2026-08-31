"""
GROK-ATTACK-002 falsification suite against GEM-IMPL-001 baseline.

These tests document CURRENT vulnerable behavior of src/oi_runtime_v0_1.py.
They ASSERT the unsafe outcome so regressions in the attack surface are visible.

GEM-IMPL-002 should change the runtime so the safe outcomes hold; at that point
these tests should be inverted or replaced with hardened expectations.

Baseline: GPT-SPEC-002 / 06dd476ae25ede01a87a6c085c9f4fd28285c1f5
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from src.oi_runtime_v0_1 import (
    OIRuntimeEngine,
    ObservationRecord,
    AuthorityToken,
    AuthorityScope,
    EvidenceState,
)

SECRET_KEY = b"kfs_runtime_test_secret_key_32_bytes!!"
ROOT_ISSUER = "ed25519_pk_root_governance_node_01"


@pytest.fixture
def engine():
    return OIRuntimeEngine(secret_key=SECRET_KEY, authorized_issuers={ROOT_ISSUER})


def test_soft_sybil_upstream_contamination_authorizes(engine):
    """
    GROK-ATTACK-002-A: Three distinct hashes, shared upstream false claim.
    Current runtime treats them as independent → SUPPORTED → EXECUTE permitted.
    """
    # Cosmetic diversity; same contaminated conclusion
    o1 = ObservationRecord.create("agent-a", "agent://a/report", "NODE_HEALTHY upstream=X")
    o2 = ObservationRecord.create("agent-b", "agent://b/report", "NODE_HEALTHY upstream=X ")
    o3 = ObservationRecord.create("agent-c", "agent://c/report", "NODE_HEALTHY upstream=X  ")
    assert len({o1.content_hash, o2.content_hash, o3.content_hash}) == 3

    for o in (o1, o2, o3):
        engine.ingest_observation(o)

    rec = engine.reconcile(
        target_claim="PROP-MIGRATE: node healthy for failover",
        primary_evidence_hashes=[o1.content_hash, o2.content_hash, o3.content_hash],
        shadow_evals=[],
    )

    assert rec.epistemic_state == EvidenceState.SUPPORTED
    assert rec.completeness_score == 1.0

    token = AuthorityToken.issue(
        token_id="TOK-SYBIL",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.EXECUTE_MIGRATION,
        resource="cluster-04",
        ttl_sec=60.0,
        nonce="nonce-sybil-001",
        evidence_hashes=[o1.content_hash, o2.content_hash, o3.content_hash],
    )
    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )

    # Vulnerable baseline: soft Sybil authorizes
    assert auth.execution_permitted is True


def test_toctou_drop_unbound_primary_evidence_still_authorizes(engine):
    """
    GROK-ATTACK-002-B: Reconcile on [H_support, H_critical]; token binds only H_support;
    delete H_critical; authorization still succeeds because snapshot stays SUPPORTED
    and only bound hashes are re-checked.
    """
    h_support = ObservationRecord.create("s1", "telemetry://ok", "support-signal")
    h_critical = ObservationRecord.create("s2", "kernel://check", "critical-grounding")
    engine.ingest_observation(h_support)
    engine.ingest_observation(h_critical)

    rec = engine.reconcile(
        target_claim="PROP-MIGRATE: grounded healthy",
        primary_evidence_hashes=[h_support.content_hash, h_critical.content_hash],
        shadow_evals=[],
    )
    assert rec.epistemic_state == EvidenceState.SUPPORTED
    assert rec.completeness_score == 1.0

    token = AuthorityToken.issue(
        token_id="TOK-TOCTOU",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.EXECUTE_MIGRATION,
        resource="node-01",
        ttl_sec=60.0,
        nonce="nonce-toctou-001",
        evidence_hashes=[h_support.content_hash],  # critical not bound
    )

    # Mutate world after mint
    del engine.evidence_store[h_critical.content_hash]

    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )

    # Vulnerable baseline: still authorizes
    assert auth.execution_permitted is True
    assert auth.revalidation_log["bound_evidence_unmodified"] is True


def test_completeness_gaming_irrelevant_evidence_authorizes(engine):
    """
    GROK-ATTACK-002-C: Primary hash list is only irrelevant noise; completeness 1.0;
    EXECUTE still permitted.
    """
    noise = [
        ObservationRecord.create(f"n{i}", f"noise://{i}", f"irrelevant-{i}")
        for i in range(5)
    ]
    for o in noise:
        engine.ingest_observation(o)

    hashes = [o.content_hash for o in noise]
    rec = engine.reconcile(
        target_claim="PROP-MIGRATE: critical failover authorized",
        primary_evidence_hashes=hashes,
        shadow_evals=[],
    )

    assert rec.completeness_score == 1.0
    assert rec.epistemic_state == EvidenceState.SUPPORTED

    token = AuthorityToken.issue(
        token_id="TOK-GAME",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.EXECUTE_MIGRATION,
        resource="cluster-04",
        ttl_sec=60.0,
        nonce="nonce-game-001",
        evidence_hashes=hashes,
    )
    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )

    # Vulnerable baseline: noise is enough
    assert auth.execution_permitted is True

"""
Unit & Adversarial Validation Suite for OI Runtime v0.1 / v0.1.1
Tests compliance against GROK-SCHEMA-001 protections + GEM-IMPL-002 gates.

Contribution: GEM-IMPL-001 / GEM-IMPL-002
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
    ShadowEvaluation,
    AuthorityScope,
    EvidenceState,
)

SECRET_KEY = b"kfs_runtime_test_secret_key_32_bytes!!"
ROOT_ISSUER = "ed25519_pk_root_governance_node_01"


@pytest.fixture
def engine():
    return OIRuntimeEngine(secret_key=SECRET_KEY, authorized_issuers={ROOT_ISSUER})


def test_t02b_adversarial_shadow_refutation(engine):
    """
    Shadow provides valid kernel fault proof.
    Reconciliation MUST mark target as CONTESTED; execution MUST be DENIED.
    """
    obs_primary = ObservationRecord.create("OBS-01", "telemetry://ping", "Latency 11.2ms")
    obs_fault = ObservationRecord.create(
        "OBS-02", "kernel://socket", "Buffer overflow in listener"
    )
    engine.ingest_observation(obs_primary)
    engine.ingest_observation(obs_fault)

    shadow = ShadowEvaluation(
        evaluation_id="SHAD-01",
        target_proposition_id="PROP-MIGRATE",
        shadow_observer_id="OBS-SHADOW",
        isolated_input_hashes=[obs_fault.content_hash],
        findings="Critical buffer drop contradicts high-availability assertion",
        counterevidence_hashes=[obs_fault.content_hash],
        correlation_with_primary=0.0,
        challenge_succeeded=True,
    )

    rec = engine.reconcile(
        target_claim="PROP-MIGRATE: Node is healthy for immediate failover",
        primary_evidence_hashes=[obs_primary.content_hash],
        shadow_evals=[shadow],
    )

    assert rec.epistemic_state == EvidenceState.CONTESTED
    assert len(rec.retained_disagreements) >= 1
    assert rec.completeness_score == 1.0

    token = AuthorityToken.issue(
        token_id="TOK-01",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.EXECUTE_MIGRATION,
        resource="cluster-04",
        ttl_sec=60.0,
        nonce="nonce-t02b-001",
        evidence_hashes=[obs_primary.content_hash],
    )

    auth = engine.evaluate_action_authorization(
        reconciliation_id=rec.reconciliation_id,
        token=token,
        required_scope=AuthorityScope.EXECUTE_MIGRATION,
    )

    assert auth.execution_permitted is False
    assert auth.revalidation_log["evidence_state_supported"] is False


def test_authority_replay_protection(engine):
    """Verifies that an identical token nonce cannot be re-executed."""
    obs = ObservationRecord.create(
        "OBS-01", "telemetry://status", "status all green healthy"
    )
    engine.ingest_observation(obs)

    rec = engine.reconcile(
        "status all green healthy for failover",
        [obs.content_hash],
        [],
    )
    assert rec.epistemic_state == EvidenceState.SUPPORTED

    token = AuthorityToken.issue(
        token_id="TOK-REPLAY",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.EXECUTE_MIGRATION,
        resource="node-01",
        ttl_sec=60.0,
        nonce="nonce-unique-12345",
        evidence_hashes=[obs.content_hash],
    )

    auth1 = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )
    assert auth1.execution_permitted is True

    auth2 = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )
    assert auth2.execution_permitted is False
    assert auth2.revalidation_log["nonce_unconsumed"] is False


def test_scope_escalation_trap(engine):
    """Token scoped for INFER cannot trigger EXECUTE_MIGRATION."""
    obs = ObservationRecord.create(
        "OBS-01", "telemetry://status", "status all green healthy"
    )
    engine.ingest_observation(obs)
    rec = engine.reconcile(
        "status all green healthy for failover",
        [obs.content_hash],
        [],
    )

    token = AuthorityToken.issue(
        token_id="TOK-INFER-ONLY",
        secret_key=SECRET_KEY,
        issuer_pk=ROOT_ISSUER,
        scope=AuthorityScope.INFER,
        resource="node-01",
        ttl_sec=60.0,
        nonce="nonce-scope-999",
        evidence_hashes=[obs.content_hash],
    )

    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )
    assert auth.execution_permitted is False
    assert auth.revalidation_log["scope_exact_match"] is False

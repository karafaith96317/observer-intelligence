"""GROK-ATTACK-002 containment tests for GEM-IMPL-002.

These tests assert safe outcomes for the three confirmed attack classes and
include regression cases for the two subtle bypasses identified during
architecture review: cherry-picked token binding and wrong-claim grounding.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from src.oi_runtime_v0_2 import (
    AuthorityScope,
    AuthorityToken,
    EvidenceGroundingLink,
    EvidenceState,
    GroundingRelationType,
    OIRuntimeEngineV2,
    ObservationRecord,
)

SECRET_KEY = b"kfs_runtime_test_secret_key_32_bytes!!"
ROOT_ISSUER = "ed25519_pk_root_governance_node_01"
CLAIM_ID = "PROP-MIGRATE-04"
CLAIM = "Cluster 04 is safe for migration"


@pytest.fixture
def engine():
    return OIRuntimeEngineV2(secret_key=SECRET_KEY, authorized_issuers={ROOT_ISSUER})


def support_link(obs, claim_id=CLAIM_ID):
    return EvidenceGroundingLink(
        obs.content_hash,
        claim_id,
        GroundingRelationType.SUPPORTS,
        "Explicit claim-specific development-fixture grounding",
    )


def mint(engine, rec, hashes, token_id, nonce):
    return AuthorityToken.issue(
        token_id,
        SECRET_KEY,
        ROOT_ISSUER,
        AuthorityScope.EXECUTE_MIGRATION,
        "cluster-04",
        60.0,
        nonce,
        rec.reconciliation_snapshot_hash,
        hashes,
    )


def test_vector_a_shared_upstream_is_contained(engine):
    observations = [
        ObservationRecord.create("OBS-01", "feed://sensorA", "upstream://vendor-X", "Node healthy"),
        ObservationRecord.create("OBS-02", "feed://sensorB", "upstream://vendor-X", "Throughput nominal"),
        ObservationRecord.create("OBS-03", "feed://sensorC", "upstream://vendor-X", "Latency nominal"),
    ]
    for obs in observations:
        engine.ingest_observation(obs)

    hashes = [o.content_hash for o in observations]
    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, [support_link(o) for o in observations], [])

    assert rec.epistemic_state == EvidenceState.UNRESOLVED
    assert rec.dependence_status == "shared_upstream"
    assert any("Shared upstream detected" in d for d in rec.retained_disagreements)

    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id,
        mint(engine, rec, hashes, "TOK-SYBIL", "nonce-sybil-01"),
        AuthorityScope.EXECUTE_MIGRATION,
    )
    assert auth.execution_permitted is False
    assert auth.revalidation_log["evidence_state_supported"] is False


def test_vector_a_unknown_upstream_gets_no_independence_credit(engine):
    observations = [
        ObservationRecord.create("OBS-U1", "agent://a", None, "Node healthy"),
        ObservationRecord.create("OBS-U2", "agent://b", None, "Node healthy wrapped"),
    ]
    for obs in observations:
        engine.ingest_observation(obs)
    hashes = [o.content_hash for o in observations]
    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, [support_link(o) for o in observations], [])

    assert rec.epistemic_state == EvidenceState.UNRESOLVED
    assert rec.dependence_status == "unknown"
    assert any("independence unresolved" in d for d in rec.retained_disagreements)


def test_vector_b_deleted_primary_evidence_is_contained(engine):
    support = ObservationRecord.create("OBS-SUP", "telemetry://net", "upstream://net", "Link up")
    critical = ObservationRecord.create("OBS-CRIT", "kernel://fault", "upstream://kernel", "Socket healthy")
    for obs in (support, critical):
        engine.ingest_observation(obs)

    hashes = [support.content_hash, critical.content_hash]
    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, [support_link(support), support_link(critical)], [])
    assert rec.epistemic_state == EvidenceState.SUPPORTED

    token = mint(engine, rec, hashes, "TOK-TOCTOU", "nonce-toctou-01")
    del engine.evidence_store[critical.content_hash]

    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )
    assert auth.execution_permitted is False
    assert auth.revalidation_log["full_grounding_set_live"] is False


def test_vector_b_cherry_picked_token_subset_is_contained(engine):
    support = ObservationRecord.create("OBS-S1", "telemetry://1", "upstream://1", "Signal 1")
    critical = ObservationRecord.create("OBS-S2", "telemetry://2", "upstream://2", "Signal 2")
    for obs in (support, critical):
        engine.ingest_observation(obs)
    hashes = [support.content_hash, critical.content_hash]
    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, [support_link(support), support_link(critical)], [])
    assert rec.epistemic_state == EvidenceState.SUPPORTED

    token = mint(engine, rec, [support.content_hash], "TOK-SUBSET", "nonce-subset-01")
    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id, token, AuthorityScope.EXECUTE_MIGRATION
    )

    assert auth.execution_permitted is False
    assert auth.revalidation_log["token_evidence_exact_match"] is False


def test_vector_c_irrelevant_resolvable_noise_is_contained(engine):
    noise1 = ObservationRecord.create("NOISE-01", "telemetry://fan", "upstream://fan", "Fan RPM 3200")
    noise2 = ObservationRecord.create("NOISE-02", "telemetry://temp", "upstream://temp", "Temp 42C")
    for obs in (noise1, noise2):
        engine.ingest_observation(obs)
    hashes = [noise1.content_hash, noise2.content_hash]
    links = [
        EvidenceGroundingLink(noise1.content_hash, CLAIM_ID, GroundingRelationType.INSUFFICIENT_FOR, "Fan RPM does not establish migration safety"),
        EvidenceGroundingLink(noise2.content_hash, CLAIM_ID, GroundingRelationType.INSUFFICIENT_FOR, "Temperature alone does not establish migration safety"),
    ]

    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, links, [])
    assert rec.resolvability_score == 1.0
    assert rec.epistemic_state == EvidenceState.UNRESOLVED
    assert rec.completeness_score == 0.0

    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id,
        mint(engine, rec, hashes, "TOK-GAMING", "nonce-gaming-01"),
        AuthorityScope.EXECUTE_MIGRATION,
    )
    assert auth.execution_permitted is False


def test_vector_c_support_link_for_wrong_claim_does_not_ground_target(engine):
    obs = ObservationRecord.create("OBS-WRONG", "telemetry://x", "upstream://x", "Valid telemetry")
    engine.ingest_observation(obs)
    wrong_link = EvidenceGroundingLink(
        obs.content_hash,
        "PROP-OTHER",
        GroundingRelationType.SUPPORTS,
        "Supports a different proposition",
    )

    rec = engine.reconcile(CLAIM_ID, CLAIM, [obs.content_hash], [wrong_link], [])
    assert rec.epistemic_state == EvidenceState.UNRESOLVED
    assert rec.relevance_score == 0.0
    assert rec.completeness_score == 0.0


def test_supported_control_path_authorizes(engine):
    obs1 = ObservationRecord.create("OBS-C1", "telemetry://a", "upstream://a", "Healthy A")
    obs2 = ObservationRecord.create("OBS-C2", "telemetry://b", "upstream://b", "Healthy B")
    for obs in (obs1, obs2):
        engine.ingest_observation(obs)
    hashes = [obs1.content_hash, obs2.content_hash]
    rec = engine.reconcile(CLAIM_ID, CLAIM, hashes, [support_link(obs1), support_link(obs2)], [])

    assert rec.epistemic_state == EvidenceState.SUPPORTED
    auth = engine.evaluate_action_authorization(
        rec.reconciliation_id,
        mint(engine, rec, hashes, "TOK-CONTROL", "nonce-control-01"),
        AuthorityScope.EXECUTE_MIGRATION,
    )
    assert auth.execution_permitted is True

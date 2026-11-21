import base64
import os
import random
import tempfile
import time
from dataclasses import dataclass
from typing import List

import pytest

from src.oi_protocol_v0_2_1 import (
    AdversarialAttack,
    AttackAdjudication,
    AuthorizationToken,
    AuthorityScope,
    Ed25519Verifier,
    EpistemicCategory,
    EvidenceGroundingLink,
    EvidenceItem,
    GroundingRelationType,
    ObserverContextManifest,
    ObserverIntelligenceV2_1,
    PersistentNonceStore,
    Proposition,
    PropositionRelation,
    PropositionRelationType,
    verify_chain,
)


@dataclass
class BaselineAgentMessage:
    agent_id: str
    confidence: float
    vote_to_execute: bool


class StandardMultiAgentDebateBaseline:
    """Deliberately simple comparison condition, not a claim about all multi-agent systems."""
    def __init__(self, threshold: float = 0.65):
        self.threshold = threshold
        self.messages: List[BaselineAgentMessage] = []

    def submit(self, msg: BaselineAgentMessage):
        self.messages.append(msg)

    def evaluate(self, token: str) -> bool:
        total = sum(m.confidence for m in self.messages)
        positive = sum(m.confidence for m in self.messages if m.vote_to_execute)
        score = positive / total if total else 0.0
        return bool(token) and score >= self.threshold


def manifest(oi, observer, role, evidence=(), prior=()):
    m = ObserverContextManifest.generate(observer, role, evidence, prior)
    oi.register_manifest(m)
    return m


def prop(oi, pid, statement, category, observer, deps=None):
    p = Proposition(pid, statement, category, observer, dependency_proposition_ids=deps or [])
    oi.register_proposition(p)
    return p


def test_consensus_bias_sybil_fixture():
    ev = EvidenceItem.create("EV-FATAL", "Cluster 04 listener dropping all mTLS SYN packets", "telemetry://kernel/socket_err")
    base = StandardMultiAgentDebateBaseline()
    for aid, conf, vote in [("A1", .95, True), ("A2", .92, True), ("A3", .94, True), ("SHADOW", .99, False)]:
        base.submit(BaselineAgentMessage(aid, conf, vote))
    assert base.evaluate("MOCK") is True

    oi = ObserverIntelligenceV2_1("Unsafe migration", [ev], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "PRI", "Primary")
    manifest(oi, "SHD", "Shadow", ["EV-FATAL"])
    prop(oi, "P-PRI", "Execute migration", EpistemicCategory.RECOMMENDATION, "PRI")
    prop(oi, "P-SHD", "Fatal network partition detected", EpistemicCategory.OBSERVATION, "SHD")
    oi.register_grounding(EvidenceGroundingLink("L1", "EV-FATAL", "P-SHD", GroundingRelationType.SUPPORTS, "Direct kernel log", "SHD"))
    oi.register_relation(PropositionRelation("R1", "P-SHD", "P-PRI", PropositionRelationType.CONTRADICTS, "Failure blocks safe migration", "SHD"))
    out = oi.reconcile_graph()
    assert "P-PRI" in out["contested"]
    assert "P-SHD" in out["supported"]


def test_insufficient_grounding_semantic_leap():
    ev = EvidenceItem.create("EV-LAT", "Ping latency 11.6ms", "telemetry://ping")
    oi = ObserverIntelligenceV2_1("Security from latency", [ev], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "SEC", "Security", ["EV-LAT"])
    prop(oi, "P-LEAP", "Cluster is immune to all zero-days", EpistemicCategory.INFERENCE, "SEC")
    oi.register_grounding(EvidenceGroundingLink("L", "EV-LAT", "P-LEAP", GroundingRelationType.INSUFFICIENT_FOR, "Latency does not establish exploit immunity", "SEC"))
    assert "P-LEAP" in oi.reconcile_graph()["unresolved"]


def test_directed_contradiction_asymmetry():
    ev = EvidenceItem.create("EV-AUD", "Missing redundant listener", "audit://mesh")
    oi = ObserverIntelligenceV2_1("Asymmetry", [ev], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "A", "Primary")
    manifest(oi, "B", "Auditor", ["EV-AUD"])
    prop(oi, "P-A", "Mesh is fully redundant", EpistemicCategory.HYPOTHESIS, "A")
    prop(oi, "P-B", "Second listener absent", EpistemicCategory.OBSERVATION, "B")
    oi.register_grounding(EvidenceGroundingLink("L", "EV-AUD", "P-B", GroundingRelationType.SUPPORTS, "Config audit", "B"))
    oi.register_relation(PropositionRelation("R", "P-B", "P-A", PropositionRelationType.CONTRADICTS, "Direct configuration contradiction", "B"))
    out = oi.reconcile_graph()
    assert "P-A" in out["contested"]
    assert "P-B" in out["supported"]


def test_isolation_breach_rejected():
    ev1 = EvidenceItem.create("E1", "allowed", "x://1")
    ev2 = EvidenceItem.create("E2", "forbidden", "x://2")
    oi = ObserverIntelligenceV2_1("Isolation", [ev1, ev2], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "A", "Primary", ["E1"])
    prop(oi, "P", "Claim", EpistemicCategory.OBSERVATION, "A")
    with pytest.raises(PermissionError):
        oi.register_grounding(EvidenceGroundingLink("L", "E2", "P", GroundingRelationType.SUPPORTS, "Not visible", "A"))


def test_irrelevant_counterevidence_does_not_win_attack():
    ev = EvidenceItem.create("TEMP", "CPU temp 52C", "telemetry://temp")
    oi = ObserverIntelligenceV2_1("Irrelevance", [ev], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "PRI", "Primary")
    manifest(oi, "SHD", "Shadow", ["TEMP"])
    prop(oi, "P", "Listener redundancy exists", EpistemicCategory.INFERENCE, "PRI")
    attack = AdversarialAttack("ATK", "SHD", "P", "irrelevant", ["TEMP"], [])
    oi.submit_adversarial_attack(attack)
    oi.adjudicate_attacks()
    assert attack.adjudication == AttackAdjudication.FAILED


def test_unsupported_contradiction_does_not_demote_target():
    ev = EvidenceItem.create("GOOD", "Redundant listener observed", "audit://mesh")
    oi = ObserverIntelligenceV2_1("Unsupported contradiction", [ev], nonce_store=PersistentNonceStore(":memory:"))
    manifest(oi, "A", "Primary", ["GOOD"])
    manifest(oi, "B", "Challenger")
    prop(oi, "PA", "Redundant listener exists", EpistemicCategory.OBSERVATION, "A")
    prop(oi, "PB", "No redundant listener", EpistemicCategory.HYPOTHESIS, "B")
    oi.register_grounding(EvidenceGroundingLink("L", "GOOD", "PA", GroundingRelationType.SUPPORTS, "Audit", "A"))
    oi.register_relation(PropositionRelation("R", "PB", "PA", PropositionRelationType.CONTRADICTS, "Unsupported assertion", "B"))
    out = oi.reconcile_graph()
    assert "PA" in out["supported"]
    assert "PB" in out["unresolved"]


def _signed_token(oi, nonce):
    cryptography = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    serialization = pytest.importorskip("cryptography.hazmat.primitives.serialization")
    private = cryptography.Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    pub_b64 = base64.b64encode(public).decode()
    now = time.time()
    unsigned = AuthorizationToken(pub_b64, AuthorityScope.AUTHORIZE_MIGRATION, oi.run_id, nonce, now, now + 300, "")
    sig = private.sign(unsigned.canonical_payload())
    token = AuthorizationToken(pub_b64, unsigned.subject_action, unsigned.target_run_id, nonce, now, now + 300, base64.b64encode(sig).decode())
    return token, pub_b64


def test_replay_rejected_after_engine_restart():
    with tempfile.TemporaryDirectory() as td:
        db = os.path.join(td, "nonces.sqlite3")
        store1 = PersistentNonceStore(db)
        oi1 = ObserverIntelligenceV2_1("Replay", [], nonce_store=store1)
        token, pub = _signed_token(oi1, "N-1")
        assert oi1.verify_and_authorize(token, {pub}, AuthorityScope.AUTHORIZE_MIGRATION)

        store2 = PersistentNonceStore(db)
        oi2 = ObserverIntelligenceV2_1("Replay", [], nonce_store=store2)
        oi2.run_id = oi1.run_id  # reconstruct same archived run for replay attempt
        with pytest.raises(PermissionError, match="Replay"):
            oi2.verify_and_authorize(token, {pub}, AuthorityScope.AUTHORIZE_MIGRATION)


def test_signature_mutation_fails():
    oi = ObserverIntelligenceV2_1("Signature", [], nonce_store=PersistentNonceStore(":memory:"))
    token, pub = _signed_token(oi, "N-2")
    mutated = AuthorizationToken(pub, AuthorityScope.EXECUTE, token.target_run_id, token.nonce, token.issued_at, token.expires_at, token.signature_b64)
    with pytest.raises(PermissionError):
        oi.verify_and_authorize(mutated, {pub}, AuthorityScope.AUTHORIZE_MIGRATION)


def test_chain_tamper_detected():
    oi = ObserverIntelligenceV2_1("Chain", [], nonce_store=PersistentNonceStore(":memory:"))
    b1 = oi.generate_and_advance_block()
    b2 = oi.generate_and_advance_block()
    assert verify_chain([b1, b2])
    b1["payload"]["target_goal"] = "tampered"
    assert not verify_chain([b1, b2])


def test_monte_carlo_lossy_telemetry_containment():
    random.seed(20260827)
    iterations = 1000
    baseline_false_authorizations = 0
    oi_false_support = 0
    oi_unresolved = 0

    def arrives(loss=.25, max_jitter=180.0, threshold=80.0):
        if random.random() < loss:
            return False
        return random.uniform(5.0, max_jitter) <= threshold

    for i in range(iterations):
        hb_arrives = arrives()
        crit_arrives = arrives()

        base = StandardMultiAgentDebateBaseline()
        if not crit_arrives:
            base.submit(BaselineAgentMessage("OPT1", .95, True))
            base.submit(BaselineAgentMessage("OPT2", .90, True))
        else:
            base.submit(BaselineAgentMessage("SHADOW", .99, False))
        if base.evaluate("MOCK"):
            baseline_false_authorizations += 1

        evidence = []
        if hb_arrives:
            evidence.append(EvidenceItem.create(f"HB-{i}", "Heartbeat normal", "telemetry://hb"))
        if crit_arrives:
            evidence.append(EvidenceItem.create(f"CRIT-{i}", "Critical socket overflow", "telemetry://kernel"))

        oi = ObserverIntelligenceV2_1("Cluster health", evidence, nonce_store=PersistentNonceStore(":memory:"))
        hb_ids = [e.evidence_id for e in evidence if e.evidence_id.startswith("HB-")]
        crit_ids = [e.evidence_id for e in evidence if e.evidence_id.startswith("CRIT-")]
        manifest(oi, "PRI", "Primary", hb_ids)
        manifest(oi, "SHD", "Shadow", crit_ids)
        prop(oi, "P-PRI", "Cluster healthy for routing", EpistemicCategory.INFERENCE, "PRI")
        if hb_ids:
            oi.register_grounding(EvidenceGroundingLink("L-HB", hb_ids[0], "P-PRI", GroundingRelationType.INSUFFICIENT_FOR, "Heartbeat alone cannot prove full health", "PRI"))
        if crit_ids:
            prop(oi, "P-SHD", "Critical fault invalidates cluster", EpistemicCategory.OBSERVATION, "SHD")
            oi.register_grounding(EvidenceGroundingLink("L-CRIT", crit_ids[0], "P-SHD", GroundingRelationType.SUPPORTS, "Kernel fault", "SHD"))
            oi.register_relation(PropositionRelation("R", "P-SHD", "P-PRI", PropositionRelationType.CONTRADICTS, "Critical fault", "SHD"))
        out = oi.reconcile_graph()
        if "P-PRI" in out["supported"]:
            oi_false_support += 1
        if "P-PRI" in out["unresolved"]:
            oi_unresolved += 1

    # This fixture is deterministic via seed. The exact baseline rate is an observed
    # test output, not predeclared evidence. OI should never promote the broad health
    # claim from heartbeat-only or absent telemetry.
    assert baseline_false_authorizations > 500
    assert oi_false_support == 0
    assert oi_unresolved > 0

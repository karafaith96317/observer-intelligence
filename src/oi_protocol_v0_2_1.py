"""Observer Intelligence protocol v0.2.1 prototype.

OI preserves three lineages: provenance, epistemic reasoning, and authority.
Subjective confidence is metadata, not a truth metric.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Set


class EpistemicCategory(Enum):
    OBSERVATION = "Observation"
    INFERENCE = "Inference"
    HYPOTHESIS = "Hypothesis"
    PREDICTION = "Prediction"
    EVALUATION = "Evaluation"
    RECOMMENDATION = "Recommendation"
    UNKNOWN = "Unknown"


class EvidenceState(Enum):
    SUPPORTED = "Supported"
    CONTESTED = "Contested"
    UNRESOLVED = "Unresolved"
    FALSIFIED = "Falsified"
    SUPERSEDED = "Superseded"


class GroundingRelationType(Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    CONTEXTUALIZES = "contextualizes"
    INSUFFICIENT_FOR = "insufficient_for"


class PropositionRelationType(Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    QUALIFIES = "qualifies"
    INDEPENDENT_OF = "independent_of"


class AttackAdjudication(Enum):
    SUCCESSFUL = "Successful"
    PARTIAL = "Partial"
    FAILED = "Failed"
    UNRESOLVED = "Unresolved"


class AuthorityScope(Enum):
    OBSERVE = "scope:observe"
    RECOMMEND = "scope:recommend"
    AUTHORIZE_MIGRATION = "scope:action:migrate"
    EXECUTE = "scope:execute"


@dataclass(frozen=True)
class ObserverContextManifest:
    observer_id: str
    observer_role: str
    allowed_evidence_ids: tuple[str, ...]
    allowed_prior_proposition_ids: tuple[str, ...]
    started_at_utc: float
    context_hash: str

    @classmethod
    def generate(cls, observer_id: str, role: str, allowed_ev: Iterable[str], allowed_props: Iterable[str]):
        ev = tuple(sorted(set(allowed_ev)))
        props = tuple(sorted(set(allowed_props)))
        now = time.time()
        body = json.dumps({"observer_id": observer_id, "role": role, "evidence": ev, "prior_props": props, "started": now}, sort_keys=True, separators=(",", ":"))
        return cls(observer_id, role, ev, props, now, hashlib.sha256(body.encode()).hexdigest())


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    content: str
    source_uri: str
    captured_at_utc: float
    raw_hash: str

    @classmethod
    def create(cls, evidence_id: str, content: str, source_uri: str):
        now = time.time()
        body = json.dumps({"id": evidence_id, "content": content, "source": source_uri, "captured": now}, sort_keys=True, separators=(",", ":"))
        return cls(evidence_id, content, source_uri, now, hashlib.sha256(body.encode()).hexdigest())


@dataclass(frozen=True)
class EvidenceGroundingLink:
    link_id: str
    evidence_id: str
    proposition_id: str
    relation: GroundingRelationType
    rationale: str
    asserted_by_observer: str


@dataclass
class Proposition:
    proposition_id: str
    statement: str
    epistemic_category: EpistemicCategory
    observer_id: str
    context_manifest_hash: str = ""
    dependency_proposition_ids: List[str] = field(default_factory=list)
    subjective_confidence: float = 0.0
    evidence_state: EvidenceState = EvidenceState.UNRESOLVED


@dataclass(frozen=True)
class PropositionRelation:
    relation_id: str
    source_proposition_id: str
    target_proposition_id: str
    relation_type: PropositionRelationType
    rationale: str
    asserted_by_observer_id: str


@dataclass
class AdversarialAttack:
    attack_id: str
    shadow_observer_id: str
    target_proposition_id: str
    attack_vector: str
    counter_evidence_ids: List[str]
    target_dependency_ids: List[str]
    adjudication: AttackAdjudication = AttackAdjudication.UNRESOLVED
    adjudication_rationale: Optional[str] = None


@dataclass(frozen=True)
class AuthorizationToken:
    issuer_public_key_b64: str
    subject_action: AuthorityScope
    target_run_id: str
    nonce: str
    issued_at: float
    expires_at: float
    signature_b64: str

    def canonical_payload(self) -> bytes:
        return json.dumps({
            "issuer": self.issuer_public_key_b64,
            "scope": self.subject_action.value,
            "run": self.target_run_id,
            "nonce": self.nonce,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
        }, sort_keys=True, separators=(",", ":")).encode()


class PersistentNonceStore:
    def __init__(self, db_path: str = "oi_authorization_nonces.sqlite3"):
        self.db_path = db_path
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS consumed_nonces (nonce TEXT PRIMARY KEY, run_id TEXT NOT NULL, scope TEXT NOT NULL, consumed_at REAL NOT NULL)")

    def is_consumed(self, nonce: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT 1 FROM consumed_nonces WHERE nonce=?", (nonce,)).fetchone() is not None

    def consume_atomically(self, nonce: str, run_id: str, scope: AuthorityScope) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("BEGIN IMMEDIATE")
                conn.execute("INSERT INTO consumed_nonces VALUES (?, ?, ?, ?)", (nonce, run_id, scope.value, time.time()))
                conn.commit()
        except sqlite3.IntegrityError as exc:
            raise PermissionError(f"Replay detected: nonce '{nonce}' already consumed") from exc


class Ed25519Verifier:
    @staticmethod
    def verify(public_key_b64: str, signature_b64: str, payload: bytes) -> None:
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        except ImportError as exc:
            raise RuntimeError("Install 'cryptography' for Ed25519 verification") from exc
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
        key.verify(base64.b64decode(signature_b64), payload)


class ObserverIntelligenceV2_1:
    def __init__(self, target_goal: str, evidence_boundary: List[EvidenceItem], nonce_store: Optional[PersistentNonceStore] = None, initial_prev_block_hash: str = "0" * 64):
        self.run_id = "OI-v0.2.1-" + hashlib.sha256(f"{target_goal}:{time.time()}".encode()).hexdigest()[:12]
        self.target_goal = target_goal
        self.evidence_boundary = {e.evidence_id: e for e in evidence_boundary}
        self.manifests: Dict[str, ObserverContextManifest] = {}
        self.grounding_links: List[EvidenceGroundingLink] = []
        self.propositions: Dict[str, Proposition] = {}
        self.relations: List[PropositionRelation] = []
        self.adversarial_attacks: List[AdversarialAttack] = []
        self.nonce_store = nonce_store or PersistentNonceStore()
        self.sequence_number = 0
        self.previous_block_hash = initial_prev_block_hash
        self.reconciled_outcomes: Dict[str, Any] = {}

    def register_manifest(self, manifest: ObserverContextManifest) -> None:
        if manifest.observer_id in self.manifests:
            raise ValueError(f"Manifest already locked for {manifest.observer_id}")
        unknown = set(manifest.allowed_evidence_ids) - set(self.evidence_boundary)
        if unknown:
            raise ValueError(f"Manifest evidence outside boundary: {sorted(unknown)}")
        self.manifests[manifest.observer_id] = manifest

    def register_proposition(self, prop: Proposition) -> None:
        manifest = self.manifests.get(prop.observer_id)
        if manifest is None:
            raise PermissionError("Observer requires a locked manifest")
        forbidden = set(prop.dependency_proposition_ids) - set(manifest.allowed_prior_proposition_ids)
        if forbidden:
            raise PermissionError(f"Isolation breach: forbidden proposition dependencies {sorted(forbidden)}")
        prop.context_manifest_hash = manifest.context_hash
        self.propositions[prop.proposition_id] = prop

    def register_grounding(self, link: EvidenceGroundingLink) -> None:
        prop = self.propositions.get(link.proposition_id)
        if prop is None:
            raise KeyError("Proposition does not exist")
        if link.evidence_id not in self.evidence_boundary:
            raise KeyError("Evidence outside verified boundary")
        if link.asserted_by_observer != prop.observer_id:
            raise PermissionError("Grounding author must match proposition author")
        if link.evidence_id not in self.manifests[prop.observer_id].allowed_evidence_ids:
            raise PermissionError(f"Isolation breach: {prop.observer_id} cannot cite {link.evidence_id}")
        self.grounding_links.append(link)

    def register_relation(self, relation: PropositionRelation) -> None:
        if relation.source_proposition_id not in self.propositions or relation.target_proposition_id not in self.propositions:
            raise KeyError("Both propositions must exist")
        source = self.propositions[relation.source_proposition_id]
        if relation.asserted_by_observer_id != source.observer_id:
            raise PermissionError("Relation author must match source proposition observer")
        self.relations.append(relation)

    def submit_adversarial_attack(self, attack: AdversarialAttack) -> None:
        if attack.target_proposition_id not in self.propositions:
            raise KeyError("Attack target does not exist")
        manifest = self.manifests.get(attack.shadow_observer_id)
        if manifest is None:
            raise PermissionError("Shadow observer requires a manifest")
        for ev_id in attack.counter_evidence_ids:
            if ev_id not in self.evidence_boundary or ev_id not in manifest.allowed_evidence_ids:
                raise PermissionError(f"Counterevidence {ev_id} outside shadow isolation envelope")
        self.adversarial_attacks.append(attack)

    def _counterevidence_relevant(self, attack: AdversarialAttack) -> bool:
        targets = {attack.target_proposition_id, *attack.target_dependency_ids}
        return any(
            link.evidence_id in attack.counter_evidence_ids
            and link.proposition_id in targets
            and link.relation == GroundingRelationType.CONTRADICTS
            for link in self.grounding_links
        )

    def adjudicate_attacks(self) -> None:
        for attack in self.adversarial_attacks:
            target = self.propositions[attack.target_proposition_id]
            dependency_targeted = any(d in target.dependency_proposition_ids for d in attack.target_dependency_ids)
            if attack.counter_evidence_ids and self._counterevidence_relevant(attack):
                attack.adjudication = AttackAdjudication.SUCCESSFUL
                attack.adjudication_rationale = "Relevant verified counterevidence explicitly contradicts target/dependency"
            elif dependency_targeted:
                attack.adjudication = AttackAdjudication.PARTIAL
                attack.adjudication_rationale = "Valid dependency targeted without direct relevant counterevidence"
            else:
                attack.adjudication = AttackAdjudication.FAILED
                attack.adjudication_rationale = "No relevant evidence-to-target contradiction established"

    def reconcile_graph(self) -> Dict[str, Any]:
        self.adjudicate_attacks()
        for p_id, prop in self.propositions.items():
            links = [l for l in self.grounding_links if l.proposition_id == p_id]
            if any(l.relation == GroundingRelationType.CONTRADICTS for l in links):
                prop.evidence_state = EvidenceState.CONTESTED
            elif any(l.relation == GroundingRelationType.SUPPORTS for l in links):
                prop.evidence_state = EvidenceState.SUPPORTED
            else:
                prop.evidence_state = EvidenceState.UNRESOLVED

        for p_id, prop in self.propositions.items():
            incoming = [r for r in self.relations if r.target_proposition_id == p_id and r.relation_type == PropositionRelationType.CONTRADICTS and self.propositions[r.source_proposition_id].evidence_state in {EvidenceState.SUPPORTED, EvidenceState.CONTESTED}]
            attacks = [a for a in self.adversarial_attacks if a.target_proposition_id == p_id and a.adjudication == AttackAdjudication.SUCCESSFUL]
            broken_deps = [d for d in prop.dependency_proposition_ids if d not in self.propositions or self.propositions[d].evidence_state in {EvidenceState.CONTESTED, EvidenceState.FALSIFIED}]
            if incoming or attacks or broken_deps:
                prop.evidence_state = EvidenceState.CONTESTED

        out = {"supported": [], "contested": [], "unresolved": []}
        for p_id, prop in self.propositions.items():
            key = "supported" if prop.evidence_state == EvidenceState.SUPPORTED else "contested" if prop.evidence_state == EvidenceState.CONTESTED else "unresolved"
            out[key].append(p_id)
        self.reconciled_outcomes = out
        return out

    def verify_and_authorize(self, token: AuthorizationToken, authorized_issuers: Set[str], required_scope: AuthorityScope) -> bool:
        now = time.time()
        if token.issuer_public_key_b64 not in authorized_issuers:
            raise PermissionError("Unauthorized issuer")
        if token.subject_action != required_scope or token.target_run_id != self.run_id:
            raise PermissionError("Scope or run mismatch")
        if token.issued_at > now + 30 or now > token.expires_at:
            raise PermissionError("Authorization token outside valid time window")
        if self.nonce_store.is_consumed(token.nonce):
            raise PermissionError("Replay detected: authorization nonce already consumed")
        Ed25519Verifier.verify(token.issuer_public_key_b64, token.signature_b64, token.canonical_payload())
        self.nonce_store.consume_atomically(token.nonce, self.run_id, required_scope)
        return True

    def generate_and_advance_block(self, external_anchor_proof: str = "PENDING_EXTERNAL_ANCHOR") -> Dict[str, Any]:
        self.sequence_number += 1
        payload = {
            "sequence_number": self.sequence_number,
            "created_at_utc": time.time(),
            "run_id": self.run_id,
            "target_goal": self.target_goal,
            "manifests": {k: vars(v) for k, v in self.manifests.items()},
            "evidence_boundary": {k: vars(v) for k, v in self.evidence_boundary.items()},
            "grounding_links": [vars(x) for x in self.grounding_links],
            "propositions": {k: vars(v) for k, v in self.propositions.items()},
            "relations": [vars(x) for x in self.relations],
            "attacks": [vars(x) for x in self.adversarial_attacks],
            "reconciliation": self.reconciled_outcomes,
            "previous_block_hash": self.previous_block_hash,
            "external_anchor_proof": external_anchor_proof,
        }
        raw = json.dumps(payload, default=lambda x: x.value if isinstance(x, Enum) else list(x) if isinstance(x, tuple) else str(x), sort_keys=True, separators=(",", ":"))
        current = hashlib.sha256(raw.encode()).hexdigest()
        self.previous_block_hash = current
        return {"current_block_hash": current, "payload": payload}


def verify_chain(blocks: List[Dict[str, Any]]) -> bool:
    expected_prev = "0" * 64
    expected_seq = 1
    run_id = None
    for block in blocks:
        payload = block["payload"]
        if payload["sequence_number"] != expected_seq:
            return False
        if payload["previous_block_hash"] != expected_prev:
            return False
        if run_id is None:
            run_id = payload["run_id"]
        elif payload["run_id"] != run_id:
            return False
        raw = json.dumps(payload, default=lambda x: x.value if isinstance(x, Enum) else list(x) if isinstance(x, tuple) else str(x), sort_keys=True, separators=(",", ":"))
        current = hashlib.sha256(raw.encode()).hexdigest()
        if current != block["current_block_hash"]:
            return False
        expected_prev = current
        expected_seq += 1
    return True

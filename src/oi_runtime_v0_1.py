"""
Reference Runtime for Observer Intelligence (OI) v0.1
Implements:
1. ObservationRecord
2. AuthorityToken (Scoped, Bound, Expiring, Nonce-tracked)
3. ShadowEvaluation (Isolated, Targeted Challenge)
4. ReconciliationRecord (Resolvability Completeness, Retained Disagreement)
5. ActionAuthorization (Mandatory Revalidation Gate)

Contribution: GEM-IMPL-001 (reference implementation targeting GROK-SCHEMA-001)
"""

import time
import hashlib
import hmac
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Set


# --- 1. Enums & Lineage Types ---

class EpistemicCategory(Enum):
    OBSERVATION = "Observation"
    INFERENCE = "Inference"
    HYPOTHESIS = "Hypothesis"
    RECOMMENDATION = "Recommendation"
    UNKNOWN = "Unknown"


class EvidenceState(Enum):
    SUPPORTED = "Supported"
    CONTESTED = "Contested"
    UNRESOLVED = "Unresolved"
    FALSIFIED = "Falsified"


class AuthorityScope(Enum):
    OBSERVE = "scope:observe"
    INFER = "scope:infer"
    RECOMMEND = "scope:recommend"
    EXECUTE_MIGRATION = "scope:action:migrate"


# --- 2. Five Core Runtime Objects ---

@dataclass
class ObservationRecord:
    observation_id: str
    source_uri: str
    raw_payload: str
    captured_at_utc: float
    content_hash: str
    epistemic_category: EpistemicCategory = EpistemicCategory.OBSERVATION

    @classmethod
    def create(cls, observation_id: str, source_uri: str, payload: str) -> "ObservationRecord":
        c_hash = hashlib.sha256(f"{observation_id}:{source_uri}:{payload}".encode()).hexdigest()
        return cls(observation_id, source_uri, payload, time.time(), c_hash)


@dataclass
class AuthorityToken:
    token_id: str
    issuer_public_key: str
    subject_scope: AuthorityScope
    target_resource: str
    not_before_utc: float
    not_after_utc: float
    nonce: str
    bound_evidence_hashes: List[str]
    signature: str

    @classmethod
    def issue(
        cls,
        token_id: str,
        secret_key: bytes,
        issuer_pk: str,
        scope: AuthorityScope,
        resource: str,
        ttl_sec: float,
        nonce: str,
        evidence_hashes: List[str],
    ) -> "AuthorityToken":
        now = time.time()
        nbf = now - 1.0
        naf = now + ttl_sec
        payload = (
            f"{token_id}|{issuer_pk}|{scope.value}|{resource}|"
            f"{nbf}|{naf}|{nonce}|{sorted(evidence_hashes)}"
        )
        sig = hmac.new(secret_key, payload.encode(), hashlib.sha256).hexdigest()
        return cls(
            token_id,
            issuer_pk,
            scope,
            resource,
            nbf,
            naf,
            nonce,
            sorted(evidence_hashes),
            sig,
        )

    def verify_binding(self, secret_key: bytes) -> bool:
        payload = (
            f"{self.token_id}|{self.issuer_public_key}|{self.subject_scope.value}|"
            f"{self.target_resource}|{self.not_before_utc}|{self.not_after_utc}|"
            f"{self.nonce}|{sorted(self.bound_evidence_hashes)}"
        )
        expected_sig = hmac.new(secret_key, payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.signature, expected_sig)


@dataclass
class ShadowEvaluation:
    evaluation_id: str
    target_proposition_id: str
    shadow_observer_id: str
    isolated_input_hashes: List[str]
    findings: str
    counterevidence_hashes: List[str]
    correlation_with_primary: float
    challenge_succeeded: bool


@dataclass
class ReconciliationRecord:
    reconciliation_id: str
    target_claim: str
    grounding_resolvable: bool
    retained_disagreements: List[str]
    epistemic_state: EvidenceState
    lineage_exclusions: List[str]
    completeness_score: float  # Resolvability-based metric (0.0 - 1.0)


@dataclass
class ActionAuthorization:
    authorization_id: str
    reconciliation_ref: str
    token_ref: str
    authorized_at_utc: float
    execution_permitted: bool
    revalidation_log: Dict[str, bool]


# --- 3. Deterministic Runtime Engine ---

class OIRuntimeEngine:
    def __init__(self, secret_key: bytes, authorized_issuers: Set[str]):
        self.secret_key = secret_key
        self.authorized_issuers = authorized_issuers

        # State stores
        self.evidence_store: Dict[str, ObservationRecord] = {}
        self.consumed_nonces: Set[str] = set()
        self.reconciliation_store: Dict[str, ReconciliationRecord] = {}

    def ingest_observation(self, obs: ObservationRecord) -> None:
        self.evidence_store[obs.content_hash] = obs

    def reconcile(
        self,
        target_claim: str,
        primary_evidence_hashes: List[str],
        shadow_evals: List[ShadowEvaluation],
    ) -> ReconciliationRecord:
        """
        Calculates completeness from evidence resolvability.
        Retains explicit disagreements rather than averaging.
        """
        # 1. Resolvability Check
        resolvable = [h for h in primary_evidence_hashes if h in self.evidence_store]
        completeness = (
            len(resolvable) / len(primary_evidence_hashes)
            if primary_evidence_hashes
            else 0.0
        )
        grounding_ok = completeness == 1.0

        # 2. Shadow Challenges & Contradictions
        retained_disagreements: List[str] = []
        successful_challenges = 0

        for shadow in shadow_evals:
            if shadow.challenge_succeeded:
                successful_challenges += 1
                retained_disagreements.append(
                    f"Observer {shadow.shadow_observer_id} refuted claim: {shadow.findings}"
                )

        # 3. State Determination
        if successful_challenges > 0:
            final_state = EvidenceState.CONTESTED
        elif not grounding_ok:
            final_state = EvidenceState.UNRESOLVED
        else:
            final_state = EvidenceState.SUPPORTED

        rec = ReconciliationRecord(
            reconciliation_id=f"REC-{hashlib.sha256(target_claim.encode()).hexdigest()[:8]}",
            target_claim=target_claim,
            grounding_resolvable=grounding_ok,
            retained_disagreements=retained_disagreements,
            epistemic_state=final_state,
            lineage_exclusions=[
                h for h in primary_evidence_hashes if h not in self.evidence_store
            ],
            completeness_score=completeness,
        )
        self.reconciliation_store[rec.reconciliation_id] = rec
        return rec

    def evaluate_action_authorization(
        self,
        reconciliation_id: str,
        token: AuthorityToken,
        required_scope: AuthorityScope,
    ) -> ActionAuthorization:
        """
        Mandatory revalidation gate (GROK-SCHEMA-001 compliant).
        Checks binding, scope, window, replay, and current evidence state.
        """
        now = time.time()
        rec = self.reconciliation_store.get(reconciliation_id)

        revalidation = {
            "token_signature_valid": token.verify_binding(self.secret_key),
            "issuer_authorized": token.issuer_public_key in self.authorized_issuers,
            "scope_exact_match": token.subject_scope == required_scope,
            "within_time_window": token.not_before_utc <= now <= token.not_after_utc,
            "nonce_unconsumed": token.nonce not in self.consumed_nonces,
            "reconciliation_exists": rec is not None,
            "evidence_state_supported": (
                rec.epistemic_state == EvidenceState.SUPPORTED if rec else False
            ),
            "bound_evidence_unmodified": all(
                h in self.evidence_store for h in token.bound_evidence_hashes
            ),
        }

        all_passed = all(revalidation.values())

        if all_passed:
            self.consumed_nonces.add(token.nonce)

        return ActionAuthorization(
            authorization_id=f"AUTH-ACT-{hashlib.sha256(f'{token.token_id}:{now}'.encode()).hexdigest()[:8]}",
            reconciliation_ref=reconciliation_id,
            token_ref=token.token_id,
            authorized_at_utc=now,
            execution_permitted=all_passed,
            revalidation_log=revalidation,
        )

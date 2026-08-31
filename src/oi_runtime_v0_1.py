"""
Reference Runtime for Observer Intelligence (OI) v0.1 → v0.1.1 (GEM-IMPL-002)
Implements:
1. ObservationRecord
2. AuthorityToken (Scoped, Bound, Expiring, Nonce-tracked)
3. ShadowEvaluation (Isolated, Targeted Challenge)
4. ReconciliationRecord (Resolvability + relevance + effective independence)
5. ActionAuthorization (Mandatory Revalidation Gate + live primary re-resolve)

GEM-IMPL-001: baseline against GROK-SCHEMA-001
GEM-IMPL-002: hardens GROK-ATTACK-002 vectors (soft Sybil, TOCTOU, completeness gaming)
"""

import re
import time
import hashlib
import hmac
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple


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


_STOP = {
    "a", "an", "the", "is", "are", "for", "to", "of", "and", "or", "on", "in",
    "prop", "migrate", "node", "claim",
}


def _normalize_payload(payload: str) -> str:
    return re.sub(r"\s+", " ", payload.strip().lower())


def _tokens(text: str) -> Set[str]:
    return {t for t in re.findall(r"[a-z0-9_]+", text.lower()) if t not in _STOP and len(t) > 2}


@dataclass
class ObservationRecord:
    observation_id: str
    source_uri: str
    raw_payload: str
    captured_at_utc: float
    content_hash: str
    epistemic_category: EpistemicCategory = EpistemicCategory.OBSERVATION
    soft_source: Optional[str] = None

    @classmethod
    def create(
        cls,
        observation_id: str,
        source_uri: str,
        payload: str,
        soft_source: Optional[str] = None,
    ) -> "ObservationRecord":
        c_hash = hashlib.sha256(
            f"{observation_id}:{source_uri}:{payload}".encode()
        ).hexdigest()
        return cls(
            observation_id,
            source_uri,
            payload,
            time.time(),
            c_hash,
            soft_source=soft_source,
        )


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
        expected_sig = hmac.new(
            secret_key, payload.encode(), hashlib.sha256
        ).hexdigest()
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
    completeness_score: float
    primary_evidence_hashes: List[str] = field(default_factory=list)
    effective_independent_pathways: float = 0.0
    relevance_score: float = 0.0
    resolvability_score: float = 0.0


@dataclass
class ActionAuthorization:
    authorization_id: str
    reconciliation_ref: str
    token_ref: str
    authorized_at_utc: float
    execution_permitted: bool
    revalidation_log: Dict[str, bool]


class OIRuntimeEngine:
    """GEM-IMPL-002: dependence-aware reconcile + live primary re-resolve at authorize."""

    # EXECUTE requires at least this many effective independent pathways
    MIN_EXECUTE_INDEPENDENCE = 1.5
    # EXECUTE requires claim–evidence token overlap ratio
    MIN_EXECUTE_RELEVANCE = 0.15

    def __init__(self, secret_key: bytes, authorized_issuers: Set[str]):
        self.secret_key = secret_key
        self.authorized_issuers = authorized_issuers
        self.evidence_store: Dict[str, ObservationRecord] = {}
        self.consumed_nonces: Set[str] = set()
        self.reconciliation_store: Dict[str, ReconciliationRecord] = {}

    def ingest_observation(self, obs: ObservationRecord) -> None:
        self.evidence_store[obs.content_hash] = obs

    def _effective_independence(
        self, hashes: List[str]
    ) -> Tuple[float, List[str]]:
        """Cluster by soft_source if set, else by normalized payload."""
        notes: List[str] = []
        if not hashes:
            return 0.0, notes

        groups: Dict[str, int] = {}
        for h in hashes:
            obs = self.evidence_store.get(h)
            if obs is None:
                continue
            key = obs.soft_source or _normalize_payload(obs.raw_payload)
            groups[key] = groups.get(key, 0) + 1

        if not groups:
            return 0.0, notes

        # Each unique cluster counts as 1 pathway; duplicates within cluster add 0
        effective = float(len(groups))
        for key, count in groups.items():
            if count > 1:
                notes.append(f"cluster={key[:48]!r} n={count} → dependence")
        return effective, notes

    def _relevance_score(self, claim: str, hashes: List[str]) -> float:
        claim_toks = _tokens(claim)
        if not claim_toks or not hashes:
            return 0.0
        hits = 0
        considered = 0
        for h in hashes:
            obs = self.evidence_store.get(h)
            if obs is None:
                continue
            considered += 1
            if claim_toks & _tokens(obs.raw_payload):
                hits += 1
        if considered == 0:
            return 0.0
        return hits / considered

    def reconcile(
        self,
        target_claim: str,
        primary_evidence_hashes: List[str],
        shadow_evals: List[ShadowEvaluation],
    ) -> ReconciliationRecord:
        resolvable = [h for h in primary_evidence_hashes if h in self.evidence_store]
        resolvability = (
            len(resolvable) / len(primary_evidence_hashes)
            if primary_evidence_hashes
            else 0.0
        )
        grounding_ok = resolvability == 1.0

        effective, dep_notes = self._effective_independence(primary_evidence_hashes)
        relevance = self._relevance_score(target_claim, primary_evidence_hashes)

        retained_disagreements: List[str] = []
        successful_challenges = 0
        high_correlation_shadow = False

        for shadow in shadow_evals:
            if shadow.challenge_succeeded:
                successful_challenges += 1
                retained_disagreements.append(
                    f"Observer {shadow.shadow_observer_id} refuted claim: {shadow.findings}"
                )
            if shadow.correlation_with_primary >= 0.5:
                high_correlation_shadow = True
                retained_disagreements.append(
                    f"Shadow {shadow.shadow_observer_id} correlation_with_primary="
                    f"{shadow.correlation_with_primary}"
                )

        for n in dep_notes:
            retained_disagreements.append(f"dependence: {n}")

        # Soft-Sybil: many listed hashes collapse to few pathways
        soft_sybil = (
            len(primary_evidence_hashes) >= 2
            and effective < self.MIN_EXECUTE_INDEPENDENCE
            and effective < len(resolvable)
        )

        if successful_challenges > 0:
            final_state = EvidenceState.CONTESTED
        elif not grounding_ok:
            final_state = EvidenceState.UNRESOLVED
        elif soft_sybil or high_correlation_shadow:
            final_state = EvidenceState.UNRESOLVED
            if soft_sybil:
                retained_disagreements.append(
                    f"soft-Sybil: effective_independent_pathways={effective}"
                )
        elif relevance < self.MIN_EXECUTE_RELEVANCE and len(primary_evidence_hashes) > 0:
            # Irrelevant resolvable evidence does not support EXECUTE-grade claims
            final_state = EvidenceState.UNRESOLVED
            retained_disagreements.append(
                f"low relevance_score={relevance:.3f} vs claim"
            )
        else:
            final_state = EvidenceState.SUPPORTED

        # Completeness for display: require both resolvability and relevance for full credit
        completeness = min(resolvability, max(relevance, resolvability * relevance))
        if final_state == EvidenceState.SUPPORTED:
            completeness = resolvability

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
            primary_evidence_hashes=list(primary_evidence_hashes),
            effective_independent_pathways=effective,
            relevance_score=relevance,
            resolvability_score=resolvability,
        )
        self.reconciliation_store[rec.reconciliation_id] = rec
        return rec

    def evaluate_action_authorization(
        self,
        reconciliation_id: str,
        token: AuthorityToken,
        required_scope: AuthorityScope,
    ) -> ActionAuthorization:
        now = time.time()
        rec = self.reconciliation_store.get(reconciliation_id)

        primary_ok = True
        if rec is not None:
            primary_ok = all(
                h in self.evidence_store for h in rec.primary_evidence_hashes
            )

        independence_ok = True
        relevance_ok = True
        if rec is not None and required_scope == AuthorityScope.EXECUTE_MIGRATION:
            independence_ok = (
                rec.effective_independent_pathways >= self.MIN_EXECUTE_INDEPENDENCE
            )
            relevance_ok = rec.relevance_score >= self.MIN_EXECUTE_RELEVANCE

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
            "primary_evidence_still_resolvable": primary_ok,
            "execute_independence_ok": independence_ok
            if required_scope == AuthorityScope.EXECUTE_MIGRATION
            else True,
            "execute_relevance_ok": relevance_ok
            if required_scope == AuthorityScope.EXECUTE_MIGRATION
            else True,
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

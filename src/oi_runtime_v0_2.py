"""Observer Intelligence reference runtime v0.2.

GEM-IMPL-002 hardening against GROK-ATTACK-002:
- T02b dependence containment via explicit upstream provenance and unknown-dependence refusal
- full reconciliation grounding-set binding and execution-time re-resolution (TOCTOU)
- claim-specific typed grounding links; resolvability is not semantic support

This remains a development harness. HMAC and in-memory nonce state are not
production authority mechanisms (see GPT-SPEC-002 boundary lock).
"""

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set


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


class GroundingRelationType(Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    CONTEXTUALIZES = "contextualizes"
    INSUFFICIENT_FOR = "insufficient_for"


class AuthorityScope(Enum):
    OBSERVE = "scope:observe"
    INFER = "scope:infer"
    RECOMMEND = "scope:recommend"
    EXECUTE_MIGRATION = "scope:action:migrate"


@dataclass(frozen=True)
class ObservationRecord:
    observation_id: str
    source_uri: str
    upstream_source_id: Optional[str]
    raw_payload: str
    captured_at_utc: float
    content_hash: str
    epistemic_category: EpistemicCategory = EpistemicCategory.OBSERVATION

    @classmethod
    def create(
        cls,
        observation_id: str,
        source_uri: str,
        upstream_id: Optional[str],
        payload: str,
    ) -> "ObservationRecord":
        content_hash = hashlib.sha256(
            f"{observation_id}:{source_uri}:{upstream_id}:{payload}".encode()
        ).hexdigest()
        return cls(
            observation_id=observation_id,
            source_uri=source_uri,
            upstream_source_id=upstream_id,
            raw_payload=payload,
            captured_at_utc=time.time(),
            content_hash=content_hash,
        )


@dataclass(frozen=True)
class EvidenceGroundingLink:
    evidence_hash: str
    target_claim_id: str
    relation: GroundingRelationType
    rationale: str


@dataclass
class AuthorityToken:
    token_id: str
    issuer_public_key: str
    subject_scope: AuthorityScope
    target_resource: str
    not_before_utc: float
    not_after_utc: float
    nonce: str
    bound_reconciliation_hash: str
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
        rec_hash: str,
        evidence_hashes: List[str],
    ) -> "AuthorityToken":
        now = time.time()
        not_before = now - 1.0
        not_after = now + ttl_sec
        canonical_hashes = sorted(set(evidence_hashes))
        payload = cls._payload(
            token_id,
            issuer_pk,
            scope,
            resource,
            not_before,
            not_after,
            nonce,
            rec_hash,
            canonical_hashes,
        )
        signature = hmac.new(secret_key, payload, hashlib.sha256).hexdigest()
        return cls(
            token_id=token_id,
            issuer_public_key=issuer_pk,
            subject_scope=scope,
            target_resource=resource,
            not_before_utc=not_before,
            not_after_utc=not_after,
            nonce=nonce,
            bound_reconciliation_hash=rec_hash,
            bound_evidence_hashes=canonical_hashes,
            signature=signature,
        )

    @staticmethod
    def _payload(
        token_id: str,
        issuer_pk: str,
        scope: AuthorityScope,
        resource: str,
        not_before: float,
        not_after: float,
        nonce: str,
        rec_hash: str,
        evidence_hashes: List[str],
    ) -> bytes:
        data = {
            "token_id": token_id,
            "issuer_public_key": issuer_pk,
            "subject_scope": scope.value,
            "target_resource": resource,
            "not_before_utc": not_before,
            "not_after_utc": not_after,
            "nonce": nonce,
            "bound_reconciliation_hash": rec_hash,
            "bound_evidence_hashes": sorted(set(evidence_hashes)),
        }
        return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()

    def verify_binding(self, secret_key: bytes) -> bool:
        expected = hmac.new(
            secret_key,
            self._payload(
                self.token_id,
                self.issuer_public_key,
                self.subject_scope,
                self.target_resource,
                self.not_before_utc,
                self.not_after_utc,
                self.nonce,
                self.bound_reconciliation_hash,
                self.bound_evidence_hashes,
            ),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected)


@dataclass(frozen=True)
class ShadowEvaluation:
    evaluation_id: str
    target_proposition_id: str
    shadow_observer_id: str
    isolated_input_hashes: List[str]
    findings: str
    counterevidence_hashes: List[str]
    correlation_with_primary: Optional[float]
    challenge_succeeded: bool


@dataclass
class ReconciliationRecord:
    reconciliation_id: str
    target_claim_id: str
    target_claim: str
    primary_evidence_hashes: List[str]
    grounding_links: List[EvidenceGroundingLink]
    grounding_resolvable: bool
    retained_disagreements: List[str]
    epistemic_state: EvidenceState
    lineage_exclusions: List[str]
    resolvability_score: float
    relevance_score: float
    completeness_score: float
    dependence_status: str
    reconciliation_snapshot_hash: str


@dataclass
class ActionAuthorization:
    authorization_id: str
    reconciliation_ref: str
    token_ref: str
    authorized_at_utc: float
    execution_permitted: bool
    revalidation_log: Dict[str, bool]


class OIRuntimeEngineV2:
    def __init__(self, secret_key: bytes, authorized_issuers: Set[str]):
        self.secret_key = secret_key
        self.authorized_issuers = authorized_issuers
        self.evidence_store: Dict[str, ObservationRecord] = {}
        self.consumed_nonces: Set[str] = set()
        self.reconciliation_store: Dict[str, ReconciliationRecord] = {}

    def ingest_observation(self, obs: ObservationRecord) -> None:
        self.evidence_store[obs.content_hash] = obs

    @staticmethod
    def compute_snapshot_hash(
        claim_id: str,
        claim: str,
        state: EvidenceState,
        primary_hashes: List[str],
        grounding_links: List[EvidenceGroundingLink],
    ) -> str:
        canonical_links = [
            {
                "evidence_hash": link.evidence_hash,
                "target_claim_id": link.target_claim_id,
                "relation": link.relation.value,
                "rationale": link.rationale,
            }
            for link in sorted(
                grounding_links,
                key=lambda x: (x.evidence_hash, x.target_claim_id, x.relation.value, x.rationale),
            )
        ]
        data = {
            "target_claim_id": claim_id,
            "target_claim": claim,
            "epistemic_state": state.value,
            "primary_evidence_hashes": sorted(set(primary_hashes)),
            "grounding_links": canonical_links,
        }
        return hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def reconcile(
        self,
        target_claim_id: str,
        target_claim: str,
        primary_evidence_hashes: List[str],
        grounding_links: List[EvidenceGroundingLink],
        shadow_evals: List[ShadowEvaluation],
    ) -> ReconciliationRecord:
        primary = sorted(set(primary_evidence_hashes))
        resolvable = [h for h in primary if h in self.evidence_store]
        resolvability = len(resolvable) / len(primary) if primary else 0.0

        links_for_claim = [
            link
            for link in grounding_links
            if link.target_claim_id == target_claim_id and link.evidence_hash in primary
        ]
        linked_hashes = {link.evidence_hash for link in links_for_claim}
        supporting_hashes = {
            link.evidence_hash
            for link in links_for_claim
            if link.relation == GroundingRelationType.SUPPORTS
        }
        insufficient_hashes = {
            link.evidence_hash
            for link in links_for_claim
            if link.relation == GroundingRelationType.INSUFFICIENT_FOR
        }
        contradictory_hashes = {
            link.evidence_hash
            for link in links_for_claim
            if link.relation == GroundingRelationType.CONTRADICTS
        }

        # Relevance is explicit and claim-specific. It is still an asserted relation;
        # the runtime does not claim to solve semantic truth by itself.
        relevance = len(linked_hashes) / len(primary) if primary else 0.0
        semantic_support_ok = (
            bool(primary)
            and linked_hashes == set(primary)
            and bool(supporting_hashes)
            and not insufficient_hashes
        )

        upstream_ids = [self.evidence_store[h].upstream_source_id for h in resolvable]
        known_upstreams = {u for u in upstream_ids if u}
        has_unknown_upstream = any(not u for u in upstream_ids)
        exact_shared_upstream = len(resolvable) > 1 and len(known_upstreams) == 1 and not has_unknown_upstream

        # Unknown provenance cannot receive independence credit for high-authority
        # decisions. This contains hidden-dependence risk; it does not prove detection.
        dependence_uncertain = len(resolvable) > 1 and has_unknown_upstream
        if exact_shared_upstream:
            dependence_status = "shared_upstream"
        elif dependence_uncertain:
            dependence_status = "unknown"
        else:
            dependence_status = "distinct_declared_upstreams"

        retained: List[str] = []
        successful_challenges = 0
        high_shadow_correlation = False
        for shadow in shadow_evals:
            if shadow.challenge_succeeded:
                successful_challenges += 1
                retained.append(
                    f"Observer {shadow.shadow_observer_id} refuted: {shadow.findings}"
                )
            if (
                shadow.correlation_with_primary is None
                or shadow.correlation_with_primary > 0.70
            ):
                high_shadow_correlation = True
                retained.append(
                    f"Shadow {shadow.shadow_observer_id} lacks sufficient independence evidence"
                )

        if successful_challenges or contradictory_hashes:
            final_state = EvidenceState.CONTESTED
        elif (
            resolvability < 1.0
            or not semantic_support_ok
            or exact_shared_upstream
            or dependence_uncertain
            or high_shadow_correlation
        ):
            final_state = EvidenceState.UNRESOLVED
        else:
            final_state = EvidenceState.SUPPORTED

        if exact_shared_upstream:
            retained.append(
                f"Shared upstream detected across {len(resolvable)} records: {next(iter(known_upstreams))}"
            )
        if dependence_uncertain:
            retained.append("Upstream independence unresolved; no independence credit granted")
        if not semantic_support_ok:
            retained.append("Claim-specific semantic grounding is incomplete or insufficient")

        snapshot = self.compute_snapshot_hash(
            target_claim_id,
            target_claim,
            final_state,
            primary,
            links_for_claim,
        )
        rec_id = f"REC-{snapshot[:12]}"
        rec = ReconciliationRecord(
            reconciliation_id=rec_id,
            target_claim_id=target_claim_id,
            target_claim=target_claim,
            primary_evidence_hashes=primary,
            grounding_links=links_for_claim,
            grounding_resolvable=resolvability == 1.0,
            retained_disagreements=retained,
            epistemic_state=final_state,
            lineage_exclusions=[h for h in primary if h not in self.evidence_store],
            resolvability_score=resolvability,
            relevance_score=relevance,
            completeness_score=min(resolvability, relevance) if semantic_support_ok else 0.0,
            dependence_status=dependence_status,
            reconciliation_snapshot_hash=snapshot,
        )
        self.reconciliation_store[rec_id] = rec
        return rec

    def evaluate_action_authorization(
        self,
        reconciliation_id: str,
        token: AuthorityToken,
        required_scope: AuthorityScope,
    ) -> ActionAuthorization:
        now = time.time()
        rec = self.reconciliation_store.get(reconciliation_id)

        if rec:
            live_primary_resolvable = all(
                h in self.evidence_store for h in rec.primary_evidence_hashes
            )
            token_evidence_exact_match = (
                sorted(set(token.bound_evidence_hashes)) == rec.primary_evidence_hashes
            )
            recomputed_snapshot = self.compute_snapshot_hash(
                rec.target_claim_id,
                rec.target_claim,
                rec.epistemic_state,
                rec.primary_evidence_hashes,
                rec.grounding_links,
            )
            reconciliation_snapshot_valid = (
                recomputed_snapshot == rec.reconciliation_snapshot_hash
                and token.bound_reconciliation_hash == rec.reconciliation_snapshot_hash
            )
        else:
            live_primary_resolvable = False
            token_evidence_exact_match = False
            reconciliation_snapshot_valid = False

        revalidation = {
            "token_signature_valid": token.verify_binding(self.secret_key),
            "issuer_authorized": token.issuer_public_key in self.authorized_issuers,
            "scope_exact_match": token.subject_scope == required_scope,
            "within_time_window": token.not_before_utc <= now < token.not_after_utc,
            "nonce_unconsumed": token.nonce not in self.consumed_nonces,
            "reconciliation_exists": rec is not None,
            "reconciliation_snapshot_valid": reconciliation_snapshot_valid,
            "token_evidence_exact_match": token_evidence_exact_match,
            "full_grounding_set_live": live_primary_resolvable,
            "evidence_state_supported": (
                rec.epistemic_state == EvidenceState.SUPPORTED if rec else False
            ),
        }
        permitted = all(revalidation.values())
        if permitted:
            self.consumed_nonces.add(token.nonce)

        return ActionAuthorization(
            authorization_id=f"AUTH-ACT-{hashlib.sha256(f'{token.token_id}:{now}'.encode()).hexdigest()[:8]}",
            reconciliation_ref=reconciliation_id,
            token_ref=token.token_id,
            authorized_at_utc=now,
            execution_permitted=permitted,
            revalidation_log=revalidation,
        )

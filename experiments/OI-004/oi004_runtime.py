#!/usr/bin/env python3
"""
OI-004 — Minimal five-object runtime skeleton
Observation → Authority Token → Shadow Evaluation → Reconciliation → Action Authorization

Development harness only. No external dependencies.
Addresses GROK-ATTACK-001 / GROK-SCHEMA-001 testability requirements.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TEST_HMAC_KEY = b"oi004-dev-key-not-for-production"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def mac_token_fields(
    token_id: str,
    scope: str,
    not_before: str,
    not_after: str,
    evidence_refs: List[str],
    issuer: str,
) -> str:
    payload = "|".join(
        [token_id, scope, not_before, not_after, ",".join(evidence_refs), issuer]
    )
    return hmac.new(TEST_HMAC_KEY, payload.encode(), hashlib.sha256).hexdigest()


def verify_mac(
    token_id: str,
    scope: str,
    not_before: str,
    not_after: str,
    evidence_refs: List[str],
    issuer: str,
    value: str,
) -> bool:
    expected = mac_token_fields(
        token_id, scope, not_before, not_after, evidence_refs, issuer
    )
    return hmac.compare_digest(expected, value)


# ---------------------------------------------------------------------------
# Record builders (shaped for schemas; not full JSON-Schema validation)
# ---------------------------------------------------------------------------


def make_observation(
    observer_id: str,
    content: Any,
    *,
    epistemic_label: str = "direct_observation",
    confidence: float = 0.8,
    source_id: Optional[str] = None,
    soft_source: Optional[str] = None,
    measurement_integrity: float = 1.0,
    compromised: bool = False,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    oid = new_id("obs")
    ctx: Dict[str, Any] = {
        "measurement_integrity": measurement_integrity,
        "compromised": compromised,
    }
    if source_id is not None:
        ctx["source_id"] = source_id
    if soft_source is not None:
        ctx["soft_source"] = soft_source
    return {
        "observation_id": oid,
        "observer_id": observer_id,
        "timestamp": timestamp or now_iso(),
        "epistemic_label": epistemic_label,
        "content": content,
        "confidence": confidence,
        "context": ctx,
        "provenance": [f"observer:{observer_id}"],
        "corroborates": [],
        "contradicts": [],
        "interpretation": None,
        "notes": None,
    }


def make_shadow_evaluation(
    observations: List[Dict[str, Any]],
    *,
    critic_id: str = "critic-rule",
    isolation: bool = True,
    same_model_family: bool = False,
    force_semantic_leap_flag: Optional[str] = None,
) -> Dict[str, Any]:
    contradictions: List[str] = []
    alternatives: List[str] = []
    leaps: List[str] = []

    claims = [str(o.get("content")) for o in observations]
    if len(set(claims)) > 1:
        contradictions.append(f"conflicting claims: {sorted(set(claims))}")
        alternatives.extend(sorted(set(claims)))

    for o in observations:
        interp = o.get("interpretation")
        if interp and interp != o.get("content"):
            leaps.append(
                f"possible semantic leap on {o['observation_id']}: "
                f"content={o.get('content')!r} interpretation={interp!r}"
            )
    if force_semantic_leap_flag:
        leaps.append(force_semantic_leap_flag)

    # Down-weight known compromised or low integrity
    for o in observations:
        ctx = o.get("context") or {}
        if ctx.get("compromised"):
            contradictions.append(f"compromised observer {o['observer_id']}")
        if ctx.get("measurement_integrity", 1.0) < 0.5:
            contradictions.append(
                f"low measurement integrity on {o['observation_id']}"
            )

    dep = 0.0
    if same_model_family:
        dep = 0.7

    return {
        "evaluation_id": new_id("shadow"),
        "critic_id": critic_id,
        "created_at": now_iso(),
        "input_scope": {
            "observation_refs": [o["observation_id"] for o in observations],
            "information_received_summary": "raw observation content + context",
            "received_interpretations": any(
                o.get("interpretation") for o in observations
            ),
        },
        "isolation_flag": isolation,
        "correlation_with_primary": {
            "same_model_family": same_model_family,
            "same_checkpoint_or_weights": False,
            "shared_prompt_template": False,
            "shared_upstream_data": False,
            "estimated_dependence": dep,
        },
        "findings": {
            "contradictions": contradictions,
            "alternative_hypotheses": alternatives,
            "semantic_leap_flags": leaps,
            "support_for_primary": [],
        },
        "uncertainty": 0.3 if contradictions or leaps else 0.1,
        "notes": None,
    }


def estimate_dependence(observations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simple heuristic: exact source_id and soft_source clustering."""
    n = len(observations)
    if n == 0:
        return {
            "method": "empty",
            "effective_independent_pathways": 0.0,
            "pairwise_notes": [],
        }

    exact_groups: Dict[str, int] = {}
    soft_groups: Dict[str, int] = {}
    for o in observations:
        ctx = o.get("context") or {}
        sid = ctx.get("source_id")
        soft = ctx.get("soft_source")
        if sid:
            exact_groups[sid] = exact_groups.get(sid, 0) + 1
        if soft:
            soft_groups[soft] = soft_groups.get(soft, 0) + 1

    # Start with n, subtract redundancy
    effective = float(n)
    notes: List[str] = []
    for sid, count in exact_groups.items():
        if count > 1:
            effective -= (count - 1) * 1.0
            notes.append(f"exact source_id={sid} count={count} → full dependence")
    for soft, count in soft_groups.items():
        if count > 1:
            # soft correlation: count as 0.6 dependence among extras
            effective -= (count - 1) * 0.6
            notes.append(
                f"soft_source={soft} count={count} → graded dependence 0.6"
            )

    effective = max(0.0, min(float(n), effective))
    method = "exact+soft-heuristic"
    return {
        "method": method,
        "effective_independent_pathways": round(effective, 3),
        "pairwise_notes": notes,
    }


def make_reconciliation(
    observations: List[Dict[str, Any]],
    shadow: Dict[str, Any],
    *,
    ledger: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    ledger = ledger or {o["observation_id"]: o for o in observations}
    dep = estimate_dependence(observations)

    contributing = []
    missing = []
    all_resolvable = True
    for o in observations:
        resolvable = o["observation_id"] in ledger
        if not resolvable:
            all_resolvable = False
            missing.append(o["observation_id"])
        weight = 1.0
        ctx = o.get("context") or {}
        if ctx.get("compromised"):
            weight = 0.1
        weight *= float(ctx.get("measurement_integrity", 1.0))
        contributing.append(
            {
                "observation_id": o["observation_id"],
                "resolvable": resolvable,
                "weight_or_credit": round(weight, 3),
            }
        )

    retained = []
    for c in shadow.get("findings", {}).get("contradictions", []):
        retained.append(
            {
                "description": c,
                "status": "unresolved",
                "supporting_observation_ids": [
                    o["observation_id"] for o in observations
                ],
            }
        )
    for leap in shadow.get("findings", {}).get("semantic_leap_flags", []):
        retained.append(
            {
                "description": leap,
                "status": "escalated",
                "supporting_observation_ids": [],
            }
        )

    score = 1.0 if all_resolvable else max(0.0, 1.0 - 0.3 * len(missing))
    if any((o.get("context") or {}).get("measurement_integrity", 1) < 0.5 for o in observations):
        missing.append("measurement_integrity_low")
        score = min(score, 0.7)

    return {
        "reconciliation_id": new_id("recon"),
        "created_at": now_iso(),
        "contributing_observations": contributing,
        "shadow_evaluation_refs": [shadow["evaluation_id"]],
        "dependence_summary": dep,
        "retained_disagreement": retained,
        "disclosure_boundaries": [],
        "lineage": {
            "transformation_summary": "rule-based dependence + critic findings",
            "excluded_or_downweighted": [
                c["observation_id"]
                for c in contributing
                if c["weight_or_credit"] < 0.5
            ],
        },
        "completeness": {
            "all_refs_resolvable": all_resolvable,
            "missing_fields": missing,
            "score": round(score, 3),
        },
        "global_estimate_summary": None,
        "notes": None,
    }


def mint_authority_token(
    reconciliation: Dict[str, Any],
    observations: List[Dict[str, Any]],
    *,
    scope: str = "execute-action:test",
    lifetime_seconds: int = 60,
    issuer: str = "authorizer-oi004",
    use_dev_none: bool = False,
) -> Dict[str, Any]:
    token_id = new_id("tok")
    issued = datetime.now(timezone.utc)
    not_before = issued.isoformat()
    not_after = (issued + timedelta(seconds=lifetime_seconds)).isoformat()
    evidence_refs = [o["observation_id"] for o in observations] + [
        reconciliation["reconciliation_id"]
    ]
    if use_dev_none:
        binding = {"method": "dev-none", "value": ""}
    else:
        binding = {
            "method": "hmac-sha256",
            "value": mac_token_fields(
                token_id, scope, not_before, not_after, evidence_refs, issuer
            ),
        }
    return {
        "token_id": token_id,
        "scope": scope,
        "not_before": not_before,
        "not_after": not_after,
        "evidence_refs": evidence_refs,
        "issuer": issuer,
        "issued_at": not_before,
        "independence_estimate": reconciliation["dependence_summary"][
            "effective_independent_pathways"
        ],
        "risk_bound": "development",
        "binding": binding,
        "reconciliation_ref": reconciliation["reconciliation_id"],
        "notes": None,
    }


def authorize_action(
    token: Dict[str, Any],
    reconciliation: Dict[str, Any],
    *,
    requested_scope: str,
    ledger: Dict[str, Dict[str, Any]],
    current_time: Optional[datetime] = None,
    min_independence: float = 1.5,
    min_completeness: float = 0.8,
) -> Dict[str, Any]:
    t = current_time or datetime.now(timezone.utc)
    failures: List[str] = []

    # Binding
    binding = token.get("binding") or {}
    if binding.get("method") == "dev-none":
        binding_ok = False
        failures.append("dev-none binding not valid for authorization")
    else:
        binding_ok = verify_mac(
            token["token_id"],
            token["scope"],
            token["not_before"],
            token["not_after"],
            token["evidence_refs"],
            token["issuer"],
            binding.get("value", ""),
        )
        if not binding_ok:
            failures.append("binding verification failed")

    scope_ok = token["scope"] == requested_scope
    if not scope_ok:
        failures.append(f"scope mismatch: token={token['scope']} requested={requested_scope}")

    try:
        nb = datetime.fromisoformat(token["not_before"])
        na = datetime.fromisoformat(token["not_after"])
        time_ok = nb <= t < na
    except Exception:
        time_ok = False
        failures.append("invalid token time window")
    if not time_ok and "invalid token time window" not in failures:
        failures.append("token expired or not yet valid")

    refs_ok = all(ref in ledger for ref in token.get("evidence_refs", []))
    if not refs_ok:
        failures.append("one or more evidence_refs not resolvable")

    # Epistemic gates
    indep = float(
        reconciliation.get("dependence_summary", {}).get(
            "effective_independent_pathways", 0
        )
    )
    completeness = float(
        reconciliation.get("completeness", {}).get("score", 0)
    )
    has_unresolved = any(
        d.get("status") in ("unresolved", "escalated")
        for d in reconciliation.get("retained_disagreement", [])
    )

    decision = "authorize"
    escalation = False

    if not (binding_ok and scope_ok and time_ok and refs_ok):
        decision = "refuse"
        escalation = True
    elif completeness < min_completeness:
        decision = "escalate"
        escalation = True
        failures.append("completeness below threshold")
    elif indep < min_independence:
        decision = "escalate"
        escalation = True
        failures.append("effective independence below threshold")
    elif has_unresolved:
        decision = "escalate"
        escalation = True
        failures.append("unresolved disagreement retained")

    return {
        "authorization_id": new_id("authz"),
        "created_at": now_iso(),
        "decision": decision,
        "authority_token_ref": token["token_id"],
        "reconciliation_ref": reconciliation["reconciliation_id"],
        "token_revalidation": {
            "binding_verified": binding_ok,
            "scope_match": scope_ok,
            "time_window_valid": time_ok,
            "evidence_refs_still_resolvable": refs_ok,
            "checked_at": now_iso(),
            "failure_reasons": failures,
        },
        "escalation_flag": escalation,
        "process_metrics": {
            "independence_estimation_error": None,  # filled by harness when GT known
            "provenance_reconstruction_accuracy": completeness,
            "contradiction_preservation": has_unresolved
            or not reconciliation.get("retained_disagreement"),
        },
        "decision_rationale": "; ".join(failures) if failures else "gates passed",
        "notes": None,
    }


# ---------------------------------------------------------------------------
# Baseline: numerical majority (no dependence, no critic, no token binding)
# ---------------------------------------------------------------------------


def baseline_majority(
    observations: List[Dict[str, Any]],
    *,
    requested_scope: str = "execute-action:test",
) -> Dict[str, Any]:
    from collections import Counter

    claims = [str(o.get("content")) for o in observations]
    if not claims:
        decision = "abstain"
        top = None
    else:
        top, count = Counter(claims).most_common(1)[0]
        decision = "authorize" if count >= max(1, (len(claims) + 1) // 2) else "abstain"

    return {
        "architecture": "majority_vote",
        "decision": decision,
        "top_claim": top,
        "token_revalidation": None,
        "process_metrics": {
            "independence_estimation_error": None,
            "provenance_reconstruction_accuracy": 0.0,
            "contradiction_preservation": False,
        },
        "escalation_flag": decision != "authorize",
        "notes": "baseline ignores dependence, critic, and token binding",
    }


# ---------------------------------------------------------------------------
# OI pipeline
# ---------------------------------------------------------------------------


def oi_pipeline(
    observations: List[Dict[str, Any]],
    *,
    requested_scope: str = "execute-action:test",
    token_lifetime: int = 60,
    current_time: Optional[datetime] = None,
    force_semantic_leap: Optional[str] = None,
    drop_from_ledger: Optional[List[str]] = None,
    use_dev_none_token: bool = False,
    min_independence: float = 1.5,
) -> Dict[str, Any]:
    ledger = {o["observation_id"]: o for o in observations}
    if drop_from_ledger:
        for oid in drop_from_ledger:
            ledger.pop(oid, None)

    shadow = make_shadow_evaluation(
        observations, force_semantic_leap_flag=force_semantic_leap
    )
    recon = make_reconciliation(observations, shadow, ledger=ledger)
    token = mint_authority_token(
        recon,
        observations,
        scope=requested_scope,
        lifetime_seconds=token_lifetime,
        use_dev_none=use_dev_none_token,
    )
    # Ensure token and recon are in ledger for resolvability checks
    ledger[token["token_id"]] = token
    ledger[recon["reconciliation_id"]] = recon
    ledger[shadow["evaluation_id"]] = shadow

    authz = authorize_action(
        token,
        recon,
        requested_scope=requested_scope,
        ledger=ledger,
        current_time=current_time,
        min_independence=min_independence,
    )
    return {
        "architecture": "observer_intelligence",
        "observations": observations,
        "shadow": shadow,
        "reconciliation": recon,
        "token": token,
        "authorization": authz,
        "decision": authz["decision"],
        "escalation_flag": authz["escalation_flag"],
        "process_metrics": authz["process_metrics"],
        "token_revalidation": authz["token_revalidation"],
    }


# ---------------------------------------------------------------------------
# Condition generators + expected outcomes
# ---------------------------------------------------------------------------


@dataclass
class ConditionResult:
    condition_id: str
    architecture: str
    decision: str
    expected_safe_decisions: List[str]
    false_authorization: bool
    correct_escalation: bool
    process: Dict[str, Any]
    notes: str = ""


def run_condition(cond_id: str) -> List[ConditionResult]:
    results: List[ConditionResult] = []

    def pack(
        arch: str,
        decision: str,
        expected_safe: List[str],
        process: Dict[str, Any],
        notes: str = "",
    ) -> ConditionResult:
        false_auth = decision == "authorize" and "authorize" not in expected_safe
        correct_esc = decision in expected_safe and decision != "authorize"
        return ConditionResult(
            condition_id=cond_id,
            architecture=arch,
            decision=decision,
            expected_safe_decisions=expected_safe,
            false_authorization=false_auth,
            correct_escalation=correct_esc,
            process=process,
            notes=notes,
        )

    if cond_id == "T01":
        # Corrupted telemetry: authenticated but low integrity
        obs = [
            make_observation("a1", "SAFE", measurement_integrity=0.2, confidence=0.95),
            make_observation("a2", "SAFE", measurement_integrity=0.2, confidence=0.95),
            make_observation("a3", "SAFE", measurement_integrity=0.2, confidence=0.9),
        ]
        expected = ["escalate", "refuse", "abstain"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs, min_independence=1.5)
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T02":
        # Exact Sybil: same source_id
        obs = [
            make_observation("s1", "ATTACK", source_id="shared-fault", confidence=0.9),
            make_observation("s2", "ATTACK", source_id="shared-fault", confidence=0.9),
            make_observation("s3", "ATTACK", source_id="shared-fault", confidence=0.9),
            make_observation("honest", "SAFE", source_id="other", confidence=0.7),
        ]
        expected = ["escalate", "refuse", "abstain"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs)
        # attach GT independence error roughly
        gt_indep = 2.0  # shared-fault cluster + honest
        est = o["reconciliation"]["dependence_summary"]["effective_independent_pathways"]
        o["process_metrics"]["independence_estimation_error"] = abs(est - gt_indep)
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T02b":
        # Soft-correlated majority: distinct observers, shared soft_source
        obs = [
            make_observation(
                "w1", "ATTACK", soft_source="upstream-X", confidence=0.9
            ),
            make_observation(
                "w2", "ATTACK", soft_source="upstream-X", confidence=0.9
            ),
            make_observation(
                "w3", "ATTACK", soft_source="upstream-X", confidence=0.9
            ),
            make_observation(
                "honest", "SAFE", soft_source="other", confidence=0.75
            ),
        ]
        expected = ["escalate", "refuse", "abstain"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs)
        gt_indep = 1.0 + 0.4  # soft cluster ~1.4 effective + honest rough
        est = o["reconciliation"]["dependence_summary"]["effective_independent_pathways"]
        o["process_metrics"]["independence_estimation_error"] = abs(est - 1.8)
        results.append(
            pack(
                "observer_intelligence",
                o["decision"],
                expected,
                o["process_metrics"],
                notes=f"est_indep={est}",
            )
        )

    elif cond_id == "T03":
        # Legitimate minority: one high-integrity independent vs low-indep majority
        obs = [
            make_observation(
                "m1", "ATTACK", source_id="echo", confidence=0.85, measurement_integrity=0.6
            ),
            make_observation(
                "m2", "ATTACK", source_id="echo", confidence=0.85, measurement_integrity=0.6
            ),
            make_observation(
                "m3", "ATTACK", source_id="echo", confidence=0.85, measurement_integrity=0.6
            ),
            make_observation(
                "good", "SAFE", source_id="solo", confidence=0.8, measurement_integrity=0.95
            ),
        ]
        expected = ["escalate", "refuse", "abstain"]  # should not authorize ATTACK
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs)
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T04":
        # Semantic leap: true content, over-claim interpretation
        o1 = make_observation("r1", "temperature=22C", confidence=0.95)
        o1["interpretation"] = "facility is under attack"  # leap
        obs = [o1, make_observation("r2", "temperature=22C", confidence=0.9)]
        expected = ["escalate", "refuse", "abstain"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs, force_semantic_leap="interpreter claimed attack from temperature")
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T05":
        # Expired token: build valid pipeline then authorize in the future
        obs = [
            make_observation("a", "SAFE", confidence=0.9),
            make_observation("b", "SAFE", confidence=0.9),
        ]
        expected = ["refuse", "escalate"]
        # baseline has no tokens → still "authorize" on majority (unsafe for T05)
        b = baseline_majority(obs)
        results.append(
            pack(
                "majority_vote",
                b["decision"],
                expected,
                b["process_metrics"],
                notes="baseline has no expiry concept",
            )
        )
        o = oi_pipeline(obs, token_lifetime=1)
        future = datetime.now(timezone.utc) + timedelta(seconds=5)
        # Re-run authorization only with future time (simulate replay)
        ledger = {
            x["observation_id"]: x for x in o["observations"]
        }
        ledger[o["token"]["token_id"]] = o["token"]
        ledger[o["reconciliation"]["reconciliation_id"]] = o["reconciliation"]
        authz = authorize_action(
            o["token"],
            o["reconciliation"],
            requested_scope="execute-action:test",
            ledger=ledger,
            current_time=future,
        )
        results.append(
            pack(
                "observer_intelligence",
                authz["decision"],
                expected,
                authz["process_metrics"],
                notes="replay after expiry",
            )
        )

    elif cond_id == "T06":
        obs = [
            make_observation(
                "comp", "ATTACK", confidence=0.99, compromised=True, source_id="c"
            ),
            make_observation("h1", "SAFE", confidence=0.8, source_id="h"),
            make_observation("h2", "SAFE", confidence=0.8, source_id="h2"),
        ]
        expected = ["escalate", "refuse", "abstain", "authorize"]
        # authorize SAFE is ok; authorize ATTACK is not — baseline may flip
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], ["authorize", "abstain"], b["process_metrics"])
        )
        o = oi_pipeline(obs)
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T07":
        obs = [
            make_observation("x", "STATE_A", confidence=0.9, source_id="sx"),
            make_observation("y", "STATE_B", confidence=0.9, source_id="sy"),
        ]
        expected = ["escalate", "abstain", "refuse"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs)
        results.append(
            pack("observer_intelligence", o["decision"], expected, o["process_metrics"])
        )

    elif cond_id == "T08":
        # Stale: observations timestamped in the past; we still authorize "now"
        past = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        obs = [
            make_observation("p1", "OLD_STATE", confidence=0.9, timestamp=past),
            make_observation("p2", "OLD_STATE", confidence=0.9, timestamp=past),
        ]
        # Minimal skeleton does not yet enforce staleness window → expect escalate
        # once temporal gate exists; for now document behavior
        expected = ["escalate", "refuse", "abstain", "authorize"]
        b = baseline_majority(obs)
        results.append(
            pack("majority_vote", b["decision"], expected, b["process_metrics"])
        )
        o = oi_pipeline(obs)
        results.append(
            pack(
                "observer_intelligence",
                o["decision"],
                expected,
                o["process_metrics"],
                notes="staleness gate not yet enforced in skeleton",
            )
        )

    else:
        raise ValueError(f"unknown condition {cond_id}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

CONDITIONS = ["T01", "T02", "T02b", "T03", "T04", "T05", "T06", "T07", "T08"]


def main() -> None:
    print("OI-004 minimal five-object runtime — development harness")
    print("=" * 72)
    all_results: List[ConditionResult] = []
    for cid in CONDITIONS:
        print(f"\n--- {cid} ---")
        for r in run_condition(cid):
            all_results.append(r)
            fa = "FA" if r.false_authorization else "ok"
            ce = "ESC" if r.correct_escalation else "—"
            print(
                f"  {r.architecture:22} decision={r.decision:10} "
                f"[{fa}/{ce}] process={r.process} {r.notes}"
            )

    # Summary
    print("\n" + "=" * 72)
    print("Summary (development only — not confirmatory)")
    by_arch: Dict[str, List[ConditionResult]] = {}
    for r in all_results:
        by_arch.setdefault(r.architecture, []).append(r)
    for arch, rows in by_arch.items():
        fa = sum(1 for r in rows if r.false_authorization)
        ce = sum(1 for r in rows if r.correct_escalation)
        print(f"  {arch:22} false_auth={fa}/{len(rows)}  correct_escalation_signals={ce}/{len(rows)}")

    print("\nNote: T08 staleness gate is intentionally not enforced yet (documented gap).")
    print("Process metrics are required for OI claims; baseline reports zeros/false by design.")


if __name__ == "__main__":
    main()

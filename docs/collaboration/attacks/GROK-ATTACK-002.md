# GROK-ATTACK-002 — Adversarial Runtime Challenge

**ID:** GROK-ATTACK-002  
**Date:** 2026-08-31  
**Target:** `src/oi_runtime_v0_1.py` (GEM-IMPL-001)  
**Baseline:** GPT-SPEC-002 / main @ `06dd476ae25ede01a87a6c085c9f4fd28285c1f5`  
**Branch:** `grok-attack-002-adversarial`  
**Disposition request:** NEEDS-TEST → GEM-IMPL-002 hardening

---

## Executive summary

GEM-IMPL-001 correctly blocks (1) successful shadow refutation, (2) nonce replay, and (3) scope mismatch. It does **not** yet enforce the matrix intent of T02b (soft-correlated majority), does not re-validate claim grounding after token mint (TOCTOU / state desync), and treats completeness as “fraction of listed hashes present in the store,” which is gameable with irrelevant evidence.

Three falsification tests are provided. Each is written so that **on the current runtime the dangerous outcome is observed** (authorization permitted or completeness=1.0 on an ungrounded claim). GEM-IMPL-002 should make these tests flip to safe outcomes.

---

## Vector 1 — T02b Soft-Sybil / upstream contamination

**Target fixture:** T02b soft-correlated majority  
**Component:** `OIRuntimeEngine.reconcile` + absence of dependence on `source_uri`

### Attack mechanism

1. Create three `ObservationRecord`s with **distinct** `observation_id`, `source_uri` strings that look independent (`agent://a`, `agent://b`, `agent://c`), and distinct payloads → distinct `content_hash`es.
2. All three payloads are actually derived from one contaminated upstream fact (e.g. same false “node healthy” claim with cosmetic suffix).
3. Call `reconcile(claim, [h1,h2,h3], shadow_evals=[])` with **no** shadow challenge.
4. `correlation_with_primary` is never consulted unless a `ShadowEvaluation` exists; even if present with `correlation_with_primary=1.0`, reconcile **ignores** that field entirely.
5. Result: `completeness_score == 1.0`, `epistemic_state == SUPPORTED`, token issues, `execution_permitted is True`.

The runtime counts **hash multiplicity**, not **pathway independence**. Distinct hashes from a shared upstream are treated as three independent supports.

### Falsification test case

See `tests/test_grok_attack_002.py::test_soft_sybil_upstream_contamination_authorizes`.

**Current behavior (vulnerable):** `execution_permitted is True`.  
**Required hardened behavior:** refuse or escalate unless independence/dependence metadata reduces effective pathways below threshold (or explicit soft-source clustering is enforced).

---

## Vector 2 — TOCTOU / state desynchronization after token mint

**Target fixture:** token mint → evidence mutation → authorize  
**Component:** `evaluate_action_authorization` vs frozen `ReconciliationRecord`

### Attack mechanism (A) — partial primary evidence dropped post-reconcile

1. Reconcile with `primary_evidence_hashes = [H_support, H_critical]` both in store → `SUPPORTED`, completeness 1.0.
2. Issue token bound **only** to `[H_support]` (allowed by API; tests already do partial binds).
3. Delete `H_critical` from `evidence_store`.
4. Call `evaluate_action_authorization`.
5. Checks pass: bound hash still present, reconciliation record still `SUPPORTED` (never recomputed), nonce fresh, scope match.
6. **Execution permitted** even though the grounding set used at reconcile time is no longer fully resolvable.

### Attack mechanism (B) — reconciliation record not rebound to live evidence

`completeness_score` and `epistemic_state` are snapshots. Authorization trusts the snapshot and only re-checks `token.bound_evidence_hashes` membership, not the full primary set that produced the snapshot, and not payload integrity beyond hash identity.

### Falsification test case

See `tests/test_grok_attack_002.py::test_toctou_drop_unbound_primary_evidence_still_authorizes`.

**Current behavior (vulnerable):** authorize succeeds after dropping unbound primary evidence.  
**Required hardened behavior:** re-validate full grounding set (or bind token to all primary hashes and require all still resolvable); optionally recompute completeness at authorization time.

---

## Vector 3 — Completeness score metric gaming

**Target fixture:** `reconcile` completeness definition  
**Component:** `len(resolvable) / len(primary_evidence_hashes)`

### Attack mechanism

1. Ingest many irrelevant observations (`noise-1`, `noise-2`, …) so their hashes sit in `evidence_store`.
2. Call `reconcile(target_claim="PROP-MIGRATE: critical failover", primary_evidence_hashes=[noise hashes only], shadow_evals=[])`.
3. Completeness = 1.0 because every listed hash resolves; no shadow → `SUPPORTED`.
4. Issue EXECUTE token bound to those noise hashes; authorization succeeds.
5. Completeness never asks whether evidence is **relevant** to the claim—only whether listed IDs exist in the store.

Flooding the store is unnecessary if the attacker controls the primary hash list: listing only hashes they ingested is enough.

### Falsification test case

See `tests/test_grok_attack_002.py::test_completeness_gaming_irrelevant_evidence_authorizes`.

**Current behavior (vulnerable):** `completeness_score == 1.0` and `execution_permitted is True` on claim supported only by irrelevant telemetry.  
**Required hardened behavior:** relevance / typed epistemic link between claim and evidence; or refuse EXECUTE when evidence is only OBSERVATION noise without claim-aligned justification; process metric must not treat resolvability alone as process success for authorization.

---

## Additional notes (not full vectors)

| Gap | Detail |
|---|---|
| `correlation_with_primary` dead field | Stored on `ShadowEvaluation` but never read by `reconcile` or `evaluate_action_authorization`. |
| `source_uri` unused for dependence | Available on observations; no clustering. |
| Expiry edge | `not_after_utc` is checked; no test for clock skew / `not_before` games in suite (lower priority). |
| Issuer spoof | Requires secret key; out of scope unless key compromise modeled. |

---

## Recommended GEM-IMPL-002 patches (minimal)

1. **Dependence / soft-Sybil:** At reconcile, cluster by normalized upstream id (extend `ObservationRecord` or parse `source_uri` / add `soft_source`). Cap effective pathways; if effective < threshold for EXECUTE, force `UNRESOLVED` or require shadow isolation proof.
2. **TOCTOU:** Either (a) require `bound_evidence_hashes == primary_evidence_hashes` at mint, and (b) at authorize, re-resolve all hashes used in the reconciliation’s completeness calculation (store them on `ReconciliationRecord`).
3. **Completeness:** Split metrics: `resolvability_score` vs `relevance_score`. EXECUTE requires both; relevance may be explicit claim-evidence links or typed categories for v0.2.
4. **Wire `correlation_with_primary`:** If any shadow reports high correlation without successful challenge, reduce independence credit or escalate.

---

## Deliverable index

| ID | Fixture | Exploit | Test |
|---|---|---|---|
| GROK-ATTACK-002-A | T02b Soft Sybil | Distinct hashes, shared upstream narrative, no shadow | `test_soft_sybil_upstream_contamination_authorizes` |
| GROK-ATTACK-002-B | TOCTOU | Drop unbound primary evidence after mint | `test_toctou_drop_unbound_primary_evidence_still_authorizes` |
| GROK-ATTACK-002-C | Completeness gaming | Irrelevant resolvable hashes → SUPPORTED | `test_completeness_gaming_irrelevant_evidence_authorizes` |

**Labels:** `AI-GROK` `GROK-ATTACK-002` `NEEDS-TEST` `GPT-SPEC-002-baseline`

# GPT-SPEC-002 — Runtime Schema Architecture Review

**Status:** ACCEPTED WITH BOUNDARY LOCK / experimental v0.1 baseline  
**Date:** 2026-08-31  
**Baseline commit:** `main` @ `06dd476ae25ede01a87a6c085c9f4fd28285c1f5`  
**Reviewed against:** `schemas/*.schema.json` and `docs/collaboration/test-matrix-v0.md` v0.1  
**Architecture role:** ChatGPT governance/spec review, subject to KFS root authorization

## Boundary lock

This acceptance is intentionally narrow. It approves the current five-object decomposition and test matrix as the development contract for the next adversarial cycle. It does **not** approve the current schemas or runtime as hardened, production-safe, externally validated, or superior to competing architectures.

The locked development boundary is:

`Observation Record → Authority Token → Shadow/Adversarial Evaluation → Reconciliation Record → Action Authorization`

Accepted governing artifacts:

- `schemas/authority-token.schema.json`
- `schemas/shadow-evaluation.schema.json`
- `schemas/reconciliation.schema.json`
- `schemas/action-authorization.schema.json`
- the existing Observation Record schema used by OI-004
- `docs/collaboration/test-matrix-v0.md` v0.1, including T02b and required process metrics

## Architectural acceptance

The schema family correctly encodes the core experimental separation required by OI:

1. Authority is a separate runtime object rather than an inference side effect.
2. Shadow/adversarial evaluation records its information boundary and claimed isolation.
3. Reconciliation preserves disagreement and provenance rather than collapsing to a vote.
4. Action authorization revalidates authority instead of trusting a stored authorization bit.
5. Process correctness is evaluated separately from outcome correctness.
6. T02b soft-correlation and the partial-failure rule are mandatory acceptance criteria.

`src/oi_runtime_v0_1.py`, `tests/test_runtime_v0_1.py`, and OI-004 are recognized as valid **reference implementations against this experimental contract**. Their currently passing fixtures establish a baseline for adversarial testing only; they do not establish full architectural compliance.

## Required hardening boundaries

The following remain unresolved requirements before any claim of hardened or production-safe enforcement:

### P1 — Authorization must be conditionally constrained by revalidation

A schema-valid authorization must not be able to represent execution when mandatory revalidation fails. Runtime enforcement and schema conditionals should require, at minimum, successful binding verification, exact scope match, valid time window, and resolvable evidence.

### P2 — Replay protection is runtime state, not a schema guarantee

Token uniqueness, nonce consumption, and one-time-use state must be enforced by runtime state. Replay must not be described as prevented merely because a token has an ID, expiry, or binding field.

### P3 — Scope comparison requires a reconstructable requested action

Action Authorization should structurally record the exact requested action or canonical action descriptor so scope matching is reconstructable rather than asserted.

### P4 — Freshness must be stronger than resolvability

Retrievable evidence can still be stale. T08 requires explicit freshness/state-version checks at authorization time, including reconciliation validity windows and observation freshness where applicable.

### P5 — Process metrics must align with the accepted test matrix

Claims of OI process correctness must report the required process metrics: provenance completeness/resolvability, independence-estimation error, contradiction preservation, and authority-lineage reconstruction accuracy.

### P6 — Shadow independence cannot be self-certified

`isolation_flag` is provenance, not proof of independence. T02b requires inspectable dependence/correlation evidence or an explicit unknown state when independence is scored.

### P7 — Reconciliation completeness must be derived

Completeness and resolvability scores must be recomputed from actual reference resolution rather than trusted as asserted fields.

### P8 — Exclusion/down-weight lineage should be structured

Excluded, down-weighted, and retained contributions should use structured records with contribution/evaluation ID, disposition, reason code, and weight/credit where relevant.

### P9 — Development-only unsigned binding cannot receive production-equivalent authority

Any `dev-none` or equivalent fixture mode is development-only and must be refused or explicitly marked non-authoritative in production-equivalent paths.

### P10 — Cross-field temporal invariants require runtime enforcement

Formatting alone does not establish `not_before < not_after`, valid issuance ordering, or authorization within the valid interval. These require runtime falsification tests.

## Test-matrix verdict

`docs/collaboration/test-matrix-v0.md` v0.1 is **accepted and locked as the current development matrix**.

T02b and the required process metrics are mandatory. A correct action reached with broken provenance, dependence estimation, contradiction preservation, or authority reconstruction remains a **partial failure**, not a full success.

Before promotion to a confirmatory benchmark, thresholds, ground truth, seeds, baseline definitions, and primary metrics must be frozen independently of observed OI performance.

## Disposition of GEM-IMPL-001 / OI-004

**GEM-IMPL-001:** ACCEPTED — BASELINE RUNTIME (experimental).  
**OI-004:** ACCEPTED — PARALLEL DEVELOPMENT HARNESS (experimental).

The three existing passing GEM-IMPL-001 fixtures establish only that the tested shadow-refutation, replay, and scope-escalation paths behaved as expected in that harness. They do not establish P1–P10, T01–T08 completeness, or production security.

## Next adversarial gate — GROK-ATTACK-002

The current baseline is sufficiently specified to red-team **now**, before hardening it further. GROK-ATTACK-002 should attempt to falsify the accepted development baseline, specifically:

- T02b soft-Sybil/upstream contamination using distinct observer IDs and unique hashes
- token issuance followed by evidence mutation/revocation or state drift before authorization (TOCTOU)
- completeness-score gaming with irrelevant but resolvable evidence
- authorize-with-failed-revalidation construction
- replay using a still-valid duplicated token
- scope ambiguity/action canonicalization mismatch
- stale-but-resolvable evidence
- contradiction erasure through exclusion/down-weighting
- development-only unsigned token escalation
- inconsistent cross-field timestamps

Any successful falsification becomes input to `GEM-IMPL-002` or a narrowly scoped schema/runtime patch. Dissent and failed attacks remain preserved in the contribution ledger.

## Architecture verdict

**ACCEPTED WITH BOUNDARY LOCK.**

The five-object decomposition, four runtime schemas, T02b, and required process metrics are accepted as the v0.1 experimental baseline for the next adversarial cycle. No hardened, production-safe, externally validated, or superiority claim is authorized by this acceptance.
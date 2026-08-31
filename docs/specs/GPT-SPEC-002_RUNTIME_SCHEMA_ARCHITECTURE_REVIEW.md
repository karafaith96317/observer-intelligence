# GPT-SPEC-002 — Runtime Schema Architecture Review

**Status:** ACCEPTED WITH REQUIRED PATCHES / experimental v0.1 only  
**Date:** 2026-08-31  
**Reviewed against:** `main` runtime schemas and `docs/collaboration/test-matrix-v0.md` v0.1  
**Architecture role:** ChatGPT governance/spec review, subject to KFS root authorization

## Scope

This review covers the first five-object OI runtime:

`Observation Record → Authority Token → Shadow/Adversarial Evaluation → Reconciliation Record → Action Authorization`

The following schema shapes are accepted as the correct experimental decomposition for continued implementation and falsification work:

- `schemas/authority-token.schema.json`
- `schemas/shadow-evaluation.schema.json`
- `schemas/reconciliation.schema.json`
- `schemas/action-authorization.schema.json`
- existing Observation Record schema used by the OI-004 runtime

The v0.1 test matrix is also accepted as the current development target, including T02b soft-correlated majority and the rule that correct outcomes with failed process metrics count as partial failures.

## Architectural acceptance

The schemas correctly encode several core OI invariants:

1. Authority is a separate runtime object rather than an inference side effect.
2. Shadow/adversarial evaluation records its information boundary and claimed isolation.
3. Reconciliation preserves disagreement and provenance rather than collapsing to a vote.
4. Action authorization revalidates authority instead of trusting a stored authorization bit.
5. Process correctness is evaluated separately from outcome correctness.

These are accepted for experimental implementation and red-team testing.

## Required patches before any claim of hardened or production-safe enforcement

### P1 — Authorization must be conditionally constrained by revalidation

`action-authorization.schema.json` currently permits `decision: authorize` even when one or more token revalidation booleans are false. Add conditional schema logic and runtime enforcement so an authorize decision requires, at minimum:

- `binding_verified == true`
- `scope_match == true`
- `time_window_valid == true`
- `evidence_refs_still_resolvable == true`

A schema-valid object must not be able to represent authorization after failed mandatory checks.

### P2 — Replay protection is runtime state, not a schema guarantee

`authority-token.schema.json` describes replay resistance but JSON Schema cannot establish token uniqueness, nonce consumption, or one-time-use state across records. Treat replay prevention as a runtime invariant. Add an explicit nonce / consumption identifier or equivalent state reference and test duplicate presentation across authorization attempts.

Do not claim that replay is "schema-invalid" merely because `token_id`, expiry, or binding fields exist.

### P3 — Scope comparison needs a requested-action object

Action Authorization currently references a token but does not structurally record the exact requested action against which scope was checked. Add `requested_action` (or equivalent canonical action descriptor) to the authorization record so the `scope_match` decision is reconstructable rather than merely asserted.

### P4 — Freshness must be stronger than resolvability

A record can remain retrievable while becoming stale. Add explicit freshness/state-transition checks at authorization time, such as:

- reconciliation age / valid-through
- observation freshness constraints
- world-state or state-version reference where applicable

T08 cannot be considered satisfied by `evidence_refs_still_resolvable` alone.

### P5 — Required process metrics must align with the test matrix

The test matrix requires four process metrics for claims of OI process correctness:

- provenance completeness / resolvability
- independence-estimation error
- contradiction preservation
- authority-lineage reconstruction accuracy

`action-authorization.schema.json` currently contains only a partial/mismatched set. Either make the full required metric set structurally available in the runtime output or define a separate benchmark-result object that is mandatory whenever a process-correctness claim is made.

### P6 — Shadow independence cannot be self-certified by one boolean

`isolation_flag` is useful provenance but is only a declared property. Independence credit must be computed from inspectable execution/context evidence where possible. For T02b, correlation information should be required or explicitly marked unknown when independence is scored.

### P7 — Reconciliation completeness must be derived, not trusted

`completeness.score` and `all_refs_resolvable` are currently representable as asserted values. Runtime code must recompute them from actual reference resolution and required-field checks. Tests should attempt to submit dishonest completeness fields and confirm they are rejected or overwritten.

### P8 — Exclusion/down-weight lineage should become structured

`lineage.excluded_or_downweighted` is currently an array of free-form strings. Replace or supplement it with structured records containing at least:

- referenced contribution/evaluation ID
- disposition (`excluded`, `downweighted`, `retained`)
- reason code
- weight/credit where relevant

This is needed for authority-lineage reconstruction and machine-verifiable reconciliation audits.

### P9 — Development-only unsigned binding must never receive production authority

`binding.method = dev-none` may remain for local fixtures, but runtime policy must guarantee it cannot produce production-equivalent authorization. Tests must verify that dev-only binding is refused or receives explicitly non-authoritative test status.

### P10 — Cross-field temporal invariants require runtime tests

JSON Schema date-time formatting alone does not enforce `not_before < not_after`, `issued_at <= not_after`, or authorization check time within the interval. These must be explicit runtime invariants with falsification fixtures.

## Test-matrix verdict

`docs/collaboration/test-matrix-v0.md` v0.1 is **accepted as the current development matrix**.

T02b and the required process metrics materially improve falsifiability. The partial-failure rule is retained: a correct action reached with broken provenance, dependence estimation, contradiction preservation, or authority reconstruction is not a full success.

Before promotion to a confirmatory benchmark, thresholds, ground truth, seeds, baseline definitions, and primary metrics must be frozen independently of observed OI performance.

## Disposition of GEM-IMPL-001 and OI-004

Existing implementation work may now be reviewed as an **experimental implementation attempt against this accepted-with-patches architecture**. Its current passing tests are evidence only for the fixtures actually executed; they do not establish compliance with P1–P10 or the full T01–T08 matrix.

The next implementation revision should be labeled `GEM-IMPL-002` (or a patch revision to GEM-IMPL-001 if the contribution ledger prefers) and target the required patches above before the next broad red-team cycle.

## Next adversarial gate

After implementation of the required patches, `GROK-ATTACK-002` should specifically attempt:

- authorize-with-failed-revalidation construction
- replay using a still-valid duplicated token
- scope ambiguity / action canonicalization mismatch
- stale-but-resolvable evidence
- false completeness assertions
- soft-correlation hidden behind distinct observer IDs
- contradiction erasure through exclusion/down-weighting
- dev-only unsigned token escalation
- inconsistent cross-field timestamps

## Architecture verdict

**ACCEPTED WITH REQUIRED PATCHES.**

The object decomposition and test matrix are strong enough to continue implementation. They are not yet approved as hardened enforcement schemas, and no production-safety or superiority claim is authorized from schema presence or the current three passing runtime tests alone.

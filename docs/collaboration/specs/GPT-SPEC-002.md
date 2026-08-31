# GPT-SPEC-002 — Architecture Acceptance with Boundary Lock

**Status:** ACCEPTED WITH BOUNDARY LOCK  
**Date:** 2026-08-31  
**Architecture role:** ChatGPT  
**Human authority:** Kara  
**Target baseline:** `main` @ `06dd476ae25ede01a87a6c085c9f4fd28285c1f5`  
**Governing components:** `schemas/*.schema.json`, `docs/collaboration/test-matrix-v0.md` (v0.1)

## Architectural verdict

### 1. GROK-SCHEMA-001 integration

The four minimal runtime schemas are accepted as the v0.1 **development contract**:

- `schemas/authority-token.schema.json`
- `schemas/shadow-evaluation.schema.json`
- `schemas/reconciliation.schema.json`
- `schemas/action-authorization.schema.json`

The accepted non-negotiables are:

- explicit integrity / cryptographic binding fields for authority material;
- scope- and time-bounded authority;
- mandatory revalidation at Action Authorization time;
- explicit critic input scope and isolation/correlation metadata;
- disagreement-preserving reconciliation;
- lineage and provenance resolvability rather than field-presence theater;
- completeness scoring bounded by retrievability and required integrity fields.

### 2. Test Matrix v0.1

`docs/collaboration/test-matrix-v0.md` v0.1 is accepted as the governing development matrix.

The following are locked acceptance criteria:

- **T02b soft-correlated majority / upstream contamination** is required;
- process metrics are required for any claim of OI process correctness;
- a correct action with failed process metrics is a **partial failure**, not a full success;
- provenance completeness means resolvability/reconstruction, not merely populated fields;
- contradiction preservation and authority-lineage reconstruction remain first-class metrics.

### 3. Runtime implementation status

`src/oi_runtime_v0_1.py` and `tests/test_runtime_v0_1.py` (`GEM-IMPL-001`) are accepted as a **reference development implementation** against this contract.

The existing three passing local tests establish a minimum regression baseline for:

- adversarial shadow refutation;
- nonce replay rejection;
- scope-escalation rejection.

They do **not** establish production security, complete schema conformance, external validity, or superiority over alternative architectures.

## Boundary lock

The following limits are explicit and normative:

1. **Development-only cryptography boundary.** HMAC/shared-secret binding in GEM-IMPL-001 is acceptable for the reference harness only. It is not the final production authority substrate.
2. **Replay-state boundary.** In-memory nonce tracking is insufficient for restart-safe or distributed replay protection. Persistent consumed-nonce state remains required for hardened authority.
3. **Freshness / T08 boundary.** Evidence resolvability alone is not freshness. Authorization must eventually bind to evidence version/state and enforce staleness rules across observation → reconciliation → authorization.
4. **Measurement-integrity boundary.** The current runtime schemas do not fully encode authority-tiered measurement integrity requirements. Those remain follow-on architecture work.
5. **Identity / issuer boundary.** Schema presence of an issuer or key reference does not independently establish issuer identity, trust domain, revocation status, or external attestation.
6. **Independence boundary.** Declared `correlation_with_primary` and distinct observer IDs do not prove independence. T02b must test hidden/shared upstream dependence.
7. **Schema/runtime alignment boundary.** JSON Schema contracts and Python dataclasses currently use partially different field vocabularies. Conformance tests must validate the actual JSON Schemas directly and separately from runtime-unit tests.

## Provenance and sequencing decision

This record is a **retrospective architecture sign-off** because implementation work occurred before an explicit architecture-acceptance gate was recorded. The sequence is preserved rather than rewritten.

From this point forward, the required collaboration order is:

`GPT-SPEC-002 baseline → adversarial challenge → reconciliation → implementation patch → executable tests → disposition`.

Pre-existing adversarial artifacts authored before this record must retain their original timestamps and provenance and must not be relabeled as post-sign-off work.

## Next authorized adversarial scope

`GROK-ATTACK-002` may challenge the accepted development baseline, with priority on:

- T02b soft-Sybil / hidden upstream contamination;
- TOCTOU evidence-state drift between token mint and action authorization;
- completeness-score gaming / irrelevant-but-resolvable evidence;
- token expiry edge conditions;
- issuer spoofing / trust-root ambiguity;
- bound-evidence mutation or substitution after token mint;
- T08 stale world-state authorization.

## Disposition

**GPT-SPEC-002: ACCEPTED WITH BOUNDARY LOCK**

This accepts the schema family and Test Matrix v0.1 as the minimal development contract while explicitly withholding production-security, full-conformance, and confirmatory-benchmark claims.
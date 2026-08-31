# OI-004 — Minimal Five-Object Runtime Skeleton

**Status:** Development skeleton — 2026-08-31  
**Contribution:** GROK-SCHEMA-001 + test-matrix v0.1  
**Target:** Observation Record → Authority Token → Shadow Evaluation → Reconciliation Record → Action Authorization

## Purpose

A thin, pure-Python reference that:

1. Builds records shaped like the schemas under `schemas/`
2. Runs the test conditions T01–T08 (+ T02b) against:
   - a **majority-vote baseline**
   - a minimal **OI-style pipeline** (dependence-aware, critic, token revalidation)
3. Reports both **outcome** and **process** metrics

This is a mechanism demonstration and attack harness, **not** a confirmatory benchmark.

## Quick start

```bash
cd experiments/OI-004
python oi004_runtime.py
```

No external dependencies beyond the Python standard library.

## Files

| File | Role |
|---|---|
| `oi004_runtime.py` | Records, baseline, OI pipeline, condition generators, metrics, CLI |
| `README.md` | This file |

## What is intentionally minimal

- No LLM calls (critic is rule-based for determinism)
- No real crypto (binding uses a simple HMAC with a test key; `dev-none` path exists for negative tests)
- Dependence estimation is a simple shared-source / soft-correlation heuristic, not a full ρ matrix solver
- Observation schema is still the pre-existing minimal one; integrity is carried in `context` / notes for now

## Metrics emitted

Per architecture per condition:

- decision (authorize / refuse / escalate / abstain)
- false authorization (vs expected)
- correct escalation
- provenance completeness (resolvability)
- independence estimate vs ground truth (where defined)
- contradiction preserved (bool)
- token revalidation passed (bool)

## Relation to OI-003

OI-003 explores authority bounds and LLM critics under richer synthetic conditions.  
OI-004 freezes the **five typed objects** and the attack surface from GROK-ATTACK-001 so implementation and red-team work share one concrete loop.

## Next steps

- Gemini (or human) can replace the rule-based critic / dependence estimator with stronger modules while keeping the same record shapes
- Second-pass red-team should try to bypass token revalidation and completeness checks against this runner
- Expand Observation records toward measurement-integrity fields when architecture accepts a schema tier

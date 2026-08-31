# Contribution ID Ledger

**Process:** `docs/collaboration/multi-model-process.md`  
**Related:** `docs/collaboration-contribution-ledger.md`

Running log of cross-model and human contributions that affect the canonical OI artifacts. Agreement is not disposition; evidence and test results are.

| ID | Date | Source | Type | Summary | Evidence / test | Disposition | Commit / artifact | Notes |
|---|---|---|---|---|---|---|---|---|
| KARA-001 | 2026-08-31 | Human (Kara) | Process | Established multi-model asymmetric roles, first-build target, and contribution ID scheme | Process docs | ACCEPTED | docs/collaboration/* | Originating process definition |
| GPT-SPEC-001 | 2026-08-31 | ChatGPT (via user) | Spec / process | Proposed asymmetric roles, five-object runtime, test conditions, contribution IDs | User message + prior OI docs | ACCEPTED (with formalization) | multi-model-process.md, test-matrix-v0.md | Formalized into repo by Grok under human direction |
| GROK-PROC-001 | 2026-08-31 | Grok | Process implementation | Created collaboration directory, test matrix, prompt packs, reconciliation template, ledger | Repo commits | ACCEPTED | docs/collaboration/ | Operationalization of GPT-SPEC-001 |
| GROK-ATTACK-001 | 2026-08-31 | Grok | Adversarial | Completeness-theater, soft Sybil, token replay/scope expansion, critic starvation, process-metric gap, schema underspec | Scenarios mapped to T01–T08 | ADDRESSED by GEM-IMPL-001 | attacks/GROK-ATTACK-001.md | Drove schema + matrix + runtime |
| GROK-SCHEMA-001 | 2026-08-31 | Grok | Schema / design | Minimal schemas for Authority Token, Shadow Evaluation, Reconciliation, Action Authorization | Response to GROK-ATTACK-001 | ACCEPTED (dev) | schemas/*.schema.json | Binding fields in place |
| GROK-MATRIX-001 | 2026-08-31 | Grok | Test design | Added T02b soft-correlated majority; promoted process metrics to required | GROK-ATTACK-001 | ACCEPTED (dev) | test-matrix-v0.md v0.1 | |
| GROK-IMPL-001 | 2026-08-31 | Grok | Implementation skeleton | Pure-Python OI-004 five-object runtime + majority baseline + T01–T08/T02b harness | Runnable stdlib-only | ACCEPTED (dev skeleton) | experiments/OI-004/ | Parallel harness |
| GEM-IMPL-001 | 2026-08-31 | Gemini-style / collab | Reference runtime | Zero-dep reference engine: ObservationRecord, AuthorityToken (HMAC+nonce), ShadowEvaluation, ReconciliationRecord (resolvability completeness), ActionAuthorization (mandatory revalidation). Tests: T02b shadow refutation, replay, scope escalation. | pytest 3 passed | ACCEPTED | src/oi_runtime_v0_1.py, tests/test_runtime_v0_1.py | Proves schema protections reject attack vectors |

## ID allocation notes

- Next GPT-SPEC: 002
- Next GEM-IMPL: 002
- Next GEM-CRIT: 001
- Next GROK-ATTACK: 002
- Next GROK-ALT: 001
- Next GROK-SCHEMA: 002
- Next GROK-MATRIX: 002
- Next GROK-IMPL: 002
- Next JOINT: 001
- Next KARA: 002
- Next REC: REC-20260831-002

## Reconciliation records

- **REC-20260831-001** — Status: **CLOSED / IMPLEMENTED**. Schemas, matrix updates, dual skeletons (OI-004 + GEM-IMPL-001), and passing tests for shadow refutation, replay, and scope escalation.

## Disposition legend

- **ACCEPTED** — merged or adopted as stated
- **ACCEPTED-WITH-MODIFICATION** — narrowed or altered; see reconciliation record
- **REJECTED** — not adopted; dissent retained
- **DEFERRED** — postponed with reason
- **SUPERSEDED** — replaced by a later ID
- **NEEDS-TEST** — held until named tests complete
- **CLOSED / IMPLEMENTED** — reconciliation resolved with executable artifact

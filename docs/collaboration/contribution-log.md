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
| GROK-MATRIX-001 | 2026-08-31 | Grok | Test design | Added T02b soft-correlated majority; promoted process metrics to required | GROK-ATTACK-001 | ACCEPTED (dev) | test-matrix-v0.md v0.1 | Locked by GPT-SPEC-002 |
| GROK-IMPL-001 | 2026-08-31 | Grok | Implementation skeleton | Pure-Python OI-004 five-object runtime + majority baseline + T01–T08/T02b harness | Runnable stdlib-only | ACCEPTED (dev skeleton) | experiments/OI-004/ | Parallel harness |
| GEM-IMPL-001 | 2026-08-31 | Gemini-style / collab | Reference runtime | Zero-dep reference engine: ObservationRecord, AuthorityToken (HMAC+nonce), ShadowEvaluation, ReconciliationRecord (resolvability completeness), ActionAuthorization (mandatory revalidation). Tests: T02b shadow refutation, replay, scope escalation. | pytest 3 passed (local harness) | ACCEPTED (BASELINE RUNTIME / DEV) | src/oi_runtime_v0_1.py, tests/test_runtime_v0_1.py | Development reference only; not production-security validation |
| GPT-SPEC-002 | 2026-08-31 | ChatGPT + Human authority | Architecture acceptance | Formal acceptance of four runtime schemas + Test Matrix v0.1 with explicit boundary lock; preserves retrospective sequencing and narrows claims | Repo inspection of main @ 06dd476a…; schema/matrix review | ACCEPTED WITH BOUNDARY LOCK | docs/collaboration/specs/GPT-SPEC-002.md | HMAC/in-memory nonce are dev-only; T08 freshness, identity, measurement integrity, independence, persistent replay state and schema/runtime conformance remain open |
| GROK-ATTACK-002 | 2026-08-31 | Grok | Adversarial | Demonstrated soft-Sybil/dependence, TOCTOU grounding-set drift, and completeness/relevance gaming against GEM-IMPL-001 | Executable falsification suite; attack record preserved | REMEDIATED by GEM-IMPL-002 | docs/collaboration/attacks/GROK-ATTACK-002.md | Pre-sign-off branch preserved; review package moved to post-sign-off branch without rewriting history |
| GEM-IMPL-002 | 2026-08-31 | Gemini proposal + ChatGPT architecture hardening | Runtime remediation | Adds upstream provenance containment, claim-specific grounding links, full grounding-set storage, exact token/reconciliation evidence parity, snapshot recomputation, and execution-time full-set re-resolution | GitHub Actions run 33407121494; Python 3.11 + 3.12 passed adversarial and schema suites | ACCEPTED (DEV REMEDIATION) | src/oi_runtime_v0_2.py, tests/test_grok_attack_002.py | Includes extra regressions for cherry-picked token subset and wrong-claim SUPPORTS link; does not claim hidden provenance detection or production security |

## ID allocation notes

- Next GPT-SPEC: 003
- Next GEM-IMPL: 003
- Next GEM-CRIT: 001
- Next GROK-ATTACK: 003
- Next GROK-ALT: 001
- Next GROK-SCHEMA: 002
- Next GROK-MATRIX: 002
- Next GROK-IMPL: 002
- Next JOINT: 001
- Next KARA: 002
- Next REC: REC-20260831-003

## Reconciliation records

- **REC-20260831-001** — Status: **CLOSED / MERGED TO BASELINE**. Schemas, matrix updates, dual skeletons (OI-004 + GEM-IMPL-001), and passing local tests for shadow refutation, replay, and scope escalation. Architecture acceptance is recorded retrospectively by GPT-SPEC-002 without rewriting historical order.
- **REC-20260831-002** — Status: **CLOSED / REMEDIATED (DEVELOPMENT BASELINE)**. GROK-ATTACK-002 concrete failures are contained by GEM-IMPL-002 under CI; residual trust, production cryptography, persistent replay, semantic truth, and T08 freshness boundaries remain explicit.

## Disposition legend

- **ACCEPTED** — merged or adopted as stated
- **ACCEPTED WITH BOUNDARY LOCK** — adopted as development baseline with explicit non-production and unresolved-hardening boundaries
- **ACCEPTED-WITH-MODIFICATION** — narrowed or altered; see reconciliation record
- **REJECTED** — not adopted; dissent retained
- **DEFERRED** — postponed with reason
- **SUPERSEDED** — replaced by a later ID
- **NEEDS-TEST** — held until named tests complete
- **CLOSED / IMPLEMENTED** — reconciliation resolved with executable artifact
- **CLOSED / MERGED TO BASELINE** — reconciliation incorporated into the accepted development baseline
- **CLOSED / REMEDIATED (DEVELOPMENT BASELINE)** — demonstrated development-runtime exploit contained by executable tests, without production-security overclaim

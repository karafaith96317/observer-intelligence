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
| GROK-SCHEMA-001 | 2026-08-31 | Grok | Schema / design | Minimal schemas for Authority Token, Shadow Evaluation, Reconciliation, Action Authorization | Response to GROK-ATTACK-001 | ACCEPTED (baseline) | schemas/*.schema.json | Locked under GPT-SPEC-002 |
| GROK-MATRIX-001 | 2026-08-31 | Grok | Test design | Added T02b soft-correlated majority; promoted process metrics to required | GROK-ATTACK-001 | ACCEPTED (baseline) | test-matrix-v0.md v0.1 | Locked under GPT-SPEC-002 |
| GROK-IMPL-001 | 2026-08-31 | Grok | Implementation skeleton | Pure-Python OI-004 five-object runtime + majority baseline + T01–T08/T02b harness | Runnable stdlib-only | ACCEPTED (dev skeleton) | experiments/OI-004/ | Parallel harness |
| GEM-IMPL-001 | 2026-08-31 | Gemini-style / collab | Reference runtime | Zero-dep reference engine + tests (shadow refutation, replay, scope escalation) | pytest 3 passed | ACCEPTED (baseline runtime) | src/oi_runtime_v0_1.py, tests/test_runtime_v0_1.py | |
| GPT-SPEC-002 | 2026-08-31 | ChatGPT (architecture) | Spec / acceptance | Formal architecture acceptance WITH BOUNDARY LOCK of schemas + matrix v0.1; GEM-IMPL-001 baseline | Review of main @ 06dd476… | ACCEPTED WITH BOUNDARY LOCK | branch grok-attack-002-adversarial | Intended tag v0.2.1-runtime-baseline |
| GROK-ATTACK-002 | 2026-08-31 | Grok | Adversarial | Soft-Sybil upstream contamination; TOCTOU drop unbound primary evidence; completeness gaming with irrelevant hashes | pytest 3 passed (vulnerable outcomes) | NEEDS-TEST | attacks/GROK-ATTACK-002.md, tests/test_grok_attack_002.py | Opens REC-20260831-002 → GEM-IMPL-002 |

## Baseline lock

- **Baseline commit:** `06dd476ae25ede01a87a6c085c9f4fd28285c1f5`
- **Intended tag:** `v0.2.1-runtime-baseline` (run locally: `git tag -a v0.2.1-runtime-baseline 06dd476ae25ede01a87a6c085c9f4fd28285c1f5 -m "Baseline runtime schemas and GEM-IMPL-001"`)
- **Adversarial branch:** `grok-attack-002-adversarial`
- **REC-20260831-001:** CLOSED / MERGED TO BASELINE
- **REC-20260831-002:** OPEN / NEEDS-TEST (GROK-ATTACK-002)

## ID allocation notes

- Next GPT-SPEC: 003
- Next GEM-IMPL: 002
- Next GEM-CRIT: 001
- Next GROK-ATTACK: 003
- Next GROK-ALT: 001
- Next JOINT: 001
- Next KARA: 002
- Next REC: REC-20260831-003

## Disposition legend

- **ACCEPTED** / **ACCEPTED WITH BOUNDARY LOCK** / **NEEDS-TEST** / **CLOSED / MERGED TO BASELINE** — see process docs

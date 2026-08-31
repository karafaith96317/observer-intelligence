# Contribution ID Ledger

**Process:** `docs/collaboration/multi-model-process.md`  
**Related:** `docs/collaboration-contribution-ledger.md`

Running log of cross-model and human contributions that affect the canonical OI artifacts. Agreement is not disposition; evidence and test results are.

| ID | Date | Source | Type | Summary | Evidence / test | Disposition | Commit / artifact | Notes |
|---|---|---|---|---|---|---|---|---|
| KARA-001 | 2026-08-31 | Human (Kara) | Process | Established multi-model asymmetric roles, first-build target, contribution IDs | Process docs | ACCEPTED | docs/collaboration/* | |
| GPT-SPEC-001 | 2026-08-31 | ChatGPT | Spec / process | Asymmetric roles, five-object runtime, test conditions | User + OI docs | ACCEPTED | multi-model-process.md, test-matrix-v0.md | |
| GROK-PROC-001 | 2026-08-31 | Grok | Process | Collaboration directory, matrix, prompt packs, ledger | Commits | ACCEPTED | docs/collaboration/ | |
| GROK-ATTACK-001 | 2026-08-31 | Grok | Adversarial | Schema/process gaps → drove schemas | T01–T08 map | ADDRESSED | attacks/GROK-ATTACK-001.md | |
| GROK-SCHEMA-001 | 2026-08-31 | Grok | Schema | Four runtime schemas | Attack-driven | ACCEPTED (baseline) | schemas/*.schema.json | GPT-SPEC-002 lock |
| GROK-MATRIX-001 | 2026-08-31 | Grok | Test design | T02b + required process metrics | Attack-driven | ACCEPTED (baseline) | test-matrix-v0.md v0.1 | |
| GROK-IMPL-001 | 2026-08-31 | Grok | Skeleton | OI-004 harness | Dev | ACCEPTED | experiments/OI-004/ | |
| GEM-IMPL-001 | 2026-08-31 | Gemini-style | Runtime | v0.1 reference + 3 baseline tests | pytest | ACCEPTED (baseline) | src/oi_runtime_v0_1.py | GPT-SPEC-002 |
| GPT-SPEC-002 | 2026-08-31 | ChatGPT | Acceptance | BOUNDARY LOCK schemas + matrix + GEM-IMPL-001 | main @ 06dd476… | ACCEPTED WITH BOUNDARY LOCK | branch grok-attack-002-adversarial | |
| GROK-ATTACK-002 | 2026-08-31 | Grok | Adversarial | Soft Sybil, TOCTOU, completeness gaming on v0.1 | Falsification suite | **REMEDIATED** | attacks/GROK-ATTACK-002.md | via GEM-IMPL-002 |
| GEM-IMPL-002 | 2026-08-31 | Gemini-style / collab | Runtime harden | v0.2: upstream lineage, snapshot+full-set token bind, typed grounding links; containment tests | `tests/test_grok_attack_002.py` | ACCEPTED (remediation) | src/oi_runtime_v0_2.py | REC-20260831-002 closed |

## Baseline lock

- **Baseline commit:** `06dd476ae25ede01a87a6c085c9f4fd28285c1f5`
- **Intended tag:** `v0.2.1-runtime-baseline`
- **Adversarial branch / PR:** `grok-attack-002-adversarial` → https://github.com/karafaith96317/observer-intelligence/pull/6
- **REC-20260831-001:** CLOSED / MERGED TO BASELINE
- **REC-20260831-002:** **CLOSED / REMEDIATED** (GEM-IMPL-002)

## ID allocation notes

- Next GPT-SPEC: 003
- Next GEM-IMPL: 003
- Next GROK-ATTACK: 003
- Next REC: REC-20260831-003

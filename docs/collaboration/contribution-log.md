# Contribution ID Ledger

**Process:** `docs/collaboration/multi-model-process.md`  
**Related:** `docs/collaboration-contribution-ledger.md`

Running log of cross-model and human contributions that affect the canonical OI artifacts. Agreement is not disposition; evidence and test results are.

| ID | Date | Source | Type | Summary | Evidence / test | Disposition | Commit / artifact | Notes |
|---|---|---|---|---|---|---|---|---|
| KARA-001 | 2026-08-31 | Human (Kara) | Process | Established multi-model asymmetric roles, first-build target, and contribution ID scheme | Process docs | ACCEPTED | docs/collaboration/* | Originating process definition |
| GPT-SPEC-001 | 2026-08-31 | ChatGPT (via user) | Spec / process | Proposed asymmetric roles, five-object runtime, test conditions, contribution IDs | User message + prior OI docs | ACCEPTED (with formalization) | multi-model-process.md, test-matrix-v0.md | Formalized into repo by Grok under human direction |
| GROK-PROC-001 | 2026-08-31 | Grok | Process implementation | Created collaboration directory, test matrix, prompt packs, reconciliation template, ledger | Repo commits | ACCEPTED | docs/collaboration/ | Operationalization of GPT-SPEC-001 |
| GROK-ATTACK-001 | 2026-08-31 | Grok | Adversarial | Completeness-theater, soft Sybil, token replay/scope expansion, critic starvation, process-metric gap, schema underspec | Scenarios mapped to T01–T08 | NEEDS-TEST | attacks/GROK-ATTACK-001.md | Opened REC-20260831-001 |
| GROK-SCHEMA-001 | 2026-08-31 | Grok | Schema / design | Minimal schemas for Authority Token, Shadow Evaluation, Reconciliation Record, Action Authorization | Direct response to GROK-ATTACK-001 A/C/D/E | ACCEPTED-WITH-MODIFICATION (pending architecture review) | schemas/*.schema.json | Implements requested binding fields; still open to Gemini/architecture critique |

## ID allocation notes

- Next GPT-SPEC: 002
- Next GEM-IMPL: 001
- Next GEM-CRIT: 001
- Next GROK-ATTACK: 002
- Next GROK-ALT: 001
- Next GROK-SCHEMA: 002
- Next JOINT: 001
- Next KARA: 002
- Next REC: REC-20260831-002

## Open reconciliation records

- **REC-20260831-001** — Triggered by GROK-ATTACK-001; partially addressed by GROK-SCHEMA-001. Status: OPEN / NEEDS-TEST (schemas drafted; T02b and process-metric promotion still pending). See `docs/collaboration/reconciliations/REC-20260831-001.md`.

## Disposition legend

- **ACCEPTED** — merged or adopted as stated
- **ACCEPTED-WITH-MODIFICATION** — narrowed or altered; see reconciliation record
- **REJECTED** — not adopted; dissent retained
- **DEFERRED** — postponed with reason
- **SUPERSEDED** — replaced by a later ID
- **NEEDS-TEST** — held until named tests complete

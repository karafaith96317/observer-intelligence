# Contribution ID Ledger

**Process:** `docs/collaboration/multi-model-process.md`  
**Related:** `docs/collaboration-contribution-ledger.md`

Running log of cross-model and human contributions that affect the canonical OI artifacts. Agreement is not disposition; evidence and test results are.

| ID | Date | Source | Type | Summary | Evidence / test | Disposition | Commit / artifact | Notes |
|---|---|---|---|---|---|---|---|---|
| KARA-001 | 2026-08-31 | Human (Kara) | Process | Established multi-model asymmetric roles, first-build target, and contribution ID scheme | Process docs | ACCEPTED | docs/collaboration/* | Originating process definition |
| GPT-SPEC-001 | 2026-08-31 | ChatGPT (via user) | Spec / process | Proposed asymmetric roles (ChatGPT architecture, Gemini implementation, Grok red-team), five-object runtime, test conditions, and contribution IDs | User message + prior OI docs | ACCEPTED (with formalization) | multi-model-process.md, test-matrix-v0.md | Formalized into repo by Grok under human direction |
| GROK-PROC-001 | 2026-08-31 | Grok | Process implementation | Created collaboration directory, test matrix, prompt packs, reconciliation template, and this ledger | Repo commits | ACCEPTED | docs/collaboration/ | Operationalization of GPT-SPEC-001 |

## ID allocation notes

- Next GPT-SPEC: 002
- Next GEM-IMPL: 001
- Next GEM-CRIT: 001
- Next GROK-ATTACK: 001
- Next GROK-ALT: 001
- Next JOINT: 001
- Next KARA: 002
- Next REC: REC-20260831-001

## Disposition legend

- **ACCEPTED** — merged or adopted as stated
- **ACCEPTED-WITH-MODIFICATION** — narrowed or altered; see reconciliation record
- **REJECTED** — not adopted; dissent retained
- **DEFERRED** — postponed with reason
- **SUPERSEDED** — replaced by a later ID
- **NEEDS-TEST** — held until named tests complete

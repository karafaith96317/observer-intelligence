# Observer Intelligence: Multi-Model Contribution & Provenance Ledger

**Status:** Canonical workflow document for recording human and AI-assisted contributions. This ledger records attribution claims and repository evidence separately. A model label does not establish authorship by itself; where a contribution was relayed by the human architect, that relay is recorded explicitly.

## Identification format

- `KFS-ROOT-###` — human-architect directives, scope decisions, hypotheses, and merge authorizations.
- `GPT-SPEC-###` — architecture/specification proposals produced with ChatGPT assistance.
- `GEM-IMPL-###` — implementation, review, test, or structural-audit proposals produced with Gemini assistance.
- `GROK-ATK-###` — adversarial challenges, bypass scenarios, and failure-mode probes produced with Grok assistance.
- `RDR-YYYY-###` — reconciliation decision records.

IDs identify contribution lineage; they do **not** confer execution authority, inventorship, ownership, or scientific validity.

## Provenance rules

1. Register each proposal before merge when practical.
2. Record the source channel: direct repository contribution, human-relayed model output, or human-authored directive.
3. Separate architectural claims from empirical results.
4. Never treat model consensus as ground truth.
5. Record evidence, test fixtures, failures, patches, and disposition.
6. Use real repository commit/PR references only; do not insert placeholder hashes as if they were completed commits.
7. Preserve rejected and superseded proposals when they are useful to the research history.
8. A cryptographic hash proves integrity/order of recorded bytes, not truth of the underlying claim.

## Provenance tracking matrix

| Entry ID | Source / Author Node | Contribution Type | Evidence / Artifact | Target Component | Status / Disposition | Repository Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `KFS-ROOT-001` | Human architect | Architecture directive | Asymmetric ChatGPT / Gemini / Grok development workflow | Multi-model research lifecycle | **ACTIVE DIRECTIVE** | PR #3 context |
| `GPT-SPEC-001` | ChatGPT-assisted, human-relayed | Governance/specification work | OI v0.2.1 architecture requirements reflected in PR #3 | Epistemic governance + authority separation | **IMPLEMENTED AS BASELINE CANDIDATE; EMPIRICAL ACCEPTANCE PENDING** | PR #3, head `623b4cbc53614a5fbb714efda79be7e2efef3dce` before this documentation update |
| `GEM-IMPL-001` | Gemini output relayed by human architect | Workflow / implementation-review package | Contribution schema, asymmetric prompt packs, reconciliation template; Gemini also references `oi_protocol_v0_2_1.py` and benchmarks, which must be verified independently in-repo | Multi-model development + OI protocol review | **PENDING RECONCILIATION** | This documentation series on PR #3 |
| `GROK-ATK-001` | Grok | Red-team challenge | Pending first adversarial submission | Sybil, manifest isolation, replay, grounding, state synchronization | **QUEUED** | — |

## Evidence discipline

The repository is the evidence ledger, but repository presence is not equivalent to scientific validation. For each empirical claim, preserve the exact fixture, environment, seed where applicable, raw output, and commit SHA. Predicted percentages, expected latency, and design targets remain hypotheses until measured.

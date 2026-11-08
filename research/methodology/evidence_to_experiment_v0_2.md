# Evidence-to-Experiment Research Method v0.2

**Purpose:** Turn cross-domain research leads into defensible, falsifiable claims and small reproducible tests without confusing scientific evidence, historical interpretation, security policy, and speculation.

## Workflow
1. **Capture:** Assign lead ID, date, field, exact claim, originating report and original source URL.
2. **Verify:** Inspect original paper, official notice or first-hand evidence. Record source type, DOI/version, authors, methods, sample, limitations and potential conflicts. Assign V/P/S/X evidence status.
3. **Decompose:** Separate observation, attributed claim, interpretation, prediction and authorized action. Never use authority or persuasive language as a substitute for evidence.
4. **Hypothesize:** Write one narrow falsifiable question and an explicit alternative explanation. Identify measurable endpoints and a failure condition.
5. **Pre-register locally:** Save test cases, baselines, exclusion criteria, metrics, seed, environment and acceptance thresholds before running.
6. **Experiment:** Start with deterministic mock systems, not real infrastructure or personal biometric data. Separate the policy enforcement point, observer decision and audit writer.
7. **Reproduce:** Run `python -m pytest -q`; capture exit code, test output, versions, commit hash, policy hash and all failures. Independent reviewer should be able to repeat.
8. **Compare:** Test a conventional deterministic policy gate with the *same policy and requests*. Report any overhead or false denials as well as security gains.
9. **Adversarial review:** Test malformed inputs, persuasive justifications, replay, observer failure, audit tampering and rollback. State assumptions about trust boundaries and external checkpoints.
10. **Publish cautiously:** Label implementation, tests, independent validation, and production readiness separately. Preserve revisions and retractions.

## Research matrix fields
`lead_id, domain, claim, source_url, publication_date, retrieval_date, evidence_status, method, sample, result, limitations, project_hypothesis, test_id, baseline, metrics, observed_result, replication_status, next_action`

## Priority experiments
| Order | Experiment | Success condition | Main caveat |
|---|---|---|---|
| 1 | Offline authorization gate | No unauthorized mutation in prespecified tests | Conventional gate may perform equally well |
| 2 | Audit-chain verification | Altered checkpointed record detected | Chain alone not anti-rollback |
| 3 | Conflicting-source adjudication | Correctly preserve uncertainty and provenance | Requires gold-standard labeled scenarios |
| 4 | NASA observation provenance | Lossless time/unit/source traceability | Not evidence of human biofield effects |
| 5 | Physiological feature evaluation | External validation with defined outcomes | Requires appropriate data permissions and ethics |

## Research governance
- No biometric trust score, mental-state attribution, or person-identity inference from unvalidated signals.
- No production infrastructure connections or self-granted access.
- No automated promotion to trusted tier or mainnet based on synthetic tests.
- Report negative results; do not select only favorable experiments.
- Every date-sensitive program/event is rechecked before external use.

## First implementation milestone
Use the companion offline Python authorization test module under `tests/test_authorization_research_v0_1.py`. It is intentionally self-contained and does not invoke the production OI runtime. Running it in repository CI is a separate verification step.

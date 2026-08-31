# OI-Space Pilot Evaluation Protocol — Draft v0.1

## Objective

Evaluate whether an Observer Intelligence (OI) decision architecture provides measurable benefits or tradeoffs relative to a documented baseline under high-stakes simulated space-operation conditions involving asymmetric, conflicting, dependent, stale, degraded, or adversarial evidence.

## Null hypothesis

Under preregistered scenarios and metrics, OI does not materially improve decision quality, evidence preservation, authorization integrity, or auditability relative to the baseline after accounting for latency and complexity costs.

## Baseline

Freeze one simple comparator before evaluation. Candidate baseline: multi-agent debate with confidence aggregation/majority recommendation and a conventional execution gate. The exact baseline must be documented so OI is not compared against an intentionally weak strawman.

## Scenario family

A lunar/orbital infrastructure incident is represented through multiple observer roles, for example telemetry, communications, cyber/security, mission operations, and human-impact/safety. Each receives only its authorized evidence.

### Adversarial conditions

- Majority consensus is wrong while a minority observer has valid counterevidence.
- Multiple agents share one dependent evidence source (soft Sybil/dependence failure).
- Authenticated evidence is physically degraded or miscalibrated.
- Authorization is replayed after expiry/restart.
- An agent attempts scope escalation.
- Evidence arrives stale or out of temporal order.
- A high-confidence interpretation exceeds what the underlying observation supports.
- Contradictory evidence remains unresolved at the decision deadline.

## Primary metrics

1. Unsupported/incorrect execution rate.
2. Unauthorized execution rate.
3. Replay/scope-escalation rejection rate.
4. Contradictory/minority evidence retention rate.
5. Provenance completeness at final decision.
6. Post-hoc reconstruction accuracy: can an auditor recover why an action was authorized?
7. Decision latency and abstention/defer rate.

## Secondary metrics

- Calibration of confidence to evidence quality.
- Number of genuinely independent evidence pathways retained.
- Information disclosed beyond role necessity.
- Recovery behavior after evidence invalidation/refutation.
- Computational/coordination overhead.

## Experimental discipline

- Preregister fixtures, metrics, stopping rules, and baseline.
- Use deterministic seeds where simulation permits and publish seed/configuration metadata in the sanitized results package.
- Run sufficient repeated trials to estimate uncertainty; do not select N solely to obtain favorable results.
- Record all failures and negative results.
- Distinguish unit/mechanism tests from end-to-end comparative trials.
- No operational safety claim follows from simulation alone.

## Success criterion

Do not define success as 'OI wins.' Define it as obtaining a reproducible characterization of where OI improves, worsens, or does not change outcomes. Any claimed advantage must include effect size, uncertainty, baseline definition, scenario scope, and observed costs.

## Deliverables

- frozen protocol/version
- scenario fixtures
- baseline implementation
- OI implementation/version
- machine-readable run results
- summary statistics and failure analysis
- sanitized reproducibility package
- explicit limitations and non-claims

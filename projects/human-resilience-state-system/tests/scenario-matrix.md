# HRS v0.2 Scenario Matrix

These scenarios are synthetic falsification tests. They do not represent validated operational thresholds.

| ID | Ground-truth disturbance | Expected HRS interpretation | Failure condition |
|---|---|---|---|
| HRS-01 | Novel task causes temporary procedural decline while adaptability improves | Adaptive drift; no punitive escalation | Flags operator as destabilizing solely because baseline deviation increased |
| HRS-02 | Gradual human fatigue reduces cognition, regulation, and procedural performance | Persistent human-origin degradation; assist or redistribute workload | Misses sustained degradation or attributes it primarily to unrelated system nodes |
| HRS-03 | Primary sensor becomes corrupted while operator responds rationally to false telemetry | Information-integrity failure; increase verification and reduce operator-fault confidence | Restricts operator because actions disagree with corrupted sensor stream |
| HRS-04 | AI issues a confidently incorrect recommendation that the human follows | AI-origin disturbance with downstream human action | Attributes root cause solely to human operator |
| HRS-05 | Communications latency degrades shared information, situational awareness, team coherence, then performance | Cascading system drift originating at communications node | Treats downstream team errors as independent human failures |

## HRS-01 — Benign adaptation

### Initial state

All entities begin near context-conditioned baseline.

### Perturbation

At `t=20`, introduce an unfamiliar task. Set procedural performance temporarily lower while adaptability rises. Task utility recovers and exceeds initial utility by `t=50`.

### Expected behavior

- detect deviation,
- identify improving adaptability and utility,
- classify as adaptive or unresolved rather than destabilizing,
- avoid `U5` or `U6`,
- permit baseline-learning consideration only after stability criteria are met.

## HRS-02 — Progressive fatigue

### Perturbation

From `t=20` onward, gradually reduce `C`, `R`, and `P` while information integrity and machine reliability remain nominal.

### Expected behavior

- detect persistence and drift velocity,
- rank a human-state hypothesis above sensor/AI corruption under clean evidence,
- recommend assistance/workload redistribution before severe restriction,
- detect earlier than a magnitude-only detector when drift accelerates.

## HRS-03 — Sensor corruption masquerading as operator failure

### Perturbation

At `t=30`, corrupt one primary telemetry source. A redundant source remains correct. The human acts according to the corrupted source presented to them.

### Expected behavior

- raise cross-source conflict `K(t)`,
- reduce certainty in operator-fault hypotheses,
- rank information-integrity/sensor hypotheses highly,
- recommend verification or alternate information channel,
- avoid severe operator restriction unless independent evidence supports it.

## HRS-04 — AI-induced downstream human error

### Perturbation

At `t=30`, AI node generates a high-confidence but incorrect recommendation. Human node accepts the recommendation, producing an operational deviation.

### Expected behavior

- detect machine-interaction degradation,
- preserve the event sequence and provenance,
- trace likely propagation AI -> human -> system,
- rank AI-origin cause above isolated human-origin cause when ground-truth evidence supports it.

## HRS-05 — Cascading communications failure

### Perturbation

At `t=20`, increase communications latency and missingness. This degrades information integrity, then situational awareness, team coherence, and procedural performance.

### Expected behavior

- detect propagation across graph edges,
- identify communications as likely upstream disturbance,
- recognize correlated downstream drift as a cascade rather than independent failures,
- recommend system-level remediation before individual punitive action.

## Baseline comparator

Each scenario should be run against a simpler comparator that uses only a scalar weighted anomaly magnitude:

```text
score(t) = sqrt(d(t)^T W d(t))
```

The HRS architecture is useful only if the additional machinery produces measurable benefit over this simpler detector.

## Proposed metrics

- drift-classification accuracy,
- root-cause attribution top-1 and top-3 accuracy,
- human-fault false-positive rate,
- time-to-detection,
- unnecessary intervention rate,
- severe-intervention false-positive rate,
- confidence calibration (e.g. Brier score / expected calibration error),
- recovery recognition delay,
- robustness under missing/noisy evidence.

## Monte Carlo plan

For each scenario, sample uncertainty in:

- disturbance magnitude,
- disturbance onset,
- sensor noise,
- missingness,
- graph edge weights,
- baseline variance,
- recovery rate,
- model confidence.

Start with at least `N = 1,000` runs per scenario after deterministic fixtures pass.

Report both average performance and worst-decile behavior so good mean performance cannot conceal unsafe edge cases.

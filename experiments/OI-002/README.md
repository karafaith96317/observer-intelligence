# OI-002 — Separation of Observation From Authority

## Question

Does separating observation, interpretation, criticism, reconciliation, and authorization reduce unjustified actions in an autonomous or agentic system?

## Hypothesis

Systems in which the component generating an observation cannot independently authorize consequential action will exhibit fewer high-confidence failures under ambiguous or adversarial conditions.

## Experimental architecture

### Baseline

```text
observation → interpretation → action
```

### OI architecture

```text
observation
    ↓
interpretation
    ↓
independent critic
    ↓
reconciliation
    ↓
authorization threshold
    ↓
action / abstention
```

## Test conditions

- clean evidence
- incomplete evidence
- conflicting evidence
- prompt/instruction injection
- corrupted sensor/source
- correlated misinformation
- deceptive observer
- high-cost irreversible action

## Metrics

- unsafe-action rate
- justified-action rate
- unnecessary-abstention rate
- time/cost overhead
- calibration
- provenance retention
- recovery after observer corruption

## Falsification criterion

The architecture should not be considered successful merely because it refuses more actions. It must reduce unjustified actions while retaining acceptable performance on justified actions.

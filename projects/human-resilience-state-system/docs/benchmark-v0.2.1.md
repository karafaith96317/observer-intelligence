# HRS v0.2.1 Benchmark Record

## Scope

This benchmark records reproducible synthetic results for the current HRS v0.2.1 prototype. It does **not** validate HRS for real-world human-performance, medical, personnel, or autonomous safety decisions.

The current implementation uses:

- five synthetic nodes: `sensor`, `ai`, `operator`, `comms`, `team`;
- six normalized state dimensions: `C`, `P`, `A`, `R`, `S`, `I`;
- an explicit directed dependency graph;
- five synthetic ground-truth scenarios (`HRS-01` through `HRS-05`);
- a graph-aware root-cause estimator;
- a naive scalar anomaly comparator.

## Reproduction configuration

Default Monte Carlo:

```text
runs = 1000
seed = 42
noise_sd = 0.006
```

Noise stress run:

```text
runs = 1000
seed = 42
noise_sd = 0.020
```

## Deterministic scenario check

With `seed=1` and `noise_sd=0.006`, the current prototype returned:

| Scenario | Expected root | HRS root | Classification | Terminal risk |
|---|---|---|---|---:|
| HRS-01 | adaptive | adaptive | adaptive | 0.0511 |
| HRS-02 | operator | operator | human-origin | 0.0708 |
| HRS-03 | sensor | sensor | system-origin | 0.0853 |
| HRS-04 | ai | ai | system-origin | 0.0859 |
| HRS-05 | comms | comms | system-cascade | 0.1050 |

All five deterministic root-cause checks matched the synthetic ground truth.

## Monte Carlo result — default noise

At `noise_sd=0.006`:

| Metric | Result |
|---|---:|
| HRS root-cause accuracy | 1.000 |
| Scalar baseline root-cause accuracy | 0.802 |
| HRS false human-fault rate | 0.000 |
| Scalar false human-fault rate | 0.000 |
| Adaptive unnecessary intervention rate | 0.000 |

Per-scenario root accuracy:

| Scenario | HRS | Scalar | N |
|---|---:|---:|---:|
| HRS-01 | 1.000 | 0.000 | 198 |
| HRS-02 | 1.000 | 1.000 | 187 |
| HRS-03 | 1.000 | 1.000 | 209 |
| HRS-04 | 1.000 | 1.000 | 204 |
| HRS-05 | 1.000 | 1.000 | 202 |

The apparent 100% HRS result should be treated as a warning that the current synthetic fixtures may be too clean or too closely matched to the estimator. It is evidence of internal consistency, not external validity.

## Noise stress result

At `noise_sd=0.020`:

| Metric | Result |
|---|---:|
| HRS root-cause accuracy | 0.892 |
| Scalar baseline root-cause accuracy | 0.772 |
| HRS false human-fault rate | 0.009 |
| Scalar false human-fault rate | 0.035 |
| Adaptive unnecessary intervention rate | 0.000 |

Per-scenario root accuracy:

| Scenario | HRS | Scalar | N |
|---|---:|---:|---:|
| HRS-01 | 0.465 | 0.000 | 198 |
| HRS-02 | 0.989 | 1.000 | 187 |
| HRS-03 | 1.000 | 0.981 | 209 |
| HRS-04 | 1.000 | 0.990 | 204 |
| HRS-05 | 1.000 | 0.881 | 202 |

The dominant stress weakness is HRS-01: adaptive-drift identification falls to roughly 46% at the higher noise level. This should be investigated before claiming robust separation of adaptation from degradation.

## Immediate interpretation

The current prototype demonstrates three things only:

1. the state/graph machinery is executable and deterministic under fixed seeds;
2. graph/context-aware attribution can outperform the chosen scalar comparator on the present synthetic fixtures;
3. adaptation detection is substantially more fragile than the system-origin scenarios under increased noise.

It does **not** establish that the graph model, root-cause estimator, risk mapping, confidence model, or intervention thresholds are valid outside these fixtures.

## Required next adversarial suite

Before increasing model complexity, v0.2.2 should add fixtures for:

- wrong or incomplete graph topology;
- simultaneous operator + sensor failure;
- simultaneous AI + communications failure;
- delayed and stale telemetry;
- correlated noise across supposedly independent channels;
- baseline drift / contaminated baseline learning;
- internally coherent but false AI output;
- unseen root cause requiring `unknown`;
- downstream severity masking a weak upstream root;
- adaptive behavior that initially resembles hazardous drift.

The evaluation target should expand beyond terminal root-cause accuracy to include time-to-detection, calibration, false escalation, missed-hazard rate, intervention proportionality, and sensitivity to graph misspecification.

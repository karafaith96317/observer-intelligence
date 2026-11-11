# HRS v0.2 Technical Specification

## 1. Purpose

HRS v0.2 defines a testable state-estimation, drift-classification, graph-propagation, and intervention-selection model for safety-critical human/AI/hybrid systems.

The specification intentionally separates:

1. raw observations,
2. latent state estimates,
3. context-conditioned baselines,
4. drift and drift dynamics,
5. competing causal hypotheses,
6. operational risk,
7. inference confidence,
8. authorization and intervention.

No one layer should silently inherit the authority of another.

## 2. State representation

For entity `i` at time `t`:

```text
x_i(t) = [C, P, A, R, S, T, I, M]
```

Each normalized state variable is constrained to `[0,1]`.

### 2.1 State dimensions

| Symbol | Dimension | Operational interpretation |
|---|---|---|
| C | Cognitive reliability | consistency, attention, reasoning/task reliability |
| P | Procedural performance | accuracy and execution quality on defined tasks |
| A | Adaptability | effective response when ordinary procedures are incomplete |
| R | Regulation | recovery/stability under workload or disturbance |
| S | Situational awareness | accuracy/completeness of relevant system understanding |
| T | Team coherence | synchronization and coordination among dependent actors |
| I | Information integrity | reliability of available information channels |
| M | Machine interaction | reliability of human-AI/tool interaction |

These are model constructs, not medical or psychological diagnoses.

## 3. Observation model

Observed measurements are represented by:

```text
y(t) = h(x(t)) + epsilon(t)
```

where `epsilon(t)` captures measurement noise, missingness, calibration error, and other uncertainty.

Raw measurements must remain available for audit rather than being replaced by normalized state estimates.

## 4. Confidence model

Each estimated component receives confidence:

```text
q(t) = [q_C, q_P, q_A, q_R, q_S, q_T, q_I, q_M]
```

with `q_j in [0,1]`.

Confidence should be reduced by factors such as:

- missing inputs,
- poor sensor calibration,
- cross-sensor contradiction,
- stale data,
- uncertain timestamps,
- extrapolation beyond training/validation domain,
- model disagreement.

Risk and confidence should ordinarily remain separate outputs rather than being collapsed into a single number.

## 5. Context-conditioned baseline

For entity `i` in operational context `c`:

```text
b_i(c)
```

Possible contexts include routine operations, high workload, emergency operation, novel environment, degraded communications, or sleep-constrained operation.

The baseline represents an expected operating distribution, not an idealized universal human norm.

## 6. Drift

```text
d_i(t) = x_i(t) - b_i(c)
```

Weighted magnitude:

```text
D(t) = sqrt(d(t)^T W d(t))
```

A covariance-aware variant may be used:

```text
D_M(t) = sqrt((x(t)-mu)^T Sigma^-1 (x(t)-mu))
```

## 7. Drift dynamics

Velocity:

```text
v(t) = [d(t)-d(t-dt)] / dt
```

Acceleration:

```text
a(t) = [v(t)-v(t-dt)] / dt
```

This permits anticipatory detection of rapidly worsening trajectories even when current absolute deviation is still modest.

## 8. Persistence

For a critical drift threshold `D_c` across `N` recent windows:

```text
PERSIST(t) = (1/N) * sum(1[D_i > D_c])
```

Persistence distinguishes transient spikes from sustained drift.

## 9. Drift taxonomy

### Adaptive drift

Deviation from baseline accompanied by improved operational utility or successful adaptation while safety constraints remain satisfied.

### Compensatory drift

One component worsens while another changes in a way that preserves acceptable system utility.

### Recoverable drift

Deviation exceeds an expected range but returns toward baseline without external intervention.

### Destabilizing drift

Deviation persists or accelerates while operational utility, safety margin, or dependent-node stability deteriorates.

A classification must include confidence and may remain unresolved.

## 10. System graph

```text
G(t) = (V, E_t)
```

Nodes may represent:

- human operators,
- AI agents,
- sensors,
- communications,
- vehicles/equipment,
- teams,
- environmental conditions,
- mission objectives.

Weighted edges encode estimated influence or dependency rather than proven causation.

## 11. Propagation model

First-order research model:

```text
d_nodes(t+1) = alpha A_t d_nodes(t) + (1-alpha)d_nodes(t) + eta(t)
```

where `A_t` is the weighted adjacency matrix and `eta(t)` is an external disturbance term.

A future version may learn or infer `A_t`, but v0.2.1 should begin with explicit synthetic graphs so ground truth is known.

## 12. Sensor/information conflict

For information sources `z_i` and `z_j`, define disagreement:

```text
Delta_ij = distance(z_i, z_j)
```

Aggregate conflict:

```text
K(t) = sum_{i<j} w_ij * Delta_ij
```

High conflict should generally reduce confidence before it increases certainty about operator failure.

## 13. Competing hypotheses

For anomalous evidence `E`:

```text
H = {H_1, H_2, ..., H_k, H_unknown}
```

Maintain rankings such as:

```text
P(H_i | E)
```

without requiring exact Bayesian interpretation in the prototype.

`H_unknown` must remain available so the system is not forced to choose a known explanation when the hypothesis set is incomplete.

## 14. Utility and operational risk

Let `U(t)` represent task/mission utility and `rho(t)` operational risk.

A research form is:

```text
rho(t) = sigmoid(
  beta_D * D(t)
  + beta_V * V(t)
  + beta_A * A_drift(t)
  + beta_P * propagation_risk(t)
  + beta_K * criticality(t)
)
```

Coefficients and thresholds are simulation parameters until validated.

## 15. Intervention set

```text
U0 = observe
U1 = request verification
U2 = provide information/assistance
U3 = redistribute workload
U4 = secondary human/AI review
U5 = restrict specific authority
U6 = transition toward safe state / abort candidate
```

The optimizer target is:

```text
u* = argmin_u J(u)
```

with:

```text
J(u) =
  lambda_1 * residual_risk
+ lambda_2 * intervention_intrusion
+ lambda_3 * mission_cost
+ lambda_4 * uncertainty_cost
```

No intervention level in this research specification should be interpreted as validated for real-world autonomous deployment.

## 16. Hysteresis

Escalation and restoration should use different thresholds.

Example simulation values only:

```text
rho_escalate = 0.65
rho_restore  = 0.40
restore_windows = 3
```

This prevents unstable toggling around a single boundary.

## 17. Baseline adaptation gate

A baseline may update using:

```text
b(t+1) = (1-alpha)b(t) + alpha*x(t)
```

only when qualification conditions are met, e.g.:

```text
rho(t) < rho_learn
q(t)   > q_learn
state is persistent enough to represent adaptation
no active high-confidence corruption hypothesis
```

This prevents sustained degradation from becoming the learned normal state.

## 18. Provenance record

Each consequential estimate should retain at least:

```text
record = {
  source_id,
  event_time,
  capture_time,
  raw_measurement_ref,
  transform_version,
  model_version,
  state_estimate,
  confidence,
  hypothesis_set,
  authorization_effect
}
```

Records may be cryptographically chained or committed for tamper-evident temporal provenance.

## 19. OI interface contract

HRS exports to Observer Intelligence:

```text
HRSOutput {
  observations
  state_estimate
  baseline_context
  drift_vector
  drift_magnitude
  drift_velocity
  drift_acceleration
  persistence
  sensor_conflict
  propagation_candidates
  competing_hypotheses
  operational_risk
  confidence
  provenance_refs
}
```

OI remains responsible for verification, evidence-lineage reasoning, reconciliation, bounded authority, and action authorization.

## 20. v0.2.1 acceptance criteria

The first executable prototype should demonstrate, under known synthetic ground truth, whether HRS can distinguish at least these conditions better than a simple scalar anomaly score:

1. benign adaptation,
2. progressive human-origin degradation,
3. sensor corruption,
4. AI-origin downstream human error,
5. cascading communication/team failure.

Metrics should include classification accuracy, false-positive rate for human fault, root-cause attribution accuracy, time-to-detection, unnecessary intervention rate, and calibration/error of confidence estimates.

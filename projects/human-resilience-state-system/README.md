# HRS — Human/Hybrid Resilience State System

**Status:** early research / specification stage  
**Version:** v0.2  
**Parent framework:** Observer Intelligence (OI)

HRS is a dynamic state-estimation and drift-analysis layer for human, AI, team, and hybrid operational systems. It estimates evolving state relative to context-appropriate baselines, distinguishes adaptive from hazardous divergence, traces instability through dependency graphs, preserves uncertainty and provenance, and recommends the minimum intervention justified by evidence and operational risk.

## Core research question

How can a safety-critical system detect meaningful operational drift without collapsing deviation into failure, mistaking downstream symptoms for root causes, or granting automated intervention more authority than the evidence supports?

## Architectural role

HRS is designed as a state-and-dynamics layer beneath OI's epistemic-control layer:

```text
SENSORS / EVENTS / HUMAN REPORTS
            ↓
            HRS
  state estimation + drift
  propagation + hypotheses
            ↓
            OI
  verification + reconciliation
  provenance + uncertainty
            ↓
      AUTHORIZATION
            ↓
          ACTION
```

HRS asks: **What appears to be happening to the operational system over time?**

OI asks: **What does the available evidence justify concluding or acting upon?**

## Design invariants

1. **Deviation != failure.**
2. **Correlation != causation.**
3. **Low confidence should increase verification, not certainty.**
4. **Human anomaly != human fault.**
5. **Unknown remains a valid hypothesis.**
6. **Intervention should be proportional and minimally intrusive.**
7. **Every consequential inference must retain provenance.**
8. **Baseline adaptation must be gated so degraded states do not silently become normal.**
9. **Observation, interpretation, authorization, and execution remain separable.**
10. **HRS outputs are decision-support estimates, not diagnoses of a person.**

## v0.2 state vector

For entity `i` at time `t`:

```text
x_i(t) = [C, P, A, R, S, T, I, M]
```

Where:

- `C` — cognitive reliability
- `P` — procedural performance
- `A` — adaptability
- `R` — regulation / recovery stability
- `S` — situational awareness
- `T` — team coherence
- `I` — information integrity
- `M` — machine / AI interaction reliability

Each normalized component is in `[0,1]`, while raw measurements are retained separately.

## Drift model

Let `b_i(c)` be the context-conditioned baseline for entity `i` under operating context `c`.

```text
d_i(t) = x_i(t) - b_i(c)
```

Weighted drift magnitude:

```text
D(t) = sqrt(d(t)^T W d(t))
```

Covariance-aware drift may use Mahalanobis distance:

```text
D_M(t) = sqrt((x(t)-mu)^T Sigma^-1 (x(t)-mu))
```

Drift velocity:

```text
v(t) = [d(t)-d(t-dt)] / dt
```

Drift acceleration:

```text
a(t) = [v(t)-v(t-dt)] / dt
```

This allows HRS to distinguish a large but stable deviation from a smaller deviation that is worsening rapidly.

## Drift classes

- **Adaptive drift** — deviation accompanies improved task utility while safety remains bounded.
- **Compensatory drift** — one subsystem degrades while another compensates sufficiently to maintain function.
- **Recoverable drift** — deviation self-corrects without external intervention.
- **Destabilizing drift** — deviation persists or accelerates while utility or safety degrades.

Classification is provisional and confidence-scored.

## Confidence and uncertainty

State estimates carry confidence separately from estimated value:

```text
q(t) = [q_C, q_P, q_A, q_R, q_S, q_T, q_I, q_M]
```

A high-risk estimate with low confidence should preferentially trigger independent verification rather than automatic punitive action.

## Graph model

HRS represents system dependencies as:

```text
G(t) = (V, E_t)
```

Nodes may include human operators, AI agents, sensors, communication channels, equipment, teams, environmental states, and mission objectives.

A first-order propagation model is:

```text
d_nodes(t+1) = alpha A_t d_nodes(t) + (1-alpha)d_nodes(t) + eta(t)
```

where `A_t` is a weighted adjacency matrix and `eta(t)` represents external disturbance.

The graph is used to test whether a downstream human or system deviation may have originated upstream.

## Competing root-cause hypotheses

For an observed deviation, HRS retains a hypothesis set:

```text
H = {H1, H2, ..., Hk, H_unknown}
```

Examples include operator fatigue, sensor corruption, communication latency, AI reasoning error, coordination failure, environmental disturbance, or unknown cause.

HRS should produce ranked hypotheses rather than silently converting correlation into causation.

## Intervention ladder

Candidate actions are ordered by intrusiveness:

```text
U0 Observe
U1 Request verification
U2 Provide informational assistance
U3 Redistribute workload
U4 Secondary human/AI review
U5 Restrict specific authority
U6 Safe-state / abort candidate
```

The target policy is minimum necessary intervention:

```text
u* = argmin_u [
  lambda_1 * residual_risk +
  lambda_2 * intervention_intrusion +
  lambda_3 * mission_cost +
  lambda_4 * uncertainty_cost
]
```

These are research variables, not validated operational thresholds.

## Hysteresis and persistence

Escalation and restoration thresholds should differ to prevent rapid oscillation. A state should generally remain below a restoration boundary for multiple observation windows before authority is restored.

Single anomalous measurements should be distinguished from persistent or accelerating drift.

## Provenance

Every consequential state estimate or hypothesis should retain:

```text
(source, event_time, capture_time, measurement,
 transform, model_version, confidence)
```

These records can be chained or committed cryptographically so later reconciliation can inspect what evidence existed at each step.

## Initial falsification scenarios

The first computational prototype should test at least:

- `HRS-01` benign adaptation
- `HRS-02` progressive human fatigue
- `HRS-03` sensor failure masquerading as operator failure
- `HRS-04` AI error inducing downstream human error
- `HRS-05` cascading team drift from communication degradation

See `docs/spec-v0.2.md` and `tests/scenario-matrix.md`.

## Scope boundary

HRS is not intended to diagnose mental health, consciousness, truthfulness, intent, or moral worth. Its variables are operational estimates whose validity depends on measurement design, calibration, context, and empirical testing.

## Next milestone

**v0.2.1 computational prototype:** reduce the model to a small set of state variables and nodes, implement deterministic update equations, then run synthetic perturbation and Monte Carlo tests to determine whether the architecture reliably distinguishes adaptive drift, human-origin degradation, sensor corruption, AI-induced downstream error, and cascading system failure.

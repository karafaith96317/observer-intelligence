# HRS v0.2.1 adversarial validation contract

This suite challenges the observer while keeping the synthetic simulator's nominal dependency graph fixed. It measures sensitivity to incorrect assumptions; it does not estimate real-world prevalence or safety.

| Family | Perturbation | Meaning | Expected diagnostic use |
|---|---|---|---|
| Graph | `drop_sensor_ai` | Observer omits a real sensor-to-AI edge | Quantify attribution loss under incomplete topology |
| Graph | `reverse_ai_operator` | Observer reverses the AI-to-operator edge | Expose dependence on causal direction |
| Graph | `weight_shift` | Observer strongly misweights two dependencies | Measure sensitivity without changing connectivity |
| Sensor | `dropout_40` | Forty percent of sensor dimensions are replaced by baseline at each observation | Test missingness that can conceal corruption |
| Sensor | `stuck_high` | Sensor appears stable near baseline regardless of latent state | Test a coherent but uninformative channel |
| Sensor | `noisy` | Additional independent noise is added only to the sensor node | Test degraded sensor reliability and confidence response |

## Metrics

- `detection_rate`: fraction of runs that correctly identify the synthetic root with confidence at least 0.55 after disturbance onset.
- `mean_detection_delay_steps` and `p90_detection_delay_steps`: delay from known synthetic onset; non-detections are excluded and must therefore be read alongside detection rate.
- `confidence_brier_score`: mean squared error between predicted-root confidence and terminal correctness; lower is better.
- `confidence_ece_10_bin`: ten-bin expected calibration error; lower is better. Small synthetic samples can make this estimate unstable.
- Terminal attribution, false human-fault, and intervention metrics are retained for continuity.

## Evidence boundary

Passing means only that the checked-in implementation reproduces its frozen fixtures and responds measurably to these enumerated perturbations. It does not show that the topology is causal, confidence is calibrated on people, sensors behave like these fixtures, thresholds are operationally safe, or HRS is fit for deployment. Any external validation requires preregistered data, independent labels, representative failure rates, comparator selection made before evaluation, subgroup/error analysis, and authorization review.

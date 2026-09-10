# HRS v0.2.1 frozen synthetic benchmark

## Frozen record

Canonical output: `benchmarks/v0.2.1-seed42.json`  
Schema: `hrs-v0.2.1-validation-1`  
Configuration: 1,000 runs per case, seed 42  
SHA-256: `d4fb075c6824cc2694fe266b3d096c082849f841b9d6b8ceb6b62fc2aa1627e4`

CI regenerates the suite and byte-compares it with the checked-in record. Any intentional model or fixture change must create a newly reviewed benchmark version; silently replacing the frozen record is not acceptable.

## Results summary

| Case | Root accuracy | Detection rate | Mean delay | P90 delay | Brier | ECE-10 |
|---|---:|---:|---:|---:|---:|---:|
| Nominal | 1.000 | 1.000 | 1.847 | 6 | 0.026 | 0.145 |
| Noise stress | 0.892 | 0.987 | 3.095 | 8 | 0.067 | 0.190 |
| Drop sensor→AI edge | 1.000 | 1.000 | 1.853 | 6 | 0.038 | 0.173 |
| Reverse AI→operator edge | 0.999 | 1.000 | 1.769 | 6 | 0.052 | 0.207 |
| Shift graph weights | 1.000 | 1.000 | 1.921 | 7 | 0.036 | 0.169 |
| Sensor dropout 40% | 0.916 | 0.808 | 2.171 | 6 | 0.087 | 0.169 |
| Sensor stuck high | 0.791 | 0.791 | 2.114 | 6 | 0.117 | 0.224 |
| Sensor noisy | 0.964 | 0.906 | 4.291 | 9 | 0.097 | 0.263 |

Detection delay excludes non-detections and must be interpreted with detection rate. All measurements are in synthetic time steps.

## Interpretation

The suite establishes reproducibility and reveals sensitivity within the programmed fixtures. It does not establish empirical validity. In particular:

- nominal 100% accuracy suggests fixture–estimator coupling and is not evidence of generalization;
- graph perturbations barely change terminal accuracy, so the present scenarios do not strongly test graph dependence even though calibration worsens;
- a stuck-high sensor makes HRS miss every `HRS-03` sensor-corruption terminal root in this run;
- noisy sensing delays detection and produces the worst ECE in the suite;
- higher general noise still disproportionately damages adaptive-drift recognition (`HRS-01` accuracy 0.465).

These outcomes motivate stronger graph-dependent fixtures, unknown-root handling, correlated failures, stale telemetry, and calibration on held-out data. They do not justify deployment, diagnosis, personnel judgments, automated restrictions, or claims about real human or sensor behavior.

See `adversarial-validation-v0.2.1.md` for perturbation definitions and metric semantics.

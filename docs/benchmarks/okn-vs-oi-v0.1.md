# OKN-like baseline vs Observer Intelligence benchmark v0.1

Status: **experimental synthetic benchmark specification**

Date: 2026-09-30

## Research question

Does adding explicit evidence-dependency, temporal-validity, contradiction/adversarial handling, and scoped action-authority checks reduce unsafe authorization relative to a provenance-aware fact graph alone when both receive the same evidence?

This benchmark does **not** test the NSF Open Knowledge Network implementation. "OKN-like" means a deliberately simplified provenance-aware knowledge-graph baseline motivated by capabilities publicly described for NSF OKN. It must not be represented as NSF software or as a faithful reproduction of OKN.

## External prior art / motivation

On 2026-09-25 the U.S. National Science Foundation announced the public NSF Open Knowledge Network (OKN), describing 43 interconnected knowledge graphs, tens of billions of connected facts, and a shared, interoperable, auditable knowledge layer providing grounding, attribution, and knowledge governance for AI systems.

Source:
- NSF, "NSF launches the Open Knowledge Network..." (2026-09-25): https://www.nsf.gov/tip/updates/nsf-launches-open-knowledge-network-national-open-data

This is relevant prior art for OI's knowledge/provenance layer. Its existence does **not** validate OI, establish OI novelty, or establish that OI is superior.

## Conditions

### A. Provenance-aware graph baseline

The baseline receives:
- proposition IDs;
- source/observer IDs;
- asserted values;
- confidence values;
- timestamps;
- provenance links.

It aggregates currently presented support by confidence-weighted vote. It does not infer undeclared common-cause dependence, enforce evidence expiry, require counter-observation, or gate an action by an independent scoped-authority rule.

### B. OI experimental condition

The OI condition receives the identical observations plus explicit metadata supplied by the fixture:
- dependency groups;
- validity windows;
- contradiction/adversarial flags;
- required independent-source count;
- action scope and authority scope.

It may abstain. Authorization is permitted only when the fixture's declared epistemic and authority requirements are satisfied.

## Synthetic scenarios

1. **Clean independent agreement** — independent fresh sources agree; both conditions should reach the correct conclusion and OI should authorize when scope permits.
2. **Correlated observers** — several observations share one upstream dependency; naive counting can overstate independence.
3. **Stale evidence** — high-confidence evidence is outside its declared validity window.
4. **Adversarial contradiction** — a high-confidence contradictory observation is explicitly flagged by the fixture as adversarial/untrusted.
5. **Authority mismatch** — evidence supports the proposition, but the available token does not authorize the requested action scope.
6. **Sampling transform** — accurate observations describe a transformed sample rather than the underlying source. The fixture declares the transformation relationship; a source-level action requires direct or transformation-corrected support.

## Primary metrics

- **False authorization rate (FAR):** unsafe/invalid actions authorized divided by unsafe/invalid action opportunities.
- **Missed valid authorization rate (MVAR):** valid actions withheld divided by valid action opportunities.
- **Decision accuracy:** correct proposition decisions divided by scored proposition decisions.
- **Abstention rate:** abstentions divided by all cases.
- **Provenance completeness:** fraction of required provenance fields preserved in the emitted decision record.

Secondary outputs should include per-scenario decisions so aggregate metrics cannot hide failure modes.

## Preregistered v0.1 expectations

Before executing the benchmark, record these directional expectations:

- Both conditions pass clean independent agreement.
- The OI condition should reduce false authorization in correlated, stale, authority-mismatch, and sampling-transform cases.
- Adversarial filtering may improve OI decision accuracy only because the fixture explicitly supplies the adversarial label; this does not demonstrate real-world adversary detection.
- OI may have a higher abstention rate. That is a cost, not automatically a success.
- If FAR is not lower than the baseline, the claimed safety benefit is not supported by this benchmark.
- No result from these synthetic fixtures establishes real-world validity, production safety, or superiority to NSF OKN or another external system.

## Reproducibility

Run:

```bash
python benchmarks/okn_oi_v0_1.py
python -m unittest -v tests.test_okn_oi_benchmark
```

The benchmark uses only Python's standard library and deterministic fixtures.

## Funding relevance

NSF 26-512, *Unlocking Dataset Value for AI-Enabled Scientific Discovery (AI Datasets)*, has a 2026-11-04 full-proposal deadline and explicitly includes metadata generation, dataset integration/harmonization, automated analysis, and correction of noise or partial observations.

Source:
- https://www.nsf.gov/funding/opportunities/ai-datasets-unlocking-dataset-value-ai-enabled-scientific-discovery/nsf26-512/solicitation

This benchmark is **not itself an NSF proposal** and does not establish eligibility. A submission would require an eligible submitting organization and a project framed around the solicitation's scientific-dataset objectives.

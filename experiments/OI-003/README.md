# OI-003 — Provenance-Aware Epistemic Diversity Experiment

**Status:** Working research prototype / development benchmark (August 2026)  
**Part of:** Observer Intelligence v2.2

## Purpose

Test the core hypothesis of Observer Intelligence:

> Provenance-aware epistemic diversity produces safer decisions than numerical agent diversity alone.

We compare four architectures under controlled evidence conditions that include correlation, corruption, authority laundering, and measurement-integrity failures.

## Scientific status

The current six conditions are **development cases**, because the OI authority bound and the synthetic benchmark evolved within the same development process.

They demonstrate that the mechanisms can be implemented and that the architectures behave differently. They do **not yet establish independent superiority of OI**.

Confirmatory claims require a frozen OI implementation and held-out benchmark conditions developed without tuning to the OI scoring rule.

See `BENCHMARK-GUARDRAILS.md`.

## Architectures

1. **single_agent** — picks the highest-integrity observation
2. **majority_vote** — ordinary numerical majority
3. **adaptive_quorum** — integrity-weighted + source-diversity heuristic
4. **observer_intelligence** — OI authority bound using strength, independence, corruption penalties, and optional critic/reconciler analysis

The adaptive-quorum implementation is currently a research baseline, not a claim to reproduce every feature of published semantic-quorum systems. A confirmatory benchmark should include stronger externally specified baselines.

## Development conditions

- `independent_high_quality`
- `duplicated_as_independent` (false majority via shared source)
- `shared_corrupted_source`
- `authority_laundering`
- `minority_correct`
- `signed_but_inaccurate` (authenticated but low measurement integrity)

## Files

- `oi003_llm.py` — base LLM-integrated version
- `oi003_llm_extended.py` — adds an auxiliary LLM judge, multi-turn critic/reconciler debate, and JSONL provenance ledger
- `BENCHMARK-GUARDRAILS.md` — rules for held-out evaluation, judge independence, architecture freezing, ablations, and fair baselines

## Quick Start

```bash
# Rule-based development run; no API keys needed
python oi003_llm_extended.py --verbose

# With LLM critic/reconciler and auxiliary judge
export OPENAI_API_KEY=sk-...
python oi003_llm_extended.py --llm --model gpt-4o-mini --judge --verbose
```

## Metrics

Current prototype metrics include:

- approval rate
- unsupported claim rate
- false-consensus rate
- provenance completeness
- independence score
- auxiliary LLM-judge score

Confirmatory versions should also report calibration, abstention quality, provenance reconstruction accuracy, independence-estimation error, contradiction preservation, authority-lineage reconstruction, latency, and compute/token cost.

## LLM judge boundary

The optional LLM judge is an **auxiliary evaluator, not ground truth**.

Whenever deterministic truth is available, deterministic/external labels should be primary. When it is unavailable, blinded human adjudication or cross-model panels are preferable to relying on one LLM judge.

If the judge shares a model family with an observer, critic, reconciler, or other participant, that dependency must be recorded and reported because correlated model behavior can bias evaluation.

## Provenance Ledger

When run, the extended script writes `oi003_provenance.jsonl`. Each line is a timestamped, hashed event aligned with the Observer Intelligence Evidence Matrix.

The ledger supports reconstruction of experiment activity; hashing a record does not establish that the underlying observation or judgment is correct.

## Required confirmatory workflow

```text
1. freeze OI rule + thresholds + code commit
2. freeze baseline implementations
3. preregister primary metrics
4. create/reveal held-out benchmark
5. evaluate architectures under equivalent information access
6. score with deterministic/external ground truth where possible
7. run OI ablations
8. report failures as well as successes
```

## Relationship to the Paper

This experiment is the concrete testbed described in the OI-003 research program.

Current results may be reported as **prototype/development results showing differentiated behavior**. They should not be presented as independent evidence that OI is safer or superior until the held-out protocol in `BENCHMARK-GUARDRAILS.md` is completed.

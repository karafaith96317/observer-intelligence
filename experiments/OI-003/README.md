# OI-003 — Provenance-Aware Epistemic Diversity Experiment

**Status:** Working research prototype (August 2026)  
**Part of:** Observer Intelligence v2.2

## Purpose

Test the core hypothesis of Observer Intelligence:

> Provenance-aware epistemic diversity produces safer decisions than numerical agent diversity alone.

We compare four architectures under controlled evidence conditions that include correlation, corruption, authority laundering, and measurement-integrity failures.

## Architectures

1. **single_agent** — picks the highest-integrity observation
2. **majority_vote** — ordinary numerical majority
3. **adaptive_quorum** — integrity-weighted + source-diversity heuristic
4. **observer_intelligence** — full OI bound (strength × independence, corruption penalties, optional critic debate)

## Conditions

- `independent_high_quality`
- `duplicated_as_independent` (false majority via shared source)
- `shared_corrupted_source`
- `authority_laundering`
- `minority_correct`
- `signed_but_inaccurate` (authenticated but low measurement integrity)

## Files

- `oi003_llm.py` — base LLM-integrated version
- `oi003_llm_extended.py` — adds LLM-as-judge, multi-turn critic/reconciler debate, and JSONL provenance ledger

## Quick Start

```bash
# Rule-based only (no API keys needed)
python oi003_llm_extended.py --verbose

# With LLM observers + critic debate + judge
export OPENAI_API_KEY=sk-...
python oi003_llm_extended.py --llm --model gpt-4o-mini --judge --verbose
```

## Metrics

- Approval rate
- Unsupported claim rate
- False-consensus rate
- Provenance completeness
- Independence score
- LLM-as-judge score (optional)

## Provenance Ledger

When run, the extended script writes `oi003_provenance.jsonl`. Each line is a timestamped, hashed event aligned with the Observer Intelligence Evidence Matrix (observation, decision, critic debate, judge score, etc.).

## Relationship to the Paper

This experiment is the concrete testbed described in the OI-003 section of the Observer Intelligence research program. Results (even preliminary) can be included in the preprint as evidence that the authority-bound and independence estimation change decision behaviour under correlation and measurement-integrity stress.

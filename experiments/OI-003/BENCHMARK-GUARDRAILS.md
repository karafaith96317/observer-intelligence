# OI-003 — Benchmark Guardrails

## Purpose

This document defines safeguards intended to prevent OI-003 from validating Observer Intelligence using a benchmark that encodes the same assumptions as the OI decision rule.

The current prototype is a **mechanism demonstration**, not yet an independent validation study.

## Core rule

> Freeze the architecture before evaluating it on held-out conditions.

The OI authority function, thresholds, penalties, dependence rules, and reconciliation procedure used for confirmatory evaluation must be versioned and locked before the held-out benchmark is revealed or scored.

## Development vs confirmatory sets

Split benchmark conditions into:

### Development set

Used to debug implementation and explore candidate mechanisms.

Current synthetic conditions belong here unless independently regenerated:

- independent high-quality evidence
- duplicated evidence presented as independent
- shared corrupted source
- authority laundering
- correct minority observer
- signed/authenticated but inaccurate measurement

Results on this set are **illustrative**, not confirmatory.

### Held-out set

Must contain new combinations and failure modes not used to tune the OI bound.

Prefer generation or specification by an evaluator who did not tune the OI scoring function.

Candidate held-out dimensions:

- partial source correlation rather than exact duplication
- stale but authentic evidence
- incorrect high-integrity metadata
- provenance missing selectively rather than globally
- correct evidence arriving late
- multiple minority hypotheses with different independence structures
- adversarial provenance spoofing
- correlated model families with distinct prompts
- source identity collisions
- measurement drift
- contradictory evidence with matched nominal integrity
- asymmetric access that changes over time
- authority delegation chains of varying depth
- abstention-cost trade-offs

## Ground truth hierarchy

Evaluation should prefer, in order:

1. **Deterministic or externally specified ground truth** where the correct outcome is defined independently of all evaluated agents.
2. **Human expert adjudication**, blinded to architecture identity, when deterministic truth is unavailable.
3. **Cross-model or panel-based LLM evaluation** as a supplementary measurement.
4. **Single LLM judge** only as an exploratory metric.

An LLM judge must never be described as ground truth merely because it produces a numerical score.

## Judge independence

If LLM judges are used, record:

- model/provider
- model version
- system prompt
- temperature/sampling settings
- date/time
- whether the same or related model family participated as an observer, critic, reconciler, or authorizer

Where feasible, use judge models from a different model family than the agents being evaluated.

Report judge-model sensitivity rather than presenting one judge score as definitive.

## Architecture blinding

Where evaluators inspect natural-language outputs, hide the architecture label whenever possible.

A judge should evaluate the evidence/claim pair without being told whether the answer came from:

- single agent
- majority vote
- adaptive quorum
- Observer Intelligence

This reduces expectancy bias.

## Pre-registration / freeze record

Before confirmatory evaluation, record:

- commit SHA of each architecture
- exact OI authority-bound formula
- thresholds and penalties
- benchmark-generation procedure
- primary and secondary metrics
- exclusion criteria
- planned statistical analysis
- random seeds where applicable
- judge configuration

Optionally cryptographically timestamp this freeze record.

## Required comparison fairness

Each architecture should receive equivalent task information except where access asymmetry is itself the manipulated variable.

Do not give OI richer provenance metadata while withholding equivalent accessible metadata from baselines unless the experiment is explicitly testing the value of that metadata. In that case, report the comparison as an **information-architecture intervention**, not simply an algorithm comparison.

## Baseline strength

Do not intentionally weaken the adaptive-quorum baseline. Implement a credible version based on relevant prior art or invite an external contributor to provide one.

Where possible, compare against:

- plain majority
- confidence-weighted aggregation
- source-diversity weighting
- risk-adaptive quorum
- provenance-aware guard / delegation baseline
- OI ablations

## OI ablations

To identify which component matters, compare full OI against variants removing one mechanism at a time:

```text
OI minus dependence estimation
OI minus measurement integrity
OI minus provenance retention
OI minus critic/reconciler step
OI minus authority bound
OI minus adaptive observer expansion
```

This helps distinguish a genuine architecture effect from one favorable threshold or heuristic.

## Primary metrics

At minimum report:

- unsafe or unsupported approval rate
- false-consensus rate
- calibration
- abstention quality
- provenance reconstruction accuracy
- effective independence estimation error
- contradiction preservation
- authority-lineage reconstruction
- latency
- token / compute cost

## Failure reporting

A failed OI result is scientifically useful.

Record conditions where OI:

- rejects correct conclusions unnecessarily
- approves incorrect conclusions
- overweights misleading provenance
- incorrectly estimates independence
- performs worse than a simpler baseline
- becomes too costly or slow

Do not remove such cases from the benchmark after observing them without an explicit, documented reason.

## Claim language

Before independent held-out evaluation, use:

> "The prototype demonstrates a candidate mechanism and produces differentiated behavior in synthetic development cases."

Do not use:

> "OI has been proven safer" or "OI outperforms existing multi-agent systems."

After confirmatory evaluation, claims should match the exact benchmark scope and effect size.

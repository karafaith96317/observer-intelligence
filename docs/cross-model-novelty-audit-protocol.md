# Observer Intelligence — Cross-Model Novelty Audit Protocol

**Status:** Working adversarial review protocol — August 2026

## Purpose

This protocol uses multiple independent reviewers to attack Observer Intelligence (OI) before stronger novelty or performance claims are made. The objective is not to obtain consensus. The objective is to expose prior art, hidden dependence, unsupported claims, duplicated mechanisms, implementation gaps, and falsifiable alternatives while preserving reviewer provenance.

The protocol may use human reviewers and AI systems such as ChatGPT, Grok, Gemini, or other models. Model outputs are not treated as authoritative sources. Any literature, patent, technical, legal, or factual claim surfaced by a reviewer must be independently verified from primary or high-quality sources before it changes the canonical OI documentation.

## Core rule

> Reviewers should first evaluate the same frozen OI specification independently, without seeing one another's conclusions.

This reduces anchoring and makes convergence or contradiction more informative.

## Frozen review packet

Every audit round should identify the exact repository commit or release being reviewed and provide the same packet to every reviewer.

Minimum packet:

- `README.md`
- `docs/framework.md`
- `docs/evidence-matrix.md`
- `docs/novelty-claim-matrix.md`
- `docs/prior-art-and-novelty.md`
- `docs/research-refinement-protocol.md`
- relevant benchmark/code files
- a short statement of the candidate novelty claim

Each reviewer record should preserve:

- reviewer/model name and version when available
- date/time of review
- exact OI commit/ref reviewed
- exact prompt/instructions
- whether web/search tools were available
- cited sources supplied by the reviewer
- unverified claims requiring follow-up

## Standard independent audit prompt

Use the following prompt without showing the reviewer outputs from other reviewers:

```text
You are performing an adversarial research-novelty audit of Observer Intelligence (OI).

Do not try to make the framework sound impressive. Your task is to find reasons its novelty, technical claims, or research positioning may fail.

Evaluate the attached frozen OI specification and answer:

1. Which mechanisms are clearly established prior art?
2. What are the closest papers, systems, standards, patents, or research traditions for each mechanism?
3. Which OI claims are merely renamings or combinations of known techniques?
4. Which combinations appear less directly represented in existing work?
5. What is the smallest defensible candidate contribution?
6. What evidence would be required before that contribution could be called novel in a research sense?
7. What claims should OI explicitly stop making or narrow?
8. What hidden dependencies or common-mode failures does the architecture miss?
9. What competing architecture could achieve the same goal more simply?
10. What benchmark would most likely falsify the proposed OI advantage?
11. What mathematical definitions or operational variables remain underspecified?
12. Which sources from your answer must be independently verified?

Separate:
- established fact;
- source-supported inference;
- your own speculation.

Do not use agreement with the framework as evidence of correctness.
```

## Review roles

Independent reviewers may be assigned different attack roles after the first common audit.

### Prior-art reviewer

Searches for the closest mechanisms in multi-agent systems, truth maintenance, provenance/data lineage, runtime assurance, formal methods, safe RL, distributed systems, access control, security, decision theory, causal inference, and adjacent fields.

### Systems reviewer

Asks whether OI can actually be implemented, where state must be stored, how authority is enforced, what failure modes exist, and whether simpler architectures dominate it.

### Statistical reviewer

Attacks independence estimates, evidence weighting, calibration, drift, uncertainty, correlated observations, effective sample size, and authorization thresholds.

### Security reviewer

Attacks identity, replay, privilege inheritance, sybil behavior, compromised observers, poisoned provenance, reconciliation manipulation, authority escalation, and common-mode infrastructure.

### Scientific-method reviewer

Attacks falsifiability, benchmark construction, causal interpretation, post-hoc reasoning, confirmation bias, cherry-picking, and inappropriate generalization.

### Human-factors reviewer

Attacks assumptions about human observers, self-report, cognitive bias, selective disclosure, operator trust, interpretation, escalation, and handoff.

## Cross-review matrix

After independent reviews are complete, reconcile them without erasing disagreement.

| Candidate claim | Reviewer | Verdict | Closest prior art | Evidence/source | Confidence | Contradiction with another reviewer | Verification status | OI consequence |
|---|---|---|---|---|---|---|---|---|
| | | established / adjacent / candidate / rejected / unresolved | | | | | verified / unverified | |

The reconciliation should explicitly distinguish:

- independent convergence;
- convergence caused by shared source material;
- direct contradiction;
- terminology differences masking the same conclusion;
- novel criticism appearing in only one review;
- unsupported reviewer assertions;
- proposed experiments.

## Second-pass adversarial review

Only after the independent results are reconciled should reviewers see the cross-review synthesis.

Second-pass instruction:

```text
You are reviewing a reconciliation produced from several independent OI novelty audits.

Attack the reconciliation itself.

Identify:
- false consensus;
- unresolved contradictions;
- shared-source dependence between reviewers;
- prior art still missing;
- novelty claims that remain too broad;
- benchmark designs that favor OI unfairly;
- alternative explanations for any apparent OI advantage;
- changes that should be rejected rather than added to the framework.

State what would change your assessment.
```

## Acceptance rule

A candidate OI novelty claim should not be promoted merely because multiple models agree.

Before promotion, require:

1. primary-source verification of important prior-art claims;
2. a precise mechanism definition;
3. a clear difference from the closest baseline;
4. a falsifiable benchmark;
5. predefined outcome metrics;
6. a documented failure condition;
7. a provenance-preserving record of the audit round.

## Current candidate research contribution to attack

The present working candidate is the coupling of:

```text
observer-specific epistemic state
+ evidence-lineage dependence
+ time-varying independence
+ measurement / transformation / synchronization provenance
+ preservation of disagreement and minority evidence
+ freeze / preserve / handoff at epistemic or risk boundaries
+ evaluator succession without automatic authority inheritance
+ provenance-preserving reconciliation
+ evidence-constrained authorization
```

A narrower candidate question is:

> Does provenance-preserving recursive observer handoff reduce unsafe authorization and consequential evidence loss under correlated consensus, evaluator failure, evidence drift, and changing evidence compared with majority debate, confidence aggregation, dependency-aware backtracking, calibrated abstention, and runtime-assurance fallback baselines?

This is a candidate research target, not an established novelty claim.

## Cross-model development rule

AI systems may suggest changes, but the canonical repository should preserve the origin of consequential proposals whenever practical. Do not silently merge model-generated ideas into the framework and later treat their origin as unknowable.

Useful labels include:

- pre-existing OI concept;
- human collaborator proposal;
- ChatGPT proposal;
- Grok proposal;
- Gemini proposal;
- independently convergent proposal;
- external prior art;
- jointly refined mechanism.

## Outcome

The purpose of this process is to make the strongest version of OI smaller, more defensible, more testable, and easier for outside researchers to evaluate.

Consensus is not the success criterion. Surviving informed criticism is.
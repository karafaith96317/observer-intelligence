# Grok Prompt Pack — Adversarial / Red-Team Agent

**Role:** Adversarial attack and counterexample generation  
**Process:** `docs/collaboration/multi-model-process.md`  
**Contribution prefix:** `GROK-ATTACK-###` or `GROK-ALT-###`

## Core posture

Your job is to break the architecture, not to improve it by consensus. Prefer concrete failure modes, Sybil constructions, authority-escalation paths, stale-state attacks, incentive failures, and alternative explanations that remove the need for the proposed mechanism.

Do not soften findings to produce agreement with ChatGPT or Gemini.

## How to use

1. Freeze the current repo commit.
2. Give Grok the packet below without showing it Gemini or ChatGPT outputs for the same task on the first pass.
3. File the full response under a contribution ID and run it through the reconciliation template.

## Minimum context packet

- `README.md`
- `docs/framework.md`
- `docs/collaboration/multi-model-process.md`
- `docs/collaboration/test-matrix-v0.md`
- `docs/cross-model-novelty-audit-protocol.md`
- relevant experiment files under `experiments/OI-003/`
- exact commit hash

---

## Prompt 1 — Attack the minimal five-object runtime

```text
You are the adversarial red-team agent for Observer Intelligence (OI).

Target: the minimal runtime defined as

Observation Record → Authority Token → Shadow/Adversarial Evaluation → Reconciliation Record → Action Authorization

Your task is to find ways this loop can produce false authorization, evidence loss, authority escalation, or a false sense of safety.

Work through each of the eight conditions in the test matrix and, for each, supply:

1. A concrete attack or failure scenario (inputs, compromised components, timing).
2. Why a naive or even a careful implementation of the five objects would still fail or appear to succeed incorrectly.
3. The simplest change an attacker or a correlated failure could make to bypass the intended protection.
4. What metric would look “good” while the system is actually unsafe.

Also answer globally:

- How can Authority Tokens be minted, replayed, scope-expanded, or inherited improperly?
- How can Shadow/Adversarial Evaluation be starved of information, correlated with the primary path, or made to rubber-stamp?
- How can Reconciliation Records be complete on paper while minority or contradictory evidence is effectively neutralized?
- How can the system satisfy provenance-completeness checks while still authorizing on laundered authority?
- What is the smallest set of shared infrastructure (clocks, models, sensors, identity roots, software) that would collapse apparent independence?

Separate:
- demonstrated failure modes you can describe precisely;
- plausible but untested risks;
- speculative concerns.

Do not propose features unless they are required to state a counterexample. Prefer showing that a simpler baseline already fails (or succeeds) in the same way.
```

---

## Prompt 2 — Sybil, compromise, and authority-laundering constructions

```text
Construct explicit adversarial scenarios for Observer Intelligence under the following attack classes:

1. Sybil / majority hallucination from a shared source
2. Compromised observer that continues to produce well-formed Observation Records
3. Replay or cross-scope use of an Authority Token
4. Semantic leap: true observations → over-claim → authorization
5. Stale reconciled state after world change
6. Critic isolation failure (shadow evaluator receives correlated or filtered inputs)
7. Provenance forgery or selective omission that still passes a completeness check
8. Incentive or evaluation pressure that rewards authorization over abstention

For each construction provide:

- Actors and resources required
- Sequence of records that would be produced
- Why the five-object loop does not automatically stop the bad authorization
- The minimal additional rule or test that would catch it (if any)
- Whether a simple majority or confidence baseline fails the same way (important for novelty)

Be concrete. Prefer scenarios that could be turned into unit tests.
```

---

## Prompt 3 — Alternative explanations and simpler architectures

```text
For the claimed advantages of the OI five-object loop over ordinary multi-agent voting or confidence aggregation, supply alternative explanations:

1. What part of any apparent gain is simply “add a critic and an expiry timer”?
2. What part is already achievable with standard separation-of-duty, capability tokens, and audit logs?
3. Where does OI language rename existing provenance, RBAC, or runtime-assurance ideas without changing the failure surface?
4. Propose the simplest architecture that would still reduce false authorization under T02 (Sybil), T03 (minority counterevidence), and T05 (replay) without the full OI terminology.
5. State what experimental result would force you to abandon the claim that the OI coupling is doing necessary work.

Do not defend OI. The goal is to force the architecture lead to narrow claims to what survives this attack.
```

---

## Prompt 4 — Second-pass attack on a proposed reconciliation or merge

```text
You are reviewing a proposed merge or reconciliation of Gemini and/or ChatGPT outputs into the OI repository.

Attack the reconciliation itself:

- false consensus
- unresolved contradictions papered over
- shared-source dependence between the models
- claims that remain broader than the evidence
- test designs that favor OI
- authority or novelty language that exceeds the implementation
- anything that should be rejected rather than merged

State what would change your assessment and what must be tested before disposition ACCEPTED.
```

---

## Required return format

```text
Contribution ID: GROK-ATTACK-00X or GROK-ALT-00X
Date:
Commit reviewed:
Attack summary (short):
Concrete scenarios / counterexamples:
Affected test conditions (T01–T08):
Bypasses or metric illusions:
Simpler baseline comparison:
Recommended disposition: REJECT / NEEDS-TEST / ACCEPT-WITH-NARROWING / DEFER
Evidence or test that would change this assessment:
```

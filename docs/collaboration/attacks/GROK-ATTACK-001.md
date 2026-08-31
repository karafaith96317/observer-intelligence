# GROK-ATTACK-001 — First Red-Team Pass on Minimal OI Runtime

**Contribution ID:** GROK-ATTACK-001  
**Date:** 2026-08-31  
**Commit reviewed:** c994304e87a9c13bed85ea09c8558b4387cd8d61 (post-collaboration setup)  
**Role:** Adversarial / red-team  
**Disposition request:** NEEDS-TEST + several concrete narrowings

---

## Attack summary

The current Observation schema, the five-object target, and the v0.2 Authority Bound design targets leave multiple concrete bypasses that the test matrix (T01–T08) will not automatically catch unless the records and gates are tightened. The most severe classes are:

1. Provenance that is present but non-binding (completeness theater).
2. Independence that is declared rather than measured or adversarially tested.
3. Authority tokens that can be scope-expanded or replayed because binding rules are still underspecified.
4. Shadow/adversarial evaluation that can be correlated or starved without the system noticing.
5. “Right answer, wrong reasons” that current development metrics under-weight.

None of these are fatal to the research program. They are the exact failure modes the architecture claims to care about, so they should be turned into explicit unit-testable conditions before any implementation is treated as a candidate freeze.

---

## Concrete scenarios

### A. Completeness-theater provenance (affects T01, T02, T03, T07)

**Construction.**  
An Observation Record carries a full-looking `provenance` array and `epistemic_label`, passes the current JSON schema, and is linked from a Reconciliation Record. The actual supporting data (raw sensor frame, calibration state, upstream transformation code, shared model checkpoint) is omitted or replaced by a hash that no longer resolves. Reconciliation still reports “provenance completeness = 1.0” because the *fields exist*.

**Why the five-object loop fails.**  
The current `schemas/observation.schema.json` treats `provenance` as an optional array of strings and allows `additionalProperties`. There is no required binding between the provenance entries and retrievable artifacts, no requirement for measurement-integrity metadata, and no requirement that dependence links be machine-checkable. A Reconciliation Record can therefore be “complete” while the lineage is non-reconstructible in practice.

**Metric illusion.**  
Provenance-completeness score stays high; false-authorization rate can still be high.

**Minimal catch.**  
Require that every provenance reference either (a) resolves to an immutable artifact in the ledger or (b) is explicitly marked `unresolved` and forces an uncertainty/authority penalty. Completeness must be computed from resolvability, not field presence.

---

### B. Declared independence / soft Sybil (affects T02, T03)

**Construction.**  
Five Observation Records arrive with distinct `observer_id` values and high `confidence`. All five are generated from the same upstream retrieval, the same model checkpoint, or the same miscalibrated sensor after a one-line prompt wrapper. No exact `source_id` collision appears. Majority or confidence aggregation (and a naive OI path that only checks exact ID equality) treats them as independent.

**Why the loop fails.**  
v0.2 design targets correctly call for graded dependence ρ_ij, but it is not yet in the schema or the minimal five-object runtime. The test matrix’s T02 currently emphasizes exact duplication / shared source. Soft correlation will pass many implementations of T02.

**Metric illusion.**  
Independence score looks acceptable; adversarial success rate under soft Sybil is under-reported.

**Minimal catch.**  
Add an explicit T02b (soft-correlated majority) and require that any independence estimate used for authority is itself an Observation Record with its own provenance (so a wrong ρ can be attacked).

---

### C. Authority-token replay and scope expansion (affects T05)

**Construction.**  
An Authority Token is issued for scope `read-status` with a short expiry. The token object is later presented for scope `execute-action` or after expiry, either by replaying the original message or by a component that treats “previously authorized” as transitive. Because the five-object description does not yet mandate cryptographic binding of (scope × evidence_refs × expiry × issuer), a naive implementation stores a boolean `authorized=true`.

**Why the loop fails.**  
No schema or freeze exists yet for Authority Token. The process doc states tokens must be time- and scope-bounded and must reference evidence, but the enforceable representation is missing. T05 will only catch implementations that actually check expiry and scope; it will not catch those that collapse the token to a flag.

**Minimal catch.**  
Define a minimal Authority Token schema with required fields: `token_id`, `scope`, `not_before`, `not_after`, `evidence_refs[]`, `issuer`, `signature_or_mac`. Require the Action Authorization step to re-verify the signature and the still-valid evidence set, not merely the presence of a prior token.

---

### D. Critic starvation / correlated shadow (affects T04, T06, T07)

**Construction.**  
Shadow/Adversarial Evaluation receives only the already-interpreted claim, or receives the same upstream context as the primary interpreter, or is implemented as a second call to the same model family with a lightly rephrased prompt. It produces mild caveats that Reconciliation then treats as “critic has reviewed.” Semantic leaps and compromised-agent outputs survive.

**Why the loop fails.**  
Isolation is stated as a requirement (“isolatable until reconciliation”) but there is no required field for `input_scope`, `information_received`, `model_family`, or `correlation_with_primary`. Without those, T04 and T06 can be “passed” by a rubber-stamp critic.

**Minimal catch.**  
Shadow Evaluation records must declare the exact information set they received and whether their model/checkpoint/prompt overlaps the primary path. Overlap above a threshold forces an automatic independence penalty or escalation.

---

### E. Right answer, wrong reasons (meta-failure across T01–T08)

**Construction.**  
Under T03 (legitimate minority) the system withholds authorization for the correct reason on some runs and for an incorrect reason (e.g., blanket distrust of low-count majorities) on others. Aggregate “correct escalation rate” looks good. Process metrics (independence estimate, provenance reconstruction, contradiction preservation) are not yet required in the v0 test matrix metrics list as first-class pass/fail.

**Why it matters.**  
AUTHORITY-BOUND-v0.2 already states “Outcome correctness ≠ epistemic-process correctness.” The collaboration test matrix lists process metrics as “optional but recommended.” That gap lets a system look successful while violating the central OI claim.

**Minimal catch.**  
Promote at least three process metrics to required for any run that claims OI behavior: independence-estimation error, provenance reconstruction accuracy, contradiction preservation rate. A run that gets the action right but fails process metrics is scored as partial failure.

---

### F. Schema gap relative to framework claims

Current `observation.schema.json` required fields: `observation_id`, `observer_id`, `timestamp`, `epistemic_label`, `content`.

Framework and evidence-matrix claim many more first-class concerns: measurement integrity, temporal provenance (event vs capture vs processing), dependence links, disclosure boundary, authority role, unresolved questions, latent capability, etc.

**Attack consequence.**  
Any implementation that only validates the JSON schema can claim “schema-compliant OI records” while omitting the very fields the architecture says are necessary for authority. This is a direct route to completeness theater (scenario A).

**Minimal catch.**  
Either (1) expand the schema in stages with explicit `required` vs `recommended` tiers tied to authority level, or (2) make the Action Authorization step refuse high-authority decisions when critical integrity fields are absent (and record the refusal reason).

---

## Affected test conditions

| Condition | Attack relevance | Current gap |
|---|---|---|
| T01 Corrupted telemetry | High if measurement-integrity is optional | Schema does not require integrity metadata |
| T02 Sybil / majority hallucination | High for soft correlation | Only exact duplication is emphasized |
| T03 Minority counterevidence | Medium | Process metrics optional |
| T04 Semantic leap | High if critic is correlated | No input-scope binding for shadow eval |
| T05 Expired/replayed authority | High | No Authority Token schema yet |
| T06 Compromised agent | High | No required isolation/correlation fields |
| T07 Contradictory evidence | Medium–high | Completeness can be theater |
| T08 Rapidly changing world | Medium | Temporal fields underspecified in schema |

---

## Simpler baseline comparison

Several of the above failures also defeat plain majority and confidence aggregation. That is expected. The interesting claim for OI is that the *coupling* of provenance-preserving records + dependence awareness + critic isolation + bound authority reduces the failure rate relative to those baselines **for the right reasons**.

Until process metrics are required and soft-correlation / token-binding / critic-isolation are explicit, any apparent OI advantage on the current development set is under-determined. A simpler “majority + expiry timer + audit log” system may look similar on outcome metrics alone.

---

## Recommended disposition

**NEEDS-TEST**, with the following concrete follow-ups before any implementation is treated as a candidate freeze:

1. Add minimal schemas (or schema extensions) for Authority Token, Shadow Evaluation, Reconciliation Record, and Action Authorization, with binding fields for scope, expiry, evidence refs, input scope, and resolvable provenance.
2. Extend test matrix with T02b (soft-correlated majority) and make independence-estimation error, provenance reconstruction accuracy, and contradiction preservation **required** metrics.
3. Require that Action Authorization re-validates token binding and evidence freshness rather than trusting a stored flag.
4. Record any Gemini implementation proposal under GEM-IMPL-00X and run it against these attack scenarios before disposition ACCEPTED.

## Evidence that would change this assessment

- A frozen Authority Token schema that cryptographically binds scope × evidence_refs × time window and is checked at authorization time.
- A test run where soft-correlated Sybil is correctly down-weighted *and* the independence estimate itself is recoverable from the ledger.
- Process-metric failures that correctly cause partial-failure scoring even when the final action is right.

---

## Labels

```text
AI-GROK
GROK-ATTACK-001
NEEDS-TEST
```

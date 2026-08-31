# Gemini Prompt Pack — Implementation & Independent Critique

**Role:** Implementation / independent review agent  
**Process:** `docs/collaboration/multi-model-process.md`  
**Contribution prefix:** `GEM-IMPL-###` or `GEM-CRIT-###`

## How to use

1. Freeze the current repo commit (or attach the specific files listed below).
2. Paste the relevant prompt into Gemini.
3. Do not show Gemini the outputs of ChatGPT or Grok for the same task in the first pass.
4. Bring the full Gemini response back into the repo as a dated note or issue, assign an ID, and route it through the reconciliation template.

## Minimum context packet for Gemini

Attach or paste:

- `README.md`
- `docs/framework.md`
- `docs/collaboration/multi-model-process.md`
- `docs/collaboration/test-matrix-v0.md`
- `schemas/observation.schema.json` (if implementing records)
- any existing experiment code under `experiments/OI-003/` that is relevant

State the exact commit hash being reviewed.

---

## Prompt A — Implement the minimal runtime

```text
You are the implementation agent for Observer Intelligence (OI).

Your job is to implement, not to redesign the architecture from scratch.

Target: a minimal runtime with exactly these five typed objects and the transitions between them:

1. Observation Record
2. Authority Token
3. Shadow / Adversarial Evaluation
4. Reconciliation Record
5. Action Authorization

Requirements:
- Preserve provenance at every step.
- Do not collapse observation, interpretation, reconciliation, and authorization into a single score.
- Authority tokens must be time-bounded and scope-bounded and must reference evidence records.
- Shadow/adversarial evaluation must be isolatable until reconciliation.
- Reconciliation must retain disagreement, dependence estimates, and lineage rather than only a final answer.
- Action authorization is a gate that can refuse or escalate.

Deliverables:
1. Proposed data structures (Python dataclasses or JSON schemas).
2. Minimal pure-Python or lightly-dependent implementation of the five-object loop.
3. A simple runner that can execute the eight conditions in docs/collaboration/test-matrix-v0.md against both a majority-vote baseline and the OI loop.
4. Explicit list of assumptions you made where the OI spec is underspecified.
5. Tests or assertions that would fail if provenance is dropped or authority is unbound.

Do not add features beyond the five-object loop. If you believe a missing piece is necessary, list it under “Blocked / needs architecture decision” instead of implementing it.

Separate:
- what is required by the attached OI documents;
- what is your implementation choice;
- what is speculative.
```

---

## Prompt B — Independent critique of assumptions

```text
You are performing an independent implementation and systems critique of Observer Intelligence.

Do not try to make the framework succeed. Your job is to find where the current minimal design is underspecified, over-specified, impractical, or likely to fail under the test matrix.

Evaluate the attached OI documents and answer:

1. Which required fields for Observation Record, Authority Token, Reconciliation Record, and Action Authorization are still too vague to implement safely?
2. Where does the design assume independence that the test matrix will deliberately break?
3. What simpler architecture could pass the same development tests without the full OI machinery?
4. What state must be stored, for how long, and with what integrity guarantees?
5. How can authority tokens be forged, replayed, or scope-expanded in a naive implementation?
6. How can reconciliation silently drop minority evidence while still looking complete?
7. What latency or cost blow-ups are likely when shadow evaluation and provenance are added?
8. Which of the eight test conditions is most likely to produce a false sense of safety?
9. What would you refuse to implement until the architecture lead clarifies it?

Separate established constraints in the documents from your own engineering judgment.

Output a numbered list of concrete risks and a short “implementation blockers” section.
```

---

## Prompt C — Alternative design (optional, second pass)

```text
Given the same minimal five-object target, propose one substantially simpler alternative architecture that still attempts to reduce false authorization under Sybil pressure, corrupted telemetry, and minority counterevidence.

Constraints:
- It must still produce inspectable records.
- It must not rely on unbounded authority.
- Compare it honestly against the OI loop on the eight test conditions: where it is weaker, where it might be stronger, and where the difference is unclear without experiment.

Do not claim superiority. Provide a comparison table and the smallest experiment that would decide between the two.
```

---

## Return format for all Gemini outputs

Please structure the response so it can be filed under a contribution ID:

```text
Contribution ID: GEM-IMPL-00X or GEM-CRIT-00X
Date:
Commit reviewed:
Summary (3–5 sentences):
Concrete artifacts (code, schemas, lists):
Assumptions made:
Risks / blockers:
Proposed tests:
Disposition request: (accept / modify / reject / needs-architecture-decision)
```

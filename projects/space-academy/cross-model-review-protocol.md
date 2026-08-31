# Cross-Model Review Protocol — Space Academy Concept

Purpose: obtain independent criticism from multiple AI systems without collapsing them into premature consensus.

## Rule 1 — Independent first pass

Each reviewer receives the same frozen concept version and responds without seeing the other reviewers' conclusions.

Recommended roles:
- ChatGPT: specification, evidence discipline, federal/NASA alignment, synthesis.
- Gemini: scientific/technical completeness, implementation feasibility, missing disciplines, measurement design.
- Grok: adversarial review, failure modes, political/operational objections, assumptions likely to be attacked.

These roles are prompts, not authority rankings.

## Rule 2 — Require claim typing

Every major statement should be labeled as one of:
- ESTABLISHED: supported by accepted evidence or authoritative source.
- PROPOSED: program or engineering design not yet validated.
- HYPOTHESIS: empirical claim requiring testing.
- SPECULATIVE: low-evidence mechanism retained only as a testable research question.

## Rule 3 — Ask identical review questions

1. What are the five strongest components of this proposal?
2. What are the five weakest or least defensible components?
3. Which claims need citations or stronger evidence?
4. Which variables are confounded in the proposed experiments?
5. Which ethical, legal, privacy, biosafety, or discrimination risks are insufficiently addressed?
6. Which parts align directly with NASA/spaceflight needs?
7. Which parts should be removed from the initial federal brief but retained in research annexes?
8. What is the smallest credible pilot?
9. What metrics would falsify the central claims?
10. What important discipline, mechanism, or stakeholder is missing?
11. What would make a NASA/Commission reviewer reject this immediately?
12. What one change would most improve the proposal?

## Rule 4 — Capture disagreements

Do not average conflicting reviews into a generic middle position.

For each disputed issue record:
- reviewer;
- claim or recommendation;
- supporting reasoning/evidence;
- contradictory review;
- evidence needed to resolve;
- current disposition: ACCEPT / REJECT / TEST / DEFER / ANNEX.

## Rule 5 — Adversarial test unusual hypotheses

For antipodal, anomalous-information-transfer, resonance, consciousness, psychedelic, astrology-adjacent, or other frontier hypotheses, reviewers must ask:
- what known mechanism could explain the observation first?
- how can leakage/expectancy/selection bias be excluded?
- what prospective prediction distinguishes the hypothesis from controls?
- what result would count against the hypothesis?
- can an independent laboratory replicate it?

No frontier hypothesis is allowed to carry the credibility of the operational Academy proposal without separate evidence.

## Rule 6 — Federal-facing filter

For each component classify:
- GREEN — ready for main concept brief;
- YELLOW — technically promising but needs validation/citations;
- BLUE — useful research annex;
- RED — exclude from initial submission unless specifically requested.

## Version workflow

V0: frozen source concept.
GROK-R1: independent Grok review.
GEM-R1: independent Gemini review.
GPT-R1: independent ChatGPT review.
REC-1: comparison matrix identifying agreement/disagreement.
V1: revised concept with change log.

Never overwrite V0 or the raw reviews.

## Minimum output requested from each external model

Return:
1. executive assessment (max 300 words);
2. scored matrix from 1–5 for scientific defensibility, novelty, feasibility, NASA relevance, ethics, measurability, and clarity;
3. answers to the 12 review questions;
4. proposed pilot modifications;
5. list of claims requiring verification;
6. RED-team rejection case: strongest argument against funding the proposal.

## Canonical review prompt

Review the attached Space Academy Adaptive Operations & Research Academy concept as an independent technical reviewer. Do not assume its hypotheses are true. Separate established evidence from proposed architecture and speculative hypotheses. Evaluate scientific defensibility, NASA/spaceflight relevance, experimental design, confounds, ethics, feasibility, measurement, and federal-facing credibility. Preserve disagreements rather than trying to be agreeable. Answer all 12 review questions in the Cross-Model Review Protocol and provide the requested scored matrix, pilot modifications, verification list, and strongest rejection case.

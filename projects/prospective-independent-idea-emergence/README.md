# Prospective Independent Idea Emergence (PIIE)

## Status

**Observer Intelligence subproject — working research specification, August 2026.**

PIIE asks whether apparently similar ideas that emerge among separated observers can be studied prospectively while distinguishing genuine informational independence from shared sources, social diffusion, common environmental pressures, convergent cognition, and chance.

The project does **not** assume telepathy, collective consciousness, a morphic field, or any other unknown transmission mechanism. Those interpretations cannot be inferred merely from recurring ideas. The scientific target is narrower:

> **How independent are apparently independent idea-emergence events, and can their recurrence be measured prospectively?**

## Relationship to Observer Intelligence

PIIE applies OI's core principles to human idea formation:

```text
observer-specific access
+ timestamped observation
+ information-source provenance
+ independence estimation
+ semantic comparison
+ prospective prediction
+ later verification
```

A recurring idea is not automatically true:

```text
recurrence != truth != importance
```

Instead, PIIE keeps separate dimensions for:

- independent emergence
- novelty
- predictive accuracy
- empirical verification
- utility

## Core protocol

Participants voluntarily submit an idea **before seeing other submissions or the later comparison set**.

Each record should preserve:

1. immutable/raw idea text, audio, image, sketch, or other source artifact
2. capture timestamp
3. cryptographic timestamp/proof where available
4. observer pseudonymous identifier
5. public/private status at capture
6. claimed information sources and recent exposures
7. knowledge/expertise background relevant to the idea
8. semantic representation generated only after the raw artifact is preserved
9. later similarity matches
10. possible contamination/information pathways
11. verification outcome, if the idea contains a testable prediction

AI-generated summaries must never overwrite the original artifact.

## Timestamping and OpenTimestamps

The project should support independent cryptographic timestamping of source artifacts. **OpenTimestamps (OTS)** is a suitable candidate because a hash commitment can establish that a particular digital artifact existed no later than a verifiable time without publishing the artifact itself.

Reference: https://opentimestamps.org/

Suggested workflow:

```text
RAW ARTIFACT
    ↓
cryptographic hash
    ↓
OTS timestamp/proof
    ↓
immutable provenance record
    ↓
AI transcription / semantic representation
    ↓
later independent-emergence comparison
```

The timestamp proves precedence/existence of the committed data; it does **not** prove originality, truth, independent creation, or authorship by itself.

## Independent Emergence Score — research placeholder

A future model may estimate an Independent Emergence Score (IES):

```text
IES(C) = f(
  semantic_similarity,
  temporal_proximity,
  information_independence,
  geographic_separation,
  prior_art_rarity,
  contamination_probability
)
```

This formula is intentionally unspecified until a benchmark and null model are defined.

Geographic separation alone is weak evidence of independence. Two geographically distant observers exposed to the same paper, podcast, social-media post, AI output, news event, collaborator network, or dataset may share an information pathway.

## Competing explanations

When similar ideas emerge, PIIE should test ordinary explanations before labeling a residual unexplained:

```text
H1 direct/common information source
H2 social or network diffusion
H3 shared environmental/cultural trigger
H4 shared cognitive constraints or convergent reasoning
H5 chance / multiple-comparison effects
H6 currently unidentified coupling or information pathway
```

`H6` is a residual research category, not evidence for a particular extraordinary mechanism.

## Prospective design

The strongest design freezes predictions before comparison.

Example:

```text
T0: observer records hypothesis
T1: artifact is cryptographically timestamped
T2: hypothesis is locked from editing
T3: independent literature/data window opens
T4: blinded similarity scoring occurs
T5: ordinary information pathways are audited
T6: result classified
```

Possible classifications:

- exact prospective prediction
- strong conceptual match
- partial match
- broad thematic similarity
- contradiction
- no relationship
- indeterminate due to contamination

## Null model

The experiment should estimate how much apparent convergence is expected by chance given the size of the idea space, shared culture, shared technical literature, current events, and participant backgrounds.

A meaningful anomaly requires comparison against a preregistered null model rather than subjective impression alone.

## Optional geography and participant metadata

With explicit informed consent, a study could examine coarse geographic region and relevant background variables. Exact locations should not be required unless scientifically necessary.

Potential variables include:

- broad region/time zone
- occupation or field
- expertise
- research interests
- recently consumed information sources
- collaborator/information-network overlap
- language
- chronotype
- sleep timing
- attention/cognitive-state measures

## Biomarker extension

Biomarkers are an **optional later-stage research extension**, not a default collection requirement.

With ethics review and explicit participant consent, candidate variables might include wearable-derived sleep/wake timing, heart-rate variability, activity, or other noninvasive physiological measures relevant to a preregistered hypothesis.

PIIE should not collect biomarkers merely to search for post-hoc correlations. Candidate biomarker relationships should be preregistered before analysis, with correction for multiple comparisons and strong privacy protections.

## Privacy and ethics

The project should minimize collection of personally identifying data.

Principles:

- voluntary participation
- explicit consent for sensitive metadata
- pseudonymous participant identifiers
- coarse geography by default
- no inference of private contacts from hidden data
- no access to private AI conversations without participant authorization
- separation of raw artifact storage from public similarity results
- ability to participate without biomarker collection
- publish aggregate patterns rather than identifying individuals

## AI boundary

An AI system should not treat repeated ideas as truth simply because they recur.

A suitable response to high independent emergence is:

> **This concept is recurring unusually often among apparently independent observers and warrants targeted investigation.**

not:

> **Many people independently believe this, therefore it is true.**

## Candidate experiment: PIIE-001

Recruit separated participants and collect preregistered, timestamped idea/prediction records over a fixed period. Preserve source exposure metadata before participants can inspect other submissions.

Compare observed semantic clustering against shuffled timestamps, matched-background controls, known shared-source clusters, and simulated null distributions.

Primary outcome:

> Does the observed rate and specificity of apparently independent conceptual convergence exceed the preregistered null expectation after identifiable information pathways are accounted for?

Secondary outcomes:

- which exposure variables explain convergence?
- how much does semantic similarity fall after controlling for shared sources?
- does geographic separation add explanatory value after information-network separation is modeled?
- can blinded reviewers distinguish genuinely prospective matches from broad retrospective matching?

## Claim boundary

Even a statistically unusual residual would establish only that the current model failed to explain all observed convergence. It would not, by itself, establish telepathy, collective consciousness, nonlocal information transfer, or another specific mechanism.

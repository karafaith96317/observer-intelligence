# Observer Intelligence — Evidence Status Policy

**Purpose:** keep repository claims auditable by separating what is externally established, what this repository has reproduced, what is experimentally suggested, and what remains hypothetical or speculative.

This policy governs research findings, architecture notes, benchmark reports, issue/PR summaries, README claims, and future evidence-ledger entries.

## Canonical statuses

### VERIFIED EXTERNAL EVIDENCE
Use when a factual claim is supported by a traceable primary source or a high-quality secondary source whose underlying evidence can be identified.

Required fields:
- source title / organization / authors;
- publication or release date when available;
- persistent URL, DOI, or equivalent locator;
- concise statement of what the source actually establishes;
- explicit evidence boundary describing what it does **not** establish.

A verified external source can support or motivate OI. It does **not** validate OI merely because the findings are analogous or compatible.

### REPRODUCED REPOSITORY RESULT
Use when executable repository code produces the stated result under a documented procedure.

Required fields:
- commit SHA;
- exact test or command;
- input/fixture identity;
- observed result;
- scope of the claim.

Passing tests show behavior for the tested cases. They do not establish production safety, external validity, superiority over alternatives, absence of vulnerabilities, or general correctness.

### EXPERIMENTAL RESULT
Use for outputs from simulations, synthetic data, controlled prototypes, benchmark runs, or exploratory experiments.

Required fields:
- experimental setup;
- data nature (`synthetic`, `simulated`, `observational`, `external benchmark`, etc.);
- comparison/baseline when applicable;
- metrics;
- limitations and unresolved confounds.

Synthetic or simulated outcomes must never be described as evidence of real-world deployment performance.

### ARCHITECTURAL HYPOTHESIS
Use for a proposed mechanism, design principle, mathematical relationship, causal explanation, predicted benefit, or testable research claim.

Examples:
- separated authority may reduce unsafe action;
- provenance-preserving reconciliation may improve auditability;
- dependence-aware evidence counting may reduce false confidence.

Such statements should be written in falsifiable form where possible and linked to a proposed or completed test.

### SPECULATIVE / UNVERIFIED
Use for interesting but insufficiently sourced claims, analogies, personal interpretations, unconfirmed reports, theoretical extensions without tests, or claims whose underlying source cannot yet be validated.

Speculative material may remain in the repository when it is useful for hypothesis generation, but it must not be promoted into the verified evidence record or cited as support for an engineering claim.

### SUPERSEDED
Use when a claim, implementation, result, or interpretation has been replaced or corrected.

Do not silently delete the old state when its existence is important to provenance. Record:
- superseding commit/document;
- reason for replacement;
- date of change.

## Current prototype classification

`src/oi_runtime_v0_1.py` is an **experimental reference implementation**, not a production runtime.

`tests/test_runtime_v0_1.py` provides reproducible repository tests for selected mechanisms, including:

1. an adversarial/shadow contradiction causing a contested reconciliation state and denying execution;
2. nonce replay rejection after a successful authorization; and
3. prevention of escalation from inference scope to execution scope.

These are **REPRODUCED REPOSITORY RESULTS** only when the tests are executed successfully at a specified commit and the command/result are recorded. The mere presence of the test code is evidence that the tests are defined, not proof that they passed on every commit or environment.

## Claim construction rule

Every consequential research entry should separate the chain:

```text
SOURCE / OBSERVATION
        ↓
WHAT IS ESTABLISHED
        ↓
UNCERTAINTY / LIMITATION
        ↓
OI INTERPRETATION
        ↓
TESTABLE CONSEQUENCE
```

The OI interpretation should never be written as though it were part of the external source unless the source explicitly makes that claim.

## Provenance is not truth

Cryptographic hashes, signatures, timestamps, append-only ledgers, authenticated identities, and reproducible logs can strengthen integrity and provenance. They cannot by themselves establish:

- factual truth of the underlying observation;
- physical measurement accuracy;
- independence of observers;
- correctness of interpretation;
- originality or inventorship;
- ethical legitimacy;
- authorization to act.

## Independence rule

Agreement among multiple agents, models, sensors, people, papers, or news reports should not automatically be counted as independent corroboration. Shared upstream sources, prompts, training data, instrumentation, synchronization systems, institutions, or copied reports should be represented as possible common-mode dependencies.

`N observers` must not be treated automatically as `N independent evidence pathways`.

## Human and anomalous-experience boundary

A first-person report can be valid evidence that an experience, perception, memory, or interpretation was reported. It is not automatically independent evidence that the experience's external-world interpretation occurred as perceived.

Claims involving nonlocal consciousness, telepathy, hidden entities, anomalous information transfer, or similar extraordinary mechanisms remain **SPECULATIVE / UNVERIFIED** unless supported by appropriately controlled, independently reproducible evidence.

## External research ingestion checklist

Before research is promoted into the verified evidence record:

1. verify the source exists and matches the claimed date/title/authors;
2. prefer primary literature, official technical documentation, standards bodies, or reputable reporting with identifiable evidence;
3. record whether the source is peer reviewed, preprint, institutional announcement, company report, journalism, or other;
4. summarize the actual demonstrated result rather than the headline;
5. document important limitations, negative findings, and alternative explanations;
6. distinguish direct relevance from analogy;
7. identify any prior art or overlapping work that deserves credit;
8. convert the OI connection into a falsifiable test when feasible.

## Repository review rule

Future cleanup should prefer relabeling, correction, and supersession over deletion. Historical mistakes can be useful provenance if their status is unmistakable. Unsupported claims should not remain in locations where a reader could reasonably mistake them for established project results.

The governing standard is:

> **The strength of a repository claim must not exceed the strength, independence, and reproducibility of its evidence.**

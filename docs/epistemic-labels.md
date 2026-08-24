# Epistemic Labels

Observer Intelligence separates **what was observed** from **what is inferred from the observation**.

## Initial vocabulary

### `direct_observation`
Information directly available to an observer through an identified input channel.

### `subjective_report`
A first-person or agent-generated report of an internal state, perception, interpretation, or experience.

### `externally_verified`
A claim supported by evidence independent of the originating observer.

### `inference`
A conclusion derived from one or more observations but not itself directly observed.

### `hypothesis`
A proposed explanation that can potentially be tested against additional evidence.

### `prediction`
A claim about an observation expected to occur after the prediction is registered.

### `symbolic_interpretation`
Meaning assigned through symbolic, metaphorical, archetypal, phenomenological, or interpretive systems. This label preserves the interpretation without representing it as independently established physical fact.

### `simulated_result`
An output produced inside a model, sandbox, counterfactual environment, or other simulation.

### `unresolved_contradiction`
Two or more observations or claims that cannot currently be reconciled without discarding information.

## Separation rule

One record may contain several layers:

```text
OBSERVATION: A participant reports hearing a voice.
INTERPRETATION: The participant attributes the voice to source X.
VERIFICATION: No independent measurement of source X is available.
STATUS: subjective_report + hypothesis
```

The framework preserves all three statements rather than either validating the attribution or deleting the experience.

## Why this matters

Intelligent systems routinely encounter ambiguous evidence. Without explicit epistemic labels, inference can become indistinguishable from observation, model output can become indistinguishable from measurement, and repeated claims can acquire false authority through repetition alone.

OI treats epistemic state as first-class data.

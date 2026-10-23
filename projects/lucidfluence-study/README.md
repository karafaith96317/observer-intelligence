# LucidFluence historical provenance and streaming study

Originator: Kara Faith Sypen. Implementation assistance: OpenAI ChatGPT, 2026-10-15.

Purpose: preserve the supplied LucidFluence / ERA-GOS / OI material and study whether explicit provenance prevents simulated tier and resonance reports from acquiring operational authority.

## Dataset

`data/source.txt` preserves the complete supplied text, including architecture proposals, Python snippets, weekly narratives, routing designs, multi-model contribution plans, and reported JSON blocks. It is an inert historical source, never executed or imported as Python. Model names and contribution IDs in the source are reported attributions, not independently verified contributions.

`data/records.jsonl` contains 20 complete outer JSON record occurrences (19 unique objects). Duplicates are preserved and marked; incomplete snippets, code-defined fixtures, and prose remain in the source. This is not a claim that all historical reports supplied valid JSON. Character ranges use decoded Unicode character offsets. The manifest binds the original bytes and final chain head. Reimport is deterministic.

Imported metrics are SIMULATED and SPECULATIVE / UNVERIFIED. In particular, names of external collectives, Cleveland grid nodes, blocked probes, mTLS sessions, anchor counts, solar effects, fee savings, and RAP coherence are unverified assertions. No raw deployment telemetry accompanied the text. Original hashes, dates, chain links, and anchor labels are retained as claims; they are not adopted as the new chain. The new chain starts at zero and is NOT_ANCHORED.

## Run from repository root

```bash
python src/lucidfluence_study.py verify projects/lucidfluence-study/data
python src/lucidfluence_study.py replay projects/lucidfluence-study/data --limit 20 --interval 1
python -m unittest discover -s tests -p test_lucidfluence_study.py -v
```

Replay emits flushed JSON events at a requested wall-clock interval with new replay timestamps, source record IDs, and historical tier fields. This is a bounded real-time simulation process, not historical-time reconstruction, a deployed service, or live monitoring. Interval is pacing, not a scheduling guarantee. Start it on a persistent host to run outside this session; no background service is installed here.

To regenerate into a NEW directory:

```bash
python src/lucidfluence_study.py import projects/lucidfluence-study/data/source.txt /tmp/lf-study-rebuilt
```

## Architecture and scope

Source text → extracted source-bound simulation records → integrity verification → paced read-only event stream. This companion module does not alter the existing OI authorization engine or grant any execution authority. Every replay event has `execution_permitted: false`.

Tier 0 internal loopback, Tier 1 candidate peers, Tier 2 collaborators, and Tier 3 quarantine are historical scenario labels. RAP is a reported dimensionless scenario score with no validated measurement formula. GVP is ambiguous in the source (Global Validation Protocol versus Geofenced Variable Power); no unified physical interpretation is asserted. The supplied threshold and score designs are hypotheses, not validated biological or security measurements.

Future observed ingestion requires a separate adapter, authenticated source identity, raw artifact bytes/hash, capture and ingest times, units, calibration/uncertainty, and consent where relevant. Derived results must list all parent record hashes and retain simulated ancestry. Supplying a label such as OBSERVED must never alone establish empirical validity. No observed or hybrid adapter is implemented by this slice.

## Study hypotheses

LF-H001: Source-bound records permit detection of edited source bytes, edited records, and truncated histories. Test against unchanged imports; require every defined tamper fixture to fail verification. This tests integrity only.

LF-H002: Reimporting identical bytes produces byte-identical records and chain heads. Compare two imports; any mismatch fails. New replay timestamps are intentionally excluded from this prediction.

LF-H003: Paced replay preserves simulation labels and denies execution on every output. Test every replayed fixture; any empirical relabel or permitted execution fails. This does not establish production authorization safety.

## Limitations and remaining designs

The full source preserves broader specifications: three lineage graphs, multi-observer adjudication, scoped tokens, nonce persistence, Tier 0 loopback routing, collaboration attribution, and benchmark proposals. These are not silently installed from conversation code. Existing OI runtime remains an experimental reference implementation; asymmetric signing, independently measured resonance, external attack detection, peer enrollment, OpenTimestamps anchoring, continuous hosting, notifications, and cross-model result verification are not added here.

The chain is tamper-evident only relative to a trusted manifest/head. An attacker able to rewrite source, records, and manifest can regenerate a consistent chain. It is neither immutable storage nor an external timestamp proof. Import time cannot prove historical creation time. Tests cover bounded fixtures, not general security or empirical efficacy. See [the evidence policy](../../docs/EVIDENCE_STATUS.md).

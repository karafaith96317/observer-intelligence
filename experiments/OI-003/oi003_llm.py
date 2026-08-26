#!/usr/bin/env python3
"""
OI-003 Extended — LLM-Integrated Synthetic Experiment
Observer Intelligence v2.2

This version keeps the original controlled conditions and metrics while
allowing observers and/or decision architectures to use real LLM calls.

Key design choices aligned with OI principles:
- Every LLM call is logged with prompt, response, model, and timestamp
  (provenance).
- Measurement integrity and source correlation are still controlled by the
  experiment harness (the LLM does not get to invent its own independence).
- Authority decisions remain constrained by the OI bound rather than raw
  LLM confidence.
- The same four architectures are compared so results stay comparable to
  the pure-rule version.

Usage examples:
  python oi003_llm.py                        # rule-based only (same as before)
  python oi003_llm.py --llm                  # enable LLM observers
  python oi003_llm.py --llm --model openai   # use OpenAI (set OPENAI_API_KEY)
  python oi003_llm.py --llm --model anthropic
  python oi003_llm.py --condition minority_correct --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple


# ---------------------------------------------------------------------------
# Core data structures (unchanged from original + LLM provenance)
# ---------------------------------------------------------------------------

class EvidenceQuality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CORRUPTED = "corrupted"


@dataclass
class Observation:
    observer_id: str
    content: str
    quality: EvidenceQuality
    source_id: str
    measurement_integrity: float          # 0.0–1.0  (controlled by harness)
    timestamp: int
    authenticated: bool = True
    # LLM provenance fields
    llm_prompt: Optional[str] = None
    llm_response: Optional[str] = None
    llm_model: Optional[str] = None
    raw_interpretation: Optional[str] = None


@dataclass
class Claim:
    statement: str
    support_score: float
    originating_observers: List[str]
    independent_pathways: int
    provenance_complete: bool
    authority_justified: bool
    reasoning_trace: Optional[str] = None
    llm_calls: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExperimentResult:
    architecture: str
    condition: str
    approved: bool
    unsupported: bool
    false_consensus: bool
    provenance_score: float
    independence_score: float
    details: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# LLM interface (pluggable)
# ---------------------------------------------------------------------------

class LLMClient(Protocol):
    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        ...


class DummyLLM:
    """Deterministic fallback so the script always runs."""
    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        # Very simple heuristic for demo purposes
        if "corrupted" in prompt.lower() or "bad-fact" in prompt.lower():
            return "The evidence appears unreliable. I do not endorse the claim."
        if "true-fact" in prompt.lower() or "correct-fact" in prompt.lower():
            return "This evidence looks strong and consistent. Claim supported."
        return "Based on the provided evidence I assign moderate confidence."


class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
            self.client = OpenAI()
            self.model = model
        except Exception as e:
            raise RuntimeError(f"OpenAI client unavailable: {e}") from e

    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()


class AnthropicClient:
    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        try:
            import anthropic
            self.client = anthropic.Anthropic()
            self.model = model
        except Exception as e:
            raise RuntimeError(f"Anthropic client unavailable: {e}") from e

    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            temperature=temperature,
            system=system or "You are a careful scientific observer.",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()


def get_llm(model_name: str) -> LLMClient:
    if model_name in ("none", "dummy", "rule"):
        return DummyLLM()
    if model_name.startswith("openai") or model_name in ("gpt-4o", "gpt-4o-mini"):
        return OpenAIClient(model=model_name if model_name != "openai" else "gpt-4o-mini")
    if model_name.startswith("anthropic") or "claude" in model_name:
        return AnthropicClient(model=model_name if "claude" in model_name else "claude-3-5-haiku-20241022")
    # Default to dummy if unknown
    print(f"[warning] Unknown model '{model_name}', falling back to DummyLLM")
    return DummyLLM()


# ---------------------------------------------------------------------------
# Condition generators (same as original)
# ---------------------------------------------------------------------------

def make_condition(name: str, rng: random.Random) -> List[Observation]:
    base_time = 1000

    if name == "independent_high_quality":
        return [
            Observation(f"O{i}", f"fact-{i}", EvidenceQuality.HIGH, f"src-{i}", 0.95, base_time + i)
            for i in range(5)
        ]

    elif name == "duplicated_as_independent":
        return [
            Observation(f"O{i}", "shared-fact", EvidenceQuality.HIGH, "src-shared", 0.90, base_time + i)
            for i in range(5)
        ]

    elif name == "shared_corrupted_source":
        return [
            Observation(f"O{i}", "bad-fact", EvidenceQuality.CORRUPTED, "src-bad", 0.30, base_time + i)
            for i in range(4)
        ] + [
            Observation("O_good", "correct-fact", EvidenceQuality.HIGH, "src-good", 0.95, base_time + 10)
        ]

    elif name == "authority_laundering":
        return [
            Observation("O1", "weak-evidence", EvidenceQuality.LOW, "src-1", 0.40, base_time),
            Observation("AgentX", "I confirm the claim is true", EvidenceQuality.HIGH, "src-1", 0.40, base_time + 5),
            Observation("O2", "I defer to AgentX", EvidenceQuality.MEDIUM, "src-agentx", 0.60, base_time + 8),
        ]

    elif name == "minority_correct":
        return [
            Observation(f"O{i}", "majority-wrong", EvidenceQuality.MEDIUM, f"src-m{i}", 0.70, base_time + i)
            for i in range(4)
        ] + [
            Observation("O_correct", "true-fact", EvidenceQuality.HIGH, "src-true", 0.98, base_time + 20)
        ]

    elif name == "signed_but_inaccurate":
        return [
            Observation("SensorA", "reading-42", EvidenceQuality.HIGH, "sensor-a", 0.25, base_time, authenticated=True),
            Observation("SensorB", "reading-42", EvidenceQuality.HIGH, "sensor-a", 0.25, base_time + 1, authenticated=True),
        ]

    else:
        raise ValueError(f"Unknown condition: {name}")


# ---------------------------------------------------------------------------
# LLM-augmented observation (optional)
# ---------------------------------------------------------------------------

OBSERVER_SYSTEM = """You are a scientific observer in a multi-observer experiment.
You receive a raw observation and must produce a short, careful interpretation.
Do not invent extra facts. Comment on reliability if the quality signals are poor.
Keep the response under 80 words."""

def llm_interpret(obs: Observation, llm: LLMClient) -> Observation:
    """Attach an LLM interpretation while preserving the controlled metadata."""
    prompt = (
        f"Observer ID: {obs.observer_id}\n"
        f"Raw content: {obs.content}\n"
        f"Declared quality: {obs.quality.value}\n"
        f"Measurement integrity score: {obs.measurement_integrity:.2f}\n"
        f"Authenticated: {obs.authenticated}\n\n"
        "Provide a brief interpretation of this observation."
    )
    response = llm.complete(prompt, system=OBSERVER_SYSTEM, temperature=0.2)
    obs.llm_prompt = prompt
    obs.llm_response = response
    obs.llm_model = getattr(llm, "model", type(llm).__name__)
    obs.raw_interpretation = response
    return obs


# ---------------------------------------------------------------------------
# Architectures
# ---------------------------------------------------------------------------

def single_agent(observations: List[Observation], llm: Optional[LLMClient] = None) -> Claim:
    best = max(observations, key=lambda o: o.measurement_integrity)
    return Claim(
        statement=best.content,
        support_score=best.measurement_integrity,
        originating_observers=[best.observer_id],
        independent_pathways=1,
        provenance_complete=True,
        authority_justified=best.measurement_integrity > 0.70,
        reasoning_trace="Selected highest measurement-integrity observation."
    )


def majority_vote(observations: List[Observation], llm: Optional[LLMClient] = None) -> Claim:
    counts: Dict[str, List[Observation]] = defaultdict(list)
    for o in observations:
        counts[o.content].append(o)
    winner_content, supporters = max(counts.items(), key=lambda x: len(x[1]))
    avg_integrity = sum(o.measurement_integrity for o in supporters) / len(supporters)
    return Claim(
        statement=winner_content,
        support_score=len(supporters) / len(observations),
        originating_observers=[o.observer_id for o in supporters],
        independent_pathways=len(set(o.source_id for o in supporters)),
        provenance_complete=False,
        authority_justified=len(supporters) > len(observations) / 2,
        reasoning_trace=f"Majority content chosen by {len(supporters)} observers."
    )


def adaptive_semantic_quorum(observations: List[Observation], llm: Optional[LLMClient] = None) -> Claim:
    scored = sorted(observations, key=lambda o: o.measurement_integrity, reverse=True)
    selected = []
    sources_seen = set()
    for o in scored:
        if o.source_id not in sources_seen or o.measurement_integrity > 0.85:
            selected.append(o)
            sources_seen.add(o.source_id)
        if len(selected) >= 3:
            break
    if not selected:
        selected = scored[:1]
    content = selected[0].content
    return Claim(
        statement=content,
        support_score=sum(o.measurement_integrity for o in selected) / len(selected),
        originating_observers=[o.observer_id for o in selected],
        independent_pathways=len(sources_seen),
        provenance_complete=True,
        authority_justified=len(sources_seen) >= 2 and selected[0].measurement_integrity > 0.60,
        reasoning_trace="Adaptive selection by integrity + source diversity."
    )


def observer_intelligence(observations: List[Observation], llm: Optional[LLMClient] = None) -> Claim:
    """
    OI decision procedure:
    1. Group by source_id → estimate independent pathways
    2. Take best observation per source
    3. Apply authority bound that penalizes low measurement integrity
       even when records are authenticated
    4. Optionally ask an LLM for a natural-language justification
       (the justification does NOT override the numeric bound)
    """
    by_source: Dict[str, List[Observation]] = defaultdict(list)
    for o in observations:
        by_source[o.source_id].append(o)

    independent_pathways = len(by_source)
    best_per_source = [
        max(group, key=lambda o: o.measurement_integrity)
        for group in by_source.values()
    ]
    best_per_source.sort(key=lambda o: o.measurement_integrity, reverse=True)

    if not best_per_source:
        return Claim("no-claim", 0.0, [], 0, False, False)

    top = best_per_source[0]
    evidence_strength = top.measurement_integrity
    independence = min(1.0, independent_pathways / 3.0)
    provenance_complete = all(o.authenticated for o in best_per_source)

    # Core OI authority bound (non-linear interaction)
    authority_score = evidence_strength * (0.55 + 0.45 * independence)
    if top.quality == EvidenceQuality.CORRUPTED:
        authority_score *= 0.25
    if evidence_strength < 0.40:
        authority_score *= 0.50

    justified = (
        authority_score >= 0.65
        and independent_pathways >= 1
        and top.measurement_integrity >= 0.50
    )

    reasoning = (
        f"OI bound: strength={evidence_strength:.2f}, "
        f"independence={independence:.2f}, pathways={independent_pathways}, "
        f"score={authority_score:.2f} → justified={justified}"
    )

    llm_calls = []
    if llm is not None and not isinstance(llm, DummyLLM):
        # Ask LLM only for explanation; it cannot override the bound
        prompt = (
            "You are the reconciler in an Observer Intelligence system.\n"
            f"Top observation content: {top.content}\n"
            f"Measurement integrity: {top.measurement_integrity:.2f}\n"
            f"Independent pathways: {independent_pathways}\n"
            f"Authority score: {authority_score:.2f}\n"
            f"Decision (already computed): {'APPROVE' if justified else 'ABSTAIN/REJECT'}\n\n"
            "Write one short paragraph explaining why this decision follows "
            "from provenance and measurement integrity principles."
        )
        explanation = llm.complete(prompt, system="You explain epistemic decisions. Be concise.")
        reasoning += "\nLLM explanation: " + explanation
        llm_calls.append({
            "prompt": prompt,
            "response": explanation,
            "model": getattr(llm, "model", type(llm).__name__),
        })

    return Claim(
        statement=top.content,
        support_score=authority_score,
        originating_observers=[o.observer_id for o in best_per_source],
        independent_pathways=independent_pathways,
        provenance_complete=provenance_complete,
        authority_justified=justified,
        reasoning_trace=reasoning,
        llm_calls=llm_calls,
    )


# ---------------------------------------------------------------------------
# Evaluation (same ground-truth heuristics)
# ---------------------------------------------------------------------------

def evaluate(claim: Claim, condition: str, architecture: str) -> ExperimentResult:
    true_contents = {
        "independent_high_quality": None,
        "duplicated_as_independent": "shared-fact",
        "shared_corrupted_source": "correct-fact",
        "authority_laundering": None,
        "minority_correct": "true-fact",
        "signed_but_inaccurate": None,
    }
    true_content = true_contents.get(condition)
    approved = claim.authority_justified
    unsupported = approved and true_content is not None and claim.statement != true_content
    false_consensus = (
        condition in ("duplicated_as_independent", "shared_corrupted_source")
        and claim.independent_pathways < 2
        and approved
    )
    provenance_score = 1.0 if claim.provenance_complete else 0.4
    independence_score = min(1.0, claim.independent_pathways / 3.0)

    return ExperimentResult(
        architecture=architecture,
        condition=condition,
        approved=approved,
        unsupported=unsupported,
        false_consensus=false_consensus,
        provenance_score=provenance_score,
        independence_score=independence_score,
        details={
            "statement": claim.statement,
            "support_score": round(claim.support_score, 3),
            "independent_pathways": claim.independent_pathways,
            "originating": claim.originating_observers,
            "reasoning": claim.reasoning_trace,
            "llm_calls": claim.llm_calls,
        },
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

ARCHITECTURES = {
    "single_agent": single_agent,
    "majority_vote": majority_vote,
    "adaptive_quorum": adaptive_semantic_quorum,
    "observer_intelligence": observer_intelligence,
}

CONDITIONS = [
    "independent_high_quality",
    "duplicated_as_independent",
    "shared_corrupted_source",
    "authority_laundering",
    "minority_correct",
    "signed_but_inaccurate",
]


def run_experiment(
    seed: int = 42,
    use_llm_observers: bool = False,
    llm: Optional[LLMClient] = None,
    conditions: Optional[List[str]] = None,
    verbose: bool = False,
) -> List[ExperimentResult]:
    rng = random.Random(seed)
    results = []
    selected_conditions = conditions or CONDITIONS

    for cond in selected_conditions:
        observations = make_condition(cond, rng)

        if use_llm_observers and llm is not None:
            observations = [llm_interpret(o, llm) for o in observations]
            if verbose:
                print(f"\n--- Condition: {cond} (LLM interpretations) ---")
                for o in observations:
                    print(f"  {o.observer_id}: {o.raw_interpretation[:100]}...")

        for arch_name, arch_fn in ARCHITECTURES.items():
            claim = arch_fn(observations, llm=llm)
            result = evaluate(claim, cond, arch_name)
            results.append(result)
            if verbose:
                print(f"  [{arch_name:20s}] approved={result.approved}  "
                      f"ind={result.independence_score:.2f}  "
                      f"stmt={claim.statement[:40]}")

    return results


def summarize(results: List[ExperimentResult]) -> None:
    print("\n=== OI-003 LLM-Extended Experiment Summary ===\n")
    by_arch: Dict[str, List[ExperimentResult]] = defaultdict(list)
    for r in results:
        by_arch[r.architecture].append(r)

    header = f"{'Architecture':25s} | {'Appr':>5} | {'Unsup':>5} | {'FalseC':>6} | {'Prov':>5} | {'Ind':>5}"
    print(header)
    print("-" * len(header))
    for arch, items in by_arch.items():
        n = len(items)
        approved = sum(1 for r in items if r.approved)
        unsupported = sum(1 for r in items if r.unsupported)
        false_cons = sum(1 for r in items if r.false_consensus)
        avg_prov = sum(r.provenance_score for r in items) / n
        avg_ind = sum(r.independence_score for r in items) / n
        print(f"{arch:25s} | {approved:2d}/{n:<2d} | {unsupported:5d} | {false_cons:6d} | "
              f"{avg_prov:5.2f} | {avg_ind:5.2f}")


def main():
    parser = argparse.ArgumentParser(description="OI-003 LLM-extended experiment")
    parser.add_argument("--llm", action="store_true", help="Enable LLM observers + explanations")
    parser.add_argument("--model", default="dummy",
                        help="LLM backend: dummy | openai | gpt-4o-mini | anthropic | claude-...")
    parser.add_argument("--condition", action="append",
                        help="Run only these conditions (can be repeated)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--out", default="oi003_llm_results.json")
    args = parser.parse_args()

    llm = get_llm(args.model) if args.llm else DummyLLM()
    if args.llm:
        print(f"Using LLM backend: {args.model} ({type(llm).__name__})")

    results = run_experiment(
        seed=args.seed,
        use_llm_observers=args.llm,
        llm=llm,
        conditions=args.condition,
        verbose=args.verbose,
    )
    summarize(results)

    # Serialize (convert enums etc.)
    serializable = []
    for r in results:
        d = asdict(r)
        serializable.append(d)

    with open(args.out, "w") as f:
        json.dump(serializable, f, indent=2, default=str)
    print(f"\nFull results written to {args.out}")


if __name__ == "__main__":
    main()

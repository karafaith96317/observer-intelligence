#!/usr/bin/env python3
"""
OI-003 Extended with:
  - LLM-as-judge for ground-truth scoring
  - Multi-turn critic / debate step inside Observer Intelligence
  - Structured JSONL provenance ledger (Evidence-Matrix aligned)
  - Compatible with the original four-architecture comparison

This file is the research prototype for the Observer Intelligence paper.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
import hashlib
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Data structures
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
    measurement_integrity: float
    timestamp: int
    authenticated: bool = True
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
    critic_notes: Optional[str] = None
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
    judge_score: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# LLM interface
# ---------------------------------------------------------------------------

class LLMClient(Protocol):
    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        ...


class DummyLLM:
    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        p = prompt.lower()
        if "corrupted" in p or "bad-fact" in p or "weak-evidence" in p:
            return "Evidence appears low-integrity or correlated. Recommend caution / abstain."
        if "true-fact" in p or "correct-fact" in p:
            return "Evidence appears strong and independent. Support is reasonable."
        if "judge" in system.lower() or "score the claim" in p:
            if "true-fact" in p or "correct-fact" in p:
                return "SCORE: 0.85\nThe claim matches the high-integrity independent source."
            if "bad-fact" in p or "majority-wrong" in p:
                return "SCORE: 0.25\nThe claim conflicts with better evidence."
            return "SCORE: 0.50\nAmbiguous."
        return "Moderate confidence based on available evidence."


class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model

    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=temperature, max_tokens=400
        )
        return resp.choices[0].message.content.strip()


class AnthropicClient:
    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model

    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> str:
        resp = self.client.messages.create(
            model=self.model, max_tokens=400, temperature=temperature,
            system=system or "You are a careful scientific observer.",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()


def get_llm(name: str) -> LLMClient:
    if name in ("none", "dummy", "rule"):
        return DummyLLM()
    if "gpt" in name or name == "openai":
        return OpenAIClient(model=name if "gpt" in name else "gpt-4o-mini")
    if "claude" in name or name == "anthropic":
        return AnthropicClient(model=name if "claude" in name else "claude-3-5-haiku-20241022")
    print(f"[warning] Unknown model '{name}', using DummyLLM")
    return DummyLLM()


# ---------------------------------------------------------------------------
# Provenance ledger (Evidence-Matrix aligned JSONL)
# ---------------------------------------------------------------------------

class ProvenanceLedger:
    def __init__(self, path: str = "oi003_provenance.jsonl"):
        self.path = path
        self._file = open(path, "a", encoding="utf-8")

    def record(self, event_type: str, payload: Dict[str, Any]):
        entry = {
            "event_id": hashlib.sha256(f"{time.time()}{event_type}{json.dumps(payload, default=str)}".encode()).hexdigest()[:16],
            "event_type": event_type,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self._file.write(json.dumps(entry, default=str) + "\n")
        self._file.flush()

    def close(self):
        self._file.close()


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def make_condition(name: str, rng: random.Random) -> List[Observation]:
    base = 1000
    if name == "independent_high_quality":
        return [Observation(f"O{i}", f"fact-{i}", EvidenceQuality.HIGH, f"src-{i}", 0.95, base+i) for i in range(5)]
    if name == "duplicated_as_independent":
        return [Observation(f"O{i}", "shared-fact", EvidenceQuality.HIGH, "src-shared", 0.90, base+i) for i in range(5)]
    if name == "shared_corrupted_source":
        return [Observation(f"O{i}", "bad-fact", EvidenceQuality.CORRUPTED, "src-bad", 0.30, base+i) for i in range(4)] + \
               [Observation("O_good", "correct-fact", EvidenceQuality.HIGH, "src-good", 0.95, base+10)]
    if name == "authority_laundering":
        return [
            Observation("O1", "weak-evidence", EvidenceQuality.LOW, "src-1", 0.40, base),
            Observation("AgentX", "I confirm the claim is true", EvidenceQuality.HIGH, "src-1", 0.40, base+5),
            Observation("O2", "I defer to AgentX", EvidenceQuality.MEDIUM, "src-agentx", 0.60, base+8),
        ]
    if name == "minority_correct":
        return [Observation(f"O{i}", "majority-wrong", EvidenceQuality.MEDIUM, f"src-m{i}", 0.70, base+i) for i in range(4)] + \
               [Observation("O_correct", "true-fact", EvidenceQuality.HIGH, "src-true", 0.98, base+20)]
    if name == "signed_but_inaccurate":
        return [
            Observation("SensorA", "reading-42", EvidenceQuality.HIGH, "sensor-a", 0.25, base, True),
            Observation("SensorB", "reading-42", EvidenceQuality.HIGH, "sensor-a", 0.25, base+1, True),
        ]
    raise ValueError(name)


# ---------------------------------------------------------------------------
# Architectures
# ---------------------------------------------------------------------------

def single_agent(obs: List[Observation], llm=None, ledger=None) -> Claim:
    best = max(obs, key=lambda o: o.measurement_integrity)
    return Claim(best.content, best.measurement_integrity, [best.observer_id], 1, True,
                 best.measurement_integrity > 0.70, "Highest integrity observation selected.")


def majority_vote(obs: List[Observation], llm=None, ledger=None) -> Claim:
    counts = defaultdict(list)
    for o in obs:
        counts[o.content].append(o)
    content, supporters = max(counts.items(), key=lambda x: len(x[1]))
    return Claim(content, len(supporters)/len(obs), [o.observer_id for o in supporters],
                 len(set(o.source_id for o in supporters)), False,
                 len(supporters) > len(obs)/2, f"Majority of {len(supporters)} observers.")


def adaptive_quorum(obs: List[Observation], llm=None, ledger=None) -> Claim:
    scored = sorted(obs, key=lambda o: o.measurement_integrity, reverse=True)
    selected, sources = [], set()
    for o in scored:
        if o.source_id not in sources or o.measurement_integrity > 0.85:
            selected.append(o)
            sources.add(o.source_id)
        if len(selected) >= 3:
            break
    if not selected:
        selected = scored[:1]
    return Claim(selected[0].content,
                 sum(o.measurement_integrity for o in selected)/len(selected),
                 [o.observer_id for o in selected], len(sources), True,
                 len(sources) >= 2 and selected[0].measurement_integrity > 0.60,
                 "Adaptive integrity + source diversity.")


def observer_intelligence(obs: List[Observation], llm: Optional[LLMClient] = None,
                          ledger: Optional[ProvenanceLedger] = None) -> Claim:
    """OI with optional critic debate step."""
    by_source = defaultdict(list)
    for o in obs:
        by_source[o.source_id].append(o)
    pathways = len(by_source)
    best_per = [max(g, key=lambda o: o.measurement_integrity) for g in by_source.values()]
    best_per.sort(key=lambda o: o.measurement_integrity, reverse=True)
    if not best_per:
        return Claim("no-claim", 0.0, [], 0, False, False)

    top = best_per[0]
    strength = top.measurement_integrity
    independence = min(1.0, pathways / 3.0)
    prov_complete = all(o.authenticated for o in best_per)

    score = strength * (0.55 + 0.45 * independence)
    if top.quality == EvidenceQuality.CORRUPTED:
        score *= 0.25
    if strength < 0.40:
        score *= 0.50
    justified = score >= 0.65 and pathways >= 1 and strength >= 0.50

    reasoning = (f"OI bound: strength={strength:.2f}, independence={independence:.2f}, "
                 f"pathways={pathways}, score={score:.2f} → justified={justified}")
    critic_notes = None
    llm_calls = []

    # Critic / debate step (multi-turn style)
    if llm is not None:
        critic_prompt = (
            "You are the Critic agent in Observer Intelligence.\n"
            f"Proposed claim: {top.content}\n"
            f"Measurement integrity: {strength:.2f}\n"
            f"Independent pathways: {pathways}\n"
            f"Authority score: {score:.2f}\n"
            f"Preliminary decision: {'APPROVE' if justified else 'ABSTAIN'}\n\n"
            "Challenge this decision. Point out possible correlation, "
            "measurement problems, or authority-laundering risks. "
            "Be concise (max 60 words)."
        )
        critic_resp = llm.complete(critic_prompt, system="You are a rigorous epistemic critic.")
        critic_notes = critic_resp
        llm_calls.append({"role": "critic", "prompt": critic_prompt, "response": critic_resp})

        # Reconciler replies (second turn)
        recon_prompt = (
            f"Critic said: {critic_resp}\n\n"
            f"Original OI score was {score:.2f} (justified={justified}).\n"
            "Does the critic raise a material issue that should flip the decision? "
            "Answer YES or NO and give one sentence reason."
        )
        recon_resp = llm.complete(recon_prompt, system="You are the OI reconciler. Protect the authority bound.")
        llm_calls.append({"role": "reconciler", "prompt": recon_prompt, "response": recon_resp})
        reasoning += f"\nCritic: {critic_resp}\nReconciler: {recon_resp}"

        if ledger:
            ledger.record("critic_debate", {
                "claim": top.content, "score": score, "critic": critic_resp, "reconciler": recon_resp
            })

    if ledger:
        ledger.record("oi_decision", {
            "statement": top.content, "score": score, "justified": justified,
            "pathways": pathways, "strength": strength
        })

    return Claim(
        statement=top.content, support_score=score,
        originating_observers=[o.observer_id for o in best_per],
        independent_pathways=pathways, provenance_complete=prov_complete,
        authority_justified=justified, reasoning_trace=reasoning,
        critic_notes=critic_notes, llm_calls=llm_calls
    )


# ---------------------------------------------------------------------------
# LLM-as-judge
# ---------------------------------------------------------------------------

def llm_judge(claim: Claim, condition: str, observations: List[Observation],
              llm: LLMClient, ledger: Optional[ProvenanceLedger] = None) -> float:
    """Returns a 0–1 correctness / support score from an LLM judge."""
    obs_summary = "\n".join(
        f"- {o.observer_id} (src={o.source_id}, integrity={o.measurement_integrity:.2f}): {o.content}"
        for o in observations
    )
    prompt = (
        f"Condition under test: {condition}\n"
        f"Claim made by architecture: {claim.statement}\n"
        f"Observations:\n{obs_summary}\n\n"
        "Score how correct / well-supported this claim is given the observations "
        "and known integrity signals. Reply with:\nSCORE: <float 0.0-1.0>\nReason: <one sentence>"
    )
    resp = llm.complete(prompt, system="You are an impartial scientific judge for multi-observer experiments.")
    if ledger:
        ledger.record("llm_judge", {"claim": claim.statement, "condition": condition, "response": resp})

    # Parse SCORE
    score = 0.5
    for line in resp.splitlines():
        if line.strip().upper().startswith("SCORE:"):
            try:
                score = float(line.split(":", 1)[1].strip().split()[0])
                score = max(0.0, min(1.0, score))
            except Exception:
                pass
            break
    return score


# ---------------------------------------------------------------------------
# Evaluation + Runner
# ---------------------------------------------------------------------------

ARCHITECTURES = {
    "single_agent": single_agent,
    "majority_vote": majority_vote,
    "adaptive_quorum": adaptive_quorum,
    "observer_intelligence": observer_intelligence,
}

CONDITIONS = [
    "independent_high_quality", "duplicated_as_independent", "shared_corrupted_source",
    "authority_laundering", "minority_correct", "signed_but_inaccurate",
]


def evaluate(claim: Claim, condition: str, architecture: str,
             judge_score: Optional[float] = None) -> ExperimentResult:
    true_map = {
        "independent_high_quality": None,
        "duplicated_as_independent": "shared-fact",
        "shared_corrupted_source": "correct-fact",
        "authority_laundering": None,
        "minority_correct": "true-fact",
        "signed_but_inaccurate": None,
    }
    true_content = true_map.get(condition)
    approved = claim.authority_justified
    unsupported = approved and true_content is not None and claim.statement != true_content
    false_consensus = (condition in ("duplicated_as_independent", "shared_corrupted_source")
                       and claim.independent_pathways < 2 and approved)
    return ExperimentResult(
        architecture=architecture, condition=condition,
        approved=approved, unsupported=unsupported, false_consensus=false_consensus,
        provenance_score=1.0 if claim.provenance_complete else 0.4,
        independence_score=min(1.0, claim.independent_pathways / 3.0),
        judge_score=judge_score,
        details={
            "statement": claim.statement, "support_score": round(claim.support_score, 3),
            "independent_pathways": claim.independent_pathways,
            "reasoning": claim.reasoning_trace, "critic": claim.critic_notes,
            "llm_calls": claim.llm_calls,
        }
    )


def run_experiment(seed=42, llm=None, use_judge=False, conditions=None,
                   verbose=False, ledger_path="oi003_provenance.jsonl"):
    rng = random.Random(seed)
    ledger = ProvenanceLedger(ledger_path)
    results = []
    for cond in (conditions or CONDITIONS):
        observations = make_condition(cond, rng)
        if verbose:
            print(f"\n=== Condition: {cond} ===")
        for arch_name, arch_fn in ARCHITECTURES.items():
            claim = arch_fn(observations, llm=llm, ledger=ledger)
            judge_score = None
            if use_judge and llm is not None:
                judge_score = llm_judge(claim, cond, observations, llm, ledger)
            result = evaluate(claim, cond, arch_name, judge_score)
            results.append(result)
            if verbose:
                js = f" judge={judge_score:.2f}" if judge_score is not None else ""
                print(f"  [{arch_name:22s}] approved={str(result.approved):5s} "
                      f"ind={result.independence_score:.2f}{js}  | {claim.statement[:45]}")
    ledger.close()
    return results


def summarize(results: List[ExperimentResult]):
    print("\n=== OI-003 Extended Summary ===\n")
    by_arch = defaultdict(list)
    for r in results:
        by_arch[r.architecture].append(r)
    print(f"{'Architecture':22s} | {'Appr':>5} | {'Unsup':>5} | {'FalseC':>6} | {'Prov':>5} | {'Ind':>5} | {'Judge':>5}")
    print("-" * 70)
    for arch, items in by_arch.items():
        n = len(items)
        ap = sum(r.approved for r in items)
        un = sum(r.unsupported for r in items)
        fc = sum(r.false_consensus for r in items)
        pr = sum(r.provenance_score for r in items) / n
        ind = sum(r.independence_score for r in items) / n
        judges = [r.judge_score for r in items if r.judge_score is not None]
        javg = sum(judges)/len(judges) if judges else None
        jstr = f"{javg:.2f}" if javg is not None else "  -  "
        print(f"{arch:22s} | {ap:2d}/{n:<2d} | {un:5d} | {fc:6d} | {pr:5.2f} | {ind:5.2f} | {jstr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true")
    parser.add_argument("--model", default="dummy")
    parser.add_argument("--judge", action="store_true", help="Enable LLM-as-judge scoring")
    parser.add_argument("--condition", action="append")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--out", default="oi003_extended_results.json")
    parser.add_argument("--ledger", default="oi003_provenance.jsonl")
    args = parser.parse_args()

    llm = get_llm(args.model) if args.llm or args.judge else DummyLLM()
    print(f"LLM backend: {args.model} ({type(llm).__name__})")

    results = run_experiment(
        seed=args.seed, llm=llm, use_judge=args.judge,
        conditions=args.condition, verbose=args.verbose, ledger_path=args.ledger
    )
    summarize(results)

    with open(args.out, "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2, default=str)
    print(f"\nResults → {args.out}")
    print(f"Provenance ledger → {args.ledger}")


if __name__ == "__main__":
    main()

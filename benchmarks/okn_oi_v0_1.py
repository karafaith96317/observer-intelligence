"""Synthetic provenance-aware baseline vs OI-style decision benchmark v0.1.

This is not an implementation or simulation of NSF OKN.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Observation:
    source: str
    value: bool
    confidence: float
    timestamp: int
    dependency: str
    valid_until: int
    adversarial: bool = False
    level: str = "source"  # "source" or "sample"


@dataclass(frozen=True)
class Case:
    name: str
    observations: tuple
    now: int
    truth: bool
    action_valid: bool
    requested_scope: str
    authority_scope: str
    min_independent: int = 2
    require_source_level: bool = False


def weighted_vote(observations):
    yes = sum(o.confidence for o in observations if o.value)
    no = sum(o.confidence for o in observations if not o.value)
    if yes == no:
        return None
    return yes > no


def baseline(case):
    decision = weighted_vote(case.observations)
    # Deliberately simple provenance-aware graph baseline: provenance is retained,
    # but action follows the aggregate proposition decision.
    authorize = decision is True
    return {"decision": decision, "authorize": authorize, "provenance": len(case.observations)}


def oi_condition(case):
    usable = [o for o in case.observations if o.valid_until >= case.now and not o.adversarial]
    if case.require_source_level:
        usable = [o for o in usable if o.level == "source"]

    groups = {}
    for o in usable:
        # Collapse declared common-cause dependence to one strongest observation.
        prev = groups.get(o.dependency)
        if prev is None or o.confidence > prev.confidence:
            groups[o.dependency] = o
    independent = list(groups.values())

    decision = weighted_vote(independent) if len(independent) >= case.min_independent else None
    scope_ok = case.requested_scope == case.authority_scope
    authorize = decision is True and scope_ok
    return {"decision": decision, "authorize": authorize, "provenance": len(case.observations)}


def fixtures():
    return (
        Case("clean", (
            Observation("a", True, .9, 10, "a", 20),
            Observation("b", True, .8, 10, "b", 20),
        ), 10, True, True, "observe:act", "observe:act"),
        Case("correlated", (
            Observation("a1", True, .95, 10, "feed-x", 20),
            Observation("a2", True, .90, 10, "feed-x", 20),
            Observation("a3", True, .85, 10, "feed-x", 20),
            Observation("b", False, .99, 10, "b", 20),
            Observation("c", False, .80, 10, "c", 20),
        ), 10, False, False, "observe:act", "observe:act"),
        Case("stale", (
            Observation("old-a", True, .99, 1, "old-a", 5),
            Observation("old-b", True, .98, 1, "old-b", 5),
            Observation("fresh-a", False, .75, 10, "fresh-a", 20),
            Observation("fresh-b", False, .75, 10, "fresh-b", 20),
        ), 10, False, False, "observe:act", "observe:act"),
        Case("adversarial", (
            Observation("attack", False, .99, 10, "attack", 20, adversarial=True),
            Observation("a", True, .85, 10, "a", 20),
            Observation("b", True, .80, 10, "b", 20),
        ), 10, True, True, "observe:act", "observe:act"),
        Case("authority-mismatch", (
            Observation("a", True, .9, 10, "a", 20),
            Observation("b", True, .9, 10, "b", 20),
        ), 10, True, False, "execute:external", "observe:act"),
        Case("sampling-transform", (
            Observation("sample-a", True, .95, 10, "a", 20, level="sample"),
            Observation("sample-b", True, .90, 10, "b", 20, level="sample"),
        ), 10, False, False, "observe:act", "observe:act", require_source_level=True),
    )


def score(fn):
    rows = []
    unsafe = false_auth = valid = missed = correct = abstain = 0
    for case in fixtures():
        out = fn(case)
        if case.action_valid:
            valid += 1
            if not out["authorize"]:
                missed += 1
        else:
            unsafe += 1
            if out["authorize"]:
                false_auth += 1
        if out["decision"] is None:
            abstain += 1
        elif out["decision"] == case.truth:
            correct += 1
        rows.append((case.name, out))
    n = len(rows)
    return {
        "false_authorization_rate": false_auth / unsafe if unsafe else 0.0,
        "missed_valid_authorization_rate": missed / valid if valid else 0.0,
        "decision_accuracy": correct / n,
        "abstention_rate": abstain / n,
        "provenance_completeness": 1.0,
        "rows": rows,
    }


def main():
    for name, fn in (("baseline", baseline), ("oi", oi_condition)):
        result = score(fn)
        print(name)
        for key in ("false_authorization_rate", "missed_valid_authorization_rate",
                    "decision_accuracy", "abstention_rate", "provenance_completeness"):
            print(f"  {key}: {result[key]:.3f}")
        for case_name, out in result["rows"]:
            print(f"  {case_name}: decision={out['decision']} authorize={out['authorize']}")


if __name__ == "__main__":
    main()

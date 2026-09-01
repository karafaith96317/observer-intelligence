"""HRS v0.2.1 synthetic computational prototype.

Research prototype only. The model uses explicit synthetic graphs and known
scenario ground truth. It is not validated for real-world safety, personnel,
medical, psychological, or autonomous authority decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import random

DIMS = ("C", "P", "A", "R", "S", "I")
NODES = ("sensor", "ai", "operator", "comms", "team")
BASELINE_VALUE = 0.80

# Directed influence graph. Edge weights are synthetic dependencies, not causal claims.
EDGES = {
    "sensor": {"ai": 0.55, "operator": 0.20},
    "ai": {"operator": 0.50},
    "operator": {"team": 0.30},
    "comms": {"operator": 0.35, "team": 0.55},
    "team": {},
}

GROUND_TRUTH_ROOT = {
    "HRS-01": "adaptive",
    "HRS-02": "operator",
    "HRS-03": "sensor",
    "HRS-04": "ai",
    "HRS-05": "comms",
}


@dataclass
class Snapshot:
    state: Dict[str, List[float]]
    confidence: Dict[str, float]
    drift: Dict[str, List[float]]
    node_drift: Dict[str, float]
    risk: float
    classification: str
    root_cause: str
    intervention: str


def clip(x: float) -> float:
    return min(1.0, max(0.0, x))


def rms(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v) / len(v))


def scenario_shock(scenario: str, t: int) -> Dict[str, List[float]]:
    """Return exogenous perturbations for one synthetic scenario/time step."""
    z = {n: [0.0] * len(DIMS) for n in NODES}

    if scenario == "HRS-01":
        # Temporary procedural dip with increasing adaptability and later recovery.
        if 4 <= t <= 8:
            z["operator"][1] -= 0.035
            z["operator"][2] += 0.045
        elif 9 <= t <= 13:
            z["operator"][1] += 0.018
            z["operator"][2] += 0.025

    elif scenario == "HRS-02" and t >= 5:
        scale = min(1.0, (t - 4) / 10)
        z["operator"][0] -= 0.024 * scale
        z["operator"][1] -= 0.026 * scale
        z["operator"][3] -= 0.030 * scale

    elif scenario == "HRS-03" and t >= 5:
        z["sensor"][5] -= 0.055
        z["sensor"][4] -= 0.025

    elif scenario == "HRS-04" and t >= 5:
        z["ai"][0] -= 0.035
        z["ai"][1] -= 0.045
        z["ai"][5] -= 0.030

    elif scenario == "HRS-05" and t >= 5:
        z["comms"][5] -= 0.060
        z["comms"][4] -= 0.030

    return z


def simulate(
    scenario: str,
    seed: int = 0,
    steps: int = 18,
    noise_sd: float = 0.006,
) -> Snapshot:
    """Run one synthetic HRS scenario and return the terminal HRS estimate."""
    if scenario not in GROUND_TRUTH_ROOT:
        raise ValueError(f"unknown scenario: {scenario}")

    rng = random.Random(seed)
    state = {n: [BASELINE_VALUE] * len(DIMS) for n in NODES}
    recent_global: List[float] = []
    last_velocity = 0.0

    for t in range(steps):
        shock = scenario_shock(scenario, t)
        old = {n: list(v) for n, v in state.items()}
        incoming = {n: [0.0] * len(DIMS) for n in NODES}

        # Only negative deviation is propagated in this first-order failure model.
        # Positive adaptation is therefore not treated as failure contagion.
        for src, targets in EDGES.items():
            src_dev = [min(0.0, old[src][j] - BASELINE_VALUE) for j in range(len(DIMS))]
            for dst, weight in targets.items():
                for j in range(len(DIMS)):
                    incoming[dst][j] += weight * src_dev[j] * 0.28

        for node in NODES:
            for j in range(len(DIMS)):
                dev = old[node][j] - BASELINE_VALUE
                state[node][j] = clip(
                    BASELINE_VALUE
                    + 0.82 * dev
                    + shock[node][j]
                    + incoming[node][j]
                    + rng.gauss(0.0, noise_sd)
                )

        drift = {
            n: [state[n][j] - BASELINE_VALUE for j in range(len(DIMS))]
            for n in NODES
        }
        node_drift = {n: rms(drift[n]) for n in NODES}
        global_drift = sum(node_drift.values()) / len(NODES)
        last_velocity = global_drift - (recent_global[-1] if recent_global else 0.0)
        recent_global.append(global_drift)

    values = [state[n][j] for n in NODES for j in range(len(DIMS))]
    dispersion = max(values) - min(values)
    confidence = {
        n: clip(0.95 - 0.30 * dispersion - 2.0 * noise_sd) for n in NODES
    }

    parents = {n: [] for n in NODES}
    for src, targets in EDGES.items():
        for dst, weight in targets.items():
            parents[dst].append((src, weight))

    # A node gets less root-cause credit when its drift is plausibly explained by
    # already-drifting upstream parents.
    root_scores: Dict[str, float] = {}
    for node in NODES:
        explained = sum(weight * node_drift[parent] for parent, weight in parents[node])
        root_scores[node] = max(0.0, node_drift[node] - 0.70 * explained)

    op = drift["operator"]
    adaptive = (
        op[2] > 0.02
        and op[1] > -0.05
        and max(node_drift["sensor"], node_drift["ai"], node_drift["comms"]) < 0.05
    )

    if adaptive:
        classification = "adaptive"
        root = "adaptive"
    else:
        root = max(root_scores, key=root_scores.get)
        if root == "comms" and (node_drift["team"] + node_drift["operator"]) > 0.08:
            classification = "system-cascade"
        elif root in ("sensor", "ai", "comms"):
            classification = "system-origin"
        else:
            classification = "human-origin"

    global_drift = sum(node_drift.values()) / len(NODES)
    propagation = max(node_drift["operator"], node_drift["team"])
    risk_logit = (
        -3.2
        + 10.0 * global_drift
        + 4.0 * max(0.0, last_velocity)
        + 3.0 * propagation
    )
    risk = 1.0 / (1.0 + math.exp(-risk_logit))

    if classification == "adaptive" and risk < 0.60:
        intervention = "U0"
    elif risk < 0.30:
        intervention = "U0"
    elif risk < 0.45:
        intervention = "U1"
    elif risk < 0.65:
        intervention = "U2"
    elif risk < 0.80:
        intervention = "U4"
    else:
        intervention = "U5"

    return Snapshot(
        state=state,
        confidence=confidence,
        drift=drift,
        node_drift=node_drift,
        risk=risk,
        classification=classification,
        root_cause=root,
        intervention=intervention,
    )


def scalar_baseline(snapshot: Snapshot, threshold: float = 0.04) -> Tuple[str, str]:
    """Simple comparator: aggregate anomaly + largest uncontextualized node drift.

    This comparator has no graph discounting and no directional adaptive-drift rule.
    """
    score = sum(snapshot.node_drift.values()) / len(NODES)
    root = max(snapshot.node_drift, key=snapshot.node_drift.get)
    return ("anomaly" if score >= threshold else "nominal", root)


def run_monte_carlo(
    runs: int = 1000,
    seed: int = 42,
    noise_sd: float = 0.006,
) -> Dict[str, object]:
    """Evaluate root attribution and intervention behavior across random scenarios."""
    rng = random.Random(seed)
    scenarios = list(GROUND_TRUTH_ROOT)
    hrs_correct = 0
    scalar_correct = 0
    human_false_positive = 0
    scalar_human_false_positive = 0
    unnecessary_intervention = 0
    per = {s: {"correct": 0, "scalar_correct": 0, "n": 0} for s in scenarios}

    for _ in range(runs):
        scenario = rng.choice(scenarios)
        snapshot = simulate(
            scenario,
            seed=rng.randrange(10**9),
            noise_sd=noise_sd,
        )
        truth = GROUND_TRUTH_ROOT[scenario]
        scalar_status, scalar_root = scalar_baseline(snapshot)

        hrs_ok = snapshot.root_cause == truth
        scalar_ok = scalar_root == truth
        hrs_correct += int(hrs_ok)
        scalar_correct += int(scalar_ok)
        per[scenario]["correct"] += int(hrs_ok)
        per[scenario]["scalar_correct"] += int(scalar_ok)
        per[scenario]["n"] += 1

        nonhuman_truth = scenario in ("HRS-01", "HRS-03", "HRS-04", "HRS-05")
        if nonhuman_truth and snapshot.root_cause == "operator":
            human_false_positive += 1
        if nonhuman_truth and scalar_status == "anomaly" and scalar_root == "operator":
            scalar_human_false_positive += 1
        if scenario == "HRS-01" and snapshot.intervention not in ("U0", "U1"):
            unnecessary_intervention += 1

    return {
        "runs": runs,
        "noise_sd": noise_sd,
        "hrs_root_accuracy": hrs_correct / runs,
        "scalar_root_accuracy": scalar_correct / runs,
        "human_fault_false_positive_rate": human_false_positive / runs,
        "scalar_human_fault_false_positive_rate": scalar_human_false_positive / runs,
        "adaptive_unnecessary_intervention_rate": unnecessary_intervention / runs,
        "per_scenario_accuracy": {
            scenario: {
                "hrs": values["correct"] / values["n"],
                "scalar": values["scalar_correct"] / values["n"],
                "n": values["n"],
            }
            for scenario, values in per.items()
        },
    }

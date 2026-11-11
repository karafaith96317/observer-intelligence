"""HRS v0.2.1 synthetic validation prototype.

All fixtures, graph relationships, disturbances, and labels are synthetic.
Results test implementation behavior only; they do not validate real-world
human, medical, personnel, or autonomous safety decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Tuple
import math
import random

DIMS = ("C", "P", "A", "R", "S", "I")
NODES = ("sensor", "ai", "operator", "comms", "team")
BASELINE_VALUE = 0.80
SHOCK_ONSET = {"HRS-01": 4, "HRS-02": 5, "HRS-03": 5, "HRS-04": 5, "HRS-05": 5}

EDGES = {
    "sensor": {"ai": 0.55, "operator": 0.20},
    "ai": {"operator": 0.50},
    "operator": {"team": 0.30},
    "comms": {"operator": 0.35, "team": 0.55},
    "team": {},
}

GROUND_TRUTH_ROOT = {
    "HRS-01": "adaptive", "HRS-02": "operator", "HRS-03": "sensor",
    "HRS-04": "ai", "HRS-05": "comms",
}

GRAPH_PERTURBATIONS = ("correct", "drop_sensor_ai", "reverse_ai_operator", "weight_shift")
SENSOR_PERTURBATIONS = ("nominal", "dropout_40", "stuck_high", "noisy")


@dataclass
class Snapshot:
    state: Dict[str, List[float]]
    confidence: Dict[str, float]
    drift: Dict[str, List[float]]
    node_drift: Dict[str, float]
    risk: float
    classification: str
    root_cause: str
    root_confidence: float
    intervention: str
    detection_time: int | None


def clip(x: float) -> float:
    return min(1.0, max(0.0, x))


def rms(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v) / len(v))


def scenario_shock(scenario: str, t: int) -> Dict[str, List[float]]:
    z = {n: [0.0] * len(DIMS) for n in NODES}
    if scenario == "HRS-01":
        if 4 <= t <= 8:
            z["operator"][1] -= 0.035; z["operator"][2] += 0.045
        elif 9 <= t <= 13:
            z["operator"][1] += 0.018; z["operator"][2] += 0.025
    elif scenario == "HRS-02" and t >= 5:
        scale = min(1.0, (t - 4) / 10)
        z["operator"][0] -= 0.024 * scale
        z["operator"][1] -= 0.026 * scale
        z["operator"][3] -= 0.030 * scale
    elif scenario == "HRS-03" and t >= 5:
        z["sensor"][5] -= 0.055; z["sensor"][4] -= 0.025
    elif scenario == "HRS-04" and t >= 5:
        z["ai"][0] -= 0.035; z["ai"][1] -= 0.045; z["ai"][5] -= 0.030
    elif scenario == "HRS-05" and t >= 5:
        z["comms"][5] -= 0.060; z["comms"][4] -= 0.030
    return z


def perturbed_graph(mode: str) -> Dict[str, Dict[str, float]]:
    if mode not in GRAPH_PERTURBATIONS:
        raise ValueError(f"unknown graph perturbation: {mode}")
    graph = {src: dict(targets) for src, targets in EDGES.items()}
    if mode == "drop_sensor_ai":
        graph["sensor"].pop("ai")
    elif mode == "reverse_ai_operator":
        graph["ai"].pop("operator")
        graph["operator"]["ai"] = 0.50
    elif mode == "weight_shift":
        graph["sensor"]["ai"] = 0.10
        graph["comms"]["operator"] = 0.80
    return graph


def _observe(state: Mapping[str, List[float]], rng: random.Random, sensor_mode: str):
    if sensor_mode not in SENSOR_PERTURBATIONS:
        raise ValueError(f"unknown sensor perturbation: {sensor_mode}")
    observed = {n: list(v) for n, v in state.items()}
    reliability = 1.0
    if sensor_mode == "dropout_40":
        reliability = 0.60
        for j, value in enumerate(observed["sensor"]):
            if rng.random() < 0.40:
                observed["sensor"][j] = BASELINE_VALUE
    elif sensor_mode == "stuck_high":
        reliability = 0.35
        observed["sensor"] = [BASELINE_VALUE + 0.01] * len(DIMS)
    elif sensor_mode == "noisy":
        reliability = 0.55
        observed["sensor"] = [clip(v + rng.gauss(0.0, 0.04)) for v in observed["sensor"]]
    return observed, reliability


def _infer(observed, graph, noise_sd, sensor_reliability, last_velocity):
    drift = {n: [v - BASELINE_VALUE for v in observed[n]] for n in NODES}
    node_drift = {n: rms(drift[n]) for n in NODES}
    parents = {n: [] for n in NODES}
    for src, targets in graph.items():
        for dst, weight in targets.items():
            parents[dst].append((src, weight))
    scores = {}
    for node in NODES:
        explained = sum(weight * node_drift[parent] for parent, weight in parents[node])
        scores[node] = max(0.0, node_drift[node] - 0.70 * explained)
    op = drift["operator"]
    adaptive = (op[2] > 0.02 and op[1] > -0.05
                and max(node_drift["sensor"], node_drift["ai"], node_drift["comms"]) < 0.05)
    if adaptive:
        classification, root = "adaptive", "adaptive"
        evidence = min(1.0, max(0.0, op[2]) / 0.08)
        root_confidence = clip(0.50 + 0.42 * evidence)
    else:
        ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        root = ordered[0][0]
        margin = ordered[0][1] - ordered[1][1]
        evidence = ordered[0][1]
        root_confidence = clip(0.45 + 3.0 * margin + 1.2 * evidence)
        if root == "sensor":
            root_confidence *= sensor_reliability
        if root == "comms" and (node_drift["team"] + node_drift["operator"]) > 0.08:
            classification = "system-cascade"
        elif root in ("sensor", "ai", "comms"):
            classification = "system-origin"
        else:
            classification = "human-origin"
    dispersion = max(v for values in observed.values() for v in values) - min(v for values in observed.values() for v in values)
    confidence = {n: clip((0.95 - 0.30 * dispersion - 2.0 * noise_sd)
                          * (sensor_reliability if n == "sensor" else 1.0)) for n in NODES}
    global_drift = sum(node_drift.values()) / len(NODES)
    propagation = max(node_drift["operator"], node_drift["team"])
    risk = 1.0 / (1.0 + math.exp(-(-3.2 + 10.0 * global_drift
                                    + 4.0 * max(0.0, last_velocity) + 3.0 * propagation)))
    if classification == "adaptive" and risk < 0.60: intervention = "U0"
    elif risk < 0.30: intervention = "U0"
    elif risk < 0.45: intervention = "U1"
    elif risk < 0.65: intervention = "U2"
    elif risk < 0.80: intervention = "U4"
    else: intervention = "U5"
    return drift, node_drift, confidence, classification, root, root_confidence, risk, intervention


def simulate(scenario: str, seed: int = 0, steps: int = 18, noise_sd: float = 0.006,
             graph_perturbation: str = "correct", sensor_perturbation: str = "nominal") -> Snapshot:
    if scenario not in GROUND_TRUTH_ROOT:
        raise ValueError(f"unknown scenario: {scenario}")
    rng = random.Random(seed)
    graph = perturbed_graph(graph_perturbation)
    state = {n: [BASELINE_VALUE] * len(DIMS) for n in NODES}
    recent_global: List[float] = []
    detection_time = None
    result = None
    for t in range(steps):
        shock, old = scenario_shock(scenario, t), {n: list(v) for n, v in state.items()}
        incoming = {n: [0.0] * len(DIMS) for n in NODES}
        # The simulator retains the nominal graph; perturbations affect the observer's graph.
        for src, targets in EDGES.items():
            src_dev = [min(0.0, old[src][j] - BASELINE_VALUE) for j in range(len(DIMS))]
            for dst, weight in targets.items():
                for j in range(len(DIMS)): incoming[dst][j] += weight * src_dev[j] * 0.28
        for node in NODES:
            for j in range(len(DIMS)):
                dev = old[node][j] - BASELINE_VALUE
                state[node][j] = clip(BASELINE_VALUE + 0.82 * dev + shock[node][j]
                                      + incoming[node][j] + rng.gauss(0.0, noise_sd))
        observed, reliability = _observe(state, rng, sensor_perturbation)
        provisional_drift = {n: rms([v - BASELINE_VALUE for v in observed[n]]) for n in NODES}
        global_drift = sum(provisional_drift.values()) / len(NODES)
        velocity = global_drift - (recent_global[-1] if recent_global else 0.0)
        recent_global.append(global_drift)
        result = _infer(observed, graph, noise_sd, reliability, velocity)
        if (detection_time is None and t >= SHOCK_ONSET[scenario]
                and result[4] == GROUND_TRUTH_ROOT[scenario] and result[5] >= 0.55):
            detection_time = t
    drift, node_drift, confidence, classification, root, root_confidence, risk, intervention = result
    return Snapshot(state, confidence, drift, node_drift, risk, classification, root,
                    root_confidence, intervention, detection_time)


def scalar_baseline(snapshot: Snapshot, threshold: float = 0.04) -> Tuple[str, str]:
    score = sum(snapshot.node_drift.values()) / len(NODES)
    root = max(snapshot.node_drift, key=snapshot.node_drift.get)
    return ("anomaly" if score >= threshold else "nominal", root)


def _ece(predictions, bins=10):
    total, error = len(predictions), 0.0
    for lower_i in range(bins):
        lower, upper = lower_i / bins, (lower_i + 1) / bins
        group = [(p, y) for p, y in predictions if lower <= p <= upper if (p < upper or upper == 1.0)]
        if group:
            error += len(group) / total * abs(sum(p for p, _ in group) / len(group) - sum(y for _, y in group) / len(group))
    return error


def run_monte_carlo(runs: int = 1000, seed: int = 42, noise_sd: float = 0.006,
                    graph_perturbation: str = "correct", sensor_perturbation: str = "nominal") -> Dict[str, object]:
    rng, scenarios = random.Random(seed), list(GROUND_TRUTH_ROOT)
    hrs_correct = scalar_correct = human_fp = scalar_human_fp = unnecessary = 0
    per = {s: {"correct": 0, "scalar_correct": 0, "n": 0} for s in scenarios}
    calibration, delays = [], []
    for _ in range(runs):
        scenario = rng.choice(scenarios)
        snapshot = simulate(scenario, seed=rng.randrange(10**9), noise_sd=noise_sd,
                            graph_perturbation=graph_perturbation, sensor_perturbation=sensor_perturbation)
        truth = GROUND_TRUTH_ROOT[scenario]
        scalar_status, scalar_root = scalar_baseline(snapshot)
        ok, scalar_ok = snapshot.root_cause == truth, scalar_root == truth
        hrs_correct += ok; scalar_correct += scalar_ok
        per[scenario]["correct"] += ok; per[scenario]["scalar_correct"] += scalar_ok; per[scenario]["n"] += 1
        calibration.append((snapshot.root_confidence, int(ok)))
        if snapshot.detection_time is not None: delays.append(snapshot.detection_time - SHOCK_ONSET[scenario])
        nonhuman = scenario in ("HRS-01", "HRS-03", "HRS-04", "HRS-05")
        human_fp += nonhuman and snapshot.root_cause == "operator"
        scalar_human_fp += nonhuman and scalar_status == "anomaly" and scalar_root == "operator"
        unnecessary += scenario == "HRS-01" and snapshot.intervention not in ("U0", "U1")
    sorted_delays = sorted(delays)
    return {
        "schema_version": "hrs-v0.2.1-validation-1", "synthetic_only": True,
        "configuration": {"runs": runs, "seed": seed, "noise_sd": noise_sd,
                          "graph_perturbation": graph_perturbation, "sensor_perturbation": sensor_perturbation},
        "hrs_root_accuracy": hrs_correct / runs, "scalar_root_accuracy": scalar_correct / runs,
        "human_fault_false_positive_rate": human_fp / runs,
        "scalar_human_fault_false_positive_rate": scalar_human_fp / runs,
        "adaptive_unnecessary_intervention_rate": unnecessary / runs,
        "detection_rate": len(delays) / runs,
        "mean_detection_delay_steps": (sum(delays) / len(delays) if delays else None),
        "p90_detection_delay_steps": (sorted_delays[math.ceil(.9 * len(delays)) - 1] if delays else None),
        "confidence_brier_score": sum((p - y) ** 2 for p, y in calibration) / runs,
        "confidence_ece_10_bin": _ece(calibration),
        "per_scenario_accuracy": {s: {"hrs": v["correct"] / v["n"],
                                      "scalar": v["scalar_correct"] / v["n"], "n": v["n"]}
                                  for s, v in per.items()},
    }


def run_validation_suite(runs: int = 1000, seed: int = 42):
    cases = [
        ("frozen_nominal", 0.006, "correct", "nominal"),
        ("noise_stress", 0.020, "correct", "nominal"),
        ("graph_drop_sensor_ai", 0.006, "drop_sensor_ai", "nominal"),
        ("graph_reverse_ai_operator", 0.006, "reverse_ai_operator", "nominal"),
        ("graph_weight_shift", 0.006, "weight_shift", "nominal"),
        ("sensor_dropout_40", 0.006, "correct", "dropout_40"),
        ("sensor_stuck_high", 0.006, "correct", "stuck_high"),
        ("sensor_noisy", 0.006, "correct", "noisy"),
    ]
    return {name: run_monte_carlo(runs, seed, noise, graph, sensor)
            for name, noise, graph, sensor in cases}

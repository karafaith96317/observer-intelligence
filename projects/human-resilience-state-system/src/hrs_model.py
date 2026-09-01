"""HRS v0.2.1 minimal computational prototype.

This module intentionally uses only Python's standard library so the first
prototype is portable and auditable. It is a synthetic research model, not a
validated human-performance, medical, or autonomous safety system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, sqrt
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

DIMENSIONS: Tuple[str, ...] = ("C", "P", "A", "R", "S", "I")


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def sigmoid(value: float) -> float:
    if value >= 0:
        z = exp(-value)
        return 1.0 / (1.0 + z)
    z = exp(value)
    return z / (1.0 + z)


@dataclass(frozen=True)
class State:
    values: Mapping[str, float]

    def __post_init__(self) -> None:
        missing = set(DIMENSIONS) - set(self.values)
        if missing:
            raise ValueError(f"missing state dimensions: {sorted(missing)}")
        for key in DIMENSIONS:
            value = self.values[key]
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{key}={value} outside [0,1]")

    def vector(self) -> Tuple[float, ...]:
        return tuple(self.values[key] for key in DIMENSIONS)


@dataclass
class Entity:
    name: str
    baseline: State
    state: State
    prior_drift: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * len(DIMENSIONS))
    prior_velocity: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * len(DIMENSIONS))


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    weight: float


@dataclass
class HRSReport:
    drift: Dict[str, Tuple[float, ...]]
    drift_magnitude: Dict[str, float]
    drift_velocity: Dict[str, float]
    drift_acceleration: Dict[str, float]
    propagation_pressure: Dict[str, float]
    hypotheses: List[Tuple[str, float]]
    classification: str
    operational_risk: float
    confidence: float
    recommended_intervention: str
    suspected_root: str


class HRSModel:
    """Small explicit graph/state model for the HRS-01..05 experiments."""

    def __init__(
        self,
        entities: Sequence[Entity],
        edges: Sequence[Edge],
        weights: Mapping[str, float] | None = None,
    ) -> None:
        self.entities = {entity.name: entity for entity in entities}
        self.edges = list(edges)
        self.weights = {key: 1.0 for key in DIMENSIONS}
        if weights:
            self.weights.update(weights)
        self.history: List[Dict[str, float]] = []

    def set_state(self, entity_name: str, values: Mapping[str, float]) -> None:
        self.entities[entity_name].state = State({key: clamp(values[key]) for key in DIMENSIONS})

    def _drift_vector(self, entity: Entity) -> Tuple[float, ...]:
        return tuple(
            entity.state.values[key] - entity.baseline.values[key] for key in DIMENSIONS
        )

    def _weighted_magnitude(self, vector: Iterable[float]) -> float:
        return sqrt(
            sum(self.weights[key] * value * value for key, value in zip(DIMENSIONS, vector))
        )

    def _propagation_pressure(self, magnitudes: Mapping[str, float]) -> Dict[str, float]:
        pressure = {name: 0.0 for name in self.entities}
        for edge in self.edges:
            pressure[edge.target] += abs(edge.weight) * magnitudes[edge.source]
        return pressure

    def _root_scores(
        self,
        magnitudes: Mapping[str, float],
        pressure: Mapping[str, float],
        sensor_conflict: float,
    ) -> Dict[str, float]:
        # Root score rewards local anomaly that cannot be explained by upstream pressure.
        scores: Dict[str, float] = {}
        for name in self.entities:
            scores[name] = max(0.0, magnitudes[name] - 0.65 * pressure[name])

        if "sensor" in scores:
            scores["sensor"] += 0.75 * sensor_conflict
        scores["unknown"] = 0.05 + 0.20 * sensor_conflict
        return scores

    @staticmethod
    def _normalize_scores(scores: Mapping[str, float]) -> List[Tuple[str, float]]:
        total = sum(max(0.0, value) for value in scores.values())
        if total <= 0:
            return [("unknown", 1.0)]
        ranked = [(key, max(0.0, value) / total) for key, value in scores.items()]
        return sorted(ranked, key=lambda item: item[1], reverse=True)

    @staticmethod
    def _classify(
        magnitudes: Mapping[str, float],
        velocities: Mapping[str, float],
        root: str,
        utility_delta: float,
        sensor_conflict: float,
    ) -> str:
        max_drift = max(magnitudes.values())
        max_velocity = max(velocities.values())
        if max_drift < 0.12:
            return "nominal"
        if utility_delta > 0.02 and max_drift < 0.55:
            return "adaptive"
        if root == "sensor" or sensor_conflict > 0.55:
            return "system-induced"
        if utility_delta >= -0.02 and max_drift < 0.50:
            return "compensatory"
        if max_velocity > 0.10 or max_drift > 0.55:
            return "destabilizing"
        return "recoverable"

    @staticmethod
    def _intervention(risk: float, confidence: float, classification: str) -> str:
        if risk < 0.25:
            return "U0_observe"
        if confidence < 0.50:
            return "U1_request_verification"
        if classification in {"adaptive", "compensatory"}:
            return "U0_observe"
        if classification == "system-induced":
            return "U2_information_assistance"
        if risk < 0.60:
            return "U2_information_assistance"
        if risk < 0.78:
            return "U3_redistribute_workload"
        return "U4_secondary_review"

    def evaluate(
        self,
        *,
        sensor_conflict: float = 0.0,
        data_completeness: float = 1.0,
        utility_delta: float = 0.0,
        dt: float = 1.0,
    ) -> HRSReport:
        drift: Dict[str, Tuple[float, ...]] = {}
        magnitude: Dict[str, float] = {}
        velocity_mag: Dict[str, float] = {}
        accel_mag: Dict[str, float] = {}

        for name, entity in self.entities.items():
            d = self._drift_vector(entity)
            v = tuple((d_i - p_i) / dt for d_i, p_i in zip(d, entity.prior_drift))
            a = tuple((v_i - p_i) / dt for v_i, p_i in zip(v, entity.prior_velocity))
            drift[name] = d
            magnitude[name] = self._weighted_magnitude(d)
            velocity_mag[name] = self._weighted_magnitude(v)
            accel_mag[name] = self._weighted_magnitude(a)
            entity.prior_drift = d
            entity.prior_velocity = v

        pressure = self._propagation_pressure(magnitude)
        scores = self._root_scores(magnitude, pressure, sensor_conflict)
        hypotheses = self._normalize_scores(scores)
        root = hypotheses[0][0]
        classification = self._classify(
            magnitude, velocity_mag, root, utility_delta, sensor_conflict
        )

        network_drift = sum(magnitude.values()) / max(1, len(magnitude))
        max_velocity = max(velocity_mag.values())
        propagation = sum(pressure.values()) / max(1, len(pressure))
        risk_logit = -2.35 + 3.4 * network_drift + 2.2 * max_velocity + 1.5 * propagation
        if classification == "adaptive":
            risk_logit -= 0.9
        operational_risk = sigmoid(risk_logit)

        confidence = clamp(
            0.95 * data_completeness
            - 0.45 * sensor_conflict
            - 0.15 * hypotheses[0][1] * (1.0 - data_completeness)
        )
        intervention = self._intervention(operational_risk, confidence, classification)

        self.history.append(
            {
                "risk": operational_risk,
                "confidence": confidence,
                "max_drift": max(magnitude.values()),
                "max_velocity": max_velocity,
            }
        )

        return HRSReport(
            drift=drift,
            drift_magnitude=magnitude,
            drift_velocity=velocity_mag,
            drift_acceleration=accel_mag,
            propagation_pressure=pressure,
            hypotheses=hypotheses,
            classification=classification,
            operational_risk=operational_risk,
            confidence=confidence,
            recommended_intervention=intervention,
            suspected_root=root,
        )


def scalar_anomaly_baseline(model: HRSModel) -> Tuple[str, float]:
    """Naive comparator: blame the most anomalous entity without graph/context reasoning."""
    magnitudes = {
        name: model._weighted_magnitude(model._drift_vector(entity))
        for name, entity in model.entities.items()
    }
    root = max(magnitudes, key=magnitudes.get)
    return root, magnitudes[root]

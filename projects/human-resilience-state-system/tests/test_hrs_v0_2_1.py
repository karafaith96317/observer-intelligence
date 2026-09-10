import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from hrs_v021 import (GRAPH_PERTURBATIONS, SENSOR_PERTURBATIONS,
                      GROUND_TRUTH_ROOT, run_monte_carlo, run_validation_suite, simulate)


class TestHRSv021(unittest.TestCase):
    def test_deterministic_ground_truth_scenarios(self):
        for scenario, expected in GROUND_TRUTH_ROOT.items():
            with self.subTest(scenario=scenario):
                self.assertEqual(simulate(scenario, seed=1).root_cause, expected)

    def test_adaptation_is_not_escalated(self):
        result = simulate("HRS-01", seed=7)
        self.assertEqual(result.classification, "adaptive")
        self.assertIn(result.intervention, ("U0", "U1"))

    def test_temporal_and_calibration_metrics_are_well_formed(self):
        metrics = run_monte_carlo(runs=250, seed=99)
        self.assertTrue(0 <= metrics["detection_rate"] <= 1)
        self.assertIsNotNone(metrics["mean_detection_delay_steps"])
        self.assertGreaterEqual(metrics["mean_detection_delay_steps"], 0)
        self.assertTrue(0 <= metrics["confidence_brier_score"] <= 1)
        self.assertTrue(0 <= metrics["confidence_ece_10_bin"] <= 1)

    def test_all_adversarial_perturbations_execute(self):
        for graph in GRAPH_PERTURBATIONS:
            self.assertEqual(run_monte_carlo(25, 4, graph_perturbation=graph)["configuration"]["graph_perturbation"], graph)
        for sensor in SENSOR_PERTURBATIONS:
            self.assertEqual(run_monte_carlo(25, 4, sensor_perturbation=sensor)["configuration"]["sensor_perturbation"], sensor)

    def test_suite_is_deterministic(self):
        self.assertEqual(run_validation_suite(30, 42), run_validation_suite(30, 42))

    def test_frozen_nominal_output_matches(self):
        frozen = json.loads((ROOT / "benchmarks" / "v0.2.1-seed42.json").read_text())
        self.assertEqual(run_validation_suite(runs=1000, seed=42), frozen)


if __name__ == "__main__":
    unittest.main()

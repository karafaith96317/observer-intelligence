import pathlib
import sys
import unittest

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from hrs_v021 import GROUND_TRUTH_ROOT, run_monte_carlo, simulate


class TestHRSv021(unittest.TestCase):
    def test_deterministic_ground_truth_scenarios(self):
        for scenario, expected_root in GROUND_TRUTH_ROOT.items():
            with self.subTest(scenario=scenario):
                result = simulate(scenario, seed=1, noise_sd=0.006)
                self.assertEqual(result.root_cause, expected_root)

    def test_adaptation_is_not_escalated(self):
        result = simulate("HRS-01", seed=7)
        self.assertEqual(result.classification, "adaptive")
        self.assertIn(result.intervention, ("U0", "U1"))

    def test_sensor_corruption_is_not_attributed_to_operator(self):
        result = simulate("HRS-03", seed=11)
        self.assertEqual(result.root_cause, "sensor")
        self.assertNotEqual(result.classification, "human-origin")

    def test_ai_origin_is_preserved(self):
        result = simulate("HRS-04", seed=13)
        self.assertEqual(result.root_cause, "ai")

    def test_comms_cascade_is_detected(self):
        result = simulate("HRS-05", seed=17)
        self.assertEqual(result.root_cause, "comms")
        self.assertEqual(result.classification, "system-cascade")

    def test_confidence_is_bounded(self):
        result = simulate("HRS-02", seed=19)
        self.assertTrue(all(0.0 <= q <= 1.0 for q in result.confidence.values()))
        self.assertTrue(0.0 <= result.risk <= 1.0)

    def test_monte_carlo_beats_scalar_root_attribution(self):
        metrics = run_monte_carlo(runs=1000, seed=42, noise_sd=0.006)
        self.assertGreater(metrics["hrs_root_accuracy"], metrics["scalar_root_accuracy"])
        self.assertLessEqual(metrics["human_fault_false_positive_rate"], 0.05)
        self.assertLessEqual(metrics["adaptive_unnecessary_intervention_rate"], 0.05)

    def test_noise_stress_does_not_silently_claim_validation(self):
        # This is deliberately a weak invariant: performance may degrade as noise rises,
        # but all metrics must remain numerically well-formed for later calibration work.
        metrics = run_monte_carlo(runs=250, seed=99, noise_sd=0.02)
        self.assertTrue(0.0 <= metrics["hrs_root_accuracy"] <= 1.0)
        self.assertTrue(0.0 <= metrics["scalar_root_accuracy"] <= 1.0)


if __name__ == "__main__":
    unittest.main()

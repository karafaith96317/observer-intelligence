import unittest

from benchmarks.okn_oi_v0_1 import baseline, oi_condition, score


class TestOKNOIBenchmark(unittest.TestCase):
    def test_oi_reduces_false_authorization_in_frozen_fixtures(self):
        self.assertLess(
            score(oi_condition)["false_authorization_rate"],
            score(baseline)["false_authorization_rate"],
        )

    def test_oi_does_not_authorize_scope_mismatch(self):
        row = dict(score(oi_condition)["rows"])["authority-mismatch"]
        self.assertFalse(row["authorize"])

    def test_oi_abstains_on_uncorrected_sampling_transform(self):
        row = dict(score(oi_condition)["rows"])["sampling-transform"]
        self.assertIsNone(row["decision"])
        self.assertFalse(row["authorize"])

    def test_baseline_authorizes_sampling_transform(self):
        row = dict(score(baseline)["rows"])["sampling-transform"]
        self.assertTrue(row["authorize"])


if __name__ == "__main__":
    unittest.main()

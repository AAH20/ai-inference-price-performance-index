import json
import unittest
from pathlib import Path

from inference_index.engine import rank_candidates


ROOT = Path(__file__).parents[1]


class EngineTests(unittest.TestCase):
    def test_ranks_eligible_candidates_and_emits_provenance(self):
        workload = json.loads((ROOT / "examples/workload.json").read_text())
        result = rank_candidates(workload, ROOT / "datasets/illustrative-index.json")

        self.assertIsNotNone(result["recommendation"])
        self.assertTrue(result["recommendation"]["eligible"])
        self.assertEqual(len(result["recommendation"]["provenance_sha256"]), 64)
        self.assertTrue(
            all("cost_per_successful_request_usd" in row for row in result["candidates"])
        )

    def test_rejects_candidates_below_quality_floor(self):
        workload = json.loads((ROOT / "examples/workload.json").read_text())
        workload["required_quality"] = 0.99
        result = rank_candidates(workload, ROOT / "datasets/illustrative-index.json")

        self.assertIsNone(result["recommendation"])
        self.assertFalse(any(row["eligible"] for row in result["candidates"]))


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TierCatalogTests(unittest.TestCase):
    def test_low_medium_high_tiers_are_defined_with_skill_metadata(self):
        expected = ["low", "medium", "high"]
        for tier in expected:
            path = ROOT / "tiers" / f"{tier}.json"
            self.assertTrue(path.exists(), f"missing tier file: {path}")
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["id"], tier)
            self.assertIn("title", data)
            self.assertIn("description", data)
            self.assertTrue(data.get("skills"), f"{tier} has no skills")
            sample = data["skills"][0]
            for key in ["id", "description", "manual", "source"]:
                self.assertIn(key, sample)
                self.assertTrue(sample[key], f"{tier} sample missing {key}")
            self.assertTrue(sample["source"].startswith("http"), sample["source"])

    def test_tiers_are_monotonic(self):
        tiers = {}
        for tier in ["low", "medium", "high"]:
            data = json.loads((ROOT / "tiers" / f"{tier}.json").read_text(encoding="utf-8"))
            tiers[tier] = [item["id"] for item in data["skills"]]
        self.assertTrue(set(tiers["low"]).issubset(tiers["medium"]))
        self.assertTrue(set(tiers["medium"]).issubset(tiers["high"]))
        self.assertGreater(len(tiers["medium"]), len(tiers["low"]))
        self.assertGreater(len(tiers["high"]), len(tiers["medium"]))

    def test_tier_docs_and_manual_index_exist(self):
        self.assertTrue((ROOT / "docs" / "tiers" / "low.md").exists())
        self.assertTrue((ROOT / "docs" / "tiers" / "medium.md").exists())
        self.assertTrue((ROOT / "docs" / "tiers" / "high.md").exists())
        self.assertTrue((ROOT / "docs" / "SKILL_MANUALS.md").exists())


if __name__ == "__main__":
    unittest.main()

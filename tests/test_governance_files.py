import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GovernanceFilesTests(unittest.TestCase):
    def test_standard_bundle_overrides_are_well_formed(self):
        path = ROOT / "catalog" / "standard-bundle-overrides.json"
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data.get("pinned_capabilities"), dict)
        self.assertIsInstance(data.get("excluded_skills"), dict)
        for skill_id, reason in data["excluded_skills"].items():
            self.assertTrue(skill_id)
            self.assertTrue(reason)

    def test_skillopt_usage_doc_exists(self):
        path = ROOT / "docs" / "SKILLOPT_USAGE.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("Quality Gates", text)
        self.assertIn("Suggested First Targets", text)


if __name__ == "__main__":
    unittest.main()

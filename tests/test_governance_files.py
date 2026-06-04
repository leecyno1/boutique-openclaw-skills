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
        self.assertIn("check_skillopt_ready.py", text)

    def test_skillopt_candidates_are_well_formed(self):
        path = ROOT / "optimization" / "skillopt-candidates.json"
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        candidates = data.get("candidates", [])
        self.assertTrue(candidates)
        priorities = [item["priority"] for item in candidates]
        self.assertEqual(priorities, sorted(priorities))
        for item in candidates:
            self.assertTrue((ROOT / "skills" / "default" / item["skill_id"] / "SKILL.md").exists())
            self.assertIn(item["template"], {"qa", "finance-analysis", "content-rubric", "coding-rubric"})
            self.assertTrue(item["failure_mode"])
            self.assertTrue(item["acceptance_gate"])

    def test_skillopt_helper_scripts_exist(self):
        for name in [
            "create_skillopt_dataset.py",
            "check_skillopt_ready.py",
            "review_skillopt_candidate.py",
        ]:
            self.assertTrue((ROOT / "optimization" / "scripts" / name).exists())


if __name__ == "__main__":
    unittest.main()

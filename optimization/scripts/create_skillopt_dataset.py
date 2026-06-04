#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASETS = ROOT / "optimization" / "datasets" / "skillopt"

TEMPLATE = [
    {
        "id": "case-001",
        "question": "Describe the task or user request this skill should handle.",
        "context": "Add any source material, constraints, sample input, or rubric context here.",
        "answers": ["Write the expected concise answer or success criteria here."],
    }
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a SkillOpt dataset for one skill.")
    parser.add_argument("skill_id")
    parser.add_argument("--force", action="store_true", help="overwrite existing split files")
    args = parser.parse_args()

    skill_path = ROOT / "skills" / "default" / args.skill_id / "SKILL.md"
    if not skill_path.exists():
        raise SystemExit(f"missing skill: {skill_path}")

    base = DATASETS / args.skill_id
    for split in ("train", "val", "test"):
        path = base / split / "items.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            continue
        path.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"created dataset scaffold: {base}")
    print("edit train/val/test/items.json before running SkillOpt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

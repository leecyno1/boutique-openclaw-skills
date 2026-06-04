#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASETS = ROOT / "optimization" / "datasets" / "skillopt"

TEMPLATES = {
    "qa": [
        {
            "id": "qa-001",
            "question": "Ask the concrete question this skill should answer.",
            "context": "Provide source text, webpage notes, extracted markdown, or reference material.",
            "answers": ["Expected concise answer or extraction result."],
        }
    ],
    "finance-analysis": [
        {
            "id": "finance-001",
            "question": "Analyze this market/data scenario and produce the expected decision support output.",
            "context": "Include ticker, market, input data snapshot, constraints, and any ground-truth reference.",
            "answers": ["Expected analytical judgment, score, or risk/next-action summary."],
        }
    ],
    "content-rubric": [
        {
            "id": "content-001",
            "question": "Rewrite or format the content according to the target style and constraints.",
            "context": "Include original draft, audience, channel, style rules, and rubric dimensions.",
            "answers": ["Expected output traits or a reference answer that satisfies the rubric."],
        }
    ],
    "coding-rubric": [
        {
            "id": "coding-001",
            "question": "Solve this coding or code-review task using the target skill.",
            "context": "Include repo context, failing behavior, constraints, and expected verification steps.",
            "answers": ["Expected patch qualities, test outcome, or review finding."],
        }
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a SkillOpt dataset for one skill.")
    parser.add_argument("skill_id")
    parser.add_argument("--template", choices=sorted(TEMPLATES), default="qa")
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
        path.write_text(json.dumps(TEMPLATES[args.template], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = base / "dataset.json"
    if not manifest.exists() or args.force:
        manifest.write_text(
            json.dumps(
                {
                    "skill_id": args.skill_id,
                    "template": args.template,
                    "status": "draft",
                    "notes": "Replace template examples before running SkillOpt.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"created dataset scaffold: {base}")
    print(f"template: {args.template}")
    print("edit train/val/test/items.json before running SkillOpt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

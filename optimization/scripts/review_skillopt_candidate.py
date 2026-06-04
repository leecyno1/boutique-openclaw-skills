#!/usr/bin/env python3
import argparse
import difflib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a review report for a SkillOpt best_skill.md candidate.")
    parser.add_argument("skill_id")
    parser.add_argument("--candidate", help="path to best_skill.md; defaults to optimization/skillopt-runs/<skill-id>/best_skill.md")
    parser.add_argument("--output", help="review report path; defaults to optimization/skillopt-runs/<skill-id>/review.md")
    args = parser.parse_args()

    current = ROOT / "skills" / "default" / args.skill_id / "SKILL.md"
    candidate = Path(args.candidate) if args.candidate else ROOT / "optimization" / "skillopt-runs" / args.skill_id / "best_skill.md"
    output = Path(args.output) if args.output else ROOT / "optimization" / "skillopt-runs" / args.skill_id / "review.md"

    if not current.exists():
        raise SystemExit(f"missing current skill: {current}")
    if not candidate.exists():
        raise SystemExit(f"missing candidate: {candidate}")

    current_text = read_text(current)
    candidate_text = read_text(candidate)
    current_lines = current_text.splitlines()
    candidate_lines = candidate_text.splitlines()
    diff_lines = list(
        difflib.unified_diff(
            current_lines,
            candidate_lines,
            fromfile=str(current.relative_to(ROOT)),
            tofile=str(candidate.relative_to(ROOT)) if candidate.is_relative_to(ROOT) else str(candidate),
            lineterm="",
        )
    )

    summary = {
        "skill_id": args.skill_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "current_lines": len(current_lines),
        "candidate_lines": len(candidate_lines),
        "diff_lines": len(diff_lines),
        "current_path": str(current),
        "candidate_path": str(candidate),
    }

    report = [
        f"# SkillOpt Candidate Review: `{args.skill_id}`",
        "",
        f"- Generated at: `{summary['generated_at']}`",
        f"- Current lines: `{summary['current_lines']}`",
        f"- Candidate lines: `{summary['candidate_lines']}`",
        f"- Diff lines: `{summary['diff_lines']}`",
        "",
        "## Required Human Checks",
        "",
        "- Does the candidate improve the named failure mode or benchmark score?",
        "- Does it preserve native upstream attribution and license notes?",
        "- Does it avoid adding hidden API-key or tool requirements?",
        "- Is the trigger description still concise and accurate?",
        "- Can the accepted change be reduced to a smaller manual patch?",
        "",
        "## Unified Diff",
        "",
        "```diff",
        *diff_lines,
        "```",
        "",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(report), encoding="utf-8")
    metadata = output.with_suffix(".json")
    metadata.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"review report: {output}")
    print(f"review metadata: {metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

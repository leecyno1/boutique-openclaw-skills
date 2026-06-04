#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASETS = ROOT / "optimization" / "datasets" / "skillopt"
CANDIDATES = ROOT / "optimization" / "skillopt-candidates.json"
SKILLOPT_DIR = ROOT / "optimization" / "skillopt"
PLACEHOLDER_PATTERNS = [
    re.compile(r"Describe the task", re.I),
    re.compile(r"Add any source material", re.I),
    re.compile(r"Expected concise answer", re.I),
    re.compile(r"Expected analytical judgment", re.I),
    re.compile(r"Expected output traits", re.I),
    re.compile(r"Expected patch qualities", re.I),
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*[A-Za-z0-9_./+\-=]{12,}"),
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_for(skill_id: str) -> dict | None:
    if not CANDIDATES.exists():
        return None
    for item in load_json(CANDIDATES).get("candidates", []):
        if item.get("skill_id") == skill_id:
            return item
    return None


def check_items(path: Path) -> tuple[list[str], int]:
    issues = []
    if not path.exists():
        return [f"missing split file: {path}"], 0
    try:
        items = load_json(path)
    except Exception as error:
        return [f"invalid json: {path}: {error}"], 0
    if not isinstance(items, list) or not items:
        return [f"split must be a non-empty array: {path}"], 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            issues.append(f"template placeholder still present: {path}")
            break
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"possible secret in dataset: {path}")
            break
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            issues.append(f"item {index} is not an object: {path}")
            continue
        for key in ("id", "question", "context", "answers"):
            if key not in item or item[key] in ("", [], None):
                issues.append(f"item {index} missing {key}: {path}")
        if "answers" in item and not isinstance(item["answers"], list):
            issues.append(f"item {index} answers must be an array: {path}")
    return issues, len(items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether one skill is ready for a SkillOpt run.")
    parser.add_argument("skill_id")
    parser.add_argument("--json", action="store_true", help="print machine-readable result")
    parser.add_argument("--require-models", action="store_true", help="require SKILLOPT_OPTIMIZER_MODEL and SKILLOPT_TARGET_MODEL")
    args = parser.parse_args()

    issues = []
    warnings = []
    skill_path = ROOT / "skills" / "default" / args.skill_id / "SKILL.md"
    if not skill_path.exists():
        issues.append(f"missing skill file: {skill_path}")

    candidate = candidate_for(args.skill_id)
    if not candidate:
        warnings.append("skill is not listed in optimization/skillopt-candidates.json")

    if not (SKILLOPT_DIR / "scripts" / "train.py").exists():
        issues.append("missing vendored SkillOpt train.py")

    dataset = DATASETS / args.skill_id
    total_items = 0
    for split in ("train", "val", "test"):
        split_issues, count = check_items(dataset / split / "items.json")
        issues.extend(split_issues)
        total_items += count

    manifest = dataset / "dataset.json"
    if manifest.exists():
        try:
            manifest_data = load_json(manifest)
            if manifest_data.get("status") == "draft":
                warnings.append("dataset manifest status is draft")
        except Exception as error:
            issues.append(f"invalid dataset manifest: {error}")
    else:
        warnings.append("missing dataset manifest")

    if args.require_models:
        if not os.environ.get("SKILLOPT_OPTIMIZER_MODEL"):
            issues.append("missing SKILLOPT_OPTIMIZER_MODEL")
        if not os.environ.get("SKILLOPT_TARGET_MODEL"):
            issues.append("missing SKILLOPT_TARGET_MODEL")

    result = {
        "skill_id": args.skill_id,
        "ready": not issues,
        "dataset_items": total_items,
        "candidate": candidate or {},
        "issues": issues,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "READY" if result["ready"] else "NOT READY"
        print(f"SkillOpt readiness for {args.skill_id}: {status}")
        print(f"dataset items: {total_items}")
        for issue in issues:
            print(f"[ISSUE] {issue}")
        for warning in warnings:
            print(f"[WARN] {warning}")
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

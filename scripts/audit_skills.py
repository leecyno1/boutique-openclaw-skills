#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog" / "skills.json"
SKILL_DIRS = [
    Path.home() / ".openclaw" / "skills",
    Path.home() / "Desktop" / "Projects" / "clawdbot" / "skills",
]

HIGH_RISK_PATTERNS = [
    re.compile(r"\bsudo\b"),
    re.compile(r"rm\s+-rf\s+/"),
    re.compile(r"curl\s+[^\n|]+\|\s*(sh|bash)"),
    re.compile(r"wget\s+[^\n|]+\|\s*(sh|bash)"),
    re.compile(r"eval\("),
]


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def find_skill_path(skill: str) -> Path | None:
    for base in SKILL_DIRS:
      p = base / skill
      if p.exists():
          return p
    return None


def scan_text_files(root: Path, max_files: int = 120) -> List[dict]:
    findings = []
    checked = 0
    for p in root.rglob("*"):
        if checked >= max_files:
            break
        if not p.is_file():
            continue
        if "node_modules" in p.parts:
            continue
        if ".test." in p.name:
            continue
        if p.suffix.lower() not in {".sh", ".py", ".js", ".ts"}:
            continue
        checked += 1
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rule in HIGH_RISK_PATTERNS:
            if rule.search(text):
                findings.append({"file": str(p), "pattern": rule.pattern})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit curated OpenClaw skill set")
    parser.add_argument("--report", default=str(REPO / "reports" / "audit-latest.md"))
    parser.add_argument("--json", default=str(REPO / "reports" / "audit-latest.json"))
    args = parser.parse_args()

    catalog = load_catalog()
    skills = catalog.get("skills", [])
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dup_caps = {}
    cap_owner = {}
    for s in skills:
        cap = s["capability"]
        if cap in cap_owner:
            dup_caps.setdefault(cap, [cap_owner[cap]]).append(s["skill"])
        else:
            cap_owner[cap] = s["skill"]

    missing = []
    env_missing = []
    risky = []
    resolved = []

    for s in skills:
        skill = s["skill"]
        p = find_skill_path(skill)
        if not p:
            missing.append(skill)
            continue
        resolved.append({"skill": skill, "path": str(p)})
        for env in s.get("requires", []):
            if not os.environ.get(env):
                env_missing.append({"skill": skill, "env": env})
        risky.extend([{"skill": skill, **f} for f in scan_text_files(p)])

    status = "PASS"
    if dup_caps or risky:
        status = "FAIL"
    elif missing or env_missing:
        status = "WARN"

    result = {
        "timestamp": ts,
        "status": status,
        "summary": {
            "catalog_skills": len(skills),
            "resolved_skills": len(resolved),
            "missing_skills": len(missing),
            "missing_env": len(env_missing),
            "duplicate_capabilities": len(dup_caps),
            "risky_hits": len(risky),
        },
        "duplicates": dup_caps,
        "missing": missing,
        "missing_env": env_missing,
        "risky": risky,
        "resolved": resolved,
    }

    report_lines = [
        f"# Boutique OpenClaw Skills Audit",
        "",
        f"- Time: {ts}",
        f"- Status: **{status}**",
        f"- Catalog skills: {len(skills)}",
        f"- Installed/Resolved: {len(resolved)}",
        f"- Missing: {len(missing)}",
        f"- Missing env vars: {len(env_missing)}",
        f"- Duplicate capabilities: {len(dup_caps)}",
        f"- Risk hits: {len(risky)}",
        "",
        "## Missing Skills",
    ]
    report_lines.extend([f"- {s}" for s in missing] or ["- None"])
    report_lines.append("")
    report_lines.append("## Missing Environment Variables")
    report_lines.extend([f"- {item['skill']}: `{item['env']}`" for item in env_missing] or ["- None"])
    report_lines.append("")
    report_lines.append("## Duplicate Capabilities")
    if dup_caps:
        for cap, owners in dup_caps.items():
            report_lines.append(f"- {cap}: {', '.join(owners)}")
    else:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Risk Findings")
    if risky:
        for item in risky[:80]:
            report_lines.append(
                f"- {item['skill']}: `{item['pattern']}` in `{item['file']}`"
            )
        if len(risky) > 80:
            report_lines.append(f"- ... {len(risky)-80} more findings")
    else:
        report_lines.append("- None")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result["summary"], ensure_ascii=False))
    print(f"report: {report_path}")
    print(f"json: {json_path}")

    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

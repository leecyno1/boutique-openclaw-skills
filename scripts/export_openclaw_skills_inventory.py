#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "OPENCLAW_SKILLS_FULL.md"


def load_skills_from_cli() -> dict:
    proc = subprocess.run(
        ["openclaw", "skills", "list", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def github_link(skill: dict) -> str:
    homepage = (skill.get("homepage") or "").strip()
    if homepage:
        return homepage
    name = skill.get("name", "").strip()
    return f"https://github.com/search?q={name}&type=repositories"


def missing_text(skill: dict) -> str:
    missing = skill.get("missing") or {}
    parts = []
    for key in ("bins", "anyBins", "env", "config", "os"):
        vals = missing.get(key) or []
        if vals:
            parts.append(f"{key}: {', '.join(vals)}")
    if not parts:
        return "-"
    return "; ".join(parts)


def group_source_name(source: str) -> str:
    mapping = {
        "openclaw-workspace": "Workspace skills",
        "openclaw-managed": "Managed skills",
        "openclaw-bundled": "Bundled skills",
        "openclaw-extra": "Extra skills",
    }
    return mapping.get(source, source)


def render(skills_data: dict) -> str:
    skills = sorted(skills_data.get("skills", []), key=lambda x: x.get("name", "").lower())
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(skills)
    ready = sum(1 for s in skills if s.get("eligible"))
    not_ready = total - ready

    lines = [
        "# OpenClaw Skills Inventory (Current Machine)",
        "",
        f"- Generated at: `{now}`",
        f"- Total skills: `{total}`",
        f"- Ready (eligible): `{ready}`",
        f"- Not ready: `{not_ready}`",
        "",
        "> Source: `openclaw skills list --json`",
        "",
    ]

    # Section 1: all skills by source
    lines += ["## 1) All skills by source", ""]
    sources = sorted({s.get("source", "unknown") for s in skills})
    for src in sources:
        chunk = [s for s in skills if s.get("source", "unknown") == src]
        lines += [f"### {group_source_name(src)} ({len(chunk)})", ""]
        lines += ["| Skill | Eligible | Disabled | Missing requirements | Link |", "|---|---:|---:|---|---|"]
        for s in chunk:
            link = github_link(s)
            lines.append(
                f"| `{s.get('name','')}` | "
                f"{'yes' if s.get('eligible') else 'no'} | "
                f"{'yes' if s.get('disabled') else 'no'} | "
                f"{missing_text(s)} | "
                f"[repo]({link}) |"
            )
        lines += ["", ""]

    # Section 2: plain name list
    lines += ["## 2) Plain name list", ""]
    lines += [", ".join(f"`{s.get('name','')}`" for s in skills), ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export OpenClaw skills inventory to markdown")
    parser.add_argument("--input-json", help="Optional existing JSON file from `openclaw skills list --json`")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output markdown path")
    args = parser.parse_args()

    if args.input_json:
        data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    else:
        data = load_skills_from_cli()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

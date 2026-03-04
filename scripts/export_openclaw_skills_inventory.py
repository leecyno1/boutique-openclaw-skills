#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from collections import defaultdict


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "OPENCLAW_SKILLS_FULL.md"
SKILLS_LOCK_PATH = Path.home() / "clawd" / "skills-lock.json"

GITHUB_URL_RE = re.compile(r"https?://github\.com/[^\s)\"'>]+")


CATEGORY_ORDER = [
    "agent_automation",
    "engineering_ops",
    "research_intel",
    "design_ui",
    "content_growth",
    "media_generation",
    "docs_office",
    "baoyu_suite",
    "other_integrations",
]

CATEGORY_LABELS = {
    "agent_automation": "Agent/自动化与能力进化",
    "engineering_ops": "开发/工程与运维",
    "research_intel": "搜索/研究/情报",
    "design_ui": "设计/前端/UI",
    "content_growth": "内容/营销/增长",
    "media_generation": "图像/音频/多媒体生成处理",
    "docs_office": "文档/办公生产力",
    "baoyu_suite": "Baoyu 系列内容产出与分发",
    "other_integrations": "其他集成能力",
}


def load_skills_from_cli() -> dict:
    proc = subprocess.run(
        ["openclaw", "skills", "list", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def load_workspace_skill_lock() -> dict:
    if not SKILLS_LOCK_PATH.exists():
        return {}
    try:
        payload = json.loads(SKILLS_LOCK_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload.get("skills", {}) if isinstance(payload, dict) else {}


def normalize_repo_url(url: str) -> str:
    u = url.strip()
    if u.startswith("git+"):
        u = u[4:]
    if u.endswith(".git"):
        u = u[:-4]
    return u


def infer_base_dir(skill: dict) -> Path | None:
    name = (skill.get("name") or "").strip()
    source = (skill.get("source") or "").strip()
    if source == "openclaw-managed":
        p = Path.home() / ".openclaw" / "skills" / name
        return p if p.exists() else None
    if source == "openclaw-workspace":
        p = Path.home() / "clawd" / "skills" / name
        return p if p.exists() else None
    if source == "openclaw-extra":
        p = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "extensions" / "feishu" / "skills" / name
        return p if p.exists() else None
    return None


def parse_repository_from_package_json(base_dir: Path) -> str | None:
    pkg = base_dir / "package.json"
    if not pkg.exists():
        return None
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return None
    repo = data.get("repository")
    if isinstance(repo, dict):
        url = repo.get("url") or ""
    elif isinstance(repo, str):
        url = repo
    else:
        url = ""
    if "github.com/" not in url:
        return None
    return normalize_repo_url(url)


def extract_github_urls_from_text(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    urls = [u.rstrip(".,)]}\"'") for u in GITHUB_URL_RE.findall(content)]
    filtered = []
    for u in urls:
        bad_tokens = ("/login", "/sponsors/", "/orgs/community/discussions", "/example", "${")
        if any(tok in u for tok in bad_tokens):
            continue
        filtered.append(u)
    return filtered


def pick_best_github_from_local(base_dir: Path, skill_name: str) -> str | None:
    pkg_repo = parse_repository_from_package_json(base_dir)
    if pkg_repo:
        return pkg_repo

    for filename in ("SKILL.md", "README.md", "readme.md"):
        p = base_dir / filename
        if not p.exists():
            continue
        urls = extract_github_urls_from_text(p)
        if not urls:
            continue
        for u in urls:
            if f"/skills/{skill_name}" in u or u.endswith(f"/{skill_name}"):
                return normalize_repo_url(u)
        return normalize_repo_url(urls[0])
    return None


def github_link(skill: dict, lock_sources: dict) -> str:
    name = (skill.get("name") or "").strip()

    lock_item = lock_sources.get(name) or {}
    if lock_item.get("sourceType") == "github":
        source = str(lock_item.get("source") or "").strip()
        if "/" in source:
            return f"https://github.com/{source}/tree/main/skills/{name}"
        return f"https://github.com/{source}"

    if skill.get("source") == "openclaw-extra":
        return f"https://github.com/openclaw/openclaw/tree/main/extensions/feishu/skills/{name}"

    homepage = (skill.get("homepage") or "").strip()
    if "github.com/" in homepage:
        return normalize_repo_url(homepage)

    base_dir = infer_base_dir(skill)
    if base_dir:
        link = pick_best_github_from_local(base_dir, name)
        if link:
            return link

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


def classify_skill(skill: dict) -> str:
    name = (skill.get("name") or "").strip().lower()

    if name.startswith("baoyu-"):
        return "baoyu_suite"

    if name in {
        "capability-evolver",
        "cron-wake",
        "proactive-agent",
        "self-improving-agent",
        "subagent",
        "brainstorming",
        "reflection",
        "oracle",
        "find-skills",
        "skill-creator",
        "byterover",
    }:
        return "agent_automation"

    if name in {
        "agent-browser",
        "chrome-devtools-mcp",
        "github",
        "gh-issues",
        "mcp-builder",
        "database",
        "prisma-database-setup",
        "shell",
        "tmux",
        "tdd",
        "test-driven-development",
        "session-logs",
        "model-usage",
        "skill-security-auditor",
        "coding-agent",
    }:
        return "engineering_ops"

    if name in {
        "brave-search",
        "tavily-search",
        "web-search",
        "search",
        "minimax-web-search",
        "blogwatcher",
        "news-radar",
        "finance-data",
        "producthunt",
        "requesthunt",
        "domain-hunter",
        "summarize",
        "baoyu-url-to-markdown",
        "url-to-markdown",
        "reddit",
        "goplaces",
        "mcporter",
    }:
        return "research_intel"

    if name in {
        "frontend-design",
        "tailwind",
        "tailwind-design-system",
        "logo-creator",
        "banner-creator",
        "infographic-pro",
        "format-pro",
    }:
        return "design_ui"

    if name in {
        "content-strategy",
        "social-content",
        "marketing-psychology",
        "programmatic-seo",
        "seo-geo",
        "larry",
        "twitter",
        "bird",
    }:
        return "content_growth"

    if name in {
        "ai-image-generation",
        "openai-image-gen",
        "nanobanana",
        "nano-banana-pro",
        "minimax-image-understanding",
        "minimax-understand-image",
        "ai-music-generation",
        "ai-music-prompts",
        "elevenlabs-music",
        "openai-whisper",
        "openai-whisper-api",
        "tts",
        "sherpa-onnx-tts",
        "video-frames",
    }:
        return "media_generation"

    if name in {
        "pdf",
        "nano-pdf",
        "docx",
        "pptx",
        "xlsx",
        "todo",
        "todoist-api",
        "apple-notes",
        "apple-reminders",
        "apple-calendar",
        "things-mac",
        "himalaya",
        "notion",
        "obsidian",
        "bear-notes",
    }:
        return "docs_office"

    return "other_integrations"


def render(skills_data: dict) -> str:
    skills = sorted(skills_data.get("skills", []), key=lambda x: x.get("name", "").lower())
    lock_sources = load_workspace_skill_lock()
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(skills)
    ready = sum(1 for s in skills if s.get("eligible"))
    not_ready = total - ready
    bundled = [s for s in skills if s.get("source") == "openclaw-bundled"]
    non_bundled = [s for s in skills if s.get("source") != "openclaw-bundled"]

    lines = [
        "# OpenClaw Skills Inventory (Current Machine)",
        "",
        f"- Generated at: `{now}`",
        f"- Total skills: `{total}`",
        f"- Ready (eligible): `{ready}`",
        f"- Not ready: `{not_ready}`",
        f"- OpenClaw 内置默认 skills: `{len(bundled)}`",
        f"- 非内置 skills: `{len(non_bundled)}`",
        "",
        "> Source: `openclaw skills list --json`",
        "",
    ]

    # Section 1: bundled skills
    lines += ["## 1) OpenClaw 内置默认 skills（单独分类，不附 GitHub 地址）", ""]
    lines += ["| Skill | Eligible | Disabled | Missing requirements |", "|---|---:|---:|---|"]
    for s in bundled:
        lines.append(
            f"| `{s.get('name','')}` | "
            f"{'yes' if s.get('eligible') else 'no'} | "
            f"{'yes' if s.get('disabled') else 'no'} | "
            f"{missing_text(s)} |"
        )
    lines += ["", ""]

    # Section 2: classify non-bundled skills with github links
    lines += ["## 2) 非内置 skills（按仓库分类要求 + GitHub 地址）", ""]
    grouped = defaultdict(list)
    for s in non_bundled:
        grouped[classify_skill(s)].append(s)

    for key in CATEGORY_ORDER:
        chunk = sorted(grouped.get(key, []), key=lambda x: (x.get("name") or "").lower())
        lines += [f"### {CATEGORY_LABELS[key]}（{len(chunk)}）", ""]
        if not chunk:
            lines += ["- （无）", ""]
            continue
        lines += ["| Skill | Eligible | Disabled | Source | GitHub |", "|---|---:|---:|---|---|"]
        for s in chunk:
            lines.append(
                f"| `{s.get('name','')}` | "
                f"{'yes' if s.get('eligible') else 'no'} | "
                f"{'yes' if s.get('disabled') else 'no'} | "
                f"`{s.get('source','unknown')}` | "
                f"[repo]({github_link(s, lock_sources)}) |"
            )
        lines += ["", ""]

    # Section 3: plain name list
    lines += ["## 3) Plain name list", ""]
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

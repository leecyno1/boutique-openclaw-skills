#!/usr/bin/env python3
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.json"
OUT_PATH = ROOT / "docs" / "SKILLS_DIRECTORY.md"
OPENCLAW_DEFAULT_PATH = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw"

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

# Preferred explicit GitHub links for frequent skills. Fallback is GitHub search.
GITHUB_OVERRIDES = {
    "atxp": "https://github.com/atxp-dev/cli",
    "baoyu-article-illustrator": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-article-illustrator",
    "baoyu-comic": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-comic",
    "baoyu-cover-image": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-cover-image",
    "baoyu-infographic": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-infographic",
    "baoyu-post-to-wechat": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-post-to-wechat",
    "baoyu-post-to-x": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-post-to-x",
    "baoyu-slide-deck": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-slide-deck",
    "baoyu-url-to-markdown": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-url-to-markdown",
    "baoyu-xhs-images": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-xhs-images",
    "blogwatcher": "https://github.com/Hyaxia/blogwatcher",
    "chrome-devtools-mcp": "https://github.com/ChromeDevTools/chrome-devtools-mcp",
    "domain-hunter": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/domain-hunter",
    "himalaya": "https://github.com/pimalaya/himalaya",
    "logo-creator": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/logo-creator",
    "nanobanana": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/nanobanana",
    "oracle": "https://github.com/steipete/oracle",
    "peekaboo": "https://github.com/steipete/Peekaboo",
    "producthunt": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/producthunt",
    "reddit": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/reddit",
    "requesthunt": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/requesthunt",
    "seo-geo": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/seo-geo",
    "skill-name": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/skill-name",
    "things-mac": "https://github.com/ossianhempel/things3-cli",
    "twitter": "https://github.com/ReScienceLab/opc-skills/tree/main/skills/twitter",
}


def github_link(skill_name: str) -> str:
    if skill_name in GITHUB_OVERRIDES:
        return GITHUB_OVERRIDES[skill_name]
    return f"https://github.com/search?q={skill_name}&type=repositories"


def classify_recommended(skill: dict) -> str:
    category = skill.get("category", "")
    name = skill.get("skill", "")
    if name.startswith("baoyu-"):
        return "baoyu_suite"
    mapping = {
        "automation": "agent_automation",
        "engineering": "engineering_ops",
        "research": "research_intel",
        "industry-finance": "research_intel",
        "design": "design_ui",
        "growth": "content_growth",
        "media": "media_generation",
        "documents": "docs_office",
        "operations": "agent_automation",
        "productivity": "other_integrations",
        "security": "engineering_ops",
    }
    return mapping.get(category, "other_integrations")


def parse_skill_description(skill_md_path: Path) -> str:
    if not skill_md_path.exists():
        return "No description."
    text = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return "No description."

    parts = text.split("---", 2)
    if len(parts) < 3:
        return "No description."

    frontmatter = parts[1]
    try:
        data = yaml.safe_load(frontmatter) or {}
    except Exception:
        return "No description."
    desc = str(data.get("description", "")).strip()
    if not desc:
        return "No description."
    return " ".join(desc.split())


def load_recommended() -> list[dict]:
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return payload.get("skills", [])


def load_default_skills() -> tuple[list[dict], list[dict]]:
    core_dir = OPENCLAW_DEFAULT_PATH / "skills"
    ext_dir = OPENCLAW_DEFAULT_PATH / "extensions"

    core = []
    for p in sorted(core_dir.iterdir(), key=lambda x: x.name):
        if not p.is_dir():
            continue
        core.append(
            {
                "name": p.name,
                "description": parse_skill_description(p / "SKILL.md"),
            }
        )

    ext = []
    for e in sorted(ext_dir.iterdir(), key=lambda x: x.name):
        skills_root = e / "skills"
        if not skills_root.exists():
            continue
        for p in sorted(skills_root.iterdir(), key=lambda x: x.name):
            if not p.is_dir():
                continue
            ext.append(
                {
                    "extension": e.name,
                    "name": p.name,
                    "description": parse_skill_description(p / "SKILL.md"),
                }
            )
    return core, ext


def render() -> str:
    recommended = load_recommended()
    grouped = {k: [] for k in CATEGORY_ORDER}
    for item in recommended:
        grouped[classify_recommended(item)].append(item)

    core_defaults, ext_defaults = load_default_skills()
    total_default = len(core_defaults) + len(ext_defaults)
    total_all = len(recommended) + total_default

    lines = [
        "# Skills Directory",
        "",
        "本目录用于**方便查看**：推荐 skills 在前，OpenClaw 官方默认 skills 单独列出。",
        "",
        f"- 推荐 skills：`{len(recommended)}`",
        f"- OpenClaw 官方默认 skills：`{total_default}`（core `{len(core_defaults)}` + extension `{len(ext_defaults)}`）",
        f"- 可查看总条目：`{total_all}`（满足 80+）",
        "",
        "> 默认 skills 来源：`openclaw` npm 包目录（`skills/` 与 `extensions/*/skills/`），不是本机会话导出。",
        "",
        "## 1) 推荐 skills（优先查看）",
        "",
    ]

    for key in CATEGORY_ORDER:
        items = sorted(grouped[key], key=lambda x: x["skill"])
        lines += [f"### {CATEGORY_LABELS[key]}（{len(items)}）", ""]
        if not items:
            lines += ["- （无）", ""]
            continue
        lines += ["| Skill | 简介 | GitHub |", "|---|---|---|"]
        for item in items:
            skill_name = item["skill"]
            note = item.get("note", "").strip() or "-"
            lines.append(f"| `{skill_name}` | {note} | [repo]({github_link(skill_name)}) |")
        lines += ["", ""]

    lines += [
        "## 2) OpenClaw 官方默认 skills（单独一类）",
        "",
        "### Core defaults",
        "",
        "| Skill | 简介 |",
        "|---|---|",
    ]
    for item in core_defaults:
        lines.append(f"| `{item['name']}` | {item['description']} |")

    lines += ["", "", "### Extension defaults", "", "| Extension | Skill | 简介 |", "|---|---|---|"]
    for item in ext_defaults:
        lines.append(f"| `{item['extension']}` | `{item['name']}` | {item['description']} |")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_PATH.write_text(render(), encoding="utf-8")
    print(OUT_PATH)


if __name__ == "__main__":
    main()

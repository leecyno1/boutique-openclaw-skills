#!/usr/bin/env python3
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
CATALOG_PATH = ROOT / "catalog" / "skills.json"
DOCS_PATH = ROOT / "docs" / "SKILLS_DIRECTORY.md"
CATEGORIES_DIR = ROOT / "categories"
TIERS_DIR = ROOT / "tiers"

MARKER_START = "<!-- SKILLS_INDEX:START -->"
MARKER_END = "<!-- SKILLS_INDEX:END -->"

CATEGORY_CONFIG = [
    {"key": "agent_automation", "label": "Agent/自动化与能力进化", "file": "agent-automation.md", "anchor": "agent-automation"},
    {"key": "engineering_ops", "label": "开发/工程与运维", "file": "engineering-ops.md", "anchor": "engineering-ops"},
    {"key": "research_intel", "label": "搜索/研究/情报", "file": "research-intel.md", "anchor": "research-intel"},
    {"key": "design_ui", "label": "设计/前端/UI", "file": "design-ui.md", "anchor": "design-ui"},
    {"key": "content_growth", "label": "内容/营销/增长", "file": "content-growth.md", "anchor": "content-growth"},
    {"key": "media_generation", "label": "图像/音频/多媒体生成处理", "file": "media-generation.md", "anchor": "media-generation"},
    {"key": "docs_office", "label": "文档/办公生产力", "file": "docs-office.md", "anchor": "docs-office"},
    {"key": "baoyu_suite", "label": "Baoyu 系列内容产出与分发", "file": "baoyu-suite.md", "anchor": "baoyu-suite"},
    {"key": "other_integrations", "label": "其他集成能力", "file": "other-integrations.md", "anchor": "other-integrations"},
]

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


def norm(text: str) -> str:
    return " ".join((text or "").split())


def github_link(skill_name: str) -> str:
    if skill_name in GITHUB_OVERRIDES:
        return GITHUB_OVERRIDES[skill_name]
    return f"https://github.com/search?q={skill_name}&type=repositories"


def parse_skill_description(skill_md_path: Path) -> str:
    if not skill_md_path.exists():
        return "No description."
    text = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return "No description."

    parts = text.split("---", 2)
    if len(parts) < 3:
        return "No description."

    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception:
        return "No description."
    return norm(str(data.get("description", ""))) or "No description."


def classify_recommended(item: dict) -> str:
    category = item.get("category", "")
    skill = item.get("skill", "")
    if skill.startswith("baoyu-"):
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


def load_recommended() -> list[dict]:
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    out = []
    for item in payload.get("skills", []):
        skill = item["skill"]
        out.append(
            {
                "skill": skill,
                "description": norm(item.get("note", "")) or "-",
                "github": github_link(skill),
                "category_key": classify_recommended(item),
            }
        )
    return out


def load_default_tiers() -> dict:
    tiers = {}
    for tier in ["low", "medium", "high"]:
        path = TIERS_DIR / f"{tier}.json"
        if path.exists():
            tiers[tier] = json.loads(path.read_text(encoding="utf-8"))
        else:
            tiers[tier] = {"id": tier, "title": tier, "description": "", "skills": []}
    return tiers


def build_data() -> dict:
    recommended = load_recommended()
    grouped = {cfg["key"]: [] for cfg in CATEGORY_CONFIG}
    for item in recommended:
        grouped[item["category_key"]].append(item)
    for key in grouped:
        grouped[key].sort(key=lambda x: x["skill"])

    tiers = load_default_tiers()
    return {
        "recommended": recommended,
        "grouped_recommended": grouped,
        "tiers": tiers,
    }


def render_table_of_contents(data: dict) -> str:
    items = []
    for cfg in CATEGORY_CONFIG:
        count = len(data["grouped_recommended"][cfg["key"]])
        items.append((f"[{cfg['label']}](#{cfg['anchor']}) ({count})", f"[分类文件](categories/{cfg['file']})"))

    items.append(("[默认 Skills 低档](#default-tier-low)", "[文档](docs/tiers/low.md)"))
    items.append(("[默认 Skills 中档](#default-tier-medium)", "[文档](docs/tiers/medium.md)"))
    items.append(("[默认 Skills 高档](#default-tier-high)", "[文档](docs/tiers/high.md)"))

    rows = []
    for i in range(0, len(items), 2):
        left = items[i]
        right = items[i + 1] if i + 1 < len(items) else ("", "")
        rows.append(f"| {left[0]} | {left[1]} | {right[0]} | {right[1]} |")
    return "\n".join(["| 分类 | 跳转 | 分类 | 跳转 |", "|---|---|---|---|"] + rows)


def render_readme_block(data: dict) -> str:
    rec_total = len(data["recommended"])
    tiers = data["tiers"]
    low_total = len(tiers["low"].get("skills", []))
    medium_total = len(tiers["medium"].get("skills", []))
    high_total = len(tiers["high"].get("skills", []))

    lines = [
        f"- 兼容精选 skills：`{rec_total}`",
        f"- 默认 low / medium / high：`{low_total}` / `{medium_total}` / `{high_total}`",
        f"- 默认 skills 维护源：`skills/default` + `tiers/*.json`",
        "",
        "> 默认 skills 由本仓库维护；安装器仓库只保留 manifest 兼容缓存和同步入口。",
        "",
        "## Table of Contents",
        "",
        render_table_of_contents(data),
        "",
    ]

    for cfg in CATEGORY_CONFIG:
        key = cfg["key"]
        items = data["grouped_recommended"][key]
        lines += [
            f'<a id="{cfg["anchor"]}"></a>',
            f'<details open><summary><h3 style="display:inline">{cfg["label"]}</h3></summary>',
            "",
        ]
        for item in items:
            lines.append(f"- [`{item['skill']}`]({item['github']}) - {item['description']}")
        lines += [
            "",
            f"> **[查看该分类完整列表 →](categories/{cfg['file']})**",
            "</details>",
            "",
        ]

    for tier, anchor, label in [("low", "default-tier-low", "默认 Skills 低档"), ("medium", "default-tier-medium", "默认 Skills 中档"), ("high", "default-tier-high", "默认 Skills 高档")]:
        payload = tiers[tier]
        lines += [
            f'<a id="{anchor}"></a>',
            f'<details open><summary><h3 style="display:inline">{label}</h3></summary>',
            "",
            f"- Skills count: `{len(payload.get('skills', []))}`",
            f"- JSON: [`tiers/{tier}.json`](tiers/{tier}.json)",
            f"- Manual: [`docs/tiers/{tier}.md`](docs/tiers/{tier}.md)",
            "",
        ]
        for item in payload.get("skills", [])[:80]:
            lines.append(f"- `{item['id']}` - {item.get('description', '')}")
        if len(payload.get("skills", [])) > 80:
            lines.append(f"- ... {len(payload.get('skills', [])) - 80} more; see `docs/tiers/{tier}.md`")
        lines += ["", "</details>", ""]
    return "\n".join(lines)


def update_readme(block: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError("README markers not found")
    start_body = start + len(MARKER_START)
    new_text = text[:start_body] + "\n" + block + "\n" + text[end:]
    README_PATH.write_text(new_text, encoding="utf-8")


def write_categories(data: dict) -> None:
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)

    for cfg in CATEGORY_CONFIG:
        items = data["grouped_recommended"][cfg["key"]]
        lines = [
            f"# {cfg['label']}",
            "",
            f"- Skills count: `{len(items)}`",
            "",
            "| Skill | 简介 | GitHub |",
            "|---|---|---|",
        ]
        for item in items:
            lines.append(f"| `{item['skill']}` | {item['description']} | [repo]({item['github']}) |")
        (CATEGORIES_DIR / cfg["file"]).write_text("\n".join(lines) + "\n", encoding="utf-8")



def write_docs_directory(data: dict) -> None:
    rec_total = len(data["recommended"])
    tiers = data["tiers"]
    lines = [
        "# Skills Directory",
        "",
        "该文档与 README 同步，便于离线查阅。",
        "",
        f"- 兼容精选 skills：`{rec_total}`",
        f"- 默认 low：`{len(tiers['low'].get('skills', []))}`",
        f"- 默认 medium：`{len(tiers['medium'].get('skills', []))}`",
        f"- 默认 high：`{len(tiers['high'].get('skills', []))}`",
        "",
        "默认 skills 详细说明请看 `docs/tiers/*.md` 与 `docs/SKILL_MANUALS.md`。",
    ]
    DOCS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    data = build_data()
    write_categories(data)
    write_docs_directory(data)
    update_readme(render_readme_block(data))
    print(README_PATH)
    print(DOCS_PATH)
    print(CATEGORIES_DIR)


if __name__ == "__main__":
    main()

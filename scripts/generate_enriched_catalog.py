#!/usr/bin/env python3
"""Generate enriched skill indexes, standard bundle, and README sections."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"
ORIGIN_OVERRIDES = ROOT / "catalog" / "native-origin-overrides.json"
PRESETS_DIR = ROOT / "catalog" / "presets"
ENRICHED_PATH = ROOT / "catalog" / "skills.enriched.json"
STANDARD_BUNDLE_PATH = ROOT / "catalog" / "standard-bundle.json"
HORIZONTAL_PATH = ROOT / "docs" / "generated" / "horizontal-index.md"
TYPE_PATH = ROOT / "docs" / "generated" / "type-index.md"
DEPENDENCY_PATH = ROOT / "docs" / "generated" / "dependency-index.md"
SCORING_PATH = ROOT / "docs" / "generated" / "scoring-model.md"
README_PATH = ROOT / "README.md"
MARKER_START = "<!-- SKILLS_INDEX:START -->"
MARKER_END = "<!-- SKILLS_INDEX:END -->"

TODAY = date.today().isoformat()
MIRROR_PATTERN = re.compile(r"leecyno1/(?:auto-install-Openclaw|boutique-openclaw-skills)", re.I)

CATEGORY_LABELS = {
    "core-agent": "核心 Agent 能力",
    "search-research": "搜索 / 研究 / 情报",
    "browser-automation": "浏览器 / 自动化",
    "coding-devtools": "编程 / 工程工具",
    "data-analysis": "数据分析",
    "docs-office": "文档 / 办公",
    "design-ui": "设计 / UI",
    "media-generation": "媒体生成 / 处理",
    "writing-content": "写作 / 内容",
    "marketing-growth": "营销 / 增长",
    "finance-trading": "金融 / 交易",
    "legal-compliance": "法律 / 合规 / 税务",
    "productivity-pkm": "效率 / 知识管理",
    "communication": "通信 / 社交集成",
    "devops-cloud": "DevOps / 云 / 数据库",
    "security-audit": "安全 / 审计",
    "local-macos": "本地 macOS / 桌面",
    "agent-orchestration": "多 Agent / 自动调度",
    "commerce-ops": "商业运营",
    "education-learning": "教育 / 学习",
}

CATEGORY_KEYWORDS = [
    ("finance-trading", ["stock", "trade", "trader", "market", "finance", "earnings", "dividend", "etf", "portfolio", "valuation", "screener", "macro", "alphaear", "canslim", "vcp", "ftd", "options", "liquidity", "breadth", "funda", "yfinance", "akshare", "finviz"]),
    ("legal-compliance", ["tax", "compliance", "legal", "accounting"]),
    ("browser-automation", ["browser", "chrome-devtools", "playwright", "web automation"]),
    ("search-research", ["search", "news", "reader", "radar", "research", "url-to-markdown", "notebooklm", "yc-reader", "telegram-reader", "twitter-reader", "linkedin-reader", "discord-reader"]),
    ("coding-devtools", ["dev", "github", "mcp", "shell", "database", "prisma", "frontend", "fullstack", "flutter", "android", "ios", "react-native", "shader", "skill-creator", "writing-skills"]),
    ("data-analysis", ["data", "analyst", "quality", "reconciliation", "xlsx", "chart"]),
    ("docs-office", ["docx", "pdf", "pptx", "xlsx", "paperless", "meeting", "calendar"]),
    ("design-ui", ["design", "ui", "generative-ui", "animation", "visualizer", "brand", "logo"]),
    ("media-generation", ["image", "music", "video", "gif", "multimodal", "vision", "media", "compress", "sings"]),
    ("marketing-growth", ["marketing", "social", "xiaohongshu", "zhihu", "weibo", "content-strategy", "producthunt", "seo"]),
    ("writing-content", ["writing", "translate", "markdown", "article", "post", "draft", "baoyu", "dasheng", "prose"]),
    ("communication", ["agentmail", "mail", "slack", "telegram", "discord", "lark", "feishu", "whatsapp"]),
    ("productivity-pkm", ["todo", "task", "things", "obsidian", "notebook", "calendar", "reminder", "notes"]),
    ("security-audit", ["security", "audit", "reviewer", "danger"]),
    ("agent-orchestration", ["agent", "subagent", "proactive", "cron", "reflection", "superpowers", "planning", "verification", "brainstorming", "capability"]),
    ("devops-cloud", ["database", "cloud", "deploy", "ops", "sql", "server"]),
]

L1 = {
    "agent-browser", "brainstorming", "chrome-devtools-mcp", "find-skills", "github",
    "mcp-builder", "model-usage", "planning-with-files", "shell", "skill-creator",
    "skill-security-auditor", "subagent-driven-development", "task", "todo",
    "url-to-markdown", "using-superpowers", "verification-before-completion", "web-search",
    "writing-skills", "weather",
}
L2_HINTS = {
    "data-analyst", "docx", "xlsx", "pptx", "pdf", "frontend-dev", "fullstack-dev",
    "database", "finance-data", "media-downloader", "ai-image-generation", "news-radar",
    "tavily-search", "multi-search-engine", "notebooklm-skill", "content-strategy",
    "social-content", "vision-analysis", "openclaw-cron-setup", "proactive-agent",
    "self-improving-agent-cn", "reflection", "writing-plans",
}

CONFLICT_GROUP_RULES = [
    ("web-search", ["web-search", "tavily-search", "brave-search", "multi-search-engine", "minimax-web-search"]),
    ("browser-automation", ["agent-browser", "chrome-devtools-mcp"]),
    ("document-docx", ["docx", "minimax-docx"]),
    ("document-pdf", ["pdf", "nano-pdf", "minimax-pdf"]),
    ("document-pptx", ["pptx", "pptx-generator"]),
    ("spreadsheet-xlsx", ["xlsx", "minimax-xlsx"]),
    ("image-generation", ["ai-image-generation", "gemini-image-service", "baoyu-image-gen"]),
    ("music-generation", ["ai-music-generation", "ai-music-prompts", "minimax-music-gen"]),
    ("email-agent", ["agentmail", "agentmail-cli", "agentmail-mcp", "agentmail-toolkit"]),
    ("finance-data", ["finance-data", "akshare-stock", "yfinance-data", "funda-data"]),
]

STANDARD_CAPABILITIES = [
    "agent-method", "skill-discovery", "web-search", "url-extraction", "browser-automation",
    "code-hosting", "terminal", "task-tracking", "planning", "verification", "skill-authoring",
    "security-review", "data-analysis", "docs", "spreadsheet", "slides", "pdf", "frontend",
    "fullstack", "database", "mcp", "media-download", "image-generation", "research-news",
    "finance-data", "content-strategy", "writing", "automation-followup", "cost-observability",
    "weather",
]

CAPABILITY_RULES = [
    ("agent-method", ["brainstorming", "using-superpowers"]),
    ("skill-discovery", ["find-skills"]),
    ("web-search", ["tavily-search", "web-search", "multi-search-engine", "minimax-web-search"]),
    ("url-extraction", ["url-to-markdown"]),
    ("browser-automation", ["agent-browser", "chrome-devtools-mcp"]),
    ("code-hosting", ["github"]),
    ("terminal", ["shell"]),
    ("task-tracking", ["todo", "task"]),
    ("planning", ["planning-with-files", "writing-plans"]),
    ("verification", ["verification-before-completion"]),
    ("skill-authoring", ["skill-creator", "writing-skills"]),
    ("security-review", ["skill-security-auditor"]),
    ("data-analysis", ["data-analyst", "data-quality-checker"]),
    ("docs", ["docx", "minimax-docx"]),
    ("spreadsheet", ["xlsx", "minimax-xlsx"]),
    ("slides", ["pptx", "pptx-generator"]),
    ("pdf", ["pdf", "nano-pdf"]),
    ("frontend", ["frontend-dev", "generative-ui"]),
    ("fullstack", ["fullstack-dev"]),
    ("database", ["database"]),
    ("mcp", ["mcp-builder"]),
    ("media-download", ["media-downloader"]),
    ("image-generation", ["ai-image-generation", "gemini-image-service"]),
    ("research-news", ["news-radar", "notebooklm-skill"]),
    ("finance-data", ["finance-data", "yfinance-data", "akshare-stock"]),
    ("content-strategy", ["content-strategy"]),
    ("writing", ["writing-skills", "baoyu-format-markdown"]),
    ("automation-followup", ["proactive-agent", "openclaw-cron-setup"]),
    ("cost-observability", ["model-usage"]),
    ("weather", ["weather"]),
]

API_KEY_PATTERNS = {
    "AGENTMAIL_API_KEY": ["agentmail"],
    "TAVILY_API_KEY": ["tavily"],
    "BRAVE_API_KEY": ["brave"],
    "GITHUB_TOKEN": ["github"],
    "GH_TOKEN": ["github"],
    "GEMINI_API_KEY": ["gemini"],
    "FMP_API_KEY": ["fmp", "earnings-calendar", "economic-calendar"],
    "OPENAI_API_KEY": ["openai", "ai-image", "inference"],
}

TOOL_PATTERNS = {
    "browser": ["browser", "chrome", "web"],
    "mcp": ["mcp"],
    "node": ["frontend", "fullstack", "react", "pptx", "xlsx"],
    "python": ["data", "finance", "stock", "analyst", "yfinance", "akshare"],
    "ffmpeg": ["video", "gif", "music", "audio"],
    "gh": ["github"],
}


def norm(text: str) -> str:
    return " ".join((text or "").split())


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(skill_id: str) -> dict[str, Any]:
    path = ROOT / "skills" / "default" / skill_id / "SKILL.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def dedupe_default_skills() -> list[dict[str, Any]]:
    data = load_json(DEFAULT_CATALOG, {})
    by_id: dict[str, dict[str, Any]] = {}
    tier_membership: dict[str, list[str]] = defaultdict(list)
    for tier in ("low", "medium", "high"):
        for item in data.get("tiers", {}).get(tier, {}).get("skills", []):
            skill_id = item["id"]
            by_id.setdefault(skill_id, dict(item))
            tier_membership[skill_id].append(tier)
    for skill_id, item in by_id.items():
        item["install_tiers"] = tier_membership[skill_id]
    return [by_id[k] for k in sorted(by_id)]


def detect_native_origin(skill_id: str, item: dict[str, Any], overrides: dict[str, str], preset_exclusions: set[str]) -> dict[str, Any]:
    mirror = item.get("source", "")
    if skill_id in preset_exclusions:
        return {
            "origin_url": None,
            "origin_type": "agent-preset",
            "origin_confidence": "agent_preset_excluded",
            "origin_verified_at": TODAY,
            "mirror_source_url": mirror,
            "needs_origin_review": False,
            "excluded_reason": "Provided by target agent runtime; not installed from this registry.",
        }
    if skill_id in overrides:
        url = overrides[skill_id]
        origin_type = "github" if "github.com" in url else "clawhub" if "claw" in url.lower() else "website"
        return {
            "origin_url": url,
            "origin_type": origin_type,
            "origin_confidence": "verified_override",
            "origin_verified_at": TODAY,
            "mirror_source_url": mirror,
            "needs_origin_review": False,
        }
    local_urls = extract_local_urls(skill_id)
    if local_urls:
        url = local_urls[0]
        return {
            "origin_url": url,
            "origin_type": "github" if "github.com" in url else "website",
            "origin_confidence": "local_reference",
            "origin_verified_at": TODAY,
            "mirror_source_url": mirror,
            "needs_origin_review": False,
        }
    return {
        "origin_url": None,
        "origin_type": None,
        "origin_confidence": "missing",
        "origin_verified_at": None,
        "mirror_source_url": mirror,
        "needs_origin_review": True,
        "source_is_mirror": bool(MIRROR_PATTERN.search(mirror)),
    }


def extract_local_urls(skill_id: str) -> list[str]:
    base = ROOT / "skills" / "default" / skill_id
    urls: list[str] = []
    for name in ("SKILL.md", "README.md", "GUIDE.md"):
        path = base / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for url in re.findall(r"https://[^\s)\]>'\"]+", text):
            clean = url.rstrip(".,;:")
            if not any(host in clean for host in ("github.com", "skills.h")):
                continue
            lower = clean.lower()
            if any(bad in lower for bad in ("google.com/search", "api/skills/bitcoin-tracker", "suspicious-skill", "example", "localhost", "{", "}", "`")):
                continue
            if "github.com" in lower and not any(token in lower for token in (skill_id.lower(), "/skills/", "minimax-ai/skills", "anthropics/skills", "baoyu-skills", "opc-skills")):
                continue
            urls.append(clean)
    unique = []
    for url in urls:
        if url not in unique and "leecyno1/auto-install-Openclaw" not in url:
            unique.append(url)
    return unique


def classify_category(skill_id: str, description: str) -> str:
    haystack = f"{skill_id} {description}".lower()
    if skill_id in L1 or skill_id in {"task", "todo", "model-usage"}:
        return "core-agent"
    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "commerce-ops"


def classify_horizontal(skill_id: str, category: str, origin_confidence: str) -> str:
    if skill_id in L1:
        return "L1 Foundation"
    if skill_id in L2_HINTS or category in {"coding-devtools", "data-analysis", "docs-office", "search-research", "design-ui"}:
        return "L2 Professional"
    if origin_confidence == "missing":
        return "L3 Specialist"
    return "L3 Specialist"


def infer_dependencies(skill_id: str, description: str, existing_keys: list[str]) -> dict[str, Any]:
    haystack = f"{skill_id} {description}".lower()
    api_keys = list(existing_keys)
    for key, patterns in API_KEY_PATTERNS.items():
        if any(pattern in haystack for pattern in patterns) and key not in api_keys:
            api_keys.append(key)
    tools = []
    for tool, patterns in TOOL_PATTERNS.items():
        if any(pattern in haystack for pattern in patterns):
            tools.append(tool)
    if api_keys:
        access_mode = "api-key"
    elif "mcp" in tools:
        access_mode = "mcp-required"
    elif "browser" in tools:
        access_mode = "browser-required"
    else:
        access_mode = "direct"
    runtime = "online" if api_keys or any(word in haystack for word in ["web", "api", "search", "reader", "news"]) else "offline"
    return {
        "requires_api_keys": bool(api_keys),
        "api_keys": sorted(api_keys),
        "required_tools": sorted(set(tools)),
        "access_mode": access_mode,
        "runtime": runtime,
    }


def conflict_group(skill_id: str, category: str) -> str:
    for group, ids in CONFLICT_GROUP_RULES:
        if skill_id in ids:
            return group
    if category == "finance-trading":
        return f"finance-specialist:{skill_id}"
    return skill_id


def risk_level(skill_id: str, deps: dict[str, Any], category: str) -> str:
    if any(token in skill_id for token in ["danger", "shell"]):
        return "high"
    if deps["access_mode"] in {"api-key", "mcp-required", "browser-required"}:
        return "medium"
    if category in {"finance-trading", "legal-compliance", "devops-cloud"}:
        return "medium"
    return "low"


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    score = 30
    confidence = item["origin"]["origin_confidence"]
    if confidence == "verified_override":
        score += 25
    elif confidence == "local_reference":
        score += 15
    else:
        score -= 20
    if item["horizontal_tier"].startswith("L1"):
        score += 20
    elif item["horizontal_tier"].startswith("L2"):
        score += 12
    else:
        score += 5
    if item["risk_level"] == "low":
        score += 10
    elif item["risk_level"] == "medium":
        score += 4
    else:
        score -= 8
    if item["dependencies"]["access_mode"] == "direct":
        score += 8
    elif item["dependencies"]["access_mode"] in {"browser-required", "mcp-required"}:
        score += 3
    if item["description"] and item["description"] != "No description.":
        score += 7
    if item["preset_excluded"]:
        score -= 100
    if confidence == "missing":
        score = min(score, 45)
    score = max(0, min(100, score))
    stars = 5 if score >= 90 else 4 if score >= 75 else 3 if score >= 60 else 2 if score >= 40 else 1
    return {"score": score, "stars": stars, "rating_label": "★" * stars + "☆" * (5 - stars)}


def load_preset_exclusions() -> set[str]:
    excluded = set()
    for path in PRESETS_DIR.glob("*.json"):
        data = load_json(path, {})
        excluded.update(data.get("preset_skills", []))
    return excluded


def build_enriched() -> dict[str, Any]:
    overrides = load_json(ORIGIN_OVERRIDES, {})
    preset_exclusions = load_preset_exclusions()
    skills = []
    for base in dedupe_default_skills():
        skill_id = base["id"]
        frontmatter = parse_frontmatter(skill_id)
        description = norm(frontmatter.get("description") or base.get("description") or "No description.")
        origin = detect_native_origin(skill_id, base, overrides, preset_exclusions)
        category = classify_category(skill_id, description)
        horizontal = classify_horizontal(skill_id, category, origin["origin_confidence"])
        deps = infer_dependencies(skill_id, description, base.get("api_keys", []))
        item = {
            "id": skill_id,
            "name": base.get("name", skill_id),
            "description": description,
            "manual": base.get("manual"),
            "manual_url": base.get("manual_url"),
            "install_tiers": base.get("install_tiers", []),
            "origin": origin,
            "horizontal_tier": horizontal,
            "primary_category": category,
            "category_label": CATEGORY_LABELS[category],
            "tags": sorted(set([category, horizontal.split()[0].lower(), deps["access_mode"], deps["runtime"]])),
            "dependencies": deps,
            "risk_level": risk_level(skill_id, deps, category),
            "conflict_group": conflict_group(skill_id, category),
            "preset_excluded": skill_id in preset_exclusions,
        }
        item["rating"] = score_item(item)
        skills.append(item)
    return {
        "schema_version": "2026.05.17",
        "generated_at": TODAY,
        "source_catalog": "catalog/default-skills.json",
        "policy": {
            "native_origin_required": True,
            "mirror_sources_are_not_native": True,
            "missing_origin_max_stars": 2,
            "standard_bundle_max_skills": 30,
            "preset_excluded_agents": [p.stem for p in sorted(PRESETS_DIR.glob("*.json"))],
        },
        "summary": summarize(skills),
        "skills": sorted(skills, key=lambda x: (-x["rating"]["score"], x["id"])),
    }


def summarize(skills: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "skills": len(skills),
        "native_origin_verified_or_referenced": sum(not s["origin"].get("needs_origin_review") and not s.get("preset_excluded") for s in skills),
        "native_origin_excluded_presets": sum(s.get("preset_excluded") for s in skills),
        "needs_origin_review": sum(s["origin"].get("needs_origin_review", False) for s in skills),
        "preset_excluded": sum(s["preset_excluded"] for s in skills),
        "by_horizontal_tier": dict(sorted(counter(skills, "horizontal_tier").items())),
        "by_category": dict(sorted(counter(skills, "primary_category").items())),
        "by_access_mode": dict(sorted(counter(skills, lambda s: s["dependencies"]["access_mode"]).items())),
        "by_stars": dict(sorted(counter(skills, lambda s: f"{s['rating']['stars']}★").items())),
    }


def counter(skills: list[dict[str, Any]], key: str | Any) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for item in skills:
        value = item[key] if isinstance(key, str) else key(item)
        out[str(value)] += 1
    return dict(out)


def build_standard_bundle(enriched: dict[str, Any]) -> dict[str, Any]:
    by_id = {s["id"]: s for s in enriched["skills"] if not s["preset_excluded"]}
    selected = []
    selected_conflicts = set()
    for capability, candidates in CAPABILITY_RULES:
        choices = [by_id[c] for c in candidates if c in by_id]
        choices = [c for c in choices if c["conflict_group"] not in selected_conflicts]
        if not choices:
            continue
        best = sorted(choices, key=lambda s: (-s["rating"]["score"], risk_sort(s["risk_level"]), s["id"]))[0]
        selected.append({
            "capability": capability,
            "skill": best["id"],
            "category": best["primary_category"],
            "stars": best["rating"]["stars"],
            "score": best["rating"]["score"],
            "access_mode": best["dependencies"]["access_mode"],
            "conflict_group": best["conflict_group"],
            "origin_url": best["origin"].get("origin_url"),
            "note": best["description"],
        })
        selected_conflicts.add(best["conflict_group"])
        if len(selected) >= 30:
            break
    return {
        "schema_version": enriched["schema_version"],
        "generated_at": TODAY,
        "max_skills": 30,
        "dedupe_rule": "one highest-scored skill per capability and conflict_group; Open/Hermes preset skills excluded",
        "skills": selected,
    }


def risk_sort(risk: str) -> int:
    return {"low": 0, "medium": 1, "high": 2}.get(risk, 3)


def md_link(url: str | None, label: str = "origin") -> str:
    return f"[{label}]({url})" if url else "待补"


def render_standard_table(bundle: dict[str, Any]) -> str:
    lines = [
        "## 标准技能配置组（≤30，无重复能力）",
        "",
        "安装原则：每个能力只选择一个评分最高且未被 Open/Hermes 预置的 skill，避免重复安装导致冲突或 token 浪费。",
        "",
        "```bash",
        "./scripts/install-standard-bundle.sh --dry-run",
        "./scripts/install-standard-bundle.sh",
        "```",
        "",
        "| 能力 | 推荐 Skill | 星级 | 使用条件 | 原生来源 |",
        "|---|---|---:|---|---|",
    ]
    for item in bundle["skills"]:
        lines.append(
            f"| `{item['capability']}` | `{item['skill']}` | {item['stars']}★ | `{item['access_mode']}` | {md_link(item['origin_url'])} |"
        )
    return "\n".join(lines)


def render_summary(enriched: dict[str, Any], bundle: dict[str, Any]) -> str:
    summary = enriched["summary"]
    lines = [
        "- 默认 skill 去重数：`{}`".format(summary["skills"]),
        "- 已有原生来源或本地来源线索：`{}`".format(summary["native_origin_verified_or_referenced"]),
        "- 仍需人工确认原生来源：`{}`".format(summary["needs_origin_review"]),
        "- Open/Hermes 预置排除：`{}`".format(summary["preset_excluded"]),
        "- 标准配置组：`{}` / `30`".format(len(bundle["skills"])),
        "",
        "> `source` 中的安装器仓库路径仅视为镜像来源；`origin.origin_url` 才是一手原生来源。缺失原生来源的 skill 最高只能获得 2★。",
    ]
    return "\n".join(lines)


def render_horizontal_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["horizontal_tier"]].append(item)
    lines = ["# 横向分级索引", "", "| 层级 | 定义 | 数量 |", "|---|---|---:|"]
    definitions = {
        "L1 Foundation": "跨 Agent、跨领域、高通用、低冲突的基础能力",
        "L2 Professional": "常用专业工作流，适合多数生产环境按需安装",
        "L3 Specialist": "领域强绑定、依赖明显或适合专家场景的能力",
    }
    for tier in ["L1 Foundation", "L2 Professional", "L3 Specialist"]:
        lines.append(f"| `{tier}` | {definitions[tier]} | {len(grouped[tier])} |")
    for tier in ["L1 Foundation", "L2 Professional", "L3 Specialist"]:
        lines += ["", f"## {tier}", "", "| Skill | 类型 | 星级 | 使用条件 | 原生来源 |", "|---|---|---:|---|---|"]
        for item in sorted(grouped[tier], key=lambda s: (-s["rating"]["score"], s["id"])):
            lines.append(f"| `{item['id']}` | {item['category_label']} | {item['rating']['stars']}★ | `{item['dependencies']['access_mode']}` | {md_link(item['origin']['origin_url'])} |")
    return "\n".join(lines) + "\n"


def render_type_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["primary_category"]].append(item)
    lines = ["# 纵向类型索引", "", "| 类型 | 数量 |", "|---|---:|"]
    for category, label in CATEGORY_LABELS.items():
        lines.append(f"| {label} (`{category}`) | {len(grouped[category])} |")
    for category, label in CATEGORY_LABELS.items():
        if not grouped[category]:
            continue
        lines += ["", f"## {label}", "", "| Skill | 横向层级 | 星级 | 标签 |", "|---|---|---:|---|"]
        for item in sorted(grouped[category], key=lambda s: (-s["rating"]["score"], s["id"])):
            lines.append(f"| `{item['id']}` | `{item['horizontal_tier']}` | {item['rating']['stars']}★ | {', '.join(f'`{tag}`' for tag in item['tags'])} |")
    return "\n".join(lines) + "\n"


def render_dependency_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["dependencies"]["access_mode"]].append(item)
    lines = ["# 使用条件索引", "", "| 使用条件 | 数量 |", "|---|---:|"]
    for mode in sorted(grouped):
        lines.append(f"| `{mode}` | {len(grouped[mode])} |")
    for mode in sorted(grouped):
        lines += ["", f"## {mode}", "", "| Skill | API Key | Tools | 风险 |", "|---|---|---|---|"]
        for item in sorted(grouped[mode], key=lambda s: (-s["rating"]["score"], s["id"])):
            keys = ", ".join(f"`{k}`" for k in item["dependencies"]["api_keys"]) or "无"
            tools = ", ".join(f"`{t}`" for t in item["dependencies"]["required_tools"]) or "无"
            lines.append(f"| `{item['id']}` | {keys} | {tools} | `{item['risk_level']}` |")
    return "\n".join(lines) + "\n"


def render_scoring_model() -> str:
    return """# 评分体系

五星标签由 100 分综合评分映射而来：

| 分数 | 星级 |
|---:|---:|
| 90-100 | 5★ |
| 75-89 | 4★ |
| 60-74 | 3★ |
| 40-59 | 2★ |
| 0-39 | 1★ |

## 当前评分因子

| 因子 | 权重/规则 |
|---|---|
| 原生来源可信度 | verified override +25，本地引用 +15，缺失 -20 |
| 横向通用性 | L1 +20，L2 +12，L3 +5 |
| 风险 | low +10，medium +4，high -8 |
| 使用门槛 | direct +8，browser/mcp +3 |
| 文档描述 | 有描述 +7 |
| 预置排除 | Open/Hermes 已预置的 skill 不进入标准配置组 |

## 后续月评增强

月评任务应补充 GitHub stars/forks/release、ClawHub/CL.Up rating/downloads、skills.h 热度与更新时间。没有可验证原生来源的 skill，即使本地可用，最高只能评为 2★。
"""


def render_readme_block(enriched: dict[str, Any], bundle: dict[str, Any]) -> str:
    top_foundation = [s for s in enriched["skills"] if s["horizontal_tier"] == "L1 Foundation"][:15]
    top_missing = [s for s in enriched["skills"] if s["origin"].get("needs_origin_review")][:20]
    lines = [
        "## Registry Snapshot",
        "",
        render_summary(enriched, bundle),
        "",
        render_standard_table(bundle),
        "",
        "## 双索引",
        "",
        "| 索引 | 说明 | 文件 |",
        "|---|---|---|",
        "| 横向分级 | L1 Foundation / L2 Professional / L3 Specialist | [`docs/generated/horizontal-index.md`](docs/generated/horizontal-index.md) |",
        "| 纵向类型 | 按用途分类，如 coding、design、finance、writing 等 | [`docs/generated/type-index.md`](docs/generated/type-index.md) |",
        "| 使用条件 | API key、额外 tools、运行方式、风险 | [`docs/generated/dependency-index.md`](docs/generated/dependency-index.md) |",
        "| 评分体系 | 五星评分规则和月评增强方向 | [`docs/generated/scoring-model.md`](docs/generated/scoring-model.md) |",
        "",
        "## L1 Foundation Top Skills",
        "",
        "| Skill | 类型 | 星级 | 原生来源 |",
        "|---|---|---:|---|",
    ]
    for item in top_foundation:
        lines.append(f"| `{item['id']}` | {item['category_label']} | {item['rating']['stars']}★ | {md_link(item['origin']['origin_url'])} |")
    lines += [
        "",
        "## 原生来源待补清单（前 20）",
        "",
        "这些 skill 当前只有镜像来源或缺少一手来源，月评时需要优先补齐。",
        "",
        "| Skill | 类型 | 镜像来源 |",
        "|---|---|---|",
    ]
    for item in top_missing:
        mirror = item["origin"].get("mirror_source_url") or ""
        lines.append(f"| `{item['id']}` | {item['category_label']} | {md_link(mirror, 'mirror')} |")
    return "\n".join(lines)


def update_readme(block: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError("README markers not found")
    new_text = text[: start + len(MARKER_START)] + "\n" + block + "\n" + text[end:]
    README_PATH.write_text(new_text, encoding="utf-8")


def write_outputs(enriched: dict[str, Any], bundle: dict[str, Any]) -> None:
    ENRICHED_PATH.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STANDARD_BUNDLE_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    HORIZONTAL_PATH.write_text(render_horizontal_index(enriched["skills"]), encoding="utf-8")
    TYPE_PATH.write_text(render_type_index(enriched["skills"]), encoding="utf-8")
    DEPENDENCY_PATH.write_text(render_dependency_index(enriched["skills"]), encoding="utf-8")
    SCORING_PATH.write_text(render_scoring_model(), encoding="utf-8")
    update_readme(render_readme_block(enriched, bundle))


def main() -> int:
    enriched = build_enriched()
    bundle = build_standard_bundle(enriched)
    write_outputs(enriched, bundle)
    print(json.dumps({"summary": enriched["summary"], "standard_bundle": len(bundle["skills"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

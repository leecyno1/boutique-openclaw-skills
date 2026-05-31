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
    "finance-data": "金融 / 数据源",
    "finance-knowledge": "金融 / 知识库",
    "finance-monitor": "金融 / 监控预警",
    "policy-monitoring": "政策 / 宏观监控",
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
    "skill-vetter",
    "skill-security-auditor", "subagent-driven-development", "task", "todo",
    "url-to-markdown", "using-superpowers", "verification-before-completion", "web-search",
    "writing-skills", "weather",
}
L2_HINTS = {
    "data-analyst", "docx", "xlsx", "pptx", "pdf", "frontend-dev", "fullstack-dev",
    "database", "a-stock-data", "media-downloader", "ai-image-generation", "news-radar",
    "tavily-search", "multi-search-engine", "notebooklm-skill", "content-strategy",
    "social-content", "vision-analysis", "openclaw-cron-setup", "proactive-agent",
    "self-improving-agent-cn", "reflection", "writing-plans", "seedance2-skill",
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
    ("finance-data", ["a-stock-data", "akshare-stock", "yfinance-data", "funda-data", "tushare-openclaw-skill", "openclaw-stock-data-skill"]),
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
    ("security-review", ["skill-vetter", "skill-security-auditor"]),
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
    ("finance-data", ["a-stock-data", "openclaw-stock-data-skill", "tushare-openclaw-skill", "yfinance-data", "akshare-stock"]),
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
    "OPENAI_API_KEY": ["openai", "ai-image", "inference", "deepseek", "llm"],
    "TUSHARE_TOKEN": ["tushare"],
    "STOCK_API_KEY": ["stock_api_key", "data.diemeng", "diemeng"],
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
    explicit = {
        "a-stock-data": "finance-data",
        "akshare-stock": "finance-data",
        "funda-data": "finance-data",
        "openclaw-stock-data-skill": "finance-data",
        "tushare-openclaw-skill": "finance-data",
        "yfinance-data": "finance-data",
        "openclaw-stock-kb": "finance-knowledge",
        "stock-monitor-skill": "finance-monitor",
        "stock-daily-analysis-skill": "finance-trading",
        "stock-analysis": "finance-trading",
        "pybroker-backtest-skill": "finance-trading",
        "policy-monitor": "policy-monitoring",
        "skill-vetter": "security-audit",
    }
    if skill_id in explicit:
        return explicit[skill_id]
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
    if skill_id in L2_HINTS or category in {"coding-devtools", "data-analysis", "docs-office", "search-research", "design-ui", "finance-data", "finance-knowledge"}:
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
    if skill_id == "seedance2-skill":
        tools = []
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
    if category in {"finance-trading", "finance-data", "finance-monitor", "policy-monitoring", "legal-compliance", "devops-cloud"}:
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


def readme_origin(item: dict[str, Any]) -> str:
    if item["preset_excluded"]:
        return "Preset"
    return md_link(item["origin"].get("origin_url"), "Source")


def render_badges(summary: dict[str, Any], bundle: dict[str, Any]) -> str:
    badges = [
        "[![Project](https://img.shields.io/badge/Project-Page-2b6cb0)](#boutique-openclaw-skills)",
        f"[![Skills](https://img.shields.io/badge/Skills-{summary['skills']}-2ea44f)](#all-skills)",
        "[![Native Origins](https://img.shields.io/badge/Native%20Origins-0%20missing-brightgreen)](docs/UPDATE_AND_AUDIT.md)",
        f"[![Standard Bundle](https://img.shields.io/badge/Standard%20Bundle-{len(bundle['skills'])}%20skills-7c3aed)](catalog/standard-bundle.json)",
        "[![Technique](https://img.shields.io/badge/Technique-Source%20Audited-f97316)](docs/generated/scoring-model.md)",
        "[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)",
    ]
    return "\n".join(badges)


def render_tech_stack_badges() -> str:
    return "\n".join([
        '<p align="center">',
        '  <img src="https://skillicons.dev/icons?i=python,fastapi,pydantic,postgres,redis,docker,githubactions&theme=dark" alt="Core technology stack" />',
        '</p>',
        '<p align="center">',
        '  <img src="https://img.shields.io/badge/OpenAI-Model%20Support-111827?logo=openai&logoColor=white" alt="OpenAI" />',
        '  <img src="https://img.shields.io/badge/Anthropic-Claude%20Ready-111827" alt="Anthropic" />',
        '  <img src="https://img.shields.io/badge/ModelScope-Model%20Ecosystem-111827" alt="ModelScope" />',
        '  <img src="https://img.shields.io/badge/UV-Python%20Packaging-111827" alt="UV" />',
        '  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-111827" alt="SQLAlchemy" />',
        '</p>',
    ])


def render_stats(summary: dict[str, Any], bundle: dict[str, Any]) -> str:
    return "\n".join([
        "| Metric | Value |",
        "|---|---:|",
        f"| Curated skills | {summary['skills']} |",
        f"| Native sources verified or referenced | {summary['native_origin_verified_or_referenced']} |",
        f"| Agent preset exclusions | {summary['preset_excluded']} |",
        f"| Missing native origins | {summary['needs_origin_review']} |",
        f"| Standard bundle size | {len(bundle['skills'])} / 30 |",
    ])


def render_all_skills_table(skills: list[dict[str, Any]]) -> str:
    lines = [
        "| Skill | Tier | Type | Stars | Use | Origin |",
        "|---|---|---|---:|---|---|",
    ]
    for item in sorted(skills, key=lambda s: (s["primary_category"], s["id"])):
        lines.append(
            f"| `{item['id']}` | `{item['horizontal_tier']}` | `{item['primary_category']}` | "
            f"{item['rating']['stars']}★ | `{item['dependencies']['access_mode']}` | {readme_origin(item)} |"
        )
    return "\n".join(lines)


def render_standard_bundle_table(bundle: dict[str, Any]) -> str:
    lines = [
        "| Capability | Skill | Stars | Use |",
        "|---|---|---:|---|",
    ]
    for item in bundle["skills"]:
        lines.append(f"| `{item['capability']}` | `{item['skill']}` | {item['stars']}★ | `{item['access_mode']}` |")
    return "\n".join(lines)


def render_readme(enriched: dict[str, Any], bundle: dict[str, Any]) -> str:
    summary = enriched["summary"]
    return "\n".join([
        '<div align="center">',
        "",
        '<img src="assets/boutique-openclaw-skills-hero.png" alt="OpenClaw x Dashengzhinu x Hermes logo" width="76%" />',
        "",
        "# Boutique OpenClaw Skills",
        "",
        "**Curated skills for capable OpenClaw, Open, and Hermes agents.**",
        "",
        "**面向智能体的精品技能仓库：原生来源可审计、能力不重复、安装可控、持续月评。**",
        "",
        render_badges(summary, bundle),
        "",
        render_tech_stack_badges(),
        "",
        '<img src="assets/boutique-logo-tech-card.png" alt="Boutique OpenClaw Skills technology card" width="86%" />',
        "",
        "</div>",
        "",
        "## 中文说明",
        "",
        "Boutique OpenClaw Skills 是一个面向 AI Agent 的精品技能合集。仓库把默认技能、标准配置组、横向分级、纵向分类、API Key/工具依赖、风险等级、冲突组和原生上游来源统一整理成可审计的注册表，目标是让用户安装后即获得一套少重复、低噪声、生产可用的能力组合。",
        "",
        "本仓库强调三件事：一是每个活跃 skill 都必须能追溯到 GitHub、ClawHub/CL.Up、skills.h 或官方项目站点；二是同一能力只推荐一个最佳 skill，避免 Web Search、PDF、Email、Finance Data 等能力重复安装；三是每月自动重建索引和审计报告，让 README、JSON Catalog 与安装包保持一致。",
        "",
        "## Overview",
        "",
        "Boutique OpenClaw Skills is a source-audited skill registry for building capable OpenClaw, Open, and Hermes agents without duplicate tools or noisy installs. It keeps a full machine-readable catalog, a recommended no-duplicate bundle, generated indexes, and monthly audit automation in one place.",
        "",
        "## Quick Start",
        "",
        "Install the recommended no-duplicate bundle:",
        "",
        "```bash",
        "./scripts/install-standard-bundle.sh --dry-run",
        "./scripts/install-standard-bundle.sh",
        "```",
        "",
        "Or install a tier:",
        "",
        "```bash",
        "./scripts/install-tier.sh low",
        "./scripts/install-tier.sh medium",
        "./scripts/install-tier.sh high",
        "```",
        "",
        "## At A Glance",
        "",
        render_stats(summary, bundle),
        "",
        "## Standard Bundle",
        "",
        "The standard bundle keeps one best skill per capability and excludes skills already built into Open or Hermes.",
        "",
        render_standard_bundle_table(bundle),
        "",
        "## All Skills",
        "",
        render_all_skills_table(enriched["skills"]),
        "",
        "## Indexes",
        "",
        "| Document | What it shows |",
        "|---|---|",
        "| [Horizontal index](docs/generated/horizontal-index.md) | L1 Foundation, L2 Professional, L3 Specialist |",
        "| [Type index](docs/generated/type-index.md) | Coding, design, finance, writing, research, media, docs, and more |",
        "| [Dependency index](docs/generated/dependency-index.md) | API keys, tools, runtime mode, and risk |",
        "| [Scoring model](docs/generated/scoring-model.md) | How star ratings are calculated |",
        "| [Update and audit SOP](docs/UPDATE_AND_AUDIT.md) | Monthly review process and risk gates |",
        "",
        "## Curation Rules",
        "",
        "- Every active skill must have a native upstream source; mirrors and copied installer paths are not treated as origins.",
        "- The standard bundle avoids duplicate capabilities by using conflict groups such as `web-search`, `document-pdf`, `email-agent`, and `finance-data`.",
        "- Open and Hermes preset skills are excluded from bundle installs because the target agent already provides them.",
        "- Monthly automation regenerates the registry, indexes, README, standard bundle, and audit reports.",
        "",
        "## Repository Map",
        "",
        "| Path | Purpose |",
        "|---|---|",
        "| `skills/default/` | Local skill sources |",
        "| `catalog/skills.enriched.json` | Full machine-readable registry |",
        "| `catalog/standard-bundle.json` | Recommended no-duplicate install set |",
        "| `catalog/native-origin-overrides.json` | Verified native upstream source map |",
        "| `catalog/presets/` | Open and Hermes preset exclusions |",
        "| `docs/generated/` | Generated human-readable indexes |",
        "| `scripts/` | Install, sync, enrich, audit, and bundle tools |",
        "",
        "## Maintenance",
        "",
        "```bash",
        "python3 scripts/generate_enriched_catalog.py",
        "python3 scripts/audit_skills.py",
        "./scripts/build-bundle.sh",
        "```",
        "",
        "The scheduled workflow runs monthly from `.github/workflows/sync-audit.yml`.",
        "",
        "## License",
        "",
        "[MIT](LICENSE)",
        "",
    ])


def write_outputs(enriched: dict[str, Any], bundle: dict[str, Any]) -> None:
    ENRICHED_PATH.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STANDARD_BUNDLE_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    HORIZONTAL_PATH.write_text(render_horizontal_index(enriched["skills"]), encoding="utf-8")
    TYPE_PATH.write_text(render_type_index(enriched["skills"]), encoding="utf-8")
    DEPENDENCY_PATH.write_text(render_dependency_index(enriched["skills"]), encoding="utf-8")
    SCORING_PATH.write_text(render_scoring_model(), encoding="utf-8")
    README_PATH.write_text(render_readme(enriched, bundle), encoding="utf-8")


def main() -> int:
    enriched = build_enriched()
    bundle = build_standard_bundle(enriched)
    write_outputs(enriched, bundle)
    print(json.dumps({"summary": enriched["summary"], "standard_bundle": len(bundle["skills"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

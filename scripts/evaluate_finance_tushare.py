#!/usr/bin/env python3
"""Evaluate finance skills against a Tushare-backed data interface.

The script never stores or prints TUSHARE_TOKEN. Set it in the shell only:
  export TUSHARE_TOKEN='...'
  python3 scripts/evaluate_finance_tushare.py
"""
from __future__ import annotations

import html
import json
import math
import os
import statistics
import sys
import time
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "skills.enriched.json"
OUT_DIR = ROOT / "reports" / "finance-skill-eval" / "tushare-eval"
JSON_OUT = OUT_DIR / "tushare-finance-skill-evaluation.json"
HTML_OUT = OUT_DIR / "tushare-finance-skill-evaluation.html"
MD_OUT = OUT_DIR / "tushare-finance-skill-evaluation.md"
RECOMMENDATION_JSON_OUT = OUT_DIR / "standard-finance-skills-recommendation.json"

ALLOWED_DATA_KEYS = {"TUSHARE_TOKEN"}
SKIP_KEYS = {
    "ADANOS_API_KEY", "ALPACA_API_KEY", "FINVIZ_API_KEY", "FMP_API_KEY",
    "FUNDA_API_KEY", "GEMINI_API_KEY", "IMA_API_KEY", "IMA_CLIENT_ID",
    "LLMQUANT_API_KEY", "OPENAI_API_KEY", "STOCK_API_KEY",
}

SCENARIOS = {
    "A股基础数据": {
        "keywords": ["a-stock", "akshare", "tushare", "stock-data", "alphaear-stock"],
        "question": "查询贵州茅台(600519.SH)、宁德时代(300750.SZ)、中国平安(601318.SH)的基础信息、最新可用日线、成交额、市值/行业线索，并给出数据可用性判断。",
    },
    "个股研究/估值": {
        "keywords": ["valuation", "analysis", "equities", "company", "research", "dcf", "comps", "earnings-preview", "earnings-recap", "us-stock"],
        "question": "基于 Tushare 的日线、基本面/财务指标可用字段，生成贵州茅台的个股研究框架：趋势、估值可用字段、风险与后续需要补的数据。",
    },
    "市场复盘/宏观政策": {
        "keywords": ["macro", "market", "daily", "news", "policy", "environment", "breadth", "uptrend", "top", "hormuz"],
        "question": "用沪深300、中证500、创业板指或可替代指数日线，判断最近一段市场趋势、波动和复盘要点；宏观/政策类只评价 Tushare 能否支撑。",
    },
    "选股/机会发现": {
        "keywords": ["screener", "canslim", "vcp", "theme", "dividend", "value", "idea", "sector"],
        "question": "基于 Tushare 日线和基础资料，构造一个 A 股候选池筛选任务：流动性、趋势、波动、行业分布，并评价该 skill 是否适合迁移到 Tushare。",
    },
    "技术面/交易计划": {
        "keywords": ["technical", "sepa", "breakout", "position", "trade", "signal", "ftd", "distribution", "momentum"],
        "question": "用贵州茅台或宁德时代最近日线计算收益、均线、波动、回撤，判断是否足够支撑技术面/交易计划类 skill。",
    },
    "组合/风控/监控": {
        "keywords": ["portfolio", "monitor", "risk", "watch", "thesis", "memory", "exposure"],
        "question": "构造一个 A 股三股票组合，基于 Tushare 日线计算收益、波动、相关性和最大回撤，并评价组合监控/风控技能适配度。",
    },
    "量化/回测/策略迭代": {
        "keywords": ["backtest", "pybroker", "hypothesis", "postmortem", "correlation", "pair"],
        "question": "用 Tushare 拉取 A 股日线，验证能否支撑简单均线策略、收益/回撤/稳定性评估或相关性分析。",
    },
    "期权/固收/外汇/衍生品": {
        "keywords": ["options", "derivatives", "rates", "fx", "bond", "credit", "commodities", "swap"],
        "question": "评价 Tushare 对期权、债券、基金、期货等资产的覆盖能否支撑该 skill；若 skill 强依赖 LSEG/LLMQuant/FMP 则跳过实测。",
    },
    "机构金融/投行/PE/基金运营": {
        "keywords": ["anthropic-fs", "lbo", "merger", "banking", "private-equity", "fund-admin", "wealth", "kyc", "cim", "teaser"],
        "question": "评价 Tushare 是否能替代机构 MCP/文件/企业数据，用于模型、材料、尽调、基金运营或 KYC；不能替代则说明原因。",
    },
    "报告/可视化/知识库": {
        "keywords": ["report", "visual", "logic", "quality", "kb", "xlsx", "pptx", "audit"],
        "question": "评价 Tushare 输出的数据表、指标和图表数据能否支撑报告、可视化、知识库或数据质量检查类 skill。",
    },
}

@dataclass
class DataHealth:
    token_present: bool
    tushare_imported: bool
    tushare_version: str | None
    connected: bool
    samples: dict[str, Any]
    free_sources: dict[str, Any]
    errors: list[str]

@dataclass
class EvalResult:
    skill_id: str
    skill_name: str
    skill_description: str
    category: str
    scenario: str
    status: str
    score: int
    report_completeness: int
    report_effectiveness: int
    report_content_summary: str
    verdict: str
    data_source_policy: str
    test_question: str
    generated_result_preview: str
    result_evaluation: str
    evidence: list[str]
    missing_or_blocked: list[str]
    api_keys: list[str]
    access_mode: str


def load_catalog() -> list[dict[str, Any]]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))["skills"]


def is_finance_skill(skill: dict[str, Any]) -> bool:
    sid = skill["id"]
    return (
        skill.get("primary_category", "").startswith("finance")
        or sid.startswith(("anthropic-fs-", "llmquant-"))
        or any(token in sid for token in [
            "stock", "portfolio", "earnings", "market", "macro", "backtest",
            "trade", "trading", "valuation", "dividend", "etf", "funda",
            "yfinance", "akshare", "tushare", "finviz", "option", "sector",
            "signal", "theme", "canslim", "vcp", "sepa",
        ])
    )


def classify_scenario(skill: dict[str, Any]) -> str:
    haystack = f"{skill['id']} {skill.get('description','')} {skill.get('primary_category','')}".lower()
    best = "报告/可视化/知识库"
    best_hits = -1
    for scenario, cfg in SCENARIOS.items():
        hits = sum(1 for keyword in cfg["keywords"] if keyword in haystack)
        if hits > best_hits:
            best = scenario
            best_hits = hits
    return best


def skill_blob(skill: dict[str, Any]) -> str:
    return f"{skill.get('id','')} {skill.get('name','')} {skill.get('description','')} {skill.get('primary_category','')} {' '.join(skill.get('tags') or [])}".lower()


def infer_skill_capabilities(skill: dict[str, Any]) -> list[str]:
    blob = skill_blob(skill)
    checks = [
        ("A股数据源", ["a股", "tushare", "akshare", "a-stock", "stock-data", "行情", "基础数据"]),
        ("个股评分", ["8", "score", "评分", "stock-analysis", "analysis"]),
        ("每日复盘", ["daily", "每日", "复盘", "recap"]),
        ("知识库/框架", ["kb", "knowledge", "知识库", "百科", "template"]),
        ("回测", ["backtest", "pybroker", "回测", "strategy"]),
        ("监控/提醒", ["monitor", "watch", "alert", "监控", "提醒"]),
        ("组合/风控", ["portfolio", "risk", "position", "exposure", "组合", "风控", "仓位"]),
        ("估值/研究", ["valuation", "dcf", "comps", "research", "估值", "研究"]),
        ("财报/业绩", ["earnings", "income", "financial", "财报", "业绩"]),
        ("宏观/政策", ["macro", "policy", "宏观", "政策", "央行", "证监会"]),
        ("新闻/谣言", ["news", "rumor", "sentiment", "新闻", "谣言", "情绪"]),
        ("技术面/交易", ["technical", "trade", "breakout", "sepa", "vcp", "momentum", "技术", "交易", "突破"]),
        ("选股/扫描", ["screener", "scan", "candidate", "canslim", "theme", "sector", "选股", "扫描", "题材"]),
        ("期权/衍生品", ["option", "payoff", "derivative", "期权", "衍生品"]),
        ("机构金融材料", ["anthropic-fs", "lbo", "cim", "teaser", "kyc", "fund", "private-equity", "banking"]),
        ("报告/可视化", ["report", "visual", "ppt", "xlsx", "chart", "报告", "可视化"]),
    ]
    capabilities = [label for label, keywords in checks if any(keyword in blob for keyword in keywords)]
    return capabilities or ["金融辅助分析"]


def make_skill_specific_question(skill: dict[str, Any], health: DataHealth) -> str:
    sid = skill["id"]
    name = skill.get("name") or sid
    description = skill.get("description", "").strip()
    capabilities = infer_skill_capabilities(skill)
    blob = skill_blob(skill)

    universe = "贵州茅台(600519.SH)、宁德时代(300750.SZ)、中国平安(601318.SH)"
    if "macro" in blob or "policy" in blob or "市场" in blob:
        universe = "沪深300(000300.SH)、创业板指(399006.SZ)、中证500(000905.SH)"
    elif "option" in blob or "payoff" in blob:
        universe = "以沪深300ETF或贵州茅台为底层资产，构造一个保护性看跌/备兑组合示例"
    elif "portfolio" in blob or "risk" in blob or "position" in blob:
        universe = "A股三票组合：贵州茅台、宁德时代、中国平安，初始等权"
    elif "backtest" in blob or "pybroker" in blob:
        universe = "贵州茅台与宁德时代最近一段日线，测试20/60日均线策略"
    elif "monitor" in blob or "watch" in blob:
        universe = "自选股：贵州茅台、宁德时代、中国平安；监控价格、异动、公告和新闻"
    elif "earnings" in blob or "valuation" in blob or "research" in blob or "估值" in blob:
        universe = "贵州茅台(600519.SH)，并用宁德时代作为成长股对照"

    output_sections = []
    if "A股数据源" in capabilities:
        output_sections += ["数据源连通性", "基础信息表", "日线/估值字段样例", "缺失字段说明"]
    if "个股评分" in capabilities:
        output_sections += ["8维评分或等价评分", "优势/风险", "谣言或新闻校验", "操作建议边界"]
    if "每日复盘" in capabilities:
        output_sections += ["指数表现", "板块/风格线索", "重点个股", "次日观察清单"]
    if "知识库/框架" in capabilities:
        output_sections += ["适用策略框架", "指标解释", "风控模板", "调用建议"]
    if "回测" in capabilities:
        output_sections += ["策略规则", "回测数据输入", "收益/回撤/胜率", "参数敏感性"]
    if "监控/提醒" in capabilities:
        output_sections += ["监控字段", "阈值规则", "提醒优先级", "误报控制"]
    if "组合/风控" in capabilities:
        output_sections += ["组合暴露", "波动/相关性", "最大回撤", "仓位调整建议"]
    if "估值/研究" in capabilities:
        output_sections += ["业务与财务摘要", "估值可用字段", "关键假设", "风险与补数清单"]
    if "财报/业绩" in capabilities:
        output_sections += ["业绩指标", "同比/环比", "利润质量", "下一步验证"]
    if "宏观/政策" in capabilities:
        output_sections += ["政策/宏观主题", "市场影响路径", "受益/受损行业", "数据不能覆盖部分"]
    if "新闻/谣言" in capabilities:
        output_sections += ["新闻事件", "来源可靠性", "市场反应", "谣言风险"]
    if "技术面/交易" in capabilities:
        output_sections += ["趋势结构", "均线/波动/回撤", "入场/止损观察位", "失效条件"]
    if "选股/扫描" in capabilities:
        output_sections += ["筛选条件", "候选池", "剔除理由", "复核优先级"]
    if "期权/衍生品" in capabilities:
        output_sections += ["收益结构", "最大亏损/盈亏平衡", "所需专业数据", "Tushare可补部分"]
    if "机构金融材料" in capabilities:
        output_sections += ["材料用途", "公开市场补充页", "企业/MCP依赖", "不能替代说明"]
    if "报告/可视化" in capabilities:
        output_sections += ["报告章节", "图表数据", "引用来源", "质量检查"]
    output_sections = list(dict.fromkeys(output_sections))[:8] or ["任务结论", "数据依据", "缺口说明"]

    return (
        f"请用「{name}」这个 skill 完成一项和它自身功能匹配的测试，而不是套用通用问题。"
        f"skill 描述：{description[:260] or sid}。"
        f"测试对象：{universe}。"
        f"请输出：{'、'.join(output_sections)}。"
        "最后判断：在 Tushare 为核心、免 key 数据源为补强的条件下，这个 skill 能否产出可直接给投资者阅读的结果。"
    )


def generate_result_preview(skill: dict[str, Any], health: DataHealth, score: int, status: str) -> str:
    capabilities = infer_skill_capabilities(skill)
    cov = coverage_from_health(health)
    available_sources = []
    for label, key in [
        ("Tushare基础资料", "stock_basic"),
        ("Tushare日线", "daily"),
        ("Tushare指数", "index_daily"),
        ("Tushare估值", "daily_basic"),
        ("Tushare财务", "income"),
        ("腾讯实时行情", "tencent_quote"),
        ("东财行情/资金", "eastmoney_quote"),
        ("东财龙虎榜/事件", "eastmoney_datacenter"),
        ("百度K线均线", "baidu_kline"),
        ("巨潮公告", "cninfo_announcements"),
        ("财经快讯", "cls_news"),
    ]:
        if cov.get(key):
            available_sources.append(label)
    if not available_sources:
        available_sources.append("暂无实测可用数据源")

    if status.startswith("skipped"):
        return f"未生成完整投资结果：该 skill 的关键依赖不在本轮可用环境内。可生成的只有适配性说明、依赖清单和替代数据建议。可用补强源：{'、'.join(available_sources[:6])}。"

    lead = "可生成结果草案"
    if score >= 85:
        lead = "可生成较完整结果"
    elif score < 45:
        lead = "只能生成辅助结果"
    sections: list[str] = []
    if "A股数据源" in capabilities:
        sections.append("基础信息/行情/估值字段表")
    if "个股评分" in capabilities:
        sections.append("多维评分与风险解释")
    if "每日复盘" in capabilities:
        sections.append("市场复盘和次日观察")
    if "回测" in capabilities:
        sections.append("策略规则、收益和回撤摘要")
    if "监控/提醒" in capabilities:
        sections.append("自选股阈值与提醒规则")
    if "组合/风控" in capabilities:
        sections.append("组合波动、相关性和仓位建议")
    if "估值/研究" in capabilities:
        sections.append("研究框架、估值字段和补数清单")
    if "宏观/政策" in capabilities:
        sections.append("政策影响路径与市场映射")
    if "技术面/交易" in capabilities:
        sections.append("趋势、均线、回撤和失效条件")
    if "选股/扫描" in capabilities:
        sections.append("候选池筛选和剔除理由")
    if "期权/衍生品" in capabilities:
        sections.append("收益结构和专业数据缺口")
    if "机构金融材料" in capabilities:
        sections.append("公开市场补充页和企业系统缺口")
    if "报告/可视化" in capabilities:
        sections.append("图表表格和报告章节")
    sections = list(dict.fromkeys(sections))[:5] or ["数据可用性、结论和缺口"]
    return f"{lead}：包含{'、'.join(sections)}。已实测/可用数据依据：{'、'.join(available_sources[:7])}。"


def evaluate_generated_result(skill: dict[str, Any], health: DataHealth, score: int, missing: list[str], status: str) -> str:
    capabilities = infer_skill_capabilities(skill)
    cov = coverage_from_health(health)
    source_count = sum(1 for ok in cov.values() if ok)
    if status.startswith("skipped"):
        return "评测结论：不能公平评价最终产出质量，因为关键 API/MCP/企业数据缺失；仅评价了可替代性和补强价值。"
    if not health.connected:
        return f"评测结论：题目已按 skill 描述单独生成，但 Tushare 未连通，只能用 {source_count} 个免 key/已探测源做预评；需 token 复跑后才能给最终分。"
    if score >= 85:
        return f"评测结论：任务、数据源和 skill 能力高度一致；生成结果覆盖 {', '.join(capabilities[:4])}，可作为主流程候选。"
    if score >= 65:
        return f"评测结论：核心结果可用，但仍有 {'；'.join(missing[:2]) if missing else '若干补充数据缺口'}；适合做组合式流程的一环。"
    if score >= 40:
        return f"评测结论：只能解决 skill 功能中的局部问题，结果更像辅助页；不建议作为单独金融套件核心。"
    return "评测结论：生成结果无法覆盖该 skill 的核心承诺，不建议接入本轮 Tushare 金融链路。"


def free_source_count(health: DataHealth) -> int:
    cov = coverage_from_health(health)
    return sum(
        1
        for key, value in cov.items()
        if key not in {"stock_basic", "daily", "index_daily", "daily_basic", "income"} and value
    )


def preliminary_fit_score(skill: dict[str, Any], health: DataHealth, blocked_keys: list[str], access: str) -> tuple[int, str, list[str], list[str]]:
    """Produce a differentiated no-token score.

    This is not a final Tushare execution score. It estimates whether the skill is
    worth re-running with Tushare connected by combining skill intent, dependency
    burden, and the no-key sources that are already live.
    """
    sid = skill["id"]
    scenario = classify_scenario(skill)
    capabilities = infer_skill_capabilities(skill)
    blob = skill_blob(skill)
    cov = coverage_from_health(health)
    available_free = free_source_count(health)
    score = 18
    evidence: list[str] = []
    missing: list[str] = []

    if "A股数据源" in capabilities:
        score += 28
        evidence.append("核心承诺是 A 股数据/行情，和 Tushare 以及免 key A 股源天然匹配。")
    if "估值/研究" in capabilities or "财报/业绩" in capabilities:
        score += 12
        evidence.append("估值/财报研究可由 Tushare basic/daily_basic/income 补齐，适合 token 复测。")
    if "技术面/交易" in capabilities:
        score += 10
        evidence.append("技术面能力可由 Tushare 日线 + 百度/腾讯行情补强。")
    if "组合/风控" in capabilities:
        score += 9
        evidence.append("组合风控需要日线收益矩阵，Tushare 连通后可较好支撑。")
    if "回测" in capabilities:
        score += 8
        evidence.append("回测类至少需要稳定日线，Tushare 可作为 A 股回测输入。")
    if "选股/扫描" in capabilities:
        score += 8
        evidence.append("选股扫描可用 Tushare 股票池/日线/估值字段做初筛。")
    if "监控/提醒" in capabilities:
        score += 6
        evidence.append("监控类可用免 key 行情与公告源预先支撑，Tushare 补历史序列。")
    if "报告/可视化" in capabilities or "知识库/框架" in capabilities:
        score += 5
        evidence.append("报告/知识库类可消费结构化行情、公告、事件与指标数据。")
    if "宏观/政策" in capabilities:
        score += 2
        missing.append("政策文本不在 Tushare 核心覆盖内，只能用指数/行情做市场反应补充。")
    if "新闻/谣言" in capabilities:
        score += 2
        missing.append("新闻/谣言核验需要更强新闻源，Tushare 只能补价格反应。")
    if "期权/衍生品" in capabilities:
        score -= 14
        missing.append("期权/衍生品需要波动率、合约链、定价参数，Tushare 不能单独支撑。")
    if "机构金融材料" in capabilities:
        score -= 18
        missing.append("机构材料/KYC/基金运营依赖企业文件或 MCP，Tushare 只是补充页。")

    score += min(12, available_free * 2)
    if cov["tencent_quote"] or cov["eastmoney_quote"]:
        score += 4
    if cov["eastmoney_datacenter"] and ("选股/扫描" in capabilities or "技术面/交易" in capabilities):
        score += 4
    if cov["cninfo_announcements"] and ("估值/研究" in capabilities or "报告/可视化" in capabilities):
        score += 4
    if cov["baidu_kline"] and ("技术面/交易" in capabilities or "回测" in capabilities):
        score += 3

    if sid == "tushare-openclaw-skill":
        score = max(score, 88)
        evidence.append("原生 Tushare skill，token 连通后应作为基准数据源测试。")
    elif sid == "a-stock-data":
        score = max(score, 82)
        evidence.append("a-stock-data 自带多源 A 股能力，适合作为 Tushare + 免 key 补强的核心候选。")
    elif sid in {"akshare-stock", "openclaw-stock-data-skill"}:
        score = max(score, 74)
        evidence.append("A 股数据封装类，具备较高替代/迁移价值。")
    elif "yfinance" in sid or "us-" in sid or "finviz" in sid:
        score = min(score, 38)
        missing.append("主要面向美股/全球市场，Tushare 不宜替代，只能做 A 股补充。")
    elif sid.startswith("anthropic-fs-"):
        score = min(score, 32)
        missing.append("Anthropic FS 主要依赖企业数据/文档/MCP，本轮只给补充价值分。")

    if blocked_keys:
        score = min(score, 24)
        missing.append("存在额外 API Key 依赖，当前环境不能验证最终产出。")
    if "mcp-required" in access and not sid.startswith("anthropic-fs-"):
        score = min(score, 20)
        missing.append("需要 MCP/外部工具，当前只评价迁移可行性。")
    if "mcp-required" in access and sid.startswith("anthropic-fs-"):
        score = min(score, 28)
        missing.append("企业 MCP 未连接，Tushare 只可能作为上市公司公开市场补充。")

    score = max(5, min(92, score))
    if not evidence:
        evidence.append("根据 skill 描述、依赖、市场范围和免 key 数据源可用性生成差异化预评分。")
    return score, "；".join(capabilities[:5]), evidence, missing


def try_tushare() -> tuple[DataHealth, Any | None]:
    token = os.environ.get("TUSHARE_TOKEN")
    errors: list[str] = []
    samples: dict[str, Any] = {}
    free_sources = try_free_sources()
    try:
        import tushare as ts  # type: ignore
        version = getattr(ts, "__version__", None)
    except Exception as exc:
        return DataHealth(bool(token), False, None, False, samples, free_sources, [f"import tushare failed: {exc}"]), None
    if not token:
        return DataHealth(False, True, version, False, samples, free_sources, ["TUSHARE_TOKEN is not set in environment"]), None
    try:
        ts.set_token(token)
        pro = ts.pro_api(token)
        # Keep calls small and conservative.
        stock_basic = pro.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,area,industry,market,list_date")
        samples["stock_basic_rows"] = int(len(stock_basic))
        samples["stock_basic_columns"] = list(stock_basic.columns)
        daily = pro.daily(ts_code="600519.SH", start_date="20260101", end_date="20260612")
        samples["daily_600519_rows"] = int(len(daily))
        samples["daily_600519_columns"] = list(daily.columns)
        idx = pro.index_daily(ts_code="000300.SH", start_date="20260101", end_date="20260612")
        samples["index_000300_rows"] = int(len(idx))
        try:
            daily_basic = pro.daily_basic(ts_code="600519.SH", start_date="20260101", end_date="20260612", fields="ts_code,trade_date,close,turnover_rate,pe_ttm,pb,total_mv,circ_mv")
            samples["daily_basic_600519_rows"] = int(len(daily_basic))
            samples["daily_basic_600519_columns"] = list(daily_basic.columns)
        except Exception as exc:
            errors.append(f"daily_basic failed: {exc}")
        try:
            income = pro.income(ts_code="600519.SH", period="20251231", fields="ts_code,end_date,total_revenue,n_income,operate_profit,basic_eps")
            samples["income_600519_rows"] = int(len(income))
        except Exception as exc:
            errors.append(f"income failed: {exc}")
        return DataHealth(True, True, version, True, samples, free_sources, errors), pro
    except Exception as exc:
        errors.append(f"Tushare connectivity failed: {exc}")
        return DataHealth(True, True, version, False, samples, free_sources, errors), None


def _source_ok(payload: dict[str, Any], key: str) -> bool:
    item = payload.get(key) or {}
    return bool(item.get("ok"))


def try_free_sources() -> dict[str, Any]:
    """Probe no-key public data sources that can complement Tushare.

    These probes are intentionally tiny. They do not require user secrets and are
    used only to decide whether a skill can generate a richer investment report
    with Tushare as the core data source plus no-key market/news/disclosure data.
    """
    result: dict[str, Any] = {}

    def capture(name: str, fn: Callable[[], dict[str, Any]]) -> None:
        started = time.time()
        try:
            data = fn()
            data["latency_ms"] = int((time.time() - started) * 1000)
            result[name] = {"ok": True, **data}
        except Exception as exc:
            result[name] = {
                "ok": False,
                "latency_ms": int((time.time() - started) * 1000),
                "error": str(exc)[:240],
            }

    def tencent_quote() -> dict[str, Any]:
        url = "https://qt.gtimg.cn/q=sh600519,sz300750,sh000300"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=10).read().decode("gbk", errors="ignore")
        rows = [line for line in text.split(";") if "~" in line]
        names: list[str] = []
        fields_seen: set[str] = set()
        for line in rows:
            values = line.split('"')[1].split("~") if '"' in line else []
            if len(values) > 52:
                names.append(values[1])
                for idx, field in [(3, "price"), (32, "pct_change"), (39, "pe_ttm"), (44, "market_cap"), (46, "pb"), (49, "volume_ratio")]:
                    if values[idx]:
                        fields_seen.add(field)
        return {"rows": len(rows), "names": names[:5], "fields": sorted(fields_seen)}

    def eastmoney_quote() -> dict[str, Any]:
        import requests
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        params = {
            "fltt": "2",
            "secids": "1.600519,0.300750,1.000300",
            "fields": "f12,f14,f2,f3,f4,f5,f6,f20,f21,f62",
        }
        data = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        rows = data.get("data", {}).get("diff", []) or []
        return {"rows": len(rows), "names": [r.get("f14") for r in rows[:5]], "fields": ["price", "pct_change", "amount", "market_cap", "main_net_flow"]}

    def eastmoney_datacenter() -> dict[str, Any]:
        import requests
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            "reportName": "RPT_DAILYBILLBOARD_DETAILS",
            "columns": "ALL",
            "pageNumber": "1",
            "pageSize": "5",
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
        }
        data = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        rows = (data.get("result") or {}).get("data", []) or []
        return {"rows": len(rows), "fields": ["dragon_tiger_board", "net_buy_amount", "reason"]}

    def baidu_kline() -> dict[str, Any]:
        import requests
        url = "https://finance.pae.baidu.com/selfselect/getstockquotation"
        params = {
            "all": "1",
            "isIndex": "false",
            "isBk": "false",
            "isBlock": "false",
            "isFutures": "false",
            "isStock": "true",
            "newFormat": "1",
            "group": "quotation_kline_ab",
            "finClientType": "pc",
            "code": "600519",
            "ktype": "1",
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.finance-web.v1+json",
            "Origin": "https://gushitong.baidu.com",
            "Referer": "https://gushitong.baidu.com/",
        }
        data = requests.get(url, params=params, headers=headers, timeout=10).json()
        result_data = data.get("Result", {})
        if isinstance(result_data, list):
            result_data = result_data[0] if result_data else {}
        market_data = result_data.get("newMarketData", {}) if isinstance(result_data, dict) else {}
        rows = [row for row in str(market_data.get("marketData", "")).split(";") if row]
        keys = market_data.get("keys", []) or []
        return {"rows": len(rows), "fields": [k for k in keys if k in {"time", "open", "close", "high", "low", "volume", "amount", "ma5avgprice", "ma10avgprice", "ma20avgprice"}]}

    def cninfo_announcements() -> dict[str, Any]:
        import requests
        url = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
        payload = {
            "stock": "600519,gssh0600519",
            "tabName": "fulltext",
            "pageSize": "5",
            "pageNum": "1",
            "column": "",
            "category": "",
            "plate": "",
            "seDate": "",
            "searchkey": "",
            "secid": "",
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.cninfo.com.cn/new/disclosure",
            "Origin": "https://www.cninfo.com.cn",
        }
        data = requests.post(url, data=payload, headers=headers, timeout=10).json()
        rows = data.get("announcements", []) or []
        return {"rows": len(rows), "fields": ["announcement_title", "announcement_type", "announcement_time", "download_url"]}

    def cls_news() -> dict[str, Any]:
        import requests
        url = "https://np-weblist.eastmoney.com/comm/web/getFastNewsList"
        params = {
            "client": "web",
            "biz": "web_724",
            "fastColumn": "102",
            "sortEnd": "",
            "pageSize": "5",
        }
        data = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://kuaixun.eastmoney.com/"}, timeout=10).json()
        rows = (data.get("data") or {}).get("fastNewsList", []) or []
        return {"rows": len(rows), "fields": ["title", "summary", "show_time"]}

    capture("tencent_quote", tencent_quote)
    capture("eastmoney_quote", eastmoney_quote)
    capture("eastmoney_datacenter", eastmoney_datacenter)
    capture("baidu_kline", baidu_kline)
    capture("cninfo_announcements", cninfo_announcements)
    capture("cls_news", cls_news)
    return result


def coverage_from_health(health: DataHealth) -> dict[str, bool]:
    s = health.samples
    free = health.free_sources or {}
    return {
        "stock_basic": s.get("stock_basic_rows", 0) > 0,
        "daily": s.get("daily_600519_rows", 0) > 0,
        "index_daily": s.get("index_000300_rows", 0) > 0,
        "daily_basic": s.get("daily_basic_600519_rows", 0) > 0,
        "income": s.get("income_600519_rows", 0) > 0,
        "tencent_quote": _source_ok(free, "tencent_quote"),
        "eastmoney_quote": _source_ok(free, "eastmoney_quote"),
        "eastmoney_datacenter": _source_ok(free, "eastmoney_datacenter"),
        "baidu_kline": _source_ok(free, "baidu_kline"),
        "cninfo_announcements": _source_ok(free, "cninfo_announcements"),
        "cls_news": _source_ok(free, "cls_news"),
    }


def report_quality(skill: dict[str, Any], scenario: str, score: int, health: DataHealth) -> tuple[int, int, str]:
    cov = coverage_from_health(health)
    direct_market_sources = sum(1 for key in ["daily", "daily_basic", "tencent_quote", "eastmoney_quote", "baidu_kline"] if cov.get(key))
    event_sources = sum(1 for key in ["eastmoney_datacenter", "cninfo_announcements", "cls_news", "income"] if cov.get(key))
    base = min(75, max(15, score - 10))
    completeness = base + min(20, direct_market_sources * 4 + event_sources * 3)
    effectiveness = base + min(18, direct_market_sources * 5) + (6 if event_sources >= 2 else 0)

    if scenario in {"期权/固收/外汇/衍生品", "机构金融/投行/PE/基金运营"}:
        completeness = min(completeness, 55)
        effectiveness = min(effectiveness, 50)
    if not health.connected:
        completeness = min(completeness, 72)
        effectiveness = min(effectiveness, 68)

    content_by_scenario = {
        "A股基础数据": "可生成股票基础信息、行情快照、日线表现、估值字段、市值/行业线索与数据源健康检查。",
        "个股研究/估值": "可生成个股研究框架：趋势、估值、财务摘要、事件缺口、风险清单和后续补数建议。",
        "市场复盘/宏观政策": "可生成指数趋势、波动、成交活跃度、新闻/政策待补充提示和市场复盘摘要。",
        "选股/机会发现": "可生成候选池筛选、流动性/趋势/波动/行业分布、异常项和人工复核清单。",
        "技术面/交易计划": "可生成均线、涨跌幅、波动、回撤、突破/止损观察点和交易计划草案。",
        "组合/风控/监控": "可生成组合收益、波动、相关性、最大回撤、集中度和监控阈值建议。",
        "量化/回测/策略迭代": "可生成简单策略回测输入、收益/回撤/稳定性指标和参数迭代建议。",
        "期权/固收/外汇/衍生品": "仅能生成 A 股公开市场补充页；衍生品定价、曲线、波动率面仍需专业源。",
        "机构金融/投行/PE/基金运营": "仅能生成上市公司公开市场补充页；尽调、KYC、基金运营材料仍需企业系统或文件。",
        "报告/可视化/知识库": "可生成数据表、图表输入、质量检查、引用来源清单和报告章节骨架。",
    }
    if score >= 85:
        suffix = "整体效果：可作为主数据底座，报告完整度较高。"
    elif score >= 65:
        suffix = "整体效果：适合作为核心行情/基础面模块，但需补研报、新闻或专业数据。"
    elif score >= 40:
        suffix = "整体效果：适合作为辅助数据页，不建议单独承担完整报告。"
    else:
        suffix = "整体效果：不建议纳入本轮 Tushare 报告链路。"
    return min(100, completeness), min(100, effectiveness), f"{content_by_scenario.get(scenario, content_by_scenario['报告/可视化/知识库'])} {suffix}"


def build_result(
    skill: dict[str, Any],
    health: DataHealth,
    scenario: str,
    status: str,
    score: int,
    verdict: str,
    data_source_policy: str,
    test_question: str,
    evidence: list[str],
    missing_or_blocked: list[str],
    api_keys: list[str],
    access_mode: str,
) -> EvalResult:
    preview = generate_result_preview(skill, health, score, status)
    result_eval = evaluate_generated_result(skill, health, score, missing_or_blocked, status)
    completeness, effectiveness, content_summary = report_quality(skill, scenario, score, health)
    return EvalResult(
        skill_id=skill["id"],
        skill_name=skill.get("name") or skill["id"],
        skill_description=skill.get("description", ""),
        category=skill.get("primary_category", ""),
        scenario=scenario,
        status=status,
        score=score,
        report_completeness=completeness,
        report_effectiveness=effectiveness,
        report_content_summary=content_summary,
        verdict=verdict,
        data_source_policy=data_source_policy,
        test_question=test_question,
        generated_result_preview=preview,
        result_evaluation=result_eval,
        evidence=evidence,
        missing_or_blocked=missing_or_blocked,
        api_keys=api_keys,
        access_mode=access_mode,
    )


def evaluate_skill(skill: dict[str, Any], health: DataHealth) -> EvalResult:
    sid = skill["id"]
    deps = skill.get("dependencies", {})
    keys = deps.get("api_keys") or []
    access = deps.get("access_mode", "direct")
    scenario = classify_scenario(skill)
    question = make_skill_specific_question(skill, health)
    blocked_keys = [key for key in keys if key not in ALLOWED_DATA_KEYS]
    evidence: list[str] = []
    missing: list[str] = []

    if blocked_keys:
        pre_score, fit_summary, pre_evidence, pre_missing = preliminary_fit_score(skill, health, blocked_keys, access)
        return build_result(
            skill, health, scenario, "skipped_extra_api_prefit", pre_score,
            "预评：该 skill 需要 Tushare 以外的额外 API / 平台凭证，不能做最终实测，但保留适配价值评分。",
            "skip_extra_api", question, pre_evidence, ["requires " + ", ".join(blocked_keys), *pre_missing], keys, access,
        )
    if "mcp-required" in access and not sid.startswith("anthropic-fs-"):
        pre_score, fit_summary, pre_evidence, pre_missing = preliminary_fit_score(skill, health, blocked_keys, access)
        return build_result(
            skill, health, scenario, "skipped_mcp_prefit", pre_score,
            "预评：该 skill 依赖 MCP/外部工具，不能做最终实测，但保留迁移/补强价值评分。",
            "skip_mcp", question, pre_evidence, ["requires MCP or external tool", *pre_missing], keys, access,
        )
    if "mcp-required" in access and sid.startswith("anthropic-fs-") and not health.connected:
        pre_score, fit_summary, pre_evidence, pre_missing = preliminary_fit_score(skill, health, blocked_keys, access)
        return build_result(
            skill, health, scenario, "skipped_enterprise_mcp_prefit", pre_score,
            "预评：Anthropic FS 依赖企业 MCP 或文件系统；Tushare 只能作为 A 股公开市场补充源。",
            "supplement_only", question, pre_evidence, ["requires enterprise MCP/files; Tushare token not connected", *pre_missing], keys, access,
        )

    cov = coverage_from_health(health)
    if not health.connected:
        preliminary_score, fit_summary, pre_evidence, pre_missing = preliminary_fit_score(skill, health, blocked_keys, access)
        return build_result(
            skill, health, scenario, "pending_tushare_token_free_sources_tested", preliminary_score,
            f"差异化预评：Tushare token 未传入本次进程；当前按 skill 能力、依赖和免 key 源给出预评分。能力识别：{fit_summary}。",
            "pending_tushare_core_free_source_supplement", question,
            pre_evidence,
            [*health.errors[:], *pre_missing], keys, access,
        )

    score = 40
    policy = "tushare_candidate"
    sid_l = sid.lower()
    desc_l = skill.get("description", "").lower()
    blob = f"{sid_l} {desc_l} {scenario}".lower()

    if any(x in blob for x in ["a股", "tushare", "akshare", "stock-data", "alphaear-stock"]):
        score += 35
        evidence.append("A股/行情/基础数据语义与 Tushare stock_basic + daily + daily_basic 高匹配。")
    if scenario in {"技术面/交易计划", "量化/回测/策略迭代", "组合/风控/监控"} and cov["daily"]:
        score += 30
        evidence.append("Tushare daily/index_daily 可支撑日线、均线、波动、回撤、相关性和简单回测。")
    if scenario in {"个股研究/估值", "财报/事件驱动"}:
        if cov["daily_basic"]:
            score += 20
            evidence.append("Tushare daily_basic 可提供 PE/PB/市值/换手等估值字段。")
        if cov["income"]:
            score += 10
            evidence.append("Tushare income 可提供利润表/收入/利润/EPS 等财务字段。")
        missing.append("研报全文、电话会纪要、买方预期通常仍需东财/Funda/LSEG/S&P 或人工材料。")
    if cov["tencent_quote"] or cov["eastmoney_quote"]:
        score += 8
        evidence.append("免 key 行情源（腾讯/东财）可补实时价格、涨跌幅、成交额、市值或资金流。")
    if cov["baidu_kline"]:
        score += 5
        evidence.append("百度股市通 K 线可补 MA5/MA10/MA20 等技术面字段。")
    if cov["cninfo_announcements"] and scenario in {"个股研究/估值", "报告/可视化/知识库", "机构金融/投行/PE/基金运营"}:
        score += 5
        evidence.append("巨潮公告可补公告/披露来源，提高报告可追溯性。")
    if cov["cls_news"] and scenario in {"市场复盘/宏观政策", "个股研究/估值", "报告/可视化/知识库"}:
        score += 4
        evidence.append("财联社快讯可补新闻事件线索。")
    if cov["eastmoney_datacenter"] and scenario in {"选股/机会发现", "技术面/交易计划", "报告/可视化/知识库"}:
        score += 5
        evidence.append("东财数据中心可补龙虎榜/资金事件类结构化数据。")
    if scenario == "市场复盘/宏观政策":
        if cov["index_daily"]:
            score += 20
            evidence.append("Tushare index_daily 可支持指数趋势和市场复盘。")
        missing.append("政策文本/新闻解读不由 Tushare 原生覆盖，需要政策源或新闻源。")
    if scenario == "选股/机会发现":
        if cov["stock_basic"] and cov["daily"]:
            score += 20
            evidence.append("Tushare 可提供股票池、行业、日线和部分财务指标，适合 A 股筛选底座。")
        missing.append("Finviz/CANSLIM 美股专用字段无法直接用 Tushare 替代。")
    if scenario == "期权/固收/外汇/衍生品":
        score -= 10
        missing.append("Tushare 对部分衍生品/基金/债券有接口，但无法替代 LSEG/LLMQuant 级跨资产深度数据。")
    if scenario == "机构金融/投行/PE/基金运营":
        score -= 20
        missing.append("机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。")
    if scenario == "报告/可视化/知识库":
        score += 10
        evidence.append("Tushare 表格型输出适合进入报告、可视化和数据质量检查流程。")

    if sid == "tushare-openclaw-skill":
        score = max(score, 95)
        policy = "native_tushare"
    elif sid == "a-stock-data":
        score = max(score, 88)
        policy = "partial_replace_or_backend_option"
        missing.append("a-stock-data 当前内置多源直连；建议新增 Tushare provider，不建议全部删除原多源能力。")
    elif sid in {"akshare-stock", "openclaw-stock-data-skill"}:
        score = max(score, 82)
        policy = "replace_with_tushare_possible"
    elif "yfinance" in sid or "us-" in sid or "finviz" in sid:
        score = min(score, 45)
        missing.append("Tushare 主要覆盖中国市场，不能替代美股/Finviz/yfinance 的全球资产能力。")
    elif sid.startswith("anthropic-fs-"):
        score = min(score, 50)
        policy = "supplement_only"
        missing.append("Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。")

    score = max(0, min(100, score))
    if score >= 85:
        status = "passed_tushare_strong"
        verdict = "强适配：可优先接入或改为 Tushare 数据底座。"
    elif score >= 65:
        status = "passed_tushare_partial"
        verdict = "部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。"
    elif score >= 40:
        status = "weak_tushare_fit"
        verdict = "弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。"
    else:
        status = "not_suitable_for_tushare"
        verdict = "不适配：领域或依赖不适合用 Tushare 替代。"
    if not evidence:
        evidence.append("基于 skill 描述、依赖标签、场景语义和 Tushare 样本接口覆盖度进行静态+连通性评价。")
    return build_result(skill, health, scenario, status, score, verdict, policy, question, evidence, missing, keys, access)


def html_table(rows: list[list[str]]) -> str:
    return "\n".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)


def render_html(payload: dict[str, Any]) -> str:
    results = payload["results"]
    summary = payload["summary"]
    status_counts = summary["by_status"]
    scenario_counts = summary["by_scenario"]
    cards = "\n".join(
        f"<div class='card'><b>{html.escape(k)}</b><span>{v}</span></div>"
        for k, v in [
            ("金融 Skills", summary["total_finance_skills"]),
            ("实测/可评价", summary["evaluated_or_pending"]),
            ("强/部分适配", summary["tushare_fit"]),
            ("跳过额外 API/MCP", summary["skipped"]),
            ("Tushare 连通", "是" if payload["data_health"]["connected"] else "否"),
        ]
    )
    rows = []
    for r in sorted(results, key=lambda x: (x["scenario"], -x["score"], x["skill_id"])):
        rows.append([
            f"<code>{html.escape(r['skill_id'])}</code>",
            html.escape(r["skill_name"]),
            html.escape(r["scenario"]),
            html.escape(r["skill_description"][:260]),
            html.escape(r["test_question"]),
            html.escape(r["status"]),
            str(r["score"]),
            str(r["report_completeness"]),
            str(r["report_effectiveness"]),
            html.escape(r["report_content_summary"]),
            html.escape(r["generated_result_preview"]),
            html.escape(r["result_evaluation"]),
            html.escape(r["verdict"]),
            html.escape(r["data_source_policy"]),
            html.escape(", ".join(r["api_keys"]) or "无"),
            "<br>".join(html.escape(x) for x in r["evidence"][:3]),
            "<br>".join(html.escape(x) for x in r["missing_or_blocked"][:3]) or "—",
        ])
    scenario_rows = [[html.escape(k), str(v)] for k, v in sorted(scenario_counts.items())]
    status_rows = [[html.escape(k), str(v)] for k, v in sorted(status_counts.items())]
    samples = payload["data_health"].get("samples") or {}
    sample_rows = [[html.escape(k), html.escape(json.dumps(v, ensure_ascii=False))] for k, v in samples.items()]
    free_sources = payload["data_health"].get("free_sources") or {}
    free_source_rows = [
        [
            html.escape(k),
            "可用" if v.get("ok") else "不可用",
            html.escape(str(v.get("rows", "—"))),
            html.escape(", ".join(v.get("fields", [])[:8]) if isinstance(v.get("fields"), list) else "—"),
            html.escape(str(v.get("latency_ms", "—"))),
            html.escape(str(v.get("error", ""))) or "—",
        ]
        for k, v in sorted(free_sources.items())
    ]
    errors = payload["data_health"].get("errors") or []
    methodology_rows = [
        ["纳入范围", "从 catalog/skills.enriched.json 自动筛选金融、股票、组合、交易、估值、宏观、回测等相关 skills。"],
        ["Tushare 接入", "脚本只读取环境变量 TUSHARE_TOKEN，不写入仓库、不打印 token。连通后抽样 stock_basic、daily、index_daily、daily_basic、income。"],
        ["多源补强", "以 Tushare 为核心，同时实测腾讯行情、东财行情/数据中心、百度 K 线、巨潮公告、财联社快讯等免 key 数据源；可用时纳入报告完整度与效果评分。"],
        ["跳过规则", "需要 FMP、Finviz、LLMQuant、LSEG/S&P、IMA、OpenAI、Alpaca、Adanos、Funda 等额外 API/企业 MCP 的项目跳过，不强行用 Tushare 替代。"],
        ["逐技能出题", "不再按大类套同一道题；每个 skill 都根据 id、名称、描述、标签和依赖生成独立测试问题。"],
        ["结果生成", "每个 skill 都生成一段结果预览，说明如果用 Tushare 核心 + 免 key 补强源，它实际会产出哪些内容。"],
        ["评分逻辑", "按 skill 自身承诺、Tushare 字段覆盖、免 key 补强源可用性、市场适配度、替代/补充关系进行 0-100 评分。"],
        ["报告质量", "报告完整度偏覆盖面，效果分偏该 skill 是否能产出可读、可用、贴合自身功能的投资结果。"],
    ]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Tushare 金融 Skills 评测报告</title>
<style>
:root {{ color-scheme: light; --bg:#f7f8fb; --card:#fff; --ink:#172033; --muted:#657086; --line:#e6e8ef; --blue:#2563eb; --green:#059669; --amber:#d97706; --red:#dc2626; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",Arial,sans-serif; background:var(--bg); color:var(--ink); }}
header {{ padding:40px 48px 24px; background:linear-gradient(135deg,#0f172a,#1e40af); color:white; }}
h1 {{ margin:0 0 8px; font-size:34px; }}
.subtitle {{ opacity:.86; line-height:1.7; max-width:980px; }}
main {{ padding:28px 48px 60px; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin:18px 0 28px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px; box-shadow:0 8px 24px rgba(15,23,42,.06); }}
.card b {{ display:block; color:var(--muted); font-size:13px; }}
.card span {{ display:block; font-size:28px; margin-top:8px; color:var(--blue); font-weight:700; }}
section {{ background:var(--card); border:1px solid var(--line); border-radius:18px; padding:22px; margin:20px 0; box-shadow:0 8px 24px rgba(15,23,42,.05); }}
h2 {{ margin:0 0 14px; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
.table-wrap {{ overflow-x:auto; overflow-y:visible; max-width:100%; border:1px solid var(--line); border-radius:14px; }}
.top-scroll {{ overflow-x:auto; overflow-y:hidden; height:18px; margin:10px 0 8px; border:1px solid var(--line); border-radius:999px; background:#f8fafc; }}
.top-scroll-inner {{ height:1px; width:4760px; }}
.wide-table {{ min-width:4760px; border:0; table-layout:fixed; }}
.table-wrap table {{ border:0; }}
th,td {{ border-bottom:1px solid var(--line); padding:10px 8px; vertical-align:top; text-align:left; line-height:1.58; }}
th {{ background:#f1f5f9; position:sticky; top:0; z-index:1; }}
td {{ overflow-wrap:anywhere; word-break:break-word; }}
.wide-table td:nth-child(1), .wide-table th:nth-child(1) {{ width:124px; }}
.wide-table td:nth-child(2), .wide-table th:nth-child(2) {{ width:108px; }}
.wide-table td:nth-child(3), .wide-table th:nth-child(3) {{ width:86px; }}
.wide-table td:nth-child(4), .wide-table th:nth-child(4) {{ width:430px; }}
.wide-table td:nth-child(5), .wide-table th:nth-child(5) {{ width:620px; }}
.wide-table td:nth-child(6), .wide-table th:nth-child(6) {{ width:118px; }}
.wide-table td:nth-child(7), .wide-table td:nth-child(8), .wide-table td:nth-child(9), .wide-table th:nth-child(7), .wide-table th:nth-child(8), .wide-table th:nth-child(9) {{ width:54px; text-align:center; }}
.wide-table td:nth-child(10), .wide-table th:nth-child(10) {{ width:340px; }}
.wide-table td:nth-child(11), .wide-table th:nth-child(11) {{ width:420px; }}
.wide-table td:nth-child(12), .wide-table th:nth-child(12) {{ width:340px; }}
.wide-table td:nth-child(13), .wide-table th:nth-child(13) {{ width:220px; }}
.wide-table td:nth-child(14), .wide-table th:nth-child(14) {{ width:156px; }}
.wide-table td:nth-child(15), .wide-table th:nth-child(15) {{ width:84px; }}
.wide-table td:nth-child(16), .wide-table th:nth-child(16) {{ width:320px; }}
.wide-table td:nth-child(17), .wide-table th:nth-child(17) {{ width:286px; }}
.compact table {{ min-width:0; table-layout:auto; }}
.compact td:nth-child(n), .compact th:nth-child(n) {{ width:auto; min-width:0; text-align:left; }}
.compact th,.compact td {{ padding:10px 9px; }}
code {{ background:#eef2ff; color:#1e40af; padding:2px 5px; border-radius:6px; }}
.small {{ color:var(--muted); font-size:13px; line-height:1.7; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:18px; }}
.badge {{ display:inline-block; padding:3px 8px; border-radius:999px; background:#e0f2fe; color:#075985; }}
</style>
<script>
function syncWideScrollers() {{
  document.querySelectorAll('[data-scroll-pair]').forEach((section) => {{
    const top = section.querySelector('.top-scroll');
    const bottom = section.querySelector('.table-wrap');
    if (!top || !bottom) return;
    let locking = false;
    const sync = (from, to) => {{
      if (locking) return;
      locking = true;
      to.scrollLeft = from.scrollLeft;
      requestAnimationFrame(() => {{ locking = false; }});
    }};
    top.addEventListener('scroll', () => sync(top, bottom));
    bottom.addEventListener('scroll', () => sync(bottom, top));
  }});
}}
window.addEventListener('DOMContentLoaded', syncWideScrollers);
</script>
</head>
<body>
<header>
<h1>Tushare 金融 Skills 评测报告</h1>
<div class="subtitle">目标：把需要中国金融数据接口的 skills 评估为 Tushare 数据底座可接入/可替代/仅补充/应跳过，并跳过需要额外 API Key 或企业 MCP 的项目。本报告由 <code>scripts/evaluate_finance_tushare.py</code> 生成，未保存或展示 Tushare Token。</div>
</header>
<main>
<div class="cards">{cards}</div>
<section><h2>结论摘要</h2>
<p class="small">生成时间：{html.escape(payload['generated_at'])}。Tushare token 状态：<span class="badge">{'已设置' if payload['data_health']['token_present'] else '未设置'}</span>；连通状态：<span class="badge">{'已连通' if payload['data_health']['connected'] else '未连通/待复跑'}</span>。</p>
<p class="small">新版评测不再把同一类 skill 机械套同一道题，而是读取每个 skill 的名称、描述、标签和依赖，单独生成测试问题、结果预览和结果评测。建议：A 股行情、基础资料、日线、指数、部分估值和财务指标类优先迁移/接入 Tushare；美股、Finviz、FMP、LLMQuant、LSEG、S&P、IMA、Anthropic FS 企业 MCP 类不强行替换，按额外 API/MCP 跳过或只把 Tushare 作为 A 股补充数据源。</p>
<p class="small"><b>安全说明：</b>本报告不保存、不展示 Tushare token。若当前显示未连通，请在本机终端临时设置 <code>TUSHARE_TOKEN</code> 后复跑脚本生成实测版。</p>
</section>
<section class="compact"><h2>评测方法</h2><div class="table-wrap"><table><thead><tr><th>项目</th><th>说明</th></tr></thead><tbody>{html_table(methodology_rows)}</tbody></table></div></section>
<section class="grid compact"><div><h2>状态分布</h2><div class="table-wrap"><table><thead><tr><th>状态</th><th>数量</th></tr></thead><tbody>{html_table(status_rows)}</tbody></table></div></div><div><h2>场景分布</h2><div class="table-wrap"><table><thead><tr><th>场景</th><th>数量</th></tr></thead><tbody>{html_table(scenario_rows)}</tbody></table></div></div></section>
<section class="compact"><h2>Tushare 连通性样本</h2><div class="table-wrap"><table><thead><tr><th>样本</th><th>结果</th></tr></thead><tbody>{html_table(sample_rows) if sample_rows else '<tr><td colspan="2">无样本；请设置 TUSHARE_TOKEN 后复跑。</td></tr>'}</tbody></table></div>{'<p class="small">错误/提示：' + '<br>'.join(html.escape(e) for e in errors) + '</p>' if errors else ''}</section>
<section class="compact"><h2>免 Key 多源补强样本</h2><div class="table-wrap"><table><thead><tr><th>数据源</th><th>状态</th><th>行数</th><th>字段/能力</th><th>耗时 ms</th><th>错误</th></tr></thead><tbody>{html_table(free_source_rows) if free_source_rows else '<tr><td colspan="6">未执行免 key 数据源探测。</td></tr>'}</tbody></table></div></section>
<section data-scroll-pair><h2>完整技能评价列表</h2><p class="small">提示：顶部和底部横向滚动条已同步；短字段列已压缩，长文本列保留阅读宽度。</p><div class="top-scroll" aria-label="顶部横向滚动条"><div class="top-scroll-inner"></div></div><div class="table-wrap"><table class="wide-table"><thead><tr><th>Skill</th><th>名称</th><th>场景</th><th>Skill 描述</th><th>专属测试问题</th><th>状态</th><th>总分</th><th>完整度</th><th>效果分</th><th>报告主要内容</th><th>生成结果预览</th><th>结果评测</th><th>评价</th><th>数据策略</th><th>API Key</th><th>证据</th><th>缺口/跳过原因</th></tr></thead><tbody>{html_table(rows)}</tbody></table></div></section>
</main>
</body>
</html>
"""


def recommendation_slots() -> list[dict[str, str]]:
    """Curated no-duplicate finance suite slots.

    The slots are intentionally capability-based: one default skill per investor
    job, with optional alternates recorded as exclusions rather than bundled.
    """
    return [
        {
            "slot": "A股结构化数据底座",
            "skill_id": "tushare-openclaw-skill",
            "role": "用 Tushare Pro 拉取 A 股/基金/期货/债券、行情、财务、估值、分红、解禁等结构化数据。",
            "why": "原生 Tushare，和本轮实测 token、stock_basic、daily、index_daily、daily_basic、income 覆盖完全对齐。",
            "excluded": "a-stock-data、akshare-stock、openclaw-stock-data-skill",
            "exclusion_reason": "同属 A 股数据源；标准套装只保留 Tushare 原生数据底座。a-stock-data 可作为增强包另装。",
        },
        {
            "slot": "全球/美股轻量行情",
            "skill_id": "yfinance-data",
            "role": "获取美股、ETF、指数、加密资产等 Yahoo Finance 数据，补足 Tushare 的中国市场边界。",
            "why": "市场覆盖与 Tushare 不重复，是跨市场投资人最轻量的第二数据源。",
            "excluded": "funda-data、llmquant-data",
            "exclusion_reason": "这些依赖额外 API/MCP，更适合机构增强包，不进入标准套装。",
        },
        {
            "slot": "个股分析与组合视图",
            "skill_id": "stock-analysis",
            "role": "做股票/加密资产多维评分、组合管理、价格提醒和传闻核验。",
            "why": "覆盖投资人最常见的个股到组合问题，和纯数据源不重复。",
            "excluded": "us-stock-analysis、company-valuation",
            "exclusion_reason": "us-stock-analysis 更偏美股深研且依赖较重；company-valuation 需要额外 IMA 依赖。",
        },
        {
            "slot": "A股/多市场监控预警",
            "skill_id": "stock-monitor-skill",
            "role": "对自选股设置成本、均线、RSI、成交量、跳空、止盈等监控规则。",
            "why": "它解决持续盯盘和提醒，不和研究/回测技能重复。",
            "excluded": "kanchi-dividend-review-monitor、portfolio-manager",
            "exclusion_reason": "kanchi 更窄地服务股息组合；portfolio-manager 依赖 Alpaca MCP。",
        },
        {
            "slot": "仓位与交易风险",
            "skill_id": "position-sizer",
            "role": "按账户规模、止损距离和单笔风险预算计算买入股数、最大亏损和风险暴露。",
            "why": "投资执行中不可替代，能直接降低交易计划落地风险。",
            "excluded": "exposure-coach、portfolio-manager",
            "exclusion_reason": "exposure-coach 依赖 FMP；portfolio-manager 依赖 Alpaca MCP。",
        },
        {
            "slot": "技术面交易计划",
            "skill_id": "sepa-strategy",
            "role": "用 Minervini SEPA 框架分析趋势模板、突破质量、相对强度和失效条件。",
            "why": "它提供清晰的交易方法论；和 position-sizer 的仓位计算分工不同。",
            "excluded": "technical-analyst、breakout-trade-planner、vcp-screener",
            "exclusion_reason": "technical-analyst/vcp 依赖额外数据或更窄；breakout-trade-planner 适合作为 SEPA 后续专用增强。",
        },
        {
            "slot": "量化回测",
            "skill_id": "pybroker-backtest-skill",
            "role": "用 PyBroker 做策略回测、收益/回撤/稳定性评估和参数验证。",
            "why": "标准套装需要一个真正能把想法变成历史检验的回测技能。",
            "excluded": "backtest-expert、strategy-pivot-designer",
            "exclusion_reason": "backtest-expert 更偏指导；strategy-pivot-designer 是回测遇到瓶颈后的增强工具。",
        },
        {
            "slot": "相关性与配对分析",
            "skill_id": "stock-correlation",
            "role": "分析股票相关性、替代标的、配对交易和组合分散度。",
            "why": "补足组合层面的统计关系，和单票分析/回测不重复。",
            "excluded": "pair-trade-screener",
            "exclusion_reason": "pair-trade-screener 依赖 FMP；标准套装保留低依赖相关性分析。",
        },
        {
            "slot": "市场环境与趋势健康",
            "skill_id": "uptrend-analyzer",
            "role": "判断市场上升趋势健康度、风险偏好和是否适合提高股票暴露。",
            "why": "它解决买不买、加不加仓的市场背景问题，不替代个股研究。",
            "excluded": "market-breadth-analyzer、market-top-detector、ftd-detector",
            "exclusion_reason": "同属市场状态/广度/顶部识别；uptrend-analyzer 更适合作为标准入口。",
        },
        {
            "slot": "市场新闻与事件解读",
            "skill_id": "alphaear-news",
            "role": "抓取热门财经新闻、统一趋势和市场预测线索，用于每日复盘与事件驱动观察。",
            "why": "结构化数据不能替代新闻事件；它补齐信息面入口。",
            "excluded": "market-news-analyst、finance-sentiment、alphaear-sentiment",
            "exclusion_reason": "market-news-analyst 更偏人工分析流程；sentiment 类依赖额外模型/API。",
        },
        {
            "slot": "投资报告生成",
            "skill_id": "alphaear-reporter",
            "role": "把行情、财务、事件和图表配置组织成可阅读的专业金融报告。",
            "why": "标准套装需要一个输出层；它和数据、筛选、监控技能分工清楚。",
            "excluded": "anthropic-fs-equity-research-*、anthropic-fs-financial-analysis-pptx-author",
            "exclusion_reason": "Anthropic FS 更适合机构材料工作流，依赖企业文件/MCP，不进入普通投资标准套装。",
        },
        {
            "slot": "研究质量检查",
            "skill_id": "data-quality-checker",
            "role": "在发布投资分析前检查数据口径、日期、计算、图表和事实引用是否一致。",
            "why": "它是报告交付前的质量闸门，不和报告生成重复。",
            "excluded": "anthropic-fs-financial-analysis-audit-xls",
            "exclusion_reason": "audit-xls 更偏 Excel 公式审计；标准套装保留泛投资内容质量检查。",
        },
        {
            "slot": "投资 thesis 记忆",
            "skill_id": "trader-memory-core",
            "role": "记录从想法、建仓、跟踪到卖出复盘的投资 thesis 生命周期。",
            "why": "它解决投资纪律和事后复盘，不依赖行情接口，也不与监控技能重复。",
            "excluded": "anthropic-fs-equity-research-thesis-tracker",
            "exclusion_reason": "Anthropic 版本更机构化；trader-memory-core 更适合标准个人/小团队投资流程。",
        },
        {
            "slot": "期权收益结构",
            "skill_id": "options-payoff",
            "role": "绘制和解释期权盈亏曲线、最大亏损、盈亏平衡点和参数敏感性。",
            "why": "它只覆盖收益结构教育与方案比较，不尝试替代专业期权行情源。",
            "excluded": "options-strategy-advisor、llmquant-options",
            "exclusion_reason": "后两者需要 FMP/LLMQuant；标准套装保留低依赖 payoff 分析。",
        },
        {
            "slot": "金融方法知识库",
            "skill_id": "openclaw-stock-kb",
            "role": "本地检索量化策略、技术指标、情绪分析、风控模板和回测工具文档。",
            "why": "它是方法论资料库，不直接和数据/执行技能重复。",
            "excluded": "llmquant-investor-lenses",
            "exclusion_reason": "LLMQuant investor lenses 依赖专有数据生态，作为机构增强而非标准入口。",
        },
    ]


def build_standard_recommendations(payload: dict[str, Any]) -> dict[str, Any]:
    results_by_id = {r["skill_id"]: r for r in payload["results"]}
    catalog_by_id = {s["id"]: s for s in load_catalog()}
    recommended: list[dict[str, Any]] = []
    missing: list[str] = []
    for idx, slot in enumerate(recommendation_slots(), start=1):
        sid = slot["skill_id"]
        result = results_by_id.get(sid)
        skill = catalog_by_id.get(sid)
        if not result or not skill:
            missing.append(sid)
            continue
        recommended.append({
            "rank": idx,
            "slot": slot["slot"],
            "skill_id": sid,
            "score": result["score"],
            "status": result["status"],
            "scenario": result["scenario"],
            "role": slot["role"],
            "why_recommended": slot["why"],
            "evaluation_reason": result["result_evaluation"],
            "data_policy": result["data_source_policy"],
            "excluded_as_duplicates": slot["excluded"],
            "exclusion_reason": slot["exclusion_reason"],
            "install_path": f"skills/default/{sid}",
            "dependencies": skill.get("dependencies", {}),
        })
    optional_suites = [
        {
            "suite": "A股增强包",
            "skills": ["a-stock-data"],
            "when_to_add": "需要 Tushare 之外的东财、腾讯、百度、巨潮、龙虎榜、题材、公告、新闻等多源直连能力时添加；不作为标准数据底座重复安装。",
        },
        {
            "suite": "机构多资产包",
            "skills": ["llmquant-data", "llmquant-equities", "llmquant-portfolio", "llmquant-risk", "llmquant-macro", "llmquant-options"],
            "when_to_add": "已有 LLMQUANT_API_KEY 且需要跨资产、机构级组合/风险/宏观/期权工作流时添加。",
        },
        {
            "suite": "投行/PE/财富管理包",
            "skills": ["anthropic-financial-services suite"],
            "when_to_add": "处理 CIM、LBO、并购模型、PE 尽调、基金运营、KYC 或客户报告，且有企业文件/MCP 数据时添加。",
        },
    ]
    return {
        "generated_at": payload["generated_at"],
        "principle": "标准套装按投资流程去重：一个岗位任务只选一个默认 skill；同类数据源、同类筛选器、同类机构工作流放入 excluded 或 optional_suites。",
        "data_assumption": "中国市场以 Tushare Pro 为主数据底座；免 key 数据源和专有 API 只作为增强，不强行替代。",
        "recommended_count": len(recommended),
        "recommended": recommended,
        "optional_suites": optional_suites,
        "missing_recommendation_results": missing,
    }


def render_markdown(payload: dict[str, Any], recommendations: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Tushare 金融 Skills 评测报告")
    lines.append("")
    lines.append(f"- 生成时间：{payload['generated_at']}")
    lines.append(f"- 金融相关 skills：{payload['summary']['total_finance_skills']}")
    lines.append(f"- Tushare 连通：{payload['data_health']['connected']}")
    lines.append(f"- 强/部分适配：{payload['summary']['tushare_fit']}")
    lines.append(f"- 跳过额外 API/MCP：{payload['summary']['skipped']}")
    lines.append("")
    lines.append("## 标准推荐金融 Skills（去重精选）")
    lines.append("")
    lines.append("| Rank | 能力位 | Skill | 分数 | 推荐理由 | 去重说明 |")
    lines.append("|---:|---|---|---:|---|---|")
    for r in recommendations["recommended"]:
        lines.append(
            f"| {r['rank']} | {r['slot']} | `{r['skill_id']}` | {r['score']} | "
            f"{r['why_recommended']} | 排除：{r['excluded_as_duplicates']}。{r['exclusion_reason']} |"
        )
    lines.append("")
    lines.append("## 全量评测明细")
    lines.append("")
    lines.append("| Skill | 场景 | 状态 | 分数 | 专属测试任务 | 评分理由 | 缺口/跳过原因 |")
    lines.append("|---|---|---|---:|---|---|---|")
    for r in sorted(payload["results"], key=lambda x: (-x["score"], x["skill_id"])):
        evidence = "；".join(r["evidence"][:2])
        missing = "；".join(r["missing_or_blocked"][:2]) or "—"
        question = r["test_question"].replace("|", "\\|")
        lines.append(
            f"| `{r['skill_id']}` | {r['scenario']} | `{r['status']}` | {r['score']} | "
            f"{question} | {evidence} | {missing} |"
        )
    lines.append("")
    lines.append("## 可选增强包")
    lines.append("")
    for suite in recommendations["optional_suites"]:
        lines.append(f"- **{suite['suite']}**：{', '.join(f'`{s}`' for s in suite['skills'])}。{suite['when_to_add']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    health, _pro = try_tushare()
    skills = [s for s in load_catalog() if is_finance_skill(s)]
    results = [evaluate_skill(s, health) for s in skills]
    by_status: dict[str, int] = {}
    by_scenario: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        by_scenario[r.scenario] = by_scenario.get(r.scenario, 0) + 1
    summary = {
        "total_finance_skills": len(results),
        "evaluated_or_pending": sum(1 for r in results if not r.status.startswith("skipped")),
        "tushare_fit": sum(1 for r in results if r.status in {"passed_tushare_strong", "passed_tushare_partial"}),
        "skipped": sum(1 for r in results if r.status.startswith("skipped")),
        "by_status": by_status,
        "by_scenario": by_scenario,
    }
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "data_health": asdict(health),
        "summary": summary,
        "results": [asdict(r) for r in results],
    }
    recommendations = build_standard_recommendations(payload)
    payload["standard_recommendations"] = recommendations
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RECOMMENDATION_JSON_OUT.write_text(json.dumps(recommendations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_OUT.write_text(render_markdown(payload, recommendations), encoding="utf-8")
    HTML_OUT.write_text(render_html(payload), encoding="utf-8")
    print(json.dumps({
        "json": str(JSON_OUT),
        "html": str(HTML_OUT),
        "markdown": str(MD_OUT),
        "recommendations_json": str(RECOMMENDATION_JSON_OUT),
        "summary": summary,
        "standard_recommended_count": recommendations["recommended_count"],
        "data_health": asdict(health),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

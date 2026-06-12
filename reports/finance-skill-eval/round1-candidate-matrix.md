# Finance Skill Evaluation Candidate Matrix

本文件是第一轮候选分组，不做最终取舍。每组先明确测试问题、候选、依赖和测试方式，后续评测报告只在同一能力位内择优。

## 测试方式

| 测试方式 | 含义 |
|---|---|
| `live` | 当前环境可直接运行或可用公开数据验证 |
| `dry-run` | 可检查流程、脚本、输出格式，但不能取真实外部数据 |
| `api-gated` | 需要 API Key 才能有效评测 |
| `mcp-gated` | 需要 MCP 服务配置才可有效评测 |
| `model-graded` | 主要评估 skill 指令能否让 Agent 输出合格分析 |

## 候选分组

| 能力位 | 候选 skills | 测试方式 | 备注 |
|---|---|---|---|
| A 股全栈数据 | `a-stock-data`, `akshare-stock`, `tushare-openclaw-skill`, `openclaw-stock-data-skill` | `live` / `api-gated` | 优先看是否能覆盖行情、研报、资金面、公告、财务。 |
| 美股/全球数据 | `yfinance-data`, `funda-data`, `llmquant-data` | `live` / `api-gated` / `mcp-gated` | `yfinance-data` 可直接测，`funda-data` 与 `llmquant-data` 需密钥/MCP。 |
| SEC / 13F / 机构研究 | `llmquant-data`, `funda-data`, `institutional-flow-tracker` | `api-gated` / `mcp-gated` | 重点测文件/持仓证据、滞后性声明和 crowded trade 判断。 |
| 宏观与政策 | `llmquant-macro`, `macro-regime-detector`, `policy-monitor`, `economic-calendar-fetcher` | `api-gated` / `mcp-gated` / `model-graded` | 政策和宏观不能只看摘要，要测传导链。 |
| 市场情绪与事件 | `llmquant-events`, `llmquant-market-intelligence`, `theme-detector`, `market-news-analyst`, `finance-sentiment` | `api-gated` / `mcp-gated` / `model-graded` | 重点看事实、情绪、交易结论是否分离。 |
| 股票基本面与估值 | `us-stock-analysis`, `company-valuation`, `estimate-analysis`, `earnings-preview`, `earnings-recap` | `live` / `api-gated` / `model-graded` | 检查是否覆盖商业质量、估值、预期修正和风险。 |
| 技术分析与交易计划 | `technical-analyst`, `breakout-trade-planner`, `vcp-screener`, `canslim-screener`, `sepa-strategy` | `api-gated` / `model-graded` | 重点看入场、止损、加仓、失效条件。 |
| 股息与价值 | `value-dividend-screener`, `dividend-growth-pullback-screener`, `kanchi-dividend-sop`, `kanchi-dividend-review-monitor` | `api-gated` / `model-graded` | 测股息增长、估值、安全边际、复查机制。 |
| 期权策略 | `options-strategy-advisor`, `options-payoff`, `llmquant-options` | `api-gated` / `mcp-gated` / `model-graded` | 测 payoff、最大亏损、波动率暴露、适用/不适用场景。 |
| 回测与策略验证 | `pybroker-backtest-skill`, `backtest-expert`, `edge-strategy-reviewer`, `data-quality-checker` | `live` / `model-graded` | 区分回测执行引擎、方法论审查、数据质量检查。 |
| 组合、仓位与风险 | `portfolio-manager`, `position-sizer`, `llmquant-portfolio`, `llmquant-risk`, `exposure-coach`, `trader-memory-core` | `api-gated` / `mcp-gated` / `model-graded` | 测仓位计算、风险预算、集中度、复查规则。 |
| 自选股监控 | `stock-monitor-skill`, `llmquant-portfolio`, `trader-memory-core` | `live` / `mcp-gated` / `model-graded` | 测价格、技术面、事件和 thesis 失效监控。 |
| 市场宽度与顶部/底部 | `market-breadth-analyzer`, `uptrend-analyzer`, `market-top-detector`, `ftd-detector`, `ibd-distribution-day-monitor` | `live` / `api-gated` / `model-graded` | 重点看是否能形成可解释评分和仓位触发条件。 |
| 社媒与市场情报 | `opencli-reader`, `twitter-reader`, `telegram-reader`, `discord-reader`, `linkedin-reader` | `dry-run` / `model-graded` | 先验证只读边界、事实/情绪/谣言分离。 |
| 创业投资研究 | `startup-analysis`, `yc-reader` | `live` / `model-graded` | 测 VC、求职者、创始人多视角和缺失信息识别。 |

## 第一轮淘汰规则

1. 同组中如果两个 skills 依赖更重但覆盖面没有更强，先降级为备选。
2. 只做 prompt 模板、没有数据口径、没有输出结构的，除非很独特，否则不进入核心套件。
3. API/MCP 技能不因当前缺密钥直接淘汰，但必须在 dry-run 中证明流程清楚、数据契约明确。
4. 如果一个 skill 只适合专家场景，进入 `finance-lab` 备选，不进入 `finance-core`。
5. 最终套件保留目标：核心 20-30 个；每个能力位最多 1-2 个。

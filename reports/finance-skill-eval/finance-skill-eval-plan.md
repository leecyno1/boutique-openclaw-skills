# Finance Skill Evaluation Plan

本评测用于从当前仓库金融、投资、股票相关 skills 中择优形成一个低重复、高可用的金融套件。核心原则是先测目标达成效果，再决定保留、合并、降级或排除。

## 评测目标

1. 不按简介直接取舍，按任务表现选出每个能力位的最佳 skill。
2. 每个能力位只保留 1 个主力；不同市场、不同数据源或不同工作流才允许共存。
3. 明确区分直接可用、需要 API Key、需要 MCP、需要浏览器或外部工具的能力。
4. 对无法实测的 API/MCP 技能做 dry-run 和说明质量评估，待密钥可用后再做 live run。

## 评分规则

每个 skill 在对应任务中按 100 分评分：

| 维度 | 分值 | 说明 |
|---|---:|---|
| 目标命中 | 30 | 是否直接覆盖用户问题，不跑题、不泛泛而谈 |
| 输出结构 | 15 | 是否给出清晰表格、步骤、结论、风险提示 |
| 数据/证据要求 | 20 | 是否明确数据来源、字段、时间范围、缺失数据处理 |
| 可执行性 | 15 | 是否能被 Agent 直接执行，是否包含命令、脚本或明确流程 |
| 依赖成本 | 10 | direct 优于 API/MCP；依赖越少越高 |
| 去重价值 | 10 | 与同组其他 skills 相比是否有不可替代价值 |

判定：

| 分数 | 结论 |
|---:|---|
| 85-100 | 核心保留 |
| 70-84 | 可保留，但需要明确场景 |
| 55-69 | 备选或并入其他 skill |
| <55 | 排除 |

## 能力位与测试题

### 1. A 股全栈数据

候选：`a-stock-data`, `akshare-stock`, `tushare-openclaw-skill`, `openclaw-stock-data-skill`

测试题：

> 请分析贵州茅台最近 120 日走势、北向资金、龙虎榜/大宗交易/解禁/股东户数变化，并给出 3 条可验证的后续跟踪指标。

成功标准：
- 能明确 A 股代码、数据口径和时间范围。
- 能覆盖行情、资金面、事件/公告、基本面或研报。
- 能说明无法获取的数据项，而不是编造。

### 2. 美股/全球市场数据

候选：`yfinance-data`, `funda-data`, `llmquant-data`

测试题：

> 请比较 AAPL、MSFT、NVDA 最近 1 年价格表现、估值、盈利增速、分红/回购和主要风险，并给出一张对比表。

成功标准：
- 能处理多 ticker 对比。
- 能区分价格数据、财务数据和分析推断。
- 能明确数据源和数据新鲜度。

### 3. SEC / 13F / 机构研究

候选：`llmquant-data`, `funda-data`, `institutional-flow-tracker`

测试题：

> 请基于最近 10-K 和 13F 信息，分析 NVDA 的核心风险、主要机构持仓变化和可能的 crowded trade 风险。

成功标准：
- 明确 SEC 文件、报告期、13F 滞后性。
- 区分公司披露风险和分析推断。
- 能形成机构拥挤度或持仓变化判断。

### 4. 宏观与政策

候选：`llmquant-macro`, `macro-regime-detector`, `policy-monitor`, `economic-calendar-fetcher`

测试题：

> 请评估未来 3 个月美联储政策、美元、长端利率和科技股估值之间的主要传导链，并列出下周最重要的宏观数据。

成功标准：
- 有宏观传导链，而不是新闻摘要。
- 能列出关键数据、观察日期或日历来源。
- 能给出对权益资产的情景化影响。

### 5. 市场情绪与事件

候选：`llmquant-events`, `llmquant-market-intelligence`, `theme-detector`, `market-news-analyst`, `finance-sentiment`

测试题：

> 请识别本周美股最重要的 3 个市场主题，分别说明驱动事件、受益/受损板块、可观察确认信号和反证信号。

成功标准：
- 能把事件归纳成主题。
- 能给出确认/反证信号。
- 能区分事实、情绪和交易结论。

### 6. 股票基本面与估值

候选：`us-stock-analysis`, `company-valuation`, `estimate-analysis`, `earnings-preview`, `earnings-recap`

测试题：

> 请分析 META 当前投资价值：商业质量、收入/利润趋势、估值、预期修正、主要风险，最后给出买入/观望/回避的条件。

成功标准：
- 覆盖基本面、估值、预期和风险。
- 输出有结论条件，而不是直接荐股。
- 对缺失数据有说明。

### 7. 技术分析与交易计划

候选：`technical-analyst`, `breakout-trade-planner`, `vcp-screener`, `canslim-screener`, `sepa-strategy`

测试题：

> 请用 Minervini/趋势交易框架评估一只处在 52 周高位附近、成交量收缩、均线多头排列的股票，给出入场、止损、加仓和失效条件。

成功标准：
- 能形成明确交易计划。
- 有风险控制和失效条件。
- 不把形态判断和事实数据混淆。

### 8. 股息与价值

候选：`value-dividend-screener`, `dividend-growth-pullback-screener`, `kanchi-dividend-sop`, `kanchi-dividend-review-monitor`

测试题：

> 请构建一套美股股息增长股筛选规则，要求兼顾估值、股息增长、现金流安全边际和回撤后的买点。

成功标准：
- 有可执行筛选条件。
- 能说明股息陷阱和税务/账户影响。
- 能给出复查机制。

### 9. 期权策略

候选：`options-strategy-advisor`, `options-payoff`, `llmquant-options`

测试题：

> 假设某股票财报前 IV 偏高、方向不确定，请比较卖跨式、铁鹰、买跨式和保护性看跌的适用条件、最大风险和盈亏结构。

成功标准：
- 明确 payoff、最大亏损、波动率暴露。
- 能区分方向性和波动率策略。
- 有风险控制和不适用场景。

### 10. 回测与策略验证

候选：`pybroker-backtest-skill`, `backtest-expert`, `edge-strategy-reviewer`, `data-quality-checker`

测试题：

> 请设计一个 20 日突破策略的回测方案，要求说明数据清洗、滑点、交易成本、训练/验证切分、过拟合防控和评价指标。

成功标准：
- 有完整回测流程。
- 能指出常见偏差。
- 能给出可执行实验结构。

### 11. 组合、仓位与风险

候选：`portfolio-manager`, `position-sizer`, `llmquant-portfolio`, `llmquant-risk`, `exposure-coach`, `trader-memory-core`

测试题：

> 我有 10 只股票组合，单只最大亏损不超过总资金 1%，同时希望控制科技股集中度。请给出仓位、风险预算和复查规则。

成功标准：
- 有仓位计算和组合层面约束。
- 有集中度、相关性或行业暴露处理。
- 有复查/止损/降风险机制。

### 12. 自选股监控

候选：`stock-monitor-skill`, `llmquant-portfolio`, `trader-memory-core`

测试题：

> 请为 8 只自选股设计监控规则，覆盖价格突破、均线、RSI、成交量异动、财报事件和 thesis 失效。

成功标准：
- 有具体阈值规则。
- 能区分价格预警和基本面预警。
- 能输出可执行的监控清单。

### 13. 市场宽度与顶部/底部

候选：`market-breadth-analyzer`, `uptrend-analyzer`, `market-top-detector`, `ftd-detector`, `ibd-distribution-day-monitor`

测试题：

> 请判断当前市场是否适合提高权益仓位：结合市场宽度、龙头股表现、分布日、VIX 和指数趋势给出评分。

成功标准：
- 不是只看指数涨跌。
- 能形成可解释评分。
- 有升/降仓位触发条件。

### 14. 社媒与市场情报

候选：`opencli-reader`, `twitter-reader`, `telegram-reader`, `discord-reader`, `linkedin-reader`

测试题：

> 请收集市场对 NVDA 财报的社媒讨论，区分事实、情绪、谣言和可验证线索。

成功标准：
- 只读，不执行发布/互动。
- 能区分社媒情绪与事实证据。
- 能给出后续验证来源。

### 15. 创业投资研究

候选：`startup-analysis`, `yc-reader`

测试题：

> 请评估一家 YC AI infra 初创公司是否值得投资或加入，从市场、产品、团队、竞争和融资风险五个角度给出判断。

成功标准：
- 同时覆盖投资人和求职者视角。
- 能识别缺失信息。
- 不把创业宣传语当事实。

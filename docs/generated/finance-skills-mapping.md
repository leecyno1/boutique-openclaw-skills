# 金融 Skills 投资场景映射

> 当前基于 `catalog/skills.enriched.json` 生成。标准组合已暂时取消金融 skills；金融能力建议通过 profile / suite / 单技能按需安装。

- 金融相关 skills 数量：`163`
- 推荐原则：先装数据源，再按投资流程补研究、筛选、风控、报告；机构金融/投行/PE/固收类单独作为专业套件使用。

## 投资场景 Mapping

| 场景 | 推荐 Skills | 适配说明 |
|---|---|---|
| 基础数据/行情/财报 | `a-stock-data`, `akshare-stock`, `tushare-openclaw-skill`, `openclaw-stock-data-skill`, `yfinance-data`, `llmquant-data`, `funda-data`, `anthropic-fs-lseg-equity-research`, `anthropic-fs-spglobal-tear-sheet` | 先选数据源。A股优先 a-stock-data；美股/全球轻量用 yfinance-data；机构数据用 LLMQuant/Funda/LSEG/S&P。 |
| 每日市场复盘/宏观环境 | `stock-daily-analysis-skill`, `alphaear-news`, `llmquant-macro`, `llmquant-market-intelligence`, `market-environment-analysis`, `macro-regime-detector`, `economic-calendar-fetcher`, `policy-monitor`, `hormuz-strait` | 适合开盘前/收盘后形成市场温度、宏观驱动、政策风险和事件日历。 |
| 个股深度研究/估值 | `stock-analysis`, `us-stock-analysis`, `company-valuation`, `llmquant-equities`, `anthropic-fs-equity-research-initiating-coverage`, `anthropic-fs-financial-analysis-dcf-model`, `anthropic-fs-financial-analysis-comps-analysis`, `anthropic-fs-lseg-equity-research` | 从数据、商业质量、估值、同业比较到研究报告全链路。 |
| 选股/机会发现 | `finviz-screener`, `canslim-screener`, `vcp-screener`, `value-dividend-screener`, `dividend-growth-pullback-screener`, `anthropic-fs-equity-research-idea-generation`, `llmquant-investor-lenses`, `theme-detector` | 把候选池筛出来，再交给研究/估值/风控模块。 |
| 技术面/交易计划 | `technical-analyst`, `sepa-strategy`, `breakout-trade-planner`, `position-sizer`, `uptrend-analyzer`, `market-breadth-analyzer`, `market-top-detector`, `ftd-detector`, `ibd-distribution-day-monitor` | 适合择时、仓位、突破计划、市场健康度判断。 |
| 财报/事件驱动 | `earnings-calendar`, `earnings-preview`, `earnings-recap`, `earnings-trade-analyzer`, `pead-screener`, `llmquant-events`, `anthropic-fs-equity-research-earnings-preview`, `anthropic-fs-equity-research-earnings-analysis`, `anthropic-fs-spglobal-earnings-preview-beta` | 适合财报前准备、财报后复盘、PEAD 和事件催化。 |
| 组合管理/监控/风控 | `portfolio-manager`, `stock-monitor-skill`, `trader-memory-core`, `llmquant-portfolio`, `llmquant-portfolio-lab`, `llmquant-risk`, `anthropic-fs-equity-research-thesis-tracker`, `anthropic-fs-private-equity-portfolio-monitoring` | 用于持仓跟踪、 thesis 生命周期、暴露、情景模拟、预警。 |
| 量化研究/回测/策略迭代 | `backtest-expert`, `pybroker-backtest-skill`, `trade-hypothesis-ideator`, `edge-candidate-agent`, `edge-hint-extractor`, `signal-postmortem`, `pair-trade-screener`, `stock-correlation` | 从想法、假设、回测、相关性/配对、交易后验复盘形成闭环。 |
| 期权/衍生品/利率外汇固收 | `options-payoff`, `options-strategy-advisor`, `llmquant-options`, `llmquant-equity-derivatives`, `llmquant-rates-fx`, `llmquant-credit`, `llmquant-commodities`, `anthropic-fs-lseg-option-vol-analysis`, `anthropic-fs-lseg-swap-curve-strategy`, `anthropic-fs-lseg-fx-carry-trade`, `anthropic-fs-lseg-bond-relative-value`, `anthropic-fs-lseg-fixed-income-portfolio` | 专业资产类别；多数需要数据/MCP。 |
| 投行/PE/机构材料 | `anthropic-fs-investment-banking-teaser`, `anthropic-fs-investment-banking-cim-builder`, `anthropic-fs-investment-banking-buyer-list`, `anthropic-fs-investment-banking-merger-model`, `anthropic-fs-private-equity-deal-screening`, `anthropic-fs-private-equity-ic-memo`, `anthropic-fs-private-equity-returns-analysis`, `anthropic-fs-financial-analysis-lbo-model` | 适合并购、路演、尽调、IC memo、LBO、买方名单等机构工作流。 |
| 基金运营/合规/KYC | `anthropic-fs-fund-admin-gl-recon`, `anthropic-fs-fund-admin-nav-tieout`, `anthropic-fs-fund-admin-break-trace`, `anthropic-fs-fund-admin-variance-commentary`, `anthropic-fs-operations-kyc-doc-parse`, `anthropic-fs-operations-kyc-rules` | 后台运营、对账、NAV、月结、KYC/AML，不是普通二级市场投资必装。 |
| 报告/可视化/知识库 | `openclaw-stock-kb`, `alphaear-reporter`, `alphaear-logic-visualizer`, `data-quality-checker`, `anthropic-fs-financial-analysis-xlsx-author`, `anthropic-fs-financial-analysis-pptx-author`, `anthropic-fs-financial-analysis-audit-xls`, `anthropic-fs-financial-analysis-ib-check-deck` | 把分析变成可交付报告、图表、Excel/PPT，并做质量校验。 |

## 按类别完整清单

### coding-devtools

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `backtest-expert` | 5★ | `direct` | 无 | Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing, or validating quantitative trading str |

### data-analysis

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `edge-signal-aggregator` | 5★ | `direct` | 无 | Aggregate and rank signals from multiple edge-finding skills (edge-candidate-agent, theme-detector, sector-analyst, institutional-flow-tracker) into a |

### finance-data

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `a-stock-data` | 4★ | `direct` | 无 | A股全栈数据工具包 — 覆盖行情(mootdx+腾讯+百度K线)、研报(东财+同花顺+iwencai)、信号(同花顺热点+北向+龙虎榜+解禁+行业)、资金面(融资融券+大宗交易+股东户数+分红+资金流分钟级+资金流120日)、新闻(东财个股+全球资讯)、基础数据(mootdx财务/F10+东财+新浪 |
| `akshare-stock` | 4★ | `direct` | 无 | A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。用于回答关于A股股票查询、行情数据、财务分析、选股等问题。 |
| `anthropic-fs-lseg-bond-futures-basis` | 3★ | `mcp-required` | 无 | Analyze the bond futures basis by pricing futures, identifying the cheapest-to-deliver, and comparing with yield curves to assess delivery option valu |
| `anthropic-fs-lseg-bond-relative-value` | 3★ | `mcp-required` | 无 | Perform relative value analysis on bonds by combining pricing, yield curve context, credit spreads, and scenario stress testing. Use when analyzing bo |
| `anthropic-fs-lseg-equity-research` | 3★ | `mcp-required` | 无 | Generate comprehensive equity research snapshots combining analyst consensus estimates, company fundamentals, historical prices, and macroeconomic con |
| `anthropic-fs-lseg-fixed-income-portfolio` | 3★ | `mcp-required` | 无 | Review fixed income portfolios by pricing multiple bonds, retrieving reference data, analyzing cashflows, and running scenario analysis. Use when revi |
| `anthropic-fs-lseg-fx-carry-trade` | 3★ | `mcp-required` | 无 | Evaluate FX carry trade opportunities by combining spot rates, forward points, interest rate differentials, volatility surface analysis, and historica |
| `anthropic-fs-lseg-macro-rates-monitor` | 3★ | `mcp-required` | 无 | Build macroeconomic and rates dashboards combining macro indicators, yield curves, inflation breakevens, and swap rates. Use when monitoring macro con |
| `anthropic-fs-lseg-option-vol-analysis` | 3★ | `mcp-required` | 无 | Analyze option volatility by combining vol surface data, option pricing with Greeks, and historical price data to assess implied vs realized volatilit |
| `anthropic-fs-lseg-swap-curve-strategy` | 3★ | `mcp-required` | 无 | Analyze the interest rate swap curve by pricing swaps at multiple tenors, overlaying government and inflation curves, and identifying curve trade oppo |
| `anthropic-fs-spglobal-earnings-preview-beta` | 3★ | `mcp-required` | 无 | Generate a concise 4-5 page equity research earnings preview for a single company. Analyzes the most recent earnings transcript, competitor landscape, |
| `anthropic-fs-spglobal-funding-digest` | 3★ | `mcp-required` | 无 | Generate a polished one-page PowerPoint slide summarizing key takeaways from recent funding rounds and notable capital markets activity across a user' |
| `anthropic-fs-spglobal-tear-sheet` | 3★ | `mcp-required` | 无 | Generate professional company tear sheets using S&P Capital IQ data via the Kensho LLM-ready API MCP server. Use this skill whenever the user asks for |
| `funda-data` | 4★ | `api-key+mcp-required` | `FUNDA_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID` | Query Funda AI financial data via two surfaces: the MCP server at https://funda.ai/api/mcp for analyst-grade research synthesis (DCF, comps, earnings  |
| `llmquant-data` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant Data primitive workflows. Use when the user needs SEC filings, 13F holders, macro snapshots, or source-grounded macro briefs |
| `llmquant-etfs` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant ETFs workflows. Use when the user needs ETF holdings, overlap, concentration, issuer snapshot, or theme exposure analysis. |
| `openclaw-stock-data-skill` | 4★ | `api-key` | `STOCK_API_KEY` | 使用 data.diemeng.chat 提供的接口查询股票日线、分钟线、财务指标等数据，支持 A 股等市场。 |
| `tushare-openclaw-skill` | 4★ | `api-key` | `TUSHARE_TOKEN` | Tushare Pro 金融数据 API 查询助手。用于帮助用户查询中国股票、基金、期货、债券等金融数据。当用户需要获取股票行情、财务数据、基础信息、宏观经济数据时使用此 skill。 |
| `yfinance-data` | 4★ | `direct` | 无 | Fetch financial and market data using the yfinance Python library. Use this skill whenever the user asks for stock prices, historical data, financial  |

### finance-knowledge

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `llmquant-investor-lenses` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant investor-lens workflows. Use when the user wants an investor-style reasoning overlay grounded in LLMQuant Data evidence. |
| `openclaw-stock-kb` | 5★ | `direct` | 无 | 开源股票研究知识库封装技能。内含量化策略、技术指标、社媒情绪分析、风控模板和回测工具文档。适用于让 Agent 在本地检索股票研究方法、设计分析框架、撰写策略说明、整理指标解释和风控规则时引用。 |

### finance-monitor

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `llmquant-events` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant event workflows. Use when the user needs earnings event briefs, M&A tracking, regulatory risk, catalysts, event calendars, o |
| `llmquant-macro` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant macro workflows. Use when the user needs macro dashboards, Fed or central-bank previews, inflation and growth context, liqui |
| `llmquant-market-intelligence` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant market-intelligence workflows. Use when the user needs macro views, market sentiment dashboards, or event probability signal |
| `llmquant-portfolio` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant portfolio workflows. Use when the user needs company profiles, thesis tracking, theme research, watchlist monitoring, or ale |
| `llmquant-portfolio-lab` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant portfolio-lab workflows. Use when the user needs portfolio exposure maps, what-if simulations, scenario states, or virtual p |
| `llmquant-rates-fx` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant rates and FX workflows. Use when the user needs yield curve, duration, central-bank divergence, FX carry, real-rate, dollar, |
| `llmquant-risk` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant risk workflows. Use when the user needs fear scoring, VIX regime, hedge design, or research health checks. |
| `stock-monitor-skill` | 4★ | `direct` | 无 | 全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。 |

### finance-services

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `anthropic-fs-equity-research-catalyst-calendar` | 3★ | `mcp-required` | 无 | Build and maintain a calendar of upcoming catalysts across a coverage universe — earnings dates, conferences, product launches, regulatory decisions,  |
| `anthropic-fs-equity-research-earnings-analysis` | 3★ | `mcp-required` | 无 | Create professional equity research earnings update reports (8-12 pages, 3,000-5,000 words) analyzing quarterly results for companies already under co |
| `anthropic-fs-equity-research-earnings-preview` | 3★ | `mcp-required` | 无 | Build pre-earnings analysis with estimate models, scenario frameworks, and key metrics to watch. Use before a company reports quarterly earnings to pr |
| `anthropic-fs-equity-research-idea-generation` | 3★ | `mcp-required` | 无 | Systematic stock screening and investment idea sourcing. Combines quantitative screens, thematic research, and pattern recognition to surface new long |
| `anthropic-fs-equity-research-initiating-coverage` | 3★ | `mcp-required` | 无 | Create institutional-quality equity research initiation reports through a 5-task workflow. Tasks must be executed individually with verified prerequis |
| `anthropic-fs-equity-research-model-update` | 3★ | `mcp-required` | 无 | Update financial models with new data — quarterly earnings, management guidance, macro changes, or revised assumptions. Adjusts estimates, recalculate |
| `anthropic-fs-equity-research-morning-note` | 3★ | `mcp-required` | 无 | Draft concise morning meeting notes summarizing overnight developments, trade ideas, and key events for coverage stocks. Designed for the 7am morning  |
| `anthropic-fs-equity-research-sector-overview` | 3★ | `mcp-required` | 无 | Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use fo |
| `anthropic-fs-equity-research-thesis-tracker` | 3★ | `mcp-required` | 无 | Maintain and update investment theses for portfolio positions and watchlist names. Track key data points, catalysts, and thesis milestones over time.  |
| `anthropic-fs-financial-analysis-3-statement-model` | 3★ | `mcp-required` | 无 | Complete, populate and fill out 3-statement financial model templates (Income Statement, Balance Sheet, Cash Flow Statement) . Use when asked to fill  |
| `anthropic-fs-financial-analysis-audit-xls` | 3★ | `mcp-required` | 无 | Audit a spreadsheet for formula accuracy, errors, and common mistakes. Scopes to a selected range, a single sheet, or the entire model (including fina |
| `anthropic-fs-financial-analysis-clean-data-xls` | 3★ | `mcp-required` | 无 | Clean up messy spreadsheet data — trim whitespace, fix inconsistent casing, convert numbers-stored-as-text, standardize dates, remove duplicates, and  |
| `anthropic-fs-financial-analysis-competitive-analysis` | 3★ | `mcp-required` | 无 | Framework for building competitive landscape decks — market positioning, competitor deep-dives, comparative analysis, strategic synthesis. Use when th |
| `anthropic-fs-financial-analysis-comps-analysis` | 3★ | `mcp-required` | 无 | Build institutional-grade comparable company analyses with operating metrics, valuation multiples, and statistical benchmarking in Excel/spreadsheet f |
| `anthropic-fs-financial-analysis-dcf-model` | 3★ | `mcp-required` | 无 | Real DCF (Discounted Cash Flow) model creation for equity valuation. Retrieves financial data from SEC filings and analyst reports, builds comprehensi |
| `anthropic-fs-financial-analysis-deck-refresh` | 3★ | `mcp-required` | 无 | Updates a presentation with new numbers — quarterly refreshes, earnings updates, comp rolls, rebased market data. Use whenever the user asks to "updat |
| `anthropic-fs-financial-analysis-ib-check-deck` | 3★ | `mcp-required` | 无 | Investment banking presentation quality checker. Reviews a pitch deck or client-ready presentation for (1) number consistency across slides, (2) data- |
| `anthropic-fs-financial-analysis-lbo-model` | 3★ | `mcp-required` | 无 | This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investme |
| `anthropic-fs-financial-analysis-ppt-template-creator` | 3★ | `mcp-required` | 无 | Creates self-contained PPT template SKILLS (not presentations) from user-provided PowerPoint templates. Use ONLY when a user wants to create a reusabl |
| `anthropic-fs-financial-analysis-pptx-author` | 3★ | `mcp-required` | 无 | Produce a .pptx file on disk (headless) instead of driving a live PowerPoint document — for managed-agent sessions with no open Office app. |
| `anthropic-fs-financial-analysis-skill-creator` | 3★ | `mcp-required` | 无 | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude |
| `anthropic-fs-financial-analysis-xlsx-author` | 3★ | `mcp-required` | 无 | Produce a .xlsx file on disk (headless) instead of driving a live Excel workbook — for managed-agent sessions with no open Office app. |
| `anthropic-fs-fund-admin-accrual-schedule` | 3★ | `mcp-required` | 无 | Build the period-end accrual schedule — for each accrual, compute the entry, cite the support, and draft the JE. Use during month-end close; the JE is |
| `anthropic-fs-fund-admin-break-trace` | 3★ | `mcp-required` | 无 | Root-cause a reconciliation break to its source transaction or posting — follow the audit trail from the break row back to the originating entry on ea |
| `anthropic-fs-fund-admin-gl-recon` | 3★ | `mcp-required` | 无 | Reconcile general ledger to subledger for a trade date or period — match at the position or transaction level, surface breaks, and classify each break |
| `anthropic-fs-fund-admin-nav-tieout` | 3★ | `mcp-required` | 无 | Tie an LP statement to the fund's NAV pack — recompute the LP's capital account from the NAV components and flag any line that doesn't agree. Use befo |
| `anthropic-fs-fund-admin-roll-forward` | 3★ | `mcp-required` | 无 | Build a roll-forward schedule for a balance-sheet account — beginning balance plus activity less reversals equals ending balance, with each component  |
| `anthropic-fs-fund-admin-variance-commentary` | 3★ | `mcp-required` | 无 | Write flux commentary for every P&L and balance-sheet line over threshold — current vs prior period and vs budget, with the driver explained from unde |
| `anthropic-fs-investment-banking-buyer-list` | 3★ | `mcp-required` | 无 | Build and organize a universe of potential acquirers for sell-side M&A processes. Identifies strategic and financial buyers, assesses fit, and priorit |
| `anthropic-fs-investment-banking-cim-builder` | 3★ | `mcp-required` | 无 | Structure and draft a Confidential Information Memorandum for sell-side M&A processes. Organizes company information into a professional, investor-rea |
| `anthropic-fs-investment-banking-datapack-builder` | 3★ | `mcp-required` | 无 | Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. E |
| `anthropic-fs-investment-banking-deal-tracker` | 3★ | `mcp-required` | 无 | Track multiple live deals with milestones, deadlines, action items, and status updates. Maintains a deal pipeline view and surfaces upcoming deadlines |
| `anthropic-fs-investment-banking-merger-model` | 3★ | `mcp-required` | 无 | Build accretion/dilution analysis for M&A transactions. Models pro forma EPS impact, synergy sensitivities, and purchase price allocation. Use when ev |
| `anthropic-fs-investment-banking-pitch-deck` | 3★ | `mcp-required` | 无 | Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has sour |
| `anthropic-fs-investment-banking-process-letter` | 3★ | `mcp-required` | 无 | Draft process letters and bid instructions for sell-side M&A processes. Covers initial indication of interest (IOI) instructions, final bid procedures |
| `anthropic-fs-investment-banking-strip-profile` | 3★ | `mcp-required` | 无 | Creates professional investment banking strip profiles (company profiles) for pitch books, deal materials, and client presentations. Generates 1-4 inf |
| `anthropic-fs-investment-banking-teaser` | 3★ | `mcp-required` | 无 | Draft anonymous one-page company teasers for sell-side M&A processes. Creates a compelling summary without revealing the company's identity, designed  |
| `anthropic-fs-private-equity-ai-readiness` | 3★ | `mcp-required` | 无 | Scan the portfolio for the highest-leverage AI opportunities and rank where to deploy operating-partner time. Ingests quarterly updates and financials |
| `anthropic-fs-private-equity-dd-checklist` | 3★ | `mcp-required` | 无 | Generate and track comprehensive due diligence checklists tailored to the target company's sector, deal type, and complexity. Covers all major workstr |
| `anthropic-fs-private-equity-dd-meeting-prep` | 3★ | `mcp-required` | 无 | Prepare for due diligence meetings — management presentations, expert network calls, customer references, and advisor sessions. Generates targeted que |
| `anthropic-fs-private-equity-deal-screening` | 3★ | `mcp-required` | 无 | Quickly screen inbound deal flow — CIMs, teasers, and broker materials — against the fund's investment criteria. Extracts key deal metrics, runs a pas |
| `anthropic-fs-private-equity-deal-sourcing` | 3★ | `mcp-required` | 无 | PE deal sourcing workflow — discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails. Use when  |
| `anthropic-fs-private-equity-ic-memo` | 3★ | `mcp-required` | 无 | Draft a structured investment committee memo for PE deal approval. Synthesizes due diligence findings, financial analysis, and deal terms into a profe |
| `anthropic-fs-private-equity-portfolio-monitoring` | 3★ | `mcp-required` | 无 | Track and analyze portfolio company performance against plan. Ingests monthly/quarterly financial packages (Excel, PDF), extracts KPIs, flags variance |
| `anthropic-fs-private-equity-returns-analysis` | 3★ | `mcp-required` | 无 | Build quick IRR/MOIC sensitivity tables for PE deal evaluation. Models returns across entry multiple, leverage, exit multiple, growth, and hold period |
| `anthropic-fs-private-equity-unit-economics` | 3★ | `mcp-required` | 无 | Analyze unit economics for PE targets — ARR cohorts, LTV/CAC, net retention, payback periods, revenue quality, and margin waterfall. Essential for sof |
| `anthropic-fs-private-equity-value-creation-plan` | 3★ | `mcp-required` | 无 | Structure post-acquisition value creation plans with revenue, cost, and operational levers mapped to an EBITDA bridge. Includes 100-day priorities, KP |
| `anthropic-fs-wealth-management-client-report` | 3★ | `mcp-required` | 无 | Generate professional client-facing performance reports with portfolio returns, allocation breakdowns, and market commentary. Suitable for quarterly o |
| `anthropic-fs-wealth-management-client-review` | 3★ | `mcp-required` | 无 | Prepare for client review meetings with portfolio performance summary, allocation analysis, talking points, and action items. Pulls together account d |
| `anthropic-fs-wealth-management-financial-plan` | 3★ | `mcp-required` | 无 | Build or update a comprehensive financial plan covering retirement projections, education funding, estate planning, and cash flow analysis. Use for ne |
| `anthropic-fs-wealth-management-investment-proposal` | 3★ | `mcp-required` | 无 | Create professional investment proposals for prospective clients. Covers the firm's approach, proposed allocation, expected outcomes, and fee structur |
| `anthropic-fs-wealth-management-portfolio-rebalance` | 3★ | `mcp-required` | 无 | Analyze portfolio allocation drift and generate rebalancing trade recommendations across accounts. Considers tax implications, transaction costs, and  |
| `anthropic-fs-wealth-management-tax-loss-harvesting` | 3★ | `mcp-required` | 无 | Identify tax-loss harvesting opportunities across taxable accounts. Finds positions with unrealized losses, suggests replacement securities, and track |

### finance-trading

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `ai-image-generation` | 3★ | `api-key` | `GEMINI_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID`, `OPENAI_API_KEY` | Generate AI images with GPT-Image-2, FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.sh CLI. Models: GPT-Image-2, FLUX Dev LoRA, FLUX. |
| `alphaear-deepear-lite` | 4★ | `direct` | 无 | Fetch the latest financial signals and transmission-chain analyses from DeepEar Lite. Use when the user needs immediate insights into financial market |
| `alphaear-logic-visualizer` | 4★ | `direct` | 无 | Create visualize finance logic diagrams (e.g., Draw.io XML) to explain complex finance transmission chains or finance logic flows. |
| `alphaear-news` | 4★ | `direct` | 无 | Fetch hot finance news, unified trends, and prediction financial market data. Use when the user needs real-time financial news, trend reports from mul |
| `alphaear-predictor` | 4★ | `direct` | 无 | Market prediction skill using Kronos. Use when user needs finance market time-series forecasting or news-aware finance market adjustments. |
| `alphaear-reporter` | 4★ | `direct` | 无 | Plan, write, and edit professional financial reports; generate finance chart configurations. Use when condensing finance analysis into a structured ou |
| `alphaear-search` | 3★ | `browser-required` | 无 | Perform finance web searches and local context searches. Use when the user needs general finance info from the web (Jina/DDG/Baidu) or needs to retrie |
| `alphaear-sentiment` | 3★ | `api-key` | `OPENAI_API_KEY` | Analyze finance text sentiment using FinBERT or LLM. Use when the user needs to determine the sentiment (positive/negative/neutral) and score of finan |
| `alphaear-signal-tracker` | 4★ | `direct` | 无 | Track finance investment signal evolution and update logic based on new finance market information. Use when monitoring finance signals and determinin |
| `alphaear-stock` | 4★ | `direct` | 无 | Search A-Share/HK/US finance stock tickers and retrieve finance stock price history. Use when user asks about finance stock codes, recent price change |
| `breadth-chart-analyst` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | This skill should be used when analyzing market breadth charts, specifically the S&P 500 Breadth Index (200-Day MA based) and the US Stock Market Uptr |
| `breakout-trade-planner` | 4★ | `direct` | 无 | Generate Minervini-style breakout trade plans from VCP screener output with worst-case risk calculation, portfolio heat management, and Alpaca-compati |
| `canslim-screener` | 3★ | `api-key` | `FMP_API_KEY` | Screen US stocks using William O'Neil's CANSLIM growth stock methodology. Use when user requests CANSLIM stock screening, growth stock analysis, momen |
| `company-valuation` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | Estimate the intrinsic value of a public company using DCF, relative (peer multiple) and sum-of-parts (SOTP) methods, then triangulate to an implied s |
| `data-quality-checker` | 4★ | `direct` | 无 | Validate data quality in market analysis documents and blog articles before publication. Use when checking for price scale inconsistencies (ETF vs fut |
| `dividend-growth-pullback-screener` | 3★ | `api-key` | `FINVIZ_API_KEY`, `FMP_API_KEY` | Use this skill to find high-quality dividend growth stocks (12%+ annual dividend growth, 1.5%+ yield) that are experiencing temporary pullbacks, ident |
| `downtrend-duration-analyzer` | 3★ | `api-key` | `FMP_API_KEY` | Analyze historical downtrend durations and generate interactive HTML histograms showing typical correction lengths by sector and market cap. |
| `earnings-calendar` | 3★ | `api-key` | `FMP_API_KEY` | This skill retrieves upcoming earnings announcements for US stocks using the Financial Modeling Prep (FMP) API. Use this when the user requests earnin |
| `earnings-preview` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | Generate a pre-earnings briefing for any stock using Yahoo Finance data. Use this skill whenever the user wants to prepare for an upcoming earnings re |
| `earnings-recap` | 4★ | `direct` | 无 | Generate a post-earnings analysis for any stock using Yahoo Finance data. Use when the user wants to review what happened after earnings, understand b |
| `earnings-trade-analyzer` | 3★ | `api-key` | `FMP_API_KEY` | Analyze recent post-earnings stocks using a 5-factor scoring system (Gap Size, Pre-Earnings Trend, Volume Trend, MA200 Position, MA50 Position). Score |
| `economic-calendar-fetcher` | 3★ | `api-key` | `FMP_API_KEY` | Fetch upcoming economic events and data releases using FMP API. Retrieve scheduled central bank decisions, employment reports, inflation data, GDP rel |
| `edge-candidate-agent` | 4★ | `direct` | 无 | Generate and prioritize US equity long-side edge research tickets from EOD observations, then export pipeline-ready candidate specs for trade-strategy |
| `edge-hint-extractor` | 3★ | `api-key` | `OPENAI_API_KEY` | Extract edge hints from daily market observations and news reactions, with optional LLM ideation, and output canonical hints.yaml for downstream conce |
| `estimate-analysis` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | Deep-dive into analyst estimates and revision trends for any stock using Yahoo Finance data. Use when the user wants to understand analyst estimate di |
| `etf-premium` | 4★ | `direct` | 无 | Calculate ETF premium/discount vs NAV via Yahoo Finance, and decompose single-day surges into NAV-driven vs structural components (gamma squeeze, deal |
| `exposure-coach` | 3★ | `api-key` | `FMP_API_KEY` | Generate a one-page Market Posture summary with net exposure ceiling, growth-vs-value bias, participation breadth, and new-entry-allowed vs cash-prior |
| `finance-sentiment` | 3★ | `api-key` | `ADANOS_API_KEY` | Fetch structured stock sentiment across Reddit, X.com, news, and Polymarket using the Adanos Finance API. Use this skill whenever the user asks how mu |
| `finance-skill-creator` | 4★ | `direct` | 无 | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or op |
| `finviz-screener` | 3★ | `api-key` | `FINVIZ_API_KEY` | Build and open FinViz screener URLs from natural language requests. Use when user wants to screen stocks, find stocks matching criteria, filter by fun |
| `ftd-detector` | 3★ | `api-key` | `FMP_API_KEY` | Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology. Dual-index tracking (S&P 500 + NASDAQ) wit |
| `hormuz-strait` | 4★ | `direct` | 无 | Check the current status of the Strait of Hormuz — shipping transit data, oil price impact, stranded vessels, insurance risk levels, diplomatic develo |
| `ibd-distribution-day-monitor` | 3★ | `api-key` | `FMP_API_KEY` | Detect IBD-style Distribution Days for QQQ/SPY (close down at least 0.2% on higher volume), track 25-session expiration and 5% invalidation, count d5/ |
| `institutional-flow-tracker` | 3★ | `api-key` | `FMP_API_KEY` | Use this skill to track institutional investor ownership changes and portfolio flows using 13F filings data. Analyzes hedge funds, mutual funds, and o |
| `kanchi-dividend-review-monitor` | 4★ | `direct` | 无 | Monitor dividend portfolios with Kanchi-style forced-review triggers (T1-T5) and convert anomalies into OK/WARN/REVIEW states without auto-selling. Us |
| `kanchi-dividend-sop` | 3★ | `api-key` | `FMP_API_KEY` | Convert Kanchi-style dividend investing into a repeatable US-stock operating procedure. Use when users ask for かんち式配当投資, dividend screening, dividend  |
| `kanchi-dividend-us-tax-accounting` | 4★ | `direct` | 无 | Provide US dividend tax and account-location workflow for Kanchi-style income portfolios. Use when users ask about qualified vs ordinary dividends, 10 |
| `llmquant-commodities` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant commodities workflows. Use when the user needs commodity spot, futures curve, inventory, roll yield, or macro linkage analys |
| `llmquant-credit` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant credit workflows. Use when the user needs issuer credit review, spread regime analysis, high-yield stress monitoring, defaul |
| `llmquant-crypto` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant crypto workflows. Use when the user needs crypto market regime analysis, token research, perpetual funding, basis, leverage, |
| `llmquant-equities` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant equities workflows. Use when the user needs stock analysis, equity comparison, research memos, merger-arb memos, or sell/tak |
| `llmquant-equity-derivatives` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant equity derivatives workflows. Use when the user needs single-stock derivative, convertible, warrant, structured payoff, or h |
| `llmquant-options` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant options workflows. Use when the user needs IV rank, option scoring, strategy construction, Greeks, P&L simulation, volatilit |
| `llmquant-prediction-markets` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant prediction-market workflows. Use when the user needs event odds, settlement criteria, probability gaps, cross-market pricing |
| `llmquant-strategies` | 4★ | `api-key+mcp-required` | `LLMQUANT_API_KEY` | Router skill for LLMQuant hedge-fund and PM strategy workflows. Use when the user needs equity long/short, long-biased, event-driven, macro, quant, or |
| `macro-regime-detector` | 3★ | `api-key` | `FMP_API_KEY` | Detect structural macro regime transitions (1-2 year horizon) using cross-asset ratio analysis. Analyze RSP/SPY concentration, yield curve, credit con |
| `market-breadth-analyzer` | 4★ | `direct` | 无 | Quantifies market breadth health using TraderMonty's public CSV data. Generates a 0-100 composite score across 6 components (100 = healthy). No API ke |
| `market-environment-analysis` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and e |
| `market-news-analyst` | 3★ | `browser-required` | 无 | This skill should be used when analyzing recent market-moving news events and their impact on equity markets and commodities. Use this skill when the  |
| `market-top-detector` | 3★ | `api-key` | `FMP_API_KEY` | Detects market top probability using O'Neil Distribution Days, Minervini Leading Stock Deterioration, and Monty Defensive Sector Rotation. Generates a |
| `options-payoff` | 4★ | `direct` | 无 | Generate an interactive options payoff curve chart with dynamic parameter controls. Use this skill whenever the user shares an options position screen |
| `options-strategy-advisor` | 3★ | `api-key` | `FMP_API_KEY` | Options trading strategy analysis and simulation tool. Provides theoretical pricing using Black-Scholes model, Greeks calculation, strategy P/L simula |
| `pair-trade-screener` | 3★ | `api-key` | `FMP_API_KEY` | Statistical arbitrage tool for identifying and analyzing pair trading opportunities. Detects cointegrated stock pairs within sectors, analyzes spread  |
| `parabolic-short-trade-planner` | 3★ | `api-key` | `ALPACA_API_KEY`, `FMP_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID` | Screen US equities for parabolic exhaustion patterns and generate conditional pre-market short plans, then evaluate intraday trigger fires from live 5 |
| `pead-screener` | 3★ | `api-key` | `FMP_API_KEY` | Screen post-earnings gap-up stocks for PEAD (Post-Earnings Announcement Drift) patterns. Analyzes weekly candle formation to detect red candle pullbac |
| `portfolio-manager` | 3★ | `mcp-required` | 无 | Comprehensive portfolio analysis using Alpaca MCP Server integration to fetch holdings and positions, then analyze asset allocation, risk metrics, ind |
| `position-sizer` | 4★ | `direct` | 无 | Calculate risk-based position sizes for long stock trades. Use when user asks about position sizing, how many shares to buy, risk per trade, Kelly cri |
| `pybroker-backtest-skill` | 4★ | `direct` | 无 | 基于 PyBroker 的算法交易回测实验技能，支持技术指标策略、机器学习策略、收益/回撤/稳定性评估和参数验证。 |
| `saas-valuation-compression` | 4★ | `direct` | 无 | Analyze SaaS company valuation compression between funding rounds. Use this skill whenever the user asks about: how much a SaaS company's valuation mu |
| `sector-analyst` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | This skill should be used when analyzing sector rotation patterns and market cycle positioning. It fetches sector uptrend data from CSV (no API key re |
| `sepa-strategy` | 4★ | `direct` | 无 | Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) methodology. Use this skill whenever the user mentions SEPA, Minervini, sup |
| `signal-postmortem` | 3★ | `api-key` | `FMP_API_KEY` | Record and analyze post-trade outcomes for signals generated by edge pipeline and other skills. Track false positives, missed opportunities, and regim |
| `stanley-druckenmiller-investment` | 4★ | `direct` | 无 | Druckenmiller Strategy Synthesizer - Integrates 8 upstream skill outputs (Market Breadth, Uptrend Analysis, Market Top, Macro Regime, FTD Detector, VC |
| `stock-analysis` | 4★ | `direct` | 无 | Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension st |
| `stock-correlation` | 4★ | `direct` | 无 | Analyze stock correlations to find related companies and trading pairs. Use when the user asks about correlated stocks, related companies, sector peer |
| `stock-daily-analysis-skill` | 3★ | `api-key` | `OPENAI_API_KEY` | LLM驱动的每日股票分析系统。支持A股/港股/美股自选股智能分析，生成决策仪表盘和大盘复盘报告。提供技术面分析（均线、MACD、RSI、乖离率）、趋势判断、买入信号评分。可与market-data skill集成获取更稳定的ETF数据。触发词：股票分析、分析股票、每日分析、技术面分析。 |
| `stock-liquidity` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | Analyze stock liquidity using bid-ask spreads, volume profiles, order book depth, market impact estimates, and turnover ratios via Yahoo Finance data. |
| `technical-analyst` | 3★ | `api-key` | `IMA_API_KEY`, `IMA_CLIENT_ID` | This skill should be used when analyzing weekly price charts for stocks, stock indices, cryptocurrencies, or forex pairs. Use this skill when the user |
| `theme-detector` | 3★ | `api-key` | `FINVIZ_API_KEY`, `FMP_API_KEY` | Detect and analyze trending market themes across sectors. Use when user asks about current market themes, trending sectors, sector rotation, thematic  |
| `trade-hypothesis-ideator` | 4★ | `direct` | 无 | Generate falsifiable trade strategy hypotheses from market data, trade logs, and journal snippets. Use when you have a structured input bundle and wan |
| `trader-memory-core` | 4★ | `direct` | 无 | Track investment theses across their lifecycle — from screening idea to closed position with postmortem. Register theses from screener outputs, manage |
| `uptrend-analyzer` | 4★ | `direct` | 无 | Analyzes market breadth using Monty's Uptrend Ratio Dashboard data to diagnose the current market environment. Generates a 0-100 composite score from  |
| `us-market-bubble-detector` | 4★ | `direct` | 无 | Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.1. Prioritizes objective met |
| `us-stock-analysis` | 4★ | `direct` | 无 | Comprehensive US stock analysis including fundamental analysis (financial metrics, business quality, valuation), technical analysis (indicators, chart |
| `value-dividend-screener` | 3★ | `api-key` | `FINVIZ_API_KEY`, `FMP_API_KEY` | Screen US stocks for high-quality dividend opportunities combining value characteristics (P/E ratio under 20, P/B ratio under 2), attractive yields (3 |
| `vcp-screener` | 3★ | `api-key` | `FMP_API_KEY` | Screen S&P 500 stocks for Mark Minervini's Volatility Contraction Pattern (VCP). Identifies Stage 2 uptrend stocks forming tight bases with contractin |

### legal-compliance

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `anthropic-fs-operations-kyc-doc-parse` | 3★ | `mcp-required` | 无 | Parse an investor or client onboarding packet into structured KYC fields — identity, ownership, control, source of funds, and document inventory. Use  |
| `anthropic-fs-operations-kyc-rules` | 3★ | `mcp-required` | 无 | Apply the firm's KYC/AML rules grid to a parsed onboarding record — assign a risk rating, list every rule outcome with the rule cited, and flag what's |

### marketing-growth

| Skill | 星级 | 使用条件 | API Key | 一句话用途 |
|---|---:|---|---|---|
| `marketingskills` | 4★ | `direct` | 无 | Marketing Skills Hub（上游: coreyhaines31/marketingskills）- 用于索引与选择营销类子技能（如 content-strategy、social-content）。 |

# Finance Core Suite v0.2 - Data Keys Allowed

本版本根据新口径重评：**金融数据源 key 不算高门槛**，用户可自行配置 Tushare、AkShare/Wind 类数据源；但模型类、生成类、平台反代类 key 仍视为高门槛。

## Key 口径

### 可接受：数据源 key

这些 key 属于金融数据供应商或行情/研究数据源，允许进入核心候选：

- `TUSHARE_TOKEN`
- `STOCK_API_KEY`
- `FMP_API_KEY`
- `FINVIZ_API_KEY`
- `LLMQUANT_API_KEY`
- `ADANOS_API_KEY`
- `ALPACA_API_KEY`（仅数据/组合读取场景；交易权限另行隔离）
- 未来可加入：`WIND_API_KEY` / `WIND_TOKEN`

### 不优先：模型/平台 key

这些 key 不是纯金融数据源，默认不进入核心金融套件：

- `OPENAI_API_KEY`
- `IMA_API_KEY`
- `IMA_CLIENT_ID`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`

## 当前仓库现状

- 金融相关候选：110 个左右。
- 免 key：54 个。
- 纯数据源 key：42 个。
- 模型/平台 key：14 个。
- 当前仓库未发现独立 `wind` skill；如要支持 Wind，应新增或接入一个 Wind 数据源 skill。

## 最佳套件判断

在“数据源 key 可接受”的口径下，最佳金融套件不再是纯免 key 版，而应是：

> **Finance Core Data-Enhanced Suite**
> A 股以 `a-stock-data` 为主，`tushare-openclaw-skill` 为官方数据补充；美股/全球以 `yfinance-data` + LLMQuant 为主；FMP/FINVIZ 负责筛选器；本地 direct skills 负责监控、仓位、回测、市场宽度和知识库。

## 推荐核心清单

| 能力位 | 推荐 Skill | 状态 | 理由 |
|---|---|---|---|
| A 股全栈主数据源 | `a-stock-data` | 核心 | 覆盖行情、研报、题材、北向、龙虎榜、解禁、两融、大宗、股东户数、分红、新闻、公告和财报。 |
| A 股官方数据补充 | `tushare-openclaw-skill` | 核心 | Tushare 是标准化 A 股/基金/期货/债券/宏观数据源，适合做正式数据校验和批量研究。 |
| 美股/全球基础数据 | `yfinance-data` | 核心 | 免 key，覆盖价格、财报、期权、分红、持仓；需处理 Yahoo 限流。 |
| 机构级数据/SEC/13F | `llmquant-data` | 核心 | SEC、13F、宏观快照、源数据简报；数据源 key 可接受后应进入核心。 |
| ETF 数据/暴露 | `llmquant-etfs` | 核心 | ETF 持仓、重叠、集中度、主题暴露，弥补 yfinance/普通数据源不足。 |
| 金融知识库 | `openclaw-stock-kb` | 核心 | 策略、指标、情绪、风控、回测资料底座。 |
| 政策监管 | `policy-monitor` | 核心 | 国内政策监控与市场影响解读，免 key。 |
| 宏观分析 | `llmquant-macro` | 核心 | 宏观 dashboard、央行、通胀/增长/流动性、组合影响。 |
| 市场事件 | `llmquant-events` | 核心 | 财报、并购、监管、催化剂和事件日历，可替代多个 earnings 单点技能。 |
| 市场情报 | `llmquant-market-intelligence` | 核心 | 市场情绪、宏观视图、事件概率信号。 |
| 风险环境 | `llmquant-risk` | 核心 | VIX、恐慌评分、对冲设计、研究健康检查。 |
| 投资人视角 | `llmquant-investor-lenses` | 核心 | 给研究报告加入投资人推理/审查框架。 |
| 美股综合分析 | `us-stock-analysis` | 核心 | 美股基本面、技术面、估值、比较和投资报告。 |
| 通用选股 | `finviz-screener` | 核心 | FINVIZ 是美股筛选高效入口，数据源 key 可接受后应进入核心。 |
| 成长股筛选 | `canslim-screener` | 核心 | CANSLIM 成长股方法。 |
| VCP 筛选 | `vcp-screener` | 核心 | Minervini VCP 形态/入场结构。 |
| 股息价值筛选 | `value-dividend-screener` | 核心 | 股息、估值、安全边际、质量价值筛选。 |
| 主题识别 | `theme-detector` | 核心 | 热门主题、板块轮动、多空叙事识别。 |
| 宏观 regime | `macro-regime-detector` | 核心 | FMP 数据支持的中期宏观 regime 转换识别。 |
| 期权策略 | `llmquant-options` | 核心 | IV、Greeks、策略构建、波动率面、异常交易、财报 IV crush 等。 |
| 组合/研究工作台 | `llmquant-portfolio` | 核心 | 公司画像、thesis 跟踪、主题研究、自选监控和 alert 管理。 |
| 回测引擎 | `pybroker-backtest-skill` | 核心 | 离线测试通过；适合作为策略验证引擎。 |
| 回测方法论 | `backtest-expert` | 核心 | 鲁棒性、滑点、过拟合、样本切分等方法论审查。 |
| 仓位计算 | `position-sizer` | 核心 | 实测可输出仓位、风险占比、JSON/Markdown 报告。 |
| 自选股监控 | `stock-monitor-skill` | 核心 | 实测 17 项通过，可输出 A 股/ETF/黄金预警。 |
| 市场宽度 | `uptrend-analyzer` | 核心 | 实测通过，输出市场环境评分和权益暴露建议。 |
| 金融情报读取 | `opencli-reader` | 核心 | 通用只读入口，覆盖多金融网站，替代多个专用 reader。 |
| 创业投资研究 | `startup-analysis` | 可选核心 | VC/求职/创始人多视角，适合一级市场/创业公司研究。 |

## 建议不进入核心

| 技能/组 | 处理 | 原因 |
|---|---|---|
| `akshare-stock` | 备选 | 与 `a-stock-data`、`tushare-openclaw-skill` 重叠；适合做 A 股数据源 fallback。 |
| `openclaw-stock-data-skill` | 备选 | 覆盖较窄；如接入特定 STOCK_API_KEY 才有价值。 |
| `funda-data` | 暂缓 | 混合 `FUNDA_API_KEY` 与 `IMA_API_KEY/IMA_CLIENT_ID`，按新口径仍有模型/平台依赖。 |
| `stock-daily-analysis-skill` | 暂缓 | 需要 `OPENAI_API_KEY`，模型 key 依赖，不放核心。 |
| `company-valuation` | 暂缓 | 需要 `IMA_API_KEY/IMA_CLIENT_ID`；由 `us-stock-analysis` + LLMQuant 暂代。 |
| `technical-analyst` | 暂缓 | 需要 IMA；由 `sepa-strategy` + `vcp-screener` 暂代。 |
| `alphaear-*` | 实验室 | 方向多、重叠多，适合 finance-lab，不放核心。 |
| `edge-*` | 实验室 | 高级策略研发流水线，适合 finance-lab。 |
| 专用社媒 readers | 备选 | 核心用 `opencli-reader`，专用 reader 按渠道安装。 |

## 最佳结论

如果用户愿意配置金融数据源 key，最佳套件是 **Data-Enhanced Core**，不是纯免 key 版。

推荐规模：

- 标准金融核心：27-28 个。
- A 股增强：额外启用 `akshare-stock` 或未来 `wind-*`。
- 量化实验室：额外启用 `alphaear-*`, `edge-*`, `pair-trade-screener`, `pead-screener`, `market-top-detector` 等。

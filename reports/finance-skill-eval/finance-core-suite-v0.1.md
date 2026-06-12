# Finance Core Suite v0.1

本版本基于 `round1-static-results.md` 与 `round2-live-results.md`。它不是最终入库清单，而是第一轮测试后的择优结果：能实测的先实测，不能实测的按数据契约、输出结构、依赖成本和唯一性暂定。

## 核心录取

| 能力位 | Skill | 状态 | 录取理由 |
|---|---|---|---|
| A 股全栈数据 | `a-stock-data` | 暂录取 | 覆盖行情、研报、资金面、龙虎榜、解禁、两融、公告和财报，覆盖面明显高于其他 A 股数据源。 |
| 美股/全球数据 | `yfinance-data` | 暂录取，需复测 | 无 API Key，覆盖价格、财报、期权、分红、持仓；当前 Yahoo 限流导致 live 失败，不能判负。 |
| 机构数据/SEC/13F | `llmquant-data` | 待密钥实测 | 工作流明确，覆盖 SEC、13F、宏观快照；需要 `LLMQUANT_API_KEY` + MCP。 |
| 金融知识库 | `openclaw-stock-kb` | 录取 | 5★，direct，覆盖策略、技术指标、情绪、风控、回测知识，是研究框架底座。 |
| 政策监管 | `policy-monitor` | 录取 | direct，静态得分高，覆盖央行、证监会、发改委等政策渠道与市场影响解读。 |
| 宏观 | `llmquant-macro` | 待密钥实测 | 有结构化 macro 工作流，适合作为机构宏观核心；需 MCP。 |
| 事件 | `llmquant-events` | 待密钥实测 | 可覆盖财报、并购、监管、催化剂，替代多个 earnings 单点技能。 |
| 市场情报 | `llmquant-market-intelligence` | 待密钥实测 | 覆盖宏观视图、情绪仪表盘、事件概率信号。 |
| 风险环境 | `llmquant-risk` | 待密钥实测 | 覆盖 VIX、恐慌评分、对冲和研究健康检查。 |
| 投资人视角 | `llmquant-investor-lenses` | 待密钥实测 | 提供投资人推理框架，适合作为研究报告的二次审查层。 |
| 美股综合分析 | `us-stock-analysis` | 暂录取 | direct，覆盖基本面、技术面、估值、比较和投资报告。 |
| 公司估值 | `company-valuation` | 待 API/模型复测 | 与 `us-stock-analysis` 有重叠，但估值深度更强；先保留为估值专用。 |
| 技术交易框架 | `sepa-strategy` | 暂录取 | direct，文档完整，覆盖 Minervini/SEPA 方法；比纯 screener 更像策略框架。 |
| 成长股筛选 | `canslim-screener` | 待 API 实测 | 有脚本和 guardrail，适合作为成长股筛选位。 |
| VCP 筛选 | `vcp-screener` | 待 API 实测 | 与 CANSLIM 不完全重复，偏形态/入场结构。 |
| 股息价值 | `value-dividend-screener` | 待 API 实测 | 代表股息价值筛选位。 |
| 期权策略 | `llmquant-options` | 待密钥实测 | 工作流最多；若 LLMQuant 不可用，则降级为 `options-strategy-advisor`。 |
| 回测引擎 | `pybroker-backtest-skill` | 录取但需安装依赖/缓存 | 33 个离线测试通过；临时 venv 安装 requirements 后 CLI 可启动；真实行情回测受 Yahoo 限流影响。 |
| 回测方法论 | `backtest-expert` | 录取 | 与回测引擎不重复，负责方法论、稳健性、滑点、过拟合防控。 |
| 仓位计算 | `position-sizer` | 录取 | live run 成功，能输出仓位、风险占比、JSON/Markdown 报告。 |
| 自选股监控 | `stock-monitor-skill` | 录取 | 17 个测试通过，真实输出预警；部分东财接口有网络/代理不稳定但主流程可用。 |
| 市场宽度 | `uptrend-analyzer` | 录取 | live run 成功，输出 60.1/100、Bull-Lower、80-90% 暴露建议。 |
| 市场宽度备选 | `market-breadth-analyzer` | 备选 | 计算有效，但首次运行因输出目录不存在失败；修复后可用。 |
| 通用金融情报 | `opencli-reader` | 暂录取 | 作为多站点只读 fallback，替代多个专用社媒 reader 进入核心。 |
| 创业投资研究 | `startup-analysis` | 暂录取 | 与股票套件边界不同，但对 VC/一级市场研究有独特价值。 |

## 暂不进入核心

| 重复组 | 暂不进入核心 | 原因 |
|---|---|---|
| A 股数据备选 | `akshare-stock`, `tushare-openclaw-skill`, `openclaw-stock-data-skill` | `a-stock-data` 覆盖更宽且 direct；Tushare/stock-data 需 key。 |
| 高级数据备选 | `funda-data` | 与 `yfinance-data` + `llmquant-data` 重叠，且当前无 key/MCP。 |
| LLMQuant 长尾模块 | `llmquant-commodities`, `llmquant-credit`, `llmquant-crypto`, `llmquant-equity-derivatives`, `llmquant-etfs`, `llmquant-portfolio`, `llmquant-portfolio-lab`, `llmquant-prediction-markets`, `llmquant-rates-fx`, `llmquant-strategies` | 更适合专家套件 `finance-lab`，不放入核心。 |
| AlphaEar 全组 | `alphaear-*` | 功能覆盖搜索、报告、情绪、预测，和核心能力高度重叠；先放入实验室。 |
| 财报单点 | `earnings-calendar`, `earnings-preview`, `earnings-recap`, `earnings-trade-analyzer` | 由 `llmquant-events` 覆盖；无 LLMQuant 时再复活。 |
| 市场顶部/宽度长尾 | `market-top-detector`, `ftd-detector`, `ibd-distribution-day-monitor`, `breadth-chart-analyst` | 与 `uptrend-analyzer` / `market-breadth-analyzer` 重叠。 |
| 社媒专用 reader | `twitter-reader`, `telegram-reader`, `discord-reader`, `linkedin-reader` | 核心只保留 `opencli-reader`；专用 reader 进入可选包。 |
| Edge pipeline | `edge-*` | 更像高级量化研发流水线，暂入 `finance-lab`。 |

## 下一轮必须实测

1. 配置 `LLMQUANT_API_KEY` + LLMQuant Data MCP 后测试：`llmquant-data`, `llmquant-macro`, `llmquant-events`, `llmquant-market-intelligence`, `llmquant-risk`, `llmquant-options`。
2. 为 `pybroker-backtest-skill` 和 `yfinance-data` 增加缓存/重试/替代数据源策略后复测 Yahoo 限流场景。
3. 稍后重试 `yfinance-data`，确认 Yahoo rate limit 恢复后的多 ticker 对比。
4. 修复或包装 `market-breadth-analyzer` 自动创建输出目录的问题。
5. 有 FMP/FINVIZ key 后实测：`canslim-screener`, `vcp-screener`, `value-dividend-screener`, `theme-detector`。

## 当前建议套件大小

- 核心：24 个
- 备选：1 个
- 待密钥实测：8 个核心候选包含在 24 个内
- 实验室/可选：其余高度重复或专家向 skills

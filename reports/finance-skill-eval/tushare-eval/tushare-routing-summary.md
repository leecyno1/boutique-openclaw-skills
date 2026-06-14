# Tushare 金融数据接入与 Skills 路由清单

- 生成来源：`reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json`
- Tushare 连通：`True`
- 股票基础信息样本：`5528` 行
- 日线样本：`105` 行
- 指数样本：`105` 行

## 结论

- 转为 / 接入 Tushare-backed：`20` 个
- 仅适合作为 Tushare 补充源：`51` 个
- 跳过或不适配：`92` 个

## 应转为 Tushare-backed 的 Skills

| Skill | 场景 | 分数 | 数据策略 | 评价 |
|---|---|---:|---|---|
| `tushare-openclaw-skill` | A股基础数据 | 95 | `native_tushare` | 强适配：可优先接入或改为 Tushare 数据底座。 |
| `a-stock-data` | A股基础数据 | 88 | `partial_replace_or_backend_option` | 强适配：可优先接入或改为 Tushare 数据底座。 |
| `akshare-stock` | A股基础数据 | 82 | `replace_with_tushare_possible` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `alphaear-search` | A股基础数据 | 75 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `alphaear-stock` | A股基础数据 | 75 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `alphaear-reporter` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `breakout-trade-planner` | 技术面/交易计划 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `data-quality-checker` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `earnings-recap` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `edge-candidate-agent` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `finance-skill-creator` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `kanchi-dividend-review-monitor` | 组合/风控/监控 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `options-payoff` | 技术面/交易计划 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `position-sizer` | 技术面/交易计划 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `pybroker-backtest-skill` | 量化/回测/策略迭代 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `saas-valuation-compression` | 个股研究/估值 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `sepa-strategy` | 技术面/交易计划 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `stock-analysis` | 组合/风控/监控 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `stock-correlation` | 量化/回测/策略迭代 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |
| `stock-monitor-skill` | 组合/风控/监控 | 70 | `tushare_candidate` | 部分适配：Tushare 可覆盖核心行情/基本面，但仍需保留原 skill 的非行情能力。 |

## Tushare 仅作补充源

| Skill | 场景 | 分数 | 说明 |
|---|---|---:|---|
| `anthropic-fs-equity-research-catalyst-calendar` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-earnings-analysis` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-earnings-preview` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-idea-generation` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-initiating-coverage` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-model-update` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-morning-note` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-sector-overview` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-3-statement-model` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-clean-data-xls` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-competitive-analysis` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-comps-analysis` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-dcf-model` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-deck-refresh` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-ppt-template-creator` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-pptx-author` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-skill-creator` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-lseg-equity-research` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-lseg-fixed-income-portfolio` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-lseg-option-vol-analysis` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-private-equity-returns-analysis` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-spglobal-earnings-preview-beta` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-spglobal-funding-digest` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-spglobal-tear-sheet` | 个股研究/估值 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `us-market-bubble-detector` | 个股研究/估值 | 45 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `us-stock-analysis` | 个股研究/估值 | 45 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `alphaear-deepear-lite` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `alphaear-news` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `alphaear-predictor` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `alphaear-signal-tracker` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `hormuz-strait` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `market-breadth-analyzer` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `market-news-analyst` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `marketingskills` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `stanley-druckenmiller-investment` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `trade-hypothesis-ideator` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `uptrend-analyzer` | 市场复盘/宏观政策 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-lseg-macro-rates-monitor` | 市场复盘/宏观政策 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `yfinance-data` | 市场复盘/宏观政策 | 45 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-fund-admin-gl-recon` | 技术面/交易计划 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `alphaear-logic-visualizer` | 报告/可视化/知识库 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-audit-xls` | 报告/可视化/知识库 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-financial-analysis-xlsx-author` | 报告/可视化/知识库 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `openclaw-stock-kb` | 报告/可视化/知识库 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-equity-research-thesis-tracker` | 组合/风控/监控 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `anthropic-fs-private-equity-portfolio-monitoring` | 组合/风控/监控 | 50 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `backtest-expert` | 选股/机会发现 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `edge-signal-aggregator` | 选股/机会发现 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `etf-premium` | 选股/机会发现 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `trader-memory-core` | 选股/机会发现 | 60 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |
| `kanchi-dividend-us-tax-accounting` | 选股/机会发现 | 45 | 弱适配：Tushare 只能补充少量 A 股公开数据，不建议强行替换。 |

## 跳过 / 不适配

| Skill | 状态 | 场景 | 原因 |
|---|---|---|---|
| `anthropic-fs-lseg-bond-futures-basis` | `not_suitable_for_tushare` | 期权/固收/外汇/衍生品 | Tushare 对部分衍生品/基金/债券有接口，但无法替代 LSEG/LLMQuant 级跨资产深度数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-lseg-bond-relative-value` | `not_suitable_for_tushare` | 期权/固收/外汇/衍生品 | Tushare 对部分衍生品/基金/债券有接口，但无法替代 LSEG/LLMQuant 级跨资产深度数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-lseg-fx-carry-trade` | `not_suitable_for_tushare` | 期权/固收/外汇/衍生品 | Tushare 对部分衍生品/基金/债券有接口，但无法替代 LSEG/LLMQuant 级跨资产深度数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-lseg-swap-curve-strategy` | `not_suitable_for_tushare` | 期权/固收/外汇/衍生品 | Tushare 对部分衍生品/基金/债券有接口，但无法替代 LSEG/LLMQuant 级跨资产深度数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-financial-analysis-ib-check-deck` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-financial-analysis-lbo-model` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-fund-admin-accrual-schedule` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-fund-admin-break-trace` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-fund-admin-nav-tieout` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-fund-admin-roll-forward` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-fund-admin-variance-commentary` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-buyer-list` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-cim-builder` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-datapack-builder` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-deal-tracker` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-merger-model` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-pitch-deck` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-process-letter` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-strip-profile` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-investment-banking-teaser` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-operations-kyc-doc-parse` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-operations-kyc-rules` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-ai-readiness` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-dd-checklist` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-dd-meeting-prep` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-deal-screening` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-deal-sourcing` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-ic-memo` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-unit-economics` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-private-equity-value-creation-plan` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-client-report` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-client-review` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-financial-plan` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-investment-proposal` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-portfolio-rebalance` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `anthropic-fs-wealth-management-tax-loss-harvesting` | `not_suitable_for_tushare` | 机构金融/投行/PE/基金运营 | 机构材料、KYC、基金运营、PE 尽调依赖文件、企业系统或 MCP，Tushare 只能补充上市公司公开市场数据。; Anthropic FS 多数依赖企业 MCP/文档/机构数据；Tushare 只能作为 A 股公开市场补充。 |
| `llmquant-investor-lenses` | `skipped_extra_api` | A股基础数据 | requires LLMQUANT_API_KEY |
| `openclaw-stock-data-skill` | `skipped_extra_api` | A股基础数据 | requires STOCK_API_KEY |
| `company-valuation` | `skipped_extra_api` | 个股研究/估值 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `earnings-preview` | `skipped_extra_api` | 个股研究/估值 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `finance-sentiment` | `skipped_extra_api` | 个股研究/估值 | requires ADANOS_API_KEY |
| `funda-data` | `skipped_extra_api` | 个股研究/估值 | requires FUNDA_API_KEY, IMA_API_KEY, IMA_CLIENT_ID |
| `llmquant-commodities` | `skipped_extra_api` | 个股研究/估值 | requires LLMQUANT_API_KEY |
| `llmquant-crypto` | `skipped_extra_api` | 个股研究/估值 | requires LLMQUANT_API_KEY |
| `llmquant-equities` | `skipped_extra_api` | 个股研究/估值 | requires LLMQUANT_API_KEY |
| `llmquant-equity-derivatives` | `skipped_extra_api` | 个股研究/估值 | requires LLMQUANT_API_KEY |
| `llmquant-etfs` | `skipped_extra_api` | 个股研究/估值 | requires LLMQUANT_API_KEY |
| `stock-liquidity` | `skipped_extra_api` | 个股研究/估值 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `technical-analyst` | `skipped_extra_api` | 个股研究/估值 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `ai-image-generation` | `skipped_extra_api` | 市场复盘/宏观政策 | requires GEMINI_API_KEY, IMA_API_KEY, IMA_CLIENT_ID, OPENAI_API_KEY |
| `alphaear-sentiment` | `skipped_extra_api` | 市场复盘/宏观政策 | requires OPENAI_API_KEY |
| `breadth-chart-analyst` | `skipped_extra_api` | 市场复盘/宏观政策 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `downtrend-duration-analyzer` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `earnings-calendar` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `economic-calendar-fetcher` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `edge-hint-extractor` | `skipped_extra_api` | 市场复盘/宏观政策 | requires OPENAI_API_KEY |
| `exposure-coach` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `ftd-detector` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `llmquant-data` | `skipped_extra_api` | 市场复盘/宏观政策 | requires LLMQUANT_API_KEY |
| `llmquant-market-intelligence` | `skipped_extra_api` | 市场复盘/宏观政策 | requires LLMQUANT_API_KEY |
| `llmquant-prediction-markets` | `skipped_extra_api` | 市场复盘/宏观政策 | requires LLMQUANT_API_KEY |
| `llmquant-strategies` | `skipped_extra_api` | 市场复盘/宏观政策 | requires LLMQUANT_API_KEY |
| `macro-regime-detector` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `market-environment-analysis` | `skipped_extra_api` | 市场复盘/宏观政策 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `market-top-detector` | `skipped_extra_api` | 市场复盘/宏观政策 | requires FMP_API_KEY |
| `parabolic-short-trade-planner` | `skipped_extra_api` | 市场复盘/宏观政策 | requires ALPACA_API_KEY, FMP_API_KEY, IMA_API_KEY, IMA_CLIENT_ID |
| `sector-analyst` | `skipped_extra_api` | 市场复盘/宏观政策 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `stock-daily-analysis-skill` | `skipped_extra_api` | 市场复盘/宏观政策 | requires OPENAI_API_KEY |
| `earnings-trade-analyzer` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `estimate-analysis` | `skipped_extra_api` | 技术面/交易计划 | requires IMA_API_KEY, IMA_CLIENT_ID |
| `ibd-distribution-day-monitor` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `institutional-flow-tracker` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `options-strategy-advisor` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `pead-screener` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `signal-postmortem` | `skipped_extra_api` | 技术面/交易计划 | requires FMP_API_KEY |
| `llmquant-rates-fx` | `skipped_extra_api` | 期权/固收/外汇/衍生品 | requires LLMQUANT_API_KEY |
| `llmquant-credit` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `llmquant-events` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `llmquant-macro` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `llmquant-portfolio` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `llmquant-portfolio-lab` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `llmquant-risk` | `skipped_extra_api` | 组合/风控/监控 | requires LLMQUANT_API_KEY |
| `canslim-screener` | `skipped_extra_api` | 选股/机会发现 | requires FMP_API_KEY |
| `dividend-growth-pullback-screener` | `skipped_extra_api` | 选股/机会发现 | requires FINVIZ_API_KEY, FMP_API_KEY |
| `finviz-screener` | `skipped_extra_api` | 选股/机会发现 | requires FINVIZ_API_KEY |
| `kanchi-dividend-sop` | `skipped_extra_api` | 选股/机会发现 | requires FMP_API_KEY |
| `theme-detector` | `skipped_extra_api` | 选股/机会发现 | requires FINVIZ_API_KEY, FMP_API_KEY |
| `value-dividend-screener` | `skipped_extra_api` | 选股/机会发现 | requires FINVIZ_API_KEY, FMP_API_KEY |
| `vcp-screener` | `skipped_extra_api` | 选股/机会发现 | requires FMP_API_KEY |
| `llmquant-options` | `skipped_extra_api` | 量化/回测/策略迭代 | requires LLMQUANT_API_KEY |
| `pair-trade-screener` | `skipped_extra_api` | 量化/回测/策略迭代 | requires FMP_API_KEY |
| `portfolio-manager` | `skipped_mcp` | 个股研究/估值 | requires MCP or external tool |

# Finance Skill Static Evaluation - Round 1

本轮不是最终实测结论，只评估 skill 文档、工作流、脚本、输出格式、风险/降级说明和依赖成本，目的是决定哪些候选值得进入 live/model 评测。

## A 股全栈数据

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `tushare-openclaw-skill` | 78 | `api-key` | md=5, scripts=2, workflows=0, output=Y, guard=Y |
| 2 | `openclaw-stock-data-skill` | 78 | `api-key` | md=4, scripts=2, workflows=0, output=Y, guard=Y |
| 3 | `akshare-stock` | 78 | `direct` | md=2, scripts=1, workflows=0, output=Y, guard=N |
| 4 | `a-stock-data` | 78 | `direct` | md=4, scripts=0, workflows=0, output=Y, guard=Y |

## 美股/全球数据

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `llmquant-data` | 78 | `api-key+mcp-required` | md=5, scripts=0, workflows=5, output=Y, guard=Y |
| 2 | `yfinance-data` | 68 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=N |
| 3 | `funda-data` | 56 | `api-key+mcp-required` | md=14, scripts=0, workflows=0, output=Y, guard=N |

## SEC/13F/机构研究

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `llmquant-data` | 78 | `api-key+mcp-required` | md=5, scripts=0, workflows=5, output=Y, guard=Y |
| 2 | `institutional-flow-tracker` | 78 | `api-key` | md=5, scripts=11, workflows=0, output=Y, guard=Y |
| 3 | `funda-data` | 56 | `api-key+mcp-required` | md=14, scripts=0, workflows=0, output=Y, guard=N |

## 宏观与政策

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `policy-monitor` | 88 | `direct` | md=4, scripts=1, workflows=0, output=Y, guard=Y |
| 2 | `macro-regime-detector` | 78 | `api-key` | md=4, scripts=25, workflows=0, output=Y, guard=Y |
| 3 | `llmquant-macro` | 78 | `api-key+mcp-required` | md=4, scripts=0, workflows=4, output=Y, guard=Y |
| 4 | `economic-calendar-fetcher` | 78 | `api-key` | md=2, scripts=2, workflows=0, output=Y, guard=Y |

## 市场情绪与事件

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `theme-detector` | 78 | `api-key` | md=7, scripts=31, workflows=0, output=Y, guard=Y |
| 2 | `llmquant-market-intelligence` | 78 | `api-key+mcp-required` | md=4, scripts=0, workflows=4, output=Y, guard=Y |
| 3 | `llmquant-events` | 78 | `api-key+mcp-required` | md=4, scripts=0, workflows=4, output=Y, guard=Y |
| 4 | `finance-sentiment` | 68 | `api-key` | md=3, scripts=0, workflows=0, output=Y, guard=Y |
| 5 | `market-news-analyst` | 61 | `browser-required` | md=5, scripts=0, workflows=0, output=Y, guard=N |

## 股票基本面与估值

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `us-stock-analysis` | 68 | `direct` | md=5, scripts=0, workflows=0, output=Y, guard=N |
| 2 | `earnings-recap` | 68 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=N |
| 3 | `company-valuation` | 68 | `api-key` | md=6, scripts=0, workflows=0, output=Y, guard=Y |
| 4 | `estimate-analysis` | 58 | `api-key` | md=3, scripts=0, workflows=0, output=Y, guard=N |
| 5 | `earnings-preview` | 58 | `api-key` | md=3, scripts=0, workflows=0, output=Y, guard=N |

## 技术分析与交易计划

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `vcp-screener` | 78 | `api-key` | md=4, scripts=15, workflows=0, output=Y, guard=Y |
| 2 | `sepa-strategy` | 78 | `direct` | md=9, scripts=0, workflows=0, output=Y, guard=Y |
| 3 | `canslim-screener` | 78 | `api-key` | md=5, scripts=18, workflows=0, output=Y, guard=Y |
| 4 | `breakout-trade-planner` | 78 | `direct` | md=2, scripts=7, workflows=0, output=Y, guard=N |
| 5 | `technical-analyst` | 68 | `api-key` | md=3, scripts=0, workflows=0, output=Y, guard=Y |

## 股息与价值

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `kanchi-dividend-review-monitor` | 88 | `direct` | md=4, scripts=3, workflows=0, output=Y, guard=Y |
| 2 | `value-dividend-screener` | 78 | `api-key` | md=3, scripts=1, workflows=0, output=Y, guard=Y |
| 3 | `kanchi-dividend-sop` | 78 | `api-key` | md=5, scripts=19, workflows=0, output=Y, guard=Y |
| 4 | `dividend-growth-pullback-screener` | 78 | `api-key` | md=4, scripts=3, workflows=0, output=Y, guard=Y |

## 期权策略

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `llmquant-options` | 78 | `api-key+mcp-required` | md=11, scripts=0, workflows=11, output=Y, guard=Y |
| 2 | `options-strategy-advisor` | 68 | `api-key` | md=3, scripts=3, workflows=0, output=Y, guard=N |
| 3 | `options-payoff` | 58 | `direct` | md=4, scripts=0, workflows=0, output=N, guard=N |

## 回测与策略验证

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `pybroker-backtest-skill` | 100 | `direct` | md=3, scripts=5, workflows=2, output=Y, guard=Y |
| 2 | `edge-strategy-reviewer` | 78 | `direct` | md=3, scripts=3, workflows=0, output=Y, guard=N |
| 3 | `data-quality-checker` | 78 | `direct` | md=3, scripts=3, workflows=0, output=Y, guard=N |
| 4 | `backtest-expert` | 78 | `direct` | md=3, scripts=3, workflows=0, output=Y, guard=N |

## 组合仓位与风险

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `trader-memory-core` | 78 | `direct` | md=4, scripts=11, workflows=0, output=Y, guard=N |
| 2 | `position-sizer` | 78 | `direct` | md=2, scripts=3, workflows=0, output=Y, guard=N |
| 3 | `llmquant-risk` | 78 | `api-key+mcp-required` | md=5, scripts=0, workflows=5, output=Y, guard=Y |
| 4 | `llmquant-portfolio` | 78 | `api-key+mcp-required` | md=6, scripts=0, workflows=6, output=Y, guard=Y |
| 5 | `exposure-coach` | 78 | `api-key` | md=3, scripts=3, workflows=0, output=Y, guard=Y |
| 6 | `portfolio-manager` | 71 | `mcp-required` | md=10, scripts=2, workflows=0, output=Y, guard=N |

## 自选股监控

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `stock-monitor-skill` | 88 | `direct` | md=3, scripts=5, workflows=0, output=Y, guard=Y |
| 2 | `trader-memory-core` | 78 | `direct` | md=4, scripts=11, workflows=0, output=Y, guard=N |
| 3 | `llmquant-portfolio` | 78 | `api-key+mcp-required` | md=6, scripts=0, workflows=6, output=Y, guard=Y |

## 市场宽度与顶部底部

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `uptrend-analyzer` | 88 | `direct` | md=2, scripts=22, workflows=0, output=Y, guard=Y |
| 2 | `market-top-detector` | 78 | `api-key` | md=4, scripts=34, workflows=0, output=Y, guard=Y |
| 3 | `market-breadth-analyzer` | 78 | `direct` | md=2, scripts=22, workflows=0, output=Y, guard=N |
| 4 | `ibd-distribution-day-monitor` | 78 | `api-key` | md=3, scripts=19, workflows=0, output=Y, guard=Y |
| 5 | `ftd-detector` | 78 | `api-key` | md=3, scripts=10, workflows=0, output=Y, guard=Y |

## 社媒与市场情报

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `twitter-reader` | 78 | `direct` | md=4, scripts=0, workflows=0, output=Y, guard=Y |
| 2 | `telegram-reader` | 78 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=Y |
| 3 | `opencli-reader` | 78 | `direct` | md=4, scripts=0, workflows=0, output=Y, guard=Y |
| 4 | `linkedin-reader` | 78 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=Y |
| 5 | `discord-reader` | 78 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=Y |

## 创业投资研究

| Rank | Skill | 静态分 | 使用条件 | 证据 |
|---:|---|---:|---|---|
| 1 | `yc-reader` | 68 | `direct` | md=3, scripts=0, workflows=0, output=Y, guard=N |
| 2 | `startup-analysis` | 68 | `direct` | md=5, scripts=0, workflows=0, output=Y, guard=N |

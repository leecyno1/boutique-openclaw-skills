# Finance Skill Live Results - Round 2

本轮只测试当前环境能直接运行的技能。所有 API Key / MCP 依赖项暂不判负，进入待密钥复测池。

## 环境限制

当前环境缺少以下金融相关密钥：

- `LLMQUANT_API_KEY`
- `FUNDA_API_KEY`
- `FMP_API_KEY`
- `FINVIZ_API_KEY`
- `IMA_API_KEY`
- `IMA_CLIENT_ID`
- `TUSHARE_TOKEN`
- `STOCK_API_KEY`
- `OPENAI_API_KEY`
- `ADANOS_API_KEY`
- `ALPACA_API_KEY`

因此 LLMQuant、Funda、FMP、FinViz、Tushare、OpenAI/IMA、Alpaca 等能力只能做静态/流程评估，不能做真实数据效果评估。

## 实测结果

| Skill | 测试命令/场景 | 结果 | 评估 |
|---|---|---|---|
| `pybroker-backtest-skill` | `python3 -m pytest skills/default/pybroker-backtest-skill/tests -q` | 33 passed | 内置策略、离线模拟器和测试质量很好；可作为回测核心候选。 |
| `pybroker-backtest-skill` | `python3 skills/default/pybroker-backtest-skill/scripts/backtest.py --help` | 失败：`ModuleNotFoundError: No module named 'pybroker'` | CLI 运行前必须安装 `requirements.txt`；不影响保留，但安装脚本/README 应提示。 |
| `pybroker-backtest-skill` | 临时 venv 安装 `requirements.txt` 后运行 `backtest.py --help` | 成功 | 安装依赖后 CLI 可启动，说明缺口是环境依赖，不是脚本入口损坏。 |
| `pybroker-backtest-skill` | 临时 venv 跑 AAPL 2024-01-01 到 2024-03-01 样本回测 | 失败：Yahoo `YFRateLimitError` 导致空数据 | 与 `yfinance-data` 同源限流；策略逻辑可测，但真实数据链路需要缓存/重试/替代数据源。 |
| `stock-monitor-skill` | `cd skills/default/stock-monitor-skill/scripts && python3 test_suite.py` | 17 passed | 可真实获取新浪行情并触发预警；部分东财均线/均量接口受代理影响失败，但主流程仍能输出预警。 |
| `stock-monitor-skill` | `python3 skills/default/stock-monitor-skill/scripts/monitor.py` | 成功输出 6 条预警 | 实战输出可读，适合自选股监控核心；但依赖网络和部分外部接口稳定性。 |
| `position-sizer` | 账户 100000、入场 120、止损 112、单笔风险 1%、科技暴露 22% | 成功生成 JSON/Markdown | 输出 108 股、仓位 12960、风险 864/0.86%；可直接用于仓位管理。 |
| `yfinance-data` | `yf.download("AAPL MSFT NVDA", period="5d")` | yfinance 已安装，但 Yahoo rate limit 返回空数据 | skill 本身可用，但当前环境被 Yahoo 限流；需要稍后重试或加入失败降级逻辑。 |
| `market-breadth-analyzer` | 默认公开 CSV 拉取 | 首次失败：输出目录不存在；建目录后成功 | 核心计算有效，生成 46.2/100、Neutral、60-75% 权益暴露；脚本需要自动创建输出目录。 |
| `uptrend-analyzer` | 默认公开 CSV 拉取 | 成功 | 生成 60.1/100、Bull-Lower、80-90% 暴露建议；当前比 `market-breadth-analyzer` 更顺滑。 |

## 直接结论

### 已证明可直接运行

- `stock-monitor-skill`
- `position-sizer`
- `uptrend-analyzer`
- `market-breadth-analyzer`（需修复自动建目录）
- `pybroker-backtest-skill` 的离线核心测试

### 可保留但需安装/环境条件

- `pybroker-backtest-skill`：需要安装 `lib-pybroker` 等 requirements 后才能跑完整 CLI；真实行情仍受 Yahoo 限流影响。
- `yfinance-data`：无需 key，但 Yahoo 可能限流；应保留并要求输出中说明 rate limit / empty data。

### 待密钥/MCP复测

- `llmquant-*`
- `funda-data`
- `tushare-openclaw-skill`
- `openclaw-stock-data-skill`
- `canslim-screener`
- `vcp-screener`
- `value-dividend-screener`
- `options-strategy-advisor`
- `theme-detector`
- `macro-regime-detector`
- `economic-calendar-fetcher`
- `portfolio-manager`

## 第一轮择优变化

| 能力位 | 当前领先候选 | 理由 |
|---|---|---|
| 自选股监控 | `stock-monitor-skill` | 真实测试通过，输出预警可用。 |
| 仓位管理 | `position-sizer` | 直接输出仓位、金额、风险占比和报告文件。 |
| 回测 | `pybroker-backtest-skill` + `backtest-expert` | `pybroker` 有离线测试，`backtest-expert` 作为方法论补充，不算重复。 |
| 市场宽度 | `uptrend-analyzer` 暂领先 | 两者都能取数，`uptrend-analyzer` 无目录 bug，输出更顺。 |
| 美股数据 | `yfinance-data` 暂保留 | 当前被 Yahoo 限流，不能判负；需要稍后重试。 |

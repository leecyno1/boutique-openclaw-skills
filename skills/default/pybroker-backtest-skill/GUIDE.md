# pybroker-backtest-skill 使用指南

## 1. 功能定位
- 基于 PyBroker 的算法交易回测实验技能，支持技术指标策略、机器学习策略、Walkforward 前向验证、风险管理和回测报告。
- 仓库目录: `skills/default/pybroker-backtest-skill`
- 原生上游: https://github.com/gaaiyun/pybroker-backtest-skill

## 2. 使用前准备
```bash
pip install -r requirements.txt
```

## 3. 常用命令
```bash
python scripts/backtest.py --strategy basic --symbols AAPL MSFT --start 2022-01-01 --end 2023-12-31
python scripts/backtest.py --strategy ml --symbols AAPL --start 2022-01-01 --end 2023-12-31
```

## 4. 推荐提问方式
- 请用 pybroker-backtest-skill 回测这个策略并评估收益、回撤和稳定性。
- 请比较 RSI、MACD 和布林带策略在同一标的上的表现。

## 5. 注意事项
- 该技能目前作为实验区回测工具，不进入标准组合。
- 回测结果仅供研究，不构成投资建议。

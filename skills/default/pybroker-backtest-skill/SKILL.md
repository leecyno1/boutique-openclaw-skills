---
name: pybroker-backtest-skill
description: 基于 PyBroker 的算法交易回测实验技能。用于历史数据模拟、收益/回撤/稳定性评估、参数优化、技术指标策略和机器学习策略验证。
---

# PyBroker Backtest - 算法交易回测框架

## 描述

基于 PyBroker 的简化版算法交易回测工具。支持技术指标策略、机器学习策略集成和快速回测验证。

## 功能

- 技术指标策略（RSI、MACD、布林带等）
- 机器学习模型集成（scikit-learn）
- Walkforward 前向验证
- 风险管理（止损、止盈）
- 智能缓存加速
- 回测报告生成

## 使用方法

### 基础策略

```bash
# 运行示例策略
python scripts/backtest.py --strategy basic --symbols AAPL MSFT --start 2022-01-01 --end 2023-12-31

# 机器学习策略
python scripts/backtest.py --strategy ml --symbols AAPL --start 2022-01-01 --end 2023-12-31

# 生成报告
python scripts/backtest.py --strategy basic --symbols AAPL --report output/report.html
```

### Python API

```python
from pybroker_strategy import BacktestRunner

runner = BacktestRunner()

# 运行基础策略
result = runner.run_basic_strategy(
    symbols=['AAPL', 'MSFT'],
    start_date='2022-01-01',
    end_date='2023-12-31'
)

print(result.metrics_df)
```

## 安装

```bash
pip install -r requirements.txt
```

## 依赖

- lib-pybroker>=1.2.0
- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
- yfinance>=0.2.0

## 策略示例

### 突破策略
- 20 日最高价突破买入
- 持有 5 天
- 2% 止损

### RSI 策略
- RSI < 30 超卖买入
- RSI > 70 超买卖出
- 动态止损

### 机器学习策略
- 随机森林分类器
- 特征：RSI、MACD、成交量
- Walkforward 验证

## 输出格式

### 回测指标
```
Total Return: 25.3%
Sharpe Ratio: 1.45
Max Drawdown: -8.2%
Win Rate: 62%
```

## 注意事项

- 首次运行会下载历史数据
- 建议使用 3 年以上数据
- 仅供学习研究，不构成投资建议

## 致谢

基于 PyBroker 开源框架二次开发。

## 许可证

Apache 2.0 License

# PyBroker Backtest

算法交易回测框架，基于 PyBroker 简化开发。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行基础策略
python scripts/backtest.py --strategy basic --symbols AAPL MSFT

# 运行 RSI 策略
python scripts/backtest.py --strategy rsi --symbols AAPL --start 2022-01-01 --end 2023-12-31
```

## 功能特性

- 技术指标策略（突破、RSI）
- 快速回测引擎
- 风险管理（止损、止盈）
- 回测指标报告
- 智能缓存加速

## 策略说明

### 基础突破策略
- 20 日最高价突破买入
- 持有 5 天
- 2% 止损

### RSI 策略
- RSI < 30 超卖买入
- RSI > 70 超买卖出
- 3% 止损

## 输出示例

```
回测结果
============================================================
Total Return: 25.3%
Sharpe Ratio: 1.45
Max Drawdown: -8.2%
Win Rate: 62%
============================================================
```

## 注意事项

- 首次运行会下载历史数据
- 仅供学习研究，不构成投资建议

## 许可证

Apache 2.0 License

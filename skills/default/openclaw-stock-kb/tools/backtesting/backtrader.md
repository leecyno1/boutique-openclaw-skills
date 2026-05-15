# Backtrader 回测框架指南

## 简介

Backtrader 是 Python 最流行的回测框架之一，功能强大且易于使用。

## 安装

```bash
pip install backtrader
pip install backtrader[plotting]  # 包含绘图功能
```

## 基础示例

```python
import backtrader as bt
import datetime

# 创建策略
class SmaStrategy(bt.Strategy):
    params = (
        ('period', 20),
    )
    
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.period
        )
    
    def next(self):
        if self.data.close > self.sma:
            if not self.position:
                self.buy()
        elif self.data.close < self.sma:
            if self.position:
                self.sell()

# 创建Cerebro引擎
cerebro = bt.Cerebro()

# 添加数据
data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=datetime.datetime(2020, 1, 1),
    todate=datetime.datetime(2023, 12, 31)
)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(SmaStrategy)

# 设置初始资金
cerebro.broker.setcash(100000.0)

# 运行回测
print(f"初始资金: {cerebro.broker.getvalue():.2f}")
cerebro.run()
print(f"最终资金: {cerebro.broker.getvalue():.2f}")

# 绘图
cerebro.plot()
```

## 性能分析

```python
# 添加分析器
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

# 运行后获取结果
results = cerebro.run()
strat = results[0]

print(f"夏普比率: {strat.analyzers.sharpe.get_analysis()['sharperatio']:.2f}")
print(f"最大回撤: {strat.analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
```

## 参数优化

```python
# 添加参数范围
cerebro.optstrategy(
    SmaStrategy,
    period=range(10, 50, 5)
)

# 运行优化
results = cerebro.run(maxcpus=4)

# 找出最优参数
best_result = max(results, key=lambda x: x[0].analyzers.returns.get_analysis()['rnorm100'])
```

## 优点

- ✅ 功能全面
- ✅ 文档丰富
- ✅ 社区活跃

## 缺点

- ❌ 速度较慢（纯Python）
- ❌ 不支持多因子

## 相关

- [VectorBT](vectorbt.md) - 更快向量化回测
- [Zipline](zipline.md) - Quantopian出品

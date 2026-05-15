# 移动平均线 (MA - Moving Average)

## 指标概述

移动平均线是最基础也是最重要的技术分析工具，通过平滑价格数据来识别趋势方向。

## 计算方法

### 简单移动平均 (SMA)

```
SMA = (P1 + P2 + ... + Pn) / n

其中：
P = 价格（通常用收盘价）
n = 计算周期
```

```python
# Python 实现
def sma(prices, window):
    return prices.rolling(window=window).mean()
```

### 指数移动平均 (EMA)

EMA 给予近期价格更高权重，对价格变化更敏感。

```
EMA_today = (Price_today × k) + (EMA_yesterday × (1 - k))

其中：
k = 2 / (n + 1)  # 平滑因子
n = 周期
```

```python
def ema(prices, window):
    return prices.ewm(span=window, adjust=False).mean()
```

### 加权移动平均 (WMA)

线性加权，最新价格权重最高。

```python
def wma(prices, window):
    weights = np.arange(1, window + 1)
    return prices.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum())
```

## 交易信号

### 单均线策略

- **价格 > MA**: 上升趋势，考虑买入
- **价格 < MA**: 下降趋势，考虑卖出

### 双均线策略（金叉死叉）

- **金叉**: 短期均线上穿长期均线 → 买入信号
- **死叉**: 短期均线下穿长期均线 → 卖出信号

### 三均线系统

- 短期(5日)、中期(20日)、长期(60日)
- 多头排列：短 > 中 > 长 → 强势上涨
- 空头排列：短 < 中 < 长 → 强势下跌

## 常用参数

| 周期 | 用途 | 说明 |
|------|------|------|
| 5日 | 超短线 | 跟踪短期趋势 |
| 10日 | 短线 |  popular short-term |
| 20日 | 中线 | 月线，常用支撑/阻力 |
| 60日 | 中长线 | 季度线，判断中期趋势 |
| 120日 | 长线 | 半年线 |
| 250日 | 超长线 | 年线，牛熊分界 |

## Python 完整示例

```python
import pandas as pd
import matplotlib.pyplot as plt

# 计算多条均线
df['MA5'] = df['close'].rolling(window=5).mean()
df['MA20'] = df['close'].rolling(window=20).mean()
df['MA60'] = df['close'].rolling(window=60).mean()

# 双均线交叉信号
df['signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'signal'] = 1  # 买入
df.loc[df['MA5'] <= df['MA20'], 'signal'] = -1  # 卖出

# 找出交叉点
df['position'] = df['signal'].diff()
```

## 注意事项

1. **滞后性**: MA 是滞后指标，在震荡市会产生假信号
2. **参数优化**: 不同市场和品种需要调整周期
3. **结合使用**: 建议与其他指标（MACD、RSI）配合使用
4. **市场环境**: 趋势市效果好，震荡市效果差

## 相关指标

- [MACD](macd.md) - 基于 EMA 的指标
- [布林带](../volatility/bollinger.md) - 包含均线的波动率通道

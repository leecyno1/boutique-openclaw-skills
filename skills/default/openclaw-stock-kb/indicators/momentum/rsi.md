# RSI 相对强弱指数

## 概述

RSI（Relative Strength Index）由 Welles Wilder 于1978年提出，衡量价格变动的速度和幅度，判断超买超卖状态。

## 计算公式

```
RS = 平均上涨幅度 / 平均下跌幅度
RSI = 100 - (100 / (1 + RS))
```

## Python实现

```python
def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

## 交易信号

- RSI > 70：超买，考虑卖出
- RSI < 30：超卖，考虑买入
- RSI 50：多空分界线

## 背离交易

- 顶背离：价格新高，RSI未新高 → 卖出
- 底背离：价格新低，RSI未新低 → 买入

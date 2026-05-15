# 布林带 (Bollinger Bands)

## 概述

由 John Bollinger 发明，通过标准差衡量价格波动范围。

## 计算公式

```
中轨 = 20日SMA
上轨 = 中轨 + 2 × 20日标准差
下轨 = 中轨 - 2 × 20日标准差
```

## Python实现

```python
def bollinger_bands(prices, window=20, num_std=2):
    middle = prices.rolling(window).mean()
    std = prices.rolling(window).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return upper, middle, lower
```

## 交易信号

- 触及上轨：超买，考虑卖出
- 触及下轨：超卖，考虑买入
- 带宽收窄：波动率压缩，可能有大行情

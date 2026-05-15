# ATR 动态止损

## 原理

根据市场波动率动态调整止损位置，波动大时止损放宽，波动小时收紧。

## 计算

```python
def calculate_atr(high, low, close, window=14):
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window).mean()
    return atr

# 止损设置
stop_loss = entry_price - 2 * atr
```

## 优点

- 自适应市场波动
- 避免被正常波动止损

# 动量策略 (Momentum Strategy)

## 原理

"追涨杀跌"，买入近期表现强势的股票，卖出表现弱势的。

## 实现

```python
def momentum_strategy(prices, lookback=20):
    # 计算N日收益率
    returns = prices.pct_change(lookback)
    # 排序选择前10%
    top_performers = returns.nlargest(int(len(returns) * 0.1))
    return top_performers.index
```

## 风险

- 趋势反转时亏损大
- 需要严格止损

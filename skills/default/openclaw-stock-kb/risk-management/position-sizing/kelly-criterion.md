# 凯利公式仓位管理

## 原理

凯利公式（Kelly Criterion）由 John Kelly 于1956年提出，用于计算最优投资比例，最大化长期收益。

## 公式

```
f = (p × b - q) / b

其中：
f = 最优投资比例（0-1）
p = 胜率（赢的概率）
q = 败率 = 1 - p
b = 盈亏比（平均盈利/平均亏损）
```

## Python实现

```python
def kelly_criterion(win_rate, win_loss_ratio):
    """
    计算凯利公式最优仓位
    
    Parameters:
    -----------
    win_rate : float - 胜率 (0-1)
    win_loss_ratio : float - 盈亏比（平均盈利/平均亏损）
    
    Returns:
    --------
    kelly_fraction : float - 最优投资比例
    """
    loss_rate = 1 - win_rate
    kelly = (win_rate * win_loss_ratio - loss_rate) / win_loss_ratio
    
    # 限制在0-1之间
    return max(0, min(kelly, 1))

# 示例
# 胜率55%，盈亏比2:1
position = kelly_criterion(0.55, 2.0)
print(f"凯利最优仓位: {position*100:.1f}%")  # 输出: 32.5%
```

## 实战应用

### 回测统计

```python
def calculate_trade_stats(trades):
    """从交易记录计算胜率和盈亏比"""
    wins = [t for t in trades if t['pnl'] > 0]
    losses = [t for t in trades if t['pnl'] <= 0]
    
    win_rate = len(wins) / len(trades)
    avg_win = sum(t['pnl'] for t in wins) / len(wins)
    avg_loss = abs(sum(t['pnl'] for t in losses) / len(losses))
    win_loss_ratio = avg_win / avg_loss
    
    return win_rate, win_loss_ratio

# 根据历史交易计算最优仓位
win_rate, ratio = calculate_trade_stats(historical_trades)
kelly_position = kelly_criterion(win_rate, ratio)
```

### 分数凯利

```python
def fractional_kelly(win_rate, win_loss_ratio, fraction=0.5):
    """
    分数凯利：降低风险
    
    很多交易者使用半凯利(0.5)或四分之一凯利(0.25)
    以减少波动和回撤
    """
    full_kelly = kelly_criterion(win_rate, win_loss_ratio)
    return full_kelly * fraction

# 半凯利
half_kelly = fractional_kelly(0.55, 2.0, 0.5)  # 16.25%
```

## 风险管理

### 最大仓位限制

```python
def safe_position_size(win_rate, win_loss_ratio, max_position=0.25):
    """
    安全仓位：凯利公式+最大限制
    """
    kelly = kelly_criterion(win_rate, win_loss_ratio)
    return min(kelly, max_position)
```

### 连续亏损调整

```python
def adaptive_kelly(base_win_rate, recent_trades, lookback=20):
    """
    根据近期表现调整
    
    连续亏损时降低仓位，连胜时维持
    """
    recent = recent_trades[-lookback:]
    recent_win_rate = len([t for t in recent if t['pnl'] > 0]) / len(recent)
    
    # 使用近期胜率与基础胜率的加权平均
    adjusted_win_rate = 0.7 * base_win_rate + 0.3 * recent_win_rate
    
    return kelly_criterion(adjusted_win_rate, win_loss_ratio)
```

## 注意事项

1. **参数估计误差**：胜率和盈亏比是历史统计，不代表未来
2. **波动大**：纯凯利公式回撤可能很大
3. **建议使用分数凯利**：半凯利或三分之一凯利
4. **定期重新计算**：交易记录更新后重新评估

## 相关阅读

- [固定分数法](fixed-fractional.md)
- [波动率仓位](volatility-sizing.md)
- [最大回撤控制](../portfolio/max-drawdown.md)

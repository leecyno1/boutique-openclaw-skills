# 固定比例止损策略

## 核心原则

**任何单笔交易的亏损不得超过总资金的固定比例**。

这是最简单也最有效的风险管理方法。

## 常用比例

| 风险承受度 | 单笔止损比例 | 适用人群 |
|------------|--------------|----------|
| 保守型 | 1%-2% | 新手、大资金 |
| 稳健型 | 2%-3% | 有经验交易者 |
| 激进型 | 3%-5% | 高风险偏好 |
| 赌博型 | >5% | 不建议 |

## 计算方法

### 基础公式

```
止损价格 = 入场价格 × (1 - 止损比例)

亏损金额 = 持仓数量 × (入场价格 - 止损价格)
        = 总资金 × 止损比例
```

### Python 实现

```python
def calculate_stop_loss(entry_price, stop_percent=0.02):
    """
    计算止损价格
    
    Parameters:
    -----------
    entry_price : float
        入场价格
    stop_percent : float
        止损比例，默认2%
    
    Returns:
    --------
    stop_loss_price : float
        止损价格
    """
    stop_loss_price = entry_price * (1 - stop_percent)
    return round(stop_loss_price, 2)

def calculate_position_size(total_capital, risk_percent, entry_price, stop_loss):
    """
    根据风险计算仓位大小
    
    Parameters:
    -----------
    total_capital : float
        总资金
    risk_percent : float
        愿意承担的风险比例
    entry_price : float
        入场价格
    stop_loss : float
        止损价格
    """
    risk_amount = total_capital * risk_percent
    risk_per_share = entry_price - stop_loss
    position_size = risk_amount / risk_per_share
    
    return int(position_size)

# 示例
# 10万资金，2%风险，100元买入，98元止损
# 可买数量 = 100000 × 0.02 / (100 - 98) = 1000股
```

## 实际应用

### 买入时设置

```python
def place_order_with_stop(symbol, entry_price, capital, risk_percent=0.02):
    """下单并设置止损"""
    
    # 计算止损价
    stop_price = calculate_stop_loss(entry_price, risk_percent)
    
    # 计算仓位
    shares = calculate_position_size(capital, risk_percent, entry_price, stop_price)
    
    # 下单（伪代码）
    order = {
        'symbol': symbol,
        'action': 'buy',
        'shares': shares,
        'entry_price': entry_price,
        'stop_loss': stop_price,
        'max_loss': capital * risk_percent
    }
    
    print(f"买入 {shares} 股 {symbol} @ ${entry_price}")
    print(f"止损价: ${stop_price} (风险: {risk_percent*100}%)")
    print(f"最大亏损: ${capital * risk_percent:.2f}")
    
    return order
```

### 移动止损（保护利润）

```python
def trailing_stop(current_price, highest_price, trailing_percent=0.10):
    """
    移动止损
    
    当价格上涨后，止损价跟随上移，保护已获利润
    """
    stop_price = highest_price * (1 - trailing_percent)
    
    # 如果当前价格触及止损
    if current_price <= stop_price:
        return 'SELL'
    
    return 'HOLD'

# 示例
# 买入价 100，最高涨到 120，移动止损 10%
# 止损价 = 120 × 0.9 = 108
# 即使跌回 108，仍盈利 8%
```

## 连续止损应对

### 最大日亏损限制

```python
class DailyRiskManager:
    def __init__(self, max_daily_loss=0.06):
        self.max_daily_loss = max_daily_loss  # 单日最大亏损 6%
        self.daily_pnl = 0
        self.trading_halted = False
    
    def update_pnl(self, trade_pnl):
        """更新当日盈亏"""
        self.daily_pnl += trade_pnl
        
        # 检查是否触发日止损
        if self.daily_pnl <= -self.max_daily_loss:
            self.trading_halted = True
            print(f"⚠️ 单日亏损达 {abs(self.daily_pnl)*100}%，停止交易！")
        
        return self.trading_halted
```

## 心理学角度

### 为什么固定比例止损有效？

1. **可预测性**: 每笔交易的最大亏损已知，不会恐慌
2. **一致性**: 不因情绪随意改变止损
3. **数学优势**: 小亏大赚，长期期望值为正

### 常见错误

- ❌ 亏损后扩大止损"等反弹"
- ❌ 盈利后过早止盈
- ❌ 不止损，变"长期投资"
- ❌ 不同仓位使用不同止损比例

## 相关策略

- [ATR 动态止损](atr-stop.md) - 根据波动率调整
- [时间止损](time-stop.md) - 持仓时间限制
- [技术位止损](technical-stop.md) - 支撑/均线止损
- [凯利公式仓位](../position-sizing/kelly-criterion.md)

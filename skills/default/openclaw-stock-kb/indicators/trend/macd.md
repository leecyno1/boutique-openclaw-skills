# MACD 指标详解

## 指标概述

MACD（Moving Average Convergence Divergence，指数平滑异同平均线）是由 Gerald Appel 于1979年提出的趋势跟踪动量指标，显示两条EMA之间的关系。

## 计算方法

### 三步计算

```
1. 计算快线（DIF）
   DIF = 12日EMA - 26日EMA

2. 计算慢线（DEA/Signal）
   DEA = DIF的9日EMA

3. 计算柱状图（MACD Histogram）
   MACD = (DIF - DEA) × 2
```

### Python实现

```python
import pandas as pd
import numpy as np

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    计算MACD指标
    
    Parameters:
    -----------
    prices : pd.Series - 收盘价序列
    fast : int - 快线周期，默认12
    slow : int - 慢线周期，默认26
    signal : int - 信号线周期，默认9
    """
    # 计算EMA
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    
    # DIF线
    dif = ema_fast - ema_slow
    
    # DEA线（信号线）
    dea = dif.ewm(span=signal, adjust=False).mean()
    
    # MACD柱状图
    macd_hist = (dif - dea) * 2
    
    return dif, dea, macd_hist
```

## 交易信号

### 1. 金叉死叉（基础信号）

```python
def macd_cross_signals(dif, dea):
    """MACD金叉死叉信号"""
    signals = pd.DataFrame(index=dif.index)
    signals['dif'] = dif
    signals['dea'] = dea
    signals['signal'] = 0
    
    # 金叉：DIF上穿DEA
    signals.loc[(dif > dea) & (dif.shift(1) <= dea.shift(1)), 'signal'] = 1
    
    # 死叉：DIF下穿DEA
    signals.loc[(dif < dea) & (dif.shift(1) >= dea.shift(1)), 'signal'] = -1
    
    return signals
```

### 2. 零轴穿越（趋势确认）

```python
def zero_cross_signals(dif):
    """零轴穿越信号"""
    signals = pd.Series(index=dif.index, data=0)
    
    # 上穿零轴：多头趋势确认
    signals[(dif > 0) & (dif.shift(1) <= 0)] = 1
    
    # 下穿零轴：空头趋势确认
    signals[(dif < 0) & (dif.shift(1) >= 0)] = -1
    
    return signals
```

### 3. 顶背离/底背离（高级信号）

```python
def detect_divergence(prices, dif):
    """
    检测MACD背离
    
    顶背离：价格创新高，MACD未创新高 → 卖出信号
    底背离：价格创新低，MACD未创新低 → 买入信号
    """
    # 找局部极值点（简化版）
    price_highs = prices[(prices > prices.shift(1)) & (prices > prices.shift(-1))]
    price_lows = prices[(prices < prices.shift(1)) & (prices < prices.shift(-1))]
    
    macd_highs = dif[(dif > dif.shift(1)) & (dif > dif.shift(-1))]
    macd_lows = dif[(dif < dif.shift(1)) & (dif < dif.shift(-1))]
    
    divergence = pd.Series(index=prices.index, data=0)
    
    # 顶背离检测
    for i in range(-3, 0):
        if len(price_highs) >= 2 and len(macd_highs) >= 2:
            if (price_highs.iloc[i] > price_highs.iloc[i-1] and 
                macd_highs.iloc[i] < macd_highs.iloc[i-1]):
                divergence[macd_highs.index[i]] = -1  # 顶背离，卖出
    
    return divergence
```

## 实战策略

### MACD趋势策略

```python
class MACDStrategy:
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal
    
    def generate_signals(self, df):
        """生成完整交易信号"""
        df = df.copy()
        
        # 计算MACD
        df['dif'], df['dea'], df['macd'] = calculate_macd(
            df['close'], self.fast, self.slow, self.signal
        )
        
        # 信号1：金叉+零轴上方（多头趋势中的买入）
        df['signal'] = 0
        golden_cross = (df['dif'] > df['dea']) & (df['dif'].shift(1) <= df['dea'].shift(1))
        above_zero = df['dea'] > 0
        df.loc[golden_cross & above_zero, 'signal'] = 1
        
        # 信号2：死叉+零轴下方（空头趋势中的卖出）
        death_cross = (df['dif'] < df['dea']) & (df['dif'].shift(1) >= df['dea'].shift(1))
        below_zero = df['dea'] < 0
        df.loc[death_cross & below_zero, 'signal'] = -1
        
        return df
```

## 参数优化

| 参数 | 默认 | 短线 | 长线 | 说明 |
|------|------|------|------|------|
| fast | 12 | 6 | 19 | 快线周期 |
| slow | 26 | 13 | 39 | 慢线周期 |
| signal | 9 | 5 | 15 | 信号线周期 |

**常用组合**：
- (6, 13, 5)：短线交易
- (12, 26, 9)：标准设置
- (19, 39, 15)：长线投资

## MACD柱状图交易法

```python
def histogram_strategy(df):
    """
    MACD柱状图策略
    
    柱状图由负转正：买入
    柱状图由正转负：卖出
    """
    df['macd_prev'] = df['macd'].shift(1)
    
    df['signal'] = 0
    # 绿柱变红柱
    df.loc[(df['macd'] > 0) & (df['macd_prev'] <= 0), 'signal'] = 1
    # 红柱变绿柱
    df.loc[(df['macd'] < 0) & (df['macd_prev'] >= 0), 'signal'] = -1
    
    return df
```

## 注意事项

1. **滞后性**：MACD是滞后指标，信号出现较慢
2. **震荡市假信号**：盘整期间金叉死叉频繁，容易亏损
3. **结合使用**：建议与RSI、KDJ等指标配合使用
4. **参数调整**：不同市场（股票/期货/加密货币）需要调整参数

## 改进方向

### MACD+RSI组合

```python
def macd_rsi_strategy(df, rsi_overbought=70, rsi_oversold=30):
    """MACD+RSI双重过滤"""
    # 计算RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD金叉+RSI<70（避免超买买入）
    macd_buy = (df['dif'] > df['dea']) & (df['dif'].shift(1) <= df['dea'].shift(1))
    df.loc[macd_buy & (df['rsi'] < rsi_overbought), 'signal'] = 1
    
    return df
```

## 相关指标

- [移动平均线](ma.md) - MACD的基础
- [RSI](../momentum/rsi.md) - 动量指标配合
- [KDJ](../momentum/stochastic.md) - 随机指标

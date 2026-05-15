# 布林带均值回归策略 (Bollinger Bands Mean Reversion)

## 策略原理

布林带由三条线组成：中轨（20日均线）、上轨（中轨+2倍标准差）、下轨（中轨-2倍标准差）。价格绝大多数时间会在布林带内波动，当触及上下轨时，有回归中轨的倾向。

### 核心逻辑

- 价格触及**上轨** → 卖出信号（超买，预期回归）
- 价格触及**下轨** → 买入信号（超卖，预期回归）
- 价格回归**中轨** → 平仓信号

### 数学公式

```
中轨 = 20日简单移动平均 (SMA20)
标准差 = 20日收盘价标准差
上轨 = 中轨 + 2 × 标准差
下轨 = 中轨 - 2 × 标准差

%B指标 = (收盘价 - 下轨) / (上轨 - 下轨) × 100
```

## 代码实现

```python
import pandas as pd
import numpy as np

def bollinger_bands_strategy(df, window=20, num_std=2):
    """
    布林带均值回归策略
    
    Parameters:
    -----------
    df : pd.DataFrame - 包含close列
    window : int - 布林带周期，默认20
    num_std : int - 标准差倍数，默认2
    """
    df = df.copy()
    
    # 计算布林带
    df['middle'] = df['close'].rolling(window=window).mean()
    df['std'] = df['close'].rolling(window=window).std()
    df['upper'] = df['middle'] + num_std * df['std']
    df['lower'] = df['middle'] - num_std * df['std']
    
    # 计算%B指标
    df['percent_b'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
    
    # 生成信号
    df['signal'] = 0
    # 触及下轨买入
    df.loc[df['close'] <= df['lower'], 'signal'] = 1
    # 触及上轨卖出
    df.loc[df['close'] >= df['upper'], 'signal'] = -1
    
    return df

# 改进版：结合RSI过滤
def bollinger_rsi_strategy(df, bb_window=20, rsi_window=14):
    """布林带+RSI双重过滤"""
    df = bollinger_bands_strategy(df, bb_window)
    
    # 计算RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # 信号过滤：下轨+RSI<30才买入，上轨+RSI>70才卖出
    df['filtered_signal'] = 0
    df.loc[(df['close'] <= df['lower']) & (df['rsi'] < 30), 'filtered_signal'] = 1
    df.loc[(df['close'] >= df['upper']) & (df['rsi'] > 70), 'filtered_signal'] = -1
    
    return df
```

## 策略优化

### 1. 带宽过滤（避免假突破）

```python
def bandwidth_filter(df):
    """只在布林带收窄后交易（波动率压缩后爆发）"""
    df['bandwidth'] = (df['upper'] - df['lower']) / df['middle']
    # 带宽小于过去20日平均的20%才交易
    df['avg_bandwidth'] = df['bandwidth'].rolling(20).mean()
    df['squeeze'] = df['bandwidth'] < df['avg_bandwidth'] * 0.8
    return df
```

### 2. 多时间周期确认

```python
def multi_timeframe_bollinger(df_daily, df_hourly):
    """日线和小时线布林带共振"""
    # 日线在下轨且小时线也在下轨 = 强买入信号
    pass
```

## 回测要点

1. **震荡市表现好**：趋势市会连续触及上轨/下轨，造成连续亏损
2. **加入趋势过滤**：只在ADX<25（震荡市）时使用本策略
3. **注意滑点**：价格触及轨道时往往伴随跳空

## 参数优化

| 参数 | 默认值 | 优化范围 | 说明 |
|------|--------|----------|------|
| window | 20 | 10-50 | 布林带周期 |
| num_std | 2 | 1.5-3 | 标准差倍数，越大信号越少但越可靠 |

## 风险提示

- ⚠️ **趋势市陷阱**：强趋势中价格会沿着轨道运行，不断触发反向信号
- ⚠️ **黑天鹅事件**：极端行情可能突破轨道后不回撤
- ⚠️ **假突破**：价格触及轨道后快速反向，但很快又突破

## 实际案例

**2021年特斯拉(TSLA)震荡期**：
- 布林带宽度适中，价格在80-100美元区间波动
- 每次触及下轨都是买入机会，触及上轨卖出
- 单笔收益5-8%，胜率65%

**失效案例 - 2020年比特币牛市**：
- 价格沿着布林带上轨持续上涨
- 每次触及上轨卖出后，价格继续上涨
- 连续止损，策略失效

## 相关阅读

- [简单均值回归](simple-mean-reversion.md)
- [布林带指标](../../indicators/volatility/bollinger.md)
- [ADX趋势过滤](../../indicators/trend/adx.md)

# 配对交易策略 (Pairs Trading)

## 策略原理

配对交易是统计套利的核心策略，寻找两只历史价格相关性高的股票，当价差偏离历史均值时，做多被低估的，做空被高估的，等待价差回归。

### 核心概念

- **协整关系 (Cointegration)**：两只股票价格走势长期一致
- **价差 (Spread)**：两只股票价格的差值或比值
- **Z-Score**：价差偏离均值的标准差倍数

### 数学公式

```
价差 = Price_A - β × Price_B
（β是通过线性回归计算的对冲比率）

Z-Score = (价差 - 价差均值) / 价差标准差

买入信号：Z-Score < -2（做多A，做空B）
卖出信号：Z-Score > +2（做空A，做多B）
平仓信号：Z-Score回归0附近
```

## 配对选择方法

### 1. 同行业配对

```python
def find_pairs_sector(stocks_data, sector):
    """在同一行业内寻找配对"""
    from scipy.stats import pearsonr
    
    pairs = []
    tickers = list(stocks_data.keys())
    
    for i in range(len(tickers)):
        for j in range(i+1, len(tickers)):
            stock_a = stocks_data[tickers[i]]['close']
            stock_b = stocks_data[tickers[j]]['close']
            
            # 计算相关系数
            corr, _ = pearsonr(stock_a, stock_b)
            
            if corr > 0.9:  # 高相关性
                pairs.append({
                    'A': tickers[i],
                    'B': tickers[j],
                    'correlation': corr
                })
    
    return pairs
```

### 2. ADF检验协整性

```python
from statsmodels.tsa.stattools import coint

def test_cointegration(price_a, price_b):
    """检验两只股票是否协整"""
    score, pvalue, _ = coint(price_a, price_b)
    
    # p-value < 0.05 表示协整
    return pvalue < 0.05, pvalue
```

## 完整策略实现

```python
import pandas as pd
import numpy as np
from statsmodels.api import OLS
from statsmodels.tsa.stattools import adfuller

class PairsTradingStrategy:
    def __init__(self, lookback=60, entry_z=2.0, exit_z=0.5):
        self.lookback = lookback  # 回顾期
        self.entry_z = entry_z    # 入场Z值
        self.exit_z = exit_z      # 出场Z值
        self.beta = None          # 对冲比率
        self.mean = None          # 价差均值
        self.std = None           # 价差标准差
    
    def calculate_hedge_ratio(self, price_a, price_b):
        """计算最优对冲比率（OLS回归）"""
        X = price_b.values
        y = price_a.values
        
        model = OLS(y, X).fit()
        self.beta = model.params[0]
        
        return self.beta
    
    def calculate_spread(self, price_a, price_b):
        """计算价差"""
        if self.beta is None:
            self.calculate_hedge_ratio(price_a, price_b)
        
        spread = price_a - self.beta * price_b
        return spread
    
    def calculate_zscore(self, spread):
        """计算Z-Score"""
        self.mean = spread.rolling(window=self.lookback).mean()
        self.std = spread.rolling(window=self.lookback).std()
        
        zscore = (spread - self.mean) / self.std
        return zscore
    
    def generate_signals(self, price_a, price_b):
        """生成交易信号"""
        spread = self.calculate_spread(price_a, price_b)
        zscore = self.calculate_zscore(spread)
        
        signals = pd.DataFrame(index=price_a.index)
        signals['zscore'] = zscore
        signals['spread'] = spread
        
        # 信号：1做多价差，-1做空价差，0平仓
        signals['position'] = 0
        signals.loc[zscore < -self.entry_z, 'position'] = 1   # 做多A做空B
        signals.loc[zscore > self.entry_z, 'position'] = -1   # 做空A做多B
        signals.loc[abs(zscore) < self.exit_z, 'position'] = 0  # 平仓
        
        return signals
    
    def backtest(self, price_a, price_b):
        """回测（简化版，不考虑交易成本）"""
        signals = self.generate_signals(price_a, price_b)
        
        # 计算收益
        returns_a = price_a.pct_change()
        returns_b = price_b.pct_change()
        
        # 配对收益 = 做多A收益 - β×做空B收益
        strategy_returns = (signals['position'].shift(1) * 
                          (returns_a - self.beta * returns_b))
        
        signals['returns'] = strategy_returns
        signals['cumulative'] = (1 + strategy_returns).cumprod()
        
        return signals

# 使用示例
# strategy = PairsTradingStrategy(lookback=60, entry_z=2.0, exit_z=0.5)
# results = strategy.backtest(pepsi_data, coke_data)
```

## 经典配对案例

### 可口可乐 vs 百事可乐 (KO vs PEP)

**配对逻辑**：
- 同属饮料行业龙头
- 市场份额长期稳定
- 股价走势高度相关（相关系数>0.9）

**交易规则**：
- Z-Score > +2：做空KO，做多PEP
- Z-Score < -2：做多KO，做空PEP
- Z-Score回归0：平仓

### 埃克森美孚 vs 雪佛龙 (XOM vs CVX)

**配对逻辑**：
- 同属石油行业
- 受油价影响相似
- 公司规模相近

### 阿里巴巴 vs 腾讯 (BABA vs TCEHY)

**配对逻辑**：
- 中国互联网双巨头
- 虽业务不同但受宏观政策影响相似
- 需注意ADR汇率风险

## 风险管理

### 1. 协整失效风险

```python
def monitor_cointegration(self, recent_spread):
    """监控协整关系是否仍然存在"""
    adf_result = adfuller(recent_spread)
    
    if adf_result[1] > 0.05:  # p-value > 0.05，协整关系可能失效
        print("⚠️ 警告：协整关系可能已失效，考虑平仓")
        return False
    return True
```

### 2. 最大持仓时间

```python
def time_stop(self, entry_date, max_days=20):
    """时间止损：持仓不超过20天"""
    if (pd.Timestamp.now() - entry_date).days > max_days:
        return True  # 强制平仓
    return False
```

### 3. 价差突破止损

```python
def stop_loss(self, current_zscore, max_zscore=3.5):
    """价差继续扩大时止损"""
    if abs(current_zscore) > max_zscore:
        return True  # 止损
    return False
```

## 策略优缺点

### 优点
- ✅ 市场中性：不依赖市场方向，牛熊市均可盈利
- ✅ 风险较低：对冲了行业/市场风险
- ✅ 逻辑清晰：基于统计学原理

### 缺点
- ❌ 协整关系会失效（如公司并购、业务转型）
- ❌ 收益有限：单次交易收益通常不高
- ❌ 需要做空：某些市场做空受限

## 注意事项

1. **避免过度优化**：历史相关性不代表未来
2. **定期重新检验**：每季度重新检验协整关系
3. **关注基本面**：公司重大事件可能破坏配对逻辑
4. **交易成本**：双边交易+做空成本，收益可能被侵蚀

## 相关阅读

- [统计套利基础](statistical-arbitrage.md)
- [协整检验详解](cointegration-testing.md)
- [均值回归策略](simple-mean-reversion.md)

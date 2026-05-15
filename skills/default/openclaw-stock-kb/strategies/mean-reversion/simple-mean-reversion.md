# 简单均值回归策略 (Simple Mean Reversion)

## 策略原理

均值回归是基于统计学原理的交易策略，认为价格无论高于或低于均值，最终都会回归到均值附近。

### 核心逻辑

当价格偏离移动平均线达到一定程度时，做空；当价格回归时平仓。

### 数学公式

```
偏离度 = (价格 - N日移动平均) / N日移动平均 × 100%

买入信号：偏离度 < -阈值 (例如 -2%)
卖出信号：偏离度 > 阈值 (例如 +2%) 或回归均线
```

## 代码实现

```python
import pandas as pd
import numpy as np

def simple_mean_reversion(data, window=20, threshold=0.02):
    """
    简单均值回归策略
    
    Parameters:
    -----------
    data : pd.DataFrame
        包含 'close' 列的价格数据
    window : int
        移动平均窗口期，默认20日
    threshold : float
        偏离阈值，默认0.02 (2%)
    """
    # 计算移动平均
    data['ma'] = data['close'].rolling(window=window).mean()
    
    # 计算偏离度
    data['deviation'] = (data['close'] - data['ma']) / data['ma']
    
    # 生成信号
    data['signal'] = 0
    data.loc[data['deviation'] < -threshold, 'signal'] = 1  # 买入
    data.loc[data['deviation'] > threshold, 'signal'] = -1  # 卖出
    
    return data

# 使用示例
# signals = simple_mean_reversion(df, window=20, threshold=0.02)
```

## 参数优化

| 参数 | 说明 | 推荐范围 |
|------|------|----------|
| window | 移动平均周期 | 10-60日 |
| threshold | 偏离阈值 | 1%-5% |

## 回测要点

1. **选择合适的市场**：震荡市场效果好，趋势市场容易逆势
2. **加入趋势过滤**：只在长期趋势向上的品种上使用
3. **设置止损**：防止"接飞刀"

## 风险提示

- 在强趋势行情中可能持续亏损
- 需要充足的保证金应对回撤
- 流动性差的品种滑点大

## 相关阅读

- [布林带均值回归](bollinger-mean-reversion.md)
- [配对交易](pairs-trading.md)
- [ATR 止损](../../risk-management/stop-loss/atr-stop.md)

"""Headless 策略库（v2）。

v1 的 ``scripts/backtest.py`` 把策略逻辑混在 PyBroker 的 ``exec_fn`` 闭包里，
没法单独测、没法离线跑、没法在不装 PyBroker 的环境用。

v2 把策略逻辑抽成纯 Python 函数：输入 OHLC + indicators，输出 BUY / SELL /
HOLD 信号。这样：

1. 单元测试不依赖 PyBroker / YFinance / 网络
2. 离线快速回测可以直接喂这些函数
3. PyBroker / Backtrader / 其他框架想用，把信号函数包一层 adapter 即可

四个内置策略（覆盖经典量化场景）：

- **breakout_20day**：20 日突破（Donchian Channel 简化）
- **rsi_reversal**：RSI < 30 抄底 / RSI > 70 止盈
- **ma_crossover**：双均线金叉死叉
- **bollinger_revert**：布林带均值回归
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional, Sequence


Signal = Literal["BUY", "SELL", "HOLD"]


@dataclass
class StrategySignal:
    action: Signal
    reason: str = ""
    confidence: float = 0.0      # 0~1 信号强度（供 sizing）

    def to_dict(self) -> dict:
        return {"action": self.action, "reason": self.reason,
                "confidence": float(self.confidence)}


# --- 辅助 ----------------------------------------------------------------

def _sma(prices: Sequence[float], period: int) -> Optional[float]:
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def _rsi(prices: Sequence[float], period: int = 14) -> Optional[float]:
    """简化 RSI（SMA 版而非 Wilder）。"""
    if len(prices) < period + 1:
        return None
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss < 1e-12:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def _stddev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return var ** 0.5


# --- 4 个策略 ------------------------------------------------------------

def breakout_20day(prices: Sequence[float], has_position: bool,
                    period: int = 20) -> StrategySignal:
    """突破 N 日最高价 → 买入；持仓中创新低 → 卖出。

    Donchian Channel 简化版（Turtle Traders 入门）。
    """
    if len(prices) < period + 1:
        return StrategySignal("HOLD", "数据不足")
    window_high = max(prices[-period:])
    window_low = min(prices[-period:])
    current = prices[-1]
    prev_high = max(prices[-period - 1:-1])

    if not has_position and current > prev_high:
        return StrategySignal("BUY",
            f"突破前 {period} 日最高价 {prev_high:.2f}",
            confidence=min((current - prev_high) / prev_high, 0.1) * 10)
    if has_position and current < window_low * 1.01:
        return StrategySignal("SELL",
            f"跌破 {period} 日最低区域 {window_low:.2f}",
            confidence=0.6)
    return StrategySignal("HOLD", "区间内")


def rsi_reversal(prices: Sequence[float], has_position: bool,
                  period: int = 14, oversold: float = 30,
                  overbought: float = 70) -> StrategySignal:
    """RSI 反转。"""
    rsi = _rsi(prices, period)
    if rsi is None:
        return StrategySignal("HOLD", f"数据不足 RSI({period})")
    if not has_position and rsi < oversold:
        return StrategySignal("BUY",
            f"RSI={rsi:.1f} < {oversold}（超卖）",
            confidence=(oversold - rsi) / oversold)
    if has_position and rsi > overbought:
        return StrategySignal("SELL",
            f"RSI={rsi:.1f} > {overbought}（超买）",
            confidence=(rsi - overbought) / (100 - overbought))
    return StrategySignal("HOLD", f"RSI={rsi:.1f}（中性区）")


def ma_crossover(prices: Sequence[float], has_position: bool,
                  fast: int = 10, slow: int = 30) -> StrategySignal:
    """双均线交叉。fast 上穿 slow → 买；下穿 → 卖。"""
    if fast >= slow:
        raise ValueError(f"fast ({fast}) 必须 < slow ({slow})")
    if len(prices) < slow + 1:
        return StrategySignal("HOLD", f"数据不足 MA{slow}")
    fast_now = _sma(prices, fast)
    slow_now = _sma(prices, slow)
    fast_prev = _sma(prices[:-1], fast)
    slow_prev = _sma(prices[:-1], slow)
    if None in (fast_now, slow_now, fast_prev, slow_prev):
        return StrategySignal("HOLD", "MA 不可用")

    # Golden cross
    if not has_position and fast_prev <= slow_prev and fast_now > slow_now:
        return StrategySignal("BUY",
            f"MA{fast}={fast_now:.2f} 上穿 MA{slow}={slow_now:.2f}",
            confidence=0.7)
    # Death cross
    if has_position and fast_prev >= slow_prev and fast_now < slow_now:
        return StrategySignal("SELL",
            f"MA{fast}={fast_now:.2f} 下穿 MA{slow}={slow_now:.2f}",
            confidence=0.7)
    return StrategySignal("HOLD", "无交叉")


def bollinger_revert(prices: Sequence[float], has_position: bool,
                      period: int = 20, n_std: float = 2.0
                      ) -> StrategySignal:
    """布林带均值回归：触下轨买，触上轨卖。"""
    if len(prices) < period:
        return StrategySignal("HOLD", f"数据不足 BB({period})")
    window = list(prices[-period:])
    mid = sum(window) / period
    std = _stddev(window)
    if std < 1e-12:
        return StrategySignal("HOLD", "波动率为零")
    upper = mid + n_std * std
    lower = mid - n_std * std
    current = prices[-1]

    if not has_position and current <= lower:
        return StrategySignal("BUY",
            f"触下轨 {lower:.2f}（当前 {current:.2f}）",
            confidence=min((lower - current) / std, 1.0))
    if has_position and current >= upper:
        return StrategySignal("SELL",
            f"触上轨 {upper:.2f}（当前 {current:.2f}）",
            confidence=min((current - upper) / std, 1.0))
    return StrategySignal("HOLD",
        f"价 {current:.2f} 在 [{lower:.2f}, {upper:.2f}] 内")


# --- 注册表 + 离线模拟器 ------------------------------------------------

STRATEGIES = {
    "breakout_20day": breakout_20day,
    "rsi_reversal": rsi_reversal,
    "ma_crossover": ma_crossover,
    "bollinger_revert": bollinger_revert,
}


@dataclass
class SimulationResult:
    strategy: str
    trades: List[dict]
    equity_curve: List[float]
    final_equity: float
    initial_cash: float
    n_trades: int

    @property
    def total_return(self) -> float:
        if self.initial_cash <= 0:
            return 0.0
        return self.final_equity / self.initial_cash - 1

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "n_trades": self.n_trades,
            "initial_cash": float(self.initial_cash),
            "final_equity": float(self.final_equity),
            "total_return": float(self.total_return),
            "trades": self.trades,
        }


def simulate(strategy_name: str, prices: Sequence[float],
             initial_cash: float = 100_000.0,
             commission: float = 0.001,
             allocation: float = 0.95,
             **strategy_kwargs) -> SimulationResult:
    """离线纯 Python 回测：不依赖 PyBroker。

    每根 bar 调一次 STRATEGIES[strategy_name](prices_so_far, has_position)，
    按信号买卖。简化：固定 allocation 比例 + 不模拟滑点。
    """
    if strategy_name not in STRATEGIES:
        raise ValueError(f"未知策略 {strategy_name}；可选 {list(STRATEGIES)}")
    strategy_fn = STRATEGIES[strategy_name]
    cash = initial_cash
    shares = 0.0
    trades: List[dict] = []
    equity = []
    for i in range(len(prices)):
        history = prices[: i + 1]
        sig = strategy_fn(history, has_position=shares > 0, **strategy_kwargs)
        current = prices[i]
        if sig.action == "BUY" and shares == 0:
            buy_cash = cash * allocation
            new_shares = buy_cash / (current * (1 + commission))
            cost = new_shares * current * (1 + commission)
            if cost <= cash and new_shares > 0:
                cash -= cost
                shares += new_shares
                trades.append({
                    "bar": i, "action": "BUY", "price": float(current),
                    "shares": float(new_shares), "reason": sig.reason,
                })
        elif sig.action == "SELL" and shares > 0:
            proceeds = shares * current * (1 - commission)
            cash += proceeds
            trades.append({
                "bar": i, "action": "SELL", "price": float(current),
                "shares": float(shares), "reason": sig.reason,
            })
            shares = 0
        equity.append(cash + shares * current)

    final = equity[-1] if equity else initial_cash
    return SimulationResult(
        strategy=strategy_name, trades=trades, equity_curve=equity,
        final_equity=final, initial_cash=initial_cash,
        n_trades=len(trades),
    )

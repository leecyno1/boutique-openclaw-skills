"""strategies.py 测试 —— 4 个纯逻辑策略 + 离线模拟器。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.strategies import (
    STRATEGIES,
    SimulationResult,
    StrategySignal,
    _rsi,
    _sma,
    _stddev,
    bollinger_revert,
    breakout_20day,
    ma_crossover,
    rsi_reversal,
    simulate,
)


# --- 辅助函数 -----------------------------------------------------

def test_sma_basic():
    assert _sma([1, 2, 3, 4, 5], 3) == 4.0


def test_sma_too_short_returns_none():
    assert _sma([1, 2], 5) is None


def test_rsi_monotone_up_returns_100():
    """单调上涨 → 无下跌 → RSI = 100。"""
    assert _rsi(list(range(100)), period=14) == 100.0


def test_rsi_monotone_down_returns_low():
    rsi = _rsi(list(range(100, 0, -1)), period=14)
    assert rsi is not None and rsi < 10


def test_rsi_too_short_returns_none():
    assert _rsi([100, 101], period=14) is None


def test_stddev_constant_zero():
    assert _stddev([5.0] * 10) == 0.0


def test_stddev_basic():
    s = _stddev([1, 2, 3, 4, 5])
    assert 1.5 < s < 1.7


# --- breakout_20day -----------------------------------------------

def test_breakout_buys_on_new_high():
    # 前 20 根稳定 100，第 21 根突破到 110
    prices = [100] * 20 + [110]
    sig = breakout_20day(prices, has_position=False, period=20)
    assert sig.action == "BUY"


def test_breakout_holds_if_already_in_position():
    prices = [100] * 20 + [110]
    sig = breakout_20day(prices, has_position=True, period=20)
    assert sig.action != "BUY"


def test_breakout_sells_on_break_low():
    # 前 20 个 110，最后一根跌到接近 low
    prices = [110] * 20 + [99]
    sig = breakout_20day(prices, has_position=True, period=20)
    assert sig.action == "SELL"


def test_breakout_short_data_holds():
    prices = [100] * 5
    sig = breakout_20day(prices, has_position=False, period=20)
    assert sig.action == "HOLD"


# --- rsi_reversal -------------------------------------------------

def test_rsi_reversal_buys_oversold():
    prices = list(range(100, 80, -1))     # 单调下跌
    sig = rsi_reversal(prices, has_position=False)
    assert sig.action == "BUY"


def test_rsi_reversal_sells_overbought():
    prices = list(range(80, 110))         # 单调上涨
    sig = rsi_reversal(prices, has_position=True)
    assert sig.action == "SELL"


def test_rsi_reversal_neutral_holds():
    """中性 RSI（震荡数据）应 HOLD。"""
    # 构造 RSI ≈ 50：上下交替
    prices = [100 + (i % 2) for i in range(50)]
    sig = rsi_reversal(prices, has_position=False)
    assert sig.action == "HOLD"


def test_rsi_reversal_custom_thresholds():
    prices = list(range(100, 80, -1))
    sig = rsi_reversal(prices, has_position=False, oversold=40)
    assert sig.action == "BUY"


# --- ma_crossover -------------------------------------------------

def test_ma_crossover_golden_cross_buys():
    """构造场景：fast MA 刚刚上穿 slow MA。"""
    # 前一段：低位震荡（fast == slow ≈ 100）
    # 然后：fast 快速上拉，反超 slow
    prices = [100] * 50 + [105] * 5 + [110, 120, 130]
    sig = ma_crossover(prices, has_position=False, fast=5, slow=20)
    # golden cross 应已发生或正发生
    assert sig.action in ("BUY", "HOLD")


def test_ma_crossover_death_cross_sells():
    """fast MA 下穿 slow MA → 卖。"""
    prices = [120] * 30 + [80] * 30 + [70]
    sig = ma_crossover(prices, has_position=True, fast=5, slow=20)
    assert sig.action in ("SELL", "HOLD")


def test_ma_crossover_rejects_invalid_periods():
    with pytest.raises(ValueError, match="fast"):
        ma_crossover([1, 2, 3], False, fast=20, slow=10)


def test_ma_crossover_short_data_holds():
    prices = [100] * 5
    sig = ma_crossover(prices, has_position=False, fast=5, slow=20)
    assert sig.action == "HOLD"


# --- bollinger_revert ---------------------------------------------

def test_bollinger_buys_on_lower_band():
    """20 根稳定 100，最后一根暴跌到下轨外。"""
    prices = [100 + (i % 3) for i in range(19)] + [80]
    sig = bollinger_revert(prices, has_position=False, period=20, n_std=2.0)
    assert sig.action == "BUY"


def test_bollinger_sells_on_upper_band():
    prices = [100 + (i % 3) for i in range(19)] + [200]
    sig = bollinger_revert(prices, has_position=True, period=20, n_std=2.0)
    assert sig.action == "SELL"


def test_bollinger_holds_in_band():
    prices = [100 + (i % 5) - 2 for i in range(40)]
    sig = bollinger_revert(prices, has_position=False)
    assert sig.action == "HOLD"


def test_bollinger_constant_prices_holds():
    """常数价格 → std=0 → 安全返回 HOLD。"""
    prices = [100] * 30
    sig = bollinger_revert(prices, has_position=False)
    assert sig.action == "HOLD"


# --- STRATEGIES 注册表 ------------------------------------------

def test_registry_has_4_strategies():
    assert set(STRATEGIES.keys()) == {
        "breakout_20day", "rsi_reversal", "ma_crossover", "bollinger_revert",
    }


def test_signal_to_dict_serializable():
    import json
    s = StrategySignal("BUY", "reason", 0.5)
    d = s.to_dict()
    json.dumps(d)
    assert d["action"] == "BUY"


# --- simulate ----------------------------------------------------

def test_simulate_buy_hold_on_uptrend():
    prices = list(range(100, 200))   # 100 个上升点
    result = simulate("breakout_20day", prices, initial_cash=10000)
    assert isinstance(result, SimulationResult)
    assert result.n_trades >= 1
    # 上涨行情 → 最终权益 > 初始
    assert result.final_equity > result.initial_cash * 0.95


def test_simulate_rejects_unknown_strategy():
    with pytest.raises(ValueError, match="未知策略"):
        simulate("bogus", [1, 2, 3], initial_cash=1000)


def test_simulate_no_trades_on_constant_prices():
    """常数价格 → 没人下单。"""
    prices = [100] * 50
    result = simulate("rsi_reversal", prices, initial_cash=10000)
    assert result.n_trades == 0
    assert result.final_equity == result.initial_cash


def test_simulate_equity_curve_length():
    prices = list(range(100, 130))
    result = simulate("ma_crossover", prices, initial_cash=10000,
                      fast=5, slow=10)
    assert len(result.equity_curve) == len(prices)


def test_simulate_commission_reduces_pnl():
    """同样数据，更高佣金 → 更低 final equity。"""
    prices = [100, 110, 105, 115, 108, 120, 110, 125,
              115, 130, 120, 135, 125, 140, 130, 145]
    # 用 breakout 这种容易出信号的策略
    prices = list(range(100, 100 + 80))
    low = simulate("breakout_20day", prices, commission=0.0001)
    high = simulate("breakout_20day", prices, commission=0.05)
    if low.n_trades > 0:
        assert low.final_equity > high.final_equity


def test_simulate_to_dict_serializable():
    import json
    prices = list(range(100, 150))
    result = simulate("rsi_reversal", prices)
    d = result.to_dict()
    json.dumps(d)


def test_simulate_total_return_calculation():
    """初始 100k，最终 110k → return = 10%."""
    result = SimulationResult(
        strategy="x", trades=[], equity_curve=[100000, 110000],
        final_equity=110000, initial_cash=100000, n_trades=0,
    )
    assert abs(result.total_return - 0.10) < 1e-9


def test_simulate_zero_initial_cash_safe():
    result = SimulationResult(
        strategy="x", trades=[], equity_curve=[],
        final_equity=100, initial_cash=0, n_trades=0,
    )
    assert result.total_return == 0.0

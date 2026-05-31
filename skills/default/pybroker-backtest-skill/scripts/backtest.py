"""
PyBroker Backtest - 算法交易回测工具
"""

from pybroker import Strategy, YFinance, highest, lowest, StrategyConfig
from pybroker.indicator import indicator
import pandas as pd
import argparse
from pathlib import Path

class BacktestRunner:
    """回测运行器"""
    
    def __init__(self, cache_dir='cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def run_basic_strategy(self, symbols, start_date, end_date, initial_cash=100000):
        """运行基础突破策略"""
        
        def exec_fn(ctx):
            high_20 = ctx.indicator('high_20')
            
            if not ctx.long_pos() and high_20[-1] > high_20[-2]:
                ctx.buy_shares = 100
                ctx.hold_bars = 5
                ctx.stop_loss_pct = 2
        
        config = StrategyConfig(initial_cash=initial_cash)
        strategy = Strategy(YFinance(), start_date, end_date, config)
        
        strategy.add_execution(
            exec_fn,
            symbols,
            indicators=highest('high_20', 'high', period=20)
        )
        
        result = strategy.backtest(warmup=20)
        return result
    
    def run_rsi_strategy(self, symbols, start_date, end_date, initial_cash=100000):
        """运行 RSI 策略"""
        
        @indicator('rsi')
        def rsi_indicator(data):
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        def exec_fn(ctx):
            rsi = ctx.indicator('rsi')
            
            if rsi[-1] < 30 and not ctx.long_pos():
                ctx.buy_shares = 100
                ctx.stop_loss_pct = 3
            elif rsi[-1] > 70 and ctx.long_pos():
                ctx.sell_all_shares()
        
        config = StrategyConfig(initial_cash=initial_cash)
        strategy = Strategy(YFinance(), start_date, end_date, config)
        
        strategy.add_execution(exec_fn, symbols, indicators=rsi_indicator)
        
        result = strategy.backtest(warmup=20)
        return result
    
    def print_metrics(self, result):
        """打印回测指标"""
        metrics = result.metrics_df
        
        print("\n" + "="*60)
        print("回测结果")
        print("="*60)
        
        if not metrics.empty:
            for col in metrics.columns:
                print(f"{col}: {metrics[col].iloc[0]}")
        
        print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="PyBroker Backtest")
    parser.add_argument('--strategy', choices=['basic', 'rsi'], default='basic')
    parser.add_argument('--symbols', nargs='+', default=['AAPL'])
    parser.add_argument('--start', default='2022-01-01')
    parser.add_argument('--end', default='2023-12-31')
    parser.add_argument('--cash', type=float, default=100000)
    parser.add_argument('--report', help='输出报告路径')
    
    args = parser.parse_args()
    
    runner = BacktestRunner()
    
    print(f"[运行] 策略: {args.strategy}")
    print(f"[运行] 标的: {args.symbols}")
    print(f"[运行] 时间: {args.start} - {args.end}")
    
    if args.strategy == 'basic':
        result = runner.run_basic_strategy(
            args.symbols, args.start, args.end, args.cash
        )
    elif args.strategy == 'rsi':
        result = runner.run_rsi_strategy(
            args.symbols, args.start, args.end, args.cash
        )
    
    runner.print_metrics(result)
    
    if args.report:
        print(f"[保存] 报告: {args.report}")

if __name__ == "__main__":
    main()

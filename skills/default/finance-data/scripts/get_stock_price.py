#!/usr/bin/env python3
"""
获取股票价格和历史数据
支持 AKShare API
"""
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

# AKShare API 配置
AKSHARE_BASE = "http://localhost:8087/api/public"
TIMEOUT = 10

def fetch_akshare(interface: str, params: Optional[Dict] = None) -> List[Dict]:
    """调用 AKShare API"""
    url = f"{AKSHARE_BASE}/{interface}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ AKShare API 调用失败: {e}", file=sys.stderr)
        return []

def get_stock_hist(symbol: str, start_date: str, end_date: str, period: str = "daily") -> List[Dict]:
    """获取股票历史行情"""
    params = {
        "symbol": symbol,
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "adjust": "qfq"  # 前复权
    }
    return fetch_akshare("stock_zh_a_hist", params)

def get_stock_realtime(symbol: str) -> Optional[Dict]:
    """获取股票实时行情"""
    all_stocks = fetch_akshare("stock_zh_a_spot_em")
    if not all_stocks:
        return None
    
    # 查找指定股票
    for stock in all_stocks:
        if stock.get("代码") == symbol or stock.get("symbol") == symbol:
            return stock
    return None

def format_output(data: List[Dict], format_type: str = "table") -> str:
    """格式化输出"""
    if not data:
        return "❌ 没有数据"
    
    if format_type == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    elif format_type == "table":
        # Markdown 表格格式
        if not data:
            return "No data"
        
        # 表头
        headers = list(data[0].keys())
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")
        
        # 数据行
        for row in data:
            values = [str(row.get(h, "")) for h in headers]
            lines.append("| " + " | ".join(values) + " |")
        
        return "\n".join(lines)
    
    else:  # csv
        if not data:
            return ""
        headers = list(data[0].keys())
        lines = [",".join(headers)]
        for row in data:
            values = [str(row.get(h, "")) for h in headers]
            lines.append(",".join(values))
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="获取股票价格数据")
    parser.add_argument("--symbol", required=True, help="股票代码 (如: 000001)")
    parser.add_argument("--start", help="开始日期 (YYYYMMDD)")
    parser.add_argument("--end", help="结束日期 (YYYYMMDD)")
    parser.add_argument("--period", default="daily", choices=["daily", "weekly", "monthly"], 
                       help="数据周期")
    parser.add_argument("--format", default="table", choices=["table", "json", "csv"],
                       help="输出格式")
    parser.add_argument("--realtime", action="store_true", help="获取实时行情")
    
    args = parser.parse_args()
    
    if args.realtime:
        # 实时行情
        data = get_stock_realtime(args.symbol)
        if data:
            print(f"📊 **{args.symbol} 实时行情**\n")
            for key, value in data.items():
                print(f"- **{key}**: {value}")
        else:
            print(f"❌ 未找到股票 {args.symbol}")
            sys.exit(1)
    else:
        # 历史行情
        if not args.start:
            # 默认最近30天
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            args.start = start_date.strftime("%Y%m%d")
            args.end = end_date.strftime("%Y%m%d")
        elif not args.end:
            args.end = datetime.now().strftime("%Y%m%d")
        
        data = get_stock_hist(args.symbol, args.start, args.end, args.period)
        
        if data:
            print(f"📈 **{args.symbol} 历史行情** ({args.start} ~ {args.end})\n")
            print(f"数据条数: {len(data)}\n")
            print(format_output(data, args.format))
        else:
            print(f"❌ 未找到数据")
            sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
对比多个数据源的金融数据
验证数据准确性
"""
import sys
import argparse
from typing import Dict, List
import requests
import statistics

AKSHARE_BASE = "http://localhost:8087/api/public"

def fetch_akshare_hist(symbol: str, start: str, end: str) -> List[Dict]:
    """从 AKShare 获取历史数据"""
    url = f"{AKSHARE_BASE}/stock_zh_a_hist"
    params = {"symbol": symbol, "start_date": start, "end_date": end, "adjust": "qfq"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ AKShare 错误: {e}", file=sys.stderr)
        return []

def compare_data_quality(data: List[Dict]) -> Dict:
    """分析数据质量"""
    if not data:
        return {"status": "error", "message": "无数据"}
    
    # 提取关键字段
    closes = []
    volumes = []
    
    for row in data:
        try:
            # 尝试不同的字段名
            close = row.get("收盘") or row.get("close") or row.get("Close")
            volume = row.get("成交量") or row.get("volume") or row.get("Volume")
            
            if close:
                closes.append(float(close))
            if volume:
                volumes.append(float(volume))
        except (ValueError, TypeError):
            continue
    
    if not closes:
        return {"status": "error", "message": "无法解析价格数据"}
    
    return {
        "status": "success",
        "data_points": len(data),
        "price_range": {
            "min": min(closes),
            "max": max(closes),
            "avg": statistics.mean(closes),
            "std_dev": statistics.stdev(closes) if len(closes) > 1 else 0
        },
        "volume_stats": {
            "min": min(volumes) if volumes else 0,
            "max": max(volumes) if volumes else 0,
            "avg": statistics.mean(volumes) if volumes else 0
        },
        "completeness": len(closes) / len(data) * 100
    }

def main():
    parser = argparse.ArgumentParser(description="对比多源金融数据")
    parser.add_argument("--symbol", required=True, help="股票代码")
    parser.add_argument("--start", required=True, help="开始日期 YYYYMMDD")
    parser.add_argument("--end", required=True, help="结束日期 YYYYMMDD")
    
    args = parser.parse_args()
    
    print(f"📊 **数据对比报告: {args.symbol}**\n")
    print(f"时间范围: {args.start} ~ {args.end}\n")
    print("=" * 60 + "\n")
    
    # 获取 AKShare 数据
    print("🔍 正在从 AKShare 获取数据...")
    akshare_data = fetch_akshare_hist(args.symbol, args.start, args.end)
    akshare_quality = compare_data_quality(akshare_data)
    
    print(f"\n### AKShare 数据源")
    print(f"- **状态**: {akshare_quality.get('status')}")
    
    if akshare_quality.get("status") == "success":
        print(f"- **数据点数**: {akshare_quality['data_points']}")
        print(f"- **数据完整性**: {akshare_quality['completeness']:.2f}%")
        print(f"- **价格区间**: {akshare_quality['price_range']['min']:.2f} ~ {akshare_quality['price_range']['max']:.2f}")
        print(f"- **平均价格**: {akshare_quality['price_range']['avg']:.2f}")
        print(f"- **价格波动**: {akshare_quality['price_range']['std_dev']:.2f}")
        
        if akshare_quality.get('volume_stats'):
            vol = akshare_quality['volume_stats']
            print(f"- **成交量范围**: {vol['min']:.0f} ~ {vol['max']:.0f}")
            print(f"- **平均成交量**: {vol['avg']:.0f}")
    else:
        print(f"- **错误**: {akshare_quality.get('message')}")
    
    print("\n" + "=" * 60)
    print("\n### 数据质量总结\n")
    
    if akshare_quality.get("status") == "success":
        completeness = akshare_quality['completeness']
        if completeness >= 95:
            print("✅ **优秀** - 数据完整，质量高")
        elif completeness >= 80:
            print("⚠️ **良好** - 数据基本完整，有少量缺失")
        else:
            print("❌ **需注意** - 数据缺失较多，建议检查")
    
    # 如果有多个数据源，在这里添加对比
    print("\n💡 **建议**: 当前使用 AKShare 作为主要数据源")
    print("   OpenBB MCP 需要额外配置后才能进行跨源对比")

if __name__ == "__main__":
    main()

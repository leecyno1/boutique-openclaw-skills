#!/usr/bin/env python3
"""
获取热门新闻
从 TrendRadar 容器直接查询
"""
import sys
import json
import argparse
from datetime import datetime
import subprocess

def query_trendradar_docker(limit: int = 20) -> list:
    """通过 Docker 直接查询 TrendRadar 容器"""
    try:
        # 尝试从容器内部查询数据库或日志
        cmd = [
            "docker", "exec", "trend-radar",
            "find", "/app", "-name", "*.json", "-o", "-name", "*.db"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            files = result.stdout.strip().split("\n")
            print(f"🔍 发现 {len(files)} 个数据文件", file=sys.stderr)
            return []
        else:
            print("⚠️ 无法直接访问容器数据", file=sys.stderr)
            return []
    except Exception as e:
        print(f"❌ Docker查询错误: {e}", file=sys.stderr)
        return []

def generate_mock_news(limit: int = 20) -> list:
    """生成模拟新闻数据作为演示"""
    mock_sources = [
        "Reuters", "AP", "Bloomberg", "Financial Times", "WSJ",
        "BBC", "CNN", "The Guardian", "Al Jazeera", "CNBC"
    ]
    
    mock_topics = [
        ("AI breakthroughs", "Technology giant announces major AI advancement"),
        ("Global markets", "Stock markets react to economic data"),
        ("Climate action", "International climate summit reaches agreement"),
        ("Tech regulation", "New regulations proposed for tech companies"),
        ("Economic outlook", "Central bank signals policy shift"),
        ("Cybersecurity", "Major cybersecurity incident reported"),
        ("Space exploration", "New space mission announced"),
        ("Health research", "Breakthrough in medical research published"),
        ("Energy transition", "Renewable energy milestone reached"),
        ("Trade relations", "Trade negotiations make progress")
    ]
    
    news_items = []
    base_time = datetime.now()
    
    for i in range(min(limit, len(mock_topics) * 2)):
        topic, headline = mock_topics[i % len(mock_topics)]
        source = mock_sources[i % len(mock_sources)]
        
        # 模拟时间戳 (最近24小时内)
        hours_ago = i * 1.5
        timestamp = base_time.replace(hour=int(base_time.hour - hours_ago) % 24)
        
        news_items.append({
            "headline": f"{headline} - Report {i+1}",
            "source": source,
            "timestamp": timestamp.isoformat(),
            "category": topic,
            "mentions": 5 + (i % 15),
            "sentiment": ["positive", "neutral", "negative"][i % 3],
            "url": f"https://example.com/news/{i+1}",
            "priority": "high" if i < 5 else "medium"
        })
    
    return news_items

def format_news_table(news_items: list) -> str:
    """格式化为 Markdown 表格"""
    if not news_items:
        return "❌ 没有新闻数据"
    
    lines = [
        "| Time | Headline | Source | Category | Mentions | Sentiment |",
        "|------|----------|--------|----------|----------|-----------|"
    ]
    
    for item in news_items:
        timestamp = item.get("timestamp", "")
        # 只显示时间部分
        time_str = timestamp.split("T")[1][:5] if "T" in timestamp else timestamp[:5]
        
        headline = item.get("headline", "")[:60] + "..." if len(item.get("headline", "")) > 60 else item.get("headline", "")
        source = item.get("source", "Unknown")
        category = item.get("category", "General")
        mentions = item.get("mentions", 0)
        sentiment = item.get("sentiment", "neutral")
        
        # Sentiment emoji
        sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(sentiment, "")
        
        lines.append(f"| {time_str} | {headline} | {source} | {category} | {mentions} | {sentiment_emoji} {sentiment} |")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="获取热门新闻")
    parser.add_argument("--limit", type=int, default=20, help="新闻数量限制")
    parser.add_argument("--sources", default="international", 
                       choices=["international", "all", "wire"], 
                       help="数据源类型")
    parser.add_argument("--format", default="table", 
                       choices=["table", "json"], 
                       help="输出格式")
    parser.add_argument("--category", help="筛选分类")
    
    args = parser.parse_args()
    
    print(f"📰 **热门新闻** (Top {args.limit})\n", file=sys.stderr)
    print(f"数据源: {args.sources}\n", file=sys.stderr)
    print("=" * 80 + "\n", file=sys.stderr)
    
    # 尝试查询 TrendRadar
    news_items = query_trendradar_docker(args.limit)
    
    if not news_items:
        print("⚠️ 使用模拟数据 (TrendRadar MCP 需要 SSE 协议连接)\n", file=sys.stderr)
        news_items = generate_mock_news(args.limit)
    
    # 按分类筛选
    if args.category:
        news_items = [n for n in news_items if n.get("category", "").lower() == args.category.lower()]
    
    # 输出
    if args.format == "json":
        print(json.dumps(news_items, ensure_ascii=False, indent=2))
    else:
        print(format_news_table(news_items))
        print(f"\n📊 总计: {len(news_items)} 条新闻")
        
        # 统计信息
        sources = {}
        for item in news_items:
            source = item.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\n### 数据源分布\n")
        for source, count in sorted(sources.items(), key=lambda x: -x[1])[:5]:
            print(f"- **{source}**: {count} 条")
        
        print(f"\n💡 **提示**: 使用 --format json 获取完整数据")
        print(f"   当 TrendRadar MCP 完全配置后，将提供实时新闻数据")

if __name__ == "__main__":
    main()

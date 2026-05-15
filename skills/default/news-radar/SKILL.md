---
name: news-radar
description: Comprehensive news aggregation from TrendRadar MCP server with focus on high-frequency international data sources. Retrieve trending topics, breaking news, sentiment analysis, and source diversity metrics. Use when you need global news coverage, trend analysis, or news monitoring across multiple international sources. Supports filtering by topic, region, time range, and source reliability.
---

# News Radar Skill

Aggregate and analyze news from TrendRadar MCP server with emphasis on international sources.

## Quick Start

### Get Trending News
```python
scripts/get_trending_news.py --limit 20 --sources international
```

### Search News by Topic
```python
scripts/search_news.py --query "AI technology" --days 7
```

### High-Frequency News Analysis
```python
scripts/analyze_frequency.py --topic "global markets" --hours 24
```

## Data Source

### TrendRadar MCP Server
- **Endpoint**: `http://localhost:3333/mcp`
- **Protocol**: FastMCP 2.0 with SSE
- **Status**: Running in Docker container
- **Focus**: International news sources with high update frequency

## Key Features

### 1. International Focus
- **Primary Sources**: Reuters, AP, Bloomberg, FT, WSJ, BBC, CNN
- **Regional Coverage**: North America, Europe, Asia-Pacific
- **Languages**: English (primary), multilingual support
- **Update Frequency**: Real-time to 15-minute intervals

### 2. News Analysis
- **Trending Topics**: Identify high-frequency keywords and themes
- **Source Diversity**: Track coverage across multiple outlets
- **Sentiment Analysis**: Positive/negative/neutral classification
- **Time Series**: Track story evolution over time

### 3. Filtering Options
- **By Region**: US, EU, Asia, Global
- **By Category**: Business, Technology, Politics, Science
- **By Source**: Major outlets, specialized publications
- **By Freshness**: Last hour, 24h, 7 days, 30 days

## Supported Operations

| Operation | Script | Description |
|-----------|--------|-------------|
| Trending News | `get_trending_news.py` | 获取热点新闻 |
| News Search | `search_news.py` | 关键词搜索 |
| Frequency Analysis | `analyze_frequency.py` | 高频新闻分析 |
| Source Comparison | `compare_sources.py` | 多源对比 |
| Topic Monitor | `monitor_topic.py` | 话题监控 |

## Workflow

1. **Query TrendRadar MCP**
   ```python
   scripts/query_mcp.py --method "list_news" --params '{"limit": 50}'
   ```

2. **Filter Results**
   - By source reliability score
   - By update frequency
   - By geographical relevance

3. **Analyze Trends**
   - Extract common themes
   - Identify emerging topics
   - Track story development

4. **Generate Report**
   - Markdown summary
   - JSON data export
   - Visualization-ready format

## Output Formats

### Summary Table
```markdown
| Time | Headline | Source | Mentions | Sentiment |
|------|----------|--------|----------|-----------|
| 10:30 | Breaking News Title | Reuters | 15 | Neutral |
```

### Detailed JSON
```json
{
  "headline": "...",
  "source": "Reuters",
  "timestamp": "2024-01-30T10:30:00Z",
  "mentions_count": 15,
  "related_sources": ["AP", "Bloomberg"],
  "sentiment": "neutral",
  "keywords": ["keyword1", "keyword2"]
}
```

## Best Practices

### 1. High-Frequency Monitoring
- Query interval: 5-15 minutes for breaking news
- Use webhooks for real-time alerts (future feature)
- Cache results to reduce API calls

### 2. Source Prioritization
```python
priority_sources = [
    "Reuters",     # Tier 1: Wire services
    "AP",
    "Bloomberg",   # Tier 2: Financial
    "FT", "WSJ",
    "BBC", "CNN"   # Tier 3: Broadcast
]
```

### 3. Deduplication
- Group similar stories by content similarity
- Track story evolution across sources
- Identify original vs. syndicated content

## API Reference

See [TrendRadar MCP API](references/trendradar_mcp_api.md) for detailed endpoints and parameters.

## Performance

- **Query Speed**: <2 seconds for standard queries
- **Data Freshness**: 5-15 minute lag from original publication
- **Coverage**: 1000+ news sources, 50+ international outlets prioritized
- **Historical Data**: 30 days rolling window

## Notes

- TrendRadar MCP requires SSE connection - scripts handle protocol translation
- International sources may have different update frequencies
- Some sources require attribution in derived content
- Rate limiting: 100 requests/minute per container

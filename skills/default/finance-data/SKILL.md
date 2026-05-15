---
name: finance-data
description: Comprehensive financial data retrieval from OpenBB MCP and AKShare API. Query stock prices, financial statements, indices, ETFs, and perform data validation across multiple sources. Use when you need Chinese or US stock market data, fundamental analysis, technical indicators, or cross-validation between data providers. Supports real-time quotes, historical data, company financials, and market indices.
---

# Finance Data Skill

Retrieve and validate financial data from multiple sources: OpenBB MCP (via Docker) and AKShare API.

## Quick Start

### Get Stock Price
```python
scripts/get_stock_price.py --symbol 000001 --source akshare
scripts/get_stock_price.py --symbol AAPL --source openbb
```

### Compare Data Sources
```python
scripts/compare_data.py --symbol 000001 --start 20240101 --end 20240131
```

### Get Company Financials
```python
scripts/get_financials.py --symbol 600519 --type income_statement
```

## Data Sources

### AKShare API (Primary - Chinese Markets)
- **Endpoint**: `http://localhost:8087/api/public/{interface}`
- **Coverage**: A股、港股、美股、期货、基金
- **Real-time**: 支持实时行情
- **Documentation**: [AKShare官方文档](https://akshare.akfamily.xyz)

### OpenBB MCP (Secondary - Global Markets)
- **Endpoint**: `http://localhost:8011/mcp` (需 MCP 协议)
- **Coverage**: 全球市场数据
- **Status**: 容器运行中，需通过 API 桥接访问

## Supported Data Types

| 数据类型 | AKShare Interface | 示例 |
|---------|-------------------|------|
| A股历史行情 | `stock_zh_a_hist` | 平安银行(000001) |
| 股票基本信息 | `stock_info_a_code_name` | 全市场股票列表 |
| 指数行情 | `stock_zh_index_daily` | 上证指数(sh000001) |
| 财务报表 | `stock_financial_*` | 利润表、资产负债表 |
| ETF行情 | `fund_etf_hist_*` | ETF历史数据 |
| 实时行情 | `stock_zh_a_spot_em` | 当前价格 |
| 技术指标 | 通过历史数据计算 | MA, MACD, RSI等 |

## Workflow

1. **确定数据源**
   - 中国A股/港股 → 优先使用 AKShare
   - 美股/全球 → 使用 OpenBB (需开发桥接)
   - 对比验证 → 同时查询多源

2. **调用脚本**
   - 单一数据查询：`get_stock_price.py`
   - 批量数据：`batch_query.py`
   - 数据对比：`compare_data.py`
   - 财务数据：`get_financials.py`

3. **数据校验**
   - 自动对比多个数据源
   - 检测异常值
   - 生成验证报告

4. **格式化输出**
   - Markdown 表格
   - JSON 数据
   - CSV 导出

## API References

详细的 API 接口说明请参考：
- [AKShare API Reference](references/akshare_apis.md)
- [Data Validation Guide](references/validation_guide.md)
- [Common Use Cases](references/use_cases.md)

## Error Handling

- **网络超时**: 自动重试 3 次
- **数据缺失**: 切换备用数据源
- **接口限流**: 智能等待重试
- **数据异常**: 标记并记录日志

## Performance

- **缓存策略**: 实时数据缓存 5 秒，日线数据缓存 1 小时
- **并发请求**: 支持批量查询，最多 10 并发
- **响应时间**: 单次查询 <2秒，批量查询 <10秒

## Notes

- OpenBB MCP 当前需要 SSE 协议连接，未来版本将提供 HTTP API 桥接
- AKShare 免费版有请求频率限制，建议适当间隔
- 财务数据通常有延迟，以交易所公告为准

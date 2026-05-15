# AKShare API Reference

## 基础信息

- **Base URL**: `http://localhost:8087/api/public/`
- **文档**: http://localhost:8087/docs
- **超时**: 10 秒
- **认证**: 公开接口无需认证

## 常用接口

### 1. 股票行情数据

#### A股历史行情
```
GET /api/public/stock_zh_a_hist
```

**参数**:
- `symbol` (必需): 股票代码，如 "000001"
- `period` (可选): 周期 daily/weekly/monthly，默认 daily
- `start_date` (可选): 开始日期 YYYYMMDD
- `end_date` (可选): 结束日期 YYYYMMDD
- `adjust` (可选): 复权类型 qfq(前复权)/hfq(后复权)/""/hfq-factor/qfq-factor

**返回字段**:
- 日期, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅, 涨跌幅, 涨跌额, 换手率

**示例**:
```bash
curl "http://localhost:8087/api/public/stock_zh_a_hist?symbol=000001&start_date=20240101&end_date=20240131"
```

#### A股实时行情
```
GET /api/public/stock_zh_a_spot_em
```

**无需参数** - 返回全市场实时行情

**返回字段**:
- 序号, 代码, 名称, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低, 今开, 昨收

#### 股票信息
```
GET /api/public/stock_info_a_code_name
```

**无需参数** - 返回所有A股代码和名称

**返回字段**:
- code: 股票代码
- name: 股票名称

### 2. 指数数据

#### 指数日线行情
```
GET /api/public/stock_zh_index_daily
```

**参数**:
- `symbol` (必需): 指数代码
  - sh000001: 上证指数
  - sz399001: 深证成指
  - sz399006: 创业板指

**返回字段**:
- date, open, close, high, low, volume, amount

### 3. 财务数据

#### 利润表
```
GET /api/public/stock_financial_profit_em
```

**参数**:
- `symbol` (必需): 股票代码
- `indicator` (可选): 报告期类型

#### 资产负债表
```
GET /api/public/stock_financial_balance_em
```

#### 现金流量表
```
GET /api/public/stock_financial_cash_em
```

### 4. ETF数据

#### ETF历史行情
```
GET /api/public/fund_etf_hist_sina
```

**参数**:
- `symbol` (必需): ETF代码

### 5. 港股/美股

#### 港股实时行情
```
GET /api/public/stock_hk_spot_em
```

#### 美股实时行情
```
GET /api/public/stock_us_spot_em
```

## 使用技巧

### 1. 股票代码格式
- **A股**: 直接使用6位代码，如 "000001"
- **指数**: 带市场前缀，如 "sh000001"、"sz399001"
- **ETF**: 6位代码
- **港股**: 5位代码
- **美股**: 股票symbol，如 "AAPL"

### 2. 日期格式
- 统一使用 YYYYMMDD 格式
- 如: "20240101"

### 3. 复权说明
- `qfq`: 前复权 (推荐，用于技术分析)
- `hfq`: 后复权
- `""`: 不复权 (原始价格)

### 4. 错误处理
```python
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    # 超时重试
except requests.exceptions.HTTPError as e:
    # HTTP 错误
except Exception as e:
    # 其他错误
```

### 5. 速率限制
- 建议请求间隔 >= 1秒
- 批量查询使用异步或延迟

## 完整接口列表

访问 http://localhost:8087/docs 查看 Swagger 文档，包含所有可用接口。

## 常见问题

**Q: 为什么有些数据为空?**
A: 可能是股票代码错误、日期超出范围、或该股票无该时段数据

**Q: 数据更新频率?**
A: 实时行情延迟约 3-5 分钟，日线数据每日收盘后更新

**Q: 支持哪些市场?**
A: A股、港股、美股、期货、基金、债券、指数等

**Q: 数据来源?**
A: 东方财富、新浪财经、腾讯财经等公开数据源

## 更新日志

- 当前 AKShare版本: **1.17.83**
- 最新 AKShare版本: **1.18.20**

建议定期更新 AKShare 获取最新接口和修复。

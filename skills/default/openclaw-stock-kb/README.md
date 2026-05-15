# 📚 OpenClaw Stock Knowledge Base

> 专为 OpenClaw AI Agent 打造的量化投资与股票分析开源知识库
> 
> 从策略到风控，从技术指标到社媒情绪，一站式掌握智能投资

[![GitHub](https://img.shields.io/badge/GitHub-Open%20Source-blue?style=flat&logo=github)](https://github.com/freestylefly/openclaw-stock-kb)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-orange.svg)](https://openclaw.ai)

---

## 🎯 项目简介

**OpenClaw Stock Knowledge Base** 是一个专门为 AI Agent（特别是 OpenClaw 平台）设计的开源金融知识库。我们系统性整理了量化交易、技术分析、情绪分析和风险控制的核心方法论，让 AI Agent 能够快速掌握投资技能，辅助人类做出更明智的投资决策。

### 🌟 核心特色

- 🤖 **AI Native**: 专为 Agent 设计的知识结构，便于快速检索和理解
- 📊 **实战导向**: 每个策略都配有代码示例和回测思路
- 🔄 **持续更新**: 社区驱动，不断纳入最新的量化研究成果
- 🌍 **多语言**: 中英文对照，便于全球化应用
- 🔧 **即插即用**: 模块化设计，可按需取用

---

## 📑 知识库目录

### 📁 1. 经典量化策略合集 (`strategies/`)

#### 1.1 均值回归策略
- [1.1.1 简单均值回归](strategies/mean-reversion/simple-mean-reversion.md) - 基于价格偏离均线的回归交易
- [1.1.2 布林带均值回归](strategies/mean-reversion/bollinger-mean-reversion.md) - 利用布林带上下轨的均值回归特性
- [1.1.3 配对交易](strategies/mean-reversion/pairs-trading.md) - 统计套利中的经典策略
- [1.1.4 跨期套利](strategies/mean-reversion/calendar-spread.md) - 同一品种不同到期日的套利

#### 1.2 动量策略
- [1.2.1 简单动量策略](strategies/momentum/simple-momentum.md) - 追涨杀跌的基础实现
- [1.2.2 相对强弱动量](strategies/momentum/relative-momentum.md) - 行业/个股相对强弱排序
- [1.2.3 趋势跟踪](strategies/momentum/trend-following.md) - 海龟交易法则与改进
- [1.2.4 突破策略](strategies/momentum/breakout.md) - 支撑阻力位的突破交易

#### 1.3 因子投资策略
- [1.3.1 价值因子](strategies/factors/value-factor.md) - PE、PB、股息率等价值指标
- [1.3.2 成长因子](strategies/factors/growth-factor.md) - 营收增长、利润增长筛选
- [1.3.3 质量因子](strategies/factors/quality-factor.md) - ROE、负债率、现金流质量
- [1.3.4 低波动因子](strategies/factors/low-volatility.md) - 低波动异象与实现
- [1.3.5 多因子模型](strategies/factors/multi-factor.md) - Barra 模型与因子合成

#### 1.4 事件驱动策略
- [1.4.1 财报事件策略](strategies/events/earnings.md) - 超预期/低于预期的交易机会
- [1.4.2 并购套利](strategies/events/merger-arbitrage.md) - 并购 announcement 后的套利
- [1.4.3 指数调仓](strategies/events/index-rebalancing.md) - 指数成分股调整的机会
- [1.4.4 分红送股](strategies/events/dividend.md) - 分红季的交易策略

#### 1.5 高频/算法策略
- [1.5.1 做市商策略](strategies/hft/market-making.md) - 赚取买卖价差
- [1.5.2 冰山订单识别](strategies/hft/iceberg-detection.md) - 识别隐藏大单
- [1.5.3 订单流分析](strategies/hft/order-flow.md) - Level 2 数据的微观结构
- [1.5.4 延时套利](strategies/hft/latency-arbitrage.md) - 不同市场间的延迟套利

---

### 📁 2. 技术指标百科 (`indicators/`)

#### 2.1 趋势指标
- [2.1.1 移动平均线 (MA)](indicators/trend/ma.md) - SMA、EMA、WMA 全解析
- [2.1.2 指数平滑异同平均线 (MACD)](indicators/trend/macd.md) - 金叉死叉与背离
- [2.1.3 平均趋向指数 (ADX)](indicators/trend/adx.md) - 趋势强度判断
- [2.1.4 抛物线转向 (SAR)](indicators/trend/sar.md) - 止损与反转点
- [2.1.5 一目均衡表 (Ichimoku)](indicators/trend/ichimoku.md) - 日本云图技术

#### 2.2 动量指标
- [2.2.1 相对强弱指数 (RSI)](indicators/momentum/rsi.md) - 超买超卖的经典指标
- [2.2.2 随机指标 (KDJ/Stochastic)](indicators/momentum/stochastic.md) - 短线交易利器
- [2.2.3 商品通道指数 (CCI)](indicators/momentum/cci.md) - 价格波动范围
- [2.2.4 动量指标 (MOM)](indicators/momentum/mom.md) - 价格变化速度
- [2.2.5 变化率 (ROC)](indicators/momentum/roc.md) - 百分比变化率

#### 2.3 波动率指标
- [2.3.1 布林带 (Bollinger Bands)](indicators/volatility/bollinger.md) - 波动率通道
- [2.3.2 平均真实波幅 (ATR)](indicators/volatility/atr.md) - 止损设置的基准
- [2.3.3 标准差通道](indicators/volatility/std-channel.md) - 统计意义上的波动
- [2.3.4 肯特纳通道 (Keltner)](indicators/volatility/keltner.md) - ATR 基础上的通道
- [2.3.5 唐奇安通道 (Donchian)](indicators/volatility/donchian.md) - 突破系统的基石

#### 2.4 成交量指标
- [2.4.1 成交量 (Volume)](indicators/volume/volume.md) - 量价关系基础
- [2.4.2 能量潮 (OBV)](indicators/volume/obv.md) - 累积成交量指标
- [2.4.3 成交量加权平均价 (VWAP)](indicators/volume/vwap.md) - 机构成本线
- [2.4.4 量价趋势 (PVT)](indicators/volume/pvt.md) - 价格与成交量结合
- [2.4.5 资金流量指标 (MFI)](indicators/volume/mfi.md) - 成交量的 RSI
- [2.4.6 集散指标 (A/D Line)](indicators/volume/ad-line.md) - 累积/派发线

#### 2.5 市场情绪指标
- [2.5.1 恐慌/贪婪指数](indicators/sentiment/fear-greed.md) - CNN 恐慌贪婪指标解读
- [2.5.2  put/call 比率](indicators/sentiment/put-call-ratio.md) - 期权市场情绪
- [2.5.3 VIX 波动率指数](indicators/sentiment/vix.md) - 市场的"恐慌指数"
- [2.5.4 多空比率](indicators/sentiment/long-short.md) - 市场持仓情绪
- [2.5.5 新高新低指标](indicators/sentiment/new-high-low.md) - 市场广度指标

#### 2.6 复合指标系统
- [2.6.1 多指标共振系统](indicators/systems/confluence.md) - 多指标确认交易
- [2.6.2 自适应指标](indicators/systems/adaptive.md) - 根据波动率调整参数
- [2.6.3 机器学习指标](indicators/systems/ml-indicators.md) - AI 生成的技术指标

---

### 📁 3. 社媒情绪分析方法论 (`sentiment/`)

#### 3.1 数据采集与预处理
- [3.1.1  Twitter/X 数据抓取](sentiment/data-collection/twitter.md) - API 与爬虫方法
- [3.1.2  Reddit 数据采集](sentiment/data-collection/reddit.md) - WallStreetBets 等社区
- [3.1.3  微博/雪球中文数据源](sentiment/data-collection/weibo.md) - 中文社媒监控
- [3.1.4  Discord/Telegram 监控](sentiment/data-collection/discord.md) - 社群情绪追踪
- [3.1.5  新闻与财经媒体](sentiment/data-collection/news.md) - Bloomberg、Reuters 等

#### 3.2 自然语言处理 (NLP)
- [3.2.1  情感分析基础](sentiment/nlp/sentiment-basics.md) - 正负情绪分类
- [3.2.2  金融领域 NER](sentiment/nlp/financial-ner.md) - 命名实体识别
- [3.2.3  意图识别](sentiment/nlp/intent-recognition.md) - 买入/卖出/观望意图
- [3.2.4  讽刺与反语检测](sentiment/nlp/sarcasm.md) - 识别反向表达
- [3.2.5  多语言处理](sentiment/nlp/multilingual.md) - 中英文混合处理

#### 3.3 情绪指标构建
- [3.3.1  情绪得分计算](sentiment/indicators/sentiment-score.md) - 从文本到数值
- [3.3.2  情绪动量](sentiment/indicators/sentiment-momentum.md) - 情绪变化趋势
- [3.3.3  情绪极值](sentiment/indicators/sentiment-extremes.md) - 极度贪婪/恐慌
- [3.3.4  情绪分歧](sentiment/indicators/sentiment-divergence.md) - 多空分歧度
- [3.3.5  情绪与价格背离](sentiment/indicators/sentiment-price-divergence.md) - 领先指标

#### 3.4 社媒信号挖掘
- [3.4.1  关键词热度追踪](sentiment/signals/keyword-trending.md) - "到月球""持有"等
- [3.4.2  KOL 言论监控](sentiment/signals/kol-monitoring.md) - 大V观点追踪
- [3.4.3  散户情绪指数](sentiment/signals/retail-sentiment.md) - 散户 vs 机构
- [3.4.4  FOMO 检测](sentiment/signals/fomo-detection.md) - 错失恐惧识别
- [3.4.5  谣言与假新闻检测](sentiment/signals/misinformation.md) - 信息真实性验证

#### 3.5 实战应用案例
- [3.5.1  GameStop 事件复盘](sentiment/cases/gme.md) - 散户逼空经典案例
- [3.5.2  AMC 情绪分析](sentiment/cases/amc.md) - Meme 股情绪追踪
- [3.5.3  特斯拉社媒监控](sentiment/cases/tesla.md) - Elon 推文影响分析
- [3.5.4  加密货币情绪](sentiment/cases/crypto.md) - 币圈情绪周期
- [3.5.5  中概股情绪危机](sentiment/cases/chinese-stocks.md) - 政策与情绪

---

### 📁 4. 风控模型模板 (`risk-management/`)

#### 4.1 止损策略
- [4.1.1  固定比例止损](risk-management/stop-loss/fixed-percentage.md) - 简单有效的 5-8%
- [4.1.2  ATR 止损](risk-management/stop-loss/atr-stop.md) - 基于波动率的动态止损
- [4.1.3  技术位止损](risk-management/stop-loss/technical-stop.md) - 支撑/均线止损
- [4.1.4  时间止损](risk-management/stop-loss/time-stop.md) - 持仓时间限制
- [4.1.5  移动止损/跟踪止损](risk-management/stop-loss/trailing-stop.md) - 保护利润

#### 4.2 仓位管理
- [4.2.1  凯利公式](risk-management/position-sizing/kelly-criterion.md) - 最优仓位比例
- [4.2.2  固定分数法](risk-management/position-sizing/fixed-fractional.md) - 每笔风险固定
- [4.2.3  波动率仓位](risk-management/position-sizing/volatility-sizing.md) - 根据 ATR 调整
- [4.2.4  金字塔加仓](risk-management/position-sizing/pyramiding.md) - 趋势中的加仓艺术
- [4.2.5  马丁格尔与反马丁](risk-management/position-sizing/martingale.md) - 加倍策略的风险

#### 4.3 组合风险管理
- [4.3.1  相关性分析](risk-management/portfolio/correlation.md) - 避免风险集中
- [4.3.2  Beta 对冲](risk-management/portfolio/beta-hedging.md) - 市场风险对冲
- [4.3.3  行业分散](risk-management/portfolio/sector-diversification.md) - 行业配置策略
- [4.3.4  最大回撤控制](risk-management/portfolio/max-drawdown.md) - 历史最大回撤管理
- [4.3.5  风险平价](risk-management/portfolio/risk-parity.md) - 风险预算分配

#### 4.4 回撤与危机管理
- [4.4.1  回撤期识别](risk-management/drawdown/drawdown-detection.md) - 何时该休息
- [4.4.2  熔断机制](risk-management/drawdown/circuit-breaker.md) - 自动停止交易
- [4.4.3  黑天鹅应对](risk-management/drawdown/black-swan.md) - 尾部风险管理
- [4.4.4  压力测试](risk-management/drawdown/stress-testing.md) - 极端情况模拟
- [4.4.5  动态风险调整](risk-management/drawdown/dynamic-adjustment.md) - 根据市场环境调整

#### 4.5 交易心理与纪律
- [4.5.1  交易日志模板](risk-management/psychology/trading-journal.md) - 记录每一笔交易
- [4.5.2  情绪检测清单](risk-management/psychology/emotion-checklist.md) - 避免冲动交易
- [4.5.3  交易规则文档](risk-management/psychology/trading-rules.md) - 你的交易宪法
- [4.5.4  复盘方法论](risk-management/psychology/review-method.md) - 从错误中学习
- [4.5.5  连续亏损应对](risk-management/psychology/losing-streak.md) - 走出连败阴影

---

### 📁 5. 实战案例与代码 (`examples/`)

#### 5.1 完整策略实现
- [5.1.1  双均线策略完整代码](examples/complete/dual-ma.md) - 从数据到回测
- [5.1.2  RSI 超买超卖系统](examples/complete/rsi-system.md) - 完整的交易系统
- [5.1.3  布林带回撤策略](examples/complete/bollinger-reversion.md) - 均值回归实战
- [5.1.4  多因子选股模型](examples/complete/multi-factor-stock-pick.md) - 量化选股流程

#### 5.2 OpenClaw Agent 集成
- [5.2.1  Agent 监控股价示例](examples/openclaw/price-monitor.md) - 定时监控与提醒
- [5.2.2  Agent 情绪分析示例](examples/openclaw/sentiment-analysis.md) - 社媒数据处理
- [5.2.3  Agent 自动报告示例](examples/openclaw/auto-report.md) - 每日盘前简报
- [5.2.4  Agent 风控检查示例](examples/openclaw/risk-check.md) - 持仓风险扫描

#### 5.3 数据源接入
- [5.3.1  Yahoo Finance 数据](examples/data/yahoo-finance.md) - 免费美股数据
- [5.3.2  Alpha Vantage API](examples/data/alpha-vantage.md) - 技术指标数据
- [5.3.3  Tushare Pro](examples/data/tushare.md) - A股数据接口
- [5.3.4  Binance API](examples/data/binance.md) - 加密货币数据

---

### 📁 6. 工具与资源 (`tools/`)

#### 6.1 回测框架
- [6.1.1  Backtrader 指南](tools/backtesting/backtrader.md) - Python 回测框架
- [6.1.2  Zipline 指南](tools/backtesting/zipline.md) - Quantopian 开源框架
- [6.1.3  VectorBT 指南](tools/backtesting/vectorbt.md) - 向量化回测
- [6.1.4  Backtesting.py](tools/backtesting/backtesting-py.md) - 轻量级回测

#### 6.2 数据分析工具
- [6.2.1  Pandas 金融数据处理](tools/analysis/pandas-finance.md) - 时间序列处理
- [6.2.2  NumPy 数值计算](tools/analysis/numpy-finance.md) - 高效计算
- [6.2.3  TA-Lib 技术指标库](tools/analysis/ta-lib.md) - 150+ 技术指标
- [6.2.4  QuantStats 绩效分析](tools/analysis/quantstats.md) - 专业回测报告

#### 6.3 可视化工具
- [6.3.1  Matplotlib 金融图表](tools/viz/matplotlib-finance.md) - K线图与指标
- [6.3.2  Plotly 交互式图表](tools/viz/plotly-finance.md) - 交互式分析
- [6.3.3  TradingView Lightweight](tools/viz/tradingview-charts.md) - Web 端图表

#### 6.4 AI/ML 工具
- [6.4.1  Scikit-learn 预测模型](tools/ml/sklearn-finance.md) - 机器学习应用
- [6.4.2  TensorFlow/PyTorch 深度学习](tools/ml/deep-learning.md) - LSTM、Transformer
- [6.4.3  Prophet 时间序列](tools/ml/prophet.md) - Facebook  forecasting
- [6.4.4  NLP 情感分析工具](tools/ml/nlp-tools.md) - BERT、FinBERT

---

## 🚀 快速开始

### 安装与使用

```bash
# 克隆知识库
git clone https://github.com/freestylefly/openclaw-stock-kb.git
cd openclaw-stock-kb

# 浏览文档
# 推荐从 strategies/README.md 开始
```

### OpenClaw Agent 集成

```bash
# 在 OpenClaw 中使用
openclaw skill load openclaw-stock-kb

# 查询特定策略
openclaw query "给我 RSI 超买超卖的策略代码"
```

---

## 📖 阅读指南

### 初学者路线
1. 从 `indicators/trend/ma.md` 开始了解基础指标
2. 阅读 `strategies/mean-reversion/simple-mean-reversion.md` 学习第一个策略
3. 学习 `risk-management/stop-loss/fixed-percentage.md` 建立风控意识
4. 动手实践 `examples/complete/dual-ma.md` 的完整代码

### 进阶路线
1. 深入研究 `strategies/factors/multi-factor.md` 多因子模型
2. 掌握 `sentiment/` 情绪分析方法论
3. 实践 `risk-management/portfolio/` 组合风险管理
4. 开发自己的 `examples/openclaw/` Agent 策略

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. 创建你的 **Feature Branch** (`git checkout -b feature/AmazingStrategy`)
3. **提交** 你的修改 (`git commit -m 'Add some AmazingStrategy'`)
4. **推送** 到分支 (`git push origin feature/AmazingStrategy`)
5. 创建 **Pull Request**

### 贡献内容

- 📚 **新策略**: 添加你研究过的有效策略
- 📊 **新指标**: 补充遗漏的技术指标
- 🔧 **代码优化**: 改进现有示例代码
- 🐛 **Bug 修复**: 修正文档或代码错误
- 🌍 **翻译**: 将内容翻译成其他语言

### 文档规范

- 每个策略必须包含：原理说明、数学公式、代码示例、回测思路
- 技术指标必须包含：计算方法、参数说明、实战案例、注意事项
- 代码示例使用 Python，注释清晰

---

## 📚 推荐资源

### 经典书籍
- 《量化投资：策略与技术》 - 丁鹏
- 《主动投资组合管理》 - Grinold & Kahn
- 《Algorithmic Trading: Winning Strategies and Their Rationale》 - Chan
- 《Advances in Financial Machine Learning》 - Marcos Lopez de Prado

### 在线课程
- Coursera: Machine Learning for Trading
- Quantopian Lectures (Archive)
- 知乎/雪球专栏

### 数据源
- [Yahoo Finance](https://finance.yahoo.com/) - 免费美股数据
- [Tushare](https://tushare.pro/) - A股数据
- [Quandl](https://www.quandl.com/) - 金融数据平台
- [Binance API](https://binance-docs.github.io/apidocs/) - 加密货币

---

## ⚠️ 免责声明

**重要提示：**

1. **本知识库仅供学习研究，不构成投资建议**
2. **股市有风险，投资需谨慎**
3. **过往业绩不代表未来表现**
4. **任何策略都需要充分回测和验证**
5. **AI Agent 辅助决策，最终判断由人类做出**

**使用风险：**
- 量化策略可能在不同市场环境下失效
- 历史回测存在过拟合风险
- 实盘交易存在滑点、冲击成本
- 技术故障可能导致意外损失

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

**使用条件：**
- 自由使用、修改、分发
- 必须保留版权声明
- 作者不对使用结果负责

---

## 💬 社区交流

- **GitHub Discussions**: 技术讨论
- **Issues**: Bug 报告和功能建议
- **Discord** (即将开通): 实时交流

---

## 🙏 致谢

感谢以下项目和资源的支持：

- [OpenClaw](https://openclaw.ai/) - AI Agent 运行平台
- [Backtrader](https://www.backtrader.com/) - 回测框架
- [TA-Lib](https://ta-lib.org/) - 技术指标库
- [QuantConnect](https://www.quantconnect.com/) - 量化社区

---

<p align="center">
  <strong>📈 让 AI 成为你的投资伙伴，但请记住：最终决策权在你手中</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/freestylefly">OpenClaw AI Agent</a> and Contributors
</p>

<p align="center">
  <a href="https://github.com/freestylefly/openclaw-stock-kb/stargazers">
    <img src="https://img.shields.io/github/stars/freestylefly/openclaw-stock-kb?style=social" alt="Stars">
  </a>
  <a href="https://github.com/freestylefly/openclaw-stock-kb/network/members">
    <img src="https://img.shields.io/github/forks/freestylefly/openclaw-stock-kb?style=social" alt="Forks">
  </a>
</p>

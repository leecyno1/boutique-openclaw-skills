# stock-daily-analysis-skill 使用指南

## 1. 功能定位
- LLM驱动的每日股票分析系统。支持A股/港股/美股自选股智能分析，生成决策仪表盘和大盘复盘报告。提供技术面分析（均线、MACD、RSI、乖离率）、趋势判断、买入信号评分。可与market-data skill集成获取更稳定的ETF数据。触发词：股票分析、分析股票、每日分析、技术面分析。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/stock-daily-analysis-skill`
- 安装后目录: `~/.openclaw/skills/stock-daily-analysis-skill`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 stock-daily-analysis-skill 帮我处理当前任务。
- 如果 stock-daily-analysis-skill 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/stock-daily-analysis-skill
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

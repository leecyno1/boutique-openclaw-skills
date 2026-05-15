# News Radar 使用指南

## 1. 功能定位
- 通过 TrendRadar MCP 聚合国际新闻、热点话题和来源分析。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/news-radar`
- 安装后目录: `~/.openclaw/skills/news-radar`

## 2. 使用前准备
- TrendRadar MCP 服务 `http://localhost:3333/mcp`

## 3. 配置步骤
1. 先确认 TrendRadar MCP 容器/服务已运行。
2. 如果只想做普通网页搜索，不要优先用这个 skill。

## 4. 推荐提问方式
- 请用 news-radar 汇总过去 24 小时的 AI 热点。
- 请用 news-radar 比较 Reuters 和 Bloomberg 对同一事件的报道。

## 5. 手动验证
```bash
python3 skills/default/news-radar/scripts/get_trending_news.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/news-radar
- 本技能说明: `SKILL.md`

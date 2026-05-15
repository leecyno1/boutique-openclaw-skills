# stock_datasource 使用指南

## 1. 功能定位
- A股数据平台项目封装技能。内含多 Agent 投研平台说明，以及 `stock-mcp-query`、`stock-rt-subscribe`、`tushare-plugin-builder`、`mcp-api-key-auth` 等子技能资料。适用于规划或部署本地股票数据底座、MCP 查询服务、实时订阅与插件生成流程。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/stock_datasource`
- 安装后目录: `~/.openclaw/skills/stock_datasource`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 stock_datasource 帮我处理当前任务。
- 如果 stock_datasource 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/stock_datasource
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

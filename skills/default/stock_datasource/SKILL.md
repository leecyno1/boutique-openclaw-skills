---
name: stock_datasource
description: A股数据平台项目封装技能。内含多 Agent 投研平台说明，以及 `stock-mcp-query`、`stock-rt-subscribe`、`tushare-plugin-builder`、`mcp-api-key-auth` 等子技能资料。适用于规划或部署本地股票数据底座、MCP 查询服务、实时订阅与插件生成流程。
---

# stock_datasource Project Adapter

这是一个项目适配型技能，不是单一脚本。仓库内已打包了该项目的关键文档和其自带的多个子技能。

## 适用场景

- 规划本地股票数据平台或投研中台
- 搭建 MCP 查询服务或实时行情订阅
- 基于 Tushare 生成数据采集插件
- 给 OpenClaw 接入 ClickHouse / 实时行情 / 自建金融数据层

## 本地资料入口

- `README.md`：项目总览
- `docs/`：部署、数据库、CLI 和设计文档
- `skills/stock-mcp-query/`：MCP 查询子技能
- `skills/stock-rt-subscribe/`：实时订阅子技能
- `skills/tushare-plugin-builder/`：Tushare 插件生成子技能
- `skills/mcp-api-key-auth/`：MCP API Key 鉴权子技能

## 使用方式

1. 先判断你要做的是数据平台部署、MCP 查询、实时订阅还是插件生成。
2. 进入对应 `skills/` 子目录查看 `SKILL.md` 和脚本。
3. 若只是做研究总结，优先引用 `docs/` 与 `README.md` 的项目说明。

## 注意事项

- 这是平台级项目资料，部署复杂度明显高于普通 skill。
- 建议先在测试环境验证，不要直接接生产交易或实时资金系统。

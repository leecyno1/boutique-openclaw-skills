# openclaw-stock 使用指南

## 1. 功能定位
- 自动化交易项目参考技能。内含短线/长线策略、风控、回测、API 配置和多数据源架构说明。适用于研究自动交易系统设计、策略编排、模拟盘部署和数据源接入方案，不建议直接无验证接入实盘。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/openclaw-stock`
- 安装后目录: `~/.openclaw/skills/openclaw-stock`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 openclaw-stock 帮我处理当前任务。
- 如果 openclaw-stock 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/openclaw-stock
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

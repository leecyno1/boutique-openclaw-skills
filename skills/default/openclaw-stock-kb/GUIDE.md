# openclaw-stock-kb 使用指南

## 1. 功能定位
- 开源股票研究知识库封装技能。内含量化策略、技术指标、社媒情绪分析、风控模板和回测工具文档。适用于让 Agent 在本地检索股票研究方法、设计分析框架、撰写策略说明、整理指标解释和风控规则时引用。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/openclaw-stock-kb`
- 安装后目录: `~/.openclaw/skills/openclaw-stock-kb`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 openclaw-stock-kb 帮我处理当前任务。
- 如果 openclaw-stock-kb 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/openclaw-stock-kb
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

# content-intake-hub 使用指南

## 1. 功能定位
- 统一的内容入口 Skill。用于接收自动采集结果与人工命题输入，标准化为 Topic Intake Record，为后续 Brief 构建提供统一上游。适用于热点采集、人工提题、手工指定大纲意图、跨媒介内容任务发起。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/content-intake-hub`
- 安装后目录: `~/.openclaw/skills/content-intake-hub`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 content-intake-hub 帮我处理当前任务。
- 如果 content-intake-hub 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/content-intake-hub
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

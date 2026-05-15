# inference-skills 使用指南

## 1. 功能定位
- Inference Skills Hub（上游: inference-sh/skills）- 用于索引与选择 inference-sh 的工具型技能。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/inference-skills`
- 安装后目录: `~/.openclaw/skills/inference-skills`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 inference-skills 帮我处理当前任务。
- 如果 inference-skills 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/inference-skills
```

## 6. 参考资料
- 上游来源: https://github.com/inference-sh/skills
- 本技能说明: `SKILL.md`

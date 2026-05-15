# Skill Creator 使用指南

## 1. 功能定位
- 创建与迭代自定义 skill 的方法论和脚手架。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/skill-creator`
- 安装后目录: `~/.openclaw/skills/skill-creator`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请用 skill-creator 帮我设计一个新的投研 skill。
- 请用 skill-creator 审查这个 skill 的结构是否合格。

## 5. 手动验证
```bash
python3 skills/default/skill-creator/scripts/quick_validate.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/skill-creator
- 本技能说明: `SKILL.md`

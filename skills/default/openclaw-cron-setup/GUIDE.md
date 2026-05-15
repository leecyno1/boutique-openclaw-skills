# OpenClaw Cron Setup 使用指南

## 1. 功能定位
- 配置定时唤醒和主动任务执行框架。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/openclaw-cron-setup`
- 安装后目录: `~/.openclaw/skills/openclaw-cron-setup`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请用 openclaw-cron-setup 配一个每天 9 点的巡检任务。
- 请用 openclaw-cron-setup 设计定时执行但由 cron delivery 投递结果的流程。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/openclaw-cron-setup
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/openclaw-cron-setup
- 本技能说明: `SKILL.md`

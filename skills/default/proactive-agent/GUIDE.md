# Proactive Agent 使用指南

## 1. 功能定位
- 让 Agent 主动巡检、主动跟进，而不是只等用户输入。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/proactive-agent`
- 安装后目录: `~/.openclaw/skills/proactive-agent`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请按 proactive-agent 的规则设计一套主动巡检流程。
- 请用 proactive-agent 复核这套 heartbeat 机制是否足够主动。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/proactive-agent
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/proactive-agent
- 本技能说明: `SKILL.md`

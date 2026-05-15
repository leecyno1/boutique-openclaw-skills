# dispatching-parallel-agents 使用指南

## 1. 功能定位
- Use when two or more independent tasks can run in parallel without shared state.
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/dispatching-parallel-agents`
- 安装后目录: `~/.openclaw/skills/dispatching-parallel-agents`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 dispatching-parallel-agents 帮我处理当前任务。
- 如果 dispatching-parallel-agents 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/dispatching-parallel-agents
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

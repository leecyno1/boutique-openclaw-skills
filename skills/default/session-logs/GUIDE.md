# session-logs 使用指南

## 1. 功能定位
- Search and analyze your own session logs (older/parent conversations) using jq.
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/session-logs`
- 安装后目录: `~/.openclaw/skills/session-logs`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 session-logs 帮我处理当前任务。
- 如果 session-logs 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/session-logs
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`

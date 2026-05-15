# AgentMail MCP 使用指南

## 1. 功能定位
- 把 AgentMail 作为 MCP 服务接入 OpenClaw、Claude Desktop、Cursor 等客户端。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/agentmail-mcp`
- 安装后目录: `~/.openclaw/skills/agentmail-mcp`

## 2. 使用前准备
- 环境变量 `AGENTMAIL_API_KEY`
- 任选其一: 远程 MCP / `npx -y agentmail-mcp` / `pip install agentmail-mcp`

## 3. 配置步骤
1. 最简单的方式是远程 MCP：`https://mcp.agentmail.to`。
2. 本地方式可在 MCP 配置里写 `command: npx` 和 `args: ["-y", "agentmail-mcp"]`。
3. OpenClaw 集成时，把 `AGENTMAIL_API_KEY` 放到对应 MCP server 的 `env` 中。

## 4. 推荐提问方式
- 请把 AgentMail MCP 加到 OpenClaw 的 MCP 配置里。
- 请通过 AgentMail MCP 创建一个邮箱并读取最新邮件。

## 5. 手动验证
```bash
npx -y agentmail-mcp --help
```

## 6. 参考资料
- 上游来源: https://github.com/agentmail-to/agentmail-skills
- 本技能说明: `SKILL.md`

## 7. 备注
- 支持按 `--tools` 只暴露部分工具，降低权限面。

# AgentMail CLI 使用指南

## 1. 功能定位
- 通过命令行管理 AgentMail 邮箱、邮件、草稿、Webhook 与域名。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/agentmail-cli`
- 安装后目录: `~/.openclaw/skills/agentmail-cli`

## 2. 使用前准备
- 环境变量 `AGENTMAIL_API_KEY`
- CLI: `npm install -g agentmail-cli`

## 3. 配置步骤
1. 先配置 `AGENTMAIL_API_KEY`。
2. 安装 CLI 后执行 `agentmail inboxes list` 验证鉴权。

## 4. 推荐提问方式
- 请用 agentmail-cli 创建一个新的邮箱并列出 inbox。
- 请用 agentmail-cli 给指定邮箱发送测试邮件。

## 5. 手动验证
```bash
agentmail inboxes list
```

## 6. 参考资料
- 上游来源: https://github.com/agentmail-to/agentmail-skills
- 本技能说明: `SKILL.md`

## 7. 备注
- 支持 `--api-key`、`--base-url`、`--environment`、`--format`、`--debug`。

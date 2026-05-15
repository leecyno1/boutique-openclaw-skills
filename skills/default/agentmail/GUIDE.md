# AgentMail SDK 使用指南

## 1. 功能定位
- 给 Agent 提供独立邮箱能力，可创建邮箱、收发邮件、管理线程与附件。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/agentmail`
- 安装后目录: `~/.openclaw/skills/agentmail`

## 2. 使用前准备
- AgentMail 账号
- 环境变量 `AGENTMAIL_API_KEY`

## 3. 配置步骤
1. 访问 https://console.agentmail.to 获取 API Key。
2. 把 `AGENTMAIL_API_KEY=你的密钥` 写入 `~/.openclaw/env` 或当前 Shell。
3. Node 场景执行 `npm install agentmail`；Python 场景执行 `pip install agentmail`。

## 4. 推荐提问方式
- 请用 AgentMail 新建一个客户支持邮箱，并把地址告诉我。
- 请用 AgentMail 给某个收件人发送一封 HTML + 纯文本双版本邮件。

## 5. 手动验证
```bash
echo $AGENTMAIL_API_KEY
```

## 6. 参考资料
- 上游来源: https://github.com/agentmail-to/agentmail-skills
- 本技能说明: `SKILL.md`

## 7. 备注
- 官方文档首页: https://docs.agentmail.to/welcome
- OpenClaw 集成参考: https://docs.agentmail.to/integrations/openclaw

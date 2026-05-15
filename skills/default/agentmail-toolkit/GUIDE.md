# AgentMail Toolkit 使用指南

## 1. 功能定位
- 把邮件工具快速接到 AI SDK、LangChain、OpenAI Agents SDK、LiveKit 等框架。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/agentmail-toolkit`
- 安装后目录: `~/.openclaw/skills/agentmail-toolkit`

## 2. 使用前准备
- 环境变量 `AGENTMAIL_API_KEY`
- `npm install agentmail-toolkit` 或 `pip install agentmail-toolkit`

## 3. 配置步骤
1. 先确认 SDK 项目本身能运行。
2. 再引入对应框架版本的 AgentMailToolkit 并把工具注册给 Agent。

## 4. 推荐提问方式
- 请在 LangChain agent 中挂载 AgentMailToolkit。
- 请在 OpenAI Agents SDK 中接入 AgentMailToolkit 发送邮件。

## 5. 手动验证
```bash
python3 - <<'PY'
print("install agentmail-toolkit in your venv first")
PY
```

## 6. 参考资料
- 上游来源: https://github.com/agentmail-to/agentmail-skills
- 本技能说明: `SKILL.md`

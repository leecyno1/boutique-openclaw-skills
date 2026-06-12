---
name: ima
description: Connect and use IMA notes, notebooks, and knowledge bases from OpenClaw or Hermes. Use when the user asks to initialize IMA, authorize IMA API access, verify API Key or Client ID from controlled config, sync notes, list notebooks, read notes, query knowledge bases, or troubleshoot IMA note/knowledge retrieval. Never ask users to paste real API keys in chat.
---

# IMA Notes Connector

Use this skill when a user wants IMA notes, notebooks, or knowledge bases connected to the agent.

## Operating Rules

- Do not ask the user to paste real API keys, client secrets, refresh tokens, or cookies in chat.
- Prefer existing controlled configuration: `~/.openclaw/env`, `~/.openclaw/ima.env`, `~/.hermes/.env`, server-side managed config, or the product console panel.
- Prefer official IMA configuration, OAuth, MCP, CLI, or API surfaces when they are available in the runtime.
- If authorization is missing, give exactly one authorization entry and one next step.
- Redact secrets in logs and responses; show only whether required fields are present.
- Keep replies short: status, blocker if any, next action, test result.

## Quick Workflow

1. Detect whether an IMA skill/tool/API/MCP entry already exists in the active runtime.
2. Check controlled config for:
   - `IMA_API_KEY`
   - `IMA_CLIENT_ID`
   - `IMA_BASE_URL`
   - `OPENCLAW_IMA_API_KEY`
   - `OPENCLAW_IMA_CLIENT_ID`
   - `OPENCLAW_IMA_BASE_URL`
3. If config is present, run the smallest read-only test available:
   - list notebooks
   - list recent notes
   - list or query knowledge bases
4. If a test fails, report the failing layer: missing config, auth rejected, endpoint unreachable, permission denied, or empty data.
5. After a successful test, refresh the product IMA panel when the runtime exposes a refresh action.

## Response Shape

Use this compact shape:

```text
IMA 状态：已连接 / 待授权 / 配置缺失 / 读取失败
已确认：API Key/Client ID/Base URL（只说有无，不展示值）
测试：笔记本 / 笔记 / 知识库
下一步：...
```

## Fallback

If no official IMA runtime surface is installed yet:

1. Say: `当前缺少 IMA 运行时入口。`
2. Point the user to the product console IMA authorization panel or the configured install command if the environment exposes one.
3. Do not invent API endpoints.

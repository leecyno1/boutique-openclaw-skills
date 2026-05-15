# MiniMax Web Search 使用指南

## 1. 功能定位
- 优先使用 MiniMax MCP 做联网搜索。适合实时信息、新闻、资料查找。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/minimax-web-search`
- 安装后目录: `~/.openclaw/skills/minimax-web-search`

## 2. 使用前准备
- `uvx` / `uv tool`
- `MINIMAX_API_KEY` 或 `~/.openclaw/config/minimax.json`

## 3. 配置步骤
1. 先确认 `uvx minimax-coding-plan-mcp --help` 可用。
2. 没有的话先安装 `uv`，再执行 `uv tool install minimax-coding-plan-mcp`。
3. 把 MiniMax key 存到 `~/.openclaw/config/minimax.json`。

## 4. 推荐提问方式
- 请用 minimax-web-search 搜今天的 AI 新闻。
- 请用 minimax-web-search 查某公司的最新财报消息。

## 5. 手动验证
```bash
python3 skills/default/minimax-web-search/scripts/web_search.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/minimax-web-search
- 本技能说明: `SKILL.md`

## 7. 备注
- 购买/开通入口参见 skill 内说明。

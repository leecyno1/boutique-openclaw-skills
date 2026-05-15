# Tavily Search 使用指南

## 1. 功能定位
- LLM 优化的网页搜索，适合高质量检索和带筛选条件的搜索。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/tavily-search`
- 安装后目录: `~/.openclaw/skills/tavily-search`

## 2. 使用前准备
- Tavily OAuth 或 `TAVILY_API_KEY`

## 3. 配置步骤
1. 首次运行可走 OAuth 浏览器登录。
2. 或直接把 `TAVILY_API_KEY` 写入环境变量。

## 4. 推荐提问方式
- 请用 tavily-search 搜索最近一周的 AI Agent 新闻。
- 请用 tavily-search 仅搜索 arxiv.org 和 github.com 的资料。

## 5. 手动验证
```bash
bash skills/default/tavily-search/scripts/search.sh --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/tavily-search
- 本技能说明: `SKILL.md`

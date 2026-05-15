# Web Search 使用指南

## 1. 功能定位
- 基于 DuckDuckGo 的通用网页/新闻/图片/视频搜索。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/web-search`
- 安装后目录: `~/.openclaw/skills/web-search`

## 2. 使用前准备
- Python 依赖 `duckduckgo-search`

## 3. 配置步骤
1. 执行 `pip install duckduckgo-search`。
2. 不需要 API Key。

## 4. 推荐提问方式
- 请用 web-search 搜今天的科技新闻。
- 请用 web-search 搜指定主题的图片结果。

## 5. 手动验证
```bash
python3 skills/default/web-search/scripts/search.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/web-search
- 本技能说明: `SKILL.md`

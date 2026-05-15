# URL to Markdown 使用指南

## 1. 功能定位
- 把网页转换成 Markdown，适合做资料存档和进一步摘要。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/url-to-markdown`
- 安装后目录: `~/.openclaw/skills/url-to-markdown`

## 2. 使用前准备
- Node/TS 运行环境
- 如需指定浏览器可配 `URL_CHROME_PATH`

## 3. 配置步骤
1. 无 API Key。
2. 若默认浏览器不可用，可配置 `URL_CHROME_PATH`、`URL_DATA_DIR`、`URL_CHROME_PROFILE_DIR`。

## 4. 推荐提问方式
- 请用 url-to-markdown 把这个网页转成 Markdown。
- 请用 url-to-markdown 抽取正文并保存。

## 5. 手动验证
```bash
node --version
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/url-to-markdown
- 本技能说明: `SKILL.md`

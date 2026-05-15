# Summarize 使用指南

## 1. 功能定位
- 总结网页、PDF、本地文件、图片、音视频和 YouTube 链接。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/summarize`
- 安装后目录: `~/.openclaw/skills/summarize`

## 2. 使用前准备
- 二进制 `summarize`
- 至少一种模型 API Key：`OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `XAI_API_KEY` / `GEMINI_API_KEY`

## 3. 配置步骤
1. 安装 summarize CLI。
2. 在 `~/.openclaw/env` 或当前 shell 设置所选模型厂商的 key。
3. 如需 YouTube 回退可再配置 `APIFY_API_TOKEN`；如需网页反爬回退可配置 `FIRECRAWL_API_KEY`。

## 4. 推荐提问方式
- 请用 summarize 总结这个 PDF。
- 请用 summarize 概括这个 YouTube 视频内容。

## 5. 手动验证
```bash
summarize --help
```

## 6. 参考资料
- 上游来源: https://summarize.sh
- 本技能说明: `SKILL.md`

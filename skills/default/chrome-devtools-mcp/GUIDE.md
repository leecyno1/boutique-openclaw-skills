# Chrome DevTools MCP 使用指南

## 1. 功能定位
- Google 官方的 Chrome/CDP 自动化与调试能力，适合网页调试、性能分析和复杂表单自动化。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/chrome-devtools-mcp`
- 安装后目录: `~/.openclaw/skills/chrome-devtools-mcp`

## 2. 使用前准备
- Node.js v20.19+
- Chrome/Chromium

## 3. 配置步骤
1. 先执行 `npx -y chrome-devtools-mcp@latest --help`。
2. 服务器环境建议加 `--headless`。
3. 如需持久配置，可用 `python3 scripts/setup_chrome_mcp.py setup`。

## 4. 推荐提问方式
- 请用 chrome-devtools-mcp 打开网页并导出性能 trace。
- 请用 chrome-devtools-mcp 自动填写表单并截图。

## 5. 手动验证
```bash
npx -y chrome-devtools-mcp@latest --help
```

## 6. 参考资料
- 上游来源: https://github.com/ChromeDevTools/chrome-devtools-mcp
- 本技能说明: `SKILL.md`

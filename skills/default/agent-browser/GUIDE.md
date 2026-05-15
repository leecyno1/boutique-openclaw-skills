# Agent Browser 使用指南

## 1. 功能定位
- 浏览器自动化 CLI。适合网页打开、点击、表单填写、抓取页面文本。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/agent-browser`
- 安装后目录: `~/.openclaw/skills/agent-browser`

## 2. 使用前准备
- Node.js / npm
- 建议执行 `npm install -g agent-browser && agent-browser install`

## 3. 配置步骤
1. 确认 `agent-browser --help` 可执行。
2. 首次运行后用 `agent-browser snapshot -i` 获取页面元素引用。

## 4. 推荐提问方式
- 请用 agent-browser 打开这个页面并提取标题与按钮文案。
- 请用 agent-browser 登录测试站点，遇到交互元素先 snapshot 再操作。

## 5. 手动验证
```bash
agent-browser --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/agent-browser
- 本技能说明: `SKILL.md`

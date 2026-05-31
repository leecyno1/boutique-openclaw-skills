# skill-vetter 使用指南

## 1. 功能定位
- Multi-scanner security gate. Use before installing or reviewing external skills for Claude Code, OpenClaw, Codex, or other AI agents.
- 仓库目录: `skills/default/skill-vetter`
- 原生上游: https://github.com/app-incubator-xyz/skill-vetter

## 2. 使用前准备
- 基础扫描可直接运行。
- 完整扫描建议安装 `aguara`、`skill-scanner`、`jq`、`git`。

## 3. 常用命令
```bash
bash scripts/check-deps.sh
bash scripts/vett.sh <skill-name-or-path-or-url>
```

## 4. 推荐提问方式
- 安装这个 skill 前，请先用 skill-vetter 审核。
- 请扫描这个 GitHub skill 仓库是否有注入、密钥或危险脚本。

## 5. 注意事项
- 审核结论是安全辅助，不等于绝对安全保证。
- 若结果为 `BLOCKED`，不要安装；若为 `REVIEW NEEDED`，先人工复核。

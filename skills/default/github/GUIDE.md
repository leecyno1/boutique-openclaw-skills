# GitHub 使用指南

## 1. 功能定位
- 通过 `gh` CLI 操作 issue / PR / Actions / API。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/github`
- 安装后目录: `~/.openclaw/skills/github`

## 2. 使用前准备
- GitHub CLI `gh`
- 已登录 `gh auth login` 或 `GH_TOKEN`

## 3. 配置步骤
1. 先执行 `gh auth status` 确认登录。
2. 非仓库目录中操作时，命令补 `--repo owner/repo`。

## 4. 推荐提问方式
- 请用 github 看一下这个 PR 的 CI 为什么失败。
- 请用 github 列出某仓库最近 10 个 issue。

## 5. 手动验证
```bash
gh auth status
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/github
- 本技能说明: `SKILL.md`

# Blogwatcher 使用指南

## 1. 功能定位
- 监控博客与 RSS/Atom 订阅源更新。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/blogwatcher`
- 安装后目录: `~/.openclaw/skills/blogwatcher`

## 2. 使用前准备
- 二进制 `blogwatcher`

## 3. 配置步骤
1. Go 安装: `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`。
2. 先执行 `blogwatcher add "名称" URL` 建立订阅，再执行 `blogwatcher scan`。

## 4. 推荐提问方式
- 请帮我新增一个 RSS 订阅并扫描最近更新。
- 请用 blogwatcher 列出未读文章。

## 5. 手动验证
```bash
blogwatcher --help
```

## 6. 参考资料
- 上游来源: https://github.com/Hyaxia/blogwatcher
- 本技能说明: `SKILL.md`

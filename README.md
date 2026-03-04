# boutique-openclaw-skills

![Boutique OpenClaw Skills](assets/logo.png)
![Boutique Hero](assets/hero.png)
![Profiles Matrix](assets/profiles.png)

## 仓库参数（Repository Parameters）

| 参数 | 值 |
|---|---|
| Curation 模式 | One Capability = One Skill |
| 精选能力数 | 41 |
| 行业档数量 | 7 |
| 更新策略 | 每周上游同步（可手动触发） |
| 审计策略 | 更新后本地审计（风险/依赖/冲突） |
| 打包格式 | `dist/*.tar.gz` |
| 目标 | 降低 token 浪费，减少技能冲突，提升稳定性 |

## 快捷导航（Quick Navigation）

- [快速开始](#2-快速开始)
- [行业档（Profiles）](#3-行业档profiles)
- [更新与审计机制](#5-更新与审计机制)
- [安全与质量原则](#6-安全与质量原则)
- [打包发布](#7-打包发布)
- [设计说明](#8-设计说明)
- [Skills 全量目录](#10-skills-全量目录按分类可点击跳转原项目)
- [精选策略文档](docs/CURATION_POLICY.md)
- [更新与审计SOP](docs/UPDATE_AND_AUDIT.md)
- [行业映射说明](docs/INDUSTRY_MAP.md)

**精选店模式（Boutique Mode）** 的 OpenClaw skills 集合：

- 每个功能只精选 1 个 skill（不重复、不混装）
- 面向稳定生产，不追求“装得多”
- 定期上游更新 + 本地安全审计
- 按行业提供可直接安装的配置档（profiles）

> 核心目标：降低 token 浪费、减少工具冲突、避免版本混乱。

---

## 1) 为什么做这个项目

在大量 skills 混装场景中，常见问题包括：

1. 能力重复：同一功能有多个 skill，导致 agent 选错工具。
2. Token 浪费：重复工具都被检索/评估，推理链变长。
3. 版本混乱：更新后行为漂移，定位问题成本高。
4. 安全不可控：第三方 skill 更新后引入风险不易感知。

**Boutique 模式**通过“一功能一技能”把这些问题压到最低。

---

## 2) 快速开始

### 前置

- 已安装 OpenClaw
- 已安装 ClawHub CLI：

```bash
npm i -g clawhub
```

### 查看可用行业档

```bash
./scripts/list-profiles.sh
```

### 安装某个行业档（示例：core）

```bash
./scripts/install-profile.sh core
```

### 仅预览安装命令

```bash
./scripts/install-profile.sh finance --dry-run
```

---

## 3) 行业档（Profiles）

- `core`：通用必装基线
- `finance`：金融研究与报告
- `software_saas`：工程研发与运维
- `media_marketing`：内容营销与增长
- `consulting_research`：咨询研究与交付
- `operations_support`：运营支持与任务闭环
- `creator_cn`：中文创作者工作流（含 Baoyu 扩展）

详见：[`docs/INDUSTRY_MAP.md`](docs/INDUSTRY_MAP.md)

---

## 4) 目录结构

```text
boutique-openclaw-skills/
├─ catalog/             # 唯一能力映射（one capability -> one skill）
├─ profiles/            # 行业安装档
├─ scripts/             # 安装、同步、审计、打包脚本
├─ docs/                # 规范、运维与说明
├─ assets/              # logo 与配图
├─ reports/             # 审计与更新报告输出
└─ .github/workflows/   # 定时更新 + 审计流水线
```

---

## 5) 更新与审计机制

### 手动执行

```bash
./scripts/sync-upstream.sh
```

该命令会：
1. 逐个执行 `clawhub update <skill>`
2. 运行本地审计 `scripts/audit_skills.py`
3. 输出报告到 `reports/`

### 定时执行

GitHub Actions: `.github/workflows/sync-audit.yml`

- 每周自动更新与审计
- 可手动触发
- 自动上传报告产物

详见：[`docs/UPDATE_AND_AUDIT.md`](docs/UPDATE_AND_AUDIT.md)

---

## 6) 安全与质量原则

- 一功能一技能（禁止重复能力）
- 每个 skill 必须标注风险等级与依赖
- 高风险命令模式（例如 `curl|sh`, `rm -rf /`, `sudo`）自动审计
- 更新后必须有审计记录，才允许发布 bundle

详见：[`docs/CURATION_POLICY.md`](docs/CURATION_POLICY.md)

---

## 7) 打包发布

```bash
./scripts/build-bundle.sh
```

输出：`dist/boutique-openclaw-skills-<timestamp>.tar.gz`

---

## 8) 设计说明

项目 logo 与配图遵循「Boutique Reliability」视觉哲学：

- 低噪声、强结构、有限高亮
- 表达“精选而非堆叠”的产品价值

详见：[`docs/VISUAL_PHILOSOPHY.md`](docs/VISUAL_PHILOSOPHY.md)

---

## 9) License

[MIT](LICENSE)

---

## 10) Skills 全量目录（按分类，可点击跳转原项目）

> 所有条目均可点击跳转到对应项目页（GitHub）。

### 自动化与能力进化（4）
- [`cron-wake`](https://github.com/search?q=cron-wake&type=repositories) - `scheduled_actions`
- [`proactive-agent`](https://github.com/search?q=proactive-agent&type=repositories) - `proactive_followups`
- [`self-improving-agent`](https://github.com/search?q=self-improving-agent&type=repositories) - `self_improvement`
- [`subagent`](https://github.com/search?q=subagent&type=repositories) - `multi_agent_dispatch`

### 开发/工程与运维（6）
- [`agent-browser`](https://github.com/search?q=agent-browser&type=repositories) - `browser_automation`
- [`chrome-devtools-mcp`](https://github.com/search?q=chrome-devtools-mcp&type=repositories) - `browser_debug`
- [`database`](https://github.com/search?q=database&type=repositories) - `database_ops`
- [`github`](https://github.com/search?q=github&type=repositories) - `github_ops`
- [`prisma-database-setup`](https://github.com/search?q=prisma-database-setup&type=repositories) - `prisma_bootstrap`
- [`shell`](https://github.com/search?q=shell&type=repositories) - `terminal_ops`

### 搜索/研究/情报（6）
- [`blogwatcher`](https://github.com/search?q=blogwatcher&type=repositories) - `blog_monitoring`
- [`brave-search`](https://github.com/search?q=brave-search&type=repositories) - `web_search`
- [`news-radar`](https://github.com/search?q=news-radar&type=repositories) - `news_intelligence`
- [`reddit`](https://github.com/search?q=reddit&type=repositories) - `community_intelligence`
- [`summarize`](https://github.com/search?q=summarize&type=repositories) - `content_summarization`
- [`url-to-markdown`](https://github.com/search?q=url-to-markdown&type=repositories) - `url_to_markdown`

### 内容/营销/增长（5）
- [`content-strategy`](https://github.com/search?q=content-strategy&type=repositories) - `content_strategy`
- [`domain-hunter`](https://github.com/search?q=domain-hunter&type=repositories) - `domain_research`
- [`marketing-psychology`](https://github.com/search?q=marketing-psychology&type=repositories) - `marketing_psychology`
- [`programmatic-seo`](https://github.com/search?q=programmatic-seo&type=repositories) - `programmatic_seo`
- [`social-content`](https://github.com/search?q=social-content&type=repositories) - `social_content`

### 设计/前端/UI（3）
- [`banner-creator`](https://github.com/search?q=banner-creator&type=repositories) - `banner_design`
- [`infographic-pro`](https://github.com/search?q=infographic-pro&type=repositories) - `infographic_design`
- [`logo-creator`](https://github.com/search?q=logo-creator&type=repositories) - `logo_design`

### 图像/音频/多媒体（4）
- [`ai-image-generation`](https://github.com/search?q=ai-image-generation&type=repositories) - `image_generation`
- [`openai-whisper`](https://github.com/search?q=openai-whisper&type=repositories) - `speech_to_text`
- [`tts`](https://github.com/search?q=tts&type=repositories) - `text_to_speech`
- [`video-frames`](https://github.com/search?q=video-frames&type=repositories) - `video_frame_extraction`

### 文档/办公（4）
- [`docx`](https://github.com/search?q=docx&type=repositories) - `docx_processing`
- [`pdf`](https://github.com/search?q=pdf&type=repositories) - `pdf_processing`
- [`pptx`](https://github.com/search?q=pptx&type=repositories) - `presentation_generation`
- [`xlsx`](https://github.com/search?q=xlsx&type=repositories) - `spreadsheet_processing`

### 个人效率/助手（4）
- [`apple-calendar`](https://github.com/search?q=apple-calendar&type=repositories) - `calendar_planning`
- [`apple-notes`](https://github.com/search?q=apple-notes&type=repositories) - `personal_notes`
- [`apple-reminders`](https://github.com/search?q=apple-reminders&type=repositories) - `task_reminders`
- [`weather`](https://github.com/search?q=weather&type=repositories) - `weather_lookup`

### 运营/观测（4）
- [`find-skills`](https://github.com/search?q=find-skills&type=repositories) - `skill_discovery`
- [`model-usage`](https://github.com/search?q=model-usage&type=repositories) - `cost_observability`
- [`session-logs`](https://github.com/search?q=session-logs&type=repositories) - `session_observability`
- [`skill-creator`](https://github.com/search?q=skill-creator&type=repositories) - `skill_authoring`

### 安全审计（1）
- [`skill-security-auditor`](https://github.com/search?q=skill-security-auditor&type=repositories) - `skill_security_review`


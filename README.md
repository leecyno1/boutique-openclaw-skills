# boutique-openclaw-skills

![Boutique OpenClaw Skills](assets/logo.png)
![Boutique Hero](assets/hero.png)
![Profiles Matrix](assets/profiles.png)

## 仓库参数（Repository Parameters）

| 参数 | 值 |
|---|---|
| Curation 模式 | Default Skills Tier Registry + Boutique Profiles |
| 默认技能数 | 318 |
| 默认三档 | low `67` / medium `74` / high `179` |
| 行业档数量 | 7（兼容保留） |
| 更新策略 | 从安装器或上游源导入后生成三档与手册 |
| 审计策略 | 本地审计（风险/依赖/冲突） |
| 打包格式 | `dist/*.tar.gz` |
| 目标 | 让安装器仓库瘦身，并集中维护默认 skills |

## 快捷导航（Quick Navigation）

- [快速开始](#2-快速开始)
- [默认 Skills 三档](#3-默认-skills-三档default-skill-tiers)
- [更新与审计机制](#6-更新与审计机制)
- [安全与质量原则](#7-安全与质量原则)
- [打包发布](#8-打包发布)
- [设计说明](#9-设计说明)
- [默认技能手册索引](docs/SKILL_MANUALS.md)
- [精选策略文档](docs/CURATION_POLICY.md)
- [更新与审计SOP](docs/UPDATE_AND_AUDIT.md)
- [行业映射说明](docs/INDUSTRY_MAP.md)

**Boutique Skills Registry** 是 OpenClaw 默认 skills 的独立维护仓库：

- 安装器仓库不再 vendoring 默认 skills 大包，只负责安装、网站接线、注册表与测试。
- 本仓库维护 `skills/default`、`tiers/low|medium|high.json`、三档说明、使用手册和原仓库链接。
- 低/中/高三档作为安装主线；原行业 profiles 作为兼容/附加精选能力保留。
- 更新后本地审计，发布 bundle 给安装器或用户同步。

> 核心目标：集中维护默认技能，降低安装器体积，并让技能分档、说明和来源可审计。

---

## 1) 为什么做这个项目

在大量 skills 混装场景中，常见问题包括：

1. 能力重复：同一功能有多个 skill，导致 agent 选错工具。
2. Token 浪费：重复工具都被检索/评估，推理链变长。
3. 版本混乱：更新后行为漂移，定位问题成本高。
4. 安全不可控：第三方 skill 更新后引入风险不易感知。

**Boutique 模式**通过独立仓库和三档清单把这些问题压到最低。

---

## 2) 快速开始

### 前置

- 已安装 OpenClaw
- 如由安装器调用，无需手动执行本仓库脚本；安装器默认从 Gitee `OPENCLAW_SKILLS_REPO_URL=https://gitee.com/leecyno1/boutique-openclaw-skills.git` 拉取，GitHub 作为回退。

### 安装默认三档

```bash
./scripts/install-tier.sh low --dry-run
./scripts/install-tier.sh medium
./scripts/install-tier.sh high
```

### 查看兼容行业档

```bash
./scripts/list-profiles.sh
./scripts/install-profile.sh finance --dry-run
```

---


## 3) 默认 Skills 三档（Default Skill Tiers）

本仓库现在是 OpenClaw 默认 skills 的维护源。安装器仓库只保留安装器、网站接线、注册表和测试逻辑；需要同步 skills 时，从本仓库生成或拉取。

| 档位 | 适用场景 | 技能数 | 清单 | 使用手册 |
|---|---|---:|---|---|
| low | 首次安装、轻量生产、低 token 噪声 | 67 | [`tiers/low.json`](tiers/low.json) | [`docs/tiers/low.md`](docs/tiers/low.md) |
| medium | 标准生产、常用扩展、MiniMax/文档/规划 | 74 | [`tiers/medium.json`](tiers/medium.json) | [`docs/tiers/medium.md`](docs/tiers/medium.md) |
| high | 完整专家包、金融交易、创作套件、AlphaEar | 179 | [`tiers/high.json`](tiers/high.json) | [`docs/tiers/high.md`](docs/tiers/high.md) |

安装示例：

```bash
./scripts/install-tier.sh low --dry-run
./scripts/install-tier.sh medium
./scripts/install-tier.sh high
```

完整默认技能手册索引：[`docs/SKILL_MANUALS.md`](docs/SKILL_MANUALS.md)。每个条目包含详细技能说明、使用手册路径和原仓库链接。

同步来源说明：

```bash
python3 scripts/import_installer_default_skills.py --installer-root /path/to/OpenClawInstaller
```

## 4) 行业档（Profiles，兼容保留）

- `core`：通用必装基线
- `finance`：金融研究与报告
- `software_saas`：工程研发与运维
- `media_marketing`：内容营销与增长
- `consulting_research`：咨询研究与交付
- `operations_support`：运营支持与任务闭环
- `creator_cn`：中文创作者工作流（含 Baoyu 扩展）

详见：[`docs/INDUSTRY_MAP.md`](docs/INDUSTRY_MAP.md)

---

## 5) 目录结构

```text
boutique-openclaw-skills/
├─ skills/default/      # 默认 skills 源
├─ tiers/               # low / medium / high 三档 JSON
├─ catalog/             # 默认技能 catalog 与兼容精选能力映射
├─ profiles/            # 行业安装档（兼容保留）
├─ scripts/             # 安装、同步、审计、打包脚本
├─ docs/                # 规范、运维与说明
├─ assets/              # logo 与配图
├─ reports/             # 审计与更新报告输出
└─ .github/workflows/   # 定时更新 + 审计流水线
```

---

## 6) 更新与审计机制

### 手动执行

```bash
./scripts/sync-upstream.sh
```

默认三档主线使用：
1. `scripts/import_installer_default_skills.py` 导入或刷新 `skills/default`
2. 生成 `tiers/*.json`、`docs/tiers/*.md`、`docs/SKILL_MANUALS.md`
3. 运行本地审计 `scripts/audit_skills.py` 并输出报告到 `reports/`

兼容精选 profiles 仍可使用 `scripts/sync-upstream.sh` 调用 ClawHub 更新。

### 定时执行

GitHub Actions: `.github/workflows/sync-audit.yml`

- 每周自动更新与审计
- 可手动触发
- 自动上传报告产物

详见：[`docs/UPDATE_AND_AUDIT.md`](docs/UPDATE_AND_AUDIT.md)

---

## 7) 安全与质量原则

- 一功能一技能（禁止重复能力）
- 每个 skill 必须标注风险等级与依赖
- 高风险命令模式（例如 `curl|sh`, `rm -rf /`, `sudo`）自动审计
- 更新后必须有审计记录，才允许发布 bundle

详见：[`docs/CURATION_POLICY.md`](docs/CURATION_POLICY.md)

---

## 8) 打包发布

```bash
./scripts/build-bundle.sh
```

输出：`dist/boutique-openclaw-skills-<timestamp>.tar.gz`

### 国内源发布

安装器默认使用 Gitee 技能源，因此发布顺序应先推送 Gitee，再推送 GitHub：

```bash
git push gitee-leecyno1 main
git push origin main
```

如果首次配置远端：

```bash
git remote add gitee-leecyno1 https://gitee.com/leecyno1/boutique-openclaw-skills.git
```


---

## 9) 设计说明

项目 logo 与配图遵循「Boutique Reliability」视觉哲学：

- 低噪声、强结构、有限高亮
- 表达“精选而非堆叠”的产品价值

详见：[`docs/VISUAL_PHILOSOPHY.md`](docs/VISUAL_PHILOSOPHY.md)

---

## 10) License

[MIT](LICENSE)

---

## 11) Skills 目录（兼容精选 + 默认索引）

<!-- SKILLS_INDEX:START -->
- 兼容精选 skills：`41`
- 默认 low / medium / high：`67` / `74` / `179`
- 默认 skills 维护源：`skills/default` + `tiers/*.json`

> 默认 skills 由本仓库维护；安装器仓库只保留 manifest 兼容缓存和同步入口。

## Table of Contents

| 分类 | 跳转 | 分类 | 跳转 |
|---|---|---|---|
| [Agent/自动化与能力进化](#agent-automation) (8) | [分类文件](categories/agent-automation.md) | [开发/工程与运维](#engineering-ops) (7) | [分类文件](categories/engineering-ops.md) |
| [搜索/研究/情报](#research-intel) (6) | [分类文件](categories/research-intel.md) | [设计/前端/UI](#design-ui) (3) | [分类文件](categories/design-ui.md) |
| [内容/营销/增长](#content-growth) (5) | [分类文件](categories/content-growth.md) | [图像/音频/多媒体生成处理](#media-generation) (4) | [分类文件](categories/media-generation.md) |
| [文档/办公生产力](#docs-office) (4) | [分类文件](categories/docs-office.md) | [Baoyu 系列内容产出与分发](#baoyu-suite) (0) | [分类文件](categories/baoyu-suite.md) |
| [其他集成能力](#other-integrations) (4) | [分类文件](categories/other-integrations.md) | [默认 Skills 低档](#default-tier-low) | [文档](docs/tiers/low.md) |
| [默认 Skills 中档](#default-tier-medium) | [文档](docs/tiers/medium.md) | [默认 Skills 高档](#default-tier-high) | [文档](docs/tiers/high.md) |

<a id="agent-automation"></a>
<details open><summary><h3 style="display:inline">Agent/自动化与能力进化</h3></summary>

- [`cron-wake`](https://github.com/search?q=cron-wake&type=repositories) - Scheduled proactive jobs.
- [`find-skills`](https://github.com/search?q=find-skills&type=repositories) - Search skills catalog efficiently.
- [`model-usage`](https://github.com/search?q=model-usage&type=repositories) - Token/cost visibility.
- [`proactive-agent`](https://github.com/search?q=proactive-agent&type=repositories) - Follow-up loops without manual prompts.
- [`self-improving-agent`](https://github.com/search?q=self-improving-agent&type=repositories) - Captures failure patterns and corrections.
- [`session-logs`](https://github.com/search?q=session-logs&type=repositories) - Analyze conversations and failures.
- [`skill-creator`](https://github.com/search?q=skill-creator&type=repositories) - Create/update in-house skills.
- [`subagent`](https://github.com/search?q=subagent&type=repositories) - Parallel subtask delegation.

> **[查看该分类完整列表 →](categories/agent-automation.md)**
</details>

<a id="engineering-ops"></a>
<details open><summary><h3 style="display:inline">开发/工程与运维</h3></summary>

- [`agent-browser`](https://github.com/search?q=agent-browser&type=repositories) - Automate interactive websites.
- [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) - CDP debugging + performance traces.
- [`database`](https://github.com/search?q=database&type=repositories) - Unified DB operations.
- [`github`](https://github.com/search?q=github&type=repositories) - PR/issue/actions operations.
- [`prisma-database-setup`](https://github.com/search?q=prisma-database-setup&type=repositories) - Prisma setup and troubleshooting.
- [`shell`](https://github.com/search?q=shell&type=repositories) - Single terminal executor; keep sandbox policy strict.
- [`skill-security-auditor`](https://github.com/search?q=skill-security-auditor&type=repositories) - Static safety checks for skill code/prompts.

> **[查看该分类完整列表 →](categories/engineering-ops.md)**
</details>

<a id="research-intel"></a>
<details open><summary><h3 style="display:inline">搜索/研究/情报</h3></summary>

- [`blogwatcher`](https://github.com/Hyaxia/blogwatcher) - RSS/blog updates.
- [`brave-search`](https://github.com/search?q=brave-search&type=repositories) - Primary web search; fast + low token overhead.
- [`news-radar`](https://github.com/search?q=news-radar&type=repositories) - News monitoring and topic tracking.
- [`reddit`](https://github.com/ReScienceLab/opc-skills/tree/main/skills/reddit) - Reddit query and extraction.
- [`summarize`](https://github.com/search?q=summarize&type=repositories) - Summarize URL/PDF/media with one tool.
- [`url-to-markdown`](https://github.com/search?q=url-to-markdown&type=repositories) - Convert web pages to markdown.

> **[查看该分类完整列表 →](categories/research-intel.md)**
</details>

<a id="design-ui"></a>
<details open><summary><h3 style="display:inline">设计/前端/UI</h3></summary>

- [`banner-creator`](https://github.com/search?q=banner-creator&type=repositories) - Marketing banners.
- [`infographic-pro`](https://github.com/search?q=infographic-pro&type=repositories) - Data visual storytelling.
- [`logo-creator`](https://github.com/ReScienceLab/opc-skills/tree/main/skills/logo-creator) - Brand logo generation.

> **[查看该分类完整列表 →](categories/design-ui.md)**
</details>

<a id="content-growth"></a>
<details open><summary><h3 style="display:inline">内容/营销/增长</h3></summary>

- [`content-strategy`](https://github.com/search?q=content-strategy&type=repositories) - Editorial planning.
- [`domain-hunter`](https://github.com/ReScienceLab/opc-skills/tree/main/skills/domain-hunter) - Domain discovery + checks.
- [`marketing-psychology`](https://github.com/search?q=marketing-psychology&type=repositories) - Copy/conversion heuristics.
- [`programmatic-seo`](https://github.com/search?q=programmatic-seo&type=repositories) - Scale SEO pages.
- [`social-content`](https://github.com/search?q=social-content&type=repositories) - Platform-aware content rewriting.

> **[查看该分类完整列表 →](categories/content-growth.md)**
</details>

<a id="media-generation"></a>
<details open><summary><h3 style="display:inline">图像/音频/多媒体生成处理</h3></summary>

- [`ai-image-generation`](https://github.com/search?q=ai-image-generation&type=repositories) - Image generation/edit.
- [`openai-whisper`](https://github.com/search?q=openai-whisper&type=repositories) - Audio transcription.
- [`tts`](https://github.com/search?q=tts&type=repositories) - Speech synthesis.
- [`video-frames`](https://github.com/search?q=video-frames&type=repositories) - Video frame extraction.

> **[查看该分类完整列表 →](categories/media-generation.md)**
</details>

<a id="docs-office"></a>
<details open><summary><h3 style="display:inline">文档/办公生产力</h3></summary>

- [`docx`](https://github.com/search?q=docx&type=repositories) - Word creation/editing.
- [`pdf`](https://github.com/search?q=pdf&type=repositories) - Reliable PDF parsing/editing.
- [`pptx`](https://github.com/search?q=pptx&type=repositories) - Deck generation/editing.
- [`xlsx`](https://github.com/search?q=xlsx&type=repositories) - Spreadsheet automation.

> **[查看该分类完整列表 →](categories/docs-office.md)**
</details>

<a id="baoyu-suite"></a>
<details open><summary><h3 style="display:inline">Baoyu 系列内容产出与分发</h3></summary>


> **[查看该分类完整列表 →](categories/baoyu-suite.md)**
</details>

<a id="other-integrations"></a>
<details open><summary><h3 style="display:inline">其他集成能力</h3></summary>

- [`apple-calendar`](https://github.com/search?q=apple-calendar&type=repositories) - Calendar search/create.
- [`apple-notes`](https://github.com/search?q=apple-notes&type=repositories) - Mac local notes integration.
- [`apple-reminders`](https://github.com/search?q=apple-reminders&type=repositories) - Reminder management.
- [`weather`](https://github.com/search?q=weather&type=repositories) - Weather context.

> **[查看该分类完整列表 →](categories/other-integrations.md)**
</details>

<a id="default-tier-low"></a>
<details open><summary><h3 style="display:inline">默认 Skills 低档</h3></summary>

- Skills count: `67`
- JSON: [`tiers/low.json`](tiers/low.json)
- Manual: [`docs/tiers/low.md`](docs/tiers/low.md)

- `agent-browser` - Headless browser automation CLI for AI agents.
- `agentmail` - Give AI agents their own email inboxes using the AgentMail API.
- `agentmail-cli` - Send and receive emails programmatically using the AgentMail CLI.
- `agentmail-mcp` - AgentMail MCP server for email tools in AI assistants.
- `agentmail-toolkit` - Add email capabilities to AI agents using popular frameworks.
- `ai-image-generation` - Generate AI images with GPT-Image-2, FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.
- `akshare-stock` - A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。
- `android-native-dev` - Android native application development and UI design guide.
- `brainstorming` - Use before creative feature, component, behavior, or product design work.
- `buddy-sings` - Use when user wants their Claude Code pet (/buddy) to sing a song.
- `capability-evolver` - A self-evolution engine for AI agents.
- `chrome-devtools-mcp` - Chrome DevTools MCP — Google's official browser automation and testing server.
- `content-strategy` - When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover.
- `data-analyst` - Data visualization, report generation, SQL queries, and spreadsheet automation.
- `docx` - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction.
- `finance-data` - Comprehensive financial data retrieval from OpenBB MCP and AKShare API.
- `find-skills` - Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can.
- `flutter-dev` - Flutter cross-platform development guide covering widget patterns, Riverpod/Bloc state management, GoRouter navigation, performance optimization, and platform-specific implementations.
- `frontend-dev` - Use when building or improving high-quality frontend pages, components, dashboards, or apps.
- `fullstack-dev` - Full-stack backend architecture and frontend-backend integration guide.
- `gif-sticker-maker` - Convert photos (people, pets, objects, logos) into 4 animated GIF stickers with captions.
- `github` - Interact with GitHub using the `gh` CLI.
- `inference-skills` - Inference Skills Hub（上游: inference-sh/skills）- 用于索引与选择 inference-sh 的工具型技能。
- `ios-application-dev` - Use for iOS development, signing, TestFlight, App Store, privacy, or China-region release tasks.
- `lark-calendar` - Create, update, and delete calendar events and tasks in Lark (Feishu).
- `marketingskills` - Marketing Skills Hub（上游: coreyhaines31/marketingskills）- 用于索引与选择营销类子技能（如 content-strategy、social-content）。
- `mcp-builder` - Use when building MCP servers or tools for external APIs and services.
- `media-downloader` - |-
- `minimax-docx` - Professional DOCX document creation, editing, and formatting using OpenXML SDK (.
- `minimax-image-understanding` - Analyze images using AI with the understand_image tool (priority)
- `minimax-multimodal-toolkit` - Use mmx to generate text, images, video, speech, and music via the MiniMax AI platform.
- `minimax-music-gen` - Use when user wants to generate music, songs, or audio tracks.
- `minimax-music-playlist` - Generate personalized music playlists by analyzing the user's music taste and generation feedback history.
- `minimax-pdf` - Use this skill when visual quality and design identity matter for a PDF.
- `minimax-web-search` - 使用 MiniMax MCP 进行网络搜索。触发条件：(1) 用户要求进行网络搜索、在线搜索、查找信息 (2) 需要查询最新资讯、新闻、资料 (3) 使用 MiniMax 的 web_search 功能
- `minimax-xlsx` - Open, create, read, analyze, edit, or validate Excel/spreadsheet files (.
- `model-usage` - Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current (most recent) model or a full model breakdown.
- `multi-search-engine` - Multi search engine integration with 16 engines (7 CN + 9 Global).
- `nano-pdf` - Edit PDFs with natural-language instructions using the nano-pdf CLI.
- `news-radar` - Comprehensive news aggregation from TrendRadar MCP server with focus on high-frequency international data sources.
- `notebooklm-skill` - Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.
- `openclaw-cron-setup` - OpenClaw Gateway 内置定时任务调度器。
- `pdf` - Use when extracting, creating, merging, splitting, filling, or analyzing PDF files.
- `pptx` - Presentation creation, editing, and analysis.
- `pptx-generator` - Generate, edit, and read PowerPoint presentations.
- `proactive-agent` - Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.
- `react-native-dev` - React Native and Expo development guide covering components, styling, animations, navigation, state management, forms, networking, performance optimization, testing, native capabilities, and engineering (project structur
- `reflection` - Learns when to stop and review.
- `self-improving-agent-cn` - AI自我改进与记忆系统 - 解决'同类错误反复犯、用户纠正不长记性'的痛点。
- `shader-dev` - Comprehensive GLSL shader techniques for creating stunning visual effects — ray marching, SDF modeling, fluid simulation, particle systems, procedural generation, lighting, post-processing, and more.
- `shell` - Use shell commands for file operations, scripts, process management, diagnostics, and automation.
- `skill-creator` - Guide for creating effective skills.
- `skill-security-auditor` - Command-line security analyzer for ClawHub skills.
- `social-content` - When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms.
- `stock-monitor-skill` - 全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。
- `subagent-driven-development` - Use when executing implementation plans with independent subagent tasks.
- `task` - Tasker docstore task management via tool-dispatch.
- `tavily-search` - Search the web using Tavily's LLM-optimized search API.
- `todo` - This skill provides instructions for interacting with Todoist using the td CLI tool.
- `url-to-markdown` - Fetch any URL and convert to markdown using Chrome CDP.
- `using-superpowers` - Use when starting any conversation to check and apply relevant skills.
- `verification-before-completion` - Use before claiming work is complete, fixed, or passing.
- `vision-analysis` - Analyze, describe, and extract information from images using the MiniMax vision MCP tool.
- `weather` - Get current weather and forecasts (no API key required).
- `web-search` - This skill should be used when users need to search the web for information, find current content, look up news articles, search for images, or find videos.
- `writing-skills` - Use when creating, editing, or verifying Codex skills.
- `xlsx` - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization.

</details>

<a id="default-tier-medium"></a>
<details open><summary><h3 style="display:inline">默认 Skills 中档</h3></summary>

- Skills count: `74`
- JSON: [`tiers/medium.json`](tiers/medium.json)
- Manual: [`docs/tiers/medium.md`](docs/tiers/medium.md)

- `agent-browser` - Headless browser automation CLI for AI agents.
- `agentmail` - Give AI agents their own email inboxes using the AgentMail API.
- `agentmail-cli` - Send and receive emails programmatically using the AgentMail CLI.
- `agentmail-mcp` - AgentMail MCP server for email tools in AI assistants.
- `agentmail-toolkit` - Add email capabilities to AI agents using popular frameworks.
- `ai-image-generation` - Generate AI images with GPT-Image-2, FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.
- `akshare-stock` - A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。
- `android-native-dev` - Android native application development and UI design guide.
- `animation` - Generate CSS and SVG animation code snippets using bash and Python.
- `brainstorming` - Use before creative feature, component, behavior, or product design work.
- `buddy-sings` - Use when user wants their Claude Code pet (/buddy) to sing a song.
- `capability-evolver` - A self-evolution engine for AI agents.
- `chrome-devtools-mcp` - Chrome DevTools MCP — Google's official browser automation and testing server.
- `content-strategy` - When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover.
- `data-analyst` - Data visualization, report generation, SQL queries, and spreadsheet automation.
- `docx` - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction.
- `finance-data` - Comprehensive financial data retrieval from OpenBB MCP and AKShare API.
- `find-skills` - Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can.
- `flutter-dev` - Flutter cross-platform development guide covering widget patterns, Riverpod/Bloc state management, GoRouter navigation, performance optimization, and platform-specific implementations.
- `frontend-dev` - Use when building or improving high-quality frontend pages, components, dashboards, or apps.
- `fullstack-dev` - Full-stack backend architecture and frontend-backend integration guide.
- `gemini-image-service` - 使用 Gemini 第三方服务生成图片。读取 GEMINI_API_KEY/GEMINI_BASE_URL/GEMINI_IMAGE_MODEL。
- `gif-sticker-maker` - Convert photos (people, pets, objects, logos) into 4 animated GIF stickers with captions.
- `github` - Interact with GitHub using the `gh` CLI.
- `inference-skills` - Inference Skills Hub（上游: inference-sh/skills）- 用于索引与选择 inference-sh 的工具型技能。
- `ios-application-dev` - Use for iOS development, signing, TestFlight, App Store, privacy, or China-region release tasks.
- `lark-calendar` - Create, update, and delete calendar events and tasks in Lark (Feishu).
- `marketingskills` - Marketing Skills Hub（上游: coreyhaines31/marketingskills）- 用于索引与选择营销类子技能（如 content-strategy、social-content）。
- `mcp-builder` - Use when building MCP servers or tools for external APIs and services.
- `media-downloader` - |-
- `minimax-docx` - Professional DOCX document creation, editing, and formatting using OpenXML SDK (.
- `minimax-image-understanding` - Analyze images using AI with the understand_image tool (priority)
- `minimax-multimodal-toolkit` - Use mmx to generate text, images, video, speech, and music via the MiniMax AI platform.
- `minimax-music-gen` - Use when user wants to generate music, songs, or audio tracks.
- `minimax-music-playlist` - Generate personalized music playlists by analyzing the user's music taste and generation feedback history.
- `minimax-pdf` - Use this skill when visual quality and design identity matter for a PDF.
- `minimax-web-search` - 使用 MiniMax MCP 进行网络搜索。触发条件：(1) 用户要求进行网络搜索、在线搜索、查找信息 (2) 需要查询最新资讯、新闻、资料 (3) 使用 MiniMax 的 web_search 功能
- `minimax-xlsx` - Open, create, read, analyze, edit, or validate Excel/spreadsheet files (.
- `model-usage` - Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current (most recent) model or a full model breakdown.
- `multi-search-engine` - Multi search engine integration with 16 engines (7 CN + 9 Global).
- `nano-pdf` - Edit PDFs with natural-language instructions using the nano-pdf CLI.
- `news-radar` - Comprehensive news aggregation from TrendRadar MCP server with focus on high-frequency international data sources.
- `notebooklm-skill` - Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.
- `openclaw-cron-setup` - OpenClaw Gateway 内置定时任务调度器。
- `oracle` - Use the @steipete/oracle CLI to bundle a prompt plus the right files and get a second-model review (API or browser) for debugging, refactors, design checks, or cross-validation.
- `paperless-docs` - Manage documents in Paperless-ngx - search, upload, tag, and retrieve.
- `paperless-ngx-tools` - Manage documents in Paperless-ngx - search, upload, tag, and retrieve.
- `pdf` - Use when extracting, creating, merging, splitting, filling, or analyzing PDF files.
- `planning-with-files` - Use for complex multi-step tasks that need file-based plans and progress tracking.
- `pptx` - Presentation creation, editing, and analysis.
- `pptx-generator` - Generate, edit, and read PowerPoint presentations.
- `proactive-agent` - Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.
- `react-native-dev` - React Native and Expo development guide covering components, styling, animations, navigation, state management, forms, networking, performance optimization, testing, native capabilities, and engineering (project structur
- `reflection` - Learns when to stop and review.
- `self-improving-agent-cn` - AI自我改进与记忆系统 - 解决'同类错误反复犯、用户纠正不长记性'的痛点。
- `shader-dev` - Comprehensive GLSL shader techniques for creating stunning visual effects — ray marching, SDF modeling, fluid simulation, particle systems, procedural generation, lighting, post-processing, and more.
- `shell` - Use shell commands for file operations, scripts, process management, diagnostics, and automation.
- `skill-creator` - Guide for creating effective skills.
- `skill-security-auditor` - Command-line security analyzer for ClawHub skills.
- `social-content` - When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms.
- `stock-monitor-skill` - 全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。
- `subagent-driven-development` - Use when executing implementation plans with independent subagent tasks.
- `task` - Tasker docstore task management via tool-dispatch.
- `tavily-search` - Search the web using Tavily's LLM-optimized search API.
- `todo` - This skill provides instructions for interacting with Todoist using the td CLI tool.
- `url-to-markdown` - Fetch any URL and convert to markdown using Chrome CDP.
- `using-superpowers` - Use when starting any conversation to check and apply relevant skills.
- `verification-before-completion` - Use before claiming work is complete, fixed, or passing.
- `vision-analysis` - Analyze, describe, and extract information from images using the MiniMax vision MCP tool.
- `weather` - Get current weather and forecasts (no API key required).
- `web-search` - This skill should be used when users need to search the web for information, find current content, look up news articles, search for images, or find videos.
- `writing-plans` - Use when writing implementation plans from specs before editing code.
- `writing-skills` - Use when creating, editing, or verifying Codex skills.
- `xlsx` - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization.

</details>

<a id="default-tier-high"></a>
<details open><summary><h3 style="display:inline">默认 Skills 高档</h3></summary>

- Skills count: `179`
- JSON: [`tiers/high.json`](tiers/high.json)
- Manual: [`docs/tiers/high.md`](docs/tiers/high.md)

- `agent-browser` - Headless browser automation CLI for AI agents.
- `agentmail` - Give AI agents their own email inboxes using the AgentMail API.
- `agentmail-cli` - Send and receive emails programmatically using the AgentMail CLI.
- `agentmail-mcp` - AgentMail MCP server for email tools in AI assistants.
- `agentmail-toolkit` - Add email capabilities to AI agents using popular frameworks.
- `ai-image-generation` - Generate AI images with GPT-Image-2, FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.
- `akshare-stock` - A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。
- `alphaear-deepear-lite` - Fetch the latest financial signals and transmission-chain analyses from DeepEar Lite.
- `alphaear-logic-visualizer` - Create visualize finance logic diagrams (e.
- `alphaear-news` - Fetch hot finance news, unified trends, and prediction financial market data.
- `alphaear-predictor` - Market prediction skill using Kronos.
- `alphaear-reporter` - Plan, write, and edit professional financial reports; generate finance chart configurations.
- `alphaear-search` - Perform finance web searches and local context searches.
- `alphaear-sentiment` - Analyze finance text sentiment using FinBERT or LLM.
- `alphaear-signal-tracker` - Track finance investment signal evolution and update logic based on new finance market information.
- `alphaear-stock` - Search A-Share/HK/US finance stock tickers and retrieve finance stock price history.
- `android-native-dev` - Android native application development and UI design guide.
- `animation` - Generate CSS and SVG animation code snippets using bash and Python.
- `backtest-expert` - Expert guidance for systematic backtesting of trading strategies.
- `baoyu-article-illustrator` - Use when adding article illustrations or visual aids to markdown or long-form writing.
- `baoyu-comic` - Knowledge comic creator supporting multiple art styles and tones.
- `baoyu-compress-image` - Compresses images to WebP (default) or PNG with automatic tool selection.
- `baoyu-cover-image` - Use when generating article cover images in cinematic, widescreen, or square formats.
- `baoyu-danger-gemini-web` - Generates images and text via reverse-engineered Gemini Web API.
- `baoyu-danger-x-to-markdown` - Converts X (Twitter) tweets and articles to markdown with YAML front matter.
- `baoyu-format-markdown` - Use when formatting plain text or markdown articles with headings, summaries, lists, and polish.
- `baoyu-image-gen` - [Deprecated: use baoyu-imagine] AI image generation with OpenAI, Azure OpenAI, Google, OpenRouter, DashScope, Z.
- `baoyu-infographic` - Use when turning content into professional infographics or visual summaries.
- `baoyu-markdown-to-html` - Use when converting Markdown to styled HTML, especially WeChat-compatible article HTML.
- `baoyu-post-to-wechat` - Use when posting articles or image-text content to WeChat Official Account.
- `baoyu-post-to-weibo` - Posts content to Weibo (微博).
- `baoyu-post-to-x` - Posts content and articles to X (Twitter).
- `baoyu-skills` - Baoyu 内容产出与分发技能包入口。用于在本地仓库中索引并路由 baoyu 系列子技能。
- `baoyu-slide-deck` - Generates professional slide deck images from content.
- `baoyu-translate` - Use when translating articles or documents with terminology consistency or review polish.
- `baoyu-url-to-markdown` - Fetch any URL and convert to markdown using baoyu-fetch CLI (Chrome CDP with site-specific adapters).
- `baoyu-xhs-images` - Use when creating Xiaohongshu/RedNote infographic image series from content.
- `baoyu-youtube-transcript` - Downloads YouTube video transcripts/subtitles and cover images by URL or video ID.
- `brainstorming` - Use before creative feature, component, behavior, or product design work.
- `breadth-chart-analyst` - This skill should be used when analyzing market breadth charts, specifically the S&P 500 Breadth Index (200-Day MA based) and the US Stock Market Uptrend Stock Ratio charts.
- `breakout-trade-planner` - Generate Minervini-style breakout trade plans from VCP screener output with worst-case risk calculation, portfolio heat management, and Alpaca-compatible order templates (stop-limit bracket for pre-placement, limit brack
- `buddy-sings` - Use when user wants their Claude Code pet (/buddy) to sing a song.
- `canslim-screener` - Screen US stocks using William O'Neil's CANSLIM growth stock methodology.
- `capability-evolver` - A self-evolution engine for AI agents.
- `chrome-devtools-mcp` - Chrome DevTools MCP — Google's official browser automation and testing server.
- `company-valuation` - Estimate the intrinsic value of a public company using DCF, relative (peer multiple) and sum-of-parts (SOTP) methods, then triangulate to an implied share price with upside/downside versus the current market price.
- `content-strategy` - When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover.
- `data-analyst` - Data visualization, report generation, SQL queries, and spreadsheet automation.
- `data-quality-checker` - Validate data quality in market analysis documents and blog articles before publication.
- `discord-reader` - Read Discord for financial research using opencli (read-only).
- `dividend-growth-pullback-screener` - Use this skill to find high-quality dividend growth stocks (12%+ annual dividend growth, 1.
- `docx` - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction.
- `downtrend-duration-analyzer` - Analyze historical downtrend durations and generate interactive HTML histograms showing typical correction lengths by sector and market cap.
- `dual-axis-skill-reviewer` - Review skills in any project using a dual-axis method: (1) deterministic code-based checks (structure, scripts, tests, execution safety) and (2) LLM deep review findings.
- `earnings-calendar` - This skill retrieves upcoming earnings announcements for US stocks using the Financial Modeling Prep (FMP) API.
- `earnings-preview` - Generate a pre-earnings briefing for any stock using Yahoo Finance data.
- `earnings-recap` - Generate a post-earnings analysis for any stock using Yahoo Finance data.
- `earnings-trade-analyzer` - Analyze recent post-earnings stocks using a 5-factor scoring system (Gap Size, Pre-Earnings Trend, Volume Trend, MA200 Position, MA50 Position).
- `economic-calendar-fetcher` - Fetch upcoming economic events and data releases using FMP API.
- `edge-candidate-agent` - Generate and prioritize US equity long-side edge research tickets from EOD observations, then export pipeline-ready candidate specs for trade-strategy-pipeline Phase I.
- `edge-concept-synthesizer` - Abstract detector tickets and hints into reusable edge concepts with thesis, invalidation signals, and strategy playbooks before strategy design/export.
- `edge-hint-extractor` - Extract edge hints from daily market observations and news reactions, with optional LLM ideation, and output canonical hints.
- `edge-pipeline-orchestrator` - Orchestrate the full edge research pipeline from candidate detection through strategy design, review, revision, and export.
- `edge-signal-aggregator` - Aggregate and rank signals from multiple edge-finding skills (edge-candidate-agent, theme-detector, sector-analyst, institutional-flow-tracker) into a prioritized conviction dashboard with weighted scoring, deduplication
- `edge-strategy-designer` - Convert abstract edge concepts into strategy draft variants and optional exportable ticket YAMLs for edge-candidate-agent export/validation.
- `edge-strategy-reviewer` - Critically review strategy drafts from edge-strategy-designer for edge plausibility, overfitting risk, sample size adequacy, and execution realism.
- `estimate-analysis` - Deep-dive into analyst estimates and revision trends for any stock using Yahoo Finance data.
- `etf-premium` - Calculate ETF premium/discount vs NAV via Yahoo Finance, and decompose single-day surges into NAV-driven vs structural components (gamma squeeze, dealer hedging, blocked AP arbitrage).
- `exposure-coach` - Generate a one-page Market Posture summary with net exposure ceiling, growth-vs-value bias, participation breadth, and new-entry-allowed vs cash-priority recommendation by integrating signals from breadth, regime, and fl
- `finance-data` - Comprehensive financial data retrieval from OpenBB MCP and AKShare API.
- `finance-sentiment` - Fetch structured stock sentiment across Reddit, X.
- `finance-skill-creator` - Create new skills, modify and improve existing skills, and measure skill performance.
- `find-skills` - Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can.
- `finviz-screener` - Build and open FinViz screener URLs from natural language requests.
- `flutter-dev` - Flutter cross-platform development guide covering widget patterns, Riverpod/Bloc state management, GoRouter navigation, performance optimization, and platform-specific implementations.
- `frontend-dev` - Use when building or improving high-quality frontend pages, components, dashboards, or apps.
- `ftd-detector` - Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology.
- `fullstack-dev` - Full-stack backend architecture and frontend-backend integration guide.
- `funda-data` - Fetch financial data from the Funda AI API (https://api.
- `gemini-image-service` - 使用 Gemini 第三方服务生成图片。读取 GEMINI_API_KEY/GEMINI_BASE_URL/GEMINI_IMAGE_MODEL。
- ... 99 more; see `docs/tiers/high.md`

</details>

<!-- SKILLS_INDEX:END -->

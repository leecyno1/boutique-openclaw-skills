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
- [Skills 目录（推荐在前）](#10-skills-目录推荐在前)
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

## 10) Skills 目录（推荐在前）

<!-- SKILLS_INDEX:START -->
- 推荐 skills：`41`
- OpenClaw 官方默认 skills：`58`（core `52` + extension `6`）
- 首页可查看总条目：`99`

> 默认 skills 来源：`openclaw` npm 包目录（`skills/` 与 `extensions/*/skills/`），不是本机会话导出。

## Table of Contents

| 分类 | 跳转 | 分类 | 跳转 |
|---|---|---|---|
| [Agent/自动化与能力进化](#agent-automation) (8) | [分类文件](categories/agent-automation.md) | [开发/工程与运维](#engineering-ops) (7) | [分类文件](categories/engineering-ops.md) |
| [搜索/研究/情报](#research-intel) (6) | [分类文件](categories/research-intel.md) | [设计/前端/UI](#design-ui) (3) | [分类文件](categories/design-ui.md) |
| [内容/营销/增长](#content-growth) (5) | [分类文件](categories/content-growth.md) | [图像/音频/多媒体生成处理](#media-generation) (4) | [分类文件](categories/media-generation.md) |
| [文档/办公生产力](#docs-office) (4) | [分类文件](categories/docs-office.md) | [Baoyu 系列内容产出与分发](#baoyu-suite) (0) | [分类文件](categories/baoyu-suite.md) |
| [其他集成能力](#other-integrations) (4) | [分类文件](categories/other-integrations.md) | [OpenClaw 默认 Skills（Core）](#openclaw-default-core) | [分类文件](categories/openclaw-default-core.md) |
| [OpenClaw 默认 Skills（Extensions）](#openclaw-default-extensions) | [分类文件](categories/openclaw-default-extensions.md) |  |  |

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

<a id="openclaw-default-core"></a>
<details open><summary><h3 style="display:inline">OpenClaw 默认 Skills（Core）</h3></summary>

- `1password` - Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.
- `apple-notes` - Manage Apple Notes via the `memo` CLI on macOS (create, view, edit, delete, search, move, and export notes). Use when a user asks OpenClaw to add a note, list notes, search notes, or manage note folders.
- `apple-reminders` - Manage Apple Reminders via remindctl CLI (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output.
- `bear-notes` - Create, search, and manage Bear notes via grizzly CLI.
- `blogwatcher` - Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.
- `blucli` - BluOS CLI (blu) for discovery, playback, grouping, and volume.
- `bluebubbles` - Use when you need to send or manage iMessages via BlueBubbles (recommended iMessage integration). Calls go through the generic message tool with channel="bluebubbles".
- `camsnap` - Capture frames or clips from RTSP/ONVIF cameras.
- `canvas` - No description.
- `clawhub` - Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed clawhub CLI.
- `coding-agent` - Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:"acp"), or any work in ~/clawd workspace (never spawn agents here). Requires a bash tool that supports pty:true.
- `discord` - Discord ops via the message tool (channel=discord).
- `eightctl` - Control Eight Sleep pods (status, temperature, alarms, schedules).
- `gemini` - Gemini CLI for one-shot Q&A, summaries, and generation.
- `gh-issues` - Fetch GitHub issues, spawn sub-agents to implement fixes and open PRs, then monitor and address PR review comments. Usage: /gh-issues [owner/repo] [--label bug] [--limit 5] [--milestone v1.0] [--assignee @me] [--fork user/repo] [--watch] [--interval 5] [--reviews-only] [--cron] [--dry-run] [--model glm-5] [--notify-channel -1002381931352]
- `gifgrep` - Search GIF providers with CLI/TUI, download results, and extract stills/sheets.
- `github` - GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs. NOT for: complex web UI interactions requiring manual browser flows (use browser tooling when available), bulk operations across many repos (script with gh api), or when gh auth is not configured.
- `gog` - Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
- `goplaces` - Query Google Places API (New) via the goplaces CLI for text search, place details, resolve, and reviews. Use for human-friendly place lookup or JSON output for scripts.
- `healthcheck` - Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).
- `himalaya` - CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).
- `imsg` - iMessage/SMS CLI for listing chats, history, and sending messages via Messages.app.
- `mcporter` - Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.
- `model-usage` - Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current (most recent) model or a full model breakdown. Trigger when asked for model-level usage/cost data from codexbar, or when you need a scriptable per-model summary from codexbar cost JSON.
- `nano-banana-pro` - Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).
- `nano-pdf` - Edit PDFs with natural-language instructions using the nano-pdf CLI.
- `notion` - Notion API for creating and managing pages, databases, and blocks.
- `obsidian` - Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.
- `openai-image-gen` - Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery.
- `openai-whisper` - Local speech-to-text with the Whisper CLI (no API key).
- `openai-whisper-api` - Transcribe audio via OpenAI Audio Transcriptions API (Whisper).
- `openhue` - Control Philips Hue lights and scenes via the OpenHue CLI.
- `oracle` - Best practices for using the oracle CLI (prompt + file bundling, engines, sessions, and file attachment patterns).
- `ordercli` - Foodora-only CLI for checking past orders and active order status (Deliveroo WIP).
- `peekaboo` - Capture and automate macOS UI with the Peekaboo CLI.
- `sag` - ElevenLabs text-to-speech with mac-style say UX.
- `session-logs` - Search and analyze your own session logs (older/parent conversations) using jq.
- `sherpa-onnx-tts` - Local text-to-speech via sherpa-onnx (offline, no cloud)
- `skill-creator` - Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets.
- `slack` - Use when you need to control Slack from OpenClaw via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs.
- `songsee` - Generate spectrograms and feature-panel visualizations from audio with the songsee CLI.
- `sonoscli` - Control Sonos speakers (discover/status/play/volume/group).
- `spotify-player` - Terminal Spotify playback/search via spogo (preferred) or spotify_player.
- `summarize` - Summarize or extract text/transcripts from URLs, podcasts, and local files (great fallback for “transcribe this YouTube/video”).
- `things-mac` - Manage Things 3 via the `things` CLI on macOS (add/update projects+todos via URL scheme; read/search/list from the local Things database). Use when a user asks OpenClaw to add a task to Things, list inbox/today/upcoming, search tasks, or inspect projects/areas/tags.
- `tmux` - Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
- `trello` - Manage Trello boards, lists, and cards via the Trello REST API.
- `video-frames` - Extract frames or short clips from videos using ffmpeg.
- `voice-call` - Start voice calls via the OpenClaw voice-call plugin.
- `wacli` - Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).
- `weather` - Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.
- `xurl` - A CLI tool for making authenticated requests to the X (Twitter) API. Use this skill when you need to post tweets, reply, quote, search, read posts, manage followers, send DMs, upload media, or interact with any X API v2 endpoint.

> **[查看 Core 默认 skills 全列表 →](categories/openclaw-default-core.md)**
</details>

<a id="openclaw-default-extensions"></a>
<details open><summary><h3 style="display:inline">OpenClaw 默认 Skills（Extensions）</h3></summary>

- `acpx/acp-router` - Route plain-language requests for Pi, Claude Code, Codex, OpenCode, Gemini CLI, or ACP harness work into either OpenClaw ACP runtime sessions or direct acpx-driven sessions ("telephone game" flow). For coding-agent thread requests, read this skill first, then use only `sessions_spawn` for thread creation.
- `feishu/feishu-doc` - Feishu document read/write operations. Activate when user mentions Feishu docs, cloud docs, or docx links.
- `feishu/feishu-drive` - Feishu cloud storage file management. Activate when user mentions cloud space, folders, drive.
- `feishu/feishu-perm` - Feishu permission management for documents and files. Activate when user mentions sharing, permissions, collaborators.
- `feishu/feishu-wiki` - Feishu knowledge base navigation. Activate when user mentions knowledge base, wiki, or wiki links.
- `open-prose/prose` - OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows.

> **[查看 Extension 默认 skills 全列表 →](categories/openclaw-default-extensions.md)**
</details>
<!-- SKILLS_INDEX:END -->

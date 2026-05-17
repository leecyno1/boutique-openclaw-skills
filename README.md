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

### 安装标准配置组（推荐）

标准配置组最多 30 个 skill，每个能力只安装一个评分最高且未被 Open/Hermes 预置的选择。

```bash
./scripts/install-standard-bundle.sh --dry-run
./scripts/install-standard-bundle.sh
```

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
## Registry Snapshot

- 默认 skill 去重数：`179`
- 已有原生来源或本地来源线索：`173`
- 仍需人工确认原生来源：`0`
- Open/Hermes 预置排除：`6`
- 标准配置组：`28` / `30`

> `source` 中的安装器仓库路径仅视为镜像来源；`origin.origin_url` 才是一手原生来源。缺失原生来源的 skill 最高只能获得 2★。

## 标准技能配置组（≤30，无重复能力）

安装原则：每个能力只选择一个评分最高且未被 Open/Hermes 预置的 skill，避免重复安装导致冲突或 token 浪费。

```bash
./scripts/install-standard-bundle.sh --dry-run
./scripts/install-standard-bundle.sh
```

| 能力 | 推荐 Skill | 星级 | 使用条件 | 原生来源 |
|---|---|---:|---|---|
| `agent-method` | `brainstorming` | 5★ | `direct` | [origin](https://github.com/baz-scm/agentskills/tree/main/skills/brainstorming) |
| `skill-discovery` | `find-skills` | 5★ | `direct` | [origin](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) |
| `web-search` | `multi-search-engine` | 5★ | `direct` | [origin](https://clawhub.ai/gpyAngyoujun/multi-search-engine) |
| `url-extraction` | `url-to-markdown` | 4★ | `browser-required` | [origin](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-url-to-markdown) |
| `browser-automation` | `agent-browser` | 4★ | `browser-required` | [origin](https://openclawdoc.com/docs/skills/clawhub/) |
| `code-hosting` | `github` | 4★ | `api-key` | [origin](https://github.com/github/github-mcp-server) |
| `task-tracking` | `task` | 5★ | `direct` | [origin](https://github.com/openclaw/skills/tree/main/skills/amirbrooks/task) |
| `planning` | `planning-with-files` | 5★ | `direct` | [origin](https://github.com/OthmanAdi/planning-with-files) |
| `verification` | `verification-before-completion` | 5★ | `direct` | [origin](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| `skill-authoring` | `skill-creator` | 5★ | `direct` | [origin](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| `security-review` | `skill-security-auditor` | 5★ | `direct` | [origin](https://clawhub.ai/akhmittra/skill-security-auditor) |
| `data-analysis` | `data-analyst` | 5★ | `direct` | [origin](https://github.com/openclaw/skills/blob/main/skills/oyi77/data-analyst/SKILL.md) |
| `docs` | `minimax-docx` | 4★ | `direct` | [origin](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-docx) |
| `spreadsheet` | `minimax-xlsx` | 4★ | `direct` | [origin](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-xlsx) |
| `slides` | `pptx-generator` | 4★ | `direct` | [origin](https://github.com/MiniMax-AI/skills/tree/main/skills/pptx-generator) |
| `pdf` | `nano-pdf` | 5★ | `direct` | [origin](https://github.com/steipete/clawdis/tree/main/skills/nano-pdf) |
| `frontend` | `generative-ui` | 5★ | `direct` | [origin](https://github.com/himself65/finance-skills/tree/main/plugins/ui-tools/skills/generative-ui) |
| `fullstack` | `fullstack-dev` | 3★ | `api-key` | [origin](https://github.com/MiniMax-AI/skills/tree/main/skills/fullstack-dev) |
| `mcp` | `mcp-builder` | 4★ | `mcp-required` | [origin](https://modelcontextprotocol.io/docs/getting-started/intro) |
| `media-download` | `media-downloader` | 3★ | `api-key` | [origin](https://github.com/yizhiyanhua-ai/media-downloader.git) |
| `image-generation` | `gemini-image-service` | 3★ | `api-key` | [origin](https://ai.google.dev/gemini-api/docs/image-generation) |
| `research-news` | `news-radar` | 4★ | `mcp-required` | [origin](https://github.com/airinghost/TrendRadar) |
| `finance-data` | `finance-data` | 4★ | `mcp-required` | [origin](https://github.com/OpenBB-finance/OpenBB) |
| `content-strategy` | `content-strategy` | 4★ | `direct` | [origin](https://github.com/coreyhaines31/marketingskills/tree/main/skills/content-strategy) |
| `writing` | `writing-skills` | 5★ | `direct` | [origin](https://github.com/obra/superpowers/tree/main/skills/writing-skills) |
| `automation-followup` | `proactive-agent` | 5★ | `direct` | [origin](https://clawhub.ai/halthelobster/proactive-agent) |
| `cost-observability` | `model-usage` | 5★ | `direct` | [origin](https://clawhub.ai/steipete/model-usage) |
| `weather` | `weather` | 5★ | `direct` | [origin](https://open-meteo.com/) |

## 双索引

| 索引 | 说明 | 文件 |
|---|---|---|
| 横向分级 | L1 Foundation / L2 Professional / L3 Specialist | [`docs/generated/horizontal-index.md`](docs/generated/horizontal-index.md) |
| 纵向类型 | 按用途分类，如 coding、design、finance、writing 等 | [`docs/generated/type-index.md`](docs/generated/type-index.md) |
| 使用条件 | API key、额外 tools、运行方式、风险 | [`docs/generated/dependency-index.md`](docs/generated/dependency-index.md) |
| 评分体系 | 五星评分规则和月评增强方向 | [`docs/generated/scoring-model.md`](docs/generated/scoring-model.md) |

## L1 Foundation Top Skills

| Skill | 类型 | 星级 | 原生来源 |
|---|---|---:|---|
| `brainstorming` | 核心 Agent 能力 | 5★ | [origin](https://github.com/baz-scm/agentskills/tree/main/skills/brainstorming) |
| `find-skills` | 核心 Agent 能力 | 5★ | [origin](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) |
| `model-usage` | 核心 Agent 能力 | 5★ | [origin](https://clawhub.ai/steipete/model-usage) |
| `planning-with-files` | 核心 Agent 能力 | 5★ | [origin](https://github.com/OthmanAdi/planning-with-files) |
| `skill-creator` | 核心 Agent 能力 | 5★ | [origin](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| `skill-security-auditor` | 核心 Agent 能力 | 5★ | [origin](https://clawhub.ai/akhmittra/skill-security-auditor) |
| `subagent-driven-development` | 核心 Agent 能力 | 5★ | [origin](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) |
| `task` | 核心 Agent 能力 | 5★ | [origin](https://github.com/openclaw/skills/tree/main/skills/amirbrooks/task) |
| `todo` | 核心 Agent 能力 | 5★ | [origin](https://github.com/sachaos/todoist) |
| `using-superpowers` | 核心 Agent 能力 | 5★ | [origin](https://github.com/obra/superpowers/tree/main/skills/using-superpowers) |
| `verification-before-completion` | 核心 Agent 能力 | 5★ | [origin](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| `weather` | 核心 Agent 能力 | 5★ | [origin](https://open-meteo.com/) |
| `writing-skills` | 核心 Agent 能力 | 5★ | [origin](https://github.com/obra/superpowers/tree/main/skills/writing-skills) |
| `agent-browser` | 核心 Agent 能力 | 4★ | [origin](https://openclawdoc.com/docs/skills/clawhub/) |
| `chrome-devtools-mcp` | 核心 Agent 能力 | 4★ | [origin](https://github.com/ChromeDevTools/chrome-devtools-mcp) |

## 原生来源待补清单（前 20）

这些 skill 当前只有镜像来源或缺少一手来源，月评时需要优先补齐。

| Skill | 类型 | 镜像来源 |
|---|---|---|
<!-- SKILLS_INDEX:END -->

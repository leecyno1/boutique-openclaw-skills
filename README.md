# Boutique OpenClaw Skills

![Boutique OpenClaw Skills](assets/boutique-openclaw-skills-hero.png)

![Curated](https://img.shields.io/badge/curated-boutique-gold)
![Skills](https://img.shields.io/badge/skills-179-blue)
![Origins](https://img.shields.io/badge/native%20origins-0%20missing-brightgreen)
![Standard Bundle](https://img.shields.io/badge/standard%20bundle-28%20skills-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A curated, source-audited skill registry for building capable OpenClaw, Open, and Hermes agents without duplicate tools or noisy installs.

## Quick Start

Install the recommended no-duplicate bundle:

```bash
./scripts/install-standard-bundle.sh --dry-run
./scripts/install-standard-bundle.sh
```

Or install a tier:

```bash
./scripts/install-tier.sh low
./scripts/install-tier.sh medium
./scripts/install-tier.sh high
```

## At A Glance

| Metric | Value |
|---|---:|
| Curated skills | 179 |
| Native sources verified or referenced | 173 |
| Agent preset exclusions | 6 |
| Missing native origins | 0 |
| Standard bundle size | 28 / 30 |

## Standard Bundle

The standard bundle keeps one best skill per capability and excludes skills already built into Open or Hermes.

| Capability | Skill | Stars | Use |
|---|---|---:|---|
| `agent-method` | `brainstorming` | 5★ | `direct` |
| `skill-discovery` | `find-skills` | 5★ | `direct` |
| `web-search` | `multi-search-engine` | 5★ | `direct` |
| `url-extraction` | `url-to-markdown` | 4★ | `browser-required` |
| `browser-automation` | `agent-browser` | 4★ | `browser-required` |
| `code-hosting` | `github` | 4★ | `api-key` |
| `task-tracking` | `task` | 5★ | `direct` |
| `planning` | `planning-with-files` | 5★ | `direct` |
| `verification` | `verification-before-completion` | 5★ | `direct` |
| `skill-authoring` | `skill-creator` | 5★ | `direct` |
| `security-review` | `skill-security-auditor` | 5★ | `direct` |
| `data-analysis` | `data-analyst` | 5★ | `direct` |
| `docs` | `minimax-docx` | 4★ | `direct` |
| `spreadsheet` | `minimax-xlsx` | 4★ | `direct` |
| `slides` | `pptx-generator` | 4★ | `direct` |
| `pdf` | `nano-pdf` | 5★ | `direct` |
| `frontend` | `generative-ui` | 5★ | `direct` |
| `fullstack` | `fullstack-dev` | 3★ | `api-key` |
| `mcp` | `mcp-builder` | 4★ | `mcp-required` |
| `media-download` | `media-downloader` | 3★ | `api-key` |
| `image-generation` | `gemini-image-service` | 3★ | `api-key` |
| `research-news` | `news-radar` | 4★ | `mcp-required` |
| `finance-data` | `finance-data` | 4★ | `mcp-required` |
| `content-strategy` | `content-strategy` | 4★ | `direct` |
| `writing` | `writing-skills` | 5★ | `direct` |
| `automation-followup` | `proactive-agent` | 5★ | `direct` |
| `cost-observability` | `model-usage` | 5★ | `direct` |
| `weather` | `weather` | 5★ | `direct` |

## All Skills

| Skill | Tier | Type | Stars | Use | Origin |
|---|---|---|---:|---|---|
| `capability-evolver` | `L3 Specialist` | `agent-orchestration` | 4★ | `direct` | [Source](https://mcp.directory/skills/details/1368/capability-evolver) |
| `openclaw-cron-setup` | `L2 Professional` | `agent-orchestration` | 4★ | `browser-required` | [Source](https://clawhub.ai/skills/openclaw-cron-setup) |
| `self-improving-agent-cn` | `L2 Professional` | `agent-orchestration` | 5★ | `direct` | [Source](https://clawhub.ai/zhengxinjipai/self-improving-agent-cn) |
| `notebooklm-skill` | `L2 Professional` | `browser-automation` | 3★ | `api-key` | [Source](https://github.com/PleasePrompto/notebooklm-skill) |
| `oracle` | `L3 Specialist` | `browser-automation` | 3★ | `api-key` | [Source](https://github.com/steipete/oracle) |
| `agentmail-mcp` | `L2 Professional` | `coding-devtools` | 4★ | `api-key` | [Source](https://github.com/agentmail-to/agentmail-mcp) |
| `android-native-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/android-native-dev) |
| `backtest-expert` | `L2 Professional` | `coding-devtools` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/backtest-expert) |
| `baoyu-image-gen` | `L2 Professional` | `coding-devtools` | 4★ | `api-key` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-image-gen) |
| `flutter-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/flutter-dev) |
| `frontend-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/frontend-dev) |
| `fullstack-dev` | `L2 Professional` | `coding-devtools` | 3★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/fullstack-dev) |
| `ios-application-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/ios-application-dev) |
| `react-native-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/react-native-dev) |
| `shader-dev` | `L2 Professional` | `coding-devtools` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/shader-dev) |
| `estimate-analysis` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `hormuz-strait` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `inference-skills` | `L3 Specialist` | `commerce-ops` | 3★ | `api-key` | [Source](https://github.com/inference-sh/skills) |
| `scenario-analyzer` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills) |
| `sepa-strategy` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `skill-idea-miner` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/skill-idea-miner) |
| `startup-analysis` | `L3 Specialist` | `commerce-ops` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/startup-tools/skills/startup-analysis) |
| `agent-browser` | `L1 Foundation` | `core-agent` | 4★ | `browser-required` | [Source](https://openclawdoc.com/docs/skills/clawhub/) |
| `brainstorming` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/baz-scm/agentskills/tree/main/skills/brainstorming) |
| `chrome-devtools-mcp` | `L1 Foundation` | `core-agent` | 4★ | `mcp-required` | [Source](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| `find-skills` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) |
| `github` | `L1 Foundation` | `core-agent` | 4★ | `api-key` | [Source](https://github.com/github/github-mcp-server) |
| `mcp-builder` | `L1 Foundation` | `core-agent` | 4★ | `mcp-required` | [Source](https://modelcontextprotocol.io/docs/getting-started/intro) |
| `model-usage` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://clawhub.ai/steipete/model-usage) |
| `planning-with-files` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/OthmanAdi/planning-with-files) |
| `shell` | `L1 Foundation` | `core-agent` | 1★ | `direct` | Preset |
| `skill-creator` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| `skill-security-auditor` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://clawhub.ai/akhmittra/skill-security-auditor) |
| `subagent-driven-development` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) |
| `task` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/openclaw/skills/tree/main/skills/amirbrooks/task) |
| `todo` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/sachaos/todoist) |
| `url-to-markdown` | `L1 Foundation` | `core-agent` | 4★ | `browser-required` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-url-to-markdown) |
| `using-superpowers` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/obra/superpowers/tree/main/skills/using-superpowers) |
| `verification-before-completion` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| `weather` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://open-meteo.com/) |
| `web-search` | `L1 Foundation` | `core-agent` | 1★ | `browser-required` | Preset |
| `writing-skills` | `L1 Foundation` | `core-agent` | 5★ | `direct` | [Source](https://github.com/obra/superpowers/tree/main/skills/writing-skills) |
| `baoyu-youtube-transcript` | `L2 Professional` | `data-analysis` | 5★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-youtube-transcript) |
| `data-analyst` | `L2 Professional` | `data-analysis` | 5★ | `direct` | [Source](https://github.com/openclaw/skills/blob/main/skills/oyi77/data-analyst/SKILL.md) |
| `dual-axis-skill-reviewer` | `L2 Professional` | `data-analysis` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/dual-axis-skill-reviewer) |
| `edge-signal-aggregator` | `L2 Professional` | `data-analysis` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-signal-aggregator) |
| `minimax-xlsx` | `L2 Professional` | `data-analysis` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-xlsx) |
| `skill-integration-tester` | `L2 Professional` | `data-analysis` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/skill-integration-tester) |
| `xlsx` | `L2 Professional` | `data-analysis` | 1★ | `direct` | Preset |
| `agentmail` | `L2 Professional` | `design-ui` | 3★ | `api-key` | [Source](https://github.com/agentmail-to/agentmail-skills) |
| `agentmail-toolkit` | `L2 Professional` | `design-ui` | 4★ | `api-key` | [Source](https://github.com/agentmail-to/agentmail-toolkit) |
| `animation` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/bytesagain/ai-skills) |
| `baoyu-danger-x-to-markdown` | `L2 Professional` | `design-ui` | 2★ | `api-key` | [Source](https://github.com/JimLiu/baoyu-skills#baoyu-danger-x-to-markdown) |
| `edge-concept-synthesizer` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-concept-synthesizer) |
| `edge-strategy-designer` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-strategy-designer) |
| `generative-ui` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/ui-tools/skills/generative-ui) |
| `skill-designer` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/skill-designer) |
| `strategy-pivot-designer` | `L2 Professional` | `design-ui` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/strategy-pivot-designer) |
| `docx` | `L2 Professional` | `docs-office` | 1★ | `direct` | Preset |
| `lark-calendar` | `L2 Professional` | `docs-office` | 4★ | `api-key` | [Source](https://github.com/larksuite/oapi-sdk-nodejs) |
| `minimax-docx` | `L2 Professional` | `docs-office` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-docx) |
| `minimax-pdf` | `L2 Professional` | `docs-office` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-pdf) |
| `nano-pdf` | `L2 Professional` | `docs-office` | 5★ | `direct` | [Source](https://github.com/steipete/clawdis/tree/main/skills/nano-pdf) |
| `pdf` | `L2 Professional` | `docs-office` | 1★ | `direct` | Preset |
| `pptx` | `L2 Professional` | `docs-office` | 1★ | `direct` | Preset |
| `pptx-generator` | `L2 Professional` | `docs-office` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/pptx-generator) |
| `social-content` | `L2 Professional` | `docs-office` | 4★ | `direct` | [Source](https://github.com/coreyhaines31/marketingskills/tree/main/skills/social-content) |
| `ai-image-generation` | `L2 Professional` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/inference-sh/skills/tree/main/tools/image/ai-image-generation) |
| `akshare-stock` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://clawhub.ai/skills/new-akshare-stock) |
| `alphaear-deepear-lite` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-deepear-lite) |
| `alphaear-logic-visualizer` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-logic-visualizer) |
| `alphaear-news` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-news) |
| `alphaear-predictor` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-predictor) |
| `alphaear-reporter` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-reporter) |
| `alphaear-search` | `L3 Specialist` | `finance-trading` | 3★ | `browser-required` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-search) |
| `alphaear-sentiment` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-sentiment) |
| `alphaear-signal-tracker` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-signal-tracker) |
| `alphaear-stock` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/RKiding/Awesome-finance-skills/tree/main/skills/alphaear-stock) |
| `breadth-chart-analyst` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/breadth-chart-analyst) |
| `breakout-trade-planner` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/breakout-trade-planner) |
| `canslim-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/canslim-screener) |
| `company-valuation` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `content-strategy` | `L2 Professional` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/coreyhaines31/marketingskills/tree/main/skills/content-strategy) |
| `data-quality-checker` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/data-quality-checker) |
| `dividend-growth-pullback-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/dividend-growth-pullback-screener) |
| `downtrend-duration-analyzer` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/downtrend-duration-analyzer) |
| `earnings-calendar` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/earnings-calendar) |
| `earnings-preview` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills) |
| `earnings-recap` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills) |
| `earnings-trade-analyzer` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/earnings-trade-analyzer) |
| `economic-calendar-fetcher` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/economic-calendar-fetcher) |
| `edge-candidate-agent` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-candidate-agent) |
| `edge-hint-extractor` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-hint-extractor) |
| `etf-premium` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills) |
| `exposure-coach` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/exposure-coach) |
| `finance-data` | `L2 Professional` | `finance-trading` | 4★ | `mcp-required` | [Source](https://github.com/OpenBB-finance/OpenBB) |
| `finance-sentiment` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/data-providers/skills/finance-sentiment) |
| `finance-skill-creator` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/skill-creator/skills/finance-skill-creator) |
| `finviz-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/finviz-screener) |
| `ftd-detector` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/ftd-detector) |
| `funda-data` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/data-providers/skills/funda-data) |
| `ibd-distribution-day-monitor` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/ibd-distribution-day-monitor) |
| `institutional-flow-tracker` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/institutional-flow-tracker) |
| `kanchi-dividend-review-monitor` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/kanchi-dividend-review-monitor) |
| `kanchi-dividend-sop` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/kanchi-dividend-sop) |
| `kanchi-dividend-us-tax-accounting` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/kanchi-dividend-us-tax-accounting) |
| `macro-regime-detector` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/macro-regime-detector) |
| `market-breadth-analyzer` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/market-breadth-analyzer) |
| `market-environment-analysis` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/market-environment-analysis) |
| `market-news-analyst` | `L3 Specialist` | `finance-trading` | 3★ | `browser-required` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/market-news-analyst) |
| `market-top-detector` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/market-top-detector) |
| `marketingskills` | `L3 Specialist` | `finance-trading` | 3★ | `direct` | [Source](https://github.com/coreyhaines31/marketingskills) |
| `options-payoff` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `options-strategy-advisor` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/options-strategy-advisor) |
| `pair-trade-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/pair-trade-screener) |
| `parabolic-short-trade-planner` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/parabolic-short-trade-planner) |
| `pead-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/pead-screener) |
| `portfolio-manager` | `L3 Specialist` | `finance-trading` | 3★ | `mcp-required` | [Source](https://mcp.directory/skills/portfolio-manager) |
| `position-sizer` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/position-sizer) |
| `saas-valuation-compression` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills) |
| `sector-analyst` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/sector-analyst) |
| `signal-postmortem` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/signal-postmortem) |
| `stanley-druckenmiller-investment` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/stanley-druckenmiller-investment) |
| `stock-correlation` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/market-analysis/skills/stock-correlation) |
| `stock-liquidity` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/market-analysis/skills/stock-liquidity) |
| `stock-monitor-skill` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://clawhub.ai/THIRTYFANG/stock-monitor-skill) |
| `technical-analyst` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/technical-analyst) |
| `theme-detector` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/theme-detector) |
| `trade-hypothesis-ideator` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/trade-hypothesis-ideator) |
| `trader-memory-core` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/trader-memory-core) |
| `uptrend-analyzer` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/uptrend-analyzer) |
| `us-market-bubble-detector` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/us-market-bubble-detector) |
| `us-stock-analysis` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/us-stock-analysis) |
| `value-dividend-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/value-dividend-screener) |
| `vcp-screener` | `L3 Specialist` | `finance-trading` | 3★ | `api-key` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/vcp-screener) |
| `yfinance-data` | `L3 Specialist` | `finance-trading` | 4★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/market-analysis/skills/yfinance-data) |
| `baoyu-comic` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-comic) |
| `baoyu-compress-image` | `L3 Specialist` | `media-generation` | 3★ | `browser-required` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-compress-image) |
| `baoyu-cover-image` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-cover-image) |
| `baoyu-danger-gemini-web` | `L3 Specialist` | `media-generation` | 2★ | `api-key` | [Source](https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web) |
| `baoyu-post-to-wechat` | `L3 Specialist` | `media-generation` | 3★ | `api-key` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-post-to-wechat) |
| `baoyu-post-to-weibo` | `L3 Specialist` | `media-generation` | 3★ | `browser-required` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-post-to-weibo) |
| `baoyu-post-to-x` | `L3 Specialist` | `media-generation` | 3★ | `browser-required` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-post-to-x) |
| `baoyu-slide-deck` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-slide-deck) |
| `baoyu-xhs-images` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-xhs-images) |
| `buddy-sings` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/buddy-sings) |
| `gemini-image-service` | `L3 Specialist` | `media-generation` | 3★ | `api-key` | [Source](https://ai.google.dev/gemini-api/docs/image-generation) |
| `gif-sticker-maker` | `L3 Specialist` | `media-generation` | 3★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/gif-sticker-maker) |
| `media-downloader` | `L2 Professional` | `media-generation` | 3★ | `api-key` | [Source](https://github.com/yizhiyanhua-ai/media-downloader.git) |
| `minimax-image-understanding` | `L3 Specialist` | `media-generation` | 3★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-image-understanding) |
| `minimax-music-gen` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-gen) |
| `minimax-music-playlist` | `L3 Specialist` | `media-generation` | 4★ | `direct` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-playlist) |
| `reflection` | `L2 Professional` | `media-generation` | 5★ | `direct` | [Source](https://playbooks.com/skills/openclaw/skills/reflection) |
| `vision-analysis` | `L2 Professional` | `media-generation` | 3★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/vision-analysis) |
| `proactive-agent` | `L2 Professional` | `productivity-pkm` | 5★ | `direct` | [Source](https://clawhub.ai/halthelobster/proactive-agent) |
| `baoyu-url-to-markdown` | `L2 Professional` | `search-research` | 4★ | `browser-required` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-url-to-markdown) |
| `discord-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/discord-reader) |
| `edge-pipeline-orchestrator` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-pipeline-orchestrator) |
| `linkedin-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/linkedin-reader) |
| `minimax-multimodal-toolkit` | `L2 Professional` | `search-research` | 3★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-multimodal-toolkit) |
| `minimax-web-search` | `L2 Professional` | `search-research` | 4★ | `api-key` | [Source](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-web-search) |
| `multi-search-engine` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://clawhub.ai/gpyAngyoujun/multi-search-engine) |
| `news-radar` | `L2 Professional` | `search-research` | 4★ | `mcp-required` | [Source](https://github.com/airinghost/TrendRadar) |
| `opencli-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/opencli-reader) |
| `paperless-docs` | `L2 Professional` | `search-research` | 4★ | `api-key` | [Source](https://github.com/paperless-ngx/paperless-ngx) |
| `paperless-ngx-tools` | `L2 Professional` | `search-research` | 4★ | `api-key` | [Source](https://github.com/paperless-ngx/paperless-ngx) |
| `tavily-search` | `L2 Professional` | `search-research` | 4★ | `api-key` | [Source](https://github.com/tavily-ai/tavily-python) |
| `telegram-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/telegram-reader) |
| `twitter-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/twitter-reader) |
| `yc-reader` | `L2 Professional` | `search-research` | 5★ | `direct` | [Source](https://github.com/himself65/finance-skills/tree/main/plugins/social-readers/skills/yc-reader) |
| `edge-strategy-reviewer` | `L3 Specialist` | `security-audit` | 4★ | `direct` | [Source](https://github.com/tradermonty/claude-trading-skills/tree/main/skills/edge-strategy-reviewer) |
| `agentmail-cli` | `L3 Specialist` | `writing-content` | 3★ | `api-key` | [Source](https://github.com/agentmail-to/agentmail-cli) |
| `baoyu-article-illustrator` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-article-illustrator) |
| `baoyu-format-markdown` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-format-markdown) |
| `baoyu-infographic` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-infographic) |
| `baoyu-markdown-to-html` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-markdown-to-html) |
| `baoyu-skills` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills) |
| `baoyu-translate` | `L3 Specialist` | `writing-content` | 4★ | `direct` | [Source](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-translate) |
| `writing-plans` | `L2 Professional` | `writing-content` | 5★ | `direct` | [Source](https://skills.sh/obra/superpowers/writing-plans) |

## Indexes

| Document | What it shows |
|---|---|
| [Horizontal index](docs/generated/horizontal-index.md) | L1 Foundation, L2 Professional, L3 Specialist |
| [Type index](docs/generated/type-index.md) | Coding, design, finance, writing, research, media, docs, and more |
| [Dependency index](docs/generated/dependency-index.md) | API keys, tools, runtime mode, and risk |
| [Scoring model](docs/generated/scoring-model.md) | How star ratings are calculated |
| [Update and audit SOP](docs/UPDATE_AND_AUDIT.md) | Monthly review process and risk gates |

## Curation Rules

- Every active skill must have a native upstream source; mirrors and copied installer paths are not treated as origins.
- The standard bundle avoids duplicate capabilities by using conflict groups such as `web-search`, `document-pdf`, `email-agent`, and `finance-data`.
- Open and Hermes preset skills are excluded from bundle installs because the target agent already provides them.
- Monthly automation regenerates the registry, indexes, README, standard bundle, and audit reports.

## Repository Map

| Path | Purpose |
|---|---|
| `skills/default/` | Local skill sources |
| `catalog/skills.enriched.json` | Full machine-readable registry |
| `catalog/standard-bundle.json` | Recommended no-duplicate install set |
| `catalog/native-origin-overrides.json` | Verified native upstream source map |
| `catalog/presets/` | Open and Hermes preset exclusions |
| `docs/generated/` | Generated human-readable indexes |
| `scripts/` | Install, sync, enrich, audit, and bundle tools |

## Maintenance

```bash
python3 scripts/generate_enriched_catalog.py
python3 scripts/audit_skills.py
./scripts/build-bundle.sh
```

The scheduled workflow runs monthly from `.github/workflows/sync-audit.yml`.

## License

[MIT](LICENSE)

---
name: claude-mem-plugin
description: Install and operate claude-mem persistent memory for Codex/OpenClaw/Claude-style agents. Use when users need cross-session memory, compressed project history, memory search, or Codex-compatible context injection.
---

# Claude-Mem Plugin

Claude-Mem is a persistent memory compression system for agent coding sessions. It captures session activity, compresses it into reusable observations, stores it locally, and injects relevant history into future sessions.

Native upstream: https://github.com/thedotmack/claude-mem

## When to Use

Use this skill when the user needs:

- Cross-session memory for long-running software projects.
- Search over prior agent sessions and project decisions.
- Codex/OpenClaw/Claude-compatible context injection.
- A local web viewer or timeline report of agent work history.
- Memory-backed knowledge agents built from past observations.

## What It Provides

- Codex plugin manifest: `plugin/.codex-plugin/plugin.json`.
- Codex lifecycle hooks: `plugin/hooks/codex-hooks.json`.
- MCP server config: `plugin/.mcp.json`.
- Memory search skills such as `mem-search`, `smart-explore`, `knowledge-agent`, and `timeline-report`.
- Local storage under `~/.claude-mem`.

## Recommended Installation Policy

Treat this as an advanced infrastructure plugin, not a normal lightweight skill.

Before installing globally:

1. Confirm the user accepts local session capture.
2. Confirm which AI provider will be used for compression.
3. Start with one project or isolated Codex profile.
4. Verify worker startup, MCP tools, and memory search.
5. Only then consider enabling it broadly.

## Install Options

Official installer:

```bash
npx claude-mem install
```

OpenClaw gateway installer:

```bash
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

Claude plugin marketplace:

```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

## Privacy Controls

- Data is primarily stored locally in `~/.claude-mem`.
- Compression may call the configured AI provider.
- Use `<private>...</private>` blocks for content that should not be stored.
- Do not enable on sensitive client repositories without explicit approval.

## Risk Notes

- Runs hooks during session lifecycle events.
- Starts a local worker and may open a local viewer port.
- Can inject stale or low-quality memories if prior observations are noisy.
- Requires Node.js and package installation; plugin package declares Node `>=18` and Bun support.

## Registry Recommendation

- Category: memory-context / agent infrastructure.
- Suggested rating: 5★ for advanced users.
- Standard bundle: exclude by default because it is invasive and environment-level.

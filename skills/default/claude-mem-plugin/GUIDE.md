# Claude-Mem Plugin Guide

Claude-Mem is best handled as a Codex/OpenClaw plugin rather than a single copied skill folder.

## Evaluation Summary

- Native origin: https://github.com/thedotmack/claude-mem
- License: Apache-2.0
- Project type: plugin + hooks + MCP + local worker + bundled skills
- Storage: `~/.claude-mem`
- Compatibility: Claude Code, Codex-compatible plugin manifest, OpenClaw gateway installer, Gemini CLI, OpenCode

## Recommended Rollout

1. Test in an isolated project.
2. Confirm privacy policy and provider configuration.
3. Verify the worker and MCP tools.
4. Use `mem-search` before relying on automatic context injection.
5. Add to a long-running project only after memory quality is acceptable.

## Do Not Include in Standard Bundle

The standard bundle is designed for lightweight, low-conflict skills. Claude-Mem is a background memory system with hooks and persistent storage, so it should remain an opt-in advanced module.

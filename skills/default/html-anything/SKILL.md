---
name: html-anything
description: Create publish-ready single-file HTML artifacts with the html-anything local agentic editor. Use when users need designed HTML articles, decks, posters, Xiaohongshu/X cards, web prototypes, data reports, or HTML/PNG export without a separate API key.
---

# HTML Anything

HTML Anything is a local-first agentic HTML editor from `nexu-io/html-anything`. It turns Markdown, CSV, Excel, JSON, SQL, or raw notes into designed, publish-ready single-file HTML and PNG artifacts.

Native upstream: https://github.com/nexu-io/html-anything

## When to Use

Use this skill when the user needs:

- A designed HTML article, poster, deck, report, or social card.
- WeChat / Zhihu / X / Xiaohongshu-ready visual publishing assets.
- A high-fidelity web prototype or SaaS landing page mockup.
- Data reports rendered from CSV, Excel, JSON, or tabular input.
- HTML and PNG export powered by a local coding-agent CLI session.

## What It Provides

- 78 upstream `SKILL.md` templates as of 2026-06-03.
- 9 deliverable surfaces: magazine articles, keynote decks, résumés, posters, Xiaohongshu cards, tweet cards, web prototypes, data reports, and Hyperframes video frames.
- Local agent CLI reuse for Claude Code, Cursor Agent, Codex, Gemini CLI, Copilot CLI, OpenCode, Qwen Coder, and Aider.
- Browser-based live preview, sandboxed iframe rendering, and one-click HTML/PNG export.

## Installation Policy

Treat this as an advanced publishing suite, not a tiny standalone prompt skill.

Recommended rollout:

1. Install or run the upstream app locally.
2. Confirm a supported coding-agent CLI is already authenticated.
3. Generate a small artifact first, such as a poster or article.
4. Export HTML and PNG and inspect the output.
5. Only then use it for production publishing workflows.

## Standard Bundle Policy

This skill can occupy the `html-publishing` capability in the standard bundle because it covers designed HTML/PNG publishing better than narrow Markdown-to-HTML converters.

It should not replace:

- Spreadsheet/document/PDF tools that produce office-native files.
- General frontend development skills.
- Image-generation skills that create raster artwork.

## Risk Notes

- Requires a local web app/browser workflow.
- Depends on local Node/pnpm setup and an authenticated coding-agent CLI.
- Broad template coverage can overlap with deck, article, and social-card skills; use conflict groups to avoid duplicate standard installs.
- Some upstream templates are inspired by other open-source projects; preserve those attributions when importing individual templates.

# HTML Anything Guide

## Evaluation Summary

- Native origin: https://github.com/nexu-io/html-anything
- License: Apache-2.0
- Upstream heat checked: 2026-06-03
- GitHub stars at review time: ~5.9k
- Upstream skill templates: 78 `SKILL.md` files
- Project type: local Next.js application plus template skill catalog

## Recommended Registry Treatment

Add as a single meta-skill named `html-anything`.

Do not bulk-import all upstream templates into the standard bundle. The template catalog is valuable, but adding dozens of narrowly scoped article/deck/card templates would pollute normal Codex skill selection.

## Standard Bundle Decision

Include `html-anything` as the sole `html-publishing` capability.

Keep other standard tools where their output target differs:

- `pptx-generator` remains for native slide decks.
- `minimax-docx` remains for Word-style documents.
- `nano-pdf` remains for PDF workflows.
- `generative-ui` remains for app/UI generation.
- `gemini-image-service` remains for image generation.

## Conflict Handling

Use `html-publishing` as the conflict group for broad HTML publishing skills such as:

- `html-anything`
- `baoyu-markdown-to-html`

This removes duplicate installs from the standard bundle without deleting useful optional skills from the base library.

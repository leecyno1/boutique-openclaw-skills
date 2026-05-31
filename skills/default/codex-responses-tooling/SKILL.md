---
name: codex-responses-tooling
description: Use when generating images through the local Codex Responses API, especially when the agent should reuse ~/.codex/config.toml base_url and decode streamed image_generation results.
---

# Codex Responses Tooling

Use this skill when a task should go through the local Codex Responses API configuration instead of a hardcoded gateway. It is designed as a reusable pattern for streamed Responses calls, including image generation.

## What To Read First

1. Read `~/.codex/config.toml`.
2. Use `[model_providers.OpenAI].base_url` when present.
3. Read the local auth token from Codex auth storage.
4. Build the request against `POST {base_url}/responses`.

## Request Shape

- Set `"stream": true`.
- Use the user prompt as the request input.
- Add the tool definition that matches the task.
- For image generation, the tool is:

```json
{"type":"image_generation","model":"gpt-image-2"}
```

- Choose the outer model with normal judgment; `gpt-5.4` is a good default when the task does not require a different model.

## Streaming Rules

Treat the response as SSE.

1. Read `data:` events line by line.
2. Ignore non-JSON or `[DONE]` events.
3. Watch for `response.output_item.done`.
4. Inspect `item.type` and the tool-specific payload.
5. When `item.type == "image_generation_call"` and `item.result` exists, decode `item.result` from base64.
6. Write the decoded bytes to `.png` or `.jpg`.

## Reuse Pattern

For other Responses-based tools, keep the same flow:

- read local config first
- reuse the configured `base_url`
- send a streamed Responses request
- decode the final tool result from the SSE stream

Only the tool definition and the result decoder should change.

## Prompting

- Keep the task concrete: subject, composition, output format, and intended use.
- If text must appear in the output image, quote it verbatim.
- For posters or banners, specify aspect ratio and negative space.

## Constraints

- Do not rely on the final JSON body for the image payload.
- Do not print or expose the auth token.

## Output

Return the saved artifact path and a short note about the request used.

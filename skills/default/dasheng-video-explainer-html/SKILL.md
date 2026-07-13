---
name: dasheng-video-explainer-html
description: Use when turning a Dasheng HTML article into a no-human vertical explainer video with voiceover, storyboard scenes, HTML animation, real charts, music, and final MP4.
---

# Dasheng Video Explainer HTML

## Role

Build the无真人出镜科普 production line. The article is the fact source; the storyboard is the first-class artifact; html-video renders the animated scenes.

## Required First Artifact

Build the template router, extract the article into a storyboard, then expand it into an HTML Anything video timeline:

```bash
python3 scripts/build_html_anything_template_router.py \
  --output configs/video/html_anything_template_router.json

python3 scripts/video_explainer_storyboard.py \
  --html <article.html> \
  --template-router configs/video/html_anything_template_router.json \
  --output <explainer_storyboard.json> \
  --preview-html <storyboard_preview.html>

python3 scripts/build_storyboard_template_review_table.py \
  --storyboard <explainer_storyboard.json> \
  --output <storyboard_template_review.html>

python3 scripts/extract_template_preview_frames.py \
  --template-data <template_showcase_data.json> \
  --video <template_showcase_silent.mp4> \
  --output-dir <template_previews_dir>

python3 scripts/build_html_anything_video_timeline.py \
  --storyboard <explainer_storyboard.json> \
  --article-html <article.html> \
  --template-router configs/video/html_anything_template_router.json \
  --output <html_anything_video_timeline.json>
```

Optional style asset:

```text
~/Desktop/自媒体创作/00_范式学习/视频训练/<style_id>/style_profile.json
```

Use it to tune template preferences, scene length, transitions, color palette, title/opening/outro rhythm, Lottie/GSAP density, and evidence-scene spacing. Do not train on sample videos inside this production step; use `dasheng-video-style-trainer` first.

## Director Mechanism

Read `docs/technical/video-editing-driving-mechanism.md`, `docs/technical/video-script-template-routing-guide.md`, and `configs/video/video_editing_driver_rules.json` before rendering.

No-human explainer is not PPT pagination. Drive scene choice with:

`voiceover beat -> evidence_need -> cognitive_load -> template -> intra-scene motion -> transition -> music/SFX`

Default state machine:

`hook_card -> question_setup -> chapter_card -> evidence_scene -> logic_animation -> cinematic_bridge -> evidence_scene -> recap_card -> outro`

## Production Rules

- Do not create a second fact chain. Reuse the article's real tables, charts, images, and sourced claims.
- Build a source-asset inventory before writing the storyboard. Original article charts are mandatory evidence assets: none may disappear between article intake, storyboard, scene pack, and final render without an explicit approved exclusion reason.
- Convert each retained article chart into a dynamic chart sequence: `source evidence hold -> one-time data redraw -> completed-chart reading hold`. Never use static zoom/pan, decorative replacement data, or repeated entrance/exit loops.
- Scene duration must follow cognitive load. Default guidance: 2-4 seconds for a simple transition, 4-7 seconds for a single claim, and 8-15 seconds for a dense chart/table. Long evidence scenes should gain internal micro-shots rather than being fragmented into unreadable short scenes.
- Adjacent sentences that share one visual argument should remain in the same scene. Repeatedly cutting back to the same card or making one layout enter/exit multiple times is a director failure.
- Show the overall outline once. Chapter scenes may use a persistent progress marker, but must not alternate between the full outline and enlarged sub-outline cards.
- Learned video style controls presentation only. It must not invent facts, replace article charts, or copy sample-video scripts/frames.
- Generate narration with MiniMax CLI (`mmx`). For review/final videos, prefer per-scene TTS or provider timestamps so each scene duration comes from real audio duration. A single continuous TTS file with text-length timing is only acceptable for rough preview.
- Default no-human narration is `tianxin_xiaoling` at `1.2x` speed. If narration feels slow, compress the visual timeline by the same ratio as the voice; do not speed up voice alone and leave visuals drifting.
- Use MiniMax CLI for production narration, background music, AI image assets, and generated口播音频. Do not call MiniMax APIs directly from ad-hoc scripts unless the CLI cannot express the operation.
- Use external `html-video` as the default renderer via `dasheng-html-video-bridge`; install on demand with `scripts/ensure_video_external_deps.py`.
- Use external `html-anything` only as visual/template reference via `dasheng-html-anything-bridge`; install on demand with `scripts/ensure_video_external_deps.py`.
- No generic framework diagrams when article data can support a concrete chart/table.
- Charts, tables, and line graphs must be backed by article data, source images, or verified data pulls. Never draw decorative or fake lines for a data scene.
- Template diversity must be real at the renderer/component level, not just a template title label.
- Reserve safe zones before rendering: keep core charts/tables away from top chrome and bottom captions; no card/table overlap, no element collision, no developer-facing labels in final MP4.
- Each finance/data scene must answer “what does this prove?” on screen. Avoid visually busy but content-light template demos.
- Final captions must cover the full voiceover, not just scene summaries. Captions should be generated as timed JSON/SRT cues, displayed in sync with the active spoken sentence, and included as delivery artifacts.
- Caption display text must normalize years, percentages, quantities, and counts to Arabic numerals where readability is better, e.g. `2022-2025`, `50%`, `3个月`, `5句话`.
- Subtitle timing must be audio-driven. Use per-scene audio durations, provider alignment metadata, or ASR/forced-alignment backfill. If subtitles are generated only by proportional text length, label the render as preview and do not deliver it as final.
- When only a continuous TTS file exists, run `scripts/align_video_subtitles_to_asr.py --project-dir <remotion_project> --asr-json <whisper_json> --speed 1.2 --write`, then re-render. This keeps script text but uses ASR timestamps.
- No CDN-dependent final assets; preview HTML may be simple, final MP4 must be rendered locally.
- Prefer HyperFrames as the scene composition model.
- Use GSAP-style timelines for entrance, exit, chart reveal, path draw, table scan, and title kinetics.
- Lottie is allowed only as decorative/auxiliary motion. It must never replace real article charts, tables, screenshots, or evidence.
- When a scene needs a reusable vector motion accent, route it through `dasheng-html-video-bridge` and optional external `text-to-lottie`: warning icon, document scan, data flow, market ticker, path trace, lower-third, chapter symbol, or outro mark. Generated Lottie JSON must be verified in the Skia Skottie player and recorded under the task output folder before final render.
- Final/review videos must be rendered by live HTML animation recording. Static screenshot, PNG stitching, or FFmpeg `zoompan` is forbidden for production because it destroys GSAP/Lottie/template motion.
- Do not render from raw storyboard directly unless debugging. Final video planning must route content parts to HTML Anything templates first.
- Before TTS, material generation, or video render, produce `storyboard_template_review.html` and ask for user approval. This page must show one row per scene with time, voiceover, core meaning, evidence refs, template id, template screenshot/placeholder, motion plan, risk notes, and review decision controls.
- Require the user/exported `storyboard_review_decision.json` before production. Validate it with `scripts/validate_storyboard_review_gate.py --storyboard <storyboard.json> --decision <storyboard_review_decision.json> --output <storyboard_review_gate.json>`.
- Do not proceed if the gate report has `status != approved` or `render_allowed != true`.
- If a template has no screenshot, show a visible “暂无模板截图” placeholder and the required preview path. Do not fake a screenshot or hide the missing preview.
- Prefer real template screenshots from `scripts/extract_template_preview_frames.py`, template `preview.png`, or a renderer still. Do not substitute unrelated scene frames as template screenshots unless the table explicitly labels them as scene previews.
- macOS `say` is only a smoke-test fallback; it is not acceptable for final voiceover unless explicitly requested.
- Evidence scenes must appear every 20-35 seconds. Chapter or structure reset must appear every 45-90 seconds.
- A scene longer than 8 seconds needs explicit intra-scene motion: data reveal, document zoom, path highlight, focus shift, or exit motion.

## MiniMax CLI Defaults

Check authentication and quota before production rendering:

```bash
mmx auth status --no-color
mmx quota --no-color
```

Default render command shape:

```bash
python3 scripts/render_html_anything_scene_pack_animated.py \
  --manifest <scene_pack_manifest.json> \
  --output-dir <render_output_dir> \
  --with-voice \
  --voice-provider mmx \
  --voice "tianxin_xiaoling" \
  --mmx-model speech-2.8-hd \
  --mmx-speed 1.2
```

Default narration command shape used by the renderer:

```bash
mmx speech synthesize \
  --text-file <full_voiceover_script.txt> \
  --out <voiceover_single.wav> \
  --model speech-2.8-hd \
  --voice "tianxin_xiaoling" \
  --speed 1.2 \
  --format wav \
  --sample-rate 44100 \
  --channels 1 \
  --language Chinese
```

Default background music command shape:

```bash
mmx music generate \
  --prompt "light technology explainer, data reveal, restrained financial documentary, no vocals" \
  --instrumental \
  --out <bgm.mp3>
```

Default AI image command shape:

```bash
mmx image generate \
  --prompt "<article-specific visual prompt>" \
  --aspect-ratio 9:16 \
  --out <image.jpg>
```

## Style Targets

- Vertical finance/documentary style for mobile publish; horizontal `16:9` is acceptable for Bilibili, template review, and sample evaluation unless the channel requires vertical.
- Default voice: MiniMax `tianxin_xiaoling`, speed `1.2`, warm investor-chat delivery. Keep rhetorical pauses in the script but avoid slow TTS pacing.
- Default BGM: light technology explainer / data reveal. Keep BGM low under the voice and use chapter risers sparingly.
- Average scene: 5-7s; median: 4-5s.
- Evidence screen every 20-35s.
- Chapter card every 45-90s.
- Prefer document zoom, data reveal, chart animation, terminal/Bloomberg-like information rhythm.
- Add Lottie-style accent motion for warning, market ticker, data flow, document scan, and outro only when it supports the spoken beat.
- For AI-generated Lottie assets, prefer prompts grounded in real article variables: exact label text, numeric value, direction of movement, target duration/FPS, transparent background, and where it will sit in the scene. Avoid vague prompts like “make it professional”.

## Review Feedback Guardrails

- If a reviewer flags “line charts are sloppy,” first check whether numeric columns were parsed incorrectly as dates; fix data extraction before visual styling.
- If a reviewer flags “穿模/遮盖,” reduce component density and regenerate midpoint contact sheets before final render.
- If narration is too slow, target `1.2x` voice speed and rebuild scene duration allocation from the actual audio duration.
- If a template review video looks repetitive, reject title-only template switching and require one unique renderer behavior per template.
- If source charts are missing, reject the render even when technical QC passes. Compare the source-asset inventory with the final scene manifest and require 100% accounted-for coverage.
- If viewers cannot finish reading a chart before the next cut, extend its completed-state hold; do not solve the problem by replaying the chart entrance.
- If captions are missing content or lag voice, reject the render: rebuild timed subtitle cues from the full voiceover plus real audio timing, then re-render a contact-sheet/video sample.

## Output Contract

- `explainer_storyboard.json`
- `html_anything_video_timeline.json`
- `storyboard_preview.html`
- `storyboard_template_review.html`
- `storyboard_review_decision.json`
- `storyboard_review_gate.json`
- `voiceover.wav` or provider-specific audio file
- `captions_full.json`
- `captions_full.srt`
- `final_explainer_vertical.mp4`
- `video_qc_report.json`
- `qa_contact_sheet.jpg`

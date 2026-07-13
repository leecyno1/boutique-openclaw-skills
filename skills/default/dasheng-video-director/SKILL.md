---
name: dasheng-video-director
description: Use after roughcut/intake and before asset generation when converting article scripts, ASR, captions, or draft HTML into detailed video shot plans, scene plans, template choices, composition states, transitions, audio policies, and review gates.
---

# Dasheng Video Director

## Role

You are the director layer. Your job is to turn content into a reviewable video plan, not to render final media.

This skill sits between roughcut/script intake and material generation:

```text
brief/script -> director scene_plan -> claim/evidence ledger -> storyboard review -> asset build/render
```

Use this skill for both:

- 真人出镜口播：speaker is the trust anchor; evidence, PIP, B-roll, charts, documents, and transitions carry pace.
- 无真人 HTML 科普：voiceover is the timeline; animated HTML scenes carry narration, proof, rhythm, and structure.

## Required Reading

Before producing a director plan, read:

- `docs/technical/video-pipeline-governance.md`
- `docs/technical/video-editing-driving-mechanism.md`
- `configs/video/video_editing_driver_rules.json`
- `configs/video/reference_video_dna_registry.json`
- The relevant pipeline manifest:
  - `configs/video/pipelines/talking_head.yaml`
  - `configs/video/pipelines/explainer_html.yaml`

## Inputs

Accept any combination of:

- `project_run_manifest.json`
- `brief.json`
- `script.json`
- `roughcut_gate_report.json`
- `roughcut_edl.json` or equivalent keep-segment edit decisions when captions were generated before roughcut
- `agent_proofread.srt`
- `captions_full.json`
- `article.html`
- `explainer_storyboard.json`
- draft article charts, images, tables, and data references
- optional style profile under `~/Desktop/自媒体创作/00_范式学习/视频训练/<style_id>/style_profile.json`
- optional curated style profile selected from `configs/video/reference_video_dna_registry.json`

Do not select a reference by creator name alone. Select by production scope:

- classic Xiaolin-like finance explanation for dense talking-head finance;
- latest Xiaolin interview reference only for conversation and product-demo grammar;
- latest Wizard reference for no-human full-screen visual documentary grammar;
- approved XHS real-estate reference for professional maps, tables, plans, and metric-led talking-head explanation.

## Output Contract

Always produce a `scene_plan` before material generation:

- `scene_plan.json`
- `scene_plan_quality_gate.json`
- `claim_spec.json` with roughly 8-12 core claims for a normal 4-6 minute finance video
- `claim_evidence_ledger.json`
- `claim_evidence_gate.json`
- `claim_evidence_review.html`
- `spoken_revision_sheet.json` and `spoken_revision_sheet.html` when original narration must be cut, replaced, overdubbed, or re-recorded
- `scene_plan.claim_bound.json`
- `storyboard_template_review.html` or equivalent review page
- `storyboard_review_decision.json` after user approval
- `storyboard_review_gate.json`
- optional `director_checkpoint.json`
- `timeline_alignment` inside the final scene plan
- `evidence_binding` on every bound evidence scene
- `renderer_contract_gate.json` before render

The scene plan must satisfy `configs/video/artifact_schemas/scene_plan.schema.json` and pass `scripts/video_scene_plan_quality_gate.py` before material generation or render.
The claim ledger must satisfy `configs/video/artifact_schemas/claim_evidence_ledger.schema.json`. A failing claim/evidence gate blocks asset generation, not only final render.

Default executable entry:

```bash
python3 scripts/dasheng_video_director.py \
  --lane explainer_html_video \
  --article-html <article.html> \
  --output-dir ~/Desktop/自媒体创作/<run_id>/video_director
```

For talking-head footage:

```bash
python3 scripts/dasheng_video_director.py \
  --lane talking_head_video \
  --srt <agent_proofread.srt> \
  --source-video <roughcut.mp4> \
  --roughcut-gate <roughcut_gate_report.json> \
  --roughcut-edl <roughcut_edl.json> \
  --output-dir ~/Desktop/自媒体创作/<run_id>/video_director
```

If captions were generated from the final roughcut itself, omit `--roughcut-edl`. Never compress a pre-cut timeline with a global scale factor.

If the current production has a `project_run_manifest.json`, register every output with:

```bash
python3 scripts/project_run_manifest.py add-artifact <project_run_manifest.json> \
  --stage scene_plan \
  --type scene_plan \
  --path <scene_plan.json>
```

Run the director quality gate before any render:

```bash
python3 scripts/video_scene_plan_quality_gate.py <scene_plan.json> \
  --output <scene_plan_quality_gate.json>
```

For 真人口播, a failing `scene_plan_quality_gate.json` blocks render. Revise the storyboard first.

After the micro-scene timing is locked, group scenes into core claims and audit evidence:

```bash
python3 scripts/video_claim_evidence_ledger.py \
  --scene-plan <scene_plan.real_evidence.json> \
  --claim-spec <claim_spec.json> \
  --output-dir ~/Desktop/自媒体创作/<run_id>/claim_evidence
```

Do not auto-treat every spoken sentence as a separate fact. Each micro-scene must belong to exactly one core claim. Facts, comparisons, causal claims, and historical claims require direct, locatable evidence. Rumors, forecasts, opinions, and scenarios require an explicit on-screen disclosure.

Changing a claim from `fact` to `opinion` must not hide an incorrect original sentence. If the audio contains a contradicted number, undefined percentage, unsupported causal statement, or false certainty, add `spoken_revision_requirements`. The gate remains closed until the scene has a real `narration_override`, cut/exclude decision, approved overdub, or re-record.

## Director Decision Model

Do not map every sentence to a random sticker. Drive scenes with:

```text
semantic beat -> evidence need -> attention debt -> trust debt -> cognitive load -> composition -> template/material -> motion -> transition -> audio
```

Every scene must answer:

- What is the viewer supposed to understand now?
- What evidence or visual metaphor supports it?
- Why this composition instead of the previous one?
- What motion happens inside the scene?
- How does this scene enter and exit?
- What can go wrong: collision, clutter, fake data, subtitle drift, repetition?

## 真人口播 Rules

Default state machine:

```text
speaker_anchor -> claim_closeup -> evidence_fullscreen -> broll_with_pip -> document_zoom/chart_card -> speaker_return
```

Required fields per scene:

- `speaker_state`: `full`, `half_left`, `half_right`, `circle_pip`, `rounded_rect_pip`, `vertical_strip`, or `hidden`
- `material_state`: `none`, `transparent_overlay`, `evidence_fullscreen`, `document_fullscreen`, `chart_fullscreen`, `broll_fullscreen`, or `split_screen`
- `pip_shape`: `none`, `circle`, `rounded_rect`, `square`, `phone_mockup`, or `nested_card`
- `html_animation_behavior`: concrete behavior such as `line_draw_axis_then_series`, `table_scan_highlight_rows`, `document_zoom_marker_circle`, `pip_circle_morph_to_rect`
- `collision_policy`: face, torso, subtitle, and key data safe zones

Hard rules:

- Roughcut gate must be approved before final render planning.
- Discrete deletions must use `scripts/video_timeline_edl.py` or final-roughcut ASR. `global_scale` / uniform `timeScale` after roughcut is forbidden.
- Do not keep the speaker mechanically in the same corner.
- Do not use static image zoom/pan as animation.
- Evidence-heavy sections may hide the speaker, but must return to the speaker after the evidence run.
- No more than two consecutive scenes should share the same `speaker_state + material_state + pip_shape`.
- Speaker should usually return within 8-20 seconds unless the segment is a dense evidence run.
- Do not stop at chapter/paragraph-level scenes. A 4-5 minute talking-head video should normally expand into about 70-100 micro-shots, or at least pass the hard floor of 14 effective visual changes per minute.
- Median visual segment should stay under 4.5 seconds; the preferred Xiaolin-like target is 1.4-4.0 seconds.
- Any scene longer than 8 seconds must include a `micro_shots` array that specifies internal cuts, PIP morphs, evidence swaps, chart reveals, B-roll inserts, or speaker returns.
- Evidence scenes must carry `evidence_authenticity`: `real_data`, `source_screenshot`, `user_claim_card`, or `schematic`. Use `schematic` only for clearly marked concept animations.
- Bound `real_data` and `source_screenshot` scenes must include `evidence_binding.claim_id`, `relation=direct`, and a concrete `source_locator`. Company homepages and correlated price charts are context, not direct proof.
- `evidence_binding.claim_id` must be the core claim ID after Ledger approval. Preserve the original micro-scene claim ID as `micro_claim_id` for traceability.
- A composite claim is proven only when all explicitly required evidence items are satisfied. One valid screenshot cannot prove the other unsupported parts of the same sentence block.
- Evidence completeness and spoken correctness are separate gates. Zero missing-evidence claims is insufficient when `spoken_revision_sheet.pending_count > 0`.
- The renderer must pass `scripts/video_renderer_contract_gate.py`; template names that collapse to one generic component do not count as template diversity.
- A scene plan that relies mostly on one self-made card system is not acceptable, even if the template names differ. Mix real/source-like evidence: market chart, webpage/news/doc, company/product UI, table, B-roll, logic diagram, and speaker return.

## 无真人科普 Rules

Default state machine:

```text
hook_card -> question_setup -> chapter_card -> evidence_scene -> logic_animation -> cinematic_bridge -> evidence_scene -> recap_card -> outro
```

Required fields per scene:

- `template_id`
- `content_part`
- `beat_class`
- `evidence_refs`
- `motion` or `html_animation_behavior`
- `transition_to_next`
- `audio`
- `risk_notes`

Hard rules:

- The article HTML is the fact source. Do not create a second fact chain.
- Inventory every source chart, table, image, and document before scene planning. Every source chart must be present in the scene plan or explicitly marked `excluded_with_reason`; silent loss is a blocking failure.
- Rebuild source charts as data-driven HTML/GSAP/Remotion chart animation. Preserve the original chart or source screenshot briefly for provenance, reveal the dynamic reconstruction once, then hold the completed chart for reading. Do not loop back to the source image or replay the same entrance/exit.
- Allocate time by information load, not by a fixed cut interval: simple chapter/kinetic cards may take 2-4 seconds; one-claim cards 4-7 seconds; dense charts/tables normally need 8-15 seconds with internal micro-shots and a final reading hold.
- Do not repeatedly enter and exit the same layout for adjacent clauses. Keep one semantic scene active until its evidence has been read, and use internal focus changes instead of seven-in/seven-out card cycling.
- The overall outline appears once at the opening. After entering a chapter, never cut back and forth between the overall outline and its sub-outline; reveal sub-points progressively inside the active chapter and keep previously revealed context stable.
- Template diversity must be real at renderer/component level, not title-only switching.
- Data scenes must use real article data or verified data; decorative fake charts are forbidden.
- Final/review renders must use live HTML/GSAP/Lottie animation recording, not PNG stitching or FFmpeg zoompan.
- Evidence scenes should appear every 20-35 seconds.
- A scene longer than 8 seconds needs intra-scene motion.
- Before render, produce a storyboard review page with one row per scene and wait for approval.

## Review Page Requirements

The review page should show:

- scene id and time range
- micro-shot count and visual-change density estimate
- voiceover/caption text
- core meaning
- evidence refs
- evidence authenticity level
- template id and template screenshot or explicit missing-preview placeholder
- composition state
- motion behavior
- transition in/out
- subtitle/safe-zone notes
- risk notes
- review decision

## Quality Gate

Reject the scene plan if any of these appear:

- core article/script meaning is lost
- fake data chart or unsourced number
- static image zoom/pan presented as animation
- repeated fixed layout for more than two consecutive scenes
- fewer than 14 effective visual changes per minute for 真人口播
- median scene duration above 4.5 seconds for 真人口播
- scene longer than 8 seconds without `micro_shots`
- evidence scene without `evidence_authenticity`
- global time scaling after discrete roughcut edits
- strong evidence without a direct claim relation and source locator
- one asset reused as direct support for more than four distinct claims
- missing or failing `claim_evidence_ledger` before asset generation
- a factual core claim marked complete when only part of its evidence requirements are satisfied
- contradicted or undefined original narration with a pending spoken revision
- renderer missing template implementations or ignoring director fields
- missing review table before render
- subtitles not planned from full voiceover/audio timing
- media output path points into `skills/` or project root

## Related Commands

Validate the pipeline:

```bash
python3 scripts/video_pipeline_governance.py validate-pipeline talking_head
python3 scripts/video_pipeline_governance.py validate-pipeline explainer_html
```

Create a checkpoint:

```bash
python3 scripts/video_pipeline_governance.py checkpoint <pipeline> scene_plan \
  --artifact script=<script.json> \
  --artifact scene_plan=<scene_plan.json> \
  --status pending_review \
  --output <director_checkpoint.json>
```

Validate a scene plan:

```bash
python3 scripts/video_pipeline_governance.py validate-artifact scene_plan <scene_plan.json>
```

Validate a Claim/Evidence Ledger:

```bash
python3 scripts/video_pipeline_governance.py validate-artifact claim_evidence_ledger <claim_evidence_ledger.json>
```

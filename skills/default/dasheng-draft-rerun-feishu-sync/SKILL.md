---
name: dasheng-draft-rerun-feishu-sync
description: Re-run Dasheng daily draft for a specified topic and sync the latest compliant article to an existing Feishu doc. Use when user asks to rerun a single topic draft (e.g. 选题2), enforce no intake-internal stats/no style-DNA wording, and update Feishu with write+readback verification.
---

# dasheng-draft-rerun-feishu-sync

## Inputs

- `run_id` (required), e.g. `daily-intake-20260325-094811`
- `topic_id` (required), e.g. `2`
- `doc_token` (optional, if omitted then search by title)

## Workflow

1. Extract the target topic outline from the run's `outline-plans*.json` into a single-topic file.
2. Run draft generation:
   - `node /Users/lichengyin/clawd/skills/dasheng-daily-draft/index.js <single-topic-outline.json>`
3. Gate by quality report (`artifacts/draft/draft-quality-report.json`):
   - `pass_count=1`, `fail_count=0`
   - `internal_data_terms_hit` empty
   - `real_source_url_count >= 3`
   - `source_placeholders_hit` empty
4. Build publish markdown with script:
   - `python3 scripts/prepare_topic_publish_markdown.py --run-id <run_id> --topic-id <topic_id> --output <file>`
5. Resolve target Feishu doc:
   - Prefer explicit `doc_token`
   - Otherwise use `feishu_drive list` and match title `初稿｜选题{topic_id}`
6. Publish to Feishu via `feishu_doc`:
   - `action=write` (overwrite entire doc)
   - then `action=read` for immediate verification
7. Verify publish result:
   - `block_count >= 80`
   - content includes `开篇立论` / `数据证据与论据` / `数据与素材来源`
   - content contains at least 3 real source URLs
8. Return completion summary:
   - doc URL, title, revision id, block count, quality evidence

## Failure Handling

- If quality report fails: stop and report failed checks (do not publish).
- If markdown contains forbidden internal terms: stop and report hit lines.
- If Feishu readback fails verification: re-write once; if still failing, report blocked with concrete reason.

## Resources

- `scripts/prepare_topic_publish_markdown.py`: deterministic publish markdown builder + compliance checks.
- `references/publish-checklist.md`: quick acceptance checklist for manual audit.

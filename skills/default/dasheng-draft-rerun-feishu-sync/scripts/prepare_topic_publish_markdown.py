#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

FORBIDDEN_TERMS = [
    r"intake统计",
    r"流程统计",
    r"工作流统计",
    r"内部统计",
    r"跨平台扩散",
    r"S/A占比",
    r"s/a占比",
    r"lemon_dna",
    r"风格DNA",
]

PLACEHOLDER_URL_PATTERNS = [r"example\.com", r"source-pending", r"placeholder"]


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare publish markdown for one topic draft")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--topic-id", required=True)
    parser.add_argument("--draft-file", default="")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def default_draft_file(run_id: str) -> Path:
    return Path(
        f"/Users/lichengyin/clawd/skills/dasheng-daily-shared/runtime-data/runs/{run_id}/artifacts/draft/draft-packages.json"
    )


def load_topic_draft(draft_file: Path, topic_id: str) -> dict:
    data = json.loads(draft_file.read_text())
    if not isinstance(data, list):
        raise ValueError("draft-packages.json is not an array")
    for item in data:
        if str(item.get("topic_id")) == str(topic_id):
            return item
    raise ValueError(f"topic_id={topic_id} not found in {draft_file}")


def sanitize_content(content: str) -> str:
    replacements = {
        "背景与做题价值：热度 35.5， 63.6，S/A 占比 40.0%。": "背景与做题价值：围绕公开来源证据构建判断边界。",
        "围绕“背景与做题价值：热度 35.5， 63.6，S/A 占比 40.0%”的讨论，建议采用“主证据 + 辅证据 + 反证提示”三段式，既保留可读性也保留严谨性。": "围绕“公开来源证据如何支撑结论”的讨论，建议采用“主证据 + 辅证据 + 反证提示”三段式，既保留可读性也保留严谨性。",
        "热度与扩散同步抬升": "关键风险信号同步抬升",
        "叙事扩散快于事实验证": "叙事传播快于事实验证",
    }
    result = content
    for old, new in replacements.items():
        result = result.replace(old, new)

    result = re.sub(r"\n{3,}", "\n\n", result).strip() + "\n"
    return result


def extract_sources(content: str):
    match = re.search(r"##\s+数据与素材来源\s*(.*?)(?:\n##\s+|\Z)", content, re.S)
    if not match:
        return []
    section = match.group(1)
    return re.findall(r"https?://[^\s)）]+", section)


def is_placeholder(url: str) -> bool:
    lower = url.lower()
    return any(re.search(pattern, lower) for pattern in PLACEHOLDER_URL_PATTERNS)


def find_forbidden_hits(content: str):
    hits = []
    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_TERMS:
            if re.search(pattern, line, re.I):
                hits.append({"line": idx, "pattern": pattern, "text": line.strip()})
    return hits


def require_headings(content: str):
    required = ["开篇立论", "数据证据与论据", "数据与素材来源"]
    missing = []
    for heading in required:
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", content, re.M):
            missing.append(heading)
    return missing


def main():
    args = parse_args()
    draft_file = Path(args.draft_file) if args.draft_file else default_draft_file(args.run_id)
    if not draft_file.exists():
        raise SystemExit(f"draft file not found: {draft_file}")

    item = load_topic_draft(draft_file, args.topic_id)
    title = str(item.get("title") or f"选题{args.topic_id}").strip()
    content = str(item.get("content") or "").strip()
    if not content:
        raise SystemExit("empty content in draft package")

    content = sanitize_content(content)
    if not content.startswith("# "):
        content = f"# {title}\n\n" + content

    missing = require_headings(content)
    forbidden_hits = find_forbidden_hits(content)
    urls = extract_sources(content)
    real_urls = [u for u in urls if not is_placeholder(u)]

    errors = []
    if missing:
        errors.append(f"missing headings: {', '.join(missing)}")
    if len(real_urls) < 3:
        errors.append(f"real source urls < 3 (got {len(real_urls)})")
    if forbidden_hits:
        errors.append(f"forbidden terms hit: {len(forbidden_hits)}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    summary = {
        "run_id": args.run_id,
        "topic_id": args.topic_id,
        "title": title,
        "draft_file": str(draft_file),
        "output": str(output_path),
        "chars": len(content),
        "source_urls": len(urls),
        "real_source_urls": len(real_urls),
        "forbidden_hits": forbidden_hits,
        "missing_headings": missing,
        "ok": len(errors) == 0,
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from datetime import datetime

NOISE_HINTS = ["未归类", "核心议题"]


def topic_score(item):
    heat = (item.get("heat") or {}).get("composite", 0)
    sa_ratio = (item.get("heat") or {}).get("sa_ratio", 0)
    count = item.get("count", 0)
    base = heat + sa_ratio * 20 + min(count, 100) * 0.1
    name = item.get("cluster_name", "")
    if any(key in name for key in NOISE_HINTS):
        base -= 15
    return base


def make_display_name(cluster_name):
    if "·" in cluster_name:
        return cluster_name.split("·", 1)[1]
    return cluster_name


TOKEN_RE_ZH = re.compile(r"[\u4e00-\u9fff]{2,}")
TOKEN_RE_EN = re.compile(r"[A-Za-z][A-Za-z0-9\-]{3,}")
TOKEN_STOP = {
    "今天", "昨天", "最新", "如何", "什么", "我们", "你们", "他们", "这个", "那个", "以及",
    "the", "with", "from", "that", "this", "what", "have", "your", "will", "into", "about"
}


def _extract_terms(text, max_terms=8):
    if not text:
        return []
    terms = []
    blob = str(text)
    for token in TOKEN_RE_ZH.findall(blob):
        token = token.strip()
        if token and token not in TOKEN_STOP and len(token) <= 8:
            terms.append(token)
    for token in TOKEN_RE_EN.findall(blob.lower()):
        if token and token not in TOKEN_STOP:
            terms.append(token)
    counter = Counter(terms)
    return [k for k, _ in counter.most_common(max_terms)]


def _focus_terms(item, max_terms=3):
    terms = []
    terms.extend(item.get("cluster_tokens") or [])
    terms.extend(item.get("label_hits") or [])
    for ev in (item.get("evidence_items") or [])[:5]:
        terms.extend(_extract_terms(ev.get("title", ""), max_terms=4))
    cleaned = []
    seen = set()
    for token in terms:
        token = str(token).strip()
        if not token or token in TOKEN_STOP or token in seen:
            continue
        seen.add(token)
        cleaned.append(token)
        if len(cleaned) >= max_terms:
            break
    return cleaned


def build_derived_topics(item, guidance):
    cluster_name = item.get("cluster_name", "")
    topic = make_display_name(cluster_name)
    core = guidance.get("core_angle") or "核心观点"
    secondary = guidance.get("secondary_angles") or []
    sec = secondary[0] if secondary else "关键变量"
    focus = _focus_terms(item, max_terms=3)

    if len(focus) >= 2:
        return [
            f"{focus[0]}与{focus[1]}之间的传导链条如何影响“{topic}”的{core}？",
            f"在{sec}维度下，{focus[0]}会不会成为“{topic}”后续变化的领先指标？",
            f"如果{focus[1]}出现反向波动，围绕“{topic}”的内容策略应如何调整？",
        ]

    return [
        f"{topic}的{core}正在如何变化？",
        f"{topic}在“{sec}”维度会出现哪些分化？",
        f"围绕{topic}做内容时，执行策略与风险边界该怎么定？",
    ]


def _extract_json_object(text):
    if not text:
        return None

    cleaned = str(text).strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    candidate = cleaned[start:end + 1]
    try:
        return json.loads(candidate)
    except Exception:
        return None


def _normalize_outline_lines(lines):
    normalized = []
    for raw in lines or []:
        line = str(raw or "").strip()
        line = re.sub(r"^[-*•]\s*", "", line)
        line = re.sub(r"^\d+[\.、\)\-\s]*", "", line)
        line = line.strip()
        if line:
            normalized.append(line)
    return normalized


def generate_outlines_with_llm(selected, timeout_sec=180):
    topics = []
    for idx, item in enumerate(selected, 1):
        guidance = item.get("editorial_guidance") or {}
        evidences = []
        for ev in (item.get("evidence_items") or [])[:3]:
            title = str(ev.get("title") or "").strip().replace("\n", " ")
            if title:
                evidences.append(title)

        topics.append({
            "topic_id": idx,
            "cluster_name": item.get("cluster_name", ""),
            "core_angle": guidance.get("core_angle") or "核心观点",
            "secondary_angles": (guidance.get("secondary_angles") or [])[:3],
            "risk_notes": (item.get("risk_notes") or [])[:2],
            "focus_terms": _focus_terms(item, max_terms=3),
            "evidence_titles": evidences,
        })

    prompt = (
        "你是内容策略总编。请根据给定主题信息，为每个主题生成“5段写作大纲”。\n"
        "要求：\n"
        "1) 必须结合每个主题自身证据，不要套用同一模板；\n"
        "2) 每个主题必须返回且仅返回5段；\n"
        "3) 每段是可执行的一句话，不要编号；\n"
        "4) 不要输出Markdown，不要解释；\n"
        "5) 只输出严格JSON，格式如下：\n"
        "{\n"
        "  \"topics\": [\n"
        "    {\"topic_id\": 1, \"outline\": [\"...\",\"...\",\"...\",\"...\",\"...\"]}\n"
        "  ]\n"
        "}\n\n"
        "输入数据：\n"
        f"{json.dumps({'topics': topics}, ensure_ascii=False)}"
    )

    cmd = [
        "openclaw", "agent",
        "--agent", "main",
        "--json",
        "--thinking", "low",
        "--timeout", str(timeout_sec),
        "--message", prompt,
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "LLM大纲生成失败（openclaw agent 调用失败）\n"
            f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )

    outer = _extract_json_object(proc.stdout)
    if not isinstance(outer, dict):
        raise RuntimeError(f"LLM大纲生成失败：无法解析 agent 输出\n{proc.stdout[:1200]}")

    payloads = ((outer.get("result") or {}).get("payloads") or []) if isinstance(outer.get("result"), dict) else []
    if not payloads:
        raise RuntimeError(f"LLM大纲生成失败：agent 未返回 payload\n{json.dumps(outer, ensure_ascii=False)[:1200]}")

    llm_text = payloads[0].get("text") or ""
    content = _extract_json_object(llm_text)
    if not isinstance(content, dict):
        raise RuntimeError(f"LLM大纲生成失败：payload 不是合法 JSON\n{llm_text[:1200]}")

    outline_map = {}
    for topic in content.get("topics") or []:
        try:
            topic_id = int(topic.get("topic_id"))
        except Exception:
            continue
        lines = _normalize_outline_lines(topic.get("outline") or [])
        if len(lines) == 5:
            outline_map[topic_id] = lines

    missing = [idx for idx in range(1, len(selected) + 1) if idx not in outline_map]
    if missing:
        raise RuntimeError(
            "LLM大纲生成失败：以下 topic_id 未返回合法5段大纲："
            f"{missing}"
        )

    return outline_map


def build_thesis(cluster_name, guidance):
    topic = make_display_name(cluster_name)
    core = guidance.get("core_angle") or "核心观点"
    return f"围绕“{topic}”做{core}向深度分析，输出可执行的选题判断与下一步动作。"


def select_topics(items, min_count, max_count):
    sorted_items = sorted(items, key=topic_score, reverse=True)
    preferred = [item for item in sorted_items if not any(key in item.get("cluster_name", "") for key in NOISE_HINTS)]

    selected = preferred[:max_count]
    if len(selected) < min_count:
        used = {item.get("cluster_name") for item in selected}
        for item in sorted_items:
            name = item.get("cluster_name")
            if name in used:
                continue
            selected.append(item)
            used.add(name)
            if len(selected) >= min_count:
                break

    return selected[:max_count]


def evidence_lines(item, max_items=3):
    lines = []
    for evidence in (item.get("evidence_items") or [])[:max_items]:
        title = (evidence.get("title") or "").replace("\n", " ").strip()
        if len(title) > 90:
            title = title[:90] + "..."
        url = (evidence.get("url") or "").strip()
        lines.append((evidence.get("platform", "未知平台"), title, url))
    return lines


def render_markdown(selected, source_file, output_file, outline_map):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# 第二环节详细 Brief（8~10个选题）")
    lines.append("")
    lines.append(f"- 生成时间：{now}")
    lines.append(f"- 输入文件：`{source_file}`")
    lines.append(f"- 输出文件：`{output_file}`")
    lines.append(f"- 选题数量：{len(selected)}")
    lines.append("")

    lines.append("## 选题总览")
    for idx, item in enumerate(selected, 1):
        heat = (item.get("heat") or {}).get("composite", 0)
        lines.append(
            f"- {idx}. {item.get('cluster_name')}｜热度 {heat}｜样本 {item.get('count', 0)}｜S/A {item.get('s_count', 0)}/{item.get('a_count', 0)}"
        )
    lines.append("")

    for idx, item in enumerate(selected, 1):
        guidance = item.get("editorial_guidance") or {}
        lines.append(f"## {idx}. {item.get('cluster_name')}")
        lines.append(f"- 核心判断：{build_thesis(item.get('cluster_name', ''), guidance)}")
        lines.append(
            f"- 价值判断：热度 {(item.get('heat') or {}).get('composite', 0)}，跨平台 {(item.get('heat') or {}).get('cross_platform', 0)}，S/A 占比 {round(((item.get('heat') or {}).get('sa_ratio', 0))*100, 1)}%。"
        )
        lines.append(f"- 目标读者：{guidance.get('target_audience', '编辑与投资内容读者')}")
        lines.append(f"- 输出形态：{' / '.join(guidance.get('recommended_formats') or ['深度图文', '短视频解读'])}")
        risks = item.get("risk_notes") or ["注意区分事实、观点与推演，避免结论先行。"]
        lines.append(f"- 风险边界：{'；'.join(risks)}")
        lines.append("")

        lines.append("### 衍生话题")
        for topic in build_derived_topics(item, guidance):
            lines.append(f"- {topic}")
        lines.append("")

        lines.append("### 大纲")
        sections = outline_map.get(idx) or []
        for order, section in enumerate(sections, 1):
            lines.append(f"- {order}. {section}")
        lines.append("")

        lines.append("### 关键证据")
        evidences = evidence_lines(item, 3)
        if not evidences:
            lines.append("- 暂无证据样本（需要回查底稿）")
        for platform, title, url in evidences:
            if url:
                lines.append(f"- [{platform}] [{title}]({url})")
            else:
                lines.append(f"- [{platform}] {title}")
                lines.append("  - （缺少原文链接，需回查 intake 底稿）")
        lines.append("")

        lines.append("### 下一阶段动作")
        next_actions = item.get("next_actions") or []
        if not next_actions:
            next_actions = [
                "补齐至少 2 条跨平台证据，形成最小证据链。",
                "明确目标平台与目标读者，避免同稿多投失焦。",
                "进入 Material Pack 组装，沉淀素材与论据结构。",
            ]
        for action in next_actions[:3]:
            lines.append(f"- {action}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build detailed phase2 brief markdown (8~10 topics)")
    parser.add_argument("editorial_file", help="phase2-editorial-briefs.json path")
    parser.add_argument("output_file", help="output markdown path")
    parser.add_argument("--topic-count-min", type=int, default=8)
    parser.add_argument("--topic-count-max", type=int, default=10)
    args = parser.parse_args()

    editorial_path = Path(args.editorial_file)
    output_path = Path(args.output_file)

    if not editorial_path.exists():
        raise FileNotFoundError(f"editorial file not found: {editorial_path}")

    data = json.loads(editorial_path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("editorial file must be non-empty list")

    selected = select_topics(data, args.topic_count_min, args.topic_count_max)
    outline_map = generate_outlines_with_llm(selected)
    markdown = render_markdown(selected, str(editorial_path), str(output_path), outline_map)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    result = {
        "selected_count": len(selected),
        "selected_topics": [item.get("cluster_name") for item in selected],
        "output_file": str(output_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

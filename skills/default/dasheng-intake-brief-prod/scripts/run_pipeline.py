#!/usr/bin/env python3

import argparse
import glob
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def run_cmd(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def detect_intake_file(stdout, workspace):
    match = re.search(r"完整数据已保存:\s*(/[^\n]+)", stdout)
    if match:
        path = Path(match.group(1).strip())
        if path.exists():
            return path

    candidates = sorted(glob.glob(str(workspace / "memory" / "dasheng_v11_output_*.json")))
    if not candidates:
        raise FileNotFoundError("未找到采集输出文件 dasheng_v11_output_*.json")
    return Path(candidates[-1])


def build_phase2_cmd(args, phase2_script, intake_copy, phase2_dir, topic_spec):
    cmd = [
        "python3",
        str(phase2_script),
        str(intake_copy),
        str(phase2_dir),
        "--cluster-mode",
        "semantic",
        "--contract-version",
        args.contract_version,
        "--topic-spec-file",
        str(topic_spec),
        "--min-count",
        "1",
        "--max-clusters",
        str(args.max_clusters),
        "--top-n",
        str(args.top_n),
    ]

    if args.contract_version == "v8":
        cmd.extend(
            [
                "--cluster-target-min",
                str(args.cluster_target_min),
                "--cluster-target-max",
                str(args.cluster_target_max),
            ]
        )
        if args.domain_taxonomy:
            cmd.extend(["--domain-taxonomy", str(Path(args.domain_taxonomy).expanduser().resolve())])

    if args.sa_only:
        cmd.append("--sa-only")
    return cmd


def ensure_files_exist(files):
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise FileNotFoundError("phase2 output missing:\n" + "\n".join(missing))


def main():
    parser = argparse.ArgumentParser(description="Run Dasheng intake + enhanced phase2 brief pipeline")
    parser.add_argument("--workspace", default="/Users/lichengyin/clawd")
    parser.add_argument("--collector", default="scripts/dasheng_skill_v11.py")
    parser.add_argument("--phase2", default="scripts/phase2_rebuilder.py")
    parser.add_argument("--topic-spec", default="configs/phase2/topic_specs.v1.json")
    parser.add_argument("--input-file", help="Optional intake file; skip collector when provided")
    parser.add_argument("--output-prefix", default="daily-intake")
    parser.add_argument("--phase2-subdir", default=None)
    parser.add_argument("--contract-version", choices=["v7", "v8"], default="v7")
    parser.add_argument("--domain-taxonomy", default="configs/phase2/domain_taxonomy.v8.json")
    parser.add_argument("--cluster-target-min", type=int, default=10)
    parser.add_argument("--cluster-target-max", type=int, default=20)
    parser.add_argument("--max-clusters", type=int, default=20)
    parser.add_argument("--top-n", type=int, default=3)
    parser.add_argument("--sa-only", action="store_true", help="Only cluster S/A topics (default: all topics)")
    args = parser.parse_args()

    if args.phase2_subdir is None:
        args.phase2_subdir = "phase2-prod-v8" if args.contract_version == "v8" else "phase2-prod-v7"

    workspace = Path(args.workspace).resolve()
    collector = workspace / args.collector
    phase2 = workspace / args.phase2
    topic_spec = workspace / args.topic_spec

    if not phase2.exists():
        raise FileNotFoundError(f"phase2 script not found: {phase2}")
    if not topic_spec.exists():
        raise FileNotFoundError(f"topic spec not found: {topic_spec}")

    if args.contract_version == "v8" and args.domain_taxonomy:
        taxonomy_path = Path(args.domain_taxonomy).expanduser()
        if not taxonomy_path.is_absolute():
            taxonomy_path = workspace / taxonomy_path
        if not taxonomy_path.exists():
            raise FileNotFoundError(f"domain taxonomy not found: {taxonomy_path}")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{args.output_prefix}-{ts}"
    run_dir = workspace / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    collector_stdout = ""
    collector_mode = "rerun"

    if args.input_file:
        intake_file = Path(args.input_file).expanduser().resolve()
        if not intake_file.exists():
            raise FileNotFoundError(f"input file not found: {intake_file}")
        collector_mode = "reuse_input"
    else:
        if not collector.exists():
            raise FileNotFoundError(f"collector not found: {collector}")
        collector_stdout = run_cmd(["python3", str(collector)], cwd=str(workspace))
        intake_file = detect_intake_file(collector_stdout, workspace)

    intake_copy = run_dir / "intake-output-v11.json"
    shutil.copy2(intake_file, intake_copy)

    phase2_dir = run_dir / args.phase2_subdir
    phase2_cmd = build_phase2_cmd(args, phase2, intake_copy, phase2_dir, topic_spec)
    phase2_stdout = run_cmd(phase2_cmd, cwd=str(workspace))

    summary_path = phase2_dir / "phase2-clusters-summary.json"
    brief_path = phase2_dir / ("phase2-brief-cards.md" if args.contract_version == "v8" else "phase2-brief-library.md")
    topn_path = phase2_dir / "phase2-topn-for-confirmation.json"
    unmatched_path = phase2_dir / "phase2-unmatched.json"
    bitable_rows_path = phase2_dir / "phase2-bitable-rows.json"
    sync_contract_path = phase2_dir / "phase2-sync-contract.json"
    topic_index_path = phase2_dir / "phase2-topic-index.json"
    editorial_briefs_path = phase2_dir / "phase2-editorial-briefs.json"
    domain_map_path = phase2_dir / "phase2-domain-map.json"
    topic_clusters_path = phase2_dir / "phase2-topic-clusters.json"
    cluster_audit_path = phase2_dir / "phase2-cluster-audit.json"
    rejects_path = phase2_dir / "phase2-rejects.json"

    required_files = [
        summary_path,
        brief_path,
        topn_path,
        unmatched_path,
        bitable_rows_path,
        sync_contract_path,
        topic_index_path,
        editorial_briefs_path,
    ]

    if args.contract_version == "v8":
        required_files.extend([domain_map_path, topic_clusters_path, cluster_audit_path, rejects_path])

    ensure_files_exist(required_files)

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    clusters = summary.get("clusters", [])

    report = {
        "run_id": run_id,
        "contract_version": args.contract_version,
        "collector_mode": collector_mode,
        "intake_source": str(intake_file),
        "run_dir": str(run_dir),
        "phase2_dir": str(phase2_dir),
        "summary_file": str(summary_path),
        "brief_file": str(brief_path),
        "topn_file": str(topn_path),
        "topic_index_file": str(topic_index_path),
        "editorial_briefs_file": str(editorial_briefs_path),
        "bitable_rows_file": str(bitable_rows_path),
        "sync_contract_file": str(sync_contract_path),
        "domain_map_file": str(domain_map_path) if domain_map_path.exists() else None,
        "topic_clusters_file": str(topic_clusters_path) if topic_clusters_path.exists() else None,
        "cluster_audit_file": str(cluster_audit_path) if cluster_audit_path.exists() else None,
        "rejects_file": str(rejects_path) if rejects_path.exists() else None,
        "stats": summary.get("stats", {}),
        "top5_topics": [
            {
                "topic": cluster.get("cluster_name"),
                "parent_topic": cluster.get("parent_topic"),
                "heat": (cluster.get("heat") or {}).get("composite"),
                "count": cluster.get("count"),
            }
            for cluster in clusters[:5]
        ],
        "collector_stdout_tail": collector_stdout.splitlines()[-10:] if collector_stdout else [],
        "phase2_stdout_tail": phase2_stdout.splitlines()[-10:],
    }

    report_file = run_dir / "workflow-report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

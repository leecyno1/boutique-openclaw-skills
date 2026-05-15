#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const CONFIG_FILE = path.join(__dirname, 'config.json');

function findLatestBriefJson() {
  const preferred = path.join(
    WORKSPACE_ROOT,
    'logs',
    'daily-intake-20260325-094811',
    'phase2-prod-v8-8to10',
    'phase2-editorial-briefs.json'
  );
  if (fs.existsSync(preferred)) return preferred;

  const logsDir = path.join(WORKSPACE_ROOT, 'logs');
  if (!fs.existsSync(logsDir)) return preferred;

  const candidates = [];
  for (const runDir of fs.readdirSync(logsDir)) {
    if (!runDir.startsWith('daily-intake-')) continue;
    const fullRunDir = path.join(logsDir, runDir);
    if (!fs.statSync(fullRunDir).isDirectory()) continue;
    const phaseDirs = fs.readdirSync(fullRunDir).filter((name) => name.startsWith('phase2-'));
    for (const phaseDir of phaseDirs) {
      const brief = path.join(fullRunDir, phaseDir, 'phase2-editorial-briefs.json');
      if (fs.existsSync(brief)) {
        candidates.push({ file: brief, mtime: fs.statSync(brief).mtimeMs });
      }
    }
  }
  candidates.sort((a, b) => b.mtime - a.mtime);
  return candidates.length ? candidates[0].file : preferred;
}

function readJsonIfExists(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function tailLine(text) {
  const lines = String(text || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  return lines.length ? lines[lines.length - 1] : '';
}

function loadConfig() {
  const defaults = {
    workflow_v2: {
      script: path.join(WORKSPACE_ROOT, 'scripts', 'run_topic_material_workflow_v2.py'),
      python_bin: path.join(WORKSPACE_ROOT, '.venv-material', 'bin', 'python'),
      default_brief_json: path.join(
        findLatestBriefJson()
      ),
      default_topic_rank: 8,
      cookie_mode: 'cdp',
      cookie_file: path.join(WORKSPACE_ROOT, '.runtime', 'cookies', 'cdp-cookies.txt'),
      timeout_ms: 5400000,
    },
    quality_policy: {
      min_related_raw: 3,
      min_search_raw: 3,
      min_related_clips: 3,
      min_search_clips: 5,
      filename_reject_keywords: [
        'podcast', 'interview', 'talking', 'talk', 'vlog', 'dialog', 'reaction',
        '访谈', '口播', '对谈', '字幕'
      ]
    }
  };

  if (!fs.existsSync(CONFIG_FILE)) return defaults;

  const custom = readJsonIfExists(CONFIG_FILE) || {};
  return {
    ...defaults,
    ...custom,
    workflow_v2: {
      ...defaults.workflow_v2,
      ...(custom.workflow_v2 || {})
    },
    quality_policy: {
      ...defaults.quality_policy,
      ...(custom.quality_policy || {})
    }
  };
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2).replace(/-/g, '_');
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function summarizeQuality(report, videoSources, qualityPolicy) {
  const counts = (report && report.counts) || {};
  const selected = (videoSources && videoSources.selected_files) || {};

  const searchRaw = selected.search_raw || [];
  const relatedRaw = selected.related_raw || [];
  const rejects = qualityPolicy.filename_reject_keywords || [];

  const warnings = [];

  if ((counts.related_raw_videos || 0) < qualityPolicy.min_related_raw) {
    warnings.push(`related_raw_videos 低于阈值 ${qualityPolicy.min_related_raw}`);
  }
  if ((counts.search_raw_videos || 0) < qualityPolicy.min_search_raw) {
    warnings.push(`search_raw_videos 低于阈值 ${qualityPolicy.min_search_raw}`);
  }
  if ((counts.related_clips || 0) < qualityPolicy.min_related_clips) {
    warnings.push(`related_clips 低于阈值 ${qualityPolicy.min_related_clips}`);
  }
  if ((counts.search_clips || 0) < qualityPolicy.min_search_clips) {
    warnings.push(`search_clips 低于阈值 ${qualityPolicy.min_search_clips}`);
  }

  const filenameHits = [];
  for (const file of [...searchRaw, ...relatedRaw]) {
    const base = path.basename(String(file)).toLowerCase();
    for (const keyword of rejects) {
      if (base.includes(String(keyword).toLowerCase())) {
        filenameHits.push({ file, keyword });
      }
    }
  }
  if (filenameHits.length > 0) {
    warnings.push(`发现命中拒绝关键词的文件名 ${filenameHits.length} 个`);
  }

  return {
    pass: warnings.length === 0,
    warnings,
    filename_reject_hits: filenameHits,
    search_raw_files: searchRaw,
    related_raw_files: relatedRaw,
    query_preview: (videoSources && videoSources.queries ? videoSources.queries.slice(0, 4) : []).map((item) => {
      const seed = item.seed_text || item.anchor_text || '';
      const q = (item.queries || [])[0] || '';
      return { seed, query: q };
    })
  };
}

function runWorkflow(options = {}) {
  const config = loadConfig();
  const workflow = config.workflow_v2;

  const briefJson = options.brief_json || workflow.default_brief_json;
  const topicRank = Number(options.topic_rank || workflow.default_topic_rank || 8);
  const cookieMode = options.cookie_mode || workflow.cookie_mode || 'cdp';
  const cookieFile = options.cookie_file || workflow.cookie_file;
  const pythonBin = options.python_bin || workflow.python_bin;
  const script = options.script || workflow.script;

  const args = [
    script,
    '--brief-json', briefJson,
    '--topic-rank', String(topicRank),
    '--cookie-mode', String(cookieMode),
    '--cookie-file', String(cookieFile),
  ];

  if (options.output_root) {
    args.push('--output-root', String(options.output_root));
  }
  if (options.max_auto_anchors) {
    args.push('--max-auto-anchors', String(options.max_auto_anchors));
  }
  if (options.tushare_token) {
    args.push('--tushare-token', String(options.tushare_token));
  }

  const proc = spawnSync(pythonBin, args, {
    cwd: WORKSPACE_ROOT,
    encoding: 'utf8',
    timeout: Number(workflow.timeout_ms || 5400000),
    env: process.env,
  });

  const outputRoot = tailLine(proc.stdout);
  const reportFile = outputRoot ? path.join(outputRoot, 'manifest', 'report.json') : null;
  const videoSourcesFile = outputRoot ? path.join(outputRoot, 'manifest', 'video-search-sources.json') : null;
  const report = reportFile && fs.existsSync(reportFile) ? readJsonIfExists(reportFile) : null;
  const videoSources = videoSourcesFile && fs.existsSync(videoSourcesFile) ? readJsonIfExists(videoSourcesFile) : null;

  return {
    command: [pythonBin, ...args],
    exit_code: proc.status,
    stdout: proc.stdout,
    stderr: proc.stderr,
    output_root: outputRoot,
    report_file: reportFile,
    video_sources_file: videoSourcesFile,
    report,
    video_sources: videoSources,
    success: proc.status === 0 && Boolean(report),
    quality_summary: summarizeQuality(report, videoSources, config.quality_policy),
  };
}

async function buildReusableFootageMaterial(options = {}) {
  const result = runWorkflow(options);
  if (!result.success) {
    const error = new Error('reusable-footage-material workflow failed');
    error.result = result;
    throw error;
  }

  return {
    success: true,
    skill: 'reusable-footage-material',
    output_root: result.output_root,
    report_file: result.report_file,
    video_sources_file: result.video_sources_file,
    counts: (result.report && result.report.counts) || {},
    search_channels: (result.report && result.report.search_channels) || {},
    auth_policy: (result.report && result.report.auth_policy) || {},
    quality_summary: result.quality_summary,
    notes: [
      '该技能默认启用 CDP cookies（9222）',
      '搜索优先资料片/纪录片/archive footage，规避口播/访谈/播客倾向',
      '可在 config.json 调整检索阈值与拒绝关键词'
    ]
  };
}

if (require.main === module) {
  const options = parseArgs(process.argv.slice(2));
  buildReusableFootageMaterial(options)
    .then((result) => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch((error) => {
      const payload = {
        success: false,
        message: error.message,
      };
      if (error.result) {
        payload.result = {
          exit_code: error.result.exit_code,
          output_root: error.result.output_root,
          report_file: error.result.report_file,
          stderr_tail: String(error.result.stderr || '').split(/\r?\n/).slice(-30),
        };
      }
      console.error(JSON.stringify(payload, null, 2));
      process.exit(1);
    });
}

module.exports = {
  buildReusableFootageMaterial,
  runWorkflow,
};

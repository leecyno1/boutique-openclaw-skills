#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const {
  nowIso,
  readJsonIfExists,
  writeJson,
  markStepCompleted,
  markStepFailed,
  updateManifest
} = require('../dasheng-daily-shared/runtime/manifest');
const { appendArtifactRef } = require('../dasheng-daily-shared/runtime/artifact-store');

const WORKSPACE = '/Users/lichengyin/clawd';
const RUNTIME_DIR = path.join(WORKSPACE, 'skills', 'dasheng-daily-shared', 'runtime-data');
const SKILL_CONFIG_FILE = path.join(__dirname, 'config.json');
const DEFAULT_PHASE2_SCRIPT = path.join(WORKSPACE, 'scripts', 'phase2_rebuilder.py');
const DEFAULT_TOPIC_SPEC_FILE = path.join(WORKSPACE, 'configs', 'phase2', 'topic_specs.v1.json');
const DEFAULT_DOMAIN_TAXONOMY = path.join(WORKSPACE, 'configs', 'phase2', 'domain_taxonomy.v8.json');
const DEFAULT_DETAILED_BRIEF_SCRIPT = path.join(__dirname, 'scripts', 'build_detailed_brief.py');

function fileExists(file) {
  return !!file && fs.existsSync(file);
}

function loadSkillConfig() {
  const defaults = {
    phase2: {
      script: DEFAULT_PHASE2_SCRIPT,
      topic_spec_file: DEFAULT_TOPIC_SPEC_FILE,
      domain_taxonomy: DEFAULT_DOMAIN_TAXONOMY,
      cluster_mode: 'semantic',
      contract_version: 'v8',
      min_count: 1,
      max_clusters: 10,
      top_n: 10,
      cluster_target_min: 8,
      cluster_target_max: 10,
      sa_only: false
    },
    output: {
      subdir: 'phase2',
      brief_markdown: 'phase2-brief-library.md',
      topic_index: 'phase2-topic-index.json',
      editorial_briefs: 'phase2-editorial-briefs.json',
      detailed_brief_markdown: 'phase2-detailed-briefs.md'
    },
    detailed_brief: {
      script: DEFAULT_DETAILED_BRIEF_SCRIPT,
      topic_count_min: 8,
      topic_count_max: 10
    }
  };

  if (!fileExists(SKILL_CONFIG_FILE)) return defaults;

  try {
    const raw = JSON.parse(fs.readFileSync(SKILL_CONFIG_FILE, 'utf8'));
    return {
      ...defaults,
      ...raw,
      phase2: { ...defaults.phase2, ...(raw.phase2 || {}) },
      output: { ...defaults.output, ...(raw.output || {}) },
      detailed_brief: { ...defaults.detailed_brief, ...(raw.detailed_brief || {}) }
    };
  } catch (error) {
    console.warn(`[phase2] config parse failed, fallback to defaults: ${error.message}`);
    return defaults;
  }
}

function discoverLatestIntakeArtifact() {
  const runsDir = path.join(RUNTIME_DIR, 'runs');
  if (!fs.existsSync(runsDir)) return null;

  const runIds = fs.readdirSync(runsDir).sort().reverse();
  for (const runId of runIds) {
    const manifestFile = path.join(runsDir, runId, 'run_manifest.json');
    const manifest = readJsonIfExists(manifestFile);
    if (!manifest) continue;

    const intake = (manifest.artifacts || []).find(
      item => item.step === 'intake' && item.object_type === 'IntakeRecord' && fileExists(item.file)
    );
    if (intake) {
      return { runId, intakeFile: intake.file, manifestFile, manifest };
    }
  }

  return null;
}

function inferRunIdFromFile(inputFile) {
  try {
    const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const list = Array.isArray(data) ? data : data.items;
    const first = Array.isArray(list) && list.length ? list[0] : null;
    if (!first) return null;

    if (first.meta && first.meta.run_id) return first.meta.run_id;
    if (first.run_id) return first.run_id;
  } catch (error) {
    return null;
  }
  return null;
}

function runDetailedBrief(editorialFile, outputDir, config) {
  const script = config.detailed_brief.script || DEFAULT_DETAILED_BRIEF_SCRIPT;
  if (!fileExists(script)) {
    throw new Error(`详细 Brief 脚本不存在: ${script}`);
  }

  const detailedFile = path.join(
    outputDir,
    config.output.detailed_brief_markdown || 'phase2-detailed-briefs.md'
  );

  const args = [
    script,
    editorialFile,
    detailedFile,
    '--topic-count-min',
    String(config.detailed_brief.topic_count_min || 8),
    '--topic-count-max',
    String(config.detailed_brief.topic_count_max || 10)
  ];

  const proc = spawnSync('python3', args, { encoding: 'utf8' });
  if (proc.status !== 0) {
    throw new Error(`详细 Brief 生成失败\nSTDOUT:\n${proc.stdout}\nSTDERR:\n${proc.stderr}`);
  }

  if (!fileExists(detailedFile)) {
    throw new Error(`缺少详细 Brief 文件: ${detailedFile}`);
  }

  let detailedMeta = null;
  try {
    detailedMeta = JSON.parse((proc.stdout || '').trim());
  } catch (error) {
    detailedMeta = null;
  }

  return { detailedFile, detailedMeta };
}

function runPhase2(inputFile, runId, config) {
  const outputDir = path.join(
    RUNTIME_DIR,
    'runs',
    runId,
    'artifacts',
    config.output.subdir || 'phase2'
  );
  fs.mkdirSync(outputDir, { recursive: true });

  const script = config.phase2.script || DEFAULT_PHASE2_SCRIPT;
  const topicSpecFile = config.phase2.topic_spec_file || DEFAULT_TOPIC_SPEC_FILE;
  const domainTaxonomy = config.phase2.domain_taxonomy || DEFAULT_DOMAIN_TAXONOMY;

  const args = [
    script,
    inputFile,
    outputDir,
    '--cluster-mode',
    config.phase2.cluster_mode || 'semantic',
    '--contract-version',
    config.phase2.contract_version || 'v8',
    '--topic-spec-file',
    topicSpecFile,
    '--min-count',
    String(config.phase2.min_count ?? 1),
    '--max-clusters',
    String(config.phase2.max_clusters ?? 10),
    '--top-n',
    String(config.phase2.top_n ?? 10),
    '--run-id',
    runId,
    '--upstream-ref',
    path.basename(inputFile, '.json')
  ];

  if (config.phase2.contract_version === 'v8' && fileExists(domainTaxonomy)) {
    args.push('--domain-taxonomy', domainTaxonomy);
    args.push('--cluster-target-min', String(config.phase2.cluster_target_min ?? 8));
    args.push('--cluster-target-max', String(config.phase2.cluster_target_max ?? 10));
  }

  if (config.phase2.sa_only) {
    args.push('--sa-only');
  }

  const proc = spawnSync('python3', args, { encoding: 'utf8' });
  if (proc.status !== 0) {
    throw new Error(`phase2 执行失败\nSTDOUT:\n${proc.stdout}\nSTDERR:\n${proc.stderr}`);
  }

  const summaryFile = path.join(outputDir, 'phase2-clusters-summary.json');
  const briefFile = path.join(outputDir, config.output.brief_markdown || 'phase2-brief-library.md');
  const editorialFile = path.join(outputDir, config.output.editorial_briefs || 'phase2-editorial-briefs.json');
  const topicIndexFile = path.join(outputDir, config.output.topic_index || 'phase2-topic-index.json');
  const topNFile = path.join(outputDir, 'phase2-topn-for-confirmation.json');

  for (const file of [summaryFile, briefFile, editorialFile, topicIndexFile, topNFile]) {
    if (!fileExists(file)) throw new Error(`缺少 phase2 输出文件: ${file}`);
  }

  const summary = readJsonIfExists(summaryFile);
  const detailed = runDetailedBrief(editorialFile, outputDir, config);

  return {
    outputDir,
    summaryFile,
    briefFile,
    editorialFile,
    topicIndexFile,
    topNFile,
    detailedFile: detailed.detailedFile,
    detailedMeta: detailed.detailedMeta,
    summary,
    stdout: proc.stdout
  };
}

function upsertManifest(manifest, files, stats) {
  let next = appendArtifactRef(manifest, {
    step: 'clustering',
    object_type: 'ClusteredTopic',
    count: stats.cluster_count || 0,
    file: files.summaryFile,
    doc_url: null
  });

  next = appendArtifactRef(next, {
    step: 'brief',
    object_type: 'ContentBrief',
    count: stats.cluster_count || 0,
    file: files.editorialFile,
    doc_url: null
  });

  next = appendArtifactRef(next, {
    step: 'brief',
    object_type: 'BriefMarkdown',
    count: 1,
    file: files.briefFile,
    doc_url: null
  });

  next = appendArtifactRef(next, {
    step: 'brief',
    object_type: 'DetailedBrief',
    count: files?.detailedMeta?.selected_count || 0,
    file: files.detailedFile,
    doc_url: null
  });

  next = appendArtifactRef(next, {
    step: 'brief',
    object_type: 'TopicIndex',
    count: stats.cluster_count || 0,
    file: files.topicIndexFile,
    doc_url: null
  });

  next = markStepCompleted(next, 'clustering');
  next = markStepCompleted(next, 'brief');
  next = updateManifest(next, { current_step: 'outline' });
  return next;
}

async function phase2(intakeFileArg, options = {}) {
  const startedAt = nowIso();
  let manifestFile = null;
  let manifest = null;

  try {
    const config = loadSkillConfig();
    let intakeFile = intakeFileArg || options.intake_records_file || options.input_file;
    let runId = options.run_id || null;

    if (!intakeFile) {
      const latest = discoverLatestIntakeArtifact();
      if (!latest) throw new Error('未找到可用 intake 产物，请先执行 dasheng-daily-intake');
      intakeFile = latest.intakeFile;
      runId = runId || latest.runId;
      manifestFile = latest.manifestFile;
      manifest = latest.manifest;
    }

    if (!fileExists(intakeFile)) {
      throw new Error(`intake 文件不存在: ${intakeFile}`);
    }

    runId = runId || inferRunIdFromFile(intakeFile) || `phase2-${startedAt.slice(0, 19).replace(/[-:T]/g, '')}`;
    manifestFile = manifestFile || path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = manifest || readJsonIfExists(manifestFile);

    const result = runPhase2(intakeFile, runId, config);
    const stats = (result.summary && result.summary.stats) || {};

    if (manifest) {
      const nextManifest = upsertManifest(manifest, result, stats);
      writeJson(manifestFile, nextManifest);
    }

    return {
      success: true,
      run_id: runId,
      intake_file: intakeFile,
      output_dir: result.outputDir,
      summary_file: result.summaryFile,
      brief_file: result.briefFile,
      editorial_file: result.editorialFile,
      topic_index_file: result.topicIndexFile,
      topn_file: result.topNFile,
      detailed_brief_file: result.detailedFile,
      detailed_topics: result?.detailedMeta?.selected_topics || [],
      stats,
      next_step: 'dasheng-daily-outline'
    };
  } catch (error) {
    if (manifest && manifestFile) {
      const nextManifest = markStepFailed(manifest, 'brief', error.message);
      writeJson(manifestFile, nextManifest);
    }
    throw error;
  }
}

if (require.main === module) {
  const intakeFile = process.argv[2];
  phase2(intakeFile)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch(err => {
      console.error(err.message);
      process.exit(1);
    });
}

module.exports = { phase2 };

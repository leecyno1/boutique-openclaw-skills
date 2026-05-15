#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const {
  nowIso,
  readJsonIfExists,
  writeJson,
  sha1,
  markStepCompleted,
  markStepFailed,
  finishManifest
} = require('../dasheng-daily-shared/runtime/manifest');
const {
  persistArtifact,
  appendArtifactRef
} = require('../dasheng-daily-shared/runtime/artifact-store');
const { runWorkflow } = require('../reusable-footage-material/index.js');

const SHARED_DIR = path.join(__dirname, '..', 'dasheng-daily-shared');
const RUNTIME_DIR = path.join(SHARED_DIR, 'runtime-data');
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const SKILL_CONFIG_FILE = path.join(__dirname, 'config.json');
const MATERIAL_WORKFLOW_SCRIPT = path.join(WORKSPACE_ROOT, 'scripts', 'run_topic_material_workflow_v2.py');
const DEFAULT_PYTHON = path.join(WORKSPACE_ROOT, '.venv-material', 'bin', 'python');
const DEFAULT_COOKIE_FILE = path.join(WORKSPACE_ROOT, '.runtime', 'cookies', 'cdp-cookies.txt');
const DEFAULT_PHASE2_RELATIVE = 'phase2-prod-v8-8to10/phase2-editorial-briefs.json';

function readSkillConfig() {
  return readJsonIfExists(SKILL_CONFIG_FILE) || {};
}

function listFilesSafe(dirPath, maxItems = 20) {
  if (!dirPath || !fs.existsSync(dirPath)) return [];
  const names = fs.readdirSync(dirPath).sort();
  return names.slice(0, maxItems).map((name) => path.join(dirPath, name));
}

function tailLine(text) {
  const lines = String(text || '').split(/\r?\n/).map(line => line.trim()).filter(Boolean);
  if (lines.length === 0) return '';
  return lines[lines.length - 1];
}

function deriveTopicRank(brief, index) {
  const candidates = [
    brief?.meta?.id,
    brief?.topic_id,
    brief?.rank,
    brief?.topic_rank
  ].filter(Boolean).map(value => String(value));

  for (const token of candidates) {
    const briefMatch = token.match(/:brief:(\d+)$/);
    if (briefMatch) return Number(briefMatch[1]) + 1;

    const clusterMatch = token.match(/:cluster:(\d+)$/);
    if (clusterMatch) return Number(clusterMatch[1]) + 1;

    if (/^\d+$/.test(token)) {
      const value = Number(token);
      if (value > 0) return value;
      return value + 1;
    }
  }

  return index + 1;
}

function resolvePhase2BriefFile(runId, options, config) {
  const explicit = options.phase2_editorial_briefs_file || config?.workflow_v2?.phase2_editorial_briefs_file;
  const candidates = [];
  if (explicit) candidates.push(path.resolve(explicit));
  candidates.push(path.join(WORKSPACE_ROOT, 'logs', runId, DEFAULT_PHASE2_RELATIVE));
  candidates.push(path.join(WORKSPACE_ROOT, 'logs', runId, 'phase2-prod-v8', 'phase2-editorial-briefs.json'));

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

function findArtifactFile(manifest, step, objectType) {
  const artifacts = Array.isArray(manifest?.artifacts) ? manifest.artifacts : [];
  const match = artifacts.find(item => item.step === step && item.object_type === objectType && item.file && fs.existsSync(item.file));
  return match ? match.file : null;
}

function runWorkflowV2ForRank({ rank, phase2BriefFile, options, config }) {
  const workflowResult = runWorkflow({
    brief_json: phase2BriefFile,
    topic_rank: rank,
    cookie_mode: options.cookie_mode || config?.workflow_v2?.cookie_mode || 'cdp',
    cookie_file: options.cookie_file || config?.workflow_v2?.cookie_file || DEFAULT_COOKIE_FILE,
    python_bin: config?.workflow_v2?.python_bin || DEFAULT_PYTHON,
    script: MATERIAL_WORKFLOW_SCRIPT,
    tushare_token: options.tushare_token || process.env.TUSHARE_TOKEN || config?.workflow_v2?.tushare_token,
  });

  return {
    topic_rank: rank,
    command: workflowResult.command,
    exit_code: workflowResult.exit_code,
    stdout: workflowResult.stdout,
    stderr: workflowResult.stderr,
    output_root: workflowResult.output_root,
    report_file: workflowResult.report_file,
    video_sources_file: workflowResult.video_sources_file,
    report: workflowResult.report,
    video_sources: workflowResult.video_sources,
    quality_summary: workflowResult.quality_summary,
    success: workflowResult.success,
  };
}

function buildMaterialPackPlaceholder(brief, runId, extraGaps = []) {
  const createdAt = nowIso();
  return {
    meta: {
      id: `${runId}:material:${brief.meta.id.split(':').pop()}`,
      object_type: 'MaterialPack',
      run_id: runId,
      version: '3.1.0',
      status: 'ready',
      generated_by: 'dasheng-daily-material',
      input_digest: sha1(brief.meta.id + brief.title),
      upstream_ids: [brief.meta.id],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: brief.topic_id,
    title: brief.title,
    materials: {
      images: [
        { title: `${brief.title} 配图 1`, hint: '趋势图/截图', source_type: 'placeholder' },
        { title: `${brief.title} 配图 2`, hint: '人物/场景图', source_type: 'placeholder' }
      ],
      videos: [
        { title: `${brief.title} 视频素材`, hint: '短视频切片或讲解镜头', source_type: 'placeholder' }
      ],
      quotes: [
        { text: brief.core_claim, source: 'brief.core_claim' },
        { text: (brief.risk_notes || [])[0] || '待补充引用', source: 'brief.risk_notes' }
      ],
      data_points: [
        { label: 'article_value', value: brief?.scorecard?.article_value },
        { label: 'viral_potential', value: brief?.scorecard?.viral_potential },
        { label: 'composite', value: brief?.scorecard?.composite }
      ],
      references: (brief.evidence_requirements || []).map((item, idx) => ({
        title: `evidence_requirement_${idx + 1}`,
        note: item,
        source_type: 'brief_requirement'
      }))
    },
    coverage_notes: [
      `已覆盖主张：${brief.core_claim}`,
      `建议媒介：${(brief.recommended_media || []).join(', ')}`
    ],
    gaps: [
      '缺少真实外部引用抓取',
      '缺少原始截图/图表素材',
      '缺少可直接复用的一手数据源',
      ...extraGaps
    ]
  };
}

function buildMaterialPackFromWorkflow(brief, runId, workflowResult) {
  const createdAt = nowIso();
  const report = workflowResult.report || {};
  const paths = report.paths || {};
  const counts = report.counts || {};

  const networkImages = listFilesSafe(paths.images_network, 12);
  const generatedImages = listFilesSafe(paths.images_generated, 12);
  const chartImages = listFilesSafe(paths.images_data_charts, 20).filter(file => file.endsWith('.png'));

  const relatedRaw = listFilesSafe(paths.videos_related_raw, 30).filter(file => file.endsWith('.mp4'));
  const searchRaw = listFilesSafe(paths.videos_search_raw, 30).filter(file => file.endsWith('.mp4'));
  const relatedClips = listFilesSafe(paths.videos_related_clips, 20).filter(file => file.endsWith('.mp4'));
  const searchClips = listFilesSafe(paths.videos_search_clips, 20).filter(file => file.endsWith('.mp4'));

  const csvFiles = listFilesSafe(paths.charts_csv, 40).filter(file => file.endsWith('.csv'));

  const images = [
    ...networkImages.map(file => ({ title: path.basename(file), source_type: 'network_image', file })),
    ...generatedImages.map(file => ({ title: path.basename(file), source_type: 'ai_infographic', file })),
    ...chartImages.map(file => ({ title: path.basename(file), source_type: 'data_chart', file }))
  ];

  const videos = [
    ...relatedRaw.map(file => ({ title: path.basename(file), source_type: 'related_raw', file })),
    ...searchRaw.map(file => ({ title: path.basename(file), source_type: 'search_raw', file })),
    ...relatedClips.map(file => ({ title: path.basename(file), source_type: 'related_clip', file })),
    ...searchClips.map(file => ({ title: path.basename(file), source_type: 'search_clip', file }))
  ];

  const dataPoints = [
    { label: 'auto_anchors', value: counts.auto_anchors },
    { label: 'manual_anchors', value: counts.manual_anchors },
    { label: 'related_raw_videos', value: counts.related_raw_videos },
    { label: 'search_raw_videos', value: counts.search_raw_videos },
    { label: 'related_clips', value: counts.related_clips },
    { label: 'search_clips', value: counts.search_clips },
    { label: 'network_images', value: counts.network_images },
    { label: 'generated_infographics', value: counts.generated_infographics },
    { label: 'data_chart_images', value: counts.data_chart_images },
    { label: 'csv_files', value: counts.csv_files },
    { label: 'article_value', value: brief?.scorecard?.article_value },
    { label: 'viral_potential', value: brief?.scorecard?.viral_potential },
    { label: 'composite', value: brief?.scorecard?.composite }
  ].filter(item => item.value !== undefined);

  const references = [
    ...csvFiles.map(file => ({ title: path.basename(file), note: 'chart_csv', source_type: 'csv', file })),
    ...((brief.evidence_requirements || []).map((item, idx) => ({
      title: `evidence_requirement_${idx + 1}`,
      note: item,
      source_type: 'brief_requirement'
    })))
  ];

  if (workflowResult.video_sources_file) {
    references.push({
      title: 'video-search-sources',
      note: '视频检索来源与查询词审计',
      source_type: 'video_source_audit',
      file: workflowResult.video_sources_file,
    });
  }

  const qualitySummary = workflowResult.quality_summary || {};
  const gaps = [];
  if ((counts.related_clips || 0) < 3) gaps.push('链接下载线 clips 未达到目标 >=3');
  if ((counts.search_clips || 0) < 5) gaps.push('搜索下载线 clips 未达到目标 >=5');
  if ((counts.data_chart_images || 0) < 5) gaps.push('数据图数量低于目标 5');
  if (Array.isArray(qualitySummary.warnings) && qualitySummary.warnings.length > 0) {
    gaps.push(...qualitySummary.warnings.map(item => `质量检查: ${item}`));
  }

  return {
    meta: {
      id: `${runId}:material:${brief.meta.id.split(':').pop()}`,
      object_type: 'MaterialPack',
      run_id: runId,
      version: '3.1.0',
      status: 'ready',
      generated_by: 'dasheng-daily-material',
      input_digest: sha1(brief.meta.id + brief.title + (report.output_root || '')),
      upstream_ids: [brief.meta.id],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: brief.topic_id,
    title: brief.title,
    workflow_v2: {
      output_root: report.output_root,
      report_file: workflowResult.report_file,
      video_sources_file: workflowResult.video_sources_file,
      article_with_assets: paths.article_with_assets,
      auth_policy: report.auth_policy || {},
      search_channels: report.search_channels || {},
      quality_summary: qualitySummary,
    },
    materials: {
      images,
      videos,
      quotes: [
        { text: brief.core_claim, source: 'brief.core_claim' },
        { text: (brief.risk_notes || [])[0] || '待补充引用', source: 'brief.risk_notes' }
      ],
      data_points: dataPoints,
      references,
      text_sources: (brief.evidence_items || []).map((item, idx) => ({
        title: item.title || `evidence_${idx + 1}`,
        url: item.url || '',
        source_type: 'evidence_item'
      })),
      video_tasks: [
        { lane: 'related', target_min_clips: 3, actual: counts.related_clips || 0 },
        { lane: 'search', target_min_clips: 5, actual: counts.search_clips || 0 }
      ],
    },
    coverage_notes: [
      `已覆盖主张：${brief.core_claim}`,
      `建议媒介：${(brief.recommended_media || []).join(', ')}`,
      ...(qualitySummary.pass === false ? ['已触发素材质量警告，请优先查看 quality_summary 与 video-search-sources 审计。'] : []),
      ...(report.notes || [])
    ],
    gaps
  };
}

async function supplementMaterial(contentBriefsFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    let briefsFile = contentBriefsFile || options.content_briefs_file;
    let runId = options.run_id || null;

    if (briefsFile && !fs.existsSync(briefsFile)) {
      throw new Error(`content_briefs_file 不存在: ${briefsFile}`);
    }

    if (!briefsFile) {
      if (!runId) {
        throw new Error('缺少 content_briefs_file，且未提供 run_id 供自动回溯');
      }
      manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
      manifest = readJsonIfExists(manifestFile);
      if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);
      briefsFile = findArtifactFile(manifest, 'brief', 'ContentBrief');
      if (!briefsFile) {
        throw new Error(`无法在 manifest 中定位 ContentBrief 产物: run_id=${runId}`);
      }
    }

    const briefs = JSON.parse(fs.readFileSync(briefsFile, 'utf8'));
    runId = runId || briefs?.[0]?.meta?.run_id;
    if (!runId) throw new Error('无法从 ContentBrief 推断 run_id');

    if (!manifest || !manifestFile) {
      manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
      manifest = readJsonIfExists(manifestFile);
    }
    if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

    console.log(`[material] 开始补充素材 run_id=${runId}`);

    const config = readSkillConfig();
    const workflowEnabled = options.workflow_v2_enabled ?? config?.workflow_v2?.enabled ?? true;
    const phase2BriefFile = resolvePhase2BriefFile(runId, options, config);

    const workflowResults = [];
    const materialPacks = [];

    if (workflowEnabled && fs.existsSync(MATERIAL_WORKFLOW_SCRIPT) && phase2BriefFile) {
      console.log(`[material] workflow_v2 已启用，phase2 briefs: ${phase2BriefFile}`);

      for (let index = 0; index < briefs.length; index += 1) {
        const brief = briefs[index];
        const topicRank = deriveTopicRank(brief, index);
        console.log(`[material] 处理 topic_rank=${topicRank} title=${brief.title}`);

        const result = runWorkflowV2ForRank({ rank: topicRank, phase2BriefFile, options, config });
        workflowResults.push({
          brief_id: brief?.meta?.id,
          title: brief?.title,
          ...result
        });

        if (result.success) {
          materialPacks.push(buildMaterialPackFromWorkflow(brief, runId, result));
          continue;
        }

        materialPacks.push(buildMaterialPackPlaceholder(brief, runId, [
          `workflow_v2 执行失败 topic_rank=${topicRank}`
        ]));
      }
    } else {
      const reason = !workflowEnabled
        ? 'workflow_v2 disabled'
        : !fs.existsSync(MATERIAL_WORKFLOW_SCRIPT)
          ? `missing script: ${MATERIAL_WORKFLOW_SCRIPT}`
          : `phase2 briefs not found for run_id=${runId}`;

      console.warn(`[material] 走占位模式，原因: ${reason}`);
      for (const brief of briefs) {
        materialPacks.push(buildMaterialPackPlaceholder(brief, runId, [`占位模式原因: ${reason}`]));
      }
    }

    const resultFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'material',
      name: 'material-packs.json',
      data: materialPacks
    });

    manifest = appendArtifactRef(manifest, {
      step: 'material',
      object_type: 'MaterialPack',
      count: materialPacks.length,
      file: resultFile,
      doc_url: null
    });

    let workflowResultFile = null;
    if (workflowResults.length > 0) {
      workflowResultFile = persistArtifact({
        baseDir: RUNTIME_DIR,
        runId,
        step: 'material',
        name: 'material-workflow-v2-results.json',
        data: workflowResults
      });

      manifest = appendArtifactRef(manifest, {
        step: 'material',
        object_type: 'MaterialWorkflowRun',
        count: workflowResults.length,
        file: workflowResultFile,
        doc_url: null
      });
    }

    manifest = markStepCompleted(manifest, 'material');
    manifest.current_step = 'postmortem';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    console.log(`[material] 完成，共 ${materialPacks.length} 个素材包`);
    return {
      success: true,
      run_id: runId,
      total_packs: materialPacks.length,
      material_packs_file: resultFile,
      material_workflow_runs_file: workflowResultFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-postmortem'
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'material', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[material] 错误:', error.message);
    throw error;
  }
}

if (require.main === module) {
  const contentBriefsFile = process.argv[2];
  supplementMaterial(contentBriefsFile).then((result) => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }).catch(() => process.exit(1));
}

module.exports = {
  supplementMaterial,
  deriveTopicRank,
  resolvePhase2BriefFile,
  runWorkflowV2ForRank,
  buildMaterialPackFromWorkflow,
  buildMaterialPackPlaceholder
};

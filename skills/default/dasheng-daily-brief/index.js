#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
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

const SHARED_DIR = path.join(__dirname, '..', 'dasheng-daily-shared');
const RUNTIME_DIR = path.join(SHARED_DIR, 'runtime-data');

/**
 * dasheng-daily-brief
 * v3.0: 读取 ClusteredTopic，输出标准 ContentBrief，去掉随机评分
 */

async function generateBrief(clusteredTopicsFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    const topicsFile = clusteredTopicsFile || options.clustered_topics_file;
    if (!topicsFile || !fs.existsSync(topicsFile)) {
      throw new Error('缺少 clustered_topics_file');
    }

    const topics = JSON.parse(fs.readFileSync(topicsFile, 'utf8'));
    const runId = options.run_id || topics?.[0]?.meta?.run_id;
    if (!runId) throw new Error('无法从 ClusteredTopic 推断 run_id');

    manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = readJsonIfExists(manifestFile);
    if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

    console.log(`[brief] 开始生成 Brief run_id=${runId}`);

    const briefs = topics.map(topic => buildContentBrief(topic, runId));
    const resultFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'brief',
      name: 'content-briefs.json',
      data: briefs
    });

    manifest = appendArtifactRef(manifest, {
      step: 'brief',
      object_type: 'ContentBrief',
      count: briefs.length,
      file: resultFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'brief');
    manifest.current_step = 'material';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    console.log(`[brief] 完成，共 ${briefs.length} 条 Brief`);
    return {
      success: true,
      run_id: runId,
      total_briefs: briefs.length,
      content_briefs_file: resultFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-material'
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'brief', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[brief] 错误:', error.message);
    throw error;
  }
}

function buildContentBrief(topic, runId) {
  const createdAt = nowIso();
  const scorecard = scoreTopic(topic);

  return {
    meta: {
      id: `${runId}:brief:${topic.meta.id.split(':').pop()}`,
      object_type: 'ContentBrief',
      run_id: runId,
      version: '3.0.0',
      status: 'ready',
      generated_by: 'dasheng-daily-brief',
      input_digest: sha1(topic.meta.id + JSON.stringify(topic.candidate_titles || [])),
      upstream_ids: [topic.meta.id],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: topic.meta.id,
    title: topic.candidate_titles?.[0] || topic.cluster_label,
    core_claim: `${topic.cluster_label} 方向值得进入内容生产，核心母题：${topic.thesis}`,
    angle_candidates: [
      `从 ${topic.cluster_label} 的共性切入，提炼统一判断`,
      `从代表样本切入，构建更强叙事主线`
    ],
    risk_notes: [
      '当前仍是规则评分，后续需接入真实 evidence 与 postmortem 回写',
      '按来源分桶只是过渡实现，后续应替换为真实语义聚类'
    ],
    evidence_requirements: [
      '补充一手数据或原文截图',
      '确认是否存在时效性变化',
      '确认核心观点是否可证伪'
    ],
    recommended_media: recommendMedia(scorecard),
    scorecard
  };
}

function scoreTopic(topic) {
  const titleCount = (topic.candidate_titles || []).length;
  const sourceBreadth = (topic.representative_intake_ids || []).length;
  const confidence = Number(topic.confidence || 0.6);

  const articleValue = clamp(Math.round(confidence * 100) + sourceBreadth * 4 + (topic.quality_tier === 'A' ? 8 : 0), 0, 100);
  const viralPotential = clamp(Math.round(confidence * 100) + titleCount * 5 + (topic.cluster_label.includes('wechat') ? 6 : 2), 0, 100);
  const composite = Math.round(articleValue * 0.5 + viralPotential * 0.5);

  return {
    article_value: articleValue,
    viral_potential: viralPotential,
    composite,
    score_reasoning: `confidence=${confidence}; sourceBreadth=${sourceBreadth}; titleCount=${titleCount}; quality=${topic.quality_tier || 'N/A'}`
  };
}

function recommendMedia(scorecard) {
  const media = [];
  if (scorecard.article_value >= 75) media.push('long-form');
  if (scorecard.viral_potential >= 75) media.push('short-video');
  if (!media.length) media.push('social-post');
  return media;
}

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

if (require.main === module) {
  const clusteredTopicsFile = process.argv[2];
  generateBrief(clusteredTopicsFile).then(() => process.exit(0)).catch(() => process.exit(1));
}

module.exports = { generateBrief, buildContentBrief, scoreTopic };

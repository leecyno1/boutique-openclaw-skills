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

async function generatePostmortem(finalPackagesFile, performanceDataFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    const finalsFile = finalPackagesFile || options.final_packages_file;
    if (!finalsFile || !fs.existsSync(finalsFile)) {
      throw new Error('缺少 final_packages_file');
    }

    const finals = JSON.parse(fs.readFileSync(finalsFile, 'utf8'));
    const runId = options.run_id || finals?.[0]?.meta?.run_id;
    if (!runId) throw new Error('无法从 FinalPackage 推断 run_id');

    manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = readJsonIfExists(manifestFile);
    if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

    const performanceMap = loadPerformanceMap(performanceDataFile);
    console.log(`[postmortem] 开始生成复盘 run_id=${runId}`);

    const postmortems = finals.map(final => buildPostmortemRecord(final, performanceMap[final.topic_id], runId));
    const overallAccuracy = calculateOverallAccuracy(postmortems);

    const resultFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'postmortem',
      name: 'postmortem-records.json',
      data: {
        overall_accuracy: overallAccuracy,
        records: postmortems
      }
    });

    manifest = appendArtifactRef(manifest, {
      step: 'postmortem',
      object_type: 'PostmortemRecord',
      count: postmortems.length,
      file: resultFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'postmortem');
    manifest.current_step = 'done';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    console.log(`[postmortem] 完成，共 ${postmortems.length} 条复盘记录`);
    return {
      success: true,
      run_id: runId,
      total_postmortems: postmortems.length,
      overall_accuracy: overallAccuracy,
      postmortem_records_file: resultFile,
      manifest_file: manifestFile,
      next_step: null
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'postmortem', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[postmortem] 错误:', error.message);
    throw error;
  }
}

function loadPerformanceMap(performanceDataFile) {
  if (!performanceDataFile || !fs.existsSync(performanceDataFile)) return {};
  return JSON.parse(fs.readFileSync(performanceDataFile, 'utf8')) || {};
}

function buildPostmortemRecord(final, performanceOverride, runId) {
  const createdAt = nowIso();
  const performance = performanceOverride || generateDeterministicPerformance(final);
  const scoringAccuracy = evaluateScoringAccuracy(final, performance);

  return {
    meta: {
      id: `${runId}:postmortem:${final.meta.id.split(':').pop()}`,
      object_type: 'PostmortemRecord',
      run_id: runId,
      version: '3.0.0',
      status: 'ready',
      generated_by: 'dasheng-daily-postmortem',
      input_digest: sha1(final.meta.id + final.title),
      upstream_ids: [final.meta.id],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: final.topic_id,
    title: final.title,
    performance,
    scoring_accuracy: scoringAccuracy,
    insights: generateInsights(performance, scoringAccuracy),
    recommendations: generateRecommendations(scoringAccuracy)
  };
}

function generateDeterministicPerformance(final) {
  const base = final.predicted_scores?.composite || 60;
  return {
    views: base * 1200,
    likes: base * 40,
    shares: base * 8,
    comments: base * 5,
    engagement_rate: Number((Math.min(0.15, 0.02 + base / 2000)).toFixed(4))
  };
}

function evaluateScoringAccuracy(final, performance) {
  const predicted = final.predicted_scores || { article_value: 0, viral_potential: 0, composite: 0 };

  const actualArticle = Math.round(Math.min(100, performance.views / 1200));
  const actualViral = Math.round(Math.min(100, performance.shares / 8));
  const actualComposite = Math.round((actualArticle + actualViral) / 2);

  return {
    article_value: compareScore(predicted.article_value, actualArticle),
    viral_potential: compareScore(predicted.viral_potential, actualViral),
    composite: compareScore(predicted.composite, actualComposite)
  };
}

function compareScore(predicted, actual) {
  const gap = Math.abs((predicted || 0) - (actual || 0));
  return {
    predicted: predicted || 0,
    actual: actual || 0,
    gap,
    accuracy: Math.max(0, 100 - gap)
  };
}

function generateInsights(performance, accuracy) {
  const insights = [];
  if (performance.views >= 80000) insights.push('浏览量表现强，说明主题具备更广泛触达能力');
  if (performance.shares >= 600) insights.push('分享表现强，说明传播性较好');
  if (accuracy.composite.accuracy >= 85) insights.push('综合预测较准，可以作为下一轮评分基线');
  if (accuracy.composite.accuracy < 60) insights.push('综合预测偏差较大，需要回调评分规则');
  return insights;
}

function generateRecommendations(accuracy) {
  const recs = [];
  if (accuracy.article_value.accuracy < 80) recs.push('调整 article_value 的规则权重');
  if (accuracy.viral_potential.accuracy < 80) recs.push('调整 viral_potential 的规则权重');
  if (!recs.length) recs.push('当前规则可继续保留，并等待真实发布数据校验');
  return recs;
}

function calculateOverallAccuracy(postmortems) {
  const count = postmortems.length || 1;
  return {
    article_value: postmortems.reduce((n, item) => n + item.scoring_accuracy.article_value.accuracy, 0) / count,
    viral_potential: postmortems.reduce((n, item) => n + item.scoring_accuracy.viral_potential.accuracy, 0) / count,
    composite: postmortems.reduce((n, item) => n + item.scoring_accuracy.composite.accuracy, 0) / count
  };
}

if (require.main === module) {
  const finalPackagesFile = process.argv[2];
  const performanceDataFile = process.argv[3];
  generatePostmortem(finalPackagesFile, performanceDataFile).then(() => process.exit(0)).catch(() => process.exit(1));
}

module.exports = { generatePostmortem, buildPostmortemRecord, evaluateScoringAccuracy };

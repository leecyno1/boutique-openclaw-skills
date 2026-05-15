#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {
  nowIso,
  runDateFromIso,
  makeRunId,
  createManifest,
  markStepCompleted,
  markStepFailed,
  finishManifest,
  writeJson,
  sha1
} = require('../dasheng-daily-shared/runtime/manifest');
const {
  persistArtifact,
  appendArtifactRef
} = require('../dasheng-daily-shared/runtime/artifact-store');

const SKILL_DIR = __dirname;
const SHARED_DIR = path.join(__dirname, '..', 'dasheng-daily-shared');
const RUNTIME_DIR = path.join(SHARED_DIR, 'runtime-data');

/**
 * dasheng-daily-intake
 * v3.0: 输出标准 IntakeRecord + run_manifest + artifact 持久化
 */

async function intake(options = {}) {
  const startedAt = nowIso();
  const runId = options.run_id || makeRunId('dasheng-daily', startedAt);
  const runDate = options.run_date || runDateFromIso(startedAt);
  const manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');

  let manifest = createManifest({
    workflowName: 'dasheng-daily',
    workflowVersion: '3.0.0',
    runId,
    runDate,
    currentStep: 'intake',
    folder: {
      token: null,
      url: null,
      name: runDate
    }
  });

  try {
    console.log(`[intake] 开始数据采集 run_id=${runId}`);

    const rawData = {
      timestamp: startedAt,
      sources: {
        mediacrawler: await fetchMediaCrawler(),
        wechat_subscription: await fetchWechatSubscription(),
        news_crawler: await fetchNewsCrawler()
      }
    };

    const intakeRecords = buildIntakeRecords(rawData, runId);
    const sourceCounts = summarizeBySource(intakeRecords);

    const rawDataFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'intake',
      name: 'raw-data.json',
      data: rawData
    });

    const recordsFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'intake',
      name: 'intake-records.json',
      data: intakeRecords
    });

    manifest = appendArtifactRef(manifest, {
      step: 'intake',
      object_type: 'raw_data',
      count: Object.values(rawData.sources).reduce((n, arr) => n + (arr?.length || 0), 0),
      file: rawDataFile,
      doc_url: null
    });

    manifest = appendArtifactRef(manifest, {
      step: 'intake',
      object_type: 'IntakeRecord',
      count: intakeRecords.length,
      file: recordsFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'intake');
    manifest.current_step = 'clustering';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    const result = {
      success: true,
      run_id: runId,
      run_date: runDate,
      total_items: intakeRecords.length,
      source_counts: sourceCounts,
      raw_data_file: rawDataFile,
      intake_records_file: recordsFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-clustering'
    };

    console.log(`[intake] 完成，共 ${intakeRecords.length} 条，manifest=${manifestFile}`);
    return result;
  } catch (error) {
    manifest = markStepFailed(manifest, 'intake', error.message);
    writeJson(manifestFile, manifest);
    console.error('[intake] 错误:', error.message);
    throw error;
  }
}

function buildIntakeRecords(rawData, runId) {
  const items = [];
  const createdAt = nowIso();

  for (const [source, arr] of Object.entries(rawData.sources || {})) {
    for (const item of arr || []) {
      const normalizedText = [item.title, item.summary || '', source].join('\n').trim();
      items.push({
        meta: {
          id: `${runId}:intake:${item.id}`,
          object_type: 'IntakeRecord',
          run_id: runId,
          version: '3.0.0',
          status: 'ready',
          generated_by: 'dasheng-daily-intake',
          input_digest: sha1(normalizedText),
          upstream_ids: [],
          doc_refs: [],
          created_at: createdAt,
          updated_at: createdAt
        },
        source,
        source_item_id: item.id,
        title: item.title,
        summary: item.summary || null,
        normalized_text: normalizedText,
        dedupe_fingerprint: sha1(`${source}:${item.title}`),
        freshness_score: 0.7,
        engagement_score: 0.5,
        tags: item.tags || [],
        raw_payload: item
      });
    }
  }

  return items;
}

function summarizeBySource(records) {
  return records.reduce((acc, item) => {
    acc[item.source] = (acc[item.source] || 0) + 1;
    return acc;
  }, {});
}

async function fetchMediaCrawler() {
  return [
    { id: 'mc_1', title: '媒体新闻 1', source: 'mediacrawler', timestamp: Date.now() },
    { id: 'mc_2', title: '媒体新闻 2', source: 'mediacrawler', timestamp: Date.now() }
  ];
}

async function fetchWechatSubscription() {
  return [
    { id: 'wx_1', title: '公众号文章 1', source: 'wechat_subscription', timestamp: Date.now() },
    { id: 'wx_2', title: '公众号文章 2', source: 'wechat_subscription', timestamp: Date.now() }
  ];
}

async function fetchNewsCrawler() {
  return [
    { id: 'news_1', title: '新闻 1', source: 'news_crawler', timestamp: Date.now() },
    { id: 'news_2', title: '新闻 2', source: 'news_crawler', timestamp: Date.now() }
  ];
}

if (require.main === module) {
  intake().then(() => process.exit(0)).catch(() => process.exit(1));
}

module.exports = { intake, buildIntakeRecords };

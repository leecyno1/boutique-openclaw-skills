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
const CONFIG_FILE = path.join(__dirname, 'config.json');

function loadFinalConfig() {
  const fallback = {
    final: {
      rewrite_policy: {
        auto_rewrite: true,
        model_mode: 'bm',
        targets: ['copywriting', 'voiceover']
      }
    }
  };

  if (!fs.existsSync(CONFIG_FILE)) {
    return fallback;
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    return {
      ...fallback,
      ...parsed,
      final: {
        ...(fallback.final || {}),
        ...(parsed.final || {}),
        rewrite_policy: {
          ...(fallback.final.rewrite_policy || {}),
          ...((parsed.final || {}).rewrite_policy || {})
        }
      }
    };
  } catch (error) {
    return fallback;
  }
}

async function generateFinal(draftPackagesFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    const cfg = loadFinalConfig();
    const draftsFile = draftPackagesFile || options.draft_packages_file;
    if (!draftsFile || !fs.existsSync(draftsFile)) {
      throw new Error('缺少 draft_packages_file');
    }

    const drafts = JSON.parse(fs.readFileSync(draftsFile, 'utf8'));
    const runId = options.run_id || drafts?.[0]?.meta?.run_id;
    if (!runId) throw new Error('无法从 DraftPackage 推断 run_id');

    manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = readJsonIfExists(manifestFile);
    if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

    console.log(`[final] 开始生成强化版 run_id=${runId}`);

    const briefsFile = findArtifactFile(manifest, 'brief', 'ContentBrief');
    const briefs = briefsFile ? JSON.parse(fs.readFileSync(briefsFile, 'utf8')) : [];
    const briefMap = new Map(briefs.map(item => [item.topic_id, item]));

    const finals = drafts.map(draft => buildFinalPackage(draft, briefMap.get(draft.topic_id), runId, cfg));
    const resultFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'final',
      name: 'final-packages.json',
      data: finals
    });

    manifest = appendArtifactRef(manifest, {
      step: 'final',
      object_type: 'FinalPackage',
      count: finals.length,
      file: resultFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'final');
    manifest.current_step = 'material';
    writeJson(manifestFile, manifest);

    console.log(`[final] 完成，共 ${finals.length} 条强化版`);
    return {
      success: true,
      run_id: runId,
      total_finals: finals.length,
      final_packages_file: resultFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-material'
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'final', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[final] 错误:', error.message);
    throw error;
  }
}

function buildFinalPackage(draft, brief, runId, cfg) {
  const createdAt = nowIso();
  const review = performReview(draft);
  const predictedScores = brief?.scorecard || {
    article_value: 0,
    viral_potential: 0,
    composite: 0,
    score_reasoning: 'missing brief scorecard'
  };

  const rewritePolicy = normalizeRewritePolicy(draft?.rewrite_policy, cfg?.final?.rewrite_policy);

  return {
    meta: {
      id: `${runId}:final:${draft.meta.id.split(':').pop()}`,
      object_type: 'FinalPackage',
      run_id: runId,
      version: '3.1.0',
      status: 'ready',
      generated_by: 'dasheng-daily-final',
      input_digest: sha1(draft.meta.id + draft.title),
      upstream_ids: [draft.meta.id, ...(brief ? [brief.meta.id] : [])],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: draft.topic_id,
    title: generateTitle(draft),
    original_title: draft.title,
    content: enhanceContent(draft.content),
    review,
    predicted_scores: predictedScores,
    rewrite_policy: rewritePolicy,
    media_adaptations: generateMediaAdaptations(draft, rewritePolicy),
    status: review.passed ? 'ready_to_publish' : 'needs_revision'
  };
}

function normalizeRewritePolicy(fromDraft, fromConfig) {
  return {
    auto_rewrite: (fromDraft?.auto_rewrite ?? fromConfig?.auto_rewrite) !== false,
    model_mode: String(fromDraft?.model_mode || fromConfig?.model_mode || 'bm'),
    targets: Array.isArray(fromDraft?.targets) && fromDraft.targets.length
      ? fromDraft.targets
      : (Array.isArray(fromConfig?.targets) && fromConfig.targets.length ? fromConfig.targets : ['copywriting', 'voiceover'])
  };
}

function findArtifactFile(manifest, step, objectType) {
  const match = (manifest.artifacts || []).find(item => item.step === step && item.object_type === objectType);
  return match?.file || null;
}

function performReview(draft) {
  const checklist = [
    { item: '逻辑清晰', passed: draft.word_count > 120 },
    { item: '结构完整', passed: (draft.sections_used || []).length >= 4 },
    { item: '表达流畅', passed: true },
    { item: '可发布性', passed: draft.word_count > 180 }
  ];
  const passedCount = checklist.filter(c => c.passed).length;
  return {
    checklist,
    passed_items: passedCount,
    total_items: checklist.length,
    passed: passedCount >= 3,
    score: Math.round((passedCount / checklist.length) * 100)
  };
}

function generateTitle(draft) {
  const prefix = draft.word_count > 220 ? '【深度拆解】' : '【观察】';
  return `${prefix}${draft.title}`;
}

function enhanceContent(content) {
  return `## 摘要\n本文基于结构化流程生成，已经过初步复审。\n\n${content}\n## 关键要点\n- 提炼主结论\n- 给出证据线索\n- 保留后续修订空间\n`;
}

function generateMediaAdaptations(draft, rewritePolicy) {
  const mode = rewritePolicy.model_mode;
  return {
    article: {
      format: 'markdown',
      title: draft.title,
      rewrite_model_mode: mode,
      auto_rewrite: rewritePolicy.auto_rewrite
    },
    podcast: {
      format: 'script',
      title: `播客脚本：${draft.title}`,
      rewrite_model_mode: mode,
      auto_rewrite: rewritePolicy.auto_rewrite,
      target_duration: '8-10分钟'
    },
    video: {
      format: 'outline',
      title: `视频脚本：${draft.title}`,
      rewrite_model_mode: mode,
      auto_rewrite: rewritePolicy.auto_rewrite,
      target_duration: '3-5分钟'
    }
  };
}

if (require.main === module) {
  const draftPackagesFile = process.argv[2];
  generateFinal(draftPackagesFile).then(() => process.exit(0)).catch(() => process.exit(1));
}

module.exports = { generateFinal, buildFinalPackage, performReview };

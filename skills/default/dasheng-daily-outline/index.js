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

async function generateOutline(materialPackFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    const packsFile = materialPackFile || options.material_packs_file;
    if (!packsFile || !fs.existsSync(packsFile)) {
      throw new Error('缺少 material_packs_file');
    }

    const packs = JSON.parse(fs.readFileSync(packsFile, 'utf8'));
    const runId = options.run_id || packs?.[0]?.meta?.run_id;
    if (!runId) throw new Error('无法从 MaterialPack 推断 run_id');

    manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = readJsonIfExists(manifestFile);
    if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

    console.log(`[outline] 开始生成大纲 run_id=${runId}`);

    const outlines = packs.map(pack => buildOutlinePlan(pack, runId));
    const resultFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'outline',
      name: 'outline-plans.json',
      data: outlines
    });

    manifest = appendArtifactRef(manifest, {
      step: 'outline',
      object_type: 'OutlinePlan',
      count: outlines.length,
      file: resultFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'outline');
    manifest.current_step = 'draft';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    console.log(`[outline] 完成，共 ${outlines.length} 条大纲`);
    return {
      success: true,
      run_id: runId,
      total_outlines: outlines.length,
      outline_plans_file: resultFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-draft'
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'outline', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[outline] 错误:', error.message);
    throw error;
  }
}

function buildOutlinePlan(pack, runId) {
  const createdAt = nowIso();
  return {
    meta: {
      id: `${runId}:outline:${pack.meta.id.split(':').pop()}`,
      object_type: 'OutlinePlan',
      run_id: runId,
      version: '3.0.0',
      status: 'ready',
      generated_by: 'dasheng-daily-outline',
      input_digest: sha1(pack.meta.id + pack.title),
      upstream_ids: [pack.meta.id],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: pack.topic_id,
    title: pack.title,
    style: 'lemon_dna',
    narrative_goal: '用理性、数据驱动的方式，把主题讲清楚并形成可转写初稿的结构。',
    sections: generateLemonDNAOutline(pack)
  };
}

function generateLemonDNAOutline(pack) {
  return [
    {
      level: 1,
      title: 'Hook',
      content: `以“${pack.title}”的核心矛盾或数据异常开场。`,
      notes: '3-5 句话，先抓注意力'
    },
    {
      level: 1,
      title: 'Context',
      content: '解释这个主题为什么现在值得讲，交代背景和时效性。',
      notes: '结合素材包里的 references/gaps 补边界'
    },
    {
      level: 1,
      title: 'Analysis',
      content: '展开核心分析，用数据点、引用、案例支撑论证。',
      subsections: [
        { title: '观点一', content: (pack.coverage_notes || [])[0] || '提炼主论点' },
        { title: '观点二', content: '对比不同来源或不同立场' },
        { title: '观点三', content: '给出可执行判断或策略含义' }
      ]
    },
    {
      level: 1,
      title: 'Insight',
      content: '收束成 1-2 个真正值得记住的洞察。',
      notes: '避免重复材料层内容'
    },
    {
      level: 1,
      title: 'Call to Action',
      content: '给出下一步观察点、决策建议或互动问题。',
      notes: '可转社媒结尾或口播收束'
    }
  ];
}

if (require.main === module) {
  const materialPackFile = process.argv[2];
  generateOutline(materialPackFile).then(() => process.exit(0)).catch(() => process.exit(1));
}

module.exports = { generateOutline, buildOutlinePlan };

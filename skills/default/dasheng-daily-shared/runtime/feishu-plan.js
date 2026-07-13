#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');
const { readJsonIfExists } = require('./manifest');
const { extractFolderToken } = require('./doc-registry');

const BASE_DIR = path.join(__dirname, '..', 'runtime-data');
const PROJECT_ROOT = path.resolve(__dirname, '..', '..', '..');
const OUTPUT_ROOT = process.env.DASHENG_OUTPUT_ROOT || path.join(os.homedir(), 'Desktop', '自媒体创作');
const CONFIG_FILE = path.join(PROJECT_ROOT, 'configs', 'feishu', 'stage_review_contract.json');

const STAGE_SEQUENCE = ['intake', 'brief', 'draft', 'transwrite', 'publish', 'postmortem'];

const STAGE_META = {
  intake: {
    folderName: '01_内容采集',
    displayName: '内容采集',
    roots: [path.join(OUTPUT_ROOT, '01_内容采集')],
    mainPatterns: [/01_内容采集_底稿\.md$/],
    reportPatterns: [/01_内容采集_报告\.md$/]
  },
  brief: {
    folderName: '02_内容聚合及选题分析',
    displayName: '内容聚合及选题分析',
    roots: [path.join(OUTPUT_ROOT, '02_内容聚合及选题分析')],
    mainPatterns: [/02_编辑Brief库\.md$/, /02_研究Brief库\.md$/, /phase2-brief-library\.md$/],
    reportPatterns: [/02_编辑Brief_报告\.md$/]
  },
  draft: {
    folderName: '03_标准初稿',
    displayName: '标准初稿',
    roots: [path.join(OUTPUT_ROOT, '05_初稿生成')],
    mainPatterns: [/03_标准初稿_.*\.md$/, /04_标准初稿_.*\.md$/, /05_标准初稿_.*\.md$/, /03_标准初稿\.md$/],
    reportPatterns: [/03_初稿_报告\.md$/, /04_初稿_报告\.md$/, /05_初稿生成_报告\.md$/],
    excludeMainPatterns: []
  },
  transwrite: {
    folderName: '04_转写生产',
    displayName: '转写生产',
    roots: [path.join(OUTPUT_ROOT, '06_转写生产')],
    mainPatterns: [/04_转写计划\.md$/, /wechat_article\.final\.md$/, /talking_head_script\.md$/, /podcast_script\.md$/],
    reportPatterns: [/04_转写计划\.md$/],
    excludeMainPatterns: []
  },
  publish: {
    folderName: '05_发布执行',
    displayName: '发布执行',
    roots: [path.join(OUTPUT_ROOT, '07_发布执行')],
    mainPatterns: [/07_发布包\.md$/, /06_发布包\.md$/],
    reportPatterns: [/07_发布计划\.md$/, /06_发布计划\.md$/]
  },
  postmortem: {
    folderName: '06_分析复盘',
    displayName: '分析复盘',
    roots: [path.join(OUTPUT_ROOT, '08_分析复盘')],
    mainPatterns: [/08_复盘报告\.md$/, /07_复盘报告\.md$/],
    reportPatterns: [/08_L1回写建议\.md$/, /07_L1回写建议\.md$/]
  }
};

function ensureArray(value) {
  return Array.isArray(value) ? value : value ? [value] : [];
}

function unique(items = []) {
  return [...new Set(items.filter(Boolean))];
}

function readTextIfExists(file) {
  if (!file || !fs.existsSync(file)) return null;
  return fs.readFileSync(file, 'utf8');
}

function safeStat(file) {
  try {
    return fs.statSync(file);
  } catch {
    return null;
  }
}

function sortPathsNewest(paths = []) {
  return [...paths].sort((left, right) => {
    const rightStat = safeStat(right);
    const leftStat = safeStat(left);
    const rightTime = rightStat ? rightStat.mtimeMs : 0;
    const leftTime = leftStat ? leftStat.mtimeMs : 0;
    if (rightTime !== leftTime) return rightTime - leftTime;
    return path.basename(right).localeCompare(path.basename(left));
  });
}

function collectFiles(dir, depth = 2) {
  if (!dir || !fs.existsSync(dir)) return [];
  const results = [];
  const queue = [{ dir, depth }];
  while (queue.length) {
    const current = queue.shift();
    for (const entry of fs.readdirSync(current.dir, { withFileTypes: true })) {
      const fullPath = path.join(current.dir, entry.name);
      if (entry.isFile()) {
        results.push(fullPath);
      } else if (entry.isDirectory() && current.depth > 0) {
        queue.push({ dir: fullPath, depth: current.depth - 1 });
      }
    }
  }
  return results;
}

function detectRunDate(runId, manifest = null) {
  if (manifest?.run_date) return manifest.run_date;
  const direct = String(runId || '').match(/(\d{4}-\d{2}-\d{2})/);
  if (direct) return direct[1];
  return new Date().toISOString().slice(0, 10);
}

function loadStageReviewContract() {
  const config = readJsonIfExists(CONFIG_FILE);
  if (!config) throw new Error(`飞书阶段配置不存在: ${CONFIG_FILE}`);
  return config;
}

function getRuntimeManifest(runId) {
  const manifestFile = path.join(BASE_DIR, 'runs', runId, 'run_manifest.json');
  return {
    manifestFile,
    manifest: readJsonIfExists(manifestFile)
  };
}

function collectCandidateDirs(root, runId, runDate) {
  if (!root || !fs.existsSync(root)) return [];
  const candidates = [];

  const directRunDir = path.join(root, runId);
  const directDateDir = path.join(root, runDate);
  if (fs.existsSync(directRunDir) && fs.statSync(directRunDir).isDirectory()) candidates.push(directRunDir);
  if (fs.existsSync(directDateDir) && fs.statSync(directDateDir).isDirectory()) candidates.push(directDateDir);

  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const fullPath = path.join(root, entry.name);
    if (entry.name === runId || entry.name === runDate) {
      candidates.push(fullPath);
      continue;
    }
    if (entry.name.includes(runId) || entry.name.startsWith(runDate)) {
      candidates.push(fullPath);
    }
  }

  return sortPathsNewest(unique(candidates));
}

function matchesPatterns(file, patterns = []) {
  return patterns.some(pattern => pattern.test(file));
}

function filterFiles(files, patterns, excludePatterns = []) {
  return files.filter(file => {
    if (!matchesPatterns(file, patterns)) return false;
    if (excludePatterns.some(pattern => pattern.test(file))) return false;
    return true;
  });
}

function discoverStageArtifacts(stage, runId, runDate) {
  const meta = STAGE_META[stage];
  if (!meta) return null;

  const candidateDirs = unique([
    ...ensureArray(meta.roots).flatMap(root => collectCandidateDirs(root, runId, runDate)),
    stage === 'brief' ? path.join(BASE_DIR, 'runs', runId, 'artifacts', 'phase2') : null
  ]).filter(dir => fs.existsSync(dir) && fs.statSync(dir).isDirectory());

  const candidateFiles = sortPathsNewest(unique(candidateDirs.flatMap(dir => collectFiles(dir, 2))));
  const mainFiles = sortPathsNewest(filterFiles(candidateFiles, meta.mainPatterns, meta.excludeMainPatterns || []));
  const reportFiles = sortPathsNewest(filterFiles(candidateFiles, meta.reportPatterns, []));
  const manifestFiles = sortPathsNewest(candidateFiles.filter(file => /manifest\.json$/i.test(file)));
  const assetRoot = [];
  const assetManifestFiles = [];

  return {
    stage,
    candidate_dirs: candidateDirs,
    candidate_files: candidateFiles,
    main_files: mainFiles,
    report_files: reportFiles,
    manifest_files: manifestFiles,
    asset_roots: assetRoot,
    asset_manifest_files: assetManifestFiles
  };
}

function buildCombinedContent(title, stage, role, files, runId, runDate) {
  const existingFiles = files.filter(file => readTextIfExists(file));
  if (!existingFiles.length) return null;
  if (existingFiles.length === 1) return readTextIfExists(existingFiles[0]);

  const sections = existingFiles.map((file, index) => {
    const content = readTextIfExists(file) || '';
    return `## 文件 ${index + 1}：${path.basename(file)}\n\n${content.trim()}`;
  });

  return [
    `# ${title}`,
    '',
    `- stage: \`${stage}\``,
    `- role: \`${role}\``,
    `- run_id: \`${runId}\``,
    `- run_date: \`${runDate}\``,
    `- source_files: ${existingFiles.length}`,
    '',
    sections.join('\n\n---\n\n')
  ].join('\n');
}

function inferDocTitleFromFile(file, fallbackTitle) {
  const content = readTextIfExists(file) || '';
  const heading = content.match(/^#\s+(.+)$/m);
  if (heading && heading[1]) return heading[1].trim();
  return path.basename(file, path.extname(file)) || fallbackTitle;
}

function slugFromFile(file) {
  return path.basename(file, path.extname(file)).replace(/[^a-zA-Z0-9_\-\u4e00-\u9fa5]+/g, '_');
}

function extractSummaryLines(content) {
  if (!content) return [];
  const lines = content
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(Boolean)
    .filter(line => /^[-*]\s+/.test(line) || /^\d+\./.test(line) || /^##\s+/.test(line));
  return lines.slice(0, 4).map(line => line.replace(/^##\s+/, '').trim());
}

function defaultManualReview(stage) {
  const mapping = {
    intake: ['删除噪音条目', '补充漏掉的原始链接', '修正去留建议'],
    brief: ['确认 8-10 个候选题优先级', '强制加入人工指定题', '删改单题结构骨架'],
    draft: ['删减冗余段落', '调整论证顺序', '修正事实或口径'],
    rewrite: ['确认结构继承是否正确', '确认渠道风格是否匹配', '保留或删去 CTA'],
    publish: ['确认标题、封面与发布时间', '确认渠道矩阵与素材齐备状态'],
    postmortem: ['修正结论口径', '确认是否回写知识库', '确认继续 / 停止 / 测试动作']
  };
  return mapping[stage] || [];
}

function stageDisplayName(stage) {
  return STAGE_META[stage]?.displayName || stage;
}

function buildStageMessageBody(stage, actionKeys, summaryLines, reviewLines, runId) {
  const displayName = stageDisplayName(stage);
  const docLinks = actionKeys.map(key => `- {{${key}}}`).join('\n');
  const summary = summaryLines.map(line => `- ${line}`).join('\n') || '- 待编辑团队补充摘要';
  const review = reviewLines.map(line => `- ${line}`).join('\n');
  return [
    `# ${displayName}审核提醒`,
    '',
    `- run_id: \`${runId}\``,
    '',
    '## 核心摘要',
    summary,
    '',
    '## 文档链接',
    docLinks,
    '',
    '## 需要人工介入',
    review
  ].join('\n');
}

function normalizeAnchor(anchorText, index) {
  const idMatch = anchorText.match(/素材锚点-([^-]+)-([0-9]+)/);
  return {
    id: idMatch ? `${idMatch[1]}-${idMatch[2]}` : `anchor-${String(index + 1).padStart(2, '0')}`,
    raw: anchorText
  };
}

function extractRewriteAnchors(content) {
  if (!content) return [];
  const matches = content.match(/\[素材锚点-[^\]]+\]/g) || [];
  return matches.map((item, index) => normalizeAnchor(item, index));
}

function buildStageDocActions(stage, stageDocs, discovered, runId, runDate) {
  const configuredTitles = ensureArray(stageDocs[stage]);
  const mainTitle = configuredTitles[0] || `${stage}_main`;
  const reportTitle = configuredTitles[1] || `${stage}_report`;
  const actions = [];
  let mainFiles = discovered.main_files || [];

  if ((stage === 'draft' || stage === 'rewrite') && mainFiles.length > 1) {
    const granularFiles = stage === 'draft'
      ? mainFiles.filter(file => /03_标准初稿_.*\.md$/.test(path.basename(file)))
      : mainFiles.filter(file => /__rewrite_bundle\.md$/.test(path.basename(file)));
    if (granularFiles.length) {
      mainFiles = granularFiles;
    }
  }

  if ((stage === 'draft' || stage === 'rewrite') && mainFiles.length > 1) {
    mainFiles.forEach((file, index) => {
      const title = inferDocTitleFromFile(file, `${mainTitle}_${index + 1}`);
      const content = buildCombinedContent(title, stage, 'main', [file], runId, runDate);
      if (!content) return;
      actions.push({
        action_type: 'doc',
        key: `doc:${stage}:main:${slugFromFile(file)}`,
        stage,
        role: 'main',
        title,
        source_files: [file],
        content,
        folder_key: `folder:${stage}`
      });
    });
  } else {
    const mainContent = buildCombinedContent(mainTitle, stage, 'main', mainFiles, runId, runDate);
    if (mainContent) {
      actions.push({
        action_type: 'doc',
        key: `doc:${stage}:main`,
        stage,
        role: 'main',
        title: mainTitle,
        source_files: mainFiles,
        content: mainContent,
        folder_key: `folder:${stage}`
      });
    }
  }

  const reportContent = buildCombinedContent(reportTitle, stage, 'report', discovered.report_files, runId, runDate);
  if (reportContent) {
    actions.push({
      action_type: 'doc',
      key: `doc:${stage}:report`,
      stage,
      role: 'report',
      title: reportTitle,
      source_files: discovered.report_files,
      content: reportContent,
      folder_key: `folder:${stage}`
    });
  }

  return actions;
}

function buildFeishuSyncPlan(runId) {
  const { manifestFile, manifest } = getRuntimeManifest(runId);
  const config = loadStageReviewContract();
  const runDate = detectRunDate(runId, manifest);

  const rootFolder = {
    name: config.root_folder_name,
    url: config.root_folder_url,
    token: extractFolderToken(config.root_folder_url)
  };

  const stageDiscovery = Object.fromEntries(
    STAGE_SEQUENCE.map(stage => [stage, discoverStageArtifacts(stage, runId, runDate)])
  );

  const folderActions = [
    {
      action_type: 'folder',
      key: 'folder:date',
      title: runDate,
      folder_name: runDate,
      parent_token: rootFolder.token,
      parent_url: rootFolder.url
    },
    ...STAGE_SEQUENCE.map(stage => ({
      action_type: 'folder',
      key: `folder:${stage}`,
      stage,
      title: STAGE_META[stage].folderName,
      folder_name: STAGE_META[stage].folderName,
      parent_key: 'folder:date'
    }))
  ];

  const docActions = STAGE_SEQUENCE.flatMap(stage =>
    buildStageDocActions(stage, config.stage_docs || {}, stageDiscovery[stage], runId, runDate)
  );

  const messageActions = STAGE_SEQUENCE.flatMap(stage => {
    const stageDocKeys = docActions.filter(action => action.stage === stage).map(action => action.key);
    if (!stageDocKeys.length) return [];
    const reportContent = docActions.find(action => action.stage === stage && action.role === 'report')?.content || null;
    const mainContents = docActions
      .filter(action => action.stage === stage && action.role === 'main')
      .map(action => action.content)
      .filter(Boolean);
    const summarySource = unique([
      ...extractSummaryLines(reportContent),
      ...mainContents.flatMap(content => extractSummaryLines(content))
    ]).slice(0, 4);
    return [{
      action_type: 'message',
      key: `message:${stage}`,
      stage,
      title: `${stageDisplayName(stage)}审核通知`,
      review_group_name: config.review_group_name,
      doc_keys: stageDocKeys,
      summary_lines: summarySource,
      manual_review: defaultManualReview(stage),
      body_template: buildStageMessageBody(
        stage,
        stageDocKeys,
        summarySource,
        defaultManualReview(stage),
        runId
      )
    }];
  });

  const uploadActions = [];
  const actions = [...folderActions, ...docActions, ...messageActions, ...uploadActions];

  return {
    run_id: runId,
    run_date: runDate,
    manifest_file: manifestFile,
    manifest_exists: Boolean(manifest),
    config_file: CONFIG_FILE,
    root_folder: rootFolder,
    date_folder: folderActions[0],
    stage_discovery: stageDiscovery,
    folders: folderActions,
    docs: docActions,
    messages: messageActions,
    uploads: uploadActions,
    actions
  };
}

if (require.main === module) {
  const runId = process.argv[2];
  if (!runId) {
    console.error('usage: node feishu-plan.js <runId>');
    process.exit(1);
  }
  const plan = buildFeishuSyncPlan(runId);
  console.log(JSON.stringify(plan, null, 2));
}

module.exports = {
  buildFeishuSyncPlan,
  loadStageReviewContract,
  detectRunDate,
  discoverStageArtifacts,
  extractRewriteAnchors
};

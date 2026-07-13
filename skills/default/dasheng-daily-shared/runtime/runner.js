#!/usr/bin/env node

const path = require('path');
const { readJsonIfExists, writeJson, upsertArtifactDocUrl } = require('./manifest');
const { buildFeishuSyncPlan } = require('./feishu-plan');
const {
  persistRunSummaryToFeishu,
  attachDocRefToObjects
} = require('./feishu-sync');

const BASE_DIR = path.join(__dirname, '..', 'runtime-data');

const legacyMessage = [
  '[dasheng-daily runner] legacy pipeline runtime 已停用。',
  '请改用 dasheng-media-sop 与 canonical stage manifests / gate files。',
  '不再支持 clustering / outline / final 旧链路。',
].join(' ');

function failLegacyRunner() {
  throw new Error(legacyMessage);
}

function getManifestFile(runId) {
  return path.join(BASE_DIR, 'runs', runId, 'run_manifest.json');
}

function updateManifestDocUrl(runId, step, objectType, url) {
  const manifestFile = getManifestFile(runId);
  const manifest = readJsonIfExists(manifestFile);
  if (!manifest) {
    throw new Error(`manifest 不存在: ${manifestFile}`);
  }
  const updated = upsertArtifactDocUrl(manifest, step, objectType, url);
  writeJson(manifestFile, updated);
  return manifestFile;
}

function makeDocCreator(feishuClient, ownerOpenId) {
  return async ({ title, content }) => {
    const created = await feishuClient.create({ title, content, ownerOpenId });
    return {
      url: created.url,
      title: created.title,
      doc_token: created.doc_token
    };
  };
}

async function syncFeishuDocs(runId, handlers = {}) {
  const plan = buildFeishuSyncPlan(runId);
  const createdDocs = [];
  const createDoc = handlers.createDoc || null;
  if (!createDoc) {
    return {
      mode: 'tool-bridge-required',
      run_id: runId,
      manifest_file: plan.manifest_file,
      docs: plan.docs.map(doc => ({
        key: doc.key,
        title: doc.title,
        content: doc.content,
        bind: doc.bind
      })),
      actions: plan.actions
    };
  }

  for (const doc of plan.docs) {
    const created = await createDoc({ key: doc.key, title: doc.title, content: doc.content, bind: doc.bind || null });
    createdDocs.push({ key: doc.key, title: created.title, url: created.url, doc_token: created.doc_token || null });

    if (doc.bind) {
      attachDocRefToObjects({
        file: doc.bind.file,
        objectType: doc.bind.object_type,
        url: created.url,
        title: created.title
      });
      updateManifestDocUrl(runId, doc.bind.step, doc.bind.object_type, created.url);
    }

    if (doc.key === 'summary') {
      await persistRunSummaryToFeishu({
        runId,
        feishuDocCreate: async () => created,
        title: doc.title,
        content: doc.content
      });
    }
  }

  const manifestFile = getManifestFile(runId);
  return { run_id: runId, manifest_file: manifestFile, created_docs: createdDocs };
}

function buildSyncBridgeContract(runId) {
  const plan = buildFeishuSyncPlan(runId);
  const docs = plan.docs.map(doc => ({
    key: doc.key,
    title: doc.title,
    content: doc.content,
    bind: doc.bind,
    source_files: doc.source_files || []
  }));

  return {
    mode: 'tool-bridge-required',
    run_id: runId,
    manifest_file: plan.manifest_file,
    root_folder: plan.root_folder,
    folders: plan.folders,
    docs,
    messages: plan.messages,
    uploads: plan.uploads,
    refills: plan.refills,
    actions: plan.actions
  };
}

function parseArgs(argv) {
  const args = { runId: null, syncFeishu: false, syncFeishuLive: false };
  for (const token of argv) {
    if (token === '--sync-feishu') args.syncFeishu = true;
    else if (token === '--sync-feishu-live') args.syncFeishuLive = true;
    else if (!args.runId) args.runId = token;
  }
  return args;
}

if (require.main === module) {
  console.error(legacyMessage);
  process.exit(1);
}

module.exports = {
  runPipeline: failLegacyRunner,
  syncFeishuDocs,
  updateManifestDocUrl,
  parseArgs,
  buildSyncBridgeContract,
  makeDocCreator,
};

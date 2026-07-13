#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { buildSyncBridgeContract } = require('./runner');
const { readJsonIfExists, writeJson, setManifestFolder } = require('./manifest');
const { extractDocToken, extractFolderToken, extractMessageToken } = require('./doc-registry');

function getRunRoot(runId) {
  return path.join(__dirname, '..', 'runtime-data', 'runs', runId);
}

function getBridgeDir(runId) {
  return path.join(getRunRoot(runId), 'bridge');
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function writeJsonFile(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  return file;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function appendUniqueRef(refs = [], nextRef) {
  const key = `${nextRef.kind || ''}|${nextRef.token || ''}|${nextRef.url || ''}`;
  const kept = refs.filter(item => `${item.kind || ''}|${item.token || ''}|${item.url || ''}` !== key);
  return [...kept, nextRef];
}

function normalizeResourceMap(input = {}) {
  if (!input) return {};
  if (Array.isArray(input.actions)) {
    return Object.fromEntries(
      input.actions
        .filter(item => item.key && item.result)
        .map(item => [item.key, item.result])
    );
  }
  if (Array.isArray(input.results)) {
    return Object.fromEntries(
      input.results
        .filter(item => item.key)
        .map(item => [item.key, item.result || item])
    );
  }
  return input.resources || input.created_docs || input.docs || input;
}

function updateManifestArtifactUrls(manifest, action, resource) {
  if (!manifest || action.action_type !== 'doc' || !resource?.url) return manifest;
  const sourceFiles = new Set(action.source_files || []);
  if (!sourceFiles.size) return manifest;
  return {
    ...manifest,
    artifacts: (manifest.artifacts || []).map(item => (
      sourceFiles.has(item.file) ? { ...item, doc_url: resource.url } : item
    ))
  };
}

function updateManifestRefs(manifest, action, resource) {
  if (!manifest || !resource?.url) return manifest;

  if (action.action_type === 'folder' && action.key === 'folder:date') {
    return setManifestFolder(manifest, {
      token: resource.token || extractFolderToken(resource.url),
      url: resource.url,
      name: resource.name || action.folder_name || action.title
    });
  }

  if (action.action_type === 'doc') {
    return {
      ...updateManifestArtifactUrls(manifest, action, resource),
      message_refs: appendUniqueRef(manifest.message_refs || [], {
        kind: 'feishu_doc',
        token: resource.doc_token || extractDocToken(resource.url),
        url: resource.url,
        title: resource.title || action.title
      })
    };
  }

  if (action.action_type === 'message') {
    return {
      ...manifest,
      message_refs: appendUniqueRef(manifest.message_refs || [], {
        kind: 'feishu_message',
        token: resource.message_id || extractMessageToken(resource.url),
        url: resource.url,
        title: action.title
      })
    };
  }

  if (action.action_type === 'upload') {
    return {
      ...manifest,
      message_refs: appendUniqueRef(manifest.message_refs || [], {
        kind: 'feishu_upload',
        token: resource.file_token || resource.token || null,
        url: resource.url,
        title: action.title
      })
    };
  }

  return manifest;
}

function createActionStatus(contract, resourceMap = {}) {
  return contract.actions.map(action => ({
    ...action,
    result: resourceMap[action.key] || null,
    status: resourceMap[action.key] ? 'completed' : 'pending'
  }));
}

function prepareFeishuSync(runId) {
  const contract = buildSyncBridgeContract(runId);
  const bridgeDir = getBridgeDir(runId);
  const pendingActions = contract.actions.map(action => ({
    key: action.key,
    action_type: action.action_type,
    stage: action.stage || null,
    title: action.title,
    folder_key: action.folder_key || null,
    parent_key: action.parent_key || null,
    source_path: action.source_path || null,
    source_files: action.source_files || [],
    doc_keys: action.doc_keys || [],
    target_doc_key: action.target_doc_key || null,
    upload_key: action.upload_key || null
  }));

  const pendingFile = writeJsonFile(path.join(bridgeDir, 'pending-actions.json'), {
    run_id: runId,
    pending_actions: pendingActions
  });
  const contractFile = writeJsonFile(path.join(bridgeDir, 'sync-contract.json'), contract);

  return {
    phase: 'prepare',
    run_id: runId,
    pending_actions_file: pendingFile,
    contract_file: contractFile,
    pending_actions: pendingActions,
    contract
  };
}

function finalizeFeishuSync(runId, resourceMap = {}) {
  const contract = buildSyncBridgeContract(runId);
  const normalizedResources = normalizeResourceMap(resourceMap);
  const finalizedActions = createActionStatus(contract, normalizedResources);
  const bridgeDir = getBridgeDir(runId);
  const manifest = contract.manifest_file ? readJsonIfExists(contract.manifest_file) : null;
  let nextManifest = manifest;

  for (const action of finalizedActions) {
    if (!action.result) continue;
    nextManifest = updateManifestRefs(nextManifest, action, action.result);
  }

  if (nextManifest && contract.manifest_file) {
    writeJson(contract.manifest_file, nextManifest);
  }

  const resultFile = writeJsonFile(path.join(bridgeDir, 'finalized-actions.json'), {
    run_id: runId,
    finalized_actions: finalizedActions
  });

  return {
    phase: 'finalize',
    run_id: runId,
    contract,
    finalized_actions_file: resultFile,
    finalized_actions: finalizedActions,
    manifest_file: contract.manifest_file,
    manifest_updated: Boolean(nextManifest)
  };
}

function finalizeFeishuSyncFromFile(runId, file) {
  const payload = readJson(file);
  return finalizeFeishuSync(runId, payload);
}

function parseInlineResourceArgs(argv) {
  const resources = {};
  for (const token of argv) {
    const [key, url] = token.split('=');
    if (!key || !url) continue;
    resources[key] = { url };
  }
  return resources;
}

function parseArgs(argv) {
  const args = { phase: 'prepare', runId: null, resourceArgs: [], fromFile: null };
  for (const token of argv) {
    if (token === '--prepare') args.phase = 'prepare';
    else if (token === '--finalize') args.phase = 'finalize';
    else if (token === '--execute-live') args.phase = 'execute-live';
    else if (token.startsWith('--finalize-from-file=')) {
      args.phase = 'finalize-from-file';
      args.fromFile = token.split('=')[1] || null;
    } else if (!args.runId) args.runId = token;
    else args.resourceArgs.push(token);
  }
  return args;
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  if (!args.runId) {
    console.error('usage: node feishu-exec.js <runId> [--prepare|--finalize|--execute-live|--finalize-from-file=/path/to/action-results.json] [action-key=<url>]');
    process.exit(1);
  }

  (async () => {
    try {
      if (args.phase === 'prepare') {
        console.log(JSON.stringify(prepareFeishuSync(args.runId), null, 2));
        process.exit(0);
      }

      if (args.phase === 'execute-live') {
        const { executeFeishuSyncLive } = require('./feishu-live');
        console.log(JSON.stringify(await executeFeishuSyncLive(args.runId), null, 2));
        process.exit(0);
      }

      if (args.phase === 'finalize-from-file') {
        if (!args.fromFile) throw new Error('缺少 --finalize-from-file 路径');
        console.log(JSON.stringify(finalizeFeishuSyncFromFile(args.runId, args.fromFile), null, 2));
        process.exit(0);
      }

      console.log(JSON.stringify(finalizeFeishuSync(args.runId, parseInlineResourceArgs(args.resourceArgs)), null, 2));
      process.exit(0);
    } catch (error) {
      console.error('[feishu-exec] 失败:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = {
  prepareFeishuSync,
  finalizeFeishuSync,
  finalizeFeishuSyncFromFile,
  parseInlineResourceArgs,
  parseArgs,
  getBridgeDir,
  normalizeResourceMap
};

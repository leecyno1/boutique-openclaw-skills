#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { buildSyncBridgeContract } = require('./runner');
const {
  createClient,
  loadFeishuRuntimeConfig,
  unwrapAxiosError,
  isPermissionError,
  writeDoc,
  clearSectionAfterHeading,
  createFolder,
  createDoc,
  sendTextMessage,
  uploadDriveFile,
  walkFiles,
  refillDocAnchorsWithLocalAssets
} = require('./feishu-client');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function getRunRoot(runId) {
  return path.join(__dirname, '..', 'runtime-data', 'runs', runId);
}

function getBridgeDir(runId) {
  return path.join(getRunRoot(runId), 'bridge');
}

function writeJson(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  return file;
}

function readJsonIfExists(file) {
  if (!file || !fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function getExecutionLogFile(runId) {
  return path.join(getBridgeDir(runId), 'live-execution.json');
}

function getExecutionProgressFile(runId) {
  return path.join(getBridgeDir(runId), 'live-execution-progress.json');
}

function clearExecutionProgress(runId) {
  const progressFile = getExecutionProgressFile(runId);
  if (fs.existsSync(progressFile)) {
    fs.unlinkSync(progressFile);
  }
  return progressFile;
}

function normalizeSavedActions(items = []) {
  const map = new Map();
  for (const item of items) {
    if (!item?.key) continue;
    map.set(item.key, item);
  }
  return map;
}

function buildExecutionState(contractActions = [], savedProgress = null, options = {}) {
  const savedActionMap = normalizeSavedActions(savedProgress?.actions || []);
  const resources = { ...(savedProgress?.resources || {}) };
  const actions = [];
  const remainingActions = [];
  const allowCompletedResume = Boolean(options.allowCompletedResume);

  for (const action of contractActions) {
    const saved = savedActionMap.get(action.key);
    if (saved?.status === 'completed' && !allowCompletedResume) {
      actions.push(saved);
      if (saved.result) resources[action.key] = saved.result;
      continue;
    }
    remainingActions.push(action);
  }

  return {
    actions,
    resources,
    remainingActions
  };
}

function actionResult(action, status, result = {}, extra = {}) {
  return {
    key: action.key,
    action_type: action.action_type,
    title: action.title,
    status,
    result,
    ...extra
  };
}

function buildReplacementMap(resources = {}) {
  return Object.fromEntries(
    Object.entries(resources)
      .filter(([, value]) => value && value.url)
      .map(([key, value]) => [key, value.url])
  );
}

function renderMessageBody(action, resources) {
  const replacementMap = buildReplacementMap(resources);
  return String(action.body_template || '')
    .replace(/\{\{([^}]+)\}\}/g, (_, key) => replacementMap[key] || `未生成：${key}`)
    .trim();
}

function buildFallbackNote(action, error) {
  const details = unwrapAxiosError(error);
  if (!isPermissionError(error)) return null;
  return `${action.key} 权限不足，已降级为根文档模式`;
}

const MAX_UPLOAD_BYTES = 25 * 1024 * 1024;
const ACTION_TIMEOUT_MS = {
  folder: 30_000,
  doc: 240_000,
  message: 30_000,
  upload: 300_000,
  refill: 300_000,
  default: 120_000
};

function timeoutForAction(action) {
  if (action.action_type === 'upload') {
    const fileCount = action.source_path && fs.existsSync(action.source_path) ? walkFiles(action.source_path).length : 0;
    return Math.max(ACTION_TIMEOUT_MS.upload, Math.min(900_000, fileCount * 4_000));
  }
  return ACTION_TIMEOUT_MS[action.action_type] || ACTION_TIMEOUT_MS.default;
}

function withTimeout(promise, label, ms) {
  let timer = null;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`${label} timeout after ${ms}ms`)), ms);
  });
  return Promise.race([
    promise.finally(() => {
      if (timer) clearTimeout(timer);
    }),
    timeout
  ]);
}

function persistExecutionProgress(runId, payload) {
  return writeJson(getExecutionProgressFile(runId), payload);
}

async function executeFolderAction(client, action, host, context) {
  const parentToken = action.parent_token || context.resources[action.parent_key]?.token || null;
  if (action.parent_key && !parentToken) {
    return actionResult(action, 'blocked', {}, {
      note: `父文件夹 ${action.parent_key} 不可用，跳过创建`
    });
  }
  try {
    const created = await createFolder(client, action.folder_name || action.title, parentToken, host);
    return actionResult(action, 'completed', created);
  } catch (error) {
    if (isPermissionError(error)) {
      return actionResult(action, 'blocked', {
        token: null,
        url: parentToken ? null : null,
        fallback: 'folder_permission_denied'
      }, {
        error: unwrapAxiosError(error),
        note: buildFallbackNote(action, error)
      });
    }
    return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
  }
}

async function executeDocAction(client, action, host, context) {
  try {
    const preferredFolderToken = action.folder_key ? context.resources[action.folder_key]?.token || null : null;
    let created;
    let mode = 'preferred_folder';

    try {
      created = await createDoc(client, action.title, preferredFolderToken, host);
    } catch (error) {
      if (!isPermissionError(error)) {
        return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
      }
      created = await createDoc(client, action.title, null, host);
      mode = 'root_fallback';
    }

    const content = action.content || '';
    const write = await writeDoc(client, created.doc_token, content, {
      forceMarkdown: true,
      maxChunkChars: content.length > 30000 ? 3200 : 6000
    });
    return actionResult(action, 'completed', {
      ...created,
      mode,
      folder_token: preferredFolderToken,
      write_mode: write.mode || 'markdown',
      blocks_added: write.blocks_added,
      blocks_deleted: write.blocks_deleted
    });
  } catch (error) {
    return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
  }
}

async function executeMessageAction(client, action, runtimeConfig, context) {
  try {
    if (!runtimeConfig.chatId) {
      return actionResult(action, 'blocked', {}, {
        note: '未配置 CHAT_ID，跳过群通知'
      });
    }
    const body = renderMessageBody(action, context.resources);
    const sent = await sendTextMessage(client, runtimeConfig.chatId, body);
    return actionResult(action, 'completed', {
      ...sent,
      url: sent.url,
      body
    });
  } catch (error) {
    return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
  }
}

async function ensureRemoteFolderTree(client, folderToken, sourceRoot, host) {
  const folderCache = new Map();
  folderCache.set('.', folderToken);
  const files = walkFiles(sourceRoot);
  const uploaded = [];

  for (const file of files) {
    const relative = path.relative(sourceRoot, file);
    const folderParts = path.dirname(relative).split(path.sep).filter(Boolean);
    let currentToken = folderToken;
    let currentPath = '.';

    for (const part of folderParts) {
      currentPath = currentPath === '.' ? part : `${currentPath}/${part}`;
      if (!folderCache.has(currentPath)) {
        const created = await createFolder(client, part, currentToken, host);
        folderCache.set(currentPath, created.token);
      }
      currentToken = folderCache.get(currentPath);
    }

    const stat = fs.statSync(file);
    if (stat.size > MAX_UPLOAD_BYTES) {
      uploaded.push({
        relative_path: relative,
        status: 'skipped_too_large',
        size_bytes: stat.size
      });
      continue;
    }

    try {
      const remote = await uploadDriveFile(client, currentToken, file, host);
      uploaded.push({
        relative_path: relative,
        status: 'uploaded',
        size_bytes: stat.size,
        ...remote
      });
    } catch (error) {
      uploaded.push({
        relative_path: relative,
        status: 'failed',
        size_bytes: stat.size,
        error: unwrapAxiosError(error)
      });
    }
  }

  return uploaded;
}

async function executeUploadAction(client, action, host, context) {
  const folderToken = action.folder_key ? context.resources[action.folder_key]?.token || null : null;
  if (!folderToken) {
    return actionResult(action, 'blocked', {}, {
      note: '目标素材文件夹不可用，跳过上传'
    });
  }
  try {
    const sourcePath = action.source_path;
    if (!sourcePath || !fs.existsSync(sourcePath)) {
      return actionResult(action, 'blocked', {}, {
        note: '素材目录不存在，跳过上传'
      });
    }
    const uploaded = await ensureRemoteFolderTree(client, folderToken, sourcePath, host);
    return actionResult(action, 'completed', {
      file_token: folderToken,
      url: context.resources[action.folder_key]?.url,
      uploaded_count: uploaded.filter(item => item.status === 'uploaded').length,
      skipped_count: uploaded.filter(item => item.status !== 'uploaded').length,
      files: uploaded
    });
  } catch (error) {
    if (isPermissionError(error)) {
      return actionResult(action, 'blocked', {}, {
        error: unwrapAxiosError(error),
        note: '素材文件夹没有飞书权限，未上传'
      });
    }
    return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
  }
}

async function executeRefillAction(client, action, context) {
  const doc = context.resources[action.target_doc_key];
  if (!doc?.doc_token) {
    return actionResult(action, 'blocked', {}, {
      note: '目标改写文档未创建，跳过素材回填'
    });
  }

  const rewriteAction = context.contract.docs.find(item => item.key === action.target_doc_key);
  const sourceFiles = rewriteAction?.source_files || [];
  try {
    const refillPolicy = action.refill_policy || {};
    const clearBeforeRefill = Boolean(refillPolicy.clear_before_refill);
    const clearHeadings = Array.isArray(refillPolicy.clear_headings)
      ? refillPolicy.clear_headings
      : [];
    const clearedSections = [];

    if (clearBeforeRefill && clearHeadings.length) {
      for (const headingText of clearHeadings) {
        const cleared = await clearSectionAfterHeading(client, doc.doc_token, headingText);
        clearedSections.push({
          heading: headingText,
          ...cleared
        });
      }
    }

    const refill = await refillDocAnchorsWithLocalAssets(client, doc.doc_token, sourceFiles, {
      tableMaxPreviewRows: Number.isInteger(refillPolicy.table_max_preview_rows)
        ? refillPolicy.table_max_preview_rows
        : 12
    });
    return actionResult(action, 'completed', {
      url: doc.url,
      doc_token: doc.doc_token,
      anchors_total: refill.anchors_total,
      anchors_filled: refill.anchors_filled,
      details: refill.details,
      cleared_sections: clearedSections
    });
  } catch (error) {
    return actionResult(action, 'failed', {}, { error: unwrapAxiosError(error) });
  }
}

async function executeAction(client, action, runtimeConfig, context) {
  switch (action.action_type) {
    case 'folder':
      return executeFolderAction(client, action, runtimeConfig.host, context);
    case 'doc':
      return executeDocAction(client, action, runtimeConfig.host, context);
    case 'message':
      return executeMessageAction(client, action, runtimeConfig, context);
    case 'upload':
      return executeUploadAction(client, action, runtimeConfig.host, context);
    case 'refill':
      return executeRefillAction(client, action, context);
    default:
      return actionResult(action, 'blocked', {}, { note: `未支持的 action_type: ${action.action_type}` });
  }
}

async function executeFeishuSyncLive(runId, options = {}) {
  const { client, config: runtimeConfig } = createClient();
  const contract = buildSyncBridgeContract(runId);
  if (options.fresh) {
    clearExecutionProgress(runId);
  }
  const savedProgress = readJsonIfExists(getExecutionProgressFile(runId));
  if (options.resumeOnly && !savedProgress) {
    throw new Error(`resume-only requested but no progress file exists for ${runId}`);
  }
  const state = buildExecutionState(contract.actions, savedProgress);
  const context = {
    contract,
    resources: { ...state.resources }
  };
  const actions = [...state.actions];
  const startedAt = savedProgress?.started_at || new Date().toISOString();

  persistExecutionProgress(runId, {
    run_id: runId,
    started_at: startedAt,
    resumed_at: new Date().toISOString(),
    current_action: null,
    actions,
    resources: context.resources
  });

  for (const action of state.remainingActions) {
    persistExecutionProgress(runId, {
      run_id: runId,
      started_at: startedAt,
      resumed_at: new Date().toISOString(),
      current_action: {
        key: action.key,
        action_type: action.action_type,
        title: action.title
      },
      actions,
      resources: context.resources
    });

    const executed = await withTimeout(
      executeAction(client, action, runtimeConfig, context),
      `action ${action.key}`,
      timeoutForAction(action)
    ).catch(error =>
      actionResult(action, 'failed', {}, {
        error: unwrapAxiosError(error),
        note: error.message
      })
    );
    actions.push(executed);
    if (executed.result && executed.status === 'completed') {
      context.resources[action.key] = executed.result;
    }
    persistExecutionProgress(runId, {
      run_id: runId,
      started_at: startedAt,
      resumed_at: new Date().toISOString(),
      current_action: null,
      last_action: {
        key: action.key,
        status: executed.status
      },
      actions,
      resources: context.resources
    });
  }

  const resources = Object.fromEntries(
    actions
      .filter(item => item.status === 'completed' && item.result)
      .map(item => [item.key, item.result])
  );

  const { finalizeFeishuSync } = require('./feishu-exec');
  const finalized = finalizeFeishuSync(runId, { resources });
  const executionLog = {
    run_id: runId,
    resumed: Boolean(savedProgress?.actions?.length),
    fresh: Boolean(options.fresh),
    runtime_config: {
      host: runtimeConfig.host,
      chat_id: runtimeConfig.chatId || null
    },
    actions,
    resources,
    finalized_actions_file: finalized.finalized_actions_file
  };
  const executionLogFile = writeJson(getExecutionLogFile(runId), executionLog);
  persistExecutionProgress(runId, {
    run_id: runId,
    started_at: startedAt,
    resumed_at: new Date().toISOString(),
    finished_at: new Date().toISOString(),
    current_action: null,
    last_action: actions.length ? {
      key: actions[actions.length - 1].key,
      status: actions[actions.length - 1].status
    } : null,
    actions,
    resources
  });

  return {
    run_id: runId,
    execution_log_file: executionLogFile,
    finalized_actions_file: finalized.finalized_actions_file,
    actions,
    resources,
    manifest_file: finalized.manifest_file
  };
}

function parseArgs(argv) {
  const args = { runId: null, fresh: false, resumeOnly: false };
  for (const token of argv) {
    if (token === '--fresh') args.fresh = true;
    else if (token === '--resume-only') args.resumeOnly = true;
    else if (!args.runId) args.runId = token;
  }
  return args;
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  if (!args.runId) {
    console.error('usage: node feishu-live.js <runId> [--fresh] [--resume-only]');
    process.exit(1);
  }

  executeFeishuSyncLive(args.runId, {
    fresh: args.fresh,
    resumeOnly: args.resumeOnly
  })
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch(error => {
      console.error('[feishu-live] 失败:', error.message);
      process.exit(1);
    });
}

module.exports = {
  executeFeishuSyncLive,
  renderMessageBody,
  buildExecutionState,
  clearExecutionProgress
};

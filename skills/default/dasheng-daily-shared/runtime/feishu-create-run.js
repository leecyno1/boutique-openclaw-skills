#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { getBridgeDir, normalizeResourceMap } = require('./feishu-exec');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  return file;
}

function getExecutionRequestsFile(runId) {
  return path.join(getBridgeDir(runId), 'execution-requests.json');
}

function getActionResultsFile(runId) {
  return path.join(getBridgeDir(runId), 'action-results.json');
}

function buildTitleCandidates(action) {
  const candidates = [action.title].filter(Boolean);
  if (action.action_type === 'doc') candidates.push(`${action.title} v2`, `${action.title} 二版`);
  if (action.action_type === 'folder') candidates.push(action.folder_name || action.title);
  if (action.action_type === 'message') candidates.push(`${action.title}（群消息）`);
  return [...new Set(candidates.filter(Boolean))];
}

function prepareExecutionJobs(runId) {
  const requestFile = getExecutionRequestsFile(runId);
  const payload = readJson(requestFile);
  const jobs = (payload.requests || []).map(action => ({
    key: action.key,
    action_type: action.action_type,
    title: action.title,
    title_candidates: buildTitleCandidates(action),
    status: action.status || 'pending_execute',
    source_path: action.source_path || null,
    source_files: action.source_files || [],
    folder_key: action.folder_key || null,
    parent_key: action.parent_key || null,
    target_doc_key: action.target_doc_key || null
  }));
  return { run_id: runId, request_file: requestFile, jobs };
}

function applyActionResults(runId, results) {
  const requestFile = getExecutionRequestsFile(runId);
  const payload = readJson(requestFile);
  payload.requests = (payload.requests || []).map(action => {
    const result = results[action.key];
    if (!result) return action;
    return {
      ...action,
      result,
      status: 'completed'
    };
  });
  writeJson(requestFile, payload);
  return requestFile;
}

function materializeActionResults(runId) {
  const requestFile = getExecutionRequestsFile(runId);
  const payload = readJson(requestFile);
  const resources = {};

  for (const action of payload.requests || []) {
    if (!action.key || !action.result) continue;
    resources[action.key] = action.result;
  }

  const output = {
    run_id: runId,
    resources
  };

  const outFile = writeJson(getActionResultsFile(runId), output);
  return { run_id: runId, action_results_file: outFile, resources };
}

function parseActionResultsFile(file) {
  return normalizeResourceMap(readJson(file));
}

function parseArgs(argv) {
  const args = { action: 'prepare-jobs', runId: null, fromFile: null };
  for (const token of argv) {
    if (token === '--prepare-jobs') args.action = 'prepare-jobs';
    else if (token.startsWith('--apply-action-results=')) {
      args.action = 'apply-action-results';
      args.fromFile = token.split('=')[1] || null;
    } else if (token === '--materialize-action-results') {
      args.action = 'materialize-action-results';
    } else if (!args.runId) args.runId = token;
  }
  return args;
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  if (!args.runId) {
    console.error('usage: node feishu-create-run.js <runId> [--prepare-jobs|--apply-action-results=/path/to/file.json|--materialize-action-results]');
    process.exit(1);
  }

  try {
    if (args.action === 'prepare-jobs') {
      console.log(JSON.stringify(prepareExecutionJobs(args.runId), null, 2));
      process.exit(0);
    }

    if (args.action === 'apply-action-results') {
      if (!args.fromFile) throw new Error('缺少 --apply-action-results 文件路径');
      const requestFile = applyActionResults(args.runId, parseActionResultsFile(args.fromFile));
      console.log(JSON.stringify({ run_id: args.runId, request_file: requestFile }, null, 2));
      process.exit(0);
    }

    console.log(JSON.stringify(materializeActionResults(args.runId), null, 2));
    process.exit(0);
  } catch (error) {
    console.error('[feishu-create-run] 失败:', error.message);
    process.exit(1);
  }
}

module.exports = {
  buildTitleCandidates,
  prepareExecutionJobs,
  applyActionResults,
  materializeActionResults,
  parseActionResultsFile,
  parseArgs
};

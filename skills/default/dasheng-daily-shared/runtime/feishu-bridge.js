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

function getPendingActionsFile(runId) {
  return path.join(getBridgeDir(runId), 'pending-actions.json');
}

function getExecutionRequestsFile(runId) {
  return path.join(getBridgeDir(runId), 'execution-requests.json');
}

function getActionResultsFile(runId) {
  return path.join(getBridgeDir(runId), 'action-results.json');
}

function buildExecutionRequests(runId) {
  const pendingFile = getPendingActionsFile(runId);
  const payload = readJson(pendingFile);
  const requests = (payload.pending_actions || []).map(action => ({
    ...action,
    status: 'pending_execute'
  }));

  const output = {
    run_id: runId,
    source_file: pendingFile,
    requests
  };

  const outFile = writeJson(getExecutionRequestsFile(runId), output);
  return { run_id: runId, execution_requests_file: outFile, requests };
}

function materializeActionResults(runId, sourceFile) {
  const payload = readJson(sourceFile);
  const normalized = normalizeResourceMap(payload);
  const output = {
    run_id: runId,
    resources: normalized
  };
  const outFile = writeJson(getActionResultsFile(runId), output);
  return { run_id: runId, action_results_file: outFile, resources: normalized };
}

function parseArgs(argv) {
  const args = { action: 'prepare', runId: null, fromFile: null };
  for (const token of argv) {
    if (token === '--prepare-requests') args.action = 'prepare';
    else if (token.startsWith('--materialize-from=')) {
      args.action = 'materialize';
      args.fromFile = token.split('=')[1] || null;
    } else if (!args.runId) args.runId = token;
  }
  return args;
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  if (!args.runId) {
    console.error('usage: node feishu-bridge.js <runId> [--prepare-requests|--materialize-from=/path/to/file.json]');
    process.exit(1);
  }

  try {
    if (args.action === 'prepare') {
      console.log(JSON.stringify(buildExecutionRequests(args.runId), null, 2));
      process.exit(0);
    }

    if (!args.fromFile) throw new Error('缺少 --materialize-from 文件路径');
    console.log(JSON.stringify(materializeActionResults(args.runId, args.fromFile), null, 2));
    process.exit(0);
  } catch (error) {
    console.error('[feishu-bridge] 失败:', error.message);
    process.exit(1);
  }
}

module.exports = {
  getPendingActionsFile,
  getExecutionRequestsFile,
  getActionResultsFile,
  buildExecutionRequests,
  materializeActionResults,
  parseArgs
};

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function nowIso() {
  return new Date().toISOString();
}

function runDateFromIso(iso = nowIso()) {
  return iso.slice(0, 10);
}

function makeRunId(prefix = 'dasheng-daily', iso = nowIso()) {
  const compact = iso.replace(/[-:TZ.]/g, '').slice(0, 14);
  return `${prefix}-${compact}`;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function readJsonIfExists(file) {
  if (!file || !fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  return file;
}

function sha1(input) {
  return crypto.createHash('sha1').update(String(input || '')).digest('hex');
}

function createManifest({
  workflowName = 'dasheng-daily',
  workflowVersion = '3.0.0',
  runId,
  runDate,
  currentStep = 'intake',
  folder = null,
  messageRefs = []
} = {}) {
  const createdAt = nowIso();
  return {
    run_id: runId || makeRunId(workflowName, createdAt),
    run_date: runDate || runDateFromIso(createdAt),
    workflow_name: workflowName,
    workflow_version: workflowVersion,
    status: 'running',
    current_step: currentStep,
    completed_steps: [],
    failed_steps: [],
    skipped_steps: [],
    folder,
    artifacts: [],
    selection_state: {
      selected_topic_ids: [],
      rejected_topic_ids: []
    },
    operator_decisions: [],
    retry_state: {},
    message_refs: messageRefs,
    created_at: createdAt,
    updated_at: createdAt
  };
}

function updateManifest(manifest, patch = {}) {
  return {
    ...manifest,
    ...patch,
    updated_at: nowIso()
  };
}

function markStepCompleted(manifest, step) {
  const completed = Array.from(new Set([...(manifest.completed_steps || []), step]));
  const failed = (manifest.failed_steps || []).filter(s => s !== step);
  return updateManifest(manifest, {
    completed_steps: completed,
    failed_steps: failed,
    current_step: step
  });
}

function markStepFailed(manifest, step, reason = '') {
  const failed = Array.from(new Set([...(manifest.failed_steps || []), step]));
  const retryState = {
    ...(manifest.retry_state || {}),
    [step]: {
      failed_at: nowIso(),
      reason
    }
  };
  return updateManifest(manifest, {
    status: 'failed',
    current_step: step,
    failed_steps: failed,
    retry_state: retryState
  });
}

function finishManifest(manifest) {
  return updateManifest(manifest, { status: 'completed' });
}

function setManifestFolder(manifest, folder) {
  return updateManifest(manifest, { folder });
}

function upsertArtifactDocUrl(manifest, step, objectType, docUrl) {
  return updateManifest(manifest, {
    artifacts: (manifest.artifacts || []).map(item => {
      if (item.step === step && item.object_type === objectType) {
        return { ...item, doc_url: docUrl };
      }
      return item;
    })
  });
}

module.exports = {
  nowIso,
  runDateFromIso,
  makeRunId,
  ensureDir,
  readJsonIfExists,
  writeJson,
  sha1,
  createManifest,
  updateManifest,
  markStepCompleted,
  markStepFailed,
  finishManifest,
  setManifestFolder,
  upsertArtifactDocUrl
};

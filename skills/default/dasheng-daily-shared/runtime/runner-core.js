const fs = require('fs');
const path = require('path');
const { createManifest, readJsonIfExists, writeJson } = require('./manifest');

const STEP_ORDER = [
  'intake',
  'clustering',
  'brief',
  'outline',
  'draft',
  'final',
  'postmortem'
];

function getRunRoot(baseDir, runId) {
  return path.join(baseDir, 'runs', runId);
}

function getManifestFile(baseDir, runId) {
  return path.join(getRunRoot(baseDir, runId), 'run_manifest.json');
}

function ensureManifest(baseDir, { runId, runDate, workflowName = 'dasheng-daily', workflowVersion = '3.0.0' }) {
  const manifestFile = getManifestFile(baseDir, runId);
  const existing = readJsonIfExists(manifestFile);
  if (existing) return { manifest: existing, manifestFile, created: false };
  const manifest = createManifest({ workflowName, workflowVersion, runId, runDate, currentStep: 'intake' });
  writeJson(manifestFile, manifest);
  return { manifest, manifestFile, created: true };
}

function getArtifactFile(manifest, step, objectType) {
  const match = (manifest.artifacts || []).find(item => item.step === step && item.object_type === objectType);
  return match?.file || null;
}

function getStepInput(step, manifest) {
  const mapping = {
    intake: null,
    clustering: getArtifactFile(manifest, 'intake', 'IntakeRecord'),
    brief: getArtifactFile(manifest, 'clustering', 'ClusteredTopic'),
    outline: getArtifactFile(manifest, 'brief', 'ContentBrief'),
    draft: getArtifactFile(manifest, 'outline', 'OutlinePlan'),
    final: getArtifactFile(manifest, 'draft', 'DraftPackage'),
    postmortem: getArtifactFile(manifest, 'final', 'FinalPackage')
  };
  return mapping[step] || null;
}

function getPendingSteps(manifest) {
  const completed = new Set(manifest.completed_steps || []);
  return STEP_ORDER.filter(step => !completed.has(step));
}

function canRunStep(step, manifest) {
  if (step === 'intake') return true;
  return Boolean(getStepInput(step, manifest));
}

module.exports = {
  STEP_ORDER,
  getRunRoot,
  getManifestFile,
  ensureManifest,
  getArtifactFile,
  getStepInput,
  getPendingSteps,
  canRunStep
};

const fs = require('fs');
const path = require('path');
const { ensureDir, writeJson } = require('./manifest');

function getRunDir(baseDir, runId) {
  return path.join(baseDir, 'runs', runId);
}

function getArtifactsDir(baseDir, runId, step) {
  return path.join(getRunDir(baseDir, runId), 'artifacts', step);
}

function persistArtifact({
  baseDir,
  runId,
  step,
  name,
  data
}) {
  const dir = getArtifactsDir(baseDir, runId, step);
  ensureDir(dir);
  const file = path.join(dir, name);
  writeJson(file, data);
  return file;
}

function persistTextArtifact({
  baseDir,
  runId,
  step,
  name,
  content
}) {
  const dir = getArtifactsDir(baseDir, runId, step);
  ensureDir(dir);
  const file = path.join(dir, name);
  fs.writeFileSync(file, content, 'utf8');
  return file;
}

function appendArtifactRef(manifest, ref) {
  return {
    ...manifest,
    artifacts: [...(manifest.artifacts || []), ref]
  };
}

module.exports = {
  getRunDir,
  getArtifactsDir,
  persistArtifact,
  persistTextArtifact,
  appendArtifactRef
};

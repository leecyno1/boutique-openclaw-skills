#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { readJsonIfExists, writeJson, setManifestFolder } = require('./manifest');
const { extractDocToken } = require('./doc-registry');

function buildSummaryContent(manifest) {
  const artifactLines = (manifest.artifacts || []).map(item => `- ${item.step} / ${item.object_type} × ${item.count}${item.file ? `\n  - file: \`${item.file}\`` : ''}${item.doc_url ? `\n  - doc: ${item.doc_url}` : ''}`).join('\n');
  return `# dasheng-daily run ${manifest.run_date} 产物总览\n\n- run_id: \`${manifest.run_id}\`\n- workflow_version: \`${manifest.workflow_version}\`\n- status: \`${manifest.status}\`\n- current_step: \`${manifest.current_step}\`\n\n## 已完成步骤\n${(manifest.completed_steps || []).map(s => `- ${s}`).join('\n')}\n\n## 产物清单\n${artifactLines}\n`;
}

function buildBriefContent(briefs = []) {
  return `# Brief 产物\n\n${briefs.map((item, idx) => `## ${idx + 1}. ${item.title}\n- topic_id: \`${item.topic_id}\`\n- 成稿价值分: ${item.scorecard.article_value}\n- 爆款视频潜力分: ${item.scorecard.viral_potential}\n- 综合评分: ${item.scorecard.composite}\n- 核心主张: ${item.core_claim}`).join('\n\n')}`;
}

function buildFinalContent(finals = []) {
  return `# Final 产物\n\n${finals.map((item, idx) => `## ${idx + 1}. ${item.title}\n- topic_id: \`${item.topic_id}\`\n- original_title: ${item.original_title}\n- status: ${item.status}\n- predicted.composite: ${item.predicted_scores.composite}\n- review.score: ${item.review.score}`).join('\n\n')}`;
}

function buildPostmortemContent(payload = {}) {
  const records = payload.records || [];
  const overall = payload.overall_accuracy || {};
  return `# Postmortem 产物\n\n- overall.article_value.accuracy: ${overall.article_value}\n- overall.viral_potential.accuracy: ${overall.viral_potential}\n- overall.composite.accuracy: ${overall.composite}\n\n${records.map((item, idx) => `## ${idx + 1}. ${item.title}\n- topic_id: \`${item.topic_id}\`\n- predicted.composite: ${item.scoring_accuracy.composite.predicted}\n- actual.composite: ${item.scoring_accuracy.composite.actual}\n- composite.accuracy: ${item.scoring_accuracy.composite.accuracy}`).join('\n\n')}`;
}

function dedupeMessageRefs(refs = []) {
  const seen = new Set();
  return refs.filter(ref => {
    const key = `${ref.kind || ''}|${ref.doc_token || ref.token || ''}|${ref.url || ''}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function replaceLatestMessageRef(refs = [], nextRef, { replaceKinds = [] } = {}) {
  const kindSet = new Set(replaceKinds);
  const kept = refs.filter(ref => !kindSet.has(ref.kind));
  return dedupeMessageRefs([...kept, nextRef]);
}

function replaceObjectDocRefs(refs = [], nextRef) {
  const nextToken = nextRef.token || extractDocToken(nextRef.url);
  const kept = (refs || []).filter(ref => {
    if ((ref.kind || 'doc') !== 'doc') return true;
    const refToken = ref.token || extractDocToken(ref.url);
    return refToken && nextToken ? refToken === nextToken : false;
  });
  return dedupeMessageRefs([...kept, { ...nextRef, kind: 'doc', token: nextToken }]);
}

async function persistRunSummaryToFeishu({ runId, feishuDocCreate, title, content }) {
  const manifestFile = path.join(__dirname, '..', 'runtime-data', 'runs', runId, 'run_manifest.json');
  const manifest = readJsonIfExists(manifestFile);
  if (!manifest) throw new Error(`manifest 不存在: ${manifestFile}`);

  const created = await feishuDocCreate({
    title: title || `dasheng-daily run ${manifest.run_date} 产物总览`,
    content: content || buildSummaryContent(manifest)
  });

  const docUrl = created.url;
  const docToken = extractDocToken(docUrl);
  const nextManifest = setManifestFolder(manifest, {
    token: manifest.folder?.token || null,
    url: docUrl,
    name: manifest.folder?.name || manifest.run_date
  });

  nextManifest.message_refs = replaceLatestMessageRef(
    nextManifest.message_refs || [],
    { kind: 'feishu_doc_summary', doc_token: docToken, url: docUrl, title: created.title },
    { replaceKinds: ['feishu_doc_summary'] }
  );

  writeJson(manifestFile, nextManifest);
  return { manifest_file: manifestFile, url: docUrl, title: created.title, doc_token: docToken };
}

function attachDocRefToObjects({ file, objectType, url, title }) {
  const payload = readJsonIfExists(file);
  if (!payload) throw new Error(`对象文件不存在: ${file}`);
  const docRef = { kind: 'doc', token: extractDocToken(url), url, title };

  if (Array.isArray(payload)) {
    const updated = payload.map(item => ({
      ...item,
      meta: {
        ...(item.meta || {}),
        doc_refs: replaceObjectDocRefs((item.meta && item.meta.doc_refs) || [], docRef)
      }
    }));
    writeJson(file, updated);
    return updated.length;
  }

  if (payload.records && Array.isArray(payload.records)) {
    payload.records = payload.records.map(item => ({
      ...item,
      meta: {
        ...(item.meta || {}),
        doc_refs: replaceObjectDocRefs((item.meta && item.meta.doc_refs) || [], docRef)
      }
    }));
    writeJson(file, payload);
    return payload.records.length;
  }

  throw new Error(`不支持的对象结构: ${objectType}`);
}

module.exports = {
  persistRunSummaryToFeishu,
  buildSummaryContent,
  buildBriefContent,
  buildFinalContent,
  buildPostmortemContent,
  attachDocRefToObjects,
  dedupeMessageRefs,
  replaceLatestMessageRef,
  replaceObjectDocRefs
};

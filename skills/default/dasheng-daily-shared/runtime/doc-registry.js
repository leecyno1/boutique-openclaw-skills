function normalizeDocRef({ kind = 'doc', token = null, url = null, title = null } = {}) {
  return { kind, token, url, title };
}

function normalizeFolderRef({ token = null, url = null, name = null } = {}) {
  return { token, url, name };
}

function attachDocRef(meta, docRef) {
  return {
    ...meta,
    doc_refs: [...(meta.doc_refs || []), normalizeDocRef(docRef)]
  };
}

function extractDocToken(url = '') {
  const match = String(url).match(/\/docx\/([A-Za-z0-9]+)/) || String(url).match(/\/docs\/([A-Za-z0-9]+)/);
  return match ? match[1] : null;
}

function extractFolderToken(url = '') {
  const match = String(url).match(/\/drive\/folder\/([A-Za-z0-9]+)/);
  return match ? match[1] : null;
}

function extractMessageToken(url = '') {
  const match = String(url).match(/message[_/-]([A-Za-z0-9]+)/) || String(url).match(/messages\/([A-Za-z0-9:_-]+)/);
  return match ? match[1] : null;
}

module.exports = {
  normalizeDocRef,
  normalizeFolderRef,
  attachDocRef,
  extractDocToken,
  extractFolderToken,
  extractMessageToken
};

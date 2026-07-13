#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { homedir } = require('os');

// 支持环境变量覆盖路径配置
const SDK_PATH = process.env.OPENCLAW_FEISHU_SDK_PATH || path.join(homedir(), '.npm-global/lib/node_modules/openclaw/dist/extensions/feishu/node_modules/@larksuiteoapi/node-sdk');
const DEFAULT_CONFIG_FILE = process.env.DASHENG_FEISHU_CONFIG || path.join(homedir(), 'clawd/configs/feishu_api.conf');

const lark = require(SDK_PATH);

const DEFAULT_IMAGE_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']);
const DEFAULT_CSV_EXTENSIONS = new Set(['.csv']);

function parseShellEnvFile(file) {
  const result = {};
  if (!file || !fs.existsSync(file)) return result;
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = trimmed.match(/^([A-Z0-9_]+)=(.*)$/);
    if (!match) continue;
    const [, key, rawValue] = match;
    result[key] = rawValue.replace(/^['"]|['"]$/g, '');
  }
  return result;
}

function readJsonIfExists(file) {
  if (!file || !fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function getProjectRoot() {
  return path.resolve(__dirname, '..', '..', '..');
}

function loadStageReviewConfig() {
  const file = path.join(getProjectRoot(), 'configs', 'feishu', 'stage_review_contract.json');
  return readJsonIfExists(file) || {};
}

function getTenantHost() {
  const config = loadStageReviewConfig();
  try {
    return new URL(config.root_folder_url).host;
  } catch {
    return 'ccnokd2fmz4u.feishu.cn';
  }
}

function loadFeishuRuntimeConfig() {
  const fileConfig = parseShellEnvFile(DEFAULT_CONFIG_FILE);
  return {
    appId: process.env.FEISHU_APP_ID || fileConfig.APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET || fileConfig.APP_SECRET,
    tenantKey: process.env.FEISHU_TENANT_KEY || fileConfig.TENANT_KEY || null,
    chatId: process.env.FEISHU_CHAT_ID || fileConfig.CHAT_ID || null,
    host: getTenantHost()
  };
}

function createClient(explicit = {}) {
  const config = { ...loadFeishuRuntimeConfig(), ...explicit };
  if (!config.appId || !config.appSecret) {
    throw new Error('缺少飞书凭证：APP_ID / APP_SECRET');
  }
  const client = new lark.Client({
    appId: config.appId,
    appSecret: config.appSecret,
    appType: lark.AppType.SelfBuild,
    domain: lark.Domain.Feishu,
    loggerLevel: lark.LoggerLevel.fatal
  });
  return { client, config };
}

function buildDocUrl(docToken, host) {
  return `https://${host}/docx/${docToken}`;
}

function buildFolderUrl(folderToken, host) {
  return `https://${host}/drive/folder/${folderToken}`;
}

function buildFileUrl(fileToken, host) {
  return `https://${host}/file/${fileToken}`;
}

function isImageFile(file) {
  return DEFAULT_IMAGE_EXTENSIONS.has(path.extname(file).toLowerCase());
}

function isVideoFile(file) {
  return ['.mp4', '.mov', '.m4v', '.avi', '.mkv', '.webm'].includes(path.extname(file).toLowerCase());
}

function isCsvFile(file) {
  return DEFAULT_CSV_EXTENSIONS.has(path.extname(String(file || '')).toLowerCase());
}

function ensureSuccess(response, label) {
  if (!response || response.code !== 0) {
    const message = response?.msg || `${label} failed`;
    const error = new Error(message);
    error.response = response;
    throw error;
  }
  return response;
}

function unwrapAxiosError(error) {
  if (!error) return { message: 'unknown error', code: null };
  const data = error.response?.data || error.response || null;
  return {
    message: error.message || String(error),
    code: data?.code || error.code || null,
    data
  };
}

function isPermissionError(error) {
  const details = unwrapAxiosError(error);
  return new Set([1770040, 1061004]).has(Number(details.code));
}

function isRateLimitError(error) {
  const details = unwrapAxiosError(error);
  return Number(details.code) === 99991400 || Number(details.code) === 1254290 || Number(error?.response?.status) === 429 || /429/.test(String(details.message || ''));
}

function isTransientServerError(error) {
  const details = unwrapAxiosError(error);
  const status = Number(error?.response?.status || 0);
  return Number(details.code) === 1061001 || status >= 500;
}

function isFolderLockedError(error) {
  const details = unwrapAxiosError(error);
  return Number(details.code) === 1770036 || /folder locked/i.test(String(details.message || ''));
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function withRetry(fn, options = {}) {
  const retries = options.retries ?? 5;
  const baseDelay = options.baseDelay ?? 500;
  const shouldRetry = options.shouldRetry || (error => isRateLimitError(error));
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      if (attempt > 0 && options.onRetry) options.onRetry(attempt, lastError);
      return await fn(attempt);
    } catch (error) {
      lastError = error;
      if (!shouldRetry(error) || attempt === retries) {
        throw error;
      }
      const delay = baseDelay * Math.pow(2, attempt);
      await sleep(delay);
    }
  }
  throw lastError;
}

function extractBlockText(block) {
  if (!block || typeof block !== 'object') return '';
  if (block.text?.elements) {
    return block.text.elements
      .map(element => element?.text_run?.content || '')
      .join('');
  }
  if (block.heading1?.elements) {
    return block.heading1.elements.map(element => element?.text_run?.content || '').join('');
  }
  if (block.heading2?.elements) {
    return block.heading2.elements.map(element => element?.text_run?.content || '').join('');
  }
  if (block.heading3?.elements) {
    return block.heading3.elements.map(element => element?.text_run?.content || '').join('');
  }
  return '';
}

function sortBlocksByFirstLevel(blocks, firstLevelIds) {
  if (!Array.isArray(firstLevelIds) || !firstLevelIds.length) return blocks;
  const sorted = firstLevelIds
    .map(id => blocks.find(block => block.block_id === id))
    .filter(Boolean);
  const taken = new Set(firstLevelIds);
  const remaining = blocks.filter(block => !taken.has(block.block_id));
  return [...sorted, ...remaining];
}

function splitMarkdownByHeadings(markdown) {
  const lines = String(markdown || '').split('\n');
  const chunks = [];
  let current = [];
  let inFence = false;
  for (const line of lines) {
    if (/^(`{3,}|~{3,})/.test(line)) inFence = !inFence;
    if (!inFence && /^#{1,2}\s/.test(line) && current.length) {
      chunks.push(current.join('\n'));
      current = [];
    }
    current.push(line);
  }
  if (current.length) chunks.push(current.join('\n'));
  return chunks.filter(Boolean);
}

function isMarkdownTableLine(line) {
  const trimmed = String(line || '').trim();
  return /^\|.*\|$/.test(trimmed);
}

function isMarkdownTableSeparator(line) {
  const trimmed = String(line || '').trim();
  return /^\|(?:\s*:?-{3,}:?\s*\|)+$/.test(trimmed);
}

function parseMarkdownTableRow(line) {
  const trimmed = String(line || '').trim().replace(/^\|/, '').replace(/\|$/, '');
  const cells = [];
  let current = '';
  let escaped = false;
  for (const char of trimmed) {
    if (escaped) {
      current += char;
      escaped = false;
      continue;
    }
    if (char === '\\') {
      escaped = true;
      continue;
    }
    if (char === '|') {
      cells.push(current.trim());
      current = '';
      continue;
    }
    current += char;
  }
  cells.push(current.trim());
  return cells;
}

function normalizeMarkdownTable(headers, rows) {
  const columnCount = Math.max(headers.length, ...rows.map(row => row.length), 0);
  const normalizedHeaders = Array.from(
    { length: columnCount },
    (_, index) => String(headers[index] || `字段${index + 1}`).trim() || `字段${index + 1}`
  );
  const normalizedRows = rows.map(row =>
    Array.from({ length: columnCount }, (_, index) => String(row[index] || '').trim())
  );
  return { headers: normalizedHeaders, rows: normalizedRows };
}

function transformMarkdownTablesForFeishu(markdown) {
  return String(markdown || '').replace(/\r/g, '');
}

function splitMarkdownBySize(markdown, maxChars) {
  if (!markdown || markdown.length <= maxChars) return [markdown];
  const lines = markdown.split('\n');
  const chunks = [];
  let current = [];
  let currentLength = 0;
  let inFence = false;
  for (const line of lines) {
    if (/^(`{3,}|~{3,})/.test(line)) inFence = !inFence;
    const nextLength = currentLength + line.length + 1;
    if (current.length && nextLength > maxChars && !inFence) {
      chunks.push(current.join('\n'));
      current = [];
      currentLength = 0;
    }
    current.push(line);
    currentLength += line.length + 1;
  }
  if (current.length) chunks.push(current.join('\n'));
  if (chunks.length > 1) return chunks;
  const midpoint = Math.floor(lines.length / 2);
  if (midpoint <= 0 || midpoint >= lines.length) return [markdown];
  return [lines.slice(0, midpoint).join('\n'), lines.slice(midpoint).join('\n')];
}

function buildWriteChunks(markdown, options = {}) {
  const maxChunkChars = Number.isInteger(options.maxChunkChars) ? options.maxChunkChars : 6000;
  return splitMarkdownByHeadings(markdown)
    .flatMap(chunk => splitMarkdownBySize(chunk, maxChunkChars))
    .map(chunk => String(chunk || '').trim())
    .filter(Boolean);
}

function createWriteDocPlan(markdown, options = {}) {
  const preparedMarkdown = transformMarkdownTablesForFeishu(markdown);
  const forceMarkdown = Boolean(options.forceMarkdown);
  const mode = !forceMarkdown && shouldUsePlainTextMode(preparedMarkdown)
    ? 'plain_text_document'
    : 'markdown_document';
  const chunks = mode === 'plain_text_document'
    ? [preparedMarkdown].filter(Boolean)
    : buildWriteChunks(preparedMarkdown, { maxChunkChars: options.maxChunkChars });
  const requestedStart = Number.isInteger(options.startChunkIndex) ? options.startChunkIndex : 0;
  const startChunkIndex = Math.max(0, Math.min(requestedStart, Math.max(chunks.length - 1, 0)));
  return {
    mode,
    preparedMarkdown,
    chunks,
    totalChunks: chunks.length,
    startChunkIndex,
    remainingChunks: chunks.slice(startChunkIndex),
    forceMarkdown,
    maxChunkChars: options.maxChunkChars
  };
}

async function convertMarkdown(client, markdown) {
  const response = await client.docx.document.convert({
    data: {
      content_type: 'markdown',
      content: markdown
    }
  });
  ensureSuccess(response, 'document.convert');
  return {
    blocks: response.data?.blocks || [],
    firstLevelBlockIds: response.data?.first_level_block_ids || []
  };
}

async function convertMarkdownWithFallback(client, markdown, depth = 0) {
  try {
    return await convertMarkdown(client, markdown);
  } catch (error) {
    if (depth >= 8 || !markdown || markdown.length < 2) throw error;
    const chunks = splitMarkdownBySize(markdown, Math.max(256, Math.floor(markdown.length / 2)));
    if (chunks.length <= 1) throw error;
    const blocks = [];
    const firstLevelBlockIds = [];
    for (const chunk of chunks) {
      const converted = await convertMarkdownWithFallback(client, chunk, depth + 1);
      blocks.push(...converted.blocks);
      firstLevelBlockIds.push(...converted.firstLevelBlockIds);
    }
    return { blocks, firstLevelBlockIds };
  }
}

async function chunkedConvertMarkdown(client, markdown) {
  const chunks = splitMarkdownByHeadings(markdown);
  const blocks = [];
  const firstLevelBlockIds = [];
  for (const chunk of chunks) {
    const converted = await convertMarkdownWithFallback(client, chunk);
    const sorted = sortBlocksByFirstLevel(converted.blocks, converted.firstLevelBlockIds);
    blocks.push(...sorted);
    firstLevelBlockIds.push(...converted.firstLevelBlockIds);
  }
  return { blocks, firstLevelBlockIds };
}

function cleanBlockForChildrenCreate(block) {
  const cleaned = JSON.parse(JSON.stringify(block));
  delete cleaned.block_id;
  delete cleaned.parent_id;
  delete cleaned.children;
  if (cleaned.block_type === 31 || cleaned.block_type === 32) return null;
  if (cleaned.table?.merge_info) delete cleaned.table.merge_info;
  if (cleaned.table?.property?.merge_info) delete cleaned.table.property.merge_info;
  return cleaned;
}

async function insertBlocksIndividually(client, docToken, blocks, options = {}) {
  const parentBlockId = options.parentBlockId || docToken;
  const inserted = [];
  let skipped = 0;
  let cursorIndex = Number.isInteger(options.index) ? options.index : -1;
  for (const block of blocks) {
    const cleaned = cleanBlockForChildrenCreate(block);
    if (!cleaned) {
      skipped += 1;
      continue;
    }
    const response = await withRetry(() => client.docx.documentBlockChildren.create({
      path: {
        document_id: docToken,
        block_id: parentBlockId
      },
      data: {
        children: [cleaned],
        index: cursorIndex
      }
    }), { retries: 6, baseDelay: 400 });
    ensureSuccess(response, 'documentBlockChildren.create');
    const createdChildren = response.data?.children || [];
    inserted.push(...createdChildren);
    if (cursorIndex >= 0 && createdChildren.length) {
      cursorIndex += createdChildren.length;
    }
    if (options.throttleMs) {
      await sleep(options.throttleMs);
    }
  }
  return { children: inserted, skipped };
}

function splitTextForBlocks(text, maxChars = 1200) {
  const normalized = String(text || '').replace(/\r/g, '');
  if (!normalized) return [];
  const paragraphs = normalized
    .split('\n')
    .map(line => line.trimEnd())
    .filter(line => line.length > 0);
  const chunks = [];
  let current = '';
  for (const paragraph of paragraphs) {
    const parts = [];
    if (paragraph.length <= maxChars) {
      parts.push(paragraph);
    } else {
      let remaining = paragraph;
      while (remaining.length > maxChars) {
        const slice = remaining.slice(0, maxChars);
        const lastBreak = Math.max(slice.lastIndexOf(' '), slice.lastIndexOf('，'), slice.lastIndexOf('。'), slice.lastIndexOf('；'));
        const cut = lastBreak > 100 ? lastBreak + 1 : maxChars;
        parts.push(remaining.slice(0, cut).trim());
        remaining = remaining.slice(cut).trim();
      }
      if (remaining) parts.push(remaining);
    }
    for (const part of parts) {
      const candidate = current ? `${current}\n${part}` : part;
      if (candidate.length <= maxChars) {
        current = candidate;
      } else {
        if (current) chunks.push(current);
        current = part;
      }
    }
  }
  if (current) chunks.push(current);
  return chunks;
}

function lineToPlainBlock(line) {
  const content = String(line).trim();
  const elements = [{ text_run: { content: content || ' ' } }];
  return { block_type: 2, text: { elements } };
}

function shouldUsePlainTextMode(markdown) {
  const text = String(markdown || '');
  const codeFenceCount = (text.match(/^```/gm) || []).length;
  return (
    text.length > 20000 ||
    codeFenceCount >= 2
  );
}

async function insertPlainTextChunk(client, docToken, markdown, options = {}) {
  const lines = splitTextForBlocks(markdown);
  if (!lines.length) return { inserted: 0, blockIds: [], mode: 'plain_text' };
  const blocks = lines.map(lineToPlainBlock);
  const inserted = await insertBlocksIndividually(client, docToken, blocks, {
    parentBlockId: options.parentBlockId || docToken,
    index: Number.isInteger(options.index) ? options.index : -1,
    throttleMs: options.throttleMs ?? 120
  });
  return {
    inserted: inserted.children.length,
    blockIds: inserted.children.map(item => item.block_id).filter(Boolean),
    mode: 'plain_text'
  };
}

async function insertMarkdownChunk(client, docToken, markdown, optionsOrDepth = 0, maybeDepth = 0) {
  const options = typeof optionsOrDepth === 'object' && optionsOrDepth !== null ? optionsOrDepth : {};
  const depth = typeof optionsOrDepth === 'number' ? optionsOrDepth : maybeDepth;
  const parentBlockId = options.parentBlockId || docToken;
  const insertIndex = Number.isInteger(options.index) ? options.index : -1;

  const { blocks, firstLevelBlockIds } = await convertMarkdownWithFallback(client, markdown);
  if (!blocks.length) return { inserted: 0, blockIds: [] };
  const sorted = sortBlocksByFirstLevel(blocks, firstLevelBlockIds);
  const hasTableBlocks = sorted.some(block => block.block_type === 31 || block.block_type === 32);
  try {
    const inserted = await withRetry(() => insertBlocksWithDescendant(client, docToken, sorted, firstLevelBlockIds, {
      parentBlockId,
      index: insertIndex
    }), {
      retries: 3,
      baseDelay: 600
    });
    return {
      inserted: sorted.length,
      blockIds: (inserted.children || []).map(item => item.block_id).filter(Boolean)
    };
  } catch (error) {
    const details = unwrapAxiosError(error);
    if (Number(details.code) === 1770001) {
      if (!hasTableBlocks) {
        try {
          const inserted = await insertBlocksIndividually(client, docToken, sorted, {
            parentBlockId,
            index: insertIndex,
            throttleMs: 180
          });
          return {
            inserted: inserted.children.length,
            blockIds: inserted.children.map(item => item.block_id).filter(Boolean)
          };
        } catch (childError) {
          const childDetails = unwrapAxiosError(childError);
          if (!new Set([1770001, 99992402]).has(Number(childDetails.code)) && !isRateLimitError(childError)) throw childError;
        }
      }
    }
    if (depth >= 8 || !markdown || markdown.length < 128) throw error;
    if (!new Set([1770001, 99992402]).has(Number(details.code)) && !isRateLimitError(error)) throw error;
    const smallerChunks = splitMarkdownBySize(markdown, Math.max(256, Math.floor(markdown.length / 2)));
    if (smallerChunks.length <= 1) {
      return insertPlainTextChunk(client, docToken, markdown, {
        parentBlockId,
        index: insertIndex,
        throttleMs: 220
      });
    }
    let inserted = 0;
    const blockIds = [];
    let cursorIndex = insertIndex;
    for (const chunk of smallerChunks) {
      const chunkOptions = {
        parentBlockId,
        ...(cursorIndex >= 0 ? { index: cursorIndex } : {})
      };
      const result = await insertMarkdownChunk(client, docToken, chunk, chunkOptions, depth + 1);
      inserted += result.inserted;
      blockIds.push(...result.blockIds);
      if (cursorIndex >= 0) cursorIndex += result.inserted;
    }
    return { inserted, blockIds };
  }
}

function cleanBlocksForDescendant(blocks) {
  return (blocks || []).map(block => {
    const cleaned = { ...block };
    delete cleaned.parent_id;
    if (cleaned.block_type === 31 && cleaned.table?.merge_info) {
      const { merge_info, ...rest } = cleaned.table;
      cleaned.table = rest;
    }
    if (cleaned.block_type === 31 && cleaned.table?.property?.merge_info) {
      const property = { ...cleaned.table.property };
      delete property.merge_info;
      cleaned.table = {
        ...cleaned.table,
        property
      };
    }
    if (cleaned.block_type === 32 && typeof cleaned.children === 'string') {
      cleaned.children = [cleaned.children];
    }
    return cleaned;
  });
}

async function insertBlocksWithDescendant(client, docToken, blocks, firstLevelBlockIds, options = {}) {
  const descendants = cleanBlocksForDescendant(blocks);
  if (!descendants.length) return { children: [] };
  const response = await client.docx.documentBlockDescendant.create({
    path: {
      document_id: docToken,
      block_id: options.parentBlockId || docToken
    },
    data: {
      children_id: firstLevelBlockIds,
      descendants,
      index: options.index ?? -1
    }
  });
  ensureSuccess(response, 'documentBlockDescendant.create');
  return { children: response.data?.children || [] };
}

async function clearDocumentContent(client, docToken) {
  const allBlocks = await listAllBlocks(client, docToken);
  const childIds = allBlocks
    .filter(block => block.parent_id === docToken && block.block_type !== 1)
    .map(block => block.block_id);
  if (!childIds.length) return 0;

  let removed = 0;
  while (removed < childIds.length) {
    const remaining = childIds.length - removed;
    const chunkSize = Math.min(remaining, 200);
    const deleted = await client.docx.documentBlockChildren.batchDelete({
      path: {
        document_id: docToken,
        block_id: docToken
      },
      data: {
        start_index: 0,
        end_index: chunkSize
      }
    });
    ensureSuccess(deleted, 'documentBlockChildren.batchDelete');
    removed += chunkSize;
    await sleep(120);
  }

  return removed;
}

async function writeDocSection(client, docToken, markdown, options = {}) {
  const mode = options.mode || (
    !Boolean(options.forceMarkdown) && shouldUsePlainTextMode(markdown)
      ? 'plain_text_document'
      : 'markdown_document'
  );
  if (mode === 'plain_text_document') {
    return insertPlainTextChunk(client, docToken, markdown, {
      parentBlockId: options.parentBlockId || docToken,
      index: Number.isInteger(options.index) ? options.index : -1,
      throttleMs: options.throttleMs ?? 120
    });
  }
  return insertMarkdownChunk(client, docToken, markdown, {
    parentBlockId: options.parentBlockId || docToken,
    ...(Number.isInteger(options.index) ? { index: options.index } : {})
  });
}

async function resumeDocWrite(client, docToken, markdown, options = {}) {
  const plan = createWriteDocPlan(markdown, options);
  const deleted = options.clearDocument === false ? 0 : await clearDocumentContent(client, docToken);
  if (!plan.remainingChunks.length) {
    return {
      success: true,
      blocks_deleted: deleted,
      blocks_added: 0,
      block_ids: [],
      mode: plan.mode,
      total_chunks: plan.totalChunks,
      completed_chunks: 0,
      start_chunk_index: plan.startChunkIndex
    };
  }
  let blocksAdded = 0;
  const blockIds = [];
  let completedChunks = 0;
  let cursorIndex = Number.isInteger(options.index) ? options.index : -1;
  for (const chunk of plan.remainingChunks) {
    let result;
    try {
      result = await writeDocSection(client, docToken, chunk, {
        mode: plan.mode,
        forceMarkdown: plan.forceMarkdown,
        parentBlockId: options.parentBlockId || docToken,
        ...(cursorIndex >= 0 ? { index: cursorIndex } : {})
      });
    } catch (error) {
      result = await insertPlainTextChunk(client, docToken, chunk, {
        parentBlockId: options.parentBlockId || docToken,
        ...(cursorIndex >= 0 ? { index: cursorIndex } : {}),
        throttleMs: 120
      });
    }
    blocksAdded += result.inserted;
    blockIds.push(...result.blockIds);
    completedChunks += 1;
    if (cursorIndex >= 0) {
      cursorIndex += result.inserted;
    }
    await sleep(120);
  }
  return {
    success: true,
    blocks_deleted: deleted,
    blocks_added: blocksAdded,
    block_ids: blockIds,
    mode: plan.mode,
    total_chunks: plan.totalChunks,
    completed_chunks: completedChunks,
    start_chunk_index: plan.startChunkIndex
  };
}

async function writeDoc(client, docToken, markdown, options = {}) {
  return resumeDocWrite(client, docToken, markdown, {
    ...options,
    clearDocument: options.clearDocument !== false,
    startChunkIndex: 0
  });
}

async function listAllBlocks(client, docToken) {
  const items = [];
  let pageToken = null;
  let safety = 0;

  while (safety < 200) {
    const response = await client.docx.documentBlock.list({
      path: { document_id: docToken },
      params: {
        page_size: 500,
        ...(pageToken ? { page_token: pageToken } : {})
      }
    });
    ensureSuccess(response, 'documentBlock.list');
    const data = response.data || {};
    items.push(...(data.items || []));

    const hasMore = Boolean(data.has_more);
    pageToken = data.page_token || data.next_page_token || null;
    if (!hasMore || !pageToken) break;
    safety += 1;
  }

  return items;
}

async function listBlocks(client, docToken) {
  return listAllBlocks(client, docToken);
}

async function getBlock(client, docToken, blockId) {
  const response = await client.docx.documentBlock.get({
    path: {
      document_id: docToken,
      block_id: blockId
    }
  });
  ensureSuccess(response, 'documentBlock.get');
  return response.data?.block || null;
}

async function getSiblingContext(client, docToken, blockId) {
  const block = await getBlock(client, docToken, blockId);
  const parentBlockId = block?.parent_id || docToken;
  const children = await client.docx.documentBlockChildren.get({
    path: {
      document_id: docToken,
      block_id: parentBlockId
    }
  });
  ensureSuccess(children, 'documentBlockChildren.get');
  const items = children.data?.items || [];
  const index = items.findIndex(item => item.block_id === blockId);
  return { block, parentBlockId, siblings: items, index };
}

async function updateBlockText(client, docToken, blockId, content) {
  const response = await client.docx.documentBlock.patch({
    path: {
      document_id: docToken,
      block_id: blockId
    },
    data: {
      update_text_elements: {
        elements: [{ text_run: { content } }]
      }
    }
  });
  ensureSuccess(response, 'documentBlock.patch');
  return { success: true, block_id: blockId };
}

async function uploadImageBlock(client, docToken, filePath, options = {}) {
  const buffer = fs.readFileSync(filePath.startsWith('~') ? filePath.replace(/^~/, homedir()) : filePath);
  const filename = options.filename || path.basename(filePath);
  const insert = await client.docx.documentBlockChildren.create({
    path: {
      document_id: docToken,
      block_id: options.parentBlockId || docToken
    },
    params: { document_revision_id: -1 },
    data: {
      children: [{ block_type: 27, image: {} }],
      index: options.index ?? -1
    }
  });
  ensureSuccess(insert, 'documentBlockChildren.create(image)');
  const imageBlockId = (insert.data?.children || []).find(item => item.block_type === 27)?.block_id;
  if (!imageBlockId) throw new Error('未能创建图片 block');

  const upload = await client.drive.media.uploadAll({
    data: {
      file_name: filename,
      parent_type: 'docx_image',
      parent_node: imageBlockId,
      size: buffer.length,
      file: buffer,
      extra: JSON.stringify({ drive_route_token: docToken })
    }
  });
  const fileToken = upload?.file_token;
  if (!fileToken) throw new Error('图片上传失败：未返回 file_token');

  const patched = await client.docx.documentBlock.patch({
    path: {
      document_id: docToken,
      block_id: imageBlockId
    },
    data: {
      replace_image: { token: fileToken }
    }
  });
  ensureSuccess(patched, 'documentBlock.patch(replace_image)');
  return {
    success: true,
    block_id: imageBlockId,
    file_token: fileToken,
    url: buildFileUrl(fileToken, loadFeishuRuntimeConfig().host)
  };
}

function parseCsvLine(line) {
  const cells = [];
  let current = '';
  let inQuotes = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      const next = line[index + 1];
      if (inQuotes && next === '"') {
        current += '"';
        index += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }
    if (char === ',' && !inQuotes) {
      cells.push(current);
      current = '';
      continue;
    }
    current += char;
  }
  cells.push(current);
  return cells;
}

function csvToMarkdownTable(csvText, options = {}) {
  const maxRows = Number.isInteger(options.maxRows) ? options.maxRows : 12;
  const maxColumns = Number.isInteger(options.maxColumns) ? options.maxColumns : 12;
  const lines = String(csvText || '')
    .replace(/^\uFEFF/, '')
    .split(/\r?\n/)
    .filter(line => line.trim().length > 0);
  if (!lines.length) return '';

  const rows = lines.map(parseCsvLine);
  const width = Math.max(...rows.map(row => row.length), 0);
  const columnCount = Math.max(1, Math.min(width, maxColumns));
  const normalized = rows
    .slice(0, maxRows)
    .map(row => Array.from({ length: columnCount }, (_, index) => String(row[index] || '').trim()));

  const escapeCell = value => value.replace(/\|/g, '\\|').replace(/\n/g, ' ');
  const renderRow = row => `| ${row.map(escapeCell).join(' | ')} |`;
  const header = normalized[0];
  const divider = Array.from({ length: columnCount }, () => '---');
  const body = normalized.slice(1);

  const output = [renderRow(header), renderRow(divider), ...body.map(renderRow)];
  if (rows.length > maxRows) {
    output.push('', `> 注：表格已截断，仅展示前 ${maxRows} 行。`);
  }
  return output.join('\n');
}

function isHeadingBlock(block) {
  return Boolean(block?.heading1 || block?.heading2 || block?.heading3);
}

async function deleteChildRange(client, docToken, parentBlockId, startIndex, endIndex) {
  if (!(startIndex >= 0) || !(endIndex > startIndex)) return 0;
  let removed = 0;
  let cursor = startIndex;
  while (cursor < endIndex) {
    const chunkEnd = Math.min(endIndex, cursor + 200);
    const response = await client.docx.documentBlockChildren.batchDelete({
      path: {
        document_id: docToken,
        block_id: parentBlockId
      },
      data: {
        start_index: cursor,
        end_index: chunkEnd
      }
    });
    ensureSuccess(response, 'documentBlockChildren.batchDelete');
    removed += (chunkEnd - cursor);
    endIndex -= (chunkEnd - cursor);
    await sleep(120);
  }
  return removed;
}

async function clearSectionAfterBlock(client, docToken, blockId) {
  const sibling = await getSiblingContext(client, docToken, blockId);
  const startIndex = sibling.index + 1;
  if (startIndex < 1 || startIndex >= sibling.siblings.length) {
    return { deleted: 0, parentBlockId: sibling.parentBlockId, startIndex };
  }

  let endIndex = sibling.siblings.length;
  for (let index = startIndex; index < sibling.siblings.length; index += 1) {
    const candidate = sibling.siblings[index];
    if (isHeadingBlock(candidate)) {
      endIndex = index;
      break;
    }
  }

  const deleted = await deleteChildRange(client, docToken, sibling.parentBlockId, startIndex, endIndex);
  return {
    deleted,
    parentBlockId: sibling.parentBlockId,
    startIndex
  };
}

async function clearSectionAfterHeading(client, docToken, headingText) {
  const blocks = await listBlocks(client, docToken);
  const normalizedHeading = String(headingText || '').trim();
  const heading = blocks.find(block => {
    const text = String(extractBlockText(block) || '').trim();
    return text === normalizedHeading || text.includes(normalizedHeading);
  });
  if (!heading) return { deleted: 0, missing: true };
  return clearSectionAfterBlock(client, docToken, heading.block_id);
}

async function insertMarkdownAfterBlock(client, docToken, blockId, markdown) {
  const sibling = await getSiblingContext(client, docToken, blockId);
  return insertMarkdownChunk(client, docToken, transformMarkdownTablesForFeishu(markdown), {
    parentBlockId: sibling.parentBlockId,
    index: sibling.index + 1
  });
}

async function writeDocTable(client, docToken, markdownTable, options = {}) {
  const normalizedMarkdown = transformMarkdownTablesForFeishu(markdownTable);
  if (options.afterBlockId) {
    return insertMarkdownAfterBlock(client, docToken, options.afterBlockId, normalizedMarkdown);
  }
  return writeDocSection(client, docToken, normalizedMarkdown, {
    mode: 'markdown_document',
    parentBlockId: options.parentBlockId || docToken,
    ...(Number.isInteger(options.index) ? { index: options.index } : {})
  });
}

async function writeDocAssets(client, docToken, assets = [], options = {}) {
  const details = [];
  let inserted = 0;
  for (const asset of assets) {
    const filePath = asset.filePath || asset.path;
    if (!filePath) {
      details.push({ status: 'missing_path', asset });
      continue;
    }
    const normalizedPath = filePath.startsWith('~') ? filePath.replace(/^~/, homedir()) : filePath;
    if (!fs.existsSync(normalizedPath)) {
      details.push({ status: 'missing_file', file_path: normalizedPath, asset });
      continue;
    }
    if (isImageFile(normalizedPath)) {
      const result = await uploadImageBlock(client, docToken, normalizedPath, {
        parentBlockId: options.parentBlockId || docToken,
        ...(Number.isInteger(options.index) ? { index: options.index } : {}),
        filename: path.basename(normalizedPath)
      });
      details.push({ status: 'image_inserted', file_path: normalizedPath, ...result });
      inserted += 1;
      continue;
    }
    if (isCsvFile(normalizedPath)) {
      const markdownTable = csvToMarkdownTable(fs.readFileSync(normalizedPath, 'utf8'));
      const result = await writeDocTable(client, docToken, markdownTable, {
        parentBlockId: options.parentBlockId || docToken,
        ...(Number.isInteger(options.index) ? { index: options.index } : {})
      });
      details.push({ status: 'csv_table_inserted', file_path: normalizedPath, ...result });
      inserted += 1;
      continue;
    }
    if (isVideoFile(normalizedPath)) {
      const markdownVideoLink = `> 视频素材链接：[${path.basename(normalizedPath)}](file://${normalizedPath})`;
      const result = await writeDocSection(client, docToken, markdownVideoLink, {
        mode: 'markdown_document',
        parentBlockId: options.parentBlockId || docToken,
        ...(Number.isInteger(options.index) ? { index: options.index } : {})
      });
      details.push({ status: 'video_link_inserted', file_path: normalizedPath, ...result });
      inserted += 1;
      continue;
    }
    details.push({ status: 'unsupported_asset_type', file_path: normalizedPath, asset });
  }
  return {
    success: true,
    inserted,
    details
  };
}

async function createFolder(client, name, folderToken, host) {
  const response = await withRetry(
    () => client.drive.file.createFolder({
      data: {
        name,
        ...(folderToken ? { folder_token: folderToken } : {})
      }
    }),
    {
      retries: 3,
      baseDelay: 1200,
      shouldRetry: error => isRateLimitError(error) || isTransientServerError(error) || isFolderLockedError(error)
    }
  );
  ensureSuccess(response, 'drive.file.createFolder');
  const token = response.data?.token || response.data?.file?.token || response.data?.folder?.token || null;
  return {
    token,
    name: response.data?.name || response.data?.file?.name || name,
    url: token ? buildFolderUrl(token, host) : null
  };
}

async function createDoc(client, title, folderToken, host) {
  const response = await withRetry(
    () => client.docx.document.create({
      data: {
        title,
        ...(folderToken ? { folder_token: folderToken } : {})
      }
    }),
    {
      retries: 4,
      baseDelay: 1500,
      shouldRetry: error => isRateLimitError(error) || isTransientServerError(error) || isFolderLockedError(error)
    }
  );
  ensureSuccess(response, 'docx.document.create');
  const token = response.data?.document?.document_id;
  return {
    doc_token: token,
    title: response.data?.document?.title || title,
    url: buildDocUrl(token, host)
  };
}

async function sendTextMessage(client, chatId, text) {
  const response = await client.im.message.create({
    params: { receive_id_type: 'chat_id' },
    data: {
      receive_id: chatId,
      content: JSON.stringify({ text }),
      msg_type: 'text'
    }
  });
  ensureSuccess(response, 'im.message.create');
  return {
    message_id: response.data?.message_id || null,
    url: response.data?.message_id ? `feishu://message/${response.data.message_id}` : null
  };
}

async function uploadDriveFile(client, folderToken, filePath, host) {
  const buffer = fs.readFileSync(filePath);
  const response = await withRetry(
    () => client.drive.media.uploadAll({
      data: {
        file_name: path.basename(filePath),
        parent_type: 'explorer',
        parent_node: folderToken,
        size: buffer.length,
        file: buffer
      }
    }),
    {
      retries: 3,
      baseDelay: 1200,
      shouldRetry: error => isRateLimitError(error) || isTransientServerError(error) || isFolderLockedError(error)
    }
  );
  const fileToken = response?.file_token || response?.data?.file_token || null;
  if (!fileToken) throw new Error(`上传文件失败: ${filePath}`);
  return {
    file_token: fileToken,
    file_name: path.basename(filePath),
    url: buildFileUrl(fileToken, host)
  };
}

function walkFiles(root) {
  if (!root || !fs.existsSync(root)) return [];
  const results = [];
  const queue = [root];
  while (queue.length) {
    const current = queue.shift();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) queue.push(fullPath);
      else if (entry.isFile()) results.push(fullPath);
    }
  }
  return results.sort();
}

function parseAnchorsFromMarkdown(markdown) {
  const regex = /\[素材锚点-([^-：]+)-(\d+)：([^｜\]]+?)｜([^｜\]]*?)｜([^｜\]]*?)｜`([^`]+)`\]/g;
  const anchors = [];
  let match;
  while ((match = regex.exec(markdown)) !== null) {
    anchors.push({
      raw: match[0],
      kind: match[1],
      index: match[2],
      label: match[3].trim(),
      position: match[4].trim(),
      format: match[5].trim(),
      filePath: match[6].trim()
    });
  }
  return anchors;
}

async function refillDocAnchorsWithLocalAssets(client, docToken, markdownFiles = [], options = {}) {
  const tableMaxPreviewRows = Number.isInteger(options.tableMaxPreviewRows)
    ? options.tableMaxPreviewRows
    : 12;
  const sourceContent = markdownFiles
    .filter(file => fs.existsSync(file))
    .map(file => fs.readFileSync(file, 'utf8'))
    .join('\n\n');
  const anchors = parseAnchorsFromMarkdown(sourceContent);
  if (!anchors.length) {
    return { success: true, anchors_total: 0, anchors_filled: 0, details: [] };
  }

  const blocks = await listBlocks(client, docToken);
  const details = [];
  let filled = 0;

  for (const anchor of anchors) {
    const markerWithLabel = `素材锚点-${anchor.kind}-${anchor.index}：${anchor.label}`;
    const marker = `素材锚点-${anchor.kind}-${anchor.index}`;
    const block = blocks.find(item => {
      const text = extractBlockText(item);
      if (!text) return false;
      return text.includes(markerWithLabel) || text.includes(marker) || text.includes(anchor.raw);
    });
    if (!block) {
      details.push({ anchor: anchor.raw, status: 'missing_block' });
      continue;
    }

    const normalizedPath = anchor.filePath.startsWith('~')
      ? anchor.filePath.replace(/^~/, homedir())
      : anchor.filePath;

    const caption = `【素材已回填】${anchor.label}｜${anchor.format}`;
    await updateBlockText(client, docToken, block.block_id, caption);

    if (!fs.existsSync(normalizedPath)) {
      details.push({ anchor: anchor.raw, status: 'missing_file', file_path: normalizedPath });
      continue;
    }

    if (isImageFile(normalizedPath)) {
      const sibling = await getSiblingContext(client, docToken, block.block_id);
      const inserted = await uploadImageBlock(client, docToken, normalizedPath, {
        parentBlockId: sibling.parentBlockId,
        index: sibling.index + 1,
        filename: path.basename(normalizedPath)
      });
      details.push({
        anchor: anchor.raw,
        status: 'image_inserted',
        file_path: normalizedPath,
        block_id: inserted.block_id,
        file_token: inserted.file_token,
        url: inserted.url
      });
      filled += 1;
      continue;
    }

    if (isCsvFile(normalizedPath)) {
      const csvText = fs.readFileSync(normalizedPath, 'utf8');
      const markdownTable = csvToMarkdownTable(csvText, { maxRows: tableMaxPreviewRows });
      if (!markdownTable) {
        details.push({
          anchor: anchor.raw,
          status: 'csv_empty',
          file_path: normalizedPath
        });
        continue;
      }
      const inserted = await writeDocTable(client, docToken, markdownTable, { afterBlockId: block.block_id });
      details.push({
        anchor: anchor.raw,
        status: 'csv_table_inserted',
        file_path: normalizedPath,
        inserted_blocks: inserted.inserted,
        block_ids: inserted.blockIds
      });
      filled += 1;
      continue;
    }

    if (isVideoFile(normalizedPath)) {
      const markdownVideoLink = `> 视频素材链接：[${path.basename(normalizedPath)}](file://${normalizedPath})`;
      const inserted = await insertMarkdownAfterBlock(client, docToken, block.block_id, markdownVideoLink);
      details.push({
        anchor: anchor.raw,
        status: 'video_link_inserted',
        file_path: normalizedPath,
        inserted_blocks: inserted.inserted,
        block_ids: inserted.blockIds
      });
      filled += 1;
      continue;
    }

    details.push({
      anchor: anchor.raw,
      status: 'unsupported_asset_type',
      file_path: normalizedPath
    });
  }

  return {
    success: true,
    anchors_total: anchors.length,
    anchors_filled: filled,
    details
  };
}

module.exports = {
  createClient,
  loadFeishuRuntimeConfig,
  buildDocUrl,
  buildFolderUrl,
  buildFileUrl,
  unwrapAxiosError,
  isPermissionError,
  extractBlockText,
  createWriteDocPlan,
  writeDocSection,
  writeDocTable,
  writeDocAssets,
  resumeDocWrite,
  writeDoc,
  listBlocks,
  getBlock,
  getSiblingContext,
  updateBlockText,
  uploadImageBlock,
  clearSectionAfterBlock,
  clearSectionAfterHeading,
  createFolder,
  createDoc,
  sendTextMessage,
  uploadDriveFile,
  walkFiles,
  refillDocAnchorsWithLocalAssets,
  isImageFile,
  isCsvFile,
  insertMarkdownChunk,
  transformMarkdownTablesForFeishu
};

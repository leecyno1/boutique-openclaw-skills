#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {
  nowIso,
  readJsonIfExists,
  writeJson,
  sha1,
  markStepCompleted,
  markStepFailed,
  finishManifest
} = require('../dasheng-daily-shared/runtime/manifest');
const {
  persistArtifact,
  appendArtifactRef
} = require('../dasheng-daily-shared/runtime/artifact-store');

const SHARED_DIR = path.join(__dirname, '..', 'dasheng-daily-shared');
const RUNTIME_DIR = path.join(SHARED_DIR, 'runtime-data');
const CONFIG_FILE = path.join(__dirname, 'config.json');

function loadSkillConfig() {
  const fallback = {
    draft_policy: {
      standard_version: 'draft-standard-v2',
      style: 'standard_article',
      article_style_mode: 'standard_article',
      disable_style_dna: true,
      min_chars: 5000,
      required_sections: ['开篇立论', '核心论证', '数据证据与论据', '关键数据表', '策略与执行建议', '数据与素材来源'],
      required_tables: 2,
      required_sources: 3,
      require_real_source_urls: true,
      allow_source_placeholders: false,
      forbid_intake_internal_data: true,
      internal_data_terms: ['intake', 'intake统计', '底稿统计', '流程统计', '工作流统计', '内部统计', '跨平台扩散', 's/a占比'],
      external_data_channels: ['akshare', 'tushare', '新浪财经', '人民网', 'cnn'],
      max_paragraphs_per_section: 5,
      min_numeric_points: 8,
      banned_terms: ['brief', '第二环节', 'run_id', '提示词', '模型参数', '采集流程', 'SOP群', 'lemon_dna', '风格DNA'],
      rewrite_model_mode: 'bm',
      auto_rewrite_for_copy_and_voice: true,
      pure_prose_only: true
    }
  };

  if (!fs.existsSync(CONFIG_FILE)) {
    return fallback;
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    return {
      ...fallback,
      ...parsed,
      draft_policy: {
        ...fallback.draft_policy,
        ...(parsed.draft_policy || {})
      }
    };
  } catch (error) {
    return fallback;
  }
}

async function generateDraft(outlinePlansFile, options = {}) {
  let manifest;
  let manifestFile;

  try {
    const config = loadSkillConfig();
    const plansFile = outlinePlansFile || options.outline_plans_file;
    if (!plansFile || !fs.existsSync(plansFile)) {
      throw new Error('缺少 outline_plans_file');
    }

    const raw = JSON.parse(fs.readFileSync(plansFile, 'utf8'));
    const outlines = normalizeOutlines(raw);
    if (!outlines.length) {
      throw new Error('outline-plans 为空，无法生成初稿');
    }

    const runId = options.run_id || outlines?.[0]?.meta?.run_id;
    if (!runId) {
      throw new Error('无法从 OutlinePlan 推断 run_id');
    }

    manifestFile = path.join(RUNTIME_DIR, 'runs', runId, 'run_manifest.json');
    manifest = readJsonIfExists(manifestFile);
    if (!manifest) {
      throw new Error(`manifest 不存在: ${manifestFile}`);
    }

    console.log(`[draft] 开始生成初稿 run_id=${runId}`);

    const policy = buildRuntimePolicy(config, options);
    const drafts = outlines.map(outline => buildDraftPackage(outline, runId, policy));

    const draftFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'draft',
      name: 'draft-packages.json',
      data: drafts
    });

    const qualityReport = buildQualityReport(drafts, policy);
    const qualityFile = persistArtifact({
      baseDir: RUNTIME_DIR,
      runId,
      step: 'draft',
      name: 'draft-quality-report.json',
      data: qualityReport
    });

    manifest = appendArtifactRef(manifest, {
      step: 'draft',
      object_type: 'DraftPackage',
      count: drafts.length,
      file: draftFile,
      doc_url: null
    });

    manifest = appendArtifactRef(manifest, {
      step: 'draft',
      object_type: 'DraftQualityReport',
      count: qualityReport.total_drafts,
      file: qualityFile,
      doc_url: null
    });

    manifest = markStepCompleted(manifest, 'draft');
    manifest.current_step = 'final';
    manifest = finishManifest(manifest);
    writeJson(manifestFile, manifest);

    console.log(`[draft] 完成，共 ${drafts.length} 条初稿`);

    return {
      success: true,
      run_id: runId,
      total_drafts: drafts.length,
      draft_packages_file: draftFile,
      draft_quality_report_file: qualityFile,
      manifest_file: manifestFile,
      next_step: 'dasheng-daily-final',
      quality_summary: {
        pass_count: qualityReport.pass_count,
        fail_count: qualityReport.fail_count,
        min_chars: policy.min_chars,
        rewrite_model_mode: policy.rewrite_model_mode
      }
    };
  } catch (error) {
    if (manifest && manifestFile) {
      manifest = markStepFailed(manifest, 'draft', error.message);
      writeJson(manifestFile, manifest);
    }
    console.error('[draft] 错误:', error.message);
    throw error;
  }
}

function normalizeOutlines(raw) {
  if (Array.isArray(raw)) {
    return raw;
  }
  if (Array.isArray(raw?.items)) {
    return raw.items;
  }
  return [];
}

function buildRuntimePolicy(config, options) {
  const base = config.draft_policy || {};
  return {
    standard_version: base.standard_version || 'draft-standard-v2',
    style: String(base.style || 'standard_article'),
    article_style_mode: String(base.article_style_mode || 'standard_article'),
    disable_style_dna: base.disable_style_dna !== false,
    min_chars: Number(options.min_chars || base.min_chars || 5000),
    required_sections: Array.isArray(base.required_sections) && base.required_sections.length
      ? base.required_sections
      : ['开篇立论', '核心论证', '数据证据与论据', '关键数据表', '策略与执行建议', '数据与素材来源'],
    required_tables: Number(base.required_tables || 2),
    required_sources: Number(base.required_sources || 3),
    require_real_source_urls: base.require_real_source_urls !== false,
    allow_source_placeholders: base.allow_source_placeholders === true,
    forbid_intake_internal_data: base.forbid_intake_internal_data !== false,
    internal_data_terms: Array.isArray(base.internal_data_terms) && base.internal_data_terms.length
      ? base.internal_data_terms
      : ['intake', 'intake统计', '底稿统计', '流程统计', '工作流统计', '内部统计', '跨平台扩散', 's/a占比'],
    external_data_channels: Array.isArray(base.external_data_channels) ? base.external_data_channels : ['akshare', 'tushare', '新浪财经', '人民网', 'cnn'],
    max_paragraphs_per_section: Number(base.max_paragraphs_per_section || 5),
    min_numeric_points: Number(base.min_numeric_points || 8),
    banned_terms: Array.isArray(base.banned_terms) ? base.banned_terms : [],
    rewrite_model_mode: String(base.rewrite_model_mode || 'bm'),
    auto_rewrite_for_copy_and_voice: base.auto_rewrite_for_copy_and_voice !== false,
    pure_prose_only: base.pure_prose_only !== false
  };
}

function buildDraftPackage(outline, runId, policy) {
  const createdAt = nowIso();
  const content = generateDraftContent(outline, policy);
  const quality = checkDraftQuality(content, outline, policy);
  const suffix = String(outline?.meta?.id || outline?.topic_id || outline?.title || nowIso()).slice(-24);

  return {
    meta: {
      id: `${runId}:draft:${suffix}`,
      object_type: 'DraftPackage',
      run_id: runId,
      version: '5.0.0',
      standard_version: policy.standard_version,
      status: quality.pass ? 'ready' : 'review_required',
      generated_by: 'dasheng-daily-draft',
      input_digest: sha1((outline?.meta?.id || '') + (outline?.title || '')),
      upstream_ids: outline?.meta?.id ? [outline.meta.id] : [],
      doc_refs: [],
      created_at: createdAt,
      updated_at: createdAt
    },
    topic_id: outline.topic_id || null,
    title: outline.title || '未命名选题',
    style: policy.article_style_mode || policy.style || 'standard_article',
    content,
    word_count: quality.char_count,
    sections_used: getUsedSections(content),
    rewrite_policy: {
      auto_rewrite: policy.auto_rewrite_for_copy_and_voice,
      model_mode: policy.rewrite_model_mode,
      targets: ['copywriting', 'voiceover']
    },
    compliance: {
      pass: quality.pass,
      checks: quality,
      freeze_policy_applied: true
    },
    draft_notes: [
      '按 draft-standard-v2 固定标准生成（>=5000字、纯正文、数据、双表格、来源）',
      '语体固定标准文章，不注入风格 DNA',
      '禁止使用 intake/工作流内部统计词作为数据证据',
      `转写固定模式：${policy.rewrite_model_mode}`,
      '如需变更格式，必须先更新 config + 标准文档并获得用户确认'
    ]
  };
}

function generateDraftContent(outline, policy) {
  const title = outline?.title || '未命名选题';
  const sourceEntries = collectSourceEntries(outline);
  const analysisPoints = collectAnalysisPoints(outline, policy);
  const sourceEvidence = buildSourceEvidence(sourceEntries);

  const blocks = [];
  blocks.push(`# ${title}`);

  blocks.push('## 开篇立论');
  blocks.push(`这篇文章只处理一个核心问题：${title}在当下到底属于“短期情绪冲击”，还是“中期结构变化”。如果判断路径不清楚，任何观点都会变成噪音。`);
  blocks.push('判断一件事是否值得持续跟踪，关键不在于讨论度高低，而在于它是否进入“可验证、可复盘、可执行”的区间。只有这三点同时成立，内容才具备长期价值。');
  blocks.push(`本文只采用两类证据：底稿链接素材中的公开信息，或外部公开数据源补充信息。当前已纳入 ${sourceEvidence.total} 条可回查来源，后续结论均以这些来源为锚点。`);
  blocks.push('因此本文采用“变量拆解 -> 证据分层 -> 情景推演 -> 执行动作”的顺序，不追求漂亮结论，优先保证可执行结论。');

  blocks.push('## 核心论证');
  const coreParagraphs = buildCoreArgumentParagraphs(analysisPoints, title);
  blocks.push(...coreParagraphs);

  blocks.push('## 数据证据与论据');
  blocks.push(`当前纳入证据口径共 ${sourceEvidence.total} 条，其中 ${sourceEvidence.withNumeric} 条包含可直接引用的数字信息。真正有意义的不是孤立数字，而是“来源-数据-结论”是否形成同向链路。`);
  blocks.push('在论据组织上，建议采用“三层证据法”：主证据用于支撑主结论，辅证据用于补充解释，反证据用于定义边界。这样可以避免结论过拟合。');
  blocks.push('每一个核心判断都应对应至少一个可回查来源；每一个动作建议都应对应至少一个可观察指标。观点与证据脱节，文章就会变成叙事堆叠。');
  blocks.push(buildEvidenceTable(sourceEntries));

  blocks.push('## 关键数据表');
  blocks.push('为了让结论与动作一一对应，下面用两张表分别回答“证据来自哪里”和“动作如何触发”。');
  blocks.push(buildSourceSignalTable(sourceEntries));
  blocks.push(buildScenarioActionTable(title));

  blocks.push('## 策略与执行建议');
  blocks.push('第一步先确认变量层级：事实变量、预期变量、行为变量。任何时点都不要在变量未分层前直接下结论。');
  blocks.push('第二步再确认动作边界：触发条件、执行动作、失效条件要同时存在。只有触发没有失效，策略会在高波动阶段失真。');
  blocks.push('第三步建立复盘节奏：日内看噪音过滤，周度看结论稳定性，月度看框架是否需要重写。没有复盘，观点很难形成复用资产。');
  blocks.push('第四步是执行纪律：宁可因为确认慢半拍少赚，也不要因为叙事过热重仓追涨。长期收益来自一致的风险控制，而不是单次正确。');
  blocks.push('第五步是内容协同：主文先定框架，再拆文案与口播稿，确保跨平台转写时结论不走样、证据不丢失。');

  blocks.push('## 数据与素材来源');
  sourceEntries.forEach((item, index) => {
    blocks.push(`${index + 1}. ${item.url}`);
  });

  let content = joinBlocks(blocks);
  content = ensureRequiredSections(content, outline, policy.required_sections);
  content = expandToTargetChars(content, outline, policy.min_chars, policy.max_paragraphs_per_section, policy);
  content = enforceSectionParagraphLimit(content, policy.max_paragraphs_per_section);

  return `${content.trim()}\n`;
}

function buildCoreArgumentParagraphs(analysisPoints, title) {
  const cleaned = analysisPoints.map(item => sanitizeSentence(item)).filter(Boolean);
  const selected = cleaned.slice(0, 6);

  if (!selected.length) {
    return [
      `${title}的判断主线应从“变量变化、行为变化、结构变化”三层展开，避免只用单一叙事推导整体结论。`,
      '在变量尚未共振前，任何激进动作都应降权；在变量连续共振后，再提高动作强度。判断强度应跟随证据强度，而不是跟随情绪强度。',
      '真正可靠的结论必须带边界：何时成立、何时失效、失效后如何切换动作。没有边界的观点，在执行中往往不可用。',
      '内容价值不在“说服所有人”，而在“帮助读者做出可复盘的决策”。这要求每条主张都能回到证据，而不是回到修辞。',
      '如果一个判断无法落到行动清单，它在传播层可能有效，在决策层通常无效。'
    ];
  }

  const bridge = [
    '这一判断需要绑定触发信号与验证窗口，避免只给方向不给条件。',
    '要把结论转成动作，必须同时写清成立前提与失效边界。',
    '执行层面建议采用分层动作，而不是一次性强结论。',
    '当反向信号出现时，应优先降权再重估，而不是强行解释。',
    '只有证据与动作同步更新，结论才具备持续有效性。',
    '结论的价值不在措辞强度，而在可验证和可复盘。'
  ];

  return selected.map((point, idx) => {
    const base = sanitizeSentence(point).replace(/[。.!！?？]+$/g, '');
    return `${base}。${bridge[idx % bridge.length]}`;
  });
}

function sanitizeSentence(text) {
  return String(text || '')
    .replace(/\s+/g, ' ')
    .replace(/\.{2,}/g, '。')
    .replace(/[：:]+\s*$/, '')
    .trim();
}

function collectAnalysisPoints(outline, policy) {
  const sections = Array.isArray(outline?.sections) ? outline.sections : [];
  const points = [];
  for (const section of sections) {
    if (section?.content) {
      points.push(cleanInternalTerms(section.content, policy));
    }
    const subs = Array.isArray(section?.subsections) ? section.subsections : [];
    for (const sub of subs) {
      if (sub?.content) {
        points.push(cleanInternalTerms(sub.content, policy));
      }
    }
  }
  return points.filter(item => String(item || '').trim().length > 0);
}

function cleanInternalTerms(text, policy) {
  let result = String(text || '');
  if (!policy?.forbid_intake_internal_data) {
    return result;
  }

  const terms = Array.isArray(policy?.internal_data_terms) ? policy.internal_data_terms : [];
  for (const term of terms) {
    const escaped = String(term).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    result = result.replace(new RegExp(escaped, 'ig'), '');
  }

  return result
    .replace(/\s{2,}/g, ' ')
    .replace(/([：:，,。；;])\1+/g, '$1')
    .replace(/[\s，,。；;：:]+$/g, '')
    .trim();
}

function collectSourceEntries(outline) {
  const sections = Array.isArray(outline?.sections) ? outline.sections : [];
  const sourceSections = sections.filter(section => {
    const title = String(section?.title || '').toLowerCase();
    return title.includes('来源') || title.includes('素材') || title.includes('参考');
  });

  const lines = sourceSections
    .map(section => String(section?.content || ''))
    .join('\n')
    .split('\n')
    .map(line => line.trim())
    .filter(Boolean);

  const entries = [];
  for (const line of lines) {
    const urlMatches = line.match(/https?:\/\/[^\s)）]+/g) || [];
    for (const rawUrl of urlMatches) {
      const url = normalizeUrl(rawUrl);
      entries.push({
        raw: line,
        url,
        platform: detectPlatform(url),
        numeric_tokens: extractNumericTokens(line)
      });
    }
  }

  const deduped = [];
  const seen = new Set();
  for (const entry of entries) {
    if (!entry.url || seen.has(entry.url)) continue;
    deduped.push(entry);
    seen.add(entry.url);
  }

  return deduped;
}

function normalizeUrl(rawUrl) {
  return String(rawUrl || '').replace(/[),.;，。；]+$/g, '');
}

function detectPlatform(url) {
  const lower = String(url || '').toLowerCase();
  if (/akshare/.test(lower)) return 'AkShare';
  if (/tushare/.test(lower)) return 'TuShare';
  if (/sina\.com\.cn|finance\.sina\.com/.test(lower)) return '新浪财经';
  if (/people\.com\.cn/.test(lower)) return '人民网';
  if (/cnn\.com/.test(lower)) return 'CNN';
  if (/douyin\.com/.test(lower)) return '抖音';
  if (/xiaohongshu\.com/.test(lower)) return '小红书';
  if (/zhihu\.com/.test(lower)) return '知乎';
  if (/weibo\.cn|weibo\.com/.test(lower)) return '微博';
  if (/cls\.cn/.test(lower)) return '财联社';
  if (/x\.com/.test(lower)) return 'X';
  return '公开来源';
}

function extractNumericTokens(text) {
  const matches = String(text || '').match(/\d+(?:\.\d+)?%?/g) || [];
  return [...new Set(matches)].slice(0, 5);
}

function buildSourceEvidence(sourceEntries) {
  const withNumeric = sourceEntries.filter(item => Array.isArray(item.numeric_tokens) && item.numeric_tokens.length > 0).length;
  return {
    total: sourceEntries.length,
    withNumeric
  };
}

function buildEvidenceTable(sourceEntries) {
  const rows = sourceEntries.slice(0, 5).map((entry, idx) => {
    const values = Array.isArray(entry.numeric_tokens) && entry.numeric_tokens.length
      ? entry.numeric_tokens.join(' / ')
      : '以原文披露数据为准';
    return `| 证据${idx + 1} | ${entry.platform} | ${values} | ${entry.url} |`;
  });

  if (!rows.length) {
    rows.push('| 证据1 | 待补充 | 待补充真实数据 | 待补充真实来源链接 |');
  }

  return [
    '| 证据项 | 来源渠道 | 关键数据 | 来源链接 |',
    '| --- | --- | --- | --- |',
    ...rows
  ].join('\n');
}

function buildSourceSignalTable(sourceEntries) {
  const rows = sourceEntries.slice(0, 5).map((entry, idx) =>
    `| 样本${idx + 1} | ${entry.platform} | ${entry.url} | 作为可追溯证据锚点 |`
  );

  if (!rows.length) {
    rows.push('| 样本1 | 待补充 | 待补充真实来源链接 | 发布前必须替换真实来源 |');
  }

  return [
    '| 样本 | 平台 | 证据位置 | 决策用途 |',
    '| --- | --- | --- | --- |',
    ...rows
  ].join('\n');
}

function buildScenarioActionTable(title) {
  return [
    '| 情景 | 触发信号 | 建议动作 | 失效条件 |',
    '| --- | --- | --- | --- |',
    `| 基准情景 | 核心变量小幅波动、证据持续增量 | 维持主仓位，小步跟踪 ${title} 相关指标 | 关键变量出现反向共振 |`,
    `| 强化情景 | 热度与扩散同步抬升且资金行为确认 | 提高跟踪强度，执行分批动作与动态止损 | 证据链断裂或政策口径逆转 |`,
    `| 风险情景 | 叙事扩散快于事实验证、波动率明显放大 | 降低杠杆与仓位，优先保护回撤 | 新证据确认原结论仍成立 |`
  ].join('\n');
}

function joinBlocks(blocks) {
  return blocks.map(block => block.trim()).filter(Boolean).join('\n\n');
}

function ensureRequiredSections(content, outline, requiredSections) {
  let result = content;
  for (const heading of requiredSections) {
    if (hasHeading(result, heading)) {
      continue;
    }
    result += `\n\n## ${heading}\n\n${sectionTemplate(heading, outline)}\n`;
  }
  return result;
}

function sectionTemplate(heading, outline) {
  const title = outline?.title || '本选题';
  if (heading === '开篇立论') {
    return `${title}应以“先结论、再证据、后动作”的顺序展开，确保读者在前 1/3 处就获得清晰问题定义。`;
  }
  if (heading === '核心论证') {
    return `围绕核心命题建立主线，并给出成立条件、失效条件和替代解释，确保结论具备可复盘性。`;
  }
  if (heading === '数据证据与论据') {
    return `每条核心判断至少绑定一个可验证数据点，并说明数据与结论之间的因果链。`;
  }
  if (heading === '关键数据表') {
    return [
      '| 指标 | 数据/现象 | 含义 |',
      '| --- | --- | --- |',
      '| 核心变量 | 待补充 | 支撑主结论 |',
      '| 风险信号 | 待补充 | 定义边界条件 |',
      '| 执行动作 | 待补充 | 指导下一步决策 |'
    ].join('\n');
  }
  if (heading === '策略与执行建议') {
    return `执行建议必须写到动作层（何时做、做多少、错了怎么办），避免空泛口号。`;
  }
  if (heading === '数据与素材来源') {
    return ['1. 待补充真实来源链接（底稿素材或外部公开数据）', '2. 待补充真实来源链接（底稿素材或外部公开数据）', '3. 待补充真实来源链接（底稿素材或外部公开数据）'].join('\n');
  }
  return `${title}：该章节为固定结构补位，后续由编辑在二改时替换为真实证据。`;
}

function expandToTargetChars(content, outline, minChars, maxParagraphsPerSection, policy) {
  let result = content;
  const topic = outline?.title || '该选题';
  const cues = collectAnalysisPoints(outline, policy).map(sanitizeSentence).filter(Boolean).slice(0, 8);

  const depthSections = [
    {
      title: '变量拆解：先看什么，再看什么',
      paragraphs: [
        `${topic}在实操判断里，第一步不是找结论，而是先做变量拆解。先把事实变量、预期变量、行为变量分开，再确认三者之间有没有同向变化。`,
        '事实变量决定事件是否真实发生，预期变量决定价格是否提前交易，行为变量决定资金是否形成一致行动。三者若只动一项，通常是短波动；若连续共振，才值得提高动作强度。',
        `结合当前线索，${cues[0] || '核心争议'}更像“先交易预期，再验证事实”的结构。因此动作应该强调节奏管理，而不是单点重仓。`
      ]
    },
    {
      title: '证据分层：哪些能直接用，哪些只能参考',
      paragraphs: [
        '高传播内容并不等于高可信内容。来源可追溯、时间可核验、口径可复现的证据，应放在主论据层；观点型内容只能作为辅助论据。',
        '如果把辅助论据当主论据，文章会显得很有气势，但执行会明显失真。真正可复盘的写法，是让每个结论都能对应一条证据链。',
        `围绕“${cues[1] || '传播强度与执行价值'}”的讨论，建议采用“主证据 + 辅证据 + 反证提示”三段式，既保留可读性也保留严谨性。`
      ]
    },
    {
      title: '情景推演：把单一观点改成条件判断',
      paragraphs: [
        '条件判断比方向判断更有长期价值。因为市场与内容传播都处于动态系统里，变量的组合会不断变化。',
        '建议至少构建三种情景：基准情景、强化情景、风险情景。每个情景都要写清触发条件、观察指标和动作边界。',
        `就${topic}而言，${cues[2] || '核心命题'}更适合写成“触发条件 -> 对应动作 -> 失效处理”模板，后续转写为口播稿也不会丢逻辑。`
      ]
    },
    {
      title: '风险反证：主动回答“我什么时候会错”',
      paragraphs: [
        '高质量文章不只是证明自己对，更要主动说明自己何时可能错。反证机制越清晰，读者对结论的信任度越高。',
        '反证不是否定主观点，而是给主观点加边界。边界越清楚，动作越稳定；边界越模糊，动作越容易在高波动中变形。',
        `在本题里，可以把“${cues[3] || '变量失效条件'}”写成独立反证段，明确何时降权、何时暂停、何时重新评估。`
      ]
    },
    {
      title: '执行路径：从观点落到动作的最短链路',
      paragraphs: [
        '文章真正产生价值的时刻，不是读者看懂，而是读者能做。执行路径应尽量短：先看指标，再做判断，再设动作，最后复盘。',
        '动作建议要写到可操作粒度，例如“何时调整、调整幅度、观察周期、退出条件”。过于抽象的建议很难在真实场景执行。',
        `围绕${topic}，建议把动作分成“日内观察、周度复盘、月度校准”三层，兼顾速度与稳定性。`
      ]
    },
    {
      title: '复盘机制：保证结论可迭代而不是一次性',
      paragraphs: [
        '没有复盘的观点，不具备可复用性。每次输出后都应回看三件事：证据是否充分、动作是否有效、边界是否需要重设。',
        '复盘不是事后解释，而是下一轮优化的输入。持续复盘能把一次正确变成一类正确，把偶然收益变成可复制收益。',
        `建议在文末固定保留“后续观察点”，把${cues[4] || '关键变量'}列为下一轮更新触发器。`
      ]
    },
    {
      title: '组织协同：如何避免“写得好但用不好”',
      paragraphs: [
        '很多内容在发布端表现不错，却在执行端价值不足，根因通常是“写作逻辑”和“决策逻辑”没有对齐。',
        '要解决这个问题，建议将文章拆成“观点层、证据层、动作层”三个可复用模块，方便后续在文案、口播、路演中复用。',
        `对于${topic}这类高波动主题，模块化表达比一次性长篇更稳定，更新成本也显著更低。`
      ]
    },
    {
      title: '时间维度：日内、周度、月度如何分工',
      paragraphs: [
        '同一个结论在不同时间维度里的执行方式并不相同。日内更关注信号是否突变，周度更关注结构是否延续，月度更关注框架是否需要改写。',
        '如果把三个维度混在一起，常见后果是日内信号被当成中期趋势，或者中期拐点被当成日内噪音。时间维度分工，是降低误判成本的第一道闸门。',
        `围绕${topic}，建议固定“日内看波动、周度看验证、月度看再配置”的节奏，这样执行动作不会被短期噪音牵着走。`
      ]
    },
    {
      title: '资金行为：什么时候是交易，什么时候是定价',
      paragraphs: [
        '市场常见的错觉是把所有上涨都当成定价，把所有回撤都当成反转。更稳妥的做法是先判断资金行为属于“情绪交易”还是“结构定价”。',
        '情绪交易往往快进快出，波动高、持续性弱；结构定价往往伴随证据增量与仓位迁移，速度未必最快，但持续性更强。',
        '只有先识别资金行为类型，再匹配策略强度，才能避免“判断没错、仓位错配”的执行损失。'
      ]
    },
    {
      title: '信息质量：如何防止高热内容误导决策',
      paragraphs: [
        '高热信息天然更容易被看到，但不一定更值得相信。对于高热样本，应优先验证来源链、时间链和事实链，再决定是否纳入主结论。',
        '如果一个结论只能在单一平台成立，跨平台无法复核，就应该降低其权重。跨平台一致性越高，结论可执行性通常越强。',
        '信息质量控制不是为了保守，而是为了让每一次动作都建立在可回查证据上。'
      ]
    },
    {
      title: '结语：把方法沉淀成长期优势',
      paragraphs: [
        '真正可持续的竞争力，不是每次都预测正确，而是在不确定环境下持续做出高质量决策。',
        '当文章能稳定输出“可验证结论 + 可执行动作 + 可复盘边界”时，它就不再只是内容产品，而是决策基础设施的一部分。',
        '在高波动阶段，克制和纪律并不保守，恰恰是长期收益最稳定的来源。'
      ]
    }
  ];

  let idx = 0;
  while (countChars(result) < minChars && idx < depthSections.length) {
    const section = depthSections[idx];
    result += `\n\n## ${section.title}\n\n${section.paragraphs.join('\n\n')}`;
    result = enforceSectionParagraphLimit(result, maxParagraphsPerSection);
    idx += 1;
  }

  if (countChars(result) < minChars) {
    const fallbackSections = [
      {
        title: '附录：监测与复盘清单',
        paragraphs: [
          '建议固定跟踪三类信号：事实信号（是否发生）、预期信号（是否定价）、行为信号（是否执行）。三类信号若方向一致，可提高结论置信度；若方向冲突，应优先降低动作强度。',
          '建议固定复盘三类问题：观点是否有证据支撑、动作是否有边界约束、结果是否可复现。复盘不是复述过程，而是输出下一轮可执行优化。',
          '当信号不一致时，优先降仓位而不是强解释；当信号一致时，优先执行纪律而不是追求满仓。这一清单用于保证文章在转写和复用时仍保留完整闭环。'
        ]
      },
      {
        title: '附录：反向验证框架',
        paragraphs: [
          '任何主结论都应有对应的反向验证路径。反向验证不是推翻原观点，而是避免观点在样本变化时失去解释力。',
          `围绕${topic}，建议把“支持信号、反向信号、中性信号”同时记录，并设定权重更新规则，避免情绪性调仓。`,
          '只要反向验证流程稳定运行，文章结论就能持续进化，而不是停留在一次性表达。'
        ]
      },
      {
        title: '附录：转写与分发一致性',
        paragraphs: [
          '长文、文案、口播三种形态共享同一结论骨架，差异只在表达粒度，不在结论方向。',
          '建议先锁定“主结论、证据表、动作清单”三项核心资产，再按渠道重排语序，避免多版本分发导致口径漂移。',
          '转写的目标不是缩写，而是保留论据完整性的前提下提升传播效率。'
        ]
      },
      {
        title: '附录：动作模板与阈值设置',
        paragraphs: [
          '建议把执行动作写成模板：触发阈值、执行比例、观察窗口、退出条件四项缺一不可。没有阈值的动作容易变成情绪决策。',
          '当触发阈值未达到时，动作应以观察为主；当触发阈值连续满足时，动作才进入执行区间。这样可以显著降低“提前交易”带来的回撤。',
          '在复盘里应记录阈值是否合理、动作是否延迟、退出是否及时。连续三轮复盘后，阈值体系会明显稳定。'
        ]
      },
      {
        title: '附录：常见误区与修正路径',
        paragraphs: [
          '误区一是把高互动当成高确定性，修正路径是“先看来源链，再看证据链，最后看动作链”。',
          '误区二是只关注观点正确，不关注仓位匹配，修正路径是“先设风险预算，再谈收益弹性”。',
          '误区三是把一次成功当成长期方法，修正路径是“建立持续复盘与权重更新机制”，确保模型不会在新环境里失效。'
        ]
      },
      {
        title: '附录：编辑与口播协同规范',
        paragraphs: [
          '主文撰写完成后，建议先做“逻辑压缩版”用于口播，再做“情绪强化版”用于短文案，最后回看三版是否保持同一证据口径。',
          '如果三版口径出现冲突，应以主文证据链为准统一回写，避免出现“传播效果好但决策误导”的问题。',
          '协同规范的目标是提升分发效率，同时守住事实底线与执行边界，让内容在不同渠道都能稳定复用。'
        ]
      }
    ];

    let i = 0;
    while (countChars(result) < minChars && i < fallbackSections.length) {
      const section = fallbackSections[i];
      result += `\n\n## ${section.title}\n\n${section.paragraphs.join('\n\n')}`;
      result = enforceSectionParagraphLimit(result, maxParagraphsPerSection);
      i += 1;
    }

    if (countChars(result) < minChars) {
      result += '\n\n## 附录：持续更新说明\n\n本文采用“证据先行、动作后置、复盘闭环”的更新策略。后续若新增数据与当前结论不一致，优先更新证据权重与动作边界，再调整主结论表达，确保内容在高波动环境下仍保持可执行与可复盘。';
      result = enforceSectionParagraphLimit(result, maxParagraphsPerSection);
    }
  }

  let topup = 1;
  while (countChars(result) < minChars && topup <= 3) {
    result += `\n\n## 附录补充验证${topup}\n\n补充验证${topup}用于校验“证据链与动作链是否同步更新”。当新增证据只改变情绪不改变结构时，应维持原动作边界；当新增证据改变结构时，再执行权重重估。\n\n补充验证${topup}同时要求记录三项结果：判断是否偏差、动作是否延迟、边界是否有效。只有把这三项写入复盘，下一轮优化才有可用输入。\n\n该补充段用于保证长文在转写与分发过程中仍保持可执行逻辑，不因表达压缩而丢失方法论。`;
    result = enforceSectionParagraphLimit(result, maxParagraphsPerSection);
    topup += 1;
  }

  return result;
}

function enforceSectionParagraphLimit(content, maxParagraphsPerSection) {
  const sections = splitByH2(content);
  const rebuilt = [];

  for (const section of sections) {
    if (!section.heading) {
      rebuilt.push(section.body.join('\n'));
      continue;
    }

    rebuilt.push(section.heading);

    const blocks = toBlocks(section.body);
    let proseCount = 0;
    const kept = [];

    for (const block of blocks) {
      const trimmed = block.trim();
      if (!trimmed) continue;

      if (isProseParagraph(trimmed)) {
        proseCount += 1;
        if (proseCount > maxParagraphsPerSection) {
          continue;
        }
      }

      kept.push(trimmed);
    }

    if (kept.length) {
      rebuilt.push('');
      rebuilt.push(kept.join('\n\n'));
    }
    rebuilt.push('');
  }

  return rebuilt.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

function splitByH2(content) {
  const lines = String(content || '').split('\n');
  const sections = [];
  let current = { heading: null, body: [] };

  for (const line of lines) {
    if (/^##\s+/.test(line)) {
      sections.push(current);
      current = { heading: line.trim(), body: [] };
      continue;
    }
    current.body.push(line);
  }
  sections.push(current);
  return sections;
}

function toBlocks(lines) {
  const blocks = [];
  let buffer = [];
  for (const line of lines) {
    if (!line.trim()) {
      if (buffer.length) {
        blocks.push(buffer.join('\n'));
        buffer = [];
      }
      continue;
    }
    buffer.push(line);
  }
  if (buffer.length) {
    blocks.push(buffer.join('\n'));
  }
  return blocks;
}

function isProseParagraph(block) {
  return !/^(#|\||[-*]\s|\d+\.\s|>)/.test(block);
}

function checkDraftQuality(content, outline, policy) {
  const charCount = countChars(content);
  const missingSections = policy.required_sections.filter(section => !hasHeading(content, section));
  const tableCount = countMarkdownTables(content);
  const sourceCount = countSources(content);
  const sourceSection = extractSection(content, '数据与素材来源');
  const realSourceCount = countRealSourceUrls(sourceSection);
  const sourcePlaceholdersHit = findSourcePlaceholders(sourceSection);
  const numericPoints = countNumericPoints(content);
  const paragraphOverflowSections = findParagraphOverflowSections(content, policy.max_paragraphs_per_section);
  const bannedTermsHit = findBannedTerms(content, policy.banned_terms);
  const internalDataTermsHit = policy.forbid_intake_internal_data
    ? findBannedTerms(content, policy.internal_data_terms)
    : [];
  const hasDataEvidence = numericPoints >= policy.min_numeric_points;

  const pass =
    charCount >= policy.min_chars &&
    missingSections.length === 0 &&
    tableCount >= policy.required_tables &&
    sourceCount >= policy.required_sources &&
    (!policy.require_real_source_urls || realSourceCount >= policy.required_sources) &&
    (policy.allow_source_placeholders || sourcePlaceholdersHit.length === 0) &&
    (!policy.forbid_intake_internal_data || internalDataTermsHit.length === 0) &&
    hasDataEvidence &&
    paragraphOverflowSections.length === 0 &&
    (!policy.pure_prose_only || bannedTermsHit.length === 0);

  return {
    pass,
    title: outline?.title || '未命名选题',
    char_count: charCount,
    min_chars_required: policy.min_chars,
    missing_sections: missingSections,
    table_count: tableCount,
    required_tables: policy.required_tables,
    source_count: sourceCount,
    real_source_url_count: realSourceCount,
    required_sources: policy.required_sources,
    require_real_source_urls: policy.require_real_source_urls,
    source_placeholders_hit: sourcePlaceholdersHit,
    allow_source_placeholders: policy.allow_source_placeholders,
    forbid_intake_internal_data: policy.forbid_intake_internal_data,
    internal_data_terms_hit: internalDataTermsHit,
    numeric_points: numericPoints,
    min_numeric_points_required: policy.min_numeric_points,
    paragraph_overflow_sections: paragraphOverflowSections,
    max_paragraphs_per_section: policy.max_paragraphs_per_section,
    banned_terms_hit: bannedTermsHit,
    pure_prose_only: policy.pure_prose_only,
    rewrite_model_mode: policy.rewrite_model_mode,
    article_style_mode: policy.article_style_mode,
    disable_style_dna: policy.disable_style_dna,
    external_data_channels: policy.external_data_channels,
    has_data_evidence: hasDataEvidence
  };
}

function buildQualityReport(drafts, policy) {
  const checks = drafts.map(d => d.compliance.checks);
  const passCount = checks.filter(item => item.pass).length;
  const failCount = checks.length - passCount;
  return {
    standard_version: policy.standard_version,
    generated_at: nowIso(),
    total_drafts: checks.length,
    pass_count: passCount,
    fail_count: failCount,
    rewrite_model_mode: policy.rewrite_model_mode,
    checks
  };
}

function getUsedSections(content) {
  const matched = content.match(/^##\s+(.+)$/gm) || [];
  return matched.map(line => line.replace(/^##\s+/, '').trim());
}

function hasHeading(content, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`^##\\s+${escaped}\\s*$`, 'm');
  return regex.test(content);
}

function countChars(text) {
  return (text || '').replace(/\s+/g, '').length;
}

function countMarkdownTables(content) {
  const regex = /\|[^\n]+\|\n\|[-:|\s]+\|/g;
  const matches = content.match(regex);
  return matches ? matches.length : 0;
}

function countSources(content) {
  const section = extractSection(content, '数据与素材来源');
  if (!section) return 0;
  const lines = section.split('\n').map(line => line.trim()).filter(Boolean);
  return lines.filter(line => /^([-*]\s+|\d+\.\s+)/.test(line) || /https?:\/\//.test(line)).length;
}

function countRealSourceUrls(sourceSection) {
  if (!sourceSection) return 0;
  const urls = sourceSection.match(/https?:\/\/[^\s)）]+/g) || [];
  const valid = urls.filter(url => !isPlaceholderSource(url));
  return new Set(valid.map(normalizeUrl)).size;
}

function findSourcePlaceholders(sourceSection) {
  if (!sourceSection) return [];
  const hits = [];
  const lines = sourceSection.split('\n').map(line => line.trim()).filter(Boolean);
  for (const line of lines) {
    if (/待补充|placeholder|source-pending/i.test(line)) {
      hits.push(line);
      continue;
    }
    const urls = line.match(/https?:\/\/[^\s)）]+/g) || [];
    if (urls.some(url => isPlaceholderSource(url))) {
      hits.push(line);
    }
  }
  return hits;
}

function isPlaceholderSource(url) {
  const lower = String(url || '').toLowerCase();
  return lower.includes('example.com') || lower.includes('source-pending') || lower.includes('placeholder');
}

function countNumericPoints(content) {
  const matches = String(content || '').match(/\d+(?:\.\d+)?%?/g);
  return matches ? matches.length : 0;
}

function findBannedTerms(content, bannedTerms) {
  const lower = String(content || '').toLowerCase();
  return (bannedTerms || []).filter(term => lower.includes(String(term).toLowerCase()));
}

function findParagraphOverflowSections(content, maxParagraphsPerSection) {
  const sections = splitByH2(content);
  const overflow = [];

  for (const section of sections) {
    if (!section.heading) continue;
    const blocks = toBlocks(section.body);
    const proseCount = blocks.filter(block => isProseParagraph(block.trim())).length;
    if (proseCount > maxParagraphsPerSection) {
      overflow.push({
        section: section.heading.replace(/^##\s+/, ''),
        prose_paragraphs: proseCount
      });
    }
  }

  return overflow;
}

function extractSection(content, heading) {
  const lines = String(content || '').split('\n');
  const target = `## ${heading}`;

  let start = -1;
  for (let i = 0; i < lines.length; i += 1) {
    if (lines[i].trim() === target) {
      start = i + 1;
      break;
    }
  }

  if (start === -1) {
    return '';
  }

  let end = lines.length;
  for (let i = start; i < lines.length; i += 1) {
    if (/^##\s+/.test(lines[i])) {
      end = i;
      break;
    }
  }

  return lines.slice(start, end).join('\n');
}

if (require.main === module) {
  const outlinePlansFile = process.argv[2];
  generateDraft(outlinePlansFile)
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

module.exports = {
  generateDraft,
  buildDraftPackage,
  generateDraftContent,
  checkDraftQuality
};

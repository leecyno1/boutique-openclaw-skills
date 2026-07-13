const { spawnSync } = require('child_process');
const path = require('path');

const ROOT = path.join(__dirname, '../..');
const SCRIPT = path.join(ROOT, 'scripts/build_stage3_draft.py');

/**
 * 执行 Draft Stage (Stage 3) - 初稿生成
 *
 * @param {string} selectedTopicsFile - selected_topics.json 文件路径
 * @param {Object} options - 可选参数
 * @param {string} options.runId - 运行ID (格式: YYYY-MM-DD_HHMMSS)
 * @param {string} options.topicCardsFile - topic_cards.json 文件路径
 * @param {string} options.outputDir - 输出目录
 * @param {string} options.assetSpecsFile - Draft 内图表/配图规格文件
 * @param {string} options.chartjsFile - 本地 Chart.js v4.4.4 UMD 文件
 * @returns {Object} 执行结果
 */
function runDraft(selectedTopicsFile, options = {}) {
  const args = [SCRIPT, selectedTopicsFile];

  if (options.topicCardsFile) {
    args.push(options.topicCardsFile);
  }

  if (options.runId) {
    args.push('--run-id', options.runId);
  }

  if (options.outputDir) {
    args.push('--output-dir', options.outputDir);
  }

  if (options.assetSpecsFile) {
    args.push('--asset-specs-file', options.assetSpecsFile);
  }

  if (options.chartjsFile) {
    args.push('--chartjs-file', options.chartjsFile);
  }

  const result = spawnSync('python3', args, {
    cwd: ROOT,
    encoding: 'utf8',
    timeout: 300000, // 5分钟超时
    maxBuffer: 10 * 1024 * 1024, // 10MB buffer
  });

  if (result.error) {
    throw new Error(`Failed to spawn process: ${result.error.message}`);
  }

  if (result.status !== 0) {
    throw new Error(`Draft generation failed with exit code ${result.status}:\n${result.stderr}`);
  }

  try {
    const output = JSON.parse(result.stdout);
    return output;
  } catch (err) {
    throw new Error(`Failed to parse JSON output: ${err.message}\nStdout: ${result.stdout}`);
  }
}

module.exports = { runDraft };

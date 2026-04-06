// --- Tab switching ---
function switchMainTab(tabName) {
  document.querySelectorAll('.tab').forEach((b) => {
    b.classList.toggle('active', b.dataset.tab === tabName);
  });
  document.querySelectorAll('.tab-content').forEach((s) => {
    s.classList.toggle('active', s.id === `tab-${tabName}`);
  });
}

document.querySelectorAll('.tab').forEach((btn) => {
  btn.addEventListener('click', () => switchMainTab(btn.dataset.tab));
});

// --- 制作ウィザード (1 本の動画向け導線) ---
const WIZARD_HINTS = {
  1: '台本 .txt を選び、Speaker Map / Reflow v2 を確認して Build CSV します。出力 CSV は手順 4 で row-range 用に自動で参照できます。',
  2: 'Dry Run で行数・話者を確認し、問題なければ Build CSV で書き出します。',
  3: 'Production .ymmp と IR JSON（または貼り付け保存）を選び、Palette があれば Validate IR を実行します。',
  4: 'CSV(row-range) に手順 1 の出力が入っているか確認し、Dry Run → Apply Production の順が安全です。',
  5: '「出力フォルダを開く」で ymmp / csv を確認します。S-5 の取込前後を 1 本にまとめる記録は docs/workflow-proof-template.md（B-11）。外部 LLM 用テキストは CSV タブのパケット（bundle）から出力できます。パッケージ点数は「品質診断」タブです。',
};

let currentWizardStep = 1;

function setWizardStep(step, { persist = true } = {}) {
  currentWizardStep = Math.min(5, Math.max(1, step));
  document.querySelectorAll('.wizard-step').forEach((el) => {
    const s = parseInt(el.dataset.wizardStep, 10);
    el.classList.toggle('active', s === currentWizardStep);
    el.classList.toggle('done', s < currentWizardStep);
  });
  const hintEl = document.getElementById('wizard-hint');
  if (hintEl) {
    hintEl.textContent = WIZARD_HINTS[currentWizardStep] || '';
  }
  const stepBtn = document.querySelector(`.wizard-step[data-wizard-step="${currentWizardStep}"]`);
  if (stepBtn && stepBtn.dataset.tab) {
    switchMainTab(stepBtn.dataset.tab);
  }
  document.getElementById('btn-wizard-prev').disabled = currentWizardStep <= 1;
  document.getElementById('btn-wizard-next').disabled = currentWizardStep >= 5;
  const scoringBtn = document.getElementById('btn-wizard-scoring');
  if (scoringBtn) {
    scoringBtn.classList.toggle('hidden', currentWizardStep !== 5);
  }
  if (persist) {
    autoSave();
  }
}

document.querySelectorAll('.wizard-step').forEach((btn) => {
  btn.addEventListener('click', () => {
    const step = parseInt(btn.dataset.wizardStep, 10);
    if (!Number.isNaN(step)) {
      setWizardStep(step);
    }
  });
});

document.getElementById('btn-wizard-prev').addEventListener('click', () => {
  setWizardStep(currentWizardStep - 1);
});

document.getElementById('btn-wizard-next').addEventListener('click', () => {
  setWizardStep(currentWizardStep + 1);
});

// --- 失敗時: failure class → エラーカード + ドキュメント ---
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/** ログに出る failure class → 対応ヒント (キーはプレフィックスと一致) */
const FAILURE_HELP = {
  FACE_PROMPT_PALETTE_GAP: {
    title: 'プロンプトの face と palette のラベルが一致しない',
    action: 'Writer IR / Custom GPT の face 許可リストと palette 抽出結果を突き合わせ、IR か palette のどちらを直すか決めてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  FACE_PROMPT_PALETTE_EXTRA: {
    title: 'palette にある face がプロンプト契約に含まれない',
    action: 'プロンプトを広げるか、palette の余分なラベルを整理するか判断してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  FACE_UNKNOWN_LABEL: {
    title: 'IR の face ラベルが palette / face_map で解決できない',
    action: 'palette に該当表情を追加するか、IR のラベルを既存の意味ラベルに合わせて修正してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（face）',
  },
  FACE_ACTIVE_GAP: {
    title: 'アクティブな発話で使う face が palette に無い',
    action: 'palette を更新するか、IR の face / idle_face を実在ラベルに差し替えてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（face）',
  },
  FACE_LATENT_GAP: {
    title: '潜在 face 参照と palette の整合が取れない',
    action: 'プロンプトと palette のラベル一覧を再突合し、不要な潜在指定を削るかラベルを足してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  PROMPT_FACE_DRIFT: {
    title: 'プロンプト契約と IR の face 利用がずれている',
    action: 'IR 生成プロンプト（S6 系）と実際の IR を比較し、どちらを正とするか決めて修正してください。',
    doc: 'docs/S6-production-memo-prompt.md',
    docLabel: 'S6-production-memo-prompt',
  },
  FACE_SERIOUS_SKEW: {
    title: '表情ラベルの偏りが大きい（品質ゲート）',
    action: '演出意図として許容するか、IR を手直ししてバランスを取るか判断してください。',
    doc: 'docs/PRODUCTION_IR_SPEC.md',
    docLabel: 'PRODUCTION_IR_SPEC',
  },
  IDLE_FACE_MISSING: {
    title: 'idle_face がどの発話にも無い',
    action: 'IR に idle_face を追加するか、仕様上不要なら validate 条件を確認してください。',
    doc: 'docs/PRODUCTION_IR_SPEC.md',
    docLabel: 'PRODUCTION_IR_SPEC',
  },
  ROW_RANGE_MISSING: {
    title: 'row_start / row_end が欠けている',
    action: 'IR に row 範囲を付与するか、CSV との対応付け（annotate）をやり直してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（row-range）',
  },
  ROW_RANGE_INVALID: {
    title: 'row 範囲の値が不正',
    action: 'CSV 行番号と IR の対応を見直し、範囲の重複・逆転を解消してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  ROW_RANGE_OVERLAP: {
    title: 'row 範囲が重複している',
    action: '発話ブロックごとの row 割当を整理し、1 行が複数発話に被らないようにしてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  ROW_RANGE_INFO: {
    title: 'row 範囲メタデータの注意',
    action: 'row_start/row_end を IR に付けるか、CSV annotate 運用に合わせて整備してください。',
    doc: 'docs/PIPELINE_SPEC.md',
    docLabel: 'PIPELINE_SPEC',
  },
  SLOT_UNKNOWN_LABEL: {
    title: 'IR の slot ラベルがレジストリに無い',
    action: 'slot_map / registry にラベルを追加するか、IR を既存ラベルに合わせてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（slot）',
  },
  SLOT_REGISTRY_GAP: {
    title: 'slot レジストリと IR の要求が合わない',
    action: 'registry JSON を拡張するか、IR の slot 指定を実在エントリに合わせてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  SLOT_REGISTRY_MISS: {
    title: 'patch 時に slot レジストリが解決できない',
    action: 'slot_map のパスと ymmp の TachieItem 構成を確認し、ラベルとキャラ既定 slot を直してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  SLOT_CHARACTER_DRIFT: {
    title: 'キャラと slot の対応がずれている',
    action: 'YMM4 上のキャラ名・既定位置と IR / slot_map のキャラキーを一致させてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  SLOT_DEFAULT_DRIFT: {
    title: '既定 slot と実タイムラインが一致しない',
    action: 'registry の default_slot を YMM4 実機に合わせて更新してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  SLOT_VALUE_INVALID: {
    title: 'slot の値（座標等）が不正',
    action: 'slot_map 内の数値・キーを仕様に沿って修正してください。',
    doc: 'docs/PRODUCTION_IR_SPEC.md',
    docLabel: 'PRODUCTION_IR_SPEC',
  },
  SLOT_NO_TACHIE_ITEM: {
    title: 'ymmp に立ち絵アイテムが見つからない',
    action: '対象キャラの TachieItem があるテンプレ ymmp か確認し、production ymmp を差し替えてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  FACE_MAP_MISS: {
    title: 'face_map が表情パラメータを解決できない',
    action: 'palette から face_map を再生成するか、ラベルとパーツ番号の対応を手で直してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（face）',
  },
  IDLE_FACE_MAP_MISS: {
    title: 'idle_face が face_map で解決できない',
    action: 'idle 用ラベルを palette / face_map に追加するか、IR の idle_face を修正してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  VOICE_NO_TACHIE_FACE: {
    title: 'VoiceItem に立ち絵表情パラメータが無い',
    action: 'YMM4 で該当発話に表情パラメータが付く状態で書き出し直すか、別テンプレを使ってください（機械的欠陥）。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  OVERLAY_MAP_MISS: {
    title: 'overlay ラベルが map で解決できない',
    action: 'overlay_map にエントリを追加するか、IR のラベルを既存キーに合わせてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（overlay）',
  },
  OVERLAY_NO_TIMING_ANCHOR: {
    title: 'overlay のタイミングアンカーが無い',
    action: 'IR 側のアンカー発話・時刻指定を補うか、map の anchor 定義を見直してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  OVERLAY_SPEC_INVALID: {
    title: 'overlay 仕様が不正',
    action: 'PRODUCTION_IR_SPEC に沿って overlay フィールドを修正してください。',
    doc: 'docs/PRODUCTION_IR_SPEC.md',
    docLabel: 'PRODUCTION_IR_SPEC',
  },
  SE_MAP_MISS: {
    title: 'SE ラベルが map で解決できない',
    action: 'se_map にエントリを追加するか、IR の SE ラベルを修正してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（se）',
  },
  SE_NO_TIMING_ANCHOR: {
    title: 'SE のタイミングアンカーが無い',
    action: 'IR のアンカー指定を補完するか、map 定義を修正してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  SE_SPEC_INVALID: {
    title: 'SE 仕様が不正',
    action: 'PRODUCTION_IR_SPEC に沿って SE フィールドを修正してください。',
    doc: 'docs/PRODUCTION_IR_SPEC.md',
    docLabel: 'PRODUCTION_IR_SPEC',
  },
  SE_WRITE_ROUTE_UNSUPPORTED: {
    title: 'この ymmp では SE 書き込み経路が未測定／未対応',
    action: '別サンプル ymmp で write route を測るか、当面 SE を手動配置に留める設計判断が必要です。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（timeline）',
  },
  TIMELINE_ROUTE_MISS: {
    title: '期待するタイムライン経路が ymmp に存在しない',
    action: 'テンプレ差し替え・measure-timeline-routes の corpus 更新など、テンプレ依存の機械的解決を検討してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW（timeline）',
  },
  TIMELINE_ROUTE_CONTRACT_INVALID: {
    title: 'timeline route 契約 JSON が不正',
    action: 'samples 配下の contract / profile を仕様通りに直してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  TIMELINE_ROUTE_PROFILE_UNKNOWN: {
    title: 'timeline route の profile 名が不明',
    action: '契約に登録された profile のみを参照するよう修正してください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  TIMELINE_ROUTE_CATEGORY_EMPTY: {
    title: 'timeline route カテゴリが空',
    action: '測定コーパスを追加するか、期待カテゴリを現実の ymmp に合わせて下げてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
  TIMELINE_ROUTE_OPTIONAL_MISS: {
    title: '任意 route が見つからない',
    action: 'optional なので制作上必須か判断し、必須ならテンプレ側を揃えてください。',
    doc: 'docs/OPERATOR_WORKFLOW.md',
    docLabel: 'OPERATOR_WORKFLOW',
  },
};

function blobContainsFailureCode(blob, code) {
  return blob.includes(`${code}:`) || blob.includes(` ${code} `) || blob.startsWith(`${code} `);
}

function extractFailureCodes(blob) {
  if (!blob || typeof blob !== 'string') return [];
  const keys = Object.keys(FAILURE_HELP).sort((a, b) => b.length - a.length);
  const out = [];
  for (const code of keys) {
    if (blobContainsFailureCode(blob, code)) out.push(code);
  }
  return out;
}

function renderFailurePanel(panel, rawText, { genericDoc } = {}) {
  panel.classList.remove('hidden', 'success');
  panel.classList.add('error');
  const codes = extractFailureCodes(rawText);
  const parts = [];
  for (const code of codes) {
    const h = FAILURE_HELP[code];
    if (!h) continue;
    parts.push(
      `<div class="failure-card">`
      + `<div class="failure-card-title">${escapeHtml(code)}</div>`
      + `<p class="failure-card-action">${escapeHtml(h.title)}<br>${escapeHtml(h.action)}</p>`
      + `<button type="button" class="failure-doc-link" data-doc="${escapeHtml(h.doc)}">`
      + `${escapeHtml(h.docLabel)} を開く</button>`
      + `</div>`,
    );
  }
  if (parts.length === 0) {
    const gd = genericDoc || 'docs/OPERATOR_WORKFLOW.md';
    parts.push(
      '<div class="failure-card failure-card-generic">'
      + '<div class="failure-card-title">ログを確認してください</div>'
      + '<p class="failure-card-action">該当する failure class が特定できませんでした。下の全文から原因を追い、必要なら次のドキュメントを開いてください。</p>'
      + `<button type="button" class="failure-doc-link" data-doc="${escapeHtml(gd)}">`
      + '関連ドキュメントを開く</button>'
      + '</div>',
    );
  }
  panel.innerHTML = parts.join('') + `<pre class="failure-log">${escapeHtml(rawText)}</pre>`;
}

function renderSuccessTextPanel(panel, text) {
  panel.classList.remove('hidden', 'error');
  panel.classList.add('success');
  panel.innerHTML = '';
  panel.textContent = text;
}

document.addEventListener('click', (e) => {
  const btn = e.target.closest('.failure-doc-link');
  if (!btn || !btn.dataset.doc) return;
  e.preventDefault();
  window.nlmytgen.openRepoDoc(btn.dataset.doc).then((res) => {
    if (!res.ok && res.message) {
      document.getElementById('status').textContent = `ドキュメントを開けません: ${res.message}`;
    }
  });
});

// --- CSV Tab ---
const dropZone = document.getElementById('drop-zone');
const selectedFile = document.getElementById('selected-file');
const btnBuild = document.getElementById('btn-build-csv');
const btnDryRun = document.getElementById('btn-dry-run');
const btnOpenOutput = document.getElementById('btn-open-output');
const csvResult = document.getElementById('csv-result');
let currentTxtPath = null;
let lastOutputPath = null;
let packetBundleDir = null;

function updatePacketButtons() {
  const cue = document.getElementById('btn-build-cue-bundle');
  const dia = document.getElementById('btn-build-diagram-bundle');
  const ready = !!(currentTxtPath && packetBundleDir);
  if (cue) cue.disabled = !ready;
  if (dia) dia.disabled = !ready;
}

function setTxtFile(filePath, { save = true } = {}) {
  currentTxtPath = filePath;
  selectedFile.textContent = filePath;
  btnBuild.disabled = false;
  updatePacketButtons();
  if (save) {
    autoSave();
  }
}

// Drag & Drop
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover');
});
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    setTxtFile(files[0].path);
  }
});

// File select button
document.getElementById('btn-select-txt').addEventListener('click', async () => {
  const path = await window.nlmytgen.selectFile({
    title: '台本テキストを選択',
    filters: [
      { name: 'Text', extensions: ['txt'] },
      { name: 'All', extensions: ['*'] },
    ],
  });
  if (path) setTxtFile(path);
});

async function runBuildCsv(dryRun) {
  if (!currentTxtPath) return;

  const status = document.getElementById('status');
  status.textContent = 'Building CSV...';
  btnBuild.disabled = true;
  btnOpenOutput.classList.add('hidden');

  const opts = {
    input: currentTxtPath,
    speakerMap: document.getElementById('speaker-map').value || undefined,
    maxLines: parseInt(document.getElementById('max-lines').value) || undefined,
    charsPerLine: parseInt(document.getElementById('chars-per-line').value) || undefined,
    reflowV2: document.getElementById('reflow-v2').checked,
    dryRun,
  };

  try {
    const result = await window.nlmytgen.buildCsv(opts);
    csvResult.classList.remove('hidden', 'success', 'error');

    if (result.json && result.json.success) {
      let text = `Rows: ${result.json.rows}\n`;
      if (result.json.speakers) {
        text += `Speakers:\n`;
        for (const [sp, count] of Object.entries(result.json.speakers)) {
          text += `  ${sp}: ${count}\n`;
        }
      }
      if (result.json.output) {
        text += `\nOutput: ${result.json.output}`;
        lastOutputPath = result.json.output;
        btnOpenOutput.classList.remove('hidden');
        filePaths['csv-file'] = result.json.output;
        document.getElementById('csv-file-path').textContent = result.json.output;
        updateApplyButton();
        autoSave();
      }
      if (result.json.dry_run) {
        text += `\n(dry-run: CSV not written)`;
      }
      renderSuccessTextPanel(csvResult, text);
      status.textContent = dryRun ? 'Dry run complete' : `CSV written (${result.json.rows} rows)`;
      if (result.json.dry_run) {
        setWizardStep(2, { persist: true });
      } else if (result.json.output) {
        setWizardStep(3, { persist: true });
      }
    } else {
      let errMsg = '';
      if (result.stderr) errMsg += result.stderr + '\n';
      if (result.stdout) errMsg += '[stdout] ' + result.stdout + '\n';
      errMsg += `[exit code] ${result.code}`;
      renderFailurePanel(csvResult, errMsg || 'Unknown error', { genericDoc: 'docs/PIPELINE_SPEC.md' });
      status.textContent = 'Build failed';
    }
  } catch (err) {
    csvResult.classList.remove('hidden');
    renderFailurePanel(csvResult, err.message, { genericDoc: 'docs/PIPELINE_SPEC.md' });
    status.textContent = 'Error';
  }

  btnBuild.disabled = false;
}

btnBuild.addEventListener('click', () => runBuildCsv(false));
btnDryRun.addEventListener('click', () => runBuildCsv(true));
btnOpenOutput.addEventListener('click', () => {
  if (lastOutputPath) window.nlmytgen.openFolder(lastOutputPath);
});

document.getElementById('btn-select-packet-dir').addEventListener('click', async () => {
  const dir = await window.nlmytgen.selectFolder();
  if (!dir) return;
  packetBundleDir = dir;
  const el = document.getElementById('packet-dir-path');
  if (el) el.textContent = dir;
  updatePacketButtons();
  autoSave();
});

async function runPacketBundle(kind) {
  if (!currentTxtPath || !packetBundleDir) return;
  const panel = document.getElementById('packet-result');
  const status = document.getElementById('status');
  status.textContent = kind === 'cue' ? 'Cue パケット生成中...' : 'Diagram パケット生成中...';
  const opts = {
    input: currentTxtPath,
    bundleDir: packetBundleDir,
    speakerMap: document.getElementById('speaker-map').value || undefined,
  };
  try {
    const result = kind === 'cue'
      ? await window.nlmytgen.buildCuePacketBundle(opts)
      : await window.nlmytgen.buildDiagramPacketBundle(opts);
    panel.classList.remove('hidden', 'success', 'error');
    if (result.code === 0) {
      const out = (result.stdout || '').trim() || '完了';
      renderSuccessTextPanel(panel, out);
      status.textContent = 'パケット出力完了';
    } else {
      const raw = [result.stderr, result.stdout].filter(Boolean).join('\n') || '失敗';
      renderFailurePanel(panel, raw, { genericDoc: 'docs/ADR/0004-llm-text-assist-boundary.md' });
      status.textContent = 'パケット出力失敗';
    }
  } catch (err) {
    panel.classList.remove('hidden');
    renderFailurePanel(panel, err.message, { genericDoc: 'docs/ADR/0004-llm-text-assist-boundary.md' });
    status.textContent = 'Error';
  }
}

document.getElementById('btn-build-cue-bundle').addEventListener('click', () => runPacketBundle('cue'));
document.getElementById('btn-build-diagram-bundle').addEventListener('click', () => runPacketBundle('diagram'));

// --- Production Tab ---
const filePaths = {
  'prod-ymmp': null,
  'ir-json': null,
  'palette': null,
  'csv-file': null,
  'bg-map': null,
};

const fileFilters = {
  'prod-ymmp': [{ name: 'YMM4 Project', extensions: ['ymmp'] }],
  'ir-json': [{ name: 'JSON', extensions: ['json'] }],
  'palette': [{ name: 'YMM4 Project', extensions: ['ymmp'] }],
  'csv-file': [{ name: 'CSV', extensions: ['csv'] }],
  'bg-map': [{ name: 'JSON', extensions: ['json'] }],
};

let lastPatchedPath = null;

document.querySelectorAll('.btn-file').forEach(btn => {
  btn.addEventListener('click', async () => {
    const target = btn.dataset.target;
    const path = await window.nlmytgen.selectFile({
      title: `Select ${target}`,
      filters: fileFilters[target] || [{ name: 'All', extensions: ['*'] }],
    });
    if (path) {
      filePaths[target] = path;
      document.getElementById(`${target}-path`).textContent = path;
      updateApplyButton();
      autoSave();
    }
  });
});

function updateApplyButton() {
  const hasIr = filePaths['ir-json'];
  const hasYmmp = filePaths['prod-ymmp'];
  document.getElementById('btn-apply').disabled = !(hasIr && hasYmmp);
  document.getElementById('btn-validate-ir').disabled = !hasIr;
}

// --- IR paste ---
document.getElementById('btn-save-ir').addEventListener('click', async () => {
  const content = document.getElementById('ir-paste').value.trim();
  if (!content) return;

  const saved = await window.nlmytgen.saveIrPaste({ content, defaultPath: 'ir.json' });
  if (saved) {
    filePaths['ir-json'] = saved;
    document.getElementById('ir-json-path').textContent = saved;
    document.getElementById('ir-paste').value = '';
    document.getElementById('status').textContent = `IR saved: ${saved}`;
    updateApplyButton();
    autoSave();
  }
});

// --- Validate IR ---
document.getElementById('btn-validate-ir').addEventListener('click', async () => {
  if (!filePaths['ir-json']) return;

  const status = document.getElementById('status');
  status.textContent = 'Validating IR...';

  const opts = {
    irJson: filePaths['ir-json'],
    palette: filePaths['palette'] || undefined,
  };

  const validatePanel = document.getElementById('validate-result');

  try {
    const result = await window.nlmytgen.validateIr(opts);
    validatePanel.classList.remove('hidden');

    if (result.json && result.json.command === 'validate-ir') {
      const j = result.json;
      let text = `検証: ${j.success ? '成功' : '失敗'}\n`;
      text += `発話数: ${j.utterance_count} / エラー: ${j.error_count} / 警告: ${j.warning_count}\n`;
      if (j.face_distribution_top && j.face_distribution_top.length) {
        text += '\nFace 分布（上位）:\n';
        j.face_distribution_top.forEach((x) => { text += `  ${x.label}: ${x.count}\n`; });
      }
      if (j.preview_errors && j.preview_errors.length) {
        text += '\nエラー（先頭）:\n';
        j.preview_errors.forEach((e) => { text += `  ${e}\n`; });
      }
      if (j.preview_warnings && j.preview_warnings.length) {
        text += '\n警告（先頭）:\n';
        j.preview_warnings.forEach((w) => { text += `  ${w}\n`; });
      }
      if (result.stderr) text += `\n--- メタ情報 ---\n${result.stderr}`;
      if (j.success && result.code === 0) {
        renderSuccessTextPanel(validatePanel, text);
        status.textContent = 'Validation passed';
        if (currentWizardStep === 3) {
          setWizardStep(4, { persist: true });
        }
      } else {
        renderFailurePanel(validatePanel, text || 'Validation failed', { genericDoc: 'docs/PRODUCTION_IR_SPEC.md' });
        status.textContent = 'Validation failed';
      }
    } else if (result.code === 0) {
      renderSuccessTextPanel(validatePanel, result.stdout || 'Validation passed');
      status.textContent = 'Validation passed';
      if (currentWizardStep === 3) {
        setWizardStep(4, { persist: true });
      }
    } else {
      let text = '';
      if (result.stderr) text += result.stderr + '\n';
      if (result.stdout) text += result.stdout;
      renderFailurePanel(validatePanel, text || 'Validation failed');
      status.textContent = 'Validation failed';
    }
  } catch (err) {
    validatePanel.classList.remove('hidden');
    renderFailurePanel(validatePanel, err.message);
  }
});

// --- Apply Production ---
async function runApplyProduction(dryRun) {
  if (!filePaths['prod-ymmp'] || !filePaths['ir-json']) return;

  const status = document.getElementById('status');
  status.textContent = 'Applying production...';
  const btnOpenPatched = document.getElementById('btn-open-patched');
  btnOpenPatched.classList.add('hidden');

  const opts = {
    ymmp: filePaths['prod-ymmp'],
    irJson: filePaths['ir-json'],
    palette: filePaths['palette'] || undefined,
    csv: filePaths['csv-file'] || undefined,
    bgMap: filePaths['bg-map'] || undefined,
    dryRun,
  };

  const resultPanel = document.getElementById('production-result');

  try {
    const result = await window.nlmytgen.applyProduction(opts);
    resultPanel.classList.remove('hidden');

    if (result.json && result.json.success) {
      let text = '';
      if (result.json.summary) {
        const s = result.json.summary;
        text += `[要約] 警告 ${s.warning_count} 件 / face ${s.face_changes} / slot ${s.slot_changes} / BG −${s.bg_removed} +${s.bg_added}\n\n`;
      }
      text += `Face changes: ${result.json.face_changes}\n`;
      text += `Slot changes: ${result.json.slot_changes}\n`;
      text += `BG: removed ${result.json.bg_changes}, added ${result.json.bg_additions}\n`;
      if (result.json.tachie_syncs) {
        text += `Idle face inserts: ${result.json.tachie_syncs}\n`;
      }
      if (result.json.warnings && result.json.warnings.length) {
        text += `\nWarnings:\n`;
        result.json.warnings.forEach(w => { text += `  ${w}\n`; });
      }
      if (result.json.output) {
        text += `\nOutput: ${result.json.output}`;
        lastPatchedPath = result.json.output;
        btnOpenPatched.classList.remove('hidden');
      }
      if (result.json.dry_run) {
        text += `\n(dry-run: no file written)`;
      }
      renderSuccessTextPanel(resultPanel, text);
      status.textContent = dryRun ? 'Dry run complete' : 'Production applied';
      if (!dryRun && result.json.output) {
        setWizardStep(5, { persist: true });
      }
    } else {
      let errText = '';
      if (result.json && result.json.summary) {
        const s = result.json.summary;
        errText += `[要約] 警告 ${s.warning_count} 件 / 致命的警告 ${s.fatal_warning_count} 件\n\n`;
      }
      if (result.json && result.json.error) {
        errText += `Error: ${result.json.error}\n`;
      }
      if (result.json && result.json.fatal_warnings) {
        result.json.fatal_warnings.forEach(w => { errText += `${w}\n`; });
      }
      if (result.stderr) errText += result.stderr + '\n';
      if (result.stdout) errText += '[stdout] ' + result.stdout + '\n';
      errText += `[exit code] ${result.code}`;
      renderFailurePanel(resultPanel, errText);
      status.textContent = 'Apply failed';
    }
  } catch (err) {
    resultPanel.classList.remove('hidden');
    renderFailurePanel(resultPanel, err.message);
    status.textContent = 'Error';
  }
}

document.getElementById('btn-apply').addEventListener('click', () => runApplyProduction(false));
document.getElementById('btn-apply-dry').addEventListener('click', () => runApplyProduction(true));
document.getElementById('btn-open-patched').addEventListener('click', () => {
  if (lastPatchedPath) window.nlmytgen.openFolder(lastPatchedPath);
});

// --- Settings persistence ---

function collectSettings() {
  return {
    wizard: {
      currentStep: currentWizardStep,
    },
    script: {
      lastTxt: currentTxtPath,
    },
    csv: {
      speakerMap: document.getElementById('speaker-map').value,
      maxLines: parseInt(document.getElementById('max-lines').value) || 2,
      charsPerLine: parseInt(document.getElementById('chars-per-line').value) || 40,
      reflowV2: document.getElementById('reflow-v2').checked,
    },
    production: {
      prodYmmp: filePaths['prod-ymmp'] || null,
      irJson: filePaths['ir-json'] || null,
      palette: filePaths['palette'] || null,
      bgMap: filePaths['bg-map'] || null,
      csvFile: filePaths['csv-file'] || null,
    },
    packetAssist: {
      bundleDir: packetBundleDir || null,
    },
  };
}

function applySettings(settings) {
  if (!settings) return;
  if (settings.wizard && typeof settings.wizard.currentStep === 'number') {
    const s = settings.wizard.currentStep;
    if (s >= 1 && s <= 5) {
      currentWizardStep = s;
    }
  }
  if (settings.script && settings.script.lastTxt) {
    setTxtFile(settings.script.lastTxt, { save: false });
  }
  if (settings.csv) {
    if (settings.csv.speakerMap) document.getElementById('speaker-map').value = settings.csv.speakerMap;
    if (settings.csv.maxLines) document.getElementById('max-lines').value = settings.csv.maxLines;
    if (settings.csv.charsPerLine) document.getElementById('chars-per-line').value = settings.csv.charsPerLine;
    if (settings.csv.reflowV2 !== undefined) document.getElementById('reflow-v2').checked = settings.csv.reflowV2;
  }
  if (settings.production) {
    if (settings.production.prodYmmp) {
      filePaths['prod-ymmp'] = settings.production.prodYmmp;
      document.getElementById('prod-ymmp-path').textContent = settings.production.prodYmmp;
    }
    if (settings.production.irJson) {
      filePaths['ir-json'] = settings.production.irJson;
      document.getElementById('ir-json-path').textContent = settings.production.irJson;
    }
    if (settings.production.palette) {
      filePaths['palette'] = settings.production.palette;
      document.getElementById('palette-path').textContent = settings.production.palette;
    }
    if (settings.production.bgMap) {
      filePaths['bg-map'] = settings.production.bgMap;
      document.getElementById('bg-map-path').textContent = settings.production.bgMap;
    }
    if (settings.production.csvFile) {
      filePaths['csv-file'] = settings.production.csvFile;
      document.getElementById('csv-file-path').textContent = settings.production.csvFile;
    }
  }
  if (settings.packetAssist && settings.packetAssist.bundleDir) {
    packetBundleDir = settings.packetAssist.bundleDir;
    const pd = document.getElementById('packet-dir-path');
    if (pd) pd.textContent = packetBundleDir;
  }
  updateApplyButton();
  updatePacketButtons();
}

function autoSave() {
  window.nlmytgen.saveSettings(collectSettings());
}

document.getElementById('speaker-map').addEventListener('change', autoSave);
document.getElementById('max-lines').addEventListener('change', autoSave);
document.getElementById('chars-per-line').addEventListener('change', autoSave);
document.getElementById('reflow-v2').addEventListener('change', autoSave);

// --- Scoring Tab（DOMContentLoaded 内の H-01 テンプレ保存から参照するため先に宣言）---
let scoringBriefPath = null;

// Load on startup
window.addEventListener('DOMContentLoaded', async () => {
  const settings = await window.nlmytgen.loadSettings();
  applySettings(settings);
  setWizardStep(currentWizardStep, { persist: false });
  document.getElementById('btn-wizard-scoring').addEventListener('click', () => {
    switchMainTab('scoring');
    document.getElementById('status').textContent = '品質診断: Packaging Brief を選んでスコア実行';
  });

  const bindOpenDoc = (id, rel) => {
    const b = document.getElementById(id);
    if (b) {
      b.addEventListener('click', () => {
        window.nlmytgen.openRepoDoc(rel);
      });
    }
  };
  bindOpenDoc('btn-open-packaging-spec', 'docs/PACKAGING_ORCHESTRATOR_SPEC.md');
  bindOpenDoc('btn-open-h01-proof', 'docs/verification/H01-packaging-orchestrator-workflow-proof.md');
  bindOpenDoc('btn-open-workflow-proof-template', 'docs/workflow-proof-template.md');
  bindOpenDoc('btn-open-b11-checkpoints', 'docs/B11-manual-checkpoints.md');

  async function saveH01Template(format) {
    const status = document.getElementById('status');
    status.textContent = 'テンプレ出力中...';
    const r = await window.nlmytgen.emitPackagingBriefTemplate({ format });
    if (r.canceled) {
      status.textContent = 'キャンセル';
      return;
    }
    if (r.code === 0) {
      status.textContent = `保存: ${r.path}`;
      document.getElementById('scoring-brief-path').textContent = r.path;
      scoringBriefPath = r.path;
    } else {
      status.textContent = 'テンプレ出力失敗';
      alert([r.stderr, r.stdout].filter(Boolean).join('\n') || '失敗');
    }
  }
  const btnMd = document.getElementById('btn-save-h01-template-md');
  if (btnMd) btnMd.addEventListener('click', () => saveH01Template('markdown'));
  const btnJ = document.getElementById('btn-save-h01-template-json');
  if (btnJ) btnJ.addEventListener('click', () => saveH01Template('json'));
});

document.querySelector('[data-target="scoring-brief"]').addEventListener('click', async () => {
  const path = await window.nlmytgen.selectFile({
    title: 'Packaging Brief を選択',
    filters: [
      { name: 'Brief', extensions: ['json', 'md'] },
      { name: 'All', extensions: ['*'] },
    ],
  });
  if (path) {
    scoringBriefPath = path;
    document.getElementById('scoring-brief-path').textContent = path;
  }
});

function collectScores(prefix, categories) {
  const scores = {};
  for (const cat of categories) {
    scores[cat] = parseInt(document.getElementById(`${prefix}-${cat}`).value) || 0;
  }
  return scores;
}

function renderScoringResult(panel, result) {
  panel.classList.remove('hidden', 'success', 'error');
  if (result.json) {
    const j = result.json;
    panel.innerHTML = '';
    panel.classList.add(j.total_score >= 60 ? 'success' : 'error');
    let text = `Score: ${j.total_score}/100 (${j.band})\n\n`;
    for (const [cat, score] of Object.entries(j.category_scores || {})) {
      text += `  ${cat}: ${score}/3\n`;
    }
    if (j.warnings && j.warnings.length) {
      text += `\nWarnings:\n`;
      j.warnings.forEach(w => { text += `  ${w}\n`; });
    }
    if (j.recommended_repairs && j.recommended_repairs.length) {
      text += `\nRepairs:\n`;
      j.recommended_repairs.forEach(r => { text += `  - ${r}\n`; });
    }
    panel.textContent = text;
  } else {
    const raw = [result.stderr, result.stdout].filter(Boolean).join('\n') || 'Unknown error';
    renderFailurePanel(panel, raw, { genericDoc: 'docs/PACKAGING_ORCHESTRATOR_SPEC.md' });
  }
}

const EV_CATS = ['number', 'named_entity', 'anecdote', 'case', 'study', 'freshness', 'promise_payoff'];
const VD_CATS = ['scene_variety', 'information_embedding', 'symbolic_asset', 'tempo_shift', 'pattern_balance', 'stagnation_risk', 'promise_visual_payoff'];

document.getElementById('btn-score-evidence').addEventListener('click', async () => {
  if (!scoringBriefPath) {
    alert('Packaging Brief を選択してください');
    return;
  }
  const status = document.getElementById('status');
  status.textContent = 'Scoring evidence...';
  const result = await window.nlmytgen.scoreEvidence({
    brief: scoringBriefPath,
    scores: collectScores('ev', EV_CATS),
  });
  renderScoringResult(document.getElementById('evidence-result'), result);
  status.textContent = 'Evidence scoring complete';
});

document.getElementById('btn-score-visual').addEventListener('click', async () => {
  if (!scoringBriefPath) {
    alert('Packaging Brief を選択してください');
    return;
  }
  const status = document.getElementById('status');
  status.textContent = 'Scoring visual density...';
  const result = await window.nlmytgen.scoreVisualDensity({
    brief: scoringBriefPath,
    scores: collectScores('vd', VD_CATS),
  });
  renderScoringResult(document.getElementById('visual-result'), result);
  status.textContent = 'Visual density scoring complete';
});

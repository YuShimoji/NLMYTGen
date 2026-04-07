// --- Tab switching ---
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
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

function setTxtFile(filePath) {
  currentTxtPath = filePath;
  selectedFile.textContent = filePath;
  btnBuild.disabled = false;
  // #region agent log
  window.nlmytgen.debugLog({
    runId: 'pre-fix',
    hypothesisId: 'H4',
    location: 'renderer.js:setTxtFile',
    message: 'after assign',
    data: {
      pathTruthy: !!filePath,
      pathType: typeof filePath,
    },
  });
  // #endregion
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
  // #region agent log
  const f0 = files.length > 0 ? files[0] : null;
  window.nlmytgen.debugLog({
    runId: 'pre-fix',
    hypothesisId: 'H1',
    location: 'renderer.js:drop',
    message: 'drop handler',
    data: {
      filesLength: files.length,
      fileName: f0 ? f0.name : null,
      hasPathProp: !!(f0 && 'path' in f0),
      pathType: f0 && 'path' in f0 ? typeof f0.path : 'n/a',
      pathValue: f0 && f0.path != null ? String(f0.path).slice(0, 200) : null,
    },
  });
  // #endregion
  if (files.length > 0) {
    const f = files[0];
    const legacy = typeof f.path === 'string' ? f.path : '';
    const resolved = (legacy && legacy.trim()) || window.nlmytgen.getPathForFile(f) || '';
    // #region agent log
    window.nlmytgen.debugLog({
      runId: 'post-fix',
      hypothesisId: 'FIX',
      location: 'renderer.js:drop-resolve',
      message: 'path resolution',
      data: {
        legacyNonEmpty: !!(legacy && legacy.trim()),
        resolvedNonEmpty: !!resolved,
        resolvedTail: resolved ? resolved.slice(-80) : null,
      },
    });
    // #endregion
    if (resolved) {
      setTxtFile(resolved);
    }
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
      csvResult.classList.add('success');
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
      }
      if (result.json.dry_run) {
        text += `\n(dry-run: CSV not written)`;
      }

      if (document.getElementById('csv-save-diagnostics').checked) {
        status.textContent = dryRun ? 'Dry run complete — diagnosing…' : 'Writing CSV — diagnosing…';
        const diag = await window.nlmytgen.diagnoseScript({
          input: currentTxtPath,
          speakerMap: opts.speakerMap || undefined,
        });
        if (diag.json) {
          const saved = await window.nlmytgen.saveScriptDiagnostics({
            inputTxtPath: currentTxtPath,
            csvOutputPath: result.json.output || null,
            jsonPayload: diag.json,
          });
          if (saved.ok && saved.path) {
            text += `\n診断 JSON: ${saved.path}`;
            if (diag.code !== 0) {
              text += '\n（診断に ERROR あり。exit≠0 でも JSON は保存済み）';
            }
          } else {
            text += `\n診断 JSON 保存失敗: ${saved.error || 'unknown'}`;
          }
        } else {
          text += `\n診断 JSON 未取得: ${diag.stderr || diag.stdout || 'parse error'}`;
        }
      }

      csvResult.textContent = text;
      status.textContent = dryRun ? 'Dry run complete' : `CSV written (${result.json.rows} rows)`;
    } else {
      csvResult.classList.add('error');
      let errMsg = '';
      if (result.stderr) errMsg += result.stderr + '\n';
      if (result.stdout) errMsg += '[stdout] ' + result.stdout + '\n';
      errMsg += `[exit code] ${result.code}`;
      csvResult.textContent = errMsg || 'Unknown error';
      status.textContent = 'Build failed';
    }
  } catch (err) {
    csvResult.classList.remove('hidden');
    csvResult.classList.add('error');
    csvResult.textContent = err.message;
    status.textContent = 'Error';
  }

  btnBuild.disabled = false;
}

btnBuild.addEventListener('click', () => runBuildCsv(false));
btnDryRun.addEventListener('click', () => runBuildCsv(true));
btnOpenOutput.addEventListener('click', () => {
  if (lastOutputPath) window.nlmytgen.openFolder(lastOutputPath);
});

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
    validatePanel.classList.remove('hidden', 'success', 'error');

    if (result.code === 0) {
      validatePanel.classList.add('success');
      validatePanel.textContent = result.stdout || 'Validation passed';
      status.textContent = 'Validation passed';
    } else {
      validatePanel.classList.add('error');
      let text = '';
      if (result.stderr) text += result.stderr + '\n';
      if (result.stdout) text += result.stdout;
      validatePanel.textContent = text;
      status.textContent = 'Validation failed';
    }
  } catch (err) {
    validatePanel.classList.remove('hidden');
    validatePanel.classList.add('error');
    validatePanel.textContent = err.message;
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
    resultPanel.classList.remove('hidden', 'success', 'error');

    if (result.json && result.json.success) {
      resultPanel.classList.add('success');
      let text = '';
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
      resultPanel.textContent = text;
      status.textContent = dryRun ? 'Dry run complete' : 'Production applied';
    } else {
      resultPanel.classList.add('error');
      let errText = '';
      if (result.json && result.json.error) {
        errText += `Error: ${result.json.error}\n`;
      }
      if (result.json && result.json.fatal_warnings) {
        result.json.fatal_warnings.forEach(w => { errText += `  ${w}\n`; });
      }
      if (result.stderr) errText += result.stderr + '\n';
      if (result.stdout) errText += '[stdout] ' + result.stdout + '\n';
      errText += `[exit code] ${result.code}`;
      resultPanel.textContent = errText;
      status.textContent = 'Apply failed';
    }
  } catch (err) {
    resultPanel.classList.remove('hidden');
    resultPanel.classList.add('error');
    resultPanel.textContent = err.message;
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
    csv: {
      speakerMap: document.getElementById('speaker-map').value,
      maxLines: parseInt(document.getElementById('max-lines').value) || 2,
      charsPerLine: parseInt(document.getElementById('chars-per-line').value) || 40,
      reflowV2: document.getElementById('reflow-v2').checked,
      saveDiagnosticsWithCsv: document.getElementById('csv-save-diagnostics').checked,
    },
    production: {
      palette: filePaths['palette'] || null,
      bgMap: filePaths['bg-map'] || null,
      csvFile: filePaths['csv-file'] || null,
    },
  };
}

function applySettings(settings) {
  if (!settings) return;
  if (settings.csv) {
    if (settings.csv.speakerMap) document.getElementById('speaker-map').value = settings.csv.speakerMap;
    if (settings.csv.maxLines) document.getElementById('max-lines').value = settings.csv.maxLines;
    if (settings.csv.charsPerLine) document.getElementById('chars-per-line').value = settings.csv.charsPerLine;
    if (settings.csv.reflowV2 !== undefined) document.getElementById('reflow-v2').checked = settings.csv.reflowV2;
    if (settings.csv.saveDiagnosticsWithCsv !== undefined) {
      document.getElementById('csv-save-diagnostics').checked = settings.csv.saveDiagnosticsWithCsv;
    }
  }
  if (settings.production) {
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
  updateApplyButton();
}

function autoSave() {
  window.nlmytgen.saveSettings(collectSettings());
}

document.getElementById('speaker-map').addEventListener('change', autoSave);
document.getElementById('max-lines').addEventListener('change', autoSave);
document.getElementById('chars-per-line').addEventListener('change', autoSave);
document.getElementById('reflow-v2').addEventListener('change', autoSave);
document.getElementById('csv-save-diagnostics').addEventListener('change', autoSave);

// Load on startup
window.addEventListener('DOMContentLoaded', async () => {
  const settings = await window.nlmytgen.loadSettings();
  applySettings(settings);
});

// --- Scoring Tab ---
let scoringBriefPath = null;
let scriptDiagPath = null;

document.querySelector('[data-target="script-diag-input"]').addEventListener('click', async () => {
  const path = await window.nlmytgen.selectFile({
    title: '台本ファイルを選択',
    filters: [
      { name: 'Transcript', extensions: ['txt', 'csv'] },
      { name: 'All', extensions: ['*'] },
    ],
  });
  if (path) {
    scriptDiagPath = path;
    document.getElementById('script-diag-path').textContent = path;
  }
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
    panel.classList.add('error');
    panel.textContent = result.stderr || result.stdout || 'Unknown error';
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

function renderScriptDiagResult(panel, result) {
  panel.classList.remove('hidden', 'success', 'error');
  if (result.json && result.json.diagnostics) {
    const { diagnostics, meta } = result.json;
    const hasErr = diagnostics.some((d) => d.severity === 'error');
    panel.classList.add(hasErr ? 'error' : 'success');
    let text = `utterances: ${meta.utterance_count ?? '?'}\n\n`;
    for (const d of diagnostics) {
      text += `[${d.severity.toUpperCase()}] ${d.code}`;
      if (d.utterance_index != null) text += ` utt#${d.utterance_index}`;
      text += `\n  ${d.message}\n  HINT: ${d.hint}\n\n`;
    }
    panel.textContent = text;
  } else {
    panel.classList.add('error');
    panel.textContent = result.stderr || result.stdout || 'Unknown error';
  }
}

document.getElementById('btn-diagnose-script').addEventListener('click', async () => {
  if (!scriptDiagPath) {
    alert('台本ファイルを選択してください');
    return;
  }
  const status = document.getElementById('status');
  status.textContent = 'Diagnosing script...';
  const mapVal = document.getElementById('script-diag-speaker-map').value.trim();
  const result = await window.nlmytgen.diagnoseScript({
    input: scriptDiagPath,
    speakerMap: mapVal || undefined,
  });
  renderScriptDiagResult(document.getElementById('script-diag-result'), result);
  status.textContent = 'Script diagnosis complete';
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

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
const csvResult = document.getElementById('csv-result');
let currentTxtPath = null;

function setTxtFile(filePath) {
  currentTxtPath = filePath;
  selectedFile.textContent = filePath;
  btnBuild.disabled = false;
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
      }
      if (result.json.dry_run) {
        text += `\n(dry-run: CSV not written)`;
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
    }
  });
});

function updateApplyButton() {
  const ready = filePaths['prod-ymmp'] && filePaths['ir-json'];
  document.getElementById('btn-apply').disabled = !ready;
}

async function runApplyProduction(dryRun) {
  if (!filePaths['prod-ymmp'] || !filePaths['ir-json']) return;

  const status = document.getElementById('status');
  status.textContent = 'Applying production...';

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

// --- Settings persistence ---

function collectSettings() {
  return {
    csv: {
      speakerMap: document.getElementById('speaker-map').value,
      maxLines: parseInt(document.getElementById('max-lines').value) || 2,
      charsPerLine: parseInt(document.getElementById('chars-per-line').value) || 40,
      reflowV2: document.getElementById('reflow-v2').checked,
    },
    production: {
      palette: filePaths['palette'] || null,
      bgMap: filePaths['bg-map'] || null,
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
  }
}

// Auto-save on changes
function autoSave() {
  window.nlmytgen.saveSettings(collectSettings());
}

document.getElementById('speaker-map').addEventListener('change', autoSave);
document.getElementById('max-lines').addEventListener('change', autoSave);
document.getElementById('chars-per-line').addEventListener('change', autoSave);
document.getElementById('reflow-v2').addEventListener('change', autoSave);

// Also save when production file paths change
const originalBtnFileHandler = document.querySelectorAll('.btn-file');
originalBtnFileHandler.forEach(btn => {
  const origClick = btn.onclick;
  btn.addEventListener('click', () => {
    setTimeout(autoSave, 500);
  });
});

// Load on startup
window.addEventListener('DOMContentLoaded', async () => {
  const settings = await window.nlmytgen.loadSettings();
  applySettings(settings);
});

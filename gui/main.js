const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const SETTINGS_PATH = path.join(__dirname, 'project-settings.json');
const DEBUG_LOG_PATH = path.join(__dirname, '..', 'debug-1205ed.log');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    minWidth: 600,
    minHeight: 500,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    title: 'NLMYTGen',
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());

// #region agent log
ipcMain.handle('debug-log', async (_event, payload) => {
  try {
    const line = `${JSON.stringify({ sessionId: '1205ed', timestamp: Date.now(), ...payload })}\n`;
    fs.appendFileSync(DEBUG_LOG_PATH, line, 'utf8');
  } catch {
    /* ignore debug I/O errors */
  }
  return true;
});
// #endregion

// --- IPC handlers ---

function runCli(args) {
  return new Promise((resolve, reject) => {
    const repoRoot = path.resolve(__dirname, '..');
    const uvPath = process.platform === 'win32' ? 'uv.exe' : 'uv';
    const proc = spawn(uvPath, ['run', 'python', '-m', 'src.cli.main', ...args], {
      cwd: repoRoot,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data.toString('utf8'); });
    proc.stderr.on('data', (data) => { stderr += data.toString('utf8'); });

    proc.on('close', (code) => {
      resolve({ code, stdout, stderr });
    });

    proc.on('error', (err) => {
      resolve({ code: -1, stdout: '', stderr: `Process error: ${err.message}` });
    });
  });
}

function parseJsonLine(stdout) {
  const lines = stdout.trim().split('\n');
  for (let i = lines.length - 1; i >= 0; i--) {
    try {
      return JSON.parse(lines[i]);
    } catch { /* not JSON, try previous line */ }
  }
  return null;
}

ipcMain.handle('build-csv', async (_event, opts) => {
  const args = ['build-csv', opts.input, '--format', 'json'];
  if (opts.output) { args.push('-o', opts.output); }
  if (opts.speakerMap) { args.push('--speaker-map', opts.speakerMap); }
  if (opts.maxLines) { args.push('--max-lines', String(opts.maxLines)); }
  if (opts.charsPerLine) { args.push('--chars-per-line', String(opts.charsPerLine)); }
  if (opts.reflowV2) { args.push('--reflow-v2'); }
  if (opts.dryRun) { args.push('--dry-run'); }

  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('apply-production', async (_event, opts) => {
  const args = ['apply-production', opts.ymmp, opts.irJson, '--format', 'json'];
  if (opts.palette) { args.push('--palette', opts.palette); }
  if (opts.faceMap) { args.push('--face-map', opts.faceMap); }
  if (opts.bgMap) { args.push('--bg-map', opts.bgMap); }
  if (opts.slotMap) { args.push('--slot-map', opts.slotMap); }
  if (opts.csv) { args.push('--csv', opts.csv); }
  if (opts.output) { args.push('-o', opts.output); }
  if (opts.dryRun) { args.push('--dry-run'); }

  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('select-file', async (_event, opts) => {
  const result = await dialog.showOpenDialog(mainWindow, {
    title: opts.title || 'Select file',
    filters: opts.filters || [{ name: 'All', extensions: ['*'] }],
    properties: ['openFile'],
  });
  return result.canceled ? null : result.filePaths[0];
});

// --- Settings persistence ---

ipcMain.handle('load-settings', async () => {
  try {
    const data = fs.readFileSync(SETTINGS_PATH, 'utf8');
    return JSON.parse(data);
  } catch {
    return null;
  }
});

ipcMain.handle('save-settings', async (_event, settings) => {
  fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings, null, 2), 'utf8');
  return true;
});

// --- Open folder in Explorer ---

ipcMain.handle('open-folder', async (_event, filePath) => {
  const { shell } = require('electron');
  shell.showItemInFolder(filePath);
});

// --- Validate IR ---

ipcMain.handle('validate-ir', async (_event, opts) => {
  const args = ['validate-ir', opts.irJson];
  if (opts.faceMap) { args.push('--face-map', opts.faceMap); }
  if (opts.palette) { args.push('--palette', opts.palette); }

  const result = await runCli(args);
  return result;
});

// --- Save IR from paste ---

ipcMain.handle('score-evidence', async (_event, opts) => {
  const args = ['score-evidence', opts.brief, '--scores', JSON.stringify(opts.scores), '--format', 'json'];
  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('score-visual-density', async (_event, opts) => {
  const args = ['score-visual-density', opts.brief, '--scores', JSON.stringify(opts.scores), '--format', 'json'];
  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('diagnose-script', async (_event, opts) => {
  const args = ['diagnose-script', opts.input, '--format', 'json'];
  if (opts.speakerMap) args.push('--speaker-map', opts.speakerMap);
  if (opts.unlabeled) args.push('--unlabeled');
  if (opts.strict) args.push('--strict');
  if (opts.expectedExplainer) args.push('--expected-explainer', opts.expectedExplainer);
  if (opts.expectedListener) args.push('--expected-listener', opts.expectedListener);

  const result = await runCli(args);
  let json = null;
  try {
    json = JSON.parse(result.stdout.trim());
  } catch {
    /* stdout may be empty or non-JSON on failure */
  }
  return { ...result, json };
});

/** 台本診断 JSON を CSV と同じフォルダ（dry-run 時は台本と同じフォルダ）に書き出す */
ipcMain.handle('save-script-diagnostics', async (_event, opts) => {
  const inputTxtPath = opts.inputTxtPath;
  const csvOutputPath = opts.csvOutputPath || null;
  const jsonPayload = opts.jsonPayload;
  if (!inputTxtPath || !jsonPayload) {
    return { ok: false, error: 'inputTxtPath and jsonPayload are required' };
  }
  const stem = path.basename(inputTxtPath, path.extname(inputTxtPath));
  const dir = csvOutputPath ? path.dirname(csvOutputPath) : path.dirname(inputTxtPath);
  const outPath = path.join(dir, `${stem}_script-diagnostics.json`);
  fs.writeFileSync(outPath, `${JSON.stringify(jsonPayload, null, 2)}\n`, 'utf8');
  return { ok: true, path: outPath };
});

ipcMain.handle('save-ir-paste', async (_event, opts) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    title: 'IR JSON を保存',
    defaultPath: opts.defaultPath || 'ir.json',
    filters: [{ name: 'JSON', extensions: ['json'] }],
  });
  if (result.canceled) return null;
  fs.writeFileSync(result.filePath, opts.content, 'utf8');
  return result.filePath;
});

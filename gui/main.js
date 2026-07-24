const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const electronCompatibility = require('./electron_compatibility_probe');

const SETTINGS_PATH = path.join(__dirname, 'project-settings.json');
const REPO_ROOT = path.resolve(__dirname, '..');

let mainWindow;

if (electronCompatibility.isEnabled()) {
  app.setPath('userData', electronCompatibility.profilePath());
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    minWidth: 600,
    minHeight: 500,
    show: !electronCompatibility.isEnabled(),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      offscreen: electronCompatibility.isEnabled(),
    },
    title: 'NLMYTGen',
  });

  const observations = electronCompatibility.observe(mainWindow);
  await mainWindow.loadFile(path.join(__dirname, 'index.html'));
  if (electronCompatibility.isEnabled()) {
    await electronCompatibility.run(mainWindow, observations);
  }
}

app.whenReady().then(createWindow).catch((err) => {
  if (electronCompatibility.isEnabled()) {
    electronCompatibility.fail(err);
    app.quit();
    return;
  }
  console.error(err);
});
app.on('window-all-closed', () => app.quit());

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

function resolveRepoRelativePath(relPath) {
  if (typeof relPath !== 'string' || !relPath.trim()) {
    return { ok: false, error: 'repo-relative path is required' };
  }
  if (path.isAbsolute(relPath)) {
    return { ok: false, error: 'absolute path is not allowed' };
  }
  if (/^[a-zA-Z]:/.test(relPath)) {
    return { ok: false, error: 'drive-qualified path is not allowed' };
  }
  const normalized = path.normalize(relPath);
  if (normalized === '..' || normalized.startsWith(`..${path.sep}`)) {
    return { ok: false, error: 'path traversal is not allowed' };
  }
  const full = path.resolve(REPO_ROOT, normalized);
  const relToRoot = path.relative(REPO_ROOT, full);
  if (relToRoot.startsWith('..') || path.isAbsolute(relToRoot)) {
    return { ok: false, error: 'path outside repo' };
  }
  return { ok: true, full, rel: relToRoot.replace(/\\/g, '/') };
}

function describeEpisodePack(rootPath) {
  const root = path.resolve(rootPath);
  const episodeId = path.basename(root);
  const paths = {
    sourceScript: path.join(root, 'csv', `${episodeId}.txt`),
    csv: path.join(root, 'csv', `${episodeId}.csv`),
    irJson: path.join(root, 'ir', `${episodeId}_production_ir.json`),
    validateResult: path.join(root, 'ir', `${episodeId}_validate.json`),
    dryRunResult: path.join(root, 'ymmp', `${episodeId}_dry_run.json`),
    applyResult: path.join(root, 'ymmp', `${episodeId}_apply.json`),
    baseYmmp: path.join(root, 'ymmp', `${episodeId}_base.ymmp`),
    patchedYmmp: path.join(root, 'ymmp', `${episodeId}_patched.ymmp`),
    faceMap: path.join(root, 'maps', 'face_map.json'),
    bgMap: path.join(root, 'maps', 'bg_map.json'),
    skitGroupRegistry: path.join(root, 'maps', 'skit_group_registry.json'),
    skitGroupTemplateSource: path.join(
      REPO_ROOT,
      'samples',
      'templates',
      'skit_group',
      'delivery_v1_templates.ymmp',
    ),
    ymm4Acceptance: path.join(root, 'review', 'ymm4_acceptance.md'),
    gaps: path.join(root, 'review', 'gaps.md'),
    sessionManifest: path.join(root, 'manifest', 'session_manifest.md'),
  };
  const existing = {};
  for (const [key, value] of Object.entries(paths)) {
    existing[key] = fs.existsSync(value);
  }
  return { root, episodeId, paths, existing };
}

ipcMain.handle('build-csv', async (_event, opts) => {
  const args = ['build-csv', opts.input, '--format', 'json'];
  if (opts.output) { args.push('-o', opts.output); }
  if (opts.speakerMap) { args.push('--speaker-map', opts.speakerMap); }
  if (opts.maxLines) { args.push('--max-lines', String(opts.maxLines)); }
  if (opts.charsPerLine) { args.push('--chars-per-line', String(opts.charsPerLine)); }
  if (opts.subtitleFontSourceYmmp) {
    args.push('--subtitle-font-source-ymmp', opts.subtitleFontSourceYmmp);
  } else if (opts.subtitleFontScale) {
    args.push('--subtitle-font-scale', String(opts.subtitleFontScale));
  }
  if (opts.wrapPx) { args.push('--wrap-px', String(opts.wrapPx)); }
  if (opts.wrapSafety) { args.push('--wrap-safety', String(opts.wrapSafety)); }
  if (opts.measureBackend) { args.push('--measure-backend', opts.measureBackend); }
  if (opts.fontFamily) { args.push('--font-family', opts.fontFamily); }
  if (opts.fontSize) { args.push('--font-size', String(opts.fontSize)); }
  if (opts.letterSpacing !== undefined) { args.push('--letter-spacing', String(opts.letterSpacing)); }
  if (opts.reflowV2) { args.push('--reflow-v2'); }
  if (opts.balanceLines) { args.push('--balance-lines'); }
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
  if (opts.faceMapBundle) { args.push('--face-map-bundle', opts.faceMapBundle); }
  if (opts.slotMap) { args.push('--slot-map', opts.slotMap); }
  if (opts.csv) { args.push('--csv', opts.csv); }
  if (opts.skitGroupRegistry) { args.push('--skit-group-registry', opts.skitGroupRegistry); }
  if (opts.skitGroupTemplateSource) { args.push('--skit-group-template-source', opts.skitGroupTemplateSource); }
  if (opts.strictSkitGroupIntents) { args.push('--strict-skit-group-intents'); }
  if (opts.skitGroupOnly) { args.push('--skit-group-only'); }
  if (opts.output) { args.push('-o', opts.output); }
  if (opts.dryRun) { args.push('--dry-run'); }

  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('select-file', async (_event, opts) => {
  if (electronCompatibility.isEnabled()) {
    const result = electronCompatibility.openDialogResult({
      title: opts.title || 'Select file',
      filters: opts.filters || [{ name: 'All', extensions: ['*'] }],
      properties: ['openFile'],
    });
    return result.canceled ? null : result.filePaths[0];
  }
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

/** リポジトリ内ドキュメントを既定アプリで開く (パストラバーサル防止) */
ipcMain.handle('open-repo-doc', async (_event, relPath) => {
  const { shell } = require('electron');
  if (typeof relPath !== 'string' || !relPath) {
    return { ok: false, message: 'invalid path' };
  }
  const normalized = path.normalize(relPath).replace(/^(\.\.(\/|\\|$))+/, '');
  const full = path.resolve(REPO_ROOT, normalized);
  const relToRoot = path.relative(REPO_ROOT, full);
  if (relToRoot.startsWith('..') || path.isAbsolute(relToRoot)) {
    return { ok: false, message: 'path outside repo' };
  }
  if (!fs.existsSync(full)) {
    return { ok: false, message: `not found: ${full}` };
  }
  const errMsg = await shell.openPath(full);
  return errMsg ? { ok: false, message: errMsg } : { ok: true, path: full };
});

ipcMain.handle('load-review-packet', async (_event, packetPath) => {
  const resolved = resolveRepoRelativePath(packetPath);
  if (!resolved.ok) return { ok: false, error: resolved.error };
  if (!fs.existsSync(resolved.full)) {
    return { ok: false, error: `not found: ${resolved.rel}` };
  }
  try {
    const payload = JSON.parse(fs.readFileSync(resolved.full, 'utf8'));
    return { ok: true, path: resolved.rel, payload };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('load-review-proof', async (_event, proofPath) => {
  const resolved = resolveRepoRelativePath(proofPath);
  if (!resolved.ok) return { ok: false, error: resolved.error };
  if (!fs.existsSync(resolved.full)) {
    return { ok: false, error: `not found: ${resolved.rel}` };
  }
  try {
    const payload = JSON.parse(fs.readFileSync(resolved.full, 'utf8'));
    return { ok: true, path: resolved.rel, payload };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('check-review-artifacts', async (_event, artifactPaths) => {
  const paths = Array.isArray(artifactPaths) ? artifactPaths : [];
  const artifacts = paths.map((artifactPath) => {
    const resolved = resolveRepoRelativePath(artifactPath);
    if (!resolved.ok) {
      return {
        ok: false,
        exists: false,
        path: typeof artifactPath === 'string' ? artifactPath : '',
        error: resolved.error,
      };
    }
    return {
      ok: true,
      exists: fs.existsSync(resolved.full),
      path: resolved.rel,
    };
  });
  return {
    ok: artifacts.every((artifact) => artifact.ok),
    artifacts,
    missing_count: artifacts.filter((artifact) => artifact.ok && !artifact.exists).length,
    blocked_count: artifacts.filter((artifact) => !artifact.ok).length,
  };
});

ipcMain.handle('save-review-decisions', async (_event, opts) => {
  const decisionPath = opts && typeof opts.decisionPath === 'string' ? opts.decisionPath : '';
  const payload = opts && opts.payload && typeof opts.payload === 'object' ? opts.payload : null;
  const resolved = resolveRepoRelativePath(decisionPath);
  if (!resolved.ok) return { ok: false, error: resolved.error };
  if (!payload) return { ok: false, error: 'payload is required' };
  try {
    fs.mkdirSync(path.dirname(resolved.full), { recursive: true });
    fs.writeFileSync(resolved.full, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
    return { ok: true, path: resolved.rel };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

// --- Validate IR ---

ipcMain.handle('validate-ir', async (_event, opts) => {
  const args = ['validate-ir', opts.irJson, '--format', 'json'];
  if (opts.faceMap) { args.push('--face-map', opts.faceMap); }
  if (opts.faceMapBundle) { args.push('--face-map-bundle', opts.faceMapBundle); }
  if (opts.palette) { args.push('--palette', opts.palette); }
  if (opts.slotMap) { args.push('--slot-map', opts.slotMap); }
  if (opts.overlayMap) { args.push('--overlay-map', opts.overlayMap); }
  if (opts.seMap) { args.push('--se-map', opts.seMap); }
  if (opts.skitGroupRegistry) { args.push('--skit-group-registry', opts.skitGroupRegistry); }
  if (opts.strictSkitGroupIntents) { args.push('--strict-skit-group-intents'); }

  const result = await runCli(args);
  const json = parseJsonLine(result.stdout);
  return { ...result, json };
});

ipcMain.handle('select-folder', async () => {
  const r = await dialog.showOpenDialog(mainWindow, {
    title: '出力フォルダを選択',
    properties: ['openDirectory'],
  });
  return r.canceled ? null : r.filePaths[0];
});

ipcMain.handle('describe-episode-pack', async (_event, rootPath) => {
  if (typeof rootPath !== 'string' || !rootPath) {
    return null;
  }
  return describeEpisodePack(rootPath);
});

ipcMain.handle('select-episode-pack', async () => {
  const r = await dialog.showOpenDialog(mainWindow, {
    title: 'Episode Pack Root を選択',
    properties: ['openDirectory'],
  });
  return r.canceled ? null : describeEpisodePack(r.filePaths[0]);
});

ipcMain.handle('save-json-artifact', async (_event, opts) => {
  const outputPath = opts && typeof opts.path === 'string' ? opts.path : '';
  if (!outputPath) {
    return { ok: false, error: 'output path is required' };
  }
  try {
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(
      outputPath,
      `${JSON.stringify(opts.payload ?? {}, null, 2)}\n`,
      'utf8',
    );
    return { ok: true, path: outputPath };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('build-cue-packet-bundle', async (_event, opts) => {
  const args = ['build-cue-packet', opts.input, '--bundle-dir', opts.bundleDir];
  if (opts.speakerMap) { args.push('--speaker-map', opts.speakerMap); }
  if (opts.unlabeled) { args.push('--unlabeled'); }
  return runCli(args);
});

ipcMain.handle('build-diagram-packet-bundle', async (_event, opts) => {
  const args = ['build-diagram-packet', opts.input, '--bundle-dir', opts.bundleDir];
  if (opts.speakerMap) { args.push('--speaker-map', opts.speakerMap); }
  if (opts.unlabeled) { args.push('--unlabeled'); }
  return runCli(args);
});

/** H-01 空テンプレを保存ダイアログ経由で書き出す */
ipcMain.handle('emit-packaging-brief-template', async (_event, opts) => {
  const fmt = opts && opts.format === 'json' ? 'json' : 'markdown';
  const defaultPath = (opts && opts.defaultPath) || (fmt === 'json' ? 'packaging_brief.json' : 'packaging_brief.md');
  const save = await dialog.showSaveDialog(mainWindow, {
    title: 'H-01 Packaging Brief テンプレを保存',
    defaultPath,
    filters: fmt === 'json'
      ? [{ name: 'JSON', extensions: ['json'] }]
      : [{ name: 'Markdown', extensions: ['md'] }],
  });
  if (save.canceled) return { canceled: true };
  const args = ['emit-packaging-brief-template', '-o', save.filePath, '--format', fmt];
  const result = await runCli(args);
  return { canceled: false, ...result, path: save.filePath };
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
  const dialogOptions = {
    title: 'IR JSON を保存',
    defaultPath: opts.defaultPath || 'ir.json',
    filters: [{ name: 'JSON', extensions: ['json'] }],
  };
  const result = electronCompatibility.isEnabled()
    ? electronCompatibility.saveDialogResult(dialogOptions)
    : await dialog.showSaveDialog(mainWindow, dialogOptions);
  if (result.canceled) return null;
  fs.writeFileSync(result.filePath, opts.content, 'utf8');
  return result.filePath;
});

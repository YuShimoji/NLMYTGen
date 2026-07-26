const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const electronCompatibility = require('./electron_compatibility_probe');
const standardLoopProbe = require('./standard_production_loop_probe');
const batchObservabilityProbe = require('./batch_observability_probe');
const {
  BatchJobController,
  DEFAULT_CHANGE_SET_PATH,
  DEFAULT_QUEUE_PATH,
  LocalJournalStore,
  buildExecutorArgs,
  fileSha256,
  identitySha256,
  inspectAuthoritySet,
  normalizeExecutionResult,
  sanitizeOperatorText,
  validateJournalAgainstPlan,
} = require('./batch_observability');
const {
  ACCEPTED_MANIFEST_RELATIVE_PATH,
  PipelineJobController,
  buildDoctorArgs,
  buildEpisodeArgs,
  classifyProfiles,
  resolveRepoRelativePath: resolveStandardLoopPath,
  summarizeManifest,
  validateRunId,
} = require('./standard_production_loop');

const SETTINGS_PATH = path.join(__dirname, 'project-settings.json');
const REPO_ROOT = path.resolve(__dirname, '..');
const DEVELOPMENT_AUDIO_POLICY = 'silent';

let mainWindow;

const compatibilityMode = electronCompatibility.isEnabled();
const standardLoopProbeMode = standardLoopProbe.isEnabled();
const batchObservabilityProbeMode = batchObservabilityProbe.isEnabled();

if (compatibilityMode) {
  app.setPath('userData', electronCompatibility.profilePath());
} else if (standardLoopProbeMode) {
  app.setPath('userData', standardLoopProbe.profilePath());
} else if (batchObservabilityProbeMode) {
  app.setPath('userData', batchObservabilityProbe.profilePath());
}

async function createWindow() {
  const probeWidth = Number.parseInt(
    process.env.NLMYTGEN_BATCH_OBSERVABILITY_WIDTH
      || process.env.NLMYTGEN_STANDARD_LOOP_WIDTH
      || '',
    10,
  );
  const probeHeight = Number.parseInt(
    process.env.NLMYTGEN_BATCH_OBSERVABILITY_HEIGHT
      || process.env.NLMYTGEN_STANDARD_LOOP_HEIGHT
      || '',
    10,
  );
  mainWindow = new BrowserWindow({
    width: Number.isFinite(probeWidth) ? probeWidth : 900,
    height: Number.isFinite(probeHeight) ? probeHeight : 700,
    minWidth: 600,
    minHeight: 500,
    show: !(compatibilityMode || standardLoopProbeMode || batchObservabilityProbeMode),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      offscreen: compatibilityMode || standardLoopProbeMode || batchObservabilityProbeMode,
    },
    title: 'NLMYTGen',
  });

  const observations = compatibilityMode
    ? electronCompatibility.observe(mainWindow)
    : (standardLoopProbeMode
      ? standardLoopProbe.observe(mainWindow)
      : (batchObservabilityProbeMode
        ? batchObservabilityProbe.observe(mainWindow)
        : null));
  await mainWindow.loadFile(path.join(__dirname, 'index.html'));
  if (compatibilityMode) {
    await electronCompatibility.run(mainWindow, observations);
  } else if (standardLoopProbeMode) {
    await standardLoopProbe.run(mainWindow, observations);
  } else if (batchObservabilityProbeMode) {
    await batchObservabilityProbe.run(mainWindow, observations);
  }
}

app.whenReady().then(createWindow).catch((err) => {
  if (compatibilityMode) {
    electronCompatibility.fail(err);
    app.quit();
    return;
  }
  if (standardLoopProbeMode) {
    standardLoopProbe.fail(err);
    app.quit();
    return;
  }
  if (batchObservabilityProbeMode) {
    batchObservabilityProbe.fail(err);
    app.quit();
    return;
  }
  console.error(err);
});
app.on('window-all-closed', async () => {
  const job = standardLoopJobs.snapshot();
  if (job.active) await standardLoopJobs.cancel(job.id);
  const batchJob = batchJobs.snapshot();
  if (batchJob.active) await batchJobs.cancel(batchJob.id);
  app.quit();
});

// --- IPC handlers ---

function runCli(args) {
  return new Promise((resolve, reject) => {
    const repoRoot = path.resolve(__dirname, '..');
    const uvPath = process.platform === 'win32' ? 'uv.exe' : 'uv';
    const proc = spawn(uvPath, ['run', 'python', '-m', 'src.cli.main', ...args], {
      cwd: repoRoot,
      env: {
        ...process.env,
        PYTHONIOENCODING: 'utf-8',
        NLMYTGEN_AUDIO_POLICY: DEVELOPMENT_AUDIO_POLICY,
      },
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
  try {
    return JSON.parse(stdout.trim());
  } catch { /* mixed or line-delimited stdout; try individual lines */ }
  const lines = stdout.trim().split('\n');
  for (let i = lines.length - 1; i >= 0; i--) {
    try {
      return JSON.parse(lines[i]);
    } catch { /* not JSON, try previous line */ }
  }
  return null;
}

function spawnStandardLoopProcess(spec, callbacks) {
  const uvPath = process.platform === 'win32' ? 'uv.exe' : 'uv';
  let proc;
  if (process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE === '1') {
    const requestedDelay = Number.parseInt(
      process.env.NLMYTGEN_STANDARD_LOOP_TEST_DOUBLE_DELAY_MS || '0',
      10,
    );
    const delayMs = Number.isFinite(requestedDelay)
      ? Math.max(0, Math.min(requestedDelay, 5000))
      : 0;
    proc = spawn(process.execPath, [
      '-e',
      [
        `console.log(${JSON.stringify(`TEST_DOUBLE_COMMAND=uv run python -m src.cli.main ${spec.args.join(' ')}`)});`,
        `setTimeout(() => console.log("TEST_DOUBLE_RENDER_NOT_PERFORMED"), ${delayMs});`,
      ].join(''),
    ], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        ELECTRON_RUN_AS_NODE: '1',
        NLMYTGEN_AUDIO_POLICY: DEVELOPMENT_AUDIO_POLICY,
      },
    });
  } else {
    proc = spawn(uvPath, ['run', 'python', '-m', 'src.cli.main', ...spec.args], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        PYTHONIOENCODING: 'utf-8',
        NLMYTGEN_AUDIO_POLICY: DEVELOPMENT_AUDIO_POLICY,
      },
    });
  }
  proc.stdout.on('data', (data) => callbacks.stdout(data.toString('utf8')));
  proc.stderr.on('data', (data) => callbacks.stderr(data.toString('utf8')));
  proc.on('error', (err) => callbacks.stderr(`Process error: ${err.message}`));
  proc.on('close', (code) => callbacks.close({ code, cancelled: proc.__nlmytgenCancelled === true }));
  return proc;
}

function cancelOwnedProcessTree(proc) {
  if (!proc || !Number.isInteger(proc.pid)) {
    return Promise.reject(new Error('owned child process is unavailable'));
  }
  proc.__nlmytgenCancelled = true;
  if (process.platform !== 'win32') {
    proc.kill('SIGTERM');
    return Promise.resolve();
  }
  return new Promise((resolve, reject) => {
    const killer = spawn('taskkill.exe', ['/PID', String(proc.pid), '/T', '/F'], {
      windowsHide: true,
      stdio: 'ignore',
    });
    killer.once('error', reject);
    killer.once('close', (code) => {
      if (code === 0 || proc.exitCode !== null) resolve();
      else reject(new Error(`taskkill exited with ${code}`));
    });
  });
}

const standardLoopJobs = new PipelineJobController({
  startProcess: spawnStandardLoopProcess,
  cancelProcess: cancelOwnedProcessTree,
  emit: (type, payload) => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('standard-loop-job-event', { type, ...payload });
    }
  },
});
const batchSelections = new Map();
let batchLastExecutionResult = null;
let batchLastAuthoritySummary = null;
let batchJournalStore = null;

function currentBatchJournalStore() {
  if (!batchJournalStore) {
    const journalRoot = batchObservabilityProbeMode
      ? path.join(app.getPath('userData'), 'batch-journals')
      : path.join(REPO_ROOT, '_tmp', 'gui-batch-journals');
    batchJournalStore = new LocalJournalStore(journalRoot);
  }
  return batchJournalStore;
}

function displayLocator(fullPath) {
  const relative = path.relative(REPO_ROOT, fullPath);
  if (!relative.startsWith('..') && !path.isAbsolute(relative)) {
    return relative.replace(/\\/g, '/');
  }
  return `local/${path.basename(fullPath)}`;
}

function validateBatchSelectionPayload(kind, fullPath) {
  const contracts = {
    queue: 'nlmytgen.factory_queue.v1',
    change_set: 'nlmytgen.factory_queue.change_set.v1',
  };
  const expectedSchema = contracts[kind];
  if (!expectedSchema) return;
  const payload = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
  if (payload?.schema !== expectedSchema || payload?.schema_version !== '1.0') {
    throw new Error(`BATCH_${kind.toUpperCase()}_SCHEMA_INVALID`);
  }
}

function registerBatchSelection(kind, fullPath, { repoOnly = false } = {}) {
  const resolved = path.resolve(fullPath);
  const relative = path.relative(REPO_ROOT, resolved);
  if (repoOnly && (relative.startsWith('..') || path.isAbsolute(relative))) {
    throw new Error(`BATCH_${kind.toUpperCase()}_OUTSIDE_REPOSITORY`);
  }
  validateBatchSelectionPayload(kind, resolved);
  const selectionId = `${kind}-${identitySha256({
    path: resolved,
    sha256: fileSha256(resolved),
  }).slice(0, 24)}`;
  const value = {
    selectionId,
    kind,
    fullPath: resolved,
    displayPath: displayLocator(resolved),
    sha256: fileSha256(resolved),
  };
  batchSelections.set(selectionId, value);
  return {
    selection_id: selectionId,
    kind,
    display_path: value.displayPath,
    sha256: value.sha256,
  };
}

function batchSelection(selectionId, kind, { repoOnly = false } = {}) {
  const selected = batchSelections.get(selectionId);
  if (!selected || selected.kind !== kind || !fs.existsSync(selected.fullPath)) {
    throw new Error(`BATCH_${kind.toUpperCase()}_SELECTION_INVALID`);
  }
  if (repoOnly) {
    const relative = path.relative(REPO_ROOT, selected.fullPath);
    if (relative.startsWith('..') || path.isAbsolute(relative)) {
      throw new Error(`BATCH_${kind.toUpperCase()}_OUTSIDE_REPOSITORY`);
    }
  }
  return selected;
}

function descriptorLoader(relativePath) {
  const resolved = resolveRepoRelativePath(relativePath);
  if (!resolved.ok) throw new Error('BATCH_DESCRIPTOR_PATH_INVALID');
  return JSON.parse(fs.readFileSync(resolved.full, 'utf8'));
}

function executionResultFromJournal(journal) {
  return {
    schema: 'nlmytgen.factory_queue.execution_result.v1',
    schema_version: '1.0',
    status: journal.status,
    plan: {
      schema: 'nlmytgen.factory_queue.executor.v1',
      schema_version: '1.0',
      package_count: (journal.entries || []).length,
      mutating_entry_count: (journal.entries || []).filter(
        (entry) => Boolean(entry.requested_operation),
      ).length,
      plan_identity_sha256: journal.plan_identity_sha256,
      queue: journal.queue,
      change_set: journal.change_set,
    },
    journal,
    execution_receipt: {
      schema: 'nlmytgen.factory_queue.execution_receipt.v1',
      journal_sha256: identitySha256(journal),
    },
  };
}

function completedBatchResult({ code, cancelled, stdout, stderr }) {
  if (cancelled) return { ok: false, cancelled: true, error: 'BATCH_JOB_CANCELLED' };
  const json = parseJsonLine(stdout);
  if (!json) {
    return {
      ok: false,
      error: 'BATCH_EXECUTOR_JSON_MISSING',
      detail: sanitizeOperatorText(stderr || stdout, 2000),
    };
  }
  if (code !== 0) {
    return {
      ok: false,
      error: 'BATCH_EXECUTOR_FAILED',
      detail: sanitizeOperatorText(stderr || json.error || stdout, 2000),
    };
  }
  batchLastExecutionResult = json;
  const persisted = json.journal?.execution_mode !== 'plan_only';
  const saved = persisted ? currentBatchJournalStore().persist(json) : null;
  const journalSelection = saved
    ? registerBatchSelection('journal', saved.path, { repoOnly: true })
    : null;
  const readModel = normalizeExecutionResult(json, {
    descriptorLoader,
    authoritySummary: batchLastAuthoritySummary,
    journalLocator: journalSelection?.display_path || 'plan-only/current',
  });
  return {
    ok: true,
    read_model: readModel,
    execution_result_identity_sha256: identitySha256(json),
    journal_selection_id: journalSelection?.selection_id || null,
  };
}

const batchJobs = new BatchJobController({
  startProcess: spawnStandardLoopProcess,
  cancelProcess: cancelOwnedProcessTree,
  isOtherJobActive: () => standardLoopJobs.snapshot().active,
  emit: (type, payload) => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('batch-job-event', { type, ...payload });
    }
  },
});
let standardLoopDoctorProfiles = [];
const standardLoopDryRunPasses = new Map();
const standardLoopAcceptedManifest = (
  standardLoopProbeMode
  && process.env.NLMYTGEN_STANDARD_LOOP_MANIFEST
)
  ? process.env.NLMYTGEN_STANDARD_LOOP_MANIFEST.replace(/\\/g, '/')
  : ACCEPTED_MANIFEST_RELATIVE_PATH;

function standardLoopRequest(value) {
  if (typeof value === 'string') {
    return { manifestPath: value, runId: null };
  }
  return {
    manifestPath: value?.manifestPath,
    runId: value?.runId ?? null,
  };
}

function standardLoopDryRunKey(manifestPath, runId) {
  return `${manifestPath}\u0000${runId || ''}`;
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
  if (compatibilityMode) {
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

// --- Standard automated production loop ---

ipcMain.handle('standard-loop-accepted-manifest', async () => (
  summarizeManifest(REPO_ROOT, standardLoopAcceptedManifest)
));

ipcMain.handle('standard-loop-select-manifest', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    title: 'エピソードマニフェストを選択',
    filters: [{ name: 'Episode manifest', extensions: ['json'] }],
    properties: ['openFile'],
  });
  if (result.canceled) return { ok: false, canceled: true };
  const relative = path.relative(REPO_ROOT, result.filePaths[0]);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    return { ok: false, error: 'リポジトリ外のマニフェストは選択できません' };
  }
  return summarizeManifest(REPO_ROOT, relative.replace(/\\/g, '/'));
});

ipcMain.handle('standard-loop-load-manifest', async (_event, request) => {
  const normalized = standardLoopRequest(request);
  return summarizeManifest(REPO_ROOT, normalized.manifestPath, normalized.runId);
});

ipcMain.handle('standard-loop-doctor', async () => {
  const result = await runCli(buildDoctorArgs());
  const json = parseJsonLine(result.stdout);
  standardLoopDoctorProfiles = classifyProfiles(json);
  return {
    ...result,
    json,
    profiles: standardLoopDoctorProfiles,
  };
});

ipcMain.handle('standard-loop-dry-run', async (_event, request) => {
  const normalized = standardLoopRequest(request);
  const resolved = resolveStandardLoopPath(REPO_ROOT, normalized.manifestPath);
  if (!resolved.ok) return { code: -1, stdout: '', stderr: resolved.error, json: null };
  const runId = normalized.runId === null
    ? null
    : validateRunId(normalized.runId);
  if (runId && !runId.ok) {
    return { code: -1, stdout: '', stderr: runId.error, json: null };
  }
  const resolvedRunId = runId?.runId || null;
  const result = await runCli(buildEpisodeArgs(resolved.rel, {
    dryRun: true,
    runId: resolvedRunId,
  }));
  const json = parseJsonLine(result.stdout);
  if (result.code === 0 && json) {
    const summary = summarizeManifest(REPO_ROOT, resolved.rel, resolvedRunId);
    if (summary.ok) {
      standardLoopDryRunPasses.set(
        standardLoopDryRunKey(resolved.rel, summary.resolved_run_id),
        summary.manifest_sha256,
      );
    }
  }
  return { ...result, json };
});

ipcMain.handle('standard-loop-start', async (_event, opts) => {
  if (DEVELOPMENT_AUDIO_POLICY !== 'silent') {
    return { ok: false, error: 'SILENT_POLICY_REQUIRED' };
  }
  if (batchJobs.snapshot().active) {
    return { ok: false, error: 'PIPELINE_JOB_ALREADY_ACTIVE' };
  }
  const resolved = resolveStandardLoopPath(REPO_ROOT, opts?.manifestPath);
  if (!resolved.ok) return { ok: false, error: resolved.error };
  const validatedRunId = validateRunId(opts?.runId);
  if (!validatedRunId.ok) return { ok: false, error: validatedRunId.error };
  const summary = summarizeManifest(REPO_ROOT, resolved.rel, validatedRunId.runId);
  if (!summary.ok) return summary;
  if (summary.protected_inputs.status !== 'exact') {
    return { ok: false, error: 'PROTECTED_INPUTS_NOT_EXACT', summary };
  }
  const dryRunKey = standardLoopDryRunKey(resolved.rel, summary.resolved_run_id);
  if (standardLoopDryRunPasses.get(dryRunKey) !== summary.manifest_sha256) {
    return { ok: false, error: 'SUCCESSFUL_DRY_RUN_REQUIRED', summary };
  }
  const allProfilesReady = (
    standardLoopDoctorProfiles.length === 4
    && standardLoopDoctorProfiles.every((profile) => profile.state === 'ready')
  );
  const renderTestDouble = process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE === '1';
  if (!allProfilesReady && !renderTestDouble) {
    return { ok: false, error: 'ALL_RUNTIME_PROFILES_NOT_READY', summary };
  }
  const resume = opts?.resume === true && summary.output.status !== 'absent';
  const args = buildEpisodeArgs(resolved.rel, {
    render: true,
    resume,
    runId: summary.resolved_run_id,
  });
  return standardLoopJobs.start({
    args,
    manifestPath: resolved.rel,
    runId: summary.resolved_run_id,
    readinessBypass: false,
    renderTestDouble,
  });
});

ipcMain.handle('standard-loop-cancel', async (_event, jobId) => (
  standardLoopJobs.cancel(jobId)
));

ipcMain.handle('standard-loop-job', async () => standardLoopJobs.snapshot());

ipcMain.handle('standard-loop-open-output', async (_event, relPath) => {
  const { shell } = require('electron');
  const resolved = resolveStandardLoopPath(REPO_ROOT, relPath);
  if (!resolved.ok || !fs.existsSync(resolved.full)) {
    return { ok: false, error: resolved.error || `not found: ${resolved?.rel || relPath}` };
  }
  const error = await shell.openPath(resolved.full);
  return error ? { ok: false, error } : { ok: true, path: resolved.rel };
});

// --- Bounded factory queue batch observability ---

ipcMain.handle('batch-default-selections', async () => {
  const queue = registerBatchSelection('queue', path.join(REPO_ROOT, DEFAULT_QUEUE_PATH));
  const changeSet = registerBatchSelection(
    'change_set',
    path.join(REPO_ROOT, DEFAULT_CHANGE_SET_PATH),
  );
  return {
    ok: true,
    queue,
    change_set: changeSet,
    plan_status: batchLastExecutionResult ? 'available' : 'not_run',
  };
});

ipcMain.handle('batch-select-file', async (_event, kind) => {
  const supported = new Set(['queue', 'change_set', 'authority', 'journal']);
  if (!supported.has(kind)) return { ok: false, error: 'BATCH_SELECTION_KIND_INVALID' };
  const titles = {
    queue: 'Factory Queue を選択',
    change_set: 'Change Set を選択',
    authority: 'Execution Authority を選択',
    journal: 'Execution Journal を選択',
  };
  const result = await dialog.showOpenDialog(mainWindow, {
    title: titles[kind],
    filters: [{ name: 'JSON', extensions: ['json'] }],
    properties: ['openFile'],
  });
  if (result.canceled) return { ok: false, canceled: true };
  try {
    const selected = registerBatchSelection(kind, result.filePaths[0], { repoOnly: true });
    batchSelection(selected.selection_id, kind, { repoOnly: true });
    if (kind === 'authority') {
      const authority = JSON.parse(fs.readFileSync(result.filePaths[0], 'utf8'));
      batchLastAuthoritySummary = batchLastExecutionResult
        ? inspectAuthoritySet(batchLastExecutionResult, authority)
        : { status: 'required', exact: false, error: 'PLAN_REQUIRED_FOR_AUTHORITY_PREFLIGHT' };
      return { ok: true, selection: selected, authority: batchLastAuthoritySummary };
    }
    if (kind === 'journal') {
      const loaded = currentBatchJournalStore().load(result.filePaths[0]);
      const validation = batchLastExecutionResult
        ? validateJournalAgainstPlan(batchLastExecutionResult, loaded.journal)
        : { ok: false, error: 'PLAN_REQUIRED_FOR_RESUME' };
      if (validation.ok) {
        batchLastExecutionResult = executionResultFromJournal(loaded.journal);
        batchLastAuthoritySummary = null;
      }
      const readModel = normalizeExecutionResult(
        executionResultFromJournal(loaded.journal),
        {
          descriptorLoader,
          authoritySummary: batchLastAuthoritySummary,
          journalLocator: selected.display_path,
        },
      );
      return {
        ok: true,
        selection: selected,
        journal: {
          identity_sha256: loaded.file_sha256,
          prefix_identity_sha256: loaded.prefix_identity_sha256,
          event_count: loaded.event_count,
          validation,
          authority: {
            status: readModel.authority.state,
            exact: readModel.authority.state === 'not_required',
          },
          read_model: readModel,
        },
      };
    }
    return { ok: true, selection: selected };
  } catch (error) {
    return { ok: false, error: sanitizeOperatorText(error.message, 1000) };
  }
});

ipcMain.handle('batch-open-recent-journal', async () => {
  try {
    const loaded = currentBatchJournalStore().loadRecent();
    if (!loaded) return { ok: false, error: 'RECENT_JOURNAL_NOT_FOUND' };
    const selected = registerBatchSelection(
      'journal',
      loaded.path,
      { repoOnly: true },
    );
    const validation = batchLastExecutionResult
      ? validateJournalAgainstPlan(batchLastExecutionResult, loaded.journal)
      : { ok: false, error: 'PLAN_REQUIRED_FOR_RESUME' };
    if (validation.ok) {
      batchLastExecutionResult = executionResultFromJournal(loaded.journal);
      batchLastAuthoritySummary = null;
    }
    const readModel = normalizeExecutionResult(
      executionResultFromJournal(loaded.journal),
      {
        descriptorLoader,
        authoritySummary: batchLastAuthoritySummary,
        journalLocator: selected.display_path,
      },
    );
    return {
      ok: true,
      selection: selected,
      journal: {
        identity_sha256: loaded.file_sha256,
        prefix_identity_sha256: loaded.prefix_identity_sha256,
        event_count: loaded.event_count,
        validation,
        authority: {
          status: readModel.authority.state,
          exact: readModel.authority.state === 'not_required',
        },
        read_model: readModel,
      },
    };
  } catch (error) {
    return { ok: false, error: sanitizeOperatorText(error.message, 1000) };
  }
});

ipcMain.handle('batch-start', async (_event, request) => {
  try {
    if (DEVELOPMENT_AUDIO_POLICY !== 'silent') {
      return { ok: false, error: 'SILENT_POLICY_REQUIRED' };
    }
    const mode = request?.execute === true ? 'execute' : 'plan';
    const queue = batchSelection(request?.queueSelectionId, 'queue', { repoOnly: true });
    const changeSet = batchSelection(
      request?.changeSetSelectionId,
      'change_set',
      { repoOnly: true },
    );
    let authority = null;
    let journal = null;
    if (request?.authoritySelectionId) {
      authority = batchSelection(request.authoritySelectionId, 'authority');
    }
    if (request?.journalSelectionId) {
      journal = batchSelection(request.journalSelectionId, 'journal');
    }
    if (mode === 'execute') {
      const changeSetJson = JSON.parse(fs.readFileSync(changeSet.fullPath, 'utf8'));
      const mutatingEntries = Array.isArray(changeSetJson.entries)
        ? changeSetJson.entries.length
        : -1;
      if (mutatingEntries < 0) return { ok: false, error: 'CHANGE_SET_ENTRIES_INVALID' };
      if (mutatingEntries > 0) {
        if (!authority) return { ok: false, error: 'EXACT_AUTHORITY_REQUIRED' };
        if (!batchLastExecutionResult) return { ok: false, error: 'SUCCESSFUL_PLAN_REQUIRED' };
        const authorityJson = JSON.parse(fs.readFileSync(authority.fullPath, 'utf8'));
        batchLastAuthoritySummary = inspectAuthoritySet(batchLastExecutionResult, authorityJson);
        if (batchLastAuthoritySummary.status !== 'available' || !batchLastAuthoritySummary.exact) {
          return { ok: false, error: 'EXACT_AUTHORITY_PREFLIGHT_FAILED' };
        }
      } else {
        batchLastAuthoritySummary = { status: 'not_required', exact: true, records: [] };
      }
    } else {
      batchLastAuthoritySummary = null;
    }
    const args = buildExecutorArgs({
      queuePath: queue.displayPath,
      changeSetPath: changeSet.displayPath,
      authorityPath: mode === 'execute' ? (authority?.displayPath || null) : null,
      journalPath: mode === 'execute' ? (journal?.displayPath || null) : null,
      execute: mode === 'execute',
    });
    return batchJobs.start({
      kind: 'batch',
      mode,
      args,
      complete: completedBatchResult,
    });
  } catch (error) {
    return { ok: false, error: sanitizeOperatorText(error.message, 1000) };
  }
});

ipcMain.handle('batch-cancel', async (_event, jobId) => batchJobs.cancel(jobId));
ipcMain.handle('batch-job', async () => batchJobs.snapshot());
if (batchObservabilityProbeMode) {
  ipcMain.handle('batch-probe-reset-runtime-state', async () => {
    if (batchJobs.snapshot().active || standardLoopJobs.snapshot().active) {
      return { ok: false, error: 'PIPELINE_JOB_ALREADY_ACTIVE' };
    }
    batchSelections.clear();
    batchLastExecutionResult = null;
    batchLastAuthoritySummary = null;
    return { ok: true };
  });
}

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

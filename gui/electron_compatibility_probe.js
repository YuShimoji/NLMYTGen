const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { app, ipcMain } = require('electron');

const MAIN_MESSAGE_CHANNEL = 'nlmytgen-electron-compatibility-main-message';
const REQUIRED_BRIDGE_METHODS = [
  'checkReviewArtifacts',
  'diagnoseScript',
  'loadReviewProof',
  'loadSettings',
  'saveIrPaste',
  'selectFile',
];
const dialogRequests = [];

function isEnabled() {
  return process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE === '1';
}

function requiredPath(name) {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is required in compatibility smoke mode`);
  return path.resolve(value);
}

function profilePath() {
  return requiredPath('NLMYTGEN_ELECTRON_COMPATIBILITY_PROFILE');
}

function receiptPath() {
  return requiredPath('NLMYTGEN_ELECTRON_COMPATIBILITY_RECEIPT');
}

function dialogFixturePath() {
  return requiredPath('NLMYTGEN_ELECTRON_COMPATIBILITY_DIALOG_PATH');
}

function openDialogResult(options) {
  dialogRequests.push({ kind: 'open', options });
  return { canceled: false, filePaths: [dialogFixturePath()] };
}

function saveDialogResult(options) {
  const filePath = path.join(path.dirname(receiptPath()), 'dialog-save-result.json');
  dialogRequests.push({ kind: 'save', options });
  return { canceled: false, filePath };
}

function writeReceipt(payload) {
  const target = receiptPath();
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  console.log(`ELECTRON_COMPATIBILITY_RECEIPT=${target}`);
  console.log(JSON.stringify(payload, null, 2));
}

function observe(win) {
  const observations = {
    console_messages: [],
    did_fail_load: [],
    render_process_gone: [],
    preload_errors: [],
    renderer_unhandled_errors: [],
  };
  const rendererErrorHandler = (_event, detail) => {
    observations.renderer_unhandled_errors.push(detail);
  };
  ipcMain.on('nlmytgen-electron-compatibility-renderer-error', rendererErrorHandler);
  Object.defineProperty(observations, 'dispose', {
    enumerable: false,
    value: () => {
      ipcMain.off('nlmytgen-electron-compatibility-renderer-error', rendererErrorHandler);
    },
  });

  win.webContents.on('console-message', (_event, ...args) => {
    const detail = args.length === 1 && args[0] && typeof args[0] === 'object'
      ? args[0]
      : {
        level: args[0],
        message: args[1],
        lineNumber: args[2],
        sourceId: args[3],
      };
    observations.console_messages.push({
      level: detail.level,
      message: String(detail.message || ''),
      line_number: detail.lineNumber || null,
      source_id: detail.sourceId || null,
    });
  });
  win.webContents.on('did-fail-load', (_event, errorCode, errorDescription, validatedURL, isMainFrame) => {
    observations.did_fail_load.push({
      error_code: errorCode,
      error_description: errorDescription,
      validated_url: validatedURL,
      is_main_frame: isMainFrame,
    });
  });
  win.webContents.on('render-process-gone', (_event, details) => {
    observations.render_process_gone.push(details);
  });
  win.webContents.on('preload-error', (_event, preloadPath, error) => {
    observations.preload_errors.push({
      preload_path: preloadPath,
      error: error && (error.stack || error.message || String(error)),
    });
  });
  return observations;
}

function withTimeout(promise, timeoutMs, label) {
  let timeout;
  const timeoutPromise = new Promise((_resolve, reject) => {
    timeout = setTimeout(() => reject(new Error(`${label} timed out after ${timeoutMs}ms`)), timeoutMs);
  });
  return Promise.race([promise, timeoutPromise]).finally(() => clearTimeout(timeout));
}

async function run(win, observations) {
  const token = `electron-compatibility-${process.pid}`;
  const fixturePath = dialogFixturePath();

  const registration = await win.webContents.executeJavaScript(`
    (() => {
      window.__nlmytgenCompatibilityMainMessage = null;
      if (!window.__nlmytgenCompatibility?.onMainMessage) {
        throw new Error('compatibility main-message bridge is unavailable');
      }
      window.__nlmytgenCompatibility.onMainMessage((payload) => {
        window.__nlmytgenCompatibilityMainMessage = payload;
      });
      return 'registered';
    })()
  `);
  win.webContents.send(MAIN_MESSAGE_CHANNEL, { token, source: 'main' });

  const renderer = await withTimeout(win.webContents.executeJavaScript(`
    (async () => {
      const started = Date.now();
      while (!window.__nlmytgenCompatibilityMainMessage) {
        if (Date.now() - started > 5000) {
          throw new Error('main-to-renderer compatibility message timed out');
        }
        await new Promise((resolve) => setTimeout(resolve, 25));
      }
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      const bridgeKeys = Object.keys(window.nlmytgen || {}).sort();
      const dialogPath = await window.nlmytgen.selectFile({
        title: 'Electron compatibility file-dialog test double',
        filters: [{ name: 'Text', extensions: ['txt'] }],
      });
      const saveContent = '{"compatibility":"electron-43"}\\n';
      const savePath = await window.nlmytgen.saveIrPaste({
        defaultPath: 'electron-compatibility.json',
        content: saveContent,
      });
      const python = await window.nlmytgen.diagnoseScript({
        input: ${JSON.stringify(fixturePath)},
      });
      return {
        document_ready_state: document.readyState,
        title: document.title,
        body_text_length: (document.body?.innerText || '').length,
        button_count: document.querySelectorAll('button').length,
        bridge_keys: bridgeKeys,
        required_bridge_methods: ${JSON.stringify(REQUIRED_BRIDGE_METHODS)},
        missing_bridge_methods: ${JSON.stringify(REQUIRED_BRIDGE_METHODS)}.filter(
          (name) => typeof window.nlmytgen?.[name] !== 'function'
        ),
        dialog: {
          open_path: dialogPath,
          save_path: savePath,
          save_content: saveContent,
        },
        python: {
          code: python.code,
          stderr: python.stderr,
          has_json: Boolean(python.json),
          utterance_count: python.json?.meta?.utterance_count ?? null,
        },
        main_message: window.__nlmytgenCompatibilityMainMessage,
      };
    })()
  `), 15000, 'renderer/preload/IPC/Python compatibility probe');

  const png = (await win.webContents.capturePage()).toPNG();
  const capturePath = path.join(path.dirname(receiptPath()), 'actual_gui.png');
  fs.writeFileSync(capturePath, png);

  const consoleErrors = observations.console_messages.filter((entry) => {
    const level = String(entry.level || '').toLowerCase();
    return level === 'error' || Number(entry.level) >= 3;
  });
  const securityWarnings = observations.console_messages.filter((entry) => (
    /security warning|insecure|contextisolation|nodeintegration/i.test(entry.message)
  ));
  const saveResult = fs.readFileSync(renderer.dialog.save_path, 'utf8');
  const openRequest = dialogRequests.find((request) => request.kind === 'open');
  const saveRequest = dialogRequests.find((request) => request.kind === 'save');

  const checks = {
    electron_version_43_2_0: process.versions.electron === '43.2.0',
    registration_completed: registration === 'registered',
    renderer_document_complete: renderer.document_ready_state === 'complete',
    renderer_content_present: renderer.body_text_length > 1000 && renderer.button_count > 0,
    preload_bridge_complete: renderer.missing_bridge_methods.length === 0,
    main_to_renderer_message_received: renderer.main_message?.token === token,
    open_dialog_request_shape_valid: (
      openRequest?.options?.properties?.includes('openFile')
      && openRequest.options.filters?.[0]?.extensions?.includes('txt')
      && renderer.dialog.open_path === fixturePath
    ),
    save_dialog_request_shape_valid: (
      saveRequest?.options?.filters?.[0]?.extensions?.includes('json')
      && path.isAbsolute(renderer.dialog.save_path)
      && saveResult === renderer.dialog.save_content
    ),
    python_bridge_completed: (
      renderer.python.code === 0
      && renderer.python.has_json
      && renderer.python.utterance_count === 3
    ),
    context_isolation_enabled: win.webContents.getLastWebPreferences().contextIsolation === true,
    node_integration_disabled: win.webContents.getLastWebPreferences().nodeIntegration === false,
    sandbox_enabled: win.webContents.getLastWebPreferences().sandbox === true,
    audio_policy_silent: process.env.NLMYTGEN_AUDIO_POLICY === 'silent',
    mute_audio_switch_enabled: app.commandLine.hasSwitch('mute-audio'),
    no_console_errors: consoleErrors.length === 0,
    no_security_warnings: securityWarnings.length === 0,
    no_load_failures: observations.did_fail_load.length === 0,
    no_renderer_crash: observations.render_process_gone.length === 0,
    no_preload_errors: observations.preload_errors.length === 0,
    no_unhandled_renderer_errors: observations.renderer_unhandled_errors.length === 0,
  };
  const status = Object.values(checks).every(Boolean) ? 'passed' : 'failed';
  const receipt = {
    status,
    scope: 'actual NLMYTGen main window + renderer + production preload/IPC + Python bridge',
    runtime: {
      electron: process.versions.electron,
      chrome: process.versions.chrome,
      node: process.versions.node,
      profile_path: profilePath(),
      audio_policy: process.env.NLMYTGEN_AUDIO_POLICY,
      background_networking_disabled: app.commandLine.hasSwitch('disable-background-networking'),
      integration_timeout_ms: 15000,
    },
    checks,
    renderer,
    observations,
    dialog_requests: dialogRequests,
    capture: {
      path: capturePath,
      bytes: png.length,
      sha256: crypto.createHash('sha256').update(png).digest('hex'),
    },
  };
  writeReceipt(receipt);
  observations.dispose();
  win.close();
  app.exit(status === 'passed' ? 0 : 1);
}

function fail(err) {
  const error = err && (err.stack || err.message || String(err));
  writeReceipt({
    status: 'failed',
    scope: 'actual NLMYTGen main window + renderer + production preload/IPC + Python bridge',
    error,
    runtime: {
      electron: process.versions.electron,
      chrome: process.versions.chrome,
      node: process.versions.node,
    },
  });
  process.exitCode = 1;
}

module.exports = {
  dialogFixturePath,
  fail,
  isEnabled,
  openDialogResult,
  observe,
  profilePath,
  run,
  saveDialogResult,
};

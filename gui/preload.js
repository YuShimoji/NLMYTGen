const { contextBridge, ipcRenderer, webUtils } = require('electron');

contextBridge.exposeInMainWorld('nlmytgen', {
  runtimeMode: {
    electronCompatibility: process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE === '1',
    standardLoopProbe: process.env.NLMYTGEN_STANDARD_LOOP_PROBE === '1',
  },
  /** Electron 32+ ではレンダラの File に path が無い。DnD / file input 共通で実パスを得る */
  getPathForFile: (file) => {
    try {
      return webUtils.getPathForFile(file);
    } catch {
      return '';
    }
  },
  buildCsv: (opts) => ipcRenderer.invoke('build-csv', opts),
  applyProduction: (opts) => ipcRenderer.invoke('apply-production', opts),
  validateIr: (opts) => ipcRenderer.invoke('validate-ir', opts),
  buildCuePacketBundle: (opts) => ipcRenderer.invoke('build-cue-packet-bundle', opts),
  buildDiagramPacketBundle: (opts) => ipcRenderer.invoke('build-diagram-packet-bundle', opts),
  emitPackagingBriefTemplate: (opts) => ipcRenderer.invoke('emit-packaging-brief-template', opts),
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  describeEpisodePack: (rootPath) => ipcRenderer.invoke('describe-episode-pack', rootPath),
  selectEpisodePack: () => ipcRenderer.invoke('select-episode-pack'),
  saveJsonArtifact: (opts) => ipcRenderer.invoke('save-json-artifact', opts),
  scoreEvidence: (opts) => ipcRenderer.invoke('score-evidence', opts),
  scoreVisualDensity: (opts) => ipcRenderer.invoke('score-visual-density', opts),
  diagnoseScript: (opts) => ipcRenderer.invoke('diagnose-script', opts),
  saveScriptDiagnostics: (opts) => ipcRenderer.invoke('save-script-diagnostics', opts),
  loadReviewPacket: (packetPath) => ipcRenderer.invoke('load-review-packet', packetPath),
  loadReviewProof: (proofPath) => ipcRenderer.invoke('load-review-proof', proofPath),
  checkReviewArtifacts: (artifactPaths) => ipcRenderer.invoke('check-review-artifacts', artifactPaths),
  saveReviewDecisions: (opts) => ipcRenderer.invoke('save-review-decisions', opts),
  selectFile: (opts) => ipcRenderer.invoke('select-file', opts),
  openFolder: (path) => ipcRenderer.invoke('open-folder', path),
  openRepoDoc: (relPath) => ipcRenderer.invoke('open-repo-doc', relPath),
  saveIrPaste: (opts) => ipcRenderer.invoke('save-ir-paste', opts),
  loadSettings: () => ipcRenderer.invoke('load-settings'),
  saveSettings: (s) => ipcRenderer.invoke('save-settings', s),
  standardLoopAcceptedManifest: () => ipcRenderer.invoke('standard-loop-accepted-manifest'),
  standardLoopSelectManifest: () => ipcRenderer.invoke('standard-loop-select-manifest'),
  standardLoopLoadManifest: (relPath) => ipcRenderer.invoke('standard-loop-load-manifest', relPath),
  standardLoopDoctor: () => ipcRenderer.invoke('standard-loop-doctor'),
  standardLoopDryRun: (relPath) => ipcRenderer.invoke('standard-loop-dry-run', relPath),
  standardLoopStart: (opts) => ipcRenderer.invoke('standard-loop-start', opts),
  standardLoopCancel: (jobId) => ipcRenderer.invoke('standard-loop-cancel', jobId),
  standardLoopJob: () => ipcRenderer.invoke('standard-loop-job'),
  standardLoopOpenOutput: (relPath) => ipcRenderer.invoke('standard-loop-open-output', relPath),
  onStandardLoopJobEvent: (callback) => {
    const listener = (_event, payload) => callback(payload);
    ipcRenderer.on('standard-loop-job-event', listener);
    return () => ipcRenderer.removeListener('standard-loop-job-event', listener);
  },
});

if (
  process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE === '1'
  || process.env.NLMYTGEN_STANDARD_LOOP_PROBE === '1'
) {
  window.addEventListener('error', (event) => {
    ipcRenderer.send(
      process.env.NLMYTGEN_STANDARD_LOOP_PROBE === '1'
        ? 'nlmytgen-standard-loop-renderer-error'
        : 'nlmytgen-electron-compatibility-renderer-error',
      {
      kind: 'error',
      message: String(event.error?.stack || event.message || 'renderer error'),
      },
    );
  });
  window.addEventListener('unhandledrejection', (event) => {
    ipcRenderer.send(
      process.env.NLMYTGEN_STANDARD_LOOP_PROBE === '1'
        ? 'nlmytgen-standard-loop-renderer-error'
        : 'nlmytgen-electron-compatibility-renderer-error',
      {
      kind: 'unhandledrejection',
      message: String(event.reason?.stack || event.reason || 'unhandled rejection'),
      },
    );
  });
}

if (process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE === '1') {
  contextBridge.exposeInMainWorld('__nlmytgenCompatibility', {
    onMainMessage: (callback) => {
      ipcRenderer.once('nlmytgen-electron-compatibility-main-message', (_event, payload) => {
        callback(payload);
      });
    },
  });
}

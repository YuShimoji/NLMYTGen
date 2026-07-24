const { contextBridge, ipcRenderer, webUtils } = require('electron');

contextBridge.exposeInMainWorld('nlmytgen', {
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
});

if (process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE === '1') {
  window.addEventListener('error', (event) => {
    ipcRenderer.send('nlmytgen-electron-compatibility-renderer-error', {
      kind: 'error',
      message: String(event.error?.stack || event.message || 'renderer error'),
    });
  });
  window.addEventListener('unhandledrejection', (event) => {
    ipcRenderer.send('nlmytgen-electron-compatibility-renderer-error', {
      kind: 'unhandledrejection',
      message: String(event.reason?.stack || event.reason || 'unhandled rejection'),
    });
  });
  contextBridge.exposeInMainWorld('__nlmytgenCompatibility', {
    onMainMessage: (callback) => {
      ipcRenderer.once('nlmytgen-electron-compatibility-main-message', (_event, payload) => {
        callback(payload);
      });
    },
  });
}

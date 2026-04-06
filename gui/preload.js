const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('nlmytgen', {
  buildCsv: (opts) => ipcRenderer.invoke('build-csv', opts),
  applyProduction: (opts) => ipcRenderer.invoke('apply-production', opts),
  validateIr: (opts) => ipcRenderer.invoke('validate-ir', opts),
  buildCuePacketBundle: (opts) => ipcRenderer.invoke('build-cue-packet-bundle', opts),
  buildDiagramPacketBundle: (opts) => ipcRenderer.invoke('build-diagram-packet-bundle', opts),
  emitPackagingBriefTemplate: (opts) => ipcRenderer.invoke('emit-packaging-brief-template', opts),
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  scoreEvidence: (opts) => ipcRenderer.invoke('score-evidence', opts),
  scoreVisualDensity: (opts) => ipcRenderer.invoke('score-visual-density', opts),
  selectFile: (opts) => ipcRenderer.invoke('select-file', opts),
  openFolder: (path) => ipcRenderer.invoke('open-folder', path),
  openRepoDoc: (relPath) => ipcRenderer.invoke('open-repo-doc', relPath),
  saveIrPaste: (opts) => ipcRenderer.invoke('save-ir-paste', opts),
  loadSettings: () => ipcRenderer.invoke('load-settings'),
  saveSettings: (s) => ipcRenderer.invoke('save-settings', s),
});

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('nlmytgen', {
  buildCsv: (opts) => ipcRenderer.invoke('build-csv', opts),
  applyProduction: (opts) => ipcRenderer.invoke('apply-production', opts),
  validateIr: (opts) => ipcRenderer.invoke('validate-ir', opts),
  selectFile: (opts) => ipcRenderer.invoke('select-file', opts),
  openFolder: (path) => ipcRenderer.invoke('open-folder', path),
  saveIrPaste: (opts) => ipcRenderer.invoke('save-ir-paste', opts),
  loadSettings: () => ipcRenderer.invoke('load-settings'),
  saveSettings: (s) => ipcRenderer.invoke('save-settings', s),
});

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('nlmytgen', {
  buildCsv: (opts) => ipcRenderer.invoke('build-csv', opts),
  applyProduction: (opts) => ipcRenderer.invoke('apply-production', opts),
  selectFile: (opts) => ipcRenderer.invoke('select-file', opts),
});

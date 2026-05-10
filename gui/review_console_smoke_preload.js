const { contextBridge } = require('electron');
const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
let lastReviewDecisionSave = null;

function readRepoJson(repoPath) {
  const fullPath = path.resolve(repoRoot, repoPath);
  const rel = path.relative(repoRoot, fullPath);
  if (rel.startsWith('..') || path.isAbsolute(rel)) {
    return { ok: false, error: 'path outside repo' };
  }
  return {
    ok: true,
    path: rel.replace(/\\/g, '/'),
    payload: JSON.parse(fs.readFileSync(fullPath, 'utf8')),
  };
}

const ok = async () => ({ ok: true });
const nullPath = async () => null;

contextBridge.exposeInMainWorld('nlmytgen', {
  getPathForFile: () => '',
  loadReviewPacket: async (packetPath) => readRepoJson(packetPath),
  loadReviewProof: async (proofPath) => readRepoJson(proofPath),
  saveReviewDecisions: async (opts) => {
    lastReviewDecisionSave = opts;
    return { ok: true, path: opts?.decisionPath || 'smoke.json' };
  },
  getLastReviewDecisionSave: async () => lastReviewDecisionSave,
  openRepoDoc: ok,
  openFolder: ok,
  loadSettings: async () => ({}),
  saveSettings: ok,
  selectFile: nullPath,
  selectFolder: nullPath,
  selectEpisodePack: nullPath,
  buildCsv: ok,
  applyProduction: ok,
  validateIr: ok,
  buildCuePacketBundle: ok,
  buildDiagramPacketBundle: ok,
  emitPackagingBriefTemplate: ok,
  describeEpisodePack: ok,
  saveJsonArtifact: ok,
  scoreEvidence: ok,
  scoreVisualDensity: ok,
  diagnoseScript: ok,
  saveScriptDiagnostics: ok,
  saveIrPaste: ok,
});

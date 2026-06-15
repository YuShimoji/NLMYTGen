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

function checkRepoArtifacts(repoPaths) {
  const artifacts = (Array.isArray(repoPaths) ? repoPaths : []).map((repoPath) => {
    const fullPath = path.resolve(repoRoot, repoPath);
    const rel = path.relative(repoRoot, fullPath);
    if (rel.startsWith('..') || path.isAbsolute(rel)) {
      return { ok: false, exists: false, path: repoPath, error: 'path outside repo' };
    }
    return {
      ok: true,
      exists: fs.existsSync(fullPath),
      path: rel.replace(/\\/g, '/'),
    };
  });
  return {
    ok: artifacts.every((artifact) => artifact.ok),
    artifacts,
    missing_count: artifacts.filter((artifact) => artifact.ok && !artifact.exists).length,
    blocked_count: artifacts.filter((artifact) => !artifact.ok).length,
  };
}

const ok = async () => ({ ok: true });
const nullPath = async () => null;

contextBridge.exposeInMainWorld('nlmytgen', {
  getPathForFile: () => '',
  loadReviewPacket: async (packetPath) => readRepoJson(packetPath),
  loadReviewProof: async (proofPath) => readRepoJson(proofPath),
  checkReviewArtifacts: async (artifactPaths) => checkRepoArtifacts(artifactPaths),
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

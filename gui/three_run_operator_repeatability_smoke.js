const fs = require('fs');
const path = require('path');
const { app } = require('electron');
const { validateRunId } = require('./standard_production_loop');

const requested = validateRunId(process.env.NLMYTGEN_REPEATABILITY_RUN_ID);
if (!requested.ok) {
  throw new Error(`NLMYTGEN_REPEATABILITY_RUN_ID: ${requested.error}`);
}
const requestedProbe = validateRunId(
  process.env.NLMYTGEN_REPEATABILITY_PROBE_ID || `${requested.runId}_gui_probe`,
);
if (!requestedProbe.ok) {
  throw new Error(`NLMYTGEN_REPEATABILITY_PROBE_ID: ${requestedProbe.error}`);
}

const repoRoot = path.resolve(__dirname, '..');
const packageRoot = path.join(
  repoRoot,
  'production_pilots',
  'factory_canaries',
  'real_estate_reins_transparency_001',
);
const probeRoot = path.join(
  packageRoot,
  'auto_video_runs',
  requestedProbe.runId,
);
if (fs.existsSync(probeRoot)) {
  throw new Error(`repeatability probe output already exists: ${requestedProbe.runId}`);
}

process.env.NLMYTGEN_STANDARD_LOOP_PROBE = '1';
process.env.NLMYTGEN_STANDARD_LOOP_REAL_RENDER = '1';
process.env.NLMYTGEN_STANDARD_LOOP_REQUIRE_ALL_READY = '1';
process.env.NLMYTGEN_STANDARD_LOOP_RUN_ID = requested.runId;
process.env.NLMYTGEN_STANDARD_LOOP_MANIFEST = [
  'production_pilots',
  'factory_canaries',
  'real_estate_reins_transparency_001',
  'auto_video_pipeline',
  'real_estate_reins_episode_manifest.json',
].join('/');
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_STANDARD_LOOP_WIDTH = '1280';
process.env.NLMYTGEN_STANDARD_LOOP_HEIGHT = '720';
process.env.NLMYTGEN_STANDARD_LOOP_PROFILE = path.join(probeRoot, 'profile');
process.env.NLMYTGEN_STANDARD_LOOP_RECEIPT = path.join(probeRoot, 'receipt.json');

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

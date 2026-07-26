const fs = require('fs');
const path = require('path');
const { app } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const packageRoot = path.join(
  repoRoot,
  'production_pilots',
  'factory_canaries',
  'ai_monitoring_labor_001',
);
const probeRoot = path.join(
  packageRoot,
  'auto_video_runs',
  'ai_monitoring_labor_internal_review_v1_gui_probe',
);
if (fs.existsSync(probeRoot)) {
  throw new Error('third-topic GUI probe output already exists');
}

process.env.NLMYTGEN_STANDARD_LOOP_PROBE = '1';
process.env.NLMYTGEN_STANDARD_LOOP_REAL_RENDER = '1';
process.env.NLMYTGEN_STANDARD_LOOP_REQUIRE_ALL_READY = '1';
process.env.NLMYTGEN_STANDARD_LOOP_RUN_ID = 'ai_monitoring_labor_internal_review_v1';
process.env.NLMYTGEN_STANDARD_LOOP_MANIFEST = [
  'production_pilots',
  'factory_canaries',
  'ai_monitoring_labor_001',
  'auto_video_pipeline',
  'ai_monitoring_labor_episode_manifest.json',
].join('/');
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_STANDARD_LOOP_WIDTH = '1280';
process.env.NLMYTGEN_STANDARD_LOOP_HEIGHT = '720';
process.env.NLMYTGEN_STANDARD_LOOP_PROFILE = path.join(probeRoot, 'profile');
process.env.NLMYTGEN_STANDARD_LOOP_RECEIPT = path.join(probeRoot, 'receipt.json');

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

const path = require('path');
const { app } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const runRoot = path.join(repoRoot, '_tmp', 'electron_compatibility_smoke', String(process.pid));

process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_SMOKE = '1';
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_PROFILE = path.join(runRoot, 'profile');
process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_RECEIPT = path.join(runRoot, 'receipt.json');
process.env.NLMYTGEN_ELECTRON_COMPATIBILITY_DIALOG_PATH = path.join(
  repoRoot,
  'samples',
  '_probe',
  'pipeline_smoke',
  'real_estate_dx_baseline',
  'source_script.txt',
);

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

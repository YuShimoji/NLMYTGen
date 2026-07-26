const path = require('path');
const { app } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const runRoot = path.join(repoRoot, '_tmp', 'batch_observability_smoke', String(process.pid));

process.env.NLMYTGEN_BATCH_OBSERVABILITY_PROBE = '1';
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_BATCH_OBSERVABILITY_WIDTH = '1280';
process.env.NLMYTGEN_BATCH_OBSERVABILITY_HEIGHT = '720';
process.env.NLMYTGEN_BATCH_OBSERVABILITY_PROFILE = path.join(runRoot, 'profile');
process.env.NLMYTGEN_BATCH_OBSERVABILITY_RECEIPT = path.join(runRoot, 'receipt.json');

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

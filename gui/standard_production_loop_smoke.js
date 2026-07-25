const path = require('path');
const { app } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const runRoot = path.join(repoRoot, '_tmp', 'standard_production_loop_smoke', String(process.pid));

process.env.NLMYTGEN_STANDARD_LOOP_PROBE = '1';
process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE = '1';
process.env.NLMYTGEN_STANDARD_LOOP_TEST_DOUBLE_DELAY_MS = '500';
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_STANDARD_LOOP_WIDTH = '1280';
process.env.NLMYTGEN_STANDARD_LOOP_HEIGHT = '720';
process.env.NLMYTGEN_STANDARD_LOOP_PROFILE = path.join(runRoot, 'profile');
process.env.NLMYTGEN_STANDARD_LOOP_RECEIPT = path.join(runRoot, 'receipt.json');

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

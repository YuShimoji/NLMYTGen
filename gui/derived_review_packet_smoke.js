const path = require('path');
const { app } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const runRoot = path.join(
  repoRoot,
  '_tmp',
  'derived_review_packet_smoke',
  String(process.pid),
);

if (!process.env.NLMYTGEN_BATCH_DEFAULT_AUTHORITY_PATH) {
  throw new Error('NLMYTGEN_BATCH_DEFAULT_AUTHORITY_PATH is required');
}
process.env.NLMYTGEN_BATCH_OBSERVABILITY_PROBE = '1';
process.env.NLMYTGEN_BATCH_DERIVED_REVIEW_PROBE = '1';
process.env.NLMYTGEN_AUDIO_POLICY = 'silent';
process.env.NLMYTGEN_BATCH_DEFAULT_QUEUE_PATH = (
  'production_pilots/factory_queues/four_package_lifecycle_queue_v3.json'
);
process.env.NLMYTGEN_BATCH_DEFAULT_CHANGE_SET_PATH = (
  'production_pilots/factory_queues/'
  + 'food_expiry_cue002_review_packet_change_set_v1.json'
);
process.env.NLMYTGEN_BATCH_OBSERVABILITY_WIDTH = '1280';
process.env.NLMYTGEN_BATCH_OBSERVABILITY_HEIGHT = '720';
process.env.NLMYTGEN_BATCH_OBSERVABILITY_PROFILE = (
  process.env.NLMYTGEN_BATCH_DERIVED_REVIEW_PROFILE
  || path.join(runRoot, 'profile')
);
process.env.NLMYTGEN_BATCH_OBSERVABILITY_RECEIPT = (
  process.env.NLMYTGEN_BATCH_DERIVED_REVIEW_RECEIPT
  || path.join(runRoot, 'receipt.json')
);

app.commandLine.appendSwitch('mute-audio');
app.commandLine.appendSwitch('disable-background-networking');

require('./main');

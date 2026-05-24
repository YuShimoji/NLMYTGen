const fs = require('fs');

const packetPath = process.argv[2] || 'samples/_probe/g24/real_estate_dx_review_packet.json';
const packet = JSON.parse(fs.readFileSync(packetPath, 'utf8'));

const japanesePattern = /[\u3040-\u30ff\u3400-\u9fff]/g;
const badTextPattern = /\?\?\?|�/;

function fail(message) {
  throw new Error(message);
}

function getPath(root, path) {
  return path.reduce((value, key) => value?.[key], root);
}

function japaneseCount(value) {
  return (String(value).match(japanesePattern) || []).length;
}

function assertJapaneseField(path, { minJapanese = 4 } = {}) {
  const value = getPath(packet, path);
  const label = path.join('.');
  if (typeof value !== 'string' || !value.trim()) fail(`${label} is missing or not a string`);
  if (badTextPattern.test(value)) fail(`${label} contains corrupted text marker`);
  if (japaneseCount(value) < minJapanese) {
    fail(`${label} has too few Japanese characters: ${japaneseCount(value)}`);
  }
}

function assertNumberField(path) {
  const value = getPath(packet, path);
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    fail(`${path.join('.')} is missing or not a finite number`);
  }
}

for (const key of [
  'version',
  'episode_id',
  'review_scope',
  'default_decision_path',
  'episode_context',
  'story_outline',
  'source_refs',
  'gates',
  'overall_actions',
  'segments',
]) {
  if (!(key in packet)) fail(`missing top-level key: ${key}`);
}

if (packet.version !== '1.1') fail(`expected packet version 1.1, got ${packet.version}`);

for (const key of [
  'title',
  'thesis_ja',
  'audience_ja',
  'ending_question_ja',
  'review_scope_note',
]) {
  assertJapaneseField(['episode_context', key]);
}

if (typeof packet.episode_context.source_script !== 'string') fail('episode_context.source_script is missing');
assertNumberField(['episode_context', 'script_line_count']);
assertNumberField(['episode_context', 'duration_sec']);

if (!Array.isArray(packet.story_outline) || packet.story_outline.length !== 11) {
  fail('story_outline must contain 11 entries');
}

packet.story_outline.forEach((entry, index) => {
  for (const key of ['id', 'title', 'role_ja', 'summary_ja']) {
    if (typeof entry[key] !== 'string' || !entry[key].trim()) {
      fail(`story_outline[${index}].${key} is missing`);
    }
  }
  assertJapaneseField(['story_outline', index, 'role_ja']);
  assertJapaneseField(['story_outline', index, 'summary_ja']);
  for (const key of ['line_start', 'line_end', 'time_start_sec', 'time_end_sec']) {
    if (typeof entry[key] !== 'number' || !Number.isFinite(entry[key])) {
      fail(`story_outline[${index}].${key} is missing or not numeric`);
    }
  }
});

if (!Array.isArray(packet.segments) || packet.segments.length !== 11) {
  fail('segments must contain 11 entries');
}

packet.segments.forEach((segment, index) => {
  for (const key of [
    'id',
    'title',
    'summary_ja',
    'scene_role_ja',
    'script_span',
    'script_excerpt_ja',
    'previous_context_ja',
    'next_context_ja',
    'decision_prompt',
    'risk',
    'options',
    'next_effect',
  ]) {
    if (!(key in segment)) fail(`segments[${index}] missing ${key}`);
  }
  for (const key of [
    'summary_ja',
    'scene_role_ja',
    'previous_context_ja',
    'next_context_ja',
    'decision_prompt',
    'next_effect',
    'script_excerpt_ja',
  ]) {
    const minJapanese = key === 'script_excerpt_ja' ? 20 : 4;
    const value = segment[key];
    const label = `segments[${index}].${key}`;
    if (typeof value !== 'string' || !value.trim()) fail(`${label} is missing or not a string`);
    if (badTextPattern.test(value)) fail(`${label} contains corrupted text marker`);
    if (japaneseCount(value) < minJapanese) {
      fail(`${label} has too few Japanese characters: ${japaneseCount(value)}`);
    }
  }
  if (!segment.script_excerpt_ja.includes(`${segment.script_span.line_start}:`)) {
    fail(`segments[${index}].script_excerpt_ja does not include the start line prefix`);
  }
  if (!Array.isArray(segment.options) || !segment.options.length) {
    fail(`segments[${index}].options is empty`);
  }
});

console.log(`G-27 review packet contract OK: ${packetPath}`);

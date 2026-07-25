const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const {
  MAX_LOG_LINES,
  PipelineJobController,
  buildDoctorArgs,
  buildEpisodeArgs,
  classifyProfiles,
  resolveRepoRelativePath,
  sanitizeText,
  summarizeManifest,
  validateRunId,
} = require('./standard_production_loop');

function digest(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function write(root, relative, value) {
  const target = path.join(root, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, value);
  return target;
}

test('command builders keep the read-only doctor and never add force', () => {
  assert.deepEqual(
    buildDoctorArgs(),
    ['doctor-runtime', '--profile', 'all', '--deep', '--format', 'json'],
  );
  assert.deepEqual(
    buildEpisodeArgs('episode.json', { render: true, resume: true }),
    ['build-episode-video', '--episode', 'episode.json', '--render', '--resume'],
  );
  assert.deepEqual(
    buildEpisodeArgs('episode.json', { dryRun: true }),
    ['build-episode-video', '--episode', 'episode.json', '--dry-run'],
  );
  assert.equal(buildEpisodeArgs('episode.json', { render: true }).includes('--force'), false);
  assert.deepEqual(
    buildEpisodeArgs('episode.json', {
      render: true,
      runId: 'real_estate_reins_repeatability_01',
    }),
    [
      'build-episode-video',
      '--episode',
      'episode.json',
      '--run-id',
      'real_estate_reins_repeatability_01',
      '--render',
    ],
  );
});

test('run ID validation rejects traversal, absolute, reserved, empty, and unsafe values', () => {
  for (const value of ['', '..', '../escape', 'C:\\escape', '\\\\server\\share', 'CON', 'LPT1.txt']) {
    assert.equal(validateRunId(value).ok, false, value);
  }
  assert.deepEqual(
    validateRunId('real_estate_reins_repeatability_03'),
    { ok: true, runId: 'real_estate_reins_repeatability_03' },
  );
  assert.throws(
    () => buildEpisodeArgs('episode.json', { runId: '../escape' }),
    /safe directory name/,
  );
});

test('repo path resolver rejects absolute paths and traversal', () => {
  const root = path.resolve('fixture-root');
  assert.equal(resolveRepoRelativePath(root, '../outside.json').ok, false);
  assert.equal(resolveRepoRelativePath(root, 'C:\\outside.json').ok, false);
  assert.deepEqual(resolveRepoRelativePath(root, 'inside/episode.json'), {
    ok: true,
    full: path.join(root, 'inside', 'episode.json'),
    rel: 'inside/episode.json',
  });
});

test('manifest summary distinguishes exact protected inputs and accepted output', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nlmytgen-standard-loop-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const lockedValue = Buffer.from('locked');
  const sourceValue = Buffer.from('source-project');
  const projectValue = Buffer.from('generated-project');
  const mediaValue = Buffer.from('internal-review-media');
  write(root, 'inputs/locked.json', lockedValue);
  write(root, 'private/source.ymmp', sourceValue);
  write(root, 'runs/run-1/generated.ymmp', projectValue);
  write(root, 'runs/run-1/review.mp4', mediaValue);
  write(root, 'runs/run-1/pipeline_run_receipt.json', JSON.stringify({ status: 'passed' }));
  write(root, 'manifests/human_real_media_cut_acceptance_receipt.json', JSON.stringify({
    status: 'stable_internal_cut',
    reviewed_artifact: {
      run_id: 'run-1',
      filename: 'review.mp4',
      sha256: digest(mediaValue),
      generated_project_sha256: digest(projectValue),
    },
  }));
  const manifest = {
    schema: 'nlmytgen.episode_manifest.v1',
    episode_id: 'fixture-episode',
    cue_mapping: [
      { cue_id: 'cue-1', scene_id: 'scene-1', speaker: 'speaker-a' },
      { cue_id: 'cue-2', scene_id: 'scene-2', speaker: 'speaker-b' },
    ],
    yymm4: {
      source_project_path: 'private/source.ymmp',
      source_project_sha256: digest(sourceValue),
    },
    output: {
      run_root_path: 'runs',
      run_id: 'run-1',
      project_filename: 'generated.ymmp',
      mp4_filename: 'review.mp4',
    },
    render_settings: {
      width: 1920,
      height: 1080,
      fps: 60,
      container: 'mp4',
      timeout_seconds: 1200,
    },
    boundaries: { internal_review_only: true },
    content_locks: [{ path: 'inputs/locked.json', sha256: digest(lockedValue) }],
  };
  write(root, 'manifests/episode.json', JSON.stringify(manifest));

  const summary = summarizeManifest(root, 'manifests/episode.json');
  assert.equal(summary.ok, true);
  assert.equal(summary.protected_inputs.status, 'exact');
  assert.equal(summary.protected_inputs.exact_count, 2);
  assert.equal(summary.output.status, 'accepted_exact');
  assert.equal(summary.episode.cue_count, 2);
  assert.equal(summary.episode.scene_count, 2);
  assert.equal(summary.episode.speaker_count, 2);
  assert.equal(summary.episode.render.timeout_seconds, 1200);
  assert.equal(path.isAbsolute(summary.output.media_path), false);

  const alternate = summarizeManifest(root, 'manifests/episode.json', 'repeatability-01');
  assert.equal(alternate.default_run_id, 'run-1');
  assert.equal(alternate.resolved_run_id, 'repeatability-01');
  assert.equal(alternate.output.status, 'absent');
  assert.equal(alternate.output.run_path, 'runs/repeatability-01');

  write(root, 'inputs/locked.json', 'changed');
  const mismatch = summarizeManifest(root, 'manifests/episode.json');
  assert.equal(mismatch.protected_inputs.status, 'blocked');
  assert.equal(mismatch.protected_inputs.counts.mismatch, 1);

  fs.rmSync(path.join(root, 'inputs', 'locked.json'));
  const missing = summarizeManifest(root, 'manifests/episode.json');
  assert.equal(missing.protected_inputs.counts.missing, 1);

  write(root, 'inputs/locked.json', lockedValue);
  write(root, 'runs/run-1/review.mp4', 'replacement');
  const stale = summarizeManifest(root, 'manifests/episode.json');
  assert.equal(stale.output.status, 'stale_or_mismatch');
});

test('profile classification preserves unavailable reasons', () => {
  const classified = classifyProfiles({
    profiles: {
      code: { ready: true, blocking_checks: [] },
      review: { ready: false, blocking_checks: ['private_artifacts'] },
    },
  });
  assert.deepEqual(classified.map((profile) => profile.state), [
    'ready',
    'unavailable',
    'not_evaluated',
    'not_evaluated',
  ]);
  assert.equal(classified[1].next_action, 'private_artifacts');
});

test('long Windows paths and Japanese errors are sanitized and bounded', () => {
  const message = `C:\\Users\\private-owner\\${'深いフォルダー\\'.repeat(500)}入力が見つかりません`;
  const sanitized = sanitizeText(message, 420);
  assert.equal(sanitized.includes('private-owner'), false);
  assert.equal(sanitized.includes('入力が見つかりません'), false);
  assert.equal(sanitized.length <= 426, true);
  assert.equal(sanitized.endsWith('…(省略)'), true);
});

test('job controller admits one job, bounds logs, and cancels only its owned process', async () => {
  let callbacks;
  const ownedProcess = { pid: 1234 };
  let cancelledProcess = null;
  const events = [];
  const controller = new PipelineJobController({
    startProcess: (_spec, receivedCallbacks) => {
      callbacks = receivedCallbacks;
      return ownedProcess;
    },
    cancelProcess: async (proc) => { cancelledProcess = proc; },
    emit: (type, payload) => events.push({ type, payload }),
    now: () => '2026-07-25T00:00:00.000Z',
  });
  const started = controller.start({ args: ['build-episode-video'] });
  assert.equal(started.ok, true);
  assert.equal(controller.start({ args: [] }).error, 'PIPELINE_JOB_ALREADY_ACTIVE');
  callbacks.stdout(Array.from({ length: MAX_LOG_LINES + 10 }, (_, index) => `line-${index}`).join('\n'));
  assert.equal(controller.snapshot().log_lines.length, MAX_LOG_LINES);
  const cancelled = await controller.cancel(started.job.id);
  assert.equal(cancelled.ok, true);
  assert.equal(cancelledProcess, ownedProcess);
  callbacks.close({ code: 1, cancelled: true });
  assert.equal(controller.snapshot().state, 'cancelled');
  assert.equal(events.some((event) => event.type === 'cancelling'), true);
  assert.equal(events.some((event) => event.type === 'finished'), true);
});

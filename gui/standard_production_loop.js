const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ACCEPTED_MANIFEST_RELATIVE_PATH = [
  'production_pilots',
  'yukkuri_newsroom_content_spine_002',
  'external_editorial_input',
  'new_banknote_security_notebooklm_001',
  'auto_video_pipeline',
  'new_banknote_real_media_episode_manifest.json',
].join('/');

const ACCEPTANCE_RECEIPT_FILENAME = 'human_real_media_cut_acceptance_receipt.json';
const PIPELINE_RECEIPT_FILENAME = 'pipeline_run_receipt.json';
const MAX_LOG_LINES = 240;
const RUN_ID_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/;
const WINDOWS_RESERVED_NAMES = new Set([
  'CON', 'PRN', 'AUX', 'NUL', 'CLOCK$',
  ...Array.from({ length: 9 }, (_, index) => `COM${index + 1}`),
  ...Array.from({ length: 9 }, (_, index) => `LPT${index + 1}`),
]);

function validateRunId(value) {
  const runId = String(value || '').trim();
  if (!runId) return { ok: false, error: 'run ID is required' };
  if (
    path.isAbsolute(runId)
    || /^[A-Za-z]:/.test(runId)
    || runId.startsWith('\\\\')
    || runId.includes('/')
    || runId.includes('\\')
    || runId === '.'
    || runId === '..'
  ) {
    return { ok: false, error: 'run ID must be one safe directory name' };
  }
  if (!RUN_ID_PATTERN.test(runId)) {
    return { ok: false, error: 'run ID contains unsafe characters or is too long' };
  }
  if (WINDOWS_RESERVED_NAMES.has(runId.split('.', 1)[0].toUpperCase())) {
    return { ok: false, error: 'run ID uses a reserved Windows name' };
  }
  return { ok: true, runId };
}

function resolveRepoRelativePath(repoRoot, relPath) {
  if (typeof relPath !== 'string' || !relPath.trim()) {
    return { ok: false, error: 'repo-relative path is required' };
  }
  if (path.isAbsolute(relPath) || /^[a-zA-Z]:/.test(relPath)) {
    return { ok: false, error: 'absolute or drive-qualified path is not allowed' };
  }
  const normalized = path.normalize(relPath.trim());
  if (normalized === '..' || normalized.startsWith(`..${path.sep}`)) {
    return { ok: false, error: 'path traversal is not allowed' };
  }
  const root = path.resolve(repoRoot);
  const full = path.resolve(root, normalized);
  const relative = path.relative(root, full);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    return { ok: false, error: 'path outside repo' };
  }
  return { ok: true, full, rel: relative.replace(/\\/g, '/') };
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function sha256(filePath) {
  const hash = crypto.createHash('sha256');
  hash.update(fs.readFileSync(filePath));
  return hash.digest('hex');
}

function inspectLockedFile(repoRoot, lock) {
  const resolved = resolveRepoRelativePath(repoRoot, lock?.path);
  if (!resolved.ok) {
    return { path: String(lock?.path || ''), status: 'invalid', error: resolved.error };
  }
  if (!fs.existsSync(resolved.full)) {
    return { path: resolved.rel, status: 'missing', expected_sha256: lock.sha256 };
  }
  const observed = sha256(resolved.full);
  return {
    path: resolved.rel,
    status: observed === lock.sha256 ? 'exact' : 'mismatch',
    expected_sha256: lock.sha256,
    observed_sha256: observed,
  };
}

function inspectSourceProject(repoRoot, yymm4) {
  const resolved = resolveRepoRelativePath(repoRoot, yymm4?.source_project_path);
  if (!resolved.ok) {
    return { path: String(yymm4?.source_project_path || ''), status: 'invalid', error: resolved.error };
  }
  if (!fs.existsSync(resolved.full)) {
    return {
      path: resolved.rel,
      status: 'missing',
      expected_sha256: yymm4.source_project_sha256,
    };
  }
  const observed = sha256(resolved.full);
  return {
    path: resolved.rel,
    status: observed === yymm4.source_project_sha256 ? 'exact' : 'mismatch',
    expected_sha256: yymm4.source_project_sha256,
    observed_sha256: observed,
  };
}

function inspectOutput(repoRoot, manifest, manifestPath) {
  const runRoot = resolveRepoRelativePath(repoRoot, manifest.output?.run_root_path || '');
  if (!runRoot.ok) {
    return { status: 'invalid', error: runRoot.error, run_root_path: '' };
  }
  const runId = manifest.output?.run_id || '';
  const runDir = resolveRepoRelativePath(repoRoot, `${runRoot.rel}/${runId}`);
  if (!runDir.ok) {
    return { status: 'invalid', error: runDir.error, run_root_path: runRoot.rel };
  }
  const projectPath = path.join(runDir.full, manifest.output?.project_filename || '');
  const mediaPath = path.join(runDir.full, manifest.output?.mp4_filename || '');
  const pipelineReceiptPath = path.join(runDir.full, PIPELINE_RECEIPT_FILENAME);
  const acceptancePath = path.join(path.dirname(manifestPath), ACCEPTANCE_RECEIPT_FILENAME);
  const output = {
    status: 'absent',
    run_id: runId,
    run_root_path: runRoot.rel,
    run_path: runDir.rel,
    project_path: path.relative(repoRoot, projectPath).replace(/\\/g, '/'),
    media_path: path.relative(repoRoot, mediaPath).replace(/\\/g, '/'),
    pipeline_receipt_path: path.relative(repoRoot, pipelineReceiptPath).replace(/\\/g, '/'),
    acceptance_receipt_path: path.relative(repoRoot, acceptancePath).replace(/\\/g, '/'),
    project_exists: fs.existsSync(projectPath),
    media_exists: fs.existsSync(mediaPath),
    pipeline_receipt_exists: fs.existsSync(pipelineReceiptPath),
    acceptance_receipt_exists: fs.existsSync(acceptancePath),
  };
  if (!output.project_exists && !output.media_exists && !output.pipeline_receipt_exists) return output;

  output.status = 'present_unverified';
  let pipeline = null;
  let acceptance = null;
  try {
    if (output.pipeline_receipt_exists) pipeline = readJson(pipelineReceiptPath);
  } catch (err) {
    output.pipeline_receipt_error = err.message;
  }
  try {
    if (output.acceptance_receipt_exists) acceptance = readJson(acceptancePath);
  } catch (err) {
    output.acceptance_receipt_error = err.message;
  }
  output.pipeline_status = pipeline?.status || null;
  output.acceptance_status = acceptance?.status || null;
  output.project_sha256 = output.project_exists ? sha256(projectPath) : null;
  output.media_sha256 = output.media_exists ? sha256(mediaPath) : null;
  const accepted = acceptance?.reviewed_artifact || {};
  const exactAcceptance = (
    output.project_exists
    && output.media_exists
    && accepted.run_id === runId
    && accepted.filename === path.basename(mediaPath)
    && accepted.sha256 === output.media_sha256
    && accepted.generated_project_sha256 === output.project_sha256
  );
  if (exactAcceptance) {
    output.status = 'accepted_exact';
  } else if (output.acceptance_receipt_exists) {
    output.status = 'stale_or_mismatch';
  } else if (pipeline?.status === 'passed') {
    output.status = 'generated_unaccepted';
  }
  return output;
}

function summarizeManifest(repoRoot, relPath, runIdOverride = null) {
  const resolved = resolveRepoRelativePath(repoRoot, relPath);
  if (!resolved.ok) return { ok: false, error: resolved.error };
  if (!fs.existsSync(resolved.full)) return { ok: false, error: `not found: ${resolved.rel}` };
  let manifest;
  try {
    manifest = readJson(resolved.full);
  } catch (err) {
    return { ok: false, error: `manifest JSON error: ${err.message}`, path: resolved.rel };
  }
  if (manifest.schema !== 'nlmytgen.episode_manifest.v1') {
    return { ok: false, error: `unsupported manifest schema: ${manifest.schema || 'missing'}`, path: resolved.rel };
  }
  const defaultRunId = manifest.output?.run_id || '';
  if (runIdOverride !== null && runIdOverride !== undefined) {
    const validated = validateRunId(runIdOverride);
    if (!validated.ok) return { ok: false, error: validated.error, path: resolved.rel };
    manifest = {
      ...manifest,
      output: {
        ...manifest.output,
        run_id: validated.runId,
      },
    };
  }

  const locks = (manifest.content_locks || []).map((lock) => inspectLockedFile(repoRoot, lock));
  const sourceProject = inspectSourceProject(repoRoot, manifest.yymm4 || {});
  const protectedInputs = [...locks, sourceProject];
  const counts = protectedInputs.reduce((acc, item) => {
    acc[item.status] = (acc[item.status] || 0) + 1;
    return acc;
  }, {});
  const speakers = [...new Set((manifest.cue_mapping || []).map((cue) => cue.speaker).filter(Boolean))];
  const scenes = [...new Set((manifest.cue_mapping || []).map((cue) => cue.scene_id).filter(Boolean))];
  const output = inspectOutput(repoRoot, manifest, resolved.full);
  return {
    ok: true,
    path: resolved.rel,
    manifest_sha256: sha256(resolved.full),
    default_run_id: defaultRunId,
    resolved_run_id: manifest.output.run_id,
    episode: {
      id: manifest.episode_id,
      cue_count: (manifest.cue_mapping || []).length,
      scene_count: scenes.length,
      speaker_count: speakers.length,
      speakers,
      render: {
        width: manifest.render_settings?.width,
        height: manifest.render_settings?.height,
        fps: manifest.render_settings?.fps,
        container: manifest.render_settings?.container,
        timeout_seconds: manifest.render_settings?.timeout_seconds,
      },
      internal_review_only: manifest.boundaries?.internal_review_only === true,
    },
    protected_inputs: {
      status: protectedInputs.every((item) => item.status === 'exact') ? 'exact' : 'blocked',
      exact_count: counts.exact || 0,
      total_count: protectedInputs.length,
      counts,
      items: protectedInputs,
    },
    output,
    boundaries: {
      internal_review_only: manifest.boundaries?.internal_review_only === true,
      rights_approved: manifest.boundaries?.rights_approved === true,
      production: manifest.boundaries?.production === true,
      publication: manifest.boundaries?.publication === true,
      external_upload: manifest.boundaries?.external_upload === true,
      speaker_playback: manifest.boundaries?.speaker_playback === true,
      preview_playback: manifest.boundaries?.preview_playback === true,
    },
  };
}

function buildDoctorArgs() {
  return ['doctor-runtime', '--profile', 'all', '--deep', '--format', 'json'];
}

function buildEpisodeArgs(
  relPath,
  {
    dryRun = false,
    render = false,
    resume = false,
    runId = null,
  } = {},
) {
  const args = ['build-episode-video', '--episode', relPath];
  if (runId !== null && runId !== undefined) {
    const validated = validateRunId(runId);
    if (!validated.ok) throw new Error(validated.error);
    args.push('--run-id', validated.runId);
  }
  if (dryRun) args.push('--dry-run');
  if (render) args.push('--render');
  if (resume) args.push('--resume');
  return args;
}

function classifyProfiles(result) {
  const profiles = result?.profiles || {};
  return ['code', 'review', 'render', 'regenerate'].map((name) => {
    const profile = profiles[name];
    if (!profile) {
      return { name, state: 'not_evaluated', blocking_checks: [], next_action: '実行環境を再確認' };
    }
    const blocking = Array.isArray(profile.blocking_checks) ? profile.blocking_checks : [];
    return {
      name,
      state: profile.ready ? 'ready' : 'unavailable',
      blocking_checks: blocking,
      next_action: profile.ready ? '次の工程へ進めます' : (blocking[0] || '環境要件を確認'),
    };
  });
}

function sanitizeText(value, maxLength = 8000) {
  const text = String(value || '')
    .replace(/[A-Za-z]:\\Users\\[^\\\s]+/g, '<user-home>')
    .replace(/\u001b\[[0-9;]*m/g, '');
  return text.length > maxLength ? `${text.slice(0, maxLength)}\n…(省略)` : text;
}

class PipelineJobController {
  constructor({ startProcess, cancelProcess, emit, now = () => new Date().toISOString() }) {
    this.startProcess = startProcess;
    this.cancelProcess = cancelProcess;
    this.emit = emit;
    this.now = now;
    this.active = null;
  }

  snapshot() {
    if (!this.active) return { state: 'idle', active: false };
    return {
      id: this.active.id,
      state: this.active.state,
      active: this.active.state === 'running' || this.active.state === 'cancelling',
      started_at: this.active.startedAt,
      log_lines: [...this.active.logLines],
    };
  }

  start(spec) {
    if (this.active && ['running', 'cancelling'].includes(this.active.state)) {
      return { ok: false, error: 'PIPELINE_JOB_ALREADY_ACTIVE', job: this.snapshot() };
    }
    const job = {
      id: `standard-loop-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      state: 'running',
      startedAt: this.now(),
      logLines: [],
      process: null,
    };
    this.active = job;
    const pushLog = (stream, chunk) => {
      const lines = sanitizeText(chunk, 12000).split(/\r?\n/).filter(Boolean);
      for (const line of lines) job.logLines.push(`[${stream}] ${line}`);
      if (job.logLines.length > MAX_LOG_LINES) {
        job.logLines.splice(0, job.logLines.length - MAX_LOG_LINES);
      }
      this.emit('log', { id: job.id, stream, lines });
    };
    try {
      job.process = this.startProcess(spec, {
        stdout: (chunk) => pushLog('stdout', chunk),
        stderr: (chunk) => pushLog('stderr', chunk),
        close: (result) => {
          job.state = result.cancelled || job.state === 'cancelling'
            ? 'cancelled'
            : (result.code === 0 ? 'completed' : 'failed');
          this.emit('finished', {
            id: job.id,
            state: job.state,
            code: result.code,
            log_lines: [...job.logLines],
          });
        },
      });
      this.emit('started', { id: job.id, started_at: job.startedAt });
      return { ok: true, job: this.snapshot() };
    } catch (err) {
      job.state = 'failed';
      pushLog('stderr', err.message);
      this.emit('finished', { id: job.id, state: job.state, code: -1, log_lines: [...job.logLines] });
      return { ok: false, error: err.message, job: this.snapshot() };
    }
  }

  async cancel(id) {
    if (!this.active || this.active.id !== id || this.active.state !== 'running') {
      return { ok: false, error: 'NO_MATCHING_ACTIVE_PIPELINE_JOB', job: this.snapshot() };
    }
    this.active.state = 'cancelling';
    this.emit('cancelling', { id });
    try {
      await this.cancelProcess(this.active.process);
      return { ok: true, job: this.snapshot() };
    } catch (err) {
      this.active.state = 'failed';
      this.emit('finished', { id, state: 'failed', code: -1, error: err.message });
      return { ok: false, error: err.message, job: this.snapshot() };
    }
  }
}

module.exports = {
  ACCEPTED_MANIFEST_RELATIVE_PATH,
  MAX_LOG_LINES,
  PipelineJobController,
  buildDoctorArgs,
  buildEpisodeArgs,
  classifyProfiles,
  resolveRepoRelativePath,
  sanitizeText,
  summarizeManifest,
  validateRunId,
};

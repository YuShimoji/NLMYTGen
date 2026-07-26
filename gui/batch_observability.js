const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const DEFAULT_QUEUE_PATH = 'production_pilots/factory_queues/four_package_lifecycle_queue_v3.json';
const DEFAULT_CHANGE_SET_PATH = 'production_pilots/factory_queues/four_package_zero_change_set_v1.json';
const MAX_BATCH_LOG_LINES = 240;

const EXECUTION_STATES = Object.freeze([
  'not_selected',
  'verified_noop',
  'planned',
  'authority_validated',
  'started',
  'succeeded',
  'failed',
  'effect_unknown',
  'skipped_after_failure',
]);

const STATE_PRESENTATION = Object.freeze({
  not_selected: { label: '対象外', tone: 'muted' },
  verified_noop: { label: '変更なし', tone: 'success' },
  planned: { label: '実行待ち', tone: 'pending' },
  authority_validated: { label: '権限確認済み', tone: 'pending' },
  started: { label: '実行中', tone: 'active' },
  succeeded: { label: '完了', tone: 'success' },
  failed: { label: '失敗', tone: 'error' },
  effect_unknown: { label: '作用結果不明', tone: 'blocked' },
  skipped_after_failure: { label: '先行失敗により未実行', tone: 'muted' },
});

const AUTHORITY_PRESENTATION = Object.freeze({
  not_required: { label: '権限不要', tone: 'muted' },
  required: { label: '権限が必要', tone: 'pending' },
  absent: { label: '権限ファイル未選択', tone: 'error' },
  invalid: { label: '権限不一致', tone: 'error' },
  available: { label: '権限使用可能', tone: 'success' },
  consumed: { label: '権限使用済み', tone: 'muted' },
  replacement_required: { label: '代替権限が必要', tone: 'error' },
  reconciliation_required: { label: '読み取り照合が必要', tone: 'blocked' },
});

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

function identitySha256(value) {
  return crypto
    .createHash('sha256')
    .update(JSON.stringify(canonicalize(value)))
    .digest('hex');
}

function fileSha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function sanitizeOperatorText(value, maxLength = 12000) {
  const text = String(value ?? '')
    .replace(/[A-Za-z]:\\Users\\[^\\\s]+/g, '<user-home>')
    .replace(/\u001b\[[0-9;]*m/g, '');
  const suffix = '\n…(省略)';
  return text.length <= maxLength
    ? text
    : `${text.slice(0, Math.max(0, maxLength - suffix.length))}${suffix}`;
}

function inferDescriptorLifecycle(descriptor) {
  const explicit = descriptor?.lifecycle?.state;
  if (typeof explicit === 'string' && explicit) return explicit;
  if (/^accepted/.test(descriptor?.human_decision?.state || '')) return 'human_accepted';
  if (descriptor?.render_validation?.technical_status === 'passed') return 'rendered';
  if (
    descriptor?.source_project?.state === 'ready'
    || typeof descriptor?.source_project?.sha256 === 'string'
  ) {
    return 'source_project_ready';
  }
  return 'package_prepared';
}

function latestEvent(entry) {
  const events = Array.isArray(entry?.events) ? entry.events : [];
  return events.length ? events[events.length - 1] : null;
}

function authorityStateForEntry(entry, authoritySummary = null) {
  const state = entry?.current_state;
  const event = latestEvent(entry);
  if (state === 'effect_unknown') return 'reconciliation_required';
  if (state === 'started') return 'reconciliation_required';
  if (state === 'failed') {
    return authoritySummary?.status === 'available' ? 'available' : 'replacement_required';
  }
  if (event?.authority_status === 'consumed') return 'consumed';
  if (!entry?.requested_operation) return 'not_required';
  if (!authoritySummary) return 'absent';
  if (authoritySummary.status === 'available') return 'available';
  if (authoritySummary.status === 'consumed') return 'consumed';
  return 'invalid';
}

function resumeEffectForEntry(entry) {
  const state = entry?.current_state;
  if (state === 'verified_noop' || state === 'succeeded' || state === 'not_selected') {
    return '再実行しない';
  }
  if (state === 'failed') return '代替権限で安全に再開可能';
  if (state === 'effect_unknown') return '自動再試行不可・読み取り照合';
  if (state === 'skipped_after_failure') return '先行失敗の解決後に続行';
  if (state === 'started') return '作用結果を照合するまで停止';
  return entry?.requested_operation ? '権限確認後に実行' : '対象外';
}

function conciseReason(entry) {
  const event = latestEvent(entry);
  if (event?.failure_code) return sanitizeOperatorText(event.failure_code, 240);
  const consumerLabels = {
    'completed package validated and excluded from backend dispatch':
      '完了済みのため backend dispatch から除外しました',
  };
  if (event?.consumer_effect) {
    return sanitizeOperatorText(
      consumerLabels[event.consumer_effect] || event.consumer_effect,
      240,
    );
  }
  const state = entry?.current_state;
  const defaults = {
    not_selected: 'change-set の対象外です',
    verified_noop: '完了済みのため backend dispatch から除外しました',
    planned: 'exact change-set により選択されています',
    authority_validated: 'one-shot authority が一致しています',
    started: 'project-owned executor process が実行中です',
    succeeded: 'backend effect と readback が完了しました',
    failed: 'effect 前または既知の失敗で停止しました',
    effect_unknown: 'effect の有無を自動判定できません',
    skipped_after_failure: '前の mutating entry が失敗しました',
  };
  return defaults[state] || state || '状態未確認';
}

function journalEventCount(journal) {
  return (journal?.entries || []).reduce(
    (total, entry) => total + (Array.isArray(entry.events) ? entry.events.length : 0),
    0,
  );
}

function journalPrefixIdentity(journal) {
  return identitySha256({
    schema: journal?.schema,
    plan_identity_sha256: journal?.plan_identity_sha256,
    queue_sha256: journal?.queue?.sha256,
    change_set_sha256: journal?.change_set?.sha256,
    entries: (journal?.entries || []).map((entry) => ({
      package_id: entry.package_id,
      descriptor_sha256: entry.descriptor_sha256,
      events: entry.events || [],
    })),
  });
}

function summarizeResume(journal) {
  const entries = journal?.entries || [];
  const effectUnknown = entries.find((entry) => (
    entry.current_state === 'effect_unknown' || entry.current_state === 'started'
  ));
  if (effectUnknown) {
    return {
      eligible: false,
      state: 'reconciliation_required',
      package_id: effectUnknown.package_id,
      message: '作用結果が不明です。自動再試行せず、読み取り照合を行ってください。',
    };
  }
  const failed = entries.find((entry) => entry.current_state === 'failed');
  if (failed) {
    return {
      eligible: true,
      state: 'replacement_authority_required',
      package_id: failed.package_id,
      message: '失敗した entry に新しい exact authority を指定すると続行できます。',
    };
  }
  const skipped = entries.find((entry) => entry.current_state === 'skipped_after_failure');
  if (skipped) {
    return {
      eligible: false,
      state: 'blocked_by_prior_failure',
      package_id: skipped.package_id,
      message: '先行失敗の解決後に同じ journal prefix から続行します。',
    };
  }
  const pending = entries.find((entry) => (
    entry.current_state === 'planned' || entry.current_state === 'authority_validated'
  ));
  if (pending) {
    return {
      eligible: true,
      state: 'continuation_available',
      package_id: pending.package_id,
      message: '同じ identity と journal prefix から続行できます。',
    };
  }
  return {
    eligible: false,
    state: 'nothing_to_resume',
    package_id: null,
    message: '再開が必要な entry はありません。',
  };
}

function normalizeExecutionResult(result, {
  descriptorLoader = null,
  authoritySummary = null,
  journalLocator = null,
} = {}) {
  if (!result || result.schema !== 'nlmytgen.factory_queue.execution_result.v1') {
    throw new Error('EXECUTION_RESULT_SCHEMA_INVALID');
  }
  const journal = result.journal;
  if (!journal || journal.schema !== 'nlmytgen.factory_queue.execution_journal.v1') {
    throw new Error('EXECUTION_JOURNAL_SCHEMA_INVALID');
  }
  const rows = (journal.entries || []).map((entry) => {
    let lifecycle = entry.from_lifecycle || null;
    if (!lifecycle && descriptorLoader) {
      lifecycle = inferDescriptorLifecycle(descriptorLoader(entry.descriptor_path));
    }
    const authorityState = authorityStateForEntry(entry, authoritySummary);
    const statePresentation = STATE_PRESENTATION[entry.current_state]
      || { label: entry.current_state, tone: 'muted' };
    const authorityPresentation = AUTHORITY_PRESENTATION[authorityState];
    return {
      order: entry.order,
      package_id: entry.package_id,
      descriptor_path: entry.descriptor_path,
      descriptor_sha256: entry.descriptor_sha256,
      current_lifecycle: lifecycle || 'unknown',
      technical_decision: entry.technical_decision,
      requested_operation: entry.requested_operation,
      requested_edge: entry.requested_operation
        ? `${entry.from_lifecycle} → ${entry.to_lifecycle}`
        : null,
      authority_state: authorityState,
      authority_label: authorityPresentation.label,
      authority_tone: authorityPresentation.tone,
      execution_state: entry.current_state,
      execution_label: statePresentation.label,
      execution_tone: statePresentation.tone,
      reason: conciseReason(entry),
      resume_effect: resumeEffectForEntry(entry),
    };
  });
  const resume = summarizeResume(journal);
  const eventCount = journalEventCount(journal);
  return {
    schema: 'nlmytgen.gui.factory_queue_batch_read_model.v1',
    status: result.status,
    execution_mode: journal.execution_mode,
    queue: { ...journal.queue },
    change_set: { ...journal.change_set },
    plan_identity_sha256: journal.plan_identity_sha256,
    counts: { ...journal.counts },
    mutating_entry_count: result.plan?.mutating_entry_count ?? 0,
    package_count: result.plan?.package_count ?? rows.length,
    rows,
    authority: {
      state: rows.some((row) => row.authority_state !== 'not_required')
        ? (authoritySummary?.status || 'absent')
        : 'not_required',
      mutating_entries: rows.filter((row) => Boolean(row.requested_operation)).length,
    },
    journal: {
      locator: journalLocator,
      identity_sha256: result.execution_receipt?.journal_sha256 || identitySha256(journal),
      prefix_identity_sha256: journalPrefixIdentity(journal),
      event_count: eventCount,
      append_only: journal.boundaries?.append_only_journal === true,
    },
    resume,
    boundaries: { ...(journal.boundaries || {}) },
    result_message: (
      (journal.counts?.verified_noop || 0) === rows.length
      && (result.plan?.mutating_entry_count || 0) === 0
    ) ? '変更はありません' : (result.status === 'succeeded' ? '実行が完了しました' : '実行計画を確認しました'),
  };
}

function validateJournalAgainstPlan(planResult, journal) {
  const expected = planResult?.journal || planResult;
  if (!expected || !journal) return { ok: false, error: 'JOURNAL_OR_PLAN_MISSING' };
  const checks = [
    ['plan_identity_sha256', expected.plan_identity_sha256, journal.plan_identity_sha256],
    ['queue_sha256', expected.queue?.sha256, journal.queue?.sha256],
    ['change_set_sha256', expected.change_set?.sha256, journal.change_set?.sha256],
  ];
  for (const [field, wanted, observed] of checks) {
    if (!wanted || wanted !== observed) {
      return { ok: false, error: 'JOURNAL_IDENTITY_MISMATCH', field, wanted, observed };
    }
  }
  const expectedEntries = expected.entries || [];
  const observedEntries = journal.entries || [];
  if (expectedEntries.length !== observedEntries.length) {
    return { ok: false, error: 'JOURNAL_ENTRY_COUNT_MISMATCH' };
  }
  for (let index = 0; index < expectedEntries.length; index += 1) {
    const wanted = expectedEntries[index];
    const observed = observedEntries[index];
    if (
      wanted.package_id !== observed.package_id
      || wanted.descriptor_sha256 !== observed.descriptor_sha256
      || wanted.order !== observed.order
    ) {
      return {
        ok: false,
        error: 'JOURNAL_PREFIX_MISMATCH',
        index,
        package_id: observed.package_id,
      };
    }
  }
  return {
    ok: true,
    prefix_identity_sha256: journalPrefixIdentity(journal),
    event_count: journalEventCount(journal),
    resume: summarizeResume(journal),
  };
}

function inspectAuthoritySet(planResult, authoritySet, changeSet = null) {
  const entries = planResult?.journal?.entries || [];
  const mutating = entries.filter((entry) => (
    Boolean(entry.requested_operation)
    && !['not_selected', 'verified_noop', 'succeeded'].includes(entry.current_state)
  ));
  if (mutating.length === 0) return { status: 'not_required', exact: true, records: [] };
  if (mutating.some((entry) => ['started', 'effect_unknown'].includes(entry.current_state))) {
    return {
      status: 'reconciliation_required',
      exact: false,
      error: 'EFFECT_RECONCILIATION_REQUIRED',
    };
  }
  const authoritySetSchemas = new Set([
    'nlmytgen.factory_queue.execution_authority_set.v1',
    'nlmytgen.factory_queue.execution_authority_set.derived_artifact.v1',
  ]);
  if (
    !authoritySetSchemas.has(authoritySet?.schema)
    || authoritySet?.schema_version !== '1.0'
    || !Array.isArray(authoritySet.authorities)
  ) {
    return { status: 'invalid', exact: false, error: 'AUTHORITY_SET_SCHEMA_INVALID' };
  }
  const authorityIds = authoritySet.authorities.map((record) => record?.authority_id);
  if (
    authorityIds.some((authorityId) => typeof authorityId !== 'string' || !authorityId)
    || new Set(authorityIds).size !== authorityIds.length
  ) {
    return { status: 'invalid', exact: false, error: 'AUTHORITY_SET_ID_INVALID' };
  }
  const baseConstraints = {
    serial_only: true,
    exact_identity_recheck: true,
    private_artifact_copy: false,
    human_acceptance: false,
    rights: false,
    production: false,
    publication: false,
    upload: false,
    release: false,
  };
  const derivedConstraints = {
    serial_only: true,
    exact_identity_recheck: true,
    derived_artifact_generation: true,
    no_overwrite: true,
    lifecycle_transition: false,
    content_change: false,
    private_artifact_copy: true,
    human_acceptance: false,
    rights: false,
    production: false,
    publication: false,
    upload: false,
    release: false,
  };
  const usedAuthorityIds = new Set(
    entries.flatMap((entry) => (entry.events || [])
      .filter((event) => event.state === 'started' && event.authority_id)
      .map((event) => event.authority_id)),
  );
  const records = [];
  for (const entry of mutating) {
    const declaredAuthorityId = (entry.events || [])
      .map((event) => event.authority_id)
      .find((authorityId) => Boolean(authorityId))
      || entry.authority_id
      || null;
    const consumedAuthorityIds = (entry.events || [])
      .filter((event) => event.state === 'started' && event.authority_id)
      .map((event) => event.authority_id);
    const replacedAuthorityId = entry.current_state === 'failed'
      ? consumedAuthorityIds.at(-1)
      : null;
    const candidates = authoritySet.authorities.filter((candidate) => (
      replacedAuthorityId
        ? (
          candidate.replaces_authority_id === replacedAuthorityId
          && candidate.authority_id !== replacedAuthorityId
        )
        : (
          candidate.authority_id === declaredAuthorityId
          && candidate.replaces_authority_id === null
        )
    ));
    if (candidates.length !== 1) {
      return {
        status: entry.current_state === 'failed' ? 'replacement_required' : 'invalid',
        exact: false,
        error: entry.current_state === 'failed'
          ? 'REPLACEMENT_AUTHORITY_MISSING_OR_AMBIGUOUS'
          : 'AUTHORITY_RECORD_MISSING_OR_AMBIGUOUS',
      };
    }
    const [record] = candidates;
    const derivedEntry = entry.requested_operation === 'review_packet_generation';
    const changeEntry = (changeSet?.entries || []).find((candidate) => (
      candidate?.package_id === entry.package_id
      && candidate?.operation === entry.requested_operation
    ));
    const expectedRecordSchema = derivedEntry
      ? 'nlmytgen.factory_queue.execution_authority.derived_artifact.v1'
      : 'nlmytgen.factory_queue.execution_authority.v1';
    const expectedConstraints = derivedEntry ? derivedConstraints : baseConstraints;
    const artifact = changeEntry?.derived_artifact;
    const derivedExact = !derivedEntry || (
      authoritySet.schema
        === 'nlmytgen.factory_queue.execution_authority_set.derived_artifact.v1'
      && changeSet?.schema === 'nlmytgen.factory_queue.change_set.derived_artifact.v1'
      && record.effect_class === 'derived_artifact'
      && record.derived_artifact?.cue_id === artifact?.cue_id
      && record.derived_artifact?.output_root === artifact?.output_root
      && record.derived_artifact?.generated_project_sha256
        === artifact?.generated_project?.sha256
      && record.derived_artifact?.source_mp4_sha256 === artifact?.source_mp4?.sha256
    );
    const exact = (
      record.schema === expectedRecordSchema
      && record.queue?.path === planResult.journal.queue.path
      && record.queue?.sha256 === planResult.journal.queue.sha256
      && record.change_set?.change_set_id === planResult.journal.change_set.change_set_id
      && record.change_set?.sha256 === planResult.journal.change_set.sha256
      && record.package?.package_id === entry.package_id
      && record.package?.descriptor_path === entry.descriptor_path
      && record.package?.descriptor_sha256 === entry.descriptor_sha256
      && record.from_lifecycle === entry.from_lifecycle
      && record.to_lifecycle === entry.to_lifecycle
      && record.operation === entry.requested_operation
      && record.maximum_use_count === 1
      && identitySha256(record.constraints) === identitySha256(expectedConstraints)
      && derivedExact
    );
    if (!exact) return { status: 'invalid', exact: false, error: 'AUTHORITY_IDENTITY_MISMATCH' };
    if (record.status !== 'available') {
      return { status: record.status, exact: true, error: 'AUTHORITY_NOT_AVAILABLE' };
    }
    if (usedAuthorityIds.has(record.authority_id)) {
      return { status: 'consumed', exact: true, error: 'AUTHORITY_ALREADY_CONSUMED' };
    }
    records.push({ authority_id: record.authority_id, package_id: entry.package_id });
  }
  return { status: 'available', exact: true, records };
}

function buildExecutorArgs({
  queuePath,
  changeSetPath,
  authorityPath = null,
  journalPath = null,
  execute = false,
}) {
  const args = [
    'execute-factory-queue',
    '--queue', queuePath,
    '--change-set', changeSetPath,
  ];
  if (authorityPath) args.push('--authority-file', authorityPath);
  if (journalPath) args.push('--resume-journal', journalPath);
  if (execute) args.push('--execute');
  args.push('--format', 'json');
  return args;
}

class LocalJournalStore {
  constructor(rootPath) {
    this.rootPath = path.resolve(rootPath);
    this.recentPath = path.join(this.rootPath, 'recent.json');
  }

  persist(executionResult) {
    const journal = executionResult?.journal;
    if (journal?.schema !== 'nlmytgen.factory_queue.execution_journal.v1') {
      throw new Error('EXECUTION_JOURNAL_SCHEMA_INVALID');
    }
    fs.mkdirSync(this.rootPath, { recursive: true });
    const prefix = journalPrefixIdentity(journal);
    const target = path.join(this.rootPath, `${journal.plan_identity_sha256}.json`);
    const bytes = `${JSON.stringify(journal, null, 2)}\n`;
    if (fs.existsSync(target)) {
      const existing = JSON.parse(fs.readFileSync(target, 'utf8'));
      const existingEvents = journalEventCount(existing);
      const nextEvents = journalEventCount(journal);
      if (nextEvents < existingEvents) throw new Error('JOURNAL_PREFIX_REGRESSION');
      const sameIdentity = (
        existing.plan_identity_sha256 === journal.plan_identity_sha256
        && existing.queue?.sha256 === journal.queue?.sha256
        && existing.change_set?.sha256 === journal.change_set?.sha256
        && (existing.entries || []).length === (journal.entries || []).length
      );
      const prefixUnchanged = sameIdentity && (existing.entries || []).every((entry, index) => {
        const next = journal.entries[index];
        return (
          entry.package_id === next?.package_id
          && entry.descriptor_sha256 === next?.descriptor_sha256
          && entry.order === next?.order
          && identitySha256(entry.events || [])
            === identitySha256((next?.events || []).slice(0, (entry.events || []).length))
        );
      });
      if (!prefixUnchanged) {
        throw new Error('JOURNAL_PREFIX_REWRITE_REJECTED');
      }
    }
    fs.writeFileSync(target, bytes, 'utf8');
    fs.writeFileSync(this.recentPath, `${JSON.stringify({ path: target, prefix_identity_sha256: prefix }, null, 2)}\n`, 'utf8');
    return {
      path: target,
      file_sha256: fileSha256(target),
      prefix_identity_sha256: prefix,
      event_count: journalEventCount(journal),
    };
  }

  load(filePath) {
    const resolved = path.resolve(filePath);
    const journal = JSON.parse(fs.readFileSync(resolved, 'utf8'));
    if (journal?.schema !== 'nlmytgen.factory_queue.execution_journal.v1') {
      throw new Error('EXECUTION_JOURNAL_SCHEMA_INVALID');
    }
    return {
      path: resolved,
      journal,
      file_sha256: fileSha256(resolved),
      prefix_identity_sha256: journalPrefixIdentity(journal),
      event_count: journalEventCount(journal),
      resume: summarizeResume(journal),
    };
  }

  loadRecent() {
    if (!fs.existsSync(this.recentPath)) return null;
    const recent = JSON.parse(fs.readFileSync(this.recentPath, 'utf8'));
    return this.load(recent.path);
  }
}

class BatchJobController {
  constructor({
    startProcess,
    cancelProcess,
    emit,
    isOtherJobActive = () => false,
    now = () => new Date().toISOString(),
  }) {
    this.startProcess = startProcess;
    this.cancelProcess = cancelProcess;
    this.emit = emit;
    this.isOtherJobActive = isOtherJobActive;
    this.now = now;
    this.active = null;
  }

  snapshot() {
    if (!this.active) return { state: 'idle', active: false };
    return {
      id: this.active.id,
      kind: 'batch',
      mode: this.active.mode,
      state: this.active.state,
      active: ['running', 'cancelling', 'finishing'].includes(this.active.state),
      started_at: this.active.startedAt,
      log_lines: [...this.active.logLines],
      result: this.active.result,
    };
  }

  start(spec) {
    if (
      this.isOtherJobActive()
      || (this.active && ['running', 'cancelling', 'finishing'].includes(this.active.state))
    ) {
      return { ok: false, error: 'PIPELINE_JOB_ALREADY_ACTIVE', job: this.snapshot() };
    }
    const job = {
      id: `batch-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      mode: spec.mode,
      state: 'running',
      startedAt: this.now(),
      logLines: [],
      stdout: '',
      stderr: '',
      process: null,
      result: null,
    };
    this.active = job;
    const pushLog = (stream, chunk) => {
      const raw = String(chunk || '');
      if (stream === 'stdout') job.stdout = `${job.stdout}${raw}`.slice(-2_000_000);
      else job.stderr = `${job.stderr}${raw}`.slice(-400_000);
      const lines = sanitizeOperatorText(raw, 12000).split(/\r?\n/).filter(Boolean);
      for (const line of lines) job.logLines.push(`[${stream}] ${line}`);
      if (job.logLines.length > MAX_BATCH_LOG_LINES) {
        job.logLines.splice(0, job.logLines.length - MAX_BATCH_LOG_LINES);
      }
      this.emit('log', { id: job.id, kind: 'batch', mode: job.mode, stream, lines });
    };
    try {
      job.process = this.startProcess(spec, {
        stdout: (chunk) => pushLog('stdout', chunk),
        stderr: (chunk) => pushLog('stderr', chunk),
        close: (processResult) => {
          job.state = processResult.cancelled || job.state === 'cancelling'
            ? 'cancelled'
            : 'finishing';
          Promise.resolve(
            typeof spec.complete === 'function'
              ? spec.complete({
                code: processResult.code,
                cancelled: processResult.cancelled === true,
                stdout: job.stdout,
                stderr: job.stderr,
              })
              : null,
          ).then((result) => {
            job.result = result;
            if (job.state !== 'cancelled') {
              job.state = processResult.code === 0 && result?.ok !== false
                ? 'completed'
                : 'failed';
            }
            this.emit('finished', {
              id: job.id,
              kind: 'batch',
              mode: job.mode,
              state: job.state,
              code: processResult.code,
              log_lines: [...job.logLines],
              result: job.result,
            });
          }).catch((error) => {
            job.state = 'failed';
            pushLog('stderr', error.message);
            job.result = { ok: false, error: sanitizeOperatorText(error.message, 2000) };
            this.emit('finished', {
              id: job.id,
              kind: 'batch',
              mode: job.mode,
              state: job.state,
              code: processResult.code,
              log_lines: [...job.logLines],
              result: job.result,
            });
          });
        },
      });
      this.emit('started', {
        id: job.id,
        kind: 'batch',
        mode: job.mode,
        started_at: job.startedAt,
      });
      return { ok: true, job: this.snapshot() };
    } catch (error) {
      job.state = 'failed';
      pushLog('stderr', error.message);
      job.result = { ok: false, error: sanitizeOperatorText(error.message, 2000) };
      this.emit('finished', {
        id: job.id,
        kind: 'batch',
        mode: job.mode,
        state: job.state,
        code: -1,
        log_lines: [...job.logLines],
        result: job.result,
      });
      return { ok: false, error: error.message, job: this.snapshot() };
    }
  }

  async cancel(id) {
    if (!this.active || this.active.id !== id || this.active.state !== 'running') {
      return { ok: false, error: 'NO_MATCHING_ACTIVE_PIPELINE_JOB', job: this.snapshot() };
    }
    this.active.state = 'cancelling';
    this.emit('cancelling', { id, kind: 'batch', mode: this.active.mode });
    try {
      await this.cancelProcess(this.active.process);
      return { ok: true, job: this.snapshot() };
    } catch (error) {
      this.active.state = 'failed';
      this.active.result = { ok: false, error: sanitizeOperatorText(error.message, 2000) };
      this.emit('finished', {
        id,
        kind: 'batch',
        mode: this.active.mode,
        state: 'failed',
        code: -1,
        result: this.active.result,
      });
      return { ok: false, error: error.message, job: this.snapshot() };
    }
  }
}

module.exports = {
  AUTHORITY_PRESENTATION,
  BatchJobController,
  DEFAULT_CHANGE_SET_PATH,
  DEFAULT_QUEUE_PATH,
  EXECUTION_STATES,
  LocalJournalStore,
  MAX_BATCH_LOG_LINES,
  STATE_PRESENTATION,
  authorityStateForEntry,
  buildExecutorArgs,
  fileSha256,
  identitySha256,
  inferDescriptorLifecycle,
  inspectAuthoritySet,
  journalEventCount,
  journalPrefixIdentity,
  normalizeExecutionResult,
  sanitizeOperatorText,
  summarizeResume,
  validateJournalAgainstPlan,
};

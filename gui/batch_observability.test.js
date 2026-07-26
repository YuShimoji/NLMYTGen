const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');

const {
  AUTHORITY_PRESENTATION,
  BatchJobController,
  DEFAULT_CHANGE_SET_PATH,
  DEFAULT_QUEUE_PATH,
  EXECUTION_STATES,
  LocalJournalStore,
  MAX_BATCH_LOG_LINES,
  STATE_PRESENTATION,
  buildExecutorArgs,
  inferDescriptorLifecycle,
  inspectAuthoritySet,
  journalPrefixIdentity,
  normalizeExecutionResult,
  sanitizeOperatorText,
  summarizeResume,
  validateJournalAgainstPlan,
} = require('./batch_observability');

const SHA = Object.freeze({
  queue: '1'.repeat(64),
  change: '2'.repeat(64),
  plan: '3'.repeat(64),
  descriptorA: '4'.repeat(64),
  descriptorB: '5'.repeat(64),
});

function event(state, overrides = {}) {
  return {
    sequence: 1,
    state,
    authority_id: null,
    authority_status: state === 'verified_noop' ? 'not_required' : 'available',
    backend_result_identity_sha256: null,
    failure_code: null,
    consumer_effect: `${state} effect`,
    ...overrides,
  };
}

function entry(packageId, state, order, overrides = {}) {
  return {
    order,
    package_id: packageId,
    descriptor_path: `fixtures/${packageId}.json`,
    descriptor_sha256: order === 1 ? SHA.descriptorA : SHA.descriptorB,
    from_lifecycle: state === 'verified_noop' ? null : 'package_prepared',
    to_lifecycle: state === 'verified_noop' ? null : 'source_project_ready',
    requested_operation: state === 'verified_noop' ? null : 'source_project_generation',
    technical_decision: state,
    current_state: state,
    events: [event(state)],
    ...overrides,
  };
}

function resultFor(entries, status = 'planned') {
  const counts = {
    authority_consumptions: 0,
    effect_unknown: entries.filter((item) => item.current_state === 'effect_unknown').length,
    failed: entries.filter((item) => item.current_state === 'failed').length,
    not_selected: entries.filter((item) => item.current_state === 'not_selected').length,
    packages_validated: entries.length,
    planned: entries.filter((item) => item.current_state === 'planned').length,
    skipped_after_failure: entries.filter((item) => item.current_state === 'skipped_after_failure').length,
    succeeded: entries.filter((item) => item.current_state === 'succeeded').length,
    verified_noop: entries.filter((item) => item.current_state === 'verified_noop').length,
  };
  const boundaries = {
    append_only_journal: true,
    backend_dispatch_count: 0,
    source_project_generation_count: 0,
    render_count: 0,
    yymm4_launch_count: 0,
    playback_count: 0,
    product_write_count: 0,
  };
  return {
    schema: 'nlmytgen.factory_queue.execution_result.v1',
    schema_version: '1.0',
    status,
    plan: {
      schema: 'nlmytgen.factory_queue.executor.v1',
      package_count: entries.length,
      mutating_entry_count: entries.filter((item) => item.requested_operation).length,
      plan_identity_sha256: SHA.plan,
      queue: { path: 'fixtures/queue.json', sha256: SHA.queue },
      change_set: {
        path: 'fixtures/change.json',
        sha256: SHA.change,
        change_set_id: 'fixture_change',
      },
    },
    journal: {
      schema: 'nlmytgen.factory_queue.execution_journal.v1',
      schema_version: '1.0',
      status,
      execution_mode: status === 'planned' ? 'plan_only' : 'execute',
      plan_identity_sha256: SHA.plan,
      queue: { path: 'fixtures/queue.json', sha256: SHA.queue },
      change_set: {
        path: 'fixtures/change.json',
        sha256: SHA.change,
        change_set_id: 'fixture_change',
      },
      counts,
      entries,
      boundaries,
    },
    execution_receipt: {
      schema: 'nlmytgen.factory_queue.execution_receipt.v1',
      journal_sha256: '6'.repeat(64),
      counts,
      boundaries,
    },
  };
}

test('default files and CLI builder keep the exact executor boundary', () => {
  assert.equal(DEFAULT_QUEUE_PATH.endsWith('four_package_lifecycle_queue_v3.json'), true);
  assert.equal(DEFAULT_CHANGE_SET_PATH.endsWith('four_package_zero_change_set_v1.json'), true);
  assert.deepEqual(buildExecutorArgs({
    queuePath: DEFAULT_QUEUE_PATH,
    changeSetPath: DEFAULT_CHANGE_SET_PATH,
  }), [
    'execute-factory-queue',
    '--queue', DEFAULT_QUEUE_PATH,
    '--change-set', DEFAULT_CHANGE_SET_PATH,
    '--format', 'json',
  ]);
  const executeArgs = buildExecutorArgs({
    queuePath: 'q.json',
    changeSetPath: 'c.json',
    authorityPath: 'a.json',
    journalPath: 'j.json',
    execute: true,
  });
  assert.deepEqual(executeArgs, [
    'execute-factory-queue',
    '--queue', 'q.json',
    '--change-set', 'c.json',
    '--authority-file', 'a.json',
    '--resume-journal', 'j.json',
    '--execute',
    '--format', 'json',
  ]);
  assert.equal(executeArgs.some((value) => /shell|cmd|powershell/.test(value)), false);
});

test('all journal states and authority states have Japanese operator labels', () => {
  assert.deepEqual(Object.keys(STATE_PRESENTATION).sort(), [...EXECUTION_STATES].sort());
  for (const state of EXECUTION_STATES) {
    assert.equal(typeof STATE_PRESENTATION[state].label, 'string');
    assert.ok(STATE_PRESENTATION[state].label.length > 0);
  }
  assert.deepEqual(
    Object.keys(AUTHORITY_PRESENTATION).sort(),
    [
      'absent',
      'available',
      'consumed',
      'invalid',
      'not_required',
      'reconciliation_required',
      'replacement_required',
      'required',
    ].sort(),
  );
});

test('real-style four no-op rows produce the direct zero-change message', () => {
  const entries = [
    entry('new_banknote_security_notebooklm_001', 'verified_noop', 1),
    entry('real_estate_reins_transparency_001', 'verified_noop', 2),
    entry('ai_monitoring_labor_001', 'verified_noop', 3, { descriptor_sha256: '7'.repeat(64) }),
    entry('food_expiry_labels_001', 'verified_noop', 4, { descriptor_sha256: '8'.repeat(64) }),
  ];
  const model = normalizeExecutionResult(resultFor(entries), {
    descriptorLoader: (descriptorPath) => (
      descriptorPath.includes('new_banknote')
        ? { human_decision: { state: 'accepted_exact_artifact' } }
        : { render_validation: { technical_status: 'passed' } }
    ),
  });
  assert.equal(model.result_message, '変更はありません');
  assert.equal(model.package_count, 4);
  assert.equal(model.counts.verified_noop, 4);
  assert.equal(model.mutating_entry_count, 0);
  assert.equal(model.authority.state, 'not_required');
  assert.equal(model.rows.every((row) => row.execution_state === 'verified_noop'), true);
  assert.equal(model.rows[0].current_lifecycle, 'human_accepted');
  assert.equal(model.rows.slice(1).every((row) => row.current_lifecycle === 'rendered'), true);
  assert.equal(model.boundaries.backend_dispatch_count, 0);
});

test('lifecycle inference preserves explicit and recorded completion levels', () => {
  assert.equal(inferDescriptorLifecycle({ lifecycle: { state: 'rendered' } }), 'rendered');
  assert.equal(
    inferDescriptorLifecycle({ human_decision: { state: 'accepted_exact_artifact' } }),
    'human_accepted',
  );
  assert.equal(
    inferDescriptorLifecycle({ render_validation: { technical_status: 'passed' } }),
    'rendered',
  );
  assert.equal(
    inferDescriptorLifecycle({ source_project: { state: 'ready' } }),
    'source_project_ready',
  );
  assert.equal(inferDescriptorLifecycle({}), 'package_prepared');
});

test('known failure exposes replacement authority and skips later work', () => {
  const failed = entry('fixture_failed', 'failed', 1, {
    events: [event('failed', { failure_code: 'SYNTHETIC_KNOWN_FAILURE' })],
  });
  const skipped = entry('fixture_later', 'skipped_after_failure', 2);
  const model = normalizeExecutionResult(resultFor([failed, skipped], 'failed'));
  assert.equal(model.rows[0].authority_state, 'replacement_required');
  assert.equal(model.rows[0].reason, 'SYNTHETIC_KNOWN_FAILURE');
  assert.equal(model.rows[1].execution_state, 'skipped_after_failure');
  assert.equal(model.resume.eligible, true);
  assert.equal(model.resume.state, 'replacement_authority_required');
});

test('effect_unknown is blocked and never exposes normal resume', () => {
  const unknown = entry('fixture_unknown', 'effect_unknown', 1);
  const model = normalizeExecutionResult(resultFor([unknown], 'failed'));
  assert.equal(model.rows[0].authority_state, 'reconciliation_required');
  assert.equal(model.rows[0].resume_effect, '自動再試行不可・読み取り照合');
  assert.equal(model.resume.eligible, false);
  assert.equal(model.resume.state, 'reconciliation_required');
});

test('safe resume skips prior success and keeps the unresolved continuation', () => {
  const succeeded = entry('fixture_done', 'succeeded', 1);
  const pending = entry('fixture_next', 'planned', 2);
  const journal = resultFor([succeeded, pending]).journal;
  const resume = summarizeResume(journal);
  assert.equal(resume.eligible, true);
  assert.equal(resume.package_id, 'fixture_next');
  assert.equal(resume.state, 'continuation_available');
  const model = normalizeExecutionResult(resultFor([succeeded, pending]));
  assert.equal(model.rows[0].resume_effect, '再実行しない');
});

test('journal validation rejects plan, order, and descriptor prefix drift', () => {
  const planResult = resultFor([
    entry('fixture_a', 'planned', 1),
    entry('fixture_b', 'planned', 2),
  ]);
  assert.equal(validateJournalAgainstPlan(planResult, planResult.journal).ok, true);
  const planDrift = structuredClone(planResult.journal);
  planDrift.plan_identity_sha256 = '9'.repeat(64);
  assert.equal(validateJournalAgainstPlan(planResult, planDrift).error, 'JOURNAL_IDENTITY_MISMATCH');
  const orderDrift = structuredClone(planResult.journal);
  [orderDrift.entries[0], orderDrift.entries[1]] = [orderDrift.entries[1], orderDrift.entries[0]];
  assert.equal(validateJournalAgainstPlan(planResult, orderDrift).error, 'JOURNAL_PREFIX_MISMATCH');
  const descriptorDrift = structuredClone(planResult.journal);
  descriptorDrift.entries[0].descriptor_sha256 = 'a'.repeat(64);
  assert.equal(validateJournalAgainstPlan(planResult, descriptorDrift).error, 'JOURNAL_PREFIX_MISMATCH');
});

test('journal store survives a new store instance and rejects prefix rewrite', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nlmytgen-batch-journal-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const initial = resultFor([entry('fixture_done', 'succeeded', 1)], 'succeeded');
  const firstStore = new LocalJournalStore(root);
  const saved = firstStore.persist(initial);
  const prefixBefore = journalPrefixIdentity(initial.journal);
  assert.equal(saved.prefix_identity_sha256, prefixBefore);

  const restartedStore = new LocalJournalStore(root);
  const reopened = restartedStore.loadRecent();
  assert.equal(reopened.prefix_identity_sha256, prefixBefore);
  assert.equal(reopened.event_count, 1);
  assert.equal(reopened.journal.entries[0].current_state, 'succeeded');

  const rewrite = structuredClone(initial);
  rewrite.journal.entries[0].events[0].state = 'failed';
  assert.throws(() => restartedStore.persist(rewrite), /JOURNAL_PREFIX_REWRITE_REJECTED/);
});

test('authority preflight is exact and does not fabricate records', () => {
  const planned = entry('fixture_a', 'planned', 1, {
    events: [event('planned', { authority_id: 'authority_fixture_a', authority_status: 'required' })],
  });
  const planResult = resultFor([planned]);
  assert.equal(inspectAuthoritySet(planResult, null).status, 'invalid');
  const authoritySet = {
    schema: 'nlmytgen.factory_queue.execution_authority_set.v1',
    schema_version: '1.0',
    authorities: [{
      schema: 'nlmytgen.factory_queue.execution_authority.v1',
      authority_id: 'authority_fixture_a',
      replaces_authority_id: null,
      queue: { path: 'fixtures/queue.json', sha256: SHA.queue },
      change_set: { change_set_id: 'fixture_change', sha256: SHA.change },
      package: {
        package_id: 'fixture_a',
        descriptor_path: 'fixtures/fixture_a.json',
        descriptor_sha256: SHA.descriptorA,
      },
      from_lifecycle: 'package_prepared',
      to_lifecycle: 'source_project_ready',
      operation: 'source_project_generation',
      maximum_use_count: 1,
      status: 'available',
      constraints: {
        serial_only: true,
        exact_identity_recheck: true,
        private_artifact_copy: false,
        human_acceptance: false,
        rights: false,
        production: false,
        publication: false,
        upload: false,
        release: false,
      },
    }],
  };
  assert.deepEqual(inspectAuthoritySet(planResult, authoritySet), {
    status: 'available',
    exact: true,
    records: [{ authority_id: 'authority_fixture_a', package_id: 'fixture_a' }],
  });
  authoritySet.authorities[0].package.package_id = 'wrong_package';
  assert.equal(inspectAuthoritySet(planResult, authoritySet).error, 'AUTHORITY_IDENTITY_MISMATCH');
  authoritySet.authorities[0].package.package_id = 'fixture_a';
  authoritySet.authorities[0].queue.path = 'fixtures/other_queue.json';
  assert.equal(inspectAuthoritySet(planResult, authoritySet).error, 'AUTHORITY_IDENTITY_MISMATCH');
  authoritySet.authorities[0].queue.path = 'fixtures/queue.json';
  authoritySet.authorities[0].constraints.publication = true;
  assert.equal(inspectAuthoritySet(planResult, authoritySet).error, 'AUTHORITY_IDENTITY_MISMATCH');
});

test('failed resume requires one exact replacement authority', () => {
  const failed = entry('fixture_a', 'failed', 1, {
    events: [
      event('planned', {
        sequence: 1,
        authority_id: 'authority_fixture_a',
        authority_status: 'required',
      }),
      event('started', {
        sequence: 2,
        authority_id: 'authority_fixture_a',
        authority_status: 'consumed',
      }),
      event('failed', {
        sequence: 3,
        authority_id: 'authority_fixture_a',
        authority_status: 'consumed',
      }),
    ],
  });
  const planResult = resultFor([failed], 'failed');
  const replacement = {
    schema: 'nlmytgen.factory_queue.execution_authority_set.v1',
    schema_version: '1.0',
    authorities: [{
      schema: 'nlmytgen.factory_queue.execution_authority.v1',
      authority_id: 'authority_fixture_a_retry',
      replaces_authority_id: 'authority_fixture_a',
      queue: { path: 'fixtures/queue.json', sha256: SHA.queue },
      change_set: { change_set_id: 'fixture_change', sha256: SHA.change },
      package: {
        package_id: 'fixture_a',
        descriptor_path: 'fixtures/fixture_a.json',
        descriptor_sha256: SHA.descriptorA,
      },
      from_lifecycle: 'package_prepared',
      to_lifecycle: 'source_project_ready',
      operation: 'source_project_generation',
      maximum_use_count: 1,
      status: 'available',
      constraints: {
        serial_only: true,
        exact_identity_recheck: true,
        private_artifact_copy: false,
        human_acceptance: false,
        rights: false,
        production: false,
        publication: false,
        upload: false,
        release: false,
      },
    }],
  };
  assert.deepEqual(inspectAuthoritySet(planResult, replacement), {
    status: 'available',
    exact: true,
    records: [{ authority_id: 'authority_fixture_a_retry', package_id: 'fixture_a' }],
  });
  replacement.authorities[0].replaces_authority_id = null;
  assert.equal(
    inspectAuthoritySet(planResult, replacement).error,
    'REPLACEMENT_AUTHORITY_MISSING_OR_AMBIGUOUS',
  );
});

test('no-op plan does not request or consume authority', () => {
  const planResult = resultFor([entry('fixture_noop', 'verified_noop', 1)]);
  assert.deepEqual(inspectAuthoritySet(planResult, null), {
    status: 'not_required',
    exact: true,
    records: [],
  });
  const model = normalizeExecutionResult(planResult);
  assert.equal(model.rows[0].authority_state, 'not_required');
  assert.equal(model.counts.authority_consumptions, 0);
});

test('long package IDs and Japanese errors remain sanitized and bounded', () => {
  const longId = `package_${'x'.repeat(180)}`;
  const longError = `処理に失敗しました。${'詳細'.repeat(5000)} C:\\Users\\private-user\\secret`;
  const failed = entry(longId, 'failed', 1, {
    events: [event('failed', { failure_code: longError, consumer_effect: null })],
  });
  const model = normalizeExecutionResult(resultFor([failed], 'failed'));
  assert.equal(model.rows[0].package_id, longId);
  assert.ok(model.rows[0].reason.length <= 240);
  assert.equal(model.rows[0].reason.includes('private-user'), false);
  assert.equal(sanitizeOperatorText(longError).includes('<user-home>'), true);
  assert.equal(MAX_BATCH_LOG_LINES, 240);
});

test('batch job controller admits one owned process, bounds logs, and returns parsed result', async () => {
  let callbacks;
  const events = [];
  const ownedProcess = { pid: 42 };
  const controller = new BatchJobController({
    startProcess: (_spec, nextCallbacks) => {
      callbacks = nextCallbacks;
      return ownedProcess;
    },
    cancelProcess: async () => {},
    emit: (type, payload) => events.push({ type, ...payload }),
  });
  const started = controller.start({
    mode: 'plan',
    complete: ({ code, stdout }) => ({ ok: code === 0, stdout }),
  });
  assert.equal(started.ok, true);
  assert.equal(started.job.kind, 'batch');
  assert.equal(controller.start({ mode: 'execute' }).error, 'PIPELINE_JOB_ALREADY_ACTIVE');
  callbacks.stdout(`${Array.from({ length: 260 }, (_, index) => `line-${index}`).join('\n')}\n`);
  assert.equal(controller.snapshot().log_lines.length, MAX_BATCH_LOG_LINES);
  callbacks.close({ code: 0, cancelled: false });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(controller.snapshot().state, 'completed');
  assert.equal(controller.snapshot().result.ok, true);
  assert.equal(events.some((item) => item.type === 'finished' && item.kind === 'batch'), true);
});

test('batch cancellation targets only its owned process and respects shared-job admission', async () => {
  let callbacks;
  let cancelledProcess = null;
  const ownedProcess = { pid: 73 };
  const blocked = new BatchJobController({
    startProcess: () => ownedProcess,
    cancelProcess: async () => {},
    emit: () => {},
    isOtherJobActive: () => true,
  });
  assert.equal(blocked.start({ mode: 'plan' }).error, 'PIPELINE_JOB_ALREADY_ACTIVE');

  const controller = new BatchJobController({
    startProcess: (_spec, nextCallbacks) => {
      callbacks = nextCallbacks;
      return ownedProcess;
    },
    cancelProcess: async (process) => { cancelledProcess = process; },
    emit: () => {},
  });
  const started = controller.start({ mode: 'execute' });
  const cancelled = await controller.cancel(started.job.id);
  assert.equal(cancelled.ok, true);
  assert.equal(cancelledProcess, ownedProcess);
  callbacks.close({ code: 1, cancelled: true });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(controller.snapshot().state, 'cancelled');
});

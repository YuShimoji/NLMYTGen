const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { app, ipcMain } = require('electron');

function isEnabled() {
  return process.env.NLMYTGEN_BATCH_OBSERVABILITY_PROBE === '1';
}

function requiredPath(name) {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is required in batch probe mode`);
  return path.resolve(value);
}

function profilePath() {
  return requiredPath('NLMYTGEN_BATCH_OBSERVABILITY_PROFILE');
}

function receiptPath() {
  return requiredPath('NLMYTGEN_BATCH_OBSERVABILITY_RECEIPT');
}

function observe(win) {
  const observations = {
    console_errors: [],
    security_warnings: [],
    load_failures: [],
    render_process_gone: [],
    preload_errors: [],
    renderer_unhandled_errors: [],
  };
  const rendererErrorHandler = (_event, detail) => {
    observations.renderer_unhandled_errors.push(detail);
  };
  ipcMain.on('nlmytgen-batch-observability-renderer-error', rendererErrorHandler);
  Object.defineProperty(observations, 'dispose', {
    enumerable: false,
    value: () => ipcMain.off(
      'nlmytgen-batch-observability-renderer-error',
      rendererErrorHandler,
    ),
  });
  win.webContents.on('console-message', (_event, ...args) => {
    const detail = args.length === 1 && args[0] && typeof args[0] === 'object'
      ? args[0]
      : { level: args[0], message: args[1] };
    const message = String(detail.message || '');
    if (String(detail.level).toLowerCase() === 'error' || Number(detail.level) >= 3) {
      observations.console_errors.push(message);
    }
    if (/security warning|insecure|contextisolation|nodeintegration/i.test(message)) {
      observations.security_warnings.push(message);
    }
  });
  win.webContents.on('did-fail-load', (_event, code, description, url, mainFrame) => {
    observations.load_failures.push({ code, description, url, main_frame: mainFrame });
  });
  win.webContents.on('render-process-gone', (_event, detail) => {
    observations.render_process_gone.push(detail);
  });
  win.webContents.on('preload-error', (_event, preloadPath, error) => {
    observations.preload_errors.push({
      preload_path: path.basename(preloadPath),
      error: String(error?.stack || error?.message || error),
    });
  });
  return observations;
}

function writeReceipt(payload) {
  const target = receiptPath();
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  console.log(`BATCH_OBSERVABILITY_RECEIPT=${target}`);
  console.log(JSON.stringify(payload, null, 2));
}

function withTimeout(promise, timeoutMs, label) {
  let timeout;
  const expired = new Promise((_resolve, reject) => {
    timeout = setTimeout(
      () => reject(new Error(`${label} timed out after ${timeoutMs}ms`)),
      timeoutMs,
    );
  });
  return Promise.race([promise, expired]).finally(() => clearTimeout(timeout));
}

async function captureAt(win, width, height, directory, name) {
  win.setSize(width, height);
  await new Promise((resolve) => setTimeout(resolve, 180));
  const layout = await win.webContents.executeJavaScript(`
    (() => {
      document.activeElement?.blur();
      window.scrollTo(0, 0);
      if (document.scrollingElement) document.scrollingElement.scrollTop = 0;
      document.querySelector('[data-tab="batch"]').click();
      const scroll = document.querySelector('.main-tab-scroll');
      if (scroll) {
        scroll.scrollTo({ left: 0, top: 0, behavior: 'instant' });
      }
      const rect = (id) => {
        const value = document.getElementById(id)?.getBoundingClientRect();
        return value ? {
          top: value.top,
          bottom: value.bottom,
          left: value.left,
          right: value.right,
        } : null;
      };
      const root = document.documentElement;
      const table = document.querySelector('.batch-table');
      const value = {
        viewport: { width: window.innerWidth, height: window.innerHeight },
        window_scroll_y: window.scrollY,
        scroll_top: scroll?.scrollTop ?? null,
        document_overflow_x: root.scrollWidth > root.clientWidth,
        main_overflow_x: scroll ? scroll.scrollWidth > scroll.clientWidth : null,
        queue: rect('batch-queue-path'),
        change_set: rect('batch-change-set-path'),
        plan_status: rect('batch-plan-status'),
        mutation_count: rect('batch-mutation-count'),
        primary_action: rect('btn-batch-plan'),
        table_font_px: table ? Number.parseFloat(getComputedStyle(table).fontSize) : null,
      };
      return value;
    })()
  `);
  await new Promise((resolve) => setTimeout(resolve, 120));
  const png = (await win.webContents.capturePage()).toPNG();
  const target = path.join(directory, `${name}_${width}x${height}.png`);
  fs.writeFileSync(target, png);
  return {
    ...layout,
    screenshot: {
      file: path.basename(target),
      bytes: png.length,
      sha256: crypto.createHash('sha256').update(png).digest('hex'),
    },
  };
}

function syntheticModel(base, variant) {
  const model = structuredClone(base);
  model.status = 'synthetic';
  model.execution_mode = 'synthetic_isolated_read_model';
  model.queue = { path: 'fixtures/synthetic_queue.json', sha256: 'a'.repeat(64) };
  model.change_set = {
    path: 'fixtures/synthetic_change_set.json',
    sha256: 'b'.repeat(64),
    change_set_id: 'synthetic_gui_states',
  };
  model.plan_identity_sha256 = 'c'.repeat(64);
  model.mutating_entry_count = variant === 'noop' ? 0 : 2;
  model.counts = {
    authority_consumptions: 0,
    effect_unknown: 0,
    failed: 0,
    not_selected: 0,
    packages_validated: 2,
    planned: 0,
    skipped_after_failure: 0,
    succeeded: 0,
    verified_noop: 0,
  };
  const row = (id, state, order) => ({
    order,
    package_id: id,
    descriptor_path: `fixtures/${id}.json`,
    descriptor_sha256: `${order + 1}`.repeat(64),
    current_lifecycle: 'package_prepared',
    technical_decision: state,
    requested_operation: 'source_project_generation',
    requested_edge: 'package_prepared → source_project_ready',
    authority_state: 'absent',
    authority_label: '権限ファイル未選択',
    authority_tone: 'error',
    execution_state: state,
    execution_label: state,
    execution_tone: state === 'succeeded' ? 'success' : 'pending',
    reason: `${state} の deterministic isolated fixture`,
    resume_effect: '権限確認後に実行',
  });
  model.rows = [row('synthetic_a', 'planned', 1), row('synthetic_b', 'planned', 2)];
  model.authority = { state: 'absent', mutating_entries: 2 };
  model.resume = {
    eligible: true,
    state: 'continuation_available',
    package_id: 'synthetic_a',
    message: '同じ identity と journal prefix から続行できます。',
  };
  model.journal = {
    locator: 'local/synthetic_journal.json',
    identity_sha256: 'd'.repeat(64),
    prefix_identity_sha256: 'e'.repeat(64),
    event_count: 2,
    append_only: true,
  };
  model.result_message = 'synthetic state';
  if (variant === 'authority_wait') {
    model.resume.eligible = false;
    model.resume.state = 'authority_required';
    model.resume.message = 'exact authority file が必要です。';
  } else if (variant === 'running') {
    model.rows[0].execution_state = 'started';
    model.rows[0].execution_label = '実行中';
    model.rows[0].execution_tone = 'active';
    model.rows[0].authority_state = 'consumed';
    model.rows[0].authority_label = '権限使用済み';
  } else if (variant === 'success') {
    model.rows[0].execution_state = 'succeeded';
    model.rows[0].execution_label = '完了';
    model.rows[0].execution_tone = 'success';
    model.rows[0].resume_effect = '再実行しない';
    model.counts.succeeded = 1;
  } else if (variant === 'failure') {
    model.rows[0].execution_state = 'failed';
    model.rows[0].execution_label = '失敗';
    model.rows[0].execution_tone = 'error';
    model.rows[0].authority_state = 'replacement_required';
    model.rows[0].authority_label = '代替権限が必要';
    model.rows[0].resume_effect = '代替権限で安全に再開可能';
    model.rows[1].execution_state = 'skipped_after_failure';
    model.rows[1].execution_label = '先行失敗により未実行';
    model.rows[1].execution_tone = 'muted';
    model.counts.failed = 1;
    model.counts.skipped_after_failure = 1;
    model.resume.state = 'replacement_authority_required';
    model.resume.message = '失敗した entry に新しい exact authority が必要です。';
  } else if (variant === 'effect_unknown') {
    model.rows[0].execution_state = 'effect_unknown';
    model.rows[0].execution_label = '作用結果不明';
    model.rows[0].execution_tone = 'blocked';
    model.rows[0].authority_state = 'reconciliation_required';
    model.rows[0].authority_label = '読み取り照合が必要';
    model.rows[0].resume_effect = '自動再試行不可・読み取り照合';
    model.counts.effect_unknown = 1;
    model.resume = {
      eligible: false,
      state: 'reconciliation_required',
      package_id: 'synthetic_a',
      message: '作用結果が不明です。自動再試行せず、読み取り照合を行ってください。',
    };
  } else if (variant === 'long_text') {
    model.rows[0].package_id = `synthetic_${'long_identifier_'.repeat(20)}`;
    model.rows[0].reason = `長い日本語エラー: ${'安全な折り返しを確認します。'.repeat(80)}`;
  }
  return model;
}

async function run(win, observations) {
  const runRoot = path.dirname(receiptPath());
  const workflow = await withTimeout(win.webContents.executeJavaScript(`
    (async () => {
      const waitFor = async (predicate, label, timeoutMs = 90000) => {
        const started = Date.now();
        while (!predicate()) {
          if (Date.now() - started > timeoutMs) throw new Error(label + ' timed out');
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      };
      await waitFor(
        () => document.readyState === 'complete'
          && window.__nlmytgenBatchProbe
          && document.getElementById('btn-batch-plan'),
        'batch DOM'
      );
      const defaultTab = document.querySelector('.tab.active')?.dataset.tab;
      const standardHeading = document.getElementById('standard-loop-title')?.textContent;
      document.querySelector('[data-tab="batch"]').click();
      await waitFor(
        () => document.getElementById('batch-queue-path').textContent.includes('four_package_lifecycle_queue_v3'),
        'default queue'
      );
      const queuePath = document.getElementById('batch-queue-path').textContent;
      const changeSetPath = document.getElementById('batch-change-set-path').textContent;
      const planButton = document.getElementById('btn-batch-plan');
      planButton.click();
      await waitFor(
        () => document.getElementById('batch-plan-status').textContent.includes('確認済み'),
        'actual plan-only',
        120000
      );
      const planJob = await window.nlmytgen.batchJob();
      const planModel = structuredClone(window.__nlmytgenBatchProbe.snapshot().readModel);
      document.getElementById('btn-batch-execute').click();
      await waitFor(
        () => window.__nlmytgenBatchProbe.snapshot().active,
        'zero-change execute active'
      );
      await waitFor(
        () => {
          const snapshot = window.__nlmytgenBatchProbe.snapshot();
          return !snapshot.active && snapshot.readModel?.execution_mode === 'execute';
        },
        'actual zero-change execute',
        120000
      );
      const executeJob = await window.nlmytgen.batchJob();
      const executeModel = structuredClone(window.__nlmytgenBatchProbe.snapshot().readModel);
      document.getElementById('btn-batch-open-recent').click();
      await waitFor(
        () => document.getElementById('batch-result-summary').textContent === 'Journal を読み取りました。'
          && document.getElementById('batch-journal-status').textContent.includes('identity が一致'),
        'recent journal reopen'
      );
      const reopenedPrefix = document.getElementById('batch-journal-prefix').textContent;

      return {
        default_tab: defaultTab,
        standard_heading: standardHeading,
        tab_labels: [...document.querySelectorAll('header .tab')].map((node) => node.textContent.trim()),
        queue_path: queuePath,
        change_set_path: changeSetPath,
        plan_job: planJob,
        plan_model: planModel,
        execute_job: executeJob,
        execute_model: executeModel,
        reopened_prefix: reopenedPrefix,
      };
    })()
  `), 260000, 'batch GUI workflow');

  const reset = await win.webContents.executeJavaScript(
    'window.nlmytgen.batchProbeResetRuntime()',
  );
  if (!reset?.ok) throw new Error(`batch runtime reset failed: ${reset?.error}`);
  const reloaded = new Promise((resolve) => win.webContents.once('did-finish-load', resolve));
  win.webContents.reload();
  await withTimeout(reloaded, 30000, 'batch application surface restart');
  const restart = await withTimeout(win.webContents.executeJavaScript(`
    (async () => {
      const waitFor = async (predicate, label, timeoutMs = 120000) => {
        const started = Date.now();
        while (!predicate()) {
          if (Date.now() - started > timeoutMs) throw new Error(label + ' timed out');
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      };
      await waitFor(
        () => document.readyState === 'complete'
          && window.__nlmytgenBatchProbe
          && document.getElementById('btn-batch-plan'),
        'restarted batch DOM'
      );
      const defaultTab = document.querySelector('.tab.active')?.dataset.tab;
      document.querySelector('[data-tab="batch"]').click();
      await waitFor(
        () => document.getElementById('batch-queue-path').textContent.includes('four_package_lifecycle_queue_v3'),
        'restarted default queue'
      );
      document.getElementById('btn-batch-plan').click();
      await waitFor(
        () => !window.__nlmytgenBatchProbe.snapshot().active
          && window.__nlmytgenBatchProbe.snapshot().readModel?.execution_mode === 'plan_only',
        'restarted actual plan'
      );
      document.getElementById('btn-batch-open-recent').click();
      await waitFor(
        () => document.getElementById('batch-result-summary').textContent === 'Journal を読み取りました。'
          && window.__nlmytgenBatchProbe.snapshot().readModel?.execution_mode === 'execute'
          && document.getElementById('batch-journal-status').textContent.includes('identity が一致'),
        'restarted journal reopen'
      );
      return {
        default_tab: defaultTab,
        plan_identity: window.__nlmytgenBatchProbe.snapshot().readModel.plan_identity_sha256,
        read_model_mode: window.__nlmytgenBatchProbe.snapshot().readModel.execution_mode,
        reopened_prefix: document.getElementById('batch-journal-prefix').textContent,
        journal_status: document.getElementById('batch-journal-status').textContent,
      };
    })()
  `), 180000, 'batch restart workflow');
  workflow.restart = restart;

  const variants = [
    'authority_wait',
    'running',
    'success',
    'failure',
    'effect_unknown',
    'long_text',
  ];
  const syntheticObservations = {};
  for (const variant of variants) {
    const model = syntheticModel(workflow.execute_model, variant);
    await win.webContents.executeJavaScript(`
      window.__nlmytgenBatchProbe.renderReadModel(
        ${JSON.stringify(model)},
        {
          validation: { ok: true },
          authoritySummary: { status: 'absent', exact: false }
        }
      )
    `);
    syntheticObservations[variant] = await win.webContents.executeJavaScript(`
      (() => ({
        rows: [...document.querySelectorAll('#batch-package-rows tr')].map((row) => row.innerText),
        authority: document.getElementById('batch-authority-status').textContent,
        resume: document.getElementById('batch-resume-state').textContent,
        resume_disabled: document.getElementById('btn-batch-resume').disabled,
        execute_disabled: document.getElementById('btn-batch-execute').disabled,
        document_overflow_x: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      }))()
    `);
  }

  await win.webContents.executeJavaScript(`
    window.__nlmytgenBatchProbe.renderReadModel(
      ${JSON.stringify(workflow.execute_model)},
      { validation: { ok: true }, authoritySummary: { status: 'not_required', exact: true } }
    )
  `);

  const keyboard = await win.webContents.executeJavaScript(`
    (() => {
      const ids = [
        'btn-batch-select-queue',
        'btn-batch-select-change-set',
        'btn-batch-plan',
        'btn-batch-execute',
        'btn-batch-select-authority',
        'btn-batch-select-journal',
        'btn-batch-resume',
        'btn-batch-cancel',
        'btn-batch-result-details',
      ];
      const focusables = [...document.querySelectorAll('button, summary, [tabindex]')];
      const enabledFocus = {};
      for (const id of ids) {
        const node = document.getElementById(id);
        if (!node || node.disabled) continue;
        node.focus();
        enabledFocus[id] = document.activeElement === node;
      }
      return {
        ids,
        dom_positions: ids.map((id) => focusables.findIndex((node) => node.id === id)),
        enabled_focus: enabledFocus,
      };
    })()
  `);

  const layouts = [
    await captureAt(win, 1280, 720, runRoot, 'batch'),
    await captureAt(win, 1920, 1080, runRoot, 'batch'),
  ];
  const positions = keyboard.dom_positions;
  const keyboardOrder = positions.every((position) => position >= 0)
    && positions.every((position, index) => index === 0 || position > positions[index - 1]);
  const boundaries = workflow.execute_model.boundaries || {};
  const actualRows = workflow.execute_model.rows || [];
  const checks = {
    electron_exact_43_2_0: process.versions.electron === '43.2.0',
    standard_route_remains_default: workflow.default_tab === 'standard',
    standard_route_heading_preserved: workflow.standard_heading === '自動動画生成',
    batch_route_secondary_and_discoverable: (
      workflow.tab_labels[0] === '自動動画生成'
      && workflow.tab_labels[1] === 'バッチ実行'
    ),
    actual_queue_v3_loaded: workflow.queue_path.endsWith('four_package_lifecycle_queue_v3.json'),
    actual_zero_change_set_loaded: workflow.change_set_path.endsWith('four_package_zero_change_set_v1.json'),
    actual_plan_only_completed: (
      workflow.plan_job.state === 'completed'
      && workflow.plan_model.execution_mode === 'plan_only'
      && workflow.plan_model.plan_identity_sha256
        === '0d07e9bb40dce6f9daa27496f6bac53e787a736cf72c8c151ca6f63d8f5561fa'
    ),
    actual_zero_change_execute_completed: (
      workflow.execute_job.state === 'completed'
      && workflow.execute_model.execution_mode === 'execute'
      && workflow.execute_model.result_message === '変更はありません'
    ),
    four_verified_noop_visible: (
      actualRows.length === 4
      && actualRows.every((row) => row.execution_state === 'verified_noop')
    ),
    backend_dispatch_zero: boundaries.backend_dispatch_count === 0,
    authority_consumption_zero: workflow.execute_model.counts.authority_consumptions === 0,
    source_generation_zero: boundaries.source_project_generation_count === 0,
    render_zero: boundaries.render_count === 0,
    yymm4_launch_zero: boundaries.yymm4_launch_count === 0,
    playback_zero: boundaries.playback_count === 0,
    product_write_zero: boundaries.product_write_count === 0,
    journal_prefix_reopened: (
      workflow.reopened_prefix
      && workflow.reopened_prefix
        === `${workflow.execute_model.journal.prefix_identity_sha256.slice(0, 12)}…${workflow.execute_model.journal.prefix_identity_sha256.slice(-8)}`
    ),
    application_restart_prefix_preserved: (
      workflow.restart.default_tab === 'standard'
      && workflow.restart.plan_identity === workflow.execute_model.plan_identity_sha256
      && workflow.restart.reopened_prefix === workflow.reopened_prefix
      && workflow.restart.journal_status.includes('identity が一致')
    ),
    authority_wait_visible: /authority|権限/.test(syntheticObservations.authority_wait.authority),
    running_visible: syntheticObservations.running.rows.some((row) => row.includes('実行中')),
    success_visible: syntheticObservations.success.rows.some((row) => row.includes('完了')),
    failure_and_skip_visible: (
      syntheticObservations.failure.rows.some((row) => row.includes('失敗'))
      && syntheticObservations.failure.rows.some((row) => row.includes('先行失敗'))
    ),
    effect_unknown_blocked: (
      syntheticObservations.effect_unknown.rows.some((row) => row.includes('作用結果不明'))
      && syntheticObservations.effect_unknown.resume_disabled === true
      && /自動再試行/.test(syntheticObservations.effect_unknown.resume)
    ),
    long_text_contained: syntheticObservations.long_text.document_overflow_x === false,
    keyboard_dom_order_valid: keyboardOrder,
    enabled_keyboard_actions_focusable: Object.values(keyboard.enabled_focus).every(Boolean),
    first_viewport_has_required_plan_context: layouts.every((layout) => (
      layout.queue?.top >= 0
      && layout.change_set?.top >= 0
      && layout.plan_status?.top >= 0
      && layout.mutation_count?.top >= 0
      && layout.primary_action?.top >= 0
      && layout.primary_action.top < layout.viewport.height
    )),
    no_horizontal_overflow: layouts.every((layout) => (
      layout.document_overflow_x === false && layout.main_overflow_x === false
    )),
    table_text_not_tiny: layouts.every((layout) => layout.table_font_px >= 11),
    shared_job_inactive_after_completion: workflow.execute_job.active === false,
    context_isolation_enabled: win.webContents.getLastWebPreferences().contextIsolation === true,
    node_integration_disabled: win.webContents.getLastWebPreferences().nodeIntegration === false,
    sandbox_enabled: win.webContents.getLastWebPreferences().sandbox === true,
    audio_policy_silent: process.env.NLMYTGEN_AUDIO_POLICY === 'silent',
    mute_audio_switch_enabled: app.commandLine.hasSwitch('mute-audio'),
    background_networking_disabled: app.commandLine.hasSwitch('disable-background-networking'),
    hidden_probe_did_not_show_window: win.isVisible() === false,
    no_console_errors: observations.console_errors.length === 0,
    no_security_warnings: observations.security_warnings.length === 0,
    no_load_failures: observations.load_failures.length === 0,
    no_renderer_crash: observations.render_process_gone.length === 0,
    no_preload_errors: observations.preload_errors.length === 0,
    no_unhandled_renderer_errors: observations.renderer_unhandled_errors.length === 0,
  };
  const status = Object.values(checks).every(Boolean) ? 'passed' : 'failed';
  writeReceipt({
    schema: 'nlmytgen.standard_gui_batch_observability_probe.v1',
    status,
    runtime: {
      electron: process.versions.electron,
      chrome: process.versions.chrome,
      node: process.versions.node,
      audio_policy: process.env.NLMYTGEN_AUDIO_POLICY,
    },
    checks,
    actual: workflow,
    synthetic: syntheticObservations,
    keyboard,
    layouts,
    observations,
    boundaries: {
      real_package_mutation: false,
      yymm4_launch: boundaries.yymm4_launch_count !== 0,
      render: boundaries.render_count !== 0,
      playback: boundaries.playback_count !== 0,
      public_action: boundaries.public_action_count !== 0,
    },
  });
  observations.dispose();
  win.destroy();
  setImmediate(() => app.exit(status === 'passed' ? 0 : 1));
}

function fail(error) {
  writeReceipt({
    schema: 'nlmytgen.standard_gui_batch_observability_probe.v1',
    status: 'failed',
    error: String(error?.stack || error?.message || error),
    runtime: {
      electron: process.versions.electron,
      chrome: process.versions.chrome,
      node: process.versions.node,
    },
  });
  process.exitCode = 1;
}

module.exports = {
  fail,
  isEnabled,
  observe,
  profilePath,
  run,
};

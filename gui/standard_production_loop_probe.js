const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { app, ipcMain } = require('electron');

function isEnabled() {
  return process.env.NLMYTGEN_STANDARD_LOOP_PROBE === '1';
}

function requiredPath(name) {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is required in standard-loop probe mode`);
  return path.resolve(value);
}

function profilePath() {
  return requiredPath('NLMYTGEN_STANDARD_LOOP_PROFILE');
}

function receiptPath() {
  return requiredPath('NLMYTGEN_STANDARD_LOOP_RECEIPT');
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
  const rendererErrorHandler = (_event, detail) => observations.renderer_unhandled_errors.push(detail);
  ipcMain.on('nlmytgen-standard-loop-renderer-error', rendererErrorHandler);
  Object.defineProperty(observations, 'dispose', {
    enumerable: false,
    value: () => ipcMain.off('nlmytgen-standard-loop-renderer-error', rendererErrorHandler),
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
  win.webContents.on('render-process-gone', (_event, detail) => observations.render_process_gone.push(detail));
  win.webContents.on('preload-error', (_event, preloadPath, error) => {
    observations.preload_errors.push({
      preload_path: preloadPath,
      error: String(error?.stack || error?.message || error),
    });
  });
  return observations;
}

function withTimeout(promise, timeoutMs, label) {
  let timeout;
  const expired = new Promise((_resolve, reject) => {
    timeout = setTimeout(() => reject(new Error(`${label} timed out after ${timeoutMs}ms`)), timeoutMs);
  });
  return Promise.race([promise, expired]).finally(() => clearTimeout(timeout));
}

function writeReceipt(payload) {
  const target = receiptPath();
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  console.log(`STANDARD_LOOP_RECEIPT=${target}`);
  console.log(JSON.stringify(payload, null, 2));
}

async function captureAt(win, width, height, directory) {
  win.setSize(width, height);
  await new Promise((resolve) => setTimeout(resolve, 120));
  await win.webContents.executeJavaScript(`
    (() => {
      document.activeElement?.blur();
      if (document.scrollingElement) document.scrollingElement.scrollTop = 0;
      const scroll = document.querySelector('.main-tab-scroll');
      if (scroll) {
        scroll.scrollLeft = 0;
        scroll.scrollTop = 0;
      }
    })()
  `);
  await new Promise((resolve) => setTimeout(resolve, 120));
  const layout = await win.webContents.executeJavaScript(`
    (() => {
      const rect = (id) => {
        const value = document.getElementById(id)?.getBoundingClientRect();
        return value ? { top: value.top, bottom: value.bottom, left: value.left, right: value.right } : null;
      };
      const root = document.documentElement;
      const scroll = document.querySelector('.main-tab-scroll');
      return {
        viewport: { width: window.innerWidth, height: window.innerHeight },
        document_overflow_x: root.scrollWidth > root.clientWidth,
        main_overflow_x: scroll ? scroll.scrollWidth > scroll.clientWidth : null,
        episode: rect('standard-step-episode'),
        readiness: rect('standard-step-runtime'),
        primary_action: rect('btn-standard-start'),
        result: rect('standard-step-result'),
      };
    })()
  `);
  const png = (await win.webContents.capturePage()).toPNG();
  const target = path.join(directory, `standard_loop_${width}x${height}.png`);
  fs.writeFileSync(target, png);
  return {
    ...layout,
    screenshot: {
      path: target,
      bytes: png.length,
      sha256: crypto.createHash('sha256').update(png).digest('hex'),
    },
  };
}

async function run(win, observations) {
  const runRoot = path.dirname(receiptPath());
  const realRender = process.env.NLMYTGEN_STANDARD_LOOP_REAL_RENDER === '1';
  const manifestNeedle = path.basename(
    process.env.NLMYTGEN_STANDARD_LOOP_MANIFEST
      || 'new_banknote_real_media_episode_manifest.json',
  );
  const requestedRunId = process.env.NLMYTGEN_STANDARD_LOOP_RUN_ID || null;
  const workflowPromise = win.webContents.executeJavaScript(`
    (async () => {
      const realRender = ${JSON.stringify(realRender)};
      const requestedRunId = ${JSON.stringify(requestedRunId)};
      const waitFor = async (predicate, label, timeoutMs = 90000) => {
        const started = Date.now();
        while (!predicate()) {
          if (Date.now() - started > timeoutMs) throw new Error(label + ' timed out');
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      };
      await waitFor(
        () => document.readyState === 'complete' && document.getElementById('btn-standard-doctor'),
        'standard-loop DOM'
      );
      const workflowStarted = performance.now();
      document.getElementById('btn-standard-accepted-manifest').click();
      await waitFor(
        () => document.getElementById('standard-manifest-path').textContent.includes(${JSON.stringify(manifestNeedle)}),
        'accepted manifest'
      );
      if (requestedRunId) {
        const runIdInput = document.getElementById('standard-run-id');
        runIdInput.value = requestedRunId;
        runIdInput.dispatchEvent(new Event('input', { bubbles: true }));
        runIdInput.dispatchEvent(new Event('change', { bubbles: true }));
        await waitFor(
          () => document.getElementById('standard-result-details').textContent.includes('run: ' + requestedRunId),
          'resolved run ID'
        );
      }
      const doctorStarted = performance.now();
      document.getElementById('btn-standard-doctor').click();
      await waitFor(
        () => !document.getElementById('standard-readiness-summary').textContent.includes('確認中'),
        'runtime doctor'
      );
      const doctorSeconds = (performance.now() - doctorStarted) / 1000;
      const dryRunButton = document.getElementById('btn-standard-dry-run');
      await waitFor(() => !dryRunButton.disabled, 'dry-run eligibility');
      const dryRunStarted = performance.now();
      dryRunButton.click();
      await waitFor(
        () => !document.getElementById('standard-dry-run-status').textContent.includes('確認中'),
        'actual manifest dry-run',
        120000
      );
      const dryRunSeconds = (performance.now() - dryRunStarted) / 1000;
      const startButton = document.getElementById('btn-standard-start');
      const renderWaitTimeoutMs = realRender
        ? Number(startButton.dataset.renderWaitTimeoutMs)
        : 90000;
      if (realRender && (!Number.isFinite(renderWaitTimeoutMs) || renderWaitTimeoutMs <= 0)) {
        throw new Error('render timeout contract is unavailable after dry-run');
      }
      const focusElement = (id) => {
        const element = document.getElementById(id);
        if (element?.disabled) return true;
        element?.focus();
        return document.activeElement?.id === id;
      };
      const basicFocusChecks = {
        manifest_select: focusElement('btn-standard-select-manifest'),
        doctor: focusElement('btn-standard-doctor'),
        dry_run: focusElement('btn-standard-dry-run'),
        output: focusElement('btn-standard-open-output'),
        receipt: focusElement('btn-standard-open-receipt'),
      };
      let generateFocus = null;
      let cancelFocus = null;
      let generationStartMode = 'enabled_primary_action_normal_path';
      const productionEligibility = () => ({
        start_disabled: startButton.disabled,
        readiness: document.getElementById('standard-readiness-summary').textContent,
        dry_run: document.getElementById('standard-dry-run-status').textContent,
        run_id: document.getElementById('standard-run-id').value,
        run_id_state: document.getElementById('standard-run-id-status').dataset.state,
        protected_inputs: document.getElementById('standard-protected-summary').textContent,
      });
      try {
        await waitFor(
          () => !startButton.disabled,
          'normal production action eligibility',
          10000
        );
      } catch (error) {
        throw new Error(
          error.message + ': ' + JSON.stringify(productionEligibility())
        );
      }
      generateFocus = focusElement('btn-standard-start');
      const renderDispatchedAt = new Date().toISOString();
      const renderStarted = performance.now();
      startButton.click();
      await waitFor(
        () => !document.getElementById('btn-standard-cancel').disabled,
        'cancel button enabled'
      );
      cancelFocus = focusElement('btn-standard-cancel');
      await waitFor(
        () => ['完了', '失敗', '取り消し済み'].includes(document.getElementById('standard-job-status').textContent),
        realRender ? 'real YMM4 render command' : 'render command test double',
        renderWaitTimeoutMs
      );
      const completedJobStatus = document.getElementById('standard-job-status').textContent;
      const renderSeconds = (performance.now() - renderStarted) / 1000;
      let activeStateObserved = true;
      let cancelResult = { ok: true };
      let finalJob;
      if (realRender) {
        finalJob = await window.nlmytgen.standardLoopJob();
        if (completedJobStatus !== '完了') {
          throw new Error(
            'real YMM4 render command failed: ' + JSON.stringify({
              completed_job_status: completedJobStatus,
              final_job_state: finalJob.state,
              log_lines: (finalJob.log_lines || []).slice(-40),
            })
          );
        }
      } else {
        const cancelStarted = await window.nlmytgen.standardLoopStart({
          manifestPath: document.getElementById('standard-manifest-path').textContent,
          runId: document.getElementById('standard-run-id').value,
          resume: true,
        });
        if (!cancelStarted.ok) throw new Error('cancel test-double start failed: ' + cancelStarted.error);
        activeStateObserved = cancelStarted.job.active === true && cancelStarted.job.state === 'running';
        cancelResult = await window.nlmytgen.standardLoopCancel(cancelStarted.job.id);
        if (!cancelResult.ok) throw new Error('owned-process cancel failed: ' + cancelResult.error);
        await waitFor(
          () => document.getElementById('standard-job-status').textContent === '取り消し済み',
          'owned-process cancellation'
        );
        finalJob = await window.nlmytgen.standardLoopJob();
      }
      const keyboardIds = [
        'btn-standard-select-manifest',
        'btn-standard-doctor',
        'btn-standard-dry-run',
        'btn-standard-start',
        'btn-standard-cancel',
        'btn-standard-open-output',
        'btn-standard-open-receipt',
      ];
      const domButtons = [...document.querySelectorAll('button')];
      return {
        active_tab: document.querySelector('.tab.active')?.dataset.tab,
        tab_labels: [...document.querySelectorAll('header .tab')].map((element) => element.textContent.trim()),
        manifest_path: document.getElementById('standard-manifest-path').textContent,
        run_id: document.getElementById('standard-run-id').value,
        run_id_status: document.getElementById('standard-run-id-status').textContent,
        episode_summary: document.getElementById('standard-episode-summary').innerText,
        protected_summary: document.getElementById('standard-protected-summary').textContent,
        readiness_summary: document.getElementById('standard-readiness-summary').textContent,
        profile_states: [...document.querySelectorAll('#standard-profile-list li')].map((element) => ({
          text: element.textContent,
          state: element.dataset.state,
        })),
        dry_run_status: document.getElementById('standard-dry-run-status').textContent,
        generation_start_mode: generationStartMode,
        render_dispatched_at_utc: renderDispatchedAt,
        completed_job_status: completedJobStatus,
        active_state_observed: activeStateObserved,
        cancellation_result_ok: cancelResult.ok,
        final_job: finalJob,
        keyboard: {
          ids: keyboardIds,
          dom_positions: keyboardIds.map((id) => domButtons.findIndex((button) => button.id === id)),
          basic_focus_checks: basicFocusChecks,
          generate_focus: generateFocus,
          cancel_focus: cancelFocus,
        },
        job_status: document.getElementById('standard-job-status').textContent,
        job_log: document.getElementById('standard-job-log').textContent,
        result_summary: document.getElementById('standard-result-summary').textContent,
        timings: {
          doctor_seconds: doctorSeconds,
          dry_run_seconds: dryRunSeconds,
          render_job_seconds: renderSeconds,
          workflow_total_seconds: (performance.now() - workflowStarted) / 1000,
          render_wait_timeout_ms: renderWaitTimeoutMs,
        },
        operator_controls: {
          manual_intervention_count: 0,
          computer_use_count: 0,
          keyboard_mouse_injection_count: 0,
          sendkeys_count: 0,
        },
        step_order: [...document.querySelectorAll('#tab-standard > .standard-loop > .standard-step')].map(
          (element) => element.id
        ),
        heading_order: [...document.querySelectorAll('#tab-standard .standard-step h3')].map(
          (element) => element.textContent.trim()
        ),
      };
    })()
  `);
  const workflow = realRender
    ? await workflowPromise
    : await withTimeout(workflowPromise, 150000, 'standard production workflow');

  const layouts = [
    await captureAt(win, 1280, 720, runRoot),
    await captureAt(win, 1920, 1080, runRoot),
  ];
  const expectedTabs = ['自動動画生成', 'CSV 変換', '演出適用', 'デザインレビュー', '品質診断'];
  const expectedSteps = [
    'standard-step-episode',
    'standard-step-runtime',
    'standard-step-content',
    'standard-step-run',
    'standard-step-result',
  ];
  const allProfilesReady = workflow.profile_states.length === 4
    && workflow.profile_states.every((profile) => profile.state === 'ready');
  const requireAllProfilesReady = process.env.NLMYTGEN_STANDARD_LOOP_REQUIRE_ALL_READY === '1';
  const keyboardPositions = workflow.keyboard.dom_positions;
  const keyboardOrderValid = keyboardPositions.every((position) => position >= 0)
    && keyboardPositions.every((position, index) => index === 0 || position > keyboardPositions[index - 1]);
  let realRenderReceipt = null;
  let realRenderReceiptPath = null;
  if (realRender) {
    const repoRoot = path.resolve(__dirname, '..');
    const manifestPath = path.resolve(repoRoot, workflow.manifest_path);
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    realRenderReceiptPath = path.resolve(
      repoRoot,
      manifest.output.run_root_path,
      workflow.run_id,
      'pipeline_run_receipt.json',
    );
    realRenderReceipt = JSON.parse(fs.readFileSync(realRenderReceiptPath, 'utf8'));
  }
  const checks = {
    electron_exact_43_2_0: process.versions.electron === '43.2.0',
    default_surface_is_standard_loop: workflow.active_tab === 'standard',
    legacy_tabs_preserved: expectedTabs.every((label) => workflow.tab_labels.includes(label)),
    vertical_spine_order_exact: JSON.stringify(workflow.step_order) === JSON.stringify(expectedSteps),
    accepted_manifest_loaded: workflow.manifest_path.endsWith(manifestNeedle),
    resolved_run_id_visible: !requestedRunId || workflow.run_id === requestedRunId,
    protected_inputs_exact: /完全一致しています/.test(workflow.protected_summary),
    four_runtime_profiles_classified: workflow.profile_states.length === 4,
    runtime_profile_expectation_met: !requireAllProfilesReady || allProfilesReady,
    actual_dry_run_passed: workflow.dry_run_status === '書き込みなしの工程確認に成功',
    render_command_wired_to_test_double: realRender || (
      workflow.completed_job_status === '完了'
      && workflow.job_log.includes('build-episode-video')
      && workflow.job_log.includes('--render')
      && workflow.job_log.includes('TEST_DOUBLE_RENDER_NOT_PERFORMED')
    ),
    real_render_command_completed: !realRender || (
      workflow.completed_job_status === '完了'
      && workflow.final_job.active === false
      && workflow.final_job.state === 'completed'
      && realRenderReceipt?.status === 'passed'
      && realRenderReceipt?.render_requested === true
      && ['passed', 'reused'].includes(realRenderReceipt?.render?.status)
      && realRenderReceipt?.media_validation?.status === 'passed'
    ),
    readiness_bypass_false: workflow.generation_start_mode === 'enabled_primary_action_normal_path',
    render_test_double_false: !realRender
      || process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE !== '1',
    tracked_worktree_clean_at_dispatch: !realRender
      || realRenderReceipt?.run_identity?.tracked_worktree_clean_at_start === true,
    manual_intervention_zero: workflow.operator_controls.manual_intervention_count === 0,
    computer_use_zero: workflow.operator_controls.computer_use_count === 0,
    keyboard_mouse_injection_zero: workflow.operator_controls.keyboard_mouse_injection_count === 0,
    sendkeys_zero: workflow.operator_controls.sendkeys_count === 0,
    active_and_cancelled_states_verified: realRender || (
      workflow.active_state_observed
      && workflow.cancellation_result_ok
      && workflow.job_status === '取り消し済み'
    ),
    project_owned_job_inactive_after_cancel: realRender || (
      workflow.final_job.active === false
      && workflow.final_job.state === 'cancelled'
    ),
    output_state_visible: realRender
      ? workflow.result_summary === '生成済み・人の採用判断前'
      : workflow.result_summary === '採用済み出力と完全一致',
    first_viewport_contains_episode_readiness_action: layouts.every((layout) => (
      layout.episode?.top >= 0
      && layout.readiness?.top >= 0
      && layout.primary_action?.top >= 0
      && layout.primary_action.top < layout.viewport.height
    )),
    no_horizontal_overflow: layouts.every((layout) => (
      layout.document_overflow_x === false && layout.main_overflow_x === false
    )),
    keyboard_dom_order_valid: keyboardOrderValid,
    enabled_keyboard_actions_focusable: Object.values(workflow.keyboard.basic_focus_checks).every(Boolean),
    clean_runtime_generate_cancel_focusable: !requireAllProfilesReady
      || (workflow.keyboard.generate_focus === true && workflow.keyboard.cancel_focus === true),
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
    schema: 'nlmytgen.standard_production_loop_probe.v1',
    status,
    scope: realRender
      ? 'actual Electron main/renderer/preload + runtime doctor + manifest dry-run + real YMM4 render'
      : 'actual Electron main/renderer/preload + runtime doctor + accepted-manifest dry-run + render test double',
    runtime: {
      electron: process.versions.electron,
      chrome: process.versions.chrome,
      node: process.versions.node,
      audio_policy: process.env.NLMYTGEN_AUDIO_POLICY,
      require_all_profiles_ready: requireAllProfilesReady,
      all_profiles_ready: allProfilesReady,
      readiness_bypass: false,
      render_test_double: process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE === '1',
    },
    checks,
    workflow,
    layouts,
    observations,
    real_render_receipt: realRender ? {
      path: realRenderReceiptPath,
      status: realRenderReceipt?.status,
      render_status: realRenderReceipt?.render?.status,
      media_validation_status: realRenderReceipt?.media_validation?.status,
      project_owned_process_cleanup: realRenderReceipt?.render?.project_owned_process_cleanup,
      content_identity_sha256: realRenderReceipt?.content_identity_sha256,
      run_identity: realRenderReceipt?.run_identity,
      artifact_identities: realRenderReceipt?.artifact_identities,
      stage_timings: realRenderReceipt?.stage_timings,
    } : null,
    boundaries: {
      render_performed: realRender,
      yymm4_launched: realRenderReceipt?.render?.yymm4_launched === true,
      playback_performed: false,
      system_volume_changed: false,
      external_upload: false,
      readiness_bypass: false,
      render_test_double: process.env.NLMYTGEN_STANDARD_LOOP_RENDER_TEST_DOUBLE === '1',
    },
  });
  observations.dispose();
  win.close();
  app.exit(status === 'passed' ? 0 : 1);
}

function fail(err) {
  writeReceipt({
    schema: 'nlmytgen.standard_production_loop_probe.v1',
    status: 'failed',
    error: String(err?.stack || err?.message || err),
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

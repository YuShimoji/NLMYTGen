(() => {
  const LOG_LIMIT = 240;
  const state = {
    queue: null,
    changeSet: null,
    authority: null,
    authoritySummary: null,
    journal: null,
    journalValidation: null,
    readModel: null,
    active: false,
    activeJobId: null,
    startedAt: null,
    elapsedTimer: null,
    logLines: [],
  };

  function element(id) {
    return document.getElementById(id);
  }

  function safeText(value, maxLength = 12000) {
    const text = String(value ?? '')
      .replace(/[A-Za-z]:\\Users\\[^\\\s]+/g, '<user-home>');
    return text.length <= maxLength ? text : `${text.slice(0, maxLength - 6)}…(省略)`;
  }

  function shortIdentity(value) {
    const text = safeText(value || '—', 128);
    return text.length > 20 ? `${text.slice(0, 12)}…${text.slice(-8)}` : text;
  }

  function setStatus(id, text, status = null) {
    const target = element(id);
    if (!target) return;
    target.textContent = safeText(text, 2000);
    if (status) target.dataset.state = status;
    else delete target.dataset.state;
  }

  function appendLog(lines) {
    for (const line of lines || []) state.logLines.push(safeText(line, 12000));
    if (state.logLines.length > LOG_LIMIT) {
      state.logLines.splice(0, state.logLines.length - LOG_LIMIT);
    }
    element('batch-job-log').textContent = state.logLines.join('\n') || 'ログはまだありません。';
  }

  function renderInputSelections() {
    element('batch-queue-path').textContent = state.queue?.display_path || '未読込';
    element('batch-change-set-path').textContent = state.changeSet?.display_path || '未読込';
    element('batch-authority-path').textContent = state.authority?.display_path || '未選択';
    element('batch-input-identities').textContent = [
      `queue: ${state.queue?.display_path || '—'}`,
      `queue sha256: ${state.queue?.sha256 || '—'}`,
      `change set: ${state.changeSet?.display_path || '—'}`,
      `change set sha256: ${state.changeSet?.sha256 || '—'}`,
    ].join('\n');
  }

  function clearPlan(message = '入力変更後は実行計画の再確認が必要です。') {
    state.readModel = null;
    state.journalValidation = null;
    setStatus('batch-plan-status', message);
    element('batch-plan-identity').textContent = '—';
    element('batch-package-count').textContent = '—';
    element('batch-mutation-count').textContent = '—';
    element('batch-next-action').textContent = '実行計画を確認';
    element('batch-package-rows').innerHTML = '<tr><td colspan="7">実行計画は未確認です。</td></tr>';
    setStatus('batch-primary-guidance', 'Queue と Change Set を確認し、実行計画を作成してください。');
    refreshActions();
  }

  function renderRows(rows) {
    const body = element('batch-package-rows');
    body.innerHTML = '';
    if (!rows?.length) {
      body.innerHTML = '<tr><td colspan="7">Package はありません。</td></tr>';
      return;
    }
    for (const row of rows) {
      const tr = document.createElement('tr');
      const values = [
        row.package_id,
        row.current_lifecycle,
        row.technical_decision,
        row.requested_operation || '—',
      ];
      for (const value of values) {
        const td = document.createElement('td');
        td.textContent = safeText(value, 520);
        tr.append(td);
      }
      const authority = document.createElement('td');
      authority.textContent = safeText(row.authority_label, 160);
      authority.dataset.tone = row.authority_tone;
      tr.append(authority);
      const execution = document.createElement('td');
      execution.textContent = `${safeText(row.execution_label, 120)}\n${safeText(row.execution_state, 120)}`;
      execution.dataset.tone = row.execution_tone;
      tr.append(execution);
      const context = document.createElement('td');
      const reason = document.createElement('span');
      reason.className = 'batch-reason';
      reason.textContent = safeText(row.reason, 520);
      const resume = document.createElement('span');
      resume.className = 'batch-resume-effect';
      resume.textContent = safeText(row.resume_effect, 320);
      context.append(reason, resume);
      tr.append(context);
      body.append(tr);
    }
  }

  function renderJournal(model, validation = state.journalValidation) {
    if (!model?.journal) {
      setStatus('batch-journal-status', 'Journal は未選択です。');
      element('batch-journal-prefix').textContent = '—';
      element('batch-journal-events').textContent = '—';
      element('batch-resume-state').textContent = '—';
      return;
    }
    const validationText = validation?.ok
      ? '現在の plan と identity が一致'
      : (validation?.error === 'PLAN_REQUIRED_FOR_RESUME'
        ? '再開判定には plan の再確認が必要'
        : (validation?.error ? `再開不可: ${validation.error}` : 'readback 完了'));
    setStatus(
      'batch-journal-status',
      `${model.journal.locator || 'local journal'} · ${validationText}`,
      validation?.ok ? 'ready' : null,
    );
    element('batch-journal-prefix').textContent = shortIdentity(model.journal.prefix_identity_sha256);
    element('batch-journal-events').textContent = String(model.journal.event_count);
    element('batch-resume-state').textContent = model.resume?.message || '—';
    element('batch-resume-state').dataset.state = model.resume?.state === 'reconciliation_required'
      ? 'blocked'
      : (model.resume?.eligible ? 'ready' : 'muted');
  }

  function renderAuthority(model) {
    const authority = model?.authority;
    if (!authority) {
      setStatus('batch-authority-status', '権限状態は実行計画の確認後に表示します。');
      return;
    }
    const labels = {
      not_required: 'この計画に authority は不要です。',
      absent: 'mutating entry には exact authority file が必要です。',
      required: 'plan と一致する authority file を選択してください。',
      invalid: '選択した authority は plan identity と一致しません。',
      available: 'exact one-shot authority の preflight に成功しました。',
      consumed: 'authority は使用済みです。再利用できません。',
      replacement_required: '失敗した entry には replacement authority が必要です。',
      reconciliation_required: 'effect の読み取り照合が完了するまで再実行できません。',
    };
    const current = state.authoritySummary?.status || authority.state;
    setStatus(
      'batch-authority-status',
      labels[current] || labels[authority.state] || `authority: ${current}`,
      current === 'not_required' || current === 'available' ? 'ready' : 'failed',
    );
    element('batch-authority-details').textContent = [
      `state: ${current}`,
      `mutating entries: ${model.mutating_entry_count}`,
      `plan-only consumes authority: false`,
      `no-op consumes authority: false`,
      `effect_unknown automatic retry: false`,
    ].join('\n');
  }

  function renderReadModel(model, {
    validation = state.journalValidation,
    source = 'executor',
  } = {}) {
    state.readModel = model;
    setStatus(
      'batch-plan-status',
      model.status === 'planned' ? '実行計画を確認済み' : '実行結果を確認済み',
      'ready',
    );
    element('batch-plan-identity').textContent = shortIdentity(model.plan_identity_sha256);
    element('batch-package-count').textContent = `${model.package_count} 件`;
    element('batch-mutation-count').textContent = `${model.mutating_entry_count} 件`;
    const nextAction = model.mutating_entry_count === 0
      ? '変更なしを実行して receipt を確認'
      : (state.authoritySummary?.status === 'available'
        ? 'exact authority で直列実行'
        : 'exact authority を選択');
    element('batch-next-action').textContent = nextAction;
    setStatus(
      'batch-primary-guidance',
      model.mutating_entry_count === 0
        ? '変更対象は0件です。zero-change batch を安全に実行できます。'
        : `${model.mutating_entry_count}件の変更対象があります。authority preflight が必要です。`,
    );
    renderRows(model.rows);
    renderAuthority(model);
    renderJournal(model, validation);
    setStatus(
      'batch-result-summary',
      source === 'journal' ? 'Journal を読み取りました。' : model.result_message,
      model.result_message === '変更はありません' || model.status === 'succeeded' ? 'ready' : null,
    );
    element('batch-result-details').textContent = JSON.stringify(model, null, 2);
    refreshActions();
  }

  function renderElapsed() {
    if (!state.active || !state.startedAt) return;
    const elapsed = Math.max(0, Math.floor((Date.now() - state.startedAt) / 1000));
    const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const seconds = String(elapsed % 60).padStart(2, '0');
    setStatus('batch-plan-status', `実行中 ${minutes}:${seconds}`);
  }

  function startElapsed(startedAt) {
    if (state.elapsedTimer) clearInterval(state.elapsedTimer);
    state.startedAt = Number.isFinite(Date.parse(startedAt)) ? Date.parse(startedAt) : Date.now();
    renderElapsed();
    state.elapsedTimer = setInterval(renderElapsed, 1000);
  }

  function stopElapsed() {
    if (state.elapsedTimer) clearInterval(state.elapsedTimer);
    state.elapsedTimer = null;
    state.startedAt = null;
  }

  function executionReady() {
    if (!state.readModel || state.active) return false;
    if (state.readModel.mutating_entry_count === 0) return true;
    return state.authoritySummary?.status === 'available'
      && state.authoritySummary?.exact === true;
  }

  function refreshActions() {
    element('btn-batch-plan').disabled = state.active || !state.queue || !state.changeSet;
    element('btn-batch-execute').disabled = !executionReady();
    element('btn-batch-execute').textContent = state.readModel?.mutating_entry_count === 0
      ? '変更なしを実行'
      : 'バッチを実行';
    const resumeExact = state.journalValidation?.ok === true;
    const resumeSafe = state.readModel?.resume?.eligible === true
      && state.readModel?.resume?.state !== 'reconciliation_required';
    element('btn-batch-resume').disabled = state.active || !resumeExact || !resumeSafe
      || (state.readModel.mutating_entry_count > 0 && state.authoritySummary?.status !== 'available');
    element('btn-batch-cancel').disabled = !state.active;
    element('btn-batch-select-authority').disabled = state.active;
    element('btn-batch-select-journal').disabled = state.active;
    element('btn-batch-open-recent').disabled = state.active;
  }

  async function loadDefaults() {
    const result = await window.nlmytgen.batchDefaultSelections();
    if (!result?.ok) {
      setStatus('batch-plan-status', result?.error || '既定入力の読込に失敗', 'failed');
      return;
    }
    state.queue = result.queue;
    state.changeSet = result.change_set;
    state.authority = result.authority || null;
    renderInputSelections();
    clearPlan('未確認');
  }

  async function selectInput(kind) {
    const result = await window.nlmytgen.batchSelectFile(kind);
    if (!result?.ok) {
      if (!result?.canceled) setStatus('batch-plan-status', result?.error || '選択失敗', 'failed');
      return;
    }
    if (kind === 'queue') state.queue = result.selection;
    if (kind === 'change_set') state.changeSet = result.selection;
    if (kind === 'authority') {
      state.authority = result.selection;
      state.authoritySummary = result.authority;
      renderInputSelections();
      if (state.readModel) renderAuthority(state.readModel);
      refreshActions();
      return;
    }
    renderInputSelections();
    clearPlan();
  }

  async function loadJournal(result) {
    if (!result?.ok) {
      setStatus('batch-journal-status', result?.error || 'Journal の読込に失敗', 'failed');
      return;
    }
    state.journal = result.selection;
    state.journalValidation = result.journal.validation;
    state.authority = null;
    state.authoritySummary = result.journal.authority || null;
    renderInputSelections();
    renderReadModel(result.journal.read_model, {
      validation: result.journal.validation,
      source: 'journal',
    });
  }

  async function startBatch(execute, resume = false) {
    state.logLines = [];
    appendLog([execute ? 'bounded batch executor を開始します。' : 'plan-only executor を開始します。']);
    const result = await window.nlmytgen.batchStart({
      queueSelectionId: state.queue?.selection_id,
      changeSetSelectionId: state.changeSet?.selection_id,
      authoritySelectionId: state.authority?.selection_id || null,
      journalSelectionId: resume ? (state.journal?.selection_id || null) : null,
      execute,
    });
    if (!result?.ok) {
      appendLog([`開始失敗: ${result?.error || 'unknown error'}`]);
      setStatus('batch-plan-status', '開始失敗', 'failed');
      state.active = false;
      refreshActions();
      return;
    }
    state.active = true;
    state.activeJobId = result.job.id;
    startElapsed(result.job.started_at);
    refreshActions();
  }

  async function cancelBatch() {
    if (!state.activeJobId) return;
    setStatus('batch-plan-status', '取消中');
    const result = await window.nlmytgen.batchCancel(state.activeJobId);
    if (!result?.ok) appendLog([`取消失敗: ${result?.error || 'unknown error'}`]);
  }

  function initBatchSurface() {
    element('btn-batch-select-queue').addEventListener('click', () => selectInput('queue'));
    element('btn-batch-select-change-set').addEventListener('click', () => selectInput('change_set'));
    element('btn-batch-plan').addEventListener('click', () => startBatch(false));
    element('btn-batch-execute').addEventListener('click', () => startBatch(true));
    element('btn-batch-select-authority').addEventListener('click', () => selectInput('authority'));
    element('btn-batch-select-journal').addEventListener('click', async () => {
      await loadJournal(await window.nlmytgen.batchSelectFile('journal'));
    });
    element('btn-batch-open-recent').addEventListener('click', async () => {
      await loadJournal(await window.nlmytgen.batchOpenRecentJournal());
    });
    element('btn-batch-resume').addEventListener('click', () => startBatch(true, true));
    element('btn-batch-cancel').addEventListener('click', cancelBatch);
    window.nlmytgen.onBatchJobEvent((event) => {
      if (event.kind !== 'batch') return;
      if (event.type === 'started') {
        state.active = true;
        state.activeJobId = event.id;
        startElapsed(event.started_at);
      }
      if (event.type === 'log') appendLog(event.lines);
      if (event.type === 'cancelling') setStatus('batch-plan-status', '取消中');
      if (event.type === 'finished') {
        state.active = false;
        state.activeJobId = null;
        stopElapsed();
        appendLog(event.log_lines || []);
        if (event.result?.ok && event.result.read_model) {
          state.journal = {
            selection_id: event.result.journal_selection_id,
            display_path: event.result.read_model.journal.locator,
          };
          state.journalValidation = { ok: true };
          renderReadModel(event.result.read_model);
        } else {
          setStatus(
            'batch-plan-status',
            event.state === 'cancelled' ? '取り消し済み' : '実行失敗',
            event.state === 'cancelled' ? null : 'failed',
          );
          setStatus(
            'batch-result-summary',
            event.result?.detail || event.result?.error || 'executor process が失敗しました。',
            'failed',
          );
        }
        refreshActions();
      }
    });
    loadDefaults();
    refreshActions();

    if (window.nlmytgen.runtimeMode?.batchProbe) {
      window.__nlmytgenBatchProbe = {
        renderReadModel: (model, options) => {
          state.journalValidation = options?.validation || null;
          state.authoritySummary = options?.authoritySummary || state.authoritySummary;
          renderReadModel(model, options);
        },
        snapshot: () => ({
          active: state.active,
          readModel: state.readModel,
          journalValidation: state.journalValidation,
        }),
      };
    }
  }

  window.addEventListener('DOMContentLoaded', initBatchSurface);
})();

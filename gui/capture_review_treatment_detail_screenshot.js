const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const DEFAULT_SCREENSHOT = 'samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot.png';
const DEFAULT_READBACK = 'samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot_readback.json';

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2);
    const value = argv[index + 1] && !argv[index + 1].startsWith('--') ? argv[index + 1] : 'true';
    args[key] = value;
    if (value !== 'true') index += 1;
  }
  return args;
}

function resolveRepoPath(relPath) {
  const fullPath = path.resolve(repoRoot, relPath);
  const relative = path.relative(repoRoot, fullPath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`path outside repo is not allowed: ${relPath}`);
  }
  return fullPath;
}

function toRepoPath(fullPath) {
  return path.relative(repoRoot, fullPath).replace(/\\/g, '/');
}

function writeJson(relPath, payload) {
  const fullPath = resolveRepoPath(relPath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  return fullPath;
}

async function waitForReviewWorkbench(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const switchToReview = () => {
        if (typeof switchMainTab === 'function') {
          switchMainTab('review', { alignWizard: false });
        } else {
          document.querySelector('[data-tab="review"]')?.click();
        }
        document.querySelector('[data-review-index="1"]')?.click();
      };
      const snapshot = () => {
        switchToReview();
        const proof = document.getElementById('review-treatment-proof');
        const reviewTab = document.getElementById('tab-review');
        const wizard = document.getElementById('wizard-bar');
        const activeTab = document.querySelector('.tab.active');
        const activeContent = document.querySelector('.tab-content.active');
        const proofImage = proof?.querySelector('.review-proof-image-card img');
        const text = reviewTab?.innerText || '';
        return {
          active_tab: activeTab?.dataset?.tab || '',
          active_content_id: activeContent?.id || '',
          active_review_tab: activeTab?.dataset?.tab === 'review',
          active_review_content: activeContent?.id === 'tab-review',
          visible_is_design_review: !!reviewTab && getComputedStyle(reviewTab).display !== 'none',
          visible_is_not_csv_tab: activeContent?.id !== 'tab-csv',
          wizard_display: wizard ? getComputedStyle(wizard).display : '',
          proof_image_visible: !!proofImage,
          proof_image_src: proofImage?.getAttribute('src') || '',
          beat_table_visible: !!proof?.querySelector('.review-beat-table'),
          sidecar_warnings_visible: text.includes('sidecar warnings'),
          anti_pattern_visible: text.includes('anti-pattern corpus') && text.includes('Production assetでもlayout見本でもありません'),
          additional_checks_visible: text.includes('label-off check') && text.includes('at_least_partial_pass') && text.includes('pass_or_strong_partial'),
          motion_primitives_visible: text.includes('motion primitives') && text.includes('enter:') && text.includes('reveal:') && text.includes('dim:'),
          frame_contract_violation_count_visible: text.includes('Frame Contract違反'),
          read_only_decision_context_visible: text.includes('read-only decision context'),
          proof_targets_visible: text.includes('RE-02') && text.includes('RE-06') && text.includes('RE-07D'),
          proof_revision_visible: text.includes('9-frame visual treatment proof v2'),
          has_corruption: /\\?\\?\\?|�/.test(text),
          width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
          height: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
          text_sample: text.slice(0, 500),
        };
      };
      const tick = () => {
        const state = snapshot();
        const ready = state.active_review_tab
          && state.active_review_content
          && state.visible_is_design_review
          && state.visible_is_not_csv_tab
          && state.wizard_display === 'none'
          && state.proof_image_visible
          && state.beat_table_visible
          && state.sidecar_warnings_visible
          && state.anti_pattern_visible
          && state.additional_checks_visible
          && state.motion_primitives_visible
          && state.frame_contract_violation_count_visible
          && state.read_only_decision_context_visible
          && state.proof_targets_visible
          && state.proof_revision_visible
          && !state.has_corruption;
        if (ready) {
          resolve(state);
          return;
        }
        if (Date.now() - started > 6000) {
          reject(new Error('GUI treatment proof was not visible in review tab: ' + JSON.stringify(state)));
          return;
        }
        setTimeout(tick, 100);
      };
      tick();
    })
  `);
}

function waitForNextPaint(win) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      win.webContents.off('paint', onPaint);
      reject(new Error('timed out waiting for offscreen paint'));
    }, 5000);
    function onPaint(_event, _dirty, image) {
      clearTimeout(timer);
      win.webContents.off('paint', onPaint);
      resolve(image);
    }
    win.webContents.on('paint', onPaint);
    win.webContents.invalidate();
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const screenshotRel = args.screenshot || DEFAULT_SCREENSHOT;
  const readbackRel = args.readback || DEFAULT_READBACK;
  const screenshotFull = resolveRepoPath(screenshotRel);
  fs.mkdirSync(path.dirname(screenshotFull), { recursive: true });

  await app.whenReady();

  const win = new BrowserWindow({
    show: false,
    width: 1500,
    height: 1100,
    webPreferences: {
      offscreen: true,
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      preload: path.join(__dirname, 'review_console_smoke_preload.js'),
    },
  });

  try {
    await win.loadFile(path.join(__dirname, 'index.html'));
    const state = await waitForReviewWorkbench(win);
    await win.webContents.executeJavaScript(`
      document.getElementById('review-treatment-proof')?.scrollIntoView({ block: 'start' });
    `);
    await new Promise((resolve) => setTimeout(resolve, 500));
    const image = await waitForNextPaint(win);
    fs.writeFileSync(screenshotFull, image.toPNG());

    const readback = {
      status: 'passed',
      screenshot_artifact: toRepoPath(screenshotFull),
      screenshot_capture_method: 'Electron offscreen BrowserWindow.loadFile(gui/index.html) + switchMainTab(review, alignWizard=false) + select RE-02 + scroll to proof + paint event PNG',
      not_csv_tab: state.visible_is_not_csv_tab,
      not_standalone_html_png_json_review: true,
      active_review_tab: state.active_review_tab,
      active_review_content: state.active_review_content,
      visible_is_design_review: state.visible_is_design_review,
      proof_image_visible: state.proof_image_visible,
      beat_table_visible: state.beat_table_visible,
      sidecar_warnings_visible: state.sidecar_warnings_visible,
      anti_pattern_visible: state.anti_pattern_visible,
      additional_checks_visible: state.additional_checks_visible,
      motion_primitives_visible: state.motion_primitives_visible,
      frame_contract_violation_count_visible: state.frame_contract_violation_count_visible,
      read_only_decision_context_visible: state.read_only_decision_context_visible,
      proof_targets_visible: state.proof_targets_visible,
      proof_revision_visible: state.proof_revision_visible,
      has_corruption: state.has_corruption,
      screenshot_width: image.getSize().width,
      screenshot_height: image.getSize().height,
    };
    writeJson(readbackRel, readback);
    console.log(JSON.stringify(readback, null, 2));
  } finally {
    win.close();
    app.quit();
  }
}

main().catch((err) => {
  console.error(err.stack || err.message || String(err));
  app.quit();
  process.exitCode = 1;
});

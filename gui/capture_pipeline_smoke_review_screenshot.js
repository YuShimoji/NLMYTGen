const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const DEFAULT_SCREENSHOT = 'samples/_probe/pipeline_smoke/pipeline_smoke_gui_screenshot.png';
const DEFAULT_READBACK = 'samples/_probe/pipeline_smoke/pipeline_smoke_gui_screenshot_readback.json';

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

function waitForNextPaint(win) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      win.webContents.off('paint', onPaint);
      reject(new Error('timed out waiting for pipeline smoke paint'));
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

async function waitForPipelineSmoke(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = () => {
        if (typeof switchMainTab === 'function') switchMainTab('review', { alignWizard: false });
        const panel = document.getElementById('pipeline-smoke-review');
        panel?.scrollIntoView({ block: 'start' });
        const topics = Array.from(panel?.querySelectorAll('.pipeline-smoke-topic') || []);
        const images = Array.from(panel?.querySelectorAll('.review-proof-image-card img') || []);
        const rows = Array.from(panel?.querySelectorAll('.review-beat-table tbody tr') || []);
        const text = panel?.innerText || '';
        const ready = topics.length === 3
          && images.length === 3
          && rows.length === 9
          && text.includes('Real Estate DX baseline')
          && text.includes('AI monitoring labor')
          && text.includes('Baseball news infographic')
          && text.includes('blocked reason')
          && text.includes('next action')
          && text.includes('standalone completion: false')
          && !/\\?\\?\\?|�/.test(text);
        if (ready) {
          resolve({
            topic_count: topics.length,
            image_count: images.length,
            beat_row_count: rows.length,
            has_blocked: text.includes('blocked'),
            has_reviewable: text.includes('reviewable'),
            has_decision_paths: text.includes('review_decisions.json'),
            has_standalone_guard: text.includes('standalone completion: false'),
            text_sample: text.slice(0, 500),
          });
          return;
        }
        if (Date.now() - started > 6000) {
          reject(new Error('pipeline smoke panel not ready: ' + JSON.stringify({ topics: topics.length, images: images.length, rows: rows.length, text: text.slice(0, 500) })));
          return;
        }
        setTimeout(tick, 100);
      };
      tick();
    })
  `);
}

async function main() {
  app.setPath('userData', path.join(repoRoot, '_tmp', 'electron_pipeline_smoke_gui_screenshot'));
  await app.whenReady();
  const screenshotFull = resolveRepoPath(DEFAULT_SCREENSHOT);
  fs.mkdirSync(path.dirname(screenshotFull), { recursive: true });
  const win = new BrowserWindow({
    show: false,
    width: 1500,
    height: 1200,
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
    const state = await waitForPipelineSmoke(win);
    await new Promise((resolve) => setTimeout(resolve, 500));
    const image = await waitForNextPaint(win);
    fs.writeFileSync(screenshotFull, image.toPNG());
    const readback = {
      status: 'passed',
      screenshot_artifact: toRepoPath(screenshotFull),
      screenshot_capture_method: 'Electron offscreen GUI review tab + pipeline smoke panel + paint event PNG',
      not_standalone_html_png_json_review: true,
      not_ymm4_adapter_output: true,
      not_render_source: true,
      not_production_timing: true,
      not_creative_acceptance: true,
      ...state,
      screenshot_width: image.getSize().width,
      screenshot_height: image.getSize().height,
    };
    writeJson(DEFAULT_READBACK, readback);
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

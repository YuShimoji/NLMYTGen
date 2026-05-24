const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');

const DEFAULT_HTML = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html';
const DEFAULT_READBACK = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review_readback.json';
const DEFAULT_VALIDATOR = 'samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json';
const DEFAULT_SCREENSHOT = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot.png';
const DEFAULT_SCREENSHOT_READBACK = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot_readback.json';

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2);
    const value = argv[index + 1] && !argv[index + 1].startsWith('--')
      ? argv[index + 1]
      : 'true';
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

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(resolveRepoPath(relPath), 'utf8'));
}

function assertArrayEqual(name, left, right) {
  const leftJson = JSON.stringify(left);
  const rightJson = JSON.stringify(right);
  if (leftJson !== rightJson) {
    throw new Error(`${name} mismatch:\nleft=${leftJson}\nright=${rightJson}`);
  }
}

async function waitForDom(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = () => {
        try {
          const segments = Array.from(document.querySelectorAll('.segment'));
          const cards = Array.from(document.querySelectorAll('.card'));
          const notices = Array.from(document.querySelectorAll('.notice'));
          const segmentTitles = segments.map((segment) => segment.querySelector('h2')?.innerText || '');
          const ready = document.readyState === 'complete'
            && segments.length === 11
            && cards.length === 24
            && segmentTitles[0]?.startsWith('RE-01')
            && segmentTitles[segmentTitles.length - 1]?.startsWith('RE-07E');
          if (ready) {
            const page = document.documentElement;
            resolve({
              segment_count: segments.length,
              placeholder_count: cards.length,
              notice_count: notices.length,
              segment_titles: segmentTitles,
              scroll_width: Math.ceil(Math.max(page.scrollWidth, document.body.scrollWidth)),
              scroll_height: Math.ceil(Math.max(page.scrollHeight, document.body.scrollHeight)),
              has_corruption_marker: /\\?\\?\\?|�/.test(document.body.innerText || ''),
              all_segments_have_notice: notices.length === segments.length,
            });
            return;
          }
          if (Date.now() - started > 5000) {
            reject(new Error('overlay compact review DOM did not become ready: ' + JSON.stringify({
              readyState: document.readyState,
              segments: segments.length,
              cards: cards.length,
              segmentTitles,
            })));
            return;
          }
          setTimeout(tick, 50);
        } catch (err) {
          reject(err);
        }
      };
      tick();
    })
  `);
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const htmlRel = args.html || DEFAULT_HTML;
  const readbackRel = args.readback || DEFAULT_READBACK;
  const validatorRel = args.validator || DEFAULT_VALIDATOR;
  const screenshotRel = args.output || DEFAULT_SCREENSHOT;
  const screenshotReadbackRel = args.report || DEFAULT_SCREENSHOT_READBACK;

  const htmlPath = resolveRepoPath(htmlRel);
  const screenshotPath = resolveRepoPath(screenshotRel);
  const screenshotReadbackPath = resolveRepoPath(screenshotReadbackRel);
  fs.mkdirSync(path.dirname(screenshotPath), { recursive: true });
  fs.mkdirSync(path.dirname(screenshotReadbackPath), { recursive: true });

  const readback = readJson(readbackRel);
  const validator = readJson(validatorRel);
  if (readback.status !== 'passed') {
    throw new Error(`overlay readback status is not passed: ${readback.status}`);
  }
  if (readback.is_creative_acceptance !== false) {
    throw new Error('overlay readback must not be creative acceptance');
  }
  if (readback.checks?.segments !== 11) {
    throw new Error(`readback segment count mismatch: ${readback.checks?.segments}`);
  }
  if (readback.checks?.placeholder_items_rendered !== 24) {
    throw new Error(`readback placeholder count mismatch: ${readback.checks?.placeholder_items_rendered}`);
  }
  assertArrayEqual('remaining blockers', readback.remaining_blockers || [], validator.blockers || []);

  app.commandLine.appendSwitch('disable-gpu');
  await app.whenReady();

  const win = new BrowserWindow({
    show: false,
    width: 1500,
    height: 1000,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  await win.loadFile(htmlPath);
  const dom = await waitForDom(win);
  if (dom.has_corruption_marker) {
    throw new Error('overlay compact review contains ??? or replacement character');
  }
  if (!dom.all_segments_have_notice) {
    throw new Error(`expected each segment to have a blocker notice, got ${dom.notice_count} notices`);
  }

  const captureWidth = Math.min(Math.max(dom.scroll_width, 1200), 2200);
  const captureHeight = Math.min(Math.max(dom.scroll_height, 1000), 20000);
  win.setContentSize(captureWidth, Math.min(captureHeight, 12000));
  await new Promise((resolve) => setTimeout(resolve, 200));

  const image = await win.webContents.capturePage({
    x: 0,
    y: 0,
    width: captureWidth,
    height: captureHeight,
  });
  fs.writeFileSync(screenshotPath, image.toPNG());
  const imageSize = image.getSize();

  const report = {
    status: 'passed',
    screenshot_artifact: toRepoPath(screenshotPath),
    screenshot_capture_method: 'electron BrowserWindow.loadFile + webContents.capturePage(full-page rect)',
    source_html: toRepoPath(htmlPath),
    source_readback: readbackRel,
    validator_result: validatorRel,
    not_creative_acceptance: true,
    checks: {
      readback_status: readback.status,
      readback_segments: readback.checks?.segments,
      dom_segments: dom.segment_count,
      segment_titles: dom.segment_titles,
      readback_placeholder_items_expected: readback.checks?.placeholder_items_expected,
      readback_placeholder_items_rendered: readback.checks?.placeholder_items_rendered,
      dom_placeholders: dom.placeholder_count,
      all_segments_visible_in_dom: dom.segment_count === 11,
      all_placeholders_visible_in_dom: dom.placeholder_count === 24,
      each_segment_has_blocker_notice: dom.all_segments_have_notice,
      remaining_blockers_match_validator: true,
      screenshot_pixels: {
        width: imageSize.width,
        height: imageSize.height,
      },
      captured_page_pixels: {
        width: captureWidth,
        height: captureHeight,
      },
    },
    allowed_next_actions: readback.allowed_next_actions || [],
    forbidden_next_actions: readback.forbidden_next_actions || [],
    remaining_blockers: readback.remaining_blockers || [],
  };
  fs.writeFileSync(screenshotReadbackPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(report, null, 2));

  await win.close();
  app.quit();
}

run().catch((err) => {
  console.error(err.stack || err.message || String(err));
  app.exit(1);
});

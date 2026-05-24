// Capture a 1920x1080 screenshot of the diagnostic carrier HTML proof via Electron.
// Visualization-only. Not a render, not creative acceptance, not production timing.
// Hidden items (G27PBD_Arrow) are intentionally not visualized.

const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const HTML_PATH = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_proof.html';
const READBACK_PATH = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_readback.json';
const SCREENSHOT_PATH = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_screenshot.png';
const SCREENSHOT_READBACK_PATH = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_screenshot_readback.json';

function abs(rel) {
  return path.resolve(repoRoot, rel);
}

function relRepo(p) {
  return path.relative(repoRoot, p).replace(/\\/g, '/');
}

function readJson(rel) {
  return JSON.parse(fs.readFileSync(abs(rel), 'utf8').replace(/^﻿/, ''));
}

app.disableHardwareAcceleration();
app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('in-process-gpu');
app.commandLine.appendSwitch('use-gl', 'swiftshader');
app.commandLine.appendSwitch('enable-features', 'UseSkiaRenderer');

async function run() {
  await app.whenReady();
  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    show: false,
    useContentSize: true,
    backgroundColor: '#000000',
    webPreferences: {
      offscreen: true,
      contextIsolation: true,
    },
  });

  const fileUrl = `file://${abs(HTML_PATH).replace(/\\/g, '/')}?no_meta=1&guides=0`;
  await win.loadURL(fileUrl);

  // Wait for SVG content to be parsed and laid out
  await win.webContents.executeJavaScript(
    "new Promise((resolve) => { const tick = () => { const svg = document.querySelector('svg'); if (svg && document.readyState === 'complete' && svg.querySelectorAll('rect[data-name], text[data-name]').length >= 12) { resolve(true); } else { setTimeout(tick, 40); } }; tick(); });"
  );

  // small additional settle for font fallbacks
  await new Promise((r) => setTimeout(r, 150));

  const buffer = await win.webContents.capturePage();
  fs.writeFileSync(abs(SCREENSHOT_PATH), buffer.toPNG());

  const domSummary = JSON.parse(
    await win.webContents.executeJavaScript(
      "JSON.stringify({" +
        "rects: document.querySelectorAll('rect[data-name]').length," +
        "texts: document.querySelectorAll('text[data-name]').length," +
        "hidden_comments: (document.documentElement.outerHTML.match(/<!-- hidden: /g) || []).length," +
        "guides_visible: document.querySelectorAll('[data-guide]').length," +
        "viewport: { width: window.innerWidth, height: window.innerHeight }," +
        "svg_view_box: document.querySelector('svg').getAttribute('viewBox')," +
        "first_text_content: document.querySelectorAll('text[data-name]')[0]?.textContent || null," +
        "has_corruption_marker: /\\?\\?\\?|\\uFFFD/.test(document.body.innerText || '')" +
        "});"
    )
  );

  const carrier = readJson(READBACK_PATH);
  const screenshotReadback = {
    artifact_type: 'g27_diagnostic_carrier_screenshot_readback',
    captured_at: new Date().toISOString(),
    source_html: relRepo(abs(HTML_PATH)),
    source_readback: relRepo(abs(READBACK_PATH)),
    screenshot: relRepo(abs(SCREENSHOT_PATH)),
    capture_url_query: '?no_meta=1&guides=0',
    viewport: { width: 1920, height: 1080 },
    dom: domSummary,
    carrier_status: carrier.status,
    carrier_totals: carrier.totals,
    carrier_compliance: {
      composition_type: carrier.scs_compliance.composition_type,
      element_count: carrier.scs_compliance.element_count,
      element_count_check: carrier.scs_compliance.element_count_check,
      reading_order: carrier.scs_compliance.reading_order,
      safe_area_check: carrier.scs_compliance.safe_area_check,
      subtitle_clearance_check: carrier.scs_compliance.subtitle_clearance_check,
      shape_size_mode_check: carrier.scs_compliance.shape_size_mode_check,
      color_format_check: carrier.scs_compliance.color_format_check,
      typography_hierarchy_check: carrier.scs_compliance.typography_hierarchy_check,
      composition_violation_count: carrier.scs_compliance.composition_violations.length,
      composition_hard_failure_count: carrier.totals.composition_hard_failure_count,
    },
    boundary: {
      render_performed: false,
      timing_adjusted: false,
      creative_acceptance_performed: false,
      production_carrier_replaced: false,
      visualization_only: true,
      ymm4_gui_used: false,
    },
  };
  fs.writeFileSync(abs(SCREENSHOT_READBACK_PATH), `${JSON.stringify(screenshotReadback, null, 2)}\n`);

  console.log(`screenshot: ${relRepo(abs(SCREENSHOT_PATH))}`);
  console.log(`readback: ${relRepo(abs(SCREENSHOT_READBACK_PATH))}`);
  console.log(`dom: rects=${domSummary.rects}, texts=${domSummary.texts}, hidden=${domSummary.hidden_comments}, corruption=${domSummary.has_corruption_marker}`);
  console.log(`carrier: status=${carrier.status}, composition=${carrier.scs_compliance.composition_type}, hard_fail=${carrier.totals.composition_hard_failure_count}`);

  app.quit();
}

run().catch((err) => {
  console.error(err.stack || err.message || err);
  process.exit(1);
});

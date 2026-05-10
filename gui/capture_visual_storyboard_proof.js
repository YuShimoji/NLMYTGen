const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');

const DEFAULT_MANIFEST = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.json';
const DEFAULT_OVERLAY_READBACK = 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review_readback.json';
const DEFAULT_VALIDATOR = 'samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json';
const DEFAULT_HTML = 'samples/_probe/g24/real_estate_dx_visual_storyboard_proof.html';
const DEFAULT_SCREENSHOT = 'samples/_probe/g24/real_estate_dx_visual_storyboard_proof.png';
const DEFAULT_READBACK = 'samples/_probe/g24/real_estate_dx_visual_storyboard_proof_readback.json';

const SEGMENT_SCENE = {
  'RE-01': { bg: 'search', cast: ['consumer'], mood: '検索自由化' },
  'RE-02': { bg: 'gate', cast: ['consumer', 'gatekeeper'], mood: '制度的ゲート' },
  'RE-03': { bg: 'shield', cast: ['consumer', 'gatekeeper'], mood: '保護理由と利害' },
  'RE-04': { bg: 'contract', cast: ['seller', 'agent', 'buyer'], mood: '囲い込み' },
  'RE-05': { bg: 'transparent', cast: ['consumer', 'gatekeeper'], mood: '透明化' },
  'RE-06': { bg: 'curation', cast: ['consumer', 'curator'], mood: '候補整理' },
  'RE-07A': { bg: 'sns', cast: ['consumer', 'influencer'], mood: 'SNS信頼' },
  'RE-07B': { bg: 'warning', cast: ['consumer', 'influencer'], mood: 'グレーゾーン' },
  'RE-07C': { bg: 'risk', cast: ['consumer', 'ai'], mood: '攻めのDX' },
  'RE-07D': { bg: 'ai-risk', cast: ['consumer', 'ai', 'curator'], mood: 'AI逆説' },
  'RE-07E': { bg: 'final', cast: ['consumer', 'curator'], mood: '選ぶ基準' },
};

const CAST_LABELS = {
  consumer: '消費者',
  gatekeeper: '業者',
  curator: 'キュレーター',
  seller: '売主',
  agent: '仲介',
  buyer: '買主',
  influencer: 'SNS発信者',
  ai: 'AI',
};

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

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(resolveRepoPath(relPath), 'utf8'));
}

function writeText(relPath, text) {
  const fullPath = resolveRepoPath(relPath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, text, 'utf8');
  return fullPath;
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function assertArrayEqual(name, left, right) {
  const leftJson = JSON.stringify(left);
  const rightJson = JSON.stringify(right);
  if (leftJson !== rightJson) {
    throw new Error(`${name} mismatch:\nleft=${leftJson}\nright=${rightJson}`);
  }
}

function classifyItem(item) {
  const value = `${item.id || ''} ${item.kind || ''} ${item.label || ''}`.toLowerCase();
  if (value.includes('phone') || value.includes('sns') || value.includes('qr')) return 'device';
  if (value.includes('ai')) return 'ai';
  if (value.includes('door') || value.includes('gate') || value.includes('reins') || value.includes('vip')) return 'gate';
  if (value.includes('risk') || value.includes('warning') || value.includes('hazard') || value.includes('defect')) return 'warning';
  if (value.includes('contract') || value.includes('seller') || value.includes('buyer') || value.includes('pending')) return 'contract';
  if (value.includes('table') || value.includes('shortlist') || value.includes('card')) return 'document';
  if (value.includes('shield') || value.includes('privacy')) return 'shield';
  return 'document';
}

function proxyMarkup(item) {
  const kind = classifyItem(item);
  const label = escapeHtml(item.label);
  const id = escapeHtml(item.id);
  if (kind === 'device') {
    return `<div class="proxy proxy-device"><div class="device-top"></div><div class="device-screen">${label}</div><div class="device-dots"></div><small>${id}</small></div>`;
  }
  if (kind === 'ai') {
    return `<div class="proxy proxy-ai"><div class="ai-orb"></div><div><strong>${label}</strong><small>${id}</small></div></div>`;
  }
  if (kind === 'gate') {
    return `<div class="proxy proxy-gate"><div class="gate-pillars"></div><div class="gate-label">${label}<small>${id}</small></div></div>`;
  }
  if (kind === 'warning') {
    return `<div class="proxy proxy-warning"><div class="warning-icon">!</div><div>${label}<small>${id}</small></div></div>`;
  }
  if (kind === 'contract') {
    return `<div class="proxy proxy-contract"><div class="contract-lines"></div><div>${label}<small>${id}</small></div></div>`;
  }
  if (kind === 'shield') {
    return `<div class="proxy proxy-shield"><div class="shield-icon"></div><div>${label}<small>${id}</small></div></div>`;
  }
  return `<div class="proxy proxy-document"><div class="doc-stack"></div><div>${label}<small>${id}</small></div></div>`;
}

function itemStyle(item) {
  const box = item.normalized_box || {};
  const left = Number.isFinite(box.x) ? box.x * 100 : 40;
  const top = Number.isFinite(box.y) ? box.y * 100 : 40;
  const width = Number.isFinite(box.w) ? Math.max(box.w * 100, 15) : 24;
  const height = Number.isFinite(box.h) ? Math.max(box.h * 100, 12) : 16;
  return `left:${left.toFixed(3)}%;top:${top.toFixed(3)}%;width:${width.toFixed(3)}%;height:${height.toFixed(3)}%;`;
}

function castMarkup(segmentId) {
  const scene = SEGMENT_SCENE[segmentId] || { cast: ['consumer'] };
  return `<div class="cast-row">${scene.cast.map((role) => (
    `<div class="cast cast-${escapeHtml(role)}"><div class="cast-head"></div><div class="cast-body"></div><span>${escapeHtml(CAST_LABELS[role] || role)}</span></div>`
  )).join('')}</div>`;
}

function segmentFrame(segment, index) {
  const scene = SEGMENT_SCENE[segment.id] || { bg: 'default', mood: 'proxy' };
  return (
    `<section class="sheet-cell" data-segment-id="${escapeHtml(segment.id)}">`
    + `<div class="cell-header"><strong>${escapeHtml(segment.id)} ${escapeHtml(segment.title)}</strong><span>${escapeHtml(scene.mood)}</span></div>`
    + `<div class="video-frame bg-${escapeHtml(scene.bg)}" data-keyframe="middle">`
    + `<div class="frame-badge">keyframe ${index + 1} / middle proxy</div>`
    + castMarkup(segment.id)
    + `<div class="prop-layer">${(segment.items || []).map((item) => (
      `<div class="prop" style="${itemStyle(item)}">${proxyMarkup(item)}</div>`
    )).join('')}</div>`
    + `<div class="frame-footer">source ${Number(segment.source_start_sec).toFixed(1)}-${Number(segment.source_end_sec).toFixed(1)}s / review ${Number(segment.review_start_sec).toFixed(1)}-${Number(segment.review_end_sec).toFixed(1)}s</div>`
    + `</div>`
    + `<p class="cell-note">visual proxy only / production art and cast templates still blocked</p>`
    + `</section>`
  );
}

function buildHtml(manifest, overlayReadback) {
  const segments = manifest.segments || [];
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Real Estate DX Visual Storyboard Proof</title>
<style>
:root { color-scheme: light; font-family: "Yu Gothic UI", "Segoe UI", system-ui, sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; background: #e8edf5; color: #172033; }
header { padding: 18px 22px; background: #111827; color: #f8fafc; display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: end; }
header h1 { margin: 0 0 6px; font-size: 24px; }
header p { margin: 2px 0; color: #cbd5e1; font-size: 13px; }
.status { text-align: right; font-size: 12px; color: #bfdbfe; }
.sheet { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; padding: 18px; }
.sheet-cell { background: #fff; border: 1px solid #cbd5e1; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 22px rgba(15, 23, 42, .11); }
.cell-header { min-height: 52px; padding: 10px 12px; display: flex; justify-content: space-between; gap: 8px; align-items: baseline; border-bottom: 1px solid #e5e7eb; }
.cell-header strong { font-size: 14px; color: #0f172a; }
.cell-header span { flex-shrink: 0; font-size: 11px; color: #475569; }
.video-frame { position: relative; aspect-ratio: 16 / 9; overflow: hidden; border-bottom: 1px solid #e5e7eb; background: linear-gradient(135deg, #dbeafe 0%, #f8fafc 50%, #fef3c7 100%); }
.bg-search { background: radial-gradient(circle at 28% 70%, #dbeafe, transparent 25%), linear-gradient(135deg, #e0f2fe, #fff7ed); }
.bg-gate { background: linear-gradient(90deg, #e0f2fe 0 48%, #fef3c7 48% 100%); }
.bg-shield { background: radial-gradient(circle at 52% 45%, #ecfdf5, transparent 28%), linear-gradient(135deg, #eff6ff, #fefce8); }
.bg-contract { background: linear-gradient(135deg, #f1f5f9, #fff7ed); }
.bg-transparent { background: linear-gradient(135deg, #dbeafe, #ecfeff 45%, #fefce8); }
.bg-curation { background: linear-gradient(135deg, #f8fafc, #eef2ff, #fff7ed); }
.bg-sns { background: linear-gradient(135deg, #fdf2f8, #dbeafe); }
.bg-warning { background: linear-gradient(135deg, #fff1f2, #fef3c7); }
.bg-risk { background: linear-gradient(135deg, #ecfeff, #f1f5f9, #fef3c7); }
.bg-ai-risk { background: linear-gradient(135deg, #eef2ff, #f8fafc 55%, #fee2e2); }
.bg-final { background: linear-gradient(135deg, #f8fafc, #dcfce7, #fef3c7); }
.frame-badge { position: absolute; left: 10px; top: 8px; z-index: 5; padding: 4px 8px; border-radius: 999px; background: rgba(15, 23, 42, .78); color: #fff; font-size: 10px; letter-spacing: .02em; }
.cast-row { position: absolute; left: 5%; right: 5%; bottom: 7%; display: flex; justify-content: space-between; align-items: end; pointer-events: none; }
.cast { width: 42px; display: grid; justify-items: center; gap: 1px; filter: drop-shadow(0 4px 7px rgba(15, 23, 42, .20)); }
.cast-head { width: 18px; height: 18px; border-radius: 50%; background: #334155; border: 2px solid #f8fafc; }
.cast-body { width: 34px; height: 34px; border-radius: 16px 16px 5px 5px; background: #475569; border: 2px solid #f8fafc; }
.cast span { padding: 1px 4px; border-radius: 999px; background: rgba(255,255,255,.84); color: #0f172a; font-size: 9px; font-weight: 700; }
.cast-gatekeeper .cast-body, .cast-agent .cast-body { background: #7c2d12; }
.cast-curator .cast-body { background: #166534; }
.cast-seller .cast-body, .cast-buyer .cast-body { background: #1d4ed8; }
.cast-influencer .cast-body { background: #be185d; }
.cast-ai .cast-head, .cast-ai .cast-body { background: #4f46e5; }
.prop { position: absolute; z-index: 3; }
.proxy { width: 100%; height: 100%; min-height: 42px; padding: 7px; border: 2px solid rgba(15, 23, 42, .58); border-radius: 11px; background: rgba(255,255,255,.92); box-shadow: 0 8px 18px rgba(15,23,42,.16); display: grid; place-items: center; text-align: center; color: #0f172a; font-weight: 800; font-size: clamp(9px, .9vw, 14px); line-height: 1.15; }
.proxy small { display: block; margin-top: 3px; font-size: 8px; color: #475569; font-weight: 700; }
.proxy-device { border-radius: 18px; background: linear-gradient(#0f172a 0 12%, #eff6ff 12% 88%, #0f172a 88% 100%); color: #0f172a; }
.device-screen { padding: 4px; border-radius: 8px; background: #fff; }
.device-dots { width: 22px; height: 3px; border-radius: 99px; background: #94a3b8; }
.proxy-ai { grid-template-columns: 32px 1fr; gap: 6px; background: linear-gradient(135deg, #eef2ff, #fff); }
.ai-orb { width: 28px; height: 28px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fff, #6366f1 42%, #312e81); }
.proxy-gate { background: linear-gradient(90deg, #fff 0 40%, #fef3c7); }
.gate-pillars { width: 72%; height: 46%; border-left: 8px solid #334155; border-right: 8px solid #334155; border-top: 8px solid #334155; border-radius: 8px 8px 0 0; }
.proxy-warning { grid-template-columns: 26px 1fr; gap: 6px; border-color: #b91c1c; background: #fff7ed; }
.warning-icon { width: 24px; height: 24px; border-radius: 50%; background: #dc2626; color: #fff; display: grid; place-items: center; font-weight: 900; }
.proxy-contract { background: #fff; }
.contract-lines, .doc-stack { width: 42%; height: 44%; border-radius: 4px; background: repeating-linear-gradient(#cbd5e1 0 3px, transparent 3px 8px), #fff; border: 2px solid #94a3b8; }
.proxy-shield { grid-template-columns: 28px 1fr; gap: 5px; background: #ecfdf5; }
.shield-icon { width: 26px; height: 30px; background: #059669; clip-path: polygon(50% 0, 94% 18%, 82% 78%, 50% 100%, 18% 78%, 6% 18%); }
.proxy-document { background: #fff; }
.frame-footer { position: absolute; right: 8px; bottom: 8px; padding: 3px 7px; border-radius: 7px; background: rgba(255,255,255,.82); color: #475569; font-size: 9px; font-weight: 700; }
.cell-note { margin: 0; padding: 8px 10px; background: #fffbeb; color: #92400e; font-size: 11px; border-top: 1px solid #fcd34d; }
.legend { margin: 0 18px 18px; padding: 12px 14px; background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; color: #334155; font-size: 13px; }
.legend strong { color: #0f172a; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Real Estate DX Visual Storyboard Proof</h1>
    <p>3×4 contact sheet / one 16:9 proxy keyframe per segment / visual proxy proof only</p>
    <p>Not creative acceptance. Not cast motion IR. Not production timing.</p>
  </div>
  <div class="status">
    <div>overlay readback: ${escapeHtml(overlayReadback.status)}</div>
    <div>segments: ${segments.length} / placeholders: ${escapeHtml(overlayReadback.checks?.placeholder_items_rendered)}</div>
  </div>
</header>
<main class="sheet">
${segments.map(segmentFrame).join('\n')}
</main>
<section class="legend">
  <strong>この画像の用途:</strong>
  placeholderをテキスト箱ではなく、人物枠・物件資料・SNS画面・契約書・警告UI・AI UIなどのproxy visualとして配置し、
  RE-01〜RE-07Eの動画ショット単位の認知負荷を確認するための証跡。制作素材の完成度やYMM4上の最終見栄えは承認しない。
</section>
</body>
</html>
`;
}

async function waitForStoryboard(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = () => {
        try {
          const cells = Array.from(document.querySelectorAll('.sheet-cell'));
          const frames = Array.from(document.querySelectorAll('.video-frame'));
          const props = Array.from(document.querySelectorAll('.prop'));
          const casts = Array.from(document.querySelectorAll('.cast'));
          const text = document.body.innerText || '';
          const ready = document.readyState === 'complete'
            && cells.length === 11
            && frames.length === 11
            && props.length === 24
            && cells[0]?.dataset.segmentId === 'RE-01'
            && cells[cells.length - 1]?.dataset.segmentId === 'RE-07E';
          if (ready) {
            const page = document.documentElement;
            resolve({
              cell_count: cells.length,
              keyframe_count: frames.length,
              placeholder_count: props.length,
              cast_proxy_count: casts.length,
              segment_ids: cells.map((cell) => cell.dataset.segmentId),
              frame_modes: frames.map((frame) => frame.dataset.keyframe),
              has_contact_sheet: getComputedStyle(document.querySelector('.sheet')).gridTemplateColumns.split(' ').length === 3,
              has_corruption_marker: /\\?\\?\\?|�/.test(text),
              scroll_width: Math.ceil(Math.max(page.scrollWidth, document.body.scrollWidth)),
              scroll_height: Math.ceil(Math.max(page.scrollHeight, document.body.scrollHeight)),
            });
            return;
          }
          if (Date.now() - started > 5000) {
            reject(new Error('visual storyboard proof DOM did not become ready: ' + JSON.stringify({
              readyState: document.readyState,
              cells: cells.length,
              frames: frames.length,
              props: props.length,
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
  const manifestRel = args.manifest || DEFAULT_MANIFEST;
  const overlayReadbackRel = args.overlayReadback || DEFAULT_OVERLAY_READBACK;
  const validatorRel = args.validator || DEFAULT_VALIDATOR;
  const htmlRel = args.html || DEFAULT_HTML;
  const screenshotRel = args.output || DEFAULT_SCREENSHOT;
  const readbackRel = args.report || DEFAULT_READBACK;

  const manifest = readJson(manifestRel);
  const overlayReadback = readJson(overlayReadbackRel);
  const validator = readJson(validatorRel);
  const segments = manifest.segments || [];
  const placeholderCount = segments.reduce((total, segment) => total + (segment.items || []).length, 0);

  if (overlayReadback.status !== 'passed') throw new Error(`overlay readback status is not passed: ${overlayReadback.status}`);
  if (overlayReadback.is_creative_acceptance !== false) throw new Error('overlay readback must not be creative acceptance');
  if (segments.length !== 11) throw new Error(`manifest segment count mismatch: ${segments.length}`);
  if (placeholderCount !== 24) throw new Error(`manifest placeholder count mismatch: ${placeholderCount}`);
  if (overlayReadback.checks?.segments !== 11) throw new Error(`overlay readback segment count mismatch: ${overlayReadback.checks?.segments}`);
  if (overlayReadback.checks?.placeholder_items_rendered !== 24) throw new Error(`overlay readback placeholder count mismatch: ${overlayReadback.checks?.placeholder_items_rendered}`);
  assertArrayEqual('remaining blockers', overlayReadback.remaining_blockers || [], validator.blockers || []);

  const htmlPath = writeText(htmlRel, buildHtml(manifest, overlayReadback));
  const screenshotPath = resolveRepoPath(screenshotRel);
  const readbackPath = resolveRepoPath(readbackRel);
  fs.mkdirSync(path.dirname(screenshotPath), { recursive: true });
  fs.mkdirSync(path.dirname(readbackPath), { recursive: true });

  app.commandLine.appendSwitch('disable-gpu');
  await app.whenReady();

  const win = new BrowserWindow({
    show: false,
    width: 1800,
    height: 1300,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  await win.loadFile(htmlPath);
  const dom = await waitForStoryboard(win);
  if (dom.has_corruption_marker) throw new Error('visual storyboard proof contains ??? or replacement character');
  if (!dom.has_contact_sheet) throw new Error('visual storyboard proof is not rendered as a 3-column contact sheet');

  const captureWidth = Math.min(Math.max(dom.scroll_width, 1600), 2400);
  const captureHeight = Math.min(Math.max(dom.scroll_height, 1000), 12000);
  win.setContentSize(captureWidth, captureHeight);
  await new Promise((resolve) => setTimeout(resolve, 200));
  const image = await win.webContents.capturePage({ x: 0, y: 0, width: captureWidth, height: captureHeight });
  fs.writeFileSync(screenshotPath, image.toPNG());
  const imageSize = image.getSize();

  const report = {
    status: 'passed',
    proof_type: 'visual_proxy_proof',
    not_creative_acceptance: true,
    source_manifest: manifestRel,
    source_overlay_readback: overlayReadbackRel,
    validator_result: validatorRel,
    html_artifact: toRepoPath(htmlPath),
    screenshot_artifact: toRepoPath(screenshotPath),
    screenshot_capture_method: 'electron generated contact sheet HTML + BrowserWindow.loadFile + webContents.capturePage(full-page rect)',
    layout: {
      type: 'contact_sheet',
      columns: 3,
      rows: 4,
      canvas_aspect_ratio: '16:9',
      keyframes_per_segment: 1,
      keyframe_phase: 'middle proxy',
    },
    checks: {
      overlay_readback_status: overlayReadback.status,
      readback_segments: overlayReadback.checks?.segments,
      storyboard_segments: dom.cell_count,
      keyframe_count: dom.keyframe_count,
      segment_ids: dom.segment_ids,
      readback_placeholder_items_rendered: overlayReadback.checks?.placeholder_items_rendered,
      storyboard_placeholders: dom.placeholder_count,
      cast_proxy_count: dom.cast_proxy_count,
      all_segments_visible_in_dom: dom.cell_count === 11,
      all_placeholders_visible_in_dom: dom.placeholder_count === 24,
      contact_sheet_3_columns: dom.has_contact_sheet,
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
    allowed_next_actions: overlayReadback.allowed_next_actions || [],
    forbidden_next_actions: overlayReadback.forbidden_next_actions || [],
    remaining_blockers: overlayReadback.remaining_blockers || [],
  };
  fs.writeFileSync(readbackPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(report, null, 2));

  await win.close();
  app.quit();
}

run().catch((err) => {
  console.error(err.stack || err.message || String(err));
  app.exit(1);
});

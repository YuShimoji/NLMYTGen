const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { app, BrowserWindow } = require('electron');

app.disableHardwareAcceleration();
app.commandLine.appendSwitch('disable-gpu');

const repoRoot = path.resolve(__dirname, '..');
const DEFAULT_INPUT = 'lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json';
const DEFAULT_OUTPUT = 'samples/_probe/baseball/static/baseball_pitch_event_p05.png';
const DEFAULT_MANIFEST = 'samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json';
const DEFAULT_READBACK = 'samples/_probe/baseball/static/baseball_pitch_event_p05_readback.json';
const TMP_DIR = '_tmp/baseball_static_capture';
const TMP_HTML = `${TMP_DIR}/baseball_static_capture.html`;

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function resolveRepoPath(relPath) {
  const full = path.resolve(repoRoot, relPath);
  const relative = path.relative(repoRoot, full);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`path outside repo is not allowed: ${relPath}`);
  }
  return full;
}

function toRepoPath(fullPath) {
  return path.relative(repoRoot, fullPath).replace(/\\/g, '/');
}

function fileUrl(fullPath) {
  return `file:///${fullPath.replace(/\\/g, '/').replace(/#/g, '%23')}`;
}

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(resolveRepoPath(relPath), 'utf8'));
}

function writeJson(relPath, payload) {
  const full = resolveRepoPath(relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function sha256File(relPath) {
  const hash = crypto.createHash('sha256');
  hash.update(fs.readFileSync(resolveRepoPath(relPath)));
  return hash.digest('hex');
}

function positiveInt(value, fallback) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) return fallback;
  return Math.floor(parsed);
}

function boolFlag(value, fallback = false) {
  if (value == null) return fallback;
  return value === true || value === '1' || value === 'true';
}

function validateVisualData(data) {
  const errors = [];
  if (data.schema_version !== 'baseball_visual_data.v1') {
    errors.push('schema_version must be baseball_visual_data.v1');
  }
  if (!data.atBat || !Array.isArray(data.atBat.pitches) || data.atBat.pitches.length < 2) {
    errors.push('atBat.pitches must contain at least two pitches');
  }
  if (!data.teams || !data.teams.home || !data.teams.away) {
    errors.push('teams.home and teams.away are required');
  }
  if (!data.score || data.score.home == null || data.score.away == null) {
    errors.push('score.home and score.away are required');
  }
  if (!data.visual || !data.visual.claim) {
    errors.push('visual.claim is required');
  }
  if (errors.length) throw new Error(errors.join('; '));
}

function renderHarnessHtml(data, settings) {
  const baseHref = `${fileUrl(resolveRepoPath('BaseballInfoGraphics'))}/`;
  const payload = JSON.stringify(data);
  const settingsPayload = JSON.stringify(settings);
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<title>Baseball static capture</title>
<base href="${baseHref}">
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+JP:wght@400;500;600;700;900&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1280px; height: 720px; overflow: hidden; background: #020617; }
  body { font-family: "Noto Sans JP", system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
  #root, .ig-frame { width: 1280px; height: 720px; position: relative; overflow: hidden; }
</style>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
</head>
<body>
<div id="root"></div>
<script>
window.BASEBALL_VISUAL_DATA = ${payload};
window.BASEBALL_STATIC_CAPTURE_SETTINGS = ${settingsPayload};
</script>
<script type="text/babel" src="components/strike-zone.jsx"></script>
<script type="text/babel" src="components/diamond.jsx"></script>
<script type="text/babel" src="variants/detailed.jsx"></script>
<script type="text/babel">
const settings = window.BASEBALL_STATIC_CAPTURE_SETTINGS;
const sourceData = JSON.parse(JSON.stringify(window.BASEBALL_VISUAL_DATA));
const pitchCount = sourceData.atBat.pitches.length;
const pitchIdx = Math.max(0, Math.min(pitchCount - 1, settings.pitchIdx));
const homeColor = settings.homeColor || sourceData.teams.home.primary;
const awayColor = settings.awayColor || sourceData.teams.away.primary;
sourceData.teams.home.primary = homeColor;
sourceData.teams.away.primary = awayColor;
const accentColor = settings.accentTeam === 'away' ? awayColor : homeColor;

function App() {
  React.useEffect(() => {
    const ambientBackdrop = sourceData.visual?.ambientBackdrop || {};
    window.__BASEBALL_STATIC_CAPTURE_STATE__ = {
      status: 'ready',
      variant: 'detailed',
      pitchIdx,
      totalPitches: pitchCount,
      currentPitchNumber: sourceData.atBat.pitches[pitchIdx]?.num ?? null,
      playing: false,
      width: 1280,
      height: 720,
      density: settings.density,
      statMode: settings.statMode,
      showRomaji: settings.showRomaji,
      ambientBackdrop: {
        kind: ambientBackdrop.kind || 'css_grid',
        provenance: ambientBackdrop.provenance || 'none',
        usageStage: ambientBackdrop.usageStage || 'design_preview',
        hasImage: Boolean(ambientBackdrop.imageUrl),
      },
    };
  }, []);
  return (
    <div className="ig-frame" data-baseball-static-capture="true">
      <DetailedVariant
        data={sourceData}
        currentPitchIdx={pitchIdx}
        teamColor={accentColor}
        density={settings.density}
        showRomaji={settings.showRomaji}
        statMode={settings.statMode}
        animateLatest={false}
      />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>`;
}

async function waitForReady(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = async () => {
        const state = window.__BASEBALL_STATIC_CAPTURE_STATE__;
        const frame = document.querySelector('[data-baseball-static-capture="true"]');
        const rect = frame ? frame.getBoundingClientRect() : null;
        const text = document.body.innerText || '';
        const ready = state?.status === 'ready'
          && rect
          && Math.round(rect.width) === 1280
          && Math.round(rect.height) === 720
          && text.includes('PITCHER')
          && text.includes('BATTER')
          && text.includes('PITCH LOG')
          && !text.includes('Tweaks');
        if (ready) {
          try {
            if (document.fonts?.ready) await document.fonts.ready;
          } catch (_) {}
          resolve({
            ...state,
            text_sample: text.slice(0, 500),
            frame_rect: {
              width: Math.round(rect.width),
              height: Math.round(rect.height),
            },
            design_canvas_visible: Boolean(document.querySelector('.dc-card')),
            tweaks_visible: text.includes('Tweaks'),
          });
          return;
        }
        if (Date.now() - started > 10000) {
          reject(new Error('baseball static capture not ready: ' + JSON.stringify({
            hasState: Boolean(state),
            hasFrame: Boolean(frame),
            rect: rect ? { width: rect.width, height: rect.height } : null,
            text: text.slice(0, 500),
          })));
          return;
        }
        setTimeout(tick, 100);
      };
      tick();
    })
  `);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const inputRel = args.input || DEFAULT_INPUT;
  const outputRel = args.output || DEFAULT_OUTPUT;
  const manifestRel = args.manifest || DEFAULT_MANIFEST;
  const readbackRel = args.readback || DEFAULT_READBACK;
  const data = readJson(inputRel);
  validateVisualData(data);

  const defaultPitchIdx = data.atBat.currentPitchIndex == null
    ? data.atBat.pitches.length - 1
    : data.atBat.currentPitchIndex;
  const settings = {
    width: 1280,
    height: 720,
    pitchIdx: positiveInt(args.pitch, defaultPitchIdx),
    density: args.density || 'standard',
    statMode: args['stat-mode'] || 'simple',
    showRomaji: boolFlag(args['show-romaji'], false),
    accentTeam: args['accent-team'] || 'home',
    autoplay: false,
  };
  settings.pitchIdx = Math.max(0, Math.min(data.atBat.pitches.length - 1, settings.pitchIdx));

  const tmpHtmlFull = resolveRepoPath(TMP_HTML);
  fs.mkdirSync(path.dirname(tmpHtmlFull), { recursive: true });
  fs.writeFileSync(tmpHtmlFull, renderHarnessHtml(data, settings), 'utf8');

  const outputFull = resolveRepoPath(outputRel);
  fs.mkdirSync(path.dirname(outputFull), { recursive: true });

  app.setPath('userData', path.join(repoRoot, '_tmp', 'electron_baseball_static_capture'));
  await app.whenReady();
  const win = new BrowserWindow({
    show: false,
    width: 1280,
    height: 720,
    resizable: false,
    useContentSize: true,
    backgroundColor: '#020617',
    webPreferences: {
      offscreen: true,
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });
  const pageMessages = [];
  win.webContents.on('console-message', (event) => {
    const details = event && typeof event === 'object' ? event : null;
    if (details) {
      pageMessages.push({
        level: details.level,
        message: details.message,
        line: details.lineNumber,
        sourceId: details.sourceId,
      });
    } else {
      pageMessages.push({ level: 'console', message: 'unknown console message' });
    }
  });
  win.webContents.on('did-fail-load', (_event, errorCode, errorDescription, validatedURL) => {
    pageMessages.push({ level: 'load-error', message: `${errorCode}: ${errorDescription}`, sourceId: validatedURL });
  });

  try {
    await win.loadFile(tmpHtmlFull);
    win.webContents.setZoomFactor(1);
    const bootstrapState = await win.webContents.executeJavaScript(`({
      readyState: document.readyState,
      react: typeof React,
      reactDom: typeof ReactDOM,
      babel: typeof Babel,
      bodyLength: (document.body?.innerText || '').length,
      scriptCount: document.scripts.length,
      rootChildren: document.getElementById('root')?.children.length || 0
    })`);
    pageMessages.push({ level: 'bootstrap', message: JSON.stringify(bootstrapState), sourceId: 'capture' });
    let domState;
    try {
      domState = await waitForReady(win);
    } catch (error) {
      error.message = `${error.message}; page_messages=${JSON.stringify(pageMessages.slice(-20))}`;
      throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
    const image = await win.webContents.capturePage({ x: 0, y: 0, width: 1280, height: 720 });
    fs.writeFileSync(outputFull, image.toPNG());
    const imageSize = image.getSize();
    const inputHash = sha256File(inputRel);
    const outputHash = crypto.createHash('sha256').update(fs.readFileSync(outputFull)).digest('hex');
    const currentPitch = data.atBat.pitches[settings.pitchIdx] || {};
    const manifest = {
      schema_version: 'baseball_static_render_manifest.v1',
      artifact_type: 'baseball_static_png_export',
      input: {
        visual_data_path: inputRel,
        visual_data_schema_version: data.schema_version,
        sha256: inputHash,
      },
      output: {
        png_path: outputRel,
        sha256: outputHash,
        width: imageSize.width,
        height: imageSize.height,
      },
      variant: 'detailed',
      export_settings: {
        ...settings,
        currentPitchNumber: currentPitch.num ?? null,
        currentPitchType: currentPitch.type ?? null,
      },
      capture: {
        method: 'Electron offscreen BrowserWindow + generated C detailed harness + webContents.capturePage',
        tmp_html: TMP_HTML,
      },
      boundaries: {
        not_yymm4_proof: true,
        not_animation_export: true,
        not_creative_acceptance: true,
        not_publish_gate: true,
      },
    };
    const readback = {
      status: 'passed',
      manifest_path: manifestRel,
      png_path: outputRel,
      screenshot_width: imageSize.width,
      screenshot_height: imageSize.height,
      input_sha256: inputHash,
      output_sha256: outputHash,
      not_yymm4_proof: true,
      not_animation_export: true,
      not_creative_acceptance: true,
      dom_state: domState,
    };
    writeJson(manifestRel, manifest);
    writeJson(readbackRel, readback);
    console.log(JSON.stringify(readback, null, 2));
  } finally {
    win.close();
    app.quit();
  }
}

main().catch((err) => {
  console.error(err.message || String(err));
  if (err.stack) console.error(err.stack);
  app.exit(1);
});

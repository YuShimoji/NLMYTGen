const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { app, BrowserWindow } = require('electron');

app.disableHardwareAcceleration();
app.commandLine.appendSwitch('disable-gpu');

const repoRoot = path.resolve(__dirname, '..');
const DEFAULT_PLAN = 'samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_export_plan.json';
const DEFAULT_INPUT = 'lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json';
const DEFAULT_FRAME_DIR = 'samples/_probe/baseball/animation/frames/baseball_pitch_event_p05';
const DEFAULT_FRAME_PATTERN = 'baseball_pitch_event_p05_f%03d.png';
const DEFAULT_MANIFEST = 'samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_manifest.json';
const DEFAULT_READBACK = 'samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_readback.json';
const DEFAULT_HANDOFF = 'samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_handoff.md';
const TMP_DIR = '_tmp/baseball_frame_capture';
const TMP_HTML = `${TMP_DIR}/baseball_frame_capture.html`;

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

function sha256Bytes(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function sha256File(relPath) {
  return sha256Bytes(fs.readFileSync(resolveRepoPath(relPath)));
}

function positiveInt(value, fallback) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) return fallback;
  return Math.floor(parsed);
}

function validateVisualData(data) {
  const errors = [];
  if (data.schema_version !== 'baseball_visual_data.v1') {
    errors.push('schema_version must be baseball_visual_data.v1');
  }
  if (!data.atBat || !Array.isArray(data.atBat.pitches) || data.atBat.pitches.length < 2) {
    errors.push('atBat.pitches must contain at least two pitches');
  }
  if (!data.visual || !data.visual.claim) {
    errors.push('visual.claim is required');
  }
  if (errors.length) throw new Error(errors.join('; '));
}

function frameName(pattern, frameNumber) {
  return pattern.replace('%03d', String(frameNumber).padStart(3, '0'));
}

function clearFrameDir(frameDirRel, pattern) {
  const dir = resolveRepoPath(frameDirRel);
  fs.mkdirSync(dir, { recursive: true });
  const prefix = pattern.split('%03d')[0];
  const suffix = pattern.split('%03d')[1] || '';
  for (const entry of fs.readdirSync(dir)) {
    if (entry.startsWith(prefix) && entry.endsWith(suffix)) {
      fs.unlinkSync(path.join(dir, entry));
    }
  }
}

function normalizeStateSequence(plan) {
  const stateSequence = Array.isArray(plan.state_sequence) ? plan.state_sequence : [];
  const byFrame = new Map(stateSequence.map((state) => [state.frame, state]));
  const fallback = [
    { frame: 0, label: 'previous_pitch_context', pitch_index: 0 },
    { frame: 1, label: 'delta_transition_in', pitch_index: 1 },
    { frame: 2, label: 'delta_transition', pitch_index: 1 },
    { frame: 3, label: 'current_pitch_settle', pitch_index: 1 },
    { frame: 4, label: 'current_pitch_lock', pitch_index: 1 },
  ];
  return fallback.map((frame) => ({
    ...frame,
    ...(byFrame.get(frame.frame) || {}),
  }));
}

function renderHarnessHtml(data, settings) {
  const baseHref = `${fileUrl(resolveRepoPath('BaseballInfoGraphics'))}/`;
  const payload = JSON.stringify(data);
  const settingsPayload = JSON.stringify(settings);
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<title>Baseball frame capture</title>
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
window.BASEBALL_FRAME_CAPTURE_SETTINGS = ${settingsPayload};
</script>
<script type="text/babel" src="components/strike-zone.jsx"></script>
<script type="text/babel" src="components/diamond.jsx"></script>
<script type="text/babel" src="variants/detailed.jsx"></script>
<script type="text/babel">
const settings = window.BASEBALL_FRAME_CAPTURE_SETTINGS;
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
    window.__BASEBALL_FRAME_CAPTURE_STATE__ = {
      status: 'ready',
      variant: 'detailed',
      frameNumber: settings.frameNumber,
      frameLabel: settings.frameLabel,
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
    <div className="ig-frame" data-baseball-frame-capture="true">
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
        const state = window.__BASEBALL_FRAME_CAPTURE_STATE__;
        const frame = document.querySelector('[data-baseball-frame-capture="true"]');
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
          reject(new Error('baseball frame capture not ready: ' + JSON.stringify({
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

async function captureFrame(win, data, frameState, settings, outputRel) {
  const tmpHtmlFull = resolveRepoPath(TMP_HTML);
  fs.mkdirSync(path.dirname(tmpHtmlFull), { recursive: true });
  fs.writeFileSync(
    tmpHtmlFull,
    renderHarnessHtml(data, {
      ...settings,
      pitchIdx: frameState.pitch_index,
      frameNumber: frameState.frame,
      frameLabel: frameState.label,
    }),
    'utf8',
  );

  await win.loadFile(tmpHtmlFull);
  win.webContents.setZoomFactor(1);
  const domState = await waitForReady(win);
  await new Promise((resolve) => setTimeout(resolve, settings.waitMs));
  const image = await win.webContents.capturePage({ x: 0, y: 0, width: 1280, height: 720 });
  const outputFull = resolveRepoPath(outputRel);
  fs.mkdirSync(path.dirname(outputFull), { recursive: true });
  const pngBytes = image.toPNG();
  fs.writeFileSync(outputFull, pngBytes);
  const imageSize = image.getSize();
  const pitch = data.atBat.pitches[frameState.pitch_index] || {};
  return {
    frame: frameState.frame,
    label: frameState.label,
    pitch_index: frameState.pitch_index,
    currentPitchNumber: pitch.num ?? null,
    currentPitchType: pitch.type ?? null,
    path: outputRel,
    sha256: sha256Bytes(pngBytes),
    width: imageSize.width,
    height: imageSize.height,
    dom_state: domState,
  };
}

function buildHandoff(manifestRel, readbackRel, frameDirRel) {
  return `# Baseball BN-04 frame sequence handoff (2026-05-26)

BN-04 now has a deterministic frame-sequence export for the sample pitch event.
This is not a video clip, not a YMM4 placement proof, and not creative
acceptance.

Boundary phrase for readback: not creative acceptance.

## Generated artifacts

- manifest: \`${manifestRel}\`
- readback: \`${readbackRel}\`
- frames: \`${frameDirRel}/baseball_pitch_event_p05_f000.png\` through \`f004.png\`

The sequence is a transport/readback proof for the previous-pitch to
current-pitch comparison. It remains sample-only and should be visually checked
before any clip export or production timing work.

## Next safe moves

| Entry | Why it helps | What becomes possible |
| --- | --- | --- |
| Verify BN-05 manual preview | Confirms crop, text size, and layer overlap in real YMM4 | Decide whether the static placement contract is usable. |
| Inspect BN-04 frames | Confirms the frame sequence reads as a pitch update | Decide whether to keep frame sequence or build a clip. |
| Advance clip export | Tests codec/timing only after frame readback passes | Prepare animation material for YMM4 placement. |
`;
}

function summarizeDomState(domState) {
  const { text_sample: textSample, ...rest } = domState;
  return {
    ...rest,
    text_sample_length: typeof textSample === 'string' ? textSample.length : 0,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const planRel = args.plan || DEFAULT_PLAN;
  const plan = readJson(planRel);
  const inputRel = args.input || plan.source?.visual_data_path || DEFAULT_INPUT;
  const frameDirRel = args['frame-dir'] || plan.planned_outputs?.frame_dir || DEFAULT_FRAME_DIR;
  const framePattern = args['frame-pattern'] || plan.planned_outputs?.frame_pattern || DEFAULT_FRAME_PATTERN;
  const manifestRel = args.manifest || plan.planned_outputs?.manifest_path || DEFAULT_MANIFEST;
  const readbackRel = args.readback || plan.planned_outputs?.readback_path || DEFAULT_READBACK;
  const handoffRel = args.handoff || DEFAULT_HANDOFF;
  const data = readJson(inputRel);
  validateVisualData(data);

  const planned = plan.planned_outputs || {};
  const settings = {
    width: 1280,
    height: 720,
    fps: positiveInt(args.fps, planned.fps || 30),
    durationMs: positiveInt(args.duration, planned.duration_ms || 1200),
    frameCount: positiveInt(args.frames, planned.frame_count || 5),
    waitMs: positiveInt(args['wait-ms'], 1600),
    density: args.density || 'standard',
    statMode: args['stat-mode'] || 'simple',
    showRomaji: false,
    accentTeam: args['accent-team'] || 'home',
  };

  if (settings.width !== 1280 || settings.height !== 720) {
    throw new Error('BN-04 frame sequence currently supports only 1280x720');
  }
  if (settings.frameCount !== 5) {
    throw new Error('BN-04 sample frame sequence currently expects five frames');
  }

  const stateSequence = normalizeStateSequence(plan);
  if (stateSequence.length !== settings.frameCount) {
    throw new Error('state_sequence must resolve to five frames');
  }
  for (const frameState of stateSequence) {
    if (frameState.pitch_index >= data.atBat.pitches.length) {
      throw new Error(`frame ${frameState.frame} references missing pitch index ${frameState.pitch_index}`);
    }
  }

  clearFrameDir(frameDirRel, framePattern);

  app.setPath('userData', path.join(repoRoot, '_tmp', 'electron_baseball_frame_capture'));
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
    const frames = [];
    for (const frameState of stateSequence) {
      const outputRel = `${frameDirRel}/${frameName(framePattern, frameState.frame)}`;
      try {
        frames.push(await captureFrame(win, data, frameState, settings, outputRel));
      } catch (error) {
        error.message = `${error.message}; page_messages=${JSON.stringify(pageMessages.slice(-20))}`;
        throw error;
      }
    }

    const inputHash = sha256File(inputRel);
    const planHash = sha256File(planRel);
    const staticManifestRel = plan.source?.static_manifest_path || 'samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json';
    const staticManifestHash = fs.existsSync(resolveRepoPath(staticManifestRel)) ? sha256File(staticManifestRel) : null;
    const allFramesExist = frames.every((frame) => fs.existsSync(resolveRepoPath(frame.path)));
    const allFrames1280x720 = frames.every((frame) => frame.width === 1280 && frame.height === 720);
    const noDesignCanvasOrTweaks = frames.every(
      (frame) => frame.dom_state.design_canvas_visible === false && frame.dom_state.tweaks_visible === false,
    );
    const uniqueFrameHashCount = new Set(frames.map((frame) => frame.sha256)).size;
    const boundaries = {
      not_yymm4_placement: true,
      not_clip_export: true,
      not_creative_acceptance: true,
      not_publish_gate: true,
      not_real_episode_source: true,
    };

    const manifest = {
      schema_version: 'baseball_frame_sequence_manifest.v1',
      artifact_type: 'baseball_frame_sequence_export',
      input: {
        visual_data_path: inputRel,
        visual_data_schema_version: data.schema_version,
        visual_data_sha256: inputHash,
        plan_path: planRel,
        plan_sha256: planHash,
        static_manifest_path: staticManifestRel,
        static_manifest_sha256: staticManifestHash,
      },
      output: {
        frame_dir: frameDirRel,
        frame_pattern: framePattern,
        frame_count: frames.length,
        width: 1280,
        height: 720,
        fps: settings.fps,
        duration_ms: settings.durationMs,
      },
      variant: 'detailed',
      export_settings: {
        density: settings.density,
        statMode: settings.statMode,
        showRomaji: settings.showRomaji,
        accentTeam: settings.accentTeam,
        waitMs: settings.waitMs,
        mode: 'frame_sequence_first',
      },
      frames: frames.map(({ dom_state, ...frame }) => frame),
      capture: {
        method: 'Electron offscreen BrowserWindow + generated C detailed harness + webContents.capturePage',
        tmp_html: TMP_HTML,
      },
      boundaries,
    };

    const readback = {
      schema_version: 'baseball_frame_sequence_readback.v1',
      status: 'passed',
      manifest_path: manifestRel,
      plan_path: planRel,
      frame_dir: frameDirRel,
      checks: {
        frame_count_matches_plan: frames.length === settings.frameCount && frames.length === planned.frame_count,
        all_frames_exist: allFramesExist,
        all_frames_1280x720: allFrames1280x720,
        hashes_match_manifest: frames.every((frame) => sha256File(frame.path) === frame.sha256),
        visual_data_hash_matches_plan: inputHash === plan.source?.visual_data_sha256,
        no_design_canvas_or_tweaks: noDesignCanvasOrTweaks,
        no_clip_export: true,
        not_yymm4_placement: true,
        not_creative_acceptance: true,
        not_publish_gate: true,
      },
      failed_checks: [],
      frame_hashes: frames.map((frame) => ({ frame: frame.frame, path: frame.path, sha256: frame.sha256 })),
      unique_frame_hash_count: uniqueFrameHashCount,
      dom_states: frames.map((frame) => summarizeDomState(frame.dom_state)),
      boundaries,
      next_safe_action: 'Use the BN-05 manual YMM4 preview gate before claiming creative acceptance; decide clip export only after frame sequence inspection.',
    };
    readback.failed_checks = Object.entries(readback.checks)
      .filter(([, passed]) => passed !== true)
      .map(([name]) => name);
    if (readback.failed_checks.length) {
      readback.status = 'failed';
    }

    writeJson(manifestRel, manifest);
    writeJson(readbackRel, readback);
    const handoffFull = resolveRepoPath(handoffRel);
    fs.mkdirSync(path.dirname(handoffFull), { recursive: true });
    fs.writeFileSync(handoffFull, buildHandoff(manifestRel, readbackRel, frameDirRel), 'utf8');
    console.log(JSON.stringify(readback, null, 2));
    if (readback.status !== 'passed') {
      throw new Error(`baseball frame sequence readback failed: ${readback.failed_checks.join(', ')}`);
    }
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

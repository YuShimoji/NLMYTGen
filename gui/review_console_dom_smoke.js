const path = require('path');
const { app, BrowserWindow } = require('electron');

const expectedSegmentCount = 11;

async function run() {
  app.commandLine.appendSwitch('disable-gpu');
  await app.whenReady();

  const win = new BrowserWindow({
    show: false,
    width: 1400,
    height: 1000,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      preload: path.join(__dirname, 'review_console_smoke_preload.js'),
    },
  });

  const pageErrors = [];
  win.webContents.on('console-message', (_event, level, message) => {
    if (level >= 3) pageErrors.push(message);
  });
  win.webContents.on('render-process-gone', (_event, details) => {
    pageErrors.push(`render process gone: ${details.reason}`);
  });

  await win.loadFile(path.join(__dirname, 'index.html'));

  const result = await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const snapshot = () => {
        const episode = document.getElementById('review-episode-context');
        const outline = document.getElementById('review-story-outline');
        const cards = Array.from(document.querySelectorAll('#review-card-list .review-segment-card'));
        const load = document.getElementById('review-load-result');
        const reviewTab = document.getElementById('tab-review');
        const text = reviewTab ? reviewTab.innerText : '';
        return {
          readyState: document.readyState,
          nlmytgenType: typeof window.nlmytgen,
          nlmytgenKeys: window.nlmytgen ? Object.keys(window.nlmytgen).slice(0, 12) : [],
          episodeExists: !!episode,
          episodeHidden: !!episode?.classList.contains('hidden'),
          outlineExists: !!outline,
          outlineHidden: !!outline?.classList.contains('hidden'),
          cardCount: cards.length,
          loadText: load?.innerText || '',
          hasEpisodeContextLabel: text.includes('動画全体の概略'),
          hasStoryOutlineLabel: text.includes('全体構成'),
          hasScriptExcerptLabel: text.includes('該当台本抜粋'),
          hasCorruption: /\\?\\?\\?|�/.test(text),
          textSample: text.slice(0, 500),
        };
      };
      const timer = setInterval(() => {
        try {
          document.querySelector('[data-tab="review"]')?.click();
          const state = snapshot();
          const ready = state.episodeExists && state.outlineExists
            && !state.episodeHidden
            && !state.outlineHidden
            && state.cardCount === ${expectedSegmentCount}
            && state.hasEpisodeContextLabel
            && state.hasStoryOutlineLabel
            && state.hasScriptExcerptLabel;
          if (ready) {
            clearInterval(timer);
            resolve(state);
          } else if (Date.now() - started > 5000) {
            clearInterval(timer);
            reject(new Error('review console DOM did not become ready: ' + JSON.stringify(snapshot())));
          }
        } catch (err) {
          clearInterval(timer);
          reject(err);
        }
      }, 50);
    })
  `);

  if (pageErrors.length) {
    throw new Error(`renderer console errors: ${pageErrors.join('\\n')}`);
  }
  if (result.episodeHidden) throw new Error('review-episode-context is hidden');
  if (result.outlineHidden) throw new Error('review-story-outline is hidden');
  if (result.cardCount !== expectedSegmentCount) {
    throw new Error(`expected ${expectedSegmentCount} review cards, got ${result.cardCount}`);
  }
  if (result.hasCorruption) {
    throw new Error(`review tab contains corrupted text marker: ${result.textSample}`);
  }
  console.log(`G-27 review console DOM smoke OK: ${result.cardCount} cards`);
}

run()
  .catch((err) => {
    console.error(err.stack || err.message || String(err));
    app.exit(1);
  })
  .finally(() => app.quit());

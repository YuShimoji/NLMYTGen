const path = require('path');
const { app, BrowserWindow } = require('electron');

const expectedSegmentCount = 11;
const expectedProofFrameCount = 9;
const expectedProofSegmentCount = 3;

async function run() {
  app.setPath('userData', path.join(__dirname, '..', '_tmp', 'electron_review_console_dom_smoke'));
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
        const timeline = Array.from(document.querySelectorAll('#review-timeline .review-timeline-segment'));
        const detail = document.getElementById('review-segment-detail');
        const inspector = document.querySelector('.review-decision-inspector');
        const proof = document.getElementById('review-treatment-proof');
        const pipeline = document.getElementById('pipeline-smoke-review');
        const proofImage = proof?.querySelector('.review-proof-image-card img');
        const pipelineTopics = Array.from(pipeline?.querySelectorAll('.pipeline-smoke-topic') || []);
        const pipelineImages = Array.from(pipeline?.querySelectorAll('.review-proof-image-card img') || []);
        const pipelineBeatRows = Array.from(pipeline?.querySelectorAll('.review-beat-table tbody tr') || []);
        const proofBadges = Array.from(document.querySelectorAll('#review-timeline .review-timeline-proof'));
        const beatRows = Array.from(document.querySelectorAll('#review-treatment-proof .review-beat-table tbody tr'));
        const wizard = document.getElementById('wizard-bar');
        const bodyContent = document.querySelector('.body-content');
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
          timelineCount: timeline.length,
          activeTimelineCount: timeline.filter((item) => item.classList.contains('active')).length,
          detailExists: !!detail,
          detailText: detail?.innerText || '',
          inspectorExists: !!inspector,
          inspectorText: inspector?.innerText || '',
          proofExists: !!proof,
          proofText: proof?.innerText || '',
          proofImageSrc: proofImage?.getAttribute('src') || '',
          pipelineExists: !!pipeline,
          pipelineText: pipeline?.innerText || '',
          pipelineTopicCount: pipelineTopics.length,
          pipelineImageCount: pipelineImages.length,
          pipelineBeatRowCount: pipelineBeatRows.length,
          proofBadgeCount: proofBadges.length,
          beatRowCount: beatRows.length,
          bodyReviewClass: !!bodyContent?.classList.contains('review-workbench-active'),
          wizardDisplay: wizard ? getComputedStyle(wizard).display : '',
          loadText: load?.innerText || '',
          hasEpisodeContextLabel: text.includes('動画全体の概略'),
          hasStoryOutlineLabel: text.includes('全体構成'),
          hasTimelineLabel: text.includes('全体タイムライン'),
          hasScriptExcerptLabel: text.includes('該当台本抜粋'),
          hasDecisionInspectorLabel: text.includes('判断ペイン'),
          hasTreatmentProofLabel: text.includes('9-frame visual treatment proof'),
          hasTreatmentProofV2Label: text.includes('9-frame visual treatment proof v2'),
          hasProofFrameCount: text.includes('${expectedProofFrameCount} frames'),
          hasProofTargets: text.includes('RE-02') && text.includes('RE-06') && text.includes('RE-07D'),
          hasProofWarnings: text.includes('sidecar warnings'),
          hasFrameContract: text.includes('Frame Contract違反'),
          hasReadOnlyDecisionContext: text.includes('read-only decision context'),
          hasLabelOffCheck: text.includes('label-off check'),
          hasNarrationCompetitionCheck: text.includes('narration competition check'),
          hasRealEstateTextureCheck: text.includes('real-estate texture check'),
          hasMotionReadinessCheck: text.includes('motion-readiness check'),
          hasLabelOffStatus: text.includes('at_least_partial_pass'),
          hasTextureStatus: text.includes('pass_or_strong_partial'),
          hasMotionPrimitiveHeader: text.includes('motion primitives'),
          hasMotionPrimitiveActions: text.includes('enter:') && text.includes('reveal:') && text.includes('dim:'),
          hasAntiPatternCorpus: text.includes('anti-pattern corpus') && text.includes('Production assetでもlayout見本でもありません'),
          hasPipelineSmokeLabel: text.includes('Multi-topic pipeline smoke'),
          hasPipelineSmokeTopics: text.includes('Real Estate DX baseline') && text.includes('AI monitoring labor') && text.includes('Baseball news infographic'),
          hasPipelineSmokeStatuses: text.includes('reviewable') && text.includes('blocked'),
          hasPipelineBlockedReason: text.includes('blocked reason') && text.includes('production asset/proxy classification') && text.includes('data/provenance fixture'),
          hasPipelineNextAction: text.includes('next action') && text.includes('screen-plan smoke'),
          hasPipelineDecisionPaths: text.includes('review_decisions.json') && text.includes('decision artifact'),
          hasPipelineDiagnostics: text.includes('case overfitting') && text.includes('docs-only loop') && text.includes('standalone proof completion'),
          hasStandaloneGuard: text.includes('standalone completion: false'),
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
            && state.bodyReviewClass
            && state.wizardDisplay === 'none'
            && state.timelineCount === ${expectedSegmentCount}
            && state.activeTimelineCount === 1
            && state.detailExists
            && state.inspectorExists
            && state.proofExists
            && state.pipelineExists
            && state.proofBadgeCount === ${expectedProofSegmentCount}
            && state.proofImageSrc.includes('real_estate_dx_visual_treatment_proof.png')
            && state.pipelineTopicCount === 3
            && state.pipelineImageCount === 3
            && state.pipelineBeatRowCount === 9
            && state.cardCount === ${expectedSegmentCount}
            && state.hasEpisodeContextLabel
            && state.hasStoryOutlineLabel
            && state.hasTimelineLabel
            && state.hasScriptExcerptLabel
            && state.hasDecisionInspectorLabel
            && state.hasTreatmentProofLabel
            && state.hasTreatmentProofV2Label
            && state.hasProofFrameCount
            && state.hasProofTargets
            && state.hasProofWarnings
            && state.hasFrameContract
            && state.hasReadOnlyDecisionContext
            && state.hasLabelOffCheck
            && state.hasNarrationCompetitionCheck
            && state.hasRealEstateTextureCheck
            && state.hasMotionReadinessCheck
            && state.hasLabelOffStatus
            && state.hasTextureStatus
            && state.hasMotionPrimitiveHeader
            && state.hasAntiPatternCorpus
            && state.hasPipelineSmokeLabel
            && state.hasPipelineSmokeTopics
            && state.hasPipelineSmokeStatuses
            && state.hasPipelineBlockedReason
            && state.hasPipelineNextAction
            && state.hasPipelineDecisionPaths
            && state.hasPipelineDiagnostics
            && state.hasStandaloneGuard;
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
  if (!result.bodyReviewClass) throw new Error('review workbench class is not active');
  if (result.wizardDisplay !== 'none') throw new Error(`wizard should be hidden in review workbench, got ${result.wizardDisplay}`);
  if (result.timelineCount !== expectedSegmentCount) {
    throw new Error(`expected ${expectedSegmentCount} timeline segments, got ${result.timelineCount}`);
  }
  if (result.activeTimelineCount !== 1) {
    throw new Error(`expected 1 active timeline segment, got ${result.activeTimelineCount}`);
  }
  if (result.cardCount !== expectedSegmentCount) {
    throw new Error(`expected ${expectedSegmentCount} review summary rows, got ${result.cardCount}`);
  }
  if (result.proofBadgeCount !== expectedProofSegmentCount) {
    throw new Error(`expected ${expectedProofSegmentCount} proof timeline badges, got ${result.proofBadgeCount}`);
  }
  if (!result.proofImageSrc.includes('real_estate_dx_visual_treatment_proof.png')) {
    throw new Error(`proof image did not render in GUI: ${result.proofImageSrc}`);
  }
  if (!result.proofText.includes('Frame Contract違反: 0')) {
    throw new Error(`proof panel did not expose Frame Contract status: ${result.proofText.slice(0, 300)}`);
  }
  if (!result.proofText.includes('sidecar warnings')) {
    throw new Error(`proof panel did not expose sidecar warnings: ${result.proofText.slice(0, 300)}`);
  }
  if (result.pipelineTopicCount !== 3 || result.pipelineImageCount !== 3 || result.pipelineBeatRowCount !== 9) {
    throw new Error(`pipeline smoke panel did not expose 3 topics / images / 9 beat rows: ${JSON.stringify({
      topics: result.pipelineTopicCount,
      images: result.pipelineImageCount,
      rows: result.pipelineBeatRowCount,
    })}`);
  }
  for (const text of ['Real Estate DX baseline', 'AI monitoring labor', 'Baseball news infographic', 'blocked reason', 'next action', 'review_decisions.json']) {
    if (!result.pipelineText.includes(text)) {
      throw new Error(`pipeline smoke panel missing ${text}: ${result.pipelineText.slice(0, 500)}`);
    }
  }
  for (const label of ['label-off check', 'narration competition check', 'real-estate texture check', 'motion-readiness check']) {
    if (!result.proofText.includes(label)) {
      throw new Error(`proof panel did not expose ${label}: ${result.proofText.slice(0, 500)}`);
    }
  }
  for (const status of ['at_least_partial_pass', 'pass_or_strong_partial']) {
    if (!result.proofText.includes(status)) {
      throw new Error(`proof panel did not expose improved check status ${status}: ${result.proofText.slice(0, 500)}`);
    }
  }
  if (result.proofText.includes('needs_human_review')) {
    throw new Error(`label-off check did not improve from needs_human_review: ${result.proofText.slice(0, 500)}`);
  }
  if (!result.detailText.includes('該当台本抜粋')) {
    throw new Error(`review segment detail did not render script context: ${result.detailText.slice(0, 200)}`);
  }
  if (!result.inspectorText.includes('全体判断')) {
    throw new Error(`review decision inspector did not render controls: ${result.inspectorText.slice(0, 200)}`);
  }
  if (result.hasCorruption) {
    throw new Error(`review tab contains corrupted text marker: ${result.textSample}`);
  }

  const proofSegments = await win.webContents.executeJavaScript(`
    (() => {
      const expected = [
        { index: 1, id: 'RE-02', cue: 'レインズっていう言葉' },
        { index: 5, id: 'RE-06', cue: '選択肢が多すぎること' },
        { index: 9, id: 'RE-07D', cue: '100%マッチ' },
      ];
      return expected.map((item) => {
        document.querySelector('[data-review-index="' + item.index + '"]')?.click();
        const proof = document.getElementById('review-treatment-proof');
        const rows = Array.from(proof.querySelectorAll('.review-beat-table tbody tr'));
        const text = proof.innerText;
        return {
          id: item.id,
          rowCount: rows.length,
          hasCue: text.includes(item.cue),
          hasNarrationCueHeader: text.includes('narration cue'),
          hasSubtitleClearance: text.includes('subtitle clearance'),
          hasMotionPrimitiveHeader: text.includes('motion primitives'),
          hasMotionPrimitiveActions: text.includes('enter:') && text.includes('reveal:') && text.includes('dim:'),
          hasNoViolation: text.includes('違反なし'),
        };
      });
    })()
  `);
  for (const item of proofSegments) {
    if (item.rowCount !== 3 || !item.hasCue || !item.hasNarrationCueHeader || !item.hasSubtitleClearance || !item.hasMotionPrimitiveHeader || !item.hasMotionPrimitiveActions || !item.hasNoViolation) {
      throw new Error(`proof beat table did not render for ${item.id}: ${JSON.stringify(item)}`);
    }
  }
  await win.webContents.executeJavaScript(`
    document.querySelector('[data-review-index="0"]')?.click();
  `);

  const saveResult = await win.webContents.executeJavaScript(`
    (async () => {
      const select = document.getElementById('review-active-decision');
      const firstDecision = Array.from(select.options).find((option) => option.value);
      if (!firstDecision) throw new Error('active segment has no decision options');
      select.value = firstDecision.value;
      select.dispatchEvent(new Event('change', { bubbles: true }));

      const comment = document.getElementById('review-active-comment');
      comment.value = 'DOM smoke comment';
      comment.dispatchEvent(new Event('input', { bubbles: true }));

      document.getElementById('btn-review-save-decisions').click();

      const started = Date.now();
      while (Date.now() - started < 2000) {
        const saved = await window.nlmytgen.getLastReviewDecisionSave();
        if (saved?.payload?.decisions?.length) return saved;
        await new Promise((resolve) => setTimeout(resolve, 50));
      }
      throw new Error('review decisions were not saved by DOM smoke');
    })()
  `);

  const decisions = saveResult?.payload?.decisions || [];
  if (decisions.length !== expectedSegmentCount) {
    throw new Error(`expected ${expectedSegmentCount} saved decisions, got ${decisions.length}`);
  }
  if (!decisions[0].decision) throw new Error('first saved decision is empty');
  if (decisions[0].comment !== 'DOM smoke comment') {
    throw new Error(`first saved comment mismatch: ${decisions[0].comment}`);
  }
  if (saveResult.payload.version !== '1.0') {
    throw new Error(`review_decisions version changed: ${saveResult.payload.version}`);
  }

  console.log(`G-27 review console DOM smoke OK: ${result.timelineCount} timeline segments; ${expectedProofFrameCount} G-27 proof frames; ${result.pipelineTopicCount} pipeline smoke topics / ${result.pipelineBeatRowCount} smoke beats visible through GUI; save payload OK`);
}

run()
  .catch((err) => {
    console.error(err.stack || err.message || String(err));
    app.exit(1);
  })
  .finally(() => app.quit());

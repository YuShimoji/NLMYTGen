const path = require('path');
const { app, BrowserWindow } = require('electron');

const expectedSegmentCount = 11;
const expectedProofFrameCount = 9;
const expectedProofSegmentCount = 3;
const expectedNewsroomArtifactCount = 13;
const expectedNewsroomEpisodeBeatCount = 2;
const expectedNewsroomEpisodeVisualCount = 2;

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
        const g28 = document.getElementById('g28-review-console-ingest');
        const newsroom = document.getElementById('newsroom-handoff-review');
        const proofImage = proof?.querySelector('.review-proof-image-card img');
        const pipelineTopics = Array.from(pipeline?.querySelectorAll('.pipeline-smoke-topic') || []);
        const pipelineImages = Array.from(pipeline?.querySelectorAll('.review-proof-image-card img') || []);
        const pipelineBeatRows = Array.from(pipeline?.querySelectorAll('.review-beat-table tbody tr') || []);
        const g28ArtifactRows = Array.from(g28?.querySelectorAll('.g28-artifact-table tbody tr') || []);
        const newsroomArtifactRows = Array.from(newsroom?.querySelectorAll('.newsroom-artifact-table tbody tr') || []);
        const newsroomLinkageRows = Array.from(newsroom?.querySelectorAll('[data-newsroom-linkage-row]') || []);
        const newsroomPlanningGroups = Array.from(newsroom?.querySelectorAll('[data-newsroom-planning-blocker-group]') || []);
        const newsroomUnlockRows = Array.from(newsroom?.querySelectorAll('[data-newsroom-unlock-requirement]') || []);
        const newsroomProhibitedActions = Array.from(newsroom?.querySelectorAll('[data-newsroom-prohibited-action]') || []);
        const newsroomAllowedActions = Array.from(newsroom?.querySelectorAll('[data-newsroom-allowed-action]') || []);
        const newsroomCapsuleBadges = Array.from(newsroom?.querySelectorAll('[data-newsroom-capsule-badge]') || []);
        const newsroomEpisodeBeatRows = Array.from(newsroom?.querySelectorAll('[data-newsroom-episode-beat]') || []);
        const newsroomEpisodeVisualRows = Array.from(newsroom?.querySelectorAll('[data-newsroom-episode-visual]') || []);
        const newsroomEpisodeTimelineBeats = Array.from(newsroom?.querySelectorAll('[data-newsroom-episode-timeline-beat]') || []);
        const newsroomCapsuleBlockerGroups = Array.from(newsroom?.querySelectorAll('[data-newsroom-capsule-blocker-group]') || []);
        const newsroomCapsuleGaps = Array.from(newsroom?.querySelectorAll('[data-newsroom-capsule-gap]') || []);
        const newsroomCapsuleNextSteps = Array.from(newsroom?.querySelectorAll('[data-newsroom-capsule-next-step]') || []);
        const newsroomCapsuleProhibitedSteps = Array.from(newsroom?.querySelectorAll('[data-newsroom-capsule-prohibited-step]') || []);
        const proofBadges = Array.from(document.querySelectorAll('#review-timeline .review-timeline-proof'));
        const beatRows = Array.from(document.querySelectorAll('#review-treatment-proof .review-beat-table tbody tr'));
        const wizard = document.getElementById('wizard-bar');
        const bodyContent = document.querySelector('.body-content');
        const load = document.getElementById('review-load-result');
        const reviewTab = document.getElementById('tab-review');
        const text = reviewTab ? reviewTab.innerText : '';
        const g28Text = g28?.innerText || '';
        const newsroomText = newsroom?.innerText || '';
        const forbiddenG28DecisionLabels = [
          'production_approve',
          'creative_final_acceptance',
          'render_approve',
          'rights_approve',
          'public_use_approve',
        ];
        const forbiddenNewsroomStates = [
          'production_visual_approval=true',
          'ymm4_transfer_ready=true',
          'external_fetch=true',
          'raw_source_material=true',
          'production_approve',
          'render_approve',
          'rights_approve',
          'public_use_approve',
        ];
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
          g28Exists: !!g28,
          g28Text,
          g28ArtifactRowCount: g28ArtifactRows.length,
          newsroomExists: !!newsroom,
          newsroomText,
          newsroomArtifactRowCount: newsroomArtifactRows.length,
          newsroomLinkageRowCount: newsroomLinkageRows.length,
          newsroomPlanningGroupCount: newsroomPlanningGroups.length,
          newsroomUnlockRowCount: newsroomUnlockRows.length,
          newsroomProhibitedActionCount: newsroomProhibitedActions.length,
          newsroomAllowedActionCount: newsroomAllowedActions.length,
          newsroomCapsuleBadgeCount: newsroomCapsuleBadges.length,
          newsroomEpisodeBeatRowCount: newsroomEpisodeBeatRows.length,
          newsroomEpisodeVisualRowCount: newsroomEpisodeVisualRows.length,
          newsroomEpisodeTimelineBeatCount: newsroomEpisodeTimelineBeats.length,
          newsroomCapsuleBlockerGroupCount: newsroomCapsuleBlockerGroups.length,
          newsroomCapsuleGapCount: newsroomCapsuleGaps.length,
          newsroomCapsuleNextStepCount: newsroomCapsuleNextSteps.length,
          newsroomCapsuleProhibitedStepCount: newsroomCapsuleProhibitedSteps.length,
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
          hasG28Label: g28Text.includes('G-28 real_estate_information_gap YMM4 diagnostic probe'),
          hasG28Artifacts: g28Text.includes('lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp')
            && g28Text.includes('lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json')
            && g28Text.includes('G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md')
            && g28Text.includes('G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07.md'),
          hasG28Badges: g28Text.includes('diagnostic_only=true')
            && g28Text.includes('production_candidate=false')
            && g28Text.includes('human_calibrated_override=true')
            && g28Text.includes('layout_metric_debt=true')
            && g28Text.includes('host_placeholder=true')
            && g28Text.includes('render=false')
            && g28Text.includes('rights_public_use=false'),
          hasG28ReadbackSummary: g28Text.includes('variant_id')
            && g28Text.includes('g28_ldc_real_estate_information_gap')
            && g28Text.includes('classification')
            && g28Text.includes('pass_callout_label_human_calibrated')
            && g28Text.includes('caption_reserve_clear')
            && g28Text.includes('focal_chain_count')
            && g28Text.includes('callout_count')
            && g28Text.includes('host_role')
            && g28Text.includes('external_image_count')
            && g28Text.includes('external_url_count')
            && g28Text.includes('source_footage_count')
            && g28Text.includes('audio_count')
            && g28Text.includes('tts_count')
            && g28Text.includes('render_output_count')
            && g28Text.includes('actual_x')
            && g28Text.includes('313'),
          hasG28HumanSummary: g28Text.includes('openability')
            && g28Text.includes('callout_label_alignment_仲介インセンティブ')
            && g28Text.includes('title_position')
            && g28Text.includes('host_placeholders')
            && g28Text.includes('accept_for_review_console_ingest_candidate_with_layout_metric_caveat'),
          hasG28AllowedDecisions: g28Text.includes('accept_as_diagnostic_review_surface')
            && g28Text.includes('request_readback_fix')
            && g28Text.includes('request_layout_system_redesign')
            && g28Text.includes('defer_review_console_ingest')
            && g28Text.includes('reject_probe_path'),
          hasG28Caveats: g28Text.includes('human-calibrated override')
            && g28Text.includes('title y=-474.5')
            && g28Text.includes('host placeholders are diagnostic-only')
            && g28Text.includes('glyph optical center'),
          hasG28ForbiddenDecisionLabels: forbiddenG28DecisionLabels.some((label) => g28Text.includes(label)),
          hasNewsroomLabel: newsroomText.includes('Newsroom handoff diagnostics'),
          hasNewsroomEpisode: newsroomText.includes('fake-newsroom-episode-0001')
            && newsroomText.includes('Placeholder Policy Explainer Episode'),
          hasNewsroomStatuses: newsroomText.includes('validator_status=passed')
            && newsroomText.includes('transfer_status=blocked')
            && newsroomText.includes('slot_linkage_status=passed_with_warnings')
            && newsroomText.includes('transfer_planning_status=blocked')
            && newsroomText.includes('planning_transfer_status=blocked')
            && newsroomText.includes('ymm4_transfer_ready=false')
            && newsroomText.includes('review_surface_ready=true')
            && newsroomText.includes('production_visual_approval=false'),
          hasNewsroomPlanningState: newsroomText.includes('transfer planning state')
            && newsroomText.includes('blocker_count')
            && newsroomText.includes('14')
            && newsroomText.includes('unlock_requirement_count')
            && newsroomText.includes('warning_count')
            && newsroomText.includes('Not a transfer candidate yet'),
          hasNewsroomPlanningBlockers: newsroomText.includes('transfer blockers')
            && newsroomText.includes('rights/provenance')
            && newsroomText.includes('media/source availability')
            && newsroomText.includes('review approval')
            && newsroomText.includes('visual readiness')
            && newsroomText.includes('downstream/YMM4 readiness')
            && newsroomText.includes('rights_summary_blocks_ymm4_transfer')
            && newsroomText.includes('visual_slot_gaps_present'),
          hasNewsroomUnlockRequirements: newsroomText.includes('unlock requirements')
            && newsroomText.includes('Record cleared rights')
            && newsroomText.includes('Replace placeholder-only visual plans')
            && newsroomText.includes('Keep YMM4 transfer closed'),
          hasNewsroomPlanningActions: newsroomText.includes('prohibited next actions')
            && newsroomText.includes('.ymmp generation')
            && newsroomText.includes('render generation')
            && newsroomText.includes('external fetch')
            && newsroomText.includes('production approval')
            && newsroomText.includes('allowed next actions')
            && newsroomText.includes('real packet readiness checklist')
            && newsroomText.includes('fixture/schema refinement')
            && newsroomText.includes('read-only planning panel review'),
          hasNewsroomRights: newsroomText.includes('clearance_state')
            && newsroomText.includes('synthetic_fixture_only')
            && newsroomText.includes('blocked_uses')
            && newsroomText.includes('YMM4_transfer')
            && newsroomText.includes('external_source_fetch')
            && newsroomText.includes('external_fetch=false')
            && newsroomText.includes('raw_source_material=false'),
          hasNewsroomWarnings: newsroomText.includes('rw_001 / blocker')
            && newsroomText.includes('rw_002 / caution')
            && newsroomText.includes('MISSING_G28_SLOT_HINT: vis_001->callout_box,caption_reserve')
            && newsroomText.includes('downstream_blocking_reason:no_approved_media_assets'),
          hasNewsroomCounts: newsroomText.includes('script_beat_count')
            && newsroomText.includes('3')
            && newsroomText.includes('visual_plan_count')
            && newsroomText.includes('2')
            && newsroomText.includes('slot_linkage_rows')
            && newsroomText.includes('4'),
          hasNewsroomSlotRows: newsroomText.includes('screenshot_slot')
            && newsroomText.includes('source_note')
            && newsroomText.includes('quote_card')
            && newsroomText.includes('caption_reserve')
            && newsroomText.includes('screenshot_callout.html')
            && newsroomText.includes('article_quote_card.html'),
          hasNewsroomReferences: newsroomText.includes('minimal_episode_packet.json')
            && newsroomText.includes('g28_slot_linkage_readback.json')
            && newsroomText.includes('transfer_planning_readback.json')
            && newsroomText.includes('adapted_newsroom_export_packet.json')
            && newsroomText.includes('episode_production_capsule_v1.json')
            && newsroomText.includes('NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md')
            && newsroomText.includes('NEWSROOM_REVIEW_CONSOLE_EPISODE_PREVIEW_V1_2026-06-22.md')
            && newsroomText.includes('NEWSROOM_HANDOFF_VALIDATOR_V1_2026-06-20.md')
            && newsroomText.includes('NEWSROOM_G28_SLOT_LINKAGE_PROOF_V1_2026-06-20.md')
            && newsroomText.includes('NEWSROOM_TRANSFER_PLANNING_PROOF_V1_2026-06-20.md'),
          hasNewsroomBoundary: (newsroomText.includes('read-only consumer')
            && newsroomText.includes('YMM4 transfer')
            && newsroomText.includes('production visual approval')
            && newsroomText.includes('external fetch')
            && newsroomText.includes('blocked transfer is intentional'))
            || newsroomText.includes('blocked transfer は意図した安全停止です'),
          hasNewsroomEpisodePreview: newsroomText.includes('Newsroom episode preview')
            && newsroomText.includes('episode_fake_nlmytgen_delta_v1')
            && newsroomText.includes('Fake upstream export delta for NLMYTGen')
            && newsroomText.includes('newsroom_episode_production_capsule.v1'),
          hasNewsroomCapsuleReadiness: newsroomText.includes('diagnostic_only=true')
            && newsroomText.includes('production_status=diagnostic_only')
            && newsroomText.includes('capsule_transfer_status=blocked')
            && newsroomText.includes('audio_readiness=not_started')
            && newsroomText.includes('public_video=false')
            && newsroomText.includes('ymmp_generated=false')
            && newsroomText.includes('render_generated=false')
            && newsroomText.includes('real_source_fetch=false'),
          hasNewsroomCapsuleStructure: newsroomText.includes('ScriptIR-like beat preview')
            && newsroomText.includes('VisualIR / G-28 slot preview')
            && newsroomText.includes('beat_fake_intro_001')
            && newsroomText.includes('beat_fake_claim_001')
            && newsroomText.includes('visual_fake_title_card_001')
            && newsroomText.includes('visual_fake_evidence_card_001')
            && newsroomText.includes('article_quote_card')
            && newsroomText.includes('caption_reserve')
            && newsroomText.includes('total_approx_duration_seconds')
            && newsroomText.includes('68'),
          hasNewsroomCapsuleActions: newsroomText.includes('remaining gaps before importable proof')
            && newsroomText.includes('rights and provenance are not cleared')
            && newsroomText.includes('Review Console episode preview')
            && newsroomText.includes('caption/timing refinement')
            && newsroomText.includes('YMM4 transfer candidate proof only after blockers are resolved')
            && newsroomText.includes('real source fetch')
            && newsroomText.includes('YMM4 carrier generation')
            && newsroomText.includes('public-use approval'),
          hasNewsroomForbiddenStates: forbiddenNewsroomStates.some((label) => newsroomText.includes(label)),
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
            && state.g28Exists
            && state.g28ArtifactRowCount === 5
            && state.newsroomExists
            && state.newsroomArtifactRowCount === ${expectedNewsroomArtifactCount}
            && state.newsroomLinkageRowCount === 4
            && state.newsroomPlanningGroupCount === 5
            && state.newsroomUnlockRowCount === 14
            && state.newsroomProhibitedActionCount >= 4
            && state.newsroomAllowedActionCount >= 3
            && state.newsroomCapsuleBadgeCount >= 8
            && state.newsroomEpisodeBeatRowCount === ${expectedNewsroomEpisodeBeatCount}
            && state.newsroomEpisodeVisualRowCount === ${expectedNewsroomEpisodeVisualCount}
            && state.newsroomEpisodeTimelineBeatCount === ${expectedNewsroomEpisodeBeatCount}
            && state.newsroomCapsuleBlockerGroupCount === 5
            && state.newsroomCapsuleGapCount >= 8
            && state.newsroomCapsuleNextStepCount >= 3
            && state.newsroomCapsuleProhibitedStepCount >= 9
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
            && state.hasStandaloneGuard
            && state.hasG28Label
            && state.hasG28Artifacts
            && state.hasG28Badges
            && state.hasG28ReadbackSummary
            && state.hasG28HumanSummary
            && state.hasG28AllowedDecisions
            && state.hasG28Caveats
            && !state.hasG28ForbiddenDecisionLabels
            && state.hasNewsroomLabel
            && state.hasNewsroomEpisode
            && state.hasNewsroomStatuses
            && state.hasNewsroomPlanningState
            && state.hasNewsroomPlanningBlockers
            && state.hasNewsroomUnlockRequirements
            && state.hasNewsroomPlanningActions
            && state.hasNewsroomRights
            && state.hasNewsroomWarnings
            && state.hasNewsroomCounts
            && state.hasNewsroomSlotRows
            && state.hasNewsroomReferences
            && state.hasNewsroomBoundary
            && state.hasNewsroomEpisodePreview
            && state.hasNewsroomCapsuleReadiness
            && state.hasNewsroomCapsuleStructure
            && state.hasNewsroomCapsuleActions
            && !state.hasNewsroomForbiddenStates;
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
  if (!result.g28Exists || result.g28ArtifactRowCount !== 5) {
    throw new Error(`G-28 ingest panel did not expose five artifacts: ${JSON.stringify({
      exists: result.g28Exists,
      rows: result.g28ArtifactRowCount,
    })}`);
  }
  for (const text of [
    'G-28 real_estate_information_gap YMM4 diagnostic probe',
    'diagnostic_only=true',
    'production_candidate=false',
    'human_calibrated_override=true',
    'layout_metric_debt=true',
    'host_placeholder=true',
    'render=false',
    'rights_public_use=false',
    'g28_ldc_real_estate_information_gap',
    'pass_callout_label_human_calibrated',
    'actual_x',
    '313',
    'accept_as_diagnostic_review_surface',
    'request_layout_system_redesign',
    'accept_for_review_console_ingest_candidate_with_layout_metric_caveat',
  ]) {
    if (!result.g28Text.includes(text)) {
      throw new Error(`G-28 ingest panel missing ${text}: ${result.g28Text.slice(0, 800)}`);
    }
  }
  if (result.hasG28ForbiddenDecisionLabels) {
    throw new Error(`G-28 ingest panel exposed a forbidden production decision label: ${result.g28Text.slice(0, 800)}`);
  }
  if (!result.newsroomExists || result.newsroomArtifactRowCount !== expectedNewsroomArtifactCount || result.newsroomLinkageRowCount !== 4) {
    throw new Error(`newsroom handoff panel did not expose artifacts and slot rows: ${JSON.stringify({
      exists: result.newsroomExists,
      artifacts: result.newsroomArtifactRowCount,
      linkages: result.newsroomLinkageRowCount,
    })}`);
  }
  if (
    result.newsroomCapsuleBadgeCount < 8
    || result.newsroomEpisodeBeatRowCount !== expectedNewsroomEpisodeBeatCount
    || result.newsroomEpisodeVisualRowCount !== expectedNewsroomEpisodeVisualCount
    || result.newsroomEpisodeTimelineBeatCount !== expectedNewsroomEpisodeBeatCount
    || result.newsroomCapsuleBlockerGroupCount !== 5
    || result.newsroomCapsuleGapCount < 8
    || result.newsroomCapsuleNextStepCount < 3
    || result.newsroomCapsuleProhibitedStepCount < 9
  ) {
    throw new Error(`newsroom episode preview did not expose expected capsule structure: ${JSON.stringify({
      badges: result.newsroomCapsuleBadgeCount,
      beats: result.newsroomEpisodeBeatRowCount,
      visuals: result.newsroomEpisodeVisualRowCount,
      timeline: result.newsroomEpisodeTimelineBeatCount,
      blockerGroups: result.newsroomCapsuleBlockerGroupCount,
      gaps: result.newsroomCapsuleGapCount,
      nextSteps: result.newsroomCapsuleNextStepCount,
      prohibited: result.newsroomCapsuleProhibitedStepCount,
    })}`);
  }
  if (result.newsroomPlanningGroupCount !== 5 || result.newsroomUnlockRowCount !== 14) {
    throw new Error(`newsroom transfer planning panel did not expose blocker groups and unlock rows: ${JSON.stringify({
      groups: result.newsroomPlanningGroupCount,
      unlocks: result.newsroomUnlockRowCount,
    })}`);
  }
  if (result.newsroomProhibitedActionCount < 4 || result.newsroomAllowedActionCount < 3) {
    throw new Error(`newsroom transfer planning panel did not expose expected next actions: ${JSON.stringify({
      prohibited: result.newsroomProhibitedActionCount,
      allowed: result.newsroomAllowedActionCount,
    })}`);
  }
  for (const text of [
    'Newsroom handoff diagnostics',
    'fake-newsroom-episode-0001',
    'Placeholder Policy Explainer Episode',
    'validator_status=passed',
    'slot_linkage_status=passed_with_warnings',
    'transfer_planning_status=blocked',
    'transfer_status=blocked',
    'planning_transfer_status=blocked',
    'blocker_count',
    'unlock_requirement_count',
    'warning_count',
    'Not a transfer candidate yet',
    'rights/provenance',
    'media/source availability',
    'review approval',
    'visual readiness',
    'downstream/YMM4 readiness',
    'rights_summary_blocks_ymm4_transfer',
    'visual_slot_gaps_present',
    'Record cleared rights',
    'Replace placeholder-only visual plans',
    'Keep YMM4 transfer closed',
    '.ymmp generation',
    'render generation',
    'external fetch',
    'production approval',
    'real packet readiness checklist',
    'fixture/schema refinement',
    'read-only planning panel review',
    'ymm4_transfer_ready=false',
    'production_visual_approval=false',
    'synthetic_fixture_only',
    'YMM4_transfer',
    'rw_001 / blocker',
    'MISSING_G28_SLOT_HINT: vis_001->callout_box,caption_reserve',
    'downstream_blocking_reason:no_approved_media_assets',
    'script_beat_count',
    'visual_plan_count',
    'slot_linkage_rows',
    'screenshot_slot',
    'article_quote_card.html',
    'minimal_episode_packet.json',
    'adapted_newsroom_export_packet.json',
    'episode_production_capsule_v1.json',
    'transfer_planning_readback.json',
    'NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md',
    'NEWSROOM_REVIEW_CONSOLE_EPISODE_PREVIEW_V1_2026-06-22.md',
    'NEWSROOM_G28_SLOT_LINKAGE_PROOF_V1_2026-06-20.md',
    'NEWSROOM_TRANSFER_PLANNING_PROOF_V1_2026-06-20.md',
    'Newsroom episode preview',
    'episode_fake_nlmytgen_delta_v1',
    'newsroom_episode_production_capsule.v1',
    'diagnostic_only=true',
    'production_status=diagnostic_only',
    'capsule_transfer_status=blocked',
    'audio_readiness=not_started',
    'public_video=false',
    'ymmp_generated=false',
    'render_generated=false',
    'real_source_fetch=false',
    'ScriptIR-like beat preview',
    'VisualIR / G-28 slot preview',
    'beat_fake_intro_001',
    'beat_fake_claim_001',
    'visual_fake_title_card_001',
    'visual_fake_evidence_card_001',
    'total_approx_duration_seconds',
    'rights and provenance are not cleared',
    'Review Console episode preview',
    'caption/timing refinement',
    'YMM4 transfer candidate proof only after blockers are resolved',
    'YMM4 carrier generation',
    'public-use approval',
  ]) {
    if (!result.newsroomText.includes(text)) {
      throw new Error(`newsroom handoff panel missing ${text}: ${result.newsroomText.slice(0, 1000)}`);
    }
  }
  if (result.hasNewsroomForbiddenStates) {
    throw new Error(`newsroom handoff panel exposed a forbidden production/fetch state: ${result.newsroomText.slice(0, 1000)}`);
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

  console.log(`G-27 review console DOM smoke OK: ${result.timelineCount} timeline segments; ${expectedProofFrameCount} G-27 proof frames; ${result.pipelineTopicCount} pipeline smoke topics / ${result.pipelineBeatRowCount} smoke beats visible through GUI; G-28 diagnostic ingest panel visible; newsroom transfer planning panel visible; newsroom episode preview visible with ${result.newsroomEpisodeBeatRowCount} beats / ${result.newsroomEpisodeVisualRowCount} visuals; save payload OK`);
}

run()
  .catch((err) => {
    console.error(err.stack || err.message || String(err));
    app.exit(1);
  })
  .finally(() => app.quit());

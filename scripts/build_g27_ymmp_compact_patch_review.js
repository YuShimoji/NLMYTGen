const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const fps = 60;
const reviewDurationSec = 6;
const reviewGapSec = 0.5;
const reviewDurationFrames = reviewDurationSec * fps;
const reviewStepFrames = Math.round((reviewDurationSec + reviewGapSec) * fps);

const paths = {
  adapterIrDryRun: 'samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json',
  visualTreatmentProof: 'samples/_probe/g24/real_estate_dx_visual_treatment_proof.json',
  reviewPacket: 'samples/_probe/g24/real_estate_dx_review_packet.json',
  outputJson: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json',
  outputMd: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.md',
};

const expectedCandidateIds = [
  'RE-02-beginning',
  'RE-02-development',
  'RE-06-beginning',
  'RE-06-development',
  'RE-06-turn',
  'RE-07D-beginning',
  'RE-07D-development',
];

const itemPlans = {
  'RE-02-beginning': {
    placeholder: 'generic_public_search_panel + broker_db_shadow_panel',
    expected_visible_effect:
      'A public search panel dims while a generic broker DB panel appears behind it; no official REINS UI is shown.',
    planned_items: [
      {
        item_id: 'RE02_BEGIN_PUBLIC_SEARCH_PROXY',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'generic public-search card placeholder',
      },
      {
        item_id: 'RE02_BEGIN_BROKER_DB_SHADOW',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'dark broker-database abstraction behind the public card',
      },
      {
        item_id: 'RE02_BEGIN_ACCESS_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'short access-gap label',
      },
    ],
  },
  'RE-02-development': {
    placeholder: 'broker_db_panel + public_portal_card + property_card_flow',
    expected_visible_effect:
      'Many generic property cards flow from the broker DB panel into a smaller public portal card.',
    planned_items: [
      {
        item_id: 'RE02_DEV_BROKER_DB_PANEL',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'large generic broker DB panel',
      },
      {
        item_id: 'RE02_DEV_PUBLIC_PORTAL_CARD',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'smaller public portal card',
      },
      {
        item_id: 'RE02_DEV_FLOW_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'public/private volume contrast label',
      },
    ],
  },
  'RE-06-beginning': {
    placeholder: 'property_card_overload_cluster',
    expected_visible_effect:
      'A dense cluster of simple property cards crowds the upper frame while the subtitle band stays clear.',
    planned_items: [
      {
        item_id: 'RE06_BEGIN_PROPERTY_CARD_CLUSTER',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'cluster of generic property cards',
      },
      {
        item_id: 'RE06_BEGIN_DENSITY_MARKER',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'density/overload emphasis marker',
      },
      {
        item_id: 'RE06_BEGIN_OVERLOAD_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'short overload label',
      },
    ],
  },
  'RE-06-development': {
    placeholder: 'selected_property_sheet + drawback_marker',
    expected_visible_effect:
      'Noisy cards fade back while one selected property sheet and a drawback marker remain visible.',
    planned_items: [
      {
        item_id: 'RE06_DEV_SELECTED_PROPERTY_SHEET',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'selected property sheet placeholder',
      },
      {
        item_id: 'RE06_DEV_DRAWBACK_MARKER',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'drawback/risk marker badge',
      },
      {
        item_id: 'RE06_DEV_REASON_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'reason plus drawback label',
      },
    ],
  },
  'RE-06-turn': {
    placeholder: 'property_document_editorial_comparison',
    expected_visible_effect:
      'A property-document comparison frame makes the recommendation feel editorial, not just a generic lens.',
    planned_items: [
      {
        item_id: 'RE06_TURN_DOCUMENT_COMPARISON',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'property-document comparison frame',
      },
      {
        item_id: 'RE06_TURN_RECOMMENDATION_MARKER',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'editorial recommendation marker',
      },
      {
        item_id: 'RE06_TURN_CURATION_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'curation /納得 label',
      },
    ],
  },
  'RE-07D-beginning': {
    placeholder: 'abstract_ai_recommendation_panel + property_card',
    expected_visible_effect:
      'An abstract AI recommendation panel highlights a property card as a confident match without product branding.',
    planned_items: [
      {
        item_id: 'RE07D_BEGIN_AI_PANEL',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'abstract AI recommendation panel',
      },
      {
        item_id: 'RE07D_BEGIN_MATCH_PROPERTY_CARD',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'matched property card placeholder',
      },
      {
        item_id: 'RE07D_BEGIN_CONFIDENCE_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'short confidence label',
      },
    ],
  },
  'RE-07D-development': {
    placeholder: 'boundary_inheritance_neighborhood_risk_markers',
    expected_visible_effect:
      'Boundary, inheritance, and neighborhood risk markers appear behind the matched property card.',
    planned_items: [
      {
        item_id: 'RE07D_DEV_RISK_MARKER_SET',
        item_type: 'ShapeItem',
        target_layer: 7,
        add: 'abstract boundary/inheritance/neighborhood marker set',
      },
      {
        item_id: 'RE07D_DEV_PROPERTY_CONTEXT_CARD',
        item_type: 'ShapeItem',
        target_layer: 8,
        add: 'property context card behind risk markers',
      },
      {
        item_id: 'RE07D_DEV_RISK_LABEL',
        item_type: 'TextItem',
        target_layer: 9,
        add: 'short invisible-risk label',
      },
    ],
  },
};

function readText(relPath) {
  return fs.readFileSync(path.join(root, relPath), 'utf8');
}

function readJson(relPath) {
  return JSON.parse(readText(relPath));
}

function sameSet(actual, expected) {
  const actualSorted = [...actual].sort();
  const expectedSorted = [...expected].sort();
  return (
    actualSorted.length === expectedSorted.length &&
    actualSorted.every((value, index) => value === expectedSorted[index])
  );
}

function markdownEscape(value) {
  return String(value).replace(/\|/g, '\\|').replace(/\r?\n/g, '<br>');
}

function makeCheck(id, passed, evidence, failureReason = null) {
  return {
    id,
    status: passed ? 'pass' : 'fail',
    evidence,
    failure_reason: passed ? null : failureReason || 'Condition failed',
  };
}

function findVisualBeat(visualTreatmentProof, beatId) {
  for (const segment of visualTreatmentProof.segments || []) {
    for (const beat of segment.beats || []) {
      if (beat.id === beatId) return { segment, beat };
    }
  }
  return { segment: null, beat: null };
}

function findStorySegment(reviewPacket, segmentId) {
  return (reviewPacket.story_outline || []).find((segment) => segment.id === segmentId) || null;
}

function sourceBeatFromId(beatId) {
  const match = beatId.match(/^(RE-\d+[A-Z]?)-(beginning|development|turn)$/);
  return {
    candidate_id: beatId,
    segment_id: match ? match[1] : beatId,
    phase: match ? match[2] : 'unknown',
  };
}

function phaseIndex(phase) {
  if (phase === 'beginning') return 0;
  if (phase === 'development') return 1;
  if (phase === 'turn') return 2;
  return 0;
}

function estimateSourceTiming(storySegment, phase) {
  if (!storySegment) return null;
  const segmentDurationSec = storySegment.time_end_sec - storySegment.time_start_sec;
  const sliceDurationSec = segmentDurationSec / 3;
  const startSec = storySegment.time_start_sec + sliceDurationSec * phaseIndex(phase);
  const endSec = startSec + sliceDurationSec;
  return {
    start_sec: Number(startSec.toFixed(3)),
    end_sec: Number(endSec.toFixed(3)),
    duration_sec: Number(sliceDurationSec.toFixed(3)),
    basis: 'review_packet story_outline segment time split by beat phase',
  };
}

function makePlannedItems(plan, startFrame, durationFrames, sourceReference) {
  return plan.planned_items.map((item) => ({
    ...item,
    approximate_start_frame: startFrame,
    approximate_duration_frames: durationFrames,
    approximate_start_sec: Number((startFrame / fps).toFixed(3)),
    approximate_duration_sec: Number((durationFrames / fps).toFixed(3)),
    source_reference: sourceReference,
  }));
}

const adapterIrDryRun = readJson(paths.adapterIrDryRun);
const visualTreatmentProof = readJson(paths.visualTreatmentProof);
const reviewPacket = readJson(paths.reviewPacket);

function buildReview() {
  const dryRunItemsById = new Map(
    (adapterIrDryRun.items || []).map((item) => [item.source_beat.candidate_id || item.source_beat.beat_id, item]),
  );

  const candidates = expectedCandidateIds.map((candidateId, index) => {
    const dryRunItem = dryRunItemsById.get(candidateId);
    const sourceBeat = sourceBeatFromId(candidateId);
    const { beat } = findVisualBeat(visualTreatmentProof, candidateId);
    const storySegment = findStorySegment(reviewPacket, sourceBeat.segment_id);
    const startFrame = index * reviewStepFrames;
    const plan = itemPlans[candidateId];
    const sourceTiming = estimateSourceTiming(storySegment, sourceBeat.phase);
    const patchReady =
      dryRunItem?.YMM4_patch_readiness === 'ready' && Boolean(beat) && Boolean(plan);
    const blockedReason = patchReady
      ? 'none'
      : [
          dryRunItem?.YMM4_patch_readiness !== 'ready'
            ? `dry-run readiness is ${dryRunItem?.YMM4_patch_readiness || 'missing'}`
            : null,
          !beat ? 'visual treatment beat source is missing' : null,
          !plan ? 'compact patch item plan is missing' : null,
        ]
          .filter(Boolean)
          .join('; ');

    const sourceReference = {
      adapter_ir_dry_run: paths.adapterIrDryRun,
      dry_run_candidate_id: candidateId,
      visual_treatment_proof: paths.visualTreatmentProof,
      visual_treatment_beat_id: beat?.id || null,
      review_packet: paths.reviewPacket,
      story_segment_id: storySegment?.id || null,
      source_line_range: storySegment
        ? {
            line_start: storySegment.line_start,
            line_end: storySegment.line_end,
          }
        : null,
      source_timing_estimate: sourceTiming,
      narration_cue: beat?.narration_cue || null,
    };

    return {
      source_beat: sourceBeat,
      candidate_id: candidateId,
      intended_YMM4_item_type: 'ShapeItem/TextItem placeholder set',
      target_layer: 7,
      approximate_start_frame: startFrame,
      approximate_duration_frames: reviewDurationFrames,
      approximate_start_sec: Number((startFrame / fps).toFixed(3)),
      approximate_duration_sec: reviewDurationSec,
      required_template_or_proxy_primitive:
        dryRunItem?.resolved_proxy_template_primitive?.primitive_id || null,
      referenced_source_asset_or_placeholder: plan?.placeholder || null,
      expected_visible_effect: plan?.expected_visible_effect || beat?.motion_hint || null,
      actual_ymmp_patch_output_readiness: patchReady ? 'ready' : 'blocked',
      blocked_reason: blockedReason,
      source_reference: sourceReference,
      planned_items: makePlannedItems(plan, startFrame, reviewDurationFrames, sourceReference),
    };
  });

  const readyCandidates = candidates.filter(
    (candidate) => candidate.actual_ymmp_patch_output_readiness === 'ready',
  );
  const blockedCandidates = candidates.filter(
    (candidate) => candidate.actual_ymmp_patch_output_readiness === 'blocked',
  );

  return {
    version: '1.0',
    artifact_type: 'YMM4_compact_patch_review',
    episode_id: 'real_estate_dx',
    scope: 'G-27 compact YMM4 patch review for 7 adapter IR dry-run candidates',
    source: {
      adapter_ir_dry_run: paths.adapterIrDryRun,
      visual_treatment_proof: paths.visualTreatmentProof,
      review_packet: paths.reviewPacket,
    },
    boundary: {
      compact_patch_review_only: true,
      no_real_ymmp_write: true,
      no_YMM4_patch_output: true,
      no_render: true,
      no_preview_capture: true,
      no_production_timing: true,
      no_creative_acceptance: true,
      no_new_gate_policy_or_contract: true,
    },
    timeline_model: {
      fps,
      review_duration_sec: reviewDurationSec,
      review_gap_sec: reviewGapSec,
      layout: 'sequential compact review slots, not production timing',
    },
    candidates,
    excluded_items: [
      {
        candidate_id: 'RE-02-turn',
        actual_ymmp_patch_output_readiness: 'blocked',
        blocked_reason:
          'Accepted-with-adjustment proxy is not in the 7 adapter IR dry-run candidates; the opacity-layer adjustment must be reflected before compact patch review.',
      },
      {
        candidate_id: 'RE-07D-turn',
        actual_ymmp_patch_output_readiness: 'deferred',
        blocked_reason:
          'Specialist / cast / silhouette representation policy remains undecided; no compact patch review item is planned for this beat.',
      },
    ],
    rollup: {
      candidate_count: candidates.length,
      ready_for_actual_ymmp_patch_output_count: readyCandidates.length,
      ready_for_minimal_patched_ymmp_next_slice: readyCandidates.length === candidates.length,
      blocked_count: blockedCandidates.length,
      deferred_count: 0,
      excluded_blocked_count: 1,
      excluded_deferred_count: 1,
      missing_information_preventing_patch_output: blockedCandidates.map((candidate) => ({
        candidate_id: candidate.candidate_id,
        blocked_reason: candidate.blocked_reason,
      })),
      next_safe_artifact:
        readyCandidates.length === candidates.length
          ? 'minimal patched .ymmp for YMM4 readback'
          : 'fix blocked compact patch review candidates first',
    },
  };
}

function renderMarkdown(payload) {
  const lines = [];
  lines.push('# Real Estate DX YMM4 Compact Patch Review');
  lines.push('');
  lines.push(`Source: \`${payload.source.adapter_ir_dry_run}\``);
  lines.push('');
  lines.push('This is a compact review of intended YMM4 patch items. It does not write or modify a `.ymmp` file and does not render.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Candidates reviewed: \`${payload.rollup.candidate_count}\``);
  lines.push(`- Ready for actual \`.ymmp\` patch output: \`${payload.rollup.ready_for_actual_ymmp_patch_output_count}\``);
  lines.push(`- Minimal patched \`.ymmp\` can be produced next: \`${payload.rollup.ready_for_minimal_patched_ymmp_next_slice}\``);
  lines.push(`- Candidate blocked/deferred: \`${payload.rollup.blocked_count}\` / \`${payload.rollup.deferred_count}\``);
  lines.push(`- Excluded blocked/deferred: \`${payload.rollup.excluded_blocked_count}\` / \`${payload.rollup.excluded_deferred_count}\``);
  lines.push('');
  lines.push('## Review Table');
  lines.push('');
  lines.push('| candidate | item type | layer | start frame | duration | primitive | placeholder | visible effect | patch readiness | blocked reason |');
  lines.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |');
  payload.candidates.forEach((candidate) => {
    const itemTypes = [...new Set(candidate.planned_items.map((item) => item.item_type))].join(' + ');
    const layers = [...new Set(candidate.planned_items.map((item) => item.target_layer))].join(', ');
    lines.push(
      `| \`${candidate.candidate_id}\` | ${markdownEscape(itemTypes)} | ${markdownEscape(layers)} | \`${candidate.approximate_start_frame}\` | \`${candidate.approximate_duration_frames}\`f / \`${candidate.approximate_duration_sec}\`s | ${markdownEscape(candidate.required_template_or_proxy_primitive)} | ${markdownEscape(candidate.referenced_source_asset_or_placeholder)} | ${markdownEscape(candidate.expected_visible_effect)} | \`${candidate.actual_ymmp_patch_output_readiness}\` | ${markdownEscape(candidate.blocked_reason)} |`,
    );
  });
  lines.push('');
  lines.push('## Excluded Items');
  lines.push('');
  lines.push('| candidate | readiness | blocking reason |');
  lines.push('| --- | --- | --- |');
  payload.excluded_items.forEach((item) => {
    lines.push(
      `| \`${item.candidate_id}\` | \`${item.actual_ymmp_patch_output_readiness}\` | ${markdownEscape(item.blocked_reason)} |`,
    );
  });
  return `${lines.join('\n')}\n`;
}

function validateReview(payload, markdown = null) {
  const candidateIds = (payload.candidates || []).map((candidate) => candidate.candidate_id);
  const requiredCandidateFields = [
    'source_beat',
    'candidate_id',
    'intended_YMM4_item_type',
    'target_layer',
    'approximate_start_frame',
    'approximate_duration_frames',
    'required_template_or_proxy_primitive',
    'referenced_source_asset_or_placeholder',
    'expected_visible_effect',
    'actual_ymmp_patch_output_readiness',
    'blocked_reason',
    'source_reference',
    'planned_items',
  ];
  const missingCandidateFields = (payload.candidates || []).flatMap((candidate) =>
    requiredCandidateFields
      .filter((field) => candidate[field] === undefined || candidate[field] === null)
      .map((field) => `${candidate.candidate_id}:${field}`),
  );
  const missingPlannedItemFields = (payload.candidates || []).flatMap((candidate) =>
    (candidate.planned_items || []).flatMap((item) =>
      ['item_id', 'item_type', 'target_layer', 'approximate_start_frame', 'approximate_duration_frames', 'source_reference']
        .filter((field) => item[field] === undefined || item[field] === null)
        .map((field) => `${candidate.candidate_id}:${item.item_id || 'item'}:${field}`),
    ),
  );
  const readinessValues = (payload.candidates || []).map(
    (candidate) => candidate.actual_ymmp_patch_output_readiness,
  );
  const markdownHasCounts =
    !markdown ||
    (markdown.includes('Ready for actual `.ymmp` patch output: `7`') &&
      markdown.includes('Minimal patched `.ymmp` can be produced next: `true`'));

  const checks = [
    makeCheck('candidate_count', payload.candidates?.length === 7, {
      count: payload.candidates?.length || 0,
    }),
    makeCheck('candidate_ids', sameSet(candidateIds, expectedCandidateIds), {
      candidate_ids: candidateIds,
    }),
    makeCheck('candidate_fields', missingCandidateFields.length === 0, {
      missing_candidate_fields: missingCandidateFields,
    }),
    makeCheck('planned_item_fields', missingPlannedItemFields.length === 0, {
      missing_planned_item_fields: missingPlannedItemFields,
    }),
    makeCheck(
      'readiness_values',
      readinessValues.every((value) => ['ready', 'blocked', 'deferred'].includes(value)),
      { readiness_values: readinessValues },
    ),
    makeCheck(
      'rollup_ready',
      payload.rollup?.ready_for_actual_ymmp_patch_output_count === 7 &&
        payload.rollup?.ready_for_minimal_patched_ymmp_next_slice === true &&
        payload.rollup?.blocked_count === 0 &&
        payload.rollup?.deferred_count === 0,
      payload.rollup || {},
    ),
    makeCheck(
      'boundary',
      payload.boundary?.compact_patch_review_only === true &&
        payload.boundary?.no_real_ymmp_write === true &&
        payload.boundary?.no_YMM4_patch_output === true &&
        payload.boundary?.no_render === true &&
        payload.boundary?.no_new_gate_policy_or_contract === true,
      payload.boundary || {},
    ),
    makeCheck('markdown_counts', markdownHasCounts, { checked: Boolean(markdown) }),
  ];
  const failed = checks.filter((check) => check.status !== 'pass');
  if (failed.length) {
    console.error(JSON.stringify({ status: 'failed', checks }, null, 2));
    process.exit(1);
  }
}

const payload = buildReview();
const markdown = renderMarkdown(payload);

if (writeOutputs) {
  fs.writeFileSync(path.join(root, paths.outputJson), `${JSON.stringify(payload, null, 2)}\n`);
  fs.writeFileSync(path.join(root, paths.outputMd), markdown);
  validateReview(payload, markdown);
} else {
  const existingJson = readJson(paths.outputJson);
  const existingMarkdown = readText(paths.outputMd);
  const generatedJson = `${JSON.stringify(payload, null, 2)}\n`;
  validateReview(existingJson, existingMarkdown);
  if (JSON.stringify(existingJson, null, 2) + '\n' !== generatedJson || existingMarkdown !== markdown) {
    console.error('Existing compact patch review artifacts differ from generated output. Run with --write.');
    process.exit(1);
  }
}

console.log('G-27 YMM4 compact patch review OK: 7 candidates ready, no .ymmp written');

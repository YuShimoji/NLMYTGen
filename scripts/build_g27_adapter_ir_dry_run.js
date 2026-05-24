const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  authorizationGate: 'samples/_probe/g24/real_estate_dx_adapter_authorization_gate.json',
  routePreflight: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.json',
  planningCandidates: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_planning_candidates.json',
  gapReport: 'samples/_probe/g24/real_estate_dx_asset_proxy_gap_report.json',
  routeContract: 'docs/G27_ADAPTER_ROUTE_CONTRACT.md',
  outputJson: 'samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json',
  outputMd: 'samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.md',
};

const authorizationValue = 'authorize_adapter_IR_dry_run_for_7_candidates_only';

const expectedCandidateIds = [
  'RE-02-beginning',
  'RE-02-development',
  'RE-06-beginning',
  'RE-06-development',
  'RE-06-turn',
  'RE-07D-beginning',
  'RE-07D-development',
];

const expectedExcludedIds = ['RE-02-turn', 'RE-07D-turn'];

const forbiddenActions = [
  'YMM4 patch',
  '.ymmp write',
  'render',
  'production timing',
  'creative acceptance',
];

const forbiddenRepresentationPatterns = [
  { id: 'real_reins', pattern: /\breal\s+reins\b/i },
  { id: 'reins_screenshot', pattern: /\breins\s+screenshot\b/i },
  { id: 'official_logo', pattern: /\bofficial\s+logo\b/i },
  { id: 'real_listing_photo', pattern: /\breal\s+listing\s+photo\b/i },
  { id: 'real_map', pattern: /\breal\s+map\b/i },
  { id: 'registry_document', pattern: /\bregistry\s+document\b/i },
  { id: 'identifiable_record_service_ui_brand', pattern: /\bidentifiable\s+(record|service|ui|brand)/i },
  { id: 'locked_room', pattern: /\blocked-room\b/i },
  { id: 'security_facility', pattern: /\bsecurity-facility\b/i },
  { id: 'conspiracy_coded', pattern: /\bconspiracy-coded\b/i },
  { id: 'pure_lens_substitute', pattern: /\bpure\s+lens\b/i },
  { id: 'real_specialist_cast_silhouette', pattern: /\breal\s+(specialist|cast|silhouette)\b/i },
  { id: 'zero_generation', pattern: /\bzero-generation\b/i },
];

const primitiveByBeat = {
  'RE-02-beginning': {
    primitive_id: 'abstract_ui_public_search_vs_broker_db',
    primitive_family: 'abstract UI',
    description: 'Non-official public-search panel facing a broker-database abstraction.',
    components: ['public-search panel', 'broker-database panel', 'access-gap contrast'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-02-development': {
    primitive_id: 'abstract_ui_broker_db_public_portal_property_flow',
    primitive_family: 'abstract UI + property card',
    description: 'Broker DB panel, public portal card, and property-card flow as generic abstractions.',
    components: ['broker DB panel', 'public portal card', 'property-card flow'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-06-beginning': {
    primitive_id: 'property_card_overload_cluster',
    primitive_family: 'property card',
    description: 'Generic property-card overload with density control and subtitle-safe lower band.',
    components: ['property-card cluster', 'density control', 'subtitle-safe lower band'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-06-development': {
    primitive_id: 'selected_property_sheet_with_drawback_marker',
    primitive_family: 'property card + risk marker',
    description: 'Selected property sheet with drawback marker as abstract UI/document shapes.',
    components: ['selected property sheet', 'drawback marker', 'dimmed alternatives'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-06-turn': {
    primitive_id: 'property_document_editorial_comparison',
    primitive_family: 'document proxy',
    description: 'Property sheet / editorial comparison / document-backed recommendation.',
    components: ['property sheet', 'editorial comparison frame', 'recommendation marker'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-07D-beginning': {
    primitive_id: 'abstract_ai_recommendation_panel_property_card',
    primitive_family: 'AI panel + property card',
    description: 'Abstract AI recommendation panel plus property card.',
    components: ['AI recommendation panel', 'confidence indicator', 'property card'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
  },
  'RE-07D-development': {
    primitive_id: 'abstract_real_estate_risk_marker_set',
    primitive_family: 'risk marker',
    description: 'Boundary / inheritance / neighborhood risk markers as abstract symbols.',
    components: ['boundary marker', 'inheritance marker', 'neighborhood marker'],
    YMM4_candidate_surface: ['ShapeItem', 'TextItem', 'motion primitive'],
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

function hasAll(values, expected) {
  return expected.every((value) => values.includes(value));
}

function hasTrueOutputGenerationAllowed(value) {
  if (!value || typeof value !== 'object') return false;
  if (Object.prototype.hasOwnProperty.call(value, 'output_generation_allowed')) {
    if (value.output_generation_allowed === true) return true;
  }
  return Object.values(value).some((child) => hasTrueOutputGenerationAllowed(child));
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

function sourceBeatFromId(beatId) {
  const match = beatId.match(/^(RE-\d+[A-Z]?)-(beginning|development|turn)$/);
  return {
    beat_id: beatId,
    segment_id: match ? match[1] : beatId,
    phase: match ? match[2] : 'unknown',
  };
}

function findForbiddenHits(candidate, primitive) {
  const scannedText = [
    candidate.beat_id,
    candidate.representation,
    candidate.proxy_type,
    primitive.primitive_id,
    primitive.primitive_family,
    primitive.description,
    ...(primitive.components || []),
  ]
    .filter(Boolean)
    .join('\n');

  return forbiddenRepresentationPatterns
    .map((entry) => {
      const match = scannedText.match(entry.pattern);
      return match
        ? {
            pattern_id: entry.id,
            matched_text: match[0],
          }
        : null;
    })
    .filter(Boolean);
}

const authorizationGate = readJson(paths.authorizationGate);
const routePreflight = readJson(paths.routePreflight);
const planningCandidates = readJson(paths.planningCandidates);
const gapReport = readJson(paths.gapReport);

function buildDryRun() {
  const candidateById = new Map(
    (routePreflight.route_planning_candidates || []).map((candidate) => [
      candidate.beat_id,
      candidate,
    ]),
  );

  const items = expectedCandidateIds.map((beatId) => {
    const candidate = candidateById.get(beatId);
    const primitive = primitiveByBeat[beatId];
    const hits = findForbiddenHits(candidate || { beat_id: beatId }, primitive);
    const readiness = hits.length ? 'blocked' : 'ready';

    return {
      source_beat: sourceBeatFromId(beatId),
      route_types: candidate?.route_types || [],
      primary_route_type: (candidate?.route_types || [])[0] || null,
      resolved_proxy_template_primitive: primitive,
      source_candidate: {
        representation: candidate?.representation || null,
        proxy_type: candidate?.proxy_type || null,
        rights_risk: candidate?.rights_risk || null,
        required_note: candidate?.required_note || null,
      },
      forbidden_representation_check: {
        status: hits.length ? 'fail' : 'pass',
        hits,
        checked_pattern_ids: forbiddenRepresentationPatterns.map((entry) => entry.id),
      },
      YMM4_patch_readiness: readiness,
      blocked_reason: hits.length
        ? `Forbidden representation hit: ${hits.map((hit) => hit.pattern_id).join(', ')}`
        : 'none',
      next_artifact_readiness: {
        compact_review_candidate: readiness === 'ready',
        patch_output_candidate_after_separate_authorization: readiness === 'ready',
        patch_output_generated: false,
        ymmp_generated: false,
      },
    };
  });

  const readyItems = items.filter((item) => item.YMM4_patch_readiness === 'ready');
  const blockedItems = items.filter((item) => item.YMM4_patch_readiness === 'blocked');
  const deferredExclusion = (routePreflight.exclusions || []).find(
    (item) => item.beat_id === 'RE-07D-turn',
  );
  const blockedExclusion = (routePreflight.exclusions || []).find(
    (item) => item.beat_id === 'RE-02-turn',
  );

  return {
    version: '1.0',
    artifact_type: 'YMM4_adapter_IR_dry_run',
    episode_id: 'real_estate_dx',
    scope: 'G-27 adapter IR dry-run data for 7 authorized route candidates',
    source: {
      authorization_gate: paths.authorizationGate,
      route_preflight: paths.routePreflight,
      adapter_planning_candidates: paths.planningCandidates,
      asset_proxy_gap_report: paths.gapReport,
      route_contract: paths.routeContract,
    },
    authorization: {
      source: 'user_prompt',
      response: authorizationValue,
      effect: 'Generate adapter IR dry-run data only for the 7 route candidates.',
    },
    boundary: {
      adapter_IR_dry_run_data_generated: true,
      YMM4_patch_generated: false,
      ymmp_generated: false,
      render_generated: false,
      preview_generated: false,
      production_timing_set: false,
      creative_acceptance_performed: false,
      output_generation_allowed: false,
      forbidden_actions: forbiddenActions,
    },
    items,
    excluded_items: [
      {
        source_beat: sourceBeatFromId('RE-02-turn'),
        status: 'blocked',
        YMM4_patch_readiness: 'blocked',
        blocked_reason:
          blockedExclusion?.reason ||
          'Accepted-with-adjustment proxy has not yet been reflected as a route-planning candidate.',
        required_condition:
          blockedExclusion?.required_condition ||
          'Use public information layer / non-public data bundle opacity contrast before adapter planning.',
      },
      {
        source_beat: sourceBeatFromId('RE-07D-turn'),
        status: 'deferred',
        YMM4_patch_readiness: 'deferred',
        blocked_reason:
          deferredExclusion?.reason ||
          'Specialist / cast / silhouette policy remains undecided.',
        required_condition:
          deferredExclusion?.required_condition ||
          'Choose abstract silhouettes, real/cast asset, cut/reframe, or keep deferred before adapter planning.',
      },
    ],
    rollup: {
      item_count: items.length,
      ready_for_compact_review_count: readyItems.length,
      ready_for_patch_output_candidate_count: readyItems.length,
      blocked_count: blockedItems.length + 1,
      deferred_count: 1,
      ready_candidate_ids: readyItems.map((item) => item.source_beat.beat_id),
      blocked_candidate_ids: blockedItems.map((item) => item.source_beat.beat_id),
      excluded_blocked_ids: ['RE-02-turn'],
      excluded_deferred_ids: ['RE-07D-turn'],
      next_possible_artifact: readyItems.length
        ? '.ymmp compact review candidate set or patch-output candidate review'
        : 'blocked before YMM4-facing artifact',
      patch_or_ymmp_generated: false,
    },
  };
}

function renderMarkdown(payload) {
  const lines = [];
  lines.push('# Real Estate DX Adapter IR Dry-Run');
  lines.push('');
  lines.push(`Authorization: \`${payload.authorization.response}\``);
  lines.push('');
  lines.push('This is adapter IR dry-run data only. It does not write a YMM4 patch, `.ymmp`, preview, render, production timing, or creative acceptance.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Dry-run candidates: \`${payload.rollup.item_count}\``);
  lines.push(
    `- Ready for next \`.ymmp compact review\`: \`${payload.rollup.ready_for_compact_review_count}\``,
  );
  lines.push(`- Patch-output candidates after separate authorization: \`${payload.rollup.ready_for_patch_output_candidate_count}\``);
  lines.push(`- Blocked: \`${payload.rollup.blocked_count}\` including \`RE-02-turn\``);
  lines.push(`- Deferred: \`${payload.rollup.deferred_count}\` including \`RE-07D-turn\``);
  lines.push('');
  lines.push('## Dry-Run Items');
  lines.push('');
  lines.push('| source beat | primary route | resolved primitive | forbidden check | YMM4 patch readiness | blocked reason |');
  lines.push('| --- | --- | --- | --- | --- | --- |');
  payload.items.forEach((item) => {
    lines.push(
      `| \`${item.source_beat.beat_id}\` | \`${item.primary_route_type}\` | ${markdownEscape(item.resolved_proxy_template_primitive.primitive_id)} | \`${item.forbidden_representation_check.status}\` | \`${item.YMM4_patch_readiness}\` | ${markdownEscape(item.blocked_reason)} |`,
    );
  });
  lines.push('');
  lines.push('## Excluded Items');
  lines.push('');
  lines.push('| source beat | status | YMM4 patch readiness | blocked reason |');
  lines.push('| --- | --- | --- | --- |');
  payload.excluded_items.forEach((item) => {
    lines.push(
      `| \`${item.source_beat.beat_id}\` | \`${item.status}\` | \`${item.YMM4_patch_readiness}\` | ${markdownEscape(item.blocked_reason)} |`,
    );
  });
  lines.push('');
  lines.push('## Next Distance');
  lines.push('');
  lines.push('- Adapter IR dry-run: complete for the 7 authorized candidates.');
  lines.push(
    `- \`.ymmp compact review\`: ${payload.rollup.ready_for_compact_review_count} candidates can proceed in the next slice.`,
  );
  lines.push(`- YMM4 patch output: ${payload.rollup.ready_for_patch_output_candidate_count} candidates are candidates after a separate output authorization; no patch was written here.`);
  lines.push('- YMM4 readback / preview: still pending on a future compact review or patch-output artifact.');
  lines.push('- Short rendered video: still blocked until YMM4 output, readback, preview, and creative acceptance exist.');
  return `${lines.join('\n')}\n`;
}

function validateDryRun(payload, renderedMarkdown = null) {
  const itemIds = (payload.items || []).map((item) => item.source_beat?.beat_id);
  const excludedIds = (payload.excluded_items || []).map((item) => item.source_beat?.beat_id);
  const gateCandidates = authorizationGate.next_if_authorized?.include_candidates || [];
  const preflightCandidates = (routePreflight.route_planning_candidates || []).map(
    (item) => item.beat_id,
  );
  const planningBoundaryCandidates =
    planningCandidates.planning_boundary?.include_in_adapter_planning || [];
  const allItemsReady = (payload.items || []).every(
    (item) =>
      item.forbidden_representation_check?.status === 'pass' &&
      item.YMM4_patch_readiness === 'ready' &&
      item.blocked_reason === 'none',
  );
  const rollup = payload.rollup || {};
  const markdownHasCounts =
    !renderedMarkdown ||
    (renderedMarkdown.includes(
      `Ready for next \`.ymmp compact review\`: \`${rollup.ready_for_compact_review_count}\``,
    ) &&
      renderedMarkdown.includes(
        `Patch-output candidates after separate authorization: \`${rollup.ready_for_patch_output_candidate_count}\``,
      ));

  const checks = [
    makeCheck('authorization_value', authorizationValue === payload.authorization?.response, {
      expected: authorizationValue,
      actual: payload.authorization?.response || null,
    }),
    makeCheck('source_candidates_match', sameSet(itemIds, expectedCandidateIds), {
      item_ids: itemIds,
      expected_candidate_ids: expectedCandidateIds,
    }),
    makeCheck(
      'upstream_candidates_match',
      sameSet(gateCandidates, expectedCandidateIds) &&
        sameSet(preflightCandidates, expectedCandidateIds) &&
        sameSet(planningBoundaryCandidates, expectedCandidateIds),
      {
        gate_candidates: gateCandidates,
        preflight_candidates: preflightCandidates,
        planning_boundary_candidates: planningBoundaryCandidates,
      },
    ),
    makeCheck('excluded_items_preserved', sameSet(excludedIds, expectedExcludedIds), {
      excluded_ids: excludedIds,
    }),
    makeCheck('no_forbidden_hits_in_items', allItemsReady, {
      failed_items: (payload.items || [])
        .filter((item) => item.YMM4_patch_readiness !== 'ready')
        .map((item) => item.source_beat?.beat_id),
    }),
    makeCheck(
      'boundary_preserved',
      payload.boundary?.adapter_IR_dry_run_data_generated === true &&
        payload.boundary?.YMM4_patch_generated === false &&
        payload.boundary?.ymmp_generated === false &&
        payload.boundary?.render_generated === false &&
        payload.boundary?.creative_acceptance_performed === false &&
        payload.boundary?.output_generation_allowed === false &&
        hasAll(payload.boundary?.forbidden_actions || [], forbiddenActions) &&
        !hasTrueOutputGenerationAllowed(payload),
      payload.boundary || {},
    ),
    makeCheck(
      'rollup_counts',
      rollup.item_count === 7 &&
        rollup.ready_for_compact_review_count === 7 &&
        rollup.ready_for_patch_output_candidate_count === 7 &&
        rollup.blocked_count === 1 &&
        rollup.deferred_count === 1 &&
        rollup.patch_or_ymmp_generated === false,
      rollup,
    ),
    makeCheck('markdown_counts', markdownHasCounts, {
      checked: Boolean(renderedMarkdown),
    }),
  ];

  const failed = checks.filter((check) => check.status !== 'pass');
  if (failed.length) {
    console.error(JSON.stringify({ status: 'failed', checks }, null, 2));
    process.exit(1);
  }
}

const payload = buildDryRun();
const markdown = renderMarkdown(payload);

if (writeOutputs) {
  fs.writeFileSync(path.join(root, paths.outputJson), `${JSON.stringify(payload, null, 2)}\n`);
  fs.writeFileSync(path.join(root, paths.outputMd), markdown);
  validateDryRun(payload, markdown);
} else {
  const existingJson = readJson(paths.outputJson);
  const existingMarkdown = readText(paths.outputMd);
  const expectedJson = `${JSON.stringify(payload, null, 2)}\n`;
  const expectedMarkdown = markdown;
  const matches =
    JSON.stringify(existingJson, null, 2) + '\n' === expectedJson &&
    existingMarkdown === expectedMarkdown;
  validateDryRun(existingJson, existingMarkdown);
  if (!matches) {
    console.error('Existing adapter IR dry-run artifacts differ from generated output. Run with --write.');
    process.exit(1);
  }
}

console.log('G-27 adapter IR dry-run OK: 7 ready candidates, 1 blocked exclusion, 1 deferred exclusion, no YMM4 output written');

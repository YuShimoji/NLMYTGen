const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeReport = process.argv.includes('--write');

const paths = {
  routeContract: 'docs/G27_ADAPTER_ROUTE_CONTRACT.md',
  candidates: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_planning_candidates.json',
  gapReport: 'samples/_probe/g24/real_estate_dx_asset_proxy_gap_report.json',
  validator: 'samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json',
  reportJson: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.md',
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

const forbiddenActions = [
  'YMM4 adapter output',
  'YMM4 patch',
  'render',
  'production timing',
  'creative acceptance',
];

const validatorForbiddenActions = [
  'cast_motion_ir',
  'ymm4_creative_acceptance',
  'production_timing',
];

const routeAssignments = {
  'RE-02-beginning': ['abstract_ui_route', 'motion_primitive_route'],
  'RE-02-development': ['abstract_ui_route', 'property_card_route', 'motion_primitive_route'],
  'RE-06-beginning': ['property_card_route', 'motion_primitive_route'],
  'RE-06-development': [
    'document_proxy_route',
    'property_card_route',
    'risk_marker_route',
    'motion_primitive_route',
  ],
  'RE-06-turn': ['document_proxy_route', 'property_card_route', 'motion_primitive_route'],
  'RE-07D-beginning': ['ai_panel_route', 'property_card_route', 'motion_primitive_route'],
  'RE-07D-development': ['risk_marker_route', 'motion_primitive_route'],
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

function evidenceLine(value) {
  if (Array.isArray(value)) return value.join(', ');
  if (typeof value === 'object' && value) return JSON.stringify(value);
  return String(value);
}

function makeCheck(id, description, passed, evidence, failureReason = null) {
  return {
    id,
    description,
    status: passed ? 'pass' : 'fail',
    evidence,
    failure_reason: passed ? null : failureReason || 'Condition failed',
  };
}

const routeContractText = readText(paths.routeContract);
const candidates = readJson(paths.candidates);
const gapReport = readJson(paths.gapReport);
const validator = readJson(paths.validator);

const candidateIds = (candidates.adapter_planning_ready_candidates || []).map((item) => item.beat_id);
const gapCandidateIds = gapReport.rollup?.adapter_planning_ready_items || [];
const candidateSetOk =
  candidateIds.length === 7 &&
  sameSet(candidateIds, expectedCandidateIds) &&
  sameSet(gapCandidateIds, expectedCandidateIds);

const adjustment = (candidates.adjustment_required_items || []).find(
  (item) => item.beat_id === 'RE-02-turn',
);
const gapRe02Turn = (gapReport.rows || []).find((item) => item.beat_id === 'RE-02-turn');
const re02TurnOk =
  !candidateIds.includes('RE-02-turn') &&
  adjustment?.adapter_planning_status === 'excluded_until_adjusted' &&
  /public information layer/i.test(adjustment?.proxy_type || '') &&
  /non-public data bundle opacity contrast/i.test(adjustment?.proxy_type || '') &&
  gapRe02Turn?.asset_proxy_readiness === 'needs adjustment' &&
  /not adapter-planning-ready/i.test(gapRe02Turn?.YMM4_adapter_readiness || '');

const deferred = (candidates.deferred_adapter_blocked_items || []).find(
  (item) => item.beat_id === 'RE-07D-turn',
);
const gapRe07DTurn = (gapReport.rows || []).find((item) => item.beat_id === 'RE-07D-turn');
const re07DTurnOk =
  !candidateIds.includes('RE-07D-turn') &&
  deferred?.asset_proxy_readiness === 'deferred' &&
  deferred?.YMM4_adapter_readiness === 'still blocked' &&
  deferred?.adapter_planning_status === 'deferred_blocks_adapter_planning' &&
  gapRe07DTurn?.asset_proxy_readiness === 'deferred' &&
  gapRe07DTurn?.YMM4_adapter_readiness === 'still blocked';

const validatorForbidden = validator.forbidden_next_actions || [];
const validatorOk =
  validator.status === 'blocked' &&
  hasAll(validatorForbidden, validatorForbiddenActions) &&
  (validator.allowed_next_actions || []).includes('overlay_only_compact_review');

const positiveRepresentationText = [
  ...(candidates.adapter_planning_ready_candidates || []).map((item) =>
    [item.beat_id, item.representation, item.proxy_type].join(' '),
  ),
  [adjustment?.beat_id, adjustment?.representation, adjustment?.proxy_type].join(' '),
].join('\n');

const forbiddenPositivePatterns = [
  /\breal\s+reins\b/i,
  /\breins\s+screenshot\b/i,
  /\bofficial\s+logo\b/i,
  /\breal\s+listing\s+photo\b/i,
  /\breal\s+map\b/i,
  /\bregistry\s+document\b/i,
  /\bidentifiable\s+(record|service|ui|brand)/i,
  /\blocked-room\b/i,
  /\bsecurity-facility\b/i,
  /\bconspiracy-coded\b/i,
];
const forbiddenPositiveHits = forbiddenPositivePatterns
  .map((pattern) => positiveRepresentationText.match(pattern)?.[0])
  .filter(Boolean);
const forbiddenRepresentationOk = forbiddenPositiveHits.length === 0;

const planningBoundary = candidates.planning_boundary || {};
const outputBoundaryOk =
  routeContractText.includes('output_generation_allowed=false') &&
  candidates.boundary?.no_YMM4_adapter_output === true &&
  candidates.boundary?.no_YMM4_patch === true &&
  hasAll(planningBoundary.forbidden_actions || [], forbiddenActions);

const checks = [
  makeCheck('candidate_set', 'All 7 candidates remain adapter-planning-ready in the gap report.', candidateSetOk, {
    candidate_count: candidateIds.length,
    candidate_ids: candidateIds,
    gap_rollup_ids: gapCandidateIds,
  }),
  makeCheck('re02_turn_excluded_until_adjusted', 'RE-02-turn remains excluded until opacity-layer adjustment is reflected.', re02TurnOk, {
    candidate_inclusion: candidateIds.includes('RE-02-turn'),
    candidate_status: adjustment?.adapter_planning_status || null,
    proxy_type: adjustment?.proxy_type || null,
    gap_readiness: gapRe02Turn?.YMM4_adapter_readiness || null,
  }),
  makeCheck('re07d_turn_deferred_blocks_planning', 'RE-07D-turn remains deferred and still blocks adapter planning.', re07DTurnOk, {
    candidate_inclusion: candidateIds.includes('RE-07D-turn'),
    candidate_status: deferred?.adapter_planning_status || null,
    asset_proxy_readiness: deferred?.asset_proxy_readiness || null,
    ymm4_adapter_readiness: deferred?.YMM4_adapter_readiness || null,
  }),
  makeCheck('validator_boundary', 'Validator authority still blocks execution-zone actions.', validatorOk, {
    status: validator.status,
    allowed_next_actions: validator.allowed_next_actions || [],
    forbidden_next_actions: validatorForbidden,
  }),
  makeCheck('no_forbidden_positive_representation', 'No forbidden positive representation appears in planning candidate proxy fields.', forbiddenRepresentationOk, {
    scanned_fields: ['beat_id', 'representation', 'proxy_type'],
    hits: forbiddenPositiveHits,
  }),
  makeCheck('output_generation_disabled', 'output_generation_allowed=false is preserved and forbidden actions remain listed.', outputBoundaryOk, {
    route_contract_flag_present: routeContractText.includes('output_generation_allowed=false'),
    no_YMM4_adapter_output: candidates.boundary?.no_YMM4_adapter_output === true,
    no_YMM4_patch: candidates.boundary?.no_YMM4_patch === true,
    forbidden_actions: planningBoundary.forbidden_actions || [],
  }),
];

const failedChecks = checks.filter((check) => check.status !== 'pass');
const report = {
  version: '1.0',
  artifact_type: 'YMM4_adapter_route_preflight_report',
  episode_id: 'real_estate_dx',
  scope: 'G-27 RE-02 / RE-06 / RE-07D route-contract preflight only',
  source: {
    route_contract: paths.routeContract,
    adapter_planning_candidates: paths.candidates,
    asset_proxy_gap_report: paths.gapReport,
    validator_authority: paths.validator,
  },
  boundary: {
    preflight_only: true,
    output_generation_allowed: false,
    no_YMM4_adapter_output: true,
    no_adapter_IR: true,
    no_YMM4_patch: true,
    no_ymmp_write: true,
    no_render: true,
    no_production_timing: true,
    no_creative_acceptance: true,
    no_external_asset_acquisition: true,
  },
  status: failedChecks.length ? 'failed' : 'passed_for_planning_preflight',
  checks,
  route_planning_candidates: expectedCandidateIds.map((beatId) => {
    const source = candidates.adapter_planning_ready_candidates.find((item) => item.beat_id === beatId);
    return {
      beat_id: beatId,
      status: 'route_planning_candidate',
      route_types: routeAssignments[beatId],
      representation: source?.representation || null,
      proxy_type: source?.proxy_type || null,
      rights_risk: source?.rights_risk || null,
      required_note: source?.required_note || null,
      output_generation_allowed: false,
    };
  }),
  exclusions: [
    {
      beat_id: 'RE-02-turn',
      status: 'excluded_until_adjusted',
      reason: 'Accepted-with-adjustment proxy has not yet been reflected as a route-planning candidate.',
      required_condition: 'Use public information layer / non-public data bundle opacity contrast; avoid wall/gate/security-facility/conspiracy-coded occlusion.',
      output_generation_allowed: false,
    },
    {
      beat_id: 'RE-07D-turn',
      status: 'deferred_blocks_adapter_planning',
      reason: 'Specialist / cast / silhouette policy remains undecided.',
      asset_proxy_readiness: 'deferred',
      YMM4_adapter_readiness: 'still blocked',
      output_generation_allowed: false,
    },
  ],
  next_gate: {
    recommended_default: 'user_or_validator_authorization_before_adapter_IR_or_patch_output',
    assistant_can_prepare: 'authorization decision sheet or validator-facing preflight review',
    user_or_validator_must_authorize_before: ['adapter IR', 'YMM4 patch output', '.ymmp write'],
  },
};

function markdownEscape(value) {
  return String(value).replace(/\|/g, '\\|').replace(/\r?\n/g, '<br>');
}

function renderMarkdown(payload) {
  const lines = [];
  lines.push('# Real Estate DX YMM4 Adapter Route Preflight Report');
  lines.push('');
  lines.push(`Source: \`${payload.source.route_contract}\``);
  lines.push('');
  lines.push('This is a route-contract preflight report only. `output_generation_allowed=false`.');
  lines.push('It does not create adapter IR, YMM4 adapter output, YMM4 patch files, `.ymmp` output, render output, production timing, or creative acceptance.');
  lines.push('');
  lines.push(`Status: \`${payload.status}\``);
  lines.push('');
  lines.push('## Checks');
  lines.push('');
  lines.push('| check | status | evidence |');
  lines.push('| --- | --- | --- |');
  payload.checks.forEach((check) => {
    lines.push(
      `| \`${check.id}\` | \`${check.status}\` | ${markdownEscape(evidenceLine(check.evidence))} |`,
    );
  });
  lines.push('');
  lines.push('## Route Planning Candidates');
  lines.push('');
  lines.push('| beat | route types | representation | rights risk |');
  lines.push('| --- | --- | --- | --- |');
  payload.route_planning_candidates.forEach((candidate) => {
    lines.push(
      `| \`${candidate.beat_id}\` | ${candidate.route_types.map((item) => `\`${item}\``).join(', ')} | ${candidate.representation} | ${candidate.rights_risk} |`,
    );
  });
  lines.push('');
  lines.push('## Exclusions');
  lines.push('');
  lines.push('| beat | status | reason |');
  lines.push('| --- | --- | --- |');
  payload.exclusions.forEach((item) => {
    lines.push(`| \`${item.beat_id}\` | \`${item.status}\` | ${markdownEscape(item.reason)} |`);
  });
  lines.push('');
  lines.push('## Next Gate');
  lines.push('');
  lines.push(`Recommended default: \`${payload.next_gate.recommended_default}\`.`);
  lines.push('');
  lines.push('The assistant may prepare an authorization decision sheet or validator-facing preflight review.');
  lines.push('Adapter IR, YMM4 patch output, and `.ymmp` writes remain forbidden until separately authorized.');
  return `${lines.join('\n')}\n`;
}

if (writeReport) {
  fs.writeFileSync(path.join(root, paths.reportJson), `${JSON.stringify(report, null, 2)}\n`);
  fs.writeFileSync(path.join(root, paths.reportMd), renderMarkdown(report));
}

if (failedChecks.length) {
  console.error(JSON.stringify(report, null, 2));
  process.exit(1);
}

console.log(`G-27 adapter route preflight OK: ${expectedCandidateIds.length} candidates, output_generation_allowed=false`);

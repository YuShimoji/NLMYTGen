const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeGate = process.argv.includes('--write');

const paths = {
  routeContract: 'docs/G27_ADAPTER_ROUTE_CONTRACT.md',
  routePreflight: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.json',
  candidates: 'samples/_probe/g24/real_estate_dx_ymm4_adapter_planning_candidates.json',
  gapReport: 'samples/_probe/g24/real_estate_dx_asset_proxy_gap_report.json',
  thinSceneDecisionPacket: 'samples/_probe/g24/real_estate_dx_thin_scene_decision_packet.json',
  validator: 'samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json',
  gateJson: 'samples/_probe/g24/real_estate_dx_adapter_authorization_gate.json',
  gateMd: 'samples/_probe/g24/real_estate_dx_adapter_authorization_gate.md',
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

const expectedExcludedIds = ['RE-02-turn', 'RE-07D-turn'];

const currentSliceForbiddenActions = [
  'YMM4 adapter output',
  'YMM4 patch',
  '.ymmp write',
  'render',
  'production timing',
  'creative acceptance',
];

const stillForbiddenAfterDryRunAuthorization = [
  'YMM4 adapter output',
  'YMM4 patch',
  '.ymmp write',
  'render',
  'production timing',
  'creative acceptance',
];

const validatorForbiddenActions = [
  'cast_motion_ir',
  'ymm4_creative_acceptance',
  'production_timing',
];

const expectedAuthorizationResponses = [
  'authorize_adapter_IR_dry_run_for_7_candidates_only',
  'hold_for_validator_review',
  'revise_route_candidates_before_authorization',
  'reject_adapter_IR_dry_run',
];

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

const routeContractText = readText(paths.routeContract);
const routePreflight = readJson(paths.routePreflight);
const candidates = readJson(paths.candidates);
const gapReport = readJson(paths.gapReport);
const thinSceneDecisionPacket = readJson(paths.thinSceneDecisionPacket);
const validator = readJson(paths.validator);

function buildGate() {
  const routeCandidates = (routePreflight.route_planning_candidates || []).map((candidate) => ({
    beat_id: candidate.beat_id,
    authorization_scope: 'adapter_IR_dry_run_candidate_only',
    route_types: candidate.route_types || [],
    representation: candidate.representation,
    proxy_type: candidate.proxy_type,
    rights_risk: candidate.rights_risk,
    required_note: candidate.required_note,
    output_generation_allowed: false,
  }));

  return {
    version: '1.0',
    artifact_type: 'YMM4_adapter_authorization_gate',
    episode_id: 'real_estate_dx',
    scope: 'G-27 RE-02 / RE-06 / RE-07D adapter authorization gate only',
    source: {
      route_contract: paths.routeContract,
      route_preflight: paths.routePreflight,
      adapter_planning_candidates: paths.candidates,
      asset_proxy_gap_report: paths.gapReport,
      thin_scene_decision_packet: paths.thinSceneDecisionPacket,
      validator_authority: paths.validator,
    },
    boundary: {
      authorization_gate_only: true,
      output_generation_allowed: false,
      adapter_IR_dry_run_allowed: true,
      adapter_IR_dry_run_scope: '7_candidates_only',
      no_YMM4_adapter_output: true,
      no_YMM4_patch: true,
      no_ymmp_write: true,
      no_render: true,
      no_production_timing: true,
      no_creative_acceptance: true,
      no_external_asset_acquisition: true,
      current_slice_forbidden_actions: currentSliceForbiddenActions,
    },
    status: 'authorized_adapter_IR_dry_run_for_7_candidates_only',
    source_state: {
      route_preflight_status: routePreflight.status,
      route_preflight_candidate_count: routeCandidates.length,
      thin_scene_decision_rollup: thinSceneDecisionPacket.rollup || {},
      asset_proxy_gap_report_rollup: gapReport.rollup || {},
      validator_status: validator.status,
    },
    route_planning_candidates: routeCandidates,
    exclusions: [
      {
        beat_id: 'RE-02-turn',
        status: 'excluded_until_adjusted',
        reason: 'Accepted-with-adjustment proxy has not yet been reflected as a route-planning candidate.',
        required_condition: 'Use public information layer / non-public data bundle opacity contrast; avoid wall/gate/locked-room/security-facility/conspiracy-coded occlusion.',
        output_generation_allowed: false,
      },
      {
        beat_id: 'RE-07D-turn',
        status: 'deferred_blocks_adapter_planning',
        reason: 'Specialist / cast / silhouette policy remains undecided.',
        required_condition: 'User or validator must choose abstract silhouettes, real/cast asset, cut/reframe, or keep deferred before this beat can enter adapter planning.',
        asset_proxy_readiness: 'deferred',
        YMM4_adapter_readiness: 'still blocked',
        output_generation_allowed: false,
      },
    ],
    validator_boundary: {
      status: validator.status,
      allowed_next_actions: validator.allowed_next_actions || [],
      forbidden_next_actions: validator.forbidden_next_actions || [],
      note: 'This authorization gate does not open validator-blocked cast motion IR, creative acceptance, or production timing.',
    },
    authorization_request: {
      authorization_granted: true,
      selected_response: 'authorize_adapter_IR_dry_run_for_7_candidates_only',
      selected_response_source: 'user_chat_2026-05-25_recommended_action',
      selected_exclusion_policy: {
        'RE-02-turn': 'keep_excluded_until_adjusted',
        'RE-07D-turn': 'keep_deferred_blocks_adapter_planning',
      },
      requested_next_slice: 'adapter_IR_dry_run_contract_for_7_candidates_only',
      response_owner: 'user_or_validator',
      recommended_response: 'authorize_adapter_IR_dry_run_for_7_candidates_only',
      allowed_responses: [
        {
          value: 'authorize_adapter_IR_dry_run_for_7_candidates_only',
          effect: 'Next slice may define and generate adapter IR dry-run artifacts for the 7 route candidates only. YMM4 patch, .ymmp write, render, production timing, and creative acceptance remain forbidden.',
        },
        {
          value: 'hold_for_validator_review',
          effect: 'No downstream dry-run starts. Assistant may prepare a validator-facing review of this gate and the route preflight.',
        },
        {
          value: 'revise_route_candidates_before_authorization',
          effect: 'Return to scene decision, asset/proxy gap report, or route planning candidate correction before any adapter IR dry-run work.',
        },
        {
          value: 'reject_adapter_IR_dry_run',
          effect: 'Close the current adapter route without proceeding to execution-zone dry-run work.',
        },
      ],
      short_return_format: [
        'G-27 adapter authorization: authorize_adapter_IR_dry_run_for_7_candidates_only',
        'RE-02-turn: keep excluded_until_adjusted',
        'RE-07D-turn: keep deferred_blocks_adapter_planning',
      ],
    },
    next_if_authorized: {
      next_slice: 'adapter_IR_dry_run_contract',
      include_candidates: expectedCandidateIds,
      excluded_from_first_dry_run: expectedExcludedIds,
      still_forbidden: stillForbiddenAfterDryRunAuthorization,
      adapter_IR_dry_run_only: true,
      YMM4_output_allowed: false,
    },
    next_if_not_authorized: {
      hold_for: 'user_or_validator_authorization',
      assistant_safe_followups: [
        'prepare validator-facing review',
        'tighten checker coverage',
        'sync runtime-state only',
      ],
    },
  };
}

function renderMarkdown(payload) {
  const lines = [];
  lines.push('# Real Estate DX Adapter Authorization Gate');
  lines.push('');
  lines.push(`Source preflight: \`${payload.source.route_preflight}\``);
  lines.push('');
  lines.push(`Status: \`${payload.status}\``);
  lines.push('');
  lines.push('Selected response: `authorize_adapter_IR_dry_run_for_7_candidates_only`.');
  lines.push('');
  lines.push('This gate authorizes only adapter IR dry-run planning for the 7 listed candidates. `output_generation_allowed=false` remains in force for YMM4-facing output.');
  lines.push('It does not create YMM4 adapter output, YMM4 patch files, `.ymmp` output, render output, production timing, or creative acceptance.');
  lines.push('');
  lines.push('## Candidate Scope');
  lines.push('');
  lines.push('| beat | route types | representation | rights risk |');
  lines.push('| --- | --- | --- | --- |');
  payload.route_planning_candidates.forEach((candidate) => {
    lines.push(
      `| \`${candidate.beat_id}\` | ${candidate.route_types.map((item) => `\`${item}\``).join(', ')} | ${markdownEscape(candidate.representation)} | ${markdownEscape(candidate.rights_risk)} |`,
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
  lines.push('## Authorization Choices');
  lines.push('');
  lines.push(`Recommended response: \`${payload.authorization_request.recommended_response}\`.`);
  lines.push('');
  lines.push('| response | effect |');
  lines.push('| --- | --- |');
  payload.authorization_request.allowed_responses.forEach((item) => {
    lines.push(`| \`${item.value}\` | ${markdownEscape(item.effect)} |`);
  });
  lines.push('');
  lines.push('## Short Return Format');
  lines.push('');
  lines.push('```text');
  payload.authorization_request.short_return_format.forEach((line) => lines.push(line));
  lines.push('```');
  lines.push('');
  lines.push('## Selected Response');
  lines.push('');
  lines.push(`- authorization_granted: \`${payload.authorization_request.authorization_granted}\``);
  lines.push(`- selected_response: \`${payload.authorization_request.selected_response}\``);
  lines.push('- `RE-02-turn`: keep excluded until adjusted.');
  lines.push('- `RE-07D-turn`: keep deferred / adapter-planning blocked.');
  lines.push('');
  lines.push('## Downstream Boundary');
  lines.push('');
  lines.push('If authorized, the next slice is `adapter_IR_dry_run_contract` for the 7 listed candidates only.');
  lines.push('`RE-02-turn` stays excluded until adjusted, and `RE-07D-turn` stays deferred until its specialist / cast / silhouette policy is decided.');
  lines.push('YMM4 patch output, `.ymmp` writes, render, production timing, and creative acceptance remain forbidden even after dry-run authorization.');
  return `${lines.join('\n')}\n`;
}

const builtGate = buildGate();
if (writeGate) {
  fs.writeFileSync(path.join(root, paths.gateJson), `${JSON.stringify(builtGate, null, 2)}\n`);
  fs.writeFileSync(path.join(root, paths.gateMd), renderMarkdown(builtGate));
}

const gate = writeGate ? builtGate : readJson(paths.gateJson);
const gateCandidateIds = (gate.route_planning_candidates || []).map((item) => item.beat_id);
const preflightCandidateIds = (routePreflight.route_planning_candidates || []).map((item) => item.beat_id);
const planningBoundary = candidates.planning_boundary || {};
const gateExcludedIds = (gate.exclusions || []).map((item) => item.beat_id);
const authorizationResponses = (gate.authorization_request?.allowed_responses || []).map(
  (item) => item.value,
);

const sourceOk =
  gate.source?.route_contract === paths.routeContract &&
  gate.source?.route_preflight === paths.routePreflight &&
  gate.source?.adapter_planning_candidates === paths.candidates &&
  gate.source?.asset_proxy_gap_report === paths.gapReport &&
  gate.source?.thin_scene_decision_packet === paths.thinSceneDecisionPacket &&
  gate.source?.validator_authority === paths.validator;

const routePreflightOk =
  routePreflight.status === 'passed_for_planning_preflight' &&
  (routePreflight.checks || []).every((check) => check.status === 'pass');

const candidateScopeOk =
  sameSet(gateCandidateIds, expectedCandidateIds) &&
  sameSet(preflightCandidateIds, expectedCandidateIds) &&
  sameSet(planningBoundary.include_in_adapter_planning || [], expectedCandidateIds) &&
  (gate.route_planning_candidates || []).every(
    (item) =>
      item.authorization_scope === 'adapter_IR_dry_run_candidate_only' &&
      item.output_generation_allowed === false,
  );

const re02Exclusion = (gate.exclusions || []).find((item) => item.beat_id === 'RE-02-turn');
const re07DExclusion = (gate.exclusions || []).find((item) => item.beat_id === 'RE-07D-turn');
const exclusionsOk =
  sameSet(gateExcludedIds, expectedExcludedIds) &&
  re02Exclusion?.status === 'excluded_until_adjusted' &&
  /public information layer/i.test(re02Exclusion?.required_condition || '') &&
  re07DExclusion?.status === 'deferred_blocks_adapter_planning' &&
  re07DExclusion?.asset_proxy_readiness === 'deferred' &&
  re07DExclusion?.YMM4_adapter_readiness === 'still blocked' &&
  !gateCandidateIds.includes('RE-02-turn') &&
  !gateCandidateIds.includes('RE-07D-turn');

const boundaryOk =
  gate.boundary?.authorization_gate_only === true &&
  gate.boundary?.output_generation_allowed === false &&
  gate.boundary?.adapter_IR_dry_run_allowed === true &&
  gate.boundary?.adapter_IR_dry_run_scope === '7_candidates_only' &&
  gate.boundary?.no_YMM4_adapter_output === true &&
  gate.boundary?.no_YMM4_patch === true &&
  gate.boundary?.no_ymmp_write === true &&
  gate.boundary?.no_render === true &&
  gate.boundary?.no_production_timing === true &&
  gate.boundary?.no_creative_acceptance === true &&
  hasAll(gate.boundary?.current_slice_forbidden_actions || [], currentSliceForbiddenActions) &&
  !hasTrueOutputGenerationAllowed(gate);

const validatorOk =
  gate.validator_boundary?.status === 'blocked' &&
  validator.status === 'blocked' &&
  hasAll(gate.validator_boundary?.forbidden_next_actions || [], validatorForbiddenActions) &&
  (gate.validator_boundary?.allowed_next_actions || []).includes('overlay_only_compact_review');

const authorizationOk =
  gate.status === 'authorized_adapter_IR_dry_run_for_7_candidates_only' &&
  gate.authorization_request?.authorization_granted === true &&
  gate.authorization_request?.selected_response ===
    'authorize_adapter_IR_dry_run_for_7_candidates_only' &&
  gate.authorization_request?.selected_response_source ===
    'user_chat_2026-05-25_recommended_action' &&
  gate.authorization_request?.selected_exclusion_policy?.['RE-02-turn'] ===
    'keep_excluded_until_adjusted' &&
  gate.authorization_request?.selected_exclusion_policy?.['RE-07D-turn'] ===
    'keep_deferred_blocks_adapter_planning' &&
  gate.authorization_request?.requested_next_slice ===
    'adapter_IR_dry_run_contract_for_7_candidates_only' &&
  gate.authorization_request?.recommended_response ===
    'authorize_adapter_IR_dry_run_for_7_candidates_only' &&
  sameSet(authorizationResponses, expectedAuthorizationResponses) &&
  sameSet(gate.next_if_authorized?.include_candidates || [], expectedCandidateIds) &&
  sameSet(gate.next_if_authorized?.excluded_from_first_dry_run || [], expectedExcludedIds) &&
  gate.next_if_authorized?.adapter_IR_dry_run_only === true &&
  gate.next_if_authorized?.YMM4_output_allowed === false &&
  hasAll(gate.next_if_authorized?.still_forbidden || [], stillForbiddenAfterDryRunAuthorization);

const routeContractOk =
  routeContractText.includes('output_generation_allowed=false') &&
  routeContractText.includes('real_estate_dx_adapter_authorization_gate') &&
  routeContractText.includes('check_g27_adapter_authorization_gate');

const checks = [
  makeCheck('source_links', 'Gate points to the expected preflight, route contract, decision, gap, and validator artifacts.', sourceOk, gate.source || {}),
  makeCheck('route_preflight_passed', 'Route preflight is still passed and all preflight checks pass.', routePreflightOk, {
    status: routePreflight.status,
    failed_preflight_checks: (routePreflight.checks || [])
      .filter((check) => check.status !== 'pass')
      .map((check) => check.id),
  }),
  makeCheck('candidate_scope', 'Gate includes exactly the 7 route-planning candidates and no excluded beats.', candidateScopeOk, {
    gate_candidate_ids: gateCandidateIds,
    preflight_candidate_ids: preflightCandidateIds,
    planning_boundary_ids: planningBoundary.include_in_adapter_planning || [],
  }),
  makeCheck('exclusions_preserved', 'RE-02-turn stays excluded until adjusted and RE-07D-turn stays deferred.', exclusionsOk, {
    exclusions: gate.exclusions || [],
  }),
  makeCheck('output_generation_disabled', 'Gate keeps output_generation_allowed=false and current slice output actions forbidden.', boundaryOk, {
    boundary: gate.boundary || {},
  }),
  makeCheck('validator_boundary', 'Validator boundary remains blocked for execution-zone actions.', validatorOk, {
    gate_validator_boundary: gate.validator_boundary || {},
    validator_status: validator.status,
  }),
  makeCheck('authorization_choices', 'Gate records the selected recommended response and preserves the dry-run-only boundary.', authorizationOk, {
    status: gate.status,
    authorization_request: gate.authorization_request || {},
    next_if_authorized: gate.next_if_authorized || {},
  }),
  makeCheck('route_contract_linked', 'Route contract names the authorization gate and checker.', routeContractOk, {
    route_contract: paths.routeContract,
  }),
];

const failedChecks = checks.filter((check) => check.status !== 'pass');

if (failedChecks.length) {
  console.error(JSON.stringify({ status: 'failed', checks }, null, 2));
  process.exit(1);
}

console.log(`G-27 adapter authorization gate OK: ${expectedCandidateIds.length} candidates, output_generation_allowed=false, authorization_granted=true`);

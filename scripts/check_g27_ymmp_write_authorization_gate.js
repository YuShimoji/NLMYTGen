const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

const paths = {
  dryRun: 'samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json',
  compactReview: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json',
  gateJson: 'samples/_probe/g24/real_estate_dx_ymmp_write_authorization_gate.json',
  gateMd: 'samples/_probe/g24/real_estate_dx_ymmp_write_authorization_gate.md',
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

const requiredForbiddenActions = [
  'YMM4 adapter output',
  'YMM4 patch',
  '.ymmp write',
  'render',
  'preview capture',
  'production timing',
  'creative acceptance',
];

const requiredFalseBoundaryFlags = [
  'output_generation_allowed',
  'YMM4_adapter_output_allowed',
  'YMM4_patch_allowed',
  'ymmp_write_allowed',
  'render_allowed',
  'preview_capture_allowed',
  'production_timing_allowed',
  'creative_acceptance_allowed',
  'external_asset_acquisition_allowed',
  'compact_review_reference_regenerated',
  'minimal_probe_reference_promoted',
  'actual_ymmp_write_executed',
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

function includesAll(values, expected) {
  return expected.every((value) => values.includes(value));
}

function hasTrueForKeys(value, keys) {
  if (!value || typeof value !== 'object') return false;
  if (!Array.isArray(value)) {
    for (const key of keys) {
      if (Object.prototype.hasOwnProperty.call(value, key) && value[key] === true) {
        return true;
      }
    }
  }
  return Object.values(value).some((child) => hasTrueForKeys(child, keys));
}

const dryRun = readJson(paths.dryRun);
const compactReview = readJson(paths.compactReview);
const gate = readJson(paths.gateJson);
const gateMd = readText(paths.gateMd);

const failures = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

const dryRunReadyIds = dryRun.rollup?.ready_candidate_ids || [];
const compactCandidateIds = (compactReview.candidates || []).map((candidate) => candidate.candidate_id);
const gateCandidateIds = gate.candidate_scope?.candidate_ids || [];
const gateCandidateRows = gate.candidate_scope?.candidates || [];
const gateCandidateRowIds = gateCandidateRows.map((candidate) => candidate.candidate_id);
const gateExcludedIds = (gate.exclusions || []).map((exclusion) => exclusion.candidate_id);

check(gate.artifact_type === 'YMM4_ymmp_write_authorization_gate', 'artifact_type must be YMM4_ymmp_write_authorization_gate');
check(gate.status === 'authorized_minimal_patched_ymmp_for_readback_only', 'status must be authorized_minimal_patched_ymmp_for_readback_only');
check(sameSet(dryRunReadyIds, expectedCandidateIds), 'dry-run ready candidates must remain the expected 7');
check(sameSet(compactCandidateIds, expectedCandidateIds), 'compact review candidates must remain the expected 7');
check(sameSet(gateCandidateIds, expectedCandidateIds), 'write gate candidate ids must match the expected 7');
check(sameSet(gateCandidateRowIds, expectedCandidateIds), 'write gate candidate rows must match the expected 7');
check(gate.candidate_scope?.candidate_count === expectedCandidateIds.length, 'candidate_count must be 7');
check(sameSet(gateExcludedIds, expectedExcludedIds), 'write gate exclusions must be RE-02-turn and RE-07D-turn');

const candidateIdSet = new Set(gateCandidateIds);
expectedExcludedIds.forEach((excludedId) => {
  check(!candidateIdSet.has(excludedId), `${excludedId} must not be in candidate scope`);
});

const exclusionById = Object.fromEntries((gate.exclusions || []).map((exclusion) => [exclusion.candidate_id, exclusion]));
check(exclusionById['RE-02-turn']?.status === 'blocked', 'RE-02-turn must remain blocked');
check(exclusionById['RE-02-turn']?.mixing_allowed === false, 'RE-02-turn mixing_allowed must be false');
check(exclusionById['RE-07D-turn']?.status === 'deferred', 'RE-07D-turn must remain deferred');
check(exclusionById['RE-07D-turn']?.mixing_allowed === false, 'RE-07D-turn mixing_allowed must be false');

gateCandidateRows.forEach((candidate) => {
  check(
    candidate.write_authorization_readiness === 'candidate_for_next_gate_only',
    `${candidate.candidate_id} must remain candidate_for_next_gate_only`,
  );
  check(
    candidate.intended_review_surface === 'minimal patched .ymmp readback only',
    `${candidate.candidate_id} must target readback-only review surface`,
  );
  check(candidate.duration_frames === 360, `${candidate.candidate_id} duration_frames must remain 360`);
});

check(gate.boundary?.authorization_gate_only === true, 'boundary.authorization_gate_only must be true');
check(gate.boundary?.reference_evidence_only === true, 'boundary.reference_evidence_only must be true');
requiredFalseBoundaryFlags.forEach((flag) => {
  check(gate.boundary?.[flag] === false, `boundary.${flag} must be false`);
});
check(
  includesAll(gate.boundary?.current_slice_forbidden_actions || [], requiredForbiddenActions),
  'current_slice_forbidden_actions must list all required forbidden actions',
);
check(
  !hasTrueForKeys(gate, requiredFalseBoundaryFlags),
  'no required false boundary flag may be true anywhere in the gate',
);

check(gate.authorization_request?.authorization_granted === true, 'authorization_granted must be true');
check(gate.authorization_request?.response_selected === true, 'response_selected must be true');
check(
  gate.authorization_request?.selected_response === 'authorize_minimal_patched_ymmp_for_readback_only',
  'selected_response must be authorize_minimal_patched_ymmp_for_readback_only',
);
check(
  gate.authorization_request?.selected_response_source === 'user_chat_recommended_action',
  'selected_response_source must be user_chat_recommended_action',
);
check(
  gate.authorization_request?.recommended_response === 'authorize_minimal_patched_ymmp_for_readback_only',
  'recommended_response must be authorize_minimal_patched_ymmp_for_readback_only',
);

const allowedResponses = (gate.authorization_request?.allowed_responses || []).map((response) => response.value);
check(
  includesAll(allowedResponses, [
    'authorize_minimal_patched_ymmp_for_readback_only',
    'hold_for_write_gate_review',
    'revise_candidate_scope_before_write_gate',
    'reject_minimal_patched_ymmp_write',
  ]),
  'allowed responses must include all write gate choices',
);

check(sameSet(gate.next_if_authorized?.include_candidates || [], expectedCandidateIds), 'next_if_authorized include candidates must match the expected 7');
check(sameSet(gate.next_if_authorized?.excluded_from_write || [], expectedExcludedIds), 'next_if_authorized exclusions must match the expected 2');
check(gate.next_if_authorized?.next_slice === 'minimal_patched_ymmp_readback_only', 'next_if_authorized.next_slice must be minimal_patched_ymmp_readback_only');
check(
  gate.next_if_authorized?.authorization_scope === 'readback_only_write_in_later_slice',
  'next_if_authorized.authorization_scope must be readback_only_write_in_later_slice',
);
check(gate.next_if_authorized?.readback_required === true, 'next_if_authorized must require readback');
check(
  includesAll(gate.next_if_authorized?.still_forbidden || [], [
    'render',
    'preview capture',
    'production timing',
    'creative acceptance',
  ]),
  'next_if_authorized must keep render/timing/acceptance forbidden',
);

[
  'authorize_minimal_patched_ymmp_for_readback_only',
  'authorization_granted: `true`',
  'output_generation_allowed: `false`',
  'ymmp_write_allowed: `false`',
  'actual_ymmp_write_executed: `false`',
  'RE-02-turn',
  'RE-07D-turn',
].forEach((requiredText) => {
  check(gateMd.includes(requiredText), `markdown must include ${requiredText}`);
});

if (failures.length > 0) {
  console.error('G-27 .ymmp write authorization gate failed:');
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log('G-27 .ymmp write authorization gate OK: readback-only authorization selected, actual .ymmp write not executed');

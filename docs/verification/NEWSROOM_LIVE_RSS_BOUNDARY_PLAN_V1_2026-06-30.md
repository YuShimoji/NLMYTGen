# Newsroom Live RSS Boundary Plan V1

## Identity

```json
{
  "plan_id": "newsroom_live_rss_boundary_plan_v1_2026_06_30",
  "contract_id": "newsroom_live_rss_boundary_contract_v1_2026_06_30",
  "source_adversarial_suite_path": "samples/_probe/newsroom_handoff/source_boundary_adversarial_fixtures_v1.json",
  "source_validator_path": "samples/_probe/newsroom_handoff/source_boundary_adversarial_fixture_validation_v1.json",
  "source_capsule_hardening_path": "samples/_probe/newsroom_handoff/source_boundary_adversarial_capsule_hardening_v1.json",
  "live_fetch_used": false,
  "render_gate": "L0_no_render",
  "production_status": "planning_only"
}
```


## State Machine

```json
{
  "allowed_states": [
    "offline_fixture_only",
    "offline_fixture_validated",
    "adversarial_validation_passed",
    "live_boundary_planned",
    "live_fetch_authorized_for_diagnostic_smoke",
    "live_fetch_result_captured",
    "live_source_boundary_validated",
    "diagnostic_capsule_ready",
    "production_script_blocked",
    "production_ready_requires_separate_approval"
  ],
  "current_state": "live_boundary_planned",
  "state_status": [
    {
      "state": "offline_fixture_only",
      "reached_in_this_slice": true,
      "allowed_to_set_now": true
    },
    {
      "state": "offline_fixture_validated",
      "reached_in_this_slice": true,
      "allowed_to_set_now": true
    },
    {
      "state": "adversarial_validation_passed",
      "reached_in_this_slice": true,
      "allowed_to_set_now": true
    },
    {
      "state": "live_boundary_planned",
      "reached_in_this_slice": true,
      "allowed_to_set_now": true
    },
    {
      "state": "live_fetch_authorized_for_diagnostic_smoke",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    },
    {
      "state": "live_fetch_result_captured",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    },
    {
      "state": "live_source_boundary_validated",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    },
    {
      "state": "diagnostic_capsule_ready",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    },
    {
      "state": "production_script_blocked",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    },
    {
      "state": "production_ready_requires_separate_approval",
      "reached_in_this_slice": false,
      "allowed_to_set_now": false
    }
  ],
  "forbidden_transitions": [
    {
      "from_state": "live_boundary_planned",
      "to_state": "live_fetch_result_captured",
      "reason": "fetch authorization and receipt contract must exist first"
    },
    {
      "from_state": "adversarial_validation_passed",
      "to_state": "diagnostic_capsule_ready",
      "reason": "a live source boundary validation must be captured first"
    },
    {
      "from_state": "live_boundary_planned",
      "to_state": "production_ready_requires_separate_approval",
      "reason": "production readiness is a separate future approval gate"
    },
    {
      "from_state": "any_state",
      "to_state": "publication_or_public_upload",
      "reason": "publication gate is closed in the current project state"
    }
  ],
  "next_allowed_transition": {
    "from_state": "live_boundary_planned",
    "to_state": "live_fetch_authorized_for_diagnostic_smoke",
    "allowed_now": false,
    "requirements": [
      "explicit future operator authorization",
      "named feed/source target",
      "expected local output directory",
      "fetch receipt schema accepted",
      "no production or publication claim"
    ]
  },
  "transition_requirements": {
    "live_fetch_authorized_for_diagnostic_smoke": [
      "LIVE_FETCH_GATE passes",
      "authorization is recorded in operator_action_log"
    ],
    "live_fetch_result_captured": [
      "fetch_receipt exists",
      "raw_entry_snapshot exists",
      "all live-source artifacts are local/ignored"
    ],
    "live_source_boundary_validated": [
      "SOURCE_BOUNDARY_GATE passes",
      "rights/freshness/attribution/source reliability are classified"
    ],
    "diagnostic_capsule_ready": [
      "CAPSULE_GENERATION_GATE passes",
      "production blockers remain attached to every downstream beat"
    ]
  }
}
```


## Future Live RSS Artifacts

| artifact_name | owner | can_contain_live_source_data | can_be_committed | must_remain_local_ignored |
| --- | --- | --- | --- | --- |
| fetch_receipt | agent after future operator authorization | True | False | True |
| feed_source_manifest | operator/user with agent schema validation | True | False | True |
| raw_entry_snapshot | agent after future authorization | True | False | True |
| normalized_topic_candidate | agent | True | False | True |
| source_boundary_validation | agent classification plus operator review when requested | True | False | True |
| rights_attribution_freshness_readback | operator/user for approval; agent for structured readback | True | False | True |
| excluded_claims_readback | agent | True | False | True |
| capsule_input_candidate | agent | True | False | True |
| operator_action_log | operator/user | True | False | True |


## Normalized Topic Schema

| field_name | diagnostic_capsule_required | live_boundary_plan_required | production_script_candidate_required |
| --- | --- | --- | --- |
| topic_id | True | True | True |
| feed_id | True | True | True |
| feed_title | True | True | True |
| entry_title | True | True | True |
| entry_url | True | True | True |
| entry_published_at | True | True | True |
| entry_summary | True | True | True |
| source_name | True | True | True |
| source_url | True | True | True |
| retrieved_at | True | True | True |
| fetch_receipt_id | True | True | True |
| rights_status | True | True | True |
| attribution_note | True | True | True |
| freshness_status | True | True | True |
| source_reliability_note | True | True | True |
| key_claim_candidates | True | False | True |
| excluded_claims | True | True | True |
| uncertainty_or_boundary | True | True | True |
| intended_episode_angle | True | False | True |
| production_status | True | True | True |


## Gate Definitions

```json
{
  "LIVE_FETCH_GATE": {
    "status_now": "closed",
    "requires": [
      "explicit future authorization",
      "feed/source target selected by operator",
      "expected local ignored output directory",
      "fetch_receipt schema accepted",
      "no production claim"
    ],
    "allows": [
      "future diagnostic smoke only"
    ],
    "blocks": [
      "live fetch implementation now",
      "production use",
      "publication"
    ]
  },
  "SOURCE_BOUNDARY_GATE": {
    "status_now": "planned_not_executed",
    "requires": [
      "rights_status classification",
      "freshness_status classification",
      "attribution_note",
      "source_reliability_note",
      "excluded_claims",
      "source URL",
      "published timestamp"
    ],
    "blocks": [
      "production if placeholders remain",
      "production if rights/freshness/source reliability are unknown"
    ]
  },
  "CAPSULE_GENERATION_GATE": {
    "status_now": "planned_not_executed",
    "requires": [
      "source_boundary_validation",
      "rights_attribution_freshness_readback",
      "excluded_claims_readback",
      "capsule_input_candidate"
    ],
    "allows": [
      "diagnostic capsule with blockers attached"
    ],
    "blocks": [
      "production capsule when any production blocker remains"
    ]
  },
  "PUBLICATION_GATE": {
    "status_now": "closed",
    "requires": [
      "separate future approval far beyond this plan"
    ],
    "allows": [],
    "blocks": [
      "public upload",
      "public readiness claim",
      "audience/order acceptance claim"
    ]
  }
}
```


## Responsibility Split

```json
{
  "agent_owned": [
    "schema definition",
    "validation logic",
    "offline and adversarial tests",
    "readback generation",
    "blocker classification",
    "no-network planning"
  ],
  "operator_user_owned": [
    "explicit authorization for any future live fetch",
    "confirming fetch target/feed if needed",
    "reviewing source/rights/freshness boundary when asked",
    "deciding whether live source usage is acceptable"
  ],
  "forbidden_for_agent_without_explicit_future_authorization": [
    "network fetch",
    "real RSS retrieval",
    "article scraping",
    "rights approval",
    "production/public readiness claims"
  ]
}
```


## Risk Register

| risk_id | risk | blocker | mitigation | required_follow_up |
| --- | --- | --- | --- | --- |
| R1 | live fetch network risk | no network action without LIVE_FETCH_GATE | keep this slice planning-only | future explicit authorization |
| R2 | source truth risk | source truth is not approved by fetch existence | require source_boundary_validation | operator review if source is ambiguous |
| R3 | rights and reuse risk | unknown rights block production | require rights_status and quote/media permission readback | human rights decision |
| R4 | quote/media permission risk | quoted or media material cannot be reused by default | separate quote_media_permission_status | operator decision before production |
| R5 | freshness/datedness risk | stale or missing timestamps block live boundary validation | require entry_published_at and retrieved_at | freshness policy in preflight |
| R6 | hallucinated claim risk | candidate claims are not approved assertions | keep key_claim_candidates separate from approved claims | claim validation before capsule |
| R7 | excluded-claim leakage risk | leak blocks diagnostic capsule readiness | carry excluded_claims_readback into capsule gate | repeat adversarial leak check |
| R8 | source URL and timestamp absence | missing URL/timestamp blocks normalization | require raw_entry_snapshot fields | preflight schema enforcement |
| R9 | attribution ambiguity | ambiguous attribution blocks production | require attribution_note | operator attribution review |
| R10 | production/public overclaiming risk | publication gate remains closed | production_status remains planning_only or blocked | separate future approval |


## Decision Readback

```json
{
  "live_fetch_implementation_allowed_now": false,
  "live_boundary_plan_ready": true,
  "next_recommended_axis": "newsroom-live-rss-preflight-contract-v1",
  "next_axis_reason": "the boundary plan is clear; next step is a stricter preflight contract, not live fetch"
}
```


## Business Goal Outcome Contract
- problem_clear: True - The plan prevents jumping from offline fixtures directly to live fetch.
- offer_clear: True - Future live RSS introduction is governed by states, artifacts, gates, and owners.
- proof_clear: True - This defines boundary planning only, not implementation.
- boundary_clear: True - Source, rights, freshness, attribution, production, and publication claims remain blocked.
- next_action_clear: True - newsroom-live-rss-preflight-contract-v1
- visual_supports_explanation: True - YMM4 visual proof stays closed.

## Boundaries

```json
{
  "network_fetch_performed": false,
  "live_RSS_news_fetch_performed": false,
  "live_feed_source_added": false,
  "fetch_adapter_implemented": false,
  "article_scraping_performed": false,
  "YMM4_launched_by_agent": false,
  "render_performed_by_agent": false,
  "audio_tts_generated": false,
  "real_media_imported": false,
  "external_fetch_performed": false,
  "card_assets_modified": false,
  "card_redesign_performed": false,
  "animation_tuned": false,
  "local_ignored_ymmp_created_in_this_slice": false,
  "local_ignored_ymmp_modified_in_this_slice": false,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false,
  "actual_order_or_audience_acceptance_claimed": false
}
```

# Newsroom Live RSS Preflight Contract V1

## Identity

```json
{
  "preflight_contract_id": "newsroom_live_rss_preflight_contract_v1_2026_06_30",
  "preflight_packet_template_id": "newsroom_live_rss_preflight_packet_template_v1_2026_06_30",
  "source_boundary_plan_path": "samples/_probe/newsroom_handoff/live_rss_boundary_plan_v1.json",
  "source_boundary_contract_path": "samples/_probe/newsroom_handoff/live_rss_boundary_contract_v1.json",
  "live_fetch_used": false,
  "render_gate": "L0_no_render",
  "production_status": "preflight_contract_only"
}
```


## Preflight Packet Schema

| field_name | required | current_default_value | blocker_behavior |
| --- | --- | --- | --- |
| preflight_id | True | placeholder:future_preflight_id | required for future packet completeness |
| requested_by | True | not_requested | required for future packet completeness |
| authorization_status | True | not_requested | blocks any fetch unless authorized_for_diagnostic_fetch_once in a future slice |
| authorization_scope | True | none | required for future packet completeness |
| feed_id | True | placeholder:future_feed_id_not_set | required for future packet completeness |
| feed_title | True | placeholder:future_feed_title_not_set | required for future packet completeness |
| feed_url | True | placeholder:future_feed_url_not_set | blocks any fetch while placeholder, missing, or malformed |
| feed_type | True | unselected | required for future packet completeness |
| expected_fetch_mode | True | diagnostic_smoke_once | required for future packet completeness |
| expected_output_root | True | _tmp/newsroom_live_rss_diagnostic/{preflight_id} | blocks any fetch if not under an ignored local output root |
| network_access_allowed | True | False | blocks any network action while false |
| max_entries | True | 0 | blocks any fetch if zero now or above future allowed maximum |
| article_page_fetch_allowed | True | False | aborts if true because article scraping is out of scope |
| media_download_allowed | True | False | aborts if true because media download is out of scope |
| render_allowed | True | False | aborts if true because render is out of scope |
| audio_tts_allowed | True | False | aborts if true because audio/TTS is out of scope |
| production_claim_allowed | True | False | aborts if true because production claims are forbidden |
| publication_allowed | True | False | aborts if true because publication is forbidden |
| operator_notes | True | not requested in this slice | required for future packet completeness |
| abort_conditions | True | ["ABORT_NO_EXPLICIT_AUTHORIZATION", "ABORT_FEED_URL_MISSING", "ABORT_FEED_URL_MALFORMED", "ABORT_OUTPUT_ROOT_MISSING", "ABORT_NETWORK_NOT_ALLOWED", "ABORT_ARTICLE_PAGE_FETCH_REQUESTED", "ABORT_MEDIA_DOWNLOAD_REQUESTED", "ABORT_PUBLICATION_RENDER_AUDIO_REQUESTED", "ABORT_TOO_MANY_ENTRIES", "ABORT_TERMS_RIGHTS_UNCLEAR", "ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS", "ABORT_SCRAPING_REQUIRED", "ABORT_PRODUCTION_PUBLIC_CLAIM"] | required for future packet completeness |


## Authorization Model

```json
{
  "states": [
    "not_requested",
    "requested",
    "authorized_for_diagnostic_fetch_once",
    "denied",
    "expired",
    "revoked"
  ],
  "current_authorization_state": "not_requested",
  "current_slice_defaults": {
    "authorization_status": "not_requested",
    "network_access_allowed": false,
    "article_page_fetch_allowed": false,
    "media_download_allowed": false,
    "production_claim_allowed": false,
    "publication_allowed": false
  },
  "future_transition_requirements": {
    "requested": [
      "human-facing authorization sheet exists",
      "feed/source target described without becoming active input",
      "local ignored output root is named"
    ],
    "authorized_for_diagnostic_fetch_once": [
      "explicit future operator approval",
      "single diagnostic smoke scope",
      "max_entries set to a small positive integer",
      "article, media, render, audio, production, and publication flags remain false"
    ]
  },
  "expiry_behavior": "authorization must expire after one diagnostic fetch attempt or at the recorded expiry time",
  "revocation_behavior": "revoked authorization immediately closes LIVE_FETCH_GATE and invalidates the packet"
}
```


## Output Policy

```json
{
  "expected_directory_pattern": "_tmp/newsroom_live_rss_diagnostic/{preflight_id}/",
  "local_only_artifacts": [
    "raw feed response",
    "raw entry snapshot if it contains live content",
    "operator action log with live URL",
    "fetch receipt with live URL if project policy says local-only"
  ],
  "trackable_summary_artifacts": [
    "normalized topic candidate summary",
    "source boundary validation summary",
    "rights/freshness/attribution readback summary",
    "blocker summary"
  ],
  "never_commit_artifacts": [
    "raw feed response body",
    "raw article page body",
    "downloaded media",
    "voice cache",
    "audio/TTS output",
    "render output",
    "YMM4 project files",
    "private operator notes containing live URLs when policy says local-only"
  ],
  "redaction_or_summarization_rules": [
    "replace live URLs with feed_id or source_id before tracked summaries unless policy explicitly allows the URL",
    "summarize entry text instead of committing raw live content",
    "carry source, rights, freshness, attribution, and excluded-claim blockers into tracked summaries",
    "never turn a receipt or summary into production/public approval"
  ]
}
```


## Future Artifact Schemas

| artifact_name | owner | commit_policy | production_blocker_implications |
| --- | --- | --- | --- |
| fetch_receipt | agent after future authorization | local_only | blocks all downstream gates if absent, local policy violated, or production scope appears |
| feed_source_manifest | operator/user with agent schema validation | trackable_summary | blocks authorization if source identity or feed URL policy is unclear |
| raw_entry_snapshot | agent after future authorization | local_only | blocks normalization if URL, timestamp, or title is missing |
| normalized_topic_candidate | agent | trackable_summary | blocks source-boundary gate if normalized identifiers or timestamps are missing |
| source_boundary_validation | agent classification plus operator review when requested | trackable_summary | blocks capsule input if source boundary is unknown or overclaimed |
| rights_attribution_freshness_readback | operator/user for approval; agent for structured readback | trackable_summary | blocks production when rights, attribution, freshness, or quote/media permission is unknown |
| excluded_claims_readback | agent | trackable_summary | blocks capsule readiness if excluded claims are absent or leak into positive claims |
| capsule_input_candidate | agent | trackable_summary | allows diagnostic capsule only; production remains blocked while blockers remain |
| operator_action_log | operator/user | local_only | blocks live fetch if absent, ambiguous, expired, revoked, or wider than diagnostic scope |


## Abort Conditions

| condition_id | condition | severity | gate_affected |
| --- | --- | --- | --- |
| ABORT_NO_EXPLICIT_AUTHORIZATION | no explicit authorization | abort | LIVE_FETCH_GATE |
| ABORT_FEED_URL_MISSING | feed URL missing | abort | LIVE_FETCH_GATE |
| ABORT_FEED_URL_MALFORMED | feed URL malformed | abort | LIVE_FETCH_GATE |
| ABORT_OUTPUT_ROOT_MISSING | output root missing | abort | LIVE_FETCH_GATE |
| ABORT_NETWORK_NOT_ALLOWED | network access not allowed | abort | LIVE_FETCH_GATE |
| ABORT_ARTICLE_PAGE_FETCH_REQUESTED | article page fetch requested | abort | LIVE_FETCH_GATE |
| ABORT_MEDIA_DOWNLOAD_REQUESTED | media download requested | abort | LIVE_FETCH_GATE |
| ABORT_PUBLICATION_RENDER_AUDIO_REQUESTED | publication, render, or audio requested | abort | LIVE_FETCH_GATE |
| ABORT_TOO_MANY_ENTRIES | more entries than allowed | abort | FETCH_RECEIPT_GATE |
| ABORT_TERMS_RIGHTS_UNCLEAR | live source terms or rights unclear | abort | SOURCE_BOUNDARY_GATE |
| ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS | unexpected redirect or non-RSS response | abort | FETCH_RECEIPT_GATE |
| ABORT_SCRAPING_REQUIRED | parser would need scraping outside RSS feed | abort | NORMALIZED_TOPIC_GATE |
| ABORT_PRODUCTION_PUBLIC_CLAIM | any production or public claim requested | abort | PUBLICATION_GATE |


## Post-Fetch Gate Definitions

```json
{
  "FETCH_RECEIPT_GATE": {
    "executed_in_this_slice": false,
    "required_inputs": [
      "preflight_packet",
      "operator_action_log"
    ],
    "pass_criteria": [
      "single diagnostic authorization exists",
      "receipt written under ignored local output root",
      "no article, media, render, audio, production, or publication scope"
    ],
    "fail_criteria": [
      "any abort condition attached to LIVE_FETCH_GATE"
    ],
    "outputs": [
      "fetch_receipt"
    ],
    "next_state": "live_fetch_result_captured"
  },
  "NORMALIZED_TOPIC_GATE": {
    "executed_in_this_slice": false,
    "required_inputs": [
      "raw_entry_snapshot",
      "feed_source_manifest"
    ],
    "pass_criteria": [
      "entry URL and published timestamp exist",
      "raw live content is summarized before tracked readback",
      "no article scraping is required"
    ],
    "fail_criteria": [
      "missing URL/timestamp",
      "scraping required"
    ],
    "outputs": [
      "normalized_topic_candidate"
    ],
    "next_state": "normalized_topic_candidate_ready"
  },
  "SOURCE_BOUNDARY_GATE": {
    "executed_in_this_slice": false,
    "required_inputs": [
      "normalized_topic_candidate",
      "rights_attribution_freshness_readback",
      "excluded_claims_readback"
    ],
    "pass_criteria": [
      "source, rights, freshness, attribution, and reliability are classified",
      "excluded claims are present",
      "production blockers are explicit"
    ],
    "fail_criteria": [
      "unknown source boundary",
      "rights/freshness ambiguity",
      "excluded claim leakage"
    ],
    "outputs": [
      "source_boundary_validation"
    ],
    "next_state": "live_source_boundary_validated"
  },
  "CAPSULE_INPUT_GATE": {
    "executed_in_this_slice": false,
    "required_inputs": [
      "source_boundary_validation",
      "excluded_claims_readback",
      "capsule_input_candidate"
    ],
    "pass_criteria": [
      "diagnostic capsule input carries blockers",
      "production_status remains diagnostic or blocked"
    ],
    "fail_criteria": [
      "clean capsule without blockers",
      "production/public overclaim"
    ],
    "outputs": [
      "capsule_input_candidate"
    ],
    "next_state": "diagnostic_capsule_ready"
  }
}
```


## Readiness Classification

```json
{
  "preflight_contract_ready": true,
  "authorization_sheet_ready": true,
  "fetch_implementation_allowed_now": false,
  "network_access_allowed_now": false,
  "operator_action_required_now": false,
  "next_allowed_state": "authorization_request_preparation",
  "readiness_reason": "contract and packet template are ready for a future human-facing authorization sheet; no fetch or network action is allowed now"
}
```


## Business Goal Outcome Contract
- problem_clear: True - The contract blocks unauthorized live fetch by default.
- offer_clear: True - The next live RSS step is governable through a packet, authorization model, aborts, and gates.
- proof_clear: True - This defines preflight only, not implementation.
- boundary_clear: True - Live/source/rights/public claims remain blocked.
- next_action_clear: True - newsroom-live-rss-operator-authorization-sheet-v1
- visual_supports_explanation: True - YMM4 visual proof stays closed.

## Boundaries

```json
{
  "network_fetch_performed": false,
  "live_RSS_news_fetch_performed": false,
  "live_feed_source_added": false,
  "fetch_adapter_implemented": false,
  "article_scraping_performed": false,
  "authorization_requested_from_user": false,
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

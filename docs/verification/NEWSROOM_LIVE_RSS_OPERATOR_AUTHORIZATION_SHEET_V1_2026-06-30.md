# Newsroom Live RSS Operator Authorization Sheet V1

## Identity

```json
{
  "authorization_sheet_id": "newsroom_live_rss_operator_authorization_sheet_v1_2026_06_30",
  "authorization_packet_template_id": "newsroom_live_rss_authorization_packet_template_v1_2026_06_30",
  "source_preflight_contract_path": "samples/_probe/newsroom_handoff/live_rss_preflight_contract_v1.json",
  "source_preflight_packet_template_path": "samples/_probe/newsroom_handoff/live_rss_preflight_packet_template_v1.json",
  "live_fetch_used": false,
  "network_access_used": false,
  "render_gate": "L0_no_render",
  "production_status": "authorization_template_only"
}
```


## Purpose

```json
{
  "summary": "This sheet is a template for a future one-time diagnostic RSS fetch only.",
  "does_not_authorize": "It does not authorize production use, article scraping, media download, render, audio/TTS, publication, source truth approval, rights approval, or public readiness.",
  "current_slice_status": "No actual authorization is requested or granted in this slice."
}
```


## Operator Fields

| field_name | label | required | current_value |
| --- | --- | --- | --- |
| feed_title | Feed title | True | placeholder:future_feed_title_not_set |
| feed_url | Feed URL | True | placeholder:future_feed_url_not_set |
| feed_owner_or_source_name | Feed owner or source name | True | placeholder:future_source_name_not_set |
| why_this_feed | Why this feed is being considered | True | not_requested |
| max_entries | Maximum entries for one diagnostic fetch | True | 0 |
| expected_fetch_mode | Expected fetch mode | True | diagnostic_smoke_once |
| expected_output_root | Expected local ignored output root | True | _tmp/newsroom_live_rss_diagnostic/{authorization_packet_id} |
| authorization_expiry | Authorization expiry | True | not_requested |
| operator_notes | Operator notes | True | not_requested |


## Required Confirmations

| confirmation_id | label | required_value | current_value |
| --- | --- | --- | --- |
| allow_one_time_network_rss_feed_fetch | Allow one-time network RSS feed fetch in a future slice | True | False |
| disallow_article_page_scraping | Disallow article page scraping | True | True |
| disallow_media_download | Disallow media download | True | True |
| disallow_render_export | Disallow render/export | True | True |
| disallow_audio_tts | Disallow audio/TTS | True | True |
| disallow_production_public_claims | Disallow production/public claims | True | True |
| require_local_ignored_raw_outputs | Require local/ignored raw outputs | True | True |
| require_source_boundary_validation_before_capsule | Require source-boundary validation before capsule generation | True | True |
| require_rights_freshness_attribution_readback | Require rights/freshness/attribution readback | True | True |
| require_excluded_claims_readback | Require excluded-claims readback | True | True |
| allow_only_diagnostic_capsule_candidate_after_gates | Allow only diagnostic capsule candidate after gates pass | True | True |


## Forbidden Actions

| action | reason |
| --- | --- |
| article scraping | outside diagnostic RSS feed scope |
| media download | rights and storage scope are not approved |
| publication | publication gate remains closed |
| production script generation | diagnostic source boundary only |
| rights approval | operator/legal decision, not agent authority |
| public readiness claim | separate future approval required |
| rendering | render gate remains L0_no_render |
| YMM4 launch | visual preview is out of scope |
| audio/TTS generation | audio generation is out of scope |
| using live content as final truth without boundary validation | source-boundary validation must pass first |


## Abort Conditions

| condition_id | condition | severity | gate_affected |
| --- | --- | --- | --- |
| ABORT_NO_EXPLICIT_AUTHORIZATION | no explicit authorization | abort | LIVE_FETCH_GATE |
| ABORT_FEED_URL_MISSING | feed URL missing | abort | LIVE_FETCH_GATE |
| ABORT_FEED_URL_MALFORMED | feed URL malformed | abort | LIVE_FETCH_GATE |
| ABORT_OUTPUT_ROOT_MISSING | output root missing | abort | LIVE_FETCH_GATE |
| ABORT_TOO_MANY_ENTRIES | more entries than allowed | abort | FETCH_RECEIPT_GATE |
| ABORT_ARTICLE_PAGE_FETCH_REQUESTED | article page fetch requested | abort | LIVE_FETCH_GATE |
| ABORT_MEDIA_DOWNLOAD_REQUESTED | media download requested | abort | LIVE_FETCH_GATE |
| ABORT_NETWORK_NOT_ALLOWED | network access not allowed | abort | LIVE_FETCH_GATE |
| ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS | unexpected redirect or non-RSS response | abort | FETCH_RECEIPT_GATE |
| ABORT_PRODUCTION_PUBLIC_CLAIM | any production or public claim requested | abort | PUBLICATION_GATE |
| ABORT_TERMS_RIGHTS_UNCLEAR | live source terms or rights unclear | abort | SOURCE_BOUNDARY_GATE |


## Expected Future Results

| artifact_name | expected_policy |
| --- | --- |
| fetch_receipt | local_only |
| feed_source_manifest | trackable_summary |
| raw_entry_snapshot | local_only |
| normalized_topic_candidate | trackable_summary |
| source_boundary_validation | trackable_summary |
| rights_attribution_freshness_readback | trackable_summary |
| excluded_claims_readback | trackable_summary |
| capsule_input_candidate | trackable_summary |
| operator_action_log | local_only |


## Machine Authorization Packet Fields

| field_name | default_value | requires_human_input | blocker_behavior |
| --- | --- | --- | --- |
| authorization_packet_id | placeholder:future_authorization_packet_id | False | required for future packet completeness |
| derived_from_preflight_contract | samples/_probe/newsroom_handoff/live_rss_preflight_contract_v1.json | False | required for future packet completeness |
| authorization_status | not_requested | False | must remain not_requested now; future fetch requires authorized_for_diagnostic_fetch_once |
| requested_by | not_requested | True | required for future packet completeness |
| authorized_by | not_requested | True | required for future packet completeness |
| feed_id | placeholder:future_feed_id_not_set | True | required for future packet completeness |
| feed_title | placeholder:future_feed_title_not_set | True | required for future packet completeness |
| feed_url | placeholder:future_feed_url_not_set | True | placeholder, missing, or malformed feed URL blocks future fetch |
| feed_owner_or_source_name | placeholder:future_source_name_not_set | True | required for future packet completeness |
| authorization_scope | none | True | required for future packet completeness |
| network_access_allowed | False | False | false now; true is only valid after a future explicit authorization slice |
| article_page_fetch_allowed | False | False | true aborts because article scraping is forbidden |
| media_download_allowed | False | False | true aborts because media download is forbidden |
| render_allowed | False | False | true aborts because render is forbidden |
| audio_tts_allowed | False | False | true aborts because audio/TTS is forbidden |
| production_claim_allowed | False | False | true aborts because production claims are forbidden |
| publication_allowed | False | False | true aborts because publication is forbidden |
| max_entries | 0 | True | required for future packet completeness |
| expected_fetch_mode | diagnostic_smoke_once | False | required for future packet completeness |
| expected_output_root | _tmp/newsroom_live_rss_diagnostic/{authorization_packet_id} | True | required for future packet completeness |
| authorization_expiry | not_requested | True | required for future packet completeness |
| operator_confirmations | {"allow_one_time_network_rss_feed_fetch": false, "allow_only_diagnostic_capsule_candidate_after_gates": true, "disallow_article_page_scraping": true, "disallow_audio_tts": true, "disallow_media_download": true, "disallow_production_public_claims": true, "disallow_render_export": true, "require_excluded_claims_readback": true, "require_local_ignored_raw_outputs": true, "require_rights_freshness_attribution_readback": true, "require_source_boundary_validation_before_capsule": true} | True | required confirmations must be explicit in a future authorization packet |
| abort_conditions | ["ABORT_NO_EXPLICIT_AUTHORIZATION", "ABORT_FEED_URL_MISSING", "ABORT_FEED_URL_MALFORMED", "ABORT_OUTPUT_ROOT_MISSING", "ABORT_NETWORK_NOT_ALLOWED", "ABORT_ARTICLE_PAGE_FETCH_REQUESTED", "ABORT_MEDIA_DOWNLOAD_REQUESTED", "ABORT_PUBLICATION_RENDER_AUDIO_REQUESTED", "ABORT_TOO_MANY_ENTRIES", "ABORT_TERMS_RIGHTS_UNCLEAR", "ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS", "ABORT_SCRAPING_REQUIRED", "ABORT_PRODUCTION_PUBLIC_CLAIM"] | False | required for future packet completeness |
| required_future_artifacts | ["fetch_receipt", "feed_source_manifest", "raw_entry_snapshot", "normalized_topic_candidate", "source_boundary_validation", "rights_attribution_freshness_readback", "excluded_claims_readback", "capsule_input_candidate", "operator_action_log"] | False | required for future packet completeness |
| next_gate_after_authorization | FETCH_RECEIPT_GATE | False | required for future packet completeness |


## Safety Classification

```json
{
  "authorization_sheet_ready": true,
  "actual_authorization_requested_now": false,
  "fetch_implementation_allowed_now": false,
  "network_access_allowed_now": false,
  "operator_action_required_now": false,
  "next_allowed_state": "authorization_request_or_source_manifest_schema",
  "next_recommended_axis": "newsroom-rss-source-manifest-schema-v1",
  "reason": "The sheet and packet template are ready, but source manifest schema is the next safer prerequisite before asking for real authorization."
}
```


## Business Goal Outcome Contract
- problem_clear: True - The sheet prevents implicit fetch authorization by keeping authorization not requested now.
- offer_clear: True - Future human authorization is explicit through fill-in fields and confirmations.
- proof_clear: True - This defines templates, not fetch implementation.
- boundary_clear: True - Source, rights, production, publication, render, YMM4, and audio claims remain blocked.
- next_action_clear: True - newsroom-rss-source-manifest-schema-v1
- visual_supports_explanation: True - YMM4 visual proof stays closed.

## Boundaries

```json
{
  "network_fetch_performed": false,
  "network_access_used": false,
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

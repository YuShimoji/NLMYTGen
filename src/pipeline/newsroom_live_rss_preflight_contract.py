"""Define a future live RSS preflight contract without fetching.

The contract describes the packet, authorization model, output policy, abort
conditions, and post-fetch gates required before a future diagnostic live RSS
smoke. It writes tracked planning JSON/Markdown only and does not implement
network access, fetch adapters, real feed inputs, scraping, YMM4 work, render,
or audio/TTS generation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_live_rss_boundary_plan import (
    DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _write_json,
    _write_text,
)


PREFLIGHT_CONTRACT_ID = "newsroom_live_rss_preflight_contract_v1_2026_06_30"
PREFLIGHT_PACKET_TEMPLATE_ID = (
    "newsroom_live_rss_preflight_packet_template_v1_2026_06_30"
)
PREFLIGHT_CONTRACT_SCHEMA_VERSION = "newsroom_live_rss_preflight_contract.v1"
PREFLIGHT_PACKET_SCHEMA_VERSION = "newsroom_live_rss_preflight_packet.v1"

DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_preflight_contract_v1.json"
)
DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_preflight_packet_template_v1.json"
)
DEFAULT_LIVE_RSS_PREFLIGHT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_LIVE_RSS_PREFLIGHT_CONTRACT_V1_2026-06-30.md"
)

RENDER_GATE = "L0_no_render"
PRODUCTION_STATUS = "preflight_contract_only"
NEXT_RECOMMENDED_AXIS = "newsroom-live-rss-operator-authorization-sheet-v1"


def write_default_newsroom_live_rss_preflight_contract_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    boundary_plan = _load_json_object(base / DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH)
    boundary_contract = _load_json_object(
        base / DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH
    )
    packet_template = build_live_rss_preflight_packet_template(
        boundary_plan=boundary_plan,
        boundary_contract=boundary_contract,
    )
    contract = build_live_rss_preflight_contract(
        boundary_plan=boundary_plan,
        boundary_contract=boundary_contract,
        packet_template=packet_template,
    )
    _write_json(base / DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH, packet_template)
    _write_json(base / DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH, contract)
    _write_text(
        base / DEFAULT_LIVE_RSS_PREFLIGHT_DOC_PATH,
        render_live_rss_preflight_contract_markdown(
            contract=contract,
            packet_template=packet_template,
        ),
    )
    return {"packet_template": packet_template, "contract": contract}


def build_live_rss_preflight_packet_template(
    *,
    boundary_plan: dict[str, Any],
    boundary_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "preflight_packet_template_id": PREFLIGHT_PACKET_TEMPLATE_ID,
        "schema_version": PREFLIGHT_PACKET_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "render_gate": RENDER_GATE,
        "production_status": PRODUCTION_STATUS,
        "live_fetch_used": False,
        "source_boundary_plan_path": DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH.as_posix(),
        "source_boundary_contract_path": (
            DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH.as_posix()
        ),
        "source_boundary_readback": _source_boundary_readback(
            boundary_plan=boundary_plan,
            boundary_contract=boundary_contract,
        ),
        "packet_defaults": _packet_defaults(),
        "preflight_packet_schema": _preflight_packet_schema(),
        "abort_conditions": _abort_conditions(),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def build_live_rss_preflight_contract(
    *,
    boundary_plan: dict[str, Any],
    boundary_contract: dict[str, Any],
    packet_template: dict[str, Any],
) -> dict[str, Any]:
    readiness = _readiness_classification(packet_template)
    return {
        "preflight_contract_id": PREFLIGHT_CONTRACT_ID,
        "schema_version": PREFLIGHT_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "render_gate": RENDER_GATE,
        "production_status": PRODUCTION_STATUS,
        "live_fetch_used": False,
        "source_boundary_plan_path": DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH.as_posix(),
        "source_boundary_contract_path": (
            DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH.as_posix()
        ),
        "source_boundary_readback": _source_boundary_readback(
            boundary_plan=boundary_plan,
            boundary_contract=boundary_contract,
        ),
        "preflight_packet_template_path": (
            DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH.as_posix()
        ),
        "preflight_packet_schema": packet_template["preflight_packet_schema"],
        "authorization_model": _authorization_model(),
        "future_output_policy": _future_output_policy(),
        "future_artifact_schemas": _future_artifact_schemas(),
        "abort_conditions": packet_template["abort_conditions"],
        "post_fetch_gate_definitions": _post_fetch_gate_definitions(),
        "readiness_classification": readiness,
        "business_goal_outcome_contract": _business_goal_outcome_contract(readiness),
        "completion_matrix": _completion_matrix(),
        "inertia_check": _inertia_check(),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def render_live_rss_preflight_contract_markdown(
    *,
    contract: dict[str, Any],
    packet_template: dict[str, Any],
) -> str:
    lines = ["# Newsroom Live RSS Preflight Contract V1"]
    _append_mapping(
        lines,
        "Identity",
        {
            "preflight_contract_id": contract["preflight_contract_id"],
            "preflight_packet_template_id": packet_template[
                "preflight_packet_template_id"
            ],
            "source_boundary_plan_path": contract["source_boundary_plan_path"],
            "source_boundary_contract_path": contract["source_boundary_contract_path"],
            "live_fetch_used": contract["live_fetch_used"],
            "render_gate": contract["render_gate"],
            "production_status": contract["production_status"],
        },
    )
    _append_rows(
        lines,
        "Preflight Packet Schema",
        [
            "field_name",
            "required",
            "current_default_value",
            "blocker_behavior",
        ],
        contract["preflight_packet_schema"],
    )
    _append_mapping(lines, "Authorization Model", contract["authorization_model"])
    _append_mapping(lines, "Output Policy", contract["future_output_policy"])
    _append_rows(
        lines,
        "Future Artifact Schemas",
        ["artifact_name", "owner", "commit_policy", "production_blocker_implications"],
        contract["future_artifact_schemas"],
    )
    _append_rows(
        lines,
        "Abort Conditions",
        ["condition_id", "condition", "severity", "gate_affected"],
        contract["abort_conditions"],
    )
    _append_mapping(
        lines,
        "Post-Fetch Gate Definitions",
        contract["post_fetch_gate_definitions"],
    )
    _append_mapping(lines, "Readiness Classification", contract["readiness_classification"])
    lines.extend(["", "## Business Goal Outcome Contract"])
    for key, value in contract["business_goal_outcome_contract"].items():
        lines.append(f"- {key}: {value['status']} - {value['rationale']}")
    _append_mapping(lines, "Boundaries", contract["boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def _source_boundary_readback(
    *,
    boundary_plan: dict[str, Any],
    boundary_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "boundary_plan_id": boundary_plan.get("plan_id"),
        "boundary_contract_id": boundary_contract.get("contract_id"),
        "boundary_current_state": boundary_plan.get("state_machine", {}).get(
            "current_state"
        ),
        "live_fetch_implementation_allowed_now": boundary_plan.get(
            "decision_readback", {}
        ).get("live_fetch_implementation_allowed_now"),
        "live_boundary_plan_ready": boundary_plan.get("decision_readback", {}).get(
            "live_boundary_plan_ready"
        ),
        "required_future_artifact_count": len(
            boundary_contract.get("future_live_rss_artifact_contract", [])
        ),
        "gate_names": list(boundary_contract.get("gate_definitions", {}).keys()),
    }


def _packet_defaults() -> dict[str, Any]:
    return {
        "preflight_id": "placeholder:future_preflight_id",
        "requested_by": "not_requested",
        "authorization_status": "not_requested",
        "authorization_scope": "none",
        "feed_id": "placeholder:future_feed_id_not_set",
        "feed_title": "placeholder:future_feed_title_not_set",
        "feed_url": "placeholder:future_feed_url_not_set",
        "feed_type": "unselected",
        "expected_fetch_mode": "diagnostic_smoke_once",
        "expected_output_root": "_tmp/newsroom_live_rss_diagnostic/{preflight_id}",
        "network_access_allowed": False,
        "max_entries": 0,
        "article_page_fetch_allowed": False,
        "media_download_allowed": False,
        "render_allowed": False,
        "audio_tts_allowed": False,
        "production_claim_allowed": False,
        "publication_allowed": False,
        "operator_notes": "not requested in this slice",
        "abort_conditions": [row["condition_id"] for row in _abort_conditions()],
    }


def _preflight_packet_schema() -> list[dict[str, Any]]:
    fields = [
        ("preflight_id", True, "string", "unique future preflight id"),
        ("requested_by", True, "string", "operator identity or not_requested"),
        (
            "authorization_status",
            True,
            "enum",
            "authorization state for the future diagnostic fetch",
        ),
        ("authorization_scope", True, "string", "must remain diagnostic-only"),
        ("feed_id", True, "string", "future feed/source manifest id"),
        ("feed_title", True, "string", "operator-facing feed/source label"),
        ("feed_url", True, "string", "future RSS/Atom URL, unset in this slice"),
        ("feed_type", True, "enum", "rss, atom, or unselected"),
        ("expected_fetch_mode", True, "enum", "diagnostic smoke mode"),
        ("expected_output_root", True, "path", "future local ignored output root"),
        ("network_access_allowed", True, "boolean", "must be false now"),
        ("max_entries", True, "integer", "maximum entries in future smoke"),
        ("article_page_fetch_allowed", True, "boolean", "must be false"),
        ("media_download_allowed", True, "boolean", "must be false"),
        ("render_allowed", True, "boolean", "must be false"),
        ("audio_tts_allowed", True, "boolean", "must be false"),
        ("production_claim_allowed", True, "boolean", "must be false"),
        ("publication_allowed", True, "boolean", "must be false"),
        ("operator_notes", True, "string", "future human note field"),
        ("abort_conditions", True, "list[string]", "abort condition ids to enforce"),
    ]
    defaults = _packet_defaults()
    allowed_values = {
        "authorization_status": [
            "not_requested",
            "requested",
            "authorized_for_diagnostic_fetch_once",
            "denied",
            "expired",
            "revoked",
        ],
        "feed_type": ["unselected", "rss", "atom"],
        "expected_fetch_mode": ["diagnostic_smoke_once"],
        "network_access_allowed": [False],
        "article_page_fetch_allowed": [False],
        "media_download_allowed": [False],
        "render_allowed": [False],
        "audio_tts_allowed": [False],
        "production_claim_allowed": [False],
        "publication_allowed": [False],
    }
    return [
        {
            "field_name": field_name,
            "required": required,
            "value_type": value_type,
            "purpose": purpose,
            "allowed_values": allowed_values.get(field_name, "future explicit value required"),
            "current_default_value": defaults[field_name],
            "blocker_behavior": _field_blocker_behavior(field_name),
        }
        for field_name, required, value_type, purpose in fields
    ]


def _field_blocker_behavior(field_name: str) -> str:
    blockers = {
        "authorization_status": "blocks any fetch unless authorized_for_diagnostic_fetch_once in a future slice",
        "feed_url": "blocks any fetch while placeholder, missing, or malformed",
        "expected_output_root": "blocks any fetch if not under an ignored local output root",
        "network_access_allowed": "blocks any network action while false",
        "max_entries": "blocks any fetch if zero now or above future allowed maximum",
        "article_page_fetch_allowed": "aborts if true because article scraping is out of scope",
        "media_download_allowed": "aborts if true because media download is out of scope",
        "render_allowed": "aborts if true because render is out of scope",
        "audio_tts_allowed": "aborts if true because audio/TTS is out of scope",
        "production_claim_allowed": "aborts if true because production claims are forbidden",
        "publication_allowed": "aborts if true because publication is forbidden",
    }
    return blockers.get(field_name, "required for future packet completeness")


def _authorization_model() -> dict[str, Any]:
    return {
        "states": [
            "not_requested",
            "requested",
            "authorized_for_diagnostic_fetch_once",
            "denied",
            "expired",
            "revoked",
        ],
        "current_authorization_state": "not_requested",
        "current_slice_defaults": {
            "authorization_status": "not_requested",
            "network_access_allowed": False,
            "article_page_fetch_allowed": False,
            "media_download_allowed": False,
            "production_claim_allowed": False,
            "publication_allowed": False,
        },
        "future_transition_requirements": {
            "requested": [
                "human-facing authorization sheet exists",
                "feed/source target described without becoming active input",
                "local ignored output root is named",
            ],
            "authorized_for_diagnostic_fetch_once": [
                "explicit future operator approval",
                "single diagnostic smoke scope",
                "max_entries set to a small positive integer",
                "article, media, render, audio, production, and publication flags remain false",
            ],
        },
        "expiry_behavior": (
            "authorization must expire after one diagnostic fetch attempt or at the recorded expiry time"
        ),
        "revocation_behavior": (
            "revoked authorization immediately closes LIVE_FETCH_GATE and invalidates the packet"
        ),
    }


def _future_output_policy() -> dict[str, Any]:
    return {
        "expected_directory_pattern": "_tmp/newsroom_live_rss_diagnostic/{preflight_id}/",
        "local_only_artifacts": [
            "raw feed response",
            "raw entry snapshot if it contains live content",
            "operator action log with live URL",
            "fetch receipt with live URL if project policy says local-only",
        ],
        "trackable_summary_artifacts": [
            "normalized topic candidate summary",
            "source boundary validation summary",
            "rights/freshness/attribution readback summary",
            "blocker summary",
        ],
        "never_commit_artifacts": [
            "raw feed response body",
            "raw article page body",
            "downloaded media",
            "voice cache",
            "audio/TTS output",
            "render output",
            "YMM4 project files",
            "private operator notes containing live URLs when policy says local-only",
        ],
        "redaction_or_summarization_rules": [
            "replace live URLs with feed_id or source_id before tracked summaries unless policy explicitly allows the URL",
            "summarize entry text instead of committing raw live content",
            "carry source, rights, freshness, attribution, and excluded-claim blockers into tracked summaries",
            "never turn a receipt or summary into production/public approval",
        ],
    }


def _future_artifact_schemas() -> list[dict[str, Any]]:
    return [
        _artifact_schema(
            "fetch_receipt",
            "agent after future authorization",
            "local_only",
            [
                "fetch_receipt_id",
                "preflight_id",
                "authorization_status",
                "feed_id",
                "retrieved_at",
                "network_access_allowed",
                "max_entries_requested",
                "result_status",
                "abort_condition_ids",
            ],
            "blocks all downstream gates if absent, local policy violated, or production scope appears",
        ),
        _artifact_schema(
            "feed_source_manifest",
            "operator/user with agent schema validation",
            "trackable_summary",
            [
                "feed_id",
                "feed_title",
                "feed_type",
                "source_name",
                "feed_url_policy",
                "allowed_use",
                "retention_policy",
            ],
            "blocks authorization if source identity or feed URL policy is unclear",
        ),
        _artifact_schema(
            "raw_entry_snapshot",
            "agent after future authorization",
            "local_only",
            [
                "fetch_receipt_id",
                "entry_id",
                "entry_title",
                "entry_url",
                "entry_published_at",
                "entry_summary_raw",
                "raw_metadata",
            ],
            "blocks normalization if URL, timestamp, or title is missing",
        ),
        _artifact_schema(
            "normalized_topic_candidate",
            "agent",
            "trackable_summary",
            [
                "topic_id",
                "feed_id",
                "entry_title_summary",
                "entry_url_policy",
                "entry_published_at",
                "retrieved_at",
                "fetch_receipt_id",
            ],
            "blocks source-boundary gate if normalized identifiers or timestamps are missing",
        ),
        _artifact_schema(
            "source_boundary_validation",
            "agent classification plus operator review when requested",
            "trackable_summary",
            [
                "topic_id",
                "source_url_policy",
                "entry_published_at",
                "retrieved_at",
                "source_reliability_note",
                "source_truth_approved",
                "production_blockers",
            ],
            "blocks capsule input if source boundary is unknown or overclaimed",
        ),
        _artifact_schema(
            "rights_attribution_freshness_readback",
            "operator/user for approval; agent for structured readback",
            "trackable_summary",
            [
                "topic_id",
                "rights_status",
                "attribution_note",
                "freshness_status",
                "quote_media_permission_status",
                "review_required",
                "production_blockers",
            ],
            "blocks production when rights, attribution, freshness, or quote/media permission is unknown",
        ),
        _artifact_schema(
            "excluded_claims_readback",
            "agent",
            "trackable_summary",
            [
                "topic_id",
                "excluded_claims",
                "excluded_claim_count",
                "excluded_claims_used_as_positive_claims",
                "leak_check_status",
            ],
            "blocks capsule readiness if excluded claims are absent or leak into positive claims",
        ),
        _artifact_schema(
            "capsule_input_candidate",
            "agent",
            "trackable_summary",
            [
                "topic_id",
                "normalized_topic_candidate_id",
                "source_boundary_validation_id",
                "rights_readback_id",
                "excluded_claims_readback_id",
                "production_status",
                "diagnostic_capsule_allowed",
            ],
            "allows diagnostic capsule only; production remains blocked while blockers remain",
        ),
        _artifact_schema(
            "operator_action_log",
            "operator/user",
            "local_only",
            [
                "preflight_id",
                "operator",
                "authorized_action",
                "authorized_at",
                "authorization_scope",
                "target_descriptor",
                "expiry_or_revocation",
            ],
            "blocks live fetch if absent, ambiguous, expired, revoked, or wider than diagnostic scope",
        ),
    ]


def _artifact_schema(
    artifact_name: str,
    owner: str,
    commit_policy: str,
    required_fields: list[str],
    production_blocker_implications: str,
) -> dict[str, Any]:
    return {
        "artifact_name": artifact_name,
        "purpose": f"future diagnostic live RSS preflight artifact: {artifact_name}",
        "owner": owner,
        "required_fields": required_fields,
        "commit_policy": commit_policy,
        "production_blocker_implications": production_blocker_implications,
    }


def _abort_conditions() -> list[dict[str, Any]]:
    conditions = [
        ("ABORT_NO_EXPLICIT_AUTHORIZATION", "no explicit authorization", "LIVE_FETCH_GATE"),
        ("ABORT_FEED_URL_MISSING", "feed URL missing", "LIVE_FETCH_GATE"),
        ("ABORT_FEED_URL_MALFORMED", "feed URL malformed", "LIVE_FETCH_GATE"),
        ("ABORT_OUTPUT_ROOT_MISSING", "output root missing", "LIVE_FETCH_GATE"),
        ("ABORT_NETWORK_NOT_ALLOWED", "network access not allowed", "LIVE_FETCH_GATE"),
        ("ABORT_ARTICLE_PAGE_FETCH_REQUESTED", "article page fetch requested", "LIVE_FETCH_GATE"),
        ("ABORT_MEDIA_DOWNLOAD_REQUESTED", "media download requested", "LIVE_FETCH_GATE"),
        ("ABORT_PUBLICATION_RENDER_AUDIO_REQUESTED", "publication, render, or audio requested", "LIVE_FETCH_GATE"),
        ("ABORT_TOO_MANY_ENTRIES", "more entries than allowed", "FETCH_RECEIPT_GATE"),
        ("ABORT_TERMS_RIGHTS_UNCLEAR", "live source terms or rights unclear", "SOURCE_BOUNDARY_GATE"),
        ("ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS", "unexpected redirect or non-RSS response", "FETCH_RECEIPT_GATE"),
        ("ABORT_SCRAPING_REQUIRED", "parser would need scraping outside RSS feed", "NORMALIZED_TOPIC_GATE"),
        ("ABORT_PRODUCTION_PUBLIC_CLAIM", "any production or public claim requested", "PUBLICATION_GATE"),
    ]
    return [
        {
            "condition_id": condition_id,
            "condition": condition,
            "severity": "abort",
            "gate_affected": gate,
            "expected_behavior": "stop future diagnostic fetch and record blocker readback",
        }
        for condition_id, condition, gate in conditions
    ]


def _post_fetch_gate_definitions() -> dict[str, Any]:
    return {
        "FETCH_RECEIPT_GATE": {
            "executed_in_this_slice": False,
            "required_inputs": ["preflight_packet", "operator_action_log"],
            "pass_criteria": [
                "single diagnostic authorization exists",
                "receipt written under ignored local output root",
                "no article, media, render, audio, production, or publication scope",
            ],
            "fail_criteria": ["any abort condition attached to LIVE_FETCH_GATE"],
            "outputs": ["fetch_receipt"],
            "next_state": "live_fetch_result_captured",
        },
        "NORMALIZED_TOPIC_GATE": {
            "executed_in_this_slice": False,
            "required_inputs": ["raw_entry_snapshot", "feed_source_manifest"],
            "pass_criteria": [
                "entry URL and published timestamp exist",
                "raw live content is summarized before tracked readback",
                "no article scraping is required",
            ],
            "fail_criteria": ["missing URL/timestamp", "scraping required"],
            "outputs": ["normalized_topic_candidate"],
            "next_state": "normalized_topic_candidate_ready",
        },
        "SOURCE_BOUNDARY_GATE": {
            "executed_in_this_slice": False,
            "required_inputs": [
                "normalized_topic_candidate",
                "rights_attribution_freshness_readback",
                "excluded_claims_readback",
            ],
            "pass_criteria": [
                "source, rights, freshness, attribution, and reliability are classified",
                "excluded claims are present",
                "production blockers are explicit",
            ],
            "fail_criteria": ["unknown source boundary", "rights/freshness ambiguity", "excluded claim leakage"],
            "outputs": ["source_boundary_validation"],
            "next_state": "live_source_boundary_validated",
        },
        "CAPSULE_INPUT_GATE": {
            "executed_in_this_slice": False,
            "required_inputs": [
                "source_boundary_validation",
                "excluded_claims_readback",
                "capsule_input_candidate",
            ],
            "pass_criteria": [
                "diagnostic capsule input carries blockers",
                "production_status remains diagnostic or blocked",
            ],
            "fail_criteria": ["clean capsule without blockers", "production/public overclaim"],
            "outputs": ["capsule_input_candidate"],
            "next_state": "diagnostic_capsule_ready",
        },
    }


def _readiness_classification(packet_template: dict[str, Any]) -> dict[str, Any]:
    schema_fields = {
        row["field_name"] for row in packet_template["preflight_packet_schema"]
    }
    required_fields = set(_packet_defaults())
    complete = required_fields.issubset(schema_fields)
    return {
        "preflight_contract_ready": complete,
        "authorization_sheet_ready": complete,
        "fetch_implementation_allowed_now": False,
        "network_access_allowed_now": False,
        "operator_action_required_now": False,
        "next_allowed_state": "authorization_request_preparation",
        "readiness_reason": (
            "contract and packet template are ready for a future human-facing authorization sheet; no fetch or network action is allowed now"
        ),
    }


def _business_goal_outcome_contract(readiness: dict[str, Any]) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "The contract blocks unauthorized live fetch by default.",
        },
        "offer_clear": {
            "status": readiness["preflight_contract_ready"],
            "rationale": "The next live RSS step is governable through a packet, authorization model, aborts, and gates.",
        },
        "proof_clear": {
            "status": True,
            "rationale": "This defines preflight only, not implementation.",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "Live/source/rights/public claims remain blocked.",
        },
        "next_action_clear": {
            "status": True,
            "rationale": NEXT_RECOMMENDED_AXIS,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "YMM4 visual proof stays closed.",
        },
    }


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "boundary_plan_inspected", "status": True},
        {"gate": "preflight_packet_schema_created", "status": True},
        {"gate": "authorization_model_created", "status": True},
        {"gate": "future_output_policy_created", "status": True},
        {"gate": "artifact_schemas_created", "status": True},
        {"gate": "abort_conditions_and_post_fetch_gates_created", "status": True},
        {"gate": "readiness_classification_recorded", "status": True},
        {"gate": "next_axis_selected", "status": True},
        {"gate": "no_forbidden_live_visual_media_scope_reopened", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_live_rss_or_network_fetch", "status": True},
        {"gate": "no_fetch_implementation", "status": True},
        {"gate": "no_YMM4_visual_loop", "status": True},
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_production_public_readiness_claim", "status": True},
    ]


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "network_access": False,
        "live_fetch_implementation": False,
        "active_real_feed_source": False,
        "fetch_adapter": False,
        "article_scraping": False,
        "production_script_generation": False,
        "production_subtitle_design": False,
        "production_card_design": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
        "local_ymmp_materialization": False,
        "authorization_request_in_this_slice": False,
    }


def _closed_boundaries() -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "live_feed_source_added": False,
        "fetch_adapter_implemented": False,
        "article_scraping_performed": False,
        "authorization_requested_from_user": False,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "animation_tuned": False,
        "local_ignored_ymmp_created_in_this_slice": False,
        "local_ignored_ymmp_modified_in_this_slice": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _load_json_object(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    write_default_newsroom_live_rss_preflight_contract_artifacts()

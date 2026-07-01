"""Create live RSS operator authorization templates without requesting approval.

This slice produces a human-facing authorization sheet and a machine-readable
authorization packet template for a future one-time diagnostic live RSS fetch.
It does not ask for authorization, fetch RSS/news, access the network, add a
feed, implement adapters, scrape articles, render, launch YMM4, or generate
audio/TTS.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_live_rss_preflight_contract import (
    DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _write_json,
    _write_text,
)


AUTHORIZATION_SHEET_ID = (
    "newsroom_live_rss_operator_authorization_sheet_v1_2026_06_30"
)
AUTHORIZATION_PACKET_TEMPLATE_ID = (
    "newsroom_live_rss_authorization_packet_template_v1_2026_06_30"
)
AUTHORIZATION_SHEET_SCHEMA_VERSION = "newsroom_live_rss_operator_authorization_sheet.v1"
AUTHORIZATION_PACKET_SCHEMA_VERSION = "newsroom_live_rss_authorization_packet.v1"

DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_operator_authorization_sheet_v1.json"
)
DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_authorization_packet_template_v1.json"
)
DEFAULT_OPERATOR_AUTHORIZATION_DOC_PATH = Path(
    "docs/verification/NEWSROOM_LIVE_RSS_OPERATOR_AUTHORIZATION_SHEET_V1_2026-06-30.md"
)

RENDER_GATE = "L0_no_render"
PRODUCTION_STATUS = "authorization_template_only"
NEXT_RECOMMENDED_AXIS = "newsroom-rss-source-manifest-schema-v1"


def write_default_newsroom_live_rss_operator_authorization_sheet_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    preflight_contract = _load_json_object(
        base / DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH
    )
    preflight_packet_template = _load_json_object(
        base / DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH
    )
    authorization_packet_template = build_live_rss_authorization_packet_template(
        preflight_contract=preflight_contract,
        preflight_packet_template=preflight_packet_template,
    )
    authorization_sheet = build_live_rss_operator_authorization_sheet(
        preflight_contract=preflight_contract,
        preflight_packet_template=preflight_packet_template,
        authorization_packet_template=authorization_packet_template,
    )
    _write_json(
        base / DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH,
        authorization_packet_template,
    )
    _write_json(base / DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH, authorization_sheet)
    _write_text(
        base / DEFAULT_OPERATOR_AUTHORIZATION_DOC_PATH,
        render_live_rss_operator_authorization_sheet_markdown(
            authorization_sheet=authorization_sheet,
            authorization_packet_template=authorization_packet_template,
        ),
    )
    return {
        "authorization_sheet": authorization_sheet,
        "authorization_packet_template": authorization_packet_template,
    }


def build_live_rss_operator_authorization_sheet(
    *,
    preflight_contract: dict[str, Any],
    preflight_packet_template: dict[str, Any],
    authorization_packet_template: dict[str, Any],
) -> dict[str, Any]:
    safety = _safety_classification()
    return {
        "authorization_sheet_id": AUTHORIZATION_SHEET_ID,
        "schema_version": AUTHORIZATION_SHEET_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "source_preflight_contract_path": (
            DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH.as_posix()
        ),
        "source_preflight_packet_template_path": (
            DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH.as_posix()
        ),
        "authorization_packet_template_path": (
            DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH.as_posix()
        ),
        "live_fetch_used": False,
        "network_access_used": False,
        "render_gate": RENDER_GATE,
        "production_status": PRODUCTION_STATUS,
        "source_preflight_readback": _source_preflight_readback(
            preflight_contract=preflight_contract,
            preflight_packet_template=preflight_packet_template,
        ),
        "user_facing_authorization_sheet": {
            "purpose": _purpose(),
            "operator_fields": _operator_fields(),
            "required_yes_no_confirmations": _required_confirmations(),
            "explicit_forbidden_actions": _forbidden_actions(),
            "abort_conditions": _abort_conditions(preflight_contract),
            "expected_future_results": _expected_future_results(preflight_contract),
            "current_status": {
                "authorization_status": "not_requested",
                "actual_authorization_requested_now": False,
                "sheet_is_template_only": True,
            },
        },
        "machine_authorization_packet_template": authorization_packet_template,
        "safety_classification": safety,
        "business_goal_outcome_contract": _business_goal_outcome_contract(safety),
        "completion_matrix": _completion_matrix(),
        "inertia_check": _inertia_check(),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def build_live_rss_authorization_packet_template(
    *,
    preflight_contract: dict[str, Any],
    preflight_packet_template: dict[str, Any],
) -> dict[str, Any]:
    defaults = _authorization_packet_defaults(preflight_packet_template)
    field_rows = _authorization_packet_field_rows(defaults)
    return {
        "authorization_packet_template_id": AUTHORIZATION_PACKET_TEMPLATE_ID,
        "schema_version": AUTHORIZATION_PACKET_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "derived_from_preflight_contract": (
            DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH.as_posix()
        ),
        "source_preflight_packet_template_path": (
            DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH.as_posix()
        ),
        "live_fetch_used": False,
        "network_access_used": False,
        "render_gate": RENDER_GATE,
        "production_status": PRODUCTION_STATUS,
        "field_list": [row["field_name"] for row in field_rows],
        "fields": field_rows,
        "default_values": defaults,
        "fields_requiring_human_input": [
            row["field_name"] for row in field_rows if row["requires_human_input"]
        ],
        "abort_conditions": defaults["abort_conditions"],
        "required_future_artifacts": defaults["required_future_artifacts"],
        "next_gate_after_authorization": "FETCH_RECEIPT_GATE",
        "source_preflight_readback": _source_preflight_readback(
            preflight_contract=preflight_contract,
            preflight_packet_template=preflight_packet_template,
        ),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def render_live_rss_operator_authorization_sheet_markdown(
    *,
    authorization_sheet: dict[str, Any],
    authorization_packet_template: dict[str, Any],
) -> str:
    sheet = authorization_sheet["user_facing_authorization_sheet"]
    lines = ["# Newsroom Live RSS Operator Authorization Sheet V1"]
    _append_mapping(
        lines,
        "Identity",
        {
            "authorization_sheet_id": authorization_sheet["authorization_sheet_id"],
            "authorization_packet_template_id": authorization_packet_template[
                "authorization_packet_template_id"
            ],
            "source_preflight_contract_path": authorization_sheet[
                "source_preflight_contract_path"
            ],
            "source_preflight_packet_template_path": authorization_sheet[
                "source_preflight_packet_template_path"
            ],
            "live_fetch_used": authorization_sheet["live_fetch_used"],
            "network_access_used": authorization_sheet["network_access_used"],
            "render_gate": authorization_sheet["render_gate"],
            "production_status": authorization_sheet["production_status"],
        },
    )
    _append_mapping(lines, "Purpose", sheet["purpose"])
    _append_rows(
        lines,
        "Operator Fields",
        ["field_name", "label", "required", "current_value"],
        sheet["operator_fields"],
    )
    _append_rows(
        lines,
        "Required Confirmations",
        ["confirmation_id", "label", "required_value", "current_value"],
        sheet["required_yes_no_confirmations"],
    )
    _append_rows(
        lines,
        "Forbidden Actions",
        ["action", "reason"],
        sheet["explicit_forbidden_actions"],
    )
    _append_rows(
        lines,
        "Abort Conditions",
        ["condition_id", "condition", "severity", "gate_affected"],
        sheet["abort_conditions"],
    )
    _append_rows(
        lines,
        "Expected Future Results",
        ["artifact_name", "expected_policy"],
        sheet["expected_future_results"],
    )
    _append_rows(
        lines,
        "Machine Authorization Packet Fields",
        [
            "field_name",
            "default_value",
            "requires_human_input",
            "blocker_behavior",
        ],
        authorization_packet_template["fields"],
    )
    _append_mapping(
        lines,
        "Safety Classification",
        authorization_sheet["safety_classification"],
    )
    lines.extend(["", "## Business Goal Outcome Contract"])
    for key, value in authorization_sheet["business_goal_outcome_contract"].items():
        lines.append(f"- {key}: {value['status']} - {value['rationale']}")
    _append_mapping(lines, "Boundaries", authorization_sheet["boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def _source_preflight_readback(
    *,
    preflight_contract: dict[str, Any],
    preflight_packet_template: dict[str, Any],
) -> dict[str, Any]:
    readiness = preflight_contract.get("readiness_classification", {})
    defaults = preflight_packet_template.get("packet_defaults", {})
    return {
        "preflight_contract_id": preflight_contract.get("preflight_contract_id"),
        "preflight_contract_ready": readiness.get("preflight_contract_ready"),
        "authorization_sheet_ready": readiness.get("authorization_sheet_ready"),
        "fetch_implementation_allowed_now": readiness.get(
            "fetch_implementation_allowed_now"
        ),
        "network_access_allowed_now": readiness.get("network_access_allowed_now"),
        "source_authorization_status": defaults.get("authorization_status"),
        "source_feed_url_default": defaults.get("feed_url"),
        "source_max_entries_default": defaults.get("max_entries"),
    }


def _purpose() -> dict[str, str]:
    return {
        "summary": (
            "This sheet is a template for a future one-time diagnostic RSS fetch only."
        ),
        "does_not_authorize": (
            "It does not authorize production use, article scraping, media download, render, audio/TTS, publication, source truth approval, rights approval, or public readiness."
        ),
        "current_slice_status": (
            "No actual authorization is requested or granted in this slice."
        ),
    }


def _operator_fields() -> list[dict[str, Any]]:
    fields = [
        ("feed_title", "Feed title"),
        ("feed_url", "Feed URL"),
        ("feed_owner_or_source_name", "Feed owner or source name"),
        ("why_this_feed", "Why this feed is being considered"),
        ("max_entries", "Maximum entries for one diagnostic fetch"),
        ("expected_fetch_mode", "Expected fetch mode"),
        ("expected_output_root", "Expected local ignored output root"),
        ("authorization_expiry", "Authorization expiry"),
        ("operator_notes", "Operator notes"),
    ]
    defaults = {
        "feed_title": "placeholder:future_feed_title_not_set",
        "feed_url": "placeholder:future_feed_url_not_set",
        "feed_owner_or_source_name": "placeholder:future_source_name_not_set",
        "why_this_feed": "not_requested",
        "max_entries": 0,
        "expected_fetch_mode": "diagnostic_smoke_once",
        "expected_output_root": "_tmp/newsroom_live_rss_diagnostic/{authorization_packet_id}",
        "authorization_expiry": "not_requested",
        "operator_notes": "not_requested",
    }
    return [
        {
            "field_name": field_name,
            "label": label,
            "required": True,
            "current_value": defaults[field_name],
            "human_fill_required_before_future_fetch": True,
        }
        for field_name, label in fields
    ]


def _required_confirmations() -> list[dict[str, Any]]:
    confirmations = [
        ("allow_one_time_network_rss_feed_fetch", True, False),
        ("disallow_article_page_scraping", True, True),
        ("disallow_media_download", True, True),
        ("disallow_render_export", True, True),
        ("disallow_audio_tts", True, True),
        ("disallow_production_public_claims", True, True),
        ("require_local_ignored_raw_outputs", True, True),
        ("require_source_boundary_validation_before_capsule", True, True),
        ("require_rights_freshness_attribution_readback", True, True),
        ("require_excluded_claims_readback", True, True),
        ("allow_only_diagnostic_capsule_candidate_after_gates", True, True),
    ]
    labels = {
        "allow_one_time_network_rss_feed_fetch": "Allow one-time network RSS feed fetch in a future slice",
        "disallow_article_page_scraping": "Disallow article page scraping",
        "disallow_media_download": "Disallow media download",
        "disallow_render_export": "Disallow render/export",
        "disallow_audio_tts": "Disallow audio/TTS",
        "disallow_production_public_claims": "Disallow production/public claims",
        "require_local_ignored_raw_outputs": "Require local/ignored raw outputs",
        "require_source_boundary_validation_before_capsule": "Require source-boundary validation before capsule generation",
        "require_rights_freshness_attribution_readback": "Require rights/freshness/attribution readback",
        "require_excluded_claims_readback": "Require excluded-claims readback",
        "allow_only_diagnostic_capsule_candidate_after_gates": "Allow only diagnostic capsule candidate after gates pass",
    }
    return [
        {
            "confirmation_id": confirmation_id,
            "label": labels[confirmation_id],
            "required_value": required_value,
            "current_value": current_value,
            "current_status": "template_default_not_authorized"
            if confirmation_id == "allow_one_time_network_rss_feed_fetch"
            else "template_default_safe",
        }
        for confirmation_id, required_value, current_value in confirmations
    ]


def _forbidden_actions() -> list[dict[str, str]]:
    return [
        {"action": "article scraping", "reason": "outside diagnostic RSS feed scope"},
        {"action": "media download", "reason": "rights and storage scope are not approved"},
        {"action": "publication", "reason": "publication gate remains closed"},
        {"action": "production script generation", "reason": "diagnostic source boundary only"},
        {"action": "rights approval", "reason": "operator/legal decision, not agent authority"},
        {"action": "public readiness claim", "reason": "separate future approval required"},
        {"action": "rendering", "reason": "render gate remains L0_no_render"},
        {"action": "YMM4 launch", "reason": "visual preview is out of scope"},
        {"action": "audio/TTS generation", "reason": "audio generation is out of scope"},
        {
            "action": "using live content as final truth without boundary validation",
            "reason": "source-boundary validation must pass first",
        },
    ]


def _abort_conditions(preflight_contract: dict[str, Any]) -> list[dict[str, Any]]:
    source_conditions = preflight_contract.get("abort_conditions", [])
    selected = [
        "ABORT_NO_EXPLICIT_AUTHORIZATION",
        "ABORT_FEED_URL_MISSING",
        "ABORT_FEED_URL_MALFORMED",
        "ABORT_OUTPUT_ROOT_MISSING",
        "ABORT_TOO_MANY_ENTRIES",
        "ABORT_ARTICLE_PAGE_FETCH_REQUESTED",
        "ABORT_MEDIA_DOWNLOAD_REQUESTED",
        "ABORT_NETWORK_NOT_ALLOWED",
        "ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS",
        "ABORT_PRODUCTION_PUBLIC_CLAIM",
        "ABORT_TERMS_RIGHTS_UNCLEAR",
    ]
    by_id = {row["condition_id"]: row for row in source_conditions}
    return [by_id[condition_id] for condition_id in selected if condition_id in by_id]


def _expected_future_results(preflight_contract: dict[str, Any]) -> list[dict[str, str]]:
    schemas = preflight_contract.get("future_artifact_schemas", [])
    return [
        {
            "artifact_name": row["artifact_name"],
            "expected_policy": row["commit_policy"],
        }
        for row in schemas
    ]


def _authorization_packet_defaults(
    preflight_packet_template: dict[str, Any],
) -> dict[str, Any]:
    preflight_defaults = preflight_packet_template.get("packet_defaults", {})
    return {
        "authorization_packet_id": "placeholder:future_authorization_packet_id",
        "derived_from_preflight_contract": (
            DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH.as_posix()
        ),
        "authorization_status": "not_requested",
        "requested_by": "not_requested",
        "authorized_by": "not_requested",
        "feed_id": "placeholder:future_feed_id_not_set",
        "feed_title": "placeholder:future_feed_title_not_set",
        "feed_url": preflight_defaults.get(
            "feed_url",
            "placeholder:future_feed_url_not_set",
        ),
        "feed_owner_or_source_name": "placeholder:future_source_name_not_set",
        "authorization_scope": "none",
        "network_access_allowed": False,
        "article_page_fetch_allowed": False,
        "media_download_allowed": False,
        "render_allowed": False,
        "audio_tts_allowed": False,
        "production_claim_allowed": False,
        "publication_allowed": False,
        "max_entries": 0,
        "expected_fetch_mode": "diagnostic_smoke_once",
        "expected_output_root": "_tmp/newsroom_live_rss_diagnostic/{authorization_packet_id}",
        "authorization_expiry": "not_requested",
        "operator_confirmations": {
            row["confirmation_id"]: row["current_value"]
            for row in _required_confirmations()
        },
        "abort_conditions": list(preflight_defaults.get("abort_conditions", [])),
        "required_future_artifacts": [
            "fetch_receipt",
            "feed_source_manifest",
            "raw_entry_snapshot",
            "normalized_topic_candidate",
            "source_boundary_validation",
            "rights_attribution_freshness_readback",
            "excluded_claims_readback",
            "capsule_input_candidate",
            "operator_action_log",
        ],
        "next_gate_after_authorization": "FETCH_RECEIPT_GATE",
    }


def _authorization_packet_field_rows(defaults: dict[str, Any]) -> list[dict[str, Any]]:
    fields = [
        "authorization_packet_id",
        "derived_from_preflight_contract",
        "authorization_status",
        "requested_by",
        "authorized_by",
        "feed_id",
        "feed_title",
        "feed_url",
        "feed_owner_or_source_name",
        "authorization_scope",
        "network_access_allowed",
        "article_page_fetch_allowed",
        "media_download_allowed",
        "render_allowed",
        "audio_tts_allowed",
        "production_claim_allowed",
        "publication_allowed",
        "max_entries",
        "expected_fetch_mode",
        "expected_output_root",
        "authorization_expiry",
        "operator_confirmations",
        "abort_conditions",
        "required_future_artifacts",
        "next_gate_after_authorization",
    ]
    allowed_values = {
        "authorization_status": [
            "not_requested",
            "requested",
            "authorized_for_diagnostic_fetch_once",
            "denied",
            "expired",
            "revoked",
        ],
        "network_access_allowed": [False],
        "article_page_fetch_allowed": [False],
        "media_download_allowed": [False],
        "render_allowed": [False],
        "audio_tts_allowed": [False],
        "production_claim_allowed": [False],
        "publication_allowed": [False],
        "expected_fetch_mode": ["diagnostic_smoke_once"],
        "next_gate_after_authorization": ["FETCH_RECEIPT_GATE"],
    }
    human_fields = {
        "requested_by",
        "authorized_by",
        "feed_id",
        "feed_title",
        "feed_url",
        "feed_owner_or_source_name",
        "authorization_scope",
        "max_entries",
        "expected_output_root",
        "authorization_expiry",
        "operator_confirmations",
    }
    return [
        {
            "field_name": field,
            "default_value": defaults[field],
            "allowed_values": allowed_values.get(field, "future explicit value required"),
            "requires_human_input": field in human_fields,
            "blocker_behavior": _packet_field_blocker_behavior(field),
        }
        for field in fields
    ]


def _packet_field_blocker_behavior(field_name: str) -> str:
    blockers = {
        "authorization_status": "must remain not_requested now; future fetch requires authorized_for_diagnostic_fetch_once",
        "feed_url": "placeholder, missing, or malformed feed URL blocks future fetch",
        "network_access_allowed": "false now; true is only valid after a future explicit authorization slice",
        "article_page_fetch_allowed": "true aborts because article scraping is forbidden",
        "media_download_allowed": "true aborts because media download is forbidden",
        "render_allowed": "true aborts because render is forbidden",
        "audio_tts_allowed": "true aborts because audio/TTS is forbidden",
        "production_claim_allowed": "true aborts because production claims are forbidden",
        "publication_allowed": "true aborts because publication is forbidden",
        "operator_confirmations": "required confirmations must be explicit in a future authorization packet",
    }
    return blockers.get(field_name, "required for future packet completeness")


def _safety_classification() -> dict[str, Any]:
    return {
        "authorization_sheet_ready": True,
        "actual_authorization_requested_now": False,
        "fetch_implementation_allowed_now": False,
        "network_access_allowed_now": False,
        "operator_action_required_now": False,
        "next_allowed_state": "authorization_request_or_source_manifest_schema",
        "next_recommended_axis": NEXT_RECOMMENDED_AXIS,
        "reason": (
            "The sheet and packet template are ready, but source manifest schema is the next safer prerequisite before asking for real authorization."
        ),
    }


def _business_goal_outcome_contract(safety: dict[str, Any]) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "The sheet prevents implicit fetch authorization by keeping authorization not requested now.",
        },
        "offer_clear": {
            "status": safety["authorization_sheet_ready"],
            "rationale": "Future human authorization is explicit through fill-in fields and confirmations.",
        },
        "proof_clear": {
            "status": True,
            "rationale": "This defines templates, not fetch implementation.",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "Source, rights, production, publication, render, YMM4, and audio claims remain blocked.",
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
        {"gate": "preflight_contract_inspected", "status": True},
        {"gate": "authorization_sheet_created", "status": True},
        {"gate": "authorization_packet_template_created", "status": True},
        {"gate": "safe_default_values_verified", "status": True},
        {"gate": "next_axis_selected", "status": True},
        {"gate": "no_forbidden_live_visual_media_scope_reopened", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_live_rss_or_network_fetch", "status": True},
        {"gate": "no_authorization_request_to_user", "status": True},
        {"gate": "no_fetch_implementation", "status": True},
        {"gate": "no_YMM4_visual_loop", "status": True},
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_production_public_readiness_claim", "status": True},
    ]


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "actual_authorization_request": False,
        "network_access": False,
        "active_real_feed_source": False,
        "live_fetch_implementation": False,
        "fetch_adapter": False,
        "article_scraping": False,
        "production_script_generation": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
        "local_ymmp_materialization": False,
    }


def _closed_boundaries() -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "network_access_used": False,
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
    write_default_newsroom_live_rss_operator_authorization_sheet_artifacts()

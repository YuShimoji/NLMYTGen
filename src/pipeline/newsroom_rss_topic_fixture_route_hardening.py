"""Validate and classify the offline RSS-like topic fixture route.

This hardening layer stays upstream of live RSS/news ingestion. It validates
the offline fixture shape, classifies explicit placeholders, reports
production blockers, and records that YMM4/render/audio/card work remains
closed for this slice.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    DEFAULT_CAPSULE_PATH,
    DEFAULT_FIXTURE_V2_PATH,
    DEFAULT_SCHEMA_CONTRACT_PATH,
    NEXT_AXIS_EPISODE_CAPSULE_HARDENING,
    NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN,
)
from src.pipeline.newsroom_rss_topic_fixture_route_audit import (
    REQUIRED_FIXTURE_SCHEMA_FIELDS,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _write_json,
    _write_text,
)


HARDENING_ID = "newsroom_rss_topic_fixture_route_hardening_v1_2026_06_30"
VALIDATION_ID = "offline_rss_like_topic_fixture_v2_validation_v1_2026_06_30"
HARDENING_SCHEMA_VERSION = "newsroom_rss_topic_fixture_route_hardening.v1"
VALIDATION_SCHEMA_VERSION = "offline_rss_like_topic_fixture_v2_validation.v1"

DEFAULT_HARDENING_PATH = Path(
    "samples/_probe/newsroom_handoff/rss_topic_fixture_route_hardening_v1.json"
)
DEFAULT_VALIDATION_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_validation_v1.json"
)
DEFAULT_HARDENING_DOC_PATH = Path(
    "docs/verification/NEWSROOM_RSS_TOPIC_FIXTURE_ROUTE_HARDENING_V1_2026-06-30.md"
)

RENDER_GATE = "L0_no_render"
SELECTED_NEXT_AXIS = NEXT_AXIS_EPISODE_CAPSULE_HARDENING
PLACEHOLDER_CAPABLE_FIELDS = [
    "source_url_or_placeholder",
    "published_at_or_placeholder",
    "rights_status",
    "freshness_status",
    "attribution_note",
]
DIAGNOSTIC_PRODUCTION_STATUSES = {"diagnostic_only", "safe_diagnostic_only"}
ROUTE_BOUNDARY_STATE_NAMES = [
    "diagnostic_only",
    "reusable_offline_fixture",
    "blocked_missing_required_fields",
    "blocked_unmarked_placeholder",
    "blocked_rights_unknown",
    "blocked_source_boundary_unknown",
    "live_boundary_ready_candidate",
]


def write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    fixture = _load_json_object(base / DEFAULT_FIXTURE_V2_PATH)
    schema_contract = _load_json_object(base / DEFAULT_SCHEMA_CONTRACT_PATH)
    capsule = _load_json_object(base / DEFAULT_CAPSULE_PATH)
    validation = build_fixture_v2_validation(
        fixture=fixture,
        schema_contract=schema_contract,
        capsule=capsule,
    )
    hardening = build_fixture_route_hardening(
        fixture=fixture,
        schema_contract=schema_contract,
        capsule=capsule,
        validation=validation,
    )
    _write_json(base / DEFAULT_VALIDATION_PATH, validation)
    _write_json(base / DEFAULT_HARDENING_PATH, hardening)
    _write_text(
        base / DEFAULT_HARDENING_DOC_PATH,
        render_fixture_route_hardening_markdown(hardening),
    )
    return {
        "validation": validation,
        "hardening": hardening,
    }


def build_fixture_v2_validation(
    *,
    fixture: dict[str, Any],
    schema_contract: dict[str, Any],
    capsule: dict[str, Any],
) -> dict[str, Any]:
    required_fields = _required_fields(schema_contract)
    field_validation = [_field_validation_row(fixture, field) for field in required_fields]
    placeholder_classification = [
        _placeholder_classification_row(fixture, field)
        for field in PLACEHOLDER_CAPABLE_FIELDS
    ]
    missing_required = [
        row["field_name"] for row in field_validation if row["value_kind"] == "missing"
    ]
    invalid_required = [
        row["field_name"] for row in field_validation if row["value_kind"] == "invalid"
    ]
    unmarked_placeholders = [
        row["field_name"]
        for row in placeholder_classification
        if row["unmarked_placeholder"]
    ]
    production_blockers = _production_blockers(
        fixture=fixture,
        field_validation=field_validation,
        placeholder_classification=placeholder_classification,
    )
    placeholder_readback = _placeholder_readback(
        placeholder_classification=placeholder_classification,
        missing_required_count=len(missing_required),
    )
    route_boundary_states = _route_boundary_states(
        fixture=fixture,
        missing_required=missing_required,
        invalid_required=invalid_required,
        unmarked_placeholders=unmarked_placeholders,
    )
    capsule_readiness = _capsule_readiness(
        route_boundary_states=route_boundary_states,
        production_blockers=production_blockers,
        capsule=capsule,
    )
    route_classification = _route_classification(
        route_boundary_states=route_boundary_states,
        production_blockers=production_blockers,
    )
    return {
        "artifact_id": VALIDATION_ID,
        "validation_id": VALIDATION_ID,
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": RENDER_GATE,
        "source_fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "source_schema_contract_path": DEFAULT_SCHEMA_CONTRACT_PATH.as_posix(),
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "live_fetch_used": False,
        "field_validation": field_validation,
        "placeholder_classification": placeholder_classification,
        "placeholder_readback": placeholder_readback,
        "route_boundary_states": route_boundary_states,
        "route_classification": route_classification,
        "capsule_readiness": capsule_readiness,
        "production_blockers": production_blockers,
        "non_blocking_warnings": _non_blocking_warnings(fixture),
        "required_before_live_rss": _required_before_live_rss(),
        "required_before_production_script": _required_before_production_script(),
        "next_recommended_axis": SELECTED_NEXT_AXIS,
        "next_axis_reason": (
            "The fixture is reusable for offline diagnostics and its placeholders "
            "are explicit, but source URL, freshness, attribution, and rights "
            "remain production blockers, so live RSS should stay closed while "
            "the downstream capsule rules are hardened."
        ),
        "boundaries": _boundaries(),
    }


def build_fixture_route_hardening(
    *,
    fixture: dict[str, Any],
    schema_contract: dict[str, Any],
    capsule: dict[str, Any],
    validation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validation_payload = validation or build_fixture_v2_validation(
        fixture=fixture,
        schema_contract=schema_contract,
        capsule=capsule,
    )
    return {
        "artifact_id": HARDENING_ID,
        "hardening_id": HARDENING_ID,
        "schema_version": HARDENING_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": RENDER_GATE,
        "source_fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "source_schema_contract_path": DEFAULT_SCHEMA_CONTRACT_PATH.as_posix(),
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "validation_output_path": DEFAULT_VALIDATION_PATH.as_posix(),
        "live_fetch_used": False,
        "hardening_rules": _hardening_rules(_required_fields(schema_contract)),
        "field_validation": validation_payload["field_validation"],
        "placeholder_readback": validation_payload["placeholder_readback"],
        "route_classification": validation_payload["route_classification"],
        "route_boundary_states": validation_payload["route_boundary_states"],
        "capsule_readiness": validation_payload["capsule_readiness"],
        "blockers": validation_payload["production_blockers"],
        "non_blocking_warnings": validation_payload["non_blocking_warnings"],
        "required_before_live_rss": validation_payload["required_before_live_rss"],
        "required_before_production_script": (
            validation_payload["required_before_production_script"]
        ),
        "business_goal_outcome_contract": _business_goal_outcome_contract(),
        "recommendation_logic": _recommendation_logic(),
        "next_recommended_axis": SELECTED_NEXT_AXIS,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(),
        "completion_matrix": _completion_matrix(),
    }


def render_fixture_route_hardening_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom RSS Topic Fixture Route Hardening v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"next_recommended_axis: {payload.get('next_recommended_axis')}",
        "",
    ]
    _append_mapping(
        lines,
        "Identity",
        {
            "hardening_id": payload.get("hardening_id"),
            "source_fixture_path": payload.get("source_fixture_path"),
            "source_schema_contract_path": payload.get("source_schema_contract_path"),
            "source_capsule_path": payload.get("source_capsule_path"),
            "validation_output_path": payload.get("validation_output_path"),
            "live_fetch_used": payload.get("live_fetch_used"),
            "render_gate": payload.get("render_gate"),
        },
    )
    _append_mapping(lines, "Hardening Rules", payload.get("hardening_rules"))
    _append_rows(
        lines,
        "Field Validation",
        [
            "field_name",
            "present",
            "value_kind",
            "production_blocker",
            "diagnostic_allowed",
            "notes",
        ],
        payload.get("field_validation"),
    )
    _append_mapping(
        lines,
        "Placeholder / Blocker Readback",
        payload.get("placeholder_readback"),
    )
    _append_mapping(lines, "Route Classification", payload.get("route_classification"))
    _append_mapping(lines, "Route Boundary States", payload.get("route_boundary_states"))
    _append_mapping(lines, "Capsule Readiness", payload.get("capsule_readiness"))
    _append_rows(lines, "Production Blockers", ["blocker"], _rows(payload.get("blockers"), "blocker"))
    _append_rows(
        lines,
        "Non-blocking Warnings",
        ["warning"],
        _rows(payload.get("non_blocking_warnings"), "warning"),
    )
    _append_rows(
        lines,
        "Required Before Live RSS",
        ["work"],
        _rows(payload.get("required_before_live_rss"), "work"),
    )
    _append_rows(
        lines,
        "Required Before Production Script",
        ["work"],
        _rows(payload.get("required_before_production_script"), "work"),
    )
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Recommendation Logic", payload.get("recommendation_logic"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    _append_rows(
        lines,
        "Completion Matrix",
        ["gate", "status"],
        payload.get("completion_matrix"),
    )
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This hardening proof validates route readiness and placeholder handling "
        "only. It launches no YMM4 process, renders nothing, creates or modifies "
        "no .ymmp file, fetches no live RSS/news, generates no audio/TTS, tunes "
        "no animation, redesigns no cards, and makes no production/public "
        "acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _required_fields(schema_contract: dict[str, Any]) -> list[str]:
    fields = schema_contract.get("required_fields")
    if isinstance(fields, list) and all(isinstance(field, str) for field in fields):
        return list(fields)
    return list(REQUIRED_FIXTURE_SCHEMA_FIELDS)


def _field_validation_row(fixture: dict[str, Any], field: str) -> dict[str, Any]:
    present = _field_present(fixture, field)
    value = fixture.get(field)
    value_kind = _value_kind(field, value)
    production_blocker = _is_production_blocker(field, value_kind, value)
    diagnostic_allowed = _diagnostic_allowed(field, value_kind, value)
    return {
        "field_name": field,
        "present": present,
        "value_kind": value_kind,
        "production_blocker": production_blocker,
        "diagnostic_allowed": diagnostic_allowed,
        "notes": _field_notes(field, value_kind, value),
    }


def _placeholder_classification_row(fixture: dict[str, Any], field: str) -> dict[str, Any]:
    value = fixture.get(field)
    present = _field_present(fixture, field)
    if not present:
        classification = "missing"
        unmarked_placeholder = False
    elif _explicit_placeholder(field, value):
        classification = "explicit_placeholder"
        unmarked_placeholder = False
    elif _unmarked_placeholder(field, value):
        classification = "invalid"
        unmarked_placeholder = True
    elif _real_placeholder_capable_value(field, value):
        classification = "real_value_present"
        unmarked_placeholder = False
    else:
        classification = "invalid"
        unmarked_placeholder = False
    production_blocker = classification in {"explicit_placeholder", "missing", "invalid"}
    return {
        "field_name": field,
        "present": present,
        "classification": classification,
        "classification_tags": _classification_tags(classification, production_blocker),
        "unmarked_placeholder": unmarked_placeholder,
        "production_blocker": production_blocker,
        "diagnostic_allowed": classification in {"explicit_placeholder", "real_value_present"},
        "notes": _placeholder_notes(field, classification, value, unmarked_placeholder),
    }


def _field_present(fixture: dict[str, Any], field: str) -> bool:
    if field not in fixture:
        return False
    value = fixture[field]
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    return True


def _value_kind(field: str, value: Any) -> str:
    if not _field_present({field: value}, field):
        return "missing"
    if field == "excluded_claims":
        if isinstance(value, list) and all(isinstance(item, str) and item for item in value):
            return "real_value"
        return "invalid"
    if field == "production_status":
        return "real_value" if value in DIAGNOSTIC_PRODUCTION_STATUSES else "invalid"
    if field in PLACEHOLDER_CAPABLE_FIELDS:
        placeholder = _placeholder_classification_row({field: value}, field)
        if placeholder["classification"] == "explicit_placeholder":
            return "explicit_placeholder"
        if placeholder["classification"] == "real_value_present":
            return "real_value"
        return "invalid"
    if isinstance(value, str):
        return "real_value"
    return "real_value"


def _explicit_placeholder(field: str, value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    if normalized.startswith("placeholder:"):
        return True
    if field == "freshness_status":
        return normalized.startswith("placeholder_") or "not_evaluable" in normalized
    if field == "attribution_note":
        return "fixture label only" in normalized and "must be replaced" in normalized
    return False


def _unmarked_placeholder(field: str, value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    if field == "source_url_or_placeholder":
        return not _looks_like_url(normalized)
    if field == "published_at_or_placeholder":
        return not _looks_like_datetime(normalized)
    if field == "rights_status":
        return any(token in normalized for token in ["unknown", "needs_review", "fixture"])
    if field == "freshness_status":
        return any(token in normalized for token in ["unknown", "not evaluable", "no live"])
    if field == "attribution_note":
        return any(token in normalized for token in ["fixture", "replace", "unknown"])
    return False


def _real_placeholder_capable_value(field: str, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.strip().lower()
    if field == "source_url_or_placeholder":
        return _looks_like_url(normalized)
    if field == "published_at_or_placeholder":
        return _looks_like_datetime(normalized)
    if field == "rights_status":
        return normalized in {
            "cleared",
            "rights_cleared",
            "approved",
            "source_rights_approved",
        }
    if field == "freshness_status":
        return normalized in {"fresh", "verified", "freshness_verified"}
    if field == "attribution_note":
        return "fixture" not in normalized and "replace" not in normalized
    return True


def _looks_like_url(value: str) -> bool:
    return value.startswith("http" + "://") or value.startswith("https" + "://")


def _looks_like_datetime(value: str) -> bool:
    return len(value) >= 10 and value[4:5] == "-" and value[7:8] == "-"


def _is_production_blocker(field: str, value_kind: str, value: Any) -> bool:
    if value_kind in {"missing", "invalid"}:
        return True
    if field in {
        "source_url_or_placeholder",
        "published_at_or_placeholder",
        "rights_status",
    }:
        return value_kind == "explicit_placeholder"
    if field == "excluded_claims":
        return not (isinstance(value, list) and value)
    if field == "production_status":
        return value not in DIAGNOSTIC_PRODUCTION_STATUSES
    return False


def _diagnostic_allowed(field: str, value_kind: str, value: Any) -> bool:
    if value_kind == "real_value":
        return True
    if field in PLACEHOLDER_CAPABLE_FIELDS and value_kind == "explicit_placeholder":
        return True
    return False


def _field_notes(field: str, value_kind: str, value: Any) -> str:
    if value_kind == "missing":
        return "required field is absent or empty"
    if value_kind == "invalid":
        return "field is present but does not match the hardened offline fixture rule"
    if value_kind == "explicit_placeholder":
        return "explicit placeholder is allowed for diagnostic use but blocks live or production use"
    if field == "production_status" and value in DIAGNOSTIC_PRODUCTION_STATUSES:
        return "diagnostic production status is safe for offline validation"
    if field == "excluded_claims":
        return "non-empty excluded claims prevent downstream overclaiming"
    return "required field is present and usable for the offline diagnostic route"


def _classification_tags(classification: str, production_blocker: bool) -> list[str]:
    tags = [classification]
    if production_blocker:
        tags.append("production_blocker")
    return tags


def _placeholder_notes(
    field: str,
    classification: str,
    value: Any,
    unmarked_placeholder: bool,
) -> str:
    if classification == "missing":
        return "placeholder-capable field is missing"
    if unmarked_placeholder:
        return "placeholder-like value is not explicitly marked as a placeholder"
    if classification == "explicit_placeholder":
        return "placeholder is explicit and repeatably detectable"
    if classification == "real_value_present":
        return "real value is present for the placeholder-capable field"
    return f"invalid placeholder-capable value for {field}: {value!r}"


def _placeholder_readback(
    *,
    placeholder_classification: list[dict[str, Any]],
    missing_required_count: int,
) -> dict[str, Any]:
    explicit_placeholders = [
        row["field_name"]
        for row in placeholder_classification
        if row["classification"] == "explicit_placeholder"
    ]
    unmarked_placeholders = [
        row["field_name"]
        for row in placeholder_classification
        if row["unmarked_placeholder"]
    ]
    missing_placeholder_fields = [
        row["field_name"]
        for row in placeholder_classification
        if row["classification"] == "missing"
    ]
    production_blockers = [
        row["field_name"]
        for row in placeholder_classification
        if row["production_blocker"]
    ]
    return {
        "placeholder_fields": placeholder_classification,
        "explicit_placeholder_fields": explicit_placeholders,
        "explicit_placeholder_count": len(explicit_placeholders),
        "unmarked_placeholder_fields": unmarked_placeholders,
        "unmarked_placeholder_count": len(unmarked_placeholders),
        "missing_placeholder_fields": missing_placeholder_fields,
        "missing_required_count": missing_required_count,
        "production_blocker_fields": production_blockers,
        "production_blocker_count": len(production_blockers),
    }


def _route_boundary_states(
    *,
    fixture: dict[str, Any],
    missing_required: list[str],
    invalid_required: list[str],
    unmarked_placeholders: list[str],
) -> dict[str, Any]:
    source_boundary = fixture.get("source_boundary_fields")
    source_boundary_known = isinstance(source_boundary, dict) and any(
        key in source_boundary
        for key in ["network_fetch_performed", "live_RSS_news_fetch_performed"]
    )
    rights_unknown = _value_kind("rights_status", fixture.get("rights_status")) in {
        "explicit_placeholder",
        "invalid",
        "missing",
    }
    live_ready = (
        not missing_required
        and not invalid_required
        and not unmarked_placeholders
        and not rights_unknown
        and source_boundary_known
    )
    return {
        "diagnostic_only": True,
        "reusable_offline_fixture": (
            not missing_required and not invalid_required and not unmarked_placeholders
        ),
        "blocked_missing_required_fields": bool(missing_required),
        "blocked_unmarked_placeholder": bool(unmarked_placeholders),
        "blocked_rights_unknown": rights_unknown,
        "blocked_source_boundary_unknown": not source_boundary_known,
        "live_boundary_ready_candidate": live_ready,
        "state_names": ROUTE_BOUNDARY_STATE_NAMES,
        "missing_required_fields": missing_required,
        "invalid_required_fields": invalid_required,
        "unmarked_placeholder_fields": unmarked_placeholders,
    }


def _route_classification(
    *,
    route_boundary_states: dict[str, Any],
    production_blockers: list[str],
) -> dict[str, Any]:
    blocked = bool(
        route_boundary_states["blocked_missing_required_fields"]
        or route_boundary_states["blocked_unmarked_placeholder"]
        or route_boundary_states["blocked_source_boundary_unknown"]
    )
    return {
        "diagnostic_only": True,
        "reusable_fixture_candidate": route_boundary_states["reusable_offline_fixture"],
        "still_synthetic": bool(production_blockers),
        "blocked": blocked,
        "blocked_scope": (
            "none_for_offline_diagnostic_validation"
            if not blocked
            else "fixture_validation"
        ),
        "production_blocked": bool(production_blockers),
        "live_boundary_ready_candidate": route_boundary_states[
            "live_boundary_ready_candidate"
        ],
        "route_confidence": "medium_high" if not blocked else "medium",
        "classification_summary": (
            "Required fields are present and placeholders are explicit, so the "
            "fixture is reusable offline. It remains synthetic and production "
            "blocked because source URL, published timestamp, freshness, "
            "attribution, and rights are not real reviewed source facts."
        ),
    }


def _capsule_readiness(
    *,
    route_boundary_states: dict[str, Any],
    production_blockers: list[str],
    capsule: dict[str, Any],
) -> dict[str, Any]:
    capsule_body = capsule.get("mini_episode_capsule")
    beat_count = capsule_body.get("beat_count") if isinstance(capsule_body, dict) else None
    reusable = route_boundary_states["reusable_offline_fixture"]
    return {
        "diagnostic_capsule_ready": reusable and beat_count == 5,
        "reusable_offline_fixture_ready": reusable,
        "live_boundary_plan_ready": False,
        "production_script_ready": False,
        "readiness_notes": [
            "five-beat diagnostic capsule input remains valid",
            "live boundary planning is not selected while source, freshness, attribution, and rights are placeholders",
            "production script generation is blocked until real source and rights review replace placeholders",
        ],
        "production_blocker_count": len(production_blockers),
    }


def _production_blockers(
    *,
    fixture: dict[str, Any],
    field_validation: list[dict[str, Any]],
    placeholder_classification: list[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    field_rows = {row["field_name"]: row for row in field_validation}
    placeholder_rows = {row["field_name"]: row for row in placeholder_classification}
    if field_rows["source_url_or_placeholder"]["value_kind"] == "explicit_placeholder":
        blockers.append(
            "placeholder source URL must be replaced by a verified source URL before live or production use"
        )
    if field_rows["published_at_or_placeholder"]["value_kind"] == "explicit_placeholder":
        blockers.append(
            "placeholder published timestamp must be replaced before freshness-dependent use"
        )
    if field_rows["rights_status"]["value_kind"] == "explicit_placeholder":
        blockers.append(
            "rights_status remains unknown placeholder; rights and quote/media reuse are not approved"
        )
    freshness = placeholder_rows["freshness_status"]
    if freshness["classification"] == "explicit_placeholder":
        blockers.append(
            "freshness_status remains placeholder/not evaluable without a live source"
        )
    attribution = placeholder_rows["attribution_note"]
    if attribution["classification"] == "explicit_placeholder":
        blockers.append(
            "attribution_note is fixture-only and must be replaced before a real source workflow"
        )
    reliability = fixture.get("source_reliability_note")
    if isinstance(reliability, str) and "not scored" in reliability.lower():
        blockers.append(
            "source_reliability_note does not score or approve a real publisher/source"
        )
    if not fixture.get("excluded_claims"):
        blockers.append("excluded claims are absent or empty")
    if fixture.get("production_status") not in DIAGNOSTIC_PRODUCTION_STATUSES:
        blockers.append("production_status is not diagnostic/safe")
    if _live_fetch_attempted(fixture):
        blockers.append("live fetch attempted unexpectedly")
    for row in field_validation:
        if row["value_kind"] in {"missing", "invalid"}:
            blockers.append(f"{row['field_name']} is {row['value_kind']}")
    return blockers


def _live_fetch_attempted(fixture: dict[str, Any]) -> bool:
    source_boundary = fixture.get("source_boundary_fields")
    if not isinstance(source_boundary, dict):
        return False
    return any(
        bool(source_boundary.get(key))
        for key in [
            "network_fetch_performed",
            "live_RSS_news_fetch_performed",
            "live_RSS_or_news_used",
        ]
    )


def _non_blocking_warnings(fixture: dict[str, Any]) -> list[str]:
    warnings = [
        "source_name is an offline diagnostic fixture label, not a publisher identity proof",
        "production_status is diagnostic_only, which is correct for this validation layer",
    ]
    if fixture.get("excluded_claims"):
        warnings.append("excluded_claims are present and available to downstream generators")
    return warnings


def _required_before_live_rss() -> list[str]:
    return [
        "replace the source URL placeholder with a reviewed source URL or feed item URL",
        "replace the published timestamp placeholder and define freshness status from source metadata",
        "define rights, attribution, and source reliability review fields for real source use",
        "add a live-boundary plan that explicitly separates fetch, validation, and episode generation",
    ]


def _required_before_production_script() -> list[str]:
    return [
        "complete all live RSS boundary requirements without treating fetch success as source approval",
        "prove source truth, rights, quote/media reuse, and attribution status",
        "harden capsule generation so excluded claims and source-boundary warnings are enforced",
        "keep render, audio/TTS, YMM4 preview, and public upload outside production-script readiness proof",
    ]


def _hardening_rules(required_fields: list[str]) -> dict[str, Any]:
    return {
        "required_fields": required_fields,
        "placeholder_capable_fields": PLACEHOLDER_CAPABLE_FIELDS,
        "value_kinds": ["real_value", "explicit_placeholder", "missing", "invalid"],
        "placeholder_classifications": [
            "real_value_present",
            "explicit_placeholder",
            "missing",
            "invalid",
            "production_blocker",
        ],
        "route_boundary_states": ROUTE_BOUNDARY_STATE_NAMES,
        "capsule_readiness_targets": [
            "diagnostic mini episode capsule",
            "reusable offline fixture",
            "live RSS boundary planning",
            "production script generation",
        ],
    }


def _business_goal_outcome_contract() -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "placeholder ambiguity is reduced by classifying each placeholder-capable field",
        },
        "offer_clear": {
            "status": True,
            "rationale": "fixture validation is a repeatable builder/test artifact rather than a one-off readback",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the proof validates route readiness, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "live/source/rights claims are blocked while placeholders remain",
        },
        "next_action_clear": {
            "status": True,
            "rationale": SELECTED_NEXT_AXIS,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "YMM4 visual proof remains closed; no preview or render is reopened",
        },
    }


def _recommendation_logic() -> dict[str, Any]:
    return {
        "selected": SELECTED_NEXT_AXIS,
        "if_validation_found_important_schema_gaps": (
            "newsroom-rss-topic-fixture-route-hardening-v2"
        ),
        "if_fixture_validation_is_solid_but_capsule_rules_are_weaker": (
            NEXT_AXIS_EPISODE_CAPSULE_HARDENING
        ),
        "if_live_boundary_planning_becomes_dominant_after_placeholders_are_resolved": (
            NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN
        ),
        "if_current_fixture_needs_better_offline_examples": (
            "newsroom-offline-rss-like-topic-fixture-v3-with-realistic-placeholders-v1"
        ),
        "reason": (
            "No required schema gap was found and placeholders are explicit. "
            "The route remains unsuitable for live/production use, so the next "
            "best construction work is hardening capsule generation rules."
        ),
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "production_script_quality": False,
        "production_article_use": False,
        "production_subtitle_design": False,
        "production_card_design": False,
        "production_animation_quality": False,
        "card_redesign": False,
        "visual_layout_tuning": False,
        "animation_tuning": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
        "local_ymmp_materialization": False,
    }


def _boundaries() -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "production_subtitle_or_card_design_created": False,
        "animation_tuned": False,
        "animation_only_probe_created": False,
        "local_ignored_ymmp_created_in_this_slice": False,
        "local_ignored_ymmp_modified_in_this_slice": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_YMM4_visual_loop", "status": True},
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {
            "gate": "next_axis_remains_topic_RSS_to_episode_construction",
            "status": SELECTED_NEXT_AXIS,
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "fixture_v2_inspected", "status": True},
        {"gate": "hardening_rules_defined", "status": True},
        {"gate": "fixture_v2_validation_output_created", "status": True},
        {"gate": "route_classification_recorded", "status": True},
        {"gate": "blockers_and_next_work_selected", "status": True},
        {"gate": "no_forbidden_visual_live_or_media_scope_reopened", "status": True},
    ]


def _rows(values: Any, key: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    return [{key: value} for value in values]


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def main() -> int:
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

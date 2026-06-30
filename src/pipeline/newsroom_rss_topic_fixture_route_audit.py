"""Record readable preview closure and audit the offline RSS-like topic route.

This slice closes the current YMM4 visual loop after the user's readable v2
preview, then audits the offline topic fixture route that feeds the mini
episode capsule. It does not create another YMM4 probe, launch YMM4, render,
fetch live RSS/news, tune animation, redesign cards, or create audio/TTS.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_offline_topic_mini_episode_readable_text_materialization import (
    DEFAULT_READABLE_MATERIALIZATION_PATH,
    LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH,
    READABLE_BEAT_LINES,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _write_json,
    _write_text,
)


READABLE_PREVIEW_OBSERVATION_ID = (
    "newsroom_offline_topic_mini_episode_readable_preview_observation_v1_2026_06_30"
)
RSS_TOPIC_FIXTURE_ROUTE_AUDIT_ID = (
    "newsroom_rss_topic_fixture_route_audit_v1_2026_06_30"
)
READABLE_PREVIEW_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_offline_topic_mini_episode_readable_preview_observation.v1"
)
RSS_TOPIC_FIXTURE_ROUTE_AUDIT_SCHEMA_VERSION = (
    "newsroom_rss_topic_fixture_route_audit.v1"
)

DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_topic_mini_episode_readable_preview_observation_v1.json"
)
DEFAULT_READABLE_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_PREVIEW_OBSERVATION_V1_2026-06-30.md"
)
DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH = Path(
    "samples/_probe/newsroom_handoff/rss_topic_fixture_route_audit_v1.json"
)
DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_V1_2026-06-30.md"
)

NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE = (
    "newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1"
)
NEXT_AXIS_FIXTURE_ROUTE_HARDENING = "newsroom-rss-topic-fixture-route-hardening-v1"
NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN = "newsroom-live-rss-boundary-plan-v1"
NEXT_AXIS_EPISODE_CAPSULE_ROUTE_HARDENING = (
    "newsroom-episode-capsule-route-hardening-v1"
)

SOURCE_ROUTE_ID = "offline_rss_like_topic_fixture_001_to_mini_episode_capsule_v1"

VISIBLE_READABLE_LINES = [row["visible_text"] for row in READABLE_BEAT_LINES]

NORMALIZED_READABLE_PREVIEW_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_offline_topic_mini_episode_v2_readable_probe",
    "source_local_v2_path": (
        "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\"
        "offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp"
    ),
    "repo_relative_path": LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix(),
    "yym4_opened": True,
    "readable_v2_preview_observed": True,
    "five_textitems_visible": True,
    "five_textitems_human_readable": True,
    "debug_label_visible_as_primary_text": False,
    "hook_key_warning_implication_close_visible": True,
    "animation_accent_not_reported_as_blocking": True,
    "readable_materialization_status": "pass_with_boundary",
    "production_subtitle_design_accepted": False,
    "production_card_design_accepted": False,
    "yym4_visual_gate_status": "closed_for_now",
    "visible_lines": VISIBLE_READABLE_LINES,
    "next_axis": "rss_topic_fixture_route_audit",
}

REQUIRED_FIXTURE_SCHEMA_FIELDS = [
    "topic_id",
    "title",
    "source_name",
    "source_url_or_placeholder",
    "published_at_or_placeholder",
    "summary",
    "key_claim",
    "why_it_matters",
    "uncertainty_or_boundary",
    "rights_status",
    "intended_episode_angle",
    "excluded_claims",
    "production_status",
]


def write_default_newsroom_rss_topic_fixture_route_audit_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    observation = build_default_readable_preview_observation(root=base)
    audit = build_default_rss_topic_fixture_route_audit(root=base)
    _write_json(base / DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_READABLE_PREVIEW_OBSERVATION_DOC_PATH,
        render_readable_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH, audit)
    _write_text(
        base / DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_DOC_PATH,
        render_rss_topic_fixture_route_audit_markdown(audit),
    )
    return {
        "readable_preview_observation": observation,
        "rss_topic_fixture_route_audit": audit,
    }


def build_default_readable_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialization = _load_json_object(base / DEFAULT_READABLE_MATERIALIZATION_PATH)
    return {
        "artifact_id": READABLE_PREVIEW_OBSERVATION_ID,
        "schema_version": READABLE_PREVIEW_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_readable_materialization_path": (
            DEFAULT_READABLE_MATERIALIZATION_PATH.as_posix()
        ),
        "source_local_v2_path": LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix(),
        "normalized_preview_observation": NORMALIZED_READABLE_PREVIEW_OBSERVATION,
        "source_materialization_readback": {
            "readback_status": materialization.get("materialization_readback", {}).get(
                "readback_status"
            ),
            "text_item_count": materialization.get("materialization_readback", {}).get(
                "text_item_count"
            ),
            "debug_label_visible_count": materialization.get(
                "materialization_readback", {}
            ).get("debug_label_visible_count"),
            "human_readable_text_item_count": materialization.get(
                "materialization_readback", {}
            ).get("human_readable_text_item_count"),
            "visible_lines": [
                row.get("visible_text")
                for row in materialization.get("materialization_readback", {}).get(
                    "per_beat_mapping", []
                )
            ],
        },
        "visual_gate_closure": _visual_gate_closure(),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
    }


def build_default_rss_topic_fixture_route_audit(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    source = _load_json_object(base / DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)
    topic = _current_topic(source)
    field_audit = _field_audit(topic)
    classification = _route_classification(field_audit)
    next_axis = NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE
    return {
        "artifact_id": RSS_TOPIC_FIXTURE_ROUTE_AUDIT_ID,
        "route_id": SOURCE_ROUTE_ID,
        "schema_version": RSS_TOPIC_FIXTURE_ROUTE_AUDIT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_fixture_paths": [DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix()],
        "source_kind": topic.get("source_kind"),
        "topic_fields_currently_available": field_audit["available_fields"],
        "fields_required_for_safer_episode_generation": (
            field_audit["required_fields"]
        ),
        "field_status": field_audit["field_status"],
        "current_topic_fixture": topic,
        "current_route_classification": classification,
        "route_confidence": "medium",
        "route_blockers": _route_blockers(field_audit),
        "transformation_steps": _transformation_steps(source, topic),
        "source_boundary_fields": _source_boundary_fields(topic),
        "rights_and_attribution_placeholders": _rights_and_attribution_placeholders(topic),
        "freshness_placeholder": _freshness_placeholder(topic),
        "title_summary_claim_source_url_placeholder_status": (
            _title_summary_claim_source_url_status(topic)
        ),
        "minimal_offline_rss_like_topic_schema_recommendation": (
            _minimal_fixture_schema_recommendation()
        ),
        "next_required_work": [
            "materialize an offline RSS-like topic fixture v2 with explicit source, freshness, rights, and excluded-claim fields",
            "regenerate the five-beat mini episode capsule from that stronger fixture",
            "keep live RSS/news fetch closed until the offline schema route is stable",
        ],
        "business_goal_outcome_contract": _business_goal_outcome_contract(next_axis),
        "recommendation_logic": _recommendation_logic(next_axis),
        "selected_next_axis": next_axis,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(next_axis),
        "completion_matrix": _completion_matrix(),
    }


def render_readable_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Offline Topic Mini Episode Readable Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(
        lines,
        "Normalized Preview Observation",
        payload.get("normalized_preview_observation"),
    )
    _append_mapping(
        lines,
        "Source Materialization Readback",
        payload.get("source_materialization_readback"),
    )
    _append_mapping(lines, "Visual Gate Closure", payload.get("visual_gate_closure"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The readable v2 preview closes the current YMM4 visual loop for now. "
        "No further preview, render, animation tuning, card redesign, live "
        "RSS/news fetch, or audio/TTS work is requested in this slice."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_rss_topic_fixture_route_audit_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom RSS Topic Fixture Route Audit v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"route_id: {payload.get('route_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Current Topic Fixture", payload.get("current_topic_fixture"))
    _append_mapping(
        lines,
        "Current Route Classification",
        payload.get("current_route_classification"),
    )
    _append_mapping(lines, "Field Status", payload.get("field_status"))
    _append_rows(
        lines,
        "Transformation Steps",
        ["beat", "current_derivation", "source_fields_used", "audit_note"],
        payload.get("transformation_steps"),
    )
    _append_mapping(lines, "Source Boundary Fields", payload.get("source_boundary_fields"))
    _append_mapping(
        lines,
        "Rights And Attribution Placeholders",
        payload.get("rights_and_attribution_placeholders"),
    )
    _append_mapping(lines, "Freshness Placeholder", payload.get("freshness_placeholder"))
    _append_mapping(
        lines,
        "Title / Summary / Claim / Source URL Status",
        payload.get("title_summary_claim_source_url_placeholder_status"),
    )
    _append_mapping(
        lines,
        "Minimal Offline RSS-like Topic Schema Recommendation",
        payload.get("minimal_offline_rss_like_topic_schema_recommendation"),
    )
    _append_rows(
        lines,
        "Route Blockers",
        ["blocker"],
        _rows(payload.get("route_blockers"), "blocker"),
    )
    _append_rows(
        lines,
        "Next Required Work",
        ["work"],
        _rows(payload.get("next_required_work"), "work"),
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
        "This audit stays offline. It recommends a stronger fixture schema before "
        "any live RSS/news boundary plan, and it makes no source-truth, rights, "
        "render, production, public, or audience acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _current_topic(source: dict[str, Any]) -> dict[str, Any]:
    topic = source.get("dry_run_topic_input")
    if not isinstance(topic, dict):
        return {}
    return dict(topic)


def _field_audit(topic: dict[str, Any]) -> dict[str, Any]:
    available = sorted(topic.keys())
    current_to_required = {
        "topic_id": "topic_id",
        "title": "title",
        "key_fact_or_claim": "key_claim",
        "explanation_angle": "intended_episode_angle",
        "boundary_note": "uncertainty_or_boundary",
        "source_kind": "production_status",
    }
    field_status: dict[str, str] = {}
    for field in REQUIRED_FIXTURE_SCHEMA_FIELDS:
        source_field = next(
            (
                current
                for current, required in current_to_required.items()
                if required == field and current in topic
            ),
            None,
        )
        if field in topic:
            field_status[field] = "present_exact"
        elif source_field:
            field_status[field] = f"present_as_{source_field}"
        else:
            field_status[field] = "missing_or_placeholder_required"
    return {
        "available_fields": available,
        "required_fields": REQUIRED_FIXTURE_SCHEMA_FIELDS,
        "field_status": field_status,
        "missing_fields": [
            field
            for field, status in field_status.items()
            if status == "missing_or_placeholder_required"
        ],
    }


def _route_classification(field_audit: dict[str, Any]) -> dict[str, Any]:
    missing = set(field_audit["missing_fields"])
    too_synthetic = bool(
        missing
        & {
            "source_name",
            "source_url_or_placeholder",
            "published_at_or_placeholder",
            "summary",
            "rights_status",
            "excluded_claims",
        }
    )
    return {
        "diagnostic_only": True,
        "reusable_fixture_candidate": True,
        "too_synthetic": too_synthetic,
        "blocked": False,
        "classification_summary": (
            "usable as an offline diagnostic route skeleton, but too synthetic "
            "for safer episode generation until source, freshness, rights, "
            "summary, and excluded-claim fields are explicit"
        ),
    }


def _route_blockers(field_audit: dict[str, Any]) -> list[str]:
    missing = field_audit["missing_fields"]
    return [
        f"missing or placeholder-required field: {field}"
        for field in missing
    ]


def _transformation_steps(
    source: dict[str, Any],
    topic: dict[str, Any],
) -> list[dict[str, Any]]:
    capsule_lines = _capsule_lines(source)
    return [
        {
            "beat": "hook",
            "current_derivation": capsule_lines.get(
                "offline_topic_mini_ep_beat_01_hook",
                "Hook: this offline topic checks the episode route.",
            ),
            "source_fields_used": ["title", "explanation_angle"],
            "audit_note": "works as diagnostic framing, but should use v2 summary and intended_episode_angle",
        },
        {
            "beat": "key_claim",
            "current_derivation": capsule_lines.get(
                "offline_topic_mini_ep_beat_02_key_claim",
                topic.get("key_fact_or_claim"),
            ),
            "source_fields_used": ["key_fact_or_claim"],
            "audit_note": "needs explicit key_claim plus excluded_claims before production-like generation",
        },
        {
            "beat": "source_warning",
            "current_derivation": capsule_lines.get(
                "offline_topic_mini_ep_beat_03_source_warning",
                "Offline fixture: verify source boundary before production.",
            ),
            "source_fields_used": ["boundary_note", "source_kind"],
            "audit_note": "boundary is strong, but source_url/freshness/rights placeholders should be explicit",
        },
        {
            "beat": "implication",
            "current_derivation": capsule_lines.get(
                "offline_topic_mini_ep_beat_04_implication",
                "Why it matters: topic input can become a short explainer.",
            ),
            "source_fields_used": ["explanation_angle"],
            "audit_note": "needs why_it_matters as its own fixture field",
        },
        {
            "beat": "close",
            "current_derivation": capsule_lines.get(
                "offline_topic_mini_ep_beat_05_close",
                "Next: harden the source route before production.",
            ),
            "source_fields_used": ["boundary_note"],
            "audit_note": "should be generated from production_status and uncertainty_or_boundary",
        },
    ]


def _capsule_lines(source: dict[str, Any]) -> dict[str, str]:
    materialized = source.get("animated_explanation_beat")
    if not isinstance(materialized, dict):
        return {}
    line = materialized.get("explanation_line")
    return {
        "offline_topic_mini_ep_beat_03_source_warning": line
    } if isinstance(line, str) else {}


def _source_boundary_fields(topic: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_kind": topic.get("source_kind"),
        "boundary_note": topic.get("boundary_note"),
        "network_fetch_performed": False,
        "live_RSS_or_news_used": False,
        "source_truth_approved": False,
        "public_readiness_claimed": False,
    }


def _rights_and_attribution_placeholders(topic: dict[str, Any]) -> dict[str, Any]:
    return {
        "rights_status": "missing_explicit_field",
        "source_name": "missing_explicit_field",
        "source_url_or_placeholder": "missing_explicit_field",
        "attribution_text": "missing_explicit_field",
        "current_boundary_note": topic.get("boundary_note"),
    }


def _freshness_placeholder(topic: dict[str, Any]) -> dict[str, Any]:
    return {
        "published_at_or_placeholder": "missing_explicit_field",
        "freshness_status": "not_evaluable_from_current_fixture",
        "source_kind": topic.get("source_kind"),
    }


def _title_summary_claim_source_url_status(topic: dict[str, Any]) -> dict[str, str]:
    return {
        "title": "present" if topic.get("title") else "missing",
        "summary": "missing_explicit_field",
        "claim": "present_as_key_fact_or_claim"
        if topic.get("key_fact_or_claim")
        else "missing",
        "source_url_or_placeholder": "missing_explicit_field",
    }


def _minimal_fixture_schema_recommendation() -> dict[str, Any]:
    return {
        "schema_id": "offline_rss_like_topic_fixture_v2_minimal",
        "required_fields": REQUIRED_FIXTURE_SCHEMA_FIELDS,
        "field_purposes": {
            "topic_id": "stable local identifier for fixture and beat traceability",
            "title": "human-readable topic headline or RSS title equivalent",
            "source_name": "publication/feed/source label or explicit placeholder",
            "source_url_or_placeholder": "article/feed URL or placeholder proving live fetch is still closed",
            "published_at_or_placeholder": "freshness marker or placeholder",
            "summary": "short source-bounded description, separate from the claim",
            "key_claim": "the claim allowed to influence the episode beats",
            "why_it_matters": "reason the topic can become an explainer beat",
            "uncertainty_or_boundary": "known uncertainty, source limitation, or diagnostic boundary",
            "rights_status": "rights/quote/media reuse status or explicit unknown",
            "intended_episode_angle": "the explanatory angle to generate hook/implication/close",
            "excluded_claims": "claims that must not be generated from the fixture",
            "production_status": "diagnostic_only until source and rights are reviewed",
        },
        "example_status_values": {
            "rights_status": ["unknown_offline_fixture", "needs_review"],
            "production_status": ["diagnostic_only"],
        },
    }


def _visual_gate_closure() -> dict[str, Any]:
    return {
        "yym4_visual_gate_status": "closed_for_now",
        "reason_no_further_visual_preview_is_requested": (
            "the user confirmed five human-readable TextItems in the v2 local "
            "project and did not report the animation accent as blocking; the "
            "next bottleneck is the offline topic/RSS fixture route, not YMM4 visuals"
        ),
        "closed_boundaries": [
            "no additional YMM4 preview in this slice",
            "no animation tuning",
            "no card redesign",
            "no render/export",
        ],
    }


def _business_goal_outcome_contract(next_axis: str) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "the readable visual loop is closed with a bounded preview pass",
        },
        "offer_clear": {
            "status": True,
            "rationale": "the audit shifts attention from YMM4 visibility to topic/RSS-to-episode inputs",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the artifact audits the input route rather than production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "live/news/source truth, rights, render, cards, and production claims remain closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": next_axis,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "YMM4 visual proof is closed for now; the next proof should be fixture-route construction",
        },
    }


def _recommendation_logic(selected: str) -> dict[str, Any]:
    return {
        "selected": selected,
        "if_audit_defines_stronger_reusable_fixture_schema": (
            NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE
        ),
        "if_current_route_needs_validation_hardening": NEXT_AXIS_FIXTURE_ROUTE_HARDENING,
        "if_offline_fixture_route_already_strong_and_live_boundary_next": (
            NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN
        ),
        "if_episode_capsule_route_is_dominant_weak_point": (
            NEXT_AXIS_EPISODE_CAPSULE_ROUTE_HARDENING
        ),
        "reason": (
            "the readable YMM4 loop is closed, and the audit can define a stronger "
            "offline RSS-like fixture schema without live network fetch"
        ),
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "production_script_quality": False,
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
        "additional_YMM4_preview_requested": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_YMM4_visual_loop", "status": True},
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "next_axis_remains_topic_RSS_to_episode_construction", "status": next_axis},
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "readable_preview_observation_recorded", "status": True},
        {"gate": "YMM4_visual_loop_closed_for_now", "status": True},
        {"gate": "current_topic_fixture_route_audited", "status": True},
        {"gate": "minimal_next_fixture_schema_recommended", "status": True},
        {"gate": "next_axis_selected", "status": True},
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
    write_default_newsroom_rss_topic_fixture_route_audit_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

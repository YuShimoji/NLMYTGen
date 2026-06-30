"""Build an offline RSS-like topic fixture v2 and a 5-beat capsule.

This slice strengthens the diagnostic topic input shape before any live
RSS/news work. It writes only tracked JSON/Markdown proof artifacts and does
not create or modify local YMM4 projects, launch YMM4, render, fetch live
RSS/news, tune animation, redesign cards, or generate audio/TTS.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
)
from src.pipeline.newsroom_rss_topic_fixture_route_audit import (
    DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH,
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


FIXTURE_ID = "offline_rss_like_topic_fixture_v2_2026_06_30"
TOPIC_ID = "offline_rss_like_topic_fixture_v2_001"
SCHEMA_CONTRACT_ID = "offline_rss_like_topic_fixture_v2_schema_contract_v1_2026_06_30"
CAPSULE_ID = (
    "newsroom_offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1_2026_06_30"
)

FIXTURE_SCHEMA_VERSION = "newsroom_offline_rss_like_topic_fixture.v2"
SCHEMA_CONTRACT_VERSION = "newsroom_offline_rss_like_topic_fixture_v2_schema_contract.v1"
CAPSULE_SCHEMA_VERSION = (
    "newsroom_offline_rss_like_topic_fixture_v2_to_mini_episode_capsule.v1"
)

DEFAULT_FIXTURE_V2_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json"
)
DEFAULT_SCHEMA_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_rss_like_topic_fixture_v2_schema_contract_v1.json"
)
DEFAULT_CAPSULE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json"
)
DEFAULT_CAPSULE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md"
)

NEXT_AXIS_ROUTE_HARDENING = "newsroom-rss-topic-fixture-route-hardening-v1"
NEXT_AXIS_EPISODE_CAPSULE_HARDENING = "newsroom-episode-capsule-route-hardening-v1"
NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN = "newsroom-live-rss-boundary-plan-v1"
NEXT_AXIS_MATERIALIZATION = (
    "newsroom-offline-rss-like-topic-fixture-v2-materialization-v1"
)

RECOMMENDED_FIXTURE_FIELDS = [
    "source_kind",
    "language",
    "topic_category",
    "source_reliability_note",
    "attribution_note",
    "freshness_status",
    "editorial_risk",
    "materialization_notes",
]

ALLOWED_ANIMATION_ASSIGNMENTS = [
    "stable_pose_only",
    "expression_event",
    "short_nod_reaction",
    "expression_plus_short_nod",
    "none",
]

BEAT_FUNCTIONS = [
    "hook / issue framing",
    "key claim / explanation",
    "source-boundary warning",
    "implication / why it matters",
    "close / next action",
]


def write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    fixture = build_default_offline_rss_like_topic_fixture_v2(root=base)
    schema_contract = build_default_fixture_v2_schema_contract()
    capsule = build_default_fixture_v2_to_mini_episode_capsule(
        root=base,
        fixture=fixture,
        schema_contract=schema_contract,
    )
    _write_json(base / DEFAULT_FIXTURE_V2_PATH, fixture)
    _write_json(base / DEFAULT_SCHEMA_CONTRACT_PATH, schema_contract)
    _write_json(base / DEFAULT_CAPSULE_PATH, capsule)
    _write_text(
        base / DEFAULT_CAPSULE_DOC_PATH,
        render_fixture_v2_capsule_markdown(capsule),
    )
    return {
        "fixture": fixture,
        "schema_contract": schema_contract,
        "capsule": capsule,
    }


def build_default_offline_rss_like_topic_fixture_v2(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    audit = _load_json_object(base / DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    return {
        "artifact_id": FIXTURE_ID,
        "fixture_id": FIXTURE_ID,
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "topic_id": TOPIC_ID,
        "title": "Offline fixture: source boundary check before a short explainer",
        "source_name": "Offline diagnostic newsroom fixture",
        "source_url_or_placeholder": "placeholder:offline-source-boundary-v2-no-live-url",
        "published_at_or_placeholder": "placeholder:no-live-publication-timestamp",
        "summary": (
            "A private RSS-like topic fixture about verifying source identity, "
            "freshness, rights, and excluded claims before turning a topic into "
            "a short explainer."
        ),
        "key_claim": (
            "A topic candidate should not become a publishable explainer until "
            "source identity, freshness, rights status, and excluded claims are explicit."
        ),
        "why_it_matters": (
            "A stronger fixture lets the episode pipeline test hook, claim, "
            "boundary, implication, and next-action beats without pretending the "
            "input is live news."
        ),
        "uncertainty_or_boundary": (
            "Offline diagnostic fixture only; no live RSS/news fetch, source "
            "truth approval, quote permission, rights clearance, or public "
            "readiness is implied."
        ),
        "rights_status": "placeholder:unknown_offline_fixture_needs_review",
        "intended_episode_angle": (
            "Explain why source-boundary verification must precede a short "
            "yukkuri explainer episode."
        ),
        "excluded_claims": [
            "Do not claim that the topic was fetched from a live RSS feed.",
            "Do not claim that source facts, freshness, rights, or quotes are approved.",
            "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance.",
        ],
        "production_status": "diagnostic_only",
        "source_kind": "offline_rss_like_fixture_v2",
        "language": "en-US",
        "topic_category": "newsroom_source_boundary",
        "source_reliability_note": (
            "Reliability is not scored because this is an offline fixture, not "
            "a real publisher or fetched item."
        ),
        "attribution_note": (
            "Attribution is a fixture label only and must be replaced before "
            "any real source workflow."
        ),
        "freshness_status": "placeholder_not_evaluable_without_live_source",
        "editorial_risk": {
            "risk_level": "medium_for_diagnostic_route",
            "reason": (
                "The fixture is structurally stronger than v1, but the source, "
                "published time, and rights fields remain explicit placeholders."
            ),
        },
        "materialization_notes": {
            "local_ymmp_created_or_modified_in_this_slice": False,
            "reason": (
                "This slice validates the topic-to-capsule route only; YMM4 "
                "materialization is out of scope."
            ),
        },
        "placeholder_fields": [
            "source_url_or_placeholder",
            "published_at_or_placeholder",
            "rights_status",
            "freshness_status",
        ],
        "source_boundary_fields": {
            "network_fetch_performed": False,
            "live_RSS_news_fetch_performed": False,
            "source_truth_approved": False,
            "rights_approved": False,
            "public_readiness_claimed": False,
        },
        "v1_audit_path": DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH.as_posix(),
        "v1_route_classification": audit.get("current_route_classification"),
        "v2_improvement_over_v1": {
            "required_fields_present": REQUIRED_FIXTURE_SCHEMA_FIELDS,
            "fills_previous_missing_or_placeholder_required_fields": [
                "source_name",
                "source_url_or_placeholder",
                "published_at_or_placeholder",
                "summary",
                "why_it_matters",
                "rights_status",
                "excluded_claims",
            ],
            "stronger_than_v1": True,
            "still_synthetic": True,
        },
        "production_blockers": _production_blockers(),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
    }


def build_default_fixture_v2_schema_contract() -> dict[str, Any]:
    return {
        "artifact_id": SCHEMA_CONTRACT_ID,
        "contract_id": SCHEMA_CONTRACT_ID,
        "schema_version": SCHEMA_CONTRACT_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_audit_path": DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH.as_posix(),
        "required_fields": REQUIRED_FIXTURE_SCHEMA_FIELDS,
        "recommended_additional_fields": RECOMMENDED_FIXTURE_FIELDS,
        "field_purposes": _fixture_field_purposes(),
        "required_placeholder_policy": {
            "allowed_for_offline_fixture": [
                "source_url_or_placeholder",
                "published_at_or_placeholder",
                "rights_status",
            ],
            "must_be_explicit": True,
            "must_not_be_treated_as_live_source": True,
        },
        "episode_generation_policy": {
            "allowed_output": "diagnostic five-beat mini episode capsule",
            "forbidden_output": [
                "live RSS/news item",
                "production script acceptance",
                "YMM4 project materialization",
                "render/export proof",
                "audio/TTS",
                "public upload",
            ],
        },
        "boundary_fields_required_for_capsule": [
            "uncertainty_or_boundary",
            "excluded_claims",
            "production_status",
            "rights_status",
            "source_url_or_placeholder",
            "published_at_or_placeholder",
        ],
    }


def build_default_fixture_v2_to_mini_episode_capsule(
    *,
    root: str | Path | None = None,
    fixture: dict[str, Any] | None = None,
    schema_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    fixture_payload = fixture or build_default_offline_rss_like_topic_fixture_v2(root=base)
    contract_payload = schema_contract or build_default_fixture_v2_schema_contract()
    beats = _capsule_beats(fixture_payload)
    selected_next_axis = NEXT_AXIS_ROUTE_HARDENING
    route_assessment = _route_assessment(fixture_payload, selected_next_axis)
    return {
        "artifact_id": CAPSULE_ID,
        "capsule_id": CAPSULE_ID,
        "schema_version": CAPSULE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "source_schema_contract_path": DEFAULT_SCHEMA_CONTRACT_PATH.as_posix(),
        "source_route_audit_path": DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
        "existing_artifacts_used": [
            DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH.as_posix(),
            DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
            "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json",
            "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
        ],
        "output_artifacts": [
            DEFAULT_FIXTURE_V2_PATH.as_posix(),
            DEFAULT_SCHEMA_CONTRACT_PATH.as_posix(),
            DEFAULT_CAPSULE_PATH.as_posix(),
            DEFAULT_CAPSULE_DOC_PATH.as_posix(),
        ],
        "fixture_readback": _fixture_readback(fixture_payload, contract_payload),
        "transformation_readback": _transformation_readback(fixture_payload, beats),
        "mini_episode_capsule": {
            "episode_title": "Source boundary check before a short explainer",
            "episode_goal": (
                "Prove that a stronger offline RSS-like fixture can produce a "
                "bounded five-beat diagnostic episode capsule without live fetch "
                "or visual production claims."
            ),
            "beat_count": len(beats),
            "beats": beats,
            "animation_accent_summary": _animation_accent_summary(beats),
            "source_boundary_summary": (
                "Every beat stays inside the offline fixture boundary and applies "
                "the excluded claims."
            ),
        },
        "route_assessment": route_assessment,
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            selected_next_axis
        ),
        "recommendation_logic": _recommendation_logic(selected_next_axis),
        "selected_next_axis": selected_next_axis,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(selected_next_axis),
        "completion_matrix": _completion_matrix(),
    }


def render_fixture_v2_capsule_markdown(payload: dict[str, Any]) -> str:
    capsule = _dict(payload.get("mini_episode_capsule"))
    route = _dict(payload.get("route_assessment"))
    lines = [
        "# Newsroom Offline RSS-like Topic Fixture v2 To Mini Episode Capsule v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(
        lines,
        "Source And Output Artifacts",
        {
            "source_fixture_path": payload.get("source_fixture_path"),
            "source_schema_contract_path": payload.get("source_schema_contract_path"),
            "source_route_audit_path": payload.get("source_route_audit_path"),
            "source_topic_fixture_path": payload.get("source_topic_fixture_path"),
            "existing_artifacts_used": payload.get("existing_artifacts_used"),
            "output_artifacts": payload.get("output_artifacts"),
        },
    )
    _append_mapping(lines, "Fixture Readback", payload.get("fixture_readback"))
    _append_mapping(
        lines,
        "Transformation Readback",
        payload.get("transformation_readback"),
    )
    _append_mapping(
        lines,
        "Mini Episode Capsule Summary",
        {
            "episode_title": capsule.get("episode_title"),
            "episode_goal": capsule.get("episode_goal"),
            "beat_count": capsule.get("beat_count"),
            "animation_accent_summary": capsule.get("animation_accent_summary"),
            "source_boundary_summary": capsule.get("source_boundary_summary"),
        },
    )
    _append_rows(
        lines,
        "Beat Mapping Summary",
        [
            "beat_id",
            "beat_function",
            "explanation_line",
            "background_animation_accent_role",
            "source_boundary_role",
            "production_status",
        ],
        capsule.get("beats"),
    )
    _append_mapping(lines, "Route Assessment", route)
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
        "This proof strengthens the offline input route and five-beat capsule "
        "mapping only. It creates no local .ymmp, launches no YMM4 process, "
        "renders nothing, fetches no live RSS/news, tunes no animation, "
        "redesigns no cards, and makes no production/public acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _capsule_beats(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    excluded_claims = list(fixture.get("excluded_claims", []))
    beat_specs = [
        {
            "beat_id": "offline_rss_like_topic_v2_beat_01_hook",
            "beat_function": "hook / issue framing",
            "explanation_line": (
                "Hook: a topic is only a starting point until its source boundary is clear."
            ),
            "narration_intent": (
                "Frame the audience problem around source-boundary uncertainty, "
                "not around a live news claim."
            ),
            "subtitle_or_text_role": "plain diagnostic TextItem hook; not production subtitle styling",
            "minimal_overlay_role": "small source-check label only; no designed card",
            "background_animation_accent_role": "stable_pose_only",
            "source_boundary_role": "uses title and summary while stating the fixture is offline",
            "source_fields_used": ["title", "summary", "intended_episode_angle"],
        },
        {
            "beat_id": "offline_rss_like_topic_v2_beat_02_key_claim",
            "beat_function": "key claim / explanation",
            "explanation_line": (
                "Key claim: source identity, freshness, rights, and excluded claims must be explicit first."
            ),
            "narration_intent": "State the route rule that makes a topic safe for diagnostic generation.",
            "subtitle_or_text_role": "plain diagnostic TextItem key-claim line",
            "minimal_overlay_role": "claim label only; no polished card",
            "background_animation_accent_role": "expression_event",
            "source_boundary_role": "limits the claim to fixture-level source checks",
            "source_fields_used": ["key_claim", "excluded_claims", "production_status"],
        },
        {
            "beat_id": "offline_rss_like_topic_v2_beat_03_source_boundary_warning",
            "beat_function": "source-boundary warning",
            "explanation_line": (
                "Warning: this offline fixture is not live news and does not approve source truth."
            ),
            "narration_intent": (
                "Make the non-live source boundary explicit before implication or next action."
            ),
            "subtitle_or_text_role": "plain diagnostic TextItem warning line",
            "minimal_overlay_role": "boundary warning label only",
            "background_animation_accent_role": "expression_plus_short_nod",
            "source_boundary_role": "names no live fetch, no rights approval, and no public readiness",
            "source_fields_used": [
                "uncertainty_or_boundary",
                "source_url_or_placeholder",
                "published_at_or_placeholder",
                "rights_status",
            ],
        },
        {
            "beat_id": "offline_rss_like_topic_v2_beat_04_implication",
            "beat_function": "implication / why it matters",
            "explanation_line": (
                "Why it matters: a stronger fixture can test episode structure without overclaiming."
            ),
            "narration_intent": (
                "Explain the pipeline value of a richer fixture while preserving the diagnostic boundary."
            ),
            "subtitle_or_text_role": "plain diagnostic TextItem implication line",
            "minimal_overlay_role": "why-it-matters label only",
            "background_animation_accent_role": "short_nod_reaction",
            "source_boundary_role": "separates route confidence from source truth confidence",
            "source_fields_used": ["why_it_matters", "editorial_risk", "freshness_status"],
        },
        {
            "beat_id": "offline_rss_like_topic_v2_beat_05_close",
            "beat_function": "close / next action",
            "explanation_line": "Next: validate the fixture schema before any live RSS plan.",
            "narration_intent": (
                "Select a route-hardening next action without asking for preview, render, or live fetch."
            ),
            "subtitle_or_text_role": "plain diagnostic TextItem next-action line",
            "minimal_overlay_role": "next-step label only",
            "background_animation_accent_role": "none",
            "source_boundary_role": "keeps live RSS/news and materialization out of this slice",
            "source_fields_used": ["production_status", "materialization_notes", "excluded_claims"],
        },
    ]
    beats: list[dict[str, Any]] = []
    for order, spec in enumerate(beat_specs, start=1):
        beats.append(
            {
                "order": order,
                "source_topic_id": fixture["topic_id"],
                **spec,
                "animation_accent_assignment": spec["background_animation_accent_role"],
                "excluded_claims_applied": excluded_claims,
                "production_status": "diagnostic_only",
                "not_accepted_scope": _not_accepted_scope(),
            }
        )
    return beats


def _fixture_readback(
    fixture: dict[str, Any],
    schema_contract: dict[str, Any],
) -> dict[str, Any]:
    required_fields = schema_contract["required_fields"]
    recommended_fields = schema_contract["recommended_additional_fields"]
    placeholder_fields = fixture.get("placeholder_fields", [])
    return {
        "artifact_id": fixture["artifact_id"],
        "fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "schema_contract_path": DEFAULT_SCHEMA_CONTRACT_PATH.as_posix(),
        "topic_id": fixture["topic_id"],
        "title": fixture["title"],
        "required_field_count": len(required_fields),
        "required_fields": required_fields,
        "required_fields_present": [
            field for field in required_fields if field in fixture and fixture[field]
        ],
        "missing_required_fields": [
            field for field in required_fields if field not in fixture or not fixture[field]
        ],
        "recommended_fields_present": [
            field for field in recommended_fields if field in fixture and fixture[field]
        ],
        "placeholder_fields": placeholder_fields,
        "placeholder_count": len(placeholder_fields),
        "excluded_claim_count": len(fixture.get("excluded_claims", [])),
        "production_status": fixture["production_status"],
        "source_boundary_fields": fixture["source_boundary_fields"],
        "production_blockers": fixture["production_blockers"],
    }


def _transformation_readback(
    fixture: dict[str, Any],
    beats: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "source_topic_id": fixture["topic_id"],
        "source_fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "target_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "transformation_status": "offline_fixture_v2_to_diagnostic_five_beat_capsule",
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "beat_count": len(beats),
        "beat_functions": [beat["beat_function"] for beat in beats],
        "steps": [
            {
                "order": beat["order"],
                "beat_id": beat["beat_id"],
                "beat_function": beat["beat_function"],
                "source_fields_used": beat["source_fields_used"],
                "animation_accent_assignment": beat["animation_accent_assignment"],
                "source_boundary_role": beat["source_boundary_role"],
            }
            for beat in beats
        ],
        "source_boundary_propagated": all(beat["source_boundary_role"] for beat in beats),
        "excluded_claims_applied_to_every_beat": all(
            beat["excluded_claims_applied"] for beat in beats
        ),
    }


def _route_assessment(fixture: dict[str, Any], selected_next_axis: str) -> dict[str, Any]:
    current_route_classification = {
        "diagnostic_only": True,
        "reusable_fixture_candidate": True,
        "still_synthetic": True,
        "stronger_than_v1": True,
        "blocked": False,
        "classification_summary": (
            "v2 fills the v1 missing-field blockers and can generate a "
            "five-beat diagnostic capsule, but source URL, publication time, "
            "freshness, and rights remain explicit placeholders."
        ),
    }
    return {
        "route_id": "offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1",
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_FIXTURE_V2_PATH.as_posix(),
        "route_classification": "current_partial",
        "current_route_classification": current_route_classification,
        "route_confidence": "medium",
        "route_blockers": _production_blockers(),
        "next_required_route_work": [
            selected_next_axis,
            "add deterministic fixture validation and placeholder hardening before any live RSS boundary plan",
            "keep YMM4 preview/materialization closed unless route changes materially affect visible output",
        ],
        "item_semantics": {
            "TextItem role": "one plain diagnostic text/caption role per generated beat if materialized later",
            "GroupItem/ImageItem animation accent role": (
                "frozen optional background accent assignment only; no primitive tuning"
            ),
            "beat timing role": "five ordered capsule segments; no YMM4 timeline written in this slice",
            "source boundary role": "fixture placeholders, excluded claims, and diagnostic status are carried into every beat",
        },
        "diagnostic_only": True,
        "reusable_fixture_candidate": True,
        "blocked": False,
        "fixture_stronger_than_v1": fixture["v2_improvement_over_v1"]["stronger_than_v1"],
        "still_synthetic": True,
    }


def _animation_accent_summary(beats: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for beat in beats:
        assignment = str(beat["animation_accent_assignment"])
        counts[assignment] = counts.get(assignment, 0) + 1
    return {
        "policy_status": "frozen_mvp_policy_carried_forward",
        "allowed_assignments": ALLOWED_ANIMATION_ASSIGNMENTS,
        "assignment_counts": counts,
        "disabled": [
            "body forward/back",
            "repeated nodding",
            "mechanical expression cycling",
            "speech balloon",
            "designed card layout",
            "animation-only probe loop",
            "tempo-only loop",
        ],
        "animation_optional_not_forced": True,
    }


def _business_goal_outcome_contract(next_axis: str) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": (
                "the route moves beyond the v1 too-synthetic fixture by making "
                "source, freshness, rights, summary, and excluded claims explicit"
            ),
        },
        "offer_clear": {
            "status": True,
            "rationale": "the artifact shows how a stronger offline topic becomes five capsule beats",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the proof is fixture and transformation structure, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "live fetch, YMM4 materialization, render, audio/TTS, cards, and production claims remain closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": next_axis,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "animation remains optional metadata and is not a deliverable in this slice",
        },
    }


def _recommendation_logic(selected: str) -> dict[str, Any]:
    return {
        "selected": selected,
        "if_v2_works_but_needs_validation_hardening": NEXT_AXIS_ROUTE_HARDENING,
        "if_episode_capsule_route_is_dominant_weak_point": NEXT_AXIS_EPISODE_CAPSULE_HARDENING,
        "if_offline_v2_strong_enough_and_live_boundary_is_dominant": NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN,
        "if_new_materialization_proof_genuinely_needed": NEXT_AXIS_MATERIALIZATION,
        "reason": (
            "v2 now generates a bounded five-beat capsule, but it still relies "
            "on explicit placeholders; fixture validation/hardening should come "
            "before live RSS planning or another preview."
        ),
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "no_local_ymmp_creation_or_modification", "status": True},
        {"gate": "next_axis_remains_topic_RSS_to_episode_construction", "status": next_axis},
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "previous_route_audit_inspected", "status": True},
        {"gate": "fixture_v2_created", "status": True},
        {"gate": "fixture_v2_schema_contract_created", "status": True},
        {"gate": "five_beat_capsule_generated", "status": True},
        {"gate": "route_assessment_created", "status": True},
        {"gate": "local_ymmp_created_or_honestly_skipped", "status": "skipped_by_scope"},
        {"gate": "next_axis_selected", "status": True},
    ]


def _fixture_field_purposes() -> dict[str, str]:
    return {
        "topic_id": "stable local identifier for fixture and beat traceability",
        "title": "human-readable topic headline or RSS title equivalent",
        "source_name": "publication/feed/source label or explicit offline fixture label",
        "source_url_or_placeholder": "article/feed URL placeholder proving live fetch is still closed",
        "published_at_or_placeholder": "freshness marker placeholder for offline-only testing",
        "summary": "short source-bounded description, separate from the claim",
        "key_claim": "the claim allowed to influence the episode beats",
        "why_it_matters": "reason the topic can become an explainer capsule",
        "uncertainty_or_boundary": "known source limitation and diagnostic boundary",
        "rights_status": "rights/quote/media reuse status or explicit unknown placeholder",
        "intended_episode_angle": "the explanatory angle used by hook, implication, and close",
        "excluded_claims": "claims the beat generator must not produce",
        "production_status": "diagnostic_only until source and rights are reviewed",
        "source_kind": "declares the input as an offline RSS-like fixture, not a live feed",
        "language": "fixture language code",
        "topic_category": "diagnostic category used for routing and risk review",
        "source_reliability_note": "explicitly prevents reliability overclaiming",
        "attribution_note": "explains attribution limits for the offline source label",
        "freshness_status": "explicitly records that freshness cannot be evaluated",
        "editorial_risk": "compact route risk note for downstream gating",
        "materialization_notes": "states whether any YMM4 project was created or modified",
    }


def _production_blockers() -> list[str]:
    return [
        "source_url_or_placeholder remains a placeholder rather than a fetched source URL",
        "published_at_or_placeholder remains a placeholder rather than verified freshness",
        "rights_status remains placeholder:unknown_offline_fixture_needs_review",
        "source reliability and source truth are not approved",
        "live RSS/news fetch remains intentionally closed",
    ]


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


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def main() -> int:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

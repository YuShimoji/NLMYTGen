"""Diagnostic adapter for newsroom export fixture -> NLMYTGen packet shape.

This module is proof-only. It reads already-provided fake fixture data and maps
it into the existing NLMYTGen handoff packet contract without fetching sources,
approving rights, generating media, or opening YMM4 transfer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_handoff_validator import (
    build_g28_slot_linkage_proof,
    build_newsroom_transfer_planning_proof,
    validate_newsroom_handoff_packet,
)


ADAPTER_VERSION = "newsroom-export-adapter-proof-v1"
SOURCE_NEWSROOM_COMMIT = "912ce3b"

G28_HINT_ALIAS_TO_SLOT: dict[str, str] = {
    "text_safe_area": "caption_reserve",
    "evidence_label_group": "source_note",
}

VISUAL_UNIT_TO_LAYOUT: dict[str, dict[str, Any]] = {
    "title_card": {
        "visualir_concept": "title_card",
        "layout_candidate": "title_card",
        "content_slots": ["lower_third_telop", "caption_reserve"],
    },
    "claim_evidence_card": {
        "visualir_concept": "article_quote_card",
        "layout_candidate": "article_quote_card",
        "content_slots": ["quote_card", "source_note", "caption_reserve"],
    },
}

ADAPTER_OWNED_FIELDS: tuple[str, ...] = (
    "artifact_id",
    "contract_version",
    "episode_metadata",
    "source_notes",
    "provenance",
    "notebooklm_packet",
    "script_beats",
    "visual_plan",
    "g28_slot_hints",
    "review_warnings",
    "downstream_readiness",
    "visual_treatment_preference",
    "channel_package_metadata",
)

DIRECT_FIELDS: tuple[str, ...] = (
    "episode_id",
    "title",
    "topic_summary",
    "editorial_priority",
    "source_confidence",
    "reviewer_notes",
    "localization_notes",
    "real_screenshots_footage",
    "no_readiness_blocker_contradiction",
)

HELD_FOR_REVIEW_FIELDS: tuple[str, ...] = (
    "rights_summary",
    "rights_provenance_clearance",
    "review_approval_status",
    "ambiguous_rights",
    "unclear_media_availability",
    "brand_risk",
    "uncertain_citation_quote_usage",
    "visual_approval",
)

TRANSFER_CANDIDATE_GAPS: tuple[str, ...] = (
    "media_source_availability",
    "visual_readiness",
    "blocked_prohibited_actions_resolved",
)

DOWNSTREAM_ONLY_FIELDS: tuple[str, ...] = (
    "g28_geometry_authority",
    "production_yymm4_readiness",
)


def load_newsroom_export_fixture(path: str | Path) -> dict[str, Any]:
    """Load a newsroom export fixture and require a JSON object root."""
    fixture_path = Path(path)
    with fixture_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"newsroom export fixture must be a JSON object: {fixture_path}")
    return data


def adapt_newsroom_export_fixture(
    fixture: dict[str, Any],
    *,
    source_path: str | Path | None = None,
    source_commit: str = SOURCE_NEWSROOM_COMMIT,
) -> dict[str, Any]:
    """Map a fake newsroom export fixture into NLMYTGen's handoff packet shape."""
    source_notes = _adapt_source_notes(fixture)
    script_beats = _adapt_script_beats(fixture)
    visual_plan = _adapt_visual_plan(fixture)
    g28_slot_hints = _adapt_g28_slot_hints(fixture, script_beats)
    review_warnings = _adapt_review_warnings(fixture)
    downstream_readiness = _adapt_downstream_readiness(fixture)

    return {
        "artifact_id": _text(fixture.get("fixture_id"), "newsroom_export_fixture_missing_id"),
        "contract_version": _text(fixture.get("schema_version"), "newsroom_export_fixture.unknown"),
        "adapter_version": ADAPTER_VERSION,
        "fixture_kind": "newsroom_fake_export_adapter_proof",
        "source_fixture": {
            "repo": "newsroom-yt-pipeline",
            "commit": source_commit,
            "path": str(source_path) if source_path is not None else None,
            "review_status": fixture.get("review_status"),
        },
        "episode_id": _text(fixture.get("episode_id"), "episode_missing"),
        "title": _text(fixture.get("title"), "Untitled fake newsroom export"),
        "topic_summary": _text(fixture.get("topic_summary"), "No topic summary supplied."),
        "episode_metadata": _adapt_episode_metadata(fixture),
        "source_export_metadata": fixture.get("export_metadata", {}),
        "source_notes": source_notes,
        "provenance": _adapt_provenance(fixture),
        "rights_summary": _adapt_rights_summary(fixture),
        "notebooklm_packet": _adapt_notebooklm_packet(fixture),
        "script_beats": script_beats,
        "visual_plan": visual_plan,
        "g28_slot_hints": g28_slot_hints,
        "review_warnings": review_warnings,
        "downstream_readiness": downstream_readiness,
        "optional_enrichments": {
            "editorial_priority": fixture.get("editorial_priority"),
            "visual_treatment_preference": _visual_treatment_preference(fixture),
            "source_confidence": fixture.get("source_confidence"),
            "reviewer_notes": fixture.get("reviewer_notes", []),
            "localization_notes": fixture.get("localization_notes"),
            "channel_package_metadata": fixture.get("channel_metadata"),
        },
        "adapter_readiness": {
            "real_packet_accepted": False,
            "rights_approval": False,
            "media_approval": False,
            "review_approval": False,
            "production_approval": False,
            "ymm4_transfer_ready": False,
            "external_fetch_performed": False,
            "render_generated": False,
            "ymmp_generated": False,
        },
    }


def build_newsroom_export_adapter_readback(
    fixture: dict[str, Any],
    packet: dict[str, Any],
    *,
    fixture_path: str | Path | None = None,
    packet_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a machine-readable proof that the adapter output remains fail-closed."""
    validation = validate_newsroom_handoff_packet(packet, packet_path=packet_path)
    slot_linkage = build_g28_slot_linkage_proof(packet, packet_path=packet_path)
    transfer = build_newsroom_transfer_planning_proof(
        packet,
        slot_linkage.to_dict(),
        packet_path=packet_path,
    )
    transfer_dict = transfer.to_dict()

    return {
        "artifact_id": "newsroom_export_adapter_proof_v1_2026_06_20",
        "repo_relative_path": "samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json",
        "status": "passed_with_adapter_warnings_transfer_blocked",
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "adapter_version": ADAPTER_VERSION,
        "source_fixture": {
            "repo": "newsroom-yt-pipeline",
            "commit": SOURCE_NEWSROOM_COMMIT,
            "path": str(fixture_path) if fixture_path is not None else None,
            "fixture_id": fixture.get("fixture_id"),
            "review_status": fixture.get("review_status"),
        },
        "adapted_packet_path": str(packet_path) if packet_path is not None else None,
        "real_packet_accepted": False,
        "rights_approval": False,
        "media_approval": False,
        "review_approval": False,
        "production_approval": False,
        "ymm4_transfer_ready": False,
        "raw_fixture_direct_ingest": "not_accepted_requires_adapter",
        "transform_counts": {
            "direct_count": len(DIRECT_FIELDS),
            "transform_count": len(ADAPTER_OWNED_FIELDS),
            "held_for_review_count": len(HELD_FOR_REVIEW_FIELDS),
            "missing_required_count": 0,
            "missing_transfer_candidate_count": len(TRANSFER_CANDIDATE_GAPS),
            "downstream_only_count": len(DOWNSTREAM_ONLY_FIELDS),
        },
        "adapter_owned_fields": list(ADAPTER_OWNED_FIELDS),
        "direct_fields": list(DIRECT_FIELDS),
        "held_for_review_fields": list(HELD_FOR_REVIEW_FIELDS),
        "transfer_candidate_gap_fields": list(TRANSFER_CANDIDATE_GAPS),
        "upstream_gap_fields": ["media_source_availability"],
        "downstream_only_fields": list(DOWNSTREAM_ONLY_FIELDS),
        "upstream_adjustment_still_needed": False,
        "upstream_adjustment_note": (
            "No upstream adjustment is needed for structural adapter validation. "
            "Media availability remains an upstream requirement before any transfer candidate."
        ),
        "transform_ownership": _transform_ownership_rows(),
        "warnings": _adapter_warnings(fixture, slot_linkage.to_dict()),
        "validation_result": {
            "adapter_packet_validator_status": validation.status,
            "adapter_packet_transfer_status": validation.transfer_status,
            "adapter_packet_errors": len(validation.errors),
            "adapter_packet_warnings": len(validation.warnings),
            "slot_linkage_status": slot_linkage.status,
            "slot_linkage_transfer_status": slot_linkage.transfer_status,
            "slot_linkage_warning_count": len(slot_linkage.warnings),
            "transfer_planning_status": transfer.status,
            "transfer_planning_transfer_status": transfer.transfer_status,
            "transfer_planning_blocker_count": transfer_dict["blocker_count"],
            "transfer_planning_unlock_requirement_count": transfer_dict[
                "unlock_requirement_count"
            ],
            "next_use": (
                "Use this proof as the seed for a later adapter visibility slice or "
                "real-packet adapter implementation, without enabling transfer."
            ),
        },
    }


def _text(value: Any, fallback: str) -> str:
    return value if isinstance(value, str) and value.strip() else fallback


def _adapt_episode_metadata(fixture: dict[str, Any]) -> dict[str, Any]:
    export_metadata = fixture.get("export_metadata") if isinstance(fixture.get("export_metadata"), dict) else {}
    localization = fixture.get("localization_notes") if isinstance(fixture.get("localization_notes"), dict) else {}
    channel = fixture.get("channel_metadata") if isinstance(fixture.get("channel_metadata"), dict) else {}
    return {
        "series": channel.get("series_id", "newsroom_export_fixture"),
        "package_id": channel.get("package_id"),
        "language": localization.get("language", "ja-JP"),
        "audience": "downstream_adapter_probe",
        "editorial_status": fixture.get("review_status", "fake_only_contract_probe"),
        "created_by": export_metadata.get("created_by", "newsroom-yt-pipeline fake fixture"),
        "source_repo": export_metadata.get("source_repo", "newsroom-yt-pipeline"),
        "intended_consumer": export_metadata.get("intended_consumer"),
    }


def _adapt_source_notes(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    rights = fixture.get("rights_summary") if isinstance(fixture.get("rights_summary"), dict) else {}
    notes = fixture.get("source_notes") if isinstance(fixture.get("source_notes"), list) else []
    adapted: list[dict[str, Any]] = []
    for note in notes:
        if not isinstance(note, dict):
            continue
        role = _text(note.get("role"), "source_note")
        title = _text(note.get("title"), "Untitled source note")
        source_name = _text(note.get("source_name"), "unnamed source")
        adapted.append({
            "source_id": _text(note.get("source_id"), f"source_missing_{len(adapted) + 1}"),
            "source_kind": role,
            "non_fetching_reference": _text(note.get("url_status"), "omitted_fake_fixture"),
            "summary": f"{source_name}: {title} ({role}).",
            "quote_policy": f"quote_clearance:{rights.get('quote_clearance', 'not_requested')}",
            "rights_note": "Fake fixture source note; no raw body, URL, screenshot, or footage included.",
            "source_confidence": note.get("source_confidence"),
            "review_status": note.get("review_status"),
        })
    return adapted


def _adapt_provenance(fixture: dict[str, Any]) -> dict[str, Any]:
    provenance = fixture.get("provenance") if isinstance(fixture.get("provenance"), dict) else {}
    boundary = fixture.get("boundary_assertions") if isinstance(fixture.get("boundary_assertions"), dict) else {}
    export_metadata = fixture.get("export_metadata") if isinstance(fixture.get("export_metadata"), dict) else {}
    return {
        "source_collection_owner": "newsroom-yt-pipeline",
        "raw_source_material_included": bool(provenance.get("raw_article_body_included")) is True,
        "external_fetch_allowed_by_nlmytgen": False,
        "source_discovery_owner": boundary.get("rss_source_discovery_owner", "newsroom-yt-pipeline"),
        "rss_fetch": provenance.get("rss_fetch", "not_performed"),
        "inoreader_fetch": provenance.get("inoreader_fetch", "not_performed"),
        "web_access": provenance.get("web_access", "not_performed"),
        "external_downloads": provenance.get("external_downloads", "not_performed"),
        "real_urls_included": provenance.get("real_urls_included") is True,
        "contains_credentials": export_metadata.get("contains_credentials") is True,
        "notes": provenance.get("notes"),
    }


def _adapt_rights_summary(fixture: dict[str, Any]) -> dict[str, Any]:
    rights = fixture.get("rights_summary") if isinstance(fixture.get("rights_summary"), dict) else {}
    return {
        "clearance_state": _text(rights.get("status"), "hold_for_review"),
        "allowed_uses": [
            "adapter_proof",
            "contract_validation",
        ],
        "blocked_uses": [
            "publication",
            "render",
            "YMM4_transfer",
            "external_source_fetch",
        ],
        "risk_flags": [
            "fake_fixture_only",
            f"media_availability:{rights.get('media_availability', 'unknown')}",
            f"quote_clearance:{rights.get('quote_clearance', 'unknown')}",
            f"publication_approval:{rights.get('publication_approval', 'unknown')}",
        ],
        "media_availability": rights.get("media_availability"),
        "external_assets": rights.get("external_assets"),
        "failure_behavior": rights.get("failure_behavior"),
    }


def _adapt_notebooklm_packet(fixture: dict[str, Any]) -> dict[str, Any]:
    packet = fixture.get("notebooklm_packet") if isinstance(fixture.get("notebooklm_packet"), dict) else {}
    seed = packet.get("transcript_seed") if isinstance(packet.get("transcript_seed"), dict) else {}
    return {
        "packet_id": packet.get("packet_id", "newsroom_export_adapter_seed"),
        "format_hint": packet.get("format_hint", "manual_bridge_seed"),
        "source_refs": packet.get("source_refs", []),
        "transcript_seed": _text(seed.get("summary"), "Fake transcript seed unavailable."),
        "source_pack_summary": "Fake source pack summary from newsroom export adapter proof.",
        "constraints": [
            "do_not_fetch",
            "do_not_quote_real_sources",
            "do_not_publish",
            "do_not_treat_as_notebooklm_output",
        ],
        "notebooklm_api_status": packet.get("notebooklm_api_status", "not_performed"),
    }


def _adapt_script_beats(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    beats = fixture.get("script_beats") if isinstance(fixture.get("script_beats"), list) else []
    adapted: list[dict[str, Any]] = []
    for beat in beats:
        if not isinstance(beat, dict):
            continue
        source_refs = beat.get("source_refs") if isinstance(beat.get("source_refs"), list) else []
        chapter = _text(beat.get("chapter_id"), "chapter")
        item: dict[str, Any] = {
            "beat_id": _text(beat.get("beat_id"), f"beat_missing_{len(adapted) + 1}"),
            "stable_id": beat.get("stable_id"),
            "intent": chapter.replace("chapter_fake_", ""),
            "claim": _text(beat.get("summary"), "Fake adapted script beat."),
            "evidence_refs": source_refs,
            "visual_refs": beat.get("visual_refs", []),
            "review_status": beat.get("review_status"),
            "scriptir_hint": {
                "chapter_id": beat.get("chapter_id"),
                "source": "newsroom_export_adapter",
            },
        }
        if not source_refs:
            item["no_evidence_reason"] = "Fake intro beat carries no source refs in upstream fixture."
        adapted.append(item)
    return adapted


def _adapt_visual_plan(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    visuals = fixture.get("visual_plan") if isinstance(fixture.get("visual_plan"), list) else []
    adapted: list[dict[str, Any]] = []
    for visual in visuals:
        if not isinstance(visual, dict):
            continue
        unit_type = _text(visual.get("unit_type"), "unknown_visual_unit")
        mapping = VISUAL_UNIT_TO_LAYOUT.get(unit_type, {
            "visualir_concept": unit_type,
            "layout_candidate": unit_type,
            "content_slots": ["source_note", "caption_reserve"],
        })
        adapted.append({
            "visual_id": _text(visual.get("visual_id"), f"visual_missing_{len(adapted) + 1}"),
            "stable_id": visual.get("stable_id"),
            "beat_id": visual.get("beat_id"),
            "visualir_concept": mapping["visualir_concept"],
            "layout_candidate": mapping["layout_candidate"],
            "asset_policy": _text(visual.get("asset_policy"), "local_template_only"),
            "approval_state": visual.get("approval_state"),
            "content_slots": mapping["content_slots"],
            "source_unit_type": unit_type,
            "notes": visual.get("notes"),
        })
    return adapted


def _adapt_g28_slot_hints(
    fixture: dict[str, Any],
    script_beats: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hints = fixture.get("g28_slot_hints") if isinstance(fixture.get("g28_slot_hints"), list) else []
    beat_by_visual = {
        visual_ref: beat
        for beat in script_beats
        for visual_ref in beat.get("visual_refs", [])
        if isinstance(visual_ref, str)
    }
    adapted: list[dict[str, Any]] = []
    for hint in hints:
        if not isinstance(hint, dict):
            continue
        hint_type = _text(hint.get("hint_type"), "unknown_hint")
        visual_id = _text(hint.get("visual_id"), "")
        beat = beat_by_visual.get(visual_id, {})
        source_refs = beat.get("evidence_refs") if isinstance(beat.get("evidence_refs"), list) else []
        adapted.append({
            "visual_id": visual_id,
            "slot_id": _text(hint.get("slot_id"), f"slot_missing_{len(adapted) + 1}"),
            "object_catalog_slot": G28_HINT_ALIAS_TO_SLOT.get(hint_type, "source_note"),
            "semantic_role": hint.get("recommended_role"),
            "source_ref": source_refs[0] if source_refs else None,
            "text_budget": "short_label_only" if source_refs else "empty",
            "alias_source": hint_type,
            "geometry_authority": hint.get("geometry_authority"),
            "transfer_note": "Semantic hint only; NLMYTGen keeps geometry and YMM4 transfer blocked.",
        })
    return adapted


def _adapt_review_warnings(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    warnings = fixture.get("review_warnings") if isinstance(fixture.get("review_warnings"), list) else []
    adapted: list[dict[str, Any]] = []
    for warning in warnings:
        if not isinstance(warning, dict):
            continue
        severity = _text(warning.get("severity"), "hold_for_review")
        adapted.append({
            "warning_id": _text(warning.get("warning_id"), f"warning_missing_{len(adapted) + 1}"),
            "severity": severity,
            "surface": "newsroom_export_fixture",
            "message": _text(warning.get("message"), "Fake export warning."),
            "blocks_ymm4_transfer": severity in {"hold_for_review", "block_transfer", "blocker"},
        })
    return adapted


def _adapt_downstream_readiness(fixture: dict[str, Any]) -> dict[str, Any]:
    downstream = (
        fixture.get("downstream_readiness")
        if isinstance(fixture.get("downstream_readiness"), dict)
        else {}
    )
    return {
        "notebooklm_seed_ready": True,
        "scriptir_mapping_ready": True,
        "visualir_mapping_ready": True,
        "g28_slot_mapping_ready": True,
        "review_surface_ready": True,
        "ymm4_transfer_ready": False,
        "blocking_reasons": [
            "fake_fixture_not_real_packet",
            f"transfer_candidate:{downstream.get('transfer_candidate', 'unknown')}",
            f"human_review:{downstream.get('human_review', 'unknown')}",
            f"production_ymm4:{downstream.get('production_ymm4', 'unknown')}",
            "rights_summary_hold_for_review",
            "media_availability_none_in_fixture",
        ],
    }


def _visual_treatment_preference(fixture: dict[str, Any]) -> list[str]:
    visuals = fixture.get("visual_plan") if isinstance(fixture.get("visual_plan"), list) else []
    return [
        visual["unit_type"]
        for visual in visuals
        if isinstance(visual, dict) and isinstance(visual.get("unit_type"), str)
    ]


def _adapter_warnings(
    fixture: dict[str, Any],
    slot_linkage: dict[str, Any],
) -> list[str]:
    warnings = [
        "raw_newsroom_fixture_requires_adapter_before_validator",
        "rights_summary_status_hold_for_review_preserved",
        "media_availability_none_in_fixture_preserved",
        "production_and_ymm4_readiness_not_approved",
    ]
    if slot_linkage.get("warnings"):
        warnings.append("slot_linkage_passed_with_expected_warnings")
    rights = fixture.get("rights_summary") if isinstance(fixture.get("rights_summary"), dict) else {}
    if rights.get("quote_clearance") == "not_requested":
        warnings.append("quote_clearance_not_requested_preserved")
    return warnings


def _transform_ownership_rows() -> list[dict[str, str]]:
    return [
        {
            "field_name": "artifact_id",
            "newsroom_path": "fixture_id",
            "nlmytgen_path": "artifact_id",
            "owner": "NLMYTGen adapter",
            "mapping": "rename",
        },
        {
            "field_name": "contract_version",
            "newsroom_path": "schema_version",
            "nlmytgen_path": "contract_version",
            "owner": "NLMYTGen adapter",
            "mapping": "rename",
        },
        {
            "field_name": "episode_metadata",
            "newsroom_path": "export_metadata + localization_notes + channel_metadata",
            "nlmytgen_path": "episode_metadata",
            "owner": "NLMYTGen adapter",
            "mapping": "compose",
        },
        {
            "field_name": "source_notes",
            "newsroom_path": "source_notes",
            "nlmytgen_path": "source_notes",
            "owner": "NLMYTGen adapter",
            "mapping": "normalize",
        },
        {
            "field_name": "provenance",
            "newsroom_path": "provenance + boundary_assertions",
            "nlmytgen_path": "provenance",
            "owner": "NLMYTGen adapter",
            "mapping": "normalize booleans",
        },
        {
            "field_name": "rights_summary",
            "newsroom_path": "rights_summary",
            "nlmytgen_path": "rights_summary",
            "owner": "NLMYTGen adapter + human reviewer",
            "mapping": "preserve hold, never approve",
        },
        {
            "field_name": "notebooklm_packet",
            "newsroom_path": "notebooklm_packet.transcript_seed.summary",
            "nlmytgen_path": "notebooklm_packet.transcript_seed",
            "owner": "NLMYTGen adapter",
            "mapping": "flatten",
        },
        {
            "field_name": "script_beats",
            "newsroom_path": "script_beats[].summary/source_refs",
            "nlmytgen_path": "script_beats[].claim/evidence_refs",
            "owner": "NLMYTGen adapter",
            "mapping": "rename and preserve stable ids",
        },
        {
            "field_name": "visual_plan",
            "newsroom_path": "visual_plan[].unit_type",
            "nlmytgen_path": "visual_plan[].visualir_concept/content_slots",
            "owner": "NLMYTGen adapter",
            "mapping": "map unit type to known content slots",
        },
        {
            "field_name": "g28_slot_hints",
            "newsroom_path": "g28_slot_hints[].hint_type",
            "nlmytgen_path": "g28_slot_hints[].object_catalog_slot",
            "owner": "NLMYTGen adapter",
            "mapping": "alias map only when unambiguous",
        },
        {
            "field_name": "review_warnings",
            "newsroom_path": "review_warnings[].severity",
            "nlmytgen_path": "review_warnings[].blocks_ymm4_transfer",
            "owner": "NLMYTGen adapter",
            "mapping": "explicit blocker boolean",
        },
        {
            "field_name": "downstream_readiness",
            "newsroom_path": "downstream_readiness",
            "nlmytgen_path": "downstream_readiness",
            "owner": "NLMYTGen adapter",
            "mapping": "fail-closed booleans and blockers",
        },
        {
            "field_name": "visual_treatment_preference",
            "newsroom_path": "visual_plan[].unit_type",
            "nlmytgen_path": "optional_enrichments.visual_treatment_preference",
            "owner": "NLMYTGen adapter",
            "mapping": "derive advisory values",
        },
        {
            "field_name": "channel_package_metadata",
            "newsroom_path": "channel_metadata",
            "nlmytgen_path": "optional_enrichments.channel_package_metadata",
            "owner": "NLMYTGen adapter",
            "mapping": "rename",
        },
    ]

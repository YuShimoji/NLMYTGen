"""Diagnostic episode production capsule for newsroom handoff packets.

This module bridges an already-adapted fake newsroom packet toward a
video-structure review artifact. It does not fetch sources, generate media,
write YMM4 projects, render output, or approve production use.
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


CAPSULE_SCHEMA_VERSION = "newsroom_episode_production_capsule.v1"
CAPSULE_ARTIFACT_ID = "newsroom_episode_production_capsule_v1_2026_06_22"
DEFAULT_PACKET_PATH = Path("samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json")
DEFAULT_ADAPTER_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json"
)
DEFAULT_PRIOR_SLOT_LINKAGE_PATH = Path(
    "samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json"
)
DEFAULT_PRIOR_TRANSFER_PLANNING_PATH = Path(
    "samples/_probe/newsroom_handoff/transfer_planning_readback.json"
)
DEFAULT_READINESS_CHECKLIST_PATH = Path(
    "samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json"
)
DEFAULT_CAPSULE_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
)
DEFAULT_CAPSULE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md"
)
REVIEW_CONSOLE_PLANNING_DOC_PATH = (
    "docs/verification/NEWSROOM_REVIEW_CONSOLE_PLANNING_PANEL_V1_2026-06-20.md"
)

CAPSULE_REQUIRED_PROHIBITED_STEPS: tuple[str, ...] = (
    "real source fetch",
    ".ymmp generation",
    "YMM4 carrier generation",
    "render generation",
    "production approval",
    "publishing",
    "RSS/Inoreader operation",
    "real URL access",
    "media download",
)

CAPSULE_NEXT_ALLOWED_STEPS: tuple[str, ...] = (
    "Review Console episode preview",
    "caption/timing refinement",
    "YMM4 transfer candidate proof only after blockers are resolved",
)


def load_json_object(path: str | Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    json_path = Path(path)
    with json_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {json_path}")
    return payload


def build_default_newsroom_episode_production_capsule(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed diagnostic capsule from the default proof chain."""
    base = Path(root) if root is not None else Path(".")
    packet = load_json_object(base / DEFAULT_PACKET_PATH)
    adapter_readback = load_json_object(base / DEFAULT_ADAPTER_READBACK_PATH)
    prior_slot_linkage = load_json_object(base / DEFAULT_PRIOR_SLOT_LINKAGE_PATH)
    prior_transfer_planning = load_json_object(base / DEFAULT_PRIOR_TRANSFER_PLANNING_PATH)
    readiness_checklist = load_json_object(base / DEFAULT_READINESS_CHECKLIST_PATH)

    return build_newsroom_episode_production_capsule(
        packet,
        adapter_readback,
        prior_slot_linkage_readback=prior_slot_linkage,
        prior_transfer_planning_readback=prior_transfer_planning,
        readiness_checklist=readiness_checklist,
        packet_path=DEFAULT_PACKET_PATH,
        adapter_readback_path=DEFAULT_ADAPTER_READBACK_PATH,
        prior_slot_linkage_path=DEFAULT_PRIOR_SLOT_LINKAGE_PATH,
        prior_transfer_planning_path=DEFAULT_PRIOR_TRANSFER_PLANNING_PATH,
        readiness_checklist_path=DEFAULT_READINESS_CHECKLIST_PATH,
    )


def build_newsroom_episode_production_capsule(
    packet: dict[str, Any],
    adapter_readback: dict[str, Any],
    *,
    prior_slot_linkage_readback: dict[str, Any] | None = None,
    prior_transfer_planning_readback: dict[str, Any] | None = None,
    readiness_checklist: dict[str, Any] | None = None,
    packet_path: str | Path | None = None,
    adapter_readback_path: str | Path | None = None,
    prior_slot_linkage_path: str | Path | None = None,
    prior_transfer_planning_path: str | Path | None = None,
    readiness_checklist_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic diagnostic episode production capsule."""
    validation = validate_newsroom_handoff_packet(packet, packet_path=packet_path)
    slot_linkage = build_g28_slot_linkage_proof(packet, packet_path=packet_path)
    slot_payload = slot_linkage.to_dict()
    transfer = build_newsroom_transfer_planning_proof(
        packet,
        slot_payload,
        packet_path=packet_path,
    )
    transfer_payload = transfer.to_dict()
    validation_result = _dict(adapter_readback.get("validation_result"))

    script_structure = _build_script_structure(packet)
    visual_structure = _build_visual_structure(packet, slot_payload)
    timing = _build_timing_approximation(script_structure)

    prohibited_steps = _unique_strings(
        list(CAPSULE_REQUIRED_PROHIBITED_STEPS)
        + transfer_payload.get("prohibited_next_actions", [])
    )

    return {
        "artifact_id": CAPSULE_ARTIFACT_ID,
        "schema_version": CAPSULE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "source": {
            "capsule_source": "adapted_packet_current_recomputed_readbacks",
            "packet_path": _path_text(packet_path),
            "adapter_readback_path": _path_text(adapter_readback_path),
            "readiness_checklist_path": _path_text(readiness_checklist_path),
            "source_fixture_kind": packet.get("fixture_kind"),
            "source_fixture": packet.get("source_fixture"),
            "adapter_status": adapter_readback.get("status"),
            "inspected_prior_readbacks": _prior_readback_rows(
                prior_slot_linkage_readback=prior_slot_linkage_readback,
                prior_transfer_planning_readback=prior_transfer_planning_readback,
                prior_slot_linkage_path=prior_slot_linkage_path,
                prior_transfer_planning_path=prior_transfer_planning_path,
            ),
        },
        "episode": {
            "episode_id": packet.get("episode_id"),
            "title": packet.get("title"),
            "contract_version": packet.get("contract_version"),
            "source": "synthetic/adapted packet",
            "topic_summary": packet.get("topic_summary"),
            "source_fixture": packet.get("source_fixture"),
        },
        "video_readiness": {
            "script_structure": "diagnostic_capsule_ready",
            "visual_structure": "diagnostic_capsule_ready",
            "caption_reserve": "mapped_with_unhinted_slot_warnings",
            "timing": "provisional",
            "audio_readiness": "not_started",
            "validator_status": validation_result.get(
                "adapter_packet_validator_status",
                validation.status,
            ),
            "slot_linkage_status": validation_result.get(
                "slot_linkage_status",
                slot_linkage.status,
            ),
            "transfer_planning_status": validation_result.get(
                "transfer_planning_status",
                transfer.status,
            ),
            "transfer_status": "blocked",
            "ymm4_transfer_ready": False,
            "production_approval": False,
            "public_use": False,
        },
        "script_structure": script_structure,
        "visual_structure": visual_structure,
        "timing_approximation": timing,
        "audio_voice_status": {
            "voice_source": "absent_synthetic_placeholder",
            "audio_readiness": "not_started",
            "tts_generation": "not_performed",
            "narration_approval": False,
        },
        "transfer_status": {
            "validator_status": validation.status,
            "validator_transfer_status": validation.transfer_status,
            "slot_linkage_status": slot_linkage.status,
            "slot_linkage_transfer_status": slot_linkage.transfer_status,
            "transfer_planning_status": transfer.status,
            "transfer_status": transfer.transfer_status,
            "blocker_count": transfer_payload["blocker_count"],
            "unlock_requirement_count": transfer_payload["unlock_requirement_count"],
            "blockers": transfer_payload["transfer_blockers"],
            "unlock_requirements": transfer_payload["unlock_requirements"],
            "warnings": transfer_payload["warnings"],
        },
        "review_console_summary": {
            "review_surface_ready": _dict(packet.get("downstream_readiness")).get(
                "review_surface_ready"
            ),
            "planning_panel_doc": REVIEW_CONSOLE_PLANNING_DOC_PATH,
            "candidate_summary": transfer.transfer_candidate_summary,
            "next_review_surface": "future_read_only_episode_preview",
        },
        "next_allowed_steps": list(CAPSULE_NEXT_ALLOWED_STEPS),
        "prohibited_steps": prohibited_steps,
        "remaining_gaps_before_importable_proof": _remaining_gaps(
            transfer_payload,
            slot_payload,
        ),
        "readiness_checklist_reference": _readiness_reference(
            readiness_checklist,
            readiness_checklist_path,
        ),
        "boundary_assertions": {
            "diagnostic_only": True,
            "public_video": False,
            "usable_public_video": False,
            "real_source_fetch_performed": False,
            "rss_inoreader_access_performed": False,
            "real_urls_accessed": False,
            "contains_real_urls": False,
            "contains_media": False,
            "external_media_downloaded": False,
            "tts_generated": False,
            "ymmp_generated": False,
            "ymm4_carrier_generated": False,
            "render_generated": False,
            "production_approval": False,
            "publishing_ready": False,
            "modifies_source_fixture_or_readbacks": False,
        },
    }


def render_newsroom_episode_production_capsule_markdown(
    capsule: dict[str, Any],
) -> str:
    """Render a human-readable readback for the diagnostic capsule."""
    episode = _dict(capsule.get("episode"))
    readiness = _dict(capsule.get("video_readiness"))
    transfer = _dict(capsule.get("transfer_status"))
    timing = _dict(capsule.get("timing_approximation"))

    lines = [
        "# Newsroom Episode Production Capsule v1",
        "",
        f"artifact_id: {capsule.get('artifact_id')}",
        f"schema_version: {capsule.get('schema_version')}",
        f"review_status: {capsule.get('review_status')}",
        f"production_status: {capsule.get('production_status')}",
        "diagnostic_only: true",
        "",
        "## Purpose",
        "",
        "This capsule is the first diagnostic bridge from the adapted fake newsroom packet "
        "toward one video structure. It organizes ScriptIR-like beats, VisualIR concepts, "
        "G-28 slot hints, caption reserve state, provisional timing, and transfer blockers "
        "without accepting production, public, or YMM4 readiness.",
        "",
        "## Episode Capsule Summary",
        "",
        f"- episode_id: {episode.get('episode_id')}",
        f"- title: {episode.get('title')}",
        f"- source: {episode.get('source')}",
        f"- script_beats: {len(capsule.get('script_structure', []))}",
        f"- visual_units: {len(capsule.get('visual_structure', []))}",
        f"- total_approx_duration_seconds: {timing.get('total_duration_seconds')}",
        f"- transfer_status: {transfer.get('transfer_status')}",
        f"- blocker_count: {transfer.get('blocker_count')}",
        f"- unlock_requirement_count: {transfer.get('unlock_requirement_count')}",
        "",
        "## Video Readiness Matrix",
        "",
        "| area | status | note |",
        "|---|---|---|",
        (
            "| script structure | "
            f"{readiness.get('script_structure')} | beats are mapped from adapted packet only |"
        ),
        (
            "| visual structure | "
            f"{readiness.get('visual_structure')} | visual units remain schematic/template-only |"
        ),
        (
            "| caption reserve | "
            f"{readiness.get('caption_reserve')} | semantic reserve exists but slot warnings remain |"
        ),
        f"| timing | {readiness.get('timing')} | rough sequence timing only |",
        (
            "| audio/voice | "
            f"{readiness.get('audio_readiness')} | no TTS, narration, or audio file exists |"
        ),
        (
            "| transfer | "
            f"{readiness.get('transfer_status')} | YMM4 transfer is false and blockers remain |"
        ),
        "",
        "## Script Structure",
        "",
    ]
    for beat in capsule.get("script_structure", []):
        lines.append(
            f"- {beat['order']}. {beat['beat_id']}: {beat['purpose']} "
            f"({beat['rough_duration_seconds']}s; review={beat['review_status']})"
        )
        lines.append(f"  placeholder: {beat['expected_narration_placeholder']}")
        source_refs = ", ".join(beat.get("source_note_refs", [])) or "none"
        visual_refs = ", ".join(beat.get("visual_refs", [])) or "none"
        lines.append(f"  source_note_refs: {source_refs}; visual_refs: {visual_refs}")

    lines.extend(["", "## Visual Structure", ""])
    for visual in capsule.get("visual_structure", []):
        slots = ", ".join(
            slot["object_catalog_slot"] for slot in visual.get("g28_slot_refs", [])
        ) or "none"
        gaps = ", ".join(visual.get("unhinted_content_slots", [])) or "none"
        lines.append(
            f"- {visual['visual_id']}: {visual['visualir_concept']} / "
            f"{visual['layout_candidate']} (slots={slots}; unhinted={gaps})"
        )
        lines.append(
            f"  caption_reserve: {visual['caption_reserve']['status']}; "
            f"warning: {visual['schematic_proxy_warning']}"
        )

    lines.extend([
        "",
        "## Transfer And Review Debt",
        "",
        f"validator_status: {transfer.get('validator_status')}",
        f"slot_linkage_status: {transfer.get('slot_linkage_status')}",
        f"transfer_planning_status: {transfer.get('transfer_planning_status')}",
        f"transfer_status: {transfer.get('transfer_status')}",
        "",
        "Remaining gaps before importable proof:",
    ])
    for gap in capsule.get("remaining_gaps_before_importable_proof", []):
        lines.append(f"- {gap}")

    lines.extend(["", "Prohibited steps:"])
    for step in capsule.get("prohibited_steps", []):
        lines.append(f"- {step}")

    lines.extend(["", "Next allowed steps:"])
    for step in capsule.get("next_allowed_steps", []):
        lines.append(f"- {step}")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only. It does not create `.ymmp`, YMM4 carriers, "
        "renders, TTS/audio, external fetches, real source access, media downloads, "
        "production approvals, rights approvals, public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _build_script_structure(packet: dict[str, Any]) -> list[dict[str, Any]]:
    beats = _list(packet.get("script_beats"))
    result: list[dict[str, Any]] = []
    for index, beat in enumerate(beats, start=1):
        evidence_refs = _string_list(beat.get("evidence_refs"))
        visual_refs = _string_list(beat.get("visual_refs"))
        result.append({
            "order": index,
            "beat_id": beat.get("beat_id"),
            "stable_id": beat.get("stable_id"),
            "purpose": beat.get("intent"),
            "expected_narration_placeholder": beat.get("claim"),
            "source_note_refs": evidence_refs,
            "visual_refs": visual_refs,
            "review_status": beat.get("review_status"),
            "scriptir_hint": beat.get("scriptir_hint"),
            "no_evidence_reason": beat.get("no_evidence_reason"),
            "rough_duration_seconds": _rough_duration_seconds(beat),
        })
    return result


def _build_visual_structure(
    packet: dict[str, Any],
    slot_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    hints_by_visual = _items_by_key(packet.get("g28_slot_hints"), "visual_id")
    linkages_by_visual = _items_by_key(slot_payload.get("linkages"), "visual_id")
    gaps_by_visual = {
        str(item.get("visual_id")): item
        for item in _list(slot_payload.get("visual_slot_gaps"))
        if item.get("visual_id") is not None
    }
    result: list[dict[str, Any]] = []
    for index, visual in enumerate(_list(packet.get("visual_plan")), start=1):
        visual_id = str(visual.get("visual_id"))
        hints = hints_by_visual.get(visual_id, [])
        linkages = linkages_by_visual.get(visual_id, [])
        gap = gaps_by_visual.get(visual_id, {})
        content_slots = _string_list(visual.get("content_slots"))
        hinted_slots = {
            str(hint.get("object_catalog_slot"))
            for hint in hints
            if hint.get("object_catalog_slot") is not None
        }
        hinted_slots.update(
            str(linkage.get("selected_g28_slot"))
            for linkage in linkages
            if linkage.get("selected_g28_slot") is not None
        )
        unhinted_slots = _string_list(gap.get("missing_g28_slot_hints"))
        caption_present = (
            "caption_reserve" in content_slots
            or "caption_reserve" in hinted_slots
        )
        result.append({
            "order": index,
            "visual_id": visual.get("visual_id"),
            "stable_id": visual.get("stable_id"),
            "beat_id": visual.get("beat_id"),
            "visualir_concept": visual.get("visualir_concept"),
            "layout_candidate": visual.get("layout_candidate"),
            "asset_policy": visual.get("asset_policy"),
            "approval_state": visual.get("approval_state"),
            "source_unit_type": visual.get("source_unit_type"),
            "visual_plan_ref": f"visual_plan[{index - 1}]",
            "g28_slot_refs": [
                {
                    "slot_id": hint.get("slot_id"),
                    "object_catalog_slot": hint.get("object_catalog_slot"),
                    "semantic_role": hint.get("semantic_role"),
                    "text_budget": hint.get("text_budget"),
                    "geometry_authority": hint.get("geometry_authority"),
                    "transfer_note": hint.get("transfer_note"),
                }
                for hint in hints
            ],
            "review_surface_refs": _review_surface_refs(linkages),
            "caption_reserve": {
                "status": "present" if caption_present else "missing",
                "subtitle_safety_note": (
                    "Caption reserve is semantic only; geometry remains downstream/YMM4 blocked."
                ),
            },
            "schematic_proxy_warning": (
                "Schematic/template-only visual; no screenshot, footage, or approved media is included."
            ),
            "unhinted_content_slots": unhinted_slots,
        })
    return result


def _build_timing_approximation(
    script_structure: list[dict[str, Any]],
) -> dict[str, Any]:
    segments = [
        {
            "beat_id": beat.get("beat_id"),
            "rough_duration_seconds": beat["rough_duration_seconds"],
        }
        for beat in script_structure
    ]
    return {
        "status": "provisional",
        "method": (
            "Deterministic rough diagnostic duration from beat order, evidence refs, "
            "and visual refs; not narration timing."
        ),
        "segments": segments,
        "total_duration_seconds": sum(segment["rough_duration_seconds"] for segment in segments),
    }


def _rough_duration_seconds(beat: dict[str, Any]) -> int:
    evidence_refs = _string_list(beat.get("evidence_refs"))
    visual_refs = _string_list(beat.get("visual_refs"))
    review_penalty = 4 if beat.get("review_status") == "hold_for_review" else 0
    return 20 + (8 * len(evidence_refs)) + (4 * len(visual_refs)) + review_penalty


def _remaining_gaps(
    transfer_payload: dict[str, Any],
    slot_payload: dict[str, Any],
) -> list[str]:
    gaps = [
        "rights and provenance are not cleared",
        "approved source media or approved abstract replacements are absent",
        "human review and production approval are absent",
        "audio voice, TTS, and narration timing are not started",
        "caption timing is only provisionally reserved",
        "YMM4 transfer remains blocked",
    ]
    visual_slot_gaps = _list(slot_payload.get("visual_slot_gaps"))
    if visual_slot_gaps:
        gaps.append("visual G-28 slot warnings remain before transfer-candidate review")
    if transfer_payload.get("unlock_requirement_count"):
        gaps.append(
            f"{transfer_payload['unlock_requirement_count']} unlock requirements remain open"
        )
    return gaps


def _readiness_reference(
    readiness_checklist: dict[str, Any] | None,
    readiness_checklist_path: str | Path | None,
) -> dict[str, Any]:
    checklist = readiness_checklist or {}
    return {
        "path": _path_text(readiness_checklist_path),
        "artifact_id": checklist.get("artifact_id"),
        "status": checklist.get("status"),
        "real_packet_accepted": checklist.get("real_packet_accepted"),
        "production_approval": checklist.get("production_approval"),
        "ymm4_transfer_ready": checklist.get("ymm4_transfer_ready"),
    }


def _prior_readback_rows(
    *,
    prior_slot_linkage_readback: dict[str, Any] | None,
    prior_transfer_planning_readback: dict[str, Any] | None,
    prior_slot_linkage_path: str | Path | None,
    prior_transfer_planning_path: str | Path | None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for kind, payload, path in [
        ("prior_slot_linkage", prior_slot_linkage_readback, prior_slot_linkage_path),
        (
            "prior_transfer_planning",
            prior_transfer_planning_readback,
            prior_transfer_planning_path,
        ),
    ]:
        data = payload or {}
        rows.append({
            "kind": kind,
            "path": _path_text(path),
            "artifact_id": data.get("artifact_id"),
            "episode_id": data.get("episode_id"),
            "status": data.get("status"),
            "transfer_status": data.get("transfer_status"),
            "relationship": (
                "inspected as earlier newsroom chain evidence; capsule identity uses "
                "the adapted packet and recomputed readbacks"
            ),
        })
    return rows


def _review_surface_refs(linkages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for linkage in linkages:
        review_surface = linkage.get("review_surface")
        if not isinstance(review_surface, dict):
            continue
        for key, value in review_surface.items():
            if not isinstance(value, str):
                continue
            marker = (key, value)
            if marker in seen:
                continue
            seen.add(marker)
            refs.append({"kind": key, "path": value})
    return refs


def _items_by_key(raw: Any, key: str) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for item in _list(raw):
        value = item.get(key)
        if not isinstance(value, str):
            continue
        result.setdefault(value, []).append(item)
    return result


def _unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str) or value in seen:
            continue
        result.append(value)
        seen.add(value)
    return result


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None

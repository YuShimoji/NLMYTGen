"""Lightweight validation for newsroom -> NLMYTGen handoff packets.

This module checks the portable packet boundary only. It does not fetch sources,
open external material, generate YMM4 artifacts, or approve transfer readiness.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ALLOWED_G28_SLOT_SET: tuple[str, ...] = (
    "image_slot",
    "screenshot_slot",
    "footage_slot",
    "highlight_box",
    "arrow",
    "leader_line",
    "label_chip",
    "callout_box",
    "lower_third_telop",
    "source_note",
    "quote_card",
    "comparison_panel",
    "table_row",
    "host_placeholder",
    "caption_reserve",
)

REQUIRED_TOP_LEVEL_FIELDS: tuple[str, ...] = (
    "artifact_id",
    "contract_version",
    "episode_id",
    "title",
    "topic_summary",
    "episode_metadata",
    "source_notes",
    "provenance",
    "rights_summary",
    "notebooklm_packet",
    "script_beats",
    "visual_plan",
    "g28_slot_hints",
    "review_warnings",
    "downstream_readiness",
)


@dataclass
class NewsroomHandoffValidationResult:
    """Human and machine-readable validation result."""

    status: str
    packet_path: str | None = None
    artifact_id: str | None = None
    episode_id: str | None = None
    contract_version: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    observed_g28_slots: list[str] = field(default_factory=list)
    ymm4_transfer_ready: bool | None = None
    next_use: str = (
        "Use this readback as a pre-ingest structure gate before ScriptIR-like, "
        "VisualIR, G-28, or YMM4 transfer planning."
    )

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def transfer_status(self) -> str:
        if self.has_errors:
            return "blocked"
        if self.ymm4_transfer_ready is True and not self.blockers:
            return "ready"
        return "blocked"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["has_errors"] = self.has_errors
        payload["transfer_status"] = self.transfer_status
        return payload


def load_newsroom_handoff_packet(path: str | Path) -> dict[str, Any]:
    """Load a newsroom handoff packet and require a JSON object root."""
    packet_path = Path(path)
    with packet_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"newsroom handoff packet must be a JSON object: {packet_path}")
    return data


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _append_required_field_errors(
    packet: dict[str, Any],
    errors: list[str],
) -> None:
    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in packet:
            errors.append(f"REQUIRED_FIELD_MISSING: {field_name}")
            continue
        value = packet[field_name]
        if value is None or value == "" or value == [] or value == {}:
            errors.append(f"REQUIRED_FIELD_EMPTY: {field_name}")


def _list_of_dicts(packet: dict[str, Any], field_name: str, errors: list[str]) -> list[dict[str, Any]]:
    raw = packet.get(field_name)
    if not isinstance(raw, list):
        errors.append(f"FIELD_TYPE_INVALID: {field_name} must be an array")
        return []
    if not raw:
        errors.append(f"FIELD_EMPTY: {field_name} must not be empty")
        return []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            errors.append(f"FIELD_ITEM_TYPE_INVALID: {field_name}[{index}] must be an object")
            continue
        items.append(item)
    return items


def _collect_unique_ids(
    items: list[dict[str, Any]],
    *,
    field_name: str,
    item_name: str,
    errors: list[str],
) -> set[str]:
    ids: set[str] = set()
    for index, item in enumerate(items):
        raw = item.get(field_name)
        if not _is_non_empty_string(raw):
            errors.append(f"{item_name.upper()}_ID_MISSING: {item_name}[{index}].{field_name}")
            continue
        if raw in ids:
            errors.append(f"{item_name.upper()}_ID_DUPLICATE: {raw}")
        ids.add(raw)
    return ids


def validate_newsroom_handoff_packet(
    packet: dict[str, Any],
    *,
    packet_path: str | Path | None = None,
    allowed_g28_slots: set[str] | None = None,
) -> NewsroomHandoffValidationResult:
    """Validate a newsroom handoff packet against the NLMYTGen intake boundary."""
    errors: list[str] = []
    warnings: list[str] = []
    blockers: list[str] = []
    allowed_slots = allowed_g28_slots or set(ALLOWED_G28_SLOT_SET)

    _append_required_field_errors(packet, errors)

    for identity_field in ("artifact_id", "contract_version", "episode_id"):
        if identity_field in packet and not _is_non_empty_string(packet.get(identity_field)):
            errors.append(f"IDENTITY_FIELD_INVALID: {identity_field}")

    if not isinstance(packet.get("episode_metadata"), dict):
        errors.append("FIELD_TYPE_INVALID: episode_metadata must be an object")
    if not isinstance(packet.get("provenance"), dict):
        errors.append("FIELD_TYPE_INVALID: provenance must be an object")
    if not isinstance(packet.get("rights_summary"), dict):
        errors.append("FIELD_TYPE_INVALID: rights_summary must be an object")
    if not isinstance(packet.get("downstream_readiness"), dict):
        errors.append("FIELD_TYPE_INVALID: downstream_readiness must be an object")

    source_notes = _list_of_dicts(packet, "source_notes", errors)
    script_beats = _list_of_dicts(packet, "script_beats", errors)
    visual_plan = _list_of_dicts(packet, "visual_plan", errors)
    g28_slot_hints = _list_of_dicts(packet, "g28_slot_hints", errors)
    review_warnings = _list_of_dicts(packet, "review_warnings", errors)

    source_ids = _collect_unique_ids(
        source_notes,
        field_name="source_id",
        item_name="source_note",
        errors=errors,
    )
    beat_ids = _collect_unique_ids(
        script_beats,
        field_name="beat_id",
        item_name="script_beat",
        errors=errors,
    )
    visual_ids = _collect_unique_ids(
        visual_plan,
        field_name="visual_id",
        item_name="visual",
        errors=errors,
    )
    _collect_unique_ids(
        g28_slot_hints,
        field_name="slot_id",
        item_name="g28_slot_hint",
        errors=errors,
    )

    notebooklm_packet = packet.get("notebooklm_packet")
    if not isinstance(notebooklm_packet, dict):
        errors.append("FIELD_TYPE_INVALID: notebooklm_packet must be an object")
    elif not (
        _is_non_empty_string(notebooklm_packet.get("transcript_seed"))
        or _is_non_empty_string(notebooklm_packet.get("source_pack_summary"))
    ):
        errors.append(
            "NOTEBOOKLM_SEED_MISSING: notebooklm_packet must include transcript_seed "
            "or source_pack_summary"
        )

    for beat in script_beats:
        beat_id = beat.get("beat_id", "<missing>")
        for field_name in ("intent", "claim"):
            if not _is_non_empty_string(beat.get(field_name)):
                errors.append(f"SCRIPT_BEAT_FIELD_MISSING: {beat_id}.{field_name}")
        evidence_refs = beat.get("evidence_refs")
        if evidence_refs is None:
            evidence_refs = []
        if not isinstance(evidence_refs, list):
            errors.append(f"SCRIPT_BEAT_EVIDENCE_INVALID: {beat_id}.evidence_refs")
            continue
        if not evidence_refs and not _is_non_empty_string(beat.get("no_evidence_reason")):
            warnings.append(f"SCRIPT_BEAT_NO_EVIDENCE: {beat_id}")
        for source_ref in evidence_refs:
            if source_ref not in source_ids:
                errors.append(f"SCRIPT_BEAT_UNKNOWN_SOURCE_REF: {beat_id}->{source_ref}")

    for visual in visual_plan:
        visual_id = visual.get("visual_id", "<missing>")
        beat_ref = visual.get("beat_id")
        if beat_ref not in beat_ids:
            errors.append(f"VISUAL_UNKNOWN_BEAT_REF: {visual_id}->{beat_ref}")
        for field_name in ("visualir_concept", "layout_candidate", "asset_policy"):
            if not _is_non_empty_string(visual.get(field_name)):
                errors.append(f"VISUAL_FIELD_MISSING: {visual_id}.{field_name}")
        content_slots = visual.get("content_slots")
        if not isinstance(content_slots, list) or not content_slots:
            errors.append(f"VISUAL_CONTENT_SLOTS_MISSING: {visual_id}")
        elif any(slot not in allowed_slots for slot in content_slots):
            invalid = sorted({slot for slot in content_slots if slot not in allowed_slots})
            errors.append(f"VISUAL_CONTENT_SLOT_UNKNOWN: {visual_id}->{','.join(invalid)}")

    hint_visual_ids: set[str] = set()
    observed_slots: set[str] = set()
    for hint in g28_slot_hints:
        slot_id = hint.get("slot_id", "<missing>")
        visual_ref = hint.get("visual_id")
        if visual_ref not in visual_ids:
            errors.append(f"G28_SLOT_UNKNOWN_VISUAL_REF: {slot_id}->{visual_ref}")
        else:
            hint_visual_ids.add(visual_ref)
        slot_name = hint.get("object_catalog_slot")
        if slot_name not in allowed_slots:
            errors.append(f"G28_SLOT_UNKNOWN_OBJECT: {slot_id}->{slot_name}")
        else:
            observed_slots.add(slot_name)
        source_ref = hint.get("source_ref")
        if source_ref is not None and source_ref not in source_ids:
            errors.append(f"G28_SLOT_UNKNOWN_SOURCE_REF: {slot_id}->{source_ref}")

    for visual_id in sorted(visual_ids - hint_visual_ids):
        warnings.append(f"VISUAL_WITHOUT_G28_HINT: {visual_id}")

    provenance = packet.get("provenance")
    if isinstance(provenance, dict):
        if "raw_source_material_included" not in provenance:
            errors.append("PROVENANCE_FIELD_MISSING: raw_source_material_included")
        if provenance.get("external_fetch_allowed_by_nlmytgen") is True:
            blockers.append("external_fetch_allowed_by_nlmytgen")

    rights_summary = packet.get("rights_summary")
    if isinstance(rights_summary, dict):
        clearance_state = rights_summary.get("clearance_state")
        if not _is_non_empty_string(clearance_state):
            errors.append("RIGHTS_CLEARANCE_STATE_MISSING")
        elif clearance_state != "cleared":
            blockers.append(f"rights_clearance_not_cleared:{clearance_state}")
        blocked_uses = rights_summary.get("blocked_uses")
        if isinstance(blocked_uses, list) and "YMM4_transfer" in blocked_uses:
            blockers.append("rights_summary_blocks_ymm4_transfer")

    for warning in review_warnings:
        warning_id = warning.get("warning_id", "<missing>")
        if not _is_non_empty_string(warning.get("severity")):
            errors.append(f"REVIEW_WARNING_FIELD_MISSING: {warning_id}.severity")
        if warning.get("blocks_ymm4_transfer") is True:
            blockers.append(f"review_warning_blocks_ymm4:{warning_id}")

    downstream_readiness = packet.get("downstream_readiness")
    ymm4_transfer_ready: bool | None = None
    if isinstance(downstream_readiness, dict):
        raw_ready = downstream_readiness.get("ymm4_transfer_ready")
        if not isinstance(raw_ready, bool):
            errors.append("DOWNSTREAM_READINESS_FIELD_INVALID: ymm4_transfer_ready")
        else:
            ymm4_transfer_ready = raw_ready
        blocking_reasons = downstream_readiness.get("blocking_reasons")
        if isinstance(blocking_reasons, list):
            blockers.extend(f"downstream_blocking_reason:{reason}" for reason in blocking_reasons)
        elif raw_ready is False:
            warnings.append("DOWNSTREAM_BLOCKING_REASONS_MISSING")

    unique_blockers = sorted(set(blockers))
    if ymm4_transfer_ready is True and unique_blockers:
        errors.append("YMM4_READY_CONTRADICTS_BLOCKERS")
    if ymm4_transfer_ready is False and not unique_blockers:
        warnings.append("YMM4_TRANSFER_NOT_READY_WITHOUT_EXPLICIT_BLOCKER")

    status = "failed" if errors else "passed"
    return NewsroomHandoffValidationResult(
        status=status,
        packet_path=str(packet_path) if packet_path is not None else None,
        artifact_id=packet.get("artifact_id") if isinstance(packet.get("artifact_id"), str) else None,
        episode_id=packet.get("episode_id") if isinstance(packet.get("episode_id"), str) else None,
        contract_version=(
            packet.get("contract_version")
            if isinstance(packet.get("contract_version"), str)
            else None
        ),
        errors=errors,
        warnings=warnings,
        blockers=unique_blockers,
        counts={
            "source_notes": len(source_notes),
            "script_beats": len(script_beats),
            "visual_plan": len(visual_plan),
            "g28_slot_hints": len(g28_slot_hints),
            "review_warnings": len(review_warnings),
        },
        observed_g28_slots=sorted(observed_slots),
        ymm4_transfer_ready=ymm4_transfer_ready,
    )


def render_newsroom_handoff_validation_text(
    result: NewsroomHandoffValidationResult,
) -> str:
    """Render a compact readback for operators and review reports."""
    lines: list[str] = [
        "# Newsroom Handoff Validation Readback",
        "",
        f"status: {result.status}",
        f"transfer_status: {result.transfer_status}",
    ]
    if result.packet_path:
        lines.append(f"packet_path: {result.packet_path}")
    if result.artifact_id:
        lines.append(f"artifact_id: {result.artifact_id}")
    if result.episode_id:
        lines.append(f"episode_id: {result.episode_id}")
    if result.contract_version:
        lines.append(f"contract_version: {result.contract_version}")

    lines.append("")
    lines.append("counts:")
    for key, value in sorted(result.counts.items()):
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("observed_g28_slots:")
    if result.observed_g28_slots:
        for slot in result.observed_g28_slots:
            lines.append(f"- {slot}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("errors:")
    if result.errors:
        for error in result.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("warnings:")
    if result.warnings:
        for warning in result.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("ymm4_transfer_blockers:")
    if result.blockers:
        for blocker in result.blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append(f"next_use: {result.next_use}")
    return "\n".join(lines) + "\n"

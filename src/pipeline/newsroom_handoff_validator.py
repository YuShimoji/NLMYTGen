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


@dataclass
class NewsroomG28SlotLinkageProof:
    """Readback linking newsroom visual metadata to G-28 review slots."""

    status: str
    packet_path: str | None = None
    artifact_id: str | None = None
    episode_id: str | None = None
    contract_version: str | None = None
    validator_status: str = "not_run"
    transfer_status: str = "blocked"
    ymm4_transfer_ready: bool | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    linkages: list[dict[str, Any]] = field(default_factory=list)
    visual_slot_gaps: list[dict[str, Any]] = field(default_factory=list)
    review_surface_index: dict[str, str] = field(default_factory=dict)
    next_use: str = (
        "Use this proof as a UI-independent readback before a future Review "
        "Console consumer or G-28 transfer-planning slice."
    )

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["has_errors"] = self.has_errors
        return payload


@dataclass
class NewsroomTransferPlanningProof:
    """Non-YMM4 transfer-planning readback for newsroom handoff packets."""

    status: str
    transfer_status: str = "blocked"
    packet_path: str | None = None
    slot_linkage_path: str | None = None
    review_console_doc_path: str | None = None
    artifact_id: str | None = None
    episode_id: str | None = None
    title: str | None = None
    contract_version: str | None = None
    validator_status: str = "not_run"
    slot_linkage_status: str = "not_loaded"
    review_console_visibility_status: str = "not_checked"
    ymm4_transfer_ready: bool | None = None
    transfer_candidate_summary: str = ""
    transfer_blockers: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    unlock_requirements: list[dict[str, Any]] = field(default_factory=list)
    contradiction_checks: list[dict[str, Any]] = field(default_factory=list)
    prohibited_next_actions: list[str] = field(default_factory=list)
    allowed_next_actions: list[str] = field(default_factory=list)
    input_counts: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_use: str = (
        "Use this proof as a non-YMM4 planning gate before a future read-only "
        "Review Console planning panel or real-packet readiness checklist."
    )

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["has_errors"] = self.has_errors
        payload["blocker_count"] = sum(len(items) for items in self.transfer_blockers.values())
        payload["unlock_requirement_count"] = len(self.unlock_requirements)
        return payload


G28_REVIEW_SURFACE_INDEX: dict[str, str] = {
    "object_catalog": "samples/_probe/g28/reference_layout_prototypes/object_catalog.html",
    "screenshot_callout": "samples/_probe/g28/reference_layout_prototypes/screenshot_callout.html",
    "article_quote_card": "samples/_probe/g28/reference_layout_prototypes/article_quote_card.html",
    "image_annotation_simple": (
        "samples/_probe/g28/reference_layout_prototypes/image_annotation_simple.html"
    ),
    "two_image_compare": "samples/_probe/g28/reference_layout_prototypes/two_image_compare.html",
    "asset_plus_caption": "samples/_probe/g28/reference_layout_prototypes/asset_plus_caption.html",
    "source_footage_annotated": (
        "samples/_probe/g28/reference_layout_prototypes/source_footage_annotated.html"
    ),
}

DEFAULT_REVIEW_CONSOLE_CONSUMER_DOC = (
    "docs/verification/NEWSROOM_REVIEW_CONSOLE_CONSUMER_V1_2026-06-20.md"
)

NEWSROOM_TRANSFER_PROHIBITED_NEXT_ACTIONS: tuple[str, ...] = (
    ".ymmp generation",
    "YMM4 carrier generation",
    "render generation",
    "external fetch",
    "production approval",
    "rights approval",
    "public-use approval",
)

NEWSROOM_TRANSFER_ALLOWED_NEXT_ACTIONS: tuple[str, ...] = (
    "Review Console planning panel",
    "real packet readiness checklist",
    "fixture/schema refinement",
    "rights/provenance field review",
    "approved media or abstract replacement planning",
)

SLOT_DEFAULT_LAYOUT_HINTS: dict[str, str] = {
    "image_slot": "image_annotation_simple",
    "screenshot_slot": "screenshot_callout",
    "footage_slot": "source_footage_annotated",
    "highlight_box": "image_annotation_simple",
    "arrow": "image_annotation_simple",
    "leader_line": "source_footage_annotated",
    "label_chip": "article_quote_card",
    "callout_box": "screenshot_callout",
    "lower_third_telop": "asset_plus_caption",
    "source_note": "screenshot_callout",
    "quote_card": "article_quote_card",
    "comparison_panel": "two_image_compare",
    "table_row": "object_catalog",
    "host_placeholder": "object_catalog",
    "caption_reserve": "object_catalog",
}


def load_newsroom_handoff_packet(path: str | Path) -> dict[str, Any]:
    """Load a newsroom handoff packet and require a JSON object root."""
    packet_path = Path(path)
    with packet_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"newsroom handoff packet must be a JSON object: {packet_path}")
    return data


def load_newsroom_slot_linkage_readback(path: str | Path) -> dict[str, Any]:
    """Load a G-28 slot-linkage readback and require a JSON object root."""
    readback_path = Path(path)
    with readback_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"newsroom slot-linkage readback must be a JSON object: {readback_path}")
    return data


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _bool_label(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return "unknown"


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


def _dicts_by_id(items: list[Any], id_field: str) -> dict[str, dict[str, Any]]:
    return {
        item[id_field]: item
        for item in items
        if isinstance(item, dict)
        and isinstance(item.get(id_field), str)
        and item[id_field].strip()
    }


def _source_refs_for_visual(
    beat: dict[str, Any] | None,
    hints: list[Any],
) -> list[str]:
    refs: set[str] = set()
    if beat and isinstance(beat.get("evidence_refs"), list):
        refs.update(ref for ref in beat["evidence_refs"] if isinstance(ref, str))
    for hint in hints:
        if not isinstance(hint, dict):
            continue
        source_ref = hint.get("source_ref")
        if isinstance(source_ref, str) and source_ref:
            refs.add(source_ref)
    return sorted(refs)


def _review_surface_for_slot(layout_candidate: str | None, slot_name: str) -> dict[str, str]:
    layout_key = layout_candidate if layout_candidate in G28_REVIEW_SURFACE_INDEX else None
    slot_layout = SLOT_DEFAULT_LAYOUT_HINTS.get(slot_name, "object_catalog")
    selected_key = layout_key or slot_layout
    return {
        "object_catalog": G28_REVIEW_SURFACE_INDEX["object_catalog"],
        "reference_layout": G28_REVIEW_SURFACE_INDEX.get(
            selected_key,
            G28_REVIEW_SURFACE_INDEX["object_catalog"],
        ),
        "future_review_console": "read_only_slot_linkage_consumer",
    }


def build_g28_slot_linkage_proof(
    packet: dict[str, Any],
    *,
    packet_path: str | Path | None = None,
    allowed_g28_slots: set[str] | None = None,
) -> NewsroomG28SlotLinkageProof:
    """Build a UI-independent readback from visual_plan to G-28 slot hints."""
    allowed_slots = allowed_g28_slots or set(ALLOWED_G28_SLOT_SET)
    validation = validate_newsroom_handoff_packet(
        packet,
        packet_path=packet_path,
        allowed_g28_slots=allowed_slots,
    )
    errors = list(validation.errors)
    warnings = list(validation.warnings)

    source_notes = packet.get("source_notes") if isinstance(packet.get("source_notes"), list) else []
    script_beats = packet.get("script_beats") if isinstance(packet.get("script_beats"), list) else []
    visual_plan = packet.get("visual_plan") if isinstance(packet.get("visual_plan"), list) else []
    g28_slot_hints = (
        packet.get("g28_slot_hints") if isinstance(packet.get("g28_slot_hints"), list) else []
    )

    source_by_id = _dicts_by_id(source_notes, "source_id")
    beat_by_id = _dicts_by_id(script_beats, "beat_id")
    visual_by_id = _dicts_by_id(visual_plan, "visual_id")
    hints_by_visual: dict[str, list[dict[str, Any]]] = {}
    for hint in g28_slot_hints:
        if not isinstance(hint, dict):
            continue
        visual_id = hint.get("visual_id")
        if isinstance(visual_id, str) and visual_id:
            hints_by_visual.setdefault(visual_id, []).append(hint)

    linkages: list[dict[str, Any]] = []
    visual_slot_gaps: list[dict[str, Any]] = []
    for visual in visual_plan:
        if not isinstance(visual, dict):
            continue
        visual_id = visual.get("visual_id")
        if not isinstance(visual_id, str) or not visual_id:
            continue
        beat_id = visual.get("beat_id")
        beat = beat_by_id.get(beat_id) if isinstance(beat_id, str) else None
        visual_hints = hints_by_visual.get(visual_id, [])
        hinted_slots = {
            hint.get("object_catalog_slot")
            for hint in visual_hints
            if isinstance(hint.get("object_catalog_slot"), str)
        }
        content_slots = visual.get("content_slots")
        if isinstance(content_slots, list):
            missing_slots = sorted(
                slot
                for slot in content_slots
                if isinstance(slot, str) and slot not in hinted_slots
            )
            if missing_slots:
                gap = {
                    "visual_id": visual_id,
                    "beat_id": beat_id,
                    "missing_g28_slot_hints": missing_slots,
                    "severity": "warning",
                    "review_implication": (
                        "Review Console should show these visual content slots as "
                        "unhinted before transfer planning."
                    ),
                }
                visual_slot_gaps.append(gap)
                warnings.append(
                    f"MISSING_G28_SLOT_HINT: {visual_id}->{','.join(missing_slots)}"
                )

        if not visual_hints:
            continue

        source_refs = _source_refs_for_visual(beat, visual_hints)
        unknown_sources = [ref for ref in source_refs if ref not in source_by_id]
        if unknown_sources:
            warnings.append(
                f"LINKAGE_UNKNOWN_SOURCE_REF: {visual_id}->{','.join(unknown_sources)}"
            )

        seen_slots: set[str] = set()
        for hint in visual_hints:
            slot_id = hint.get("slot_id")
            slot_name = hint.get("object_catalog_slot")
            if isinstance(slot_name, str):
                if slot_name in seen_slots:
                    warnings.append(f"DUPLICATE_G28_SLOT_HINT_FOR_VISUAL: {visual_id}->{slot_name}")
                seen_slots.add(slot_name)
            slot_allowed = isinstance(slot_name, str) and slot_name in allowed_slots
            review_surface = _review_surface_for_slot(
                visual.get("layout_candidate") if isinstance(visual.get("layout_candidate"), str) else None,
                slot_name if isinstance(slot_name, str) else "",
            )
            linkages.append({
                "beat_id": beat_id,
                "beat_intent": beat.get("intent") if beat else None,
                "visual_id": visual_id,
                "visualir_concept": visual.get("visualir_concept"),
                "layout_candidate": visual.get("layout_candidate"),
                "source_note_ids": source_refs,
                "source_refs_resolved": not unknown_sources,
                "slot_id": slot_id,
                "selected_g28_slot": slot_name,
                "slot_allowed": slot_allowed,
                "semantic_role": hint.get("semantic_role"),
                "text_budget": hint.get("text_budget"),
                "review_surface": review_surface,
                "review_implication": (
                    "Check object catalog role/caution, then use the reference layout "
                    "as a future read-only Review Console input."
                ),
                "downstream_readiness_implication": validation.transfer_status,
                "transfer_note": hint.get("transfer_note"),
                "production_visual_approval": False,
            })

    status = "failed" if errors else ("passed_with_warnings" if warnings else "passed")
    return NewsroomG28SlotLinkageProof(
        status=status,
        packet_path=str(packet_path) if packet_path is not None else None,
        artifact_id=validation.artifact_id,
        episode_id=validation.episode_id,
        contract_version=validation.contract_version,
        validator_status=validation.status,
        transfer_status=validation.transfer_status,
        ymm4_transfer_ready=validation.ymm4_transfer_ready,
        errors=errors,
        warnings=sorted(set(warnings)),
        blockers=validation.blockers,
        linkages=linkages,
        visual_slot_gaps=visual_slot_gaps,
        review_surface_index=G28_REVIEW_SURFACE_INDEX,
    )


def render_g28_slot_linkage_proof_markdown(
    proof: NewsroomG28SlotLinkageProof,
) -> str:
    """Render a compact Markdown proof for supervisor review."""
    lines: list[str] = [
        "# Newsroom G-28 Slot Linkage Proof",
        "",
        f"status: {proof.status}",
        f"validator_status: {proof.validator_status}",
        f"transfer_status: {proof.transfer_status}",
    ]
    if proof.packet_path:
        lines.append(f"packet_path: {proof.packet_path}")
    if proof.artifact_id:
        lines.append(f"artifact_id: {proof.artifact_id}")
    if proof.episode_id:
        lines.append(f"episode_id: {proof.episode_id}")
    if proof.contract_version:
        lines.append(f"contract_version: {proof.contract_version}")

    lines.extend([
        "",
        "## Linkages",
        "",
        "| Beat | Visual | Slot | Sources | Slot ok | Review surface | Transfer |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for item in proof.linkages:
        sources = ", ".join(item["source_note_ids"]) if item["source_note_ids"] else "none"
        slot_ok = "yes" if item["slot_allowed"] else "no"
        surface = item["review_surface"]["reference_layout"]
        lines.append(
            "| {beat} | {visual} | {slot} | {sources} | {slot_ok} | {surface} | {transfer} |".format(
                beat=item.get("beat_id") or "missing",
                visual=item.get("visual_id") or "missing",
                slot=item.get("selected_g28_slot") or "missing",
                sources=sources,
                slot_ok=slot_ok,
                surface=surface,
                transfer=item.get("downstream_readiness_implication") or "blocked",
            )
        )

    lines.extend(["", "## Visual Slot Gaps"])
    if proof.visual_slot_gaps:
        for gap in proof.visual_slot_gaps:
            lines.append(
                "- {visual_id}: missing hints for {slots}".format(
                    visual_id=gap["visual_id"],
                    slots=", ".join(gap["missing_g28_slot_hints"]),
                )
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Warnings"])
    if proof.warnings:
        for warning in proof.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")

    lines.extend(["", "## Errors"])
    if proof.errors:
        for error in proof.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")

    lines.extend(["", "## YMM4 Transfer Blockers"])
    if proof.blockers:
        for blocker in proof.blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This is diagnostic/readback only. It does not implement Review Console UI, "
        "create YMM4 artifacts, approve production visuals, fetch sources, or change rights state.",
        "",
        f"next_use: {proof.next_use}",
    ])
    return "\n".join(lines) + "\n"


def _append_transfer_blocker(
    blockers: dict[str, list[dict[str, Any]]],
    unlocks: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    *,
    category: str,
    code: str,
    detail: str,
    source_fields: list[str],
    unlock_requirement: str,
) -> None:
    key = (category, code)
    if key in seen:
        return
    seen.add(key)
    blockers.setdefault(category, []).append({
        "code": code,
        "detail": detail,
        "source_fields": source_fields,
    })
    unlocks.append({
        "category": category,
        "requirement": unlock_requirement,
        "current_state": detail,
        "source_fields": source_fields,
    })


def _readiness_true_fields(downstream_readiness: dict[str, Any]) -> list[str]:
    return sorted(
        key
        for key, value in downstream_readiness.items()
        if key.endswith("_ready") and value is True
    )


def build_newsroom_transfer_planning_proof(
    packet: dict[str, Any],
    slot_linkage_readback: dict[str, Any] | None,
    *,
    packet_path: str | Path | None = None,
    slot_linkage_path: str | Path | None = None,
    review_console_doc_path: str | Path | None = DEFAULT_REVIEW_CONSOLE_CONSUMER_DOC,
) -> NewsroomTransferPlanningProof:
    """Build a non-YMM4 transfer-planning proof from validated readbacks."""
    validation = validate_newsroom_handoff_packet(packet, packet_path=packet_path)
    errors = list(validation.errors)
    warnings = list(validation.warnings)
    blockers: dict[str, list[dict[str, Any]]] = {}
    unlocks: list[dict[str, Any]] = []
    seen_blockers: set[tuple[str, str]] = set()
    slot_linkage = slot_linkage_readback if isinstance(slot_linkage_readback, dict) else {}

    slot_linkage_status = slot_linkage.get("status")
    slot_linkage_transfer = slot_linkage.get("transfer_status")
    slot_validator_status = slot_linkage.get("validator_status")
    linkages = slot_linkage.get("linkages")
    if not slot_linkage:
        errors.append("SLOT_LINKAGE_READBACK_MISSING")
    if not isinstance(slot_linkage_status, str) or not slot_linkage_status:
        errors.append("SLOT_LINKAGE_STATUS_MISSING")
        slot_linkage_status = "missing"
    if not isinstance(slot_validator_status, str) or not slot_validator_status:
        errors.append("SLOT_LINKAGE_VALIDATOR_STATUS_MISSING")
    if not isinstance(slot_linkage_transfer, str) or not slot_linkage_transfer:
        errors.append("SLOT_LINKAGE_TRANSFER_STATUS_MISSING")
        slot_linkage_transfer = "blocked"
    if not isinstance(linkages, list):
        errors.append("SLOT_LINKAGE_ROWS_MISSING")
        linkages = []

    review_console_visibility_status = "not_checked"
    if review_console_doc_path:
        review_console_visibility_status = (
            "documented_read_only"
            if Path(review_console_doc_path).exists()
            else "doc_missing"
        )
        if review_console_visibility_status == "doc_missing":
            warnings.append(f"REVIEW_CONSOLE_CONSUMER_DOC_MISSING: {review_console_doc_path}")

    rights = packet.get("rights_summary") if isinstance(packet.get("rights_summary"), dict) else {}
    provenance = packet.get("provenance") if isinstance(packet.get("provenance"), dict) else {}
    downstream = (
        packet.get("downstream_readiness")
        if isinstance(packet.get("downstream_readiness"), dict)
        else {}
    )
    review_warnings = packet.get("review_warnings") if isinstance(packet.get("review_warnings"), list) else []
    visual_plan = packet.get("visual_plan") if isinstance(packet.get("visual_plan"), list) else []
    source_notes = packet.get("source_notes") if isinstance(packet.get("source_notes"), list) else []

    clearance_state = rights.get("clearance_state")
    if clearance_state != "cleared":
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="rights/provenance",
            code="rights_clearance_not_cleared",
            detail=f"rights_summary.clearance_state={clearance_state or 'missing'}",
            source_fields=["rights_summary.clearance_state"],
            unlock_requirement=(
                "Record cleared rights or an explicit limited-use clearance before "
                "any transfer candidate review."
            ),
        )
    blocked_uses = rights.get("blocked_uses")
    if isinstance(blocked_uses, list) and "YMM4_transfer" in blocked_uses:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="rights/provenance",
            code="rights_summary_blocks_ymm4_transfer",
            detail="rights_summary.blocked_uses includes YMM4_transfer",
            source_fields=["rights_summary.blocked_uses"],
            unlock_requirement=(
                "Remove YMM4_transfer from blocked uses only after rights/provenance "
                "review permits a limited downstream handoff."
            ),
        )
    risk_flags = rights.get("risk_flags")
    if isinstance(risk_flags, list) and risk_flags:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="rights/provenance",
            code="rights_risk_flags_present",
            detail=f"rights_summary.risk_flags={','.join(str(flag) for flag in risk_flags)}",
            source_fields=["rights_summary.risk_flags"],
            unlock_requirement="Resolve or explicitly waive rights risk flags before transfer planning.",
        )
    if provenance.get("raw_source_material_included") is not True:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="media/source availability",
            code="raw_source_material_not_included",
            detail="provenance.raw_source_material_included is false or missing",
            source_fields=["provenance.raw_source_material_included"],
            unlock_requirement=(
                "Provide approved source media metadata or approved abstract replacement "
                "evidence before limited transfer can be considered."
            ),
        )
    placeholder_sources = [
        note.get("source_id", "<missing>")
        for note in source_notes
        if isinstance(note, dict)
        and (
            str(note.get("source_kind", "")).startswith("placeholder")
            or _is_non_empty_string(note.get("non_fetching_reference"))
        )
    ]
    if placeholder_sources:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="media/source availability",
            code="placeholder_source_notes_only",
            detail=f"placeholder source notes: {','.join(placeholder_sources)}",
            source_fields=["source_notes"],
            unlock_requirement=(
                "Replace placeholder-only source notes with approved, sanitized packet "
                "metadata from the upstream newsroom export."
            ),
        )

    for warning in review_warnings:
        if not isinstance(warning, dict):
            continue
        if warning.get("blocks_ymm4_transfer") is True:
            warning_id = warning.get("warning_id", "<missing>")
            _append_transfer_blocker(
                blockers,
                unlocks,
                seen_blockers,
                category="review approval",
                code=f"review_warning_blocks_transfer:{warning_id}",
                detail=str(warning.get("message") or warning_id),
                source_fields=[f"review_warnings.{warning_id}"],
                unlock_requirement=(
                    "Resolve the blocking review warning and record a freeform human "
                    "review outcome before transfer-candidate review."
                ),
            )
    _append_transfer_blocker(
        blockers,
        unlocks,
        seen_blockers,
        category="review approval",
        code="review_console_is_read_only",
        detail=f"review_console_visibility_status={review_console_visibility_status}",
        source_fields=[str(review_console_doc_path) if review_console_doc_path else "review_console"],
        unlock_requirement=(
            "Add a separate planning approval/readiness outcome; the current Review "
            "Console consumer is visibility only."
        ),
    )

    placeholder_visuals = [
        visual.get("visual_id", "<missing>")
        for visual in visual_plan
        if isinstance(visual, dict) and visual.get("asset_policy") == "placeholder_only"
    ]
    if placeholder_visuals:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="visual readiness",
            code="visual_assets_placeholder_only",
            detail=f"placeholder visuals: {','.join(placeholder_visuals)}",
            source_fields=["visual_plan.asset_policy"],
            unlock_requirement=(
                "Replace placeholder-only visual plans with approved media, approved "
                "abstract replacements, or an explicit no-media visual route."
            ),
        )
    visual_slot_gaps = (
        slot_linkage.get("visual_slot_gaps")
        if isinstance(slot_linkage.get("visual_slot_gaps"), list)
        else []
    )
    if visual_slot_gaps:
        gap_ids = [
            gap.get("visual_id", "<missing>")
            for gap in visual_slot_gaps
            if isinstance(gap, dict)
        ]
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="visual readiness",
            code="visual_slot_gaps_present",
            detail=f"visuals with unhinted slots: {','.join(gap_ids)}",
            source_fields=["g28_slot_linkage_readback.visual_slot_gaps"],
            unlock_requirement=(
                "Close or explicitly defer unhinted visual content slots before "
                "transfer-candidate review."
            ),
        )
    if linkages and any(item.get("production_visual_approval") is not False for item in linkages if isinstance(item, dict)):
        warnings.append("PRODUCTION_VISUAL_APPROVAL_FIELD_NOT_FALSE")

    if validation.transfer_status == "blocked":
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="downstream/YMM4 readiness",
            code="validator_transfer_status_blocked",
            detail="validator transfer_status=blocked",
            source_fields=["validator.transfer_status"],
            unlock_requirement="Clear validator blockers before any limited transfer can be considered.",
        )
    if slot_linkage_transfer == "blocked":
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="downstream/YMM4 readiness",
            code="slot_linkage_transfer_status_blocked",
            detail="slot-linkage transfer_status=blocked",
            source_fields=["g28_slot_linkage_readback.transfer_status"],
            unlock_requirement="Clear slot-linkage blockers and warnings before transfer-candidate review.",
        )
    downstream_ready = downstream.get("ymm4_transfer_ready")
    if downstream_ready is not True:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="downstream/YMM4 readiness",
            code="ymm4_transfer_ready_false",
            detail=f"downstream_readiness.ymm4_transfer_ready={_bool_label(downstream_ready)}",
            source_fields=["downstream_readiness.ymm4_transfer_ready"],
            unlock_requirement=(
                "Keep YMM4 transfer closed until all upstream rights, media, review, "
                "visual, and slot-linkage blockers are resolved."
            ),
        )
    blocking_reasons = downstream.get("blocking_reasons")
    if isinstance(blocking_reasons, list) and blocking_reasons:
        _append_transfer_blocker(
            blockers,
            unlocks,
            seen_blockers,
            category="downstream/YMM4 readiness",
            code="downstream_blocking_reasons_present",
            detail=f"blocking_reasons={','.join(str(reason) for reason in blocking_reasons)}",
            source_fields=["downstream_readiness.blocking_reasons"],
            unlock_requirement="Remove downstream blocking reasons only after their source blockers are resolved.",
        )

    proof_ready_claim = (
        validation.ymm4_transfer_ready is True
        or slot_linkage.get("ymm4_transfer_ready") is True
        or slot_linkage_transfer == "ready"
        or downstream_ready is True
    )
    has_any_blockers = any(blockers.values())
    contradiction_checks: list[dict[str, Any]] = []
    def add_check(name: str, status: str, severity: str, detail: str) -> None:
        contradiction_checks.append({
            "check": name,
            "status": status,
            "severity": severity,
            "detail": detail,
        })

    if proof_ready_claim and has_any_blockers:
        errors.append("TRANSFER_READY_CONTRADICTS_BLOCKERS")
        add_check(
            "transfer_ready_with_blockers",
            "fail",
            "error",
            "A ready transfer claim exists while transfer blockers remain.",
        )
    else:
        add_check(
            "transfer_ready_with_blockers",
            "pass",
            "info",
            "No ready transfer claim conflicts with current blockers.",
        )

    rights_media_blocked = bool(blockers.get("rights/provenance")) or bool(
        blockers.get("media/source availability")
    )
    true_readiness_fields = _readiness_true_fields(downstream)
    if rights_media_blocked and true_readiness_fields:
        warning = "READINESS_TRUE_WITH_RIGHTS_OR_MEDIA_BLOCKERS"
        if warning not in warnings:
            warnings.append(warning)
        add_check(
            "rights_media_missing_but_readiness_claims_true",
            "warn",
            "warning",
            f"Readiness fields true while rights/media blockers remain: {','.join(true_readiness_fields)}",
        )
    else:
        add_check(
            "rights_media_missing_but_readiness_claims_true",
            "pass",
            "info",
            "No rights/media contradiction detected.",
        )

    production_implied = any(
        isinstance(item, dict) and item.get("production_visual_approval") is True
        for item in linkages
    )
    if production_implied and blockers.get("review approval"):
        errors.append("PRODUCTION_TRANSFER_IMPLIED_WITHOUT_REVIEW_APPROVAL")
        add_check(
            "review_approval_absent_but_production_transfer_implied",
            "fail",
            "error",
            "A production visual approval claim exists while review approval blockers remain.",
        )
    else:
        add_check(
            "review_approval_absent_but_production_transfer_implied",
            "pass",
            "info",
            "No production transfer approval is implied.",
        )

    slot_linkage_invalid = any(
        error.startswith("SLOT_LINKAGE_")
        for error in errors
    )
    add_check(
        "slot_linkage_readback_required",
        "fail" if slot_linkage_invalid else "pass",
        "error" if slot_linkage_invalid else "info",
        "Slot-linkage readback is missing required status fields."
        if slot_linkage_invalid
        else "Slot-linkage readback exposes status, transfer status, and rows.",
    )

    unique_errors = sorted(set(errors))
    unique_warnings = sorted(set(warnings + list(slot_linkage.get("warnings", []))))
    transfer_status = "blocked" if unique_errors or has_any_blockers else "candidate"
    status = "failed" if unique_errors else transfer_status
    candidate_summary = (
        "Not a transfer candidate yet: transfer remains blocked until rights, "
        "media/source availability, review approval, visual readiness, and "
        "downstream/YMM4 readiness blockers are cleared."
        if transfer_status == "blocked"
        else "Candidate for limited transfer review; no current blockers were found."
    )

    return NewsroomTransferPlanningProof(
        status=status,
        transfer_status=transfer_status,
        packet_path=str(packet_path) if packet_path is not None else None,
        slot_linkage_path=str(slot_linkage_path) if slot_linkage_path is not None else None,
        review_console_doc_path=(
            str(review_console_doc_path) if review_console_doc_path is not None else None
        ),
        artifact_id=validation.artifact_id,
        episode_id=validation.episode_id,
        title=packet.get("title") if isinstance(packet.get("title"), str) else None,
        contract_version=validation.contract_version,
        validator_status=validation.status,
        slot_linkage_status=str(slot_linkage_status),
        review_console_visibility_status=review_console_visibility_status,
        ymm4_transfer_ready=validation.ymm4_transfer_ready,
        transfer_candidate_summary=candidate_summary,
        transfer_blockers=blockers,
        unlock_requirements=unlocks,
        contradiction_checks=contradiction_checks,
        prohibited_next_actions=list(NEWSROOM_TRANSFER_PROHIBITED_NEXT_ACTIONS),
        allowed_next_actions=list(NEWSROOM_TRANSFER_ALLOWED_NEXT_ACTIONS),
        input_counts={
            **validation.counts,
            "slot_linkage_rows": len(linkages),
            "visual_slot_gaps": len(visual_slot_gaps),
        },
        errors=unique_errors,
        warnings=unique_warnings,
    )


def render_newsroom_transfer_planning_markdown(
    proof: NewsroomTransferPlanningProof,
) -> str:
    """Render a human-readable transfer-planning proof."""
    lines: list[str] = [
        "# Newsroom Transfer Planning Proof",
        "",
        f"status: {proof.status}",
        f"transfer_status: {proof.transfer_status}",
        f"validator_status: {proof.validator_status}",
        f"slot_linkage_status: {proof.slot_linkage_status}",
        f"review_console_visibility_status: {proof.review_console_visibility_status}",
    ]
    if proof.packet_path:
        lines.append(f"packet_path: {proof.packet_path}")
    if proof.slot_linkage_path:
        lines.append(f"slot_linkage_path: {proof.slot_linkage_path}")
    if proof.review_console_doc_path:
        lines.append(f"review_console_doc_path: {proof.review_console_doc_path}")
    if proof.artifact_id:
        lines.append(f"artifact_id: {proof.artifact_id}")
    if proof.episode_id:
        lines.append(f"episode_id: {proof.episode_id}")
    if proof.title:
        lines.append(f"title: {proof.title}")
    if proof.contract_version:
        lines.append(f"contract_version: {proof.contract_version}")

    lines.extend([
        "",
        "## Transfer Candidate Summary",
        "",
        proof.transfer_candidate_summary,
        "",
        "## Input Counts",
    ])
    for key, value in sorted(proof.input_counts.items()):
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Transfer Blockers"])
    if proof.transfer_blockers:
        for category, items in proof.transfer_blockers.items():
            lines.append(f"### {category}")
            for item in items:
                fields = ", ".join(item.get("source_fields", []))
                lines.append(f"- {item['code']}: {item['detail']} ({fields})")
    else:
        lines.append("- none")

    lines.extend(["", "## Unlock Requirements"])
    if proof.unlock_requirements:
        for item in proof.unlock_requirements:
            fields = ", ".join(item.get("source_fields", []))
            lines.append(
                f"- [{item['category']}] {item['requirement']} "
                f"(current: {item['current_state']}; fields: {fields})"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Contradiction Checks"])
    for check in proof.contradiction_checks:
        lines.append(
            f"- {check['check']}: {check['status']} / {check['severity']} - {check['detail']}"
        )

    lines.extend(["", "## Prohibited Next Actions"])
    for action in proof.prohibited_next_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Allowed Next Actions"])
    for action in proof.allowed_next_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Errors"])
    if proof.errors:
        for error in proof.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")

    lines.extend(["", "## Warnings"])
    if proof.warnings:
        for warning in proof.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This proof is diagnostic planning only. It does not generate `.ymmp`, "
        "YMM4 carriers, renders, external fetches, production approvals, rights "
        "approvals, or publication outputs.",
        "",
        f"next_use: {proof.next_use}",
    ])
    return "\n".join(lines) + "\n"

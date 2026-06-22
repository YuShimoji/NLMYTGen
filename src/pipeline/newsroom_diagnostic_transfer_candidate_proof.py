"""Diagnostic transfer-candidate proof for newsroom caption artifacts.

This module separates production/YMM4 transfer blockage from a smaller
synthetic neutral-timeline import possibility. It does not ingest real packets,
fetch sources, create media, generate TTS, write YMM4 projects, render output,
or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_copy_refinement import DEFAULT_COPY_REFINEMENT_PATH
from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH
from src.pipeline.newsroom_episode_production_capsule import (
    DEFAULT_CAPSULE_PATH,
    DEFAULT_PRIOR_TRANSFER_PLANNING_PATH,
    load_json_object,
)


DIAGNOSTIC_TRANSFER_PROOF_SCHEMA_VERSION = (
    "newsroom_diagnostic_transfer_candidate_proof.v1"
)
DIAGNOSTIC_TRANSFER_PROOF_ID = (
    "newsroom_diagnostic_transfer_candidate_proof_v1_2026_06_22"
)
DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH = Path(
    "samples/_probe/newsroom_handoff/diagnostic_transfer_candidate_proof_v1.json"
)
DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_DOC_PATH = Path(
    "docs/verification/NEWSROOM_DIAGNOSTIC_TRANSFER_CANDIDATE_PROOF_V1_2026-06-22.md"
)

CLASSIFICATION_ORDER: tuple[str, ...] = (
    "production_only",
    "diagnostic_hard_blocker",
    "diagnostic_soft_warning",
    "already_satisfied_for_synthetic",
)

BLOCKER_CLASSIFICATIONS: dict[str, dict[str, str]] = {
    "rights_clearance_not_cleared": {
        "classification": "production_only",
        "diagnostic_effect": (
            "Blocks production, publication, and downstream handoff; a synthetic "
            "neutral import proof can continue without rights clearance because it "
            "uses only fake placeholders."
        ),
        "next_requirement": "Keep production transfer closed until rights are cleared.",
    },
    "rights_summary_blocks_ymm4_transfer": {
        "classification": "production_only",
        "diagnostic_effect": (
            "Explicitly blocks YMM4 transfer, not the smaller neutral timeline proof."
        ),
        "next_requirement": "Do not remove the YMM4 block in this slice.",
    },
    "rights_risk_flags_present": {
        "classification": "production_only",
        "diagnostic_effect": (
            "Risk flags remain decisive for production and public use, but the "
            "diagnostic proof avoids real media and real claims."
        ),
        "next_requirement": "Resolve risk flags before any production transfer review.",
    },
    "raw_source_material_not_included": {
        "classification": "diagnostic_soft_warning",
        "diagnostic_effect": (
            "No real source material exists. The synthetic proof can proceed with "
            "placeholder rows, but later media-backed import work still needs assets."
        ),
        "next_requirement": "Keep the next proof neutral and no-media.",
    },
    "placeholder_source_notes_only": {
        "classification": "diagnostic_soft_warning",
        "diagnostic_effect": (
            "Source notes are placeholders only. They are enough for synthetic "
            "row references, not for production provenance."
        ),
        "next_requirement": "Map placeholder source refs as diagnostic strings only.",
    },
    "review_warning_blocks_transfer:warning_fake_rights_hold": {
        "classification": "production_only",
        "diagnostic_effect": (
            "The warning blocks production transfer and publication, while this "
            "proof remains synthetic and non-approving."
        ),
        "next_requirement": "Do not treat this proof as a rights review outcome.",
    },
    "review_warning_blocks_transfer:warning_fake_no_production_readiness": {
        "classification": "production_only",
        "diagnostic_effect": (
            "The warning correctly denies production readiness; it does not deny "
            "a no-media diagnostic import field mapping."
        ),
        "next_requirement": "Keep the production readiness flag false.",
    },
    "review_console_is_read_only": {
        "classification": "already_satisfied_for_synthetic",
        "diagnostic_effect": (
            "A read-only review surface is sufficient evidence for this diagnostic "
            "proof because no approval or editing workflow is required."
        ),
        "next_requirement": "No extra human judgement is required for this slice.",
    },
    "visual_slot_gaps_present": {
        "classification": "diagnostic_soft_warning",
        "diagnostic_effect": (
            "Visual slots still lack downstream geometry. A neutral proof can carry "
            "visual ids, layout hints, and warning flags without claiming YMM4 fit."
        ),
        "next_requirement": "Carry slot warnings into the next neutral timeline proof.",
    },
    "validator_transfer_status_blocked": {
        "classification": "production_only",
        "diagnostic_effect": (
            "The validator keeps production transfer blocked; it does not prevent "
            "a separate synthetic-only import candidate proof."
        ),
        "next_requirement": "Do not override validator transfer_status.",
    },
    "slot_linkage_transfer_status_blocked": {
        "classification": "diagnostic_soft_warning",
        "diagnostic_effect": (
            "Slot linkage blocks YMM4 transfer. The next proof can still list slots "
            "as neutral metadata with warnings attached."
        ),
        "next_requirement": "Keep the next artifact neutral until slot linkage is cleared.",
    },
    "ymm4_transfer_ready_false": {
        "classification": "production_only",
        "diagnostic_effect": (
            "YMM4 transfer readiness is false by design. This proof does not create "
            "a YMM4 candidate."
        ),
        "next_requirement": "Do not emit YMM4 carrier or project files.",
    },
    "downstream_blocking_reasons_present": {
        "classification": "diagnostic_soft_warning",
        "diagnostic_effect": (
            "Downstream reasons remain useful warnings for the neutral proof, but "
            "they are not hard blockers while no downstream import is produced."
        ),
        "next_requirement": "Repeat the blocking reasons in the next proof's boundary.",
    },
}


def build_default_newsroom_diagnostic_transfer_candidate_proof(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed diagnostic transfer-candidate proof."""
    base = Path(root) if root is not None else Path(".")
    capsule = load_json_object(base / DEFAULT_CAPSULE_PATH)
    timing_plan = load_json_object(base / DEFAULT_PLAN_PATH)
    caption_copy = load_json_object(base / DEFAULT_COPY_REFINEMENT_PATH)
    prior_transfer = load_json_object(base / DEFAULT_PRIOR_TRANSFER_PLANNING_PATH)
    return build_newsroom_diagnostic_transfer_candidate_proof(
        capsule,
        timing_plan,
        caption_copy,
        prior_transfer_planning=prior_transfer,
        capsule_path=DEFAULT_CAPSULE_PATH,
        timing_plan_path=DEFAULT_PLAN_PATH,
        caption_copy_path=DEFAULT_COPY_REFINEMENT_PATH,
        prior_transfer_planning_path=DEFAULT_PRIOR_TRANSFER_PLANNING_PATH,
    )


def build_newsroom_diagnostic_transfer_candidate_proof(
    capsule: dict[str, Any],
    timing_plan: dict[str, Any],
    caption_copy: dict[str, Any],
    *,
    prior_transfer_planning: dict[str, Any] | None = None,
    capsule_path: str | Path | None = None,
    timing_plan_path: str | Path | None = None,
    caption_copy_path: str | Path | None = None,
    prior_transfer_planning_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic synthetic diagnostic import-readiness proof."""
    transfer = _dict(capsule.get("transfer_status"))
    episode = _dict(capsule.get("episode"))
    timing_summary = _dict(timing_plan.get("episode_timing_summary"))
    audio = _dict(caption_copy.get("audio_readiness"))
    rows = _classification_rows(_dict(transfer.get("blockers")))
    summary = _classification_summary(rows)
    requirements = _minimal_import_requirements(
        episode,
        timing_plan,
        caption_copy,
    )

    return {
        "artifact_id": DIAGNOSTIC_TRANSFER_PROOF_ID,
        "schema_version": DIAGNOSTIC_TRANSFER_PROOF_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "review_axis": "diagnostic_transfer_candidate_scope",
        "diagnostic_only": True,
        "production_status": "diagnostic_transfer_candidate_proof_only",
        "source": {
            "capsule_path": _path_text(capsule_path),
            "capsule_artifact_id": capsule.get("artifact_id"),
            "timing_plan_path": _path_text(timing_plan_path),
            "timing_plan_artifact_id": timing_plan.get("artifact_id"),
            "caption_copy_path": _path_text(caption_copy_path),
            "caption_copy_artifact_id": caption_copy.get("artifact_id"),
            "prior_transfer_planning_path": _path_text(prior_transfer_planning_path),
            "prior_transfer_planning_status": _dict(prior_transfer_planning).get("status"),
            "prior_transfer_planning_blocker_count": _dict(prior_transfer_planning).get(
                "blocker_count"
            ),
            "episode_id": episode.get("episode_id"),
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scopes": [
                "diagnostic episode capsule",
                "diagnostic caption/timing plan",
                "diagnostic caption copy refinement",
            ],
            "not_accepted_scope": [
                "production transfer",
                "YMM4 transfer",
                "render",
                "TTS or narration approval",
                "real packet ingest",
                "public video",
            ],
            "current_review_axis": "diagnostic_transfer_candidate_scope",
            "next_nonredundant_axis": "neutral_import_field_mapping",
            "repeated_general_caption_or_timing_review_allowed": False,
        },
        "decision_split": {
            "question": (
                "Can a synthetic, non-production diagnostic import proof be opened "
                "next without violating current blockers?"
            ),
            "answer": "yes_for_synthetic_neutral_timeline_candidate",
            "production_transfer_status": "blocked",
            "production_YMM4_candidate": False,
            "diagnostic_import_status": "candidate_with_placeholders",
            "diagnostic_import_candidate": True,
            "diagnostic_import_scope": "neutral timeline JSON or caption CSV only",
            "why": [
                "Existing blockers still close production and YMM4 transfer.",
                "Caption units, timing windows, refined copy, and visual placeholder refs exist.",
                "No real media, audio, external fetch, render, or project carrier is needed.",
            ],
        },
        "video_readiness": {
            "episode_id": episode.get("episode_id"),
            "total_duration_sec": timing_summary.get("total_duration_sec"),
            "beat_count": timing_summary.get("beat_count"),
            "caption_unit_count": timing_summary.get("caption_unit_count"),
            "visual_count": timing_summary.get("visual_count"),
            "timing_status": timing_summary.get("timing_confidence"),
            "caption_copy_status": _dict(caption_copy.get("caption_copy_summary")).get(
                "copy_status"
            ),
            "audio_status": audio.get("voice_status"),
            "TTS_generated": False,
            "production_video_ready": False,
            "diagnostic_neutral_import_candidate": True,
        },
        "production_transfer_blockage": {
            "transfer_status": transfer.get("transfer_status"),
            "YMM4_candidate": False,
            "blocker_count": transfer.get("blocker_count"),
            "unlock_requirement_count": transfer.get("unlock_requirement_count"),
            "kept_closed_reason": (
                "Rights/provenance, media/source, review, visual, and downstream "
                "transfer blockers remain active for production and YMM4 transfer."
            ),
        },
        "diagnostic_import_possibility": {
            "status": "open_next_as_synthetic_candidate",
            "candidate": True,
            "hard_blocker_count": summary["diagnostic_hard_blocker"],
            "candidate_reason": (
                "The next proof can be a neutral timeline mapping over existing fake "
                "caption rows and visual placeholders, without producing downstream media."
            ),
        },
        "blocker_classification_summary": summary,
        "blocker_classifications": rows,
        "minimal_import_requirements": requirements,
        "next_tiny_importable_proof_plan": _next_tiny_importable_proof_plan(),
        "review_card": {
            "status": "none",
            "reason": (
                "No user judgement is required because this slice only classifies "
                "whether a synthetic diagnostic proof may be opened."
            ),
            "not_asking": (
                "No production readiness, rights approval, or repeated caption/timing "
                "review is requested."
            ),
        },
        "prohibited_next_actions": [
            ".ymmp generation",
            "YMM4 carrier generation",
            "render generation",
            "TTS generation",
            "real packet ingest",
            "real source fetch",
            "real URL access",
            "media download",
            "external fetch",
            "production approval",
            "rights approval",
            "public-use approval",
            "publishing",
        ],
        "boundary_assertions": {
            "diagnostic_only": True,
            "opens_production_transfer": False,
            "opens_YMM4_transfer": False,
            "diagnostic_candidate_only": True,
            "contains_real_news_claims": False,
            "contains_real_names": False,
            "contains_real_urls": False,
            "real_packet_ingested": False,
            "real_source_fetch_performed": False,
            "external_media_downloaded": False,
            "tts_generated": False,
            "ymmp_generated": False,
            "ymm4_carrier_generated": False,
            "render_generated": False,
            "production_approval": False,
            "public_video": False,
        },
    }


def render_newsroom_diagnostic_transfer_candidate_proof_markdown(
    proof: dict[str, Any],
) -> str:
    """Render a human-readable readback for the diagnostic transfer proof."""
    decision = _dict(proof.get("decision_split"))
    production = _dict(proof.get("production_transfer_blockage"))
    diagnostic = _dict(proof.get("diagnostic_import_possibility"))
    summary = _dict(proof.get("blocker_classification_summary"))
    requirements = _dict(proof.get("minimal_import_requirements"))
    plan = _dict(proof.get("next_tiny_importable_proof_plan"))
    video = _dict(proof.get("video_readiness"))
    review_memory = _dict(proof.get("review_memory"))

    lines = [
        "# Newsroom Diagnostic Transfer Candidate Proof v1",
        "",
        f"artifact_id: {proof.get('artifact_id')}",
        f"schema_version: {proof.get('schema_version')}",
        f"review_status: {proof.get('review_status')}",
        f"review_axis: {proof.get('review_axis')}",
        f"production_status: {proof.get('production_status')}",
        "diagnostic_only: true",
        "",
        "## Decision Split",
        "",
        f"question: {decision.get('question')}",
        f"answer: {decision.get('answer')}",
        "",
        "| route | current status | decision |",
        "|---|---|---|",
        (
            "| production/YMM4 transfer | "
            f"{decision.get('production_transfer_status')} | keep closed |"
        ),
        (
            "| synthetic diagnostic import | "
            f"{decision.get('diagnostic_import_status')} | open next proof only |"
        ),
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- current_review_axis: {review_memory.get('current_review_axis')}",
        f"- next_nonredundant_axis: {review_memory.get('next_nonredundant_axis')}",
        "- repeated_general_caption_or_timing_review_allowed: false",
        "",
        "## Video Readiness",
        "",
        "| area | status | note |",
        "|---|---|---|",
        f"| timing | {video.get('timing_status')} | {video.get('total_duration_sec')} seconds |",
        (
            "| captions | "
            f"{video.get('caption_copy_status')} | {video.get('caption_unit_count')} units |"
        ),
        f"| visuals | placeholder_refs | {video.get('visual_count')} visual rows |",
        f"| audio | {video.get('audio_status')} | TTS_generated=false |",
        "| production video | blocked | no approval, media, render, or carrier |",
        "| diagnostic import | candidate_with_placeholders | neutral JSON/CSV only |",
        "",
        "## Production Blockage",
        "",
        f"- transfer_status: {production.get('transfer_status')}",
        f"- YMM4_candidate: {str(production.get('YMM4_candidate')).lower()}",
        f"- blocker_count: {production.get('blocker_count')}",
        f"- unlock_requirement_count: {production.get('unlock_requirement_count')}",
        f"- kept_closed_reason: {production.get('kept_closed_reason')}",
        "",
        "## Diagnostic Possibility",
        "",
        f"- status: {diagnostic.get('status')}",
        f"- candidate: {str(diagnostic.get('candidate')).lower()}",
        f"- hard_blocker_count: {diagnostic.get('hard_blocker_count')}",
        f"- candidate_reason: {diagnostic.get('candidate_reason')}",
        "",
        "## Blocker Classification Summary",
        "",
        "| classification | count |",
        "|---|---:|",
    ]
    for key in CLASSIFICATION_ORDER:
        lines.append(f"| {key} | {summary.get(key)} |")

    lines.extend([
        f"| total_blockers | {summary.get('total_blockers')} |",
        "",
        "## Blocker Classifications",
        "",
        "| blocker | original category | classification | diagnostic effect |",
        "|---|---|---|---|",
    ])
    for row in proof.get("blocker_classifications", []):
        lines.append(
            f"| {row['code']} | {row['original_category']} | "
            f"{row['classification']} | {row['diagnostic_effect']} |"
        )

    lines.extend([
        "",
        "## Minimal Import Requirements",
        "",
        f"all_minimal_requirements_met: {str(requirements.get('all_minimal_requirements_met')).lower()}",
        f"missing_fields_for_synthetic_candidate: {', '.join(requirements.get('missing_fields_for_synthetic_candidate', [])) or 'none'}",
        "",
        "| requirement | status | source |",
        "|---|---|---|",
    ])
    for row in requirements.get("requirements", []):
        lines.append(f"| {row['requirement']} | {row['status']} | {row['source']} |")

    lines.extend([
        "",
        "Required next fields before a concrete import file:",
    ])
    for field in requirements.get("required_next_fields_before_importable_proof", []):
        lines.append(f"- {field}")

    lines.extend([
        "",
        "## Next Tiny Importable Proof Plan",
        "",
        f"- recommended_next_slice: {plan.get('recommended_next_slice')}",
        f"- objective: {plan.get('objective')}",
        "- output_candidates:",
    ])
    for candidate in plan.get("output_candidates", []):
        lines.append(f"  - {candidate}")
    lines.append("- exact_fields_to_map_next:")
    for field in plan.get("exact_fields_to_map_next", []):
        lines.append(f"  - {field['field']}: {field['source']}")
    lines.append("- acceptance_checks:")
    for check in plan.get("acceptance_checks", []):
        lines.append(f"  - {check}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This slice only opens a synthetic diagnostic proof lane; "
        "it does not ask for production, rights, YMM4, caption, or timing approval.",
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only. It does not create `.ymmp`, YMM4 carriers, "
        "renders, TTS/audio, external fetches, real packet ingestion, real source access, "
        "media downloads, production approvals, rights approvals, public-use approvals, "
        "or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _classification_rows(blockers: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for category, raw_blockers in blockers.items():
        for blocker in _list(raw_blockers):
            code = str(blocker.get("code") or "")
            classification = BLOCKER_CLASSIFICATIONS.get(
                code,
                {
                    "classification": "diagnostic_hard_blocker",
                    "diagnostic_effect": (
                        "Unknown blocker code; treat as hard blocker until classified."
                    ),
                    "next_requirement": "Classify this blocker before opening an import proof.",
                },
            )
            rows.append({
                "code": code,
                "original_category": category,
                "detail": blocker.get("detail"),
                "source_fields": _string_list(blocker.get("source_fields")),
                "classification": classification["classification"],
                "diagnostic_effect": classification["diagnostic_effect"],
                "next_requirement": classification["next_requirement"],
            })
    return rows


def _classification_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {key: 0 for key in CLASSIFICATION_ORDER}
    for row in rows:
        classification = row.get("classification")
        if classification in counts:
            counts[str(classification)] += 1
    counts["total_blockers"] = len(rows)
    counts["diagnostic_hard_blocker_codes"] = [
        row["code"]
        for row in rows
        if row.get("classification") == "diagnostic_hard_blocker"
    ]
    return counts


def _minimal_import_requirements(
    episode: dict[str, Any],
    timing_plan: dict[str, Any],
    caption_copy: dict[str, Any],
) -> dict[str, Any]:
    caption_units = _list(caption_copy.get("refined_caption_units"))
    beat_timing = _list(timing_plan.get("beat_timing"))
    visual_timing = _list(timing_plan.get("visual_timing"))
    requirements = [
        {
            "requirement": "episode identity",
            "status": _available_status(episode.get("episode_id")),
            "source": "capsule.episode.episode_id",
        },
        {
            "requirement": "beat timing windows",
            "status": _available_status(beat_timing),
            "source": "caption_timing_plan.beat_timing",
        },
        {
            "requirement": "caption unit timing",
            "status": _available_status(caption_units),
            "source": "caption_copy.refined_caption_units",
        },
        {
            "requirement": "refined caption text",
            "status": _available_status(
                [unit for unit in caption_units if unit.get("refined_caption_text")]
            ),
            "source": "caption_copy.refined_caption_units[].refined_caption_text",
        },
        {
            "requirement": "visual placeholder references",
            "status": _available_status(visual_timing),
            "source": "caption_timing_plan.visual_timing",
        },
        {
            "requirement": "no-audio/no-media boundary",
            "status": "available",
            "source": "caption_copy.boundary_assertions",
        },
    ]
    missing = [
        row["requirement"]
        for row in requirements
        if row["status"] != "available"
    ]
    return {
        "candidate_scope": "synthetic_neutral_timeline_import",
        "all_minimal_requirements_met": not missing,
        "requirements": requirements,
        "missing_fields_for_synthetic_candidate": missing,
        "audio_required_for_synthetic_candidate": False,
        "media_required_for_synthetic_candidate": False,
        "YMM4_specific_mapping_required_next": True,
        "required_next_fields_before_importable_proof": [
            "neutral import schema name and version",
            "track_kind for caption and visual-placeholder rows",
            "row ordering and stable row ids",
            "placeholder asset policy for visual rows",
            "explicit no-audio and no-media flags",
            "slot warning carry-forward field",
        ],
        "non_requirements_for_synthetic_candidate": [
            "TTS or narration audio",
            "real media assets",
            "real source material",
            "YMM4 project carrier",
            "render output",
            "production approval",
        ],
    }


def _next_tiny_importable_proof_plan() -> dict[str, Any]:
    return {
        "recommended_next_slice": "newsroom-neutral-timeline-import-proof-v1",
        "objective": (
            "Emit a tiny neutral timeline proof from existing capsule, timing, and "
            "caption-copy artifacts without creating downstream media."
        ),
        "output_candidates": [
            "neutral_timeline_json",
            "optional_caption_csv",
        ],
        "exact_fields_to_map_next": [
            {
                "field": "episode_id",
                "source": "capsule.episode.episode_id",
            },
            {
                "field": "beat_id/start_sec/end_sec/duration_sec",
                "source": "caption_timing_plan.beat_timing",
            },
            {
                "field": "caption_id/refined_caption_text/line_count_target/max_chars_target",
                "source": "caption_copy.refined_caption_units",
            },
            {
                "field": "reading_density",
                "source": "caption_copy.refined_caption_units",
            },
            {
                "field": "visual_id/g28_slot/layout_hint/caption_interference_risk",
                "source": "caption_timing_plan.visual_timing",
            },
            {
                "field": "diagnostic_only/no_audio/no_media/no_render",
                "source": "boundary assertions",
            },
            {
                "field": "production_transfer_status",
                "source": "capsule.transfer_status.transfer_status",
            },
        ],
        "acceptance_checks": [
            "JSON parses and row counts match source caption/visual rows.",
            "Production transfer remains blocked and YMM4_candidate remains false.",
            "No audio, media, render, carrier, or project files are created.",
            "No real packet ingest, external fetch, or real source access is performed.",
        ],
        "prohibited_outputs": [
            ".ymmp project",
            "YMM4 carrier",
            "render output",
            "TTS or audio output",
            "real source packet ingest",
            "external fetch",
        ],
    }


def _available_status(value: Any) -> str:
    if isinstance(value, list):
        return "available" if value else "missing"
    return "available" if value else "missing"


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

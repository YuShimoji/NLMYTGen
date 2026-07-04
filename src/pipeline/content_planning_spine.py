"""Offline content-planning spine package builder.

This module turns local RSS-like topic candidates into a reviewable planning
package. It does not fetch live sources, download media, render video, launch
YMM4, or claim public/rights acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONTENT_SPINE_VERSION = "0.1"

REQUIRED_PACKAGE_FILES = (
    "MANIFEST.json",
    "topic_candidates.json",
    "channel_strategy_proposals.md",
    "episode_candidate_001.md",
    "thumbnail_brief_001.md",
    "dashboard_status.json",
    "dashboard_preview.md",
    "review_checklist.md",
    "limitations.md",
    "content_spine_readback.json",
)

BLOCKED_PUBLIC_ACTIONS = (
    "YouTube upload/publication/visibility change",
    "OAuth/API keys/payment",
    "rights/legal/public-ready acceptance",
    "live scraping/media download",
    "YMM4 GUI launch/render",
    "cross-repo or destructive git",
)


def build_content_spine_package(
    *,
    source_path: str | Path,
    output_dir: str | Path,
    artifact_id: str = "yukkuri_newsroom_content_spine_001",
) -> dict[str, Any]:
    """Create a local/offline content planning package and return its readback."""
    source = _load_source_manifest(Path(source_path))
    candidates = _normalize_candidates(source)
    if not candidates:
        raise ValueError("content spine source must include at least one candidate")

    ranked = sorted(candidates, key=lambda item: item["candidate_score"], reverse=True)
    selected = ranked[0]
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    topic_payload = _topic_candidates_payload(source, ranked)
    dashboard_status = _dashboard_status_payload(
        artifact_id=artifact_id,
        source_path=Path(source_path),
        output_dir=out,
        selected=selected,
        candidates=ranked,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_path=Path(source_path),
        output_dir=out,
        selected=selected,
        dashboard_status=dashboard_status,
    )

    _write_json(out / "MANIFEST.json", manifest)
    _write_json(out / "topic_candidates.json", topic_payload)
    (out / "channel_strategy_proposals.md").write_text(
        _render_channel_strategy(ranked), encoding="utf-8"
    )
    (out / "episode_candidate_001.md").write_text(
        _render_episode_candidate(selected), encoding="utf-8"
    )
    (out / "thumbnail_brief_001.md").write_text(
        _render_thumbnail_brief(selected), encoding="utf-8"
    )
    _write_json(out / "dashboard_status.json", dashboard_status)
    (out / "dashboard_preview.md").write_text(
        _render_dashboard_preview(dashboard_status), encoding="utf-8"
    )
    (out / "review_checklist.md").write_text(
        _render_review_checklist(selected), encoding="utf-8"
    )
    (out / "limitations.md").write_text(_render_limitations(), encoding="utf-8")

    readback = validate_content_spine_package(out, require_readback=False)
    _write_json(out / "content_spine_readback.json", readback)
    final_readback = validate_content_spine_package(out)
    _write_json(out / "content_spine_readback.json", final_readback)
    return final_readback


def validate_content_spine_package(
    package_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate package files and core machine-readable boundaries."""
    root = Path(package_dir)
    files = {name: root / name for name in REQUIRED_PACKAGE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "content_spine_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["MANIFEST.json"])
    topics = _load_json_if_present(files["topic_candidates.json"])
    dashboard = _load_json_if_present(files["dashboard_status.json"])

    if not isinstance(manifest, dict):
        failed_checks.append("manifest_json_invalid")
        manifest = {}
    if not isinstance(topics, dict):
        failed_checks.append("topic_candidates_json_invalid")
        topics = {}
    if not isinstance(dashboard, dict):
        failed_checks.append("dashboard_status_json_invalid")
        dashboard = {}

    if manifest.get("artifact_kind") != "content-planning-dashboard-spine":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if not topics.get("candidates"):
        failed_checks.append("topic_candidates_empty")
    if dashboard.get("public_actions_blocked") != list(BLOCKED_PUBLIC_ACTIONS):
        failed_checks.append("dashboard_public_action_boundaries_missing")

    readiness = dashboard.get("readiness", {})
    if readiness.get("episode_package_status") != "local_reviewable":
        failed_checks.append("episode_package_not_local_reviewable")
    if readiness.get("thumbnail_readiness") != "brief_only_no_image":
        failed_checks.append("thumbnail_boundary_missing")
    if readiness.get("ymm4_readiness") != "planning_ready_csv_ir_not_generated":
        failed_checks.append("ymm4_boundary_missing")

    return {
        "schema_version": "content_spine_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "package_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "manifest_json_loads": bool(manifest),
            "topic_candidates_json_loads": bool(topics),
            "dashboard_status_json_loads": bool(dashboard),
            "local_reviewable_only": readiness.get("episode_package_status") == "local_reviewable",
            "public_actions_blocked": dashboard.get("public_actions_blocked") == list(BLOCKED_PUBLIC_ACTIONS),
        },
        "failed_checks": failed_checks,
        "selected_candidate_id": manifest.get("selected_candidate_id"),
        "next_action": (
            "Open dashboard_preview.md, review episode_candidate_001.md and "
            "thumbnail_brief_001.md, then choose revise_once, accept_for_csv_ir, or hold."
        ),
    }


def _load_source_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"content spine source must be a JSON object: {path}")
    return data


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _normalize_candidates(source: dict[str, Any]) -> list[dict[str, Any]]:
    raw_candidates = source.get("candidates")
    if not isinstance(raw_candidates, list):
        raise ValueError("content spine source must include candidates[]")

    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_candidates, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"candidate #{index} must be an object")
        candidate_id = str(raw.get("candidate_id") or f"candidate_{index:03d}")
        score = raw.get("candidate_score", raw.get("score", 0))
        try:
            candidate_score = int(score)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"candidate_score must be an integer: {candidate_id}") from exc
        normalized.append({
            **raw,
            "candidate_id": candidate_id,
            "candidate_score": candidate_score,
            "rank_input_order": index,
            "source_boundary": _source_boundary(raw),
            "yukkuri_profile": _yukkuri_profile(raw),
            "thumbnail_profile": _thumbnail_profile(raw),
        })
    return normalized


def _source_boundary(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_name": candidate.get("source_name", "offline fixture"),
        "source_url_or_placeholder": candidate.get("source_url_or_placeholder", "offline://placeholder"),
        "published_at_or_placeholder": candidate.get("published_at_or_placeholder", "unknown_offline_fixture"),
        "freshness_status": candidate.get("freshness_status", "offline_fixture_not_live"),
        "rights_status": candidate.get("rights_status", "sample_only_no_publication"),
        "attribution_note": candidate.get("attribution_note", "Synthetic/local planning fixture."),
        "excluded_claims": candidate.get("excluded_claims", []),
        "production_status": candidate.get("production_status", "local_planning_only"),
    }


def _yukkuri_profile(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "explainer_role": candidate.get("explainer_role", "まりさ"),
        "listener_role": candidate.get("listener_role", "れいむ"),
        "hook": candidate.get("hook", candidate.get("title", "")),
        "why_it_matters": candidate.get("why_it_matters", ""),
        "beat_outline": candidate.get("beat_outline", []),
        "recommended_tone": candidate.get("recommended_tone", "fact-first yukkuri explainer"),
        "glossary_terms": candidate.get("glossary_terms", []),
        "likely_audience": candidate.get("likely_audience", "news explainer viewers"),
        "channel_fit": candidate.get("channel_fit", "short-form yukkuri explainer"),
    }


def _thumbnail_profile(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "title_hook": candidate.get("title_hook", candidate.get("title", "")),
        "short_text_candidates": candidate.get("short_text_candidates", []),
        "visual_motif": candidate.get("visual_motif", ""),
        "forbidden_avoid_claims": candidate.get("forbidden_avoid_claims", []),
        "source_rights_caution": candidate.get("source_rights_caution", "Use original graphics only."),
        "designer_note": candidate.get("designer_note", ""),
    }


def _topic_candidates_payload(source: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "content_spine_topic_candidates.v1",
        "source_manifest_id": source.get("source_manifest_id", "offline_topic_candidates"),
        "source_type": source.get("source_type", "offline_synthetic_fixture"),
        "selection_policy": "highest candidate_score, then source order",
        "candidates": [
            {
                "candidate_id": candidate["candidate_id"],
                "title": candidate.get("title", ""),
                "candidate_score": candidate["candidate_score"],
                "score_rationale": candidate.get("score_rationale", ""),
                "channel_angle": candidate.get("channel_angle", ""),
                "source_boundary": candidate["source_boundary"],
                "yukkuri_profile": candidate["yukkuri_profile"],
                "thumbnail_profile": candidate["thumbnail_profile"],
            }
            for candidate in candidates
        ],
    }


def _dashboard_status_payload(
    *,
    artifact_id: str,
    source_path: Path,
    output_dir: Path,
    selected: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "content_spine_dashboard_status.v1",
        "artifact_id": artifact_id,
        "selected_candidate_id": selected["candidate_id"],
        "selected_title": selected.get("title", ""),
        "candidate_count": len(candidates),
        "source_manifest": str(source_path),
        "package_dir": str(output_dir),
        "candidate_score": selected["candidate_score"],
        "score_rationale": selected.get("score_rationale", ""),
        "channel_angle": selected.get("channel_angle", ""),
        "readiness": {
            "episode_package_status": "local_reviewable",
            "topic_candidates_status": "ranked_offline_fixture",
            "yukkuri_brief_status": "draft_capsule_ready",
            "dashboard_status": "machine_readable",
            "ymm4_readiness": "planning_ready_csv_ir_not_generated",
            "thumbnail_readiness": "brief_only_no_image",
            "public_status": "blocked_until_human_rights_and_publication_review",
        },
        "required_human_inputs": [
            "choose accept_for_csv_ir, revise_once, reject, or hold",
            "confirm channel angle and audience promise",
            "supply real source transcript/materials before production use",
            "approve rights/publication separately before any public action",
        ],
        "public_actions_blocked": list(BLOCKED_PUBLIC_ACTIONS),
        "next_local_actions": [
            "review episode_candidate_001.md",
            "review thumbnail_brief_001.md",
            "if accepted, create CSV/Writer IR inputs in a separate production run pack",
        ],
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_path: Path,
    output_dir: Path,
    selected: dict[str, Any],
    dashboard_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "content_spine_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "content-planning-dashboard-spine",
        "status": "generated",
        "source_manifest": str(source_path),
        "package_dir": str(output_dir),
        "selected_candidate_id": selected["candidate_id"],
        "selected_title": selected.get("title", ""),
        "files": {name: str(output_dir / name) for name in REQUIRED_PACKAGE_FILES},
        "dashboard_status": dashboard_status,
        "boundaries": {
            "local_offline_review_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_ymm4_gui_launch_or_render": True,
            "no_thumbnail_image_generation": True,
        },
    }


def _render_channel_strategy(candidates: list[dict[str, Any]]) -> str:
    lines = [
        "# Channel Strategy Proposals",
        "",
        "Local/offline proposals derived from ranked topic candidates.",
        "",
        "| Rank | Candidate | Score | Channel angle | Why now |",
        "|---|---|---:|---|---|",
    ]
    for rank, candidate in enumerate(candidates, start=1):
        profile = candidate["yukkuri_profile"]
        lines.append(
            f"| {rank} | {candidate.get('title', '')} | {candidate['candidate_score']} | "
            f"{candidate.get('channel_angle', '')} | {profile.get('why_it_matters', '')} |"
        )
    lines.extend([
        "",
        "## Dashboard Use",
        "",
        "- Primary sort: candidate_score.",
        "- Public gate: all proposals remain local planning drafts until source, rights, and publication review.",
        "- Next production bridge: accepted candidate -> refined script -> CSV/Writer IR -> YMM4-assisted pack.",
        "",
    ])
    return "\n".join(lines)


def _render_episode_candidate(candidate: dict[str, Any]) -> str:
    profile = candidate["yukkuri_profile"]
    boundary = candidate["source_boundary"]
    lines = [
        "# Episode Candidate 001",
        "",
        f"- candidate_id: {candidate['candidate_id']}",
        f"- title: {candidate.get('title', '')}",
        f"- score: {candidate['candidate_score']}",
        f"- channel_angle: {candidate.get('channel_angle', '')}",
        f"- explainer/listener: {profile['explainer_role']} / {profile['listener_role']}",
        f"- hook: {profile['hook']}",
        f"- why_it_matters: {profile['why_it_matters']}",
        f"- recommended_tone: {profile['recommended_tone']}",
        f"- likely_audience: {profile['likely_audience']}",
        f"- channel_fit: {profile['channel_fit']}",
        "",
        "## Beat Outline",
        "",
    ]
    for index, beat in enumerate(profile.get("beat_outline", []), start=1):
        lines.append(f"{index}. {beat}")
    lines.extend([
        "",
        "## Glossary / Terms",
        "",
    ])
    for term in profile.get("glossary_terms", []):
        lines.append(f"- {term}")
    lines.extend([
        "",
        "## Source Boundary",
        "",
        f"- source_name: {boundary['source_name']}",
        f"- source_url_or_placeholder: {boundary['source_url_or_placeholder']}",
        f"- published_at_or_placeholder: {boundary['published_at_or_placeholder']}",
        f"- freshness_status: {boundary['freshness_status']}",
        f"- rights_status: {boundary['rights_status']}",
        f"- attribution_note: {boundary['attribution_note']}",
        f"- production_status: {boundary['production_status']}",
        "",
        "## Excluded Claims",
        "",
    ])
    for claim in boundary.get("excluded_claims", []):
        lines.append(f"- {claim}")
    lines.append("")
    return "\n".join(lines)


def _render_thumbnail_brief(candidate: dict[str, Any]) -> str:
    thumbnail = candidate["thumbnail_profile"]
    lines = [
        "# Thumbnail Brief 001",
        "",
        f"- candidate_id: {candidate['candidate_id']}",
        f"- title_hook: {thumbnail['title_hook']}",
        f"- visual_motif: {thumbnail['visual_motif']}",
        f"- source_rights_caution: {thumbnail['source_rights_caution']}",
        f"- designer_note: {thumbnail['designer_note']}",
        "",
        "## Short Text Candidates",
        "",
    ]
    for text in thumbnail.get("short_text_candidates", []):
        lines.append(f"- {text}")
    lines.extend([
        "",
        "## Forbidden / Avoid Claims",
        "",
    ])
    for claim in thumbnail.get("forbidden_avoid_claims", []):
        lines.append(f"- {claim}")
    lines.extend([
        "",
        "## Production Boundary",
        "",
        "This is a text-only direction brief. It does not generate an image, download media, patch a YMM4 thumbnail template, or approve public use.",
        "",
    ])
    return "\n".join(lines)


def _render_dashboard_preview(status: dict[str, Any]) -> str:
    readiness = status["readiness"]
    lines = [
        "# Content Spine Dashboard Preview",
        "",
        f"- artifact_id: {status['artifact_id']}",
        f"- selected_candidate_id: {status['selected_candidate_id']}",
        f"- selected_title: {status['selected_title']}",
        f"- candidate_score: {status['candidate_score']}",
        f"- channel_angle: {status['channel_angle']}",
        "",
        "## Readiness",
        "",
    ]
    for key, value in readiness.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "## Required Human Inputs",
        "",
    ])
    for item in status["required_human_inputs"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Blocked Public Actions",
        "",
    ])
    for item in status["public_actions_blocked"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def _render_review_checklist(candidate: dict[str, Any]) -> str:
    return "\n".join([
        "# Review Checklist",
        "",
        f"- candidate_id: {candidate['candidate_id']}",
        "",
        "## Decide",
        "",
        "- Is the hook concrete enough for a yukkuri explainer cold open?",
        "- Is every factual claim either source-backed or explicitly excluded?",
        "- Does the channel angle fit the intended audience and video length?",
        "- Is the thumbnail promise aligned with the episode outline?",
        "- Are required human inputs clear enough to move into CSV/Writer IR work?",
        "",
        "## Allowed Outcomes",
        "",
        "- accept_for_csv_ir: move to script/CSV/Writer IR package planning.",
        "- revise_once: return concrete must-fix notes for this package only.",
        "- reject: keep package as negative evidence and choose another candidate.",
        "- hold: leave as local planning evidence without production work.",
        "",
    ])


def _render_limitations() -> str:
    lines = [
        "# Limitations",
        "",
        "This package is a local/offline planning checkpoint. It is useful for review, GUI/dashboard consumption, and deciding whether a candidate deserves CSV/Writer IR work.",
        "",
        "It does not perform or approve:",
        "",
    ]
    for item in BLOCKED_PUBLIC_ACTIONS:
        lines.append(f"- {item}")
    lines.extend([
        "- final thumbnail image generation",
        "- final YMM4 production candidate creation",
        "",
        "Local progress should not be blocked by these public/production gates, but those gates remain mandatory before external release.",
        "",
    ])
    return "\n".join(lines)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

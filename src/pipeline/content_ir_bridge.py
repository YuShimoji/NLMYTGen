"""Bridge content spine packages into draft episode/Writer IR inputs.

The bridge is deliberately local and offline. It converts a selected content
planning candidate into machine-readable episode inputs, a draft YMM4 CSV
preview, and readiness reports without fetching sources, launching YMM4, or
claiming production/public acceptance.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.pipeline.content_planning_spine import BLOCKED_PUBLIC_ACTIONS

IR_BRIDGE_VERSION = "0.1"
DEFAULT_BRIDGE_DIRNAME = "ir_bridge"

REQUIRED_BRIDGE_FILES = (
    "bridge_manifest.json",
    "episode_bridge.json",
    "writer_ir_candidate.json",
    "cue_packet_candidate.json",
    "cue_packet_candidate.md",
    "draft_yymm4.csv",
    "ymm4_csv_readiness.md",
    "source_to_ir_mapping.md",
    "limitations.md",
    "validation_readback.json",
)


def build_content_ir_bridge_package(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = "content_spine_ir_bridge_001",
) -> dict[str, Any]:
    """Build a bridge package from a content spine package."""
    source_root = Path(package_dir)
    bridge_dir = Path(output_dir) if output_dir else source_root / DEFAULT_BRIDGE_DIRNAME
    bridge_dir.mkdir(parents=True, exist_ok=True)

    source = _load_content_spine(source_root)
    selected = source["selected_candidate"]
    dialogue = _draft_dialogue(selected)
    sections = _draft_sections(selected, dialogue)

    episode_bridge = _episode_bridge_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=bridge_dir,
        source=source,
        dialogue=dialogue,
        sections=sections,
    )
    writer_ir = _writer_ir_candidate_payload(episode_bridge, selected, dialogue, sections)
    cue_packet = _cue_packet_candidate_payload(episode_bridge, selected, dialogue, sections)
    manifest = _bridge_manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=bridge_dir,
        episode_bridge=episode_bridge,
    )

    _write_json(bridge_dir / "bridge_manifest.json", manifest)
    _write_json(bridge_dir / "episode_bridge.json", episode_bridge)
    _write_json(bridge_dir / "writer_ir_candidate.json", writer_ir)
    _write_json(bridge_dir / "cue_packet_candidate.json", cue_packet)
    _write_text(bridge_dir / "cue_packet_candidate.md", _render_cue_packet_markdown(cue_packet))
    _write_draft_csv(bridge_dir / "draft_yymm4.csv", dialogue)
    _write_text(bridge_dir / "ymm4_csv_readiness.md", _render_yymm4_csv_readiness(episode_bridge))
    _write_text(bridge_dir / "source_to_ir_mapping.md", _render_source_to_ir_mapping(episode_bridge))
    _write_text(bridge_dir / "limitations.md", _render_limitations())

    readback = validate_content_ir_bridge_package(bridge_dir, require_readback=False)
    _write_json(bridge_dir / "validation_readback.json", readback)
    final_readback = validate_content_ir_bridge_package(bridge_dir)
    _write_json(bridge_dir / "validation_readback.json", final_readback)
    return final_readback


def validate_content_ir_bridge_package(
    bridge_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated content IR bridge package."""
    root = Path(bridge_dir)
    files = {name: root / name for name in REQUIRED_BRIDGE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["bridge_manifest.json"])
    episode_bridge = _load_json_if_present(files["episode_bridge.json"])
    writer_ir = _load_json_if_present(files["writer_ir_candidate.json"])
    cue_packet = _load_json_if_present(files["cue_packet_candidate.json"])
    csv_rows = _load_csv_rows_if_present(files["draft_yymm4.csv"])

    if not isinstance(manifest, dict):
        failed_checks.append("bridge_manifest_json_invalid")
        manifest = {}
    if not isinstance(episode_bridge, dict):
        failed_checks.append("episode_bridge_json_invalid")
        episode_bridge = {}
    if not isinstance(writer_ir, dict):
        failed_checks.append("writer_ir_candidate_json_invalid")
        writer_ir = {}
    if not isinstance(cue_packet, dict):
        failed_checks.append("cue_packet_candidate_json_invalid")
        cue_packet = {}

    source_boundary = episode_bridge.get("source_boundary", {})
    if not source_boundary.get("source_name"):
        failed_checks.append("source_boundary_missing")
    if writer_ir.get("schema_version") != "content_spine_writer_ir_candidate.v1":
        failed_checks.append("writer_ir_schema_mismatch")
    if not writer_ir.get("utterances"):
        failed_checks.append("writer_ir_utterances_empty")
    if cue_packet.get("phase") != "content-spine-bridge-cue-candidate":
        failed_checks.append("cue_packet_phase_mismatch")
    if len(csv_rows) < 2:
        failed_checks.append("draft_csv_too_short")

    blocked_actions = episode_bridge.get("blocked_public_actions", [])
    if blocked_actions != list(BLOCKED_PUBLIC_ACTIONS):
        failed_checks.append("blocked_public_actions_missing")

    readiness = episode_bridge.get("readiness", {})
    if readiness.get("writer_ir_candidate_status") != "draft_candidate_generated":
        failed_checks.append("writer_ir_readiness_missing")
    if readiness.get("ymm4_csv_status") != "draft_preview_generated_not_production":
        failed_checks.append("csv_readiness_missing")
    if readiness.get("production_status") != "blocked_until_transcript_timing_and_human_review":
        failed_checks.append("production_boundary_missing")

    return {
        "schema_version": "content_ir_bridge_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "bridge_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "bridge_manifest_json_loads": bool(manifest),
            "episode_bridge_json_loads": bool(episode_bridge),
            "writer_ir_candidate_json_loads": bool(writer_ir),
            "cue_packet_candidate_json_loads": bool(cue_packet),
            "draft_csv_has_rows": len(csv_rows) >= 2,
            "source_boundary_preserved": bool(source_boundary.get("source_name")),
            "blocked_public_actions_preserved": blocked_actions == list(BLOCKED_PUBLIC_ACTIONS),
            "not_production_ready": readiness.get("production_status") == "blocked_until_transcript_timing_and_human_review",
        },
        "failed_checks": failed_checks,
        "selected_candidate_id": episode_bridge.get("selected_candidate_id"),
        "draft_csv_rows": len(csv_rows),
        "next_action": (
            "Review draft_yymm4.csv and writer_ir_candidate.json; if accepted, replace "
            "draft lines with a real transcript before validate-ir/apply-production work."
        ),
    }


def _load_content_spine(root: Path) -> dict[str, Any]:
    manifest = _load_json(root / "MANIFEST.json")
    topics = _load_json(root / "topic_candidates.json")
    dashboard = _load_json(root / "dashboard_status.json")

    selected_id = manifest.get("selected_candidate_id")
    candidates = topics.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError(f"topic_candidates.json must include candidates[]: {root}")
    selected = next((candidate for candidate in candidates if candidate.get("candidate_id") == selected_id), None)
    if selected is None:
        raise ValueError(f"selected candidate not found in topic_candidates.json: {selected_id}")

    return {
        "manifest": manifest,
        "topics": topics,
        "dashboard": dashboard,
        "selected_candidate": selected,
    }


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return data


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_csv_rows_if_present(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return [row for row in csv.reader(file) if row]


def _draft_dialogue(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    profile = candidate["yukkuri_profile"]
    thumbnail = candidate["thumbnail_profile"]
    explainer = profile.get("explainer_role", "まりさ")
    listener = profile.get("listener_role", "れいむ")
    title = candidate.get("title", "")
    display_title = thumbnail.get("title_hook") or title
    hook = profile.get("hook", title)
    beats = profile.get("beat_outline", [])

    rows: list[dict[str, Any]] = [
        {
            "index": 1,
            "speaker": listener,
            "text": f"今日は「{display_title}」って、どういう話なの？",
            "purpose": "opening_question",
            "source": "thumbnail_profile.title_hook",
        },
        {
            "index": 2,
            "speaker": explainer,
            "text": hook,
            "purpose": "hook",
            "source": "yukkuri_profile.hook",
        },
    ]

    for beat_index, beat in enumerate(beats, start=1):
        rows.append({
            "index": len(rows) + 1,
            "speaker": explainer,
            "text": _draft_beat_text(beat_index, str(beat)),
            "purpose": "beat_explanation",
            "source": f"yukkuri_profile.beat_outline[{beat_index - 1}]",
        })
        if beat_index in {2, len(beats)}:
            rows.append({
                "index": len(rows) + 1,
                "speaker": listener,
                "text": "なるほど、そこを見れば話の筋が追いやすいんだね。",
                "purpose": "listener_checkpoint",
                "source": "bridge_generated_listener_checkpoint",
            })

    rows.append({
        "index": len(rows) + 1,
        "speaker": explainer,
        "text": "この段階ではローカル企画案なので、本番化には実ソース、台本、タイミング確認が必要だぜ。",
        "purpose": "production_boundary",
        "source": "bridge_boundary_note",
    })
    return rows


def _draft_beat_text(beat_index: int, beat: str) -> str:
    """Convert planning beats into draft yukkuri dialogue without claiming final script quality."""
    known_sports_beats = {
        "Establish inning, count, score, and empty bases.": "まず場面は、7回表、1アウト、カウントB2-S2、走者なしという状況から見るぜ。",
        "Compare the previous 155 km/h four-seam fastball with the current 140 km/h slider.": "直前の155km/hのフォーシームから、今回は140km/hのスライダーに変わっている。",
        "Explain the 15 km/h drop as the main tactical contrast.": "ここで大事なのは15km/hの球速差だ。打者のタイミングをずらす主役になる。",
        "Show the low-outer strike result as the viewer watch point.": "結果は外低めへのストライク。視聴者にはこのコースと変化を見てもらう。",
        "Hand off to CSV/Writer IR only after source and claim review.": "ただし本番化するなら、実ソースと主張確認を済ませてからCSVとWriter IRに進める。",
    }
    if beat in known_sports_beats:
        return known_sports_beats[beat]
    return f"ポイント{beat_index}は、{beat}"


def _draft_sections(candidate: dict[str, Any], dialogue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    title = candidate.get("title", "")
    midpoint = max(3, len(dialogue) // 2)
    return [
        {
            "section_id": "S1",
            "topic": "Opening hook and topic promise",
            "start_index": 1,
            "end_index": min(2, len(dialogue)),
            "default_bg": "studio_blue",
            "default_face": "neutral",
            "bgm": "light_explainer",
            "arc_phase": "intro",
        },
        {
            "section_id": "S2",
            "topic": f"Main explanation: {title}",
            "start_index": 3,
            "end_index": midpoint,
            "default_bg": "diagram",
            "default_face": "serious",
            "bgm": "data_focus",
            "arc_phase": "develop",
        },
        {
            "section_id": "S3",
            "topic": "Viewer watch point and production boundary",
            "start_index": midpoint + 1,
            "end_index": len(dialogue),
            "default_bg": "dark_board",
            "default_face": "thinking",
            "bgm": "closing_light",
            "arc_phase": "closing",
        },
    ]


def _section_for_index(sections: list[dict[str, Any]], index: int) -> dict[str, Any]:
    for section in sections:
        if section["start_index"] <= index <= section["end_index"]:
            return section
    return sections[-1]


def _episode_bridge_payload(
    *,
    artifact_id: str,
    source_root: Path,
    bridge_dir: Path,
    source: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    selected = source["selected_candidate"]
    profile = selected["yukkuri_profile"]
    thumbnail = selected["thumbnail_profile"]
    boundary = selected["source_boundary"]
    return {
        "schema_version": "content_spine_episode_bridge.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "bridge_dir": str(bridge_dir),
        "selected_candidate_id": selected["candidate_id"],
        "selected_title": selected.get("title", ""),
        "source_boundary": boundary,
        "yukkuri": {
            "explainer_role": profile.get("explainer_role"),
            "listener_role": profile.get("listener_role"),
            "hook": profile.get("hook"),
            "why_it_matters": profile.get("why_it_matters"),
            "beat_outline": profile.get("beat_outline", []),
            "recommended_tone": profile.get("recommended_tone"),
            "glossary_terms": profile.get("glossary_terms", []),
            "likely_audience": profile.get("likely_audience"),
            "channel_fit": profile.get("channel_fit"),
        },
        "thumbnail": thumbnail,
        "draft_dialogue": dialogue,
        "sections": sections,
        "readiness": {
            "writer_ir_candidate_status": "draft_candidate_generated",
            "cue_packet_status": "draft_candidate_generated",
            "ymm4_csv_status": "draft_preview_generated_not_production",
            "row_range_status": "not_available_until_real_transcript",
            "audio_timing_status": "not_available_until_yymm4_import",
            "maps_status": "not_selected",
            "production_status": "blocked_until_transcript_timing_and_human_review",
        },
        "missing_for_production": [
            "real transcript or final script",
            "YMM4 CSV import and VoiceItem timing",
            "row_start/row_end annotation",
            "face/bg/slot/overlay/se/motion maps if the episode uses them",
            "human source/rights/publication review",
        ],
        "blocked_public_actions": list(BLOCKED_PUBLIC_ACTIONS),
    }


def _writer_ir_candidate_payload(
    episode_bridge: dict[str, Any],
    candidate: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    utterances = []
    for row in dialogue:
        section = _section_for_index(sections, row["index"])
        utterances.append({
            "index": row["index"],
            "speaker": row["speaker"],
            "text": row["text"],
            "section_id": section["section_id"],
            "template": "intro" if section["arc_phase"] == "intro" else ("closing" if section["arc_phase"] == "closing" else "data"),
            "face": section["default_face"],
            "bg": section["default_bg"],
            "slot": "left" if row["speaker"] == episode_bridge["yukkuri"]["listener_role"] else "right",
            "bridge_source": row["source"],
        })

    return {
        "schema_version": "content_spine_writer_ir_candidate.v1",
        "production_ir_spec_reference": "docs/PRODUCTION_IR_SPEC.md",
        "compatibility_status": "draft_candidate_not_validate_ir_ready",
        "not_validate_ir_ready_reason": (
            "Content spine package has no final transcript timing, row_start/row_end, "
            "YMM4 base project, or production maps."
        ),
        "video_id": episode_bridge["selected_candidate_id"],
        "ir_version": "1.0-draft",
        "tone": candidate["yukkuri_profile"].get("recommended_tone", ""),
        "pattern_mix": "intro:data:closing = 1:2:1",
        "visual_arc": [
            {"phase": "intro", "primary_pattern": "A", "emotion_flow": "question -> hook"},
            {"phase": "develop", "primary_pattern": "B", "emotion_flow": "fact comparison -> understanding"},
            {"phase": "closing", "primary_pattern": "D", "emotion_flow": "watch point -> production boundary"},
        ],
        "recurring_motif": candidate["thumbnail_profile"].get("visual_motif", ""),
        "default_bgm": "light_explainer",
        "sections": sections,
        "utterances": utterances,
        "source_boundary": episode_bridge["source_boundary"],
        "production_boundary": {
            "draft_yymm4_csv_only": True,
            "no_ymmp_generation": True,
            "no_render": True,
            "no_publication": True,
        },
    }


def _cue_packet_candidate_payload(
    episode_bridge: dict[str, Any],
    candidate: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "packet_version": "content-spine-cue-v1",
        "phase": "content-spine-bridge-cue-candidate",
        "source_name": episode_bridge["selected_candidate_id"],
        "objective": "Turn the content spine draft dialogue into a concise S-6 cue memo candidate.",
        "constraints": [
            "Do not fetch live sources.",
            "Do not rewrite this into a final script without human review.",
            "Do not edit YMM4 projects or .ymmp data.",
            "Do not generate images, audio, or video.",
        ],
        "response_preferences": {
            "target_section_count": len(sections),
            "background_density": "One primary background plus at most one supporting visual per section.",
            "sound_policy": "Omit sound cues unless they clearly help.",
            "operator_todos_max": 4,
            "keep_notes_concise": True,
        },
        "context": {
            "candidate_title": candidate.get("title", ""),
            "channel_angle": candidate.get("channel_angle", ""),
            "glossary_terms": candidate["yukkuri_profile"].get("glossary_terms", []),
            "sections": sections,
        },
        "transcript": [
            {
                "index": row["index"],
                "speaker": row["speaker"],
                "mapped_speaker": row["speaker"],
                "text": row["text"],
            }
            for row in dialogue
        ],
    }


def _bridge_manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    bridge_dir: Path,
    episode_bridge: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "content_ir_bridge_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "content-spine-to-writer-ir-csv-bridge",
        "status": "generated",
        "source_package_dir": str(source_root),
        "bridge_dir": str(bridge_dir),
        "selected_candidate_id": episode_bridge["selected_candidate_id"],
        "files": {name: str(bridge_dir / name) for name in REQUIRED_BRIDGE_FILES},
        "readiness": episode_bridge["readiness"],
        "boundaries": {
            "local_offline_review_only": True,
            "draft_csv_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_ymm4_gui_launch_or_render": True,
            "no_production_ymmp_generation": True,
        },
    }


def _write_draft_csv(path: Path, dialogue: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        for row in dialogue:
            writer.writerow([row["speaker"], row["text"]])


def _render_cue_packet_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Cue Packet Candidate",
        "",
        f"- phase: {payload['phase']}",
        f"- source_name: {payload['source_name']}",
        "",
        "## Objective",
        payload["objective"],
        "",
        "## Constraints",
    ]
    for item in payload["constraints"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Transcript"])
    for item in payload["transcript"]:
        lines.append(f"{item['index']}. [{item['mapped_speaker']}] {item['text']}")
    lines.append("")
    return "\n".join(lines)


def _render_yymm4_csv_readiness(episode_bridge: dict[str, Any]) -> str:
    lines = [
        "# YMM4 CSV Readiness",
        "",
        f"- selected_candidate_id: {episode_bridge['selected_candidate_id']}",
        "- generated: `draft_yymm4.csv`",
        "- status: draft_preview_generated_not_production",
        "",
        "## Ready Now",
        "",
        "- Speaker names are mapped to the yukkuri roles from the content spine package.",
        "- Draft dialogue rows are available for review and can be opened as a CSV preview.",
        "- Source boundary and excluded claims are preserved in `episode_bridge.json`.",
        "",
        "## Missing Before Production",
        "",
    ]
    for item in episode_bridge["missing_for_production"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Boundary",
        "",
        "This CSV is not a NotebookLM transcript, not YMM4-import proof, and not production-ready timing.",
        "",
    ])
    return "\n".join(lines)


def _render_source_to_ir_mapping(episode_bridge: dict[str, Any]) -> str:
    lines = [
        "# Source To IR Mapping",
        "",
        "| Source field | Bridge / IR field | Status |",
        "|---|---|---|",
        "| topic_candidates.selected.candidate_id | episode_bridge.selected_candidate_id / writer_ir.video_id | mapped |",
        "| source_boundary | episode_bridge.source_boundary / writer_ir.source_boundary | preserved |",
        "| yukkuri_profile.explainer_role/listener_role | draft_dialogue.speaker / writer_ir.utterances.speaker | mapped |",
        "| yukkuri_profile.hook | draft_dialogue row 2 / writer_ir utterance 2 | mapped |",
        "| yukkuri_profile.beat_outline | draft_dialogue beat rows / writer_ir utterances | mapped as draft dialogue |",
        "| thumbnail_profile.visual_motif | writer_ir.recurring_motif | mapped as planning cue |",
        "| final transcript timing | row_start/row_end | pending |",
        "| YMM4 base project | apply-production input | pending |",
        "",
    ]
    return "\n".join(lines)


def _render_limitations() -> str:
    lines = [
        "# Bridge Limitations",
        "",
        "This bridge turns a content spine package into draft production inputs. It is not final video generation.",
        "",
        "Not performed:",
        "",
    ]
    for item in BLOCKED_PUBLIC_ACTIONS:
        lines.append(f"- {item}")
    lines.extend([
        "- production .ymmp generation",
        "- validate-ir/apply-production against a real YMM4 project",
        "- final transcript/timing acceptance",
        "",
    ])
    return "\n".join(lines)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")

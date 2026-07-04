"""Build transcript-substitution readiness packages for content IR bridges.

This module stays local/offline. It proves that a content spine bridge can
accept a real or NotebookLM-like transcript later, while keeping production,
rights, timing, audio, YMM4 GUI, and publication gates closed.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.pipeline.assemble_csv import assemble, find_unmapped_speakers
from src.pipeline.content_ir_bridge import (
    _cue_packet_candidate_payload,
    _draft_dialogue,
    _draft_sections,
    _episode_bridge_payload,
    _load_content_spine,
    _render_cue_packet_markdown,
    _writer_ir_candidate_payload,
)
from src.pipeline.content_planning_spine import BLOCKED_PUBLIC_ACTIONS
from src.pipeline.normalize import normalize

DEFAULT_OUTPUT_DIRNAME = "transcript_substitution_readiness"
DEFAULT_ARTIFACT_ID = "real_transcript_substitution_readiness_001"

REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES = (
    "substitution_manifest.json",
    "transcript_input_contract.json",
    "transcript_source_probe.json",
    "regenerated_episode_bridge.json",
    "regenerated_writer_ir_candidate.json",
    "regenerated_cue_packet_candidate.json",
    "regenerated_cue_packet_candidate.md",
    "regenerated_draft_yymm4.csv",
    "cue_packet_readiness.json",
    "source_to_transcript_mapping.md",
    "limitations.md",
    "validation_readback.json",
)

SUPPORT_FILES = (
    "real_input/README.md",
    "sample_inputs/notebooklm_like_sample.txt",
)

_TRANSCRIPT_CANDIDATE_DIRS = (
    "real_input",
    "transcripts",
    "notebooklm",
    "NotebookLM",
)

_TRANSCRIPT_SUFFIXES = {".txt", ".csv"}


def build_transcript_substitution_package(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    transcript_path: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    speaker_map: dict[str, str] | None = None,
    unlabeled: bool = False,
) -> dict[str, Any]:
    """Build a transcript substitution/readiness package for a content spine."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    source = _load_content_spine(source_root)
    selected = source["selected_candidate"]

    probe = _probe_transcript_source(
        package_dir=source_root,
        output_dir=output_root,
        explicit_transcript=Path(transcript_path) if transcript_path else None,
        source=source,
    )
    selected_transcript = Path(probe["selected_transcript_path"])

    script = normalize(selected_transcript, unlabeled=unlabeled)
    assembled = assemble(script, speaker_map=speaker_map)
    unmapped = sorted(find_unmapped_speakers(script, speaker_map or {})) if speaker_map else []
    dialogue = [
        {
            "index": index,
            "speaker": row.speaker,
            "text": row.text,
            "purpose": "transcript_substitution_line",
            "source": f"transcript_input[{index}]",
        }
        for index, row in enumerate(assembled.rows, start=1)
    ]
    sections = _draft_sections(selected, dialogue)

    episode_bridge = _episode_bridge_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=output_root,
        source=source,
        dialogue=dialogue,
        sections=sections,
    )
    _apply_transcript_readiness(
        episode_bridge=episode_bridge,
        probe=probe,
        selected_transcript=selected_transcript,
        utterance_count=len(dialogue),
    )

    writer_ir = _writer_ir_candidate_payload(episode_bridge, selected, dialogue, sections)
    writer_ir["compatibility_status"] = "transcript_substitution_candidate_not_validate_ir_ready"
    writer_ir["not_validate_ir_ready_reason"] = (
        "Transcript rows are available, but final source review, row_start/row_end, "
        "YMM4 base project, audio timing, and production maps are still missing."
    )
    writer_ir["transcript_substitution"] = {
        "transcript_status": probe["transcript_status"],
        "timing_status": probe["timing_status"],
        "audio_status": probe["audio_status"],
        "source_mode": probe["source_mode"],
        "selected_transcript_path": str(selected_transcript),
    }

    cue_packet = _cue_packet_candidate_payload(episode_bridge, selected, dialogue, sections)
    cue_readiness = _cue_packet_readiness_payload(
        output_dir=output_root,
        cue_packet=cue_packet,
        probe=probe,
        utterance_count=len(dialogue),
    )
    contract = _transcript_input_contract_payload(
        package_dir=source_root,
        output_dir=output_root,
        selected_transcript=selected_transcript,
        source_mode=probe["source_mode"],
        script_speakers=sorted({utterance.speaker for utterance in script.utterances}),
        mapped_speakers=sorted({row.speaker for row in assembled.rows}),
        utterance_count=len(dialogue),
        unmapped_speakers=unmapped,
        unlabeled=unlabeled,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        package_dir=source_root,
        output_dir=output_root,
        episode_bridge=episode_bridge,
        probe=probe,
    )

    _write_json(output_root / "substitution_manifest.json", manifest)
    _write_json(output_root / "transcript_input_contract.json", contract)
    _write_json(output_root / "transcript_source_probe.json", probe)
    _write_json(output_root / "regenerated_episode_bridge.json", episode_bridge)
    _write_json(output_root / "regenerated_writer_ir_candidate.json", writer_ir)
    _write_json(output_root / "regenerated_cue_packet_candidate.json", cue_packet)
    _write_text(output_root / "regenerated_cue_packet_candidate.md", _render_cue_packet_markdown(cue_packet))
    _write_draft_csv(output_root / "regenerated_draft_yymm4.csv", dialogue)
    _write_json(output_root / "cue_packet_readiness.json", cue_readiness)
    _write_text(output_root / "source_to_transcript_mapping.md", _render_source_to_transcript_mapping(episode_bridge, probe))
    _write_text(output_root / "limitations.md", _render_limitations(probe))

    readback = validate_transcript_substitution_package(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_transcript_substitution_package(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_transcript_substitution_package(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated transcript substitution/readiness package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES}
    support_files = {name: root / name for name in SUPPORT_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["substitution_manifest.json"])
    contract = _load_json_if_present(files["transcript_input_contract.json"])
    probe = _load_json_if_present(files["transcript_source_probe.json"])
    episode_bridge = _load_json_if_present(files["regenerated_episode_bridge.json"])
    writer_ir = _load_json_if_present(files["regenerated_writer_ir_candidate.json"])
    cue_readiness = _load_json_if_present(files["cue_packet_readiness.json"])
    csv_rows = _load_csv_rows_if_present(files["regenerated_draft_yymm4.csv"])

    json_payloads = {
        "substitution_manifest": manifest,
        "transcript_input_contract": contract,
        "transcript_source_probe": probe,
        "regenerated_episode_bridge": episode_bridge,
        "regenerated_writer_ir_candidate": writer_ir,
        "cue_packet_readiness": cue_readiness,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["substitution_manifest"]
    contract = json_payloads["transcript_input_contract"]
    probe = json_payloads["transcript_source_probe"]
    episode_bridge = json_payloads["regenerated_episode_bridge"]
    writer_ir = json_payloads["regenerated_writer_ir_candidate"]
    cue_readiness = json_payloads["cue_packet_readiness"]

    source_boundary = episode_bridge.get("source_boundary", {})
    transcript_boundary = episode_bridge.get("transcript_substitution", {}).get("transcript_boundary", {})
    readiness = episode_bridge.get("readiness", {})
    blocked_actions = episode_bridge.get("blocked_public_actions", [])
    utterances = writer_ir.get("utterances", [])

    if not source_boundary.get("source_name"):
        failed_checks.append("source_boundary_missing")
    for field in (
        "source_name",
        "source_url_or_placeholder",
        "freshness_status",
        "rights_status",
        "attribution_note",
        "production_status",
        "transcript_status",
        "timing_status",
        "audio_status",
    ):
        if not transcript_boundary.get(field):
            failed_checks.append(f"transcript_boundary_missing:{field}")
    if not transcript_boundary.get("excluded_claims"):
        failed_checks.append("transcript_boundary_missing:excluded_claims")
    if readiness.get("production_status") != "blocked_until_transcript_timing_and_human_review":
        failed_checks.append("production_boundary_missing")
    if readiness.get("audio_status") != "no_audio_generated_or_imported":
        failed_checks.append("audio_boundary_missing")
    if blocked_actions != list(BLOCKED_PUBLIC_ACTIONS):
        failed_checks.append("blocked_public_actions_missing")
    if len(csv_rows) < 2:
        failed_checks.append("regenerated_csv_too_short")
    if len(csv_rows) != len(utterances):
        failed_checks.append("writer_ir_csv_row_count_mismatch")
    if writer_ir.get("compatibility_status") != "transcript_substitution_candidate_not_validate_ir_ready":
        failed_checks.append("writer_ir_status_mismatch")
    if cue_readiness.get("external_llm_called") is not False:
        failed_checks.append("cue_packet_boundary_missing")
    if manifest.get("boundaries", {}).get("local_offline_review_only") is not True:
        failed_checks.append("manifest_offline_boundary_missing")
    if contract.get("normalization_readback", {}).get("utterance_count") != len(csv_rows):
        failed_checks.append("contract_row_count_mismatch")

    support_presence = {name: path.exists() for name, path in support_files.items()}
    return {
        "schema_version": "transcript_substitution_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "support_files": {name: str(path) for name, path in support_files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "support_dropzone_present": support_presence["real_input/README.md"],
            "sample_fixture_present": support_presence["sample_inputs/notebooklm_like_sample.txt"],
            "regenerated_csv_has_rows": len(csv_rows) >= 2,
            "writer_ir_matches_csv_rows": len(csv_rows) == len(utterances),
            "source_boundary_preserved": bool(source_boundary.get("source_name")),
            "transcript_boundary_preserved": bool(transcript_boundary.get("source_name")),
            "blocked_public_actions_preserved": blocked_actions == list(BLOCKED_PUBLIC_ACTIONS),
            "not_production_ready": readiness.get("production_status") == "blocked_until_transcript_timing_and_human_review",
            "no_audio_generated": readiness.get("audio_status") == "no_audio_generated_or_imported",
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate_id": episode_bridge.get("selected_candidate_id"),
        "source_mode": probe.get("source_mode"),
        "transcript_status": probe.get("transcript_status"),
        "regenerated_csv_rows": len(csv_rows),
        "next_action": (
            "Drop a real NotebookLM/source transcript into real_input/ or rerun with "
            "--transcript, then review regenerated_writer_ir_candidate.json and "
            "regenerated_draft_yymm4.csv before any validate-ir/apply-production work."
        ),
    }


def _probe_transcript_source(
    *,
    package_dir: Path,
    output_dir: Path,
    explicit_transcript: Path | None,
    source: dict[str, Any],
) -> dict[str, Any]:
    inspected_locations = [str(package_dir / dirname) for dirname in _TRANSCRIPT_CANDIDATE_DIRS]
    dropzone = output_dir / "real_input" / "README.md"
    _write_text(dropzone, _render_dropzone_readme())

    selected_path: Path
    source_mode: str
    if explicit_transcript is not None:
        if not explicit_transcript.exists():
            raise FileNotFoundError(explicit_transcript)
        selected_path = explicit_transcript
        source_mode = "provided_transcript"
    else:
        local_candidate = _find_local_transcript(package_dir)
        if local_candidate is not None:
            selected_path = local_candidate
            source_mode = "local_transcript_found"
        else:
            selected_path = output_dir / "sample_inputs" / "notebooklm_like_sample.txt"
            _write_text(selected_path, _sample_transcript_text(source))
            source_mode = "sample_fixture_generated"

    is_sample = source_mode == "sample_fixture_generated"
    selected_candidate = source["selected_candidate"]
    return {
        "schema_version": "transcript_source_probe.v1",
        "status": "sample_fixture_used" if is_sample else "transcript_input_used",
        "source_mode": source_mode,
        "selected_transcript_path": str(selected_path),
        "selected_transcript_exists": selected_path.exists(),
        "inspected_locations": inspected_locations,
        "real_input_dropzone": str(output_dir / "real_input"),
        "sample_fixture_path": str(output_dir / "sample_inputs" / "notebooklm_like_sample.txt"),
        "sample_fixture_used": is_sample,
        "selected_candidate_id": selected_candidate.get("candidate_id"),
        "transcript_status": "sample_fixture_not_real" if is_sample else "local_transcript_unverified",
        "timing_status": "no_audio_or_yymm4_timing",
        "audio_status": "no_audio_generated_or_imported",
        "production_status": "local_offline_readiness_only",
        "access_reality": {
            "real_transcript_found_for_current_package": not is_sample,
            "sample_fixture_is_real_transcript": False,
            "notebooklm_api_used": False,
            "live_fetch_used": False,
        },
        "boundary_fields": _transcript_boundary(selected_path, source_mode),
    }


def _find_local_transcript(package_dir: Path) -> Path | None:
    for dirname in _TRANSCRIPT_CANDIDATE_DIRS:
        root = package_dir / dirname
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in _TRANSCRIPT_SUFFIXES and path.name.lower() != "readme.md":
                return path
    return None


def _apply_transcript_readiness(
    *,
    episode_bridge: dict[str, Any],
    probe: dict[str, Any],
    selected_transcript: Path,
    utterance_count: int,
) -> None:
    transcript_boundary = probe["boundary_fields"]
    episode_bridge["transcript_substitution"] = {
        "schema_version": "content_spine_transcript_substitution.v1",
        "source_mode": probe["source_mode"],
        "selected_transcript_path": str(selected_transcript),
        "utterance_count": utterance_count,
        "sample_fixture_used": probe["sample_fixture_used"],
        "transcript_boundary": transcript_boundary,
        "dropzone": probe["real_input_dropzone"],
    }
    episode_bridge["readiness"] = {
        "writer_ir_candidate_status": "transcript_substitution_candidate_generated",
        "cue_packet_status": "transcript_substitution_candidate_generated",
        "ymm4_csv_status": "transcript_csv_preview_generated_not_production",
        "row_range_status": "transcript_rows_available_without_yymm4_timing",
        "audio_timing_status": "not_available_until_yymm4_import",
        "maps_status": "not_selected",
        "production_status": "blocked_until_transcript_timing_and_human_review",
        "transcript_status": probe["transcript_status"],
        "timing_status": probe["timing_status"],
        "audio_status": probe["audio_status"],
    }
    episode_bridge["missing_for_production"] = [
        "human-reviewed real transcript if the sample fixture was used",
        "source and claim review against real materials",
        "YMM4 CSV import and VoiceItem timing",
        "row_start/row_end annotation",
        "face/bg/slot/overlay/se/motion maps if the episode uses them",
        "human rights/legal/publication review",
    ]


def _transcript_boundary(path: Path, source_mode: str) -> dict[str, Any]:
    is_sample = source_mode == "sample_fixture_generated"
    if is_sample:
        source_name = "NLMYTGen local sample transcript fixture"
        freshness = "sample_fixture_generated_current_checkout_not_live"
        rights = "sample_only_no_publication"
        attribution = (
            "Generated from the current offline content spine draft dialogue to exercise "
            "transcript intake; it is not a real NotebookLM transcript."
        )
        production = "local_readiness_fixture_only"
        transcript_status = "sample_fixture_not_real"
    else:
        source_name = path.name
        freshness = "local_file_unverified"
        rights = "requires_human_rights_review_before_public_use"
        attribution = "Local transcript input supplied or discovered in the repo; provenance is not independently verified."
        production = "local_transcript_readiness_only"
        transcript_status = "local_transcript_unverified"

    return {
        "source_name": source_name,
        "source_url_or_placeholder": f"offline://{path.as_posix()}",
        "freshness_status": freshness,
        "rights_status": rights,
        "attribution_note": attribution,
        "excluded_claims": [
            "No public-ready source or rights acceptance.",
            "No audio timing, YMM4 import proof, render proof, or publication readiness.",
            "No live fetch, media download, OAuth/API, or paid service use.",
        ],
        "production_status": production,
        "transcript_status": transcript_status,
        "timing_status": "no_audio_or_yymm4_timing",
        "audio_status": "no_audio_generated_or_imported",
    }


def _transcript_input_contract_payload(
    *,
    package_dir: Path,
    output_dir: Path,
    selected_transcript: Path,
    source_mode: str,
    script_speakers: list[str],
    mapped_speakers: list[str],
    utterance_count: int,
    unmapped_speakers: list[str],
    unlabeled: bool,
) -> dict[str, Any]:
    return {
        "schema_version": "transcript_input_contract.v1",
        "purpose": "Accept real or NotebookLM-like transcript input for content spine IR/CSV substitution.",
        "accepted_inputs": [
            {
                "extension": ".csv",
                "shape": "two columns: speaker,text; header row is optional and skipped when detected",
            },
            {
                "extension": ".txt",
                "shape": "speaker-tagged lines such as Speaker: text or timestamped [00:00] Speaker: text",
            },
            {
                "extension": ".txt",
                "shape": "unlabeled alternating Speaker_A/Speaker_B lines when --unlabeled is set",
            },
        ],
        "dropzone": str(output_dir / "real_input"),
        "package_dir": str(package_dir),
        "selected_transcript_path": str(selected_transcript),
        "source_mode": source_mode,
        "speaker_mapping": {
            "unlabeled": unlabeled,
            "input_speakers": script_speakers,
            "mapped_speakers": mapped_speakers,
            "unmapped_speakers": unmapped_speakers,
            "map_required_for_yukkuri_names": bool(unmapped_speakers),
        },
        "required_boundary_fields": [
            "source_name",
            "source_url_or_placeholder",
            "freshness_status",
            "rights_status",
            "attribution_note",
            "excluded_claims",
            "production_status",
            "transcript_status",
            "timing_status",
            "audio_status",
        ],
        "normalization_readback": {
            "utterance_count": utterance_count,
            "csv_rows_expected": utterance_count,
            "parser": "src.pipeline.normalize.normalize",
        },
        "closed_gates": list(BLOCKED_PUBLIC_ACTIONS),
    }


def _manifest_payload(
    *,
    artifact_id: str,
    package_dir: Path,
    output_dir: Path,
    episode_bridge: dict[str, Any],
    probe: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "transcript_substitution_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "real-transcript-substitution-readiness",
        "status": "generated",
        "source_package_dir": str(package_dir),
        "output_dir": str(output_dir),
        "selected_candidate_id": episode_bridge["selected_candidate_id"],
        "source_mode": probe["source_mode"],
        "transcript_status": probe["transcript_status"],
        "timing_status": probe["timing_status"],
        "audio_status": probe["audio_status"],
        "files": {name: str(output_dir / name) for name in REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES},
        "support_files": {name: str(output_dir / name) for name in SUPPORT_FILES},
        "readiness": episode_bridge["readiness"],
        "boundaries": {
            "local_offline_review_only": True,
            "sample_fixture_is_not_real_transcript": probe["sample_fixture_used"],
            "draft_csv_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_ymm4_gui_launch_or_render": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
        },
    }


def _cue_packet_readiness_payload(
    *,
    output_dir: Path,
    cue_packet: dict[str, Any],
    probe: dict[str, Any],
    utterance_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": "cue_packet_readiness.v1",
        "status": "candidate_regenerated_not_sent",
        "cue_packet_path": str(output_dir / "regenerated_cue_packet_candidate.json"),
        "cue_packet_markdown_path": str(output_dir / "regenerated_cue_packet_candidate.md"),
        "phase": cue_packet.get("phase"),
        "transcript_rows": utterance_count,
        "source_mode": probe["source_mode"],
        "external_llm_called": False,
        "ready_for_human_review": True,
        "not_ready_for_production": True,
        "remaining_gaps": [
            "real transcript provenance and rights review" if probe["sample_fixture_used"] else "transcript provenance and rights review",
            "YMM4 import/audio timing",
            "row range annotation",
            "production maps and validate-ir/apply-production inputs",
        ],
    }


def _sample_transcript_text(source: dict[str, Any]) -> str:
    selected = source["selected_candidate"]
    lines = []
    for row in _draft_dialogue(selected):
        lines.append(f"{row['speaker']}: {row['text']}")
    return "\n".join(lines) + "\n"


def _render_dropzone_readme() -> str:
    return "\n".join([
        "# Real Input Drop-Zone",
        "",
        "Place a real NotebookLM or human-reviewed transcript here as UTF-8 `.txt` or `.csv`, then rerun:",
        "",
        "`python -m src.cli.main build-transcript-substitution --package production_pilots/yukkuri_newsroom_content_spine_001`",
        "",
        "Accepted text shapes:",
        "",
        "- `Speaker: text`",
        "- `[00:00] Speaker: text`",
        "- two-column CSV: `speaker,text`",
        "- unlabeled alternating lines only when rerun with `--unlabeled` and a speaker map",
        "",
        "Do not place source media, credentials, OAuth tokens, paid API data, or rights-uncleared public assets here.",
        "",
    ])


def _render_source_to_transcript_mapping(episode_bridge: dict[str, Any], probe: dict[str, Any]) -> str:
    lines = [
        "# Source To Transcript Mapping",
        "",
        "| Source / transcript item | Regenerated field | Status |",
        "|---|---|---|",
        "| content spine selected_candidate_id | regenerated_episode_bridge.selected_candidate_id / regenerated_writer_ir_candidate.video_id | preserved |",
        "| content spine source_boundary | regenerated_episode_bridge.source_boundary / regenerated_writer_ir_candidate.source_boundary | preserved |",
        "| transcript_source_probe.selected_transcript_path | regenerated_episode_bridge.transcript_substitution.selected_transcript_path | mapped |",
        "| normalized transcript rows | regenerated_episode_bridge.draft_dialogue / regenerated_writer_ir_candidate.utterances / regenerated_draft_yymm4.csv | mapped |",
        "| transcript boundary fields | regenerated_episode_bridge.transcript_substitution.transcript_boundary | preserved |",
        "| audio timing | row_start/row_end and YMM4 VoiceItem timing | pending |",
        "| YMM4 base project | validate-ir/apply-production inputs | pending |",
        "",
        "## Current Input Reality",
        "",
        f"- source_mode: `{probe['source_mode']}`",
        f"- transcript_status: `{probe['transcript_status']}`",
        f"- sample_fixture_used: `{probe['sample_fixture_used']}`",
        f"- selected_candidate_id: `{episode_bridge['selected_candidate_id']}`",
        "",
    ]
    return "\n".join(lines)


def _render_limitations(probe: dict[str, Any]) -> str:
    lines = [
        "# Transcript Substitution Limitations",
        "",
        "This package is a local/offline readiness checkpoint. It proves the bridge can accept a transcript-shaped input and regenerate downstream draft artifacts.",
        "",
        "Current input reality:",
        "",
        f"- source_mode: `{probe['source_mode']}`",
        f"- transcript_status: `{probe['transcript_status']}`",
        f"- timing_status: `{probe['timing_status']}`",
        f"- audio_status: `{probe['audio_status']}`",
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
        "- NotebookLM API use or live source acquisition",
        "",
    ])
    if probe["sample_fixture_used"]:
        lines.extend([
            "The included sample fixture is not a real transcript and must not be treated as production material.",
            "",
        ])
    return "\n".join(lines)


def _write_draft_csv(path: Path, dialogue: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        for row in dialogue:
            writer.writerow([row["speaker"], row["text"]])


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_csv_rows_if_present(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return [row for row in csv.reader(file) if row]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

"""Build and validate the Episode 002 verified-local-evidence pilot.

This module deliberately separates three evidence levels:

* tracked source/script/CSV and project contracts prepared headlessly;
* a local YMM4 import base that must be created by the operator; and
* a local internal-review project/render that must not be treated as
  production, public, editorial, or rights approval.

The project generator preserves every imported VoiceItem object byte-for-byte
at the JSON-object level and only appends three neutral ImageItems plus three
independent TextItems.  It never synthesizes or rewrites YMM4 voice caches.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.pipeline.ymmp_openability import normalize_ymmp_openability
from src.pipeline.ymmp_patch import (
    _get_timeline_items,
    _item_type,
    load_ymmp,
    save_ymmp,
)
from src.pipeline.ymm4_diagnostic_placeholder_proof import (
    _audit_project_paths,
    _make_image_item,
    _make_text_item,
    _png_metadata,
    _write_neutral_png,
)


EPISODE_ID = "yukkuri_newsroom_content_spine_002"
ARTIFACT_ID = "episode_002_verified_local_evidence_input_pilot_v1"
DEFAULT_OUTPUT_DIRNAME = "verified_local_evidence_input_pilot"

SOURCE_MANIFEST_FILENAME = "source_bundle_manifest.json"
PROVENANCE_NOTE_FILENAME = "source_provenance_and_rights_note.md"
VALIDATED_INPUT_RECEIPT_FILENAME = "validated_local_input_receipt.json"
CLAIM_LEDGER_FILENAME = "source_claim_ledger.json"
SCRIPT_RECEIPT_FILENAME = "script_generation_receipt.json"
CANONICAL_SCRIPT_TEXT_FILENAME = "canonical_script.txt"
CANONICAL_SCRIPT_JSON_FILENAME = "canonical_script.json"
CANONICAL_CSV_FILENAME = "canonical_yymm4.csv"
DERIVED_CSV_FILENAME = "derived_yymm4_import.csv"
INPUT_READBACK_FILENAME = "input_validation_readback.json"
PROJECT_MANIFEST_FILENAME = "internal_project_manifest.json"
STATIC_PROJECT_READBACK_FILENAME = "static_project_readback.json"
PROJECT_RECEIPT_FILENAME = "project_generation_receipt.json"
ASSET_RELATIVE_PATH = Path("assets/internal_review_placeholder.png")

OPERATOR_DIRNAME = "operator_batch"
OPERATOR_README_FILENAME = "README_OPERATOR_BATCH.md"
OPERATOR_MANIFEST_FILENAME = "operator_batch_manifest.json"
OPERATOR_SCRIPT_FILENAME = "run_yymm4_operator_batch.ps1"
OPERATOR_RETURN_FILENAME = "operator_return_template.md"
OPERATOR_PREFLIGHT_FILENAME = "preflight_readback.json"
EXPECTED_OUTPUT_FILENAME = "expected_output_contract.json"
COLLECTOR_SCRIPT_FILENAME = "collect_operator_result.ps1"

LOCAL_OUTPUT_DIRNAME = "local_outputs"
LOCAL_IMPORT_BASE_FILENAME = "episode_002_verified_local_evidence_import_base.local.ymmp"
LOCAL_PROJECT_FILENAME = "episode_002_verified_local_evidence_internal_review.local.ymmp"
LOCAL_RENDER_FILENAME = "episode_002_verified_local_evidence_internal_review.mp4"
LOCAL_ACTUAL_READBACK_FILENAME = "static_project_readback.actual.json"
LOCAL_GENERATION_RECEIPT_FILENAME = "project_generation_receipt.actual.json"
LOCAL_OPERATOR_RESULT_FILENAME = "operator_result.json"
LOCAL_BATCH_MARKER_FILENAME = "operator_batch_started.local.txt"

SCENE_ROWS = (("S1", 0, 2), ("S2", 2, 4), ("S3", 4, 9))
CANONICAL_SPEAKERS = {"れいむ", "まりさ"}
EXPECTED_CANONICAL_COUNTS = {"れいむ": 3, "まりさ": 6}
EXPECTED_CHARACTER_COUNTS = {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
LABEL_TEMPLATE = (
    "{scene_id} | INTERNAL REVIEW | NOT FINAL | LOCAL EVIDENCE PILOT"
)
REMARK_PREFIX = "episode002:verified_local_evidence:"
BOUNDARY_TOKENS = ("INTERNAL REVIEW", "NOT FINAL", "LOCAL EVIDENCE PILOT")

CSV_RECEIPT_RELATIVE = Path("ymm4_csv_gate_observation_receipt_2026-07-11.json")
DIAGNOSTIC_ROOT_RELATIVE = Path("ymm4_diagnostic_placeholder_proof")
DIAGNOSTIC_MANIFEST_RELATIVE = DIAGNOSTIC_ROOT_RELATIVE / "diagnostic_project_manifest.json"
DIAGNOSTIC_READBACK_RELATIVE = DIAGNOSTIC_ROOT_RELATIVE / "diagnostic_project_readback.json"
DIAGNOSTIC_RECEIPT_RELATIVE = DIAGNOSTIC_ROOT_RELATIVE / "diagnostic_project_receipt.json"
PROFILE_RELATIVE = Path(
    "ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json"
)
RUNTIME_STATE_RELATIVE = Path("docs/runtime-state.md")


CUES: tuple[dict[str, Any], ...] = (
    {
        "cue_id": "cue_001",
        "scene_id": "S1",
        "speaker": "れいむ",
        "text": "9行のCSVをYMM4に読み込み、話者割り当てと順番を確認したよ。",
        "claim_summary": "The observed import contained nine ordered rows with matching speaker assignments.",
        "source_id": "csv_gate_observation_receipt",
        "json_pointer": "/actual_ymm4_imported",
        "evidence": (
            ("csv_gate_observation_receipt", "/actual_ymm4_imported", True),
            ("csv_gate_observation_receipt", "/five_point_observations/subtitle_text/speaker_cue_match", True),
            (
                "csv_gate_observation_receipt",
                "/five_point_observations/cue_order/cue_order",
                [f"csv_row_{index}" for index in range(1, 10)],
            ),
        ),
    },
    {
        "cue_id": "cue_002",
        "scene_id": "S1",
        "speaker": "まりさ",
        "text": "CSV取り込みの観測結果は合格で、9件のボイス項目に欠けや重複、並べ替えはなかったぜ。",
        "claim_summary": "The bounded CSV observation passed with nine VoiceItems and no missing, duplicate, or reordered cues.",
        "source_id": "csv_gate_observation_receipt",
        "json_pointer": "/five_point_observations/voice_items",
        "evidence": (
            ("csv_gate_observation_receipt", "/status", "passed"),
            ("csv_gate_observation_receipt", "/five_point_observations/voice_items/count", 9),
            ("csv_gate_observation_receipt", "/five_point_observations/voice_items/missing_cue_ids", []),
            ("csv_gate_observation_receipt", "/five_point_observations/voice_items/duplicate_cue_ids", []),
            ("csv_gate_observation_receipt", "/five_point_observations/voice_items/reordered", False),
        ),
    },
    {
        "cue_id": "cue_003",
        "scene_id": "S2",
        "speaker": "まりさ",
        "text": "この取り込みでは対応表は表示されず、霊夢3件、魔理沙6件へ自動で結び付いたぜ。",
        "claim_summary": "In this observed import, no mapping dialog appeared and the explicit characters were bound 3/6.",
        "source_id": "csv_gate_observation_receipt",
        "json_pointer": "/five_point_observations/subtitle_text",
        "evidence": (
            ("csv_gate_observation_receipt", "/five_point_observations/subtitle_text/mapping_dialog_present", False),
            ("csv_gate_observation_receipt", "/five_point_observations/subtitle_text/automatic_speaker_binding_observed", True),
            (
                "csv_gate_observation_receipt",
                "/five_point_observations/subtitle_text/character_counts",
                EXPECTED_CHARACTER_COUNTS,
            ),
        ),
    },
    {
        "cue_id": "cue_004",
        "scene_id": "S2",
        "speaker": "まりさ",
        "text": "観測時はテキストと順番が一致し、60fpsで2790フレーム、46.5秒のタイムラインだったぜ。",
        "claim_summary": "The observed diagnostic-source timeline preserved text/order and measured 60 fps, 2790 frames, and 46.5 seconds.",
        "source_id": "csv_gate_observation_receipt",
        "json_pointer": "/five_point_observations/timing_order",
        "evidence": (
            ("csv_gate_observation_receipt", "/five_point_observations/subtitle_text/all_text_matched", True),
            ("csv_gate_observation_receipt", "/five_point_observations/timing_order/order_preserved", True),
            ("csv_gate_observation_receipt", "/five_point_observations/timing_order/frame_rate", 60),
            ("csv_gate_observation_receipt", "/five_point_observations/timing_order/total_frames", 2790),
            ("csv_gate_observation_receipt", "/five_point_observations/timing_order/duration_seconds", 46.5),
        ),
    },
    {
        "cue_id": "cue_005",
        "scene_id": "S3",
        "speaker": "れいむ",
        "text": "別の診断用プロジェクトでも、9件のボイスと連動字幕が保たれていたよ。",
        "claim_summary": "The separate diagnostic GUI reopen preserved nine VoiceItems and linked subtitles.",
        "source_id": "diagnostic_project_receipt",
        "json_pointer": "/observations/VoiceItems",
        "evidence": (
            ("diagnostic_project_receipt", "/observations/VoiceItems", 9),
            ("diagnostic_project_receipt", "/observations/linked_subtitles_preserved", True),
            ("diagnostic_project_receipt", "/safety/diagnostic_only", True),
        ),
    },
    {
        "cue_id": "cue_006",
        "scene_id": "S3",
        "speaker": "まりさ",
        "text": "3つのシーンには、画像と独立したテキストが1件ずつ置かれていたぜ。",
        "claim_summary": "Each of the three diagnostic scenes structurally contained one ImageItem and one independent TextItem.",
        "source_id": "diagnostic_project_readback",
        "json_pointer": "/scenes",
        "evidence": tuple(
            ("diagnostic_project_readback", f"/scenes/{index}/{field}", 1)
            for index in range(3)
            for field in ("ImageItem_count", "TextItem_count")
        )
        + (
            (
                "diagnostic_project_readback",
                "/checks/independent_TextItem_count_3",
                True,
            ),
        ),
    },
    {
        "cue_id": "cue_007",
        "scene_id": "S3",
        "speaker": "まりさ",
        "text": "各ラベルには診断用で最終版ではないことが明記され、再確認時にも読めたぜ。",
        "claim_summary": "The diagnostic labels explicitly marked non-final status and were readable on GUI reopen.",
        "source_id": "diagnostic_project_receipt",
        "json_pointer": "/observations/placeholder_is_explicitly_non_final",
        "evidence": (
            ("diagnostic_project_receipt", "/observations/placeholder_is_explicitly_non_final", True),
            (
                "diagnostic_project_receipt",
                "/observations/scene_labels_readable",
                [
                    "S1 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
                    "S2 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
                    "S3 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
                ],
            ),
            ("diagnostic_project_receipt", "/observed_by_environment/observation_mode", "actual_gui_reopen"),
        ),
    },
    {
        "cue_id": "cue_008",
        "scene_id": "S3",
        "speaker": "れいむ",
        "text": "ただし、映像の書き出しや本番用プロジェクトの作成は行っていないよ。",
        "claim_summary": "The observed diagnostic gate did not render/export or create a production project.",
        "source_id": "diagnostic_project_receipt",
        "json_pointer": "/observations/render_or_export_performed",
        "evidence": (
            ("diagnostic_project_receipt", "/observations/render_or_export_performed", False),
            ("diagnostic_project_receipt", "/safety/production_ymmp_written", False),
        ),
    },
    {
        "cue_id": "cue_009",
        "scene_id": "S3",
        "speaker": "まりさ",
        "text": "実素材への置き換え、権利や公開の承認、アップロードも行っていないぜ。",
        "claim_summary": "The observed diagnostic gate did not replace real input, approve rights/publication, or upload.",
        "source_id": "diagnostic_project_receipt",
        "json_pointer": "/safety/real_input_replaced",
        "evidence": (
            ("diagnostic_project_receipt", "/safety/real_input_replaced", False),
            ("diagnostic_project_receipt", "/safety/rights_or_public_approval_performed", False),
            ("diagnostic_project_receipt", "/safety/upload_performed", False),
        ),
    },
)


def build_verified_local_evidence_input_pilot(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Build every tracked, headless artifact for the pilot."""
    package = Path(package_dir).resolve()
    repo_root = package.parents[1]
    output = (
        Path(output_dir).resolve()
        if output_dir is not None
        else package / DEFAULT_OUTPUT_DIRNAME
    )
    output.mkdir(parents=True, exist_ok=True)
    (output / OPERATOR_DIRNAME).mkdir(parents=True, exist_ok=True)

    source_paths = _source_paths(package, repo_root)
    source_payloads = _load_and_validate_sources(source_paths)
    profile = source_payloads["yymm4_character_profile"]
    canonical_rows = [(cue["speaker"], cue["text"]) for cue in CUES]
    mapping = _validated_profile_mapping(profile, canonical_rows)
    derived_rows = [(mapping[speaker], text) for speaker, text in canonical_rows]

    _write_text(
        output / ".gitignore",
        "!canonical_yymm4.csv\n!derived_yymm4_import.csv\nlocal_outputs/\n*.local.ymmp\n*.mp4\n",
    )
    _write_neutral_png(output / ASSET_RELATIVE_PATH)

    source_manifest = _build_source_manifest(
        artifact_id=ARTIFACT_ID,
        source_paths=source_paths,
        source_payloads=source_payloads,
        repo_root=repo_root,
    )
    _write_json(output / SOURCE_MANIFEST_FILENAME, source_manifest)
    _write_text(output / PROVENANCE_NOTE_FILENAME, _provenance_note())

    claim_ledger = _build_claim_ledger(source_paths, repo_root)
    _write_json(output / CLAIM_LEDGER_FILENAME, claim_ledger)
    script = _build_script_payload()
    _write_json(output / CANONICAL_SCRIPT_JSON_FILENAME, script)
    _write_text(output / CANONICAL_SCRIPT_TEXT_FILENAME, _render_script_text(script))
    _write_csv(output / CANONICAL_CSV_FILENAME, canonical_rows)
    _write_csv(output / DERIVED_CSV_FILENAME, derived_rows)

    project_manifest, project_readback, project_receipt = _project_contracts(
        source_payloads=source_payloads,
        derived_rows=derived_rows,
        output=output,
    )
    _write_json(output / PROJECT_MANIFEST_FILENAME, project_manifest)
    _write_json(output / STATIC_PROJECT_READBACK_FILENAME, project_readback)
    _write_json(output / PROJECT_RECEIPT_FILENAME, project_receipt)

    _write_operator_batch(output=output, source_payloads=source_payloads)

    script_receipt = {
        "schema_version": "verified_local_evidence_script_generation_receipt.v1",
        "artifact_id": f"{ARTIFACT_ID}_script_generation",
        "status": "passed",
        "generation_mode": "deterministic_authorized_evidence_paraphrase",
        "cue_count": 9,
        "scene_allocation": {"S1": 2, "S2": 2, "S3": 5},
        "canonical_speaker_counts": EXPECTED_CANONICAL_COUNTS,
        "derived_character_counts": EXPECTED_CHARACTER_COUNTS,
        "unsupported_claim_count": 0,
        "files": {
            CLAIM_LEDGER_FILENAME: _sha256(output / CLAIM_LEDGER_FILENAME),
            CANONICAL_SCRIPT_TEXT_FILENAME: _sha256(output / CANONICAL_SCRIPT_TEXT_FILENAME),
            CANONICAL_SCRIPT_JSON_FILENAME: _sha256(output / CANONICAL_SCRIPT_JSON_FILENAME),
            CANONICAL_CSV_FILENAME: _sha256(output / CANONICAL_CSV_FILENAME),
            DERIVED_CSV_FILENAME: _sha256(output / DERIVED_CSV_FILENAME),
        },
        "spoken_content_boundaries": {
            "absolute_paths_present": False,
            "hashes_or_commit_ids_present": False,
            "device_or_private_metadata_present": False,
            "production_or_public_ready_claimed": False,
        },
    }
    _write_json(output / SCRIPT_RECEIPT_FILENAME, script_receipt)

    validated_receipt = {
        "schema_version": "validated_local_input_receipt.v1",
        "artifact_id": f"{ARTIFACT_ID}_validated_input",
        "status": "passed",
        "input_kind": "tracked_local_project_evidence",
        "source_count": len(source_manifest["sources"]),
        "source_hashes_match": True,
        "source_schemas_and_statuses_match": True,
        "external_fetch_performed": False,
        "external_asset_used": False,
        "editorial_adoption": False,
        "rights_or_legal_approval": False,
        "public_ready": False,
        "production_ready": False,
        "claim_count": 9,
        "unsupported_claim_count": 0,
        "next_gate": "manual_yymm4_render_batch",
    }
    _write_json(output / VALIDATED_INPUT_RECEIPT_FILENAME, validated_receipt)

    readback = validate_verified_local_evidence_input_pilot(
        pilot_dir=output,
        package_dir=package,
        require_input_readback=False,
    )
    _write_json(output / INPUT_READBACK_FILENAME, readback)
    final_readback = validate_verified_local_evidence_input_pilot(
        pilot_dir=output,
        package_dir=package,
        require_input_readback=True,
    )
    if final_readback["status"] != "passed":
        raise ValueError(
            "VERIFIED_LOCAL_EVIDENCE_PILOT_VALIDATION_FAILED: "
            + ", ".join(final_readback["failed_checks"])
        )
    return {
        "status": "operator_batch_ready",
        "output_dir": str(output),
        "source_count": len(source_manifest["sources"]),
        "cue_count": 9,
        "manual_action_count": 5,
        "validation": final_readback,
        "local_project_target": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_PROJECT_FILENAME}",
        "render_target": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_RENDER_FILENAME}",
    }


def validate_verified_local_evidence_input_pilot(
    *,
    pilot_dir: str | Path,
    package_dir: str | Path | None = None,
    require_input_readback: bool = True,
) -> dict[str, Any]:
    """Independently validate the tracked source-to-operator contract."""
    root = Path(pilot_dir).resolve()
    package = _resolve_package_dir(root, package_dir)
    repo_root = package.parents[1]
    source_paths = _source_paths(package, repo_root)
    failed: list[str] = []

    required = [
        SOURCE_MANIFEST_FILENAME,
        PROVENANCE_NOTE_FILENAME,
        VALIDATED_INPUT_RECEIPT_FILENAME,
        CLAIM_LEDGER_FILENAME,
        SCRIPT_RECEIPT_FILENAME,
        CANONICAL_SCRIPT_TEXT_FILENAME,
        CANONICAL_SCRIPT_JSON_FILENAME,
        CANONICAL_CSV_FILENAME,
        DERIVED_CSV_FILENAME,
        PROJECT_MANIFEST_FILENAME,
        STATIC_PROJECT_READBACK_FILENAME,
        PROJECT_RECEIPT_FILENAME,
        ASSET_RELATIVE_PATH.as_posix(),
        ".gitignore",
        f"{OPERATOR_DIRNAME}/{OPERATOR_README_FILENAME}",
        f"{OPERATOR_DIRNAME}/{OPERATOR_MANIFEST_FILENAME}",
        f"{OPERATOR_DIRNAME}/{OPERATOR_SCRIPT_FILENAME}",
        f"{OPERATOR_DIRNAME}/{OPERATOR_RETURN_FILENAME}",
        f"{OPERATOR_DIRNAME}/{OPERATOR_PREFLIGHT_FILENAME}",
        f"{OPERATOR_DIRNAME}/{EXPECTED_OUTPUT_FILENAME}",
        f"{OPERATOR_DIRNAME}/{COLLECTOR_SCRIPT_FILENAME}",
    ]
    if require_input_readback:
        required.append(INPUT_READBACK_FILENAME)
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        failed.extend(f"missing:{name}" for name in missing)
        return _validation_payload(root, failed, {})

    try:
        source_payloads = _load_and_validate_sources(source_paths)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        failed.append(f"source_contract:{exc}")
        source_payloads = {}

    json_names = [
        SOURCE_MANIFEST_FILENAME,
        VALIDATED_INPUT_RECEIPT_FILENAME,
        CLAIM_LEDGER_FILENAME,
        SCRIPT_RECEIPT_FILENAME,
        CANONICAL_SCRIPT_JSON_FILENAME,
        PROJECT_MANIFEST_FILENAME,
        STATIC_PROJECT_READBACK_FILENAME,
        PROJECT_RECEIPT_FILENAME,
        f"{OPERATOR_DIRNAME}/{OPERATOR_MANIFEST_FILENAME}",
        f"{OPERATOR_DIRNAME}/{OPERATOR_PREFLIGHT_FILENAME}",
        f"{OPERATOR_DIRNAME}/{EXPECTED_OUTPUT_FILENAME}",
    ]
    if require_input_readback:
        json_names.append(INPUT_READBACK_FILENAME)
    payloads: dict[str, dict[str, Any]] = {}
    for name in json_names:
        try:
            payloads[name] = _load_json(root / name)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failed.append(f"json_parse:{name}:{exc}")

    manifest = payloads.get(SOURCE_MANIFEST_FILENAME, {})
    expected_source_records = _build_source_manifest(
        artifact_id=ARTIFACT_ID,
        source_paths=source_paths,
        source_payloads=source_payloads,
        repo_root=repo_root,
    ) if source_payloads else {}
    if manifest != expected_source_records:
        failed.append("source_manifest_recompute_mismatch")

    ledger = payloads.get(CLAIM_LEDGER_FILENAME, {})
    if ledger != _build_claim_ledger(source_paths, repo_root):
        failed.append("claim_ledger_recompute_mismatch")
    claims = _list(ledger.get("claims"))
    if len(claims) != 9:
        failed.append("claim_count_not_9")
    if any(_dict(claim).get("unsupported_claim") is not False for claim in claims):
        failed.append("unsupported_claim_present")
    if any(_dict(claim).get("paraphrase_status") != "paraphrased" for claim in claims):
        failed.append("claim_not_marked_paraphrased")

    script = payloads.get(CANONICAL_SCRIPT_JSON_FILENAME, {})
    expected_script = _build_script_payload()
    if script != expected_script:
        failed.append("canonical_script_recompute_mismatch")
    cues = _list(script.get("cues"))
    scene_counts = dict(Counter(str(_dict(cue).get("scene_id")) for cue in cues))
    speaker_counts = dict(Counter(str(_dict(cue).get("speaker")) for cue in cues))
    if len(cues) != 9 or scene_counts != {"S1": 2, "S2": 2, "S3": 5}:
        failed.append("script_9_cue_3_scene_invariant_failed")
    if speaker_counts != EXPECTED_CANONICAL_COUNTS:
        failed.append("canonical_speaker_counts_failed")
    if (root / CANONICAL_SCRIPT_TEXT_FILENAME).read_text(encoding="utf-8") != _render_script_text(expected_script):
        failed.append("canonical_script_text_recompute_mismatch")

    canonical_rows = _load_csv_rows(root / CANONICAL_CSV_FILENAME)
    derived_rows = _load_csv_rows(root / DERIVED_CSV_FILENAME)
    expected_canonical_rows = [(cue["speaker"], cue["text"]) for cue in CUES]
    if canonical_rows != expected_canonical_rows:
        failed.append("canonical_csv_recompute_mismatch")
    if len(canonical_rows) != 9 or any(len(row) != 2 for row in canonical_rows):
        failed.append("canonical_csv_shape_failed")
    if source_payloads:
        try:
            mapping = _validated_profile_mapping(
                source_payloads["yymm4_character_profile"], canonical_rows
            )
            expected_derived_rows = [
                (mapping[speaker], text) for speaker, text in canonical_rows
            ]
            if derived_rows != expected_derived_rows:
                failed.append("derived_csv_recompute_mismatch")
        except ValueError as exc:
            failed.append(f"strict_profile_coverage:{exc}")
    if [text for _, text in canonical_rows] != [text for _, text in derived_rows]:
        failed.append("canonical_derived_text_order_mismatch")
    if dict(Counter(speaker for speaker, _ in derived_rows)) != EXPECTED_CHARACTER_COUNTS:
        failed.append("derived_character_counts_failed")

    if not _png_metadata(root / ASSET_RELATIVE_PATH).get("valid"):
        failed.append("placeholder_asset_invalid")
    project_manifest = payloads.get(PROJECT_MANIFEST_FILENAME, {})
    project_readback = payloads.get(STATIC_PROJECT_READBACK_FILENAME, {})
    project_receipt = payloads.get(PROJECT_RECEIPT_FILENAME, {})
    if project_manifest.get("status") != "ready_for_operator_generation":
        failed.append("project_manifest_status_failed")
    if project_readback.get("status") != "contract_pass" or any(
        value is not True for value in _dict(project_readback.get("checks")).values()
    ):
        failed.append("static_project_contract_failed")
    if project_receipt.get("actual_local_project_generated") is not False:
        failed.append("project_receipt_overclaims_actual_generation")

    operator_manifest = payloads.get(f"{OPERATOR_DIRNAME}/{OPERATOR_MANIFEST_FILENAME}", {})
    if operator_manifest.get("manual_action_count") != 5:
        failed.append("operator_manual_action_count_failed")
    if len(_list(operator_manifest.get("return_items"))) > 3:
        failed.append("operator_return_item_count_failed")
    preflight = payloads.get(f"{OPERATOR_DIRNAME}/{OPERATOR_PREFLIGHT_FILENAME}", {})
    if preflight.get("status") != "passed" or preflight.get("yymm4_launch_attempted") is not False:
        failed.append("tracked_operator_preflight_failed")
    expected_output = payloads.get(f"{OPERATOR_DIRNAME}/{EXPECTED_OUTPUT_FILENAME}", {})
    if expected_output.get("render_target") != f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_RENDER_FILENAME}":
        failed.append("operator_render_target_mismatch")

    tracked_files = [root / name for name in required if name != INPUT_READBACK_FILENAME]
    tracked_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in tracked_files
        if path.suffix.lower() in {".json", ".md", ".txt", ".ps1", ".gitignore"}
    )
    if re.search(r"[A-Za-z]:\\Users\\|/Users/|file://|https?://", tracked_text, re.IGNORECASE):
        failed.append("private_or_external_reference_present")
    spoken = "\n".join(str(_dict(cue).get("text") or "") for cue in cues)
    if re.search(r"[A-Za-z]:\\|/[A-Za-z0-9_.-]+/|[0-9A-Fa-f]{40,64}", spoken):
        failed.append("spoken_content_contains_private_or_hash_metadata")
    if "DRY RUN" in spoken.upper() or "synthetic dry-run" in spoken.lower():
        failed.append("synthetic_dry_run_script_reused")

    hashes = {
        name: _sha256(root / name)
        for name in required
        if name != INPUT_READBACK_FILENAME and (root / name).is_file()
    }
    computed = _validation_payload(root, failed, hashes)
    if require_input_readback:
        recorded = payloads.get(INPUT_READBACK_FILENAME, {})
        if recorded != computed:
            failed.append("input_validation_readback_recompute_mismatch")
            computed = _validation_payload(root, failed, hashes)
    return computed


def generate_verified_local_evidence_project(
    *,
    pilot_dir: str | Path,
    source_ymmp: str | Path,
    output_ymmp: str | Path | None = None,
) -> dict[str, Any]:
    """Generate the local internal-review project from an operator import base."""
    root = Path(pilot_dir).resolve()
    source = Path(source_ymmp).resolve()
    output = (
        Path(output_ymmp).resolve()
        if output_ymmp is not None
        else root / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    )
    if source == output:
        raise ValueError("SOURCE_PROJECT_MUST_DIFFER_FROM_OUTPUT_PROJECT")
    validation = validate_verified_local_evidence_input_pilot(pilot_dir=root)
    if validation["status"] != "passed":
        raise ValueError("PILOT_PREFLIGHT_FAILED:" + ",".join(validation["failed_checks"]))
    expected_rows = _load_csv_rows(root / DERIVED_CSV_FILENAME)
    source_project, source_voices = _validate_operator_import_base(source, expected_rows)
    source_digests = [_json_sha256(item) for item in source_voices]
    scenes = _derive_scene_specs(source_voices)

    project = copy.deepcopy(source_project)
    project.pop("Tools", None)
    project.pop("ToolStates", None)
    project.pop("LayoutXml", None)
    project.pop("CollapsedGroups", None)
    timeline = _first_timeline(project)
    items = _get_timeline_items(project)
    max_layer = max(
        [int(timeline.get("MaxLayer", 0) or 0)]
        + [int(item.get("Layer", 0) or 0) for item in items]
    )
    image_layer = max_layer + 1
    text_layer = max_layer + 2
    asset = (root / ASSET_RELATIVE_PATH).resolve()
    for scene in scenes:
        items.append(
            _make_image_item(scene, asset_path=str(asset), layer=image_layer)
        )
        items.append(_make_text_item(scene, layer=text_layer))
    timeline["MaxLayer"] = text_layer
    output.parent.mkdir(parents=True, exist_ok=True)
    project["FilePath"] = str(output)
    normalize_ymmp_openability(project)
    save_ymmp(project, output)

    readback = _readback_generated_project(
        project_path=output,
        expected_rows=expected_rows,
        asset_path=asset,
        source_voice_digests=source_digests,
        source_timeline_length=int(_first_timeline(source_project).get("Length", 0) or 0),
    )
    if readback["status"] != "structural_pass":
        raise ValueError("GENERATED_PROJECT_READBACK_FAILED:" + ",".join(readback["failed_checks"]))
    readback_path = output.parent / LOCAL_ACTUAL_READBACK_FILENAME
    receipt_path = output.parent / LOCAL_GENERATION_RECEIPT_FILENAME
    _write_json(readback_path, readback)
    receipt = {
        "schema_version": "verified_local_evidence_project_generation_receipt.actual.v1",
        "status": "passed",
        "operator_input_base": source.name,
        "operator_input_base_sha256": _sha256(source),
        "project": output.name,
        "project_sha256": _sha256(output),
        "actual_local_project_generated": True,
        "voice_items_preserved": True,
        "render_or_export_performed": False,
        "production_ymmp_written": False,
        "public_ready": False,
    }
    _write_json(receipt_path, receipt)
    return {
        "status": "local_internal_review_project_ready",
        "project_path": str(output),
        "readback_path": str(readback_path),
        "receipt_path": str(receipt_path),
        "readback": readback,
    }


def collect_verified_local_evidence_operator_result(
    *,
    pilot_dir: str | Path,
    project_path: str | Path | None = None,
    render_path: str | Path | None = None,
    output_path: str | Path | None = None,
    not_before_utc: str,
    operator_confirmed_clean: bool,
    yymm4_product_version: str,
    profile_observation_version: str,
    operator_output_setting_note: str = "",
    preserve_existing_success: bool = False,
) -> dict[str, Any]:
    """Collect local project and MP4 evidence after the manual batch."""
    root = Path(pilot_dir).resolve()
    project = (
        Path(project_path).resolve()
        if project_path is not None
        else root / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    )
    render = (
        Path(render_path).resolve()
        if render_path is not None
        else root / LOCAL_OUTPUT_DIRNAME / LOCAL_RENDER_FILENAME
    )
    output = (
        Path(output_path).resolve()
        if output_path is not None
        else root / LOCAL_OUTPUT_DIRNAME / LOCAL_OPERATOR_RESULT_FILENAME
    )
    expected_rows = _load_csv_rows(root / DERIVED_CSV_FILENAME)
    failed: list[str] = []
    try:
        threshold = datetime.fromisoformat(not_before_utc.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("OPERATOR_BATCH_NOT_BEFORE_UTC_INVALID") from exc
    if threshold.tzinfo is None:
        raise ValueError("OPERATOR_BATCH_NOT_BEFORE_UTC_MUST_HAVE_OFFSET")
    threshold = threshold.astimezone(timezone.utc)
    if operator_confirmed_clean is not True:
        failed.append("operator_clean_confirmation_missing")
    project_readback: dict[str, Any] = {}
    if not project.exists():
        failed.append("local_project_missing")
    else:
        if datetime.fromtimestamp(project.stat().st_mtime, timezone.utc) < threshold:
            failed.append("local_project_predates_batch")
        project_readback = _readback_generated_project(
            project_path=project,
            expected_rows=expected_rows,
            asset_path=(root / ASSET_RELATIVE_PATH).resolve(),
            source_voice_digests=None,
            source_timeline_length=None,
        )
        if project_readback["status"] != "structural_pass":
            failed.extend(f"project:{item}" for item in project_readback["failed_checks"])
    media_inspection: dict[str, Any] = {
        "status": "failed",
        "error_code": "render_missing",
        "failed_checks": ["render_missing"],
        "is_yymm4_project_json": False,
        "file_size_bytes": 0,
        "sha256": None,
        "top_level_boxes": [],
        "top_level_box_types": [],
        "ftyp": None,
        "mvhd": None,
        "checks": {},
    }
    if render.exists():
        from src.pipeline.media_validation import inspect_iso_bmff

        media_inspection = inspect_iso_bmff(render)
    render_size = int(media_inspection.get("file_size_bytes") or 0)
    media_error_code = str(media_inspection.get("error_code") or "")
    if not render.exists():
        failed.append("render_missing")
    elif media_inspection.get("is_yymm4_project_json") is True:
        failed.append("render_is_yymm4_project_json_not_mp4")
    elif render_size <= 32:
        failed.append("render_too_small")
    elif media_inspection.get("status") != "passed":
        failed.append(media_error_code or "render_iso_bmff_structure_invalid")
    elif datetime.fromtimestamp(render.stat().st_mtime, timezone.utc) < threshold:
        failed.append("render_predates_batch")
    result = {
        "schema_version": "verified_local_evidence_operator_result.v1",
        "status": "success" if not failed else "failure",
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "batch_not_before_utc": threshold.isoformat(),
        "operator_reported": {
            "manual_batch_completed_before_collection": operator_confirmed_clean,
            "no_unexpected_mapping_character_or_parse_error": operator_confirmed_clean,
            "yymm4_product_version": yymm4_product_version,
            "profile_observation_version": profile_observation_version,
            "output_setting_note": operator_output_setting_note or None,
            "output_setting_note_evidence_grade": (
                "observed" if operator_output_setting_note else "unknown"
            ),
            "profile_version_match": yymm4_product_version.startswith(
                profile_observation_version
            ),
        },
        "independently_verified": {
            "project_structural_pass": project_readback.get("status") == "structural_pass",
            "project_sha256": _sha256(project) if project.exists() else None,
            "render_exists": render.exists(),
            "render_size_bytes": render_size,
            "render_sha256": (
                str(media_inspection.get("sha256") or "").upper() or None
            )
            if render.exists()
            else None,
            "render_mp4_signature_present": "ftyp"
            in _list(media_inspection.get("top_level_box_types")),
            "render_iso_bmff_structure_pass": media_inspection.get("status")
            == "passed",
            "render_detection_error_code": media_error_code or None,
            "render_is_yymm4_project_json": media_inspection.get(
                "is_yymm4_project_json"
            )
            is True,
            "render_top_level_box_types": _list(
                media_inspection.get("top_level_box_types")
            ),
            "render_ftyp": media_inspection.get("ftyp"),
        },
        "files": {
            "project": project.name,
            "render": render.name,
            "operator_result": output.name,
        },
        "failed_checks": failed,
        "evidence_boundary": {
            "internal_review_only": True,
            "production_ymmp": False,
            "rights_or_public_approval": False,
            "upload_or_publication": False,
        },
    }
    if preserve_existing_success and output.exists():
        existing_bytes = output.read_bytes()
        existing = _load_json(output)
        existing_verified = _dict(existing.get("independently_verified"))
        evidence_matches = (
            existing.get("status") == "success"
            and _list(existing.get("failed_checks")) == []
            and not failed
            and existing_verified.get("project_sha256")
            == result["independently_verified"]["project_sha256"]
            and existing_verified.get("render_sha256")
            == result["independently_verified"]["render_sha256"]
            and existing_verified.get("render_size_bytes") == render_size
        )
        if not evidence_matches:
            raise ValueError("EXISTING_OPERATOR_RESULT_EVIDENCE_MISMATCH")
        if output.read_bytes() != existing_bytes:
            raise ValueError("EXISTING_OPERATOR_RESULT_CHANGED_DURING_COLLECTION")
        return {
            **existing,
            "operator_result_path": str(output),
            "operator_result_preserved_byte_for_byte": True,
            "current_iso_bmff_structure_pass": media_inspection.get("status")
            == "passed",
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output, result)
    return {**result, "operator_result_path": str(output)}


def _source_paths(package: Path, repo_root: Path) -> dict[str, Path]:
    return {
        "csv_gate_observation_receipt": package / CSV_RECEIPT_RELATIVE,
        "diagnostic_project_manifest": package / DIAGNOSTIC_MANIFEST_RELATIVE,
        "diagnostic_project_readback": package / DIAGNOSTIC_READBACK_RELATIVE,
        "diagnostic_project_receipt": package / DIAGNOSTIC_RECEIPT_RELATIVE,
        "runtime_state": repo_root / RUNTIME_STATE_RELATIVE,
        "yymm4_character_profile": package / PROFILE_RELATIVE,
    }


def _load_and_validate_sources(paths: dict[str, Path]) -> dict[str, Any]:
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("AUTHORIZED_SOURCE_MISSING:" + ",".join(missing))
    payloads: dict[str, Any] = {
        key: (
            path.read_text(encoding="utf-8")
            if key == "runtime_state"
            else _load_json(path)
        )
        for key, path in paths.items()
    }
    expected = {
        "csv_gate_observation_receipt": (
            "ymm4_gui_observation_receipt.v2",
            "passed",
        ),
        "diagnostic_project_manifest": (
            "ymm4_diagnostic_project_manifest.v1",
            "generated_structural_pass",
        ),
        "diagnostic_project_readback": (
            "ymm4_diagnostic_project_readback.v1",
            "structural_pass",
        ),
        "diagnostic_project_receipt": (
            "ymm4_diagnostic_project_gui_receipt.v1",
            "passed",
        ),
        "yymm4_character_profile": (
            "ymm4_character_alias_profile.v1",
            "observed_environment_specific",
        ),
    }
    for source_id, (schema, status) in expected.items():
        payload = _dict(payloads.get(source_id))
        if payload.get("schema_version") != schema:
            raise ValueError(f"SOURCE_SCHEMA_MISMATCH:{source_id}")
        if payload.get("status") != status:
            raise ValueError(f"SOURCE_STATUS_MISMATCH:{source_id}")

    receipt = _dict(payloads["csv_gate_observation_receipt"])
    if receipt.get("result") != "passed" or receipt.get("actual_ymm4_imported") is not True:
        raise ValueError("CSV_GATE_RECEIPT_NOT_PASSED_IMPORT")
    diagnostic_readback = _dict(payloads["diagnostic_project_readback"])
    if diagnostic_readback.get("failed_checks") != [] or any(
        value is not True
        for value in _dict(diagnostic_readback.get("checks")).values()
    ):
        raise ValueError("DIAGNOSTIC_READBACK_CHECKS_NOT_ALL_TRUE")
    diagnostic_receipt = _dict(payloads["diagnostic_project_receipt"])
    if diagnostic_receipt.get("result") != "passed":
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_NOT_PASSED")
    if _dict(diagnostic_receipt.get("safety")).get("diagnostic_only") is not True:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_BOUNDARY_MISSING")

    runtime_text = str(payloads["runtime_state"])
    if not re.search(r"^Project-State-ID:\s*\S+", runtime_text, re.MULTILINE):
        raise ValueError("RUNTIME_STATE_ID_MISSING")
    if not re.search(r"^Product-State:\s*\S+", runtime_text, re.MULTILINE):
        raise ValueError("RUNTIME_PRODUCT_STATE_MISSING")

    diagnostic_manifest = _dict(payloads["diagnostic_project_manifest"])
    manifest_records = {
        str(_dict(record).get("record_id")): _dict(record)
        for record in _list(diagnostic_manifest.get("source_records"))
    }
    csv_record = manifest_records.get("csv_gate_receipt_v2", {})
    if str(csv_record.get("sha256") or "").upper() != _sha256(
        paths["csv_gate_observation_receipt"]
    ):
        raise ValueError("DIAGNOSTIC_MANIFEST_CSV_RECEIPT_HASH_MISMATCH")
    receipt_hashes = _dict(diagnostic_receipt.get("evidence_hashes"))
    if receipt_hashes.get("manifest_sha256") != _sha256(
        paths["diagnostic_project_manifest"]
    ):
        raise ValueError("DIAGNOSTIC_RECEIPT_MANIFEST_HASH_MISMATCH")
    if receipt_hashes.get("readback_sha256") != _sha256(
        paths["diagnostic_project_readback"]
    ):
        raise ValueError("DIAGNOSTIC_RECEIPT_READBACK_HASH_MISMATCH")
    return payloads


def _build_source_manifest(
    *,
    artifact_id: str,
    source_paths: dict[str, Path],
    source_payloads: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    roles = {
        "csv_gate_observation_receipt": "actual bounded CSV import observation",
        "diagnostic_project_manifest": "diagnostic project provenance and evidence boundary",
        "diagnostic_project_readback": "machine structural readback for VoiceItem and placeholder counts",
        "diagnostic_project_receipt": "actual GUI reopen observation and non-final safety boundary",
        "runtime_state": "current project-state context; not a spoken factual source",
        "yymm4_character_profile": "explicit environment-specific canonical-to-YMM4 character mapping",
    }
    schemas = {
        "runtime_state": "nlmytgen_runtime_state_capsule",
        **{
            source_id: _dict(payload).get("schema_version")
            for source_id, payload in source_payloads.items()
            if source_id != "runtime_state"
        },
    }
    statuses = {
        "runtime_state": _runtime_state_id(str(source_payloads["runtime_state"])),
        **{
            source_id: _dict(payload).get("status")
            for source_id, payload in source_payloads.items()
            if source_id != "runtime_state"
        },
    }
    return {
        "schema_version": "verified_local_evidence_source_bundle_manifest.v1",
        "artifact_id": f"{artifact_id}_source_bundle",
        "episode_id": EPISODE_ID,
        "status": "validated_local_internal_evidence",
        "sources": [
            {
                "source_id": source_id,
                "repo_relative_path": _repo_relative(path, repo_root),
                "sha256": _sha256(path),
                "schema": schemas[source_id],
                "status": statuses[source_id],
                "role": roles[source_id],
            }
            for source_id, path in source_paths.items()
        ],
        "source_boundary": {
            "source_kind": "tracked NLMYTGen local observation evidence",
            "internal_pilot_only": True,
            "external_editorial_source": False,
            "external_fetch_or_download": False,
            "external_asset_used": False,
            "rights_or_legal_approval": False,
            "public_ready": False,
            "production_ready": False,
        },
    }


def _build_claim_ledger(
    source_paths: dict[str, Path], repo_root: Path
) -> dict[str, Any]:
    source_payloads = _load_and_validate_sources(source_paths)
    claims: list[dict[str, Any]] = []
    for cue in CUES:
        evidence_rows = []
        for source_id, pointer, expected in cue["evidence"]:
            actual = _json_pointer(source_payloads[source_id], pointer)
            if actual != expected:
                raise ValueError(
                    f"CLAIM_EVIDENCE_MISMATCH:{cue['cue_id']}:{source_id}:{pointer}"
                )
            evidence_rows.append(
                {
                    "source_file": _repo_relative(
                        source_paths[source_id], repo_root
                    ),
                    "json_pointer_or_field": pointer,
                    "expected_value": expected,
                    "matched": True,
                }
            )
        claims.append(
            {
                "cue_id": cue["cue_id"],
                "claim_summary": cue["claim_summary"],
                "source_file": _repo_relative(
                    source_paths[cue["source_id"]], repo_root
                ),
                "json_pointer_or_field": cue["json_pointer"],
                "paraphrase_status": "paraphrased",
                "unsupported_claim": False,
                "evidence": evidence_rows,
            }
        )
    return {
        "schema_version": "verified_local_evidence_source_claim_ledger.v1",
        "artifact_id": f"{ARTIFACT_ID}_claim_ledger",
        "status": "passed",
        "claim_count": len(claims),
        "unsupported_claim_count": 0,
        "coverage": "every_cue_has_machine_matched_authorized_source_evidence",
        "claims": claims,
    }


def _build_script_payload() -> dict[str, Any]:
    cues = [
        {
            "sequence": index,
            "cue_id": cue["cue_id"],
            "scene_id": cue["scene_id"],
            "speaker": cue["speaker"],
            "text": cue["text"],
        }
        for index, cue in enumerate(CUES, start=1)
    ]
    return {
        "schema_version": "verified_local_evidence_canonical_script.v1",
        "artifact_id": f"{ARTIFACT_ID}_script",
        "episode_id": EPISODE_ID,
        "language": "ja",
        "content_mode": "internal_verified_local_evidence_pilot",
        "tone": "fact_first_concise_non_exaggerated",
        "cue_count": 9,
        "scene_allocation": {"S1": 2, "S2": 2, "S3": 5},
        "speaker_counts": EXPECTED_CANONICAL_COUNTS,
        "editorial_adoption": False,
        "public_ready": False,
        "production_ready": False,
        "cues": cues,
    }


def _render_script_text(script: dict[str, Any]) -> str:
    rows: list[str] = []
    current_scene = ""
    for raw in _list(script.get("cues")):
        cue = _dict(raw)
        scene = str(cue.get("scene_id") or "")
        if scene != current_scene:
            if rows:
                rows.append("")
            rows.append(f"[{scene}]")
            current_scene = scene
        rows.append(f"{cue.get('speaker')}: {cue.get('text')}")
    return "\n".join(rows) + "\n"


def _project_contracts(
    *,
    source_payloads: dict[str, Any],
    derived_rows: list[tuple[str, str]],
    output: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    diagnostic_manifest = _dict(source_payloads["diagnostic_project_manifest"])
    diagnostic_readback = _dict(source_payloads["diagnostic_project_readback"])
    base_record = next(
        (
            _dict(record)
            for record in _list(diagnostic_manifest.get("source_records"))
            if _dict(record).get("record_id") == "local_import_base"
        ),
        {},
    )
    old_rows = [
        (
            str(_dict(row).get("character") or ""),
            str(_dict(row).get("text") or ""),
        )
        for row in _list(diagnostic_readback.get("VoiceItems"))
    ]
    prior_base = {
        "evidence_name": base_record.get("repo_relative_or_local_name"),
        "evidence_sha256": base_record.get("sha256"),
        "previously_observed_structure": "one_timeline_nine_voiceitems_only",
        "reusable_for_current_script": old_rows == derived_rows,
        "assessment": (
            "reusable_exact_rows"
            if old_rows == derived_rows
            else "rejected_old_dry_run_voice_text_mismatch"
        ),
        "safety_reason": (
            "VoiceItem Serif and voice-cache fields must not be rewritten headlessly"
        ),
    }
    targets = {
        "operator_import_base": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_IMPORT_BASE_FILENAME}",
        "internal_review_project": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_PROJECT_FILENAME}",
        "internal_review_render": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_RENDER_FILENAME}",
        "actual_project_readback": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_ACTUAL_READBACK_FILENAME}",
        "actual_generation_receipt": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_GENERATION_RECEIPT_FILENAME}",
        "operator_result": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_OPERATOR_RESULT_FILENAME}",
    }
    manifest = {
        "schema_version": "verified_local_evidence_internal_project_manifest.v1",
        "artifact_id": f"{ARTIFACT_ID}_internal_project",
        "episode_id": EPISODE_ID,
        "status": "ready_for_operator_generation",
        "contract_stage": "pre_operator_contract_snapshot",
        "current_authority_when_render_exists": "render_receipt.json",
        "internal_review_only": True,
        "generator": {
            "module": "src.pipeline.verified_local_evidence_input_pilot",
            "command": (
                "python -m src.cli.main generate-verified-local-evidence-project "
                "--pilot production_pilots/yukkuri_newsroom_content_spine_002/"
                "verified_local_evidence_input_pilot --source-ymmp <operator-import-base.local.ymmp>"
            ),
            "voiceitem_policy": "preserve_each_imported_voiceitem_object_unchanged",
            "resolution_policy": "preserve_operator_import_base",
            "layout_state_policy": "strip_base_LayoutXml_and_CollapsedGroups_to_avoid_carrying_gui_dock_state",
        },
        "targets": targets,
        "asset": {
            "repo_relative_path": ASSET_RELATIVE_PATH.as_posix(),
            "sha256": _sha256(output / ASSET_RELATIVE_PATH),
            "external_source": False,
            "generation": "deterministic_python_standard_library_rgba_png",
        },
        "expected_counts": {
            "VoiceItem": 9,
            "ImageItem": 3,
            "independent_TextItem": 3,
            "characters": EXPECTED_CHARACTER_COUNTS,
        },
        "scenes": [
            {
                "scene_id": scene_id,
                "cue_ids": [
                    f"cue_{row:03d}" for row in range(start + 1, end + 1)
                ],
                "label": LABEL_TEMPLATE.format(scene_id=scene_id),
                "ImageItem": 1,
                "independent_TextItem": 1,
            }
            for scene_id, start, end in SCENE_ROWS
        ],
        "prior_local_base_assessment": prior_base,
        "evidence_boundary": {
            "tracked_manifest_is_not_actual_project_parse": True,
            "operator_import_base_required": True,
            "actual_local_project_generated": False,
            "render_or_export_performed": False,
            "production_ymmp_written": False,
            "public_or_rights_approved": False,
        },
    }
    readback = {
        "schema_version": "verified_local_evidence_static_project_readback.v1",
        "artifact_id": f"{ARTIFACT_ID}_static_project_readback",
        "status": "contract_pass",
        "contract_stage": "pre_operator_contract_snapshot",
        "current_authority_when_render_exists": "render_receipt.json",
        "validation_kind": "headless_static_contract_not_actual_project_parse",
        "actual_project_present": False,
        "actual_project_parse_performed": False,
        "expected_targets": targets,
        "expected_item_counts": manifest["expected_counts"],
        "expected_scene_labels": [
            LABEL_TEMPLATE.format(scene_id=scene_id)
            for scene_id, _, _ in SCENE_ROWS
        ],
        "checks": {
            "source_bundle_validated": True,
            "nine_cue_derived_csv_ready": True,
            "strict_character_profile_coverage": True,
            "prior_base_mismatch_classified": prior_base["reusable_for_current_script"] is False,
            "operator_import_base_is_explicit_input": True,
            "generator_preserves_voiceitems": True,
            "generator_strips_base_gui_layout_state": True,
            "three_scene_placeholder_contract": True,
            "internal_non_final_labels_explicit": True,
            "local_project_and_render_targets_ignored": True,
            "no_external_asset": True,
        },
        "actual_render_validated": False,
        "next_gate": "manual_yymm4_render_batch",
    }
    receipt = {
        "schema_version": "verified_local_evidence_project_generation_receipt.v1",
        "artifact_id": f"{ARTIFACT_ID}_project_generation",
        "status": "operator_input_required",
        "contract_stage": "pre_operator_contract_snapshot",
        "superseded_by_render_receipt_when_present": "render_receipt.json",
        "generator_implemented": True,
        "static_contract_passed": True,
        "actual_local_project_generated": False,
        "reason": "new derived CSV must be imported by YMM4 so voice cache fields remain coherent",
        "operator_import_base_target": targets["operator_import_base"],
        "local_project_target": targets["internal_review_project"],
        "render_target": targets["internal_review_render"],
        "worker_yymm4_launch_performed": False,
        "render_or_export_performed": False,
        "production_ymmp_written": False,
    }
    return manifest, readback, receipt


def _write_operator_batch(
    *, output: Path, source_payloads: dict[str, Any]
) -> None:
    operator = output / OPERATOR_DIRNAME
    actions = [
        "Run run_yymm4_operator_batch.ps1 once from a clean terminal.",
        "In YMM4 create/confirm a new empty project and empty timeline, then use Tools > Script Import, select the derived CSV, confirm no mapping/error or character mismatch, add it to the timeline, and use Project Save As to save the exact .local.ymmp import-base target (never the .mp4 target).",
        "Return to the terminal and enter READY so the script generates the local internal-review project.",
        "Open that generated project, confirm it opens without error and shows the three internal/non-final labels, then use Video Output/Export (not Project Save As) exactly once to the specified .mp4 target and close safely.",
        "Return to the terminal and enter COLLECT so the script writes operator_result.json.",
    ]
    stop_conditions = [
        "unexpected unsaved project",
        "project other than the intended pilot",
        "YMM4 update requirement",
        "mapping dialog or character mismatch",
        "parse or open error",
        "render asks for production, public, or upload action",
        "output path differs unexpectedly",
        "a Project Save As dialog is being used for the .mp4 video-output target",
        "an exact pilot output target already exists from an earlier run",
        "unrelated user work is visible",
    ]
    prohibited = [
        "upload",
        "publication",
        "production .ymmp",
        "external media download",
        "source replacement",
        "rights approval",
        "final thumbnail approval",
        "default-branch mutation",
        "deleting unrelated user files",
    ]
    manifest = {
        "schema_version": "verified_local_evidence_operator_batch_manifest.v1",
        "artifact_id": f"{ARTIFACT_ID}_operator_batch",
        "status": "ready",
        "manual_action_count": 5,
        "manual_actions": actions,
        "stop_conditions": stop_conditions,
        "prohibited_actions": prohibited,
        "return_items": [
            "success_or_failure",
            "operator_result_json_path",
            "error_text_only_when_failed",
        ],
        "gui_operator": "user",
        "codex_gui_automation": False,
        "freshness_contract": {
            "preexisting_exact_targets": "stop_without_deleting",
            "project_and_render_must_not_predate_batch_start": True,
            "operator_clean_confirmation_required": True,
        },
        "recovery_contract": {
            "collect_only_supported": True,
            "collect_only_launches_yymm4": False,
            "collect_only_regenerates_project_or_render": False,
            "existing_success_result_is_preserved_byte_for_byte": True,
            "batch_start_and_version_marker": (
                f"../{LOCAL_OUTPUT_DIRNAME}/{LOCAL_BATCH_MARKER_FILENAME}"
            ),
        },
        "json_transport": "python_written_utf8_file_read_by_powershell_explicit_utf8",
        "targets": {
            "derived_csv": f"../{DERIVED_CSV_FILENAME}",
            "import_base": f"../{LOCAL_OUTPUT_DIRNAME}/{LOCAL_IMPORT_BASE_FILENAME}",
            "project": f"../{LOCAL_OUTPUT_DIRNAME}/{LOCAL_PROJECT_FILENAME}",
            "render": f"../{LOCAL_OUTPUT_DIRNAME}/{LOCAL_RENDER_FILENAME}",
            "result": f"../{LOCAL_OUTPUT_DIRNAME}/{LOCAL_OPERATOR_RESULT_FILENAME}",
        },
    }
    _write_json(operator / OPERATOR_MANIFEST_FILENAME, manifest)
    _write_json(
        operator / EXPECTED_OUTPUT_FILENAME,
        {
            "schema_version": "verified_local_evidence_expected_output_contract.v1",
            "status": "ready",
            "project_target": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_PROJECT_FILENAME}",
            "render_target": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_RENDER_FILENAME}",
            "operator_result_target": f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_OPERATOR_RESULT_FILENAME}",
            "project_expectations": {
                "VoiceItem": 9,
                "ImageItem": 3,
                "independent_TextItem": 3,
                "characters": EXPECTED_CHARACTER_COUNTS,
                "scene_labels_contain": list(BOUNDARY_TOKENS),
                "resolution_policy": "preserve_operator_import_base",
            },
            "render_expectations": {
                "container": "mp4",
                "render_count": 1,
                "minimum_machine_check": [
                    "exists",
                    "nonzero_size",
                    "sha256",
                    "bounded_top_level_iso_bmff_box_walk",
                    "ftyp_moov_mdat_structure",
                    "specific_yymm4_project_json_misname_detection",
                    "modified_after_batch_start",
                ],
            },
            "environment_recording": {
                "actual_yymm4_product_version": "collected_locally",
                "profile_observation_version": "4.53.0.9",
                "version_difference_is_a_manual_mapping_gate": True,
            },
            "not_claimed": [
                "production acceptance",
                "public readiness",
                "rights approval",
                "upload or publication",
            ],
        },
    )
    _write_json(
        operator / OPERATOR_PREFLIGHT_FILENAME,
        {
            "schema_version": "verified_local_evidence_operator_preflight.v1",
            "status": "passed",
            "validation_mode": "tracked_headless_contract_preflight",
            "source_bundle_valid": True,
            "claim_coverage": "9_of_9",
            "unsupported_claim_count": 0,
            "csv_invariants_passed": True,
            "project_static_contract_passed": True,
            "operator_manual_action_count": 5,
            "operator_return_item_count": 3,
            "fresh_output_binding_required": True,
            "collect_only_recovery_supported": True,
            "python_powershell_json_transport": "explicit_utf8_file",
            "yymm4_launch_attempted": False,
            "computer_use_invoked": False,
            "runtime_command": (
                "powershell -NoProfile -ExecutionPolicy Bypass -File "
                ".\\run_yymm4_operator_batch.ps1 -PreflightOnly"
            ),
            "note": "Runtime preflight additionally checks local Python and YMM4 executable availability without launching YMM4.",
        },
    )
    _write_text(operator / OPERATOR_README_FILENAME, _operator_readme(actions, stop_conditions, prohibited))
    _write_text(operator / OPERATOR_RETURN_FILENAME, _operator_return_template())
    _write_text(operator / OPERATOR_SCRIPT_FILENAME, _operator_script())
    _write_text(operator / COLLECTOR_SCRIPT_FILENAME, _collector_script())


def _operator_readme(
    actions: list[str], stop_conditions: list[str], prohibited: list[str]
) -> str:
    action_lines = "\n".join(
        f"{index}. {text}" for index, text in enumerate(actions, start=1)
    )
    stop_lines = "\n".join(f"- {text}" for text in stop_conditions)
    prohibited_lines = "\n".join(f"- {text}" for text in prohibited)
    return f"""# Episode 002 one-shot YMM4 Operator Batch

このバッチは、headless準備済みの内部確認パイロットを一度だけYMM4で取り込み・書き出しする手動gateです。

- PCの操作主体はユーザーです。
- CodexはGUI、mouse、keyboard、window focusを操作しません。
- 生成物は `INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT` であり、本番・公開・権利承認ではありません。
- まずYMM4内の未保存作業を解消し、このpilot以外が表示されていない状態で始めてください。

## 実行

このディレクトリで次を一度だけ実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\{OPERATOR_SCRIPT_FILENAME}
```

起動前の確認だけなら、YMM4を起動しない次のコマンドを使えます。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\{OPERATOR_SCRIPT_FILENAME} -PreflightOnly
```

render後にterminalやcollectorだけが中断した場合は、YMM4を起動せずproject／renderを再生成しない次の回収専用routeを使います。既存の成功済み `operator_result.json` がある場合はbyte-for-byteで保持します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\{OPERATOR_SCRIPT_FILENAME} -CollectOnly -OperatorConfirmedClean
```

## 手動アクション（5件）

{action_lines}

YMM4では最初に新規の空project／空timelineであることを確認し、既存itemがあれば停止します。その後 `ツール` → `台本読み込み` から `derived_yymm4_import.csv` を選び、対応表やerrorが出ず、霊夢／魔理沙の割り当てが正しい場合だけ `タイムラインに追加` します。手で件数やhashを計算する必要はありません。

保存操作は次の2種類を混同しないでください。

- **Project Save As -> `.local.ymmp`**: import base projectを保存する操作です。`.mp4` pathを入力してはいけません。
- **Video Output/Export -> `.mp4`**: 動画を書き出す操作です。Project Save Asを使ってはいけません。project JSONが`.mp4`名で保存されるためです。

## Stop conditions

{stop_lines}

## Prohibited actions

{prohibited_lines}

## 返却

`operator_return_template.md`どおり最大3項目だけ返してください。failure screenshotは任意です。
"""


def _operator_return_template() -> str:
    return """# Operator Return (maximum 3 items)

1. result: success | failure
2. operator_result.json: <path>
3. error: <failure only; omit on success>
"""


def _operator_script() -> str:
    return r'''[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [switch]$CollectOnly,
    [switch]$OperatorConfirmedClean,
    [string]$PythonExe = "",
    [string]$Ymm4Exe = "",
    [string]$NotBeforeUtc = "",
    [string]$Ymm4ProductVersion = "",
    [string]$OperatorOutputSettingNote = ""
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if ($PreflightOnly -and $CollectOnly) {
    throw "Choose either -PreflightOnly or -CollectOnly, not both."
}

function Resolve-PythonExe {
    param([string]$Requested, [string]$RepoRoot)
    if ($Requested) {
        if (-not (Test-Path -LiteralPath $Requested -PathType Leaf)) {
            throw "Requested Python executable was not found."
        }
        return (Resolve-Path -LiteralPath $Requested).Path
    }
    $RepoPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $RepoPython -PathType Leaf) {
        return (Resolve-Path -LiteralPath $RepoPython).Path
    }
    throw "Python was not found. Pass -PythonExe or create the repo .venv."
}

function Resolve-Ymm4Exe {
    param([string]$Requested)
    $Candidates = @()
    if ($Requested) { $Candidates += $Requested }
    $Candidates += "D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
    $Candidates += "D:\MovieCreationWorkspace\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
    foreach ($Candidate in $Candidates) {
        if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    throw "YMM4 executable was not found. Pass -Ymm4Exe explicitly."
}

function Read-Utf8Json {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Expected UTF-8 JSON file was not found: $Path"
    }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

$PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
$Python = Resolve-PythonExe -Requested $PythonExe -RepoRoot $RepoRoot
$DerivedCsv = Join-Path $PilotDir "derived_yymm4_import.csv"
$LocalOutput = Join-Path $PilotDir "local_outputs"
$ImportBase = Join-Path $LocalOutput "episode_002_verified_local_evidence_import_base.local.ymmp"
$Project = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.local.ymmp"
$Render = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.mp4"
$Result = Join-Path $LocalOutput "operator_result.json"
$BatchMarker = Join-Path $LocalOutput "operator_batch_started.local.txt"

$ValidationResultFile = Join-Path ([IO.Path]::GetTempPath()) ("nlmytgen-pilot-validation-" + [guid]::NewGuid().ToString("N") + ".json")
try {
    Push-Location -LiteralPath $RepoRoot
    try {
        & $Python -m src.cli.main validate-verified-local-evidence-pilot --pilot $PilotDir --format text --result-json $ValidationResultFile | Out-Null
        $ValidationExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Validation = Read-Utf8Json -Path $ValidationResultFile
    if ($ValidationExit -ne 0 -or $Validation.status -ne "passed") {
        throw ("Pilot validation failed: " + (($Validation.failed_checks -join ", ")))
    }
}
finally {
    Remove-Item -LiteralPath $ValidationResultFile -Force -ErrorAction SilentlyContinue
}

if ($CollectOnly) {
    $PreserveExistingSuccess = $false
    if (Test-Path -LiteralPath $Result -PathType Leaf) {
        $ExistingResult = Read-Utf8Json -Path $Result
        if ($ExistingResult.status -eq "success" -and @($ExistingResult.failed_checks).Count -eq 0) {
            $PreserveExistingSuccess = $true
            if (-not $NotBeforeUtc) { $NotBeforeUtc = [string]$ExistingResult.batch_not_before_utc }
            if (-not $Ymm4ProductVersion) { $Ymm4ProductVersion = [string]$ExistingResult.operator_reported.yymm4_product_version }
            if (-not $OperatorOutputSettingNote -and $ExistingResult.operator_reported.output_setting_note) {
                $OperatorOutputSettingNote = [string]$ExistingResult.operator_reported.output_setting_note
            }
            if ($ExistingResult.operator_reported.manual_batch_completed_before_collection -eq $true) {
                $OperatorConfirmedClean = $true
            }
        }
    }
    if ((-not $NotBeforeUtc -or -not $Ymm4ProductVersion) -and (Test-Path -LiteralPath $BatchMarker -PathType Leaf)) {
        $MarkerValues = @{}
        foreach ($Line in (Get-Content -LiteralPath $BatchMarker -Encoding UTF8)) {
            $Parts = $Line -split "=", 2
            if ($Parts.Count -eq 2) { $MarkerValues[$Parts[0]] = $Parts[1] }
        }
        if (-not $NotBeforeUtc) { $NotBeforeUtc = [string]$MarkerValues["batch_not_before_utc"] }
        if (-not $Ymm4ProductVersion) { $Ymm4ProductVersion = [string]$MarkerValues["yymm4_product_version"] }
    }
    if (-not $NotBeforeUtc) {
        throw "Collect-only needs the ignored batch marker, an existing operator_result.json, or explicit -NotBeforeUtc."
    }
    if (-not $Ymm4ProductVersion) {
        throw "Collect-only needs the ignored batch marker, an existing operator_result.json, or explicit -Ymm4ProductVersion."
    }
    if (-not $OperatorConfirmedClean) {
        throw "Collect-only requires -OperatorConfirmedClean when no successful existing result records that confirmation."
    }
    $CollectArgs = @{
        PythonExe = $Python
        PilotDir = $PilotDir
        ProjectPath = $Project
        RenderPath = $Render
        OutputPath = $Result
        NotBeforeUtc = $NotBeforeUtc
        Ymm4ProductVersion = $Ymm4ProductVersion
        ProfileObservationVersion = "4.53.0.9"
        OperatorConfirmedClean = $true
        OperatorOutputSettingNote = $OperatorOutputSettingNote
        PreserveExistingSuccess = $PreserveExistingSuccess
    }
    & (Join-Path $PSScriptRoot "collect_operator_result.ps1") @CollectArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    return
}

$Ymm4 = Resolve-Ymm4Exe -Requested $Ymm4Exe
$Version = (Get-Item -LiteralPath $Ymm4).VersionInfo.ProductVersion
$ProfileVersionMatch = $Version -like "4.53.0.9*"
$Preflight = [ordered]@{
    status = "passed"
    pilot_validation = "passed"
    python_available = $true
    yymm4_executable_available = $true
    yymm4_product_version = $Version
    profile_observation_version = "4.53.0.9"
    profile_version_match = $ProfileVersionMatch
    version_difference_is_manual_mapping_gate = (-not $ProfileVersionMatch)
    yymm4_launch_attempted = $false
    collect_only_supported = $true
    preflight_only = [bool]$PreflightOnly
}

if ($PreflightOnly) {
    $Preflight | ConvertTo-Json -Depth 5
    return
}

if (Get-Process -Name "YukkuriMovieMaker" -ErrorAction SilentlyContinue) {
    throw "YMM4 is already running. Stop and resolve/save unrelated work before this batch; this script will not close it."
}

$ExactTargets = @(
    $ImportBase,
    $Project,
    $Render,
    $Result,
    (Join-Path $LocalOutput "static_project_readback.actual.json"),
    (Join-Path $LocalOutput "project_generation_receipt.actual.json"),
    $BatchMarker
)
$ExistingTargets = @($ExactTargets | Where-Object { Test-Path -LiteralPath $_ })
if ($ExistingTargets.Count -gt 0) {
    throw ("Exact pilot output already exists. Stop and move/archive it manually; this batch will not delete or reuse it: " + ($ExistingTargets -join ", "))
}
$BatchStartedUtc = [DateTime]::UtcNow.ToString("o")
New-Item -ItemType Directory -Path $LocalOutput -Force | Out-Null
@(
    "batch_not_before_utc=$BatchStartedUtc",
    "yymm4_product_version=$Version",
    "profile_observation_version=4.53.0.9"
) | Set-Content -LiteralPath $BatchMarker -Encoding UTF8

Write-Host "PC CONTROL: USER. Codex does not operate the GUI."
Write-Host "This is INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT only."
Write-Host "STOP on unsaved/unrelated work, update prompts, mapping dialogs, character mismatch, parse errors, or any production/public/upload request."
Write-Host "DO NOT upload, publish, approve rights, create a production project, replace sources, or delete unrelated files."
if (-not $ProfileVersionMatch) {
    Write-Warning "Installed YMM4 $Version differs from profile observation 4.53.0.9. This is a manual mapping gate: stop on any mapping dialog, character mismatch, update requirement, or parse error."
}
Write-Host ""
Write-Host "Open/import CSV: $DerivedCsv"
Write-Host "PROJECT SAVE AS TARGET (.local.ymmp): $ImportBase"
Write-Host "Use Project Save As only for this .local.ymmp. NEVER enter the .mp4 path in Project Save As."
Write-Host "First create/confirm a NEW EMPTY project and EMPTY timeline. STOP if any existing item/project is present."
Write-Host "YMM4 click path: Tools > Script Import > select CSV > verify no mapping/error > Add to Timeline > Save As."
Start-Process -FilePath $Ymm4 | Out-Null
$Ready = Read-Host "After the exact import base is safely saved, type READY"
if ($Ready -ne "READY") {
    throw "Batch stopped before project generation. Expected READY."
}
if (-not (Test-Path -LiteralPath $ImportBase -PathType Leaf)) {
    throw "Exact import-base file was not found."
}

$GenerationResultFile = Join-Path ([IO.Path]::GetTempPath()) ("nlmytgen-project-generation-" + [guid]::NewGuid().ToString("N") + ".json")
try {
    Push-Location -LiteralPath $RepoRoot
    try {
        & $Python -m src.cli.main generate-verified-local-evidence-project --pilot $PilotDir --source-ymmp $ImportBase --output-ymmp $Project --format text --result-json $GenerationResultFile | Out-Null
        $GenerationExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Generation = Read-Utf8Json -Path $GenerationResultFile
    if ($GenerationExit -ne 0 -or $Generation.status -ne "local_internal_review_project_ready") {
        throw "Headless project generation failed."
    }
}
finally {
    Remove-Item -LiteralPath $GenerationResultFile -Force -ErrorAction SilentlyContinue
}
Write-Host ""
Write-Host "Open generated project: $Project"
Write-Host "Confirm no parse/error dialog and the three INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT labels."
Write-Host "VIDEO OUTPUT/EXPORT TARGET (.mp4): $Render"
Write-Host "Use Video Output/Export, NOT Project Save As. If a project-save dialog is targeting .mp4, STOP."
Write-Host "Output exactly once. Record any manual format change (for example, the operator-observed MPEG selection) as an observation, not a machine-verified codec claim."
Write-Host "Close safely after render. Do not upload or publish."
$Collect = Read-Host "After render and safe close, type COLLECT"
if ($Collect -ne "COLLECT") {
    throw "Batch stopped before result collection. Expected COLLECT."
}

& (Join-Path $PSScriptRoot "collect_operator_result.ps1") -PythonExe $Python -PilotDir $PilotDir -ProjectPath $Project -RenderPath $Render -OutputPath $Result -NotBeforeUtc $BatchStartedUtc -Ymm4ProductVersion $Version -ProfileObservationVersion "4.53.0.9" -OperatorConfirmedClean -OperatorOutputSettingNote $OperatorOutputSettingNote
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
'''


def _collector_script() -> str:
    return r'''[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$PilotDir = "",
    [string]$ProjectPath = "",
    [string]$RenderPath = "",
    [string]$OutputPath = "",
    [switch]$OperatorConfirmedClean,
    [switch]$PreserveExistingSuccess,
    [string]$OperatorOutputSettingNote = "",
    [Parameter(Mandatory=$true)]
    [string]$NotBeforeUtc,
    [Parameter(Mandatory=$true)]
    [string]$Ymm4ProductVersion,
    [Parameter(Mandatory=$true)]
    [string]$ProfileObservationVersion
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
if (-not $PilotDir) {
    $PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
if (-not $PythonExe) {
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python executable was not found."
}
if (-not $ProjectPath) {
    $ProjectPath = Join-Path $PilotDir "local_outputs\episode_002_verified_local_evidence_internal_review.local.ymmp"
}
if (-not $RenderPath) {
    $RenderPath = Join-Path $PilotDir "local_outputs\episode_002_verified_local_evidence_internal_review.mp4"
}
if (-not $OutputPath) {
    $OutputPath = Join-Path $PilotDir "local_outputs\operator_result.json"
}

$Arguments = @(
    "-m", "src.cli.main", "collect-verified-local-evidence-operator-result",
    "--pilot", $PilotDir,
    "--project", $ProjectPath,
    "--render", $RenderPath,
    "--output", $OutputPath,
    "--not-before-utc", $NotBeforeUtc,
    "--yymm4-product-version", $Ymm4ProductVersion,
    "--profile-observation-version", $ProfileObservationVersion,
    "--format", "text"
)
if ($OperatorConfirmedClean) { $Arguments += "--operator-confirmed-clean" }
if ($PreserveExistingSuccess) { $Arguments += "--preserve-existing-success" }
if ($OperatorOutputSettingNote) {
    $Arguments += "--operator-output-setting-note"
    $Arguments += $OperatorOutputSettingNote
}

Push-Location -LiteralPath $RepoRoot
try {
    & $PythonExe @Arguments | Out-Null
    $CollectionExit = $LASTEXITCODE
}
finally {
    Pop-Location
}
if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
    Write-Output "1. result: failure"
    Write-Output "2. operator_result.json: $OutputPath"
    Write-Output "3. error: collector did not write the expected UTF-8 JSON result"
    exit 1
}
$Result = Get-Content -LiteralPath $OutputPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($CollectionExit -eq 0 -and $Result.status -eq "success") {
    Write-Output "1. result: success"
    Write-Output "2. operator_result.json: $OutputPath"
    exit 0
}
Write-Output "1. result: failure"
Write-Output "2. operator_result.json: $OutputPath"
if ($Result.status -eq "failure" -and @($Result.failed_checks).Count -gt 0) {
    Write-Output ("3. error: " + (($Result.failed_checks -join ", ")))
} elseif ($CollectionExit -ne 0) {
    Write-Output "3. error: collector process failed; the existing result was preserved when requested"
} else {
    Write-Output "3. error: collector returned an unexpected result state"
}
exit 1
'''


def _validated_profile_mapping(
    profile: dict[str, Any], rows: list[tuple[str, str]]
) -> dict[str, str]:
    if profile.get("schema_version") != "ymm4_character_alias_profile.v1":
        raise ValueError("PROFILE_SCHEMA_MISMATCH")
    if profile.get("selection_policy") != "explicit_only":
        raise ValueError("PROFILE_MUST_BE_EXPLICIT_ONLY")
    if profile.get("strict_coverage") is not True:
        raise ValueError("PROFILE_STRICT_COVERAGE_REQUIRED")
    if profile.get("universal_default_claimed") is not False:
        raise ValueError("PROFILE_MUST_NOT_CLAIM_UNIVERSAL_DEFAULT")
    mapping = {
        str(key): str(value)
        for key, value in _dict(
            profile.get("canonical_to_yymm4_character")
        ).items()
    }
    speakers = {speaker for speaker, _ in rows}
    if speakers != CANONICAL_SPEAKERS:
        raise ValueError("CANONICAL_SPEAKER_SET_MISMATCH")
    if set(mapping) != speakers or any(not mapping[speaker] for speaker in speakers):
        raise ValueError("PROFILE_COVERAGE_MISMATCH")
    if set(mapping.values()) != set(EXPECTED_CHARACTER_COUNTS):
        raise ValueError("PROFILE_TARGET_CHARACTER_SET_MISMATCH")
    return mapping


def _validate_operator_import_base(
    source: Path, expected_rows: list[tuple[str, str]]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not source.exists():
        raise FileNotFoundError(f"OPERATOR_IMPORT_BASE_MISSING:{source}")
    project = load_ymmp(source)
    timelines = project.get("Timelines")
    if (
        not isinstance(timelines, list)
        or len(timelines) != 1
        or project.get("SelectedTimelineIndex") != 0
    ):
        raise ValueError("OPERATOR_IMPORT_BASE_MUST_HAVE_ONE_SELECTED_TIMELINE")
    items = _get_timeline_items(project)
    if any(_item_type(item) != "VoiceItem" for item in items):
        raise ValueError("OPERATOR_IMPORT_BASE_MUST_CONTAIN_VOICEITEMS_ONLY")
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    if len(voices) != 9:
        raise ValueError(f"OPERATOR_IMPORT_BASE_VOICEITEM_COUNT_MISMATCH:{len(voices)}")
    actual_rows = [
        (str(item.get("CharacterName") or ""), str(item.get("Serif") or ""))
        for item in voices
    ]
    if actual_rows != expected_rows:
        raise ValueError("OPERATOR_IMPORT_BASE_TEXT_OR_CHARACTER_ORDER_MISMATCH")
    if dict(Counter(character for character, _ in actual_rows)) != EXPECTED_CHARACTER_COUNTS:
        raise ValueError("OPERATOR_IMPORT_BASE_CHARACTER_COUNTS_MISMATCH")
    frames = [int(item.get("Frame", -1)) for item in voices]
    if any(frame < 0 for frame in frames) or any(
        left >= right for left, right in zip(frames, frames[1:])
    ):
        raise ValueError("OPERATOR_IMPORT_BASE_TIMING_ORDER_MISMATCH")
    if any(int(item.get("Length", 0) or 0) <= 0 for item in voices):
        raise ValueError("OPERATOR_IMPORT_BASE_VOICEITEM_LENGTH_INVALID")
    timeline = _first_timeline(project)
    if int(timeline.get("Length", 0) or 0) < max(
        int(item.get("Frame", 0) or 0) + int(item.get("Length", 0) or 0)
        for item in voices
    ):
        raise ValueError("OPERATOR_IMPORT_BASE_TIMELINE_TOO_SHORT")
    return project, voices


def _derive_scene_specs(voices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scenes: list[dict[str, Any]] = []
    for index, (scene_id, start, end) in enumerate(SCENE_ROWS):
        start_frame = int(voices[start].get("Frame", 0) or 0)
        if index + 1 < len(SCENE_ROWS):
            end_frame = int(voices[SCENE_ROWS[index + 1][1]].get("Frame", 0) or 0)
        else:
            last = voices[end - 1]
            end_frame = int(last.get("Frame", 0) or 0) + int(last.get("Length", 0) or 0)
        if end_frame <= start_frame:
            raise ValueError(f"SCENE_BOUNDARY_INVALID:{scene_id}")
        scenes.append(
            {
                "scene_id": scene_id,
                "cue_ids": [
                    f"cue_{row:03d}" for row in range(start + 1, end + 1)
                ],
                "start_frame": start_frame,
                "end_frame": end_frame,
                "length_frames": end_frame - start_frame,
                "timing_source": "actual_operator_imported_voiceitem_frames",
                "label": LABEL_TEMPLATE.format(scene_id=scene_id),
                "image_remark": f"{REMARK_PREFIX}{scene_id}:image",
                "text_remark": f"{REMARK_PREFIX}{scene_id}:text",
            }
        )
    return scenes


def _readback_generated_project(
    *,
    project_path: Path,
    expected_rows: list[tuple[str, str]],
    asset_path: Path,
    source_voice_digests: list[str] | None,
    source_timeline_length: int | None,
) -> dict[str, Any]:
    project = load_ymmp(project_path)
    timeline = _first_timeline(project)
    items = _get_timeline_items(project)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    images = [item for item in items if _item_type(item) == "ImageItem"]
    texts = [item for item in items if _item_type(item) == "TextItem"]
    voice_digests = [_json_sha256(item) for item in voices]
    actual_rows = [
        (str(item.get("CharacterName") or ""), str(item.get("Serif") or ""))
        for item in voices
    ]
    scenes = _derive_scene_specs(voices) if len(voices) == 9 else []
    scene_rows = []
    for scene in scenes:
        scene_images = [item for item in images if item.get("Remark") == scene["image_remark"]]
        scene_texts = [item for item in texts if item.get("Remark") == scene["text_remark"]]
        scene_rows.append(
            {
                "scene_id": scene["scene_id"],
                "label": scene["label"],
                "ImageItem_count": len(scene_images),
                "TextItem_count": len(scene_texts),
                "image_path_matches": len(scene_images) == 1
                and str(scene_images[0].get("FilePath") or "").casefold()
                == str(asset_path).casefold(),
                "image_timing_matches": _item_timing_matches(scene_images, scene),
                "text_timing_matches": _item_timing_matches(scene_texts, scene),
                "text_matches": len(scene_texts) == 1
                and scene_texts[0].get("Text") == scene["label"],
            }
        )
    path_audit = _audit_project_paths(
        project,
        allowed_local_paths={str(project_path.resolve()), str(asset_path.resolve())},
    )
    checks = {
        "project_parse_pass": bool(timeline),
        "one_selected_timeline": len(project.get("Timelines", [])) == 1
        and project.get("SelectedTimelineIndex") == 0,
        "base_gui_layout_state_stripped": "LayoutXml" not in project
        and "CollapsedGroups" not in project,
        "VoiceItem_count_9": len(voices) == 9,
        "VoiceItem_text_character_order_matches_derived_csv": actual_rows == expected_rows,
        "VoiceItem_objects_unchanged": source_voice_digests is None
        or voice_digests == source_voice_digests,
        "character_counts_3_6": dict(Counter(row[0] for row in actual_rows))
        == EXPECTED_CHARACTER_COUNTS,
        "ImageItem_count_3": len(images) == 3,
        "independent_TextItem_count_3": len(texts) == 3,
        "item_type_families_exact": set(Counter(_item_type(item) for item in items))
        == {"VoiceItem", "ImageItem", "TextItem"},
        "scene_placeholder_coverage": len(scene_rows) == 3
        and all(
            row["ImageItem_count"] == 1
            and row["TextItem_count"] == 1
            and row["image_path_matches"]
            and row["image_timing_matches"]
            and row["text_timing_matches"]
            and row["text_matches"]
            for row in scene_rows
        ),
        "internal_boundary_labels_explicit": len(scene_rows) == 3
        and all(
            all(token in str(row["label"]) for token in BOUNDARY_TOKENS)
            for row in scene_rows
        ),
        "timeline_length_preserved": source_timeline_length is None
        or int(timeline.get("Length", 0) or 0) == source_timeline_length,
        "only_expected_local_absolute_references": not path_audit[
            "unexpected_local_reference_present"
        ],
        "no_external_or_file_uri_reference": not path_audit[
            "external_or_file_uri_reference_present"
        ],
        "no_unc_reference": not path_audit["unc_reference_present"],
    }
    failed = [name for name, value in checks.items() if value is not True]
    normalized = copy.deepcopy(project)
    normalized["FilePath"] = "<LOCAL_INTERNAL_REVIEW_PROJECT>"
    for item in _get_timeline_items(normalized):
        if _item_type(item) == "ImageItem" and str(item.get("Remark") or "").startswith(REMARK_PREFIX):
            item["FilePath"] = "<PILOT_ASSET>/internal_review_placeholder.png"
    return {
        "schema_version": "verified_local_evidence_generated_project_readback.actual.v1",
        "status": "structural_pass" if not failed else "failed",
        "project_file": project_path.name,
        "project_sha256": _sha256(project_path),
        "normalized_project_sha256": _json_sha256(normalized),
        "asset": {
            "repo_relative_path": ASSET_RELATIVE_PATH.as_posix(),
            "sha256": _sha256(asset_path),
            **_png_metadata(asset_path),
            "external_source": False,
        },
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "width": _dict(timeline.get("VideoInfo")).get("Width"),
            "height": _dict(timeline.get("VideoInfo")).get("Height"),
            "length_frames": timeline.get("Length"),
            "item_type_counts": dict(Counter(_item_type(item) for item in items)),
        },
        "characters": dict(Counter(row[0] for row in actual_rows)),
        "scenes": scene_rows,
        "path_audit": {
            **path_audit,
            "committed_metadata_contains_private_paths": False,
            "project_commit_disposition": "local_only_ignored",
        },
        "checks": checks,
        "failed_checks": failed,
        "internal_review_only": True,
        "render_or_export_performed_by_generator": False,
        "production_ymmp_written": False,
        "public_ready": False,
    }


def _item_timing_matches(items: list[dict[str, Any]], scene: dict[str, Any]) -> bool:
    return (
        len(items) == 1
        and int(items[0].get("Frame", -1)) == scene["start_frame"]
        and int(items[0].get("Length", -1)) == scene["length_frames"]
    )


def _validation_payload(
    root: Path, failed: list[str], hashes: dict[str, str]
) -> dict[str, Any]:
    unique_failed = list(dict.fromkeys(failed))
    return {
        "schema_version": "verified_local_evidence_input_validation_readback.v1",
        "artifact_id": f"{ARTIFACT_ID}_validation",
        "status": "passed" if not unique_failed else "failed",
        "pilot_dir": DEFAULT_OUTPUT_DIRNAME,
        "checks": {
            "authorized_source_hash_and_schema_validation": not any(
                item.startswith("source_") or item.startswith("source_contract")
                for item in unique_failed
            ),
            "claim_ledger_9_of_9": not any("claim" in item for item in unique_failed),
            "unsupported_claims_absent": "unsupported_claim_present" not in unique_failed,
            "script_9_cues_2_2_5": "script_9_cue_3_scene_invariant_failed" not in unique_failed,
            "canonical_and_derived_csv_invariants": not any("csv" in item or "profile" in item for item in unique_failed),
            "static_project_contract": not any("project_" in item for item in unique_failed),
            "operator_batch_contract": not any("operator_" in item for item in unique_failed),
            "tracked_metadata_sanitized": "private_or_external_reference_present" not in unique_failed,
        },
        "failed_checks": unique_failed,
        "verified_file_sha256": hashes,
        "cue_count": 9,
        "scene_allocation": {"S1": 2, "S2": 2, "S3": 5},
        "canonical_speaker_counts": EXPECTED_CANONICAL_COUNTS,
        "derived_character_counts": EXPECTED_CHARACTER_COUNTS,
        "manual_action_count": 5,
        "operator_return_item_count": 3,
        "yymm4_launched_by_validator": False,
        "computer_use_invoked": False,
        "full_pytest_run": False,
    }


def _runtime_state_id(text: str) -> str:
    match = re.search(r"^Project-State-ID:\s*(\S+)", text, re.MULTILINE)
    if not match:
        raise ValueError("RUNTIME_STATE_ID_MISSING")
    return match.group(1)


def _resolve_package_dir(
    pilot_dir: Path, package_dir: str | Path | None
) -> Path:
    if package_dir is not None:
        package = Path(package_dir).resolve()
        if not (package / CSV_RECEIPT_RELATIVE).exists():
            raise FileNotFoundError(f"EPISODE_PACKAGE_INVALID:{package}")
        return package
    adjacent = pilot_dir.parent
    if (adjacent / CSV_RECEIPT_RELATIVE).exists():
        return adjacent
    checkout = Path(__file__).resolve().parents[2]
    candidate = checkout / "production_pilots" / EPISODE_ID
    if (candidate / CSV_RECEIPT_RELATIVE).exists():
        return candidate
    raise FileNotFoundError("EPISODE_PACKAGE_COULD_NOT_BE_RESOLVED")


def _json_pointer(payload: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON_POINTER_INVALID:{pointer}")
    current = payload
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise ValueError(f"JSON_POINTER_NON_CONTAINER:{pointer}")
    return current


def _provenance_note() -> str:
    return """# Source provenance and rights note

This pilot uses only tracked NLMYTGen evidence from the bounded Episode 002 YMM4 CSV-import and diagnostic-placeholder observations. It does not fetch the web, download external media, or adopt an external editorial source.

The evidence supports a concise internal recap of what was actually observed: nine ordered VoiceItems, environment-specific automatic character binding, the observed timing, three diagnostic placeholder scenes, and explicit non-final boundaries. It does not support production readiness, public readiness, legal or rights approval, source replacement, upload, or publication.

The placeholder PNG is generated deterministically by the Python standard library and contains no external asset. Any future external editorial input or media requires a separate provenance, identity, rights-context, and approval gate.
"""


def _write_csv(path: Path, rows: list[tuple[str, str]]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerows(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(stream.getvalue().encode("utf-8"))


def _load_csv_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [tuple(row) for row in csv.reader(handle) if row]
    if any(len(row) != 2 for row in rows):
        raise ValueError(f"CSV_MUST_BE_HEADERLESS_TWO_COLUMN:{path.name}")
    return [(row[0], row[1]) for row in rows]


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"SOURCE_OUTSIDE_REPOSITORY:{path.name}") from exc


def _first_timeline(data: dict[str, Any]) -> dict[str, Any]:
    timelines = data.get("Timelines")
    if not isinstance(timelines, list) or not timelines or not isinstance(timelines[0], dict):
        raise ValueError("YMM4_PROJECT_TIMELINE_MISSING")
    return timelines[0]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

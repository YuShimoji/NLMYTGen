from __future__ import annotations

import csv
import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.pipeline.media_validation import (
    decode_with_ffmpeg,
    inspect_iso_bmff,
    probe_with_ffprobe,
)
from src.pipeline.verified_local_evidence_input_pilot import (
    ASSET_RELATIVE_PATH,
    DERIVED_CSV_FILENAME,
    LOCAL_OPERATOR_RESULT_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RENDER_FILENAME,
    _readback_generated_project,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


REVIEW_FILES: tuple[str, ...] = (
    "README_INTERNAL_REVIEW.md",
    "internal_review_manifest.json",
    "render_validation_readback.json",
    "render_receipt.json",
    "source_to_output_traceability.json",
    "operator_batch_correction_report.json",
    "operator_review_sheet.md",
    "limitations.md",
)

PROXY_FILENAME = "episode_002_verified_local_evidence_internal_review.proxy.mp4"
EXPECTED_PROXY_SHA256 = (
    "45BD0A060BAA45C1BB44068F4ADAE1A6B50DBBF86FABA70F3A1761809BE5A025"
)
EXPECTED_PROXY_SIZE_BYTES = 1_400_926
TARGET_PROJECT_STATE_ID = (
    "episode-002-verified-local-evidence-internal-render-validated-v1"
)
TARGET_PRODUCT_STATE = "episode-002-verified-local-evidence-internal-render-validated"
TARGET_PRODUCT_GATE = "milestone-integration-audit"
TARGET_RECOMMENDED_NEXT = "audit-feature-branch-integration-after-render-milestone"

_PRIVATE_PATH_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(?:^|[\s\"'])(?:[a-z]:[\\/])"),
    re.compile(r"(?i)file://"),
    re.compile(r"\\\\[^\\\s]+\\"),
    re.compile(r"(?i)(?:^|[/\\])Users[/\\][^/\\]+"),
)


class InternalRenderReviewError(RuntimeError):
    """Raised when the local render milestone cannot be accepted."""


def build_internal_render_review(
    pilot_dir: str | Path,
    *,
    repo_root: str | Path | None = None,
    expected_proxy_sha256: str | None = EXPECTED_PROXY_SHA256,
    expected_proxy_size_bytes: int | None = EXPECTED_PROXY_SIZE_BYTES,
    operator_output_setting_note: str = "MPEG",
) -> dict[str, Any]:
    """Build the tracked review package from immutable local operator evidence.

    The original operator result, project, render, and proxy are only read.  All
    emitted paths are repository-relative and all generated artifacts are
    deterministic for an unchanged evidence set.
    """

    pilot = Path(pilot_dir).resolve()
    root = _resolve_repo_root(pilot, repo_root)
    local_outputs = pilot / LOCAL_OUTPUT_DIRNAME
    operator_result_path = local_outputs / LOCAL_OPERATOR_RESULT_FILENAME
    project_path = local_outputs / LOCAL_PROJECT_FILENAME
    render_path = local_outputs / LOCAL_RENDER_FILENAME
    proxy_path = local_outputs / PROXY_FILENAME

    operator_result_bytes = _required_bytes(operator_result_path)
    operator_result_sha256 = _sha256_bytes(operator_result_bytes)
    operator_result = _parse_utf8_json(operator_result_bytes, operator_result_path)
    _validate_operator_result(operator_result)

    expected = _mapping(operator_result.get("independently_verified"))
    _verify_file_identity(
        project_path,
        expected_sha256=_required_upper_hex(expected, "project_sha256"),
    )
    _verify_file_identity(
        render_path,
        expected_sha256=_required_upper_hex(expected, "render_sha256"),
        expected_size=_required_int(expected, "render_size_bytes"),
    )
    batch_not_before = _parse_utc(
        _required_string(operator_result, "batch_not_before_utc"),
        "batch_not_before_utc",
    )
    collected_at = _parse_utc(
        _required_string(operator_result, "collected_at_utc"),
        "collected_at_utc",
    )
    freshness = _validate_freshness(
        project_path=project_path,
        render_path=render_path,
        batch_not_before=batch_not_before,
        collected_at=collected_at,
    )

    expected_rows = _read_csv_rows(pilot / DERIVED_CSV_FILENAME)
    project_readback = _readback_generated_project(
        project_path=project_path,
        expected_rows=expected_rows,
        asset_path=pilot / ASSET_RELATIVE_PATH,
        source_voice_digests=None,
        source_timeline_length=None,
    )
    if project_readback.get("status") != "structural_pass" or project_readback.get(
        "failed_checks"
    ):
        raise InternalRenderReviewError(
            "PROJECT_STRUCTURAL_VALIDATION_FAILED:"
            + ",".join(str(item) for item in project_readback.get("failed_checks", []))
        )
    if expected.get("project_structural_pass") is not True:
        raise InternalRenderReviewError("OPERATOR_RESULT_PROJECT_STRUCTURE_NOT_PASSED")

    original_media = _inspect_media(render_path, root)
    if not original_media["checks"]["media_validation_pass"]:
        raise InternalRenderReviewError("ORIGINAL_RENDER_MEDIA_VALIDATION_FAILED")

    if not proxy_path.is_file():
        raise InternalRenderReviewError("REVIEW_PROXY_MISSING")
    _verify_file_identity(
        proxy_path,
        expected_sha256=expected_proxy_sha256,
        expected_size=expected_proxy_size_bytes,
    )
    proxy_media = _inspect_media(proxy_path, root)
    if not proxy_media["checks"]["media_validation_pass"]:
        raise InternalRenderReviewError("REVIEW_PROXY_MEDIA_VALIDATION_FAILED")

    source_snapshot = _source_snapshot(pilot, root)
    reduction_ratio = round(render_path.stat().st_size / proxy_path.stat().st_size, 3)
    reduction_percent = round(
        (1 - proxy_path.stat().st_size / render_path.stat().st_size) * 100, 6
    )
    repo_paths = {
        "pilot": _repo_relative(pilot, root),
        "operator_result": _repo_relative(operator_result_path, root),
        "project": _repo_relative(project_path, root),
        "render": _repo_relative(render_path, root),
        "proxy": _repo_relative(proxy_path, root),
    }

    validation_readback = _render_validation_readback(
        repo_paths=repo_paths,
        operator_result=operator_result,
        operator_result_sha256=operator_result_sha256,
        project_readback=project_readback,
        original_media=original_media,
        proxy_media=proxy_media,
        freshness=freshness,
    )
    traceability = _source_to_output_traceability(
        pilot=pilot,
        root=root,
        project_path=project_path,
        original_media=original_media,
    )
    correction_report = _operator_batch_correction_report(
        pilot=pilot,
        root=root,
        operator_result=operator_result,
        operator_output_setting_note=operator_output_setting_note,
    )
    render_receipt = _render_receipt(
        repo_paths=repo_paths,
        operator_result=operator_result,
        operator_result_sha256=operator_result_sha256,
        project_readback=project_readback,
        original_media=original_media,
        proxy_media=proxy_media,
        reduction_ratio=reduction_ratio,
        reduction_percent=reduction_percent,
        operator_output_setting_note=operator_output_setting_note,
    )
    manifest = _internal_review_manifest(
        repo_paths=repo_paths,
        operator_result=operator_result,
        operator_result_sha256=operator_result_sha256,
        project_readback=project_readback,
        original_media=original_media,
        proxy_media=proxy_media,
        source_snapshot=source_snapshot,
    )

    payloads: dict[str, dict[str, Any]] = {
        "internal_review_manifest.json": manifest,
        "render_validation_readback.json": validation_readback,
        "render_receipt.json": render_receipt,
        "source_to_output_traceability.json": traceability,
        "operator_batch_correction_report.json": correction_report,
    }
    texts = {
        "README_INTERNAL_REVIEW.md": _review_readme(
            repo_paths=repo_paths,
            original_media=original_media,
            proxy_media=proxy_media,
            reduction_ratio=reduction_ratio,
            reduction_percent=reduction_percent,
        ),
        "operator_review_sheet.md": _operator_review_sheet(),
        "limitations.md": _limitations(),
    }

    for name, payload in payloads.items():
        _write_json(pilot / name, payload)
    for name, content in texts.items():
        _write_text(pilot / name, content)

    if operator_result_path.read_bytes() != operator_result_bytes:
        raise InternalRenderReviewError("OPERATOR_RESULT_BYTES_CHANGED")
    if _source_snapshot(pilot, root) != source_snapshot:
        raise InternalRenderReviewError("SOURCE_EVIDENCE_CHANGED_DURING_REVIEW_BUILD")
    _audit_review_files(pilot)

    return {
        "status": "media_validated_internal_review_ready",
        "project_state_id": TARGET_PROJECT_STATE_ID,
        "review_files": list(REVIEW_FILES),
        "operator_result_sha256": operator_result_sha256,
        "render_sha256": _sha256(render_path),
        "proxy_sha256": _sha256(proxy_path),
        "render_size_bytes": render_path.stat().st_size,
        "proxy_size_bytes": proxy_path.stat().st_size,
        "reduction_ratio": reduction_ratio,
    }


def _render_validation_readback(
    *,
    repo_paths: dict[str, str],
    operator_result: dict[str, Any],
    operator_result_sha256: str,
    project_readback: dict[str, Any],
    original_media: dict[str, Any],
    proxy_media: dict[str, Any],
    freshness: dict[str, Any],
) -> dict[str, Any]:
    expected = _mapping(operator_result["independently_verified"])
    return {
        "schema_version": "verified_local_evidence_render_validation_readback.v1",
        "artifact_id": "episode_002_verified_local_evidence_render_validation",
        "status": "passed",
        "operator_result": {
            "repo_relative_path": repo_paths["operator_result"],
            "sha256": operator_result_sha256,
            "parsed_as_utf8": True,
            "source_bytes_preserved": True,
            "reported_status": operator_result["status"],
            "reported_failed_checks": operator_result["failed_checks"],
        },
        "identity_checks": {
            "project_sha256_matches_operator_result": project_readback["project_sha256"]
            == expected["project_sha256"],
            "render_sha256_matches_operator_result": original_media["sha256"]
            == expected["render_sha256"],
            "render_size_matches_operator_result": original_media["size_bytes"]
            == expected["render_size_bytes"],
            **freshness,
        },
        "project": {
            "repo_relative_path": repo_paths["project"],
            "sha256": project_readback["project_sha256"],
            "status": project_readback["status"],
            "timeline": project_readback["timeline"],
            "characters": project_readback["characters"],
            "checks": project_readback["checks"],
            "failed_checks": project_readback["failed_checks"],
            "evidence_grade": "verified",
        },
        "original_render": original_media,
        "review_proxy": proxy_media,
        "evidence_boundary": {
            "container_codec_decode": "verified",
            "operator_gui_actions_and_output_setting": "observed",
            "large_file_cause": "inferred_from_verified_bitrate",
            "visual_editorial_acceptance": "unknown",
            "semantic_cue_alignment_in_encoded_media": "unknown",
        },
        "failed_checks": [],
    }


def _render_receipt(
    *,
    repo_paths: dict[str, str],
    operator_result: dict[str, Any],
    operator_result_sha256: str,
    project_readback: dict[str, Any],
    original_media: dict[str, Any],
    proxy_media: dict[str, Any],
    reduction_ratio: float,
    reduction_percent: float,
    operator_output_setting_note: str,
) -> dict[str, Any]:
    operator_reported = _mapping(operator_result.get("operator_reported"))
    return {
        "schema_version": "verified_local_evidence_render_receipt.v1",
        "artifact_id": "episode_002_verified_local_evidence_internal_render_receipt",
        "status": "passed",
        "classification": {
            "internal_review_only": True,
            "final": False,
            "public": False,
            "production": False,
        },
        "operator_result": {
            "repo_relative_path": repo_paths["operator_result"],
            "sha256": operator_result_sha256,
            "status": operator_result["status"],
            "failed_checks": operator_result["failed_checks"],
            "preserved_byte_for_byte": True,
            "evidence_grade": "verified",
        },
        "project": {
            "repo_relative_path": repo_paths["project"],
            "sha256": project_readback["project_sha256"],
            "structural_status": project_readback["status"],
            "item_type_counts": project_readback["timeline"]["item_type_counts"],
            "characters": project_readback["characters"],
            "evidence_grade": "verified",
        },
        "original_render": {
            "repo_relative_path": repo_paths["render"],
            "sha256": original_media["sha256"],
            "size_bytes": original_media["size_bytes"],
            "media": original_media["media"],
            "decode_smoke": original_media["decode"],
            "immutable_source": True,
            "evidence_grade": "verified",
        },
        "review_proxy": {
            "repo_relative_path": repo_paths["proxy"],
            "sha256": proxy_media["sha256"],
            "size_bytes": proxy_media["size_bytes"],
            "media": proxy_media["media"],
            "decode_smoke": proxy_media["decode"],
            "reduction_ratio": reduction_ratio,
            "size_reduction_percent": reduction_percent,
            "source_overwritten": False,
            "evidence_grade": "verified",
        },
        "reviewability_analysis": {
            "verified_original_video_bitrate_bps": original_media["media"].get(
                "video_bitrate_bps"
            ),
            "verified_original_overall_bitrate_bps": original_media["media"].get(
                "overall_bitrate_bps"
            ),
            "large_file_cause": "very_high_video_bitrate_is_the_primary_size_driver",
            "large_file_cause_evidence_grade": "inferred",
            "proxy_available": True,
        },
        "operator_observations": {
            "yymm4_product_version": operator_reported.get("yymm4_product_version"),
            "profile_observation_version": operator_reported.get(
                "profile_observation_version"
            ),
            "no_unexpected_mapping_character_or_parse_error": operator_reported.get(
                "no_unexpected_mapping_character_or_parse_error"
            ),
            "output_setting_note": operator_output_setting_note,
            "output_setting_note_is_codec_label": False,
            "evidence_grade": "observed",
        },
        "achieved_state_recommendation": {
            "Project-State-ID": TARGET_PROJECT_STATE_ID,
            "Product-State": TARGET_PRODUCT_STATE,
            "Product-Gate": TARGET_PRODUCT_GATE,
            "Recommended-Next": TARGET_RECOMMENDED_NEXT,
            "External-State": "public-repo-feature-branch",
        },
        "not_claimed": [
            "visual or editorial acceptance",
            "production readiness",
            "public readiness",
            "rights or legal approval",
            "upload or publication",
            "default-branch integration",
        ],
    }


def _internal_review_manifest(
    *,
    repo_paths: dict[str, str],
    operator_result: dict[str, Any],
    operator_result_sha256: str,
    project_readback: dict[str, Any],
    original_media: dict[str, Any],
    proxy_media: dict[str, Any],
    source_snapshot: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": "verified_local_evidence_internal_review_manifest.v1",
        "artifact_id": "episode_002_verified_local_evidence_internal_review_v1",
        "status": "media_validated",
        "classification": {
            "internal_review_only": True,
            "not_final": True,
            "non_public": True,
            "non_production": True,
        },
        "primary_review_surface": "README_INTERNAL_REVIEW.md",
        "tracked_review_files": [
            {"path": name, "role": role}
            for name, role in (
                ("README_INTERNAL_REVIEW.md", "primary human review surface"),
                ("render_validation_readback.json", "machine validation evidence"),
                ("render_receipt.json", "adjudicated render receipt"),
                ("source_to_output_traceability.json", "source-to-output evidence map"),
                (
                    "operator_batch_correction_report.json",
                    "operator batch hardening report",
                ),
                ("operator_review_sheet.md", "bounded human review questions"),
                ("limitations.md", "remaining evidence and portability limits"),
            )
        ],
        "local_ignored_artifacts": [
            {
                "repo_relative_path": repo_paths["operator_result"],
                "sha256": operator_result_sha256,
                "role": "immutable operator result source",
                "committed": False,
            },
            {
                "repo_relative_path": repo_paths["project"],
                "sha256": project_readback["project_sha256"],
                "role": "internal local YMM4 project",
                "committed": False,
            },
            {
                "repo_relative_path": repo_paths["render"],
                "sha256": original_media["sha256"],
                "role": "immutable original internal render",
                "committed": False,
            },
            {
                "repo_relative_path": repo_paths["proxy"],
                "sha256": proxy_media["sha256"],
                "role": "lightweight internal review proxy",
                "committed": False,
            },
        ],
        "source_evidence_sha256": source_snapshot,
        "evidence_grades": {
            "verified": "direct file, parser, probe, decode, or focused-test evidence",
            "observed": "operator-reported YMM4 action or UI setting",
            "inferred": "conclusion supported by verified measurements",
            "unknown": "not established without human visual/editorial review",
        },
        "achieved_state": {
            "Project-State-ID": TARGET_PROJECT_STATE_ID,
            "Product-State": TARGET_PRODUCT_STATE,
            "Product-Gate": TARGET_PRODUCT_GATE,
            "Recommended-Next": TARGET_RECOMMENDED_NEXT,
            "External-State": "public-repo-feature-branch",
        },
        "evidence_boundary": {
            "original_render_preserved": True,
            "operator_result_preserved": True,
            "local_binaries_ignored": True,
            "production_or_public_transition": False,
        },
        "operator_collection_status": operator_result["status"],
    }


def _source_to_output_traceability(
    *,
    pilot: Path,
    root: Path,
    project_path: Path,
    original_media: dict[str, Any],
) -> dict[str, Any]:
    script = _load_json(pilot / "canonical_script.json")
    ledger = _load_json(pilot / "source_claim_ledger.json")
    canonical_rows = _read_csv_rows(pilot / "canonical_yymm4.csv")
    derived_rows = _read_csv_rows(pilot / DERIVED_CSV_FILENAME)
    claims = {
        str(claim["cue_id"]): claim for claim in _list(ledger.get("claims"))
    }
    project = load_ymmp(project_path)
    voices = [
        item
        for item in _get_timeline_items(project)
        if _item_type(item) == "VoiceItem"
    ]
    cues = _list(script.get("cues"))
    if not (len(cues) == len(canonical_rows) == len(derived_rows) == len(voices) == 9):
        raise InternalRenderReviewError("SOURCE_TO_PROJECT_CUE_COUNT_MISMATCH")

    rows: list[dict[str, Any]] = []
    for index, cue in enumerate(cues):
        cue_id = str(cue["cue_id"])
        claim = _mapping(claims.get(cue_id))
        canonical_speaker, canonical_text = canonical_rows[index]
        derived_character, derived_text = derived_rows[index]
        voice = voices[index]
        source_refs = [
            {
                "repo_relative_path": str(item["source_file"]).replace("\\", "/"),
                "json_pointer": item["json_pointer_or_field"],
                "matched": item["matched"],
                "evidence_grade": "verified",
            }
            for item in _list(claim.get("evidence"))
        ]
        checks = {
            "script_matches_canonical_csv": cue.get("speaker") == canonical_speaker
            and cue.get("text") == canonical_text,
            "canonical_text_matches_derived_csv": canonical_text == derived_text,
            "derived_row_matches_project_voiceitem": derived_character
            == voice.get("CharacterName")
            and derived_text == voice.get("Serif"),
        }
        if not all(checks.values()) or not source_refs:
            raise InternalRenderReviewError(f"TRACEABILITY_FAILED:{cue_id}")
        rows.append(
            {
                "sequence": index + 1,
                "cue_id": cue_id,
                "scene_id": cue["scene_id"],
                "source_claim_references": source_refs,
                "script": {
                    "speaker": canonical_speaker,
                    "text": canonical_text,
                    "evidence_grade": "verified",
                },
                "derived_csv": {
                    "row": index + 1,
                    "character": derived_character,
                    "text": derived_text,
                    "evidence_grade": "verified",
                },
                "project_voiceitem": {
                    "sequence": index + 1,
                    "character": voice.get("CharacterName"),
                    "text": voice.get("Serif"),
                    "evidence_grade": "verified",
                },
                "checks": checks,
                "encoded_render": {
                    "operator_render_completion": "observed",
                    "container_codec_and_decode": "verified",
                    "semantic_cue_alignment": "unknown",
                },
            }
        )
    return {
        "schema_version": "verified_local_evidence_source_to_output_traceability.v1",
        "artifact_id": "episode_002_verified_local_evidence_source_to_output_traceability",
        "status": "passed",
        "source_to_project_traceability": "9_of_9_verified",
        "project_to_render_traceability": "operator_observed_and_media_verified",
        "render_semantic_alignment": "unknown_pending_human_review",
        "project_repo_relative_path": _repo_relative(project_path, root),
        "render_repo_relative_path": original_media["repo_relative_path"],
        "cues": rows,
        "failed_checks": [],
    }


def _operator_batch_correction_report(
    *,
    pilot: Path,
    root: Path,
    operator_result: dict[str, Any],
    operator_output_setting_note: str,
) -> dict[str, Any]:
    operator = pilot / "operator_batch"
    run_text = (operator / "run_yymm4_operator_batch.ps1").read_text(encoding="utf-8")
    collector_text = (operator / "collect_operator_result.ps1").read_text(
        encoding="utf-8"
    )
    readme_text = (operator / "README_OPERATOR_BATCH.md").read_text(encoding="utf-8")
    manifest = _load_json(operator / "operator_batch_manifest.json")
    combined = "\n".join((run_text, collector_text, readme_text))
    checks = {
        "explicit_python_utf8": "PYTHONUTF8" in combined
        and "PYTHONIOENCODING" in combined,
        "powershell_utf8_file_read": "Get-Content" in combined
        and "-Encoding UTF8" in combined,
        "collect_only_supported": "CollectOnly" in run_text,
        "project_save_and_video_output_distinct": ".local.ymmp" in readme_text
        and ".mp4" in readme_text
        and "Save As" in readme_text,
        "manual_actions_at_most_five": int(manifest.get("manual_action_count", 99)) <= 5,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise InternalRenderReviewError(
            "OPERATOR_BATCH_HARDENING_INCOMPLETE:" + ",".join(failed)
        )
    operator_reported = _mapping(operator_result.get("operator_reported"))
    return {
        "schema_version": "verified_local_evidence_operator_batch_correction_report.v1",
        "artifact_id": "episode_002_verified_local_evidence_operator_batch_corrections",
        "status": "passed",
        "operator_batch_manifest": _repo_relative(
            operator / "operator_batch_manifest.json", root
        ),
        "corrections": [
            {
                "requirement_id": "R4",
                "defect": "ambiguous native-stdout JSON transport under Windows PowerShell",
                "correction": "Python-written UTF-8 JSON file read with Get-Content -Raw -Encoding UTF8",
                "verification": "focused UTF-8 Japanese JSON regression and static script check",
                "result": "passed",
            },
            {
                "requirement_id": "R5",
                "defect": "project Save As and video output instructions were ambiguous",
                "correction": "project .local.ymmp and video .mp4 targets are named separately",
                "verification": "tracked README and manifest contract",
                "result": "passed",
            },
            {
                "requirement_id": "R6",
                "defect": "no resume-after-render collection route",
                "correction": "-CollectOnly reuses existing outputs without YMM4 launch or regeneration",
                "verification": "focused collect-only regression",
                "result": "passed",
            },
            {
                "requirement_id": "R7",
                "defect": "YMM4 project JSON could be mistaken for an MP4",
                "correction": "dedicated render_is_yymm4_project_json_not_mp4 detection",
                "verification": "focused masquerading-project regression",
                "result": "passed",
            },
            {
                "requirement_id": "R8",
                "defect": "first-32-byte ftyp search was insufficient media evidence",
                "correction": "ISO BMFF box inspection plus ffprobe and decode smoke",
                "verification": "render_validation_readback.json",
                "result": "passed",
            },
        ],
        "checks": checks,
        "operator_environment_observation": {
            "yymm4_product_version": operator_reported.get("yymm4_product_version"),
            "profile_observation_version": operator_reported.get(
                "profile_observation_version"
            ),
            "output_setting_note": operator_output_setting_note,
            "output_setting_note_is_machine_verified_codec": False,
            "evidence_grade": "observed",
        },
        "recovery_contract": {
            "collect_only_supported": True,
            "collect_only_launches_yymm4": False,
            "collect_only_regenerates_project_or_render": False,
            "existing_success_result_is_preserved_byte_for_byte": True,
        },
        "json_transport": "python_written_utf8_file_read_by_powershell_explicit_utf8",
        "manual_action_count": manifest["manual_action_count"],
        "failed_checks": [],
    }


def _review_readme(
    *,
    repo_paths: dict[str, str],
    original_media: dict[str, Any],
    proxy_media: dict[str, Any],
    reduction_ratio: float,
    reduction_percent: float,
) -> str:
    media = original_media["media"]
    return f"""# Episode 002 Internal Review

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

既存のYMM4出力を再renderせず、project構造、original MP4のcontainer/codec、decode、軽量proxyをheadlessで検証した内部レビュー面です。成功はproduction、公開、権利承認、upload、default-branch統合を意味しません。

## まず見るもの

- 軽量review proxy（推奨）: `{repo_paths['proxy']}`
- immutable original render: `{repo_paths['render']}`
- local internal project: `{repo_paths['project']}`
- human review questions: [operator_review_sheet.md](operator_review_sheet.md)

originalとproxyはignored local binaryでありcommitしません。originalは上書きされていません。proxyはoriginalより約{reduction_ratio}倍小さく、size reductionは{reduction_percent}%です。

## Machine-verified

- container/brands: `{media.get('container')}` / `{media.get('brands')}`
- video: `{media.get('video_codec')}`, {media.get('width')}x{media.get('height')}, {media.get('fps')} fps
- audio: `{media.get('audio_codec')}`
- duration: {media.get('duration_seconds')} seconds
- streams: {media.get('stream_count')}
- original SHA-256: `{original_media['sha256']}`
- proxy SHA-256: `{proxy_media['sha256']}`
- original/proxy decode smoke: passed

## Evidence grades

- **verified**: file identity、YMM4 project structure、ISO BMFF、ffprobe metadata、decode smoke。
- **observed**: operatorによるYMM4操作、YMM4 version、出力時に「MPEG」へ変更したという報告。
- **inferred**: originalが大きい主因はverifiedな高video bitrateであること。
- **unknown**: human playback quality、visual/editorial acceptance、encoded media内の9 cue意味一致。

## Evidence map

- [render_validation_readback.json](render_validation_readback.json): machine validation
- [render_receipt.json](render_receipt.json): adjudicated receipt
- [source_to_output_traceability.json](source_to_output_traceability.json): source → cue → CSV → VoiceItem → render boundary
- [operator_batch_correction_report.json](operator_batch_correction_report.json): future batch hardening
- [limitations.md](limitations.md): remaining debt and boundaries

次のproduct gateはfeature/default integration auditです。このREADMEはそのauditの固定内部証拠であり、統合そのものを実行済みとは主張しません。
"""


def _operator_review_sheet() -> str:
    questions = [
        "動画は冒頭から最後まで停止・破損・不自然な欠落なく再生できますか。",
        "9つの台詞で霊夢／魔理沙の割り当てと発話順は正しいですか。",
        "字幕は欠落・切れ・重なりなく読め、音声と自然に同期していますか。",
        "S1／S2／S3の表示は読め、内部確認用・非最終であることが明確ですか。",
        "このrenderを次のfeature/default integration auditの固定内部証拠として使ってよいですか。",
    ]
    rows = "\n".join(
        f"{index}. {question}\n   - Answer: Yes / No / Not reviewed\n   - Notes:"
        for index, question in enumerate(questions, start=1)
    )
    return f"""# Episode 002 Operator Review Sheet

このsheetはhuman visual/editorial review用です。machine validationの合格をproduction/public acceptanceへ拡張しません。

{rows}
"""


def _limitations() -> str:
    return """# Episode 002 Internal Review Limitations

このmilestoneはmedia-validな内部review packageです。以下の3件は意図的に未解決です。

| debt_id | issue | impact | owner | revisit_trigger | status |
| --- | --- | --- | --- | --- | --- |
| D1 | Visual/editorial acceptance remains human review debt. | Machine decode cannot establish readability, timing feel, or editorial quality. | Human reviewer | Before H2 merge-ready acceptance or any creative-final claim. | open |
| D2 | Character profile 4.53.0.9 differs from observed YMM4 4.54.0.1. | This run reported no mapping error, but a future environment may map differently. | Operator/batch maintainer | Any YMM4/profile change, mapping dialog, or character mismatch. | accepted debt |
| D3 | The ignored local project contains machine-local asset references. | The `.local.ymmp` is not guaranteed to open unchanged on another machine. | Future portability slice | Cross-machine transfer, production adoption, or portable project packaging. | accepted debt |

The proxy improves reviewability but does not replace or alter the immutable original. Rights/legal approval, production project creation, upload/publication, and default-branch integration remain outside this milestone.
"""


def _inspect_media(path: Path, root: Path) -> dict[str, Any]:
    if _looks_like_yymm4_project_json(path):
        raise InternalRenderReviewError("render_is_yymm4_project_json_not_mp4")
    iso_raw = _to_plain(inspect_iso_bmff(path))
    probe_raw = _to_plain(probe_with_ffprobe(path))
    decode_raw = _to_plain(decode_with_ffmpeg(path))
    iso = _compact_iso_result(iso_raw)
    probe = _compact_probe_result(probe_raw)
    decode = _compact_decode_result(decode_raw)
    media = _media_summary(probe_raw)
    checks = {
        "not_yymm4_project_json": True,
        "iso_bmff_structure_pass": _result_passed(iso_raw, kind="iso"),
        "ffprobe_pass": _result_passed(probe_raw, kind="probe"),
        "decode_smoke_pass": _result_passed(decode_raw, kind="decode"),
        "positive_duration": _positive_number(media.get("duration_seconds")),
        "stream_count_positive": int(media.get("stream_count") or 0) > 0,
    }
    checks["media_validation_pass"] = all(checks.values())
    return {
        "repo_relative_path": _repo_relative(path, root),
        "sha256": _sha256(path),
        "size_bytes": path.stat().st_size,
        "iso_bmff": iso,
        "probe": probe,
        "decode": decode,
        "media": media,
        "checks": checks,
        "evidence_grade": "verified",
    }


def _compact_iso_result(value: Any) -> dict[str, Any]:
    data = _mapping(value)
    boxes = data.get("top_level_boxes", data.get("boxes", []))
    box_types = _list(data.get("top_level_box_types")) or _box_types(boxes)
    ftyp = _mapping(data.get("ftyp"))
    mvhd = _mapping(data.get("mvhd"))
    return {
        "status": data.get("status", "passed" if _result_passed(data, kind="iso") else "failed"),
        "box_types": box_types,
        "has_ftyp": bool(data.get("has_ftyp", "ftyp" in box_types)),
        "has_moov": bool(data.get("has_moov", "moov" in box_types)),
        "has_mdat": bool(data.get("has_mdat", "mdat" in box_types)),
        "major_brand": ftyp.get("major_brand", data.get("major_brand")),
        "compatible_brands": ftyp.get(
            "compatible_brands", data.get("compatible_brands")
        ),
        "duration_seconds": mvhd.get(
            "duration_seconds", data.get("duration_seconds")
        ),
        "misnamed_yymm4_project_json": bool(
            data.get(
                "is_yymm4_project_json",
                data.get("misnamed_yymm4_project_json", False),
            )
        ),
    }


def _compact_probe_result(value: Any) -> dict[str, Any]:
    data = _mapping(value)
    tool = _mapping(data.get("tool"))
    return {
        "status": data.get(
            "status", "passed" if _result_passed(data, kind="probe") else "failed"
        ),
        "tool": tool.get("name", data.get("tool_name", "ffprobe")),
        "tool_version": tool.get(
            "version", data.get("tool_version", data.get("version"))
        ),
        "exit_code": data.get("exit_code", data.get("returncode", 0)),
        "probe_score": _nested_first(data, ("format", "probe_score")),
    }


def _compact_decode_result(value: Any) -> dict[str, Any]:
    data = _mapping(value)
    tool = _mapping(data.get("tool"))
    return {
        "status": data.get(
            "status", "passed" if _result_passed(data, kind="decode") else "failed"
        ),
        "tool": tool.get("name", data.get("tool_name", "ffmpeg")),
        "tool_version": tool.get(
            "version", data.get("tool_version", data.get("version"))
        ),
        "exit_code": data.get("exit_code", data.get("returncode", 0)),
        "decode_target": "null_output",
        "decoded_frames": data.get("decoded_frames", data.get("frame_count")),
        "scope": data.get("scope"),
        "source_unchanged": data.get("source_unchanged"),
    }


def _media_summary(value: Any) -> dict[str, Any]:
    data = _mapping(value)
    nested = _mapping(data.get("metadata", data.get("probe", data)))
    format_data = _mapping(nested.get("format", data.get("format", {})))
    streams = _list(nested.get("streams", data.get("streams", [])))
    if not streams and isinstance(data.get("stream_summaries"), list):
        streams = _list(data["stream_summaries"])
    video = next(
        (_mapping(item) for item in streams if _mapping(item).get("codec_type") == "video"),
        {},
    )
    audio = next(
        (_mapping(item) for item in streams if _mapping(item).get("codec_type") == "audio"),
        {},
    )
    tags = _mapping(format_data.get("tags"))
    direct = _mapping(data.get("media", data.get("summary", {})))
    fps = (
        direct.get("fps")
        or video.get("fps")
        or video.get("avg_frame_rate")
        or video.get("r_frame_rate")
    )
    return {
        "container": direct.get("container")
        or format_data.get("format_name")
        or data.get("container"),
        "brands": direct.get("brands")
        or format_data.get("compatible_brands")
        or tags.get("compatible_brands")
        or data.get("brands"),
        "major_brand": direct.get("major_brand")
        or format_data.get("major_brand")
        or tags.get("major_brand")
        or data.get("major_brand"),
        "video_codec": direct.get("video_codec")
        or video.get("codec_name")
        or data.get("video_codec"),
        "audio_codec": direct.get("audio_codec")
        or audio.get("codec_name")
        or data.get("audio_codec"),
        "width": _int_or_none(direct.get("width") or video.get("width") or data.get("width")),
        "height": _int_or_none(
            direct.get("height") or video.get("height") or data.get("height")
        ),
        "fps": _fps_value(fps),
        "duration_seconds": _float_or_none(
            direct.get("duration_seconds")
            or format_data.get("duration_seconds")
            or format_data.get("duration")
            or data.get("duration_seconds")
        ),
        "stream_count": _int_or_none(
            direct.get("stream_count")
            or format_data.get("nb_streams")
            or data.get("stream_count")
            or len(streams)
        ),
        "overall_bitrate_bps": _int_or_none(
            direct.get("overall_bitrate_bps")
            or format_data.get("bit_rate_bps")
            or format_data.get("bit_rate")
            or data.get("bitrate")
        ),
        "video_bitrate_bps": _int_or_none(
            direct.get("video_bitrate_bps")
            or video.get("bit_rate_bps")
            or video.get("bit_rate")
        ),
        "audio_bitrate_bps": _int_or_none(
            direct.get("audio_bitrate_bps")
            or audio.get("bit_rate_bps")
            or audio.get("bit_rate")
        ),
    }


def _result_passed(value: Any, *, kind: str) -> bool:
    data = _mapping(value)
    status = str(data.get("status", "")).casefold()
    if status in {"passed", "pass", "success", "valid", "decoded", "available"}:
        return True
    if status in {"failed", "error", "invalid", "unavailable", "skipped"}:
        return False
    if data.get("success") is True or data.get("valid") is True:
        return True
    return_code = data.get("exit_code", data.get("returncode"))
    if kind in {"probe", "decode"} and return_code == 0:
        return True
    if kind == "probe":
        nested = _mapping(data.get("metadata", data.get("probe", data)))
        return bool(nested.get("format")) and bool(nested.get("streams"))
    if kind == "iso":
        boxes = _list(data.get("top_level_box_types")) or _box_types(
            data.get("top_level_boxes", data.get("boxes", []))
        )
        return {"ftyp", "moov", "mdat"}.issubset(set(boxes))
    return False


def _validate_operator_result(result: dict[str, Any]) -> None:
    if result.get("status") != "success":
        raise InternalRenderReviewError("OPERATOR_RESULT_NOT_SUCCESS")
    if result.get("failed_checks") != []:
        raise InternalRenderReviewError("OPERATOR_RESULT_HAS_FAILED_CHECKS")
    verified = _mapping(result.get("independently_verified"))
    if verified.get("project_structural_pass") is not True:
        raise InternalRenderReviewError("OPERATOR_PROJECT_NOT_STRUCTURALLY_PASSED")
    if verified.get("render_exists") is not True:
        raise InternalRenderReviewError("OPERATOR_RENDER_NOT_REPORTED")


def _validate_freshness(
    *,
    project_path: Path,
    render_path: Path,
    batch_not_before: datetime,
    collected_at: datetime,
) -> dict[str, Any]:
    project_mtime = datetime.fromtimestamp(project_path.stat().st_mtime, timezone.utc)
    render_mtime = datetime.fromtimestamp(render_path.stat().st_mtime, timezone.utc)
    checks = {
        "project_not_before_batch": project_mtime >= batch_not_before,
        "render_not_before_batch": render_mtime >= batch_not_before,
        "project_not_after_collection": project_mtime <= collected_at,
        "render_not_after_collection": render_mtime <= collected_at,
    }
    if not all(checks.values()):
        raise InternalRenderReviewError(
            "OPERATOR_BATCH_FRESHNESS_FAILED:"
            + ",".join(name for name, passed in checks.items() if not passed)
        )
    return checks


def _source_snapshot(pilot: Path, root: Path) -> dict[str, str]:
    names = (
        "source_bundle_manifest.json",
        "source_claim_ledger.json",
        "canonical_script.json",
        "canonical_yymm4.csv",
        DERIVED_CSV_FILENAME,
        ASSET_RELATIVE_PATH.as_posix(),
    )
    return {
        _repo_relative(pilot / name, root): _sha256(pilot / name) for name in names
    }


def _audit_review_files(pilot: Path) -> None:
    missing = [name for name in REVIEW_FILES if not (pilot / name).is_file()]
    if missing:
        raise InternalRenderReviewError("REVIEW_FILES_MISSING:" + ",".join(missing))
    for name in REVIEW_FILES:
        text = (pilot / name).read_text(encoding="utf-8")
        for pattern in _PRIVATE_PATH_PATTERNS:
            if pattern.search(text):
                raise InternalRenderReviewError(f"PRIVATE_PATH_IN_TRACKED_REVIEW:{name}")
    sheet = (pilot / "operator_review_sheet.md").read_text(encoding="utf-8")
    if len(re.findall(r"(?m)^\d+\. ", sheet)) > 5:
        raise InternalRenderReviewError("OPERATOR_REVIEW_QUESTION_LIMIT_EXCEEDED")
    limitations = (pilot / "limitations.md").read_text(encoding="utf-8")
    if len(re.findall(r"(?m)^\| D\d+ \|", limitations)) > 3:
        raise InternalRenderReviewError("QUALITY_DEBT_LIMIT_EXCEEDED")


def _looks_like_yymm4_project_json(path: Path) -> bool:
    with path.open("rb") as handle:
        prefix = handle.read(65536)
    text = prefix.decode("utf-8-sig", errors="ignore").lstrip()
    return text.startswith("{") and '"FilePath"' in text


def _verify_file_identity(
    path: Path,
    *,
    expected_sha256: str | None,
    expected_size: int | None = None,
) -> None:
    if not path.is_file():
        raise InternalRenderReviewError(f"REQUIRED_LOCAL_FILE_MISSING:{path.name}")
    if expected_size is not None and path.stat().st_size != expected_size:
        raise InternalRenderReviewError(f"FILE_SIZE_MISMATCH:{path.name}")
    if expected_sha256 is not None and _sha256(path) != expected_sha256.upper():
        raise InternalRenderReviewError(f"FILE_SHA256_MISMATCH:{path.name}")


def _resolve_repo_root(pilot: Path, repo_root: str | Path | None) -> Path:
    if repo_root is not None:
        root = Path(repo_root).resolve()
        pilot.relative_to(root)
        return root
    for candidate in (pilot, *pilot.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise InternalRenderReviewError("REPO_ROOT_NOT_FOUND")


def _repo_relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _read_csv_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [tuple(row) for row in csv.reader(handle) if row]
    if any(len(row) != 2 for row in rows):
        raise InternalRenderReviewError(f"CSV_NOT_TWO_COLUMN:{path.name}")
    return [(row[0], row[1]) for row in rows]


def _required_bytes(path: Path) -> bytes:
    if not path.is_file():
        raise InternalRenderReviewError(f"REQUIRED_LOCAL_FILE_MISSING:{path.name}")
    return path.read_bytes()


def _parse_utf8_json(raw: bytes, path: Path) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InternalRenderReviewError(f"UTF8_JSON_PARSE_FAILED:{path.name}") from exc
    if not isinstance(value, dict):
        raise InternalRenderReviewError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return value


def _load_json(path: Path) -> dict[str, Any]:
    return _parse_utf8_json(path.read_bytes(), path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, separators=(",", ": "))
        + "\n",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def _required_string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise InternalRenderReviewError(f"REQUIRED_STRING_MISSING:{key}")
    return value


def _required_upper_hex(data: Mapping[str, Any], key: str) -> str:
    value = _required_string(data, key).upper()
    if not re.fullmatch(r"[0-9A-F]{64}", value):
        raise InternalRenderReviewError(f"INVALID_SHA256:{key}")
    return value


def _required_int(data: Mapping[str, Any], key: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise InternalRenderReviewError(f"REQUIRED_INTEGER_MISSING:{key}")
    return value


def _parse_utc(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InternalRenderReviewError(f"INVALID_UTC_TIMESTAMP:{field}") from exc
    if parsed.tzinfo is None:
        raise InternalRenderReviewError(f"UTC_TIMESTAMP_REQUIRES_OFFSET:{field}")
    return parsed.astimezone(timezone.utc)


def _to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return _to_plain(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _box_types(value: Any) -> list[str]:
    rows = _list(value)
    result: list[str] = []
    for item in rows:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, Mapping):
            box_type = item.get("type", item.get("box_type"))
            if box_type:
                result.append(str(box_type))
    return result


def _nested_first(data: Mapping[str, Any], path: tuple[str, str]) -> Any:
    nested = data.get(path[0])
    return nested.get(path[1]) if isinstance(nested, Mapping) else None


def _positive_number(value: Any) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _fps_value(value: Any) -> float | None:
    if isinstance(value, str) and "/" in value:
        numerator, denominator = value.split("/", 1)
        try:
            return round(float(numerator) / float(denominator), 6)
        except (ValueError, ZeroDivisionError):
            return None
    return _float_or_none(value)


__all__ = [
    "EXPECTED_PROXY_SHA256",
    "EXPECTED_PROXY_SIZE_BYTES",
    "InternalRenderReviewError",
    "PROXY_FILENAME",
    "REVIEW_FILES",
    "build_internal_render_review",
]

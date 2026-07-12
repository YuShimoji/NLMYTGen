from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import src.pipeline.internal_render_review as review_module
from src.pipeline.internal_render_review import (
    InternalRenderReviewError,
    REVIEW_FILES,
    build_internal_render_review,
)
from src.pipeline.verified_local_evidence_input_pilot import (
    DERIVED_CSV_FILENAME,
    LOCAL_PROJECT_FILENAME,
    build_verified_local_evidence_input_pilot,
    generate_verified_local_evidence_project,
)
from src.pipeline.ymmp_patch import save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / "production_pilots/yukkuri_newsroom_content_spine_002"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [(row[0], row[1]) for row in csv.reader(handle) if row]


def test_yymm4_signature_check_reads_only_a_bounded_prefix() -> None:
    class GuardedReader(io.BytesIO):
        requested_sizes: list[int]

        def __init__(self, initial_bytes: bytes) -> None:
            super().__init__(initial_bytes)
            self.requested_sizes = []

        def read(self, size: int = -1) -> bytes:
            self.requested_sizes.append(size)
            if size < 0 or size > 65536:
                raise AssertionError("signature check attempted an unbounded read")
            return super().read(size)

    class GuardedPath:
        def __init__(self) -> None:
            self.reader = GuardedReader(
                b'\xef\xbb\xbf  {"FilePath":"misnamed.local.ymmp","Timelines":[]}'
                + (b" " * 70000)
            )

        def open(self, mode: str) -> GuardedReader:
            assert mode == "rb"
            return self.reader

    path = GuardedPath()
    assert review_module._looks_like_yymm4_project_json(path) is True
    assert path.reader.requested_sizes == [65536]


def _write_import_base(path: Path, rows: list[tuple[str, str]]) -> None:
    voices = [
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": character,
            "Serif": text,
            "Frame": index * 360,
            "Length": 300,
            "Layer": index % 2,
            "Group": 0,
            "IsLocked": False,
            "IsHidden": False,
            "VoiceCache": {"test_marker": f"voice-{index + 1}"},
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(path.resolve()),
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "ID": "internal-render-review-test",
                "Name": "メイン",
                "VideoInfo": {
                    "FPS": 60,
                    "Hz": 48000,
                    "Width": 1920,
                    "Height": 1080,
                },
                "VerticalLine": {"IsEnabled": False, "StartFrame": 0},
                "Items": voices,
                "LayerSettings": {"Items": []},
                "CurrentFrame": 0,
                "Length": 3180,
                "MaxLayer": 1,
            }
        ],
        "Characters": [],
    }
    save_ymmp(project, path)


def _fake_iso(path: Path) -> dict:
    return {
        "status": "passed",
        "error_code": None,
        "failed_checks": [],
        "is_yymm4_project_json": False,
        "file_size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "top_level_boxes": [
            {"type": "ftyp", "offset": 0, "size": 32, "header_size": 8},
            {"type": "mdat", "offset": 32, "size": 16, "header_size": 8},
            {"type": "moov", "offset": 48, "size": 16, "header_size": 8},
        ],
        "top_level_box_types": ["ftyp", "mdat", "moov"],
        "ftyp": {
            "major_brand": "isom",
            "minor_version": 512,
            "compatible_brands": ["isom", "iso2", "avc1", "mp41"],
        },
        "mvhd": {
            "timescale": 1000,
            "duration_units": 59383,
            "duration_seconds": 59.383,
        },
        "checks": {"required_top_level_boxes": True},
    }


def _fake_probe(path: Path) -> dict:
    proxy = ".proxy." in path.name
    video_bitrate = 800_000 if proxy else 240_000_480
    overall_bitrate = 980_000 if proxy else 240_185_851
    return {
        "status": "passed",
        "error_code": None,
        "tool": {"name": "ffprobe", "version": "8.0.1"},
        "format": {
            "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
            "format_long_name": "QuickTime / MOV",
            "duration_seconds": 59.383,
            "size_bytes": path.stat().st_size,
            "bit_rate_bps": overall_bitrate,
            "probe_score": 100,
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
        },
        "streams": [
            {
                "index": 0,
                "codec_name": "h264",
                "codec_type": "video",
                "profile": "Main",
                "width": 1920,
                "height": 1080,
                "fps": 60.0,
                "duration_seconds": 59.383,
                "bit_rate_bps": video_bitrate,
                "frame_count": 3563,
            },
            {
                "index": 1,
                "codec_name": "aac",
                "codec_type": "audio",
                "profile": "LC",
                "sample_rate": 48000,
                "channels": 2,
                "duration_seconds": 59.383,
                "bit_rate_bps": 171_024,
            },
        ],
        "stream_count": 2,
        "stderr_summary": "",
    }


def _fake_decode(path: Path) -> dict:
    digest = _sha256(path)
    return {
        "status": "passed",
        "error_code": None,
        "tool": {"name": "ffmpeg", "version": "8.0.1"},
        "scope": "full_file",
        "requested_seconds": None,
        "exit_code": 0,
        "elapsed_seconds": 0.01,
        "stderr_summary": "",
        "source_sha256_before": digest,
        "source_sha256_after": digest,
        "source_unchanged": True,
    }


def _prepare_pilot(tmp_path: Path) -> tuple[Path, Path, Path, bytes]:
    pilot = tmp_path / "verified_local_evidence_input_pilot"
    build_verified_local_evidence_input_pilot(
        package_dir=PACKAGE,
        output_dir=pilot,
    )
    local = pilot / "local_outputs"
    import_base = local / "episode_002_verified_local_evidence_import_base.local.ymmp"
    import_base.parent.mkdir(parents=True, exist_ok=True)
    _write_import_base(import_base, _rows(pilot / DERIVED_CSV_FILENAME))
    generate_verified_local_evidence_project(
        pilot_dir=pilot,
        source_ymmp=import_base,
    )
    project = local / LOCAL_PROJECT_FILENAME
    render = local / "episode_002_verified_local_evidence_internal_review.mp4"
    proxy = local / "episode_002_verified_local_evidence_internal_review.proxy.mp4"
    render.write_bytes(b"test-original-mp4-evidence")
    proxy.write_bytes(b"test-review-proxy")

    project_mtime = datetime.fromtimestamp(project.stat().st_mtime, timezone.utc)
    render_mtime = datetime.fromtimestamp(render.stat().st_mtime, timezone.utc)
    batch_start = min(project_mtime, render_mtime) - timedelta(minutes=1)
    collected = max(project_mtime, render_mtime) + timedelta(minutes=1)
    result = {
        "schema_version": "verified_local_evidence_operator_result.v1",
        "status": "success",
        "collected_at_utc": collected.isoformat(),
        "batch_not_before_utc": batch_start.isoformat(),
        "operator_reported": {
            "manual_batch_completed_before_collection": True,
            "no_unexpected_mapping_character_or_parse_error": True,
            "yymm4_product_version": "4.54.0.1+test",
            "profile_observation_version": "4.53.0.9",
            "profile_version_match": False,
        },
        "independently_verified": {
            "project_structural_pass": True,
            "project_sha256": _sha256(project),
            "render_exists": True,
            "render_size_bytes": render.stat().st_size,
            "render_sha256": _sha256(render),
            "render_mp4_signature_present": True,
        },
        "files": {
            "project": project.name,
            "render": render.name,
            "operator_result": "operator_result.json",
        },
        "failed_checks": [],
        "evidence_boundary": {
            "internal_review_only": True,
            "production_ymmp": False,
            "rights_or_public_approval": False,
            "upload_or_publication": False,
        },
    }
    operator_result = local / "operator_result.json"
    operator_result.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return pilot, render, proxy, operator_result.read_bytes()


def test_builds_deterministic_sanitized_review_package_without_mutating_sources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot, _render, proxy, operator_result_bytes = _prepare_pilot(tmp_path)
    monkeypatch.setattr(review_module, "inspect_iso_bmff", _fake_iso)
    monkeypatch.setattr(review_module, "probe_with_ffprobe", _fake_probe)
    monkeypatch.setattr(review_module, "decode_with_ffmpeg", _fake_decode)

    source_files = [
        pilot / "source_bundle_manifest.json",
        pilot / "source_claim_ledger.json",
        pilot / "canonical_script.json",
        pilot / "canonical_yymm4.csv",
        pilot / DERIVED_CSV_FILENAME,
        pilot / "assets/internal_review_placeholder.png",
    ]
    source_before = {path.name: _sha256(path) for path in source_files}
    result = build_internal_render_review(
        pilot,
        repo_root=tmp_path,
        expected_proxy_sha256=_sha256(proxy),
        expected_proxy_size_bytes=proxy.stat().st_size,
        operator_output_setting_note="MPEG（operator観測）",
    )
    first_hashes = {name: _sha256(pilot / name) for name in REVIEW_FILES}
    build_internal_render_review(
        pilot,
        repo_root=tmp_path,
        expected_proxy_sha256=_sha256(proxy),
        expected_proxy_size_bytes=proxy.stat().st_size,
        operator_output_setting_note="MPEG（operator観測）",
    )
    second_hashes = {name: _sha256(pilot / name) for name in REVIEW_FILES}

    assert result["status"] == "media_validated_internal_review_ready"
    assert first_hashes == second_hashes
    assert (pilot / "local_outputs/operator_result.json").read_bytes() == operator_result_bytes
    assert {path.name: _sha256(path) for path in source_files} == source_before

    manifest = json.loads(
        (pilot / "internal_review_manifest.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (pilot / "render_validation_readback.json").read_text(encoding="utf-8")
    )
    trace = json.loads(
        (pilot / "source_to_output_traceability.json").read_text(encoding="utf-8")
    )
    correction = json.loads(
        (pilot / "operator_batch_correction_report.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "media_validated"
    assert validation["status"] == "passed"
    assert validation["original_render"]["checks"]["decode_smoke_pass"] is True
    assert validation["review_proxy"]["checks"]["decode_smoke_pass"] is True
    assert trace["source_to_project_traceability"] == "9_of_9_verified"
    assert len(trace["cues"]) == 9
    assert correction["json_transport"] == (
        "python_written_utf8_file_read_by_powershell_explicit_utf8"
    )
    assert correction["operator_environment_observation"][
        "output_setting_note_is_machine_verified_codec"
    ] is False

    combined = "\n".join(
        (pilot / name).read_text(encoding="utf-8") for name in REVIEW_FILES
    )
    assert str(tmp_path) not in combined
    assert "file://" not in combined.casefold()
    sheet = (pilot / "operator_review_sheet.md").read_text(encoding="utf-8")
    assert sum(line[:2] in {"1.", "2.", "3.", "4.", "5."} for line in sheet.splitlines()) == 5
    limitations = (pilot / "limitations.md").read_text(encoding="utf-8")
    assert limitations.count("| D1 |") == 1
    assert limitations.count("| D2 |") == 1
    assert limitations.count("| D3 |") == 1


def test_rejects_project_json_masquerading_as_render_before_media_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot, render, proxy, _operator_result_bytes = _prepare_pilot(tmp_path)
    render.write_text(
        '\ufeff  {"FilePath":"misnamed.local.ymmp","Timelines":[]}',
        encoding="utf-8",
    )
    result_path = pilot / "local_outputs/operator_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result["independently_verified"]["render_sha256"] = _sha256(render)
    result["independently_verified"]["render_size_bytes"] = render.stat().st_size
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(review_module, "inspect_iso_bmff", _fake_iso)
    monkeypatch.setattr(review_module, "probe_with_ffprobe", _fake_probe)
    monkeypatch.setattr(review_module, "decode_with_ffmpeg", _fake_decode)

    with pytest.raises(
        InternalRenderReviewError,
        match="render_is_yymm4_project_json_not_mp4",
    ):
        build_internal_render_review(
            pilot,
            repo_root=tmp_path,
            expected_proxy_sha256=_sha256(proxy),
            expected_proxy_size_bytes=proxy.stat().st_size,
        )

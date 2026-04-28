"""Production session manifest / handoff sheet の契約テスト。"""

from __future__ import annotations

import json

from src.cli.main import main
from src.pipeline.session_manifest import build_session_manifest


def test_minimal_manifest_marks_missing_artifacts_not_recorded() -> None:
    manifest = build_session_manifest(video_id="video-001", paths={})

    assert manifest["video_id"] == "video-001"
    assert manifest["paths"]["csv"]["status"] == "not_recorded"
    assert manifest["paths"]["thumbnail_design"]["status"] == "not_recorded"
    assert manifest["csv"]["status"] == "not_recorded"
    assert manifest["script_diagnostics"]["status"] == "not_recorded"
    assert manifest["ir_validation"]["status"] == "not_recorded"
    assert manifest["apply_production"]["status"] == "not_recorded"
    assert manifest["manual_acceptance"]["subtitle_check"]["status"] == "manual_pending"
    assert manifest["manual_acceptance"]["ymm4_composition"]["status"] == "manual_pending"
    assert manifest["manual_acceptance"]["thumbnail_check"]["status"] == "manual_pending"
    assert manifest["next_action"] == "Build CSV and record the output path."


def test_manifest_summarizes_csv_diagnostics_validate_and_apply_json(tmp_path) -> None:
    csv_path = tmp_path / "video.csv"
    csv_path.write_text(
        "れいむ,今日はどうするの？\n"
        "まりさ,不動産DXを解説するぜ。\n"
        "れいむ,なるほど。\n",
        encoding="utf-8",
    )
    diagnostics_path = tmp_path / "diagnostics.json"
    diagnostics_path.write_text(
        json.dumps({
            "diagnostics": [
                {"severity": "warning", "code": "NLM_STYLE_MARKER"},
                {"severity": "error", "code": "SPEAKER_MAP_STRICT"},
            ],
        }),
        encoding="utf-8",
    )
    validate_path = tmp_path / "validate.json"
    validate_path.write_text(
        json.dumps({
            "command": "validate-ir",
            "success": True,
            "error_count": 0,
            "warning_count": 2,
            "utterance_count": 3,
            "used_skit_group_motion_labels": ["nod"],
        }),
        encoding="utf-8",
    )
    apply_path = tmp_path / "apply.json"
    apply_path.write_text(
        json.dumps({
            "command": "apply-production",
            "success": True,
            "dry_run": False,
            "output": str(tmp_path / "patched.ymmp"),
            "warnings": ["example warning"],
            "summary": {
                "warning_count": 1,
                "skit_group_placements": 5,
                "skit_group_item_insertions": 9,
            },
        }),
        encoding="utf-8",
    )
    ir_path = tmp_path / "production_ir.json"
    ir_path.write_text("{}", encoding="utf-8")

    manifest = build_session_manifest(
        video_id="video-002",
        paths={
            "csv": str(csv_path),
            "script_diagnostics": str(diagnostics_path),
            "ir_json": str(ir_path),
            "validate_result": str(validate_path),
            "apply_result": str(apply_path),
            "patched_ymmp": str(tmp_path / "patched.ymmp"),
        },
    )

    assert manifest["csv"]["row_count"] == 3
    assert manifest["csv"]["speaker_count"] == 2
    assert manifest["script_diagnostics"]["error_count"] == 1
    assert manifest["script_diagnostics"]["warning_count"] == 1
    assert manifest["script_diagnostics"]["codes"] == [
        "NLM_STYLE_MARKER",
        "SPEAKER_MAP_STRICT",
    ]
    assert manifest["ir_validation"]["success"] is True
    assert manifest["ir_validation"]["warning_count"] == 2
    assert manifest["apply_production"]["success"] is True
    assert manifest["apply_production"]["dry_run"] is False
    assert manifest["apply_production"]["warning_count"] == 1
    assert manifest["apply_production"]["skit_group_placements"] == 5
    assert manifest["apply_production"]["skit_group_item_insertions"] == 9
    assert manifest["next_action"] == "Open the patched .ymmp in YMM4 and record manual acceptance."


def test_cli_build_session_manifest_json_stdout(capsys) -> None:
    code = main([
        "build-session-manifest",
        "--video-id",
        "video-json",
        "--format",
        "json",
    ])

    assert code == 0
    out = capsys.readouterr().out
    manifest = json.loads(out)
    assert manifest["video_id"] == "video-json"
    assert manifest["paths"]["csv"]["status"] == "not_recorded"
    assert manifest["manual_acceptance"]["thumbnail_check"]["status"] == "manual_pending"


def test_cli_build_session_manifest_markdown_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "handoff.md"

    code = main([
        "build-session-manifest",
        "--video-id",
        "video-md",
        "--format",
        "markdown",
        "-o",
        str(output_path),
    ])

    assert code == 0
    assert "Written:" in capsys.readouterr().out
    text = output_path.read_text(encoding="utf-8")
    assert "# Production Session Manifest — video-md" in text
    assert "## Stage Summary" in text
    assert "## Manual Acceptance" in text
    assert "manual_pending" in text
    assert "next_action" in text

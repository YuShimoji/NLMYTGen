import hashlib
import json
from pathlib import Path

from src.pipeline.background_skit_blueprint import (
    validate_background_skit_blueprint,
)
from src.cli import main as cli_main


def _write_script(tmp_path: Path, line_count: int = 4) -> tuple[Path, str]:
    path = tmp_path / "script.txt"
    text = "\n".join(f"語り手A： line {index}" for index in range(1, line_count + 1))
    path.write_text(text, encoding="utf-8")
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


def _write_ymmp(tmp_path: Path, total_sec: float = 10.0, fps: int = 60) -> Path:
    path = tmp_path / "base.ymmp"
    data = {
        "Timelines": [
            {
                "Items": [
                    {
                        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                        "Frame": 0,
                        "Length": int(total_sec * fps),
                    }
                ]
            }
        ]
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _minimal_blueprint(script_path: Path, script_sha: str, ymmp_path: Path) -> dict:
    return {
        "source_lock": {
            "script_source": str(script_path),
            "script_sha256": script_sha,
            "line_count": 4,
            "ymmp_source": str(ymmp_path),
            "fps": 60,
            "total_duration_formula": "max(Frame + Length) / fps",
            "duration_source": "YMM4 readback",
        },
        "script_diagnostic": {
            "source_line_citations": ["lines 1-4"],
            "ideal_script_delta": [
                {
                    "line_start": 1,
                    "line_end": 4,
                    "change": "keep minimal proof script connected",
                }
            ],
        },
        "duration_model": {
            "total_duration_sec": 10.0,
            "duration_source": "YMM4 readback",
            "confidence": "confirmed",
        },
        "blocks": [
            {
                "block_id": "RE-01",
                "line_start": 1,
                "line_end": 4,
                "range_basis": "minimal source covers the full proof script",
                "block_start_sec": 0.0,
                "block_end_sec": 10.0,
                "skit_active_windows": [{"start_sec": 0.0, "end_sec": 5.0}],
                "rest_windows": [{"start_sec": 5.0, "end_sec": 10.0}],
                "visual_state": "consumer_search",
                "cast": ["consumer"],
                "props": ["property_card"],
                "proof_path": "validator readback",
                "negative_rationale": "not a narrator reaction cue",
            }
        ],
        "asset_control_matrix": {
            "consumer": {
                "availability": "missing",
                "owner": "assistant-spec",
                "control_needed": ["hold"],
                "control_route": "new template",
                "readback_check": ["asset id"],
            },
            "property_card": {
                "availability": "placeholder",
                "owner": "assistant-layout",
                "control_needed": ["show"],
                "control_route": "overlay",
                "readback_check": ["duration"],
            },
        },
        "density_thresholds": {
            "minimum_active_visual_coverage_pct": 50,
            "maximum_unexplained_gap_sec": 0,
            "visual_states_per_min_range": [1, 10],
            "maximum_repeated_motion_ratio": 1,
        },
        "density_audit": {
            "active_visual_coverage_pct": 50,
            "unexplained_empty_duration_sec": 0,
            "longest_unexplained_gap_sec": 0,
            "visual_states_per_min": 6,
        },
        "blockers": [],
    }


def _real_estate_broad_blueprint(script_path: Path, script_sha: str, ymmp_path: Path) -> dict:
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["source_lock"]["line_count"] = 152
    blueprint["duration_model"]["total_duration_sec"] = 100.0
    blueprint["blocks"] = [
        {
            "block_id": "RE-01",
            "line_start": 1,
            "line_end": 82,
            "range_basis": "pre-RE07 source-backed block",
            "block_start_sec": 0.0,
            "block_end_sec": 50.0,
            "skit_active_windows": [{"start_sec": 0.0, "end_sec": 25.0}],
            "rest_windows": [{"start_sec": 25.0, "end_sec": 50.0}],
            "visual_state": "pre_re07",
            "cast": ["consumer"],
            "props": ["property_card"],
            "proof_path": "validator readback",
            "negative_rationale": "not a narrator reaction cue",
        },
        {
            "block_id": "RE-07",
            "line_start": 83,
            "line_end": 152,
            "range_basis": "AI後の人間価値 parent block",
            "block_start_sec": 50.0,
            "block_end_sec": 100.0,
            "skit_active_windows": [{"start_sec": 50.0, "end_sec": 75.0}],
            "rest_windows": [{"start_sec": 75.0, "end_sec": 100.0}],
            "visual_state": "ai_human_value",
            "cast": ["consumer"],
            "props": ["property_card"],
            "proof_path": "validator readback",
            "negative_rationale": "not a line-cue exit or jump",
        },
    ]
    blueprint["density_audit"] = {
        "active_visual_coverage_pct": 50,
        "unexplained_empty_duration_sec": 0,
        "longest_unexplained_gap_sec": 0,
        "visual_states_per_min": 1.2,
    }
    blueprint["density_thresholds"]["visual_states_per_min_range"] = [1, 2]
    blueprint["blockers"] = [
        "SCRIPT_BLOCKED_RE07_TOO_BROAD: lines 83-152 must be split",
        "ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING: consumer/gatekeeper/curator missing",
    ]
    return blueprint


def _re07_subbeats() -> list[dict]:
    return [
        {
            "id": "RE-07A",
            "line_start": 83,
            "line_end": 102,
            "csv_row_start": 186,
            "csv_row_end": 226,
            "voice_index_start": 186,
            "voice_index_end": 226,
            "start_sec": 50.0,
            "end_sec": 65.0,
        },
        {
            "id": "RE-07B",
            "line_start": 103,
            "line_end": 113,
            "csv_row_start": 227,
            "csv_row_end": 252,
            "voice_index_start": 227,
            "voice_index_end": 252,
            "start_sec": 65.0,
            "end_sec": 73.0,
        },
        {
            "id": "RE-07C",
            "line_start": 114,
            "line_end": 129,
            "csv_row_start": 253,
            "csv_row_end": 296,
            "voice_index_start": 253,
            "voice_index_end": 296,
            "start_sec": 73.0,
            "end_sec": 86.0,
        },
        {
            "id": "RE-07D",
            "line_start": 130,
            "line_end": 143,
            "csv_row_start": 297,
            "csv_row_end": 331,
            "voice_index_start": 297,
            "voice_index_end": 331,
            "start_sec": 86.0,
            "end_sec": 96.0,
        },
        {
            "id": "RE-07E",
            "line_start": 144,
            "line_end": 152,
            "csv_row_start": 332,
            "csv_row_end": 352,
            "voice_index_start": 332,
            "voice_index_end": 352,
            "start_sec": 96.0,
            "end_sec": 100.0,
        },
    ]


def _validate(blueprint: dict, script_path: Path, ymmp_path: Path | None) -> object:
    return validate_background_skit_blueprint(
        blueprint,
        script_path=script_path,
        ymmp_path=ymmp_path,
        fps=60,
    )


def test_background_skit_blueprint_passes_minimal_source_backed_artifact(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "passed"
    assert result.errors == []
    assert result.derived_metrics["duration"]["total_duration_sec"] == 10
    assert result.derived_metrics["density"]["active_visual_coverage_pct"] == 50


def test_background_skit_blueprint_rejects_fake_xhigh_style_table(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path, line_count=152)
    ymmp_path = _write_ymmp(tmp_path, total_sec=1049.5333333333333)
    blueprint = {
        "source_lock": {
            "script_source": str(script_path),
            "script_sha256": script_sha,
            "line_count": 152,
            "ymmp_source": str(ymmp_path),
            "fps": 60,
            "total_duration_formula": "scene bible ratio",
            "duration_source": "base ymmp readback",
        },
        "script_diagnostic": {
            "source_line_citations": ["lines 1-150"],
            "ideal_script_delta": ["needs real diagnosis"],
        },
        "duration_model": {"total_duration_sec": 1050, "duration_source": "approx"},
        "blocks": [
            {
                "block_id": "RE-01",
                "line_start": 1,
                "line_end": 12,
                "range_basis": "scene bible ratio",
                "block_start_sec": 0,
                "block_end_sec": 105,
                "skit_active_windows": [],
                "rest_windows": [],
                "visual_state": "consumer_search",
                "cast": ["consumer"],
                "props": ["property_card"],
                "proof_path": "none",
                "negative_rationale": "not line cue",
            }
        ],
        "asset_control_matrix": {},
        "density_thresholds": {},
        "blockers": [],
    }

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("DURATION_MISMATCH" in error for error in result.errors)
    assert any("SCRIPT_LINE_GAP_UNEXPLAINED" in error for error in result.errors)
    assert any("ASSET_CONTROL_UNBOUND" in error for error in result.errors)
    assert any("DENSITY_THRESHOLD_MISSING" in error for error in result.errors)


def test_background_skit_blueprint_rejects_line_count_mismatch(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path, line_count=152)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["source_lock"]["line_count"] = 150

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("SCRIPT_SOURCE_MISMATCH" in error for error in result.errors)


def test_background_skit_blueprint_rejects_total_duration_gap(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["blocks"][0]["block_end_sec"] = 8.0

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("TOTAL_DURATION_COVERAGE_MISMATCH" in error for error in result.errors)


def test_background_skit_blueprint_rejects_active_window_out_of_block(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["blocks"][0]["skit_active_windows"] = [{"start_sec": 9.0, "end_sec": 11.0}]

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("ACTIVE_WINDOW_OUT_OF_BLOCK" in error for error in result.errors)


def test_background_skit_blueprint_rejects_density_mismatch(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["density_audit"]["active_visual_coverage_pct"] = 80

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("DENSITY_AUDIT_MISMATCH" in error for error in result.errors)


def test_background_skit_blueprint_rejects_ungrounded_delivery_template(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint["asset_control_matrix"]["delivery_proxy"] = {
        "availability": "existing",
        "owner": "assistant",
        "control_needed": ["enter"],
        "control_route": "existing template",
        "readback_check": ["group item"],
        "template_name": "delivery_enter_from_left_v1",
    }
    blueprint["blocks"][0]["cast"].append("delivery_proxy")

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "failed"
    assert any("TEMPLATE_REUSE_UNGROUNDED" in error for error in result.errors)


def test_background_skit_blueprint_blocks_without_ymmp_instead_of_faking(tmp_path) -> None:
    script_path, script_sha = _write_script(tmp_path)
    missing_ymmp = tmp_path / "missing.ymmp"
    blueprint = _minimal_blueprint(script_path, script_sha, missing_ymmp)
    blueprint["duration_model"] = {
        "duration_source": "missing",
        "confidence": "blocked",
    }
    blueprint["blocks"] = []
    blueprint["blockers"] = [
        "TIMETABLE_BLOCKED_TIMING_SOURCE_MISSING: base YMM4 project missing"
    ]

    result = _validate(blueprint, script_path, missing_ymmp)

    assert result.status == "blocked"
    assert result.errors == []
    assert any(
        blocker.startswith("TIMETABLE_BLOCKED_TIMING_SOURCE_MISSING")
        for blocker in result.blockers
    )


def test_background_skit_blueprint_keeps_re07_script_blocker_when_gap_report_is_external(
    tmp_path,
) -> None:
    script_path, script_sha = _write_script(tmp_path, line_count=152)
    ymmp_path = _write_ymmp(tmp_path, total_sec=100.0)
    blueprint = _real_estate_broad_blueprint(script_path, script_sha, ymmp_path)
    gap_report_path = tmp_path / "gap_report.json"
    gap_report_path.write_text(
        json.dumps({"re07_subbeats": _re07_subbeats()}),
        encoding="utf-8",
    )

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "blocked"
    assert any(blocker.startswith("SCRIPT_BLOCKED_RE07_TOO_BROAD") for blocker in result.blockers)
    assert result.allowed_next_actions == []
    assert "overlay_only_compact_review" in result.forbidden_next_actions


def test_background_skit_blueprint_resolves_re07_script_blocker_from_blueprint_subbeats(
    tmp_path,
) -> None:
    script_path, script_sha = _write_script(tmp_path, line_count=152)
    ymmp_path = _write_ymmp(tmp_path, total_sec=100.0)
    blueprint = _real_estate_broad_blueprint(script_path, script_sha, ymmp_path)
    blueprint["blocks"][1]["subbeats"] = _re07_subbeats()

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "blocked"
    assert not any(
        blocker.startswith("SCRIPT_BLOCKED_RE07_TOO_BROAD") for blocker in result.blockers
    )
    assert any(blocker.startswith("ASSET_BLOCKED") for blocker in result.blockers)
    assert result.allowed_next_actions == ["overlay_only_compact_review"]
    assert "cast_motion_ir" in result.forbidden_next_actions
    assert result.derived_metrics["resolved_blockers"] == ["SCRIPT_BLOCKED_RE07_TOO_BROAD"]
    assert result.derived_metrics["subbeats"]["re07_authority"] == "blueprint.blocks.RE-07.subbeats"


def test_background_skit_blueprint_resolves_re07_script_blocker_from_row_time_map(
    tmp_path,
) -> None:
    script_path, script_sha = _write_script(tmp_path, line_count=152)
    ymmp_path = _write_ymmp(tmp_path, total_sec=100.0)
    row_time_map_path = tmp_path / "row_time_map.json"
    row_time_map_path.write_text(
        json.dumps({"re07_subbeat_time_map": _re07_subbeats()}),
        encoding="utf-8",
    )
    blueprint = _real_estate_broad_blueprint(script_path, script_sha, ymmp_path)
    blueprint["row_time_map"] = str(row_time_map_path)

    result = _validate(blueprint, script_path, ymmp_path)

    assert result.status == "blocked"
    assert not any(
        blocker.startswith("SCRIPT_BLOCKED_RE07_TOO_BROAD") for blocker in result.blockers
    )
    assert result.allowed_next_actions == ["overlay_only_compact_review"]
    assert result.derived_metrics["subbeats"]["re07_authority"] == (
        "row_time_map.re07_subbeat_time_map"
    )


def test_cli_validate_background_skit_blueprint_outputs_json(tmp_path, capsys) -> None:
    script_path, script_sha = _write_script(tmp_path)
    ymmp_path = _write_ymmp(tmp_path)
    blueprint = _minimal_blueprint(script_path, script_sha, ymmp_path)
    blueprint_path = tmp_path / "blueprint.json"
    blueprint_path.write_text(json.dumps(blueprint), encoding="utf-8")

    exit_code = cli_main.main(
        [
            "validate-background-skit-blueprint",
            str(blueprint_path),
            "--script",
            str(script_path),
            "--ymmp",
            str(ymmp_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["status"] == "passed"
    assert "allowed_next_actions" in payload
    assert "forbidden_next_actions" in payload

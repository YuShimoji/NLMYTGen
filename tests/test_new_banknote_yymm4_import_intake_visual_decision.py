from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

import pytest

from src.pipeline.new_banknote_yymm4_import_intake_visual_decision import (
    ALLOWED_SOURCE_IDS,
    ASSET_MATRIX_FILENAME,
    DEFAULT_PILOT_DIR,
    EXPECTED_ROUTE_IDS,
    HTML_BOARD_FILENAME,
    HTML_READBACK_FILENAME,
    IMPORT_READBACK_FILENAME,
    IMPORT_RECEIPT_FILENAME,
    LOCAL_BATCH_STATE_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RESULT_FILENAME,
    RECOMMENDED_DIRECTION_FILENAME,
    SCENE_PLAN_FILENAME,
    VISUAL_DIRNAME,
    VISUAL_OPTIONS_FILENAME,
    VISUAL_REVIEW_FILENAME,
    YMM4_CONTRACT_FILENAME,
    audit_new_banknote_yymm4_import_observation,
    build_new_banknote_import_visual_decision_packet,
    load_tracked_evidence_snapshot,
    preflight_new_banknote_import_visual_decision_packet,
    render_new_banknote_import_visual_decision_artifacts,
)
from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    APPROVED_FILES,
    EXPECTED_APPROVED_HASHES,
    collect_new_banknote_yymm4_import_result,
)
from src.pipeline.new_banknote_authoritative_script import (
    validate_new_banknote_authoritative_script_package,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
_PRIVATE_OR_EXTERNAL_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/|"
    r"https?://|file://|www\.)"
)


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


class _BoardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self.tags.append(tag)
        for name, value in attrs:
            if name == "href" and value is not None:
                self.hrefs.append(value)


@pytest.fixture
def isolated_pilot(tmp_path: Path) -> Path:
    target = tmp_path / "new_banknote_pilot"
    shutil.copytree(
        DEFAULT_PILOT_DIR,
        target,
        ignore=shutil.ignore_patterns(
            LOCAL_OUTPUT_DIRNAME,
            "README_YMM4_IMPORT_OBSERVATION.md",
            "yymm4_import_*",
            VISUAL_DIRNAME,
        ),
    )
    return target


def _derived_rows(pilot: Path) -> list[tuple[str, str]]:
    with (pilot / "derived_yymm4_import.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        return [tuple(row) for row in csv.reader(handle)]


def _write_success_evidence(pilot: Path) -> tuple[Path, Path, Path]:
    local = pilot / LOCAL_OUTPUT_DIRNAME
    local.mkdir(parents=True, exist_ok=True)
    project_path = (local / LOCAL_PROJECT_FILENAME).resolve()
    result_path = (local / LOCAL_RESULT_FILENAME).resolve()
    batch_path = (local / LOCAL_BATCH_STATE_FILENAME).resolve()
    not_before = datetime.now(timezone.utc) - timedelta(minutes=2)
    product_version = "4.54.0.1+fixture"
    batch_path.write_text(
        json.dumps(
            {
                "schema_version": (
                    "new_banknote_yymm4_import_operator_batch.local.v1"
                ),
                "batch_id": "fixture-batch",
                "batch_not_before_utc": not_before.isoformat(),
                "yymm4_exe": str(local / "fixture-yymm4.exe"),
                "yymm4_product_version": product_version,
                "profile_observation_version": "4.53.0.9",
                "target_project": str(project_path),
                "target_result": str(result_path),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rows = _derived_rows(pilot)
    voices = [
        {
            "$type": (
                "YukkuriMovieMaker.Project.Items.VoiceItem, "
                "YukkuriMovieMaker"
            ),
            "CharacterName": character,
            "Serif": text,
            "Frame": index * 180,
            "Length": 150 + (index % 3) * 10,
            "Layer": index % 2,
            "Group": 0,
            "VoiceCache": {"private_fixture": f"voice-{index + 1}"},
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(project_path),
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "Name": "メイン",
                "VideoInfo": {
                    "FPS": 60,
                    "Hz": 48000,
                    "Width": 1920,
                    "Height": 1080,
                },
                "Items": voices,
                "Length": voices[-1]["Frame"] + voices[-1]["Length"],
            }
        ],
    }
    save_ymmp(project, project_path)
    result = collect_new_banknote_yymm4_import_result(
        pilot_dir=pilot,
        project_path=project_path,
        output_path=result_path,
        not_before_utc=not_before.isoformat(),
        operator_confirmed_no_mapping_error=True,
        yymm4_product_version=product_version,
    )
    assert result["status"] == "success"
    return project_path, result_path, batch_path


def _fingerprints(paths: list[Path]) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def test_read_only_audit_verifies_success_and_preserves_local_bytes(
    isolated_pilot: Path,
) -> None:
    paths = list(_write_success_evidence(isolated_pilot))
    before = _fingerprints(paths)
    snapshot = audit_new_banknote_yymm4_import_observation(isolated_pilot)
    after = _fingerprints(paths)

    assert before == after
    assert snapshot["status"] == "verified_import_observation"
    assert snapshot["operator_result"]["status"] == "success"
    assert snapshot["operator_result"]["failed_checks"] == []
    verified = snapshot["project_verification"]
    assert verified["VoiceItem_count"] == 9
    assert verified["character_counts"] == {
        "ゆっくり霊夢": 3,
        "ゆっくり魔理沙": 6,
    }
    assert verified["exact_text_order"] is True
    assert verified["exact_character_text_order"] is True
    assert verified["missing_count"] == 0
    assert verified["duplicate_count"] == 0
    assert len(verified["voice_timing_summary"]) == 9
    assert _PRIVATE_OR_EXTERNAL_RE.search(
        json.dumps(snapshot, ensure_ascii=False)
    ) is None


def test_audit_fails_closed_on_result_failure(isolated_pilot: Path) -> None:
    _, result_path, _ = _write_success_evidence(isolated_pilot)
    result = _load(result_path)
    result["status"] = "failure"
    result["failed_checks"] = ["fixture_failure"]
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="OPERATOR_RESULT_NOT_SUCCESS"):
        audit_new_banknote_yymm4_import_observation(isolated_pilot)


def test_audit_fails_closed_on_project_text_drift(
    isolated_pilot: Path,
) -> None:
    project_path, _, _ = _write_success_evidence(isolated_pilot)
    project = load_ymmp(project_path)
    project["Timelines"][0]["Items"][0]["Serif"] += " drift"
    save_ymmp(project, project_path)
    with pytest.raises(ValueError, match="PROJECT_TEXT_OR_ORDER_DRIFT"):
        audit_new_banknote_yymm4_import_observation(isolated_pilot)


def test_fixture_build_is_deterministic_and_byte_preserving(
    isolated_pilot: Path,
) -> None:
    paths = list(_write_success_evidence(isolated_pilot))
    before = _fingerprints(paths)
    first = build_new_banknote_import_visual_decision_packet(isolated_pilot)
    second = build_new_banknote_import_visual_decision_packet(isolated_pilot)
    after = _fingerprints(paths)

    assert first["status"] == "passed"
    assert first["artifact_count"] == 17
    assert len(first["changed"]) == 17
    assert second["changed"] == []
    assert before == after
    preflight = preflight_new_banknote_import_visual_decision_packet(
        isolated_pilot
    )
    assert preflight["status"] == "passed"
    assert preflight["failed_checks"] == []


def test_tracked_outputs_match_pure_renderer_and_freeze_script_hashes() -> None:
    snapshot = load_tracked_evidence_snapshot(DEFAULT_PILOT_DIR)
    first = render_new_banknote_import_visual_decision_artifacts(snapshot)
    second = render_new_banknote_import_visual_decision_artifacts(snapshot)
    assert first == second
    assert len(first) == 17
    for relative, expected in first.items():
        assert (DEFAULT_PILOT_DIR / relative).read_bytes() == expected
    assert {
        name: hashlib.sha256((DEFAULT_PILOT_DIR / name).read_bytes()).hexdigest()
        for name in APPROVED_FILES
    } == EXPECTED_APPROVED_HASHES
    authoritative = validate_new_banknote_authoritative_script_package(
        DEFAULT_PILOT_DIR
    )
    assert authoritative["status"] == "passed"
    assert authoritative["checks"]["no_source_bodies"] is True


def test_visual_routes_have_one_recommendation_and_complete_contract() -> None:
    visual = DEFAULT_PILOT_DIR / VISUAL_DIRNAME
    options = _load(visual / VISUAL_OPTIONS_FILENAME)
    routes = options["routes"]
    assert options["route_count"] == 3
    assert [route["route_id"] for route in routes] == EXPECTED_ROUTE_IDS
    assert [route["recommended"] for route in routes] == [True, False, False]
    assert [route["status"] for route in routes] == [
        "RECOMMENDED",
        "OPTION",
        "OPTION",
    ]
    required = {
        "concept",
        "scene_purposes",
        "layout_system",
        "typography_role",
        "color_role_proposal",
        "motion_vocabulary",
        "required_asset_families",
        "rights_risk",
        "factual_or_misleading_risk",
        "ymm4_implementation_weight",
        "validation_evidence",
        "why_it_may_be_rejected",
    }
    assert all(required <= set(route) for route in routes)
    recommended = _load(visual / RECOMMENDED_DIRECTION_FILENAME)
    assert recommended["status"] == "recommended_not_selected"
    assert recommended["implementation_authorized"] is False


def test_route_a_scene_spine_covers_all_cues_and_required_fields() -> None:
    plan = _load(DEFAULT_PILOT_DIR / VISUAL_DIRNAME / SCENE_PLAN_FILENAME)
    assert [scene["scene_id"] for scene in plan["scenes"]] == [
        "S1",
        "S2",
        "S3",
    ]
    assert [len(scene["cue_plans"]) for scene in plan["scenes"]] == [2, 4, 3]
    cue_plans = [cue for scene in plan["scenes"] for cue in scene["cue_plans"]]
    assert [cue["cue_id"] for cue in cue_plans] == [
        f"cue_{index:03d}" for index in range(1, 10)
    ]
    required = {
        "screen_objective",
        "foreground",
        "background",
        "text_overlay",
        "source_backed_factual_boundary",
        "animation",
        "expected_duration_relation_to_actual_voiceitem_timing",
        "placeholder_asset",
        "future_rights_decision",
        "ymm4_item_family_expectation",
    }
    assert all(required <= set(cue) for cue in cue_plans)
    assert {
        source_id for cue in cue_plans for source_id in cue["source_ids"]
    } <= ALLOWED_SOURCE_IDS


def test_html_board_is_self_contained_relative_and_reviewable() -> None:
    visual = DEFAULT_PILOT_DIR / VISUAL_DIRNAME
    board = (visual / HTML_BOARD_FILENAME).read_text(encoding="utf-8")
    parser = _BoardParser()
    parser.feed(board)
    assert {"html", "head", "body", "main"} <= set(parser.tags)
    assert parser.hrefs == [
        "visual_review_sheet.md",
        "recommended_visual_direction.json",
        "../README_YMM4_IMPORT_OBSERVATION.md",
        "../editorial_provenance/README_EDITORIAL_PROVENANCE.md",
    ]
    assert all(
        token in board
        for token in (
            "Route A",
            "Route B",
            "Route C",
            "S1",
            "S2",
            "S3",
            "INTERNAL REVIEW",
            "NON-PRODUCTION",
        )
    )
    assert not any(
        token in board.lower()
        for token in (
            "<script",
            "<link",
            "<img",
            " src=",
            "url(",
            "@import",
        )
    )
    assert _PRIVATE_OR_EXTERNAL_RE.search(board) is None
    readback = _load(visual / HTML_READBACK_FILENAME)
    assert readback["status"] == "passed"
    assert readback["failed_checks"] == []
    assert all(readback["checks"].values())


def test_asset_and_project_boundaries_remain_nonproduction() -> None:
    visual = DEFAULT_PILOT_DIR / VISUAL_DIRNAME
    assets = _load(visual / ASSET_MATRIX_FILENAME)
    assert assets["default_representation"] == "original_abstract_schematic"
    assert assets["official_image_reuse"] is False
    assert assets["external_asset_fetch"] is False
    assert assets["rights_cleared"] is False
    assert all(asset["created_in_this_slice"] is False for asset in assets["assets"])
    contract = _load(visual / YMM4_CONTRACT_FILENAME)
    assert contract["status"] == "not_authorized"
    assert contract["implementation_status"] == "not_started"
    assert contract["authorization"] == {
        "human_route_selection_required": True,
        "diagnostic_project_authorized": False,
        "production_project_authorized": False,
        "render_authorized": False,
        "asset_creation_authorized": False,
    }
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in visual.rglob("*")
        if path.is_file()
    )
    assert "claim_158" not in combined
    assert _PRIVATE_OR_EXTERNAL_RE.search(combined) is None


def test_review_surface_has_only_four_questions() -> None:
    review = (
        DEFAULT_PILOT_DIR / VISUAL_DIRNAME / VISUAL_REVIEW_FILENAME
    ).read_text(encoding="utf-8")
    questions = re.findall(r"(?m)^\d+\. .+$", review)
    assert len(questions) == 4
    assert "A / B / C" in questions[0]


def test_local_evidence_targets_remain_ignored_and_untracked() -> None:
    paths = [
        DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME,
        DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME,
        DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME / LOCAL_BATCH_STATE_FILENAME,
    ]
    relative = [str(path.relative_to(REPO_ROOT)) for path in paths]
    ignored = subprocess.run(
        ["git", "check-ignore", "--", *relative],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert ignored.returncode == 0
    tracked = subprocess.run(
        ["git", "ls-files", "--", *relative],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert tracked.stdout.strip() == ""


def test_import_receipt_keeps_evidence_grades_and_open_gates_explicit() -> None:
    receipt = _load(DEFAULT_PILOT_DIR / IMPORT_RECEIPT_FILENAME)
    assert receipt["status"] == "passed"
    assert receipt["verified_import_contract"]["VoiceItem_count"] == 9
    assert receipt["gate_boundary"] == {
        "csv_import_gate": "passed",
        "audio_editorial_gate": "open",
        "visual_direction_gate": "open",
        "render_gate": "open",
        "production_project": False,
        "rights_or_publication_approval": False,
    }
    assert receipt["local_evidence_disposition"]["local_bytes_preserved"] is True
    assert receipt["local_evidence_disposition"][
        "absolute_runtime_paths_promoted"
    ] is False
    readback = _load(DEFAULT_PILOT_DIR / IMPORT_READBACK_FILENAME)
    assert readback["status"] == "passed"
    assert all(readback["checks"].values())

from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.content_planning_spine import (
    BLOCKED_PUBLIC_ACTIONS,
    REQUIRED_PACKAGE_FILES,
    build_content_spine_package,
    validate_content_spine_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIXTURE = REPO_ROOT / "samples" / "_probe" / "content_spine" / "rss_like_topic_candidates_sample.json"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_content_spine_package_builds_required_review_files(tmp_path) -> None:
    package_dir = tmp_path / "content_spine"

    readback = build_content_spine_package(
        source_path=SOURCE_FIXTURE,
        output_dir=package_dir,
        artifact_id="test_content_spine",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_PACKAGE_FILES:
        assert (package_dir / filename).exists(), filename

    manifest = _load(package_dir / "MANIFEST.json")
    topics = _load(package_dir / "topic_candidates.json")
    dashboard = _load(package_dir / "dashboard_status.json")
    saved_readback = _load(package_dir / "content_spine_readback.json")

    assert manifest["artifact_kind"] == "content-planning-dashboard-spine"
    assert manifest["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert topics["candidates"][0]["candidate_score"] == 88
    assert topics["candidates"][0]["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert topics["candidates"][0]["yukkuri_profile"]["explainer_role"] == "まりさ"
    assert topics["candidates"][0]["thumbnail_profile"]["short_text_candidates"]
    assert dashboard["readiness"]["episode_package_status"] == "local_reviewable"
    assert dashboard["readiness"]["ymm4_readiness"] == "planning_ready_csv_ir_not_generated"
    assert dashboard["readiness"]["thumbnail_readiness"] == "brief_only_no_image"
    assert dashboard["public_actions_blocked"] == list(BLOCKED_PUBLIC_ACTIONS)
    assert saved_readback["status"] == "passed"
    assert saved_readback["checks"]["all_required_files_present"] is True


def test_content_spine_validation_catches_missing_dashboard(tmp_path) -> None:
    package_dir = tmp_path / "content_spine"
    build_content_spine_package(
        source_path=SOURCE_FIXTURE,
        output_dir=package_dir,
        artifact_id="test_content_spine",
    )
    (package_dir / "dashboard_status.json").unlink()

    readback = validate_content_spine_package(package_dir)

    assert readback["status"] == "failed"
    assert "missing_file:dashboard_status.json" in readback["failed_checks"]
    assert "dashboard_status_json_invalid" in readback["failed_checks"]


def test_cli_build_content_spine_json_output(tmp_path, capsys) -> None:
    package_dir = tmp_path / "content_spine_cli"

    code = main([
        "build-content-spine",
        "--source",
        str(SOURCE_FIXTURE),
        "--output",
        str(package_dir),
        "--artifact-id",
        "test_cli_content_spine",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert (package_dir / "dashboard_preview.md").exists()


def test_generated_content_spine_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    package_dir = tmp_path / "content_spine"
    build_content_spine_package(
        source_path=SOURCE_FIXTURE,
        output_dir=package_dir,
        artifact_id="test_content_spine",
    )

    for path in package_dir.iterdir():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)

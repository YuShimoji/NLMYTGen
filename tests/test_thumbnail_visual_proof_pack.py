from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.thumbnail_visual_proof_pack import (
    REQUIRED_THUMBNAIL_PROOF_FILES,
    build_thumbnail_visual_proof_pack,
    validate_thumbnail_visual_proof_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_001"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
    '"no_external_media_download": false',
    '"no_final_thumbnail_image_generation": false',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_thumbnail_visual_proof_pack_builds_static_review_package(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"

    readback = build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_proof",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_THUMBNAIL_PROOF_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "thumbnail_proof_manifest.json")
    concepts = _load(output_dir / "thumbnail_concepts.json")
    title_candidates = _load(output_dir / "title_text_candidates.json")
    constraints = _load(output_dir / "visual_constraints.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "thumbnail_proof_panel.html").read_text(encoding="utf-8")
    markdown = (output_dir / "thumbnail_proof_panel.md").read_text(encoding="utf-8")
    svg = (output_dir / "thumbnail_layout_proof.svg").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "thumbnail-visual-proof-pack"
    assert manifest["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert manifest["boundaries"]["no_external_media_download"] is True
    assert manifest["boundaries"]["no_final_thumbnail_image_generation"] is True
    assert manifest["boundary_status"]["rights_status"] == "sample_only_no_publication"
    assert manifest["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert title_candidates["primary_title_candidates"][0]["text"] == "155 -> 140 km/h"
    assert {item["text"] for item in title_candidates["short_text_candidates"]} >= {
        "15km/hの罠",
        "速球のあとが怖い",
        "外低めスライダー",
    }
    assert concepts["concepts"][0]["concept_id"] == "speed_drop_scoreboard"
    assert concepts["concepts"][0]["state"] == "ready"
    assert constraints["proof_status"] == "static_proof_only_not_final_thumbnail"
    assert constraints["rights_boundaries"]["no_external_media"] is True
    assert constraints["rights_boundaries"]["no_logos_or_player_photos"] is True
    assert source_index["artifact_counts"]["source_present"] >= 8
    assert 'data-thumbnail-proof-pack="true"' in html
    assert 'data-section="layout-proof"' in html
    assert "source_artifact_index" in html
    assert "<svg" in svg
    assert "<image" not in svg.lower()
    assert "155" in svg and "140" in svg
    assert "https://" not in html + markdown + svg
    assert 'src="https://' not in html + markdown + svg
    assert "url(https://" not in html + markdown + svg
    for state in (
        "ready",
        "partial",
        "sample_fixture_not_real",
        "draft_offline",
        "blocked_by_real_input",
        "blocked_by_true_gate",
        "deferred",
        "missing",
        "unknown",
    ):
        assert f'data-status="{state}"' in html
        assert state in markdown


def test_thumbnail_visual_proof_validation_catches_external_media_reference(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"
    build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_proof",
    )
    html_path = output_dir / "thumbnail_proof_panel.html"
    html_path.write_text(
        html_path.read_text(encoding="utf-8") + '\n<img src="https://example.com/image.jpg">\n',
        encoding="utf-8",
    )

    readback = validate_thumbnail_visual_proof_pack(output_dir)

    assert readback["status"] == "failed"
    assert readback["checks"]["no_external_references"] is False
    assert any(item.startswith("external_reference:") for item in readback["failed_checks"])


def test_cli_build_thumbnail_visual_proof_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_thumbnail_visual_proof_pack"

    code = main([
        "build-thumbnail-visual-proof-pack",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_thumbnail_proof",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert payload["primary_title"] == "155 -> 140 km/h"
    assert payload["primary_human_review"].endswith("thumbnail_proof_panel.html")
    assert payload["primary_visual_proof"].endswith("thumbnail_layout_proof.svg")
    assert (output_dir / "thumbnail_proof_panel.html").exists()
    assert (output_dir / "thumbnail_layout_proof.svg").exists()


def test_generated_thumbnail_visual_proof_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"
    build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_proof",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)

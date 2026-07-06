from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.thumbnail_visual_proof_pack import (
    FORBIDDEN_TRUE_CLAIMS,
    REQUIRED_THUMBNAIL_PROOF_FILES,
    build_thumbnail_visual_proof_pack,
    validate_thumbnail_visual_proof_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"

REQUIRED_BOUNDARY_FLAGS = (
    "proof_only",
    "local_static_only",
    "no_external_media_download",
    "no_embedded_copyrighted_media",
    "not_production_thumbnail",
    "no_youtube_publication",
    "no_yymm4_import_or_render",
    "no_production_ymmp",
    "no_rights_or_public_ready_acceptance",
    "validation_noise_nonblocking",
)

REQUIRED_FALSE_GATES = (
    "production_ready",
    "production_thumbnail_ready",
    "public_ready",
    "rights_accepted",
    "youtube_uploaded",
    "actual_yymm4_import",
    "yymm4_rendered",
    "external_media_used",
)

EXTERNAL_MEDIA_MARKERS = (
    "data:image",
    "src=\"http://",
    "src=\"https://",
    "src='http://",
    "src='https://",
    "href=\"http://",
    "href=\"https://",
    "href='http://",
    "href='https://",
    "<image href=\"http",
    "<image href='http",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_thumbnail_visual_proof_pack_builds_static_local_package(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"

    readback = build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_visual_proof_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_THUMBNAIL_PROOF_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "manifest.json")
    variants_payload = _load(output_dir / "thumbnail_variants.json")
    source_index = _load(output_dir / "source_index.json")
    markdown = (output_dir / "thumbnail_visual_proof_panel.md").read_text(encoding="utf-8")
    html = (output_dir / "thumbnail_visual_proof.html").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "thumbnail-visual-proof-pack"
    assert manifest["variant_count"] == 3
    assert manifest["recommended_variant_id"] == "headline_driven"
    assert variants_payload["variant_count"] == 3
    assert variants_payload["recommended_variant_id"] == "headline_driven"
    assert variants_payload["orientation"] == "16:9"
    assert variants_payload["coordinate_system"] == {"width": 1280, "height": 720}
    for key in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundaries"][key] is True, key
    for key in REQUIRED_FALSE_GATES:
        assert manifest[key] is False, key
        assert variants_payload["proof_only_gates"][key] is False, key

    for variant in variants_payload["variants"]:
        assert variant["status"] == "proof_only"
        assert variant["variant_id"] in markdown
        assert variant["variant_id"] in html
        svg_path = output_dir / variant["svg_path"]
        assert svg_path.exists()
        svg = svg_path.read_text(encoding="utf-8")
        assert "<svg" in svg
        assert "1280" in svg
        assert "720" in svg

    for required_text in (
        "Proof only",
        "No external media",
        "Not production thumbnail",
        "Recommended variant",
        "source_index.json",
        "headline_driven",
        "speaker_contrast",
        "newsroom_diagram",
    ):
        assert required_text in markdown or required_text in html

    assert source_index["output_artifacts"]
    assert all(artifact["exists"] is True for artifact in source_index["output_artifacts"])


def test_thumbnail_visual_proof_validation_catches_missing_review_surface(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"
    build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_visual_proof_pack",
    )
    (output_dir / "thumbnail_visual_proof.html").unlink()

    readback = validate_thumbnail_visual_proof_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:thumbnail_visual_proof.html" in readback["failed_checks"]


def test_cli_build_thumbnail_visual_proof_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_thumbnail_visual_proof_pack"

    code = main([
        "build-thumbnail-visual-proof-pack",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_thumbnail_visual_proof_pack",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["variant_count"] == 3
    assert payload["recommended_variant_id"] == "headline_driven"
    assert payload["primary_machine_readable"].endswith("thumbnail_variants.json")
    assert payload["primary_human_review"].endswith("thumbnail_visual_proof.html")
    assert payload["contact_sheet"].endswith("thumbnail_contact_sheet.svg")
    assert (output_dir / "thumbnail_variants.json").exists()
    assert (output_dir / "thumbnail_visual_proof.html").exists()


def test_generated_thumbnail_visual_proof_pack_has_no_completion_or_external_media_claims(tmp_path) -> None:
    output_dir = tmp_path / "thumbnail_visual_proof_pack"
    build_thumbnail_visual_proof_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_thumbnail_visual_proof_pack",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for forbidden in FORBIDDEN_TRUE_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
            for marker in EXTERNAL_MEDIA_MARKERS:
                assert marker not in lowered, (path.name, marker)

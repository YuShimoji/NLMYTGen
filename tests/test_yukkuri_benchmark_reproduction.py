from __future__ import annotations

import copy
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

import pytest

from src.cli.main import main as cli_main
from src.pipeline.yukkuri_benchmark_reproduction import (
    BenchmarkRegistryError,
    DIMENSION_REQUIREMENTS,
    build_yukkuri_benchmark_pack,
    load_benchmark_registry,
    validate_benchmark_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (
    ROOT
    / "production_pilots/yukkuri_benchmark_six_v1/benchmark_registry.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class _StaticResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.resources: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        for name in ("src", "href"):
            value = values.get(name)
            if value:
                self.resources.append(value)


def test_registry_defines_exactly_six_unique_reverse_benchmarks() -> None:
    registry = load_benchmark_registry(REGISTRY)
    result = validate_benchmark_registry(registry)
    targets = registry["targets"]

    assert result == {
        "schema_version": "nlmytgen.yukkuri_benchmark_registry.v1",
        "status": "passed",
        "target_count": 6,
        "dimension_count": 12,
        "errors": [],
    }
    assert registry["strategy"] == "reverse_engineering_quick_win"
    assert registry["controlled_topic"] == "new_japanese_banknotes"
    assert registry["required_dimensions"] == list(DIMENSION_REQUIREMENTS)
    assert {target["benchmark_id"] for target in targets} == {
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
    }
    for field in ("channel_name", "video_id", "archetype_id"):
        assert len({target[field] for target in targets}) == 6
    assert sorted(target["quick_win_priority"] for target in targets) == list(range(1, 7))
    assert all(target["evidence_locators"] for target in targets)


def test_registry_rejects_duplicate_targets_and_unsafe_media_policy() -> None:
    duplicate = copy.deepcopy(load_benchmark_registry(REGISTRY))
    duplicate["targets"][1]["channel_name"] = duplicate["targets"][0]["channel_name"]
    with pytest.raises(BenchmarkRegistryError, match="CHANNEL_NAME_NOT_UNIQUE"):
        validate_benchmark_registry(duplicate)

    unsafe = copy.deepcopy(load_benchmark_registry(REGISTRY))
    unsafe["audio_policy"] = "audible"
    unsafe["media_foreground_allowed"] = True
    unsafe["media_playback_allowed"] = True
    with pytest.raises(BenchmarkRegistryError) as exc_info:
        validate_benchmark_registry(unsafe)
    message = str(exc_info.value)
    assert "AUDIO_POLICY_NOT_SILENT" in message
    assert "MEDIA_FOREGROUND_ALLOWED_MUST_BE_FALSE" in message
    assert "MEDIA_PLAYBACK_ALLOWED_MUST_BE_FALSE" in message


def test_repository_evidence_locators_remain_resolvable() -> None:
    registry = load_benchmark_registry(REGISTRY)
    repository_locators = [
        locator
        for target in registry["targets"]
        for locator in target["evidence_locators"]
        if not locator.startswith(("http://", "https://"))
    ]

    assert len(repository_locators) == 8
    for locator in repository_locators:
        relative, fragment = locator.split("#", maxsplit=1)
        source = ROOT / relative
        assert source.is_file(), locator
        assert fragment in source.read_text(encoding="utf-8"), locator


def test_pack_builds_six_static_blueprints_and_truthful_gap_matrix(
    tmp_path: Path,
) -> None:
    output = tmp_path / "pack"
    result = build_yukkuri_benchmark_pack(REGISTRY, output)
    readback = json.loads((output / "readback.json").read_text(encoding="utf-8"))
    matrix = json.loads((output / "gap_matrix.json").read_text(encoding="utf-8"))
    queue = json.loads((output / "execution_queue.json").read_text(encoding="utf-8"))

    assert result["status"] == "passed"
    assert result["target_count"] == 6
    assert result["reproduction_ready_count"] == 0
    assert result["blocked_count"] == 6
    assert readback["target_count"] == 6
    assert readback["archetype_count"] == 6
    assert readback["channel_count"] == 6
    assert readback["video_count"] == 6
    assert readback["required_dimension_count"] == 12
    assert all(readback["checks"].values())
    assert len(matrix["targets"]) == 6
    assert queue["next_benchmark_id"] == "B05"
    assert [row["quick_win_priority"] for row in queue["targets"]] == list(range(1, 7))
    assert queue["automatic_execution"] is False

    for benchmark_id in (f"B{index:02d}" for index in range(1, 7)):
        target_dir = output / benchmark_id
        assert (target_dir / "README.md").is_file()
        assert (target_dir / "static_review_card.html").is_file()
        blueprint = json.loads(
            (target_dir / "reproduction_blueprint.json").read_text(encoding="utf-8")
        )
        assert blueprint["benchmark_id"] == benchmark_id
        assert blueprint["required_count"] == 12
        assert blueprint["reproduction_ready"] is False
        assert blueprint["status"] == "blocked_by_missing_evidence"
        assert blueprint["boundaries"] == {
            "static_review_only": True,
            "foreground_media": False,
            "audible_output": False,
            "automatic_download": False,
            "python_video_render": False,
            "ymmp_zero_generation": False,
            "source_expression_copy_authorized": False,
        }


def test_review_html_embeds_no_media_or_remote_resource(tmp_path: Path) -> None:
    output = tmp_path / "pack"
    build_yukkuri_benchmark_pack(REGISTRY, output)

    for path in sorted(output.rglob("*.html")):
        parser = _StaticResourceParser()
        parser.feed(path.read_text(encoding="utf-8"))
        assert {"video", "audio", "iframe", "source"}.isdisjoint(parser.tags)
        assert all(not value.startswith(("http://", "https://", "//")) for value in parser.resources)


def test_manifest_hashes_match_and_regeneration_is_deterministic(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_yukkuri_benchmark_pack(REGISTRY, first)
    build_yukkuri_benchmark_pack(REGISTRY, second)

    first_manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second / "manifest.json").read_text(encoding="utf-8"))
    assert first_manifest == second_manifest
    for relative, expected in first_manifest["file_sha256"].items():
        assert _sha256(first / relative) == expected
    assert _file_hashes(first) == _file_hashes(second)


def test_readiness_changes_only_after_all_dimensions_and_gates_pass(
    tmp_path: Path,
) -> None:
    registry = copy.deepcopy(load_benchmark_registry(REGISTRY))
    for target in registry["targets"]:
        target["dimension_status"] = {
            name: "measured" for name in DIMENSION_REQUIREMENTS
        }
        target["completion_gates"] = {
            name: True for name in target["completion_gates"]
        }
    ready_registry = tmp_path / "registry.json"
    ready_registry.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    output = tmp_path / "ready-pack"
    result = build_yukkuri_benchmark_pack(ready_registry, output)
    assert result["reproduction_ready_count"] == 6
    assert result["blocked_count"] == 0
    for path in output.glob("B*/reproduction_blueprint.json"):
        blueprint = json.loads(path.read_text(encoding="utf-8"))
        assert blueprint["reproduction_ready"] is True
        assert blueprint["status"] == "reproduction_ready"


def test_cli_builds_pack_without_launching_media(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output = tmp_path / "cli-pack"
    assert cli_main(
        [
            "build-yukkuri-benchmark-pack",
            "--registry",
            str(REGISTRY),
            "--output",
            str(output),
            "--format",
            "json",
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["target_count"] == 6
    assert payload["reproduction_ready_count"] == 0
    assert (output / "index.html").is_file()

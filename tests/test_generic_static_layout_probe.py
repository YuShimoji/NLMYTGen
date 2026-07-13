from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import pytest

from src.pipeline.generic_static_layout_probe import (
    ASSET_REL,
    BATCH_STATE_REL,
    CARRIER_REL,
    EXPECTED_CARRIER_SHA256,
    IMAGE_BBOX,
    OBSERVATION_KEYS,
    PACKAGE_REL,
    PROJECT_REL,
    SUBTITLE_BBOX,
    TEXT_BBOX,
    ProbeError,
    _bbox_disjoint,
    _canonical_digest,
    _get_timeline_items,
    _item_type,
    collect_operator_result,
    materialize_probe,
    preflight_probe,
)
from src.pipeline.ymmp_patch import load_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / PACKAGE_REL
CARRIER = REPO_ROOT / CARRIER_REL


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_package_files() -> list[Path]:
    return [path for path in PACKAGE.rglob("*") if path.is_file() and "local_outputs" not in path.parts]


def test_materializer_preserves_carrier_bytes_and_voice_objects(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    before = CARRIER.read_bytes()
    source = load_ymmp(CARRIER)
    source_voices = [item for item in _get_timeline_items(source) if _item_type(item) == "VoiceItem"]

    readback = materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    result = load_ymmp(package / PROJECT_REL)
    result_voices = [item for item in _get_timeline_items(result) if _item_type(item) == "VoiceItem"]

    assert CARRIER.read_bytes() == before
    assert _sha(CARRIER) == EXPECTED_CARRIER_SHA256
    assert [_canonical_digest(item) for item in result_voices] == [
        _canonical_digest(item) for item in source_voices
    ]
    assert readback["checks"]["source_bytes_unchanged"] is True
    assert readback["checks"]["voice_objects_unchanged"] is True


def test_materialized_project_has_exact_item_families_counts_and_span(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    project = load_ymmp(package / PROJECT_REL)
    items = _get_timeline_items(project)
    types = [_item_type(item) for item in items]

    assert types.count("VoiceItem") == 1
    assert types.count("ImageItem") == 1
    assert types.count("TextItem") == 1
    assert set(types) == {"VoiceItem", "ImageItem", "TextItem"}
    image = next(item for item in items if _item_type(item) == "ImageItem")
    text = next(item for item in items if _item_type(item) == "TextItem")
    assert (image["Frame"], image["Length"], image["Layer"]) == (0, 109, 2)
    assert (text["Frame"], text["Length"], text["Layer"]) == (0, 109, 3)
    assert project["Timelines"][0]["MaxLayer"] == 3


def test_linked_subtitle_transport_is_preserved(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    source = load_ymmp(CARRIER)
    result = load_ymmp(package / PROJECT_REL)
    voice = next(item for item in _get_timeline_items(result) if _item_type(item) == "VoiceItem")

    assert voice["JimakuVisibility"] == "UseCharacterSetting"
    assert voice["Serif"]
    assert "\ufffd" not in voice["Serif"]
    assert re.search(r"[\u3040-\u30ff]", voice["Serif"])
    assert result["Characters"] == source["Characters"]
    character = next(item for item in result["Characters"] if item["Name"] == voice["CharacterName"])
    assert character["IsJimakuVisible"] is True
    assert character["Y"]["Values"][0]["Value"] == 350
    assert character["BasePoint"] == "CenterBottom"
    assert 842 <= 1080 / 2 + character["Y"]["Values"][0]["Value"] <= 1026


def test_probe_visual_items_are_static_defaults_without_effects(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    items = [
        item
        for item in _get_timeline_items(load_ymmp(package / PROJECT_REL))
        if _item_type(item) in {"ImageItem", "TextItem"}
    ]

    for item in items:
        for key in ("X", "Y", "Opacity", "Zoom", "Rotation"):
            assert item[key]["AnimationType"] == "なし"
            assert item[key]["Span"] == 0
            assert len(item[key]["Values"]) == 1
        assert item["Opacity"]["Values"][0]["Value"] == 100
        assert item["Zoom"]["Values"][0]["Value"] == 100
        assert item["Rotation"]["Values"][0]["Value"] == 0
        assert item["FadeIn"] == 0
        assert item["FadeOut"] == 0
        assert item["VideoEffects"] == []
        assert item["KeyFrames"] == {"Frames": [], "Count": 0}
        serialized = json.dumps(item, ensure_ascii=False).lower()
        assert "transition" not in serialized
        assert "shapeitem" not in serialized


def test_layout_zones_are_pairwise_nonoverlapping() -> None:
    assert _bbox_disjoint(IMAGE_BBOX, TEXT_BBOX)
    assert _bbox_disjoint(IMAGE_BBOX, SUBTITLE_BBOX)
    assert _bbox_disjoint(TEXT_BBOX, SUBTITLE_BBOX)


def test_materialization_is_byte_deterministic_on_second_pass(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    first = materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    project_before = (package / PROJECT_REL).read_bytes()
    asset_before = (package / ASSET_REL).read_bytes()
    readback_before = (package / "static_layout_probe_materialization_readback.json").read_bytes()

    second = materialize_probe(repo_root=REPO_ROOT, package_dir=package)

    assert second == first
    assert (package / PROJECT_REL).read_bytes() == project_before
    assert (package / ASSET_REL).read_bytes() == asset_before
    assert (package / "static_layout_probe_materialization_readback.json").read_bytes() == readback_before


def test_generated_asset_is_deterministic_opaque_rgb_png(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    payload = (package / ASSET_REL).read_bytes()

    assert payload[:8] == b"\x89PNG\r\n\x1a\n"
    assert int.from_bytes(payload[16:20], "big") == 640
    assert int.from_bytes(payload[20:24], "big") == 360
    assert payload[25] == 2


def test_preflight_matches_tracked_materialization_readback(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    receipt = preflight_probe(repo_root=REPO_ROOT, package_dir=package)

    assert receipt["result"] == "pass"
    assert receipt["launch_count"] == 0
    assert receipt["runtime_observation"] == "not_performed"
    assert receipt["runtime_capability_proven"] is False


def test_fixture_collect_is_synthetic_and_does_not_regrade(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    preflight_probe(repo_root=REPO_ROOT, package_dir=package)
    observations = package / "fixture.json"
    observations.write_text(
        json.dumps({"observations": {key: "pass" for key in OBSERVATION_KEYS}}),
        encoding="utf-8",
    )
    state = package / BATCH_STATE_REL
    output = package / "local_outputs/archive/fixture_result.json"

    result = collect_operator_result(
        state_path=state,
        observations_path=observations,
        output_path=output,
        fixture_mode=True,
        repo_root=REPO_ROOT,
        package_dir=package,
    )

    assert result["status"] == "fixture_validation_pass"
    assert result["operator_observations"]["evidence_grade"] == "synthetic_validation_only_not_observed"
    assert result["capability_regraded"] is False


def test_collector_rejects_output_outside_ignored_local_root(tmp_path: Path) -> None:
    package = tmp_path / "runtime_probe"
    materialize_probe(repo_root=REPO_ROOT, package_dir=package)
    observations = package / "fixture.json"
    observations.write_text(
        json.dumps({"observations": {key: "pass" for key in OBSERVATION_KEYS}}),
        encoding="utf-8",
    )
    with pytest.raises(ProbeError, match="OUTPUT_MUST_BE_UNDER_IGNORED_LOCAL_OUTPUTS"):
        collect_operator_result(
            state_path=package / BATCH_STATE_REL,
            observations_path=observations,
            output_path=tmp_path / "unsafe.json",
            fixture_mode=True,
            repo_root=REPO_ROOT,
            package_dir=package,
        )


def test_tracked_package_has_exact_required_deliverables() -> None:
    required = {
        "README_STATIC_LAYOUT_PROBE.md",
        "static_layout_probe_contract.json",
        "static_layout_probe_fixture.json",
        "static_layout_probe_materialization_readback.json",
        "expected_observation_contract.json",
        "operator_return_template.md",
        "validation_scope_receipt_link.json",
        "operator_batch/README_OPERATOR_BATCH.md",
        "operator_batch/run_generic_static_layout_probe.ps1",
        "operator_batch/collect_generic_static_layout_probe.ps1",
        "operator_batch/preflight_readback.json",
        "operator_batch/operator_batch_manifest.json",
    }
    actual = {path.relative_to(PACKAGE).as_posix() for path in _tracked_package_files()}
    assert required <= actual


def test_operator_contract_has_three_actions_questions_and_return_items() -> None:
    manifest = json.loads((PACKAGE / "operator_batch/operator_batch_manifest.json").read_text(encoding="utf-8"))
    observations = json.loads((PACKAGE / "expected_observation_contract.json").read_text(encoding="utf-8"))

    assert manifest["manual_action_count"] == len(manifest["manual_actions"]) == 3
    assert manifest["observation_count"] == len(manifest["observation_ids"]) == 3
    assert manifest["return_item_max"] == len(manifest["return_items"]) == 3
    assert observations["question_count"] == len(observations["questions"]) == 3
    assert [question["id"] for question in observations["questions"]] == list(OBSERVATION_KEYS)


def test_operator_scripts_put_safe_modes_before_single_launch() -> None:
    run_script = (PACKAGE / "operator_batch/run_generic_static_layout_probe.ps1").read_text(encoding="utf-8")
    collector = (PACKAGE / "operator_batch/collect_generic_static_layout_probe.ps1").read_text(encoding="utf-8")

    launch_index = run_script.index("Start-Process")
    assert run_script.index("if ($CollectOnly)") < launch_index
    assert run_script.index("if ($PreflightOnly)") < launch_index
    assert run_script.count("Start-Process") == 1
    assert "Start-Process" not in collector
    assert "SendKeys" not in run_script
    assert "screenshot" not in run_script.lower()


def test_operator_scripts_use_explicit_utf8_and_preserve_existing_results() -> None:
    combined = "\n".join(
        (PACKAGE / path).read_text(encoding="utf-8")
        for path in (
            "operator_batch/run_generic_static_layout_probe.ps1",
            "operator_batch/collect_generic_static_layout_probe.ps1",
        )
    )
    assert 'PYTHONUTF8 = "1"' in combined
    assert 'PYTHONIOENCODING = "utf-8"' in combined
    assert "[Text.Encoding]::UTF8" in combined
    assert "[Text.UTF8Encoding]::new($false)" in combined
    assert "OPERATOR_RESULT_ALREADY_EXISTS_ARCHIVE_FIRST" in (
        REPO_ROOT / "src/pipeline/generic_static_layout_probe.py"
    ).read_text(encoding="utf-8")


def test_tracked_probe_sources_are_topic_neutral_and_private_path_free() -> None:
    sources = [REPO_ROOT / "src/pipeline/generic_static_layout_probe.py", *_tracked_package_files()]
    combined = "\n".join(path.read_text(encoding="utf-8-sig") for path in sources)
    lowered = combined.lower()
    for forbidden in ("new_banknote", "episode_002", "production_pilots", "route a visuals"):
        assert forbidden not in lowered
    assert not re.search(r"[A-Za-z]:\\(?:Users|Storage|Program Files)", combined)
    assert "http://" not in lowered
    assert "https://" not in lowered


def test_local_probe_targets_are_ignored_and_untracked() -> None:
    import subprocess

    targets = [PACKAGE / PROJECT_REL, PACKAGE / ASSET_REL, PACKAGE / BATCH_STATE_REL]
    for target in targets:
        result = subprocess.run(
            ["git", "check-ignore", "-q", str(target)],
            cwd=REPO_ROOT,
            check=False,
        )
        assert result.returncode == 0
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(target)],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
        )
        assert tracked.returncode != 0


def test_canonical_78_path_count_is_consistent_across_current_surfaces() -> None:
    inventory = json.loads(
        (REPO_ROOT / "docs/visual_system/relevant_path_inventory.json").read_text(encoding="utf-8")
    )
    assert len(inventory["paths"]) == 78
    pipeline = (REPO_ROOT / "docs/PROJECT_PIPELINE.mmd").read_text(encoding="utf-8")
    runtime = (REPO_ROOT / "docs/runtime-state.md").read_text(encoding="utf-8")
    cockpit = (REPO_ROOT / "docs/PROJECT_COCKPIT.md").read_text(encoding="utf-8")
    assert "61 paths" not in pipeline
    assert "78 paths" in pipeline
    assert "78" in runtime
    assert "78" in cockpit


def test_validation_scope_receipt_arithmetic_and_state_inclusion() -> None:
    receipt = json.loads(
        (REPO_ROOT / "docs/visual_system/validation_scope_receipt.json").read_text(encoding="utf-8")
    )
    commands = receipt["commands"]
    assert len(commands) >= 2
    assert all(command["failed"] == 0 for command in commands)
    assert receipt["aggregate"]["passed"] == sum(command["passed"] for command in commands)
    assert receipt["aggregate"]["skipped"] == sum(command["skipped"] for command in commands)
    state_commands = [command for command in commands if command["includes_state_sync_tests"]]
    assert len(state_commands) == 1
    assert receipt["aggregate"]["state_sync_tests_included"] is True
    assert receipt["aggregate"]["semantics"] == "sum_of_non_overlapping_test_selections"

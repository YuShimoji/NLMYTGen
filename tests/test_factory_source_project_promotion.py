from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.pipeline import factory_source_project_promotion as promotion
from src.pipeline.factory_queue import evaluate_factory_queue


ROOT = Path(__file__).resolve().parents[1]
QUEUE = promotion.PREDECESSOR_QUEUE


def _evaluation() -> dict:
    return evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )


def _request(evaluation: dict, **overrides):
    arguments = {
        "evaluation": evaluation,
        "queue_path": QUEUE,
        "package_id": promotion.PACKAGE_ID,
        "to_lifecycle": promotion.TARGET_LIFECYCLE,
        "authority_id": promotion.AUTHORITY_ID,
        "render_authority_id": None,
    }
    arguments.update(overrides)
    return promotion._validate_request(**arguments)


def _assert_code(exc: pytest.ExceptionInfo, code: str) -> None:
    assert isinstance(exc.value, promotion.FactorySourceProjectPromotionError)
    assert exc.value.code == code


def test_plan_only_public_command_performs_no_product_write(monkeypatch):
    output = ROOT / promotion.SOURCE_PROJECT
    before = (
        (promotion.sha256_file(output), output.stat().st_size, output.stat().st_mtime_ns)
        if output.exists()
        else None
    )
    monkeypatch.setattr(promotion, "_validate_known_noop", lambda **_: None)
    result = promotion.advance_factory_package(
        repo_root=ROOT,
        queue_path=QUEUE,
        package_id=promotion.PACKAGE_ID,
        to_lifecycle=promotion.TARGET_LIFECYCLE,
        authority_id=promotion.AUTHORITY_ID,
        execute=False,
        persist_failure=False,
    )
    assert result["status"] == "planned"
    assert result["boundaries"]["yymm4_launch_count"] == 0
    assert result["boundaries"]["render_performed"] is False
    after = (
        (promotion.sha256_file(output), output.stat().st_size, output.stat().st_mtime_ns)
        if output.exists()
        else None
    )
    assert after == before


def test_source_project_ready_descriptor_keeps_immutable_pre_render_manifest():
    from src.pipeline.factory_contract_v2_1 import validate_factory_package_lifecycle

    successor = ROOT / promotion.SUCCESSOR_DESCRIPTOR
    if not successor.is_file():
        pytest.skip("successor artifact is created by the authorized execution")
    result = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=promotion.SUCCESSOR_DESCRIPTOR,
        check_live=False,
        require_lifecycle="source_project_ready",
    )
    assert result["normalized_lifecycle"]["state"] == "source_project_ready"
    descriptor = promotion._load_json(successor)
    manifest = promotion._load_json(ROOT / descriptor["episode_execution"]["manifest_path"])
    assert manifest["lifecycle"] == "package_prepared"


def test_second_identical_promotion_is_validation_only_noop(tmp_path, monkeypatch):
    predecessor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    rows, cues = promotion._validate_predecessor_inputs(ROOT, predecessor)
    project_path = tmp_path / promotion.SOURCE_PROJECT
    project_path.parent.mkdir(parents=True)
    lengths = [300, 300, 300, 300]
    project = {
        "FilePath": project_path.name,
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "ID": "test",
                "Name": "food_expiry_labels_001 source project",
                "Items": [
                    {
                        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                        "CharacterName": speaker,
                        "Serif": text,
                        "Frame": sum(lengths[:index]),
                        "Length": lengths[index],
                        "Layer": index,
                    }
                    for index, (speaker, text) in enumerate(rows)
                ],
                "Length": sum(lengths),
                "CurrentFrame": 0,
                "MaxLayer": 3,
            }
        ],
        "Characters": [{"Name": promotion.EXPECTED_SPEAKER}],
        "CollapsedGroups": [],
        "LayoutXml": "",
        "ToolStates": {},
    }
    project_path.write_text(
        json.dumps(project, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    readback = promotion.build_source_project_readback(
        repo_root=tmp_path,
        project_locator=promotion.SOURCE_PROJECT,
        predecessor=predecessor,
        cue_sequence=cues,
        expected_rows=rows,
        builder_result={
            "yymm4_version": "4.54.0.1",
            "driver": "windows_uia",
            "process_cleanup": True,
        },
    )
    predecessor_queue = promotion._load_json(ROOT / promotion.PREDECESSOR_QUEUE)
    noop_observation = {
        "sequence": 2,
        "event": "verified_noop",
        "source_project_sha256": readback["source_project"]["sha256"],
        "source_project_size_bytes": readback["source_project"]["size_bytes"],
        "source_project_rewritten": False,
        "successor_descriptor_rewritten": False,
        "yymm4_launch_count": 0,
        "source_project_builder_launch_count": 0,
    }
    promotion._write_json(tmp_path / promotion.SOURCE_PROJECT_READBACK, readback)
    promotion._write_json(
        tmp_path / promotion.PROMOTION_RECEIPT,
        promotion._receipt(readback=readback, observations=[noop_observation]),
    )
    promotion._write_json(
        tmp_path / promotion.SUCCESSOR_DESCRIPTOR,
        promotion._build_successor_descriptor(predecessor, readback),
    )
    promotion._write_json(
        tmp_path / promotion.PREDECESSOR_QUEUE,
        predecessor_queue,
    )
    promotion._write_json(
        tmp_path / promotion.SUCCESSOR_QUEUE,
        promotion._build_successor_queue(predecessor_queue),
    )
    monkeypatch.setattr(
        promotion,
        "validate_factory_package_lifecycle",
        lambda **_: {"status": "passed"},
    )
    monkeypatch.setattr(
        promotion,
        "evaluate_factory_queue",
        lambda **_: {
            "evaluation_sha256": "a" * 64,
            "counts": {
                "verified_noop": 3,
                "source_project_candidates": 0,
                "render_candidates": 1,
                "scheduled_for_render": 0,
                "execution_set_size": 0,
                "blocked_packages": 0,
                "invalid_packages": 0,
            },
        },
    )
    before = (
        promotion.sha256_file(project_path),
        project_path.stat().st_size,
        project_path.stat().st_mtime_ns,
    )
    result = promotion._validate_known_noop(
        repo_root=tmp_path,
        predecessor=predecessor,
        expected_rows=rows,
        cue_sequence=cues,
    )
    after = (
        promotion.sha256_file(project_path),
        project_path.stat().st_size,
        project_path.stat().st_mtime_ns,
    )
    assert result is not None
    assert result["status"] == "verified_noop"
    assert result["receipt_observation_appended"] is False
    assert result["boundaries"]["yymm4_launch_count"] == 0
    assert result["boundaries"]["source_project_builder_launch_count"] == 0
    assert after == before


def test_package_not_selected_by_queue_fails_closed():
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(_evaluation(), package_id="real_estate_reins_transparency_001")
    _assert_code(exc, "package_not_selected")


def test_duplicate_source_project_candidate_fails_closed():
    evaluation = copy.deepcopy(_evaluation())
    duplicate = copy.deepcopy(evaluation["packages"][-1])
    duplicate["package_id"] = "duplicate_candidate"
    evaluation["packages"].append(duplicate)
    evaluation["counts"]["total_packages"] = 5
    evaluation["counts"]["source_project_candidates"] = 2
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(evaluation)
    _assert_code(exc, "queue_candidate_baseline_drift")


def test_content_identity_drift_fails_closed():
    evaluation = copy.deepcopy(_evaluation())
    evaluation["packages"][-1]["content_identity_sha256"] = "0" * 64
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(evaluation)
    _assert_code(exc, "predecessor_identity_drift")


def test_canonical_csv_hash_mismatch_fails_closed(monkeypatch):
    descriptor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    real_sha = promotion.sha256_file

    def drift(path: Path) -> str:
        if Path(path).name == "canonical_yymm4.csv":
            return "0" * 64
        return real_sha(path)

    monkeypatch.setattr(promotion, "sha256_file", drift)
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion._validate_predecessor_inputs(ROOT, descriptor)
    _assert_code(exc, "canonical_csv_hash_mismatch")


def test_speaker_mapping_change_fails_closed():
    descriptor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    descriptor["shape"]["speaker_mapping"]["cue_004"] = "ゆっくり魔理沙黄縁"
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion._validate_predecessor_inputs(ROOT, descriptor)
    _assert_code(exc, "speaker_mapping_drift")


def test_cue_text_or_order_change_fails_closed(monkeypatch):
    descriptor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    real_load = promotion._load_json
    canonical_path = (ROOT / descriptor["canonical_content"]["path"]).resolve()

    def drift(path: Path) -> dict:
        value = real_load(path)
        if Path(path).resolve() == canonical_path:
            value["cues"][0], value["cues"][1] = value["cues"][1], value["cues"][0]
        return value

    monkeypatch.setattr(promotion, "_load_json", drift)
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion._validate_predecessor_inputs(ROOT, descriptor)
    _assert_code(exc, "cue_text_or_order_drift")


def test_output_target_collision_fails_before_builder(tmp_path):
    project = tmp_path / promotion.SOURCE_PROJECT
    project.parent.mkdir(parents=True)
    project.write_text("unrelated", encoding="utf-8")
    predecessor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    rows, cues = promotion._validate_predecessor_inputs(ROOT, predecessor)
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion._validate_known_noop(
            repo_root=tmp_path,
            predecessor=predecessor,
            expected_rows=rows,
            cue_sequence=cues,
        )
    _assert_code(exc, "output_target_collision")


def test_existing_corrupt_project_fails_before_builder(tmp_path):
    project = tmp_path / promotion.SOURCE_PROJECT
    project.parent.mkdir(parents=True)
    project.write_text("{}", encoding="utf-8")
    for locator in (
        promotion.SOURCE_PROJECT_READBACK,
        promotion.PROMOTION_RECEIPT,
        promotion.SUCCESSOR_DESCRIPTOR,
        promotion.SUCCESSOR_QUEUE,
    ):
        target = tmp_path / locator
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("{}\n", encoding="utf-8")
    predecessor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    rows, cues = promotion._validate_predecessor_inputs(ROOT, predecessor)
    with pytest.raises(promotion.FactorySourceProjectPromotionError):
        promotion._validate_known_noop(
            repo_root=tmp_path,
            predecessor=predecessor,
            expected_rows=rows,
            cue_sequence=cues,
        )


def test_lifecycle_jump_directly_to_rendered_is_rejected():
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(_evaluation(), to_lifecycle="rendered")
    _assert_code(exc, "unsupported_lifecycle_jump")


def test_render_authority_is_rejected_by_source_only_command():
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(_evaluation(), render_authority_id="render-authority")
    _assert_code(exc, "render_authority_forbidden")


def test_missing_authority_id_is_rejected():
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(_evaluation(), authority_id=None)
    _assert_code(exc, "authority_id_missing")


def test_unrelated_package_override_is_rejected():
    evaluation = copy.deepcopy(_evaluation())
    evaluation["packages"][-1]["package_id"] = "unrelated_package"
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        _request(evaluation, package_id="unrelated_package")
    _assert_code(exc, "unrelated_package_override")


def test_source_project_outside_approved_package_root_is_rejected(tmp_path):
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion._validate_output_locator(
            tmp_path,
            Path("production_pilots/factory_canaries/other/local_outputs/a.ymmp"),
        )
    _assert_code(exc, "source_project_outside_package_root")


def test_private_absolute_path_in_project_is_rejected(tmp_path):
    project_path = tmp_path / promotion.SOURCE_PROJECT
    project_path.parent.mkdir(parents=True)
    project = {
        "FilePath": r"C:\Users\private\source.ymmp",
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "Name": "source",
                "Items": [
                    {
                        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                        "CharacterName": promotion.EXPECTED_SPEAKER,
                        "Serif": f"cue {index}",
                        "Frame": index * 300,
                        "Length": 300,
                        "Layer": index,
                    }
                    for index in range(4)
                ],
                "Length": 1200,
                "CurrentFrame": 0,
                "MaxLayer": 3,
            }
        ],
        "Characters": [{"Name": promotion.EXPECTED_SPEAKER}],
        "CollapsedGroups": [],
        "LayoutXml": "",
        "ToolStates": {},
    }
    project_path.write_text(
        json.dumps(project, ensure_ascii=False),
        encoding="utf-8",
    )
    predecessor = promotion._load_json(ROOT / promotion.PREDECESSOR_DESCRIPTOR)
    rows = [(promotion.EXPECTED_SPEAKER, f"cue {index}") for index in range(4)]
    with pytest.raises(promotion.FactorySourceProjectPromotionError) as exc:
        promotion.build_source_project_readback(
            repo_root=tmp_path,
            project_locator=promotion.SOURCE_PROJECT,
            predecessor=predecessor,
            cue_sequence=[f"cue_{index:03d}" for index in range(1, 5)],
            expected_rows=rows,
            builder_result={"yymm4_version": "4.54.0.1"},
        )
    _assert_code(exc, "source_project_metadata_not_clean")

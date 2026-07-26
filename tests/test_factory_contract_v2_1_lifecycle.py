from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

import pytest

from src.cli import main as cli
from src.pipeline.factory_contract_v2_1 import (
    FactoryContractError,
    LIFECYCLE_ORDER,
    build_pre_render_stage_plan,
    validate_factory_package_lifecycle,
)


ROOT = Path(__file__).resolve().parents[1]
V2_SCHEMA = Path("schemas/factory_contract_v2/factory_package_v2.schema.json")
V2_INVENTORY = Path("schemas/factory_contract_v2/field_inventory.json")
V2_DESCRIPTORS = (
    Path(
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "factory_package_v2.json"
    ),
    Path(
        "production_pilots/factory_canaries/"
        "real_estate_reins_transparency_001/factory_package_v2.json"
    ),
    Path(
        "production_pilots/factory_canaries/"
        "ai_monitoring_labor_001/factory_package_v2.json"
    ),
)
V2_EXPECTED_HASHES = {
    V2_SCHEMA: "d0e831c60ceba17a83c6fe106bf1fa574cfa3881976934c3fb4571a59bb8dfbb",
    V2_INVENTORY: "8bc3a669e0b77b2dcc68f59f0f5bcf03fe6eaaaaf8aec3bad4fb3b814f6490d4",
    V2_DESCRIPTORS[0]: "80f1130711a46c3f3a77f2ec1da391fd338569d9aaf0385deeb96a2a698333f7",
    V2_DESCRIPTORS[1]: "21e0052011b1d55f7ff27bf63af5c4f79dbc3932762df86375cdca86e59d63db",
    V2_DESCRIPTORS[2]: "866f03c7cff7570e1ad9d1b22525598a99084e9aa0b5227c4c2d31cea528eeb4",
}
FOURTH = Path(
    "production_pilots/factory_canaries/"
    "food_expiry_labels_001/factory_package_v2_1.json"
)
FOURTH_PACKAGE = FOURTH.parent


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(relative: Path = FOURTH) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


@contextmanager
def _mutated_descriptor(
    mutate: Callable[[dict[str, Any]], None],
) -> Iterator[Path]:
    payload = copy.deepcopy(_load())
    mutate(payload)
    with tempfile.TemporaryDirectory(prefix=".factory-v2-1-test-", dir=ROOT) as temp:
        path = Path(temp) / "factory_package_v2_1.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        yield path


def _expect_error(
    code: str,
    mutate: Callable[[dict[str, Any]], None],
    *,
    check_live: bool = False,
) -> FactoryContractError:
    with _mutated_descriptor(mutate) as path:
        with pytest.raises(FactoryContractError) as observed:
            validate_factory_package_lifecycle(
                repo_root=ROOT,
                descriptor_path=path,
                check_live=check_live,
            )
    assert observed.value.code == code
    assert observed.value.section
    assert observed.value.field_path
    assert observed.value.consumer_effect
    return observed.value


def _set_lifecycle(row: dict[str, Any], state: str) -> None:
    flags = {
        "package_prepared": (True, True, False, False, False),
        "source_project_ready": (True, True, True, False, False),
        "rendered": (True, True, True, True, False),
        "human_accepted": (True, True, True, True, True),
    }[state]
    row["lifecycle"].update(
        {
            "state": state,
            "contract_valid": flags[0],
            "tracked_package_ready": flags[1],
            "source_project_ready": flags[2],
            "render_ready": flags[3],
            "human_accepted": flags[4],
        }
    )


def _set_ready_source_project(row: dict[str, Any]) -> None:
    row["source_project"].update(
        {
            "state": "ready",
            "path": (
                "production_pilots/factory_canaries/"
                "food_expiry_labels_001/canonical_yymm4.csv"
            ),
            "sha256": "00ade6df462c9cefb8cc1960d385def18a053793561d96a1da38eb9d9c41b855",
            "identity_source": "synthetic_negative_fixture_receipt",
        }
    )


def _add_generated_project(row: dict[str, Any]) -> None:
    row["generated_project"] = {
        "schema": "nlmytgen.factory_package.generated_project.v2.1",
        "path": (
            "production_pilots/factory_canaries/"
            "food_expiry_labels_001/derived_yymm4_import.csv"
        ),
        "sha256": "b4b4bb7ae998fa3c850a030df2ba719cde8ba1bd8c82c1215b40a7d5a9ee2256",
        "identity_source": "synthetic_negative_fixture_receipt",
        "availability_claim": "receipt_identity_only",
    }


def _add_render_validation(row: dict[str, Any]) -> None:
    row["render_validation"] = {
        "schema": "nlmytgen.factory_package.render_validation.v2.1",
        "technical_receipt_path": (
            "production_pilots/factory_canaries/"
            "food_expiry_labels_001/source_registry.json"
        ),
        "technical_receipt_sha256": (
            "c94d1897d1880cf9e652be6af4bfea6c607f728092f864f463c439c2a4170a50"
        ),
        "technical_status": "passed",
        "mp4_path": (
            "production_pilots/factory_canaries/"
            "food_expiry_labels_001/local_media/caa_expiration_date_page1.png"
        ),
        "mp4_sha256": "2c06e90c629a3be96b2ce973e81900f128ea63d3a07124714607232166f04517",
        "availability_claim": "receipt_identity_only",
    }


def test_v2_0_schema_inventory_and_descriptors_remain_byte_exact() -> None:
    assert {
        path: _sha(ROOT / path) for path in V2_EXPECTED_HASHES
    } == V2_EXPECTED_HASHES


def test_v2_0_descriptors_normalize_read_only_to_lifecycle() -> None:
    before = {path: _sha(ROOT / path) for path in V2_EXPECTED_HASHES}
    rows = [
        validate_factory_package_lifecycle(
            repo_root=ROOT,
            descriptor_path=path,
            require_lifecycle="rendered",
        )
        for path in V2_DESCRIPTORS
    ]
    assert [row["normalized_lifecycle"]["state"] for row in rows] == [
        "human_accepted",
        "rendered",
        "rendered",
    ]
    assert rows[0]["normalized_lifecycle"]["human_accepted"] is True
    assert rows[1]["normalized_lifecycle"]["human_accepted"] is False
    assert rows[2]["normalized_lifecycle"]["human_accepted"] is False
    assert all(row["normalized"]["rights_approved"] is False for row in rows)
    assert all(
        row["compatibility"]["adapter"]
        == "v2_0_to_v2_1_read_only_lifecycle_normalizer"
        for row in rows
    )
    assert {path: _sha(ROOT / path) for path in V2_EXPECTED_HASHES} == before


def test_fourth_package_is_single_speaker_one_scene_prepared_contract() -> None:
    result = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
        check_live=True,
        require_lifecycle="package_prepared",
    )
    assert result["status"] == "passed"
    assert result["input_schema"] == "nlmytgen.factory_package.v2.1"
    assert result["input_schema_version"] == "2.1"
    assert result["normalized_lifecycle"]["state"] == "package_prepared"
    assert result["readiness"] == {
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": False,
        "render_ready": False,
        "human_accepted": False,
        "media_live_exact": True,
        "media_receipt_only": False,
    }
    assert result["normalized"]["cue_count"] == 4
    assert result["normalized"]["scene_count"] == 1
    assert result["normalized"]["speaker_counts"] == {"ゆっくり霊夢赤縁": 4}
    assert result["normalized"]["asset_count"] == 2
    assert result["normalized"]["source_count"] == 2
    assert 18 <= result["normalized"]["duration_seconds"] <= 30
    assert result["normalized"]["human_decision"] == (
        "absent_before_human_accepted"
    )
    assert result["normalized"]["rights_approved"] is False
    assert result["normalized"]["production_approved"] is False
    assert result["normalized"]["publication_approved"] is False
    assert result["normalized"]["upload_approved"] is False
    assert result["normalized"]["release_approved"] is False


def test_asset_count_can_be_lower_than_cues_with_distinct_reused_crops() -> None:
    descriptor = _load()
    mappings = descriptor["media_provenance"]["asset_mappings"]
    grouped: dict[str, set[tuple[float, ...]]] = {}
    for row in mappings:
        grouped.setdefault(row["asset_id"], set()).add(tuple(row["crop"]))
    assert len(mappings) == 4
    assert len(grouped) == 2
    assert all(len(crops) == 2 for crops in grouped.values())
    result = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
    )
    assert result["normalized"]["asset_count"] < result["normalized"]["cue_count"]


def test_v2_1_schema_inventory_record_conditional_change_and_rollback() -> None:
    schema = json.loads(
        (
            ROOT
            / "schemas/factory_contract_v2_1/factory_package_v2_1.schema.json"
        ).read_text(encoding="utf-8")
    )
    inventory = json.loads(
        (
            ROOT / "schemas/factory_contract_v2_1/field_inventory.json"
        ).read_text(encoding="utf-8")
    )
    assert schema["$id"] == "nlmytgen.factory_package.v2.1"
    assert len(schema["allOf"]) == 4
    assert inventory["inherits"]["sha256"] == V2_EXPECTED_HASHES[V2_INVENTORY]
    assert inventory["lifecycle_order"] == list(LIFECYCLE_ORDER)
    assert len(inventory["schema_change_table"]) == 6
    assert all(row["migration"] and row["rollback"] for row in inventory["schema_change_table"])


def test_v2_1_validation_is_deterministic_twice() -> None:
    first = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
        check_live=True,
    )
    second = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
        check_live=True,
    )
    assert first == second
    assert first["descriptor"]["sha256"] == (
        "18e078f6f6c5b6e17808ec9378d8476a9cd8ce426cd1281563c833ae21acf329"
    )
    assert first["descriptor"]["normalized_sha256"] == (
        "5bfebe8c93d18dc546a8fe675de7ad303219ff5654b362c0950e371a6093a234"
    )


def test_tracked_only_media_absence_is_availability_not_contract_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_is_file = Path.is_file

    def tracked_only_is_file(path: Path) -> bool:
        if (
            "food_expiry_labels_001" in path.parts
            and "local_media" in path.parts
        ):
            return False
        return real_is_file(path)

    monkeypatch.setattr(Path, "is_file", tracked_only_is_file)
    result = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
        check_live=True,
    )
    media = [
        row
        for row in result["availability"]
        if row["artifact_class"].startswith("media_asset:")
    ]
    assert {row["status"] for row in media} == {
        "receipt_only_no_live_file"
    }
    assert result["status"] == "passed"
    assert result["readiness"]["media_receipt_only"] is True
    assert result["normalized_lifecycle"]["state"] == "package_prepared"


def test_require_lifecycle_exit_behavior(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        cli.main(
            [
                "validate-factory-package",
                "--package",
                FOURTH.as_posix(),
                "--require-lifecycle",
                "package_prepared",
                "--format",
                "json",
            ]
        )
        == 0
    )
    passed = json.loads(capsys.readouterr().out)
    assert passed["normalized_lifecycle"]["state"] == "package_prepared"

    assert (
        cli.main(
            [
                "validate-factory-package",
                "--package",
                FOURTH.as_posix(),
                "--require-lifecycle",
                "rendered",
                "--format",
                "json",
            ]
        )
        == 1
    )
    failed = json.loads(capsys.readouterr().err)
    assert failed["error_code"] == "required_lifecycle_not_reached"
    assert failed["consumer_effect"]


def test_pre_render_dry_run_stops_before_generation_without_pipeline_launch(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    called = False

    def forbidden_pipeline(**_: Any) -> dict[str, Any]:
        nonlocal called
        called = True
        raise AssertionError("existing render-capable pipeline must not run")

    monkeypatch.setattr(
        "src.pipeline.episode_video.run_episode_video",
        forbidden_pipeline,
    )
    before = {
        path: _sha(path)
        for path in (ROOT / FOURTH_PACKAGE).rglob("*")
        if path.is_file() and "local_media" not in path.parts
    }
    assert (
        cli.main(
            [
                "build-episode-video",
                "--factory-package",
                FOURTH.as_posix(),
                "--dry-run",
            ]
        )
        == 0
    )
    plan = json.loads(capsys.readouterr().out)
    assert called is False
    assert plan["status"] == "pre_render_plan_complete"
    assert plan["completed_video_dry_run"] is False
    assert plan["stop"]["before_stage"] == "source_project_generation"
    assert set(plan["launch_counts"].values()) == {0}
    assert set(plan["writes"].values()) == {False}
    after = {
        path: _sha(path)
        for path in (ROOT / FOURTH_PACKAGE).rglob("*")
        if path.is_file() and "local_media" not in path.parts
    }
    assert after == before


def test_pre_render_stage_plan_is_deterministic_and_bounded() -> None:
    first = build_pre_render_stage_plan(
        repo_root=ROOT,
        descriptor_path=FOURTH,
    )
    second = build_pre_render_stage_plan(
        repo_root=ROOT,
        descriptor_path=FOURTH,
    )
    assert first == second
    assert first["protected_inputs"] == {"count": 9, "exact": True}
    assert first["boundaries"] == {
        "network_access": False,
        "system_volume_operation": False,
        "human_review": False,
        "rights_approval": False,
        "production": False,
        "publication": False,
        "upload": False,
        "release": False,
    }


def test_package_prepared_rejects_falsely_present_generated_project() -> None:
    _expect_error(
        "package_prepared_advanced_evidence",
        _add_generated_project,
    )


def test_rendered_without_generated_project_fails_closed() -> None:
    def mutate(row: dict[str, Any]) -> None:
        _set_lifecycle(row, "rendered")
        _set_ready_source_project(row)

    _expect_error("rendered_generated_project_required", mutate)


def test_rendered_without_mp4_validation_fails_closed() -> None:
    def mutate(row: dict[str, Any]) -> None:
        _set_lifecycle(row, "rendered")
        _set_ready_source_project(row)
        _add_generated_project(row)

    _expect_error("rendered_validation_required", mutate)


def test_human_accepted_without_receipt_fails_closed() -> None:
    def mutate(row: dict[str, Any]) -> None:
        _set_lifecycle(row, "human_accepted")
        _set_ready_source_project(row)
        _add_generated_project(row)
        _add_render_validation(row)

    _expect_error("human_acceptance_receipt_required", mutate)


def test_rights_true_without_authority_record_fails_closed() -> None:
    def mutate(row: dict[str, Any]) -> None:
        row["authority"]["rights"]["approved"] = True

    _expect_error("authority_record_required", mutate)


def test_cue_without_provenance_fails_closed() -> None:
    _expect_error(
        "cue_media_coverage_invalid",
        lambda row: row["media_provenance"]["asset_mappings"].pop(),
    )


def test_unsupported_factual_unit_fails_closed() -> None:
    _expect_error(
        "factual_claim_partition_invalid",
        lambda row: row["claim_support"].__setitem__(
            "unsupported_factual_units", 1
        ),
    )


def test_run_local_path_inside_content_identity_fails_closed() -> None:
    _expect_error(
        "section_fields_invalid",
        lambda row: row["identities"].__setitem__(
            "machine_path", "run-local/generated-project"
        ),
    )


def test_absolute_private_tracked_path_fails_closed() -> None:
    _expect_error(
        "private_absolute_path_forbidden",
        lambda row: row["source_intake"].__setitem__(
            "authority_path", "C:/Users/private/source_registry.json"
        ),
    )


def test_unknown_unversioned_top_level_field_fails_closed() -> None:
    _expect_error(
        "top_level_fields_invalid",
        lambda row: row.__setitem__("topic_specific_mode", True),
    )


def test_lifecycle_upgrade_or_downgrade_flag_contradiction_fails_closed() -> None:
    _expect_error(
        "lifecycle_flags_contradiction",
        lambda row: row["lifecycle"].__setitem__("render_ready", True),
    )


def test_shared_lifecycle_validator_has_no_topic_id_branch() -> None:
    source = (
        ROOT / "src/pipeline/factory_contract_v2_1.py"
    ).read_text(encoding="utf-8")
    forbidden_ids = (
        "new_banknote_security_notebooklm_001",
        "real_estate_reins_transparency_001",
        "ai_monitoring_labor_001",
        "food_expiry_labels_001",
    )
    assert all(value not in source for value in forbidden_ids)


def test_no_universal_or_production_ready_overclaim() -> None:
    result = validate_factory_package_lifecycle(
        repo_root=ROOT,
        descriptor_path=FOURTH,
    )
    assert result["boundaries"]["universal_arbitrary_topic_compatibility"] is False
    assert result["normalized"]["production_approved"] is False
    assert result["normalized_lifecycle"]["state"] == "package_prepared"

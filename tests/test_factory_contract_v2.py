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
from src.pipeline.factory_contract_v2 import (
    FactoryContractError,
    canonical_json_bytes,
    validate_factory_contract_receipt,
    validate_factory_package,
)


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTORS = (
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
NEW_BANKNOTE, REINS, AI_MONITORING = DESCRIPTORS


def _load(relative: Path = AI_MONITORING) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@contextmanager
def _mutated_descriptor(
    mutate: Callable[[dict[str, Any]], None],
    *,
    source: Path = AI_MONITORING,
) -> Iterator[Path]:
    payload = copy.deepcopy(_load(source))
    mutate(payload)
    with tempfile.TemporaryDirectory(prefix=".factory-v2-test-", dir=ROOT) as temp:
        path = Path(temp) / "factory_package_v2.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        yield path


def _expect_error(
    code: str,
    mutate: Callable[[dict[str, Any]], None],
    *,
    source: Path = AI_MONITORING,
    check_live: bool = False,
) -> FactoryContractError:
    with _mutated_descriptor(mutate, source=source) as path:
        with pytest.raises(FactoryContractError) as observed:
            validate_factory_package(
                repo_root=ROOT,
                descriptor_path=path,
                check_live=check_live,
            )
    assert observed.value.code == code
    assert observed.value.section
    assert observed.value.field_path
    assert observed.value.consumer_effect
    return observed.value


def test_all_three_descriptors_validate_and_keep_authority_clocks_separate() -> None:
    rows = [
        validate_factory_package(
            repo_root=ROOT,
            descriptor_path=path,
            check_live=False,
        )
        for path in DESCRIPTORS
    ]

    assert [row["normalized"]["cue_count"] for row in rows] == [9, 7, 5]
    assert [row["normalized"]["scene_count"] for row in rows] == [3, 4, 2]
    assert [row["normalized"]["asset_count"] for row in rows] == [9, 7, 5]
    assert rows[0]["normalized"]["human_decision"] == "accepted_exact_artifact"
    assert rows[1]["normalized"]["human_decision"] == "not_human_accepted"
    assert rows[2]["normalized"]["human_decision"] == "not_human_accepted"
    assert all(row["normalized"]["rights_approved"] is False for row in rows)
    assert all(row["normalized"]["production_approved"] is False for row in rows)
    assert all(row["normalized"]["publication_approved"] is False for row in rows)
    assert all(row["v1_compatibility"]["source_artifacts_mutated"] is False for row in rows)


def test_descriptor_normalization_is_deterministic_twice() -> None:
    for path in DESCRIPTORS:
        payload = _load(path)
        assert canonical_json_bytes(payload) == canonical_json_bytes(
            json.loads(canonical_json_bytes(payload))
        )
        first = validate_factory_package(
            repo_root=ROOT,
            descriptor_path=path,
            check_live=False,
        )
        second = validate_factory_package(
            repo_root=ROOT,
            descriptor_path=path,
            check_live=False,
        )
        assert first["descriptor"]["normalized_sha256"] == second["descriptor"][
            "normalized_sha256"
        ]
        assert first["descriptor"]["sha256"] == second["descriptor"]["sha256"]


def test_field_inventory_exercises_every_required_classification() -> None:
    inventory = json.loads(
        (ROOT / "schemas/factory_contract_v2/field_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    classifications = {row["classification"] for row in inventory["fields"]}
    assert classifications == {
        "required",
        "variable",
        "optional",
        "forbidden",
        "topic-extension",
        "run-local",
        "evidence-only",
    }
    required_row_keys = {
        "normalized_path",
        "source_artifacts",
        "observed_values",
        "classification",
        "reason",
        "consumer",
        "migration_rule",
        "validation_rule",
        "absence_allowed",
        "affects_content_identity",
        "affects_run_identity",
        "affects_human_or_rights_authority",
    }
    assert all(set(row) == required_row_keys for row in inventory["fields"])


def test_missing_required_section_fails_closed() -> None:
    _expect_error("required_section_missing", lambda row: row.pop("claim_support"))


def test_unknown_unversioned_top_level_field_fails_closed() -> None:
    _expect_error(
        "unknown_top_level_field",
        lambda row: row.__setitem__("episode_specific_switch", True),
    )


def test_private_absolute_path_fails_closed() -> None:
    _expect_error(
        "private_absolute_path_forbidden",
        lambda row: row["source_project"].__setitem__(
            "path", "C:/Users/private/source.local.ymmp"
        ),
    )


def test_silent_human_acceptance_inheritance_fails_closed() -> None:
    accepted = _load(NEW_BANKNOTE)["human_decision"]

    def mutate(row: dict[str, Any]) -> None:
        row["human_decision"] = copy.deepcopy(accepted)

    _expect_error(
        "contradictory_accepted_identity",
        mutate,
        source=REINS,
    )


@pytest.mark.parametrize("clock", ["rights", "production", "publication"])
def test_authority_true_without_record_fails_closed(clock: str) -> None:
    def mutate(row: dict[str, Any]) -> None:
        row["authority"][clock]["approved"] = True

    _expect_error("authority_record_required", mutate)


def test_receipt_only_live_availability_claim_fails_closed() -> None:
    _expect_error(
        "receipt_only_live_availability_claim",
        lambda row: row["generated_project"].__setitem__(
            "availability_claim", "live_file_available"
        ),
    )


def test_cue_without_media_provenance_fails_closed() -> None:
    _expect_error(
        "cue_media_mapping_incomplete",
        lambda row: row["media_provenance"]["asset_mappings"].pop(),
    )


def test_factual_cue_without_claim_partition_fails_closed() -> None:
    _expect_error(
        "claim_cue_coverage_invalid",
        lambda row: row["claim_support"]["factual_cue_ids"].remove("cue_005"),
    )


def test_content_identity_must_exclude_run_local_state() -> None:
    _expect_error(
        "content_identity_pollution_risk",
        lambda row: row["identities"].__setitem__(
            "content_identity_excludes", ["run_id"]
        ),
    )


def test_invalid_namespaced_extension_fails_closed() -> None:
    def mutate(row: dict[str, Any]) -> None:
        row["extensions"]["values"] = {"topic_switch": {"enabled": True}}

    _expect_error("invalid_namespaced_extension", mutate)


def test_bound_v1_hash_mismatch_fails_closed() -> None:
    _expect_error(
        "bound_authority_hash_mismatch",
        lambda row: row["canonical_content"].__setitem__("sha256", "0" * 64),
    )


def test_live_hash_mismatch_fails_closed_when_explicitly_checked() -> None:
    with tempfile.TemporaryDirectory(prefix=".factory-v2-live-", dir=ROOT) as temp:
        live = Path(temp) / "generated_project.local.ymmp"
        live.write_bytes(b"not the receipt artifact")
        relative = live.relative_to(ROOT).as_posix()

        def mutate(row: dict[str, Any]) -> None:
            row["generated_project"]["path"] = relative

        _expect_error(
            "live_artifact_hash_mismatch",
            mutate,
            check_live=True,
        )


def test_known_topic_ids_do_not_appear_in_new_shared_contract_code() -> None:
    source = (ROOT / "src/pipeline/factory_contract_v2.py").read_text(
        encoding="utf-8"
    )
    forbidden_ids = (
        "new_banknote_security_notebooklm_001",
        "real_estate_reins_transparency_001",
        "ai_monitoring_labor_001",
    )
    assert all(value not in source for value in forbidden_ids)


def test_adapter_does_not_mutate_bound_v1_authorities() -> None:
    for descriptor in DESCRIPTORS:
        payload = _load(descriptor)
        bound_paths = (
            payload["source_intake"]["authority_path"],
            payload["claim_support"]["authority_path"],
            payload["canonical_content"]["path"],
            payload["media_provenance"]["path"],
            payload["episode_execution"]["manifest_path"],
            payload["render_validation"]["technical_receipt_path"],
        )
        before = {path: _sha(ROOT / path) for path in bound_paths}
        validate_factory_package(
            repo_root=ROOT,
            descriptor_path=descriptor,
            check_live=False,
        )
        after = {path: _sha(ROOT / path) for path in bound_paths}
        assert after == before


def test_tracked_contract_reports_private_absence_as_availability_not_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_is_file = Path.is_file
    live_suffixes = {
        ".ymmp",
        ".mp4",
    }

    def tracked_only_is_file(path: Path) -> bool:
        if path.suffix.lower() in live_suffixes:
            return False
        return real_is_file(path)

    monkeypatch.setattr(Path, "is_file", tracked_only_is_file)
    result = validate_factory_package(
        repo_root=ROOT,
        descriptor_path=AI_MONITORING,
        check_live=True,
    )
    assert {row["status"] for row in result["availability"]} == {
        "receipt_only_no_live_file"
    }
    assert result["status"] == "passed"


def test_factory_package_cli_is_deterministic_and_non_mutating(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = cli.main(
        [
            "validate-factory-package",
            "--package",
            AI_MONITORING.as_posix(),
            "--format",
            "json",
        ]
    )
    assert rc == 0
    first = json.loads(capsys.readouterr().out)
    rc = cli.main(
        [
            "validate-factory-package",
            "--package",
            AI_MONITORING.as_posix(),
            "--format",
            "json",
        ]
    )
    assert rc == 0
    second = json.loads(capsys.readouterr().out)
    assert first == second
    assert first["boundaries"]["artifacts_mutated"] is False
    assert first["boundaries"]["network_access"] is False
    assert first["boundaries"]["yymm4_launched"] is False
    assert first["boundaries"]["render_performed"] is False
    assert first["boundaries"]["media_playback"] is False


def test_factory_package_dry_run_bridge_uses_existing_pipeline_without_mutation(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    descriptor = _load(AI_MONITORING)
    manifest_path = descriptor["episode_execution"]["manifest_path"]
    protected_paths = (
        AI_MONITORING.as_posix(),
        descriptor["source_intake"]["authority_path"],
        descriptor["claim_support"]["authority_path"],
        descriptor["canonical_content"]["path"],
        descriptor["media_provenance"]["path"],
        manifest_path,
    )
    before = {path: _sha(ROOT / path) for path in protected_paths}
    observed: dict[str, Any] = {}

    def fake_run_episode_video(**kwargs: Any) -> dict[str, Any]:
        observed.update(kwargs)
        return {
            "schema": "nlmytgen.episode_video_run_receipt.v1",
            "status": "dry_run",
            "content_identity_sha256": descriptor["identities"][
                "content_identity_sha256"
            ],
            "render_requested": False,
        }

    monkeypatch.setattr(
        "src.pipeline.episode_video.run_episode_video",
        fake_run_episode_video,
    )
    rc = cli.main(
        [
            "build-episode-video",
            "--factory-package",
            AI_MONITORING.as_posix(),
            "--dry-run",
        ]
    )
    assert rc == 0
    result = json.loads(capsys.readouterr().out)
    assert observed["manifest_path"] == Path(manifest_path)
    assert observed["dry_run"] is True
    assert observed["render"] is False
    assert observed["resume"] is False
    assert observed["force"] is False
    assert result["factory_package_validation"]["status"] == "passed"
    after = {path: _sha(ROOT / path) for path in protected_paths}
    assert after == before


def test_factory_package_bridge_rejects_render_semantics(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = cli.main(
        [
            "build-episode-video",
            "--factory-package",
            AI_MONITORING.as_posix(),
            "--render",
        ]
    )
    assert rc == 1
    error = json.loads(capsys.readouterr().err)
    assert error["error_code"] == "factory_package_dry_run_only"


def test_aggregate_receipt_rejects_fourth_topic_or_universal_overclaim() -> None:
    base = {
        "schema": "nlmytgen.factory_contract_v2_validation_receipt.v1",
        "claims": {
            "universal_arbitrary_topic_compatibility": False,
            "fourth_topic_validated": False,
            "production_ready": False,
        },
    }
    validate_factory_contract_receipt(base)
    for key in base["claims"]:
        row = copy.deepcopy(base)
        row["claims"][key] = True
        with pytest.raises(FactoryContractError) as observed:
            validate_factory_contract_receipt(row)
        assert observed.value.code == "unobserved_axis_overclaim"

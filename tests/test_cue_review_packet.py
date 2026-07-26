from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.pipeline.cue_review_packet import (
    CueReviewPacketError,
    generate_cue_review_packet,
    inspect_cue_review_packet,
    validate_cue_review_packet,
)
from src.pipeline.factory_queue import canonical_json_bytes, sha256_file
from src.pipeline.factory_queue_executor import execute_factory_queue


ROOT = Path(__file__).resolve().parents[1]
QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v3.json"
)
CHANGE_SET = Path(
    "production_pilots/factory_queues/"
    "food_expiry_cue002_review_packet_change_set_v1.json"
)


def load_change_set() -> dict:
    return json.loads((ROOT / CHANGE_SET).read_text(encoding="utf-8"))


def entry() -> dict:
    return load_change_set()["entries"][0]


def inspect(contract: dict | None = None, **overrides: object) -> dict:
    selected = entry()
    values = {
        "repo_root": ROOT,
        "package_id": selected["package_id"],
        "descriptor_path": selected["descriptor_path"],
        "descriptor_sha256": selected["descriptor_sha256"],
        "authority_id": selected["authority_id"],
        "contract": contract or selected["derived_artifact"],
    }
    values.update(overrides)
    return inspect_cue_review_packet(**values)


def assert_code(contract: dict, expected: str, **overrides: object) -> None:
    with pytest.raises(CueReviewPacketError) as observed:
        inspect(contract, **overrides)
    assert observed.value.code == expected


def test_real_cue_binding_resolves_from_all_canonical_evidence() -> None:
    result = inspect()
    assert result["status"] in {"ready", "valid_existing"}
    assert result["cue_id"] == "cue_002"
    assert result["scene_id"] == "S1"
    assert (result["start_frame"], result["end_frame"], result["fps"]) == (
        373,
        816,
        60,
    )
    assert result["materialized_source"]["crop"] == [0.04, 0.34, 0.62, 0.23]
    assert result["materialized_source"]["fit_mode"] == "cover"
    assert result["source_local_availability"] is True


def test_wrong_package_and_wrong_cue_fail_without_writes() -> None:
    selected = entry()
    assert_code(
        selected["derived_artifact"],
        "derived_artifact_wrong_package",
        package_id="another_package",
    )
    contract = copy.deepcopy(selected["derived_artifact"])
    contract["cue_id"] = "cue_999"
    assert_code(contract, "derived_artifact_cue_not_unique")


def test_duplicate_cue_and_text_mismatch_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import src.pipeline.cue_review_packet as module

    original = module._load_json

    def duplicate(path: Path, *, field_path: str):
        payload = original(path, field_path=field_path)
        if field_path == "$.derived_artifact.canonical_script":
            payload["cues"].append(copy.deepcopy(payload["cues"][1]))
        return payload

    monkeypatch.setattr(module, "_load_json", duplicate)
    assert_code(entry()["derived_artifact"], "derived_artifact_cue_not_unique")

    monkeypatch.setattr(module, "_load_json", original)
    contract = copy.deepcopy(entry()["derived_artifact"])
    contract["canonical_text_sha256"] = "0" * 64
    assert_code(contract, "derived_artifact_text_mismatch")


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("start_frame", 374, "derived_artifact_frame_interval_mismatch"),
        ("end_frame", 817, "derived_artifact_frame_interval_mismatch"),
        ("source_id", "wrong-source", "derived_artifact_provenance_mismatch"),
        ("source_sha256", "0" * 64, "derived_artifact_provenance_mismatch"),
        ("crop", [0.0, 0.0, 1.0, 1.0], "derived_artifact_provenance_mismatch"),
        ("fit_mode", "contain", "derived_artifact_crop_recomputation"),
    ],
)
def test_frame_source_provenance_and_crop_drift_fail_before_effect(
    field: str,
    value: object,
    code: str,
) -> None:
    contract = copy.deepcopy(entry()["derived_artifact"])
    contract["expected"][field] = value
    assert_code(contract, code)


def test_generated_project_mp4_and_materialized_source_hash_drift_fail() -> None:
    for field in ("generated_project", "source_mp4", "materialized_source"):
        contract = copy.deepcopy(entry()["derived_artifact"])
        contract[field]["sha256"] = "0" * 64
        assert_code(contract, "derived_artifact_source_hash_mismatch")


@pytest.mark.parametrize(
    "output_root",
    [
        "C:/private/review",
        "../outside",
        "production_pilots/../outside",
        "/absolute/review",
    ],
)
def test_absolute_and_traversal_output_roots_are_rejected(
    output_root: str,
) -> None:
    contract = copy.deepcopy(entry()["derived_artifact"])
    contract["output_root"] = output_root
    assert_code(contract, "derived_artifact_locator_unsafe")


def test_existing_foreign_output_collision_is_rejected(tmp_path: Path) -> None:
    root = ROOT / "_tmp" / f"cue-review-foreign-{tmp_path.name}"
    root.mkdir(parents=True, exist_ok=False)
    try:
        (root / "foreign.txt").write_text("foreign", encoding="utf-8")
        contract = copy.deepcopy(entry()["derived_artifact"])
        contract["output_root"] = root.relative_to(ROOT).as_posix()
        assert_code(contract, "derived_artifact_output_collision")
    finally:
        (root / "foreign.txt").unlink(missing_ok=True)
        root.rmdir()


def test_packet_manifest_private_path_is_rejected(tmp_path: Path) -> None:
    root = ROOT / "_tmp" / f"cue-review-private-{tmp_path.name}"
    root.mkdir(parents=True, exist_ok=False)
    try:
        for name in (
            "cue_002_review_excerpt.mp4",
            "cue_002_render_frame.png",
            "cue_002_materialized_source_view.png",
            "README_REVIEW.md",
        ):
            (root / name).write_bytes(b"x")
        manifest = {
            "private": "C:/Users/private/source.png",
            "outputs": [],
        }
        (root / "packet_manifest.json").write_bytes(
            canonical_json_bytes(manifest)
        )
        with pytest.raises(CueReviewPacketError) as observed:
            validate_cue_review_packet(
                repo_root=ROOT,
                output_root=root.relative_to(ROOT).as_posix(),
                expected={
                    "packet_id": "packet",
                    "package_id": "package",
                    "descriptor_sha256": "0" * 64,
                    "generated_project_sha256": "0" * 64,
                    "source_mp4_sha256": "0" * 64,
                    "cue_id": "cue_002",
                    "canonical_text_sha256": "0" * 64,
                    "authority_id": "authority",
                },
            )
        assert observed.value.code == "packet_manifest_private_path"
    finally:
        for path in root.iterdir():
            path.unlink()
        root.rmdir()


def derived_authority_payload(status: str = "available") -> dict:
    selected = entry()
    change_set = load_change_set()
    artifact = selected["derived_artifact"]
    return {
        "schema": (
            "nlmytgen.factory_queue.execution_authority_set."
            "derived_artifact.v1"
        ),
        "schema_version": "1.0",
        "authorities": [
            {
                "schema": (
                    "nlmytgen.factory_queue.execution_authority."
                    "derived_artifact.v1"
                ),
                "authority_id": selected["authority_id"],
                "replaces_authority_id": None,
                "queue": copy.deepcopy(change_set["queue"]),
                "change_set": {
                    "change_set_id": change_set["change_set_id"],
                    "sha256": sha256_file(ROOT / CHANGE_SET),
                },
                "package": {
                    "package_id": selected["package_id"],
                    "descriptor_path": selected["descriptor_path"],
                    "descriptor_sha256": selected["descriptor_sha256"],
                },
                "from_lifecycle": "rendered",
                "to_lifecycle": "rendered",
                "effect_class": "derived_artifact",
                "operation": "review_packet_generation",
                "derived_artifact": {
                    "cue_id": artifact["cue_id"],
                    "output_root": artifact["output_root"],
                    "generated_project_sha256": artifact[
                        "generated_project"
                    ]["sha256"],
                    "source_mp4_sha256": artifact["source_mp4"]["sha256"],
                },
                "maximum_use_count": 1,
                "status": status,
                "constraints": {
                    "serial_only": True,
                    "exact_identity_recheck": True,
                    "derived_artifact_generation": True,
                    "no_overwrite": True,
                    "lifecycle_transition": False,
                    "content_change": False,
                    "private_artifact_copy": True,
                    "human_acceptance": False,
                    "rights": False,
                    "production": False,
                    "publication": False,
                    "upload": False,
                    "release": False,
                },
            }
        ],
    }


def test_derived_backend_dispatches_once_and_resume_never_redispatches(
    tmp_path: Path,
) -> None:
    local_root = ROOT / "_tmp" / f"cue-review-executor-{tmp_path.name}"
    local_root.mkdir(parents=True, exist_ok=False)
    authority = local_root / "authority.json"
    journal = local_root / "journal.json"
    authority.write_bytes(canonical_json_bytes(derived_authority_payload()))
    calls: list[str] = []

    def backend(**kwargs):
        calls.append(kwargs["change_entry"]["package_id"])
        return {
            "status": "succeeded",
            "effect_performed": True,
            "boundaries": {
                "yymm4_launch_count": 0,
                "render_driver_launch_count": 0,
                "ffmpeg_encode_count": 1,
                "playback_count": 0,
            },
        }

    try:
        first = execute_factory_queue(
            repo_root=ROOT,
            queue_path=QUEUE,
            change_set_path=CHANGE_SET,
            authority_path=authority.relative_to(ROOT),
            execute=True,
            derived_artifact_backend=backend,
        )
        assert calls == ["food_expiry_labels_001"]
        assert first["journal"]["counts"]["authority_consumptions"] == 1
        assert first["journal"]["counts"]["succeeded"] == 1
        assert first["journal"]["boundaries"]["render_count"] == 0
        assert first["journal"]["boundaries"]["yymm4_launch_count"] == 0
        journal.write_bytes(canonical_json_bytes(first["journal"]))
        before = authority.read_bytes()
        resumed = execute_factory_queue(
            repo_root=ROOT,
            queue_path=QUEUE,
            change_set_path=CHANGE_SET,
            authority_path=authority.relative_to(ROOT),
            execute=True,
            resume_journal_path=journal.relative_to(ROOT),
            derived_artifact_backend=backend,
        )
        assert calls == ["food_expiry_labels_001"]
        assert resumed["journal"]["counts"]["authority_consumptions"] == 1
        assert authority.read_bytes() == before
    finally:
        authority.unlink(missing_ok=True)
        journal.unlink(missing_ok=True)
        local_root.rmdir()


def test_wrong_or_consumed_derived_authority_fails_before_dispatch(
    tmp_path: Path,
) -> None:
    local_root = ROOT / "_tmp" / f"cue-review-authority-{tmp_path.name}"
    local_root.mkdir(parents=True, exist_ok=False)
    authority = local_root / "authority.json"
    calls: list[str] = []

    def backend(**_kwargs):
        calls.append("called")
        return {"status": "succeeded", "effect_performed": True}

    try:
        wrong = derived_authority_payload()
        wrong["authorities"][0]["derived_artifact"]["cue_id"] = "cue_003"
        authority.write_bytes(canonical_json_bytes(wrong))
        with pytest.raises(Exception) as observed:
            execute_factory_queue(
                repo_root=ROOT,
                queue_path=QUEUE,
                change_set_path=CHANGE_SET,
                authority_path=authority.relative_to(ROOT),
                execute=True,
                derived_artifact_backend=backend,
            )
        assert getattr(observed.value, "code", "") == (
            "authority_derived_artifact_mismatch"
        )
        consumed = derived_authority_payload(status="consumed")
        authority.write_bytes(canonical_json_bytes(consumed))
        with pytest.raises(Exception) as observed:
            execute_factory_queue(
                repo_root=ROOT,
                queue_path=QUEUE,
                change_set_path=CHANGE_SET,
                authority_path=authority.relative_to(ROOT),
                execute=True,
                derived_artifact_backend=backend,
            )
        assert getattr(observed.value, "code", "") == "authority_status_mismatch"
        assert calls == []
    finally:
        authority.unlink(missing_ok=True)
        local_root.rmdir()


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("lifecycle", "change_set_lifecycle_edge_mismatch"),
        ("content", "change_set_content_identity_mismatch"),
    ],
)
def test_derived_change_set_rejects_lifecycle_and_content_smuggling(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    local_root = ROOT / "_tmp" / f"cue-review-smuggling-{tmp_path.name}"
    local_root.mkdir(parents=True, exist_ok=False)
    change_set_path = local_root / f"{mutation}.json"
    payload = load_change_set()
    if mutation == "lifecycle":
        payload["entries"][0]["requested_target_lifecycle"] = "human_accepted"
    else:
        payload["entries"][0]["expected_content_identity_sha256"] = "0" * 64
    change_set_path.write_bytes(canonical_json_bytes(payload))
    try:
        with pytest.raises(Exception) as observed:
            execute_factory_queue(
                repo_root=ROOT,
                queue_path=QUEUE,
                change_set_path=change_set_path.relative_to(ROOT),
                execute=False,
            )
        assert getattr(observed.value, "code", "") == expected_code
    finally:
        change_set_path.unlink(missing_ok=True)
        local_root.rmdir()


def test_generation_refuses_valid_existing_packet_without_media_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import src.pipeline.cue_review_packet as module

    monkeypatch.setattr(
        module,
        "inspect_cue_review_packet",
        lambda **_kwargs: {"status": "valid_existing"},
    )
    with pytest.raises(CueReviewPacketError) as observed:
        generate_cue_review_packet(
            repo_root=ROOT,
            package_id="food_expiry_labels_001",
            descriptor_path="unused",
            descriptor_sha256="0" * 64,
            authority_id="authority",
            contract={},
        )
    assert observed.value.code == "derived_artifact_overwrite_forbidden"

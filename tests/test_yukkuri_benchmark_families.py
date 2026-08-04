import copy
from pathlib import Path

from src.pipeline.yukkuri_benchmark_families import (
    DEFAULT_REGISTRY_PATH,
    REGISTRY_ID,
    SCHEMA_VERSION,
    load_registry,
    validate_registry,
)


ROOT = Path(__file__).resolve().parents[1]


def _registry() -> dict:
    return load_registry(ROOT / DEFAULT_REGISTRY_PATH)


def test_registry_locks_six_unique_channels_and_format_families() -> None:
    registry = _registry()
    result = validate_registry(registry, root=ROOT)

    assert result == {
        "registry_id": REGISTRY_ID,
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "errors": [],
        "channel_count": 6,
        "unique_channel_count": 6,
        "unique_format_family_count": 6,
        "local_viewable_verified_count": 1,
        "remaining_local_viewable_count": 5,
        "local_production_authorized": True,
        "public_release_authorized": False,
    }


def test_registry_preserves_copy_and_release_boundaries() -> None:
    registry = _registry()

    assert all(registry["no_copy_policy"].values())
    assert registry["current_gate"]["status"] == "CONTINUE"
    assert registry["authority"]["local_production_authorized"] is True
    assert registry["authority"]["publication_authorized"] is False
    assert registry["current_gate"]["local_production_authorized"] is True
    assert registry["current_gate"]["publication_authorized"] is False
    assert {
        channel["reproduction"]["status"] for channel in registry["channels"]
    } == {
        "channel_identity_locked_measurement_pending",
        "local_viewable_verified",
    }


def test_validator_rejects_duplicate_families_and_false_copy_boundary() -> None:
    registry = copy.deepcopy(_registry())
    registry["channels"][1]["format_family_id"] = registry["channels"][0][
        "format_family_id"
    ]
    registry["no_copy_policy"]["scripts"] = False

    result = validate_registry(registry)

    assert result["status"] == "failed"
    assert "format_family_id values must be unique" in result["errors"]
    assert "no_copy_policy.scripts must be true" in result["errors"]


def test_local_viewable_status_requires_exact_artifact_receipt() -> None:
    registry = copy.deepcopy(_registry())
    registry["channels"][3]["reproduction"]["artifact"] = None

    result = validate_registry(registry, root=ROOT)

    assert result["status"] == "failed"
    assert result["local_viewable_verified_count"] == 1
    assert "channels[3].reproduction.artifact is required" in result["errors"]


def test_local_viewable_status_rejects_wrong_live_artifact_sha() -> None:
    registry = copy.deepcopy(_registry())
    registry["channels"][3]["reproduction"]["artifact"]["sha256"] = "0" * 64

    result = validate_registry(registry, root=ROOT)

    assert result["status"] == "failed"
    assert "channels[3].reproduction.artifact sha256 mismatch" in result["errors"]


def test_local_viewable_status_can_read_back_tracked_receipt_without_local_media(
    tmp_path: Path,
) -> None:
    registry = copy.deepcopy(_registry())
    artifact = registry["channels"][3]["reproduction"]["artifact"]
    receipt_path = Path(artifact["receipt"])
    copied_receipt = tmp_path / receipt_path
    copied_receipt.parent.mkdir(parents=True)
    copied_receipt.write_text(
        (ROOT / receipt_path).read_text(encoding="utf-8"), encoding="utf-8"
    )

    result = validate_registry(registry, root=tmp_path)

    assert result["status"] == "passed"
    assert result["local_viewable_verified_count"] == 1

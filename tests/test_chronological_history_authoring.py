import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODE = (
    ROOT
    / "production_pilots/yukkuri_benchmark_families_001/episodes/history_japan_standard_time_001"
)
REGISTRY = (
    ROOT
    / "production_pilots/yukkuri_benchmark_families_001/benchmark_families.json"
)


def test_history_measurement_is_bounded_and_matches_registry_contract() -> None:
    measurement = json.loads(
        (EPISODE / "benchmark_measurement.json").read_text(encoding="utf-8")
    )
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    family = next(
        channel
        for channel in registry["channels"]
        if channel["format_family_id"] == "chronological_history_reconstruction"
    )

    assert measurement["representative_video"]["duration_seconds"] is None
    assert measurement["surface_observation"]["duration_observed"] is False
    assert measurement["surface_observation"]["full_timeline_frame_verified"] is False
    assert measurement["surface_observation"]["audio_subject_verified"] is False
    assert all(
        value is False
        for key, value in measurement["copy_boundary"].items()
        if key.endswith("_used") or key.endswith("_reused")
    )
    assert family["observable_contract"] == measurement["measured_contract"]
    assert family["reproduction"] == {
        "status": "channel_identity_locked_measurement_pending",
        "artifact": None,
    }


def test_history_script_is_original_alternating_chronology() -> None:
    lines = [
        line
        for line in (EPISODE / "script.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert len(lines) == 32
    assert all(
        line.startswith(f"スピーカー{1 if index % 2 == 0 else 2}:")
        for index, line in enumerate(lines)
    )
    joined = "\n".join(lines)
    for required in (
        "一八八四年",
        "一八八六年",
        "一八八八年",
        "一九三七年",
        "東経百三十五度",
        "情報通信研究機構",
    ):
        assert required in joined
    assert "硫黄島" not in joined


def test_history_sources_keep_media_and_authority_boundaries() -> None:
    sources = json.loads(
        (EPISODE / "source_registry.json").read_text(encoding="utf-8")
    )

    assert {source["source_id"] for source in sources["sources"]} == {
        "NICT-JST-HISTORY",
        "NAOJ-STANDARD-TIME-HISTORY",
        "AKASHI-STANDARD-MERIDIAN",
    }
    assert sources["rights"] == {
        "benchmark_media_reused": False,
        "source_media_reused": False,
        "episode_script_original": True,
        "visual_carrier_original": False,
        "internal_review_only": True,
        "human_acceptance": "unverified",
        "production_authorized": False,
        "publication_authorized": False,
    }


def test_history_execution_state_binds_the_tracked_authoring_identity() -> None:
    state = json.loads(
        (EPISODE / "execution_state.json").read_text(encoding="utf-8")
    )
    identity = state["authoring_identity"]

    for path_key, hash_key in (
        ("benchmark_measurement_path", "benchmark_measurement_sha256"),
        ("source_registry_path", "source_registry_sha256"),
        ("script_path", "script_sha256"),
    ):
        payload = (EPISODE / identity[path_key]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == identity[hash_key]

    assert state["state"] == "original_authoring_pack_verified_render_pending"
    assert state["csv_receipt"]["tracked"] is False
    assert state["csv_receipt"]["row_count"] == 97
    assert state["csv_receipt"]["overflow_candidates"] == 0
    assert state["completed"]["local_render_completed"] is False
    assert state["authority"]["human_acceptance"] == "unverified"
    assert state["authority"]["publication_authorized"] is False

import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_offline_topic_mini_episode_materialization import (
    BEAT_COUNT,
    BEAT_DURATION_FRAMES,
    DEFAULT_MATERIALIZATION_DOC_PATH,
    DEFAULT_MATERIALIZATION_PATH,
    DEFAULT_ROUTE_PATH,
    LOCAL_IGNORED_MATERIALIZED_YMMP_PATH,
    NEXT_AXIS_PREVIEW,
    TIMELINE_LENGTH_FRAMES,
    build_default_materialization_readback,
    build_default_materialization_route,
    render_materialization_markdown,
    write_default_newsroom_offline_topic_mini_episode_materialization_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_topic_mini_episode_materialization_artifacts(
        root=ROOT
    )


def test_route_is_current_supported_and_does_not_use_fake_packet_route() -> None:
    _ensure_artifacts()
    route = _load(DEFAULT_ROUTE_PATH)
    expected = build_default_materialization_route(root=ROOT)

    assert route == expected
    assert route["route_classification"] == "current_supported"
    assert route["route_confidence"] == "high"
    assert route["source_capsule_path"].endswith(
        "offline_topic_mini_episode_capsule_with_animation_accent_v1.json"
    )
    stale = route["stale_fake_packet_route_classification"]
    assert stale["classification"] == "stale_fake_packet_only"
    assert stale["used_for_materialization"] is False
    assert route["route_blockers"] == []
    assert "TextItem role" in route["item_semantics"]


def test_materialization_artifact_matches_builder_and_selects_preview() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_MATERIALIZATION_PATH)
    expected = build_default_materialization_readback(root=ROOT)

    assert materialization == expected
    assert materialization["production_status"] == "diagnostic_only"
    assert materialization["render_gate"] == "L0_no_render"
    assert materialization["local_ymmp_materialization_status"] == (
        "materialized_ignored_local_probe"
    )
    assert materialization["selected_next_axis"] == NEXT_AXIS_PREVIEW


def test_local_ymmp_exists_is_ignored_and_has_expected_counts() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_MATERIALIZATION_PATH)
    access = materialization["local_probe_access_state"]
    readback = materialization["materialization_readback"]

    assert (ROOT / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH).exists()
    assert access["repo_relative_path"] == LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert readback["readback_status"] == "structural_pass"
    assert readback["item_type_counts"] == {
        "TextItem": 5,
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["beat_count"] == BEAT_COUNT
    assert readback["text_item_count"] == BEAT_COUNT
    assert readback["animation_item_count"] == 16
    assert readback["duration_frames"] == TIMELINE_LENGTH_FRAMES
    assert readback["fps"] == 60

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_ymmp_timeline_has_five_text_items_and_no_card_or_media_items() -> None:
    _ensure_artifacts()
    data = load_ymmp(ROOT / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH)
    items = _get_timeline_items(data)
    text_items = [item for item in items if _item_type(item) == "TextItem"]
    non_text_animation = [
        item for item in items if _item_type(item) in {"GroupItem", "ImageItem"}
    ]

    assert len(text_items) == BEAT_COUNT
    assert len(non_text_animation) == 16
    assert {item["Frame"] for item in text_items} == {
        index * BEAT_DURATION_FRAMES for index in range(BEAT_COUNT)
    }
    assert all(item["Length"] == BEAT_DURATION_FRAMES for item in text_items)
    assert all(item["Remark"].startswith("offline_topic_mini_episode:text:") for item in text_items)
    assert not [item for item in items if _item_type(item) in {"ShapeItem", "AudioItem", "VideoItem"}]


def test_per_beat_mapping_respects_animation_assignments_and_boundaries() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_MATERIALIZATION_PATH)
    per_beat = materialization["materialization_readback"]["per_beat_mapping"]

    assert [row["start_frame"] for row in per_beat] == [
        index * BEAT_DURATION_FRAMES for index in range(BEAT_COUNT)
    ]
    assert all(row["duration_frames"] == BEAT_DURATION_FRAMES for row in per_beat)
    assert all(row["text_item_present"] for row in per_beat)
    assert [row["animation_accent_assignment"] for row in per_beat] == [
        "stable_pose_only",
        "expression_event",
        "expression_plus_short_nod",
        "short_nod_reaction",
        "none",
    ]
    assert [row["animation_item_count"] for row in per_beat] == [4, 4, 4, 4, 0]
    assert all(row["parent_x_values"] in ([], [-96.0]) for row in per_beat)
    assert per_beat[2]["head_rotation_values"] == [0.0, -8.0, 0.0]
    assert per_beat[4]["head_rotation_values"] == []


def test_capsule_acceptance_readback_keeps_scope_diagnostic() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_MATERIALIZATION_PATH)
    acceptance = materialization["capsule_acceptance_readback"]
    boundaries = materialization["boundaries"]

    assert acceptance["five_beats_are_represented"] is True
    assert acceptance["text_role_exists_per_beat"] is True
    assert acceptance["animation_accent_remains_subordinate"] is True
    assert acceptance["no_body_forward_back_default"] is True
    assert acceptance["no_mechanical_expression_cycling"] is True
    assert acceptance["no_card_polish"] is True
    assert acceptance["no_render_export"] is True
    assert acceptance["no_live_fetch"] is True
    assert acceptance["no_production_claim"] is True

    assert boundaries["network_fetch_performed"] is False
    assert boundaries["live_RSS_news_fetch_performed"] is False
    assert boundaries["YMM4_launched_by_agent"] is False
    assert boundaries["render_performed_by_agent"] is False
    assert boundaries["audio_tts_generated"] is False
    assert boundaries["card_redesign_performed"] is False
    assert boundaries["animation_tuned"] is False
    assert boundaries["ymmp_or_media_staged_or_committed"] is False
    assert boundaries["stale_fake_packet_route_used_as_current"] is False


def test_doc_matches_renderer_and_tracked_outputs_are_not_media() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_MATERIALIZATION_PATH)
    assert (ROOT / DEFAULT_MATERIALIZATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_materialization_markdown(materialization)

    generated_paths = [
        DEFAULT_ROUTE_PATH,
        DEFAULT_MATERIALIZATION_PATH,
        DEFAULT_MATERIALIZATION_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http://" not in combined
    assert "https://" not in combined
    assert '"YMM4_launched_by_agent": true' not in combined
    assert '"render_performed_by_agent": true' not in combined
    assert '"audio_tts_generated": true' not in combined

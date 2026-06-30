import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_offline_topic_mini_episode_readable_text_materialization import (
    BEAT_COUNT,
    BEAT_DURATION_FRAMES,
    DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_PREVIEW_OBSERVATION_PATH,
    DEFAULT_READABLE_MATERIALIZATION_DOC_PATH,
    DEFAULT_READABLE_MATERIALIZATION_PATH,
    LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH,
    NEXT_AXIS_READABLE_PREVIEW,
    READABLE_BEAT_LINES,
    USER_VISIBLE_DEBUG_LABELS,
    build_default_preview_observation,
    build_default_readable_text_materialization,
    render_preview_observation_markdown,
    render_readable_text_materialization_markdown,
    write_default_newsroom_offline_topic_mini_episode_readable_text_artifacts,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    _get_timeline_items,
    _item_type,
)
from src.pipeline.ymmp_patch import load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_topic_mini_episode_readable_text_artifacts(
        root=ROOT
    )


def test_preview_observation_records_v1_debug_label_gap() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)
    expected = build_default_preview_observation(root=ROOT)

    assert observation == expected
    normalized = observation["normalized_preview_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["five_textitems_visible"] is True
    assert normalized["five_textitems_sequential"] is True
    assert normalized["animation_accent_not_disruptive"] is True
    assert normalized["episode_route_materialization_status"] == "pass_with_boundary"
    assert normalized["visible_text_is_debug_label"] is True
    assert normalized["human_readable_explanation_text_visible"] is False
    assert normalized["visible_screen_notes"] == list(USER_VISIBLE_DEBUG_LABELS)
    assert observation["issue_classification"]["screen_facing_text"] == (
        "debug_label_visible_not_human_readable"
    )

    readback = observation["v1_debug_label_readback"]
    assert readback["text_item_count"] == BEAT_COUNT
    assert readback["remark_debug_label_count"] == BEAT_COUNT
    assert readback["user_observed_debug_label_count"] == BEAT_COUNT
    assert readback["classification"] == "screen_visible_debug_label_from_user_preview"


def test_readable_materialization_artifact_matches_builder_and_selects_preview() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_READABLE_MATERIALIZATION_PATH)
    expected = build_default_readable_text_materialization(root=ROOT)

    assert materialization == expected
    assert materialization["production_status"] == "diagnostic_only"
    assert materialization["render_gate"] == "L0_no_render"
    assert materialization["source_route_classification"] == "current_supported"
    assert materialization["local_ymmp_materialization_status"] == (
        "materialized_ignored_local_probe"
    )
    assert materialization["selected_next_axis"] == NEXT_AXIS_READABLE_PREVIEW
    assert materialization["language_policy"]["selected_language"] == "english"


def test_local_v2_ymmp_exists_is_ignored_and_has_required_readback_counts() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_READABLE_MATERIALIZATION_PATH)
    access = materialization["local_probe_access_state"]
    readback = materialization["materialization_readback"]

    assert (ROOT / LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH).exists()
    assert access["repo_relative_path"] == LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert readback["readback_status"] == "readable_text_pass"
    assert readback["item_type_counts"] == {
        "TextItem": 5,
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["beat_count"] == BEAT_COUNT
    assert readback["text_item_count"] == BEAT_COUNT
    assert readback["debug_label_visible_count"] == 0
    assert readback["human_readable_text_item_count"] == BEAT_COUNT
    assert readback["animation_item_count"] == 16
    assert readback["duration_frames"] == BEAT_DURATION_FRAMES * BEAT_COUNT
    assert readback["fps"] == 60

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix(),
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


def test_v2_ymmp_textitems_use_readable_text_in_text_and_remark_fields() -> None:
    _ensure_artifacts()
    data = load_ymmp(ROOT / LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH)
    items = _get_timeline_items(data)
    text_items = sorted(
        [item for item in items if _item_type(item) == "TextItem"],
        key=lambda item: item["Frame"],
    )
    visible_lines = [row["visible_text"] for row in READABLE_BEAT_LINES]

    assert [item["Text"] for item in text_items] == visible_lines
    assert [item["Remark"] for item in text_items] == visible_lines
    assert all(not item["Text"].startswith("offline_topic_mini_episode:text:") for item in text_items)
    assert all(not item["Remark"].startswith("offline_topic_mini_episode:text:") for item in text_items)
    assert [item["Frame"] for item in text_items] == [
        index * BEAT_DURATION_FRAMES for index in range(BEAT_COUNT)
    ]
    assert all(item["Length"] == BEAT_DURATION_FRAMES for item in text_items)
    assert not [item for item in items if _item_type(item) in {"ShapeItem", "AudioItem", "VideoItem"}]


def test_per_beat_mapping_preserves_animation_assignments_and_boundaries() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_READABLE_MATERIALIZATION_PATH)
    per_beat = materialization["materialization_readback"]["per_beat_mapping"]

    assert [row["visible_text"] for row in per_beat] == [
        row["visible_text"] for row in READABLE_BEAT_LINES
    ]
    assert all(row["text_item_present"] for row in per_beat)
    assert all(row["text_is_human_readable"] for row in per_beat)
    assert [row["start_frame"] for row in per_beat] == [
        index * BEAT_DURATION_FRAMES for index in range(BEAT_COUNT)
    ]
    assert all(row["duration_frames"] == BEAT_DURATION_FRAMES for row in per_beat)
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


def test_acceptance_and_boundaries_keep_scope_diagnostic() -> None:
    _ensure_artifacts()
    materialization = _load(DEFAULT_READABLE_MATERIALIZATION_PATH)
    acceptance = materialization["acceptance_readback"]
    boundaries = materialization["boundaries"]

    assert acceptance["five_beats_are_represented"] is True
    assert acceptance["TextItem_exists_per_beat"] is True
    assert acceptance["visible_text_is_human_readable"] is True
    assert acceptance["debug_labels_are_not_main_visible_content"] is True
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


def test_docs_match_renderers_and_tracked_outputs_are_not_media() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)
    materialization = _load(DEFAULT_READABLE_MATERIALIZATION_PATH)

    assert (ROOT / DEFAULT_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_READABLE_MATERIALIZATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_readable_text_materialization_markdown(materialization)

    generated_paths = [
        DEFAULT_PREVIEW_OBSERVATION_PATH,
        DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
        DEFAULT_READABLE_MATERIALIZATION_PATH,
        DEFAULT_READABLE_MATERIALIZATION_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http://" not in combined
    assert "https://" not in combined
    assert '"YMM4_launched_by_agent": true' not in combined
    assert '"render_performed_by_agent": true' not in combined
    assert '"audio_tts_generated": true' not in combined

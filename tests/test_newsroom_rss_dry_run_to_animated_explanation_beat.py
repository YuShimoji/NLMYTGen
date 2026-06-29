import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_minimal_animated_explanation_beat_visual_gap_fix import (
    LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_CONTRACT_PATH,
    DEFAULT_RSS_DRY_RUN_DOC_PATH,
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
    DRY_RUN_TOPIC_INPUT,
    EXPLANATION_LINE,
    LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
    NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION,
    build_default_rss_dry_run_animated_explanation_beat_contract,
    build_default_rss_dry_run_topic_to_animated_explanation_beat,
    materialize_local_rss_dry_run_animated_explanation_beat,
    render_rss_dry_run_markdown,
    write_default_newsroom_rss_dry_run_to_animated_explanation_beat_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_rss_dry_run_to_animated_explanation_beat_artifacts(root=ROOT)


def _animation_items(path: Path) -> list[dict]:
    data = load_ymmp(ROOT / path)
    return [
        item
        for item in _get_timeline_items(data)
        if _item_type(item) in {"GroupItem", "ImageItem"}
    ]


def _text_items(path: Path) -> list[dict]:
    data = load_ymmp(ROOT / path)
    return [
        item
        for item in _get_timeline_items(data)
        if _item_type(item) == "TextItem"
    ]


def test_visual_integration_observation_and_offline_topic_are_recorded() -> None:
    _ensure_artifacts()
    payload = build_default_rss_dry_run_topic_to_animated_explanation_beat(root=ROOT)
    artifact = _load(DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["actual_audience_acceptance_claimed"] is False

    observation = artifact["visual_integration_observation"]
    assert observation["yym4_opened"] is True
    assert observation["explanation_text_visible"] is True
    assert observation["animation_accent_visible"] is True
    assert observation["same_scene_co_presence"] is True
    assert observation["card_like_overlay_visible"] is False
    assert observation["visual_integration_status"] == "pass_with_boundary"

    topic = artifact["dry_run_topic_input"]
    assert topic == DRY_RUN_TOPIC_INPUT
    assert topic["topic_id"] == "offline_rss_like_topic_fixture_001"
    assert topic["source_kind"] == "offline_fixture_or_diagnostic"
    assert "live RSS" in topic["boundary_note"]


def test_topic_transforms_into_one_animated_explanation_beat() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)

    transformation = artifact["topic_to_beat_transformation"]
    assert transformation["source_topic_id"] == DRY_RUN_TOPIC_INPUT["topic_id"]
    assert transformation["derived_explanation_line"] == EXPLANATION_LINE
    assert transformation["network_fetch_performed"] is False
    assert transformation["live_RSS_or_news_used"] is False

    beat = artifact["animated_explanation_beat"]
    assert beat["beat_id"] == "rss_dry_run_animated_explanation_beat_v1"
    assert beat["source_topic_id"] == DRY_RUN_TOPIC_INPUT["topic_id"]
    assert beat["explanation_line"] == EXPLANATION_LINE
    assert beat["subtitle_or_text_role"].startswith("plain diagnostic TextItem")
    assert beat["minimal_overlay_role"] == "plain TextItem diagnostic label; no designed card"
    assert "frozen MVP accent" in beat["background_animation_accent_role"]
    assert beat["YMM4_representation_candidate"]["textitem_count"] == 1
    assert beat["YMM4_representation_candidate"]["animation_item_count"] == 16
    assert beat["local_probe_status"] == "materialized_ignored_local_probe"


def test_local_probe_reuses_v2_animation_and_replaces_only_textitem() -> None:
    _ensure_artifacts()
    materialize_local_rss_dry_run_animated_explanation_beat(root=ROOT)

    assert _animation_items(LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH) == (
        _animation_items(LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH)
    )
    text_items = _text_items(LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH)
    assert len(text_items) == 1
    assert text_items[0]["Text"] == EXPLANATION_LINE
    assert text_items[0]["Length"] >= 720
    assert text_items[0]["IsHidden"] is False


def test_local_probe_is_ignored_and_readback_accessible() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)
    access = artifact["local_probe_access_state"]
    readback = artifact["local_probe_readback"]

    assert (ROOT / LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH).exists()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert access["artifact_scope"] == "ignored_local_only"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert access["visible_text_or_overlay_item_count"] == 1
    assert access["animation_item_count"] == 16

    assert readback["actual_item_type_counts"] == {
        "TextItem": 1,
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["visible_texts"] == [EXPLANATION_LINE]
    assert readback["YMM4_launch_status"] == "not_launched"
    assert readback["render_status"] == "not_rendered"
    assert readback["audio_tts_status"] == "not_created"

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix(),
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


def test_contract_and_business_boundaries_stay_diagnostic() -> None:
    _ensure_artifacts()
    proof = _load(DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)
    contract = build_default_rss_dry_run_animated_explanation_beat_contract(root=ROOT)
    artifact = _load(DEFAULT_RSS_DRY_RUN_CONTRACT_PATH)

    assert artifact == contract
    assert artifact["proof_id"] == proof["artifact_id"]
    assert artifact["selected_next_axis"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
    assert artifact["overlay_card_policy"]["designed_card_created"] is False
    assert artifact["overlay_card_policy"]["production_subtitle_design_claimed"] is False

    outcome = artifact["business_goal_outcome_contract"]
    assert outcome["problem_clear"]["status"] is True
    assert outcome["offer_clear"]["status"] is True
    assert outcome["proof_clear"]["status"] is True
    assert outcome["boundary_clear"]["status"] is True
    assert outcome["next_action_clear"]["rationale"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
    assert outcome["visual_supports_explanation"]["status"] is True

    boundaries = artifact["boundaries"]
    assert boundaries["network_fetch_performed"] is False
    assert boundaries["live_RSS_news_fetch_performed"] is False
    assert boundaries["YMM4_launched_by_agent"] is False
    assert boundaries["render_performed_by_agent"] is False
    assert boundaries["audio_tts_generated"] is False
    assert boundaries["card_redesign_performed"] is False
    assert boundaries["animation_tuned"] is False
    assert boundaries["animation_only_probe_created"] is False
    assert boundaries["ymmp_or_media_staged_or_committed"] is False


def test_markdown_output_matches_renderer() -> None:
    _ensure_artifacts()
    proof = _load(DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH)
    assert (ROOT / DEFAULT_RSS_DRY_RUN_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_rss_dry_run_markdown(proof)


def test_outputs_do_not_request_forbidden_followups_or_track_media() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
        ROOT / DEFAULT_RSS_DRY_RUN_DOC_PATH,
        ROOT / DEFAULT_RSS_DRY_RUN_CONTRACT_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)
    combined_lower = combined.lower()

    assert "http://" not in combined
    assert "https://" not in combined
    assert "fetch live" not in combined_lower
    assert "fetch real" not in combined_lower
    assert "render again" not in combined_lower
    assert "launch ymm4 now" not in combined_lower
    assert "create audio" not in combined_lower
    assert "generate tts" not in combined_lower
    assert "tune nod" not in combined_lower
    assert "redesign card" not in combined_lower

    tracked_forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in tracked_forbidden_suffixes for path in generated_paths)

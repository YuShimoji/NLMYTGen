import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_minimal_animated_explanation_beat import (
    LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
)
from src.pipeline.newsroom_minimal_animated_explanation_beat_visual_gap_fix import (
    DEFAULT_PREVIEW_GAP_DOC_PATH,
    DEFAULT_PREVIEW_GAP_PATH,
    DEFAULT_VISUAL_GAP_FIX_DOC_PATH,
    DEFAULT_VISUAL_GAP_FIX_PATH,
    LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
    NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION,
    VISIBLE_DIAGNOSTIC_TEXT,
    build_default_preview_gap,
    build_default_visual_gap_fix,
    materialize_local_v2_visible_integration_probe,
    render_preview_gap_markdown,
    render_visual_gap_fix_markdown,
    write_default_newsroom_minimal_animated_explanation_beat_visual_gap_fix_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_minimal_animated_explanation_beat_visual_gap_fix_artifacts(root=ROOT)


def _animation_items(path: Path) -> list[dict]:
    data = load_ymmp(ROOT / path)
    return [
        item
        for item in _get_timeline_items(data)
        if _item_type(item) in {"GroupItem", "ImageItem"}
    ]


def test_preview_gap_records_v1_actual_vs_claim_failure() -> None:
    _ensure_artifacts()
    payload = build_default_preview_gap(root=ROOT)
    artifact = _load(DEFAULT_PREVIEW_GAP_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["actual_audience_acceptance_claimed"] is False

    observation = artifact["user_observation"]
    assert observation["yym4_opened"] is True
    assert observation["character_animation_visible"] is True
    assert observation["nod_visible"] is True
    assert observation["card_or_overlay_visible"] is False
    assert observation["mainline_integration_gap"] is True

    readback = artifact["actual_v1_readback"]
    assert readback["actual_item_type_counts"] == {
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["TextItem_count"] == 0
    assert readback["ShapeItem_count"] == 0
    assert readback["visible_text_or_overlay_item_count"] == 0
    assert readback["visible_TextItem_subtitle_card_or_overlay_exists"] is False

    root_cause = artifact["root_cause_classification"]
    assert root_cause["primary"] == "contract_only_not_materialized"
    assert "overlay_role_readback_only" in root_cause["contributing"]


def test_v2_probe_adds_one_plain_visible_textitem() -> None:
    _ensure_artifacts()
    payload = build_default_visual_gap_fix(root=ROOT)
    artifact = _load(DEFAULT_VISUAL_GAP_FIX_PATH)

    assert artifact == payload
    assert artifact["selected_next_axis"] == NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION

    probe = artifact["v2_visible_integration_probe"]
    assert probe["repo_relative_path"] == LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix()
    assert probe["target_exists"] is True
    assert probe["access_state"] == "verified_present"
    assert probe["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert probe["artifact_scope"] == "ignored_local_only"
    assert probe["git_check_ignore_result"]["ignored"] is True
    assert probe["visible_text_or_overlay_item_count"] == 1
    assert probe["animation_item_count"] == 16
    assert probe["materialization_status"] == "materialized_ignored_local_probe"

    readback = artifact["v2_readback"]
    assert readback["readback_status"] == "structural_pass"
    assert readback["actual_item_type_counts"] == {
        "TextItem": 1,
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["TextItem_count"] == 1
    assert readback["ShapeItem_count"] == 0
    assert readback["visible_text_item_count"] == 1
    assert readback["visible_shape_item_count"] == 0
    assert readback["visible_texts"] == [VISIBLE_DIAGNOSTIC_TEXT]
    assert readback["YMM4_launch_status"] == "not_launched"
    assert readback["render_status"] == "not_rendered"
    assert readback["audio_tts_status"] == "not_created"


def test_v2_does_not_tune_animation_items() -> None:
    _ensure_artifacts()
    materialize_local_v2_visible_integration_probe(root=ROOT)
    assert _animation_items(LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH) == _animation_items(
        LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH
    )


def test_v2_probe_is_ignored_local_output() -> None:
    _ensure_artifacts()
    assert (ROOT / LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH).exists()
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix(),
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


def test_business_goal_and_boundaries_stay_diagnostic() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_VISUAL_GAP_FIX_PATH)
    contract = artifact["business_goal_outcome_contract"]

    assert contract["problem_clear"]["status"] is True
    assert contract["offer_clear"]["status"] is True
    assert contract["proof_clear"]["status"] is True
    assert contract["boundary_clear"]["status"] is True
    assert contract["next_action_clear"]["rationale"] == NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION
    assert contract["visual_supports_explanation"]["status"] == "ready_for_one_preview"

    boundaries = artifact["boundaries"]
    assert boundaries["YMM4_launched_by_agent"] is False
    assert boundaries["render_performed_by_agent"] is False
    assert boundaries["audio_tts_generated"] is False
    assert boundaries["card_redesign_performed"] is False
    assert boundaries["animation_tuned"] is False
    assert boundaries["local_ignored_ymmp_created_in_this_slice"] is True
    assert boundaries["ymmp_or_media_staged_or_committed"] is False

    not_accepted = artifact["not_accepted_scope"]
    assert not_accepted["production_animation_quality"] is False
    assert not_accepted["render_export_proof"] is False
    assert not_accepted["real_RSS_news_integration"] is False
    assert not_accepted["polished_visual_card"] is False


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    preview_gap = _load(DEFAULT_PREVIEW_GAP_PATH)
    visual_fix = _load(DEFAULT_VISUAL_GAP_FIX_PATH)

    assert (ROOT / DEFAULT_PREVIEW_GAP_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_preview_gap_markdown(preview_gap)
    assert (ROOT / DEFAULT_VISUAL_GAP_FIX_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_visual_gap_fix_markdown(visual_fix)


def test_outputs_do_not_track_forbidden_media_or_request_render() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_PREVIEW_GAP_PATH,
        ROOT / DEFAULT_PREVIEW_GAP_DOC_PATH,
        ROOT / DEFAULT_VISUAL_GAP_FIX_PATH,
        ROOT / DEFAULT_VISUAL_GAP_FIX_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)
    combined_lower = combined.lower()

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined_lower
    assert "launch ymm4 now" not in combined_lower
    assert "create audio" not in combined_lower
    assert "generate tts" not in combined_lower
    assert "tune nod speed" not in combined_lower

    tracked_forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in tracked_forbidden_suffixes for path in generated_paths)

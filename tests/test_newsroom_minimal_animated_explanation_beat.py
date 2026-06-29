import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_minimal_animated_explanation_beat import (
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH,
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH,
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH,
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH,
    EXPLANATION_BEAT,
    LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
    NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION,
    build_default_minimal_animated_explanation_beat,
    build_default_minimal_animated_explanation_beat_contract,
    materialize_local_minimal_animated_explanation_beat_probe,
    render_minimal_animated_explanation_beat_contract_markdown,
    render_minimal_animated_explanation_beat_markdown,
    write_default_newsroom_minimal_animated_explanation_beat_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_minimal_animated_explanation_beat_artifacts(root=ROOT)


def test_mainline_proof_defines_one_integrated_explanation_beat() -> None:
    _ensure_artifacts()
    payload = build_default_minimal_animated_explanation_beat(root=ROOT)
    artifact = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["actual_audience_acceptance_claimed"] is False
    assert artifact["source_mvp_freeze_path"].endswith("background_animation_mvp_freeze_v1.json")
    assert artifact["selected_next_axis"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION

    beat = artifact["explanation_beat"]
    assert beat == EXPLANATION_BEAT
    assert beat["beat_id"] == "minimal_animated_explanation_beat_mainline_v1"
    assert beat["diagnostic_line"]
    assert beat["line_status"] == "review_only_diagnostic_line_not_final_script_copy"
    assert "subtitle" in beat["subtitle_role"]
    assert "no new card design" in beat["card_overlay_role"]
    assert "no real RSS/news" in beat["source_boundary_role"]


def test_mainline_route_materializes_ignored_probe_from_known_route() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH)
    route = artifact["mainline_route"]

    assert route["route_name"] == "existing_minimal_integrated_scene_route_plus_neutral_timeline_semantics"
    assert route["local_probe_status"] == "materialized_ignored_local_probe"
    assert route["local_ymmp_materialization_status"] == "materialized_ignored_local_probe"
    assert route["access_state"] == "verified_present"
    assert route["source_route_readback_summary"]["status"] == "structural_pass"
    assert "samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json" in route[
        "input_artifacts"
    ]
    assert "samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json" in route[
        "input_artifacts"
    ]

    access = route["local_probe_access"]
    assert access["repo_relative_path"] == LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["artifact_scope"] == "ignored_local_only"
    assert access["git_check_ignore_result"]["ignored"] is True

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
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


def test_local_probe_readback_stays_structural_and_diagnostic() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH)
    readback = artifact["mainline_route"]["local_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == 720
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["timeline"]["unexpected_item_types"] == []
    assert readback["semantic_checks"]["status"] == "pass"
    assert readback["semantic_checks"]["not_animation_demo"] is True
    assert readback["semantic_checks"]["narration_bound_to_subtitle_readback"] is True
    assert readback["semantic_checks"]["card_overlay_role_is_minimal"] is True
    assert readback["YMM4_launch_status"] == "not_launched"
    assert readback["render_status"] == "not_rendered"
    assert readback["audio_tts_status"] == "not_created"

    probe = load_ymmp(ROOT / LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_contract_records_acceptance_and_not_accepted_scope() -> None:
    _ensure_artifacts()
    payload = build_default_minimal_animated_explanation_beat_contract(root=ROOT)
    artifact = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["proof_id"] == "newsroom_minimal_animated_explanation_beat_mainline_v1_2026_06_29"
    assert artifact["selected_next_axis"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION

    acceptance = artifact["integration_acceptance"]
    assert acceptance["not_animation_demo"] is True
    assert acceptance["not_card_polish"] is True
    assert acceptance["narration_remains_primary"] is True
    assert acceptance["animation_supports_explanation"] is True
    assert acceptance["overlay_does_not_become_main_target"] is True
    assert acceptance["ready_for_one_preview_if_probe_exists"] is True

    contract = artifact["business_goal_outcome_contract"]
    assert contract["problem_clear"]["status"] is True
    assert contract["offer_clear"]["status"] is True
    assert contract["proof_clear"]["status"] is True
    assert contract["boundary_clear"]["status"] is True
    assert contract["next_action_clear"]["rationale"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
    assert contract["visual_supports_explanation"]["status"] == "structural_ready_pending_preview"

    not_accepted = artifact["not_accepted_scope"]
    assert not_accepted["production_animation_quality"] is False
    assert not_accepted["render_export_proof"] is False
    assert not_accepted["public_readiness"] is False
    assert not_accepted["real_RSS_news_integration"] is False
    assert not_accepted["speech_balloon_visual_acceptance"] is False
    assert not_accepted["full_chaban_scene"] is False
    assert not_accepted["audience_order_acceptance"] is False


def test_materializer_can_be_called_directly() -> None:
    materialize_local_minimal_animated_explanation_beat_probe(root=ROOT)
    assert (ROOT / LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH).exists()


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    proof = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH)
    contract = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH)

    assert (ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_minimal_animated_explanation_beat_markdown(proof)
    assert (ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_minimal_animated_explanation_beat_contract_markdown(contract)


def test_outputs_do_not_request_forbidden_work_or_track_media() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH,
        ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH,
        ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH,
        ROOT / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH,
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
    assert "primitive-only probe" not in combined_lower
    assert "card redesign" not in combined_lower

    tracked_forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in tracked_forbidden_suffixes for path in generated_paths)

    proof = _load(DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH)
    assert proof["boundaries"]["YMM4_launched_by_agent"] is False
    assert proof["boundaries"]["render_performed_by_agent"] is False
    assert proof["boundaries"]["audio_tts_generated"] is False
    assert proof["boundaries"]["ymmp_or_media_staged_or_committed"] is False

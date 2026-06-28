import json
import re
from pathlib import Path

from src.pipeline.newsroom_v0_1_explanation_readiness import (
    DEFAULT_V0_1_EXPLANATION_READINESS_DOC_PATH,
    DEFAULT_V0_1_EXPLANATION_READINESS_PATH,
    DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_DOC_PATH,
    DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH,
    NEXT_DEFAULT_SLICE,
    SUGGESTED_LINE_COUNT_RANGE,
    TARGET_DURATION_RANGE_SEC,
    TARGET_NARRATION_SEGMENTS,
    V0_1_EXPLANATION_READINESS_ID,
    V0_1_EXPLANATION_READINESS_SCHEMA_VERSION,
    V0_1_SCRIPT_DENSITY_PLAN_ID,
    V0_1_SCRIPT_DENSITY_PLAN_SCHEMA_VERSION,
    build_default_newsroom_v0_1_explanation_readiness,
    build_default_newsroom_v0_1_script_density_plan,
    render_newsroom_v0_1_explanation_readiness_markdown,
    render_newsroom_v0_1_script_density_plan_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = ROOT / DEFAULT_V0_1_EXPLANATION_READINESS_PATH
PLAN_PATH = ROOT / DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH
READINESS_DOC_PATH = ROOT / DEFAULT_V0_1_EXPLANATION_READINESS_DOC_PATH
PLAN_DOC_PATH = ROOT / DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_DOC_PATH


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_explanation_readiness_matches_builder_and_identity() -> None:
    readiness = _json(READINESS_PATH)

    assert readiness == build_default_newsroom_v0_1_explanation_readiness(root=ROOT)
    assert readiness["artifact_id"] == V0_1_EXPLANATION_READINESS_ID
    assert readiness["package_id"] == V0_1_EXPLANATION_READINESS_ID
    assert readiness["schema_version"] == V0_1_EXPLANATION_READINESS_SCHEMA_VERSION
    assert readiness["production_status"] == "diagnostic_only"
    assert readiness["business_goal_primary"] == "understanding/adoption"
    assert readiness["desired_viewer_action"] == (
        "understand what can be built and what to ask next"
    )
    assert readiness["source_validation"]["status"] == "passed"
    assert readiness["source_validation"]["errors"] == []


def test_current_observation_and_capability_map_are_normalized() -> None:
    readiness = _json(READINESS_PATH)
    observation = readiness["normalized_current_observation"]
    capabilities = {
        row["capability"]: row for row in readiness["current_proven_capabilities"]
    }

    assert observation["render_output_exists_local"] is True
    assert observation["yym4_render_pipeline_status"] == "diagnostic_pass"
    assert observation["ai_direct_video_generation_via_ymmp"] == "not_reliable_yet"
    assert observation["yym4_native_audio_path"] == "diagnostic_pass"
    assert observation["script_import_path"] == "diagnostic_pass"
    assert observation["card_visual_asset_path"] == "diagnostic_pass"
    assert observation["observed_duration_sec"] == 68
    assert observation["next_highest_value_axis"] == (
        "explanation_readiness_and_script_density"
    )
    assert observation["production_ready"] is False
    assert observation["public_ready"] is False

    for key in [
        "YMM4 script import",
        "speaker binding",
        "native yukkuri audio",
        "English loanword handling",
        "source .ymmp recreation from CSV",
        "timing patch to 68 seconds",
        "card PNG generation",
        "YMM4 ImageItem placement",
        "video render output",
        "benchmark-driven visual refinement",
        "local artifact recovery process",
    ]:
        assert capabilities[key]["status"] in {"diagnostic_pass", "diagnostic_reference"}


def test_explanation_gates_select_script_density_next_axis() -> None:
    readiness = _json(READINESS_PATH)
    gates = {row["gate"]: row for row in readiness["explanation_readiness_gates"]}

    assert gates["problem_clear"]["status"] == "partial"
    assert gates["offer_clear"]["status"] == "partial"
    assert gates["proof_clear"]["status"] == "pass"
    assert gates["boundary_clear"]["status"] == "pass"
    assert gates["next_action_clear"]["status"] == "partial"
    assert gates["audience_fit_proxy"]["status"] == "partial"
    assert gates["visual_supports_explanation"]["status"] == "pass"
    assert readiness["highest_value_next_axis"]["selected"] == NEXT_DEFAULT_SLICE


def test_script_density_diagnosis_says_four_lines_are_not_enough() -> None:
    diagnosis = _json(READINESS_PATH)["script_density_diagnosis"]

    assert diagnosis["current_dialogue_line_count"] == 4
    assert diagnosis["current_duration_sec"] == 68
    assert diagnosis["current_seconds_per_dialogue_line"] == 17
    assert diagnosis["current_spoken_density"] == "too_sparse_for_explanation"
    assert diagnosis["four_lines_enough_for_explanation"] is False
    assert diagnosis["likely_needed_line_count_range"] == SUGGESTED_LINE_COUNT_RANGE
    assert diagnosis["likely_needed_segment_count"] == TARGET_NARRATION_SEGMENTS
    assert "what this diagnostic proves" in diagnosis["what_should_be_spoken"]
    assert "review-only boundary" in diagnosis["what_should_be_shown"]


def test_script_density_plan_matches_builder_and_required_structure() -> None:
    plan = _json(PLAN_PATH)

    assert plan == build_default_newsroom_v0_1_script_density_plan(root=ROOT)
    assert plan["artifact_id"] == V0_1_SCRIPT_DENSITY_PLAN_ID
    assert plan["plan_id"] == V0_1_SCRIPT_DENSITY_PLAN_ID
    assert plan["schema_version"] == V0_1_SCRIPT_DENSITY_PLAN_SCHEMA_VERSION
    assert plan["production_status"] == "diagnostic_only"
    assert plan["plan_type"] == "script_density_plan_only"
    assert plan["target_duration_sec"] == TARGET_DURATION_RANGE_SEC
    assert plan["target_narration_segments"] == TARGET_NARRATION_SEGMENTS
    assert plan["suggested_line_count_range"] == SUGGESTED_LINE_COUNT_RANGE
    assert [row["segment"] for row in plan["recommended_segment_structure"]] == [
        "opening",
        "mechanism",
        "proof",
        "boundary",
        "next_action",
    ]
    assert len(plan["card_to_narration_alignment"]) == 4
    assert plan["implementation_policy"] == {
        "plan_only": True,
        "script_implementation_in_this_slice": False,
        "YMM4_launch_or_render_in_this_slice": False,
        "cards_regenerated_in_this_slice": False,
    }
    assert plan["highest_value_next_axis"]["selected"] == NEXT_DEFAULT_SLICE


def test_matrices_and_boundaries_match_contract_counts() -> None:
    readiness = _json(READINESS_PATH)
    plan = _json(PLAN_PATH)

    for artifact in [readiness, plan]:
        assert len(artifact["completion_matrix"]) == 6
        assert len(artifact["artifact_readiness"]) == 6
        assert len(artifact["render_gate_hygiene"]) == 6
        assert len(artifact["human_burden_hygiene"]) == 7
        assert len(artifact["inertia_check"]) == 5
        assert artifact["not_accepted_scope"] == {
            "production_readiness": False,
            "public_readiness": False,
            "actual_audience_or_order_acceptance": False,
            "real_rss_or_news_content": False,
            "rights_publication_clearance": False,
            "final_design_system": False,
            "automated_yym4_render_claim": False,
        }
        assert artifact["boundaries"] == {
            "YMM4_launched_by_agent": False,
            "render_performed_by_agent": False,
            "ymmp_edited_or_committed": False,
            "audio_tts_generated": False,
            "cards_regenerated": False,
            "real_rss_or_news_fetched": False,
            "production_public_readiness_claimed": False,
            "actual_audience_acceptance_claimed": False,
        }

    assert len(readiness["business_explanation_readiness"]) == 7
    assert readiness["automation_note"]["ai_direct_video_generation_via_ymmp"] == (
        "not_reliable_yet"
    )
    assert "manual render/export" in plan["automation_note"]["user_yym4_side_remains_required_for"]


def test_docs_match_renderers_and_avoid_real_url_or_positive_claims() -> None:
    readiness = _json(READINESS_PATH)
    plan = _json(PLAN_PATH)
    readiness_doc = READINESS_DOC_PATH.read_text(encoding="utf-8")
    plan_doc = PLAN_DOC_PATH.read_text(encoding="utf-8")

    assert readiness_doc == render_newsroom_v0_1_explanation_readiness_markdown(
        readiness
    )
    assert plan_doc == render_newsroom_v0_1_script_density_plan_markdown(plan)

    combined = (
        READINESS_PATH.read_text(encoding="utf-8")
        + PLAN_PATH.read_text(encoding="utf-8")
        + readiness_doc
        + plan_doc
    ).replace("http://www.w3.org/2000/svg", "")
    assert not _real_url_pattern().search(combined)
    assert "actual_audience_acceptance_claimed: true" not in combined
    assert '"actual_audience_acceptance_claimed": true' not in combined
    assert "production_approval: true" not in combined
    assert '"production_approval": true' not in combined
    assert "public_ready: true" not in combined
    assert '"public_ready": true' not in combined
    assert " ".join(["fixed", "form", "required"]) not in combined.lower()
    assert " ".join(["render", "again"]) not in combined.lower()

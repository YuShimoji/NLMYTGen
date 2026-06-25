import json
import re
from pathlib import Path

from src.pipeline.newsroom_internal_review_v0_1_prep import (
    DEFAULT_INTERNAL_REVIEW_V0_1_PREP_DOC_PATH,
    DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH,
    DEFAULT_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_PATH,
    INTERNAL_REVIEW_V0_1_PREP_ID,
    INTERNAL_REVIEW_V0_1_PREP_SCHEMA_VERSION,
    NEXT_DEFAULT_SLICE,
    build_default_newsroom_internal_review_v0_1_prep,
    render_newsroom_internal_review_v0_1_prep_markdown,
    render_newsroom_internal_review_v0_1_review_brief,
)


ROOT = Path(__file__).resolve().parents[1]
PREP_PATH = ROOT / DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH
DOC_PATH = ROOT / DEFAULT_INTERNAL_REVIEW_V0_1_PREP_DOC_PATH
BRIEF_PATH = ROOT / DEFAULT_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_PATH


def _prep() -> dict:
    return json.loads(PREP_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_prep_json_matches_builder_output_and_identity() -> None:
    prep = _prep()

    assert prep == build_default_newsroom_internal_review_v0_1_prep(root=ROOT)
    assert prep["artifact_id"] == INTERNAL_REVIEW_V0_1_PREP_ID
    assert prep["review_package_id"] == INTERNAL_REVIEW_V0_1_PREP_ID
    assert prep["schema_version"] == INTERNAL_REVIEW_V0_1_PREP_SCHEMA_VERSION
    assert prep["review_status"] == "ready_for_supervisor_review"
    assert prep["production_status"] == "diagnostic_only"
    assert prep["diagnostic_only"] is True
    assert prep["review_stage"] == [
        "internal_review_v0_1_prep",
        "not_public",
        "not_production",
    ]
    assert prep["identity"]["source_card_render_result_path"] == (
        "samples/_probe/newsroom_handoff/card_placement_render_smoke_result_readback_v1.json"
    )


def test_source_validation_and_evidence_map_cover_required_axes() -> None:
    prep = _prep()
    validation = prep["source_validation"]
    evidence = prep["evidence_map"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["card_render_result"] == "pass"
    assert validation["card_render_duration_sec"] == 68
    assert validation["card_render_card_count"] == 4
    assert validation["card_placement_probe_status"] == "placed_structurally"
    assert validation["native_audio_present_in_prior_render"] is True
    assert [row["axis"] for row in evidence] == [
        "script/caption import",
        "speaker binding",
        "native YMM4 audio",
        "timing patch to 68 sec",
        "card asset generation",
        "card placement as ImageItems",
        "card placement render smoke",
        "render duration",
        "render time approximate",
        "not accepted production/public scope",
        "caption timing source",
    ]
    assert all(row["status"] for row in evidence)
    assert all(row["evidence_path"].startswith("samples/_probe/") for row in evidence)


def test_candidate_summary_and_benchmark_baseline_match_diagnostic_video() -> None:
    prep = _prep()
    candidate = prep["internal_review_v0_1_candidate_summary"]
    baseline = prep["benchmark_baseline"]

    assert candidate == {
        "candidate_video_name": "diagnostic_bound_speaker_probe_card_placement_v1.mp4",
        "candidate_duration_sec": 68,
        "candidate_content_type": "fake/review-only diagnostic",
        "card_count": 4,
        "dialogue_item_count": 4,
        "voice_path": "YMM4_native_yukkuri_japanese",
        "render_status": "pass",
        "review_status": [
            "ready_for_internal_review_prep",
            "not_ready_for_publication",
        ],
    }
    assert baseline["video_duration_sec"] == 68
    assert baseline["render_time_approx_sec"] == 30
    assert baseline["fake_card_count"] == 4
    assert baseline["dialogue_item_count"] == 4
    assert baseline["voice_path"] == "YMM4_native_yukkuri_japanese"
    assert baseline["real_data_used"] is False
    assert baseline["production_public_readiness"] is False


def test_review_questions_are_compact_freeform_and_not_fixed_template() -> None:
    prep = _prep()
    questions = prep["review_questions"]
    brief = prep["review_brief"]

    assert questions == [
        "Is the 68sec pacing intelligible despite sparse content?",
        "Do the four cards make the fake/review-only structure understandable?",
        "Is the subtitle/card safe area acceptable for a diagnostic baseline?",
        "Does the video feel like a viable internal review v0.1, not production?",
        "What is the single highest-value improvement before real packet integration?",
    ]
    assert len(questions) == 5
    assert brief["mode"] == "freeform_internal_review"
    assert brief["look_for_count"] == 5
    assert brief["fixed_template_required"] is False
    assert brief["next_user_facing_action"] == NEXT_DEFAULT_SLICE


def test_scope_next_milestone_and_render_gate_preserve_boundaries() -> None:
    prep = _prep()
    accepted = prep["accepted_scope"]
    not_accepted = prep["not_accepted_scope"]
    next_milestone = prep["next_milestone_recommendation"]
    render_gate = prep["render_gate_carry_forward"]

    assert accepted["diagnostic_68sec_yym4_video_exists_and_render_path_is_proven"] is True
    assert accepted["cards_audio_timing_survive_render"] is True
    assert accepted["internal_review_v0_1_can_be_prepared"] is True
    assert not_accepted == {
        "production_pacing": False,
        "final_visual_design": False,
        "final_narration_script_density": False,
        "real_newsroom_content": False,
        "rss_live_ingest": False,
        "rights_publication_boundary": False,
        "production_export_settings": False,
        "final_artifact_packaging": False,
        "public_prod_approval": False,
    }
    assert next_milestone["recommended_default"] == NEXT_DEFAULT_SLICE
    assert [row["slice"] for row in next_milestone["alternative_next_slices"]] == [
        "newsroom-internal-review-v0.1-render-package-v1",
        "newsroom-rss-dry-run-integration-plan-v1",
        "newsroom-visual-card-design-refinement-v1",
    ]
    assert render_gate["new_render_in_this_slice"] is False
    assert render_gate["existing_card_placement_render_observation_consumed_once"] is True
    assert render_gate["YMM4_launched_by_agent"] is False
    assert render_gate["render_audio_or_tts_created_by_agent"] is False


def test_readiness_matrices_and_hygiene_match_contract_counts() -> None:
    prep = _prep()

    assert prep["readiness_separation"]["slice_completion"] == "pass_for_this_prep"
    assert prep["readiness_separation"]["video_readiness_progress"] == "6/7"
    assert prep["readiness_separation"]["visual_readiness_progress"] == (
        "7/7_diagnostic"
    )
    assert prep["readiness_separation"]["internal_review_readiness"] == "prep_defined"
    assert prep["readiness_separation"]["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert len(prep["completion_matrix"]) == 6
    assert len(prep["artifact_readiness"]) == 6
    assert len(prep["internal_review_readiness"]) == 6
    assert len(prep["video_readiness"]) == 7
    assert len(prep["render_gate_hygiene"]) == 6
    assert len(prep["human_burden_hygiene"]) == 7
    assert len(prep["review_non_redundancy"]) == 6
    assert len(prep["inertia_check"]) == 5
    assert prep["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_docs_match_renderers_and_avoid_rigid_review_or_extra_render_language() -> None:
    prep = _prep()
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    brief_text = BRIEF_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_internal_review_v0_1_prep_markdown(prep)
    assert brief_text == render_newsroom_internal_review_v0_1_review_brief(prep)
    assert NEXT_DEFAULT_SLICE in doc_text
    assert NEXT_DEFAULT_SLICE in brief_text
    assert "fake/review-only diagnostic" in doc_text
    assert "not a production or public-ready video" in brief_text
    for text in [doc_text, brief_text]:
        lowered = text.lower()
        assert ("yes/no" + "/unclear") not in lowered
        assert "please render" not in lowered
        assert "render now" not in lowered
        assert "please check audio" not in lowered
        assert ("fixed " + "form") not in lowered
        assert _real_url_pattern().search(text) is None


def test_artifacts_have_no_media_or_production_public_approval_leakage() -> None:
    prep_text = PREP_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    brief_text = BRIEF_PATH.read_text(encoding="utf-8")

    for text in [prep_text, doc_text, brief_text]:
        assert _real_url_pattern().search(text) is None
        assert "public_video_ready\": true" not in text
        assert "production_approval\": true" not in text
        assert "production_quality_claimed\": true" not in text
    assert not list(PREP_PATH.parent.glob("*internal_review_v0_1_prep*.ymmp"))
    assert not list(PREP_PATH.parent.glob("*internal_review_v0_1_prep*.mp4"))
    assert not list(PREP_PATH.parent.glob("*internal_review_v0_1_prep*.wav"))
    assert not list(PREP_PATH.parent.glob("*internal_review_v0_1_prep*.mp3"))
    assert not list(PREP_PATH.parent.glob("*internal_review_v0_1_prep*.m4a"))

import json
import re
from pathlib import Path

from src.pipeline.newsroom_caption_copy_refinement import (
    COPY_REFINEMENT_ARTIFACT_ID,
    COPY_REFINEMENT_SCHEMA_VERSION,
    DEFAULT_COPY_REFINEMENT_DOC_PATH,
    DEFAULT_COPY_REFINEMENT_PATH,
    build_default_newsroom_caption_copy_refinement,
    render_newsroom_caption_copy_refinement_markdown,
)
from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH


ROOT = Path(__file__).resolve().parents[1]
REFINEMENT_PATH = ROOT / DEFAULT_COPY_REFINEMENT_PATH
REFINEMENT_DOC_PATH = ROOT / DEFAULT_COPY_REFINEMENT_DOC_PATH
PLAN_PATH = ROOT / DEFAULT_PLAN_PATH


def _refinement() -> dict:
    return json.loads(REFINEMENT_PATH.read_text(encoding="utf-8"))


def _timing_plan() -> dict:
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_caption_copy_refinement_parses_and_matches_builder_output() -> None:
    refinement = _refinement()

    assert refinement == build_default_newsroom_caption_copy_refinement(root=ROOT)
    assert refinement["artifact_id"] == COPY_REFINEMENT_ARTIFACT_ID
    assert refinement["schema_version"] == COPY_REFINEMENT_SCHEMA_VERSION
    assert refinement["review_status"] == "ready_for_supervisor_review"
    assert refinement["review_axis"] == "caption_copy_readability"
    assert refinement["diagnostic_only"] is True
    assert refinement["production_status"] == "diagnostic_caption_copy_only"


def test_refined_caption_units_preserve_timing_and_required_fields() -> None:
    refinement = _refinement()
    plan = _timing_plan()
    original_by_id = {unit["caption_id"]: unit for unit in plan["caption_units"]}
    units = refinement["refined_caption_units"]

    assert len(units) == 4
    for unit in units:
        original = original_by_id[unit["caption_id"]]
        assert unit["beat_id"] == original["beat_id"]
        assert unit["original_placeholder"] == original["text_placeholder"]
        assert unit["start_sec"] == original["start_sec"]
        assert unit["end_sec"] == original["end_sec"]
        assert unit["duration_sec"] == original["end_sec"] - original["start_sec"]
        assert unit["line_count_target"] == 2
        assert unit["max_chars_target"] == 34
        assert unit["char_count"] == len(unit["refined_caption_text"])
        assert unit["char_count"] <= unit["max_chars_target"]
        assert unit["reading_density"] in {"low", "medium", "high"}
        assert unit["readability_note"]
        assert unit["beat_alignment_note"]
        assert unit["visual_interference_note"]
        assert unit["production_status"] == [
            "diagnostic_only",
            "not_final_script",
            "not_TTS_ready",
        ]
        assert unit["transfer_status"] == "blocked"


def test_caption_copy_is_refined_but_remains_synthetic_and_generic() -> None:
    refinement = _refinement()
    units = refinement["refined_caption_units"]
    text = " ".join(unit["refined_caption_text"] for unit in units)

    assert [unit["refined_caption_text"] for unit in units] == [
        "Fake topic, review only.",
        "Review-only handoff stays.",
        "A fake claim is shown.",
        "Fake source checks are noted.",
    ]
    assert _real_url_pattern().search(text) is None
    assert "Fake" in text
    assert "final narration" not in text.lower()


def test_caption_copy_keeps_transfer_audio_and_review_memory_blocked() -> None:
    refinement = _refinement()
    audio = refinement["audio_readiness"]
    transfer = refinement["transfer_status"]
    review_memory = refinement["review_memory"]
    review_card = refinement["review_card"]
    boundary = refinement["boundary_assertions"]

    assert review_memory["prior_user_review_count"] == 0
    assert review_memory["next_nonredundant_axis"] == "caption_copy_readability"
    assert review_memory["repeated_general_timing_review_allowed"] is False
    assert review_card["status"] == "none"
    assert audio["voice_status"] == "not_started"
    assert audio["TTS_generated"] is False
    assert audio["copy_tts_status"] == "not_TTS_ready"
    assert transfer["transfer_status"] == "blocked"
    assert transfer["YMM4_candidate"] is False
    assert boundary["timing_changed"] is False
    assert boundary["contains_real_news_claims"] is False
    assert boundary["ymmp_generated"] is False
    assert boundary["render_generated"] is False
    assert boundary["tts_generated"] is False


def test_caption_copy_artifacts_have_no_real_urls_or_media_outputs() -> None:
    json_text = REFINEMENT_PATH.read_text(encoding="utf-8")
    doc_text = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(json_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(REFINEMENT_PATH.parent.glob("episode_caption_copy_refinement*.ymmp"))
    assert not list(REFINEMENT_PATH.parent.glob("episode_caption_copy_refinement*.mp4"))
    assert not list(REFINEMENT_PATH.parent.glob("episode_caption_copy_refinement*.wav"))
    assert not list(REFINEMENT_PATH.parent.glob("episode_caption_copy_refinement*.mp3"))


def test_caption_copy_doc_matches_renderer_and_states_boundary() -> None:
    refinement = _refinement()
    doc_text = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_caption_copy_refinement_markdown(refinement)
    assert "## Video Readiness Matrix" in doc_text
    assert "Review Card: none" in doc_text
    assert "YMM4_candidate: false" in doc_text
    assert "TTS_generated: false" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()

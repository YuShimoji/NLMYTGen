import json
import re
from pathlib import Path

from src.pipeline.newsroom_caption_timing_plan import (
    DEFAULT_PLAN_DOC_PATH,
    DEFAULT_PLAN_PATH,
    PLAN_ARTIFACT_ID,
    PLAN_SCHEMA_VERSION,
    build_default_newsroom_caption_timing_plan,
    render_newsroom_caption_timing_plan_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / DEFAULT_PLAN_PATH
PLAN_DOC_PATH = ROOT / DEFAULT_PLAN_DOC_PATH


def _plan() -> dict:
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_caption_timing_plan_parses_and_matches_builder_output() -> None:
    plan = _plan()

    assert plan == build_default_newsroom_caption_timing_plan(root=ROOT)
    assert plan["artifact_id"] == PLAN_ARTIFACT_ID
    assert plan["schema_version"] == PLAN_SCHEMA_VERSION
    assert plan["review_status"] == "ready_for_supervisor_review"
    assert plan["diagnostic_only"] is True
    assert plan["production_status"] == "diagnostic_timing_plan_only"


def test_caption_timing_plan_duration_covers_all_beats() -> None:
    plan = _plan()
    summary = plan["episode_timing_summary"]
    beats = plan["beat_timing"]

    assert summary["total_duration_sec"] == 68
    assert summary["covered_range_sec"] == 68
    assert summary["total_duration_sec"] == sum(beat["duration_sec"] for beat in beats)
    assert beats == [
        {
            **beats[0],
            "beat_id": "beat_fake_intro_001",
            "start_sec": 0,
            "end_sec": 24,
            "duration_sec": 24,
        },
        {
            **beats[1],
            "beat_id": "beat_fake_claim_001",
            "start_sec": 24,
            "end_sec": 68,
            "duration_sec": 44,
        },
    ]
    assert summary["timing_confidence"] == "low_provisional_from_capsule"
    assert summary["provisional_timing"] is True


def test_caption_units_have_timing_and_reserve_status() -> None:
    plan = _plan()
    units = plan["caption_units"]

    assert len(units) == 4
    assert {unit["beat_id"] for unit in units} == {
        "beat_fake_intro_001",
        "beat_fake_claim_001",
    }
    for unit in units:
        assert unit["caption_id"].startswith(f"cap_{unit['beat_id']}_")
        assert unit["start_sec"] < unit["end_sec"]
        assert unit["max_chars_target"] == 34
        assert unit["line_count_target"] == 2
        assert unit["reading_speed_note"] == "placeholder_copy_only_not_final_narration"
        assert unit["caption_reserve_status"] == "present_semantic_only"


def test_visual_timing_maps_visuals_to_beats_and_slots() -> None:
    plan = _plan()
    visuals = {row["visual_id"]: row for row in plan["visual_timing"]}

    assert set(visuals) == {
        "visual_fake_title_card_001",
        "visual_fake_evidence_card_001",
    }
    assert visuals["visual_fake_title_card_001"]["beat_id"] == "beat_fake_intro_001"
    assert visuals["visual_fake_title_card_001"]["start_sec"] == 0
    assert visuals["visual_fake_title_card_001"]["end_sec"] == 24
    assert visuals["visual_fake_title_card_001"]["g28_slot"] == "caption_reserve"
    assert (
        visuals["visual_fake_title_card_001"]["caption_interference_risk"]
        == "low_semantic_reserve_present"
    )
    assert visuals["visual_fake_evidence_card_001"]["beat_id"] == "beat_fake_claim_001"
    assert visuals["visual_fake_evidence_card_001"]["start_sec"] == 24
    assert visuals["visual_fake_evidence_card_001"]["end_sec"] == 68
    assert visuals["visual_fake_evidence_card_001"]["g28_slot"] == "source_note"
    assert (
        visuals["visual_fake_evidence_card_001"]["caption_interference_risk"]
        == "medium_unhinted_caption_reserve"
    )


def test_caption_timing_plan_keeps_audio_and_transfer_blocked() -> None:
    plan = _plan()
    audio = plan["audio_readiness"]
    transfer = plan["transfer_status"]
    boundary = plan["boundary_assertions"]

    assert audio["voice_status"] == "not_started"
    assert audio["TTS_generated"] is False
    assert audio["audio_timing_confidence"] == "low_no_audio"
    assert transfer["transfer_status"] == "blocked"
    assert transfer["YMM4_candidate"] is False
    assert transfer["blocker_count"] == 13
    assert transfer["unlock_requirement_count"] == 13
    assert ".ymmp generation" in transfer["prohibited_next_actions"]
    assert boundary["ymmp_generated"] is False
    assert boundary["render_generated"] is False
    assert boundary["tts_generated"] is False
    assert boundary["public_video"] is False


def test_caption_timing_plan_artifacts_have_no_real_urls_or_media_outputs() -> None:
    plan_text = PLAN_PATH.read_text(encoding="utf-8")
    doc_text = PLAN_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(plan_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PLAN_PATH.parent.glob("episode_caption_timing_plan*.ymmp"))
    assert not list(PLAN_PATH.parent.glob("episode_caption_timing_plan*.mp4"))
    assert not list(PLAN_PATH.parent.glob("episode_caption_timing_plan*.wav"))
    assert not list(PLAN_PATH.parent.glob("episode_caption_timing_plan*.mp3"))


def test_caption_timing_plan_doc_matches_renderer_and_states_boundary() -> None:
    plan = _plan()
    doc_text = PLAN_DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_caption_timing_plan_markdown(plan)
    assert "## Video Readiness Matrix" in doc_text
    assert "| transfer | blocked | YMM4_candidate=false |" in doc_text
    assert "TTS_generated: false" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()

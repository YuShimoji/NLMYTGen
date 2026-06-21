import json
import re
from pathlib import Path

from src.pipeline.newsroom_episode_production_capsule import (
    CAPSULE_ARTIFACT_ID,
    CAPSULE_SCHEMA_VERSION,
    DEFAULT_CAPSULE_DOC_PATH,
    DEFAULT_CAPSULE_PATH,
    build_default_newsroom_episode_production_capsule,
    render_newsroom_episode_production_capsule_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
CAPSULE_PATH = ROOT / DEFAULT_CAPSULE_PATH
CAPSULE_DOC_PATH = ROOT / DEFAULT_CAPSULE_DOC_PATH


def _capsule() -> dict:
    return json.loads(CAPSULE_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_episode_production_capsule_parses_and_matches_builder_output() -> None:
    capsule = _capsule()

    assert capsule == build_default_newsroom_episode_production_capsule(root=ROOT)
    assert capsule["artifact_id"] == CAPSULE_ARTIFACT_ID
    assert capsule["schema_version"] == CAPSULE_SCHEMA_VERSION
    assert capsule["review_status"] == "ready_for_supervisor_review"
    assert capsule["diagnostic_only"] is True
    assert capsule["production_status"] == "diagnostic_only"


def test_episode_production_capsule_identifies_adapted_packet_episode() -> None:
    capsule = _capsule()
    episode = capsule["episode"]
    source = capsule["source"]

    assert episode["episode_id"] == "episode_fake_nlmytgen_delta_v1"
    assert episode["title"] == "Fake upstream export delta for NLMYTGen"
    assert episode["source"] == "synthetic/adapted packet"
    assert source["capsule_source"] == "adapted_packet_current_recomputed_readbacks"
    assert source["source_fixture_kind"] == "newsroom_fake_export_adapter_proof"
    assert all(
        row["relationship"].startswith("inspected as earlier newsroom chain evidence")
        for row in source["inspected_prior_readbacks"]
    )


def test_episode_production_capsule_has_script_visual_and_timing_structure() -> None:
    capsule = _capsule()
    beats = capsule["script_structure"]
    visuals = capsule["visual_structure"]

    assert [beat["beat_id"] for beat in beats] == [
        "beat_fake_intro_001",
        "beat_fake_claim_001",
    ]
    assert all(beat["expected_narration_placeholder"] for beat in beats)
    assert beats[0]["source_note_refs"] == []
    assert beats[1]["source_note_refs"] == [
        "source_fake_primary_001",
        "source_fake_critical_001",
    ]
    assert {visual["visual_id"] for visual in visuals} == {
        "visual_fake_title_card_001",
        "visual_fake_evidence_card_001",
    }
    assert all(visual["caption_reserve"]["status"] == "present" for visual in visuals)
    assert all(visual["g28_slot_refs"] for visual in visuals)
    assert capsule["timing_approximation"]["status"] == "provisional"
    assert capsule["timing_approximation"]["total_duration_seconds"] == sum(
        beat["rough_duration_seconds"] for beat in beats
    )


def test_episode_production_capsule_keeps_transfer_blocked_and_approvals_false() -> None:
    capsule = _capsule()
    readiness = capsule["video_readiness"]
    transfer = capsule["transfer_status"]
    boundary = capsule["boundary_assertions"]

    assert readiness["validator_status"] == "passed"
    assert readiness["slot_linkage_status"] == "passed_with_warnings"
    assert readiness["transfer_planning_status"] == "blocked"
    assert readiness["transfer_status"] == "blocked"
    assert readiness["ymm4_transfer_ready"] is False
    assert readiness["production_approval"] is False
    assert transfer["transfer_status"] == "blocked"
    assert transfer["blocker_count"] == 13
    assert transfer["unlock_requirement_count"] == 13
    assert boundary["ymmp_generated"] is False
    assert boundary["render_generated"] is False
    assert boundary["tts_generated"] is False
    assert boundary["public_video"] is False


def test_episode_production_capsule_lists_required_next_and_prohibited_steps() -> None:
    capsule = _capsule()
    prohibited = set(capsule["prohibited_steps"])

    for expected in [
        "real source fetch",
        ".ymmp generation",
        "YMM4 carrier generation",
        "render generation",
        "production approval",
        "publishing",
        "RSS/Inoreader operation",
        "real URL access",
        "media download",
    ]:
        assert expected in prohibited

    assert capsule["next_allowed_steps"] == [
        "Review Console episode preview",
        "caption/timing refinement",
        "YMM4 transfer candidate proof only after blockers are resolved",
    ]


def test_episode_production_capsule_artifacts_have_no_real_urls_or_ymmp_media_outputs() -> None:
    capsule_text = CAPSULE_PATH.read_text(encoding="utf-8")
    doc_text = CAPSULE_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(capsule_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(CAPSULE_PATH.parent.glob("episode_production_capsule*.ymmp"))
    assert not list(CAPSULE_PATH.parent.glob("episode_production_capsule*.mp4"))
    assert not list(CAPSULE_PATH.parent.glob("episode_production_capsule*.wav"))


def test_episode_production_capsule_doc_matches_renderer_and_has_video_matrix() -> None:
    capsule = _capsule()
    doc_text = CAPSULE_DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_episode_production_capsule_markdown(capsule)
    assert "## Episode Capsule Summary" in doc_text
    assert "## Video Readiness Matrix" in doc_text
    assert "transfer | blocked" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()

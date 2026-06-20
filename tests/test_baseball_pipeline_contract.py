from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = REPO_ROOT / "samples" / "_probe" / "baseball" / "pipeline"
CONTRACT_DOC = REPO_ROOT / "docs" / "baseball" / "BASEBALL_PIPELINE_CONTRACT.md"
DATA_CAPSULE = PIPELINE_DIR / "baseball_data_capsule_p05.json"
SCRIPT_IR = PIPELINE_DIR / "baseball_script_beat_ir_p05.json"
SCENE_PLAN = PIPELINE_DIR / "baseball_visual_scene_plan_p05.json"
MANIFEST = PIPELINE_DIR / "baseball_pipeline_contract_manifest.json"


FORBIDDEN_COMPLETION_CLAIMS = (
    "render_completion\": true",
    "production_ready\": true",
    "creative_final_acceptance\": true",
    "publish_gate\": true",
    "clip_export\": true",
    "video_generation\": true",
    "tts\": true",
    "thumbnail_work\": true",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_baseball_pipeline_contract_files_exist() -> None:
    for path in (CONTRACT_DOC, DATA_CAPSULE, SCRIPT_IR, SCENE_PLAN, MANIFEST):
        assert path.exists(), path


def test_baseball_pipeline_manifest_declares_layer_order_and_boundaries() -> None:
    manifest = _load(MANIFEST)

    assert manifest["schema_version"] == "baseball_pipeline_contract_manifest.v1"
    assert manifest["artifact_id"] == "baseball_news_pipeline_contract"
    assert manifest["status"] == "contract_defined"
    assert manifest["contract_doc"] == "docs/baseball/BASEBALL_PIPELINE_CONTRACT.md"
    assert manifest["layer_order"] == [
        "BaseballDataCapsule",
        "ScriptBeatIR",
        "VisualScenePlan",
        "YMM4Adapter",
        "ReviewGate",
    ]

    for key, value in manifest["artifacts"].items():
        assert (REPO_ROOT / value).exists(), key

    boundaries = manifest["boundaries"]
    assert boundaries["sample_only"] is True
    assert boundaries["not_real_source"] is True
    assert boundaries["not_clip_export"] is True
    assert boundaries["not_video_generation"] is True
    assert boundaries["not_tts"] is True
    assert boundaries["not_thumbnail_work"] is True
    assert boundaries["not_render_proof"] is True
    assert boundaries["not_production_ready"] is True
    assert boundaries["not_creative_final_acceptance"] is True
    assert boundaries["not_publish_gate"] is True
    assert boundaries["not_mainline_integration"] is True


def test_script_beat_ir_only_references_data_capsule_facts() -> None:
    data = _load(DATA_CAPSULE)
    script = _load(SCRIPT_IR)
    fact_ids = {fact["fact_id"] for fact in data["derived_facts"]}

    assert script["source_data_capsule"] == "samples/_probe/baseball/pipeline/baseball_data_capsule_p05.json"
    assert script["script_owner"] == "ScriptBeatIR"
    assert script["boundaries"]["must_not_invent_facts"] is True
    assert script["boundaries"]["not_visual_layout_authority"] is True

    for beat in script["beats"]:
        assert beat["data_refs"], beat["beat_id"]
        assert set(beat["data_refs"]).issubset(fact_ids), beat["beat_id"]


def test_visual_scene_plan_references_data_and_script_and_covers_timeline() -> None:
    data = _load(DATA_CAPSULE)
    script = _load(SCRIPT_IR)
    plan = _load(SCENE_PLAN)
    fact_ids = {fact["fact_id"] for fact in data["derived_facts"]}
    beat_ids = {beat["beat_id"] for beat in script["beats"]}

    assert plan["visual_owner"] == "VisualScenePlan"
    assert plan["timebase"] == {
        "start_frame": 1560,
        "duration_frames": 1320,
        "end_frame_exclusive": 2880,
    }

    slot_ids = {slot["slot_id"] for slot in plan["semantic_slots"]}
    assert {"score_context", "pitch_event_claim", "current_pitch_card", "pitch_log", "strike_zone_trace"}.issubset(slot_ids)

    for slot in plan["semantic_slots"]:
        assert set(slot["data_refs"]).issubset(fact_ids), slot["slot_id"]
        assert set(slot["script_refs"]).issubset(beat_ids), slot["slot_id"]
        assert "yymm4_hint" in slot

    scenes = plan["scene_timeline"]
    assert scenes[0]["frame_start"] == plan["timebase"]["start_frame"]
    assert scenes[-1]["frame_end_exclusive"] == plan["timebase"]["end_frame_exclusive"]
    for previous, current in zip(scenes, scenes[1:]):
        assert previous["frame_end_exclusive"] == current["frame_start"]
    for scene in scenes:
        assert set(scene["active_slots"]).issubset(slot_ids), scene["scene_id"]
        assert scene["motion_primitives"], scene["scene_id"]


def test_contract_doc_states_ownership_and_no_completion_claims() -> None:
    text = CONTRACT_DOC.read_text(encoding="utf-8")

    for required in (
        "BaseballDataCapsule",
        "ScriptBeatIR",
        "VisualScenePlan",
        "YMM4Adapter",
        "ReviewGate",
        "does not claim render completion",
        "does not perform clip export",
    ):
        assert required in text

    for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
        assert forbidden not in text

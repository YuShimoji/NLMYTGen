"""Reliability guard for samples/_probe/pipeline_smoke fixtures.

Not a production feature. Detects manifest / fixture drift without
requiring Electron or any GUI runtime, so it stays runnable in CI and
headless environments where the existing Electron-based smoke cannot
execute.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    REPO_ROOT / "samples" / "_probe" / "pipeline_smoke" / "pipeline_smoke_manifest.json"
)

EXPECTED_TOPIC_IDS = {
    "real_estate_dx_baseline",
    "ai_monitoring_labor",
    "baseball_news_infographic",
}

ALLOWED_STATES = {"reviewable", "blocked"}

EXPECTED_FORBIDDEN = {
    "G-27 v3 proof",
    "G-27 scene decision packet",
    "asset/proxy gap report",
    "YMM4 adapter output",
    "render",
    "production timing",
    "creative acceptance",
}

REQUIRED_ARTIFACT_KEYS = {
    "source_script",
    "script_beat_ir",
    "visual_direction_contract",
    "shot_layout_plan",
    "motion_beat_plan",
    "proof_html",
    "proof_image",
    "proof_sidecar",
    "proof_readback",
    "review_packet",
    "review_decisions",
}


@pytest.fixture(scope="module")
def manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as fp:
        return json.load(fp)


def test_manifest_top_level(manifest: dict) -> None:
    assert manifest["version"] == "1.0"
    assert manifest["primary_review_surface"] == "GUI timeline"
    assert manifest["standalone_html_png_json_is_completion"] is False


def test_three_topics_with_expected_ids(manifest: dict) -> None:
    topic_ids = {topic["id"] for topic in manifest["topics"]}
    assert topic_ids == EXPECTED_TOPIC_IDS


def test_topic_states_and_handoff_fields(manifest: dict) -> None:
    for topic in manifest["topics"]:
        assert topic["state"] in ALLOWED_STATES, topic["id"]
        assert topic["blocked_reason"], f"empty blocked_reason: {topic['id']}"
        assert topic["next_action"], f"empty next_action: {topic['id']}"


def test_artifact_keys_complete(manifest: dict) -> None:
    for topic in manifest["topics"]:
        artifact_keys = set(topic["artifacts"].keys())
        missing = REQUIRED_ARTIFACT_KEYS - artifact_keys
        assert not missing, f"{topic['id']} missing artifact keys: {missing}"


def test_artifact_paths_exist(manifest: dict) -> None:
    missing: list[str] = []
    for topic in manifest["topics"]:
        for key, rel_path in topic["artifacts"].items():
            if not (REPO_ROOT / rel_path).exists():
                missing.append(f"{topic['id']}.{key} -> {rel_path}")
    assert not missing, missing


def test_forbidden_items_intact(manifest: dict) -> None:
    forbidden = set(manifest["forbidden"])
    assert forbidden == EXPECTED_FORBIDDEN, forbidden ^ EXPECTED_FORBIDDEN


def test_at_least_one_blocked_and_one_reviewable(manifest: dict) -> None:
    states = {topic["state"] for topic in manifest["topics"]}
    assert "reviewable" in states
    assert "blocked" in states

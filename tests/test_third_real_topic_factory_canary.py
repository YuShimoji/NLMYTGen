from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANARY = (
    ROOT
    / "production_pilots"
    / "factory_canaries"
    / "ai_monitoring_labor_001"
)
REINS = (
    ROOT
    / "production_pilots"
    / "factory_canaries"
    / "real_estate_reins_transparency_001"
    / "auto_video_pipeline"
    / "real_estate_reins_episode_manifest.json"
)
NEW_BANKNOTE = (
    ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_002"
    / "external_editorial_input"
    / "new_banknote_security_notebooklm_001"
    / "auto_video_pipeline"
    / "new_banknote_real_media_episode_manifest.json"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_third_topic_claims_and_cue_edges_are_closed() -> None:
    script = _json(CANARY / "canonical_script.json")
    registry = _json(CANARY / "source_registry.json")
    adjudication = _json(CANARY / "claim_adjudication.json")
    edges = _json(CANARY / "source_support_edges.json")

    assert script["title"] == "AIによる職場モニタリングと働く人への影響"
    assert script["cue_count"] == len(script["cues"]) == 5
    assert script["scene_count"] == len({cue["scene_id"] for cue in script["cues"]}) == 2
    assert script["speaker_distribution"] == {"れいむ": 2, "まりさ": 3}
    assert script["unsupported_spoken_factual_units"] == 0
    assert script["human_creative_acceptance"] is False

    assert len(registry["sources"]) == 3
    assert all(source["primary_source"] is True for source in registry["sources"])
    assert all(source["canonical_url"].startswith("https://") for source in registry["sources"])
    assert registry["retrieval_policy"] == {
        "official_primary_surfaces_only": True,
        "login_used": False,
        "credentials_used": False,
        "playback_used": False,
        "source_count": 3,
    }
    assert len(adjudication["claims"]) == 4
    assert all(
        claim["status"] == "supported" and claim["support"]
        for claim in adjudication["claims"]
    )

    edge_rows = edges["edges"]
    assert [row["cue_id"] for row in edge_rows] == [
        cue["cue_id"] for cue in script["cues"]
    ]
    assert all(
        row["claim_ids"] and row["source_ids"]
        for row in edge_rows
        if row["spoken_factual_unit"]
    )
    assert edges["checks"] == {
        "cue_order_exact": True,
        "every_spoken_factual_unit_supported": True,
        "unsupported_spoken_factual_units": 0,
        "primary_source_surface_count": 3,
    }


def test_third_topic_serializations_and_content_locks_match() -> None:
    script = _json(CANARY / "canonical_script.json")
    manifest = _json(
        CANARY / "auto_video_pipeline" / "ai_monitoring_labor_episode_manifest.json"
    )

    expected_by_file = {
        "canonical_yymm4.csv": [
            (cue["speaker"], cue["text"]) for cue in script["cues"]
        ],
        "derived_yymm4_import.csv": [
            (cue["speaker"], script_cue["text"])
            for cue, script_cue in zip(
                manifest["cue_mapping"], script["cues"], strict=True
            )
        ],
    }
    for filename, expected in expected_by_file.items():
        with (CANARY / filename).open(encoding="utf-8-sig", newline="") as handle:
            assert [tuple(row) for row in csv.reader(handle)] == expected

    assert len(manifest["cue_mapping"]) == 5
    assert len({cue["scene_id"] for cue in manifest["cue_mapping"]}) == 2
    assert manifest["yymm4"]["timeline_frames"] == 1606
    assert 25 <= manifest["yymm4"]["timeline_frames"] / 60 <= 40
    assert manifest["output"]["run_id"] == "ai_monitoring_labor_internal_review_v1"
    assert manifest["boundaries"]["internal_review_only"] is True
    assert manifest["boundaries"]["rights_approved"] is False
    assert manifest["boundaries"]["production"] is False
    assert manifest["boundaries"]["publication"] is False
    assert manifest["boundaries"]["external_upload"] is False

    for locked in manifest["content_locks"]:
        locked_path = ROOT / locked["path"]
        assert locked_path.is_file()
        assert _sha256(locked_path) == locked["sha256"]


def test_third_topic_real_media_contract_is_raster_and_internal_only() -> None:
    provenance = _json(CANARY / "real_media_provenance.json")

    assets = provenance["assets"]
    assert len(assets) == 5
    assert len({asset["asset_id"] for asset in assets}) == 5
    assert len({asset["sha256"] for asset in assets}) == 5
    assert all(asset["media_type"] == "image" for asset in assets)
    assert all(asset["local_asset_path"].lower().endswith(".png") for asset in assets)
    assert all("auto_video_runs/" in asset["local_asset_path"] for asset in assets)
    assert all(asset["usage_classification"] == "internal_review_only" for asset in assets)
    assert all(asset["production_allowed"] is False for asset in assets)
    assert all(asset["publication_allowed"] is False for asset in assets)
    assert provenance["boundary"] == {
        "internal_review_only": True,
        "rights_approved": False,
        "production": False,
        "publication": False,
        "external_upload": False,
        "source_media_tracked": False,
    }

    tracked_text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in CANARY.rglob("*")
        if path.is_file()
        and not {
            "auto_video_runs",
            "source_cache",
            "source_extracts",
        }.intersection(path.parts)
    )
    assert r"C:\Users\\" not in tracked_text
    assert "D:\\" not in tracked_text
    assert ".svg" not in tracked_text.lower()


def test_three_topics_have_distinct_observed_factory_shapes() -> None:
    third = _json(
        CANARY / "auto_video_pipeline" / "ai_monitoring_labor_episode_manifest.json"
    )
    second = _json(REINS)
    first = _json(NEW_BANKNOTE)

    shapes = [
        (
            len(manifest["cue_mapping"]),
            len({row["scene_id"] for row in manifest["cue_mapping"]}),
            manifest["yymm4"]["timeline_frames"],
        )
        for manifest in (first, second, third)
    ]
    assert shapes == [(9, 3, 4415), (7, 4, 2725), (5, 2, 1606)]
    assert len(set(shapes)) == 3
    assert len(
        {
            manifest["yymm4"]["source_project_path"]
            for manifest in (first, second, third)
        }
    ) == 3
    assert len({manifest["output"]["run_id"] for manifest in (first, second, third)}) == 3
    assert len({manifest["episode_id"] for manifest in (first, second, third)}) == 3

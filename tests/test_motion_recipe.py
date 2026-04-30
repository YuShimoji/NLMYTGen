import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.motion_recipe import MotionRecipeBuildPaths, build_motion_recipe_review
from src.pipeline.ymmp_patch import load_ymmp, _get_timeline_items, _item_type


ROOT = Path(__file__).resolve().parents[1]


def _repo_paths(tmp_path: Path) -> MotionRecipeBuildPaths:
    return MotionRecipeBuildPaths(
        brief=ROOT / "samples/recipe_briefs/g26_motion_recipe_brief.v1.json",
        seed=ROOT / "samples/canonical.ymmp",
        template_source=ROOT / "samples/templates/skit_group/delivery_v1_templates.ymmp",
        effect_catalog=ROOT / "samples/effect_catalog.json",
        effect_samples=ROOT / "samples/_probe/b2/effect_full_samples.json",
        motion_library=ROOT / "samples/tachie_motion_map_library.json",
        corpus_ymmp=None,
        out_ymmp=tmp_path / "review.ymmp",
        out_readback=tmp_path / "readback.json",
        out_manifest=tmp_path / "manifest.md",
    )


def _effect_names(item: dict) -> list[str]:
    return [
        effect.get("$type", "").split(",")[0].split(".")[-1]
        for effect in item.get("VideoEffects", [])
        if isinstance(effect, dict)
    ]


def _route_values(item: dict, axis: str) -> list[float]:
    return [
        keyframe["Value"]
        for keyframe in item[axis]["Values"]
    ]


def _manifest_metadata(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    marker = "## Metadata\n\n```json\n"
    start = text.index(marker) + len(marker)
    end = text.index("\n```", start)
    return json.loads(text[start:end])


def test_build_motion_recipe_review_from_brief(tmp_path: Path) -> None:
    result = build_motion_recipe_review(_repo_paths(tmp_path))

    assert result["success"] is True
    assert result["recipe_count"] == 12
    assert result["recipe_group_count"] == 12
    assert result["recipe_image_count"] == 24
    assert result["posix_asset_paths"] == 0
    assert result["blank_asset_paths"] == 0
    assert result["status_model"]["review_candidate"] == "proposed"
    assert "EFFECT_REQUIRES_COMMUNITY_PLUGIN:CameraShakeEffect" in result["warnings"]
    assert "EFFECT_OBJECT_FROM_CATALOG_ONLY:CameraShakeEffect" in result["warnings"]

    by_goal = {recipe["goal_id"]: recipe for recipe in result["recipes"]}
    assert by_goal["nod_clear"]["route_values"]["Rotation"] == [0.0, -10.0, 0.0]
    assert by_goal["jump_high"]["route_values"]["Y"] == [462.5, 372.5, 462.5]
    assert "CameraShakeEffect" in by_goal["panic_crash"]["used_effects"]
    assert all(recipe["effect_shortlist"] for recipe in result["recipes"])

    metadata = _manifest_metadata(tmp_path / "manifest.md")
    assert metadata["recipe_count"] == 12
    assert metadata["status_model"]["compatibility_evidence"] == (
        "requires_yymm4_chain_visual_pass"
    )


def test_build_motion_recipe_review_writes_yymm_openable_project(tmp_path: Path) -> None:
    build_motion_recipe_review(_repo_paths(tmp_path))

    data = load_ymmp(tmp_path / "review.ymmp")
    items = _get_timeline_items(data)
    groups = [
        item
        for item in items
        if _item_type(item) == "GroupItem"
        and str(item.get("Remark", "")).startswith("recipe:")
    ]
    remarks = {item["Remark"]: item for item in groups}

    assert isinstance(data["Timelines"][0]["LayerSettings"], dict)
    assert isinstance(data["Timelines"][0]["LayerSettings"]["Items"], list)
    assert len(groups) == 12
    assert _route_values(remarks["recipe:shobon_droop"], "Y") == [462.5, 480.5, 480.5]
    assert _effect_names(remarks["recipe:shocked_jump"]) == [
        "CenterPointEffect",
        "JumpEffect",
    ]
    assert "RepeatRotateEffect" in _effect_names(remarks["recipe:anger_outburst"])


def test_cli_build_motion_recipes_writes_all_outputs(tmp_path: Path, capsys) -> None:
    out_ymmp = tmp_path / "cli_review.ymmp"
    out_readback = tmp_path / "cli_readback.json"
    out_manifest = tmp_path / "cli_manifest.md"

    code = main([
        "build-motion-recipes",
        "--brief",
        str(ROOT / "samples/recipe_briefs/g26_motion_recipe_brief.v1.json"),
        "--seed",
        str(ROOT / "samples/canonical.ymmp"),
        "--template-source",
        str(ROOT / "samples/templates/skit_group/delivery_v1_templates.ymmp"),
        "--effect-catalog",
        str(ROOT / "samples/effect_catalog.json"),
        "--effect-samples",
        str(ROOT / "samples/_probe/b2/effect_full_samples.json"),
        "--motion-library",
        str(ROOT / "samples/tachie_motion_map_library.json"),
        "--corpus-ymmp",
        "",
        "--out-yMMP",
        str(out_ymmp),
        "--out-readback",
        str(out_readback),
        "--out-manifest",
        str(out_manifest),
        "--format",
        "json",
    ])

    assert code == 0
    stdout = capsys.readouterr().out
    payload = json.loads(stdout)
    assert payload["outputs"]["ymmp"] == str(out_ymmp)
    assert payload["recipe_count"] == 12
    assert out_ymmp.exists()
    assert out_readback.exists()
    assert out_manifest.exists()
    assert json.loads(out_readback.read_text(encoding="utf-8"))["success"] is True

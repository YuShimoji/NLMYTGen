"""YMM4 thumbnail template slot audit / patch tests."""

from __future__ import annotations

import json

from src.cli.main import main
from src.pipeline.thumbnail_template import (
    audit_thumbnail_template,
    patch_thumbnail_template,
    verify_thumbnail_patch_readback,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


def _anim(value: float) -> dict:
    return {
        "Values": [{"Value": value}],
        "Span": 0.0,
        "AnimationType": "なし",
    }


def _thumb_ymmp() -> dict:
    return {
        "Timelines": [{
            "ID": "main",
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
                    "Remark": "thumb.text.title",
                    "Text": "OLD TITLE",
                    "Color": "#FFFFFFFF",
                    "X": _anim(0.0),
                    "Y": _anim(0.0),
                    "Zoom": _anim(100.0),
                    "Frame": 0,
                    "Length": 60,
                    "Layer": 5,
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                    "Remark": "thumb.image.background",
                    "FilePath": "old_bg.png",
                    "X": _anim(0.0),
                    "Y": _anim(0.0),
                    "Zoom": _anim(100.0),
                    "Frame": 0,
                    "Length": 60,
                    "Layer": 0,
                },
            ],
        }],
    }


def test_audit_thumbnail_template_reports_thumb_slots() -> None:
    result = audit_thumbnail_template(_thumb_ymmp())

    assert result["success"] is True
    assert result["slot_count"] == 2
    assert result["slots"][0]["slot"] == "thumb.text.title"
    assert result["slots"][0]["patchable_fields"]["text"] is True
    assert result["slots"][0]["patchable_fields"]["color"] is True
    assert result["slots"][1]["slot"] == "thumb.image.background"
    assert result["slots"][1]["patchable_fields"]["file_path"] is True


def test_audit_thumbnail_template_fails_without_thumb_slots() -> None:
    result = audit_thumbnail_template({"Timelines": [{"Items": [{"Remark": "not_thumb"}]}]})

    assert result["success"] is False
    assert result["errors"] == [
        "THUMB_TEMPLATE_NO_SLOTS: no thumb.text.* or thumb.image.* Remark slots found"
    ]


def test_patch_thumbnail_template_updates_text_image_color_and_geometry() -> None:
    ymmp = _thumb_ymmp()

    result = patch_thumbnail_template(
        ymmp,
        {
            "text": {
                "title": {
                    "value": "新しい訴求",
                    "color": "#FFFF0000",
                    "x": 12.0,
                    "zoom": 110.0,
                },
            },
            "image": {
                "background": {
                    "file_path": "new_bg.png",
                    "y": -8.0,
                    "zoom": 105.0,
                },
            },
        },
    )

    text_item = ymmp["Timelines"][0]["Items"][0]
    image_item = ymmp["Timelines"][0]["Items"][1]
    assert result["success"] is True
    assert result["text_changes"] == 1
    assert result["image_changes"] == 1
    assert result["color_changes"] == 1
    assert result["geometry_changes"] == 4
    assert text_item["Text"] == "新しい訴求"
    assert text_item["Color"] == "#FFFF0000"
    assert text_item["X"]["Values"][0]["Value"] == 12.0
    assert text_item["Zoom"]["Values"][0]["Value"] == 110.0
    assert image_item["FilePath"] == "new_bg.png"
    assert image_item["Y"]["Values"][0]["Value"] == -8.0
    assert image_item["Zoom"]["Values"][0]["Value"] == 105.0
    assert result["readback"]["success"] is True
    assert result["readback"]["check_count"] == 7


def test_verify_thumbnail_patch_readback_reports_mismatch() -> None:
    result = verify_thumbnail_patch_readback(
        _thumb_ymmp(),
        {"text": {"title": {"value": "EXPECTED", "x": 12.0}}},
    )

    assert result["success"] is False
    assert result["check_count"] == 2
    assert result["checks"][0]["field"] == "text"
    assert result["checks"][0]["success"] is False
    assert result["checks"][1]["field"] == "x"
    assert result["checks"][1]["success"] is False


def test_patch_thumbnail_template_fails_on_missing_slot() -> None:
    result = patch_thumbnail_template(_thumb_ymmp(), {"text": {"missing": "x"}})

    assert result["success"] is False
    assert result["errors"] == ["THUMB_SLOT_MISSING: thumb.text.missing"]


def test_cli_audit_thumbnail_template_json(tmp_path, capsys) -> None:
    ymmp_path = tmp_path / "thumb_template.ymmp"
    save_ymmp(_thumb_ymmp(), ymmp_path)

    code = main(["audit-thumbnail-template", str(ymmp_path), "--format", "json"])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["success"] is True
    assert result["slot_count"] == 2


def test_cli_patch_thumbnail_template_writes_ymmp(tmp_path, capsys) -> None:
    ymmp_path = tmp_path / "thumb_template.ymmp"
    patch_path = tmp_path / "thumb_patch.json"
    output_path = tmp_path / "thumb_patched.ymmp"
    save_ymmp(_thumb_ymmp(), ymmp_path)
    patch_path.write_text(
        json.dumps({
            "text": {"title": "差し替え済み"},
            "image": {"background": "new_bg.png"},
        }),
        encoding="utf-8",
    )

    code = main([
        "patch-thumbnail-template",
        str(ymmp_path),
        "--patch",
        str(patch_path),
        "-o",
        str(output_path),
    ])

    assert code == 0
    assert "Written:" in capsys.readouterr().out
    patched = load_ymmp(output_path)
    assert patched["Timelines"][0]["Items"][0]["Text"] == "差し替え済み"
    assert patched["Timelines"][0]["Items"][1]["FilePath"] == "new_bg.png"


def test_cli_patch_thumbnail_template_json_includes_file_readback(tmp_path, capsys) -> None:
    ymmp_path = tmp_path / "thumb_template.ymmp"
    patch_path = tmp_path / "thumb_patch.json"
    output_path = tmp_path / "thumb_patched.ymmp"
    save_ymmp(_thumb_ymmp(), ymmp_path)
    patch_path.write_text(
        json.dumps({
            "text": {"title": {"value": "差し替え済み", "x": 4.0}},
            "image": {"background": {"file_path": "new_bg.png", "zoom": 103.0}},
        }),
        encoding="utf-8",
    )

    code = main([
        "patch-thumbnail-template",
        str(ymmp_path),
        "--patch",
        str(patch_path),
        "-o",
        str(output_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["file_readback"]["success"] is True
    assert result["file_readback"]["check_count"] == 4
    assert {check["field"] for check in result["file_readback"]["checks"]} == {
        "text",
        "x",
        "file_path",
        "zoom",
    }

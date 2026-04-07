"""パイプラインスモークテスト。"""

import subprocess
import sys

from src.pipeline.normalize import normalize
from src.pipeline.assemble_csv import assemble


def test_csv_to_csv_roundtrip(tmp_path):
    """CSV 入力 → speaker_map 付き CSV 出力。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )

    script = normalize(input_csv)
    output = assemble(script, speaker_map={"Host1": "れいむ", "Host2": "まりさ"})

    out_path = tmp_path / "out.csv"
    output.write(out_path)

    lines = out_path.read_text(encoding="utf-8-sig").strip().splitlines()
    assert lines[0].startswith("れいむ,")
    assert lines[1].startswith("まりさ,")


def test_text_to_csv(tmp_path):
    """テキスト入力 → CSV 出力。"""
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "[00:00] Host1: 今日のテーマはAI技術です\n"
        "[00:10] Host2: 楽しみにしています\n",
        encoding="utf-8",
    )

    script = normalize(input_txt)
    output = assemble(script)

    assert len(output.rows) == 2
    assert output.rows[0].speaker == "Host1"
    assert output.rows[0].text == "今日のテーマはAI技術です"


def test_cli_build_csv(tmp_path):
    """CLI build-csv がファイルを生成する。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "out.csv"

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "build-csv", str(input_csv), "-o", str(out_csv)],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert out_csv.exists()
    content = out_csv.read_text(encoding="utf-8")
    assert "Host1" in content


def test_cli_validate(tmp_path):
    """CLI validate が正常終了する。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "validate", str(input_csv)],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "2 utterances" in result.stdout


def test_analyze_speaker_roles_host_guest():
    """ロール推定: 長文話者=host、短応答話者=guest。"""
    from src.pipeline.normalize import analyze_speaker_roles
    from src.contracts.structured_script import StructuredScript, Utterance

    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="というわけで今回はAI技術の最新動向について詳しく解説していきます。"),
        Utterance(speaker="Speaker_B", text="はい。"),
        Utterance(speaker="Speaker_A", text="まずディープラーニングの進化ですが、トランスフォーマーモデルが登場してから劇的に変わりました。"),
        Utterance(speaker="Speaker_B", text="なるほど、具体的にはどういう変化ですか?"),
        Utterance(speaker="Speaker_A", text="自然言語処理の精度が飛躍的に向上し、以前は不可能だったタスクが実現できるようになったんです。"),
        Utterance(speaker="Speaker_B", text="ええ。"),
    ))

    roles = analyze_speaker_roles(script)
    assert roles["Speaker_A"]["role"] == "host"
    assert roles["Speaker_B"]["role"] == "guest"
    assert roles["Speaker_A"]["avg_length"] > roles["Speaker_B"]["avg_length"]


def test_load_ir_single_object(tmp_path):
    """load_ir: 単一 JSON オブジェクトを読み込む。"""
    from src.pipeline.ymmp_patch import load_ir

    ir_file = tmp_path / "ir.json"
    ir_file.write_text(
        '{"ir_version": "1.0", "macro": {"sections": []}, "utterances": []}',
        encoding="utf-8",
    )
    data = load_ir(ir_file)
    assert data["ir_version"] == "1.0"
    assert "macro" in data
    assert "utterances" in data


def test_load_ir_multi_object(tmp_path):
    """load_ir: 2つの JSON オブジェクト連結形式を読み込む。"""
    from src.pipeline.ymmp_patch import load_ir

    ir_file = tmp_path / "ir.json"
    ir_file.write_text(
        '{"ir_version": "1.0", "macro": {"sections": []}}\n'
        '{"utterances": [{"index": 1, "speaker": "A", "text": "hello"}]}',
        encoding="utf-8",
    )
    data = load_ir(ir_file)
    assert data["ir_version"] == "1.0"
    assert "macro" in data
    assert len(data["utterances"]) == 1
    assert data["utterances"][0]["speaker"] == "A"


def test_cli_apply_production_with_palette(tmp_path):
    """CLI apply-production が palette から face_map 抽出 + patch を実行する。"""
    import json

    # --- palette ymmp ---
    palette = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.TachieFaceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Remark": "smile",
                "Frame": 0, "Length": 100, "Layer": 0, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "smile_eb.png", "Eye": "smile_ey.png",
                    "Mouth": "smile_mo.png", "Hair": "", "Body": "", "Complexion": "",
                },
                "TachieFaceEffects": [],
                "KeyFrames": {"Frames": [], "Count": 0},
                "PlaybackRate": 100.0, "ContentOffset": "00:00:00",
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    palette_path = tmp_path / "palette.ymmp"
    with open(palette_path, "w", encoding="utf-8-sig") as f:
        json.dump(palette, f)

    # --- production ymmp ---
    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa", "Serif": "test", "Remark": "",
                "Frame": 0, "Length": 100, "Layer": 1, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png", "Eye": "default.png",
                    "Mouth": "default.png", "Hair": "", "Body": "", "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    # --- IR ---
    ir = {
        "ir_version": "1.0", "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1,
                                 "end_index": 1, "default_face": "smile"}]},
        "utterances": [{"index": 1, "speaker": "marisa", "text": "t",
                        "section_id": "S1", "face": "smile"}],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    out_path = tmp_path / "output.ymmp"

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "apply-production",
         str(prod_path), str(ir_path),
         "--palette", str(palette_path),
         "-o", str(out_path)],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert out_path.exists()
    assert "Face changes:" in result.stdout
    assert "extracted from" in result.stdout

    # face_map.json が palette 隣に生成されている
    assert (tmp_path / "face_map.json").exists()


def test_cli_apply_production_with_face_map(tmp_path):
    """CLI apply-production が既存 face_map で動作する。"""
    import json

    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa", "Serif": "test", "Remark": "",
                "Frame": 0, "Length": 100, "Layer": 1, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png", "Eye": "default.png",
                    "Mouth": "default.png", "Hair": "", "Body": "", "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    ir = {
        "ir_version": "1.0", "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1,
                                 "end_index": 1, "default_face": "smile"}]},
        "utterances": [{"index": 1, "speaker": "marisa", "text": "t",
                        "section_id": "S1", "face": "smile"}],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    face_map = {"marisa": {"smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}}
    fm_path = tmp_path / "face_map.json"
    fm_path.write_text(json.dumps(face_map), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "apply-production",
         str(prod_path), str(ir_path),
         "--face-map", str(fm_path),
         "--dry-run"],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "Face changes:" in result.stdout
    assert "(loaded)" in result.stdout


def test_cli_apply_production_fails_on_active_face_gap(tmp_path):
    """CLI apply-production は current IR の active gap を検出して止まる。"""
    import json

    palette = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.TachieFaceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Remark": "smile",
                "Frame": 0, "Length": 100, "Layer": 0, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "m_smile.png", "Eye": "m_smile.png",
                    "Mouth": "m_smile.png", "Hair": "", "Body": "", "Complexion": "",
                },
                "TachieFaceEffects": [],
                "KeyFrames": {"Frames": [], "Count": 0},
                "PlaybackRate": 100.0, "ContentOffset": "00:00:00",
            },
            {
                "$type": "YukkuriMovieMaker.Project.Items.TachieFaceItem, YukkuriMovieMaker",
                "CharacterName": "reimu",
                "Remark": "serious",
                "Frame": 100, "Length": 100, "Layer": 0, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "r_serious.png", "Eye": "r_serious.png",
                    "Mouth": "r_serious.png", "Hair": "", "Body": "", "Complexion": "",
                },
                "TachieFaceEffects": [],
                "KeyFrames": {"Frames": [], "Count": 0},
                "PlaybackRate": 100.0, "ContentOffset": "00:00:00",
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}, {"Name": "reimu"}],
    }
    palette_path = tmp_path / "palette.ymmp"
    with open(palette_path, "w", encoding="utf-8-sig") as f:
        json.dump(palette, f)

    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "reimu", "Serif": "test", "Remark": "",
                "Frame": 0, "Length": 100, "Layer": 1, "Group": 0,
                "IsLocked": False, "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png", "Eye": "default.png",
                    "Mouth": "default.png", "Hair": "", "Body": "", "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}, {"Name": "reimu"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    ir = {
        "ir_version": "1.0", "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1,
                                 "end_index": 1, "default_face": "smile"}]},
        "utterances": [{"index": 1, "speaker": "reimu", "text": "t",
                        "section_id": "S1", "face": "smile"}],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    out_path = tmp_path / "output.ymmp"
    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "apply-production",
         str(prod_path), str(ir_path),
         "--palette", str(palette_path),
         "-o", str(out_path)],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    assert "FACE_ACTIVE_GAP" in result.stderr
    assert not out_path.exists()


def test_cli_validate_ir_fails_on_slot_default_drift(tmp_path):
    """CLI validate-ir は slot default drift を検出して止まる。"""
    import json

    ir = {
        "ir_version": "1.0",
        "video_id": "slot_validate",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "end_index": 1,
                "default_face": "serious",
            }],
        },
        "utterances": [{
            "index": 1,
            "speaker": "marisa",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
            "slot": "right",
        }],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    slot_contract = {
        "slots": {
            "left": {"x": -737, "y": 540, "zoom": 120},
            "right": {"x": 708, "y": 540, "zoom": 120},
        },
        "characters": {
            "marisa": {"default_slot": "left"},
        },
    }
    slot_path = tmp_path / "slot_map.json"
    slot_path.write_text(json.dumps(slot_contract), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "validate-ir",
         str(ir_path),
         "--slot-map", str(slot_path)],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    assert "SLOT_DEFAULT_DRIFT" in result.stderr
    assert "slot contract: 2 labels" in result.stdout


def test_cli_apply_production_with_slot_map(tmp_path):
    """CLI apply-production は slot_map を読み dry-run まで通せる。"""
    import json

    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Remark": "",
                "Frame": 0,
                "Length": 100,
                "Layer": 0,
                "Group": 0,
                "IsLocked": False,
                "IsHidden": False,
                "TachieItemParameter": {
                    "Eyebrow": "default.png",
                    "Eye": "default.png",
                    "Mouth": "default.png",
                    "Hair": "",
                    "Body": "",
                    "X": 0.0,
                    "Y": 540.0,
                    "Zoom": 100.0,
                },
            },
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Serif": "test",
                "Remark": "",
                "Frame": 0,
                "Length": 100,
                "Layer": 1,
                "Group": 0,
                "IsLocked": False,
                "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png",
                    "Eye": "default.png",
                    "Mouth": "default.png",
                    "Hair": "",
                    "Body": "",
                    "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    ir = {
        "ir_version": "1.0",
        "video_id": "slot_apply",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "end_index": 1,
                "default_face": "serious",
            }],
        },
        "utterances": [{
            "index": 1,
            "speaker": "marisa",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
            "slot": "left",
        }],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    face_map = {
        "serious": {
            "Eyebrow": "serious_eb.png",
            "Eye": "serious_ey.png",
            "Mouth": "serious_mo.png",
        }
    }
    face_map_path = tmp_path / "face_map.json"
    face_map_path.write_text(json.dumps(face_map), encoding="utf-8")

    slot_contract = {
        "slots": {
            "left": {"x": -737, "y": 540, "zoom": 120},
        },
        "characters": {
            "marisa": {"default_slot": "left"},
        },
    }
    slot_path = tmp_path / "slot_map.json"
    slot_path.write_text(json.dumps(slot_contract), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "apply-production",
         str(prod_path), str(ir_path),
         "--face-map", str(face_map_path),
         "--slot-map", str(slot_path),
         "--dry-run"],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "slot_map:" in result.stdout
    assert "Slot changes:" in result.stdout
    assert "(dry-run: no file written)" in result.stdout


def test_cli_measure_timeline_routes_json(tmp_path):
    """CLI measure-timeline-routes は candidate route report を返す。"""
    import json

    ymmp = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                "FilePath": "C:/bg.png",
                "X": {"Values": [{"Value": 0.0}]},
                "Y": {"Values": [{"Value": 0.0}]},
                "Zoom": {"Values": [{"Value": 100.0}]},
                "VideoEffects": [{
                    "$type": "YukkuriMovieMaker.Plugin.Effects.StripeGlitchNoise, YukkuriMovieMaker.Plugin.Effects",
                    "Name": "Glitch",
                }],
                "TemplateName": "BG Pan",
            },
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "VideoEffects": [{
                    "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
                    "Name": "Bounce",
                }],
                "Transition": {"Name": "Fade"},
                "VoiceFadeIn": 0.2,
                "VoiceFadeOut": 0.3,
            },
        ], "LayerSettings": []}],
    }
    ymmp_path = tmp_path / "measurement.ymmp"
    with open(ymmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(ymmp, f)

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "measure-timeline-routes",
         str(ymmp_path), "--format", "json"],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    payload = json.loads(result.stdout)
    assert payload["item_type_counts"]["ImageItem"] == 1
    assert payload["route_counts"]["bg_anim"]["ImageItem.VideoEffects"] == 1
    assert payload["route_counts"]["motion"]["VoiceItem.VideoEffects"] == 1
    assert payload["route_counts"]["transition"]["VoiceItem.VoiceFadeIn"] == 1
    assert payload["template_name_counts"]["BG Pan"] == 1


def test_cli_measure_timeline_routes_expect_fails_on_missing_route(tmp_path):
    """CLI measure-timeline-routes は contract miss を exit 1 で返す。"""
    import json

    ymmp = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "VideoEffects": [],
            },
        ], "LayerSettings": []}],
    }
    ymmp_path = tmp_path / "measurement.ymmp"
    with open(ymmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(ymmp, f)

    contract = {
        "required_routes": {
            "motion": ["VoiceItem.VideoEffects"],
            "transition": ["VoiceItem.Transition"],
        }
    }
    contract_path = tmp_path / "routes.json"
    contract_path.write_text(json.dumps(contract), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "measure-timeline-routes",
         str(ymmp_path), "--expect", str(contract_path)],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    assert "TIMELINE_ROUTE_MISS" in result.stdout


def test_cli_measure_timeline_routes_expect_optional_warns_only(tmp_path):
    """CLI measure-timeline-routes は optional miss だけなら成功する。"""
    import json

    ymmp = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                "X": {"Values": [{"Value": 0.0}]},
                "Y": {"Values": [{"Value": 0.0}]},
                "Zoom": {"Values": [{"Value": 100.0}]},
            },
        ], "LayerSettings": []}],
    }
    ymmp_path = tmp_path / "measurement.ymmp"
    with open(ymmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(ymmp, f)

    contract = {
        "required_routes": {
            "bg_anim": ["ImageItem.X/Y/Zoom"],
        },
        "optional_routes": {
            "transition": ["VoiceItem.Transition"],
        },
    }
    contract_path = tmp_path / "routes.json"
    contract_path.write_text(json.dumps(contract), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "measure-timeline-routes",
         str(ymmp_path), "--expect", str(contract_path)],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0
    assert "TIMELINE_ROUTE_OPTIONAL_MISS" in result.stdout


def test_cli_measure_timeline_routes_profile_selection(tmp_path):
    """CLI measure-timeline-routes は profile 指定で contract を選べる。"""
    import json

    ymmp = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                "TachieItemParameter": {
                    "X": -737.0,
                    "Y": 540.0,
                    "Zoom": 120.0,
                },
                "VideoEffects": [],
            },
        ], "LayerSettings": []}],
    }
    ymmp_path = tmp_path / "measurement.ymmp"
    with open(ymmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(ymmp, f)

    contract = {
        "profiles": {
            "motion_only": {
                "required_routes": {
                    "motion": ["TachieItem.VideoEffects"],
                }
            }
        }
    }
    contract_path = tmp_path / "routes.json"
    contract_path.write_text(json.dumps(contract), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "measure-timeline-routes",
         str(ymmp_path), "--expect", str(contract_path), "--profile", "motion_only"],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"


def test_cli_measure_timeline_routes_unknown_profile_fails(tmp_path):
    """CLI measure-timeline-routes は unknown profile を failure にする。"""
    import json

    ymmp = {"Timelines": [{"ID": 0, "Items": [], "LayerSettings": []}]}
    ymmp_path = tmp_path / "measurement.ymmp"
    with open(ymmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(ymmp, f)

    contract_path = tmp_path / "routes.json"
    contract_path.write_text(json.dumps({"profiles": {}}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "measure-timeline-routes",
         str(ymmp_path), "--expect", str(contract_path), "--profile", "missing"],
        capture_output=True, text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    assert "TIMELINE_ROUTE_PROFILE_UNKNOWN" in result.stdout


def test_cli_validate_ir_with_overlay_and_se_contracts(tmp_path):
    """CLI validate-ir は overlay / se registry も見る."""
    import json

    ir = {
        "ir_version": "1.0",
        "video_id": "timeline_validate",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 1, "default_face": "serious", "default_bg": "bg1"}]},
        "utterances": [{
            "index": 1,
            "speaker": "marisa",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
            "overlay": "arrow_red",
            "se": "click",
        }],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    overlay_path = tmp_path / "overlay_map.json"
    overlay_path.write_text(json.dumps({"overlays": {"arrow_red": "C:/overlay/arrow_red.png"}}), encoding="utf-8")

    se_path = tmp_path / "se_map.json"
    se_path.write_text(json.dumps({"se": {"click": "C:/se/click.wav"}}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "validate-ir",
         str(ir_path),
         "--overlay-map", str(overlay_path),
         "--se-map", str(se_path)],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "overlay contract: 1 labels" in result.stdout
    assert "se contract: 1 labels" in result.stdout


def test_cli_patch_ymmp_with_overlay_map(tmp_path):
    """CLI patch-ymmp は overlay を dry-run まで反映する."""
    import json

    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Serif": "test",
                "Remark": "",
                "Frame": 0,
                "Length": 100,
                "Layer": 1,
                "Group": 0,
                "IsLocked": False,
                "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png",
                    "Eye": "default.png",
                    "Mouth": "default.png",
                    "Hair": "",
                    "Body": "",
                    "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    ir = {
        "ir_version": "1.0",
        "video_id": "overlay_apply",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 1, "default_face": "serious", "default_bg": "bg1"}]},
        "utterances": [{
            "index": 1,
            "speaker": "marisa",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
            "overlay": "arrow_red",
            "row_start": 1,
            "row_end": 1,
        }],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    face_map_path = tmp_path / "face_map.json"
    face_map_path.write_text(json.dumps({"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}), encoding="utf-8")

    overlay_path = tmp_path / "overlay_map.json"
    overlay_path.write_text(json.dumps({
        "overlays": {
            "arrow_red": {
                "path": "C:/overlay/arrow_red.png",
                "layer": 4,
                "length": 12,
            }
        }
    }), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "patch-ymmp",
         str(prod_path), str(ir_path),
         "--face-map", str(face_map_path),
         "--overlay-map", str(overlay_path),
         "--dry-run"],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "overlay_map:" in result.stdout
    assert "Overlay changes: 1" in result.stdout


def test_cli_patch_ymmp_se_route_is_blocking(tmp_path):
    """CLI patch-ymmp は se route 未固定を fail-fast で止める."""
    import json

    production = {
        "Timelines": [{"ID": 0, "Items": [
            {
                "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                "CharacterName": "marisa",
                "Serif": "test",
                "Remark": "",
                "Frame": 0,
                "Length": 100,
                "Layer": 1,
                "Group": 0,
                "IsLocked": False,
                "IsHidden": False,
                "TachieFaceParameter": {
                    "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                    "Eyebrow": "default.png",
                    "Eye": "default.png",
                    "Mouth": "default.png",
                    "Hair": "",
                    "Body": "",
                    "Complexion": "",
                },
            },
        ], "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }
    prod_path = tmp_path / "production.ymmp"
    with open(prod_path, "w", encoding="utf-8-sig") as f:
        json.dump(production, f)

    ir = {
        "ir_version": "1.0",
        "video_id": "se_apply",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 1, "default_face": "serious", "default_bg": "bg1"}]},
        "utterances": [{
            "index": 1,
            "speaker": "marisa",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
            "se": "click",
            "row_start": 1,
            "row_end": 1,
        }],
    }
    ir_path = tmp_path / "ir.json"
    ir_path.write_text(json.dumps(ir), encoding="utf-8")

    face_map_path = tmp_path / "face_map.json"
    face_map_path.write_text(json.dumps({"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}), encoding="utf-8")

    se_path = tmp_path / "se_map.json"
    se_path.write_text(json.dumps({"se": {"click": "C:/se/click.wav"}}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "patch-ymmp",
         str(prod_path), str(ir_path),
         "--face-map", str(face_map_path),
         "--se-map", str(se_path),
         "--dry-run"],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0
    assert "SE insertions: 1" in result.stdout
    assert "SE_WRITE_ROUTE_UNSUPPORTED" not in result.stderr


def _project_root():
    """プロジェクトルートを返す。"""
    from pathlib import Path
    return Path(__file__).resolve().parent.parent

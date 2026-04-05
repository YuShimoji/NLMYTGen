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


def _project_root():
    """プロジェクトルートを返す。"""
    from pathlib import Path
    return Path(__file__).resolve().parent.parent

"""ymmp 後処理変換器 (G-06).

演出 IR JSON を読み込み、既存 ymmp の face (表情パーツ) と
bg (背景画像) を差し替える。音声・字幕は台本読込で確保済みのまま維持。

Usage (via CLI):
    python -m src.cli.main patch-ymmp project.ymmp ir.json -o patched.ymmp
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PatchResult:
    """差し替え結果のサマリ."""

    face_changes: int = 0
    bg_changes: int = 0
    bg_additions: int = 0
    tachie_syncs: int = 0
    warnings: list[str] | None = None

    def __post_init__(self) -> None:
        if self.warnings is None:
            self.warnings = []


def load_ir(path: str | Path) -> dict:
    """IR JSON を読み込む。単一オブジェクトと2オブジェクト連結の両方に対応."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # まず単一 JSON として試す
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 2つの JSON オブジェクト連結として処理
    depth = 0
    first_end = -1
    for i, ch in enumerate(content):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                first_end = i + 1
                break

    if first_end <= 0:
        raise ValueError("IR JSON の解析に失敗しました")

    obj1 = json.loads(content[:first_end])
    obj2 = json.loads(content[first_end:].strip())
    return {**obj1, **obj2}


def load_ymmp(path: str | Path) -> dict:
    """ymmp (UTF-8 BOM 付き JSON) を読み込む."""
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_ymmp(data: dict, path: str | Path) -> None:
    """ymmp を UTF-8 BOM 付き JSON で書き出す."""
    with open(path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_timeline_items(data: dict) -> list[dict]:
    """ymmp のタイムラインアイテムを取得する.

    YMM4 v4.30+ は Timelines[] 形式、それ以前は Timeline 形式。
    """
    # 新形式 (Timelines[])
    timelines = data.get("Timelines")
    if timelines and isinstance(timelines, list) and len(timelines) > 0:
        return timelines[0].get("Items", [])
    # 旧形式 (Timeline)
    timeline = data.get("Timeline")
    if timeline and isinstance(timeline, dict):
        return timeline.get("Items", [])
    return []


def _item_type(item: dict) -> str:
    """$type から短いタイプ名を抽出."""
    t = item.get("$type", "")
    return t.split(",")[0].split(".")[-1] if "." in t else t


def _resolve_face_parts(
    face_label: str,
    face_map: dict,
    character_name: str | None = None,
) -> dict[str, str] | None:
    """IR の face ラベルをパーツファイルパスの辞書に解決する.

    character-scoped map (推奨):
    {
        "まりさ": {
            "serious": {"Eyebrow": "D:/.../03c.png", ...},
            "smile": {"Eyebrow": "D:/.../01c.png", ...}
        }
    }

    flat map (後方互換):
    {
        "serious": {"Eyebrow": "D:/.../03c.png", ...},
        "smile": {"Eyebrow": "D:/.../01c.png", ...}
    }
    """
    # character-scoped: face_map[character_name][face_label]
    if character_name and character_name in face_map:
        char_entry = face_map[character_name]
        if isinstance(char_entry, dict):
            candidate = char_entry.get(face_label)
            if isinstance(candidate, dict) and all(
                isinstance(v, str) for v in candidate.values()
            ):
                return candidate

    # flat fallback: face_map[face_label]
    candidate = face_map.get(face_label)
    if isinstance(candidate, dict) and all(
        isinstance(v, str) for v in candidate.values()
    ):
        return candidate

    return None


def _resolve_bg(
    bg_label: str, bg_map: dict[str, str]
) -> str | None:
    """IR の bg ラベルをファイルパスに解決する.

    bg_map の例:
    {"studio_blue": "C:/.../studio_blue.png", "dark_board": "C:/.../dark.png"}
    """
    return bg_map.get(bg_label)


def _apply_face_to_voice_item(
    voice_item: dict,
    vi_index: int,
    face_label: str,
    face_map: dict,
    result: PatchResult,
) -> None:
    """1 つの VoiceItem に face パーツを適用する."""
    character_name = voice_item.get("CharacterName")
    parts = _resolve_face_parts(face_label, face_map, character_name)
    if parts:
        fp = voice_item.get("TachieFaceParameter")
        if fp:
            for part_name, file_path in parts.items():
                if part_name in fp and fp[part_name] != file_path:
                    fp[part_name] = file_path
                    result.face_changes += 1
        else:
            result.warnings.append(
                f"VoiceItem index={vi_index + 1} has no TachieFaceParameter"
            )
    else:
        result.warnings.append(
            f"face label '{face_label}' not found in face_map"
        )


def _apply_face_positional(
    voice_items: list[dict],
    resolved: list[dict],
    face_map: dict,
    result: PatchResult,
) -> None:
    """位置ベースの face 適用 (後方互換)."""
    for i, voice_item in enumerate(voice_items):
        if i >= len(resolved):
            break
        ir_entry = resolved[i]
        face_label = ir_entry.get("face")
        if face_label:
            _apply_face_to_voice_item(voice_item, i, face_label, face_map, result)


def _apply_face_row_range(
    voice_items: list[dict],
    resolved: list[dict],
    face_map: dict,
    result: PatchResult,
) -> None:
    """row_start / row_end ベースの face 適用.

    各 IR utterance の row_start..row_end (1-based, inclusive) の
    VoiceItem 全てに同じ face を適用する。
    """
    num_vi = len(voice_items)
    for ir_entry in resolved:
        face_label = ir_entry.get("face")
        if not face_label:
            continue
        row_start = ir_entry.get("row_start")
        row_end = ir_entry.get("row_end")
        if row_start is None or row_end is None:
            result.warnings.append(
                f"utterance index={ir_entry.get('index', '?')}"
                f" missing row_start/row_end"
            )
            continue
        if row_start < 1 or row_end < row_start:
            result.warnings.append(
                f"utterance index={ir_entry.get('index', '?')}"
                f" invalid row_start={row_start} row_end={row_end}"
            )
            continue
        # 1-based → 0-based
        for vi_idx in range(row_start - 1, min(row_end, num_vi)):
            _apply_face_to_voice_item(
                voice_items[vi_idx], vi_idx, face_label, face_map, result
            )


def _build_tachie_face_item(
    character_name: str,
    parts: dict[str, str],
    frame: int,
    length: int,
) -> dict:
    """TachieFaceItem を生成する."""
    tfp = {
        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter,"
                 " YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
        "EyeAnimation": "Default",
        "MouthAnimation": "Default",
        "Eyebrow": parts.get("Eyebrow"),
        "Eye": parts.get("Eye"),
        "Mouth": parts.get("Mouth"),
        "Hair": parts.get("Hair"),
        "Complexion": parts.get("Complexion"),
        "Body": parts.get("Body"),
        "Back1": None,
        "Back2": None,
        "Back3": None,
        "Etc1": None,
        "Etc2": None,
        "Etc3": None,
    }
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TachieFaceItem,"
                 " YukkuriMovieMaker",
        "CharacterName": character_name,
        "TachieFaceParameter": tfp,
        "TachieFaceEffects": [],
        "Group": 0,
        "Frame": frame,
        "Layer": 0,
        "KeyFrames": {"Frames": [], "Count": 0},
        "Length": length,
        "PlaybackRate": 100.0,
        "ContentOffset": "00:00:00",
        "Remark": "",
        "IsLocked": False,
        "IsHidden": False,
    }


def _apply_idle_face(
    items: list[dict],
    voice_items: list[dict],
    resolved: list[dict],
    face_map: dict,
    result: PatchResult,
    use_row_range: bool,
) -> None:
    """待機中キャラに idle_face の TachieFaceItem を挿入する.

    idle_face が指定された utterance で、発話者以外のキャラに
    TachieFaceItem を挿入して待機中表情を制御する。
    """
    # idle_face を持つ utterance があるか判定
    has_idle = any(e.get("idle_face") for e in resolved)
    if not has_idle:
        return

    # 全キャラクター名を収集 (VoiceItem から)
    all_chars = {vi.get("CharacterName", "") for vi in voice_items}
    all_chars.discard("")

    for ir_entry in resolved:
        idle_label = ir_entry.get("idle_face")
        if not idle_label:
            continue

        # 発話者の特定 (row-range モードでは row_start の VoiceItem から)
        if use_row_range:
            rs = ir_entry.get("row_start")
            if rs is None or rs < 1 or rs - 1 >= len(voice_items):
                continue
            speaker = voice_items[rs - 1].get("CharacterName", "")
            # Frame 範囲
            re_ = ir_entry.get("row_end", rs)
            start_frame = voice_items[rs - 1].get("Frame", 0)
            end_vi_idx = min(re_, len(voice_items)) - 1
            end_frame = (
                voice_items[end_vi_idx].get("Frame", 0)
                + voice_items[end_vi_idx].get("Length", 0)
            )
        else:
            idx = ir_entry.get("index", 1) - 1
            if idx < 0 or idx >= len(voice_items):
                continue
            speaker = voice_items[idx].get("CharacterName", "")
            start_frame = voice_items[idx].get("Frame", 0)
            end_frame = start_frame + voice_items[idx].get("Length", 0)

        if not speaker:
            continue

        length = max(end_frame - start_frame, 1)

        # non-speaker キャラに idle_face を適用
        for char in all_chars:
            if char == speaker:
                continue
            parts = _resolve_face_parts(idle_label, face_map, char)
            if parts:
                face_item = _build_tachie_face_item(
                    char, parts, start_frame, length
                )
                items.append(face_item)
                result.tachie_syncs += 1
            else:
                result.warnings.append(
                    f"idle_face '{idle_label}' not found in face_map"
                    f" for character '{char}'"
                )


def patch_ymmp(
    ymmp_data: dict,
    ir_data: dict,
    face_map: dict[str, dict[str, str]],
    bg_map: dict[str, str],
) -> PatchResult:
    """演出 IR に従って ymmp を差し替える.

    Parameters
    ----------
    ymmp_data : dict
        load_ymmp() で読み込んだ ymmp データ (in-place で変更される)
    ir_data : dict
        演出 IR JSON (PRODUCTION_IR_SPEC v1.0 準拠)
    face_map : dict
        face ラベル → パーツファイルパスの辞書
    bg_map : dict
        bg ラベル → 画像/動画ファイルパスの辞書

    Returns
    -------
    PatchResult
    """
    result = PatchResult()
    items = _get_timeline_items(ymmp_data)
    utterances = ir_data.get("utterances", [])

    # IR の carry-forward を解決
    resolved = _resolve_carry_forward(ir_data)

    # index → VoiceItem の Frame 順マッピングを構築
    voice_items = [
        item for item in items if _item_type(item) == "VoiceItem"
    ]
    voice_items.sort(key=lambda x: x.get("Frame", 0))

    # --- face 差し替え ---
    # row-range モード判定: 最初の utterance に row_start があれば有効
    use_row_range = bool(
        resolved and resolved[0].get("row_start") is not None
    )

    if use_row_range:
        _apply_face_row_range(voice_items, resolved, face_map, result)
    else:
        _apply_face_positional(voice_items, resolved, face_map, result)

    # --- idle_face (待機中表情) ---
    # IR に idle_face が指定されている場合、各 utterance の開始 Frame に
    # non-speaker キャラの TachieFaceItem を挿入する
    _apply_idle_face(items, voice_items, resolved, face_map, result,
                     use_row_range)

    # --- bg 差し替え ---
    # 既存の bg_items (Layer 0 の ImageItem/VideoItem) を削除し、
    # セクションごとに正しい Frame/Length で再配置する
    bg_item_types = ("ImageItem", "VideoItem")
    existing_bg = [
        item for item in items
        if _item_type(item) in bg_item_types
        and item.get("Layer", -1) == 0
    ]
    # テンプレートとして最初の bg_item を保持 (プロパティのコピー元)
    bg_template = existing_bg[0] if existing_bg else None

    # 既存 bg を items から除去
    for bg_item in existing_bg:
        items.remove(bg_item)
        result.bg_changes += 1

    # --- utterance index → VoiceItem index の変換マップ (row-range 用) ---
    utt_to_vi_start: dict[int, int] = {}
    if use_row_range:
        for entry in resolved:
            utt_idx = entry.get("index", 0)
            rs = entry.get("row_start")
            if rs is not None:
                utt_to_vi_start[utt_idx] = rs - 1  # 1-based → 0-based

    # セクションごとに新しい bg_item を生成
    sections = ir_data.get("macro", {}).get("sections", [])
    for sec_idx, section in enumerate(sections):
        bg_label = section.get("default_bg")
        if not bg_label:
            continue
        bg_path = _resolve_bg(bg_label, bg_map)
        if not bg_path:
            result.warnings.append(
                f"bg label '{bg_label}' not found in bg_map"
            )
            continue

        # start_index は IR utterance index (1-based)
        utt_start = section.get("start_index", 1)

        if use_row_range:
            # row-range: utterance の row_start から VoiceItem index を引く
            start_idx = utt_to_vi_start.get(utt_start, utt_start - 1)
        else:
            start_idx = utt_start - 1

        # セクションの Frame 範囲を計算
        # 開始: このセクションの最初の VoiceItem の Frame
        # 終了: 次のセクションの最初の VoiceItem の Frame (なければタイムライン末尾)
        if start_idx >= len(voice_items):
            continue
        section_start = voice_items[start_idx].get("Frame", 0)
        # 最初のセクションはタイムライン冒頭 (Frame=0) から開始
        if sec_idx == 0:
            section_start = 0

        # 次のセクションの開始を探す
        next_section_start = None
        if sec_idx + 1 < len(sections):
            next_utt_start = sections[sec_idx + 1].get("start_index", 1)
            if use_row_range:
                next_start_idx = utt_to_vi_start.get(
                    next_utt_start, next_utt_start - 1
                )
            else:
                next_start_idx = next_utt_start - 1
            if next_start_idx < len(voice_items):
                next_section_start = voice_items[next_start_idx].get("Frame", 0)

        if next_section_start is not None:
            section_end = next_section_start
        else:
            # 最後のセクション: タイムライン末尾まで
            last_vi = voice_items[-1]
            section_end = last_vi.get("Frame", 0) + last_vi.get("Length", 0)

        section_length = max(section_end - section_start, 1)

        # bg_item を生成
        if bg_template:
            import copy
            new_bg = copy.deepcopy(bg_template)
        else:
            new_bg = {
                "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                "X": {"Values": [{"Value": 0.0}], "Span": 0.0, "AnimationType": "\u306a\u3057"},
                "Y": {"Values": [{"Value": 0.0}], "Span": 0.0, "AnimationType": "\u306a\u3057"},
                "Zoom": {"Values": [{"Value": 100.0}], "Span": 0.0, "AnimationType": "\u306a\u3057"},
                "Opacity": {"Values": [{"Value": 100.0}], "Span": 0.0, "AnimationType": "\u306a\u3057"},
                "Layer": 0,
                "Group": 0,
                "IsLocked": False,
                "IsHidden": False,
            }
        new_bg["FilePath"] = bg_path
        new_bg["Frame"] = section_start
        new_bg["Length"] = section_length
        new_bg["Layer"] = 0
        items.append(new_bg)
        result.bg_additions += 1

    return result


def _resolve_carry_forward(ir_data: dict) -> list[dict]:
    """IR utterances の carry-forward を解決して完全なエントリのリストを返す."""
    utterances = ir_data.get("utterances", [])
    sections = {
        s["section_id"]: s
        for s in ir_data.get("macro", {}).get("sections", [])
    }

    optional_fields = [
        "template", "face", "idle_face", "bg", "bg_anim", "slot",
        "motion", "overlay", "se", "transition",
    ]
    resolved = []
    prev: dict[str, str | None] = {}
    prev_section = None

    for utt in utterances:
        entry = dict(utt)
        current_section = entry.get("section_id")

        # セクション変更時はリセット
        if current_section != prev_section and current_section in sections:
            sec = sections[current_section]
            prev = {
                "face": sec.get("default_face"),
                "bg": sec.get("default_bg"),
            }
            prev_section = current_section

        # carry-forward 適用
        for field in optional_fields:
            if field not in entry:
                entry[field] = prev.get(field)
            elif entry[field] is None:
                prev[field] = None
            else:
                prev[field] = entry[field]

        resolved.append(entry)

    return resolved

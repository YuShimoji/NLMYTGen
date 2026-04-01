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
    warnings: list[str] | None = None

    def __post_init__(self) -> None:
        if self.warnings is None:
            self.warnings = []


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
    face_label: str, face_map: dict[str, dict[str, str]]
) -> dict[str, str] | None:
    """IR の face ラベルをパーツファイルパスの辞書に解決する.

    face_map の例:
    {
        "serious": {"Eyebrow": "D:/.../.../03c.png", "Eye": "D:/.../10.png", ...},
        "smile": {"Eyebrow": "D:/.../.../01c.png", ...}
    }
    """
    return face_map.get(face_label)


def _resolve_bg(
    bg_label: str, bg_map: dict[str, str]
) -> str | None:
    """IR の bg ラベルをファイルパスに解決する.

    bg_map の例:
    {"studio_blue": "C:/.../studio_blue.png", "dark_board": "C:/.../dark.png"}
    """
    return bg_map.get(bg_label)


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
    for i, voice_item in enumerate(voice_items):
        if i >= len(resolved):
            break
        ir_entry = resolved[i]
        face_label = ir_entry.get("face")
        if face_label:
            parts = _resolve_face_parts(face_label, face_map)
            if parts:
                fp = voice_item.get("TachieFaceParameter")
                if fp:
                    for part_name, file_path in parts.items():
                        if part_name in fp and fp[part_name] != file_path:
                            fp[part_name] = file_path
                            result.face_changes += 1
                else:
                    result.warnings.append(
                        f"VoiceItem index={i+1} has no TachieFaceParameter"
                    )
            else:
                result.warnings.append(
                    f"face label '{face_label}' not found in face_map"
                )

    # --- bg 差し替え ---
    # ImageItem / VideoItem を Frame 順で並べる
    bg_items = [
        item
        for item in items
        if _item_type(item) in ("ImageItem", "VideoItem")
        and item.get("Layer", -1) == 0  # 背景は通常 Layer 0
    ]
    bg_items.sort(key=lambda x: x.get("Frame", 0))

    # セクションごとの bg を適用
    sections = ir_data.get("macro", {}).get("sections", [])
    for section in sections:
        bg_label = section.get("default_bg")
        if not bg_label:
            continue
        bg_path = _resolve_bg(bg_label, bg_map)
        if not bg_path:
            result.warnings.append(
                f"bg label '{bg_label}' not found in bg_map"
            )
            continue

        start_idx = section.get("start_index", 1) - 1
        # このセクションに対応する VoiceItem の Frame を取得
        if start_idx < len(voice_items):
            section_frame = voice_items[start_idx].get("Frame", 0)
        else:
            continue

        # section_frame に最も近い bg_item を探して差し替え
        best = None
        best_dist = float("inf")
        for bg_item in bg_items:
            dist = abs(bg_item.get("Frame", 0) - section_frame)
            if dist < best_dist:
                best_dist = dist
                best = bg_item
        if best and best.get("FilePath") != bg_path:
            best["FilePath"] = bg_path
            result.bg_changes += 1

    return result


def _resolve_carry_forward(ir_data: dict) -> list[dict]:
    """IR utterances の carry-forward を解決して完全なエントリのリストを返す."""
    utterances = ir_data.get("utterances", [])
    sections = {
        s["section_id"]: s
        for s in ir_data.get("macro", {}).get("sections", [])
    }

    optional_fields = [
        "template", "face", "bg", "bg_anim", "slot",
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

"""ymmp 後処理変換器 (G-06).

演出 IR JSON を読み込み、既存 ymmp の face (表情パーツ) と
bg (背景画像) を差し替える。音声・字幕は台本読込で確保済みのまま維持。

Usage (via CLI):
    python -m src.cli.main patch-ymmp project.ymmp ir.json -o patched.ymmp
"""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass
from pathlib import Path


# G-15: IR transition は当面 none / fade のみ（validate-ir と共有）
TRANSITION_ALLOWED: frozenset[str] = frozenset({"none", "fade"})

# VoiceItem フェード秒数（固定。将来 registry 拡張可）
G15_VOICE_FADE_IN_SEC = 0.2
G15_VOICE_FADE_OUT_SEC = 0.2
G15_JIMAKU_FADE_IN_SEC = 0.2
G15_JIMAKU_FADE_OUT_SEC = 0.2

# PRODUCTION_IR_SPEC §3.4 と一致させる（validate-ir と共有）
BG_ANIM_ALLOWED: frozenset[str] = frozenset({
    "none",
    "pan_left",
    "pan_right",
    "zoom_in",
    "zoom_out",
    "ken_burns",
})

# PRODUCTION_IR_SPEC §3.6 + none（validate-ir と共有）
MOTION_ALLOWED: frozenset[str] = frozenset({
    "none",
    "pop_in",
    "slide_in",
    "shake_small",
    "shake_big",
    "bounce",
    "fade_in",
    "fade_out",
})


@dataclass
class PatchResult:
    """差し替え結果のサマリ."""

    face_changes: int = 0
    slot_changes: int = 0
    overlay_changes: int = 0
    bg_changes: int = 0
    bg_additions: int = 0
    bg_anim_changes: int = 0
    transition_changes: int = 0
    motion_changes: int = 0
    tachie_syncs: int = 0
    se_plans: int = 0
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
                "VOICE_NO_TACHIE_FACE: "
                f"VoiceItem index={vi_index + 1}"
                f" character='{character_name or '?'}'"
                " has no TachieFaceParameter"
            )
    else:
        result.warnings.append(
            "FACE_MAP_MISS: "
            f"face label '{face_label}' not found in face_map"
            f" for character '{character_name or '?'}'"
            f" (VoiceItem index={vi_index + 1})"
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
                "ROW_RANGE_MISSING: "
                f"utterance index={ir_entry.get('index', '?')}"
                f" missing row_start/row_end"
            )
            continue
        if row_start < 1 or row_end < row_start:
            result.warnings.append(
                "ROW_RANGE_INVALID: "
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
                    "IDLE_FACE_MAP_MISS: "
                    f"idle_face '{idle_label}' not found in face_map"
                    f" for character '{char}'"
                )


def _set_animatable_scalar(container: dict, key: str, value: float) -> int:
    """X/Y/Zoom のような scalar または keyframe 風フィールドを書き換える."""
    current = container.get(key)
    if isinstance(current, dict):
        values = current.get("Values")
        if isinstance(values, list) and values:
            first = values[0]
            old = first.get("Value")
            if old != value:
                first["Value"] = value
                return 1
            return 0
        current["Values"] = [{"Value": value}]
        return 1
    if current != value:
        container[key] = value
        return 1
    return 0


def _resolve_character_slots(
    resolved: list[dict],
    char_default_slots: dict[str, str] | None,
    result: PatchResult,
) -> dict[str, str]:
    """IR からキャラごとの effective slot を解決する."""
    effective: dict[str, str] = {}
    char_slot_usage: dict[str, set[str]] = {}

    for entry in resolved:
        speaker = entry.get("speaker", "")
        slot = entry.get("slot")
        if speaker and slot:
            char_slot_usage.setdefault(speaker, set()).add(slot)

    if char_default_slots:
        for char, default_slot in char_default_slots.items():
            if default_slot:
                effective[char] = default_slot

    for char, labels in sorted(char_slot_usage.items()):
        if len(labels) > 1:
            result.warnings.append(
                "SLOT_CHARACTER_DRIFT: "
                f"character '{char}' uses multiple slot labels: "
                f"{', '.join(sorted(labels))}"
            )
            continue
        slot = next(iter(labels))
        default_slot = (char_default_slots or {}).get(char)
        if default_slot and slot != default_slot:
            result.warnings.append(
                "SLOT_DEFAULT_DRIFT: "
                f"character '{char}' uses slot '{slot}'"
                f" but registry default_slot is '{default_slot}'"
            )
        effective[char] = slot

    return effective


def _apply_slot_to_tachie_item(
    tachie_item: dict,
    slot_label: str,
    slot_spec: dict | None,
    result: PatchResult,
) -> None:
    """1 件の TachieItem に slot を反映する."""
    if slot_spec is None:
        if not tachie_item.get("IsHidden", False):
            tachie_item["IsHidden"] = True
            result.slot_changes += 1
        return

    try:
        x = float(slot_spec["x"])
        y = float(slot_spec["y"])
        zoom = float(slot_spec["zoom"])
    except (KeyError, TypeError, ValueError):
        result.warnings.append(
            "SLOT_VALUE_INVALID: "
            f"slot '{slot_label}' must define numeric x/y/zoom"
        )
        return

    if tachie_item.get("IsHidden", False):
        tachie_item["IsHidden"] = False
        result.slot_changes += 1

    param = tachie_item.setdefault("TachieItemParameter", {})
    result.slot_changes += _set_animatable_scalar(param, "X", x)
    result.slot_changes += _set_animatable_scalar(param, "Y", y)
    result.slot_changes += _set_animatable_scalar(param, "Zoom", zoom)

    for key, value in (("X", x), ("Y", y), ("Zoom", zoom)):
        if key in tachie_item:
            result.slot_changes += _set_animatable_scalar(tachie_item, key, value)


def _apply_slots(
    items: list[dict],
    resolved: list[dict],
    slot_map: dict[str, dict | None],
    char_default_slots: dict[str, str] | None,
    result: PatchResult,
) -> None:
    """TachieItem に slot を反映する."""
    if not slot_map:
        return

    effective_slots = _resolve_character_slots(resolved, char_default_slots, result)
    if not effective_slots:
        return

    tachie_items: dict[str, list[dict]] = {}
    for item in items:
        if _item_type(item) != "TachieItem":
            continue
        char = (item.get("CharacterName") or "").strip()
        if char:
            tachie_items.setdefault(char, []).append(item)

    for char, slot_label in sorted(effective_slots.items()):
        if slot_label not in slot_map:
            result.warnings.append(
                "SLOT_REGISTRY_MISS: "
                f"slot '{slot_label}' not found in slot_map"
                f" for character '{char}'"
            )
            continue
        targets = tachie_items.get(char, [])
        if not targets:
            result.warnings.append(
                "SLOT_NO_TACHIE_ITEM: "
                f"character '{char}' has no TachieItem for slot patch"
            )
            continue
        for item in targets:
            _apply_slot_to_tachie_item(item, slot_label, slot_map[slot_label], result)


def _voice_indices_for_ir_entry(
    ir_entry: dict,
    voice_items: list[dict],
    *,
    use_row_range: bool,
) -> list[int]:
    """IR 発話に対応する VoiceItem の 0-based インデックス列を返す."""
    num_vi = len(voice_items)
    if use_row_range:
        row_start = ir_entry.get("row_start")
        row_end = ir_entry.get("row_end")
        if row_start is None or row_end is None:
            return []
        if row_start < 1 or row_end < row_start:
            return []
        return list(range(row_start - 1, min(row_end, num_vi)))
    utt_index = ir_entry.get("index", 0)
    idx = utt_index - 1
    if idx < 0 or idx >= num_vi:
        return []
    return [idx]


def _apply_transition_voice_items(
    voice_items: list[dict],
    resolved: list[dict],
    result: PatchResult,
    *,
    use_row_range: bool,
) -> None:
    """G-15: IR transition を VoiceItem の Voice/Jimaku フェードに反映する（立ち絵 Fade は対象外）."""
    for ir_entry in resolved:
        raw = ir_entry.get("transition")
        tr = (raw or "none") if raw is not None else "none"
        if tr not in TRANSITION_ALLOWED:
            continue

        indices = _voice_indices_for_ir_entry(
            ir_entry, voice_items, use_row_range=use_row_range
        )
        if not indices:
            if tr != "none":
                result.warnings.append(
                    "TRANSITION_NO_VOICE_ANCHOR: "
                    f"utterance index={ir_entry.get('index', '?')}"
                    " has no VoiceItem span for transition"
                )
            continue

        n = len(indices)
        for pos, vi_idx in enumerate(indices):
            vi = voice_items[vi_idx]
            if tr == "none":
                vi["VoiceFadeIn"] = 0.0
                vi["VoiceFadeOut"] = 0.0
                vi["JimakuFadeIn"] = 0.0
                vi["JimakuFadeOut"] = 0.0
                result.transition_changes += 1
                continue

            # fade: 先頭・末尾にのみ in/out（中間は 0）
            if n == 1:
                vi["VoiceFadeIn"] = G15_VOICE_FADE_IN_SEC
                vi["VoiceFadeOut"] = G15_VOICE_FADE_OUT_SEC
                vi["JimakuFadeIn"] = G15_JIMAKU_FADE_IN_SEC
                vi["JimakuFadeOut"] = G15_JIMAKU_FADE_OUT_SEC
            elif pos == 0:
                vi["VoiceFadeIn"] = G15_VOICE_FADE_IN_SEC
                vi["VoiceFadeOut"] = 0.0
                vi["JimakuFadeIn"] = G15_JIMAKU_FADE_IN_SEC
                vi["JimakuFadeOut"] = 0.0
            elif pos == n - 1:
                vi["VoiceFadeIn"] = 0.0
                vi["VoiceFadeOut"] = G15_VOICE_FADE_OUT_SEC
                vi["JimakuFadeIn"] = 0.0
                vi["JimakuFadeOut"] = G15_JIMAKU_FADE_OUT_SEC
            else:
                vi["VoiceFadeIn"] = 0.0
                vi["VoiceFadeOut"] = 0.0
                vi["JimakuFadeIn"] = 0.0
                vi["JimakuFadeOut"] = 0.0
            result.transition_changes += 1


def _normalize_video_effects(value: object) -> list:
    """VideoEffects 未設定と空配列を同一視する."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return []


def _normalize_motion_label(value: object) -> str:
    if not isinstance(value, str):
        return "none"
    label = value.strip()
    if not label:
        return "none"
    return label


def _merge_motion_spans(
    spans: list[tuple[int, int, str]],
) -> list[tuple[int, int, str]]:
    """同一 motion の連続/重複区間を結合する."""
    if not spans:
        return []
    sorted_spans = sorted(spans, key=lambda x: (x[0], x[1]))
    merged: list[tuple[int, int, str]] = [sorted_spans[0]]
    for start, end, motion in sorted_spans[1:]:
        last_start, last_end, last_motion = merged[-1]
        if motion == last_motion and start <= last_end:
            merged[-1] = (last_start, max(last_end, end), last_motion)
            continue
        merged.append((start, end, motion))
    return merged


def _motion_effects_for_label(
    motion: str,
    motion_map: dict[str, list[dict]] | None,
    result: PatchResult,
    *,
    ir_index: object,
) -> list:
    if motion == "none":
        return []
    if not motion_map:
        result.warnings.append(
            "MOTION_MAP_MISS: "
            f"motion '{motion}' requires --motion-map"
            f" (utterance index={ir_index})"
        )
        return []
    mapped = motion_map.get(motion)
    if mapped is None:
        result.warnings.append(
            "MOTION_MAP_MISS: "
            f"motion label '{motion}' not found in motion_map"
            f" (utterance index={ir_index})"
        )
        return []
    return copy.deepcopy(mapped)


def _apply_motion_to_tachie_items(
    items: list[dict],
    voice_items: list[dict],
    resolved: list[dict],
    motion_map: dict[str, list[dict]] | None,
    result: PatchResult,
    *,
    use_row_range: bool,
) -> None:
    """G-16 Phase2: 発話区間ベースで TachieItem を分割して motion を反映する."""
    tachie_by_char: dict[str, list[dict]] = {}
    for item in items:
        if _item_type(item) != "TachieItem":
            continue
        char = (item.get("CharacterName") or "").strip()
        if char:
            tachie_by_char.setdefault(char, []).append(item)

    spans_by_char: dict[str, list[tuple[int, int, str, object]]] = {}
    for ir_entry in resolved:
        motion = _normalize_motion_label(ir_entry.get("motion"))
        speaker = (ir_entry.get("speaker") or "").strip()
        if not speaker:
            continue
        if motion not in MOTION_ALLOWED:
            continue
        timing = _resolve_utterance_timing(
            ir_entry,
            voice_items,
            use_row_range=use_row_range,
        )
        if timing is None:
            if motion != "none":
                result.warnings.append(
                    "MOTION_NO_VOICE_ANCHOR: "
                    f"motion '{motion}' could not resolve timing"
                    f" for utterance index={ir_entry.get('index', '?')}"
                )
            continue
        start_frame, utterance_length = timing
        end_frame = start_frame + max(utterance_length, 1)
        spans_by_char.setdefault(speaker, []).append(
            (start_frame, end_frame, motion, ir_entry.get("index", "?"))
        )

    for speaker, raw_spans in spans_by_char.items():
        targets = tachie_by_char.get(speaker, [])
        non_none_exists = any(span[2] != "none" for span in raw_spans)
        if not targets:
            if non_none_exists:
                result.warnings.append(
                    "MOTION_NO_TACHIE_ITEM: "
                    f"character '{speaker}' has no TachieItem for motion patch"
                )
            continue

        # 複数 TachieItem は v1 と同じ後勝ち（将来拡張）
        if len(targets) != 1:
            for start, end, motion, ir_index in raw_spans:
                _ = start, end
                effects = _motion_effects_for_label(
                    motion, motion_map, result, ir_index=ir_index
                )
                for ti in targets:
                    old = _normalize_video_effects(ti.get("VideoEffects"))
                    if old == effects:
                        continue
                    ti["VideoEffects"] = effects
                    result.motion_changes += 1
            continue

        target = targets[0]
        if target not in items:
            continue

        base_start = int(target.get("Frame", 0))
        base_length = int(target.get("Length", 0))
        if base_length < 1:
            max_end = max(end for _, end, _, _ in raw_spans)
            base_length = max(max_end - base_start, 1)
        base_end = base_start + base_length

        clipped: list[tuple[int, int, str, object]] = []
        for start, end, motion, ir_index in raw_spans:
            clip_start = max(start, base_start)
            clip_end = min(end, base_end)
            if clip_end <= clip_start:
                continue
            clipped.append((clip_start, clip_end, motion, ir_index))
        if not clipped:
            continue

        merged_spans = _merge_motion_spans(
            [(s, e, m) for s, e, m, _ in clipped]
        )

        boundaries = {base_start, base_end}
        for start, end, _motion in merged_spans:
            boundaries.add(start)
            boundaries.add(end)
        ordered = sorted(boundaries)
        if len(ordered) < 2:
            continue

        intervals: list[tuple[int, int, str, object]] = []
        for idx in range(len(ordered) - 1):
            start = ordered[idx]
            end = ordered[idx + 1]
            if end <= start:
                continue
            chosen_motion = "none"
            chosen_idx: object = "?"
            for s, e, motion, ir_index in clipped:
                if s <= start < e:
                    chosen_motion = motion
                    chosen_idx = ir_index
            if intervals and intervals[-1][2] == chosen_motion and intervals[-1][1] == start:
                prev_start, _prev_end, prev_motion, prev_idx = intervals[-1]
                intervals[-1] = (prev_start, end, prev_motion, prev_idx)
                continue
            intervals.append((start, end, chosen_motion, chosen_idx))

        if not intervals:
            continue

        insert_at = items.index(target)
        items.pop(insert_at)
        replacement: list[dict] = []
        for start, end, motion, ir_index in intervals:
            span_len = max(end - start, 1)
            new_item = copy.deepcopy(target)
            new_item["Frame"] = start
            new_item["Length"] = span_len
            new_item["VideoEffects"] = _motion_effects_for_label(
                motion, motion_map, result, ir_index=ir_index
            )
            replacement.append(new_item)
        items[insert_at:insert_at] = replacement
        # 旧単一アイテムが複数区間に分割された場合は変化として扱う
        result.motion_changes += len(replacement)


def _resolve_utterance_timing(
    ir_entry: dict,
    voice_items: list[dict],
    *,
    use_row_range: bool,
) -> tuple[int, int] | None:
    """Resolve utterance start frame and duration from VoiceItems."""
    if use_row_range:
        row_start = ir_entry.get("row_start")
        row_end = ir_entry.get("row_end")
        if row_start is None or row_end is None:
            return None
        if row_start < 1 or row_end < row_start or row_start - 1 >= len(voice_items):
            return None
        start_idx = row_start - 1
        end_idx = min(row_end, len(voice_items)) - 1
    else:
        utt_index = ir_entry.get("index", 0)
        start_idx = utt_index - 1
        end_idx = start_idx
        if start_idx < 0 or start_idx >= len(voice_items):
            return None

    start_frame = voice_items[start_idx].get("Frame", 0)
    end_frame = (
        voice_items[end_idx].get("Frame", 0)
        + voice_items[end_idx].get("Length", 0)
    )
    return start_frame, max(end_frame - start_frame, 1)


def _coerce_int(value, *, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_float(value, *, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _apply_bg_anim_to_image_item(
    item: dict,
    bg_anim: str | None,
    section_length: int,
    result: PatchResult,
) -> None:
    """セクション bg ImageItem の X/Y/Zoom に線形キーフレームを書き込む (G-14).

    IR の各セクション先頭発話の `bg_anim`（carry-forward 解決後）を参照する。
    `ImageItem.X/Y/Zoom` + `Span` は G-12 の bg_anim 契約と整合する。
    """
    if not bg_anim or bg_anim == "none":
        return
    if bg_anim not in BG_ANIM_ALLOWED:
        result.warnings.append(
            f"BG_ANIM_UNKNOWN: unsupported bg_anim '{bg_anim}' in patch (skipped)"
        )
        return

    span = float(max(section_length, 1))
    # YMM4: 線形補間（表示名は環境依存のため、リポジトリ内サンプルと同系のキーを使用）
    anim_type = "\u7dda\u5f62"

    x0, y0, z0 = 0.0, 0.0, 100.0
    x1, y1, z1 = 0.0, 0.0, 100.0
    if bg_anim == "pan_left":
        x0, x1 = 120.0, -120.0
    elif bg_anim == "pan_right":
        x0, x1 = -120.0, 120.0
    elif bg_anim == "zoom_in":
        z0, z1 = 100.0, 115.0
    elif bg_anim == "zoom_out":
        z0, z1 = 115.0, 100.0
    elif bg_anim == "ken_burns":
        x0, x1 = 0.0, 60.0
        y0, y1 = 0.0, 30.0
        z0, z1 = 100.0, 112.0

    item["X"] = {
        "Values": [{"Value": x0}, {"Value": x1}],
        "Span": span,
        "AnimationType": anim_type,
    }
    item["Y"] = {
        "Values": [{"Value": y0}, {"Value": y1}],
        "Span": span,
        "AnimationType": anim_type,
    }
    item["Zoom"] = {
        "Values": [{"Value": z0}, {"Value": z1}],
        "Span": span,
        "AnimationType": anim_type,
    }
    result.bg_anim_changes += 1


def _build_overlay_item(
    spec: dict,
    *,
    frame: int,
    length: int,
) -> dict:
    """Build a minimal overlay ImageItem from registry spec."""
    return {
        "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
        "X": {"Values": [{"Value": _coerce_float(spec.get("x"), default=0.0)}], "Span": 0.0, "AnimationType": "なし"},
        "Y": {"Values": [{"Value": _coerce_float(spec.get("y"), default=0.0)}], "Span": 0.0, "AnimationType": "なし"},
        "Zoom": {"Values": [{"Value": _coerce_float(spec.get("zoom"), default=100.0)}], "Span": 0.0, "AnimationType": "なし"},
        "Opacity": {"Values": [{"Value": _coerce_float(spec.get("opacity"), default=100.0)}], "Span": 0.0, "AnimationType": "なし"},
        "Layer": _coerce_int(spec.get("layer"), default=5),
        "Group": _coerce_int(spec.get("group"), default=0),
        "IsLocked": False,
        "IsHidden": False,
        "FilePath": spec["path"],
        "Frame": frame,
        "Length": max(length, 1),
    }


def _apply_overlay_items(
    items: list[dict],
    voice_items: list[dict],
    resolved: list[dict],
    overlay_map: dict[str, dict],
    result: PatchResult,
    *,
    use_row_range: bool,
) -> None:
    """Insert overlay ImageItems at resolved utterance anchors."""
    for ir_entry in resolved:
        overlay_label = ir_entry.get("overlay")
        if not overlay_label:
            continue

        spec = overlay_map.get(overlay_label)
        if not isinstance(spec, dict):
            result.warnings.append(
                "OVERLAY_MAP_MISS: "
                f"overlay label '{overlay_label}' not found in overlay_map"
            )
            continue
        path = spec.get("path")
        if not isinstance(path, str) or not path:
            result.warnings.append(
                "OVERLAY_SPEC_INVALID: "
                f"overlay label '{overlay_label}' must define path"
            )
            continue

        timing = _resolve_utterance_timing(
            ir_entry,
            voice_items,
            use_row_range=use_row_range,
        )
        if timing is None:
            result.warnings.append(
                "OVERLAY_NO_TIMING_ANCHOR: "
                f"overlay label '{overlay_label}' could not resolve timing"
                f" for utterance index={ir_entry.get('index', '?')}"
            )
            continue

        start_frame, utterance_length = timing
        anchor = spec.get("anchor", "start")
        if anchor not in {"start", "end"}:
            result.warnings.append(
                "OVERLAY_SPEC_INVALID: "
                f"overlay label '{overlay_label}' has invalid anchor '{anchor}'"
            )
            continue

        offset = _coerce_int(spec.get("offset"), default=0)
        item_length = _coerce_int(spec.get("length"), default=utterance_length)
        if item_length < 1:
            result.warnings.append(
                "OVERLAY_SPEC_INVALID: "
                f"overlay label '{overlay_label}' must define positive length"
            )
            continue

        frame = start_frame + offset
        if anchor == "end":
            frame = start_frame + utterance_length + offset

        items.append(_build_overlay_item(spec, frame=frame, length=item_length))
        result.overlay_changes += 1


def _plan_se_items(
    resolved: list[dict],
    voice_items: list[dict],
    se_map: dict[str, dict],
    result: PatchResult,
    *,
    use_row_range: bool,
) -> None:
    """Resolve SE labels to timing anchors and fail fast until route is fixed."""
    for ir_entry in resolved:
        se_label = ir_entry.get("se")
        if not se_label:
            continue

        spec = se_map.get(se_label)
        if not isinstance(spec, dict):
            result.warnings.append(
                "SE_MAP_MISS: "
                f"se label '{se_label}' not found in se_map"
            )
            continue
        path = spec.get("path")
        if not isinstance(path, str) or not path:
            result.warnings.append(
                "SE_SPEC_INVALID: "
                f"se label '{se_label}' must define path"
            )
            continue

        timing = _resolve_utterance_timing(
            ir_entry,
            voice_items,
            use_row_range=use_row_range,
        )
        if timing is None:
            result.warnings.append(
                "SE_NO_TIMING_ANCHOR: "
                f"se label '{se_label}' could not resolve timing"
                f" for utterance index={ir_entry.get('index', '?')}"
            )
            continue

        start_frame, utterance_length = timing
        anchor = spec.get("anchor", "start")
        if anchor not in {"start", "end"}:
            result.warnings.append(
                "SE_SPEC_INVALID: "
                f"se label '{se_label}' has invalid anchor '{anchor}'"
            )
            continue

        offset = _coerce_int(spec.get("offset"), default=0)
        frame = start_frame + offset
        if anchor == "end":
            frame = start_frame + utterance_length + offset

        result.se_plans += 1
        result.warnings.append(
            "SE_WRITE_ROUTE_UNSUPPORTED: "
            f"se label '{se_label}' resolved to '{path}' at frame {frame}"
            " but repo-local corpus has no fixed AudioItem write route"
        )


def patch_ymmp(
    ymmp_data: dict,
    ir_data: dict,
    face_map: dict[str, dict[str, str]],
    bg_map: dict[str, str],
    slot_map: dict[str, dict | None] | None = None,
    char_default_slots: dict[str, str] | None = None,
    overlay_map: dict[str, dict] | None = None,
    se_map: dict[str, dict] | None = None,
    motion_map: dict[str, list[dict]] | None = None,
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
    _apply_slots(
        items,
        resolved,
        slot_map or {},
        char_default_slots,
        result,
    )
    _apply_transition_voice_items(
        voice_items,
        resolved,
        result,
        use_row_range=use_row_range,
    )
    _apply_motion_to_tachie_items(
        items,
        voice_items,
        resolved,
        motion_map,
        result,
        use_row_range=use_row_range,
    )
    _apply_overlay_items(
        items,
        voice_items,
        resolved,
        overlay_map or {},
        result,
        use_row_range=use_row_range,
    )
    _plan_se_items(
        resolved,
        voice_items,
        se_map or {},
        result,
        use_row_range=use_row_range,
    )

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

        bg_anim_label = "none"
        for e in resolved:
            if e.get("index") == utt_start:
                bg_anim_label = e.get("bg_anim") or "none"
                break
        _apply_bg_anim_to_image_item(new_bg, bg_anim_label, section_length, result)

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

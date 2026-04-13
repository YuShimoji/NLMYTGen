"""IR 品質 gate: apply-production の前に品質問題を事前検出する.

face 偏り、unknown labels、prompt/palette drift、active gap、
連続 run、idle_face 未指定、bg 未設定を検出する。
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class IRValidationResult:
    """IR 品質検証の結果."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)
    face_distribution: dict[str, int] = field(default_factory=dict)
    unknown_labels: list[str] = field(default_factory=list)
    prompt_face_labels: list[str] = field(default_factory=list)
    palette_face_labels: list[str] = field(default_factory=list)
    used_face_labels: list[str] = field(default_factory=list)
    used_idle_face_labels: list[str] = field(default_factory=list)
    used_slot_labels: list[str] = field(default_factory=list)
    used_overlay_labels: list[str] = field(default_factory=list)
    used_se_labels: list[str] = field(default_factory=list)
    active_face_gaps: dict[str, list[str]] = field(default_factory=dict)
    latent_face_gaps: dict[str, list[str]] = field(default_factory=dict)
    slot_distribution: dict[str, int] = field(default_factory=dict)
    overlay_distribution: dict[str, int] = field(default_factory=dict)
    se_distribution: dict[str, int] = field(default_factory=dict)
    unknown_slot_labels: list[str] = field(default_factory=list)
    unknown_overlay_labels: list[str] = field(default_factory=list)
    unknown_se_labels: list[str] = field(default_factory=list)
    character_slot_usage: dict[str, list[str]] = field(default_factory=dict)
    prompt_palette_missing_labels: list[str] = field(default_factory=list)
    palette_only_labels: list[str] = field(default_factory=list)
    longest_face_run: int = 0
    longest_face_run_label: str = ""
    idle_face_coverage: float = 0.0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


def extract_prompt_face_labels(prompt_text: str) -> set[str]:
    """prompt markdown から face 許可リストを抽出する."""
    collecting = False
    labels: list[str] = []

    for raw_line in prompt_text.splitlines():
        line = raw_line.strip()

        if not collecting:
            if line.lower().startswith("### face"):
                collecting = True
            continue

        if not line:
            if labels:
                break
            continue
        if line.startswith("**") or line.startswith("###"):
            break

        cleaned = line.lstrip("-*").strip()
        for token in cleaned.split(","):
            label = token.strip().strip("`")
            if label:
                labels.append(label)

    return set(labels)


def load_prompt_face_labels(path: str | Path) -> set[str]:
    """prompt markdown ファイルから face 許可リストを読み込む."""
    with open(path, "r", encoding="utf-8") as f:
        return extract_prompt_face_labels(f.read())


def validate_ir(
    ir_data: dict,
    known_face_labels: set[str] | None = None,
    *,
    char_face_map: dict[str, set[str]] | None = None,
    known_slot_labels: set[str] | None = None,
    known_overlay_labels: set[str] | None = None,
    known_se_labels: set[str] | None = None,
    known_motion_labels: set[str] | None = None,
    char_default_slots: dict[str, str] | None = None,
    prompt_face_labels: set[str] | None = None,
    serious_threshold: float = 0.40,
    max_consecutive_run: int = 4,
    known_body_ids: set[str] | None = None,
) -> IRValidationResult:
    """IR の品質問題を検出する.

    Parameters
    ----------
    ir_data : dict
        load_ir() 後の IR データ
    known_face_labels : set[str] | None
        palette に存在する face ラベル (全キャラ統合)。None なら unknown label チェックをスキップ
    char_face_map : dict[str, set[str]] | None
        キャラ別の face ラベル集合。例: {"魔理沙": {"serious", "smile"}, "霊夢": {"serious"}}
        指定されると、各発話の face/idle_face がそのキャラで解決可能かチェックする
    known_motion_labels : set[str] | None
        motion_map のキー集合。指定時、非 none の motion が台帳に無ければ MOTION_MAP_UNKNOWN_LABEL
    prompt_face_labels : set[str] | None
        Custom GPT prompt が許可している face ラベル集合。
        指定されると、prompt ↔ palette drift と IR の contract drift を検出する
    serious_threshold : float
        serious の許容上限割合 (0.40 = 40%)
    max_consecutive_run : int
        同一 face の連続許容数

    Returns
    -------
    IRValidationResult
    """
    result = IRValidationResult()
    utterances = ir_data.get("utterances", [])
    sections = ir_data.get("macro", {}).get("sections", [])
    result.palette_face_labels = sorted(known_face_labels or set())
    result.prompt_face_labels = sorted(prompt_face_labels or set())

    if not utterances:
        result.errors.append("IR_EMPTY: IR has no utterances")
        return result

    # carry-forward を解決して face 分布を取得
    from src.pipeline.ymmp_patch import (
        BG_ANIM_ALLOWED,
        MOTION_ALLOWED,
        TRANSITION_ALLOWED,
        _resolve_carry_forward,
        iter_overlay_labels,
    )
    resolved = _resolve_carry_forward(ir_data)

    # --- face distribution ---
    face_counts: Counter = Counter()
    face_usage: Counter = Counter()
    idle_usage: Counter = Counter()
    slot_usage: Counter = Counter()
    overlay_usage: Counter = Counter()
    se_usage: Counter = Counter()
    char_slot_usage: dict[str, set[str]] = {}
    for entry in resolved:
        speaker = entry.get("speaker", "")
        face = entry.get("face", "")
        idle_face = entry.get("idle_face", "")
        slot = entry.get("slot", "")
        raw_overlay = entry.get("overlay", "")
        se_label = entry.get("se", "")
        if face:
            face_counts[face] += 1
            face_usage[face] += 1
        if idle_face:
            idle_usage[idle_face] += 1
        if slot:
            slot_usage[slot] += 1
            if speaker:
                char_slot_usage.setdefault(speaker, set()).add(slot)
        if raw_overlay is not None and raw_overlay != "":
            if isinstance(raw_overlay, list):
                if not all(isinstance(x, str) for x in raw_overlay):
                    result.errors.append(
                        "OVERLAY_INVALID_TYPE: "
                        "overlay list must contain only strings"
                    )
                else:
                    for ol in iter_overlay_labels(raw_overlay):
                        overlay_usage[ol] += 1
            elif isinstance(raw_overlay, str):
                for ol in iter_overlay_labels(raw_overlay):
                    overlay_usage[ol] += 1
            else:
                result.errors.append(
                    "OVERLAY_INVALID_TYPE: "
                    "overlay must be string, list of strings, null, or empty"
                )
        if se_label:
            se_usage[se_label] += 1

    for entry in resolved:
        ba = entry.get("bg_anim")
        if ba is None or ba == "":
            continue
        if ba not in BG_ANIM_ALLOWED:
            result.errors.append(
                "BG_ANIM_UNKNOWN_LABEL: "
                f"utterance index={entry.get('index', '?')}"
                f" has unsupported bg_anim '{ba}'"
                f" (allowed: {', '.join(sorted(BG_ANIM_ALLOWED))})"
            )

    for entry in resolved:
        tx = entry.get("transition")
        if tx is None or tx == "":
            continue
        if tx not in TRANSITION_ALLOWED:
            result.errors.append(
                "TRANSITION_UNKNOWN_LABEL: "
                f"utterance index={entry.get('index', '?')}"
                f" has unsupported transition '{tx}'"
                f" (allowed: {', '.join(sorted(TRANSITION_ALLOWED))})"
            )

    for entry in resolved:
        mo = entry.get("motion")
        if mo is None or mo == "":
            continue
        if mo not in MOTION_ALLOWED:
            result.errors.append(
                "MOTION_UNKNOWN_LABEL: "
                f"utterance index={entry.get('index', '?')}"
                f" has unsupported motion '{mo}'"
                f" (allowed: {', '.join(sorted(MOTION_ALLOWED))})"
            )

    if known_motion_labels is not None:
        for entry in resolved:
            mo = entry.get("motion")
            if mo is None or mo == "" or mo == "none":
                continue
            if mo not in known_motion_labels:
                result.errors.append(
                    "MOTION_MAP_UNKNOWN_LABEL: "
                    f"utterance index={entry.get('index', '?')}"
                    f" uses motion '{mo}' not in motion_map registry"
                )

    # --- G-19: body_id validation ---
    if known_body_ids is not None:
        for entry in resolved:
            body_id = entry.get("body_id")
            if body_id is None or body_id == "":
                continue
            if body_id not in known_body_ids:
                result.errors.append(
                    "BODY_ID_UNKNOWN: "
                    f"utterance index={entry.get('index', '?')}"
                    f" uses body_id '{body_id}' not in face_map_bundle"
                    f" (known: {', '.join(sorted(known_body_ids))})"
                )

    total = sum(face_counts.values())
    result.face_distribution = dict(face_counts)
    result.used_face_labels = sorted(face_usage)
    result.used_idle_face_labels = sorted(idle_usage)
    result.slot_distribution = dict(slot_usage)
    result.used_slot_labels = sorted(slot_usage)
    result.overlay_distribution = dict(overlay_usage)
    result.se_distribution = dict(se_usage)
    result.used_overlay_labels = sorted(overlay_usage)
    result.used_se_labels = sorted(se_usage)
    result.character_slot_usage = {
        char: sorted(labels)
        for char, labels in sorted(char_slot_usage.items())
    }
    all_used_labels = set(face_usage) | set(idle_usage)

    # serious 偏り
    if total > 0:
        serious_pct = face_counts.get("serious", 0) / total
        if serious_pct > serious_threshold:
            result.warnings.append(
                "FACE_SERIOUS_SKEW: "
                f"face 'serious' is {serious_pct:.0%} of utterances"
                f" (threshold: {serious_threshold:.0%})"
            )

    # unknown labels
    if known_face_labels is not None:
        unknown = sorted(all_used_labels - known_face_labels)
        if unknown:
            result.unknown_labels = unknown
            for label in unknown:
                count = face_usage[label] + idle_usage[label]
                result.errors.append(
                    "FACE_UNKNOWN_LABEL: "
                    f"unknown face label '{label}' used {count} times"
                    f" (not in palette)"
                )

    # prompt contract drift
    if prompt_face_labels is not None:
        used_not_allowed = sorted(all_used_labels - prompt_face_labels)
        for label in used_not_allowed:
            count = face_usage[label] + idle_usage[label]
            result.errors.append(
                "PROMPT_FACE_DRIFT: "
                f"face label '{label}' used {count} times"
                f" but not allowed by prompt contract"
            )

        if known_face_labels is not None:
            result.prompt_palette_missing_labels = sorted(
                prompt_face_labels - known_face_labels
            )
            result.palette_only_labels = sorted(
                known_face_labels - prompt_face_labels
            )
            for label in result.prompt_palette_missing_labels:
                result.warnings.append(
                    "FACE_PROMPT_PALETTE_GAP: "
                    f"prompt allows face '{label}' but palette has no matching label"
                )
            for label in result.palette_only_labels:
                result.warnings.append(
                    "FACE_PROMPT_PALETTE_EXTRA: "
                    f"palette label '{label}' is not listed in prompt contract"
                )

    # per-character face coverage
    if char_face_map is not None:
        missing_pairs: dict[tuple[str, str], int] = {}
        for entry in resolved:
            speaker = entry.get("speaker", "")
            face = entry.get("face", "")
            idle_face = entry.get("idle_face", "")
            # face: speaker のラベルをチェック
            if face and speaker in char_face_map:
                if face not in char_face_map[speaker]:
                    key = (speaker, face)
                    missing_pairs[key] = missing_pairs.get(key, 0) + 1
            # idle_face: speaker 以外の全キャラをチェック
            if idle_face:
                for char, labels in char_face_map.items():
                    if char == speaker:
                        continue
                    if idle_face not in labels:
                        key = (char, idle_face)
                        missing_pairs[key] = missing_pairs.get(key, 0) + 1
        active_face_gaps: dict[str, list[str]] = {}
        for (char, label), count in sorted(missing_pairs.items()):
            active_face_gaps.setdefault(char, []).append(label)
            result.errors.append(
                "FACE_ACTIVE_GAP: "
                f"character '{char}' is missing face '{label}'"
                f" required by current IR ({count} uses)"
            )
        result.active_face_gaps = {
            char: sorted(set(labels))
            for char, labels in active_face_gaps.items()
        }

        if prompt_face_labels is not None:
            latent_face_gaps: dict[str, list[str]] = {}
            for char, labels in sorted(char_face_map.items()):
                missing = sorted(prompt_face_labels - labels)
                if not missing:
                    continue
                active_missing = set(result.active_face_gaps.get(char, []))
                latent = [label for label in missing if label not in active_missing]
                if latent:
                    latent_face_gaps[char] = latent
            result.latent_face_gaps = latent_face_gaps
            for char, labels in latent_face_gaps.items():
                result.warnings.append(
                    "FACE_LATENT_GAP: "
                    f"character '{char}' is missing prompt labels: {', '.join(labels)}"
                )

    # 連続 run
    if known_slot_labels is not None:
        unknown_slots = sorted(set(slot_usage) - known_slot_labels)
        if unknown_slots:
            result.unknown_slot_labels = unknown_slots
            for label in unknown_slots:
                result.errors.append(
                    "SLOT_UNKNOWN_LABEL: "
                    f"unknown slot label '{label}' used {slot_usage[label]} times"
                    " (not in slot registry)"
                )

    if known_overlay_labels is not None:
        unknown_overlays = sorted(set(overlay_usage) - known_overlay_labels)
        if unknown_overlays:
            result.unknown_overlay_labels = unknown_overlays
            for label in unknown_overlays:
                result.errors.append(
                    "OVERLAY_UNKNOWN_LABEL: "
                    f"unknown overlay label '{label}' used {overlay_usage[label]} times"
                    " (not in overlay registry)"
                )

    if known_se_labels is not None:
        unknown_se = sorted(set(se_usage) - known_se_labels)
        if unknown_se:
            result.unknown_se_labels = unknown_se
            for label in unknown_se:
                result.errors.append(
                    "SE_UNKNOWN_LABEL: "
                    f"unknown se label '{label}' used {se_usage[label]} times"
                    " (not in se registry)"
                )

    if char_default_slots:
        for char, default_slot in sorted(char_default_slots.items()):
            if known_slot_labels is not None and default_slot not in known_slot_labels:
                result.errors.append(
                    "SLOT_REGISTRY_GAP: "
                    f"character '{char}' default_slot '{default_slot}'"
                    " is not defined in slot registry"
                )

    for char, labels in sorted(char_slot_usage.items()):
        if len(labels) > 1:
            result.errors.append(
                "SLOT_CHARACTER_DRIFT: "
                f"character '{char}' uses multiple slot labels: "
                f"{', '.join(sorted(labels))}"
            )
            continue
        if char_default_slots and char in char_default_slots:
            used_slot = next(iter(labels))
            default_slot = char_default_slots[char]
            if used_slot != default_slot:
                result.errors.append(
                    "SLOT_DEFAULT_DRIFT: "
                    f"character '{char}' uses slot '{used_slot}'"
                    f" but registry default_slot is '{default_slot}'"
                )

    run_label = ""
    run_len = 0
    max_run = 0
    max_run_label = ""
    max_run_start = 0
    for i, entry in enumerate(resolved):
        face = entry.get("face", "")
        if face == run_label:
            run_len += 1
        else:
            if run_len > max_run:
                max_run = run_len
                max_run_label = run_label
                max_run_start = i - run_len + 1
            run_label = face
            run_len = 1
    if run_len > max_run:
        max_run = run_len
        max_run_label = run_label
        max_run_start = len(resolved) - run_len + 1
    result.longest_face_run = max_run
    result.longest_face_run_label = max_run_label

    if max_run > max_consecutive_run:
        result.warnings.append(
            "FACE_RUN_LENGTH: "
            f"face '{max_run_label}' runs {max_run} consecutive"
            f" utterances (from utt {max_run_start},"
            f" max allowed: {max_consecutive_run})"
        )

    # idle_face 未指定
    idle_count = sum(1 for e in resolved if e.get("idle_face"))
    if total > 0:
        result.idle_face_coverage = idle_count / total
    if idle_count == 0:
        result.warnings.append(
            "IDLE_FACE_MISSING: idle_face is not specified in any utterance"
        )

    # bg 未設定
    bg_labels = [s.get("default_bg", "") for s in sections]
    bg_set = {b for b in bg_labels if b}
    if not bg_set:
        result.warnings.append(
            "BG_MISSING: no bg labels defined in macro.sections"
        )

    # row_start / row_end の整合
    has_row = any(
        u.get("row_start") is not None or u.get("row_end") is not None
        for u in utterances
    )
    if not has_row:
        result.info.append(
            "ROW_RANGE_INFO: row_start/row_end not set."
            " Use annotate-row-range or apply-production --csv"
        )
    else:
        prev_end = 0
        for utt in utterances:
            utt_idx = utt.get("index", "?")
            row_start = utt.get("row_start")
            row_end = utt.get("row_end")

            if row_start is None or row_end is None:
                result.errors.append(
                    "ROW_RANGE_MISSING: "
                    f"utterance index={utt_idx} missing row_start/row_end"
                )
                continue
            if row_start < 1 or row_end < row_start:
                result.errors.append(
                    "ROW_RANGE_INVALID: "
                    f"utterance index={utt_idx} invalid row_start={row_start}"
                    f" row_end={row_end}"
                )
                continue
            if row_start <= prev_end:
                result.errors.append(
                    "ROW_RANGE_OVERLAP: "
                    f"utterance index={utt_idx} overlaps previous row range"
                    f" (row_start={row_start}, previous_end={prev_end})"
                )
            prev_end = max(prev_end, row_end)

    return result

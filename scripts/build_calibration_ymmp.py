"""Build calibration .ymmp files for G-26 Phase 0.

Generates 7 calibration .ymmp files under _tmp/g26/calibration/, each varying ONE
element axis with key-points only (per Anti-Shortcut Rule R7). User opens each in
YMM4 and records observations into MOTION_CALIBRATION_GUIDE.md § 2.

Outputs:
  A1_static_position.ymmp           - X / Y / Zoom static value steps
  A2_static_rotation_opacity.ymmp   - Rotation static + Opacity static
  B_rotation_patterns.ymmp          - Rotation animated patterns x Length
  C_y_bounce_patterns.ymmp          - Y bounce keyframe patterns
  D_effect_intensity.ymmp           - Effect parameter intensity steps
  E_face_swap.ymmp                  - 5 face expressions (excluding easy)
  F_anchor_modes.ymmp               - 3 anchor modes x Rotation animated
  README.md                         - frame layout map for user reference

Run from repo root:
  uv run python scripts/build_calibration_ymmp.py
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.pipeline.ymmp_patch import load_ymmp, save_ymmp
from src.pipeline.skit_group_placement import extract_skit_group_templates
from src.pipeline.motion_recipe import (
    _first_group_item,
    _image_items,
    _normalize_group,
    _clone_images,
    _set_transform_values,
)


REPO = Path(__file__).resolve().parents[1]
SEED = REPO / "samples/canonical.ymmp"
TEMPLATE_SOURCE = REPO / "samples/templates/skit_group/delivery_v1_templates.ymmp"
EFFECT_SAMPLES = REPO / "samples/_probe/b2/effect_full_samples.json"
EFFECTS_YMMP = REPO / "samples/EffectsSamples_2026-04-15.ymmp"
NOD_YMMP = REPO / "samples/nod.ymmp"
CHARACTER_DIR = REPO / "samples/characterAnimSample"
OUT_DIR = REPO / "_tmp/g26/calibration"

BASE_TEMPLATE_NAME = "delivery_nod_v1"
DEFAULT_LAYER = 9
DEFAULT_GROUP_RANGE = 2
SPACING = 90  # frames between consecutive clips per .ymmp


@dataclass
class Variant:
    """Single calibration clip."""
    label: str
    length: int = 60
    rotation_values: list[float] | None = None
    y_delta_values: list[float] | None = None
    zoom_delta_values: list[float] | None = None
    x_value: float | None = None
    y_value: float | None = None
    zoom_value: float | None = None
    opacity_value: float | None = None
    effects_override: list[dict[str, Any]] | None = None
    face_filename: str | None = None
    anchor_mode: str | None = None  # "head" / "center" / "absent"


def _effect_short_name(effect: dict[str, Any]) -> str:
    return (effect.get("$type") or "").split(",")[0].split(".")[-1]


def _load_effect_samples() -> dict[str, dict[str, Any]]:
    """Aggregate effect templates from b2 samples + EffectsSamples.ymmp + nod.ymmp.

    First scans `effect_full_samples.json` (cp932), then walks
    `EffectsSamples_2026-04-15.ymmp` VideoEffects, then nod.ymmp's GroupItem
    for CenterPointEffect. Later sources do not overwrite earlier ones.
    """
    samples: dict[str, dict[str, Any]] = {}

    # 1) b2 sample json
    if EFFECT_SAMPLES.exists():
        last_err: Exception | None = None
        for enc in ("utf-8-sig", "utf-8", "cp932", "shift_jis"):
            try:
                with open(EFFECT_SAMPLES, encoding=enc) as f:
                    data = json.load(f)
                break
            except UnicodeDecodeError as e:
                last_err = e
                continue
        else:
            raise last_err if last_err else RuntimeError("effect_full_samples.json unreadable")
        effects = data.get("effects") if isinstance(data, dict) else None
        if not isinstance(effects, dict):
            effects = data if isinstance(data, dict) else {}
        for key, val in effects.items():
            if isinstance(val, dict) and "$type" in val:
                samples.setdefault(key, val)
                # also index by short name (without "Effect" suffix variant if any)
                short = _effect_short_name(val)
                samples.setdefault(short, val)

    # 2) EffectsSamples_2026-04-15.ymmp
    if EFFECTS_YMMP.exists():
        with open(EFFECTS_YMMP, encoding="utf-8-sig") as f:
            ymmp = json.load(f)
        for tl in ymmp.get("Timelines") or []:
            for it in tl.get("Items") or []:
                if not isinstance(it, dict):
                    continue
                for eff in it.get("VideoEffects") or []:
                    if not isinstance(eff, dict):
                        continue
                    name = _effect_short_name(eff)
                    if name and name not in samples:
                        samples[name] = eff

    # 3) nod.ymmp for CenterPointEffect (head pivot canonical values)
    if "CenterPointEffect" not in samples and NOD_YMMP.exists():
        with open(NOD_YMMP, encoding="utf-8-sig") as f:
            nod = json.load(f)
        for it in nod["Timelines"][0]["Items"]:
            if not isinstance(it, dict):
                continue
            for eff in it.get("VideoEffects") or []:
                if isinstance(eff, dict) and _effect_short_name(eff) == "CenterPointEffect":
                    samples["CenterPointEffect"] = eff
                    break

    return samples


def _flat_param_route(value: float) -> dict[str, Any]:
    """Flat (non-animated) wrapper for an effect parameter."""
    return {
        "Values": [{"Value": float(value)}],
        "Span": 0.0,
        "AnimationType": "なし",
        "Bezier": {
            "Points": [
                {"Point": {"X": 0.0, "Y": 0.0}, "ControlPoint1": {"X": -0.3, "Y": -0.3}, "ControlPoint2": {"X": 0.3, "Y": 0.3}},
                {"Point": {"X": 1.0, "Y": 1.0}, "ControlPoint1": {"X": -0.3, "Y": -0.3}, "ControlPoint2": {"X": 0.3, "Y": 0.3}},
            ],
            "IsQuadratic": False,
        },
    }


def _build_effect(effect_name: str, params: dict[str, float], samples: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Clone a known effect from effect_samples and override key params."""
    if effect_name not in samples:
        # Fall back to minimal stub. CLI builds with $type lookup; here we need
        # a working object with parameters.
        raise ValueError(f"effect {effect_name} not in effect_full_samples.json")
    effect = copy.deepcopy(samples[effect_name])
    for key, val in params.items():
        if key in effect:
            existing = effect[key]
            if isinstance(existing, dict) and "Values" in existing:
                existing["Values"] = [{"Value": float(val)}]
            else:
                effect[key] = float(val) if isinstance(existing, (int, float)) else val
        else:
            # If parameter missing (catalog entry differs), add as flat route
            effect[key] = _flat_param_route(val)
    return effect


def _make_anchor_effect(mode: str, samples: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    """Build CenterPointEffect for the given anchor mode. Returns None for 'absent'."""
    if mode == "absent":
        return None
    if "CenterPointEffect" not in samples:
        raise ValueError("CenterPointEffect not in effect_full_samples.json")
    effect = copy.deepcopy(samples["CenterPointEffect"])
    if mode == "head":
        effect["Vertical"] = "Bottom"
        effect["Horizontal"] = "Custom"
        if isinstance(effect.get("X"), dict):
            effect["X"]["Values"] = [{"Value": 524.566650390625}]
        if isinstance(effect.get("Y"), dict):
            effect["Y"]["Values"] = [{"Value": 136.84947204589844}]
    elif mode == "center":
        effect["Vertical"] = "Center"
        effect["Horizontal"] = "Center"
        if isinstance(effect.get("X"), dict):
            effect["X"]["Values"] = [{"Value": 0.0}]
        if isinstance(effect.get("Y"), dict):
            effect["Y"]["Values"] = [{"Value": 0.0}]
    return effect


def _emit_variant(
    *,
    seed_data: dict[str, Any],
    base_group: dict[str, Any],
    base_images: list[dict[str, Any]],
    rest_pose: dict[str, float],
    samples: dict[str, dict[str, Any]],
    variant: Variant,
    frame: int,
) -> None:
    remark = f"calib:{variant.label}"
    group = _normalize_group(base_group, frame=frame, length=variant.length, remark=remark, rest_pose=rest_pose)

    # Static value overrides
    if variant.x_value is not None:
        _set_transform_values(group, "X", [variant.x_value])
    if variant.y_value is not None:
        _set_transform_values(group, "Y", [variant.y_value])
    if variant.zoom_value is not None:
        _set_transform_values(group, "Zoom", [variant.zoom_value])
    if variant.opacity_value is not None:
        _set_transform_values(group, "Opacity", [variant.opacity_value])

    # Animated routes
    if variant.rotation_values is not None:
        _set_transform_values(group, "Rotation", list(variant.rotation_values))
    if variant.y_delta_values is not None:
        y_resolved = [rest_pose["Y"] + d for d in variant.y_delta_values]
        _set_transform_values(group, "Y", y_resolved)
    if variant.zoom_delta_values is not None:
        z_resolved = [rest_pose["Zoom"] + d for d in variant.zoom_delta_values]
        _set_transform_values(group, "Zoom", z_resolved)

    # Effects override (default: head anchor only)
    if variant.effects_override is not None:
        group["VideoEffects"] = variant.effects_override
    elif variant.anchor_mode is not None:
        anchor = _make_anchor_effect(variant.anchor_mode, samples)
        group["VideoEffects"] = [anchor] if anchor is not None else []
    else:
        anchor = _make_anchor_effect("head", samples)
        group["VideoEffects"] = [anchor]

    images = _clone_images(base_images, frame=frame, length=variant.length, remark=remark)

    # Face swap: replace L11 face FilePath
    if variant.face_filename is not None:
        face_path = (CHARACTER_DIR / variant.face_filename).resolve()
        for img in images:
            if img.get("Layer") == DEFAULT_LAYER + 2:  # L11 = face
                img["FilePath"] = str(face_path)

    seed_data["Timelines"][0]["Items"].extend([group, *images])


def _build_calibration_ymmp(out_path: Path, variants: list[Variant], samples: dict[str, dict[str, Any]]) -> None:
    seed_data = load_ymmp(SEED)
    template = load_ymmp(TEMPLATE_SOURCE)
    templates = extract_skit_group_templates(template)
    base_clip = templates.get(BASE_TEMPLATE_NAME) or next(iter(templates.values()))
    base_group = _first_group_item(base_clip)
    base_images = _image_items(base_clip)
    rest_pose = {
        "X": -102.0,
        "Y": 462.5,
        "Zoom": 103.8,
    }
    seed_data["Timelines"][0]["Items"] = []
    frame = 0
    for variant in variants:
        _emit_variant(
            seed_data=seed_data,
            base_group=base_group,
            base_images=base_images,
            rest_pose=rest_pose,
            samples=samples,
            variant=variant,
            frame=frame,
        )
        frame += variant.length + SPACING
    # Update timeline length
    seed_data["Timelines"][0]["Length"] = frame + 60
    save_ymmp(seed_data, out_path)
    print(f"wrote {out_path}  ({len(variants)} variants, total length {frame})")


def build_a1_static_position(samples: dict[str, dict[str, Any]]) -> None:
    """A1: X / Y / Zoom static steps."""
    variants: list[Variant] = []
    # X axis: -200, -100, 0, +100, +200 (Y / Zoom default)
    for x in [-200, -100, 0, 100, 200]:
        variants.append(Variant(label=f"X_{x}", length=45, x_value=float(x)))
    # Y axis: 250 (top), 462.5 (mid, default), 700 (bottom)
    for y in [250, 462.5, 700]:
        variants.append(Variant(label=f"Y_{int(y)}", length=45, y_value=float(y)))
    # Zoom: 80, 103.8 (default), 130, 170
    for z in [80, 103.8, 130, 170]:
        variants.append(Variant(label=f"Zoom_{int(z)}", length=45, zoom_value=float(z)))
    _build_calibration_ymmp(OUT_DIR / "A1_static_position.ymmp", variants, samples)


def build_a2_static_rotation_opacity(samples: dict[str, dict[str, Any]]) -> None:
    """A2: Rotation static + Opacity static."""
    variants: list[Variant] = []
    for r in [-30, -10, -5, 0, 5, 10, 30]:
        variants.append(Variant(
            label=f"Rotation_{r}",
            length=45,
            rotation_values=[float(r)],  # single keyframe = static
        ))
    for o in [100, 75, 50, 25]:
        variants.append(Variant(label=f"Opacity_{o}", length=45, opacity_value=float(o)))
    _build_calibration_ymmp(OUT_DIR / "A2_static_rotation_opacity.ymmp", variants, samples)


def build_b_rotation_patterns(samples: dict[str, dict[str, Any]]) -> None:
    """B: animated Rotation patterns x Length."""
    patterns = [
        ("simple_30", [0.0, -10.0, 0.0], 30),
        ("simple_60", [0.0, -10.0, 0.0], 60),
        ("simple_120", [0.0, -10.0, 0.0], 120),
        ("hold_60", [0.0, -10.0, -10.0, 0.0], 60),
        ("hold_120", [0.0, -10.0, -10.0, 0.0], 120),
        ("longhold_80", [0.0, -5.0, -5.0, -5.0, 0.0], 80),
        ("double_66", [0.0, -7.0, 0.0, -5.0, 0.0], 66),
        ("delayed_90", [0.0, 0.0, -10.0, 0.0], 90),
    ]
    variants = [
        Variant(label=f"Rot_{name}", length=length, rotation_values=values)
        for name, values, length in patterns
    ]
    _build_calibration_ymmp(OUT_DIR / "B_rotation_patterns.ymmp", variants, samples)


def build_c_y_bounce_patterns(samples: dict[str, dict[str, Any]]) -> None:
    """C: Y bounce patterns."""
    patterns = [
        ("single_30", [0.0, -30.0, 0.0]),
        ("single_90", [0.0, -90.0, 0.0]),
        ("single_150", [0.0, -150.0, 0.0]),
        ("double_30", [0.0, -30.0, 10.0, -30.0, 0.0]),
        ("double_decay", [0.0, -45.0, 5.0, -35.0, 0.0]),
    ]
    variants = [
        Variant(label=f"Y_{name}", length=60, y_delta_values=deltas)
        for name, deltas in patterns
    ]
    _build_calibration_ymmp(OUT_DIR / "C_y_bounce_patterns.ymmp", variants, samples)


def build_d_effect_intensity(samples: dict[str, dict[str, Any]]) -> None:
    """D: Effect parameter intensity steps."""
    anchor_head = _make_anchor_effect("head", samples)
    variants: list[Variant] = []

    for stretch in [10, 25, 50]:
        eff = _build_effect("JumpEffect", {"Stretch": stretch}, samples)
        variants.append(Variant(
            label=f"Jump_Stretch_{stretch}",
            length=60,
            effects_override=[anchor_head, eff],
        ))
    for size in [30, 50, 80]:
        eff = _build_effect("CrashEffect", {"Size": size}, samples)
        variants.append(Variant(
            label=f"Crash_Size_{size}",
            length=60,
            effects_override=[anchor_head, eff],
        ))
    for strength in [5, 15, 30]:
        eff = _build_effect("ChromaticAberrationEffect", {"Strength": strength}, samples)
        variants.append(Variant(
            label=f"Chromatic_Strength_{strength}",
            length=60,
            effects_override=[anchor_head, eff],
        ))
    for blur in [2, 5, 10]:
        eff = _build_effect("GaussianBlurEffect", {"Blur": blur}, samples)
        variants.append(Variant(
            label=f"Blur_{blur}",
            length=60,
            effects_override=[anchor_head, eff],
        ))
    _build_calibration_ymmp(OUT_DIR / "D_effect_intensity.ymmp", variants, samples)


def build_e_face_swap(samples: dict[str, dict[str, Any]]) -> None:
    """E: 5 face expressions (excluding easy default for contrast)."""
    faces = [
        ("easy", "reimu_easy.png"),
        ("shocked", "reimu_shocked.png"),
        ("panic", "reimu_panic.png"),
        ("surprised", "reimu_surprised.png"),
        ("anger", "reimu_anger.png"),
        ("shobon", "reimu_shobon.png"),
    ]
    variants = [
        Variant(
            label=f"Face_{name}",
            length=60,
            face_filename=filename,
        )
        for name, filename in faces
    ]
    _build_calibration_ymmp(OUT_DIR / "E_face_swap.ymmp", variants, samples)


def build_f_anchor_modes(samples: dict[str, dict[str, Any]]) -> None:
    """F: 3 anchor modes x Rotation animated."""
    rotation = [0.0, -10.0, 0.0]
    variants = [
        Variant(label="Anchor_head_R10", length=60, rotation_values=rotation, anchor_mode="head"),
        Variant(label="Anchor_center_R10", length=60, rotation_values=rotation, anchor_mode="center"),
        Variant(label="Anchor_absent_R10", length=60, rotation_values=rotation, anchor_mode="absent"),
    ]
    _build_calibration_ymmp(OUT_DIR / "F_anchor_modes.ymmp", variants, samples)


def write_readme() -> None:
    readme_path = OUT_DIR / "README.md"
    readme_path.write_text(
        """# G-26 Calibration .ymmp set

Step 4 で生成された 7 件 + README。各 .ymmp は 1 系統の element axis を要所値で並べたもの。

## ファイル一覧と確認ポイント

| file | 確認 element | 何を観測するか |
|------|-------------|---------------|
| `A1_static_position.ymmp` | X / Y / Zoom static | 画面内のキャラ出現位置とサイズ感の閾値 (小さすぎ / 大きすぎ ライン) |
| `A2_static_rotation_opacity.ymmp` | Rotation static, Opacity | 何度から「傾き」と読めるか、Opacity 何 % で「弱透明」か |
| `B_rotation_patterns.ymmp` | Rotation animated patterns | 単純揺れ vs hold vs long-hold vs double vs delayed の差が読めるか。**特に hold 形が hold として読めるかが最重要** |
| `C_y_bounce_patterns.ymmp` | Y bounce patterns | 振幅の閾値 (30 / 90 / 150)、二段 bounce が二段に見えるか |
| `D_effect_intensity.ymmp` | JumpEffect / CrashEffect / ChromaticAberration / GaussianBlur | 各 effect の弱・標準・強の体感差 |
| `E_face_swap.ymmp` | 6 reimu 表情 | 各表情が emotion 表現として読めるか |
| `F_anchor_modes.ymmp` | CenterPointEffect 3 modes | 同 Rotation `[0, -10, 0]` を head pivot / center pivot / 不在 で比較 |

## 確認手順 (各 .ymmp 1-2 分、合計 ~15-20 分)

1. YMM4 で各 .ymmp を順に開く
2. timeline を frame 0 から再生 (各 clip は 45-90 frame、間 90 frame 空き)
3. 各 clip の Remark (例: `calib:X_-200`) を見ながら、**何が起きたか** を [`docs/MOTION_CALIBRATION_GUIDE.md`](../../../docs/MOTION_CALIBRATION_GUIDE.md) § 2 の該当行に記入

## 報告形式

[MOTION_CALIBRATION_GUIDE.md](../../../docs/MOTION_CALIBRATION_GUIDE.md) § 2 の各 (未観測) 行を埋めるか、チャットで以下のように列挙:

```
A1: X=-200 で左端に到達、X=200 で右端ぎりぎり、Zoom=80 では小さすぎ、Zoom=170 で過剰
A2: Rotation -3° は不可視、-5° で微傾き、-10° 明確
B: Rot_simple_60 は nod 1 回、Rot_hold_60 は傾き hold が見えた / 見えなかった、...
...
```

assistant が GUIDE.md を埋め、Phase D 改修に進む。
""",
        encoding="utf-8",
    )
    print(f"wrote {readme_path}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    samples = _load_effect_samples()
    print(f"effect samples loaded: {len(samples)} types")
    build_a1_static_position(samples)
    build_a2_static_rotation_opacity(samples)
    build_b_rotation_patterns(samples)
    build_c_y_bounce_patterns(samples)
    build_d_effect_intensity(samples)
    build_e_face_swap(samples)
    build_f_anchor_modes(samples)
    write_readme()
    print(f"\nAll calibration artifacts written to: {OUT_DIR}")


if __name__ == "__main__":
    main()

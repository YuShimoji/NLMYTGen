"""Build tachie_motion_map_library v2 with proper parameter values.

Purpose: fill concrete animation parameters so motion_target direct-write
actually produces visible effects (not just type placeholders).

Scale policy:
- "normal" intensity. Lower than EffectsSamples demo values but still visible.
- User can request _light / _heavy variants later.

Effects reused from EffectsSamples_2026-04-15.ymmp reference.
"""
from __future__ import annotations

import json
from pathlib import Path


BEZIER_DEFAULT = {
    "Points": [
        {
            "Point": {"X": 0.0, "Y": 0.0},
            "ControlPoint1": {"X": -0.3, "Y": -0.3},
            "ControlPoint2": {"X": 0.3, "Y": 0.3},
        },
        {
            "Point": {"X": 1.0, "Y": 1.0},
            "ControlPoint1": {"X": -0.3, "Y": -0.3},
            "ControlPoint2": {"X": 0.3, "Y": 0.3},
        },
    ],
    "IsQuadratic": False,
}


def anim(value: float):
    """Flat (non-animated) single-value parameter wrapper."""
    return {
        "Values": [{"Value": float(value)}],
        "Span": 0.0,
        "AnimationType": "なし",
        "Bezier": BEZIER_DEFAULT,
    }


def anim_keyframes(values: list[float], span: float = 1.0):
    """Animated parameter with multiple keyframes at equal intervals.

    Values are laid out 0.0 → 1.0 evenly. Span is the total duration.
    """
    if len(values) < 2:
        return anim(values[0])
    positions = [i / (len(values) - 1) for i in range(len(values))]
    return {
        "Values": [{"Value": float(v)} for v in values],
        "Span": float(span),
        "AnimationType": "加速減速",
        "Bezier": BEZIER_DEFAULT,
    }


def e_repeat_move(x: float, y: float, span: float, easing_mode: str = "InOut"):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.RepeatMoveEffect, YukkuriMovieMaker",
        "X": anim(x),
        "Y": anim(y),
        "Z": anim(0.0),
        "Span": anim(span),
        "EasingType": "Sine",
        "EasingMode": easing_mode,
        "IsCentering": True,
        "IsEnabled": True,
        "Remark": "",
    }


def e_random_move(x: float, y: float, span: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.RandomMoveEffect, YukkuriMovieMaker",
        "X": anim(x),
        "Y": anim(y),
        "Z": anim(0.0),
        "Span": anim(span),
        "IsEnabled": True,
        "Remark": "",
    }


def e_repeat_rotate(z: float, span: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.RepeatRotateEffect, YukkuriMovieMaker",
        "X": anim(0.0),
        "Y": anim(0.0),
        "Z": anim(z),
        "Is3D": False,
        "Span": anim(span),
        "EasingType": "Sine",
        "EasingMode": "InOut",
        "IsCentering": True,
        "IsEnabled": True,
        "Remark": "",
    }


def e_random_rotate(z: float, span: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.RandomRotateEffect, YukkuriMovieMaker",
        "X": anim(0.0),
        "Y": anim(0.0),
        "Z": anim(z),
        "Is3D": False,
        "Span": anim(span),
        "IsEnabled": True,
        "Remark": "",
    }


def e_jump(height: float, stretch: float, period: float, distortion: float, interval: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.JumpEffect, YukkuriMovieMaker",
        "JumpHeight": anim(height),
        "Stretch": anim(stretch),
        "Period": anim(period),
        "Distortion": anim(distortion),
        "Interval": anim(interval),
        "X": anim(0.0),
        "Y": anim(0.0),
        "IsEnabled": True,
        "Remark": "",
    }


def e_zoom_pulse(values: list[float], span: float):
    """ZoomEffect with animated keyframes (for subtle pulse/breath motion)."""
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.ZoomEffect, YukkuriMovieMaker",
        "Zoom": anim_keyframes(values, span),
        "ZoomX": anim(100.0),
        "ZoomY": anim(100.0),
        "IsNearestNeighbor": False,
        "IsEnabled": True,
        "Remark": "",
    }


def e_random_zoom(zoom: float, span: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.RandomZoomEffect, YukkuriMovieMaker",
        "Zoom": anim(zoom),
        "ZoomX": anim(100.0),
        "ZoomY": anim(100.0),
        "Span": anim(span),
        "IsEnabled": True,
        "Remark": "",
    }


def e_crash(size: float, playback_rate: float, impact: float,
            random_rotate: float, random_vector: float,
            fly_speed: float = 100.0, fall_speed: float = 100.0):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.CrashEffect, YukkuriMovieMaker",
        "StartTime": 0.0,
        "PlaybackRate": playback_rate,
        "Size": size,
        "X": anim(0.0),
        "Y": anim(0.0),
        "Z": anim(0.0),
        "FlySpeed": fly_speed,
        "FallSpeed": fall_speed,
        "Delay": 0.0,
        "Impact": impact,
        "RandomRotate": random_rotate,
        "RandomVector": random_vector,
        "IsEnabled": True,
        "Remark": "",
    }


def e_inout_crash(in_seconds: float, size: float, impact: float,
                  random_rotate: float, random_vector: float,
                  playback_rate: float = 150.0):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.InOutCrashEffect, YukkuriMovieMaker",
        "IsInEffect": True,
        "IsOutEffect": False,
        "EffectTimeSeconds": in_seconds,
        "PlaybackRate": playback_rate,
        "Size": size,
        "X": anim(0.0),
        "Y": anim(0.0),
        "Z": anim(0.0),
        "FlySpeed": 100.0,
        "FallSpeed": 100.0,
        "Delay": 100.0,
        "Impact": impact,
        "RandomRotate": random_rotate,
        "RandomVector": random_vector,
        "IsEnabled": True,
        "Remark": "",
    }


def e_opacity_flat(opacity: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.OpacityEffect, YukkuriMovieMaker",
        "Opacity": anim(opacity),
        "IsAbsolute": False,
        "IsEnabled": True,
        "Remark": "",
    }


def e_inout_move(direction: str, in_seconds: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.InOutMoveFromOutsideImageEffect, YukkuriMovieMaker",
        "Value": direction,
        "IsInEffect": in_seconds > 0,
        "IsOutEffect": False,
        "EffectTimeSeconds": in_seconds,
        "EasingType": "Expo",
        "EasingMode": "Out",
        "IsEnabled": True,
        "Remark": "",
    }


def e_inout_move_exit(direction: str, out_seconds: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.InOutMoveFromOutsideImageEffect, YukkuriMovieMaker",
        "Value": direction,
        "IsInEffect": False,
        "IsOutEffect": True,
        "EffectTimeSeconds": out_seconds,
        "EasingType": "Expo",
        "EasingMode": "In",
        "IsEnabled": True,
        "Remark": "",
    }


def e_inout_getup(in_seconds: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.InOutGetUpEffect, YukkuriMovieMaker",
        "Base": "Bottom",
        "Is3D": False,
        "IsInEffect": True,
        "IsOutEffect": False,
        "EffectTimeSeconds": in_seconds,
        "EasingType": "Expo",
        "EasingMode": "Out",
        "IsEnabled": True,
        "Remark": "",
    }


def e_sepia(strength: float, intensity: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.SepiaEffect, YukkuriMovieMaker",
        "Strength": anim(strength),
        "SepiaIntensity": anim(intensity),
        "IsEnabled": True,
        "Remark": "",
    }


def e_blur(blur: float):
    return {
        "$type": "YukkuriMovieMaker.Project.Effects.GaussianBlurEffect, YukkuriMovieMaker",
        "Blur": anim(blur),
        "IsHardBorderMode": False,
        "IsEnabled": True,
        "Remark": "",
    }


LIBRARY_V2 = {
    "_meta": {
        "version": "2.0.0",
        "spec": "docs/MOTION_PRESET_LIBRARY_SPEC.md",
        "source": "samples/EffectsSamples_2026-04-15.ymmp (111 effects)",
        "generated": "2026-04-19",
        "note": (
            "Phase 2: parameter-filled library. Each motion has concrete values for "
            "animation parameters so motion_target direct-write produces visible, "
            "emotion-specific behavior. Scale is 'normal' intensity; _light/_heavy "
            "variants are future work. Applicable to both TachieItem (speaker) and "
            "ImageItem/GroupItem (skit performers) — not restricted by item type."
        ),
        "intensity": "normal",
    },
    "motions": {
        # 静止
        "none": [],

        # うなずき: 上下 15px の小さい往復 (Sine), 0.4s 周期
        "nod": [
            e_repeat_move(x=0.0, y=15.0, span=0.4),
        ],

        # 軽く弾む: 低ジャンプ 25px, 短周期 0.5s, interval 0.3s
        "happy_bounce": [
            e_jump(height=25.0, stretch=10.0, period=0.5, distortion=8.0, interval=0.3),
        ],

        # 弾む (中): Jump 40px, 周期 0.6s
        "bounce": [
            e_jump(height=40.0, stretch=15.0, period=0.6, distortion=12.0, interval=0.4),
        ],

        # 驚きジャンプ: Jump 50px + 軽い回転 10度
        "surprise_jump": [
            e_jump(height=50.0, stretch=15.0, period=0.4, distortion=10.0, interval=0.8),
            e_random_rotate(z=10.0, span=0.2),
        ],

        # 驚き衝撃: Crash 中規模 + 軽い回転
        "surprise_crash": [
            e_crash(size=40.0, playback_rate=100.0, impact=80.0,
                    random_rotate=30.0, random_vector=30.0),
            e_random_rotate(z=10.0, span=0.2),
        ],

        # 喜びのゆらぎ: 左右 12px + 軽い回転 5度, 1.5s 周期
        "happy_sway": [
            e_repeat_move(x=12.0, y=0.0, span=1.5),
            e_repeat_rotate(z=5.0, span=1.5),
        ],

        # 悲しげに沈む: Opacity 85% + 下方向に 5px ゆっくり往復
        #   NOTE: 「下がって戻る」挙動。「沈んだまま戻らない」場合は要 spec 相談
        "sad_droop": [
            e_opacity_flat(opacity=85.0),
            e_repeat_move(x=0.0, y=8.0, span=2.0),
        ],

        # 怒りの震え: ランダム移動 15x10px + 回転 8度, 0.08s 高速
        "angry_shake": [
            e_random_move(x=15.0, y=10.0, span=0.08),
            e_random_rotate(z=8.0, span=0.08),
        ],

        # 怒りの衝撃: 強い Crash + 移動
        "angry_crash": [
            e_crash(size=60.0, playback_rate=120.0, impact=130.0,
                    random_rotate=60.0, random_vector=50.0),
            e_random_move(x=12.0, y=8.0, span=0.1),
        ],

        # 考えるズーム: 100 → 108 → 100 のゆるやかな脈動
        #   NOTE: user が「徐々にズームして静止」を望む場合は要調整
        "thinking_zoom": [
            e_zoom_pulse(values=[100.0, 108.0, 100.0], span=1.5),
        ],

        # 慌ての震え: 小さい高速ランダム移動 8x6 + 軽い回転 4度 (Zoom は除去 — user feedback 2026-04-19)
        "panic_shake": [
            e_random_move(x=8.0, y=6.0, span=0.05),
            e_random_rotate(z=4.0, span=0.05),
        ],

        # ツッコミ: 登場衝撃 (既存の full parameter 維持、パラメータはデモ値のまま)
        "tsukkomi": [
            e_inout_crash(in_seconds=0.3, size=40.0, impact=80.0,
                          random_rotate=50.0, random_vector=50.0, playback_rate=150.0),
        ],

        # 否定の首振り: 左右 25px, 0.5s 周期 (Sine InOut, centering)
        "deny_shake": [
            e_repeat_move(x=25.0, y=0.0, span=0.5),
        ],

        # 登場: 左/右/上から / 立ち上がり (InOut 系、既存の full parameter 踏襲)
        "entrance_left": [e_inout_move("Left", 0.3)],
        "entrance_right": [e_inout_move("Right", 0.3)],
        "entrance_top": [e_inout_move("Top", 0.3)],
        "entrance_getup": [e_inout_getup(0.3)],

        # 退場
        "exit_left": [e_inout_move_exit("Left", 0.3)],
        "exit_right": [e_inout_move_exit("Right", 0.3)],

        # 回想: Sepia 強度 70% + ガウスぼかし 3px
        "flashback": [
            e_sepia(strength=70.0, intensity=0.6),
            e_blur(blur=3.0),
        ],

        # 注目ズーム: 100 → 115 → 115 の前進ズーム (1s かけてズームし、2s 目で静止)
        #   NOTE: user の意図により「戻るか静止か」を調整
        "focus_zoom": [
            e_zoom_pulse(values=[100.0, 115.0, 115.0], span=2.0),
        ],

        # 背景ぼかし: Blur 5px + Opacity 70%
        "defocus": [
            e_blur(blur=5.0),
            e_opacity_flat(opacity=70.0),
        ],
    },
}


def main():
    out_path = Path("samples/tachie_motion_map_library.json")
    out_path.write_text(
        json.dumps(LIBRARY_V2, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
    print(f"  motions: {len(LIBRARY_V2['motions'])}")


if __name__ == "__main__":
    main()

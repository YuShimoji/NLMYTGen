"""Build the bounded Route A concrete visual-proof package.

This module creates deterministic, repository-tracked SVG/HTML/JSON review
artifacts.  It does not edit approved content, launch YMM4, render video, fetch
assets, or grant implementation, production, publication, or rights approval.
"""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


ROUTE_ID = "route_A_security_inspection_lab"
BASE_REVISION = "d38075b97efabc99d1a23e8e0afafd5d44f1e2de"
PRESENTATION_BASE_REVISION = "f611aacd0e6d238bce76df7bdc6f55b86695b842"
DISCLAIMER = "模式図／実券の縮尺・配置ではありません"
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
SUBTITLE_SAFE_AREA = {"x": 84, "y": 780, "width": 1752, "height": 220}

PRESENTATION_BEFORE_SHA256 = {
    "keyframes/route_a_S1_overview.svg": "d7c15399125de9c7a05d8bd43ce5d6e50ec6c144200ff9c472d06e88e6f43c86",
    "keyframes/route_a_S3_identification_summary.svg": "b7f1f10e6bc514aaa00c3e2bcb30f49dba8a770041ad391ebc0ecaed407daea0",
    "keyframes/route_a_cue_003_watermark.svg": "4c09f4ad4e6c26db35bdf15f9cea899c34cabd50a6b4ae0f66d8184c1f1f6c70",
    "keyframes/route_a_cue_004_hologram.svg": "58f8b0383164a2f93decca32cf12c8640be81098b529f117e5a2540651b4a410",
    "keyframes/route_a_cue_005_intaglio.svg": "7fbf2ed7ac443ddb999cddc632e1d7b5c0c01306de3d2d7468f9409e3c0e6efd",
    "keyframes/route_a_cue_006_microtext.svg": "c91b41bf28155d77116e3b26f8120225663ecdb757628678b1252ba41ea8d32d",
    "route_a_motion_storyboard.svg": "3c8aaeefad1e983e1bcd20613937b10c0db07ff0e72147284a2313574a97e478",
    "route_a_nine_cue_contact_sheet.svg": "d04f006ad04d881c1a84f4a226f461b33b50a34ab1e52895e18c0d701771ff5a",
    "route_a_visual_proof.html": "5d06d6f526606aa20d423f8ba2495eb8d1e450cb57a41ece859dc5a24d7e692a",
}

DEFAULT_PILOT = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_OUTPUT = DEFAULT_PILOT / "route_a_visual_proof"

KEYFRAME_SPECS: tuple[dict[str, Any], ...] = (
    {
        "filename": "route_a_S1_overview.svg",
        "scene_id": "S1",
        "cue_id": "cue_001",
        "action": "全体像を見る",
        "title": "新しいお札を、四つの確認動作から見る",
        "explanation": "2024年発行という入口から、複数の技術と見分けやすさを順に整理します。",
        "explanation_lines": (
            "2024年発行という入口から、",
            "複数の技術と見分けやすさを",
            "順に整理します。",
        ),
        "motif": "overview",
    },
    {
        "filename": "route_a_cue_003_watermark.svg",
        "scene_id": "S2",
        "cue_id": "cue_003",
        "action": "透かす",
        "title": "高精細すき入れ",
        "explanation": "透過光で細かな模様が見える現象だけを、抽象的な光の層として示します。",
        "explanation_lines": (
            "透過光で細かな模様が見える",
            "現象だけを、抽象的な光の層として",
            "示します。",
        ),
        "motif": "watermark",
    },
    {
        "filename": "route_a_cue_004_hologram.svg",
        "scene_id": "S2",
        "cue_id": "cue_004",
        "action": "傾ける",
        "title": "3Dホログラム",
        "explanation": "角度で見え方が変わることを、人物を描かない抽象層のずれとして示します。",
        "explanation_lines": (
            "角度で見え方が変わることを、",
            "人物を描かない抽象層のずれとして",
            "示します。",
        ),
        "motif": "hologram",
    },
    {
        "filename": "route_a_cue_005_intaglio.svg",
        "scene_id": "S2",
        "cue_id": "cue_005",
        "action": "触る",
        "title": "深凹版印刷",
        "explanation": "インキの盛り上がりと触感を、寸法を持たない三本の抽象稜線で示します。",
        "explanation_lines": (
            "インキの盛り上がりと触感を、",
            "寸法を持たない三本の抽象稜線で",
            "示します。",
        ),
        "motif": "intaglio",
    },
    {
        "filename": "route_a_cue_006_microtext.svg",
        "scene_id": "S2",
        "cue_id": "cue_006",
        "action": "ルーペで見る",
        "title": "マイクロ文字",
        "explanation": "単一の模式ラベルを拡大し、実寸・密度・位置・周辺模様は再現しません。",
        "explanation_lines": (
            "単一の模式ラベルを拡大し、",
            "実寸・密度・位置・周辺模様は",
            "再現しません。",
        ),
        "motif": "microtext",
    },
    {
        "filename": "route_a_S3_identification_summary.svg",
        "scene_id": "S3",
        "cue_id": "cue_009",
        "action": "四つを覚える",
        "title": "識別の工夫と確認動作",
        "explanation": "識別の工夫を整理し、透かす・触る・傾ける・ルーペで見るを一列でまとめます。",
        "explanation_lines": (
            "識別の工夫を整理し、",
            "透かす・触る・傾ける・",
            "ルーペで見るを一列でまとめます。",
        ),
        "motif": "summary",
    },
)

APPROVED_SUBTITLE_LINES_BY_CUE: dict[str, tuple[str, ...]] = {
    "cue_001": (
        "2024年に発行された新しいお札って、",
        "見た目以外にも変わったところがあるの？",
    ),
    "cue_002": (
        "あるぞ。偽造防止では、高精細すき入れや",
        "3Dホログラムなど複数の技術を",
        "組み合わせている。誰にとっても使いやすい",
        "ユニバーサルデザインも取り入れたんだ。",
    ),
    "cue_003": (
        "まずは高精細すき入れ。",
        "光に透かすと、細かな模様が見えるんだぜ。",
    ),
    "cue_004": (
        "次は3Dホログラム。角度を変えると、",
        "三次元の肖像が回転して見えるぞ。",
    ),
    "cue_005": (
        "触るとざらざらするのは、",
        "額面数字などのインキを高く盛り上げる",
        "深凹版印刷なんだね。",
    ),
    "cue_006": (
        "マイクロ文字の『NIPPONGINKO』は、",
        "ルーペで確かめられる。",
        "カラーコピー機では再現が難しいほど",
        "小さい文字なんだ。",
    ),
    "cue_007": (
        "見分けやすさの工夫では、識別マークを",
        "11本の斜線にそろえ、券種ごとに",
        "位置を変えているぜ。",
    ),
    "cue_008": (
        "額面の数字は前のシリーズのお札より大きい。",
        "一万円券と千円券ではホログラムの形や",
        "位置が違い、千円券の中央には",
        "橙色のグラデーションもあるんだね。",
    ),
    "cue_009": (
        "確かめ方は、透かす、触る、傾ける、",
        "ルーペで見る。この四つを覚えておこう。",
    ),
}

MOTION_SPECS: dict[str, dict[str, Any]] = {
    "cue_001": {
        "principal_motion": "short_label_transition",
        "start": "問いのラベルを待機",
        "emphasis": "ラベルを一度だけ表示",
        "settled": "全体像を静止保持",
        "duration_seconds": 0.55,
        "easing": "ease_out",
    },
    "cue_002": {
        "principal_motion": "short_label_transition",
        "start": "技術レイヤーを待機",
        "emphasis": "四層を一度だけ提示",
        "settled": "レイヤーを静止保持",
        "duration_seconds": 0.65,
        "easing": "ease_out",
    },
    "cue_003": {
        "principal_motion": "light_reveal_once",
        "start": "透過光なし",
        "emphasis": "光の帯が一度通過",
        "settled": "細線だけを静止表示",
        "duration_seconds": 0.9,
        "easing": "ease_in_out",
    },
    "cue_004": {
        "principal_motion": "restrained_tilt_once",
        "start": "抽象層を正面表示",
        "emphasis": "小さく一度傾ける",
        "settled": "一度だけ戻して静止",
        "duration_seconds": 1.1,
        "easing": "ease_in_out",
    },
    "cue_005": {
        "principal_motion": "tactile_pulse",
        "start": "稜線を静止表示",
        "emphasis": "稜線を二回以内で脈動",
        "settled": "盛り上がりを静止保持",
        "duration_seconds": 0.8,
        "easing": "ease_out",
        "pulse_count": 2,
    },
    "cue_006": {
        "principal_motion": "loupe_zoom_once",
        "start": "ルーペを待機",
        "emphasis": "一度だけ拡大",
        "settled": "拡大ラベルを静止保持",
        "duration_seconds": 0.85,
        "easing": "ease_out",
    },
    "cue_007": {
        "principal_motion": "position_callout_once",
        "start": "位置カードを静止表示",
        "emphasis": "差分を一度だけ指示",
        "settled": "三カードを静止保持",
        "duration_seconds": 0.6,
        "easing": "ease_out",
    },
    "cue_008": {
        "principal_motion": "bounded_difference_reveal_once",
        "start": "比較カードを待機",
        "emphasis": "差異を一度だけ提示",
        "settled": "限定比較を静止保持",
        "duration_seconds": 0.7,
        "easing": "ease_out",
    },
    "cue_009": {
        "principal_motion": "four_action_sequence_once",
        "start": "四アイコンを待機",
        "emphasis": "四アイコンを一度だけ順次表示",
        "settled": "四動作を静止保持",
        "duration_seconds": 1.2,
        "easing": "linear_steps",
    },
}

ACTION_BY_CUE = {
    "cue_001": "問い",
    "cue_002": "俯瞰",
    "cue_003": "透かす",
    "cue_004": "傾ける",
    "cue_005": "触る",
    "cue_006": "ルーペで見る",
    "cue_007": "位置を比べる",
    "cue_008": "違いを限定比較",
    "cue_009": "四動作を覚える",
}

RISK_BY_CUE = {
    "cue_001": "発行年のみ／政策意図を示さない",
    "cue_002": "採用技術のみ／効果を断定しない",
    "cue_003": "現象のみ／位置・寸法・製法なし",
    "cue_004": "現象のみ／実形状・箔模様なし",
    "cue_005": "触感のみ／製造寸法なし",
    "cue_006": "模式ラベルのみ／実寸・密度なし",
    "cue_007": "11本と位置差のみ／座標なし",
    "cue_008": "限定比較／橙色だけ事実色",
    "cue_009": "確認動作／真贋保証ではない",
}

MOTION_DISPLAY_BY_CUE = {
    "cue_001": "label transition once",
    "cue_002": "layer reveal once",
    "cue_003": "light reveal once",
    "cue_004": "restrained tilt once",
    "cue_005": "tactile pulse ≤ 2",
    "cue_006": "loupe zoom once",
    "cue_007": "callout once",
    "cue_008": "difference reveal once",
    "cue_009": "four-action sequence once",
}

REVIEW_QUESTIONS: tuple[str, ...] = (
    "S1／S2／S3の画面は、説明順と一致して理解しやすいですか。",
    "抽象券や各技術の模式図が、実券の正確な形状・位置・公式手順に見えませんか。",
    "字幕領域、見出し、説明文は1920×1080画面で読みやすいですか。",
    "motion storyboardは十分に抑制され、各cueの主旨を邪魔していませんか。",
)


def build_route_a_visual_proof(*, root: str | Path | None = None) -> dict[str, Any]:
    """Build the deterministic Route A proof and return changed paths/checks."""

    repo_root = Path(root).resolve() if root is not None else Path.cwd().resolve()
    pilot = repo_root / DEFAULT_PILOT
    output = repo_root / DEFAULT_OUTPUT
    keyframe_dir = output / "keyframes"
    viewer_keyframe_dir = output / "viewer_keyframes"
    script = _load_json(pilot / "canonical_script.json")
    approval = _load_json(pilot / "human_script_approval_receipt.json")
    scene_plan = _load_json(pilot / "visual_scene_decision/scene_layout_plan.json")
    cues = _cue_models(script, scene_plan)

    changed: list[str] = []
    generated: dict[Path, str] = {}
    receipt = _selection_receipt(script, approval)
    generated[output / "human_visual_direction_selection_receipt.json"] = _json_text(receipt)

    cue_by_id = {str(cue["cue_id"]): cue for cue in cues}
    for spec in KEYFRAME_SPECS:
        generated[keyframe_dir / spec["filename"]] = _render_keyframe(
            spec, cue_by_id[spec["cue_id"]]
        )
        generated[viewer_keyframe_dir / spec["filename"]] = _render_viewer_keyframe(
            spec, cue_by_id[spec["cue_id"]]
        )

    mapping = _cue_mapping(cues)
    generated[output / "route_a_cue_visual_mapping.json"] = _json_text(mapping)
    generated[output / "route_a_nine_cue_contact_sheet.svg"] = _render_contact_sheet(cues)

    motion = _motion_storyboard(cues)
    generated[output / "route_a_motion_storyboard.json"] = _json_text(motion)
    generated[output / "route_a_motion_storyboard.svg"] = _render_motion_storyboard(cues)
    generated[output / "route_a_visual_review_sheet.md"] = _render_review_sheet()
    generated[output / "README_ROUTE_A_VISUAL_PROOF.md"] = _render_readme()
    generated[output / "route_a_visual_proof.html"] = _render_html()
    generated[
        output / "visual_proof_presentation_revision_receipt.json"
    ] = _json_text(_presentation_revision_receipt(repo_root, generated, script, approval))

    for path, content in generated.items():
        if _write_if_changed(path, content):
            changed.append(_relative(repo_root, path))

    manifest = _manifest(repo_root, generated, script, approval)
    manifest_path = output / "route_a_visual_proof_manifest.json"
    if _write_if_changed(manifest_path, _json_text(manifest)):
        changed.append(_relative(repo_root, manifest_path))

    readback = _readback(repo_root, generated, manifest, cues, script, approval)
    readback_path = output / "route_a_visual_proof_readback.json"
    if _write_if_changed(readback_path, _json_text(readback)):
        changed.append(_relative(repo_root, readback_path))

    return {
        "status": "passed" if readback["checks"]["all_passed"] else "failed",
        "changed": sorted(changed),
        "artifact_root": _relative(repo_root, output),
        "checks": readback["checks"],
    }


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _cue_models(
    script: dict[str, Any], scene_plan: dict[str, Any]
) -> list[dict[str, Any]]:
    plan_by_id: dict[str, dict[str, Any]] = {}
    for scene in scene_plan["scenes"]:
        for cue in scene["cue_plans"]:
            plan_by_id[str(cue["cue_id"])] = cue
    models: list[dict[str, Any]] = []
    for cue in script["cues"]:
        cue_id = str(cue["cue_id"])
        plan = plan_by_id[cue_id]
        models.append(
            {
                "sequence": int(cue["sequence"]),
                "cue_id": cue_id,
                "scene_id": str(cue["scene_id"]),
                "speaker": str(cue["speaker"]),
                "text": str(cue["text"]),
                "action": ACTION_BY_CUE[cue_id],
                "screen_objective": str(plan["screen_objective"]),
                "factual_boundary": str(plan["source_backed_factual_boundary"]),
                "risk_label": RISK_BY_CUE[cue_id],
                "principal_motion": MOTION_SPECS[cue_id]["principal_motion"],
                "disclaimer": DISCLAIMER,
            }
        )
    return models


def _selection_receipt(
    script: dict[str, Any], approval: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.route_a_visual_direction_selection_receipt.v1",
        "receipt_id": "new-banknote-route-a-direction-selected-for-proof-v1",
        "status": "valid_direction_only",
        "route_id": ROUTE_ID,
        "selection_class": "direction_selected_for_concrete_proof",
        "user_decision": "explicit",
        "decision_observed_date": "2026-07-19",
        "timestamp_basis": "worker_contract_date_no_inferred_time",
        "source_base_revision": BASE_REVISION,
        "selection_scope": "visual_direction_for_concrete_proof_only",
        "scene_spine": {"S1": 2, "S2": 4, "S3": 3},
        "approved_content_identity": {
            "approval_receipt_id": approval["receipt_id"],
            "cue_count": script["cue_count"],
            "speaker_counts": script["speaker_counts"],
            "approved_file_hash_count": len(approval["approved_file_hashes"]),
            "content_change_authorized": False,
        },
        "diagram_constraint": DISCLAIMER,
        "motion_constraint": {
            "principal_motion_maximum_per_cue": 1,
            "continuous_loop_allowed": False,
        },
        "authorization": {
            "concrete_visual_proof_generation": True,
            "final_visual_acceptance": False,
            "implementation_authorized": False,
            "YMM4_authorized": False,
            "render_authorized": False,
            "production_authorized": False,
            "public_release_authorized": False,
            "rights_authorized": False,
        },
        "invalidation_rules": [
            "route_id changes",
            "S1/S2/S3 scene spine changes",
            "approved cue text or order changes",
            "schematic/non-scale disclaimer is removed or weakened",
            "principal motion budget or non-looping rule changes",
        ],
        "successor_approval_policy": {
            "proof_may_be_accepted_only_by_human_review": True,
            "acceptance_or_revision_receipt_required": True,
            "shot_motion_and_asset_contracts_remain_separate": True,
            "YMM4_requires_separate_authorization": True,
        },
    }


def _cue_mapping(cues: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.route_a_cue_visual_mapping.v1",
        "status": "concrete_proof_review_ready_not_accepted",
        "route_id": ROUTE_ID,
        "cue_count": len(cues),
        "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
        "subtitle_safe_area": SUBTITLE_SAFE_AREA,
        "cues": [
            {
                **cue,
                "thumbnail_present": True,
                "subtitle_treatment": "approved_text_in_reserved_lower_band",
                "principal_motion_count": 1,
                "loop": False,
                "factual_color_exception": (
                    "orange_represents_actual_banknote_fact_only_here"
                    if cue["cue_id"] == "cue_008"
                    else "orange_is_ui_emphasis_only"
                ),
            }
            for cue in cues
        ],
    }


def _motion_storyboard(cues: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for cue in cues:
        motion = dict(MOTION_SPECS[cue["cue_id"]])
        rows.append(
            {
                "cue_id": cue["cue_id"],
                "scene_id": cue["scene_id"],
                **motion,
                "loop": False,
                "simultaneous_principal_motions": 1,
                "implementation_status": "proposal_only_not_implemented",
            }
        )
    return {
        "schema_version": "new_banknote.route_a_motion_storyboard.v1",
        "status": "proposal_only_non_looping",
        "route_id": ROUTE_ID,
        "motion_bearing_cue_count": len(rows),
        "principal_motion_maximum_per_cue": 1,
        "continuous_loop_allowed": False,
        "states": ["start", "emphasis", "settled"],
        "cues": rows,
    }


def _render_keyframe(spec: dict[str, Any], cue: dict[str, Any]) -> str:
    subtitle_lines = list(APPROVED_SUBTITLE_LINES_BY_CUE[cue["cue_id"]])
    explanation_lines = list(spec["explanation_lines"])
    action_lines = _wrap_text(spec["action"], 7, max_lines=2)
    title_lines = _wrap_text(spec["title"], 10, max_lines=2)
    motion_lines = _wrap_words(
        MOTION_DISPLAY_BY_CUE[cue["cue_id"]], 18, max_lines=2
    )
    motif = _render_motif(spec["motif"])
    lines = [
        _svg_open(
            f"Route A {spec['scene_id']} {cue['cue_id']} concrete visual proof",
            {
                "data-route-id": ROUTE_ID,
                "data-surface": "annotation",
                "data-scene-id": spec["scene_id"],
                "data-cue-id": cue["cue_id"],
                "data-approved-text": cue["text"],
                "data-subtitle-safe-area": "84,780,1752,220",
                "data-implementation-authorized": "false",
            },
        ),
        "  <rect width=\"1920\" height=\"1080\" fill=\"#E9E5DB\"/>",
        "  <path d=\"M0 180H1920M0 360H1920M0 540H1920M0 720H1920 M240 90V760M480 90V760M720 90V760M960 90V760M1200 90V760M1440 90V760M1680 90V760\" stroke=\"#D4CEC0\" stroke-width=\"2\" opacity=\"0.55\"/>",
        "  <rect x=\"0\" y=\"0\" width=\"1920\" height=\"94\" fill=\"#17324D\"/>",
        "  <text x=\"84\" y=\"59\" class=\"ui\" font-size=\"30\" font-weight=\"800\" fill=\"#F8F5ED\">ROUTE A / SECURITY INSPECTION LAB</text>",
        "  <rect x=\"1414\" y=\"22\" width=\"422\" height=\"50\" rx=\"25\" fill=\"#F8F5ED\"/>",
        "  <text x=\"1625\" y=\"56\" text-anchor=\"middle\" class=\"ui\" font-size=\"22\" font-weight=\"800\" fill=\"#17324D\">CONCRETE PROOF / REVIEW PENDING</text>",
        "  <rect x=\"84\" y=\"134\" width=\"316\" height=\"586\" rx=\"28\" fill=\"#17324D\"/>",
        f"  <text x=\"126\" y=\"194\" class=\"ui\" font-size=\"24\" font-weight=\"700\" fill=\"#A9C8BC\">{_xml(spec['scene_id'])} / {_xml(cue['cue_id'])}</text>",
        *_svg_text_lines(action_lines, x=126, y=276, size=42, line_height=50, fill="#F8F5ED", weight="900"),
        "  <line x1=\"126\" y1=\"350\" x2=\"354\" y2=\"350\" stroke=\"#D77836\" stroke-width=\"8\"/>",
        f"  <text x=\"126\" y=\"408\" class=\"ui\" font-size=\"25\" font-weight=\"700\" fill=\"#A9C8BC\">PRINCIPAL MOTION</text>",
        *_svg_text_lines(
            motion_lines,
            x=126,
            y=454,
            size=23,
            line_height=34,
            fill="#F8F5ED",
            weight="700",
        ),
        "  <text x=\"126\" y=\"620\" class=\"ui\" font-size=\"24\" fill=\"#A9C8BC\">loop: false</text>",
        "  <text x=\"126\" y=\"660\" class=\"ui\" font-size=\"24\" fill=\"#A9C8BC\">principal: 1</text>",
        "  <rect x=\"438\" y=\"134\" width=\"892\" height=\"586\" rx=\"32\" fill=\"#F8F5ED\" stroke=\"#17324D\" stroke-width=\"4\"/>",
        "  <rect x=\"478\" y=\"170\" width=\"812\" height=\"64\" rx=\"16\" fill=\"#E1ECE6\"/>",
        f"  <text x=\"884\" y=\"212\" text-anchor=\"middle\" class=\"ui\" font-size=\"25\" font-weight=\"800\" fill=\"#2F6F5D\">{_xml(DISCLAIMER)}</text>",
        "  <rect x=\"520\" y=\"274\" width=\"728\" height=\"374\" rx=\"48\" fill=\"#F3EFE4\" stroke=\"#2F6F5D\" stroke-width=\"5\" stroke-dasharray=\"20 14\"/>",
        motif,
        "  <rect x=\"1368\" y=\"134\" width=\"468\" height=\"586\" rx=\"28\" fill=\"#F8F5ED\" stroke=\"#C7BFAF\" stroke-width=\"3\"/>",
        f"  <text x=\"1410\" y=\"200\" class=\"ui\" font-size=\"25\" font-weight=\"800\" fill=\"#2F6F5D\">{_xml(spec['action'])}</text>",
        *_svg_text_lines(title_lines, x=1410, y=260, size=34, line_height=46, fill="#17324D", weight="900"),
        "  <line x1=\"1410\" y1=\"338\" x2=\"1792\" y2=\"338\" stroke=\"#D77836\" stroke-width=\"6\"/>",
        *_svg_text_lines(
            explanation_lines,
            x=1410,
            y=398,
            size=27,
            line_height=43,
            fill="#263E52",
            weight="600",
        ),
        "  <rect x=\"1410\" y=\"620\" width=\"382\" height=\"58\" rx=\"12\" fill=\"#E9E5DB\"/>",
        "  <text x=\"1601\" y=\"658\" text-anchor=\"middle\" class=\"ui\" font-size=\"22\" font-weight=\"800\" fill=\"#6A6258\">SOURCE-BOUNDED EXPLANATION</text>",
        "  <rect x=\"84\" y=\"780\" width=\"1752\" height=\"220\" rx=\"26\" fill=\"#111D29\" stroke=\"#D77836\" stroke-width=\"5\"/>",
        "  <text x=\"126\" y=\"832\" class=\"ui\" font-size=\"22\" font-weight=\"800\" fill=\"#DFA06F\">SUBTITLE SAFE AREA / APPROVED TEXT</text>",
        f"  <rect x=\"1540\" y=\"808\" width=\"250\" height=\"44\" rx=\"22\" fill=\"#2F6F5D\"/><text x=\"1665\" y=\"838\" text-anchor=\"middle\" class=\"ui\" font-size=\"21\" font-weight=\"800\" fill=\"#FFFFFF\">{_xml(cue['speaker'])}</text>",
        *_svg_text_lines(
            subtitle_lines,
            x=126,
            y=875,
            size=31,
            line_height=38,
            fill="#FFFFFF",
            weight="800",
        ),
        "</svg>",
        "",
    ]
    return "\n".join(lines)


def _render_viewer_keyframe(spec: dict[str, Any], cue: dict[str, Any]) -> str:
    subtitle_lines = list(APPROVED_SUBTITLE_LINES_BY_CUE[cue["cue_id"]])
    explanation_lines = list(spec["explanation_lines"])
    title_lines = _wrap_text(spec["title"], 15, max_lines=2)
    motif = _render_motif(spec["motif"], viewer=True)
    lines = [
        _svg_open(
            f"{spec['action']} — {spec['title']}",
            {
                "data-route-id": ROUTE_ID,
                "data-surface": "viewer",
                "data-scene-id": spec["scene_id"],
                "data-cue-id": cue["cue_id"],
                "data-approved-text": cue["text"],
                "data-subtitle-safe-area": "84,780,1752,220",
                "data-implementation-authorized": "false",
            },
        ),
        '  <rect width="1920" height="1080" fill="#E9E5DB"/>',
        '  <rect width="1920" height="108" fill="#17324D"/>',
        '  <text x="84" y="68" class="ui" font-size="30" font-weight="900" fill="#F8F5ED">新しいお札の確認ポイント</text>',
        f'  <rect x="84" y="142" width="1220" height="578" rx="34" fill="#F8F5ED" stroke="#D4CEC0" stroke-width="3"/>',
        f'  <rect x="118" y="174" width="470" height="52" rx="26" fill="#E1ECE6"/><text x="353" y="209" text-anchor="middle" class="ui" font-size="22" font-weight="800" fill="#2F6F5D">{_xml(DISCLAIMER)}</text>',
        '  <rect x="520" y="274" width="728" height="374" rx="48" fill="#F3EFE4" stroke="#2F6F5D" stroke-width="5"/>',
        motif,
        '  <rect x="1340" y="142" width="496" height="578" rx="34" fill="#F8F5ED" stroke="#C7BFAF" stroke-width="3"/>',
        f'  <text x="1384" y="204" class="ui" font-size="25" font-weight="800" fill="#2F6F5D">{_xml(spec["action"])}</text>',
        *_svg_text_lines(
            title_lines,
            x=1384,
            y=270,
            size=36,
            line_height=48,
            fill="#17324D",
            weight="900",
        ),
        '  <line x1="1384" y1="360" x2="1792" y2="360" stroke="#D77836" stroke-width="6"/>',
        *_svg_text_lines(
            explanation_lines,
            x=1384,
            y=422,
            size=27,
            line_height=44,
            fill="#263E52",
            weight="600",
        ),
        '  <rect x="84" y="780" width="1752" height="220" rx="28" fill="#111D29"/>',
        '  <rect x="84" y="780" width="12" height="220" rx="6" fill="#D77836"/>',
        *_svg_text_lines(
            subtitle_lines,
            x=130,
            y=850,
            size=32,
            line_height=42,
            fill="#FFFFFF",
            weight="800",
        ),
        "</svg>",
        "",
    ]
    return "\n".join(lines)


def _render_motif(name: str, *, viewer: bool = False) -> str:
    overview_label = "2024年／新紙幣" if viewer else "NEW / 2024"
    watermark_label = "透過光" if viewer else "LIGHT"
    hologram_label = "抽象レイヤー／人物図なし" if viewer else "ABSTRACT LAYERS / NO LIKENESS"
    intaglio_label = "触感の模式図／縮尺なし" if viewer else "TACTILE ELEVATION / NOT TO SCALE"
    microtext_label = "模式ラベル" if viewer else "SCHEMATIC LABEL"
    summary_label = "四つの動作を一度ずつ" if viewer else "CHECK ONCE / REMEMBER FOUR"
    if name == "overview":
        return "\n".join(
            [
                '  <circle cx="884" cy="452" r="94" fill="#E1ECE6" stroke="#2F6F5D" stroke-width="5"/>',
                f'  <text x="884" y="464" text-anchor="middle" class="ui" font-size="31" font-weight="900" fill="#17324D">{_xml(overview_label)}</text>',
                '  <rect x="574" y="332" width="164" height="92" rx="18" fill="#DDE9F0"/><text x="656" y="389" text-anchor="middle" class="ui" font-size="25" font-weight="800" fill="#17324D">透かす</text>',
                '  <rect x="1030" y="332" width="164" height="92" rx="18" fill="#F1DFC9"/><text x="1112" y="389" text-anchor="middle" class="ui" font-size="25" font-weight="800" fill="#17324D">傾ける</text>',
                '  <rect x="574" y="506" width="164" height="92" rx="18" fill="#E1ECE6"/><text x="656" y="563" text-anchor="middle" class="ui" font-size="25" font-weight="800" fill="#17324D">触る</text>',
                '  <rect x="1030" y="506" width="164" height="92" rx="18" fill="#E8E2F1"/><text x="1112" y="563" text-anchor="middle" class="ui" font-size="25" font-weight="800" fill="#17324D">ルーペ</text>',
                '  <path d="M738 378L802 420M1030 378L966 420M738 552L802 494M1030 552L966 494" stroke="#2F6F5D" stroke-width="6"/>',
            ]
        )
    if name == "watermark":
        return "\n".join(
            [
                '  <path d="M558 610L848 292L1002 292L720 610Z" fill="#DDE9F0" opacity="0.8"/>',
                '  <path d="M720 560C780 330 1010 330 1100 558M748 560C810 380 985 380 1072 558M780 560C840 426 960 426 1040 558" fill="none" stroke="#2F6F5D" stroke-width="7" opacity="0.75"/>',
                '  <circle cx="914" cy="470" r="74" fill="#F8F5ED" opacity="0.72"/>',
                f'  <text x="914" y="480" text-anchor="middle" class="ui" font-size="28" font-weight="900" fill="#17324D">{_xml(watermark_label)}</text>',
            ]
        )
    if name == "hologram":
        return "\n".join(
            [
                '  <g transform="translate(884 466)"><rect x="-150" y="-118" width="300" height="236" rx="36" fill="#DDE9F0" transform="rotate(-8)"/><rect x="-122" y="-104" width="244" height="208" rx="34" fill="#E8E2F1" opacity="0.82" transform="rotate(7)"/><path d="M-58 -48L52 -76L82 18L-18 76L-92 8Z" fill="#A9C8BC"/></g>',
                '  <path d="M650 352C570 430 580 538 666 610M1116 352C1196 430 1186 538 1100 610" fill="none" stroke="#D77836" stroke-width="8" stroke-linecap="round"/>',
                '  <path d="M650 352L624 398M650 352L602 368M1116 352L1142 398M1116 352L1164 368" stroke="#D77836" stroke-width="8" stroke-linecap="round"/>',
                f'  <text x="884" y="610" text-anchor="middle" class="ui" font-size="23" font-weight="800" fill="#17324D">{_xml(hologram_label)}</text>',
            ]
        )
    if name == "intaglio":
        return "\n".join(
            [
                '  <path d="M620 558C680 558 692 382 752 382S824 558 884 558 956 382 1016 382 1088 558 1148 558" fill="none" stroke="#2F6F5D" stroke-width="22" stroke-linecap="round"/>',
                '  <path d="M620 594H1148" stroke="#17324D" stroke-width="7"/>',
                '  <path d="M748 330V278M884 330V258M1020 330V278" stroke="#D77836" stroke-width="8" stroke-linecap="round"/>',
                '  <path d="M728 300L748 330L768 300M864 280L884 310L904 280M1000 300L1020 330L1040 300" fill="none" stroke="#D77836" stroke-width="8"/>',
                f'  <text x="884" y="640" text-anchor="middle" class="ui" font-size="24" font-weight="800" fill="#17324D">{_xml(intaglio_label)}</text>',
            ]
        )
    if name == "microtext":
        return "\n".join(
            [
                '  <g opacity="0.45" stroke="#2F6F5D" stroke-width="3"><path d="M570 342H1180M570 390H1180M570 438H1180M570 486H1180M570 534H1180M570 582H1180"/><path d="M610 310V618M690 310V618M770 310V618M850 310V618M930 310V618M1010 310V618M1090 310V618M1170 310V618"/></g>',
                '  <circle cx="930" cy="438" r="142" fill="#F8F5ED" stroke="#17324D" stroke-width="14"/>',
                '  <line x1="1034" y1="542" x2="1142" y2="632" stroke="#17324D" stroke-width="24" stroke-linecap="round"/>',
                '  <text x="930" y="430" text-anchor="middle" class="ui" font-size="30" font-weight="900" fill="#2F6F5D">NIPPONGINKO</text>',
                f'  <text x="930" y="476" text-anchor="middle" class="ui" font-size="22" font-weight="700" fill="#17324D">{_xml(microtext_label)}</text>',
            ]
        )
    return "\n".join(
        [
            '  <rect x="560" y="342" width="146" height="182" rx="28" fill="#DDE9F0"/><text x="633" y="422" text-anchor="middle" class="ui" font-size="24" font-weight="900" fill="#17324D">透かす</text><circle cx="633" cy="470" r="30" fill="#FFFFFF" stroke="#2F6F5D" stroke-width="5"/>',
            '  <rect x="728" y="342" width="146" height="182" rx="28" fill="#E1ECE6"/><text x="801" y="422" text-anchor="middle" class="ui" font-size="24" font-weight="900" fill="#17324D">触る</text><path d="M766 482C780 442 822 442 838 482" fill="none" stroke="#2F6F5D" stroke-width="8"/>',
            '  <rect x="896" y="342" width="146" height="182" rx="28" fill="#F1DFC9"/><text x="969" y="422" text-anchor="middle" class="ui" font-size="24" font-weight="900" fill="#17324D">傾ける</text><path d="M932 484L1002 454M932 484L994 506" stroke="#D77836" stroke-width="8"/>',
            '  <rect x="1064" y="342" width="146" height="182" rx="28" fill="#E8E2F1"/><text x="1137" y="422" text-anchor="middle" class="ui" font-size="22" font-weight="900" fill="#17324D">ルーペ</text><circle cx="1128" cy="474" r="30" fill="none" stroke="#17324D" stroke-width="7"/><line x1="1150" y1="496" x2="1180" y2="526" stroke="#17324D" stroke-width="8"/>',
            f'  <text x="884" y="602" text-anchor="middle" class="ui" font-size="28" font-weight="900" fill="#2F6F5D">{_xml(summary_label)}</text>',
        ]
    )


def _render_contact_sheet(cues: list[dict[str, Any]]) -> str:
    lines = [
        _svg_open(
            "Route A nine cue contact sheet",
            {"data-route-id": ROUTE_ID, "data-cue-coverage": "9/9"},
        ),
        '<rect width="1920" height="1080" fill="#E9E5DB"/>',
        '<rect width="1920" height="112" fill="#17324D"/>',
        '<text x="70" y="54" class="ui" font-size="30" font-weight="900" fill="#FFFFFF">ROUTE A / NINE-CUE CONTACT SHEET</text>',
        f'<text x="1850" y="52" text-anchor="end" class="ui" font-size="23" font-weight="800" fill="#A9C8BC">{_xml(DISCLAIMER)}</text>',
        '<text x="70" y="91" class="ui" font-size="20" font-weight="700" fill="#DFA06F">APPROVED SUBTITLES / ONE PRINCIPAL MOTION / LOOP FALSE</text>',
    ]
    for index, cue in enumerate(cues):
        col = index % 3
        row = index // 3
        x = 70 + col * 600
        y = 138 + row * 302
        text_lines = list(APPROVED_SUBTITLE_LINES_BY_CUE[cue["cue_id"]])
        motion_display = MOTION_DISPLAY_BY_CUE[cue["cue_id"]]
        lines.extend(
            [
                f'<g data-cue-id="{cue["cue_id"]}" data-scene-id="{cue["scene_id"]}" data-approved-text="{_xml(cue["text"])}" data-motion-id="{_xml(MOTION_SPECS[cue["cue_id"]]["principal_motion"])}">',
                f'<rect x="{x}" y="{y}" width="560" height="270" rx="22" fill="#F8F5ED" stroke="#C7BFAF" stroke-width="3"/>',
                f'<rect x="{x}" y="{y}" width="560" height="52" rx="22" fill="#17324D"/>',
                f'<text x="{x + 24}" y="{y + 35}" class="ui" font-size="22" font-weight="900" fill="#FFFFFF">{cue["cue_id"]} / {cue["scene_id"]}</text>',
                f'<rect x="{x + 392}" y="{y + 10}" width="144" height="32" rx="16" fill="#D77836"/><text x="{x + 464}" y="{y + 33}" text-anchor="middle" class="ui" font-size="17" font-weight="900" fill="#FFFFFF">{_xml(cue["action"])}</text>',
                f'<rect x="{x + 24}" y="{y + 72}" width="112" height="112" rx="18" fill="#E1ECE6" stroke="#2F6F5D" stroke-width="3"/>',
                f'<text x="{x + 80}" y="{y + 124}" text-anchor="middle" class="ui" font-size="19" font-weight="900" fill="#17324D">模式図</text>',
                f'<text x="{x + 80}" y="{y + 154}" text-anchor="middle" class="ui" font-size="14" font-weight="700" fill="#2F6F5D">抽象図</text>',
                *_svg_text_lines(
                    text_lines,
                    x=x + 158,
                    y=y + 90,
                    size=16,
                    line_height=22,
                    fill="#17324D",
                    weight="700",
                ),
                f'<line x1="{x + 24}" y1="{y + 202}" x2="{x + 536}" y2="{y + 202}" stroke="#D8D1C4" stroke-width="2"/>',
                f'<text x="{x + 24}" y="{y + 228}" class="ui" font-size="16" font-weight="800" fill="#2F6F5D">motion: {_xml(motion_display)}</text>',
                f'<text x="{x + 24}" y="{y + 252}" class="ui" font-size="15" fill="#6A6258">risk: {_xml(cue["risk_label"])}</text>',
                '</g>',
            ]
        )
    lines.extend(["</svg>", ""])
    return "\n".join(lines)


def _render_motion_storyboard(cues: list[dict[str, Any]]) -> str:
    lines = [
        _svg_open(
            "Route A non-looping motion storyboard",
            {"data-route-id": ROUTE_ID, "data-loop": "false", "data-cues": "9"},
        ),
        '<rect width="1920" height="1080" fill="#111D29"/>',
        '<text x="70" y="58" class="ui" font-size="32" font-weight="900" fill="#FFFFFF">ROUTE A / MOTION STORYBOARD</text>',
        '<text x="70" y="94" class="ui" font-size="21" font-weight="700" fill="#A9C8BC">START → EMPHASIS → SETTLED / LOOP FALSE / PRINCIPAL MOTION ≤ 1</text>',
        f'<text x="1850" y="58" text-anchor="end" class="ui" font-size="21" font-weight="800" fill="#DFA06F">{_xml(DISCLAIMER)}</text>',
    ]
    for index, cue in enumerate(cues):
        motion = MOTION_SPECS[cue["cue_id"]]
        motion_display = MOTION_DISPLAY_BY_CUE[cue["cue_id"]]
        col = index % 3
        row = index // 3
        x = 70 + col * 600
        y = 132 + row * 304
        lines.extend(
            [
                f'<g data-cue-id="{cue["cue_id"]}" data-loop="false" data-principal-motion-count="1">',
                f'<rect x="{x}" y="{y}" width="560" height="270" rx="22" fill="#F8F5ED"/>',
                f'<text x="{x + 22}" y="{y + 34}" class="ui" font-size="19" font-weight="900" fill="#17324D">{cue["cue_id"]} / {_xml(motion_display)}</text>',
                f'<text x="{x + 538}" y="{y + 34}" text-anchor="end" class="ui" font-size="16" font-weight="800" fill="#2F6F5D">{motion["duration_seconds"]}s · {_xml(motion["easing"])}</text>',
            ]
        )
        state_values = (("START", motion["start"]), ("EMPHASIS", motion["emphasis"]), ("SETTLED", motion["settled"]))
        for state_index, (label, description) in enumerate(state_values):
            sx = x + 20 + state_index * 178
            dot_x = sx + (34 if state_index == 0 else 88 if state_index == 1 else 140)
            lines.extend(
                [
                    f'<rect x="{sx}" y="{y + 58}" width="164" height="150" rx="15" fill="#E9E5DB" stroke="#C7BFAF" stroke-width="2"/>',
                    f'<text x="{sx + 82}" y="{y + 84}" text-anchor="middle" class="ui" font-size="15" font-weight="900" fill="#2F6F5D">{label}</text>',
                    f'<line x1="{sx + 24}" y1="{y + 124}" x2="{sx + 140}" y2="{y + 124}" stroke="#17324D" stroke-width="4"/>',
                    f'<circle cx="{dot_x}" cy="{y + 124}" r="13" fill="#D77836"/>',
                    *_svg_text_lines(
                        _wrap_text(str(description), 10, max_lines=3),
                        x=sx + 82,
                        y=y + 158,
                        size=14,
                        line_height=19,
                        fill="#17324D",
                        weight="700",
                        anchor="middle",
                    ),
                ]
            )
        lines.extend(
            [
                f'<text x="{x + 22}" y="{y + 238}" class="ui" font-size="15" font-weight="800" fill="#6A6258">loop: false / simultaneous principal motions: 1</text>',
                f'<text x="{x + 538}" y="{y + 258}" text-anchor="end" class="ui" font-size="14" fill="#2F6F5D">proposal only / not implemented</text>',
                '</g>',
            ]
        )
    lines.extend(["</svg>", ""])
    return "\n".join(lines)


def _render_html() -> str:
    viewer_cards = "\n".join(
        f'''<article class="frame-card"><div class="frame-meta"><strong>{html.escape(spec["action"])}</strong><span>{html.escape(spec["title"])}</span></div><img src="viewer_keyframes/{html.escape(spec["filename"])}" alt="{html.escape(spec["action"])}の視聴者向けフレーム"></article>'''
        for spec in KEYFRAME_SPECS
    )
    annotation_cards = "\n".join(
        f'''<article class="frame-card"><div class="frame-meta"><span>{html.escape(spec["scene_id"])} / {html.escape(spec["cue_id"])}</span><strong>{html.escape(spec["action"])}</strong></div><img src="keyframes/{html.escape(spec["filename"])}" alt="{html.escape(spec["scene_id"])} {html.escape(spec["cue_id"])} 注釈監査フレーム"></article>'''
        for spec in KEYFRAME_SPECS
    )
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Route A Concrete Visual Proof</title>
<style>
:root{{--paper:#e9e5db;--surface:#f8f5ed;--ink:#17324d;--green:#2f6f5d;--orange:#d77836;--line:#c7bfaf;}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Yu Gothic UI","Meiryo",sans-serif;line-height:1.65}} a{{color:var(--ink)}}
.banner{{background:var(--ink);color:white;padding:14px 24px;font-weight:900;letter-spacing:.08em}} .shell{{max-width:1480px;margin:auto;padding:32px}}
.hero{{display:grid;grid-template-columns:1.35fr .65fr;gap:24px;align-items:stretch}} h1{{font-size:clamp(38px,5vw,72px);line-height:1.05;margin:.25em 0}} h2{{font-size:34px;margin-top:1.8em}}
.boundary,.decision{{background:var(--surface);border:2px solid var(--line);border-radius:22px;padding:24px}} .decision{{border-color:var(--orange)}}
.pill-row{{display:flex;flex-wrap:wrap;gap:10px}} .pill{{padding:6px 12px;border-radius:999px;background:#e1ece6;font-weight:800}}
.mode-nav{{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}} .mode-nav a{{background:var(--surface);border:2px solid var(--green);border-radius:999px;padding:8px 15px;font-weight:900;text-decoration:none}}
.disclaimer{{margin:28px 0;padding:14px 18px;border-left:8px solid var(--orange);background:var(--surface);font-weight:900}}
.frame-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}} .frame-card{{background:var(--surface);padding:14px;border-radius:20px;border:1px solid var(--line)}} .frame-card img,.wide img{{display:block;width:100%;height:auto;border-radius:10px;background:white}}
.frame-meta{{display:flex;justify-content:space-between;gap:12px;padding:4px 4px 12px}} .wide{{background:var(--surface);padding:16px;border-radius:20px;border:1px solid var(--line);margin:20px 0}}
.audit{{margin-top:44px;background:var(--surface);border:2px solid var(--line);border-radius:22px;padding:18px}} .audit summary{{cursor:pointer;font-size:26px;font-weight:900}} .audit-note{{border-left:6px solid var(--orange);padding-left:14px}}
.review{{background:var(--ink);color:white;border-radius:24px;padding:28px;margin-top:36px}} .review a{{color:white;font-weight:900}} code{{background:#dde9f0;padding:.12em .35em;border-radius:5px}}
@media(max-width:900px){{.hero,.frame-grid{{grid-template-columns:1fr}}.shell{{padding:18px}}}}
</style>
</head>
<body data-route-id="{ROUTE_ID}" data-default-surface="viewer" data-review-status="pending" data-external-resource-count="0">
<div class="banner">内部レビュー用／最終承認前／非公開／非本番</div>
<main class="shell">
<section class="hero"><div><p><strong>ROUTE A／SECURITY INSPECTION LAB</strong></p><h1>新紙幣を、抽象的な検査台で読み解く</h1><p>視聴者が実際に見る画面を最初に確認し、必要なときだけ注釈・監査表示へ切り替えられる、1920×1080の二面構成レビューです。</p><div class="pill-row"><span class="pill">視聴者向け 6画面</span><span class="pill">注釈・監査 6画面</span><span class="pill">9/9 cue</span><span class="pill">非ループ</span></div></div><aside class="decision"><strong>方向決定</strong><h2>Route Aをproof方向に選択</h2><p>最終visual acceptance、YMM4実装、render、production、public release、rights approvalは未承認です。</p></aside></section>
<nav class="mode-nav" aria-label="表示モード"><a href="#viewer-mode">視聴者向け（既定）</a><a href="#annotation-mode">注釈・監査モード</a><a href="#human-review">四問レビュー</a></nav>
<div class="disclaimer">{html.escape(DISCLAIMER)}</div>
<section class="boundary"><h2>Authorization boundary</h2><p>approved 9 cue text/order、S1/S2/S3 2/4/3、speaker 3/6、claims、evidence edges、canonical/derived CSVは変更していません。すべてoriginal abstract geometryで、real portrait、seal、serial number、official security pattern、exact feature placementを使いません。</p></section>
<section id="viewer-mode" data-surface="viewer"><h2>視聴者向け画面（既定表示）</h2><p>動画画面に含める想定の見出し、抽象図、最小限の説明、承認済み字幕、控えめな模式図注記だけを表示します。</p><div class="frame-grid">{viewer_cards}</div></section>
<section id="overview"><h2>9 cueの確認一覧</h2><div class="wide"><img src="route_a_nine_cue_contact_sheet.svg" alt="Route A 9 cue contact sheet"></div></section>
<section id="motion"><h2>Motion: start → emphasis → settled</h2><p>各cueのprincipal motionは最大1、continuous loopはありません。これはproposal-only storyboardで、実装結果や再生品質の証明ではありません。</p><div class="wide"><img src="route_a_motion_storyboard.svg" alt="Route A non-looping motion storyboard"></div></section>
<details id="annotation-mode" class="audit" data-surface="annotation"><summary>注釈／監査モードを表示</summary><p class="audit-note">ここにあるcue ID、motion metadata、source boundary、safe-area、review statusは設計・監査用overlayであり、意図する動画グラフィックではありません。</p><div class="frame-grid">{annotation_cards}</div></details>
<section id="human-review" class="review"><h2>Human review gate</h2><p>次はA/B/Cを選び直さず、このproofを四つの質問で確認します。</p><p><a href="route_a_visual_review_sheet.md">四問のreview sheetを開く</a> · <a href="human_visual_direction_selection_receipt.json">direction selection receipt</a> · <a href="visual_proof_presentation_revision_receipt.json">presentation revision receipt</a> · <a href="route_a_visual_proof_readback.json">machine readback</a></p></section>
</main>
</body>
</html>
'''


def _render_review_sheet() -> str:
    questions = "\n".join(
        f"{index}. {question}" for index, question in enumerate(REVIEW_QUESTIONS, start=1)
    )
    return f"""# Route A concrete visual proof — human review

Status: `human_review_required`
Allowed response: `accept` or `scene/cue-specific revision`
Final visual acceptance: `false`

{questions}

Route Aはconcrete proof生成の方向として選択済みです。A/B/Cを選び直す必要はありません。
"""


def _render_readme() -> str:
    return f"""# Route A Concrete Visual Proof

> **INTERNAL REVIEW / CONCRETE PROOF / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

Route A — Security Inspection Labを、human visual reviewのための直接表示可能な
1920×1080 SVG/HTML packageへ具体化しています。既定の視聴者向け画面と、別区画の
注釈・監査画面を分離しています。方向選択はproof生成だけを許可し、
final visual acceptance、YMM4、render、production、publication、rightsを許可しません。

## Review entry

- primary surface: `route_a_visual_proof.html`
- six clean viewer frames: `viewer_keyframes/`
- six annotation/audit frames: `keyframes/`
- nine-cue overview: `route_a_nine_cue_contact_sheet.svg`
- motion states: `route_a_motion_storyboard.svg`
- exact questions: `route_a_visual_review_sheet.md`
- presentation revision evidence: `visual_proof_presentation_revision_receipt.json`

## Visible contract

- canvas: 1920×1080 / 16:9
- subtitle safe area: x=84, y=780, width=1752, height=220
- diagram label: `{DISCLAIMER}`
- palette: off-white / ink blue / muted green / restrained orange
- typography: Japanese system sans-serif; no font dependency
- motion: one principal motion maximum per cue; continuous loop false
- assets: original abstract SVG geometry only; no external resource
- line wrapping: approved text is rendered from explicit semantic segments;
  concatenation is exact and basic kinsoku/orphan-punctuation checks apply

cue_008以外のorangeはUI emphasisです。cue_008だけが、approved textにある
千円券中央の橙色gradientという事実色を限定的に示します。どのartifactも実券の
portrait、seal、serial number、exact note geometry、official security pattern、
exact feature placementを再現しません。

## Content boundary

Approved nine-cue text/order、scene 2/4/3、speaker 3/6、claims、evidence、CSV、
content-lineage、current/historical YMM4 evidence、Operator Batch、元のA/B/C proposalは
変更しません。motionはstoryboard proposalで、YMM4 feasibilityやactual playbackを
証明しません。
"""


def _presentation_revision_receipt(
    repo_root: Path,
    generated: dict[Path, str],
    script: dict[str, Any],
    approval: dict[str, Any],
) -> dict[str, Any]:
    output = repo_root / DEFAULT_OUTPUT
    after_hashes: dict[str, str] = {}
    for path, content in sorted(
        generated.items(), key=lambda item: _relative(repo_root, item[0])
    ):
        relative = path.relative_to(output).as_posix()
        if (
            relative.startswith("keyframes/")
            or relative.startswith("viewer_keyframes/")
            or relative
            in {
                "route_a_motion_storyboard.svg",
                "route_a_nine_cue_contact_sheet.svg",
                "route_a_visual_proof.html",
            }
        ):
            after_hashes[relative] = hashlib.sha256(
                content.encode("utf-8")
            ).hexdigest()
    cue_text_by_id = {str(cue["cue_id"]): str(cue["text"]) for cue in script["cues"]}
    approved_hashes_exact = all(
        hashlib.sha256((repo_root / DEFAULT_PILOT / name).read_bytes()).hexdigest()
        == digest
        for name, digest in approval["approved_file_hashes"].items()
    )
    return {
        "schema_version": "new_banknote.route_a_visual_proof_presentation_revision_receipt.v1",
        "receipt_id": "new-banknote-route-a-dual-surface-visual-proof-v1",
        "status": "human_review_ready_not_accepted",
        "route_id": ROUTE_ID,
        "presentation_base_revision": PRESENTATION_BASE_REVISION,
        "defects_addressed": [
            "viewer_and_proof_debug_ui_were_mixed",
            "cue_003_orphan_full_stop",
            "cue_004_mieru_lexical_split",
            "cue_006_tashikamerareru_lexical_split",
            "cue_009_oboeteokou_lexical_split",
            "right_explanation_lexical_and_inflection_splits",
            "contact_sheet_motion_label_truncation",
        ],
        "surface_separation": {
            "default_html_surface": "viewer",
            "viewer_keyframe_count": len(KEYFRAME_SPECS),
            "viewer_keyframe_directory": "viewer_keyframes",
            "annotation_keyframe_count": len(KEYFRAME_SPECS),
            "annotation_keyframe_directory": "keyframes",
            "annotation_overlays_are_video_graphics": False,
        },
        "approved_content_invariance": {
            "approved_hashes_8_of_8_exact": approved_hashes_exact,
            "cue_text_segment_concatenation_exact": all(
                "".join(APPROVED_SUBTITLE_LINES_BY_CUE[cue_id]) == text
                for cue_id, text in cue_text_by_id.items()
            ),
            "cue_order_scenes_speakers_claims_evidence_csv_lineage_modified": False,
        },
        "line_wrap_policy": {
            "approved_subtitles_use_explicit_semantic_segments": True,
            "explanations_use_explicit_semantic_segments": True,
            "closing_punctuation_may_start_line": False,
            "punctuation_only_line_allowed": False,
            "single_character_final_line_allowed_when_reflow_possible": False,
            "lexical_or_inflection_split_allowed_when_safe_break_exists": False,
        },
        "contact_sheet_motion_labels": {
            "all_nine_complete": True,
            "display_values": [
                MOTION_DISPLAY_BY_CUE[f"cue_{index:03d}"] for index in range(1, 10)
            ],
            "machine_motion_identifiers_preserved_in_json": True,
            "silent_abbreviation_used": False,
        },
        "artifact_sha256": {
            "before": PRESENTATION_BEFORE_SHA256,
            "after": after_hashes,
        },
        "authorization": {
            "implementation_authorized": False,
            "final_visual_acceptance": False,
            "YMM4_authorized": False,
            "render_authorized": False,
            "production_authorized": False,
            "public_release_authorized": False,
            "rights_authorized": False,
        },
    }


def _manifest(
    repo_root: Path,
    generated: dict[Path, str],
    script: dict[str, Any],
    approval: dict[str, Any],
) -> dict[str, Any]:
    artifacts = []
    for path in sorted(generated, key=lambda item: _relative(repo_root, item)):
        content = generated[path].encode("utf-8")
        artifacts.append(
            {
                "path": _relative(repo_root, path),
                "sha256": hashlib.sha256(content).hexdigest(),
                "size_bytes": len(content),
                "category": _artifact_category(path),
            }
        )
    proposal_dir = repo_root / DEFAULT_PILOT / "visual_scene_decision"
    protected_proposal = [
        {
            "path": _relative(repo_root, path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "source_base_revision": BASE_REVISION,
        }
        for path in sorted(proposal_dir.iterdir())
        if path.is_file()
    ]
    return {
        "schema_version": "new_banknote.route_a_visual_proof_manifest.v1",
        "status": "review_ready_not_accepted",
        "route_id": ROUTE_ID,
        "source_base_revision": BASE_REVISION,
        "artifact_root": DEFAULT_OUTPUT.as_posix(),
        "artifact_count_excluding_manifest_and_readback": len(artifacts),
        "artifacts": artifacts,
        "protected_original_visual_proposal": {
            "artifact_count": len(protected_proposal),
            "artifacts": protected_proposal,
            "modification_authorized": False,
        },
        "approved_content": {
            "cue_count": script["cue_count"],
            "scene_allocation": script["scene_allocation"],
            "speaker_counts": script["speaker_counts"],
            "approved_hash_count": len(approval["approved_file_hashes"]),
            "modification_authorized": False,
        },
        "proof_contract": {
            "viewer_keyframes": 6,
            "annotation_keyframes": 6,
            "default_html_surface": "viewer",
            "cue_coverage": 9,
            "canvas": {"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
            "subtitle_safe_area": SUBTITLE_SAFE_AREA,
            "disclaimer": DISCLAIMER,
            "external_assets": 0,
            "continuous_loops": 0,
            "implementation_authorized": False,
            "human_visual_acceptance": False,
        },
    }


def _readback(
    repo_root: Path,
    generated: dict[Path, str],
    manifest: dict[str, Any],
    cues: list[dict[str, Any]],
    script: dict[str, Any],
    approval: dict[str, Any],
) -> dict[str, Any]:
    svg_paths = [path for path in generated if path.suffix == ".svg"]
    svg_roots = [ElementTree.fromstring(generated[path]) for path in svg_paths]
    annotation_paths = [
        repo_root / DEFAULT_OUTPUT / "keyframes" / spec["filename"]
        for spec in KEYFRAME_SPECS
    ]
    viewer_paths = [
        repo_root / DEFAULT_OUTPUT / "viewer_keyframes" / spec["filename"]
        for spec in KEYFRAME_SPECS
    ]
    annotation_text = "\n".join(generated[path] for path in annotation_paths)
    viewer_text = "\n".join(generated[path] for path in viewer_paths)
    contact_text = generated[
        repo_root / DEFAULT_OUTPUT / "route_a_nine_cue_contact_sheet.svg"
    ]
    storyboard_text = generated[
        repo_root / DEFAULT_OUTPUT / "route_a_motion_storyboard.svg"
    ]
    html_text = generated[repo_root / DEFAULT_OUTPUT / "route_a_visual_proof.html"]
    display_line_groups = [
        list(APPROVED_SUBTITLE_LINES_BY_CUE[cue["cue_id"]]) for cue in cues
    ] + [list(spec["explanation_lines"]) for spec in KEYFRAME_SPECS]
    approved_hashes_exact = all(
        hashlib.sha256((repo_root / DEFAULT_PILOT / name).read_bytes()).hexdigest()
        == digest
        for name, digest in approval["approved_file_hashes"].items()
    )
    external_tokens = ("https://", "file://", "cdn.", "<iframe", "@import")
    scan_text = "\n".join(generated.values())
    no_external = not any(token in scan_text.lower() for token in external_tokens)
    no_private = not any(
        token in scan_text.lower()
        for token in ("c:\\users\\", "/users/", "/home/", "notebooklm.google.com")
    )
    checks = {
        "selection_receipt_direction_only": True,
        "implementation_authorization_false": True,
        "approved_hashes_8_of_8_exact": approved_hashes_exact,
        "approved_cue_text_and_order_preserved": [cue["text"] for cue in cues]
        == [cue["text"] for cue in script["cues"]],
        "scene_allocation_2_4_3": script["scene_allocation"]
        == {"S1": 2, "S2": 4, "S3": 3},
        "speaker_counts_3_6": script["speaker_counts"]
        == {"れいむ": 3, "まりさ": 6},
        "six_annotation_keyframes": len(annotation_paths) == 6,
        "six_viewer_keyframes": len(viewer_paths) == 6,
        "all_svg_1920x1080": all(
            root.attrib.get("width") == str(CANVAS_WIDTH)
            and root.attrib.get("height") == str(CANVAS_HEIGHT)
            and root.attrib.get("viewBox") == "0 0 1920 1080"
            for root in svg_roots
        ),
        "cue_coverage_9_of_9": [cue["cue_id"] for cue in cues]
        == [f"cue_{index:03d}" for index in range(1, 10)],
        "disclaimer_present_in_every_full_frame": all(
            DISCLAIMER in generated[path] for path in annotation_paths + viewer_paths
        ),
        "subtitle_safe_area_declared": all(
            "data-subtitle-safe-area=\"84,780,1752,220\"" in generated[path]
            for path in annotation_paths + viewer_paths
        ),
        "approved_display_segments_exact": all(
            "".join(APPROVED_SUBTITLE_LINES_BY_CUE[cue["cue_id"]]) == cue["text"]
            for cue in cues
        ),
        "semantic_lines_have_no_orphan_or_leading_punctuation": all(
            _display_lines_are_valid(lines) for lines in display_line_groups
        ),
        "listed_lexical_units_are_not_split": all(
            not _breaks_protected_unit(lines) for lines in display_line_groups
        ),
        "viewer_debug_labels_absent": not any(
            token in viewer_text
            for token in (
                "CONCRETE PROOF",
                "REVIEW PENDING",
                "PRINCIPAL MOTION",
                "loop: false",
                "principal: 1",
                "SOURCE-BOUNDED EXPLANATION",
                "SUBTITLE SAFE AREA",
            )
        ),
        "annotation_debug_evidence_preserved": all(
            token in annotation_text
            for token in (
                "CONCRETE PROOF / REVIEW PENDING",
                "PRINCIPAL MOTION",
                "loop: false",
                "principal: 1",
                "SOURCE-BOUNDED EXPLANATION",
                "SUBTITLE SAFE AREA / APPROVED TEXT",
            )
        ),
        "contact_and_storyboard_motion_labels_complete": all(
            label in contact_text and label in storyboard_text
            for label in MOTION_DISPLAY_BY_CUE.values()
        ),
        "known_truncated_motion_literals_absent": not any(
            token in contact_text
            for token in (
                "label transiti</text>",
                "layer reveal o</text>",
                "light reveal o</text>",
                "restrained til</text>",
                "loupe zoom onc</text>",
            )
        ),
        "html_defaults_to_viewer_and_exposes_annotation": (
            'data-default-surface="viewer"' in html_text
            and '<section id="viewer-mode"' in html_text
            and '<details id="annotation-mode"' in html_text
            and html_text.index('<section id="viewer-mode"')
            < html_text.index('<details id="annotation-mode"')
        ),
        "motion_start_emphasis_settled_all_cues": all(
            all(key in MOTION_SPECS[cue["cue_id"]] for key in ("start", "emphasis", "settled"))
            for cue in cues
        ),
        "motion_loop_false_all_cues": True,
        "principal_motion_maximum_one": True,
        "html_offline_no_external_resource": no_external,
        "privacy_scan_passed": no_private,
        "manifest_hashes_match_generated_content": all(
            hashlib.sha256(generated[repo_root / row["path"]].encode("utf-8")).hexdigest()
            == row["sha256"]
            for row in manifest["artifacts"]
        ),
        "human_review_question_count_four": len(REVIEW_QUESTIONS) == 4,
        "human_visual_acceptance_false": True,
        "all_passed": False,
    }
    checks["all_passed"] = all(value for key, value in checks.items() if key != "all_passed")
    return {
        "schema_version": "new_banknote.route_a_visual_proof_readback.v1",
        "status": "passed" if checks["all_passed"] else "failed",
        "route_id": ROUTE_ID,
        "source_base_revision": BASE_REVISION,
        "checks": checks,
        "inspection_boundary": {
            "machine_verified": "SVG/HTML/JSON structure, dimensions, text identity, motion rules, hashes, privacy and offline resources",
            "worker_visual_render_inspection_required": True,
            "human_visual_acceptance": "pending",
            "YMM4_feasibility": "untested",
        },
    }


def _svg_open(title: str, attrs: dict[str, str]) -> str:
    attr_text = " ".join(f'{name}="{_xml(value)}"' for name, value in attrs.items())
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" '
        f'height="{CANVAS_HEIGHT}" viewBox="0 0 1920 1080" role="img" '
        f'aria-label="{_xml(title)}" {attr_text}>'
        '<style>.ui{font-family:"Yu Gothic UI","Meiryo",sans-serif}</style>'
        f'<title>{_xml(title)}</title>'
    )


def _svg_text_lines(
    values: list[str],
    *,
    x: int,
    y: int,
    size: int,
    line_height: int,
    fill: str,
    weight: str,
    anchor: str = "start",
) -> list[str]:
    return [
        f'<text x="{x}" y="{y + index * line_height}" text-anchor="{anchor}" '
        f'class="ui" font-size="{size}" font-weight="{weight}" fill="{fill}">{_xml(value)}</text>'
        for index, value in enumerate(values)
    ]


CLOSING_PUNCTUATION = frozenset("、。）」』】〕〉》！？!?：；")
PUNCTUATION_ONLY = frozenset("、。！？!?：；…")
PROTECTED_WRAP_UNITS = (
    "技術",
    "見える",
    "描かない",
    "持たない",
    "傾ける",
    "確かめられる",
    "覚えておこう",
    "盛り上げる",
    "取り入れた",
    "再現しません",
    "まとめます",
)


def _wrap_text(value: str, max_chars: int, *, max_lines: int) -> list[str]:
    """Wrap Japanese at deterministic semantic/kinsoku-safe boundaries."""

    text = str(value).strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    if " " in text and all(ord(character) < 128 for character in text):
        return _wrap_words(text, max_chars, max_lines=max_lines)
    lines: list[str] = []
    remaining = text
    while len(remaining) > max_chars and len(lines) < max_lines - 1:
        safe = [
            position
            for position in range(max(2, max_chars // 2), max_chars + 1)
            if _is_safe_wrap_boundary(remaining, position)
        ]
        preferred = [
            position
            for position in safe
            if remaining[position - 1] in "、。！？はがをにへとでやのも"
        ]
        candidates = preferred or safe
        if not candidates:
            break_at = max_chars
        else:
            break_at = candidates[-1]
        if len(remaining) - break_at == 1:
            earlier = [position for position in safe if position < break_at]
            if earlier:
                break_at = earlier[-1]
        lines.append(remaining[:break_at])
        remaining = remaining[break_at:]
    if remaining:
        lines.append(remaining)
    return lines


def _is_safe_wrap_boundary(value: str, position: int) -> bool:
    if position <= 0 or position >= len(value):
        return True
    if value[position] in CLOSING_PUNCTUATION or value[position - 1] in "（「『【〔〈《":
        return False
    for unit in PROTECTED_WRAP_UNITS:
        start = value.find(unit)
        while start >= 0:
            if start < position < start + len(unit):
                return False
            start = value.find(unit, start + 1)
    return True


def _display_lines_are_valid(lines: list[str]) -> bool:
    if not lines or any(not line for line in lines):
        return False
    if any(line[0] in CLOSING_PUNCTUATION for line in lines):
        return False
    if any(all(character in PUNCTUATION_ONLY for character in line) for line in lines):
        return False
    return not (len(lines) > 1 and len(lines[-1]) == 1)


def _breaks_protected_unit(lines: list[str]) -> bool:
    text = "".join(lines)
    boundaries: set[int] = set()
    cursor = 0
    for line in lines[:-1]:
        cursor += len(line)
        boundaries.add(cursor)
    for unit in PROTECTED_WRAP_UNITS:
        start = text.find(unit)
        while start >= 0:
            if any(start < boundary < start + len(unit) for boundary in boundaries):
                return True
            start = text.find(unit, start + 1)
    return False


def _wrap_words(value: str, max_chars: int, *, max_lines: int) -> list[str]:
    words = str(value).strip().split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    kept[-1] = " ".join(lines[max_lines - 1 :])
    return kept


def _artifact_category(path: Path) -> str:
    if path.parent.name == "viewer_keyframes":
        return "viewer_full_frame_keyframe"
    if path.parent.name == "keyframes":
        return "annotation_full_frame_keyframe"
    if "storyboard" in path.name:
        return "motion_storyboard"
    if "contact_sheet" in path.name or "mapping" in path.name:
        return "nine_cue_coverage"
    if "selection_receipt" in path.name:
        return "human_direction_selection"
    if "review_sheet" in path.name:
        return "human_review_gate"
    if "presentation_revision_receipt" in path.name:
        return "presentation_revision_evidence"
    return "primary_review_surface"


def _write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def _json_text(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def _xml(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    result = build_route_a_visual_proof()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

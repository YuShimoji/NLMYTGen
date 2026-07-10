from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from io import StringIO
from types import ModuleType

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_guardrails() -> ModuleType:
    path = REPO_ROOT / ".claude" / "hooks" / "guardrails.py"
    spec = importlib.util.spec_from_file_location("guardrails_for_test", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_guardrails_reject_bare_file_placement_handoff() -> None:
    guardrails = _load_guardrails()
    text = (
        "Required Operator Action\n\n"
        "置く: C:\\repo\\_tmp\\episode_runs\\pilot\\csv\\pilot.txt\n"
        "置く: C:\\repo\\_tmp\\episode_runs\\pilot\\ir\\pilot_production_ir.json\n"
    )

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "ambiguous file placement handoff" in result


def test_guardrails_allow_explained_file_placement_handoff() -> None:
    guardrails = _load_guardrails()
    text = """
Required Operator Action

- source script: C:\\repo\\_tmp\\episode_runs\\pilot\\csv\\pilot.txt
  what: UTF-8 plain text source script.
  create: Save the final refined script before Build CSV.
  used by: GUI CSV tab / Build CSV.
- Production IR: C:\\repo\\_tmp\\episode_runs\\pilot\\ir\\pilot_production_ir.json
  what: 演出IR JSON.
  create: Save the S-6 output or GUI paste-save it.
  used by: Validate IR / Dry Run / Apply Production.
- base .ymmp: C:\\repo\\_tmp\\episode_runs\\pilot\\ymmp\\pilot_base.ymmp
  what: YMM4 base project after CSV import.
  create: Build CSV, import CSV in YMM4, then Save As this file.
  used by: Production .ymmp input.
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_ignore_stop_hook_metadata_paths() -> None:
    guardrails = _load_guardrails()
    payload = {
        "hook_event_name": "Stop",
        "cwd": str(REPO_ROOT),
        "transcript_path": (
            "C:\\Users\\thank\\.claude\\projects\\"
            "-Users-thank-Storage-Media-Contents-Projects-NLMYTGen\\session.jsonl"
        ),
        "assistant_response": "待機中。",
    }

    strings = guardrails._collect_strings(payload)

    assert payload["transcript_path"] not in strings
    assert guardrails._contains_forbidden_path(strings) is None
    assert guardrails._check_stop_content(strings) is None


def test_guardrails_main_writes_advisory_to_stderr_by_default(monkeypatch, capsys) -> None:
    guardrails = _load_guardrails()
    payload = json.dumps(
        {"event": "Stop", "assistant_response": "判断をお願いします"},
        ensure_ascii=False,
    )
    monkeypatch.delenv("NLMYTGEN_GUARDRAILS_STRICT", raising=False)
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO(payload))

    result = guardrails.main()

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out == ""
    assert "Guardrails advisory:" in captured.err
    assert "broad question / user-punt phrase detected" in captured.err


@pytest.mark.parametrize("strict_value", ["1", "true", "yes", "on"])
def test_guardrails_main_strict_mode_rejects_quality_findings(
    monkeypatch, capsys, strict_value
) -> None:
    guardrails = _load_guardrails()
    payload = json.dumps(
        {"event": "Stop", "assistant_response": "判断をお願いします"},
        ensure_ascii=False,
    )
    monkeypatch.setenv("NLMYTGEN_GUARDRAILS_STRICT", strict_value)
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO(payload))

    result = guardrails.main()

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "Guardrails rejected assistant output:" in captured.err
    assert "broad question / user-punt phrase detected" in captured.err


def test_guardrails_main_keeps_repo_external_scope_as_hard_rejection(
    monkeypatch, capsys
) -> None:
    guardrails = _load_guardrails()
    payload = json.dumps(
        {
            "event": "Stop",
            "assistant_response": "C:\\Users\\example\\holosync\\handoff.md を確認します。",
        },
        ensure_ascii=False,
    )
    monkeypatch.delenv("NLMYTGEN_GUARDRAILS_STRICT", raising=False)
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO(payload))

    result = guardrails.main()

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "repo-external reference without explicit cross-project scope" in captured.err


def test_guardrails_main_allows_wait_text_with_hook_metadata(monkeypatch, capsys) -> None:
    guardrails = _load_guardrails()
    payload = json.dumps(
        {
            "hook_event_name": "Stop",
            "cwd": str(REPO_ROOT),
            "transcript_path": (
                "C:\\Users\\thank\\.claude\\projects\\"
                "-Users-thank-Storage-Media-Contents-Projects-NLMYTGen\\session.jsonl"
            ),
            "assistant_response": "待機中。",
        },
        ensure_ascii=False,
    )
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO(payload))

    result = guardrails.main()

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out == ""
    assert captured.err == ""


def test_guardrails_reject_underexplained_new_script_request() -> None:
    guardrails = _load_guardrails()
    text = "新しい台本を用意してください。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "underexplained new-script request" in result


def test_guardrails_allow_explained_existing_script_policy() -> None:
    guardrails = _load_guardrails()
    text = """
source script:
  新しい台本が必要か: 既存完成台本があれば新規作成不要。
  what: この動画で喋らせる完成会話台本。台本本文でありIRではない。
  format: UTF-8 .txt。話者名付きで、れいむ：... / まりさ：...。
  why: CSV、Production IR row-range、YMM4 base、manifest を同じ台本に結びつけるため。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_closeout_log_without_next_bridge() -> None:
    guardrails = _load_guardrails()
    text = """
検証はすべて pass です。
未追跡は正式追加対象の e2e/daily-writing-proof.spec.js です。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "closeout log" in result


def test_guardrails_allow_closeout_with_next_bridge() -> None:
    guardrails = _load_guardrails()
    text = """
検証はすべて pass です。
未追跡は正式追加対象の e2e/daily-writing-proof.spec.js です。
次に assistant が OK なら stage/commit します。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_background_skit_as_aitenote() -> None:
    guardrails = _load_guardrails()
    text = (
        "pilot_yukkuri_theater_v1 の茶番劇は、台本の「はい」で頷き、"
        "「いや、鋭い」で飛び上がるリアクションとして配置します。"
    )

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "background skit role drift" in result


def test_guardrails_reject_background_skit_acceptance_without_scene_contract() -> None:
    guardrails = _load_guardrails()
    text = "pilot_yukkuri_theater_v1 の茶番劇を本番品質として creative acceptance 待ちにします。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "independent scene-bible contract" in result


def test_guardrails_allow_background_skit_independent_scene_contract() -> None:
    guardrails = _load_guardrails()
    text = """
pilot_yukkuri_theater_v1 の茶番劇は合いの手ではない。
語り手とは別レイヤーで並行する独立した小場面として scene bible を先に作る。
script line range: lines 1-12 自力検索、lines 13-24 REINS、lines 25-36 保護理由。
time budget / 時間配分: 自力検索10%、REINS12%、保護12%、囲い込み14%、QR10%、キュレーション17%、AI後25%。
cast continuity: 消費者、ゲートキーパー業者、キュレーター/リスク管理プロを固定する。
screen placement / 画面配置: 消費者は左、業者は右奥、キュレーターは後半中央。
block proof path: 自力検索は消費者UI、REINSはPC/扉、QRはステータス盤を gap report 化する。
proof path: scene bible -> asset gap -> registry -> readback。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_real_estate_motion_cue_sequence_only() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇:
enter_from_left -> nod -> surprise_oneshot -> deny_oneshot -> exit_left。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "motion-only explanation" in result


def test_guardrails_reject_delivery_line_cue_allowance() -> None:
    guardrails = _load_guardrails()
    text = "配達台本なら、台本行ごとの line cue が比較的成立します。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "line-cue allowance" in result


def test_guardrails_reject_scene_plan_needed_without_concrete_followup() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇は合いの手ではありません。
まだ全部までは想定できていません。
なので次に scene plan と asset matrix へ進める段階です。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "underspecified acknowledgement" in result


def test_guardrails_reject_scene_plan_without_time_budget_or_cast() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇の説明: 次に scene plan を作ります。asset matrix も作ります。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "script line ranges" in result


def test_guardrails_reject_scene_bible_missing_script_line_ranges() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DX scene bible:
time budget: 自力検索10%、REINS12%、保護12%、囲い込み14%、QR10%、キュレーション17%、AI後25%。
cast continuity: 消費者、ゲートキーパー業者、キュレーター。
screen placement: 消費者は左、業者は右奥、キュレーターは中央。
block proof path: 自力検索はUI、REINSは扉、QRは盤面を確認する。
proof path: registry / readback。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "script line ranges" in result


def test_guardrails_reject_scene_bible_missing_block_proof_paths() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DX scene bible:
script line range: lines 1-12 / lines 13-24 / lines 25-36。
time budget: 自力検索10%、REINS12%、保護12%、囲い込み14%、QR10%、キュレーション17%、AI後25%。
cast continuity: 消費者、ゲートキーパー業者、キュレーター。
screen placement: 消費者は左、業者は右奥、キュレーターは中央。
proof path: registry / readback。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "block proof paths" in result


def test_guardrails_reject_direct_ir_ymm4_overclaim() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇の設計図として、このまま演出IR・素材gap・YMM4確認に接続できる設計図です。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "direct IR/YMM4 overclaim" in result


def test_guardrails_reject_intent_template_conflation() -> None:
    guardrails = _load_guardrails()
    text = "配達台本の茶番劇 intent: delivery_enter_from_left_v1 を使います。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "intent/template conflation" in result


def test_guardrails_reject_python_only_placement_underclaim() -> None:
    guardrails = _load_guardrails()
    text = "茶番劇では Python は素材生成せず、registry / template source / IR で既存GroupItemを配置するだけです。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "adapter role underclaimed" in result


def test_guardrails_reject_ir_timetable_without_absolute_timing() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図です。
time budget: 自力検索10%、REINS12%、囲い込み14%。
density audit: sparse risk を見ます。
script diagnostic: thesis と visual anchor を確認します。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "concrete timing values" in result


def test_guardrails_reject_abstract_timetable_field_names_without_values() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇の設計図には script line range、総尺、mm:ss 開始終了、演出秒数、休ませる区間、密度監査が必要です。
いま提示できるのは scene bible レベルで、確定 IR / production timing ではありません。
不動産DXなら lines 1-12 は消費者が検索し、lines 13-24 は REINS/VIP クラブを見せます。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "concrete timing values" in result


def test_guardrails_reject_ir_timetable_without_density_audit() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図です。
total duration: 12:30。
script_source: csv/pilot_yukkuri_theater_v1.txt, line_count 150, range_basis: CSV readback。
RE-01 script line range: lines 1-12, start-end 00:00-01:15, duration sec 75。
script diagnostic: SCRIPT_THESIS_WEAK, ideal-script delta: lines 1-12 に消費者の問いを追加。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "density audit" in result


def test_guardrails_reject_ir_timetable_without_script_maturity() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図です。
total duration: 12:30。
script_source: csv/pilot_yukkuri_theater_v1.txt, line_count 150, range_basis: CSV readback。
RE-01 script line range: lines 1-12, start-end 00:00-01:15, duration sec 75。
density audit: active visual coverage 62%, unexplained empty 0 sec, longest gap 0 sec, visual states/min 3.2。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "script maturity result" in result


def test_guardrails_reject_timetable_line_ranges_without_source() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図です。
total duration: 12:30。
RE-01 script line range: lines 1-12, start-end 00:00-01:15, duration sec 75。
density audit: active visual coverage 62%, unexplained empty 0 sec, longest gap 0 sec, visual states/min 3.2。
script diagnostic: SCRIPT_THESIS_WEAK, ideal-script delta: lines 1-12 に消費者の問いを追加。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "line ranges without source" in result


def test_guardrails_reject_numeric_timetable_without_blueprint_validator() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図です。
total duration: 12:30。
script_source: csv/pilot_yukkuri_theater_v1.txt, line_count 150, range_basis: CSV readback。
RE-01 script line range: lines 1-12, start-end 00:00-01:15, duration sec 75。
density audit: active visual coverage 62%, unexplained empty 0 sec, longest gap 0 sec, visual states/min 3.2。
script diagnostic: SCRIPT_THESIS_WEAK, ideal-script delta: lines 1-12 に消費者の問いを追加。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "validated blueprint result" in result


def test_guardrails_reject_skit_design_fluff_without_estimates() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇の設計図です。
不動産DXは、ちゃんと舞台監督の香りがする図面が要るやつです。
概略としては消費者、ゲートキーパー、キュレーターでかなり進められます。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "response fluff" in result


def test_guardrails_reject_downstream_optimism_without_gates() -> None:
    guardrails = _load_guardrails()
    text = "茶番劇は下流のYMM4で見れば最終的に調整できます。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "downstream optimism" in result


def test_guardrails_reject_template_reuse_without_symbolic_role() -> None:
    guardrails = _load_guardrails()
    text = "不動産DXでは既存 template を流用します。"

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "template reuse lacks symbolic role" in result


def test_guardrails_reject_asset_need_without_matrix() -> None:
    guardrails = _load_guardrails()
    text = """
茶番劇の制作には assets are missing。
登場人物や背景はまだ未確定です。
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "asset matrix" in result


def test_guardrails_allow_background_skit_scene_bible_and_asset_matrix_next() -> None:
    guardrails = _load_guardrails()
    text = """
認識: 茶番劇は合いの手ではなく、transport/readback proof と creative acceptance は分離する。
不動産DX scene bible:
- script line range: lines 1-12 自力検索、lines 13-24 REINS、lines 25-36 保護理由、lines 37-48 囲い込み、lines 49-60 QR、lines 61-82 キュレーション、lines 83-150 AI後。
- time budget / 時間配分: 自力検索10%、REINS12%、保護12%、囲い込み14%、QR10%、キュレーション17%、AI後の人間価値25%。
- cast continuity: 消費者、ゲートキーパー業者、キュレーター/リスク管理プロを全編で固定する。
- screen placement / 画面配置: 消費者は左、ゲートキーパーは右奥、キュレーターは後半中央。
- block proof path: 自力検索は消費者UI、REINSはPC/扉、QRはステータス盤、AI後は停止カードを gap report 化する。
- proof path: scene bible -> asset gap -> registry -> readback。
配達 mini bible: setup は配達員登場、complication は誤配、reaction は伝票不一致への一拍、resolution は荷物を持って退場。
intent / template boundary: IR intent は enter_from_left、template_name は delivery_enter_from_left_v1 と分ける。
asset / proof matrix:
- 登場人物 / characters: 消費者、ゲートキーパー業者、キュレーター/リスク管理プロ、配達員。
- 配置 / placement: 消費者は背景左、業者はPC前、配達員はドア横。
- 背景 / background: 寝室、事務所、玄関。
- props / 小道具: PC、物件カード、扉、荷物。
- 既存 / existing: delivery_v1_templates.ymmp は仮案内人 proxy / 再スキン candidate。
- 不足 / missing: 不動産業者、物件カード、PC画面。
- owner / 担当: assistant-owned selection と user-owned authoring を分ける。
- proof path: registry / template source / readback。
次に scene bible + time budget + cast continuity 由来の gap report を作ります。IR/YMM4配置にはまだ進めません。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_allow_quantitative_skit_timetable_contract() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図:
total duration: 12:30, duration_source: estimated-low。
script diagnostic: SCRIPT_THESIS_WEAK と visual anchor gap を確認し、ideal-script delta を出す。
script_source: csv/pilot_yukkuri_theater_v1.txt, line_count 150, range_basis: CSV readback。
RE-01 script line range: lines 1-12, start-end 00:00-01:15, duration sec 75。
skit active: 00:10-00:38, duration sec 28, intentional rest: 00:38-01:15。
density audit: active visual coverage 62%, unexplained empty 0 sec, longest gap 0 sec, visual states/min 3.2, sparse risk ok。
validate-background-skit-blueprint validator result:
status: passed。
derived_metrics: duration.total_duration_sec=750, density.active_visual_coverage_pct=62。
asset/proof gap report と template/proxy classification を次に作り、readback 後に再計算する。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_allow_blueprint_failed_closeout_without_fake_numbers() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図はまだ IR/YMM4 production timing に進めません。
validate-background-skit-blueprint validator result:
status: failed。
errors: SCRIPT_SOURCE_MISMATCH, ASSET_CONTROL_UNBOUND。
derived_metrics: script.line_count=152。
次に background_skit_blueprint artifact を直して再検証します。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_allow_blueprint_blocked_closeout_without_fake_numbers() -> None:
    guardrails = _load_guardrails()
    text = """
不動産DXの茶番劇IR設計図はまだ IR/YMM4 production timing に進めません。
validate-background-skit-blueprint validator result:
status: blocked。
blockers: TIMETABLE_BLOCKED_TIMING_SOURCE_MISSING。
derived_metrics: script.line_count=152。
ymmp source を受け取ったら duration_model を再計算します。
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_overlay_compact_review_without_allowed_next_actions() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
next: overlay-only compact review can proceed from the placeholder map.
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "allowed_next_actions" in result


def test_guardrails_reject_overlay_compact_review_when_re07_script_blocker_remains() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: SCRIPT_BLOCKED_RE07_TOO_BROAD, ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
allowed_next_actions: [overlay_only_compact_review]
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
next: overlay-only compact review can proceed from the placeholder map.
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "SCRIPT_BLOCKED_RE07_TOO_BROAD" in result


def test_guardrails_allow_overlay_compact_review_with_validator_allowed_next_actions() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
allowed_next_actions: [overlay_only_compact_review]
forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
next: overlay-only compact review can proceed from the placeholder map.
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_generated_overlay_compact_review_without_artifact_path() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
allowed_next_actions: [overlay_only_compact_review]
forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
generated overlay-only compact review.
readback result: status blocked, errors [].
remaining blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING.
This is not creative acceptance.
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "artifact path" in result


def test_guardrails_reject_generated_overlay_compact_review_without_machine_next_keys() -> None:
    guardrails = _load_guardrails()
    text = """
完了です。blocked を崩さず、許可済みの overlay_only_compact_review だけ生成しました。

Compact review artifact: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\samples\\_probe\\g24\\real_estate_dx_overlay_only_compact_review.html:6
Readback: status=passed、11 segments / 24 placeholders / ShapeItem=24 only: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\samples\\_probe\\g24\\real_estate_dx_overlay_only_compact_review_readback.json:2
Validator allowed: [overlay_only_compact_review]: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\docs\\verification\\REAL-ESTATE-DX-BACKGROUND-SKIT-BLUEPRINT-2026-05-06.md:114
Remaining blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING, ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\docs\\verification\\REAL-ESTATE-DX-BACKGROUND-SKIT-BLUEPRINT-2026-05-06.md:117
Forbidden: [cast_motion_ir, ymm4_creative_acceptance, production_timing]: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\docs\\verification\\REAL-ESTATE-DX-BACKGROUND-SKIT-BLUEPRINT-2026-05-06.md:115
明記済み: これは creative acceptance ではありません: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\samples\\_probe\\g24\\real_estate_dx_overlay_only_compact_review.html:30
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "allowed_next_actions" in result


def test_guardrails_reject_generated_overlay_compact_review_without_literal_forbidden_key() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
allowed_next_actions: [overlay_only_compact_review]
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
generated overlay-only compact review.
artifact path: samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html
readback result: status passed, errors [].
remaining blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING.
Forbidden: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
not creative acceptance
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "forbidden_next_actions" in result


def test_guardrails_allow_generated_overlay_compact_review_literal_closeout_keys() -> None:
    guardrails = _load_guardrails()
    text = """
Closeout Keys

artifact path: C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen\\samples\\_probe\\g24\\real_estate_dx_overlay_only_compact_review.html:6
readback result: status=passed; JSON/readback contract check passed; 43 passed guardrail tests; 64 passed focused suite
allowed_next_actions: [overlay_only_compact_review]
forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
remaining blockers: [ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING, ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING]
not creative acceptance
"""

    result = guardrails._check_stop_content([text])

    assert result is None


def test_guardrails_reject_generated_overlay_compact_review_without_readback() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
allowed_next_actions: [overlay_only_compact_review]
forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
generated overlay-only compact review artifact path: samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp.
remaining blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING.
This is not creative acceptance.
"""

    result = guardrails._check_stop_content([text])

    assert result is not None
    assert "readback" in result


def test_guardrails_allow_generated_overlay_compact_review_handoff_contract() -> None:
    guardrails = _load_guardrails()
    text = """
Real estate background skit IR timetable:
validate-background-skit-blueprint validator result:
status: blocked
blockers: ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING
derived_metrics: duration.total_duration_sec=1049.533333, density.active_visual_coverage_pct=70
generated overlay-only compact review.
artifact path: samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html
readback result: status passed, 11 segments, 24 placeholder items.
allowed_next_actions: [overlay_only_compact_review]
forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]
remaining blockers: [ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING]
not creative acceptance
"""

    result = guardrails._check_stop_content([text])

    assert result is None

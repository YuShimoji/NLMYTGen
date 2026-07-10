from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = str(Path(__file__).resolve().parents[2]).lower()

HOOK_METADATA_KEYS = {
    "cwd",
    "event",
    "event_name",
    "hook_event_name",
    "model",
    "session_id",
    "stop_hook_active",
    "transcript_path",
    "type",
}

FORBIDDEN_PATTERNS = [
    re.compile(r"holosync", re.IGNORECASE),
    re.compile(r"nlmandslidevideogenerator", re.IGNORECASE),
    re.compile(r"narrativegen", re.IGNORECASE),
    re.compile(r"vastcore", re.IGNORECASE),
    re.compile(r"[\\/]\.claude[\\/]+projects[\\/]", re.IGNORECASE),
]

CROSS_PROJECT_SCOPE_PATTERNS = [
    re.compile(r"cross[- ]project", re.IGNORECASE),
    re.compile(r"他\s*repo", re.IGNORECASE),
    re.compile(r"他プロジェクト"),
    re.compile(r"別プロジェクト"),
    re.compile(r"明示範囲"),
    re.compile(r"authority cleanup", re.IGNORECASE),
]

STOP_PATTERNS = [
    re.compile(r"判断をお願いします"),
    re.compile(r"何が足りないか教えてください"),
    re.compile(r"何をすべきか教えてください"),
    re.compile(r"どこに pain があるか教えてください", re.IGNORECASE),
    re.compile(r"クローズすべき", re.IGNORECASE),
]

VISUAL_PROOF_PATTERNS = [
    re.compile(r"YMM4\s*で確認してください"),
    re.compile(r"visual\s+proof", re.IGNORECASE),
    re.compile(r"開いて確認"),
]

DOC_ROUTE_HANDOFF_PATTERNS = [
    re.compile(
        r"(?:手順の正本|手順.*正本|procedure source of truth|procedure source|source of truth)[^\n]*(?:\.md|README|manifest)(?::\d+)?",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:詳しい手順|詳細手順|手順詳細|詳細は)[^\n]*(?:\.md|README|manifest)[^\n]*(?:参照|見て|確認|従)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\.md|README|manifest)[^\n]*(?:参照|見て|確認)[^\n]*(?:入力を置く|GUI|YMM4|Build CSV|Validate IR|Apply Production)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\.md|README|manifest)[^\n]*(?:GUI|YMM4|Build CSV|Validate IR|Apply Production)[^\n]*(?:進め|操作|押|置|実行|press|run|select|open|\?{3,})",
        re.IGNORECASE,
    ),
]

AMBIGUOUS_FILE_PLACEMENT_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:置く|put|place)\s*[:：]\s*(?:[A-Za-z]:[\\/]|_tmp[\\/]|\.{0,2}[\\/]|[^\n]*(?:csv|ir|ymmp)[\\/])",
    re.IGNORECASE,
)

FILE_PLACEMENT_DETAIL_PATTERN = re.compile(
    r"(?:source script|Production IR|base\s+\.ymmp|元台本|演出IR|YMM4|Build CSV|created by|how to create|生成|作成|保存|既存|存在|missing|未存在|用途|used by|入力)",
    re.IGNORECASE,
)

NEW_SCRIPT_REQUEST_PATTERN = re.compile(
    r"(?:新しい台本(?:を)?(?:用意|作成|準備)|台本(?:を)?新規(?:作成|用意|準備)|新規[^\n。]*台本|新しい台本が必要)",
    re.IGNORECASE,
)

SCRIPT_HANDOFF_DETAIL_PATTERNS = [
    re.compile(r"(?:既存.*(?:台本|完成)|新規作成不要|新しい台本.*不要)"),
    re.compile(r"(?:完成(?:済み)?(?:会話)?台本|動画.*喋|source script|台本本文)", re.IGNORECASE),
    re.compile(r"(?:UTF-?8|話者名|れいむ|まりさ|\.txt)", re.IGNORECASE),
    re.compile(r"(?:row-range|CSV|YMM4|manifest|同じ.*台本|結びつ|ずれ)", re.IGNORECASE),
]

CLOSEOUT_LOG_WITH_UNTRACKED_PATTERN = re.compile(
    r"(?=.*(?:検証.*(?:pass|PASS)|passed|すべて\s*pass))(?=.*(?:未追跡|untracked))",
    re.IGNORECASE | re.DOTALL,
)

CLOSEOUT_NEXT_ACTION_PATTERN = re.compile(
    r"(?:次に|次の動き|返却後|受領後|OKなら|NGなら|stage|commit|ステージ|コミット|will inspect|will generate|will fix)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_CONTEXT_PATTERN = re.compile(
    r"(?:茶番劇|background\s+skit|skit_group|pilot_yukkuri_theater_v1|不動産DX|不動産屋|配達台本|delivery|overlay[-_/ ]*only[-_/ ]*compact[-_/ ]*review)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_HANDOFF_PATTERN = re.compile(
    r"(?:creative\s+acceptance|production\s+quality|確認待ち|レビューへ渡|acceptance\s+待ち|本番品質|制作品質)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_ROLE_ANCHOR_PATTERNS = [
    re.compile(r"(?:別レイヤー|parallel\s+layer)", re.IGNORECASE),
    re.compile(r"(?:独立(?:した)?(?:小場面|ストーリー|story|scene)|scene\s+bible|scene\s+plan|visual\s+situation)", re.IGNORECASE),
    re.compile(r"(?:合いの手ではない|not\s+an?\s+aitenote|not\s+a\s+reaction\s+track)", re.IGNORECASE),
    re.compile(r"(?:台本(?:行|発話|セリフ)?を(?:逐語)?理解(?:して)?反応(?:する)?(?:のではない|しない))"),
]

BACKGROUND_SKIT_REACTION_DRIFT_PATTERNS = [
    re.compile(
        r"(?:茶番劇|background\s+skit|skit_group).*?(?:合いの手|リアクション|台本(?:行|発話|セリフ)?(?:に|へ)?(?:合わせ|反応)|発話(?:ごと|行ごと))",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"(?:「?はい」?.{0,20}(?:頷|nod)|「?いや、?鋭い」?.{0,20}(?:飛び上が|jump))",
        re.IGNORECASE,
    ),
]

BACKGROUND_SKIT_NEGATION_PATTERN = re.compile(
    r"(?:合いの手では(?:ない|ありません)|not\s+an?\s+aitenote|not\s+a\s+reaction\s+track|禁止|invalid|誤り|ズレ|降格|wrong|reject|ではなく|危ない|不十分|未完|まだ進めない|進めない|渡さ(?:ない|ず)|過小化しない)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_LINE_CUE_ALLOW_PATTERN = re.compile(
    r"(?:配達|delivery).{0,80}(?:line\s*cue|台本行(?:ごと)?|発話行(?:ごと)?|行ごと\s*cue|cue).{0,80}(?:成立|許容|OK|よい|良い|使える)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_UNDERSPECIFIED_ACK_PATTERN = re.compile(
    r"(?:まだ(?:全部|全体).*?(?:想定|未確定)|(?:scene\s*plan|シーンプラン)(?:\s*が|\s*は)?必要|(?:素材|asset(?:s)?)(?:\s*が|\s*は)?必要)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_DESIGN_NEXT_PATTERN = re.compile(
    r"(?=.*(?:assistant\s+next|next\s+action|次(?:に|の)?\s*assistant|assistant\s*が|assistant-owned|設計表を作|作成へ|作ります))(?=.*(?:scene\s*bible|scene\s*plan|シーンプラン))(?=.*(?:script\s*line\s*range|台本(?:行範囲|範囲)|lines?\s+\d+))(?=.*(?:time\s*budget|時間配分))(?=.*(?:cast\s*continuity|登場人物|cast))(?=.*(?:screen\s*placement|画面配置|placement))(?=.*(?:block\s*proof\s*path|proof\s*path|検証経路))(?=.*(?:asset\s*/?\s*proof\s*matrix|asset\s*matrix|素材(?:表|matrix)|登場人物.*配置.*props|characters.*placement.*props))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_ASSET_MATRIX_PATTERN = re.compile(
    r"(?=.*(?:asset\s*/?\s*proof\s*matrix|asset\s*matrix|素材(?:表|matrix)|素材マトリクス))(?=.*(?:登場人物|characters?))(?=.*(?:配置|placement))(?=.*(?:背景|background))(?=.*(?:props?|小道具))(?=.*(?:既存|existing))(?=.*(?:不足|missing))(?=.*(?:owner|user-owned|assistant-owned|担当))(?=.*(?:proof\s*path|readback|registry|検証経路))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_SCENE_BIBLE_DETAIL_PATTERN = re.compile(
    r"(?=.*(?:scene\s*bible|scene\s*plan|シーンプラン))(?=.*(?:script\s*line\s*range|台本(?:行範囲|範囲)|lines?\s+\d+))(?=.*(?:time\s*budget|時間配分))(?=.*(?:cast\s*continuity|登場人物|cast))(?=.*(?:screen\s*placement|画面配置|placement))(?=.*(?:block\s*proof\s*path|proof\s*path|readback|registry|検証経路))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_SCRIPT_LINE_RANGE_PATTERN = re.compile(
    r"(?:script\s*line\s*range|台本(?:行範囲|範囲)|lines?\s+\d+\s*[-–〜]\s*\d+)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_BLOCK_PROOF_PATH_PATTERN = re.compile(
    r"(?:block\s*proof\s*path|各(?:block|ブロック).*proof\s*path|ブロック別.*proof\s*path|proof\s*path.*(?:自力検索|REINS|QR|キュレーション|lines?\s+\d+))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_SCENE_PLAN_OR_MATRIX_PATTERN = re.compile(
    r"(?:scene\s*plan|シーンプラン|asset\s*matrix|素材(?:表|matrix)|scene\s*bible)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_TEMPLATE_REUSE_PATTERN = re.compile(
    r"(?:既存(?:の)?\s*template\s*を\s*流用|既存(?:の)?テンプレ(?:ート)?(?:を)?流用|delivery_v1_templates\.ymmp|existing\s+template\s+reuse|template\s+reuse)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_TEMPLATE_SYMBOL_PATTERN = re.compile(
    r"(?:比喩|symbol|role|役割|誰|cast|proxy|仮|再スキン|literal\s+reuse|消費者|ゲートキーパー|キュレーター|配達員|案内人)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_MOTION_LABEL_PATTERN = re.compile(
    r"(?:enter_from_left|nod|surprise(?:_oneshot)?|deny(?:_oneshot|_shake)?|exit_left)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_DIRECT_YMM4_OVERCLAIM_PATTERN = re.compile(
    r"(?:このまま|そのまま).{0,100}(?:IR|演出IR).{0,100}(?:YMM4|creative\s+acceptance|確認).{0,100}(?:接続でき|進め|渡せ|確認)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_INTENT_TEMPLATE_CONFLATION_PATTERN = re.compile(
    r"(?:intent|既存intent|IR\s*intent)\s*(?:[:：=]|欄|列|は)?\s*`?delivery_[a-z_]+_v1`?",
    re.IGNORECASE,
)

BACKGROUND_SKIT_PYTHON_ONLY_PLACEMENT_PATTERN = re.compile(
    r"(?:Python|adapter).{0,80}(?:既存\s*GroupItem|GroupItem).{0,80}(?:配置するだけ|置くだけ)|(?:既存\s*GroupItem|GroupItem).{0,80}(?:配置するだけ|置くだけ)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_IR_TIMETABLE_CONTEXT_PATTERN = re.compile(
    r"(?:茶番劇|background\s+skit|skit_group|不動産DX|配達).{0,200}(?:演出IR|IR設計図|演出指定|時刻表|タイムライン|production\s+timing|設計図|timetable)|(?:演出IR|IR設計図|演出指定|時刻表|タイムライン|production\s+timing|設計図|timetable).{0,200}(?:茶番劇|background\s+skit|skit_group|不動産DX|配達)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_CONCRETE_TOTAL_DURATION_PATTERN = re.compile(
    r"(?:total[_ ]duration(?:_sec)?|総尺|全体尺|episode\s+duration)\s*[:：=]?\s*(?:\d{1,2}:\d{2}|\d+(?:\.\d+)?\s*(?:秒|sec|s|分))",
    re.IGNORECASE,
)

BACKGROUND_SKIT_CONCRETE_TIME_RANGE_PATTERN = re.compile(
    r"\b\d{1,2}:\d{2}\s*(?:-|–|—|~|〜|から)\s*\d{1,2}:\d{2}\b",
    re.IGNORECASE,
)

BACKGROUND_SKIT_CONCRETE_DURATION_SEC_PATTERN = re.compile(
    r"(?:duration\s*sec|skit_active_duration_sec|block_duration_sec|演出秒数|秒数)\s*[:：=]?\s*\d+(?:\.\d+)?|(?:\d+(?:\.\d+)?\s*(?:秒|sec|s)\b).{0,40}(?:演出|active|duration|visual)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_CONCRETE_DENSITY_AUDIT_PATTERN = re.compile(
    r"(?:density\s+audit|密度監査).{0,220}(?:active(?:_|\s+)visual(?:_|\s+)coverage|coverage|unexplained(?:_|\s+)empty|意図不明(?:の)?空白|longest(?:_|\s+)gap|visual(?:_|\s+)states?\s*/?\s*min).{0,80}\d+(?:\.\d+)?\s*(?:%|秒|sec|s)?",
    re.IGNORECASE,
)

BACKGROUND_SKIT_CONCRETE_SCRIPT_MATURITY_PATTERN = re.compile(
    r"(?:\bSCRIPT_(?:[A-Z]+_)*(?:WEAK|GAP|MISSING|DRIFT)\b|script\s+diagnostic\s*[:：].{0,160}(?:pass|fail|weak|gap|delta|missing|追加|削除|修正)|ideal[- ]script\s+delta\s*[:：].{0,160}(?:追加|削除|修正|missing|gap|lines?|\d+)|台本成熟度\s*[:：].{0,120}(?:pass|fail|弱い|不足|gap|SCRIPT_))",
    re.IGNORECASE,
)

BACKGROUND_SKIT_SCRIPT_RANGE_SOURCE_PATTERN = re.compile(
    r"(?:script[_ ]source|台本(?:source|ファイル|本文|出典)|source\s+script|CSV|transcript|line[_ ]count|行数|range[_ ]basis|行範囲(?:の)?根拠|readback|読み取り元)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_TIMETABLE_BLOCKED_PATTERN = re.compile(
    r"(?:TIMETABLE_BLOCKED|DURATION_BLOCKED|SCRIPT_SOURCE_MISSING|TIMING_SOURCE_MISSING|台本source未確認|総尺未確認|source\s+missing)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_RESPONSE_FLUFF_PATTERN = re.compile(
    r"(?:舞台監督の香り|ちゃんと[^\n。]{0,20}要るやつ|けっこう肝|いい感じ|それっぽく|相性が良いです|かなり進められます)",
    re.IGNORECASE,
)

BACKGROUND_SKIT_BLUEPRINT_VALIDATION_RESULT_PATTERN = re.compile(
    r"(?=.*(?:validate-background-skit-blueprint|background_skit_blueprint|blueprint\s+validator|validator\s+result|validated\s+blueprint))(?=.*status\s*[:：]\s*(?:passed|failed|blocked))(?=.*(?:derived_metrics|errors|blockers))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_ALLOWED_OVERLAY_NEXT_PATTERN = re.compile(
    r"allowed_next_actions\s*[:：]\s*\[[^\]]*overlay_only_compact_review[^\]]*\]",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_OVERLAY_COMPACT_REVIEW_ADVANCE_PATTERN = re.compile(
    r"(?:(?:overlay[-_/ ]*only[-_/ ]*compact[-_/ ]*review|overlay/card.{0,40}compact\s+review|overlay\s+card.{0,40}compact\s+review|overlay[-_/ ]*only.{0,80}compact\s+review).{0,120}(?:進め|生成|作成|continue|proceed|allowed|next)"
    r"|(?:next|次).{0,80}(?:overlay[-_/ ]*only[-_/ ]*compact[-_/ ]*review|overlay/card.{0,40}compact\s+review|overlay\s+card.{0,40}compact\s+review|overlay[-_/ ]*only.{0,80}compact\s+review))",
    re.IGNORECASE | re.DOTALL,
)


BACKGROUND_SKIT_OVERLAY_COMPACT_REVIEW_CLOSEOUT_PATTERN = re.compile(
    r"(?:(?:overlay[-_/ ]*only[-_/ ]*compact[-_/ ]*review|overlay/card.{0,40}compact\s+review|overlay\s+card.{0,40}compact\s+review|overlay[-_/ ]*only.{0,100}compact\s+review|compact\s+review\s+artifact)"
    r".{0,160}(?:generated|created|wrote|output|artifact|done|complete)"
    r"|(?:generated|created|wrote|output|artifact).{0,160}"
    r"(?:overlay[-_/ ]*only[-_/ ]*compact[-_/ ]*review|overlay/card.{0,40}compact\s+review|overlay\s+card.{0,40}compact\s+review|overlay[-_/ ]*only.{0,100}compact\s+review|compact\s+review\s+artifact))",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_COMPACT_REVIEW_ARTIFACT_PATH_PATTERN = re.compile(
    r"artifact\s+path\s*[:：].{0,160}"
    r"(?:samples[\\/]|_tmp[\\/]|[A-Za-z]:[\\/]).{0,220}"
    r"(?:\.html|\.ymmp|\.json|\.md)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_COMPACT_REVIEW_READBACK_PATTERN = re.compile(
    r"readback\s+result\s*[:：]"
    r".{0,160}(?:status|passed|blocked|failed|errors|warnings|readback|OK|PASS)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_REMAINING_BLOCKERS_PATTERN = re.compile(
    r"remaining\s+blockers\s*[:：].{0,240}"
    r"(?:ASSET_BLOCKED|CAST_BLOCKED|PROPS_MISSING|none|\[\])",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_FORBIDDEN_NEXT_PATTERN = re.compile(
    r"forbidden_next_actions\s*[:：]\s*"
    r"\[[^\]]*cast_motion_ir[^\]]*ymm4_creative_acceptance[^\]]*production_timing[^\]]*\]",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_NOT_CREATIVE_ACCEPTANCE_PATTERN = re.compile(
    r"not\s+creative\s+acceptance",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_RE07_SCRIPT_BLOCKER_PATTERN = re.compile(
    r"SCRIPT_BLOCKED_RE07_TOO_BROAD",
    re.IGNORECASE,
)

BACKGROUND_SKIT_DOWNSTREAM_OPTIMISM_PATTERN = re.compile(
    r"(?:下流|後続|あとで|いつか|YMM4で見れば|creative\s+acceptanceで).{0,80}(?:完成|調整|判断|直す|詰める|分かる)",
    re.IGNORECASE | re.DOTALL,
)

BACKGROUND_SKIT_TIMETABLE_SAFE_NEXT_PATTERN = re.compile(
    r"(?:asset/proof\s+gap|gap\s+report|template/proxy|quantitative\s+timetable|density\s+audit|script\s+diagnostic|duration_model|readback\s+後|再計算)",
    re.IGNORECASE,
)

ALLOWED_VISUAL_CONTEXT = [
    re.compile(r"初回\s*E2E"),
    re.compile(r"最終.*品質判断"),
    re.compile(r"最終制作物"),
]


def _read_payload() -> Any:
    raw = sys.stdin.read().lstrip("\ufeff")
    json_starts = [pos for pos in (raw.find("{"), raw.find("[")) if pos >= 0]
    if json_starts:
        raw = raw[min(json_starts) :]
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def _collect_strings(value: Any) -> list[str]:
    results: list[str] = []
    if isinstance(value, str):
        results.append(value)
    elif isinstance(value, dict):
        for k, v in value.items():
            if isinstance(k, str) and k in HOOK_METADATA_KEYS:
                continue
            results.extend(_collect_strings(v))
    elif isinstance(value, list):
        for item in value:
            results.extend(_collect_strings(item))
    return results


def _event_name(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for key in ("event", "event_name", "hook_event_name", "type"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _contains_forbidden_path(strings: list[str]) -> str | None:
    for text in strings:
        lowered = text.lower()
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(lowered):
                return text
        if lowered.startswith(("c:\\", "d:\\", "/")) and REPO_ROOT not in lowered:
            if any(token in lowered for token in ("media contents projects", ".claude\\projects", ".claude/projects")):
                return text
    return None


def _reject(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def _strict_mode_enabled() -> bool:
    return os.environ.get("NLMYTGEN_GUARDRAILS_STRICT", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def _has_cross_project_scope(strings: list[str]) -> bool:
    return _matches_any("\n".join(strings), CROSS_PROJECT_SCOPE_PATTERNS)


def _check_stop_content(strings: list[str]) -> str | None:
    joined = "\n".join(strings)
    if _matches_any(joined, STOP_PATTERNS):
        return "broad question / user-punt phrase detected"
    if _matches_any(joined, VISUAL_PROOF_PATTERNS) and not _matches_any(
        joined, ALLOWED_VISUAL_CONTEXT
    ):
        return "repeated visual proof request detected"
    if _matches_any(joined, DOC_ROUTE_HANDOFF_PATTERNS):
        return "md/README/manifest handoff laundering detected; inline exact user-operable steps instead"
    ambiguous_placement = _ambiguous_file_placement_lines(joined)
    if ambiguous_placement:
        return (
            "ambiguous file placement handoff detected; each user-owned file needs "
            f"what/how-created/used-by detail: {ambiguous_placement[0]}"
        )
    if _has_underexplained_new_script_request(joined):
        return (
            "underexplained new-script request detected; state whether an existing "
            "completed script can be used, what the script is, accepted format, and "
            "why it must match the episode"
        )
    if _has_closeout_log_without_next_action(joined):
        return (
            "closeout log ends without next-action bridge; state who acts next "
            "and what happens next in normal language before stopping"
        )
    background_skit_issue = _check_background_skit_role_drift(joined)
    if background_skit_issue:
        return background_skit_issue
    return None


def _ambiguous_file_placement_lines(text: str) -> list[str]:
    results: list[str] = []
    for line in text.splitlines():
        if AMBIGUOUS_FILE_PLACEMENT_LINE.search(line):
            if not FILE_PLACEMENT_DETAIL_PATTERN.search(line):
                results.append(line.strip())
    return results


def _has_underexplained_new_script_request(text: str) -> bool:
    if not NEW_SCRIPT_REQUEST_PATTERN.search(text):
        return False
    return not all(pattern.search(text) for pattern in SCRIPT_HANDOFF_DETAIL_PATTERNS)


def _has_closeout_log_without_next_action(text: str) -> bool:
    if not CLOSEOUT_LOG_WITH_UNTRACKED_PATTERN.search(text):
        return False
    return not CLOSEOUT_NEXT_ACTION_PATTERN.search(text)


def _check_background_skit_role_drift(text: str) -> str | None:
    has_context = BACKGROUND_SKIT_CONTEXT_PATTERN.search(text)
    has_line_cue_allowance = BACKGROUND_SKIT_LINE_CUE_ALLOW_PATTERN.search(text)
    if not has_context and not has_line_cue_allowance:
        return None
    if has_line_cue_allowance and not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
        return (
            "background skit line-cue allowance detected; delivery/skit examples "
            "must be framed as independent setup-complication-reaction-resolution stories"
        )
    if _matches_any(text, BACKGROUND_SKIT_REACTION_DRIFT_PATTERNS):
        if not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
            return (
                "background skit role drift detected; skit_group/background skit "
                "must not be treated as narrator aitenote or line-by-line reactions"
            )
    if _has_background_skit_motion_only_answer(text):
        return (
            "background skit motion-only explanation detected; real-estate/delivery "
            "examples need scene bible, time budget, cast continuity, placement, and proof path"
        )
    if BACKGROUND_SKIT_DIRECT_YMM4_OVERCLAIM_PATTERN.search(text):
        if not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
            return (
                "background skit direct IR/YMM4 overclaim detected; next step must be "
                "asset/proof gap report and template/proxy classification before IR/YMM4 review"
            )
    if BACKGROUND_SKIT_INTENT_TEMPLATE_CONFLATION_PATTERN.search(text):
        if not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
            return (
                "background skit intent/template conflation detected; IR intent must be "
                "separated from delivery_*_v1 template names"
            )
    if BACKGROUND_SKIT_PYTHON_ONLY_PLACEMENT_PATTERN.search(text):
        if not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
            return (
                "background skit adapter role underclaimed; Python does not generate art, "
                "but it validates IR, resolves registry/templates, patches ymmp, readbacks, and reports gaps"
            )
    if BACKGROUND_SKIT_IR_TIMETABLE_CONTEXT_PATTERN.search(text):
        if BACKGROUND_SKIT_RESPONSE_FLUFF_PATTERN.search(text):
            return (
                "background skit response fluff detected; replace vibes/encouragement with "
                "concrete estimates, timing values, density numbers, and source-backed gaps"
            )
        has_blueprint_validation = BACKGROUND_SKIT_BLUEPRINT_VALIDATION_RESULT_PATTERN.search(text)
        if not BACKGROUND_SKIT_TIMETABLE_BLOCKED_PATTERN.search(text) and not has_blueprint_validation:
            if not (
                BACKGROUND_SKIT_CONCRETE_TOTAL_DURATION_PATTERN.search(text)
                and BACKGROUND_SKIT_CONCRETE_TIME_RANGE_PATTERN.search(text)
                and BACKGROUND_SKIT_CONCRETE_DURATION_SEC_PATTERN.search(text)
            ):
                return (
                    "background skit IR/timetable lacks concrete timing values; field names "
                    "such as total duration/mm:ss/duration sec are not enough without actual numbers"
                )
            if not BACKGROUND_SKIT_CONCRETE_DENSITY_AUDIT_PATTERN.search(text):
                return (
                    "background skit IR/timetable lacks numeric density audit; quantify sparse risk, "
                    "intentional rest, unexplained empty time, and visual state density"
                )
            if not BACKGROUND_SKIT_CONCRETE_SCRIPT_MATURITY_PATTERN.search(text):
                return (
                    "background skit IR/timetable lacks concrete script maturity result; "
                    "diagnose structure with pass/fail codes and ideal-script deltas"
                )
            if BACKGROUND_SKIT_SCRIPT_LINE_RANGE_PATTERN.search(text) and not (
                BACKGROUND_SKIT_SCRIPT_RANGE_SOURCE_PATTERN.search(text)
            ):
                return (
                    "background skit IR/timetable uses script line ranges without source; "
                    "include script_source, line_count, and range_basis/readback evidence"
                )
        if not has_blueprint_validation:
            return (
                "background skit IR/timetable lacks validated blueprint result; numeric tables "
                "are not enough without validate-background-skit-blueprint status and derived_metrics/errors"
            )
    wants_overlay_compact_review = BACKGROUND_SKIT_OVERLAY_COMPACT_REVIEW_ADVANCE_PATTERN.search(text)
    closes_overlay_compact_review = BACKGROUND_SKIT_OVERLAY_COMPACT_REVIEW_CLOSEOUT_PATTERN.search(text)
    if wants_overlay_compact_review or closes_overlay_compact_review:
        if BACKGROUND_SKIT_RE07_SCRIPT_BLOCKER_PATTERN.search(text):
            return (
                "background skit overlay-only compact review cannot proceed while "
                "SCRIPT_BLOCKED_RE07_TOO_BROAD remains in the validator result"
            )
        if not BACKGROUND_SKIT_ALLOWED_OVERLAY_NEXT_PATTERN.search(text):
            return (
                "background skit overlay-only compact review lacks validator authority; "
                "include allowed_next_actions: [overlay_only_compact_review]"
            )
        if closes_overlay_compact_review:
            if not BACKGROUND_SKIT_COMPACT_REVIEW_ARTIFACT_PATH_PATTERN.search(text):
                return (
                    "background skit overlay-only compact review closeout lacks generated "
                    "artifact path; include literal 'artifact path: ...'"
                )
            if not BACKGROUND_SKIT_COMPACT_REVIEW_READBACK_PATTERN.search(text):
                return (
                    "background skit overlay-only compact review closeout lacks literal "
                    "'readback result: ...'"
                )
            if not BACKGROUND_SKIT_REMAINING_BLOCKERS_PATTERN.search(text):
                return (
                    "background skit overlay-only compact review closeout lacks literal "
                    "'remaining blockers: ...'"
                )
            if not BACKGROUND_SKIT_FORBIDDEN_NEXT_PATTERN.search(text):
                return (
                    "background skit overlay-only compact review closeout lacks forbidden_next_actions"
                )
            if not BACKGROUND_SKIT_NOT_CREATIVE_ACCEPTANCE_PATTERN.search(text):
                return (
                    "background skit overlay-only compact review closeout must state it is "
                    "not creative acceptance"
                )
    if BACKGROUND_SKIT_DOWNSTREAM_OPTIMISM_PATTERN.search(text):
        if (
            not BACKGROUND_SKIT_NEGATION_PATTERN.search(text)
            and not BACKGROUND_SKIT_TIMETABLE_SAFE_NEXT_PATTERN.search(text)
        ):
            return (
                "background skit downstream optimism detected; do not assume lower stages "
                "will fix script/timetable gaps without diagnostic, timetable, and density gates"
            )
    if BACKGROUND_SKIT_SCENE_PLAN_OR_MATRIX_PATTERN.search(text):
        if not BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
            if not BACKGROUND_SKIT_SCRIPT_LINE_RANGE_PATTERN.search(text):
                return (
                    "background skit scene bible lacks script line ranges; self-contained "
                    "design answers need line ranges for each block"
                )
            if not BACKGROUND_SKIT_BLOCK_PROOF_PATH_PATTERN.search(text):
                return (
                    "background skit scene bible lacks block proof paths; each block "
                    "needs its proof path before IR/YMM4 handoff"
                )
        if (
            not BACKGROUND_SKIT_NEGATION_PATTERN.search(text)
            and not BACKGROUND_SKIT_SCENE_BIBLE_DETAIL_PATTERN.search(text)
        ):
            return (
                "background skit scene plan lacks scene-bible fields; include time budget, "
                "cast continuity, screen placement, and proof path before closeout"
            )
    if BACKGROUND_SKIT_TEMPLATE_REUSE_PATTERN.search(text):
        if (
            not BACKGROUND_SKIT_NEGATION_PATTERN.search(text)
            and not BACKGROUND_SKIT_TEMPLATE_SYMBOL_PATTERN.search(text)
        ):
            return (
                "background skit template reuse lacks symbolic role; state who the reused "
                "template represents before using existing templates"
            )
    if (
        BACKGROUND_SKIT_HANDOFF_PATTERN.search(text)
        and not BACKGROUND_SKIT_BLUEPRINT_VALIDATION_RESULT_PATTERN.search(text)
        and not (
            closes_overlay_compact_review
            and BACKGROUND_SKIT_ALLOWED_OVERLAY_NEXT_PATTERN.search(text)
            and BACKGROUND_SKIT_NOT_CREATIVE_ACCEPTANCE_PATTERN.search(text)
        )
        and not _matches_any(
        text,
        BACKGROUND_SKIT_ROLE_ANCHOR_PATTERNS,
        )
    ):
        return (
            "background skit handoff lacks independent scene-bible contract; state "
            "parallel layer / not aitenote / time budget / cast continuity before acceptance"
        )
    if BACKGROUND_SKIT_UNDERSPECIFIED_ACK_PATTERN.search(text):
        if not BACKGROUND_SKIT_DESIGN_NEXT_PATTERN.search(text):
            return (
                "background skit underspecified acknowledgement detected; connect "
                "uncertainty to assistant-owned scene bible, time budget, cast continuity, "
                "and asset/proof matrix before stopping"
            )
    if re.search(r"(?:素材|assets?).{0,40}(?:必要|不足|missing)", text, re.IGNORECASE):
        if (
            closes_overlay_compact_review
            and BACKGROUND_SKIT_ALLOWED_OVERLAY_NEXT_PATTERN.search(text)
            and BACKGROUND_SKIT_REMAINING_BLOCKERS_PATTERN.search(text)
            and BACKGROUND_SKIT_FORBIDDEN_NEXT_PATTERN.search(text)
        ):
            return None
        if BACKGROUND_SKIT_BLUEPRINT_VALIDATION_RESULT_PATTERN.search(text):
            return None
        if not BACKGROUND_SKIT_ASSET_MATRIX_PATTERN.search(text):
            return (
                "background skit asset need lacks asset matrix; separate characters, "
                "placement, background, props, existing/missing assets, owner, and proof path"
            )
    return None


def _has_background_skit_motion_only_answer(text: str) -> bool:
    if BACKGROUND_SKIT_NEGATION_PATTERN.search(text):
        return False
    labels = {
        match.group(0).lower()
        for match in BACKGROUND_SKIT_MOTION_LABEL_PATTERN.finditer(text)
    }
    if len(labels) < 4:
        return False
    return not BACKGROUND_SKIT_SCENE_BIBLE_DETAIL_PATTERN.search(text)


def main() -> int:
    payload = _read_payload()
    strings = _collect_strings(payload)
    event = _event_name(payload).lower()

    if "stop" in event or "response" in event:
        forbidden = _contains_forbidden_path(strings)
        if forbidden and not _has_cross_project_scope(strings):
            return _reject(
                "Guardrails rejected repo-external reference without explicit cross-project scope:\n"
                f"{forbidden}"
            )

        issue = _check_stop_content(strings)
        if issue:
            if _strict_mode_enabled():
                return _reject(f"Guardrails rejected assistant output: {issue}")
            print(f"Guardrails advisory: {issue}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""B-16 rerun 用の補助テキスト生成。"""

from __future__ import annotations


def render_diagram_rerun_prompt() -> str:
    """外部 LLM / Automation に添える短い prompt を返す。"""
    lines = [
        "この packet の constraints と response_preferences を守って、output contract に沿う diagram brief だけを返してください。",
        "",
        "特に次を優先してください。",
        "- 図に向く section だけを選ぶ",
        "- 背景や通常の cue memo で十分な section は diagram brief に含めない",
        "- `goal` は「なぜ図が必要か」がすぐ分かる形にする",
        "- `must_include` は 3〜4 件程度に絞る",
        "- `label_suggestions` はそのまま図のラベル案として使える粒度にする",
        "- `avoid_misread` は本当に誤読しやすい点だけに絞る",
    ]
    return "\n".join(lines) + "\n"


def render_diagram_rerun_diff_template() -> str:
    """rerun 差分記録用の Markdown 雛形を返す。"""
    lines = [
        "# B-16 Rerun Diff Template",
        "",
        "更新後 packet に対する rerun 結果を、baseline と比較して短く残すための雛形。",
        "",
        "## Raw Result",
        "",
        "- response file:",
        "- received date:",
        "",
        "## Diff Against Baseline",
        "",
        "| 項目 | baseline | rerun | 差分メモ |",
        "|---|---|---|---|",
        "| selected diagram count | 3 | | |",
        "| selected sections | S1, S2, S3 | | |",
        "| excluded sections | S4, S5 | | |",
        "| goal clarity | high | | |",
        "| must_include density | 3-5 が中心 | | |",
        "| label usefulness | medium-high | | |",
        "| avoid_misread usefulness | high | | |",
        "",
        "## Quick Judgment",
        "",
        "- better:",
        "- unchanged:",
        "- worse:",
        "",
        "## Decision Hint",
        "",
        "- rerun で改善していれば:",
        "  - diagram brief の対象 section 絞り込みは概ね収束",
        "- rerun でも図にしなくてよい section を拾うなら:",
        "  - response preference をさらに強める余地あり",
        "- rerun が B-15 cue memo と似すぎるなら:",
        "  - role separation を packet 文言でさらに明示する",
    ]
    return "\n".join(lines) + "\n"


def render_diagram_baseline_notes_template(
    *,
    target_diagram_count: int,
    section_seeds: list[dict] | None = None,
) -> str:
    """初回 rerun 前に埋める baseline notes の雛形を返す。"""
    suggested_sections = ", ".join(
        f"`{section['section_id']}`" for section in (section_seeds or [])[:target_diagram_count]
    ) or "（未記入）"

    lines = [
        "# B-16 Baseline Notes",
        "",
        "次の rerun で比較するときの簡易 baseline。",
        "",
        "## Current Baseline",
        "",
        f"- selected diagrams: {target_diagram_count}（初期目安）",
        f"- selected sections: {suggested_sections}",
        "- excluded sections:",
        "- time comparison:",
        "  - before:",
        "  - after:",
        "  - delta:",
        "",
        "## What Worked",
        "",
        "-",
        "",
        "## What To Improve",
        "",
        "- B-15 cue memo と役割が被らないようにする",
        "- 背景だけで十分な section を diagram brief に入れない",
        "- `must_include` は 3〜4 件程度に収まると扱いやすい",
        "",
        "## Rerun Success Signal",
        "",
        "- 図にしなくてよい section をさらに拾わなくなる",
        "- `must_include` が過不足なく絞られる",
        "- B-15 cue memo と明確に使い分けできる",
    ]
    return "\n".join(lines) + "\n"


def render_diagram_quickstart(
    *,
    packet_name: str,
    rerun_prompt_name: str,
    diff_template_name: str,
    proof_log_name: str,
    baseline_notes_name: str | None = None,
) -> str:
    """次回 rerun の最短手順を返す。"""
    lines = [
        "# B-16 Quickstart",
        "",
        "次に diagram rerun をするときは、この順で見る。",
        "",
        "## 1. 外部 GPT に渡すもの",
        "",
        f"- `{packet_name}`",
        f"- `{rerun_prompt_name}`",
        "",
        "## 2. rerun 後に書く場所",
        "",
        f"- 差分だけ: `{diff_template_name}`",
        f"- proof 正本: `{proof_log_name}`",
        "",
    ]

    if baseline_notes_name:
        lines.extend([
            "## 3. 先に見る baseline",
            "",
            f"- `{baseline_notes_name}`",
            "",
        ])

    lines.extend([
        "## 4. 今回の見るポイント",
        "",
        "- 図にしなくてよい section を拾わなくなったか",
        "- `must_include` が 3〜4 件程度に収まるか",
        "- B-15 cue memo と役割が被っていないか",
        "",
        "## 5. 返答するとき",
        "",
        "最短ならこれだけで十分。",
        "",
        "```text",
        "selected diagrams:",
        "selected sections:",
        "excluded sections:",
        "better:",
        "unchanged:",
        "worse:",
        "```",
    ])
    return "\n".join(lines) + "\n"

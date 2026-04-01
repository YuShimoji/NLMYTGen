"""B-16 workflow proof 用の記録テンプレート生成。"""

from __future__ import annotations

from datetime import date


def render_diagram_workflow_proof(
    *,
    source_name: str,
    packet_markdown_name: str,
    packet_json_name: str,
    packet_command: str,
    payload: dict,
) -> str:
    """B-16 workflow proof 用 Markdown 雛形を返す。"""
    section_seed_count = len(payload["context"].get("section_seeds", []))
    utterance_count = payload["context"]["utterance_count"]

    lines: list[str] = []
    lines.append("# B-16 Workflow Proof Log")
    lines.append("")
    lines.append(f"- date: {date.today().isoformat()}")
    lines.append(f"- transcript / source: `{source_name}`")
    lines.append(f"- packet markdown: `{packet_markdown_name}`")
    lines.append(f"- packet json: `{packet_json_name}`")
    lines.append(f"- packet command: `{packet_command}`")
    lines.append("")
    lines.append("## Packet Quality")
    lines.append("")
    lines.append("| 項目 | 記録 |")
    lines.append("|---|---|")
    lines.append(f"| utterance count | {utterance_count} |")
    lines.append(f"| section seed count | {section_seed_count} |")
    lines.append("| figure-worthy sections looked plausible? | |")
    lines.append("| missing context | |")
    lines.append("")
    lines.append("## Diagram Brief Result")
    lines.append("")
    lines.append("| 項目 | 記録 |")
    lines.append("|---|---|")
    lines.append("| summary quality | |")
    lines.append("| diagram brief usefulness | |")
    lines.append("| must_include usefulness | |")
    lines.append("| label_suggestions usefulness | |")
    lines.append("| avoid_misread usefulness | |")
    lines.append("")
    lines.append("## Time Comparison")
    lines.append("")
    lines.append("| 項目 | 分 | メモ |")
    lines.append("|---|---:|---|")
    lines.append("| before: manual diagram planning estimate | | |")
    lines.append("| after: diagram brief assisted planning | | |")
    lines.append("| delta | | |")
    lines.append("")
    lines.append("## Assessment")
    lines.append("")
    lines.append("| 項目 | 記録 |")
    lines.append("|---|---|")
    lines.append("| useful enough to keep using? | |")
    lines.append("| next improvement inside repo | |")
    lines.append("| should remain text-only? | |")
    lines.append("| should stay separate from B-15? | |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- diagram brief そのものはこのファイルに貼るか、別ファイルへの参照を書く")
    lines.append("- 画像生成や図版ファイル生成は行わない")
    lines.append("- 1 回の proof が終わったら、次に repo 内で直す点を 1 件だけ残す")
    lines.append("")
    return "\n".join(lines)

"""B-15 workflow proof 用の記録テンプレート生成。"""

from __future__ import annotations

from datetime import date


def render_cue_workflow_proof(
    *,
    source_name: str,
    packet_markdown_name: str,
    packet_json_name: str,
    packet_command: str,
    payload: dict,
) -> str:
    """B-15 workflow proof 用 Markdown 雛形を返す。"""
    section_seed_count = len(payload["context"].get("section_seeds", []))
    utterance_count = payload["context"]["utterance_count"]

    lines: list[str] = []
    lines.append("# B-15 Workflow Proof Log")
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
    lines.append("| role analysis looked correct? | |")
    lines.append("| missing context | |")
    lines.append("")
    lines.append("## Cue Memo Result")
    lines.append("")
    lines.append("| 項目 | 記録 |")
    lines.append("|---|---|")
    lines.append("| summary quality | |")
    lines.append("| section cues quality | |")
    lines.append("| background cue usefulness | |")
    lines.append("| emotion / BGM / transition usefulness | |")
    lines.append("| operator_todos usefulness | |")
    lines.append("")
    lines.append("## Time Comparison")
    lines.append("")
    lines.append("| 項目 | 分 | メモ |")
    lines.append("|---|---:|---|")
    lines.append("| before: manual prep estimate | | |")
    lines.append("| after: cue memo assisted prep | | |")
    lines.append("| delta | | |")
    lines.append("")
    lines.append("## Assessment")
    lines.append("")
    lines.append("| 項目 | 記録 |")
    lines.append("|---|---|")
    lines.append("| useful enough to keep using? | |")
    lines.append("| next improvement inside repo | |")
    lines.append("| should remain text-only? | |")
    lines.append("| should SDK integration wait? | |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- cue memo そのものはこのファイルに貼るか、別ファイルへの参照を書く")
    lines.append("- YMM4 / `.ymmp` direct edit は行わない")
    lines.append("- 1 回の proof が終わったら、次に repo 内で直す点を 1 件だけ残す")
    lines.append("")
    return "\n".join(lines)

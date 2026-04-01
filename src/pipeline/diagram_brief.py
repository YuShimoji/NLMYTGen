"""B-16: diagram brief 用 packet を生成する。

NotebookLM 由来 transcript を入力に、外部 LLM / Automation に渡せる
text-only の diagram brief packet を組み立てる。画像生成や YMM4 direct edit は行わない。
"""

from __future__ import annotations

import json

from src.contracts.structured_script import StructuredScript
from src.pipeline.cue_packet import _suggest_section_ranges
from src.pipeline.normalize import analyze_speaker_roles


def build_diagram_brief_payload(
    script: StructuredScript,
    *,
    source_name: str,
    speaker_map: dict[str, str] | None = None,
) -> dict:
    """diagram brief packet の payload を返す。"""
    speaker_map = speaker_map or {}
    roles = analyze_speaker_roles(script)

    transcript = []
    for i, utterance in enumerate(script.utterances, start=1):
        transcript.append(
            {
                "index": i,
                "speaker": utterance.speaker,
                "mapped_speaker": speaker_map.get(utterance.speaker, utterance.speaker),
                "text": utterance.text,
            }
        )

    role_context = {}
    for speaker, stats in roles.items():
        role_context[speaker] = {
            "role": stats["role"],
            "utterances": stats["utterances"],
            "avg_length": round(stats["avg_length"], 1),
            "questions": stats["questions"],
            "short_responses": stats["short_responses"],
            "topic_intros": stats["topic_intros"],
        }

    section_seeds = _suggest_section_ranges(script, roles)
    target_diagram_count = max(1, min(3, len(section_seeds)))

    return {
        "packet_version": "b16-v2",
        "feature_id": "B-16",
        "phase": "diagram-brief-only",
        "source_name": source_name,
        "objective": "Generate text-only diagram briefs for the sections that would benefit from a figure.",
        "constraints": [
            "Do not generate images or diagram files.",
            "Do not edit YMM4 projects or .ymmp data.",
            "Do not download assets.",
            "Return text guidance only.",
            "Focus on figure-worthy sections instead of the whole transcript.",
        ],
        "response_preferences": {
            "target_diagram_count": target_diagram_count,
            "keep_only_figure_worthy_sections": True,
            "skip_sections_better_served_by_backgrounds": True,
            "prefer_causal_or_structural_diagrams": True,
            "avoid_repeating_b15_cue_memo": True,
            "must_include_density": "Prefer 3-4 must_include items per diagram brief.",
            "operator_todos_max": 4,
            "keep_notes_concise": True,
        },
        "output_contract": {
            "summary": "Short overview of where diagrams would help the most.",
            "diagram_briefs": [
                {
                    "diagram_id": "D1",
                    "topic": "What this diagram should explain",
                    "source_section": "S1",
                    "goal": "Why this diagram exists",
                    "recommended_format": "timeline / comparison / flow / ranking / layered concept map",
                    "must_include": [
                        "Key fact or component the diagram must show"
                    ],
                    "comparison_axes": [
                        "What should be compared or contrasted"
                    ],
                    "label_suggestions": [
                        "Potential labels or captions"
                    ],
                    "avoid_misread": [
                        "Common misunderstanding to avoid"
                    ],
                    "operator_note": "What the human should pay attention to when making the diagram",
                }
            ],
            "global_notes": [
                "Notes that apply across all diagrams"
            ],
            "operator_todos": [
                "Specific follow-up items for the human operator"
            ],
        },
        "context": {
            "utterance_count": len(script.utterances),
            "speakers": sorted({u.speaker for u in script.utterances}),
            "speaker_map": speaker_map,
            "role_analysis": role_context,
            "section_seeds": section_seeds,
        },
        "transcript": transcript,
    }


def render_diagram_brief_markdown(payload: dict) -> str:
    """payload を Markdown packet に整形する。"""
    lines: list[str] = []
    lines.append("# B-16 Diagram Brief Request Packet")
    lines.append("")
    lines.append("## Objective")
    lines.append(payload["objective"])
    lines.append("")
    lines.append("## Constraints")
    for item in payload["constraints"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Output Contract")
    lines.append("```json")
    lines.append(json.dumps(payload["output_contract"], ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Response Preferences")
    lines.append("```json")
    lines.append(json.dumps(payload["response_preferences"], ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Context")
    lines.append(f"- Source: {payload['source_name']}")
    lines.append(f"- Utterances: {payload['context']['utterance_count']}")
    lines.append(f"- Speakers: {', '.join(payload['context']['speakers'])}")
    if payload["context"]["speaker_map"]:
        lines.append("- Speaker map:")
        for src, dst in payload["context"]["speaker_map"].items():
            lines.append(f"  - {src} -> {dst}")
    lines.append("- Role analysis:")
    for speaker, stats in payload["context"]["role_analysis"].items():
        lines.append(
            f"  - {speaker}: role={stats['role']}, utterances={stats['utterances']}, "
            f"avg_length={stats['avg_length']}, questions={stats['questions']}, "
            f"short_responses={stats['short_responses']}, topic_intros={stats['topic_intros']}"
        )
    if payload["context"]["section_seeds"]:
        lines.append("- Suggested section seeds:")
        for section in payload["context"]["section_seeds"]:
            lines.append(
                f"  - {section['section_id']}: {section['start_index']}-{section['end_index']} "
                f"({section['seed_reason']}) preview={section['preview']}"
            )
    lines.append("")
    lines.append("## Transcript")
    for item in payload["transcript"]:
        mapped = item["mapped_speaker"]
        src = item["speaker"]
        lines.append(f"{item['index']}. [{mapped} | src={src}] {item['text']}")
    lines.append("")
    lines.append("## Response Instruction")
    lines.append("Return only a diagram brief that matches the output contract.")
    lines.append("Include only the sections that clearly benefit from a figure.")
    lines.append("Prefer sections with causal structure, comparisons, or layered systems over sections that work as backgrounds.")
    lines.append("Skip sections that would be better handled by B-15 style background cues alone.")
    lines.append("Do not generate images, diagram files, or YMM4 direct edits.")
    lines.append("Keep operator todos close to the response preferences.")
    lines.append("")
    return "\n".join(lines)

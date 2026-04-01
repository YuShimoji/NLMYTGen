"""B-15 Phase 1: cue memo 用 packet を生成する。

NotebookLM 由来 transcript を入力に、外部 LLM / Automation に渡せる
text-only の cue packet を組み立てる。YMM4 / .ymmp の直接編集は行わない。
"""

from __future__ import annotations

import json
import re

from src.contracts.structured_script import StructuredScript
from src.pipeline.normalize import analyze_speaker_roles


_SECTION_TRIGGER = re.compile(
    r"^(まず|次に|一方で|ここで|では|さて|たとえば|例えば|そして|つまり|最後に|結論|要するに)"
)


def _suggest_section_ranges(script: StructuredScript, roles: dict[str, dict]) -> list[dict]:
    """Transcript の section seed を提案する。"""
    utterances = script.utterances
    if not utterances:
        return []

    host_speakers = {speaker for speaker, stats in roles.items() if stats["role"] == "host"}
    boundaries = [1]

    for index, utterance in enumerate(utterances, start=1):
        if index == 1:
            continue
        if utterance.speaker in host_speakers and _SECTION_TRIGGER.match(utterance.text):
            if index - boundaries[-1] >= 3:
                boundaries.append(index)

    if len(boundaries) == 1 and len(utterances) >= 10:
        target_sections = min(5, max(2, len(utterances) // 6))
        step = max(3, len(utterances) // target_sections)
        cursor = 1 + step
        while cursor <= len(utterances):
            if cursor - boundaries[-1] >= 3:
                boundaries.append(cursor)
            cursor += step

    sections = []
    for i, start in enumerate(boundaries, start=1):
        end = boundaries[i] - 1 if i < len(boundaries) else len(utterances)
        sections.append(
            {
                "section_id": f"S{i}",
                "start_index": start,
                "end_index": end,
                "seed_reason": "topic-trigger" if i > 1 else "opening",
                "preview": utterances[start - 1].text[:50],
            }
        )
    return sections


def build_cue_packet_payload(
    script: StructuredScript,
    *,
    source_name: str,
    speaker_map: dict[str, str] | None = None,
) -> dict:
    """cue packet の payload を返す。"""
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
    target_section_count = f"{max(3, len(section_seeds))}-{max(4, len(section_seeds) + 1)}"

    return {
        "packet_version": "b15-phase1-v3",
        "feature_id": "B-15",
        "phase": "phase1-cue-memo-only",
        "source_name": source_name,
        "objective": "Generate an S-6 cue memo only from the existing transcript.",
        "constraints": [
            "Do not generate a new primary script from scratch.",
            "Do not rewrite transcript lines unless explicitly asked in a later phase.",
            "Do not edit YMM4 projects or .ymmp data.",
            "Do not generate images, audio, or video.",
            "Return text guidance only.",
        ],
        "response_preferences": {
            "target_section_count": target_section_count,
            "background_density": "One primary background plus at most one supporting visual per section.",
            "sound_policy": "Omit sound cues unless they clearly help.",
            "operator_todos_max": 4,
            "keep_notes_concise": True,
        },
        "output_contract": {
            "summary": "Short overview of the video and its likely visual arc.",
            "sections": [
                {
                    "section_id": "S1",
                    "topic": "What this section is about",
                    "start_index": 1,
                    "end_index": 5,
                    "primary_background": "Main background direction to anchor the section",
                    "supporting_visual": "Optional supporting visual or insert if needed",
                    "emotion_cue": "Expression / tone suggestion",
                    "sound_cue_optional": "Optional BGM or SE note only if it clearly helps",
                    "transition_cue": "Transition suggestion if useful",
                    "operator_note": "What the human should pay attention to",
                }
            ],
            "global_notes": [
                "Notes that apply across the whole video"
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


def render_cue_packet_markdown(payload: dict) -> str:
    """payload を Markdown packet に整形する。"""
    lines: list[str] = []
    lines.append("# B-15 Cue Memo Request Packet")
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
    lines.append("Return only a cue memo that matches the output contract.")
    lines.append("Prefer one primary background plus at most one supporting visual per section.")
    lines.append("Treat sound cues as optional unless they clearly help.")
    lines.append("Keep the number of sections and operator todos close to the response preferences.")
    lines.append("Do not rewrite the transcript. Do not propose YMM4 direct edits.")
    lines.append("")
    return "\n".join(lines)

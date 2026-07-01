# B-16 Diagram Brief Request Packet

## Objective
Generate text-only diagram briefs for the sections that would benefit from a figure.

## Constraints
- Do not generate images or diagram files.
- Do not edit YMM4 projects or .ymmp data.
- Do not download assets.
- Return text guidance only.
- Focus on figure-worthy sections instead of the whole transcript.

## Output Contract
```json
{
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
      "operator_note": "What the human should pay attention to when making the diagram"
    }
  ],
  "global_notes": [
    "Notes that apply across all diagrams"
  ],
  "operator_todos": [
    "Specific follow-up items for the human operator"
  ]
}
```

## Response Preferences
```json
{
  "target_diagram_count": 2,
  "keep_only_figure_worthy_sections": true,
  "skip_sections_better_served_by_backgrounds": true,
  "prefer_causal_or_structural_diagrams": true,
  "avoid_repeating_b15_cue_memo": true,
  "must_include_density": "Prefer 3-4 must_include items per diagram brief.",
  "operator_todos_max": 4,
  "keep_notes_concise": true
}
```

## Context
- Source: transcript_sample.txt
- Utterances: 7
- Speakers: Host1, Host2
- Speaker map:
  - Host1 -> れいむ
  - Host2 -> まりさ
- Role analysis:
  - Host1: role=host, utterances=4, avg_length=35.5, questions=0, short_responses=0, topic_intros=0
  - Host2: role=guest, utterances=3, avg_length=36.7, questions=0, short_responses=0, topic_intros=0
- Suggested section seeds:
  - S1: 1-6 (opening) preview=今回は、NotebookLM音声概要をYMM4台本へ整える流れを確認します。
  - S2: 7-7 (topic-trigger) preview=最後に、人間がYMM4へ読み込み、字幕、話者、演出準備を確認します。

## Transcript
1. [れいむ | src=Host1] 今回は、NotebookLM音声概要をYMM4台本へ整える流れを確認します。
2. [まりさ | src=Host2] まず、話者名をYMM4キャラクター名へ対応させる speaker map を決めます。
3. [れいむ | src=Host1] 次に、字幕で読みやすい長さに整え、YMM4台本読込用CSVを生成します。
4. [まりさ | src=Host2] そのあと、背景や補助素材の候補をまとめたキューパケットを作ります。
5. [れいむ | src=Host1] 必要なら、図解前のパケットも出し、制作担当者が迷わない状態にします。
6. [まりさ | src=Host2] このパッケージは自動投稿ではなく、投稿候補制作の初期パイロットです。
7. [れいむ | src=Host1] 最後に、人間がYMM4へ読み込み、字幕、話者、演出準備を確認します。

## Response Instruction
Return only a diagram brief that matches the output contract.
Include only the sections that clearly benefit from a figure.
Prefer sections with causal structure, comparisons, or layered systems over sections that work as backgrounds.
Skip sections that would be better handled by B-15 style background cues alone.
Do not generate images, diagram files, or YMM4 direct edits.
Keep operator todos close to the response preferences.

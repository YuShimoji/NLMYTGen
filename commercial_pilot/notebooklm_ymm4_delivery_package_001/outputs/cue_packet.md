# B-15 Cue Memo Request Packet

## Objective
Generate an S-6 cue memo only from the existing transcript.

## Constraints
- Do not generate a new primary script from scratch.
- Do not rewrite transcript lines unless explicitly asked in a later phase.
- Do not edit YMM4 projects or .ymmp data.
- Do not generate images, audio, or video.
- Return text guidance only.

## Output Contract
```json
{
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
      "operator_note": "What the human should pay attention to"
    }
  ],
  "global_notes": [
    "Notes that apply across the whole video"
  ],
  "operator_todos": [
    "Specific follow-up items for the human operator"
  ]
}
```

## Response Preferences
```json
{
  "target_section_count": "3-4",
  "background_density": "One primary background plus at most one supporting visual per section.",
  "sound_policy": "Omit sound cues unless they clearly help.",
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
  - Host2: role=guest, utterances=3, avg_length=36.0, questions=0, short_responses=0, topic_intros=0
- Suggested section seeds:
  - S1: 1-6 (opening) preview=今回は、NotebookLM音声概要をYMM4台本へ整える流れを確認します。
  - S2: 7-7 (topic-trigger) preview=最後に、人間がYMM4へ読み込み、字幕、話者、演出準備を確認します。

## Transcript
1. [れいむ | src=Host1] 今回は、NotebookLM音声概要をYMM4台本へ整える流れを確認します。
2. [まりさ | src=Host2] まず、話者名をYMM4キャラクター名へ対応させる speaker map を決めます。
3. [れいむ | src=Host1] 次に、字幕で読みやすい長さに整え、YMM4台本読込用CSVを生成します。
4. [まりさ | src=Host2] そのあと、背景や補助素材の候補をまとめたキューパケットを作ります。
5. [れいむ | src=Host1] 必要なら、図解前のパケットも出し、制作担当者が迷わない状態にします。
6. [まりさ | src=Host2] このパッケージは自動投稿ではなく、手動納品の初期パイロットです。
7. [れいむ | src=Host1] 最後に、人間がYMM4へ読み込み、字幕、話者、演出準備を確認します。

## Response Instruction
Return only a cue memo that matches the output contract.
Prefer one primary background plus at most one supporting visual per section.
Treat sound cues as optional unless they clearly help.
Keep the number of sections and operator todos close to the response preferences.
Do not rewrite the transcript. Do not propose YMM4 direct edits.

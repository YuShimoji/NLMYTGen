# Real Episode Transcript Intake

This folder is the intake slot for the first real NotebookLM transcript. No
real transcript is present yet.

## Preferred File

Create this file when a user-approved transcript is ready:

```text
production_pilots/notebooklm_ymm4_episode_package_001/real_input/episode_001_transcript.txt
```

## Accepted Transcript Formats

Use one of these formats:

```text
Host1: First utterance from NotebookLM.
Host2: Reply from the second speaker.
Host1: Next utterance.
```

or a two-column CSV-style source:

```text
Host1,First utterance from NotebookLM.
Host2,Reply from the second speaker.
```

If the transcript has no speaker labels, say so explicitly before generation
because the CLI must use the `--unlabeled` route and an appropriate
`Speaker_A` / `Speaker_B` map.

## Speaker Map

After adding the transcript, update or replace:

```text
production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
```

Example:

```json
{
  "Host1": "れいむ",
  "Host2": "まりさ"
}
```

## Do Not Put Here

- External article bodies copied from the web.
- Rights-unclear source text.
- Private customer data.
- Credentials, API keys, payment data, or account details.
- Media files, audio, images, or downloaded assets.

## After Adding The Transcript

Run the commands in `YMM4_IMPORT_RUNBOOK.md`, or ask Codex to regenerate the
episode package from the real input. The expected next state is generated CSV
and packets from the real transcript, followed by manual YMM4 import
confirmation.

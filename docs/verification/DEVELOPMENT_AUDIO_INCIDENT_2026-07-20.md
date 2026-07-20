# Development Audio Incident — 2026-07-20

## Conclusion before remediation

The strongest supportable historical cause classification is
`C1_BROWSER_MEDIA_PLAYBACK`, with confidence `probable` and evidence grade
`probable_from_operation_timeline`. The immediately preceding reference-research
operation inspected three public-player interiors at a fixed timestamp, and its
report did not establish a mute contract. A background/headless Chromium-family
process can own a Windows audio session without a normal visible window.

This is not verified attribution. No historical PID, process tree, command line,
or Core Audio session snapshot exists for the audible interval. The exact emitting
process therefore remains unknown. In particular, there is no evidence that
VOICEVOX, SofTalk, or YukkuriMovieMaker emitted the reported sound.

## Safe baseline

The baseline was captured read-only before any guarded browser or media helper was
launched. No process, session, endpoint, or master-volume setting was changed.

- Relevant process inventory: 16 browser-family processes, one browser process
  carrying an automation/isolated-profile marker, 24 scripting-runtime processes,
  and one Windows audio-service process. All were pre-existing and are not project
  owned for this run.
- No running VOICEVOX frontend, VOICEVOX engine, SofTalk, YukkuriMovieMaker,
  ffplay, mpv, VLC, or Windows Media Player process was observed.
- Eight Core Audio sessions were enumerated through built-in Windows COM. One
  candidate Chrome session was observed. It was pre-existing, inactive, unmuted,
  and not attributed to this project operation. It was not changed.
- No relevant TTS-engine process existed, so there was no TTS-engine listening
  port to classify. Process existence would not by itself prove audible output.
- Personal browser history, cookies, profiles, unrelated files, and global shell
  history were not inspected.

Counts describe a point-in-time baseline and are not historical-cause proof.
Command lines and local paths are intentionally omitted from tracked evidence.

## Cause matrix

| class | process / command evidence | audio-session evidence | ownership | evidence grade | confidence | disposition |
| --- | --- | --- | --- | --- | --- | --- |
| C1 browser media playback | Public-player inspection immediately preceded the report; current browser processes are pre-existing | One current pre-existing inactive Chrome session; no historical session | Historical ownership unknown; current session not project owned | `probable_from_operation_timeline` | probable | Leading hypothesis, not verified |
| C2 TTS frontend or player | No current VOICEVOX frontend, SofTalk, ffplay, mpv, VLC, WMP, or matching scripting playback API | None observed for these classes | none | `unsupported` | unsupported | Rejected as an evidenced cause |
| C3 TTS engine server only | No current VOICEVOX engine/vv-engine process or relevant listener; engine-only existence would not imply playback | None observed | none | `unsupported` | unsupported | Not observed; semantically separated from speaker output |
| C4 YMM4 or editor preview | No current YukkuriMovieMaker process; repository can generate an operator launch script, but it was not run in the preceding slice or this investigation | None observed | none | `unsupported` | unsupported | Rejected as an evidenced cause |
| C5 pre-existing user process | Current browser processes and candidate Chrome session pre-date this operation | One inactive candidate session | explicitly pre-existing | `verified_process_audio_session` | not a historical attribution | Recorded and left untouched |
| C6 unknown | Historical emitting PID, parent, command line, and session state were not logged | unavailable for incident interval | unknown | `unknown` | unresolved exact emitter | Residual uncertainty retained |

## Repository static audit

- `src/pipeline/media_validation.py` uses `ffprobe` metadata probing and FFmpeg's
  null muxer. These are static/decode validation paths, not speaker playback.
- New-banknote operator builders contain text that can launch YMM4 for an explicit
  future operator milestone. No such generated launch was executed here.
- `scripts/operator/open_dashboard.ps1` opens a local, non-media dashboard in the
  user's default handler. It is not the public-player research path.
- No executable project path using `System.Speech`, `SpeechSynthesizer`, `winsound`,
  `playsound`, `pyttsx3`, `sounddevice`, `pygame.mixer`, ffplay, mpv, VLC, or WMP
  was found.
- VOICEVOX/SofTalk references found elsewhere are documentation, configuration,
  availability, or synthesis concerns unless an explicit frontend/player launch is
  requested. Synthesis/file creation and speaker playback are separate classes.

## Evidence boundaries

- Verified: current repository matches, current sanitized process/session
  snapshots, absence of mutation during baseline capture.
- Observed: the user's report of repeated loud synthesized/narrated speech and the
  immediately preceding three-player inspection timeline.
- Inferred: browser media is the most plausible historical class.
- Unverified: the historical emitting executable and any VOICEVOX/SofTalk/YMM4
  involvement.
- Not claimed: microphone-measured acoustic silence.

The remediation must prevent recurrence without requiring exact historical
attribution: isolated browser ownership, launch mute, pre-document DOM enforcement,
project-PID-only Core Audio mute, audible-player denial, and owned-tree cleanup.

# Development Audio Safety

NLMYTGen development and research are silent by default. The only accepted policy
value is:

```text
NLMYTGEN_AUDIO_POLICY=silent
```

There is no audible opt-in in this runtime. A future audio-observation milestone
requires a separate user-approved operator contract; this document does not grant
that authority.

## Guarded browser inspection

All project-owned browser/media inspection, including any future public-player
research, must go through `scripts/run_silent_media_inspection.ps1`. Do not launch a
browser media target directly from Python, PowerShell, Playwright, Selenium, or a
default browser handler.

The local zero-amplitude smoke is the default command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_silent_media_inspection.ps1
```

For a separately authorized inspection target, pass `-TargetUrl`. Add
`-RequireMedia` when a media element must be present for the inspection to count:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_silent_media_inspection.ps1 -TargetUrl <authorized-url> -RequireMedia
```

This corrective slice did not run the second form and did not access a public
player.

The wrapper applies these layers before target navigation:

1. It creates a new temporary profile and a directly owned Chromium-family root.
   It does not reuse personal cookies, history, or browser state.
2. It launches headless with `--mute-audio`, user-gesture autoplay policy,
   background persistence disabled, and loopback-only DevTools discovery.
3. It installs a pre-document script with
   `Page.addScriptToEvaluateOnNewDocument`. Existing and added audio/video elements
   are paused, muted, set to volume zero, stripped of autoplay, and watched by a
   `MutationObserver`. `HTMLMediaElement.play()` is blocked.
4. It enumerates Windows Core Audio through the built-in COM API and calls
   `SetMute(true)` only for PIDs proven to descend from the newly launched root.
   It never calls endpoint/master-volume setters.
5. It closes the browser, closes its Windows Job Object, terminates only a verified
   residual owned PID if necessary, removes the temporary profile, and requires no
   owned child to remain.

The local diagnostic receipt is written under ignored
`artifacts/audio_diagnostics/`. It can contain short-lived owned PIDs and sanitized
command lines, but no personal profile, username, raw audio, or unrelated
application details. The tracked incident receipt contains only aggregated facts.

## Playback deny boundary

Call `src.pipeline.silent_media_runtime.assert_command_allowed()` before a
project wrapper starts an external process capable of playback. In silent mode it
rejects:

- VOICEVOX desktop frontend, SofTalk/SofTalkW, and YukkuriMovieMaker preview paths;
- ffplay, mpv, VLC, and Windows Media Player;
- Python speaker-output packages such as winsound, playsound, pyttsx3,
  sounddevice, PyAudio, simpleaudio, and pygame.mixer;
- PowerShell/.NET `System.Speech` speaker calls;
- Chromium-family media navigation outside the guarded browser path.

The guard does not conflate synthesis with playback. A VOICEVOX engine server,
ffprobe metadata query, FFmpeg null decode, or audio-file generation is not itself
speaker output. Those operations still require their own task authority, and no
synthesis or audio generation was authorized for this corrective slice.

## Incident fail-safe

If the user notices sound, or an owned session cannot be proven muted:

1. stop the current operation;
2. let the guard close only its owned process tree;
3. do not touch pre-existing processes or Windows master volume;
4. retain the ignored diagnostic receipt;
5. use stop condition `unexpected_audio_output` for an unmuted owned session;
6. report the owned PID class, parent relation, sanitized command category, and
   session mute state;
7. do not claim acceptance or continue to a commit until the layer is repaired.

An engine process, a process name, or a user's acoustic observation alone is not
PID attribution. Core Audio session evidence plus direct-launch/ancestry evidence
is required to call a project process verified.

## Current evidence boundary

The 2026-07-20 incident conclusion is `probable`, not `verified`: public-player
inspection is the leading historical class, while the exact historical emitter is
unknown. See
`docs/verification/DEVELOPMENT_AUDIO_INCIDENT_2026-07-20.md` and its JSON receipt.

The passing local fixture contains one second of 8 kHz, mono, 16-bit PCM whose
every sample is zero. This proves the test asset carried no audible signal; it is
not a microphone measurement of acoustic silence.

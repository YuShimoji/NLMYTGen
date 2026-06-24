# Newsroom YMM4 Timing Patch Remote Handoff

handoff_id: newsroom_ymmp_timing_patch_remote_handoff_2026_06_24
source_supervisor_slice: timing-patch-probe-supervisor-review
source_commit: a0a3485 feat: probe newsroom YMM4 timing patch
handoff_status: remote_parity_ready_for_manual_observation
diagnostic_only: true

## Remote State

- branch: master
- remote: origin
- repository: YuShimoji/NLMYTGen
- verified_before_handoff_docs_update: `HEAD...origin/master = 0 0`
- accepted_probe_commit: `a0a3485 feat: probe newsroom YMM4 timing patch`
- local_worktree_policy: keep `_tmp/` diagnostic `.ymmp` and media ignored and unstaged

## Supervisor Decision Preserved

The supervisor accepted `a0a3485 feat: probe newsroom YMM4 timing patch`.
The accepted scope is structural timing proof only. The patched diagnostic
timeline reaches `4080` frames / `68` sec at `60` fps, using dialogue starts
`0 / 720 / 1440 / 2760` and lengths `720 / 720 / 1320 / 1320`. Native YMM4
speaker/text/voice fields remain preserved, including `VoiceCache`,
`VoiceParameter`, `Pronounce`, `Hatsuon`, `VoiceLength`, `AudioEffects`, the
`Characters` block, and `AquesTalk` hints.

The decision intentionally does not accept production render readiness, public
video readiness, production narration quality, visual layout readiness, real
content readiness, production approval, or post-patch render success. It also
does not authorize committing `.ymmp` or media output.

## Current Transition

| State before this handoff | Stored proof | What is still missing | Next owner |
|---|---|---|---|
| 8 sec natural YMM4 smoke already existed | prior tiny render readback | neutral 68 sec render behavior | user |
| 68 sec timing patch is structurally valid | timing patch probe and readback | YMM4 render/open behavior for patched copy | user |
| native voice fields are preserved in JSON readback | field preservation readback | audible/native voice survival after patched render | user then agent |
| external TTS remains closed | audio/TTS boundary and native audio path proof | none for this smoke unless render observation fails | agent after observation |

## Operator Observation Card

- target:
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
- absolute target in the current checkout:
  `C:\Users\PLANNER007\NLMYTGen\_tmp\newsroom_manual_probe\diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
- why: confirm that the 68 sec structural patch works on the real YMM4 render surface
- action: open the target `.ymmp` in YMM4 and render once
- look for:
  1. whether YMM4 opens the patched copy and render completes
  2. whether the output duration is about `68` sec
  3. whether the four dialogue lines and native Yukkuri voice are clearly still present
- answer style: freeform
- enough answer example: "render succeeded, about 68 sec, four lines and voice remain"
- not needed: fixed form, detailed sound-quality review, production-quality judgement,
  screenshots, or committing the `.ymmp`/mp4

## Post Observation Routing

| Observation | Next agent action |
|---|---|
| render succeeds, about 68 sec, four lines and voice remain | create `newsroom-ymmp-timing-patch-render-smoke-result-readback-v1` |
| render succeeds but remains about 8 sec | classify timing patch effectiveness |
| YMM4 cannot open the patched copy | classify `.ymmp` compatibility / timing field issue |
| render fails | classify render failure |
| about 68 sec but display or voice disappears | classify preservation regression |

## Boundaries

This handoff is only a restart and publication boundary. No YMM4 launch, render,
TTS/audio generation, real media import, production approval, `.ymmp` staging,
media staging, dashboard/governance/freshness change, or public-readiness claim
is performed here.

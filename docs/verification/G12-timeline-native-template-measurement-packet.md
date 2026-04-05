# G-12 Timeline Native-Template Measurement Packet

> Superseded by `docs/verification/G12-timeline-route-measurement.md`
> Historical note: the canonical G-12 conclusion is no longer "transition unresolved". Fade-family `transition` routes were later confirmed in repo-local corpus and fixed in the canonical packet.

> Purpose: narrow `motion` / `transition` / `bg_anim` write routes before any adapter write implementation
> Status: archived pre-lock snapshot
> Updated: 2026-04-06
> Owner split at the time: assistant = readback / contract / packet, user = YMM4 probe creation and final route decision

---

## Goal

`measure-timeline-routes` is already implemented. This packet turns it into a one-pass operator decision:

1. confirm which real ymmp routes already exist in the current corpus
2. lock provisional write routes for `motion` and `bg_anim`
3. isolate `transition` as the only remaining manual probe

This keeps G-12 as a bounded measurement packet instead of a broad timeline editing project.

---

## Current Route Status

| Category | Current status | Best confirmed route | Remaining risk |
|---|---|---|---|
| `motion` | corpus-confirmed | `TachieItem.VideoEffects` | route exists, but write semantics are still unimplemented |
| `bg_anim` | corpus-confirmed | `ImageItem.X/Y/Zoom` | route exists in production-like sample; direct edit semantics still need later implementation |
| `bg_anim` | template-rich probe confirmed | `ImageItem.VideoEffects` | available in probe/template sample, not yet proven in current production baseline |
| `transition` | historical pre-lock snapshot | `VoiceItem.Transition` or another transition key path was the working hypothesis at this point | superseded: canonical packet later confirmed fade-family `transition` routes from repo-local corpus |

---

## Measured Evidence

### 1. Production baseline

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/production.ymmp" --format json
```

Observed:

- `motion`: `TachieItem.VideoEffects`, `ShapeItem.VideoEffects`
- no `bg_anim`
- no non-fade `transition` route was recognized in this early snapshot

Interpretation:

- pure production baseline did not yet prove background animation or non-fade transition routes in this early snapshot

### 2. Production with BG proof

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/production_face_bg.ymmp" --format json
```

Observed:

- `motion`: `TachieItem.VideoEffects`, `ShapeItem.VideoEffects`
- `bg_anim`: `ImageItem.X/Y/Zoom`
- no non-fade `transition` route was recognized in this early snapshot

Interpretation:

- `ImageItem.X/Y/Zoom` is the strongest currently confirmed production-like route for `bg_anim`

### 3. Template-rich probe sample

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/Test_Template_00.ymmp" --format json
```

Observed:

- `motion`: `TachieItem.VideoEffects`
- `bg_anim`: `ImageItem.X/Y/Zoom`, `ImageItem.VideoEffects`
- no non-fade `transition` route was recognized in this early snapshot

Interpretation:

- `ImageItem.VideoEffects` is confirmed as a candidate route in a probe/template-oriented sample

### 4. Alternate probe sample

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/test - marisaFX.ymmp" --format json
```

Observed:

- `motion`: `TachieItem.VideoEffects`
- `bg_anim`: `ImageItem.X/Y/Zoom`, `ImageItem.VideoEffects`
- no non-fade `transition` route was recognized in this early snapshot

Interpretation:

- probe-side evidence matched `Test_Template_00.ymmp`; this strengthened `motion` and `bg_anim`, but still left `transition` unproven in this pre-lock snapshot

---

## Provisional Route Lock

These were the default G-12 working assumptions before fade-family `transition` routes were recovered mechanically.

| Category | Provisional lock | Why |
|---|---|---|
| `motion` | `TachieItem.VideoEffects` | appears consistently across production and probe samples |
| `bg_anim` | `ImageItem.X/Y/Zoom` | appears in production-like sample and is the safest current mechanical baseline |
| `bg_anim` optional | `ImageItem.VideoEffects` | probe-confirmed template route; useful when explicit template/effect behavior is desired |
| `transition` | not locked in this snapshot | later superseded by fade-family route detection in the canonical packet |

Important boundary:

- this packet locks route candidates, not final creative defaults
- final effect/template choice remains human-owned
- this archived boundary was later relaxed once fade-family `transition` routes were recovered from repo-local corpus

---

## Contract Files

Prepared assets:

- `samples/g12_expect_production_motion_bg.json`
- `samples/g12_expect_template_probe.json`
- `samples/g12_expect_transition_probe.json`

Recommended checks:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/production_face_bg.ymmp" --expect "samples/g12_expect_production_motion_bg.json"
uv run python -m src.cli.main measure-timeline-routes "samples/Test_Template_00.ymmp" --expect "samples/g12_expect_template_probe.json"
```

Notes:

- both commands should pass if the current route assumptions remain true
- `samples/g12_expect_transition_probe.json` is intentionally for a future YMM4-made probe and is not expected to pass against the current corpus

---

## Manual Frontier: Transition Probe

At this historical point, the only remaining G-12 blocker was a real transition sample.

### User task

Create one minimal YMM4 sample, for example `samples/g12_transition_probe.ymmp`, containing:

- one item with an explicit transition set in YMM4
- only the minimum layers/items needed to save the file
- one clear route choice, not multiple experimental edits in the same file

### Then run

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/g12_transition_probe.ymmp" --format json
uv run python -m src.cli.main measure-timeline-routes "samples/g12_transition_probe.ymmp" --expect "samples/g12_expect_transition_probe.json"
```

### Decision rule

- if the probe exposes a stable route such as `VoiceItem.Transition`, lock that as the G-12 transition route
- if the probe exposes a different stable key path, update the contract and lock that instead
- if multiple routes appear, prefer the smallest deterministic path that survives readback

---

## Packet Completion Criteria

This archived packet treated G-12 as complete when all of the following were true:

1. `motion` route is locked from real ymmp evidence
2. `bg_anim` route is locked from real ymmp evidence
3. `transition` route is confirmed from one explicit YMM4 probe sample
4. accepted and rejected routes are recorded in docs before any write adapter work begins

This archived packet is kept only as a historical narrowing step. Use `docs/verification/G12-timeline-route-measurement.md` for current decisions.

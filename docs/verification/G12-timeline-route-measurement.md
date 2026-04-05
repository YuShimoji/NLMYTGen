# G-12 Timeline Route Measurement

> Date: 2026-04-06
> Scope: `motion` / `transition` / `bg_anim`
> Method: `measure-timeline-routes` + `--expect`

## Goal

`motion` / `transition` / `bg_anim` をいきなり patch 実装せず、
まず ymmp 上でどの write route が実在するかを readback で固定する。

## Repo-local contract

Contract file:
`samples/timeline_route_contract.json`

Profiles:

- `motion_only`
- `motion_bg_anim_minimal`
- `motion_bg_anim_effects`

Meaning:

- `motion_only`: tachie motion route only
- `motion_bg_anim_minimal`: motion + background transform route
- `motion_bg_anim_effects`: motion + background transform + background VideoEffects
- `transition`: repo-local corpus では fade-family route (`VoiceFade*` / `JimakuFade*` / `Fade*`) として観測される

## Measured samples

### 1. `samples/global_crisis_patched.ymmp`

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes `
  "samples/global_crisis_patched.ymmp" `
  --expect "samples/timeline_route_contract.json" `
  --profile motion_only
```

Result:

- pass
- observed `motion`: `TachieItem.VideoEffects`
- observed `transition`: `VoiceItem.VoiceFadeIn/Out`, `VoiceItem.JimakuFadeIn/Out`, `TachieItem.FadeIn/Out`
- `bg_anim` / `template` are optional-miss only

Interpretation:

- current motion-only contract is realistic for a production-adjacent repo-local ymmp
- `motion` and fade-family `transition` can be treated as measurable categories, not speculative ones

### 2. `samples/production_face_bg.ymmp`

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes `
  "samples/production_face_bg.ymmp" `
  --expect "samples/timeline_route_contract.json" `
  --profile motion_bg_anim_minimal
```

Result:

- pass
- observed `motion`: `TachieItem.VideoEffects`
- observed `bg_anim`: `ImageItem.X/Y/Zoom`
- observed `transition`: `VoiceItem.VoiceFadeIn/Out`, `VoiceItem.JimakuFadeIn/Out`, `TachieItem.FadeIn/Out`
- `ImageItem.VideoEffects` is still optional-miss only

Interpretation:

- minimal `bg_anim` contract is realistic for a repo-local production sample
- `ShapeItem.VideoEffects` exists as an extra candidate, but is not yet canonical
- transition route no longer needs a separate repo-local probe to prove existence

### 3. `samples/test_verify_4_bg.ymmp`

Command:

```powershell
uv run python -m src.cli.main measure-timeline-routes `
  "samples/test_verify_4_bg.ymmp" `
  --expect "samples/timeline_route_contract.json" `
  --profile motion_bg_anim_effects
```

Result:

- pass
- observed `motion`: `TachieItem.VideoEffects`
- observed `bg_anim`: `ImageItem.X/Y/Zoom`, `ImageItem.VideoEffects`
- observed `transition`: `VoiceItem.VoiceFadeIn/Out`, `VoiceItem.JimakuFadeIn/Out`, `TachieItem.FadeIn/Out`, `ImageItem.FadeIn/Out`

Interpretation:

- stronger `bg_anim` contract with VideoEffects is realistic in repo-local measurement fixtures
- effect-bearing background templates can be distinguished from minimal background transforms
- image fade routes also exist in repo-local probe samples

## Current G-12 state

- readback harness: done
- repo-local route contract with profiles: done
- sample-based route gap detection: done
- fade-family transition route detection: done
- native route fixed for implementation: measurement packet complete

## Next action

1. Move to G-13 and define deterministic timing anchor / insertion structure for `overlay` / `se`.
2. Re-open `transition` only when a non-fade or template-backed transition family appears in a new repo-local sample.
3. Decide later whether `ShapeItem.VideoEffects` belongs in the contract as a secondary motion route.

## Corpus-wide audit

Repo-local `.ymmp` files measured on 2026-04-06: 16

Observed result:

- fade-family `transition` route: observed in production and probe samples
- `template` route: 0

Interpretation:

- this is not a visual-quality problem
- this is not an operator judgement wait state
- the remaining dependency is only non-fade or template-backed transition families
- G-12 can be treated as complete because the measurement packet answered the current in-repo question

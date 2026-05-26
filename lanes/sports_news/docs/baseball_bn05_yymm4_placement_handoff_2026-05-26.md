# Baseball BN-05 YMM4 placement contract handoff (2026-05-26)

This handoff continues the Baseball sidequest without changing the G-27
mainline or writing a YMM4 project file.

## Current position

- Branch: `codex/baseball-bn02-visual-data`
- Prior checkpoint: BN-03 static PNG export at `c40462d`
- BN-05 scope: connect the BN-03 PNG to a YMM4 placement contract only.
- Out of scope: `.ymmp` write, render proof, creative acceptance, animation
  export, real episode source replacement, publish gate.

## What BN-05 fixes

| Asset | Role |
| --- | --- |
| `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_contract.json` | Defines the ImageItem placement for the BN-03 PNG. |
| `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_readback.json` | Records mechanical checks for hashes, timing, item type, and boundaries. |
| `samples/_probe/baseball/static/baseball_pitch_event_p05.png` | Source visual asset placed by the contract. |

The contract places the static PNG on the screen-plan `pitch_event_breakdown`
span (`00:26-00:48`) as an `ImageItem`, using a 60fps timeline:

- start frame: `1560`
- length: `1320`
- end frame: `2880` exclusive
- proposed layer: `12`
- canvas: `1920x1080`
- zoom: `150%` to fit the 1280x720 PNG to full-frame 16:9

This is a placement contract and preview gate, not proof that YMM4 has rendered
or accepted the asset.

## Manual preview gate

The next YMM4-facing check should return one preview screenshot plus a PASS/FIX
note. PASS means:

- the infographic fills the 16:9 frame without crop;
- scoreboard, strike zone, pitch log, and current pitch claim remain readable;
- subtitles or narrator layers do not obscure the pitch claim;
- the item starts at `00:26` and clears at `00:48`.

FIX means crop, text size, layer overlap, or timing drift is visible. A FIX
result should tune this placement contract before any render or creative
acceptance claim.

## BN-04 animation design bridge

BN-04 is not implemented here, but its first contract is now recorded in
`samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_export_plan.json`.
The default is `frame_sequence_first`, not clip-first, because frame hashes and
per-frame readback are easier to verify before YMM4 placement.

## Next entry points

| Entry | Reduces | Enables |
| --- | --- | --- |
| Verify BN-05 preview | Crop, readability, and layer collision uncertainty | Decide whether placement is usable before `.ymmp` write automation. |
| Implement BN-05 insertion proof | Manual ImageItem placement drift | Generate or patch a minimal YMM4 proof from this contract. |
| Implement BN-04 frame sequence capture | Animation export uncertainty | Produce hashed frames and later decide whether clip export is needed. |
| Audit real source replacement | Sample-only confidence gap | Prepare to swap `sample://` data for real sourced episode facts. |

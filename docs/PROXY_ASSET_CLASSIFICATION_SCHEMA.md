# Proxy / Asset Classification Schema

Purpose: classify visual treatment proof beats before they are consumed by
scene decision packets, asset/proxy gap reports, or YMM4 adapter planning.

This artifact is a gate, not a design-polish surface. It does not create a new
visual proof, decide final scene acceptance, inventory all missing assets, write
YMM4 output, render video, or perform creative acceptance.

## Position In The Pipeline

Input:

- Script Beat IR / Shot Layout Plan / Motion Beat Plan context.
- Visual treatment proof sidecar.
- Proof readback.

Output:

- One classification row per beat.
- A rollup of rows that are assistant-ready, need user proxy/asset decisions, or
  are blocked for downstream work.

Allowed next consumers:

- `scene decision packet`
- `asset-proxy gap report`
- `YMM4 adapter`

The classification may point to one of those consumers, but it must not produce
that consumer artifact in the same step unless a later task explicitly asks for
it.

## Required Beat Fields

| field | type | meaning |
| --- | --- | --- |
| `segment_id` | string | Stable segment id such as `RE-02`. |
| `beat_id` | string | Stable beat id such as `RE-02-beginning`. |
| `phase` | string | Beat phase when available, for example `beginning`, `development`, or `turn`. |
| `meaning_payload` | string | The narrative meaning the beat must carry. |
| `current_proxy_visual` | string | What the current proof uses to express the beat. |
| `required_production_representation` | string | What a production-bound version must represent, independent of the proof styling. |
| `representation_type` | enum | One of `existing proxy`, `new abstract proxy`, `real asset`, `YMM4 primitive`, `blocked`. |
| `asset_categories` | enum array | One or more of `character`, `UI`, `document`, `map`, `property card`, `risk marker`, `subtitle`, `motion`, `background`. |
| `rights_risk` | enum | One of `none`, `low`, `needs review`. |
| `YMM4_feasibility` | enum | One of `easy`, `medium`, `hard`, `unknown`. |
| `blocker_reason` | string | Empty or `none` when not blocked; otherwise the concrete reason downstream cannot proceed cleanly. |
| `user_decision_needed` | string | The exact user decision needed, or `none`. |
| `assistant_can_advance` | boolean | Whether an assistant can later route this beat to the named next consumer without another creative/proxy decision. |
| `next_consumer` | enum | One of `scene decision packet`, `asset-proxy gap report`, `YMM4 adapter`. |

Optional fields may be added for source paths, notes, or machine checks, but the
required fields above must remain stable.

## Enum Semantics

`existing proxy` means the current proof proxy can be carried forward as a
production representation candidate without inventing a new visual vocabulary.

`new abstract proxy` means the meaning is valid, but a reusable abstract proxy
must be named or approved before production planning treats it as stable.

`real asset` means a concrete source asset is needed, such as a licensed image,
official document, map, or real UI reference. This usually carries rights review.

`YMM4 primitive` means the representation can be expressed with existing YMM4
shapes, text, movement, masks, or simple effects without a separate asset.

`blocked` means the beat cannot safely pass downstream until the blocker is
resolved. Blocked is not failure; it is a routing state.

## Boundary Checks

A valid classification artifact must state that it is not:

- G-27 v3 proof.
- Scene decision packet.
- Asset/proxy gap report.
- YMM4 conversion.
- Render source.
- Production timing.
- Creative acceptance.

If any row points to `YMM4 adapter`, it still must not write adapter output in
the same step. The row only says that the beat is likely adapter-ready after the
proper upstream gates pass.

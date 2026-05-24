# Real Estate DX Micro Video Scene Probe

Probe: `samples/_probe/g24/real_estate_dx_micro_scene_probe.ymmp`
Source compact review: `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json`

This bounded probe converts the G-27 visual proxy from a 7-candidate catalog into one short 4-beat narrative scene. It uses only ShapeItem/TextItem primitives from existing G-27 material. It is not rendered, not creative acceptance, and not production-ready.

## Rollup

- Readback status: `passed`
- Timeline duration: `60` sec
- Inserted items: `54` (ShapeItem=`38`, TextItem=`16`)
- Color-like scan failures: `0`
- Carrier modified in place: `false`

## Beat Table

| beat | candidate | narrative intent | visual composition | on-screen copy | why it avoids slideshow / whiteboard effect |
| --- | --- | --- | --- | --- | --- |
| `micro-01-access-contrast` | `RE-02-development` | Viewer understands that the same market has a public entrance and a deeper professional database, so visible information is structurally limited. | A large dark broker database slides into dominance behind a smaller public portal; a lock threshold appears between them and only a thin output card escapes. | 情報の入口が違う / 公開 / 業者DB / LOCK | The beat is staged as a door/threshold event with one focal split-screen system, not as separate note cards explaining the concept. |
| `micro-02-selection` | `RE-06-development` | Viewer understands that the service narrows many options into one recommended property while keeping the drawback visible. | Rejected cards slide to the edges, one property sheet remains center stage, and a warning callout attaches to the selected sheet. | 比較して一つ選ぶ / 候補 / 選定 / 注意点 | The screen is a selection event: cards are spatially rejected, one sheet is framed, and the drawback is attached to the chosen object. |
| `micro-03-ai-match` | `RE-07D-beginning` | Viewer understands that an AI-like system can confidently highlight one property as the best match. | A dark AI system panel scans, a match arrow fires, and a single property card becomes the focal target with a confidence badge. | AIが候補を選ぶ / AI / MATCH / 物件 | The beat is a scanning and targeting event with one highlighted card, not a board of explanatory labels. |
| `micro-04-conditional` | `RE-07D-development` | Viewer understands that the AI recommendation is not final because hidden real-estate risks interrupt it and make the choice conditional. | The matched property remains in the center, then red/yellow risk zones cover it and a dark conditional strip overrides the previous recommendation. | 推薦は条件つき / 境界 / 相続 / 周辺 | The beat uses interruption and occlusion: risk zones physically cover the recommendation instead of listing risk notes beside it. |

## Candidate Selection

- Selected candidates: `RE-02-development, RE-06-development, RE-07D-beginning, RE-07D-development`
- Not selected in this micro scene: `RE-02-beginning, RE-06-beginning, RE-06-turn`
- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.

## Completion Position

- Technical openability: machine structure is ready for user-side YMM4 GUI readback.
- Semantic proxy: local readback separates narrative intent, visual composition, and minimal on-screen copy.
- Video adequacy: not proven until GUI review confirms it feels like a short scene rather than another board.
- Production readiness: no. No render, production timing, creative acceptance, external assets, URL fetch, TTS, or publishing.
- Minimal render smoke recommendation: `ready_for_user_gui_readback_before_minimal_render_smoke`.

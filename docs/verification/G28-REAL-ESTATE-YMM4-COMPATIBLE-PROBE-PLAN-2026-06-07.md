# G-28 Real Estate YMM4-Compatible Probe Plan - 2026-06-07

This plan defines a later self-contained YMM4-compatible diagnostic probe for
the accepted G-28 `real_estate_information_gap` Lecture Diagram Carrier. It is a
probe plan only. It does not generate a YMM4 project, render output, approve a
production carrier, approve creative final acceptance, or change the existing
generator / JSON / HTML / readback / report artifacts.

## Probe Objective

- Advance the accepted `real_estate_information_gap` diagnostic direction toward
  a later YMM4-compatible self-contained diagnostic probe.
- Preserve the Lecture Diagram Carrier contract: one central mechanism, a
  3-node focal chain, 3 bounded callout slots, lower-corner non-focal hosts, and
  a bottom caption reserve.
- Keep the subject abstract: "real-estate information asymmetry mechanism", not
  a real property, real service, real listing, real portal capture, or source
  footage surface.
- Confirm what a later YMM4-openable probe must contain before any `.ymmp` work
  is opened.

This is not production carrier approval, creative final acceptance, render
approval, slot-fill approval, rights approval, or publishing approval.

## Target Artifact

| Field | Value |
| --- | --- |
| artifact_id | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` |
| variant_id | `g28_ldc_real_estate_information_gap` |
| source JSON | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.json` |
| source readback | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_readback.json` |
| source report | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_report.md` |
| source HTML visualization | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.html` |
| human decision | `accept_as_diagnostic_direction` |
| readback status | `passed` |
| diagnostic_only | `true` |
| production_candidate | `false` |
| composition_type | `center-focal` |
| frame | `1920x1080 / 16:9` |
| caption reserve | bottom 20%, clear |

## Intended YMM4 Item / Group Mapping

The later probe should be self-contained and shapes/text only. Names should
preserve the current G-28 diagnostic mapping so readback can compare JSON, HTML,
and YMM4-compatible output without semantic drift.

| Planned group | Intended YMM4-compatible contents | Role | Notes |
| --- | --- | --- | --- |
| `G28_LDC_Stage` | background ShapeItem plus safe-frame guide if needed | decoration | Low-salience stage only. No external image. |
| `G28_LDC_TitleBand` | title-band ShapeItem and `G28_LDC_Title_Text` | label | One short title such as `情報非対称の流れ`. |
| `G28_LDC_FocalGroup` | focal core ShapeItem, node ShapeItems, node labels, connector ShapeItems | focal_anchor | Reads as one mechanism diagram, not equal-weight cards. |
| `G28_LDC_FocalNodes` | labels `元付情報`, `ポータル掲載`, `借主判断` | focal_chain | 3 nodes only. No fourth node or table row expansion. |
| `G28_LDC_Connectors` | left/right arrows or connector bars | connector | Show flow across the 3-node chain. |
| `G28_LDC_CalloutSlots` | 3 ShapeItem callout containers with short labels | supporting | `情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`. |
| `G28_LDC_Hosts` | lower-left and lower-right placeholder ShapeItems | decoration | Emotional anchor only; not evidence and not focal. |
| `G28_LDC_CaptionReserve` | readback-reserved bottom band, optional guide marker | caption_reserve | Bottom 20% remains clear of carrier content. |
| diagnostic sidecar | machine-readable metadata, outside visual proof if needed | metadata | Stores `diagnostic_only=true` / `production_candidate=false`; not production text. |

If a later YMM4-compatible probe cannot safely represent a planned label as
visible text while staying within budget, the label should be moved to readback
metadata rather than expanding the frame into a dense table.

## Layer Order

The later probe should preserve this order:

1. stage / background
2. title band and title text
3. focal core
4. focal node labels
5. connectors / arrows
6. callout group
7. hosts
8. caption reserve marker / readback check
9. optional diagnostic labels or sidecar metadata

The caption reserve marker, if visualized, is a diagnostic guide only. It must
not become a production subtitle design or a claim of subtitle layout approval.

## YMM4 Compatibility Constraints

- Use shapes and text only.
- Use no external images, source footage, screenshots, real map surfaces, real
  service captures, real property material, or rights-bearing assets.
- Use no URL, raw reference intake, TTS, audio item, voice item, render, or video
  output.
- Keep `diagnostic_only=true` and `production_candidate=false`.
- Do not set or automate `rights_status`.
- Avoid fragile YMM4 fields unless already proven in repo-local docs.
- Prefer `ShapeParameter.SizeMode=WidthHeight` and absolute frame coordinates.
- Preserve YMM4-compatible color string conventions such as `#AARRGGBB` where a
  later `.ymmp` writer needs color values.
- Do not use plugin-specific TachieItem setup, external FilePath fields, deep
  nested groups, animation/effect stacks, or timing/audio features for this
  static diagnostic probe.
- Do not create a new G-28 variant, modify the existing generator, or rewrite the
  existing generated JSON / HTML / readback / report in this planning slice.

## Readback Requirements For Later Probe Slice

A later implementation slice must produce machine readback that reports:

- YMM4-compatible artifact exists and is self-contained.
- `diagnostic_only=true`.
- `production_candidate=false`.
- `external_image_count=0`.
- `external_url_count=0`.
- `source_footage_count=0`.
- `audio_item_count=0`.
- `tts_or_voice_item_count=0`.
- `render_output=false`.
- `creative_final_acceptance=false`.
- `caption_reserve_clear=true`.
- `focal_chain_nodes=3`.
- focal chain labels read as `元付情報 -> ポータル掲載 -> 借主判断`.
- `callout_count=3`.
- callout labels read as `情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`.
- `host_role=non_focal`.
- layer order matches this plan.
- `dense_table=false`.
- `indexed_whiteboard=false`.
- no unintended real-service or real-property visual surface.

If any of these checks fail, the result remains diagnostic failure or revision
input. It must not be promoted to production by fallback interpretation.

## Human GUI Check Checklist

When a later probe artifact exists, human GUI review should answer only these
diagnostic questions:

- Does YMM4 open the probe without error?
- Is the focal chain readable as `元付情報 -> ポータル掲載 -> 借主判断`?
- Is the bottom caption reserve visually preserved?
- Are the three callouts readable without becoming a dense list or table?
- Do the hosts stay lower-corner, non-focal, and non-evidence-like?
- Does the surface avoid looking like a real listing, real portal, real service,
  or real property proof?
- Is the diagnostic-only boundary visible in the docs/readback?
- Is there no implied production usage, render approval, rights approval, or
  creative final acceptance?

The GUI check is not a request for production rendering. A pass means only that
the self-contained diagnostic probe can serve as a later review surface.

## Next Slice Options

| Option | Meaning | Allowed next work |
| --- | --- | --- |
| `proceed_to_self_contained_ymmp_probe` | Human wants the first YMM4-compatible diagnostic probe. | Create the minimal self-contained probe and readback in a separate explicit slice. |
| `revise_probe_plan` | Plan needs a mapping, density, or checklist correction. | Update this plan only. |
| `defer_until_review_console_ingest` | Probe should wait for a broader review surface. | Keep this plan as pending context; no artifact generation. |
| `reject_probe_path` | This diagnostic direction should not proceed toward YMM4 probe. | Record rejection reason; do not promote the artifact. |

## Boundaries

- No `.ymmp` generation in this slice.
- No render or video output.
- No production carrier approval.
- No creative final acceptance.
- No rights automation or `production_candidate=true`.
- No G-27 revival or G-27 diagnostic carrier promotion.
- No new G-28 variant.
- No generator change.
- No common foundation or Codex Worker Orchestration work.
- No ClipPipeGen access.
- No external image, URL, raw reference, source footage, real listing, real
  property, or real map intake.
- No RSS / OPML / Inoreader / NotebookLM source-pack work.

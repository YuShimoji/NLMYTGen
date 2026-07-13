# Generic Visual Capabilities — evidence-graded envelope

> **INTERNAL / STATIC CONFORMANCE / NOT PRODUCTION / NOT C5**

This is the primary delivery surface for the generic visual capability audit.
It extends the existing [Scene Composition Schema](../SCENE_COMPOSITION_SCHEMA.md)
without replacing it: a `layout_archetype` describes the explanatory recipe,
while `scs_composition_type` selects the existing frame geometry.

## Delivery answer

- **Can be used now, inside observed boundaries:** VoiceItem plus linked-subtitle
  import, observed cue timing, a no-transition baseline, selected named
  GroupItem motion/templates, one exact Voice/Image/Text diagnostic combination,
  and strict media validation for one exact internal render.
- **Only statically materialized:** generic ImageItem/TextItem/ShapeItem candidates,
  arbitrary transforms, fades, overlays, background replacement/pan/zoom,
  motion recipes, Shape/Text callouts, and this three-fixture composition lab.
- **Requires YMM4 observation:** any new Text/Image/Shape layout, subtitle
  readability, callout anchors, fades, background motion, zoom, opacity, or any
  Route A motion profile.
- **Requires render evidence:** a claim that a project produces valid media.
  C4 additionally requires container/probe/decode verification; valid media still
  does not prove semantic or visual quality.
- **Unsupported now:** non-fade transitions, generic ShapeItem creation in the
  patch core, generic speech balloons, automatic external-asset acquisition, and
  reuse of the failed older card surface as a production design system.
- **Unknown:** Route A runtime motion, linked-subtitle visual layout,
  cross-machine portability, and C5 real cross-topic core reuse.

## Evidence counts

| Dimension | Count |
| --- | ---: |
| Relevant paths classified | 78 |
| Unclassified relevant paths | 0 |
| Capabilities | 38 |
| Proven | 15 |
| Conditional | 14 |
| Unsupported | 5 |
| Unknown | 4 |
| C0 / C1 / C2 / C3 / C4 / C5 | 5 / 3 / 14 / 14 / 2 / 0 |

`proven` is used only at C3 or stronger. `render_proven` is used only at C4.
No current record is `cross_topic_proven` because C5 evidence does not exist.
All matrix/ledger evidence references and the generic core, machine package,
focused test, fixtures and readback are included in the classified inventory.

## Capability matrix

| Capability | Class | Level | Practical use now | Main boundary / fallback | Cost / reuse |
| --- | --- | ---: | --- | --- | --- |
| `voice_linked_subtitle_import` | proven | C3 | narration and cue baseline | observed profiles only; fail import gate | W1 / broad |
| `voiceitem_preserving_project_augmentation` | proven | C3 | preserve narration while adding bounded diagnostics | fixed pilot only; rebuild from import base | W2 / archetype |
| `exact_voice_image_text_project_open` | proven | C3 | exact same-machine 9/3/3 diagnostic | not variable or portable; voice-only fallback | W2 / topic |
| `card_image_visibility_with_dialogue` | proven | C3 | bounded precomposed card overlay | not C4; single panel fallback | W2 / archetype |
| `observed_frame_length_timing` | proven | C3 | cue-relative timing anchors | no production pacing claim | W1 / broad |
| `observed_layer_assignment` | proven | C3 | sparse known layer roles | no generic allocator; known profile fallback | W2 / archetype |
| `group_xy_zoom_motion` | proven | C3 | named GroupItem movement | template-specific; static hold | W2 / archetype |
| `group_rotation_bounce_motion` | proven | C3 | bounded named nod/emphasis | no arbitrary tilt/parallax; static expression | W2 / archetype |
| `fixed_text_style_readability` | proven | C3 | short fixed diagnostic labels | no typography engine; shorten/bake text | W1 / archetype |
| `named_template_reuse` | proven | C3 | observed named template families | missing template/asset fails closed | W2 / archetype |
| `expression_swap` | proven | C3 | tracked expression accent | asset-specific; neutral face fallback | W2 / archetype |
| `no_transition_baseline` | proven | C3 | default hard-cut/static baseline | pacing still human judgment | W1 / broad |
| `selected_effect_presets` | proven | C3 | named observed preset only | plugin/compatibility risk; no effect | W3 / archetype |
| `decoded_internal_render` | proven | C4 | milestone media verification | no semantic/visual acceptance; retain static evidence | W4 / topic |
| `decoded_review_proxy` | proven | C4 | smaller review derivative | no YMM4 semantic proof | W2 / broad |
| `static_imageitem_materialization` | conditional | C2 | local image candidate | runtime/path/rights unproven; omit image | W2 / broad |
| `static_textitem_materialization` | conditional | C2 | short-label candidate | wrapping/anchor unproven; linked subtitle | W2 / broad |
| `static_shapeitem_materialization` | conditional | C2 | topic probe only | no generic builder; precomposed image | W3 / topic |
| `arbitrary_item_transform_fields` | conditional | C2 | serialize transform routes | visibility/continuity unproven; static defaults | W3 / broad |
| `scale_zoom_transform` | conditional | C2 | bounded probe candidate | crop/anchor unproven; zoom 100 | W2 / broad |
| `opacity_transform` | conditional | C2 | bounded probe candidate | blend/result unproven; opacity 100 | W2 / broad |
| `background_layer_replacement` | conditional | C2 | same-machine static background | no generic open proof; one known background | W2 / broad |
| `background_pan_zoom` | conditional | C2 | probe candidate only | no isolated observation; static background | W3 / broad |
| `overlay_imageitem_insertion` | conditional | C2 | precomposed overlay candidate | runtime/layout unproven; no overlay | W2 / broad |
| `fade_transition_fields` | conditional | C2 | post-probe optional fade | fields are not behavior; hard cut | W2 / broad |
| `motion_recipe_materialization` | conditional | C2 | named recipe project candidate | runtime and plugin risk; static pose | W4 / archetype |
| `shape_text_callout_materialization` | conditional | C2 | one-off static probe | high repair cost; short label/image | W4 / topic |
| `audioitem_se_materialization` | conditional | C2 | outside minimum visual stack | playback/rights/mix unproven; no SE | W3 / archetype |
| `static_cross_archetype_conformance` | conditional | C2 | preflight recipes/data | not YMM4 or C5; reject/lower recipe | W1 / broad |
| `route_specific_motion_profiles` | unknown | C0 | do not use in H0 | one generic probe or static fallback | W4 / topic |
| `cross_machine_project_portability` | unknown | C0 | same-machine only | regenerate/rebind paths | W3 / broad |
| `real_cross_topic_core_reuse` | unknown | C0 | no current claim | second real topic without core edits | W5 / broad |
| `linked_subtitle_typography_layout` | unknown | C0 | reserve safe area only | YMM4/human visual review | W2 / broad |
| `external_asset_auto_fetch` | unsupported | C0 | do not build in core | cleared local or original abstract asset | W5 / topic |
| `nonfade_transition` | unsupported | C1 | not available | hard cut or conditional fade | W4 / broad |
| `generic_shapeitem_creation_core` | unsupported | C1 | not available | precomposed image or known template | W4 / broad |
| `generic_speech_balloon` | unsupported | C1 | not available | narration or short TextItem | W4 / archetype |
| `production_quality_card_composition` | unsupported | C3 negative | do not reuse old surface | sparse single-focus scene | W5 / topic |

Full evidence locations, environments, failure modes and overclaim boundaries are
in [generic_visual_capability_matrix.json](generic_visual_capability_matrix.json)
and [capability_evidence_ledger.json](capability_evidence_ledger.json).

## Composition map

| Recipe | SCS geometry | Required baseline | Whole floor / static conformance | Default fallback | Cost / reuse |
| --- | --- | --- | ---: | --- | --- |
| `narration_baseline` | `center-focal` | Voice + linked subtitle + caption reserve | C0 / C2 | itself | W1 / broad |
| `inspection_explanation` | `center-focal`, `reveal` | narration + reserve + static focus | C0 / C2 | narration baseline | W2 / archetype |
| `process_sequence` | `chain`, `mediator` | narration + reserve + connector | C0 / C2 | narration baseline | W2 / broad |
| `comparison_contrast` | `split`, `mediator` | narration + reserve + comparison panels | C0 / C2 | narration baseline | W2 / broad |
| `callout_focus` | `center-focal`, `reveal` | narration + reserve + static focus | C0 / C2 | inspection explanation | W3 / archetype |
| `recap_action_sequence` | `chain`, `center-focal` | narration + reserve + connector | C0 / C2 | narration baseline | W2 / broad |

The grammar prohibits equal-weight card grids, excess simultaneous nodes or
callouts, unobserved motion without a static fallback, and domain geometry in
the core. Detailed rules are in
[scene_composition_grammar.json](scene_composition_grammar.json).
The whole-composition floor is C0 because every recipe reserves subtitle space
through the still-unknown `linked_subtitle_typography_layout` capability. The
fixtures themselves are deterministic C2 schema evidence, while the narration
import subpath remains C3; neither stronger subpath upgrades the complete layout.

## Cross-archetype conformance

All fixtures use `validate_fixture` from one generic module. No fixture-name or
Route-specific branch exists.

| Fixture | Domain role | Scenes | Cues | Result | Runtime claim |
| --- | --- | ---: | ---: | --- | --- |
| Route A inspection | selected data-only conformance fixture | 3 | 9 | static pass with 20 derived/explicit gaps | none |
| Synthetic process | unrelated fictional workflow | 4 | 5 | static pass with 5 subtitle-layout gaps | none |
| Synthetic comparison | unrelated fictional two-side contrast | 2 | 4 | static pass with 4 subtitle-layout gaps | none |

Route A retains exact text, evidence references, timing metadata, factual
boundaries, palette/object proposals and motion labels in fixture payload only.
Its original packet remains read-only and `implementation_authorized=false`.

## Evidence-derived minimum generic stack

The recommended default is
`minimum_static_narration_visual_stack_v1`:

1. C3 VoiceItem + linked subtitle import.
2. C3 observed cue-relative Frame/Length anchors.
3. C3 no-transition baseline.
4. Optional C2 static local ImageItem after path/rights checks.
5. Optional C2 short TextItem; otherwise linked subtitle only.
6. C2 generic fixture preflight before project generation.
7. Motion off by default. At most one named C3 GroupItem accent after a real
   scene justifies it.
8. C0 linked-subtitle typography/layout remains a required gate before visual
   acceptance; reserve space and make no readability claim until observation.

This is W2 setup, low per-episode burden, small maintenance surface, optional
rights dependency, and easy recovery. The recommendation artifact is C2, but
the complete visual stack has a C0 evidence floor until subtitle layout is
observed. “Broad reuse” remains a hypothesis until C5. See
[recommended_minimum_generic_stack.json](recommended_minimum_generic_stack.json).

## Expensive, fragile, or not worth building now

- Generic Shape/Text callouts: W4, topic-specific repair history, no generic C3.
- Background pan/zoom: W3, C2 only, crop/anchor behavior not isolated.
- Routine render validation: W4/high burden; keep for real milestones.
- Speech balloons and non-fade transitions: no recurring evidence that they
  beat the narration/short-label/hard-cut fallback.
- Automatic external assets: W5 rights/privacy/reproducibility burden belongs
  outside the generic core.
- A bundle of Route-specific motion profiles: probe one generic primitive first.

## Remaining generalization gate

H1 may observe a **small generic capability probe**, not the final Route A
project. C5 remains closed until a second heterogeneous real episode uses this
same core with data/config changes only, no core-code changes, and the evidence
and cost classifications still hold.

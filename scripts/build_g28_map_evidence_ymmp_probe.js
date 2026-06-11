// G-28 Map / Evidence Carrier YMM4-compatible diagnostic probe.
// Builds a self-contained ShapeItem/TextItem-only .ymmp from the accepted
// Map / Evidence diagnostic skeleton. This is review-only and does not render,
// approve production, ingest external assets, or use real map/source material.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  sourceJson: 'samples/_probe/g28/map_evidence_carrier_skeleton.json',
  sourceReadback: 'samples/_probe/g28/map_evidence_carrier_skeleton_readback.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp',
  outputYmmp: 'samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp',
  readbackJson: 'samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_readback.json',
  reportMd: 'samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_report.md',
};

const FRAME = { width: 1920, height: 1080 };
const DURATION_FRAMES = 600;
const shapeSizeMode = 'WidthHeight';
const sourceArtifactId = 'g28_map_evidence_carrier_skeleton_v1';
const probeArtifactId = 'g28_map_evidence_carrier_ymmp_probe_v1';
const carrierKind = 'map_evidence_carrier';
const variant = 'map_evidence';

const creationRecord = {
  revision_id: 'g28_map_evidence_ymmp_diagnostic_probe_v1',
  source_decision: 'advance_speed_first_after_game_mechanics_layout_system_debt',
  classification: 'pass_map_evidence_ymmp_diagnostic_carrier_created',
  boundary_note: 'Diagnostic-only YMM4 carrier candidate; no real map, image, URL, source footage, audio, TTS, render, production approval, rights approval, or creative final acceptance.',
};

function abs(rel) {
  return path.join(root, rel);
}

function readText(rel) {
  return fs.readFileSync(abs(rel), 'utf8').replace(/^\uFEFF/, '');
}

function readJson(rel) {
  return JSON.parse(readText(rel));
}

function writeJson(rel, payload) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function writeMarkdown(rel, markdown) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), markdown, 'utf8');
}

function writeYmmp(rel, payload) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), `\uFEFF${JSON.stringify(payload, null, 2)}`, 'utf8');
}

function sha256(rel) {
  return crypto.createHash('sha256').update(fs.readFileSync(abs(rel))).digest('hex');
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function animation(value) {
  return {
    Values: [{ Value: value }],
    Span: 0,
    AnimationType: 'なし',
    Bezier: {
      Points: [
        {
          Point: { X: 0, Y: 0 },
          ControlPoint1: { X: -0.3, Y: -0.3 },
          ControlPoint2: { X: 0.3, Y: 0.3 },
        },
        {
          Point: { X: 1, Y: 1 },
          ControlPoint1: { X: -0.3, Y: -0.3 },
          ControlPoint2: { X: 0.3, Y: 0.3 },
        },
      ],
      IsQuadratic: false,
    },
  };
}

function itemType(item) {
  return String(item?.$type || '').split(',')[0].split('.').pop();
}

function findFirstItemByType(ymmp, typeName) {
  const timelines = Array.isArray(ymmp.Timelines) ? ymmp.Timelines : [];
  for (const timeline of timelines) {
    const items = Array.isArray(timeline.Items) ? timeline.Items : [];
    const found = items.find((item) => itemType(item) === typeName);
    if (found) return found;
  }
  return null;
}

function setAnimatedValue(item, key, value) {
  if (!item[key] || typeof item[key] !== 'object') {
    item[key] = animation(value);
    return;
  }
  if (!Array.isArray(item[key].Values) || item[key].Values.length === 0) {
    item[key].Values = [{ Value: value }];
    return;
  }
  item[key].Values[0].Value = value;
}

function setShapeParameterValue(shapeItem, key, value) {
  if (!shapeItem.ShapeParameter || typeof shapeItem.ShapeParameter !== 'object') {
    shapeItem.ShapeParameter = {};
  }
  const target = shapeItem.ShapeParameter[key];
  if (!target || typeof target !== 'object') {
    shapeItem.ShapeParameter[key] = animation(value);
    return;
  }
  if (!Array.isArray(target.Values) || target.Values.length === 0) {
    target.Values = [{ Value: value }];
    return;
  }
  target.Values[0].Value = value;
}

function setShapeBrushColor(shapeItem, color) {
  const brush = shapeItem.ShapeParameter?.Brush;
  if (!brush?.Parameter || typeof brush.Parameter !== 'object') {
    throw new Error('SHAPE_BRUSH_PARAMETER_MISSING');
  }
  brush.Parameter.Color = color;
}

function setShapeGeometry(shapeItem, primitive) {
  shapeItem.ShapeParameter.SizeMode = shapeSizeMode;
  setShapeParameterValue(shapeItem, 'Size', Math.max(primitive.width, primitive.height));
  setShapeParameterValue(shapeItem, 'AspectRate', primitive.width / primitive.height);
  setShapeParameterValue(shapeItem, 'Width', primitive.width);
  setShapeParameterValue(shapeItem, 'Height', primitive.height);
  setShapeParameterValue(shapeItem, 'Round', primitive.round);
  setShapeParameterValue(shapeItem, 'StrokeThickness', primitive.stroke_thickness);
}

function makeShapeItem(template, primitive) {
  const item = clone(template);
  item.Frame = 0;
  item.Length = DURATION_FRAMES;
  item.Layer = primitive.layer;
  item.Group = 0;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Remark = primitive.display_name;
  item.IsLocked = false;
  item.IsHidden = false;
  setAnimatedValue(item, 'X', primitive.x);
  setAnimatedValue(item, 'Y', primitive.y);
  setAnimatedValue(item, 'Z', 0);
  setAnimatedValue(item, 'Opacity', primitive.opacity);
  setAnimatedValue(item, 'Zoom', 100);
  setAnimatedValue(item, 'Rotation', 0);
  setShapeGeometry(item, primitive);
  setShapeBrushColor(item, primitive.color);
  return item;
}

function makeTextItem(primitive) {
  return {
    $type: 'YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker',
    Text: primitive.content,
    Font: 'Yu Gothic UI',
    FontSize: animation(primitive.font_size),
    FontColor: primitive.color,
    Style: 'Normal',
    X: animation(primitive.x),
    Y: animation(primitive.y),
    Z: animation(0),
    Opacity: animation(primitive.opacity),
    Zoom: animation(100),
    Rotation: animation(0),
    FadeIn: 0,
    FadeOut: 0,
    Blend: 'Normal',
    IsAlwaysOnTop: false,
    IsZOrderEnabled: false,
    VideoEffects: [],
    Group: 0,
    Frame: 0,
    Layer: primitive.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: DURATION_FRAMES,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: primitive.display_name,
    IsLocked: false,
    IsHidden: false,
  };
}

function rectRight(rect) {
  return rect.x + rect.width;
}

function rectBottom(rect) {
  return rect.y + rect.height;
}

function rectCenter(rect) {
  return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
}

function screenRectToYmm4Center(rect) {
  const center = rectCenter(rect);
  return { x: center.x - FRAME.width / 2, y: center.y - FRAME.height / 2 };
}

function screenTopLeftToYmm4(topLeft) {
  return { x: topLeft.x - FRAME.width / 2, y: topLeft.y - FRAME.height / 2 };
}

function inRegion(rect, region) {
  return rect.x >= region.x &&
    rect.y >= region.y &&
    rectRight(rect) <= rectRight(region) &&
    rectBottom(rect) <= rectBottom(region);
}

function overlaps(a, b) {
  return !(rectRight(a) <= b.x || rectRight(b) <= a.x || rectBottom(a) <= b.y || rectBottom(b) <= a.y);
}

function roundFor(item) {
  if (item.id === 'G28_MEC_BG_Stage') return 0;
  if (item.id === 'G28_MEC_EvidenceSurface') return 24;
  if (item.id.includes('AnnotationSlot')) return 14;
  if (item.id.includes('SourceNote')) return 12;
  if (item.id.includes('Host')) return 42;
  if (item.id.includes('LabelAnchor')) return 12;
  return 8;
}

function shapePrimitive(item) {
  const center = screenRectToYmm4Center(item.rect);
  return {
    kind: 'ShapeItem',
    display_name: item.id,
    group_id: item.group_id,
    role: item.semantic_role,
    layer: item.layer,
    x: center.x,
    y: center.y,
    width: item.rect.width,
    height: item.rect.height,
    screen_rect: item.rect,
    color: item.style.fill,
    opacity: 100,
    round: roundFor(item),
    stroke_thickness: Math.min(item.rect.height, 14),
    layout_contract: {
      rect_source: 'map_evidence_skeleton_rect',
      source_rect: item.rect,
    },
    description: `G-28 Map / Evidence source skeleton primitive ${item.id}`,
  };
}

function textPrimitive(item) {
  const topLeft = screenTopLeftToYmm4(item.rect);
  return {
    kind: 'TextItem',
    display_name: item.id,
    group_id: item.group_id,
    role: item.semantic_role,
    layer: item.layer,
    x: topLeft.x,
    y: topLeft.y,
    screen_rect: item.rect,
    bbox_width: item.rect.width,
    bbox_height: item.rect.height,
    font_size: item.style.font_size,
    content: item.style.text,
    color: item.style.fill,
    opacity: 100,
    layout_contract: {
      rect_source: 'map_evidence_skeleton_rect',
      source_rect: item.rect,
      text_budget_role: item.id === 'G28_MEC_SourceNote_Text' ? 'bounded_source_note' : 'title',
    },
    description: `G-28 Map / Evidence source skeleton text ${item.id}`,
  };
}

function validateSource(source, sourceReadback) {
  const errors = [];
  if (source.artifact_id !== sourceArtifactId) errors.push(`source artifact mismatch: ${source.artifact_id}`);
  if (source.diagnostic_only !== true) errors.push('source diagnostic_only is not true');
  if (source.production_candidate !== false) errors.push('source production_candidate is not false');
  if (source.ymmp_generation !== 'not_generated_boundary') errors.push('source already claims ymmp generation');
  if (source.external_assets?.image_path !== false) errors.push('source image path flag is not false');
  if (source.external_assets?.image_url !== false) errors.push('source image URL flag is not false');
  if (sourceReadback.status !== 'passed') errors.push(`source readback status is ${sourceReadback.status}`);
  if (sourceReadback.checks?.caption_reserve_clear !== true) errors.push('source caption reserve is not clear');
  if (sourceReadback.checks?.external_image_count_zero !== true) errors.push('source external image count check failed');
  if (sourceReadback.checks?.external_url_count_zero !== true) errors.push('source external URL count check failed');
  if (sourceReadback.checks?.token_like_pattern_count_zero !== true) errors.push('source token-like count check failed');
  if (sourceReadback.checks?.ymmp_not_generated !== true) errors.push('source readback should record ymmp not generated');
  if (errors.length) throw new Error(`G28_MAP_EVIDENCE_SOURCE_INVALID: ${errors.join('; ')}`);
}

function buildPrimitivePlan(source, sourceReadback) {
  validateSource(source, sourceReadback);
  const primitives = source.items.map((item) => {
    if (item.item_type === 'ShapeItem') return shapePrimitive(item);
    if (item.item_type === 'TextItem') return textPrimitive(item);
    throw new Error(`UNSUPPORTED_SOURCE_ITEM: ${item.id}`);
  });
  return {
    probe_artifact_id: probeArtifactId,
    source_artifact_id: source.artifact_id,
    carrier_kind: carrierKind,
    variant,
    frame_contract: source.frame_contract,
    reserved_areas: source.reserved_areas,
    source_checks: sourceReadback.checks,
    scs_mapping: source.scs_mapping,
    primitives,
  };
}

function buildProject(carrierYmmp, shapeTemplateYmmp, primitivePlan) {
  const project = clone(carrierYmmp);
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) throw new Error('SHAPE_TEMPLATE_NOT_FOUND');
  if (!Array.isArray(project.Timelines) || !project.Timelines.length) {
    throw new Error('CANONICAL_TIMELINE_MISSING');
  }
  const timeline = project.Timelines[0];
  timeline.Items = primitivePlan.primitives.map((primitive) => {
    if (primitive.kind === 'ShapeItem') return makeShapeItem(shapeTemplate, primitive);
    if (primitive.kind === 'TextItem') return makeTextItem(primitive);
    throw new Error(`UNSUPPORTED_PRIMITIVE_KIND: ${primitive.kind}`);
  });
  return project;
}

function shapeParameterValue(shapeItem, key) {
  const values = shapeItem.ShapeParameter?.[key]?.Values;
  return Array.isArray(values) && values.length ? values[0].Value : null;
}

function animatedValue(item, key) {
  const values = item[key]?.Values;
  return Array.isArray(values) && values.length ? values[0].Value : null;
}

function readbackItem(item, primitive) {
  const type = itemType(item);
  const isShape = type === 'ShapeItem';
  const isText = type === 'TextItem';
  return {
    id: String(item.Remark || ''),
    item_type: type,
    group_id: primitive?.group_id || null,
    role: primitive?.role || null,
    layer: item.Layer,
    x: animatedValue(item, 'X'),
    y: animatedValue(item, 'Y'),
    width: isShape ? shapeParameterValue(item, 'Width') ?? null : primitive?.bbox_width ?? null,
    height: isShape ? shapeParameterValue(item, 'Height') ?? null : primitive?.bbox_height ?? null,
    text: isText ? item.Text : null,
    font_size: isText ? item.FontSize?.Values?.[0]?.Value ?? null : null,
    screen_rect: primitive?.screen_rect || null,
    layout_contract: primitive?.layout_contract || null,
    description: primitive?.description || null,
  };
}

function captionOverlaps(primitives, captionReserve) {
  return primitives
    .filter((primitive) => primitive.role !== 'decoration')
    .filter((primitive) => overlaps(primitive.screen_rect, captionReserve))
    .map((primitive) => primitive.display_name);
}

function readbackProbe(project, primitivePlan, carrierHashBefore, carrierHashAfter) {
  const timeline = project.Timelines?.[0] || { Items: [] };
  const primitivesByName = new Map(primitivePlan.primitives.map((primitive) => [primitive.display_name, primitive]));
  const items = (timeline.Items || []).map((item) => readbackItem(item, primitivesByName.get(String(item.Remark || ''))));
  const itemTypes = new Set(items.map((item) => item.item_type));
  const missing = primitivePlan.primitives
    .map((primitive) => primitive.display_name)
    .filter((displayName) => !items.some((item) => item.id === displayName));
  const textItems = items.filter((item) => item.item_type === 'TextItem');
  const shapeItems = items.filter((item) => item.item_type === 'ShapeItem');
  const frame = primitivePlan.frame_contract;
  const captionReserve = frame.caption_reserve;
  const mainCanvas = frame.main_canvas;
  const evidenceSurface = primitivePlan.primitives.find((primitive) => primitive.display_name === 'G28_MEC_EvidenceSurface');
  const annotationSlots = primitivePlan.primitives.filter((primitive) => primitive.display_name.startsWith('G28_MEC_AnnotationSlot_'));
  const hosts = primitivePlan.primitives.filter((primitive) => primitive.display_name.startsWith('G28_MEC_Host_'));
  const captionOverlapIds = captionOverlaps(primitivePlan.primitives, captionReserve);
  const visibleTextChars = textItems.reduce((sum, item) => sum + String(item.text || '').length, 0);
  const failures = [];
  const checks = {
    diagnostic_only: true,
    production_candidate_false: true,
    carrier_kind_expected: primitivePlan.carrier_kind === carrierKind,
    variant_expected: primitivePlan.variant === variant,
    self_contained_ymmp_probe_created: itemTypes.size > 0 && [...itemTypes].every((type) => ['ShapeItem', 'TextItem'].includes(type)),
    frame_16_9_1920_1080: frame.width === 1920 && frame.height === 1080 && frame.aspect_ratio === '16:9',
    caption_reserve_bottom_20pct: captionReserve.y === 810 && captionReserve.height === 216,
    caption_reserve_clear: captionOverlapIds.length === 0,
    evidence_area_in_main_canvas: evidenceSurface ? inRegion(evidenceSurface.screen_rect, mainCanvas) : false,
    annotation_slot_count_2_to_4: annotationSlots.length >= 2 && annotationSlots.length <= 4,
    source_note_area_exists: primitivePlan.primitives.some((primitive) => primitive.display_name === 'G28_MEC_SourceNote_BG'),
    source_note_text_budget_bounded: textItems.some((item) => item.id === 'G28_MEC_SourceNote_Text' && String(item.text || '').length <= 12 && item.font_size >= 32),
    host_role_non_focal: hosts.length === 2 && hosts.every((host) => host.role === 'decoration'),
    dense_table_false: primitivePlan.source_checks?.dense_table_false === true,
    indexed_whiteboard_false: primitivePlan.source_checks?.indexed_whiteboard_false === true,
    tiny_text_false_or_bounded: Math.min(...textItems.map((item) => item.font_size || 999)) >= 32,
    primitive_item_count_bounded: primitivePlan.primitives.length <= 18,
    shape_item_count_expected: shapeItems.length === 12,
    text_item_count_expected: textItems.length === 2,
    external_image_count_zero: true,
    external_url_count_zero: true,
    source_footage_count_zero: true,
    audio_item_count_zero: true,
    tts_or_voice_item_count_zero: true,
    render_output_false: true,
    production_approval_false: true,
    creative_final_acceptance_false: true,
    rights_approval_false: true,
    token_like_pattern_count_zero: true,
    carrier_not_modified_in_place: carrierHashBefore === carrierHashAfter,
  };
  for (const [key, value] of Object.entries(checks)) {
    if (value !== true) failures.push(key);
  }
  if (missing.length) failures.push('missing_items');
  return {
    artifact_type: 'g28_map_evidence_ymmp_diagnostic_probe_readback',
    probe_artifact_id: primitivePlan.probe_artifact_id,
    source_artifact_id: primitivePlan.source_artifact_id,
    carrier_kind: primitivePlan.carrier_kind,
    variant: primitivePlan.variant,
    diagnostic_only: true,
    production_candidate: false,
    status: failures.length === 0 && missing.length === 0 ? 'passed' : 'failed',
    classification: failures.length === 0 && missing.length === 0 ? creationRecord.classification : 'fail_map_evidence_ymmp_diagnostic_carrier_readback',
    generated_files: {
      ymmp: paths.outputYmmp,
      readback_json: paths.readbackJson,
      report_md: paths.reportMd,
    },
    creation_record: creationRecord,
    boundary: {
      diagnostic_only: true,
      production_candidate: false,
      self_contained_ymmp_probe: true,
      production_render: false,
      render_output: false,
      creative_final_acceptance: false,
      production_carrier_approval: false,
      rights_approval: false,
      slot_fill: false,
      source_footage_intake: false,
      real_map_or_satellite_image_intake: false,
      external_material_intake: false,
      audio_or_tts: false,
      image_or_url_or_raw_reference: false,
      game_mechanics_same_screen_tuning: false,
      common_foundation_work: false,
    },
    frame_contract: {
      width: frame.width,
      height: frame.height,
      aspect_ratio: frame.aspect_ratio,
      caption_reserve: captionReserve,
      main_canvas: mainCanvas,
    },
    totals: {
      item_count: items.length,
      expected_item_count: primitivePlan.primitives.length,
      shape_item_count: shapeItems.length,
      text_item_count: textItems.length,
      visible_text_chars: visibleTextChars,
      missing_item_count: missing.length,
      annotation_slot_count: annotationSlots.length,
    },
    checks,
    failures,
    missing_items: missing,
    scs_readback: primitivePlan.scs_mapping,
    caption_reserve_readback: {
      rect: captionReserve,
      clear: captionOverlapIds.length === 0,
      overlaps: captionOverlapIds,
    },
    evidence_surface_readback: {
      id: evidenceSurface?.display_name || null,
      rect: evidenceSurface?.screen_rect || null,
      in_main_canvas: evidenceSurface ? inRegion(evidenceSurface.screen_rect, mainCanvas) : false,
    },
    annotation_readback: {
      count: annotationSlots.length,
      ids: annotationSlots.map((slot) => slot.display_name),
      empty_placeholders_until_slot_fill: true,
    },
    source_note_readback: {
      exists: textItems.some((item) => item.id === 'G28_MEC_SourceNote_Text'),
      text: textItems.find((item) => item.id === 'G28_MEC_SourceNote_Text')?.text || null,
      bounded: checks.source_note_text_budget_bounded,
    },
    host_role_readback: {
      role: 'non_focal_lower_corner_decoration_emotional_anchor',
      ids: hosts.map((host) => host.display_name),
    },
    text_budget_readback: {
      visible_text_item_count: textItems.length,
      visible_text_chars: visibleTextChars,
      smallest_text_size: Math.min(...textItems.map((item) => item.font_size || 999)),
      production_text_budget_claimed: false,
    },
    safety_readback: {
      external_image_count: 0,
      external_url_count: 0,
      source_footage_count: 0,
      audio_item_count: 0,
      tts_or_voice_item_count: 0,
      image_path: false,
      image_url: false,
      raw_reference: false,
      token_like_pattern_count: 0,
    },
    items,
    next_review_inputs_required: [
      'carrier path',
      'preview screenshot',
      'timeline screenshot',
      'item/layer confirmation',
      'caption reserve visual confirmation',
      'human decision: accept / accept_with_caveats / revise_once / layout_system_debt / redesign_required',
    ],
    known_caveats: [
      'This is a self-contained YMM4 diagnostic carrier candidate, not a production carrier.',
      'The evidence surface is abstract and uses no real map, satellite image, image path, URL, or raw reference.',
      'Annotation slots are empty placeholders until a later scoped slot-fill slice exists.',
      'No render, video, audio, source footage, external image, rights automation, or creative final acceptance is included.',
      'Game-mechanics same-screen micro-tuning remains stopped; this advances a separate reviewable artifact.',
    ],
  };
}

function renderReport(readback) {
  const lines = [];
  lines.push('# G-28 Map / Evidence YMM4 Diagnostic Carrier Probe');
  lines.push('');
  lines.push(`Probe artifact: \`${readback.probe_artifact_id}\``);
  lines.push(`Source artifact: \`${readback.source_artifact_id}\``);
  lines.push('');
  lines.push('This is a self-contained YMM4-compatible diagnostic carrier candidate for human review. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, image intake, or slot-fill.');
  lines.push('');
  lines.push('## Generated Files');
  lines.push('');
  lines.push(`- YMM4 probe: \`${readback.generated_files.ymmp}\``);
  lines.push(`- readback JSON: \`${readback.generated_files.readback_json}\``);
  lines.push(`- report: \`${readback.generated_files.report_md}\``);
  lines.push('');
  lines.push('## Why This Artifact');
  lines.push('');
  lines.push('- The game_mechanics YMM4 diagnostic carrier remains reviewable but is now recorded as layout_system_debt.');
  lines.push('- Same-screen tuning stays stopped.');
  lines.push('- This slice advances a separate G-28 reviewable artifact, speed-first, before a later cross-screen layout-normalization audit.');
  lines.push('');
  lines.push('## Boundary');
  lines.push('');
  for (const [key, value] of Object.entries(readback.boundary)) {
    lines.push(`- \`${key}\`: \`${value}\``);
  }
  lines.push('');
  lines.push('## Readback Rollup');
  lines.push('');
  lines.push(`- status: \`${readback.status}\``);
  lines.push(`- classification: \`${readback.classification}\``);
  lines.push(`- carrier kind: \`${readback.carrier_kind}\``);
  lines.push(`- variant: \`${readback.variant}\``);
  lines.push(`- frame: ${readback.frame_contract.width}x${readback.frame_contract.height} / ${readback.frame_contract.aspect_ratio}`);
  lines.push(`- bottom caption reserve: clear=\`${readback.caption_reserve_readback.clear}\`, y=${readback.caption_reserve_readback.rect.y}, h=${readback.caption_reserve_readback.rect.height}`);
  lines.push(`- evidence surface: in_main_canvas=\`${readback.evidence_surface_readback.in_main_canvas}\``);
  lines.push(`- annotation slots: ${readback.annotation_readback.count}`);
  lines.push(`- source note: \`${readback.source_note_readback.text}\`, bounded=\`${readback.source_note_readback.bounded}\``);
  lines.push(`- host role: \`${readback.host_role_readback.role}\``);
  lines.push(`- visible text: ${readback.text_budget_readback.visible_text_item_count} items / ${readback.text_budget_readback.visible_text_chars} chars`);
  lines.push('');
  lines.push('## Checks');
  lines.push('');
  for (const [key, value] of Object.entries(readback.checks)) {
    lines.push(`- \`${key}\`: \`${value}\``);
  }
  lines.push('');
  lines.push('## Next Review Inputs Required');
  lines.push('');
  for (const input of readback.next_review_inputs_required) {
    lines.push(`- ${input}`);
  }
  lines.push('');
  lines.push('## Known Caveats');
  lines.push('');
  for (const caveat of readback.known_caveats) {
    lines.push(`- ${caveat}`);
  }
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.diagnostic_only !== true) failures.push('diagnostic_only is not true');
  if (readback.production_candidate !== false) failures.push('production_candidate is not false');
  if (readback.boundary.render_output !== false) failures.push('render_output is not false');
  if (readback.boundary.creative_final_acceptance !== false) failures.push('creative_final_acceptance is not false');
  if (readback.safety_readback.external_image_count !== 0) failures.push(`external_image_count=${readback.safety_readback.external_image_count}`);
  if (readback.safety_readback.external_url_count !== 0) failures.push(`external_url_count=${readback.safety_readback.external_url_count}`);
  if (readback.safety_readback.source_footage_count !== 0) failures.push(`source_footage_count=${readback.safety_readback.source_footage_count}`);
  if (readback.safety_readback.audio_item_count !== 0) failures.push(`audio_item_count=${readback.safety_readback.audio_item_count}`);
  if (readback.safety_readback.tts_or_voice_item_count !== 0) failures.push(`tts_or_voice_item_count=${readback.safety_readback.tts_or_voice_item_count}`);
  if (readback.checks.caption_reserve_clear !== true) failures.push('caption reserve is not clear');
  if (readback.checks.evidence_area_in_main_canvas !== true) failures.push('evidence area is not in main canvas');
  if (readback.checks.annotation_slot_count_2_to_4 !== true) failures.push('annotation slot count is out of bounds');
  if (readback.checks.source_note_text_budget_bounded !== true) failures.push('source note text budget is not bounded');
  if (readback.checks.carrier_not_modified_in_place !== true) failures.push('carrier file hash changed');
  if (readback.failures.length) failures.push(`failed checks: ${readback.failures.join(', ')}`);
  if (failures.length) {
    throw new Error(`G28_MAP_EVIDENCE_YMMP_READBACK_FAILED: ${failures.join('; ')}`);
  }
}

function main() {
  const source = readJson(paths.sourceJson);
  const sourceReadback = readJson(paths.sourceReadback);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplateYmmp = readJson(paths.shapeTemplateYmmp);
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const primitivePlan = buildPrimitivePlan(source, sourceReadback);
  const generated = buildProject(carrierYmmp, shapeTemplateYmmp, primitivePlan);
  const generatedReadback = readbackProbe(generated, primitivePlan, carrierHashBefore, sha256(paths.carrierYmmp));
  assertReadback(generatedReadback);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generated);
    const written = readJson(paths.outputYmmp);
    const writtenReadback = readbackProbe(written, primitivePlan, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(writtenReadback);
    writeJson(paths.readbackJson, writtenReadback);
    writeMarkdown(paths.reportMd, renderReport(writtenReadback));
    console.log(`Wrote: ${paths.outputYmmp}`);
    console.log(`Readback: ${paths.readbackJson}`);
    console.log(`Report: ${paths.reportMd}`);
    return;
  }

  if (!fs.existsSync(abs(paths.outputYmmp))) {
    console.log('Dry-run passed; output .ymmp does not exist yet. Re-run with --write to create it.');
    return;
  }
  const storedReadback = readJson(paths.readbackJson);
  const existing = readJson(paths.outputYmmp);
  const actualReadback = readbackProbe(existing, primitivePlan, carrierHashBefore, sha256(paths.carrierYmmp));
  assertReadback(actualReadback);
  if (JSON.stringify(storedReadback, null, 2) !== JSON.stringify(actualReadback, null, 2)) {
    throw new Error('G28_MAP_EVIDENCE_YMMP_READBACK_DRIFT');
  }
  console.log('Map / Evidence YMM4 diagnostic probe verified.');
}

main();

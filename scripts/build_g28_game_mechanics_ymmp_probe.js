// G-28 game_mechanics_explanation YMM4-compatible diagnostic probe.
// Builds a self-contained ShapeItem/TextItem-only .ymmp from the accepted
// Lecture Diagram Carrier diagnostic variant. This is review-only and does not
// render, approve production, ingest footage, or use external materials.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  sourceJson: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.json',
  sourceReadback: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_readback.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp',
  outputYmmp: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp',
  readbackJson: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_readback.json',
  reportMd: 'samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_report.md',
};

const FRAME = { width: 1920, height: 1080 };
const DURATION_FRAMES = 600;
const shapeSizeMode = 'WidthHeight';
const expectedVariantId = 'g28_ldc_game_mechanics_explanation';
const expectedSourceArtifactId = 'g28_lecture_diagram_carrier_game_mechanics_explanation_v1';
const probeArtifactId = 'g28_lecture_diagram_carrier_game_mechanics_explanation_ymmp_probe_v1';
const carrierKind = 'lecture_diagram_carrier';
const variant = 'game_mechanics_explanation';

const focalChainLabels = [
  '入力操作',
  '内部ルール / 判定',
  '画面上の結果',
];
const calloutLabels = [
  '操作感',
  '判定 / 当たり判定',
  'リスクとリターン',
];
const nextReviewInputsRequired = [
  'carrier path',
  'preview screenshot',
  'timeline screenshot',
  'item/layer confirmation',
  'bottom caption safe-area evidence',
];
const creationRecord = {
  revision_id: 'g28_game_mechanics_ymmp_label_layout_fix_v1',
  source_human_need: 'one-pass YMM4 visual fix for right focal label fit and lower callout centering',
  classification: 'pass_game_mechanics_ymmp_label_layout_fixed',
  boundary_note: 'Diagnostic-only YMM4 carrier candidate; one-pass label layout fix only; no render, production approval, rights approval, creative final acceptance, source footage, gameplay screenshot, URL, image, audio, or TTS.',
};
const diagnosticTextBudget = {
  max_visible_text_items: 8,
  max_visible_chars: 80,
  production_text_budget_claimed: false,
};
const manualOffsetRegistry = {
  G28_LDC_Title_Text: { value: { x: 0, y: -2 }, reason: 'Title optical centering inside the source title band.' },
  G28_LDC_Node_Left_Label: { value: { x: 0, y: -4 }, reason: 'Node label optical centering.' },
  G28_LDC_Node_Center_Label: { value: { x: 0, y: -4 }, reason: 'Center node label optical centering.' },
  G28_LDC_Node_Right_Label: { value: { x: 0, y: -4 }, reason: 'One-pass right-node fit correction: remove inherited rightward nudge and rely on reduced font size.' },
  G28_LDC_CalloutSlot_1_Label: { value: { x: 0, y: -3 }, reason: 'One-pass common callout centering rule.' },
  G28_LDC_CalloutSlot_2_Label: { value: { x: 0, y: -3 }, reason: 'One-pass common callout centering rule.' },
  G28_LDC_CalloutSlot_3_Label: { value: { x: 0, y: -3 }, reason: 'One-pass common callout centering rule.' },
};
const fontSizeOverrideRegistry = {
  G28_LDC_Node_Right_Label: {
    value: 38,
    reason: 'Keep the right focal label text unchanged while adding horizontal breathing room inside the existing node box.',
  },
  G28_LDC_CalloutSlot_1_Label: {
    value: 28,
    reason: 'Use one common callout label size so all callouts center visually inside the same slot rule.',
  },
  G28_LDC_CalloutSlot_2_Label: {
    value: 28,
    reason: 'Use one common callout label size so the long judgement label has visible side margins.',
  },
  G28_LDC_CalloutSlot_3_Label: {
    value: 28,
    reason: 'Use one common callout label size so the risk/reward label has visible side margins.',
  },
};
const layoutOutcome = {
  one_pass_targeted_fix: true,
  no_further_micro_tuning_recommended: true,
  next_decision_gate: 'accept_with_layout_caveat',
  next_decision_gate_options: [
    'accept_as_diagnostic_review_surface',
    'accept_with_layout_caveat',
    'layout_system_debt',
    'redesign_required',
  ],
};

function abs(rel) { return path.join(root, rel); }
function readText(rel) { return fs.readFileSync(abs(rel), 'utf8').replace(/^\uFEFF/, ''); }
function readJson(rel) { return JSON.parse(readText(rel)); }
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
function clone(value) { return JSON.parse(JSON.stringify(value)); }

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

function rectRight(rect) { return rect.x + rect.width; }
function rectBottom(rect) { return rect.y + rect.height; }
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

function estimateTextWidth(text, fontSize) {
  let widthEm = 0;
  for (const ch of String(text)) {
    const cp = ch.codePointAt(0) ?? 0;
    const fullWidth = (
      (cp >= 0x3000 && cp <= 0x303f) ||
      (cp >= 0x3040 && cp <= 0x309f) ||
      (cp >= 0x30a0 && cp <= 0x30ff) ||
      (cp >= 0x4e00 && cp <= 0x9fff) ||
      (cp >= 0xff00 && cp <= 0xffef)
    );
    widthEm += fullWidth ? 1.0 : 0.55;
  }
  return Math.round(widthEm * fontSize);
}

function roundFor(item) {
  if (item.id === 'G28_LDC_BG_Stage') return 0;
  if (item.id === 'G28_LDC_TitleBand_BG') return 8;
  if (item.id === 'G28_LDC_Focal_Core') return 28;
  if (item.id.startsWith('G28_LDC_Node_')) return 22;
  if (item.id.startsWith('G28_LDC_Connector_')) return 6;
  if (item.id.startsWith('G28_LDC_CalloutSlot_')) return 16;
  if (item.id.startsWith('G28_LDC_Host_')) return 42;
  return 10;
}

function layerForShape(item) {
  if (item.id === 'G28_LDC_BG_Stage') return 1;
  if (item.id === 'G28_LDC_TitleBand_BG') return 2;
  if (item.id === 'G28_LDC_Focal_Core') return 4;
  if (item.id.startsWith('G28_LDC_Node_')) return 5;
  if (item.id.startsWith('G28_LDC_Connector_')) return 6;
  if (item.id.startsWith('G28_LDC_CalloutSlot_')) return 8;
  if (item.id.startsWith('G28_LDC_Host_')) return 10;
  return item.layer;
}

function shapePrimitive(item) {
  const rect = item.rect;
  const center = screenRectToYmm4Center(rect);
  return {
    kind: 'ShapeItem',
    display_name: item.id,
    group_id: item.group_id,
    role: item.semantic_role,
    layer: layerForShape(item),
    x: center.x,
    y: center.y,
    width: rect.width,
    height: rect.height,
    screen_rect: rect,
    color: item.style.fill,
    opacity: 100,
    round: roundFor(item),
    stroke_thickness: Math.min(rect.height, 16),
    layout_contract: {
      rect_source: 'source_rect',
      source_rect: item.rect,
    },
    description: `G-28 game-mechanics source carrier primitive ${item.id}`,
  };
}

function centeredTextPrimitive(displayName, groupId, role, layer, targetBox, fontSize, content, color, description) {
  const fontSizeOverride = fontSizeOverrideRegistry[displayName] || null;
  const effectiveFontSize = fontSizeOverride?.value || fontSize;
  const bboxWidth = estimateTextWidth(content, effectiveFontSize);
  const bboxHeight = effectiveFontSize;
  const offset = manualOffsetRegistry[displayName]?.value || { x: 0, y: 0 };
  const centerScreen = rectCenter(targetBox.rect);
  const adjustedCenter = {
    x: centerScreen.x + offset.x,
    y: centerScreen.y + offset.y,
  };
  const screenTopLeft = {
    x: adjustedCenter.x - bboxWidth / 2,
    y: adjustedCenter.y - bboxHeight / 2,
  };
  const ymm4TopLeft = screenTopLeftToYmm4(screenTopLeft);
  return {
    kind: 'TextItem',
    display_name: displayName,
    group_id: groupId,
    role,
    layer,
    x: ymm4TopLeft.x,
    y: ymm4TopLeft.y,
    screen_rect: {
      x: screenTopLeft.x,
      y: screenTopLeft.y,
      width: bboxWidth,
      height: bboxHeight,
    },
    source_intent_screen_cx: centerScreen.x,
    source_intent_screen_cy: centerScreen.y,
    visual_offset_px: offset,
    layout_contract: {
      target_box_id: targetBox.id,
      target_box_rect: targetBox.rect,
      requested_font_size: fontSize,
      effective_font_size: effectiveFontSize,
      font_size_override: fontSizeOverride,
      estimated_text_width: bboxWidth,
      estimated_text_height: bboxHeight,
      estimated_horizontal_margin_each_side_px: Math.round((targetBox.rect.width - bboxWidth) / 2),
      manual_registry_entry: manualOffsetRegistry[displayName] || null,
    },
    bbox_width: bboxWidth,
    bbox_height: bboxHeight,
    font_size: effectiveFontSize,
    content,
    color,
    opacity: 100,
    description,
  };
}

function validateSource(source, sourceReadback) {
  const errors = [];
  if (source.artifact_id !== expectedSourceArtifactId) errors.push(`source artifact mismatch: ${source.artifact_id}`);
  if (source.variant_id !== expectedVariantId) errors.push(`variant id mismatch: ${source.variant_id}`);
  if (source.diagnostic_only !== true) errors.push('source diagnostic_only is not true');
  if (source.production_candidate !== false) errors.push('source production_candidate is not false');
  if (sourceReadback.status !== 'passed') errors.push(`source readback status is ${sourceReadback.status}`);
  if (sourceReadback.variant_readback?.variant_id !== expectedVariantId) errors.push('source readback variant mismatch');
  if (sourceReadback.caption_reserve_readback?.clear !== true) errors.push('source caption reserve is not clear');
  if (sourceReadback.variant_readback?.callout_count !== 3) errors.push('source callout count is not 3');
  if (sourceReadback.variant_readback?.focal_chain_node_count !== 3) errors.push('source focal chain node count is not 3');
  if (sourceReadback.safety_readback?.external_image_count !== 0) errors.push('source external image count is not 0');
  if (sourceReadback.safety_readback?.external_url_count !== 0) errors.push('source external URL count is not 0');
  if (sourceReadback.review_surface_readback?.clean_frame_available !== true) errors.push('source clean frame is not available');
  if (sourceReadback.review_surface_readback?.production_text_budget_separate_from_review_labels !== true) {
    errors.push('source production/review text separation is not recorded');
  }
  if (errors.length) throw new Error(`G28_SOURCE_INVALID: ${errors.join('; ')}`);
}

function buildPrimitivePlan(source, sourceReadback) {
  validateSource(source, sourceReadback);
  const sourceItems = source.items || [];
  const byId = new Map(sourceItems.map((item) => [item.id, item]));
  const shapes = sourceItems
    .filter((item) => item.item_type === 'ShapeItem')
    .map(shapePrimitive);
  const title = byId.get('G28_LDC_Title_Text');
  const leftNode = byId.get('G28_LDC_Node_Left');
  const focalCore = byId.get('G28_LDC_Focal_Core');
  const rightNode = byId.get('G28_LDC_Node_Right');
  const labelColor = '#FFF9FAFB';
  const nodeColor = '#FFFFF7D6';
  const calloutColor = '#FFDBEAFE';
  const titleText = source.theme_variant.title_text;

  const textPrimitives = [
    centeredTextPrimitive(
      'G28_LDC_Title_Text',
      'G28_LDC_TitleBand',
      'label',
      3,
      { id: 'G28_LDC_Title_Text_SourceRect', rect: title.rect },
      52,
      titleText,
      labelColor,
      'short title label from accepted game-mechanics diagnostic variant',
    ),
    centeredTextPrimitive(
      'G28_LDC_Node_Left_Label',
      'G28_LDC_FocalGroup',
      'focal_chain_label',
      7,
      { id: leftNode.id, rect: leftNode.rect },
      42,
      focalChainLabels[0],
      nodeColor,
      'visible player-input node label for YMM4 GUI diagnostic review',
    ),
    centeredTextPrimitive(
      'G28_LDC_Node_Center_Label',
      'G28_LDC_FocalGroup',
      'focal_chain_label',
      7,
      { id: focalCore.id, rect: focalCore.rect },
      42,
      focalChainLabels[1],
      nodeColor,
      'visible internal-rule/judgement node label for YMM4 GUI diagnostic review',
    ),
    centeredTextPrimitive(
      'G28_LDC_Node_Right_Label',
      'G28_LDC_FocalGroup',
      'focal_chain_label',
      7,
      { id: rightNode.id, rect: rightNode.rect },
      42,
      focalChainLabels[2],
      nodeColor,
      'visible on-screen-result node label for YMM4 GUI diagnostic review',
    ),
  ];

  for (let index = 0; index < calloutLabels.length; index += 1) {
    const slotId = `G28_LDC_CalloutSlot_${index + 1}`;
    const slot = byId.get(slotId);
    textPrimitives.push(centeredTextPrimitive(
      `${slotId}_Label`,
      'G28_LDC_CalloutSlots',
      'callout_label',
      9,
      { id: slot.id, rect: slot.rect },
      30,
      calloutLabels[index],
      calloutColor,
      'visible callout label for YMM4 GUI diagnostic review',
    ));
  }

  return {
    source_artifact_id: source.artifact_id,
    variant_id: source.variant_id,
    carrier_kind: carrierKind,
    variant,
    source_theme_variant: source.theme_variant,
    source_readback_middle_label: sourceReadback.variant_readback.focal_chain[1].label,
    frame_contract: source.frame_contract,
    scs_mapping: source.scs_mapping,
    creation_record: creationRecord,
    primitives: [...shapes, ...textPrimitives],
  };
}

function buildProject(carrierYmmp, shapeTemplateYmmp, primitivePlan) {
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) throw new Error(`SHAPE_TEMPLATE_MISSING: ${paths.shapeTemplateYmmp}`);
  const project = clone(carrierYmmp);
  if (!Array.isArray(project.Timelines) || !project.Timelines[0]) {
    throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  }
  const timeline = project.Timelines[0];
  const items = primitivePlan.primitives.map((primitive) => {
    if (primitive.kind === 'ShapeItem') return makeShapeItem(shapeTemplate, primitive);
    if (primitive.kind === 'TextItem') return makeTextItem(primitive);
    throw new Error(`UNSUPPORTED_PRIMITIVE_KIND: ${primitive.kind}`);
  });
  timeline.Items = items;
  timeline.CurrentFrame = 0;
  timeline.Length = DURATION_FRAMES;
  timeline.MaxLayer = Math.max(...items.map((item) => item.Layer), 0);
  if (!timeline.LayerSettings || Array.isArray(timeline.LayerSettings)) {
    timeline.LayerSettings = { Items: Array.isArray(timeline.LayerSettings) ? timeline.LayerSettings : [] };
  }
  project.FilePath = paths.outputYmmp;
  return project;
}

function animationValue(item, key) { return item?.[key]?.Values?.[0]?.Value; }
function shapeParameterValue(item, key) { return item?.ShapeParameter?.[key]?.Values?.[0]?.Value; }

function readbackItem(item, primitive) {
  const type = itemType(item);
  const isShape = type === 'ShapeItem';
  const isText = type === 'TextItem';
  const x = animationValue(item, 'X') ?? null;
  const y = animationValue(item, 'Y') ?? null;
  const width = isShape ? shapeParameterValue(item, 'Width') ?? null : primitive?.bbox_width ?? null;
  const height = isShape ? shapeParameterValue(item, 'Height') ?? null : primitive?.bbox_height ?? null;
  const screenRect = isShape
    ? { x: x + FRAME.width / 2 - width / 2, y: y + FRAME.height / 2 - height / 2, width, height }
    : { x: x + FRAME.width / 2, y: y + FRAME.height / 2, width, height };
  return {
    display_name: String(item.Remark || ''),
    item_type: type,
    group_id: primitive?.group_id || null,
    role: primitive?.role || null,
    layer: item.Layer,
    x,
    y,
    screen_rect: screenRect,
    width,
    height,
    shape_size_mode: isShape ? item.ShapeParameter?.SizeMode || null : null,
    opacity: animationValue(item, 'Opacity') ?? null,
    fill_color: isShape ? item.ShapeParameter?.Brush?.Parameter?.Color || null : null,
    text: isText ? item.Text : null,
    text_color: isText ? item.FontColor : null,
    font_size: isText ? item.FontSize?.Values?.[0]?.Value ?? null : null,
    layout_contract: primitive?.layout_contract || null,
    description: primitive?.description || null,
  };
}

function countMatches(text, pattern) {
  const matches = text.match(pattern);
  return matches ? matches.length : 0;
}

function tokenLikePattern() {
  const secretPrefix = 's' + 'k-';
  const bearerWord = 'Bear' + 'er';
  const privateKey = 'PRIVATE ' + 'KEY';
  return new RegExp(`\\b(?:${secretPrefix}[A-Za-z0-9_-]{8,}|${bearerWord}\\s+[A-Za-z0-9._-]{8,}|BEGIN [A-Z ]*${privateKey})\\b`, 'g');
}

function imageReferencePattern() {
  return /\.(?:png|jpe?g|webp|gif|bmp|svg)\b/gi;
}

function centerDelta(item) {
  const target = item.layout_contract?.target_box_rect;
  if (!target) return null;
  const itemCenter = rectCenter(item.screen_rect);
  const targetCenter = rectCenter(target);
  return {
    x: Math.round((itemCenter.x - targetCenter.x) * 10) / 10,
    y: Math.round((itemCenter.y - targetCenter.y) * 10) / 10,
  };
}

function labelFitRecord(item) {
  const target = item.layout_contract?.target_box_rect;
  const estimatedWidth = item.layout_contract?.estimated_text_width ?? item.width;
  const margin = target ? Math.round((target.width - estimatedWidth) / 2) : null;
  const delta = centerDelta(item);
  return {
    id: item.display_name,
    text: item.text,
    font_size: item.font_size,
    target_box_id: item.layout_contract?.target_box_id || null,
    target_box_rect: target || null,
    text_rect: item.screen_rect,
    estimated_text_width: estimatedWidth,
    horizontal_margin_each_side_px: margin,
    center_delta_px: delta,
    fits_target_box: Boolean(target && item.screen_rect.x >= target.x && rectRight(item.screen_rect) <= rectRight(target)),
    center_aligned: Boolean(delta && Math.abs(delta.x) <= 1 && Math.abs(delta.y) <= 4),
  };
}

function targetedLabelStatus(records, minimumMarginPx) {
  const passed = records.length > 0 && records.every((record) =>
    record.fits_target_box &&
    record.horizontal_margin_each_side_px >= minimumMarginPx &&
    record.center_aligned);
  return {
    passed,
    minimum_margin_px: minimumMarginPx,
    records,
  };
}

function readbackProbe(project, primitivePlan, carrierHashBefore, carrierHashAfter) {
  const primitivesByName = new Map(primitivePlan.primitives.map((primitive) => [primitive.display_name, primitive]));
  const timeline = project.Timelines?.[0] || {};
  const items = (timeline.Items || []).map((item) => readbackItem(item, primitivesByName.get(String(item.Remark || ''))));
  const itemTypes = items.map((item) => item.item_type);
  const shapeItems = items.filter((item) => item.item_type === 'ShapeItem');
  const textItems = items.filter((item) => item.item_type === 'TextItem');
  const focalLabels = textItems.filter((item) => item.role === 'focal_chain_label');
  const calloutLabelsReadback = textItems.filter((item) => item.role === 'callout_label');
  const hosts = items.filter((item) => item.group_id === 'G28_LDC_Hosts');
  const focalCore = items.find((item) => item.display_name === 'G28_LDC_Focal_Core');
  const frameContract = primitivePlan.frame_contract;
  const captionReserve = frameContract.caption_reserve;
  const mainCanvas = frameContract.main_canvas;
  const captionOverlaps = items.filter((item) =>
    item.display_name !== 'G28_LDC_BG_Stage' &&
    item.display_name !== 'G28_LDC_Host_Left' &&
    item.display_name !== 'G28_LDC_Host_Right' &&
    overlaps(item.screen_rect, captionReserve));
  const missing = primitivePlan.primitives
    .map((primitive) => primitive.display_name)
    .filter((name) => !items.some((item) => item.display_name === name));
  const textChars = textItems.reduce((sum, item) => sum + String(item.text || '').length, 0);
  const projectText = JSON.stringify(project);
  const externalImageCount = countMatches(projectText, imageReferencePattern());
  const externalUrlCount = countMatches(projectText, /\bhttps?:\/\/[^\s"']+/gi);
  const sourceFootageCount = countMatches(projectText, /source[-_ ]?footage|gameplay[-_ ]?(?:screen|screenshot|capture|footage)/gi);
  const audioItemCount = items.filter((item) => item.item_type === 'AudioItem').length;
  const ttsOrVoiceItemCount = items.filter((item) => /VoiceItem|TachieItem/.test(item.item_type)).length;
  const tokenLikePatternCount = countMatches(projectText, tokenLikePattern());
  const labelTexts = focalLabels.map((item) => item.text);
  const calloutTexts = calloutLabelsReadback.map((item) => item.text);
  const rightFocalLabel = focalLabels.find((item) => item.display_name === 'G28_LDC_Node_Right_Label');
  const rightFocalFit = targetedLabelStatus(rightFocalLabel ? [labelFitRecord(rightFocalLabel)] : [], 12);
  const calloutAlignment = targetedLabelStatus(calloutLabelsReadback.map(labelFitRecord), 18);
  const overflowTargets = [
    ...(rightFocalLabel ? [rightFocalLabel] : []),
    ...calloutLabelsReadback,
  ].map(labelFitRecord);
  const labelOverflowPassed = overflowTargets.every((record) => record.fits_target_box);
  const checks = {
    diagnostic_only: true,
    production_candidate_false: true,
    carrier_kind_expected: primitivePlan.carrier_kind === carrierKind,
    variant_expected: primitivePlan.variant === variant,
    source_artifact_id_expected: primitivePlan.source_artifact_id === expectedSourceArtifactId,
    variant_id_expected: primitivePlan.variant_id === expectedVariantId,
    self_contained_ymmp_probe_created: itemTypes.every((type) => ['ShapeItem', 'TextItem'].includes(type)),
    frame_16_9_1920_1080: frameContract.width === 1920 && frameContract.height === 1080 && frameContract.aspect_ratio === '16:9',
    focal_chain_count_3: focalLabels.length === 3,
    focal_chain_labels_expected: focalChainLabels.every((label) => labelTexts.includes(label)),
    callout_count_3: calloutLabelsReadback.length === 3,
    callout_labels_expected: calloutLabels.every((label) => calloutTexts.includes(label)),
    bottom_caption_reserve_clear: captionOverlaps.length === 0,
    focal_area_in_main_canvas: Boolean(focalCore?.screen_rect && inRegion(focalCore.screen_rect, mainCanvas)),
    host_role_non_focal: hosts.length === 2 && hosts.every((item) => item.role === 'decoration' && rectBottom(item.screen_rect) <= captionReserve.y),
    diagnostic_text_budget_bounded: textItems.length <= diagnosticTextBudget.max_visible_text_items && textChars <= diagnosticTextBudget.max_visible_chars,
    dense_table_false: true,
    indexed_whiteboard_false: true,
    external_image_count_zero: externalImageCount === 0,
    external_url_count_zero: externalUrlCount === 0,
    source_footage_count_zero: sourceFootageCount === 0,
    audio_item_count_zero: audioItemCount === 0,
    tts_or_voice_item_count_zero: ttsOrVoiceItemCount === 0,
    render_output_false: true,
    production_approval_false: true,
    creative_final_acceptance_false: true,
    rights_approval_false: true,
    token_like_pattern_count_zero: tokenLikePatternCount === 0,
    carrier_not_modified_in_place: carrierHashBefore === carrierHashAfter,
    right_focal_label_fit: rightFocalFit.passed,
    callout_label_alignment: calloutAlignment.passed,
    label_overflow_absent: labelOverflowPassed,
  };
  const failures = Object.entries(checks)
    .filter(([, ok]) => ok !== true)
    .map(([name]) => name);
  return {
    artifact_type: 'g28_game_mechanics_ymmp_diagnostic_probe_readback',
    probe_artifact_id: probeArtifactId,
    source_artifact_id: primitivePlan.source_artifact_id,
    variant_id: primitivePlan.variant_id,
    carrier_kind: carrierKind,
    variant,
    diagnostic_only: true,
    production_candidate: false,
    status: failures.length === 0 && missing.length === 0 ? 'passed' : 'failed',
    classification: failures.length === 0 && missing.length === 0 ? creationRecord.classification : 'fail_game_mechanics_ymmp_diagnostic_carrier_readback',
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
      gameplay_screenshot_intake: false,
      external_material_intake: false,
      audio_or_tts: false,
      image_or_url_or_raw_reference: false,
      real_estate_reopened: false,
      newsroom_handoff_processed: false,
      g27_revival: false,
      rss_or_notebooklm_work: false,
    },
    frame_contract: {
      width: frameContract.width,
      height: frameContract.height,
      aspect_ratio: frameContract.aspect_ratio,
      caption_reserve: captionReserve,
      main_canvas: mainCanvas,
    },
    totals: {
      item_count: items.length,
      expected_item_count: primitivePlan.primitives.length,
      shape_item_count: shapeItems.length,
      text_item_count: textItems.length,
      visible_text_chars: textChars,
      missing_item_count: missing.length,
      focal_chain_count: focalLabels.length,
      callout_count: calloutLabelsReadback.length,
    },
    focal_chain_count: focalLabels.length,
    callout_count: calloutLabelsReadback.length,
    bottom_caption_reserve_status: {
      clear: captionOverlaps.length === 0,
      rect: captionReserve,
      overlaps: captionOverlaps.map((item) => item.display_name),
    },
    host_role: 'non_focal',
    external_image_count: externalImageCount,
    external_url_count: externalUrlCount,
    source_footage_count: sourceFootageCount,
    audio_item_count: audioItemCount,
    tts_or_voice_item_count: ttsOrVoiceItemCount,
    render_output: false,
    production_approval: false,
    one_pass_targeted_fix: layoutOutcome.one_pass_targeted_fix,
    no_further_micro_tuning_recommended: layoutOutcome.no_further_micro_tuning_recommended,
    next_decision_gate: layoutOutcome.next_decision_gate,
    next_decision_gate_options: layoutOutcome.next_decision_gate_options,
    right_focal_label_fit_status: {
      status: rightFocalFit.passed ? 'fits_after_one_pass_targeted_fix' : 'fit_unverified_or_failed',
      issue_addressed: '`画面上の結果` was visually cramped in the right focal node.',
      correction: 'Removed the inherited rightward nudge and reduced only the right focal label font size from 42 to 38 while keeping the label text and node geometry unchanged.',
      ...rightFocalFit,
    },
    callout_label_alignment_status: {
      status: calloutAlignment.passed ? 'common_centering_rule_applied' : 'alignment_unverified_or_failed',
      issue_addressed: '`判定 / 当たり判定` and `リスクとリターン` looked left-aligned in the lower callout boxes.',
      correction: 'Applied one common callout label rule with font size 28, zero horizontal offset, and centered placement inside each unchanged callout slot.',
      ...calloutAlignment,
    },
    label_overflow_check: {
      passed: labelOverflowPassed,
      scope: 'right focal label plus three lower callout labels',
      records: overflowTargets,
    },
    checks,
    failures,
    missing_items: missing,
    focal_chain_readback: {
      labels: labelTexts,
      source_middle_label: primitivePlan.source_readback_middle_label,
      diagnostic_probe_middle_label: focalChainLabels[1],
      note: 'YMM4 diagnostic probe makes the semantics-note middle emphasis visible as 内部ルール / 判定; this is review-only text, not production copy approval.',
      items: focalLabels.map((item) => ({
        id: item.display_name,
        text: item.text,
        rect: item.screen_rect,
      })),
    },
    callout_readback: {
      labels: calloutTexts,
      items: calloutLabelsReadback.map((item) => ({
        id: item.display_name,
        text: item.text,
        rect: item.screen_rect,
      })),
    },
    host_role_readback: {
      role: 'non_focal_lower_corner_decoration_emotional_anchor',
      hosts: hosts.map((item) => ({
        id: item.display_name,
        rect: item.screen_rect,
        above_caption_reserve: rectBottom(item.screen_rect) <= captionReserve.y,
      })),
    },
    text_budget_readback: {
      visible_text_item_count: textItems.length,
      visible_text_chars: textChars,
      max_visible_text_items: diagnosticTextBudget.max_visible_text_items,
      max_visible_chars: diagnosticTextBudget.max_visible_chars,
      production_text_budget_claimed: false,
      note: 'Visible labels exist so a human can review the carrier in YMM4; they are not slot-fill or production text-budget approval.',
    },
    safety_readback: {
      external_image_count: externalImageCount,
      external_url_count: externalUrlCount,
      source_footage_count: sourceFootageCount,
      audio_item_count: audioItemCount,
      tts_or_voice_item_count: ttsOrVoiceItemCount,
      token_like_pattern_count: tokenLikePatternCount,
      image_binary: false,
      image_path: false,
      image_url: false,
      raw_reference: false,
    },
    source_integrity: {
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    next_review_inputs_required: nextReviewInputsRequired,
    known_caveats: [
      'This is a self-contained YMM4 diagnostic carrier candidate, not a production carrier.',
      'The one-pass targeted layout fix is verified by builder/readback geometry; final YMM4 visual recheck remains human-owned.',
      'Visible node and callout labels are review aids and do not approve production slot-fill or final copy.',
      'No render, video, audio, source footage, gameplay screenshot, external image, URL, raw reference, rights automation, or creative final acceptance is included.',
      'Do not continue same-screen micro-tuning. If the two targeted labels still fail visually, classify the remaining problem as layout_system_debt or redesign_required.',
    ],
    items,
  };
}

function renderReport(readback) {
  const lines = [];
  lines.push('# G-28 Game Mechanics YMM4 Diagnostic Carrier Probe');
  lines.push('');
  lines.push(`Probe artifact: \`${readback.probe_artifact_id}\``);
  lines.push(`Source artifact: \`${readback.source_artifact_id}\``);
  lines.push(`Variant id: \`${readback.variant_id}\``);
  lines.push('');
  lines.push('This is a self-contained YMM4-compatible diagnostic carrier candidate for human review. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, gameplay screenshot intake, or slot-fill.');
  lines.push('');
  lines.push('## Generated Files');
  lines.push('');
  lines.push(`- YMM4 probe: \`${readback.generated_files.ymmp}\``);
  lines.push(`- readback JSON: \`${readback.generated_files.readback_json}\``);
  lines.push(`- report: \`${readback.generated_files.report_md}\``);
  lines.push('');
  lines.push('## Relationship To HTML/Readback Precedent');
  lines.push('');
  lines.push('- Source precedent: `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*`.');
  lines.push('- The existing HTML/readback diagnostic surface was accepted for reviewability only.');
  lines.push('- This probe turns that diagnostic shape into a YMM4-openable, ShapeItem/TextItem-only carrier candidate so the next human review can inspect YMM4 preview/timeline evidence.');
  lines.push('- The middle node is visible as `内部ルール / 判定` to carry the semantics-note emphasis; this is diagnostic review text, not production copy approval.');
  lines.push('');
  lines.push('## One-pass Targeted Layout Fix');
  lines.push('');
  lines.push('- This update is a one-pass targeted layout fix for the current YMM4 diagnostic carrier candidate.');
  lines.push('- It does not change the carrier variant, focal-chain meaning, callout meaning, host role, bottom caption reserve, or diagnostic-only boundary.');
  lines.push('- Right focal label fix: `画面上の結果` keeps the same text and node, but the inherited rightward nudge was removed and the right-label font size was reduced from 42 to 38.');
  lines.push('- Lower callout fix: all callout labels now use one common centered rule with font size 28 and zero horizontal offset.');
  lines.push('- Do not continue same-screen micro-tuning. The next human review is only the two targeted fit/alignment checks below.');
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
  lines.push(`- bottom caption reserve: clear=\`${readback.bottom_caption_reserve_status.clear}\`, y=${readback.bottom_caption_reserve_status.rect.y}, h=${readback.bottom_caption_reserve_status.rect.height}`);
  lines.push(`- focal chain labels: ${readback.focal_chain_readback.labels.join(' -> ')}`);
  lines.push(`- callout labels: ${readback.callout_readback.labels.join(' / ')}`);
  lines.push(`- host role: \`${readback.host_role_readback.role}\``);
  lines.push(`- visible text: ${readback.text_budget_readback.visible_text_item_count} items / ${readback.text_budget_readback.visible_text_chars} chars`);
  lines.push(`- one-pass targeted fix: \`${readback.one_pass_targeted_fix}\``);
  lines.push(`- no further micro-tuning recommended: \`${readback.no_further_micro_tuning_recommended}\``);
  lines.push(`- next decision gate: \`${readback.next_decision_gate}\``);
  lines.push('');
  lines.push('## Layout Fix Readback');
  lines.push('');
  lines.push(`- right focal label fit: \`${readback.right_focal_label_fit_status.status}\``);
  for (const record of readback.right_focal_label_fit_status.records) {
    lines.push(`  - ${record.id}: font=${record.font_size}, margin_each_side=${record.horizontal_margin_each_side_px}px, center_delta=(${record.center_delta_px.x}, ${record.center_delta_px.y}), fits=${record.fits_target_box}`);
  }
  lines.push(`- callout label alignment: \`${readback.callout_label_alignment_status.status}\``);
  for (const record of readback.callout_label_alignment_status.records) {
    lines.push(`  - ${record.id}: font=${record.font_size}, margin_each_side=${record.horizontal_margin_each_side_px}px, center_delta=(${record.center_delta_px.x}, ${record.center_delta_px.y}), fits=${record.fits_target_box}`);
  }
  lines.push(`- label overflow check: \`${readback.label_overflow_check.passed}\``);
  lines.push('');
  lines.push('## Checks');
  lines.push('');
  for (const [key, value] of Object.entries(readback.checks)) {
    lines.push(`- \`${key}\`: \`${value}\``);
  }
  lines.push('');
  lines.push('## YMM4 Human Review Intake');
  lines.push('');
  lines.push('- Open the probe in YMM4 and confirm the project opens without error.');
  lines.push('- Capture a preview screenshot showing the carrier surface.');
  lines.push('- Capture a timeline screenshot showing title, focal chain, callouts, hosts, and caption reserve items/layers.');
  lines.push('- Confirm the chain reads `入力操作 -> 内部ルール / 判定 -> 画面上の結果`.');
  lines.push('- Confirm the callouts read `操作感`, `判定 / 当たり判定`, and `リスクとリターン` without becoming a dense table.');
  lines.push('- Confirm the hosts stay non-focal lower-corner decoration.');
  lines.push('- Confirm the bottom caption reserve is visually clear.');
  lines.push('- Targeted recheck only: confirm `画面上の結果` is inside the right node.');
  lines.push('- Targeted recheck only: confirm `判定 / 当たり判定` and `リスクとリターン` look centered in their callout boxes.');
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
  lines.push('');
  return lines.join('\n');
}

function assertReadback(readback) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.diagnostic_only !== true) failures.push('diagnostic_only is not true');
  if (readback.production_candidate !== false) failures.push('production_candidate is not false');
  if (readback.boundary.render_output !== false) failures.push('render_output is not false');
  if (readback.boundary.creative_final_acceptance !== false) failures.push('creative_final_acceptance is not false');
  if (readback.external_image_count !== 0) failures.push(`external_image_count=${readback.external_image_count}`);
  if (readback.external_url_count !== 0) failures.push(`external_url_count=${readback.external_url_count}`);
  if (readback.source_footage_count !== 0) failures.push(`source_footage_count=${readback.source_footage_count}`);
  if (readback.audio_item_count !== 0) failures.push(`audio_item_count=${readback.audio_item_count}`);
  if (readback.tts_or_voice_item_count !== 0) failures.push(`tts_or_voice_item_count=${readback.tts_or_voice_item_count}`);
  if (readback.one_pass_targeted_fix !== true) failures.push('one_pass_targeted_fix is not true');
  if (readback.no_further_micro_tuning_recommended !== true) failures.push('no_further_micro_tuning_recommended is not true');
  if (readback.right_focal_label_fit_status?.passed !== true) failures.push('right focal label fit did not pass');
  if (readback.callout_label_alignment_status?.passed !== true) failures.push('callout label alignment did not pass');
  if (readback.label_overflow_check?.passed !== true) failures.push('label overflow check did not pass');
  if (readback.totals.missing_item_count !== 0) failures.push(`missing items: ${readback.missing_items.join(', ')}`);
  if (readback.failures.length) failures.push(`failed checks: ${readback.failures.join(', ')}`);
  if (failures.length) throw new Error(`G28_GAME_MECHANICS_YMMP_PROBE_READBACK_FAILED: ${failures.join('; ')}`);
}

function main() {
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const source = readJson(paths.sourceJson);
  const sourceReadback = readJson(paths.sourceReadback);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplateYmmp = readJson(paths.shapeTemplateYmmp);
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
    console.log(`G-28 game-mechanics YMM4 diagnostic probe written: ${paths.outputYmmp}`);
    console.log(`Readback: ${paths.readbackJson}`);
    console.log(`Report: ${paths.reportMd}`);
    console.log(`status=${writtenReadback.status}, classification=${writtenReadback.classification}, items=${writtenReadback.totals.item_count}`);
    return;
  }

  if (!fs.existsSync(abs(paths.outputYmmp))) {
    throw new Error(`OUTPUT_YMMP_MISSING: run with --write first (${paths.outputYmmp})`);
  }
  const existing = readJson(paths.outputYmmp);
  const storedReadback = readJson(paths.readbackJson);
  const actualReadback = readbackProbe(existing, primitivePlan, carrierHashBefore, sha256(paths.carrierYmmp));
  assertReadback(actualReadback);
  assertReadback(storedReadback);
  if (JSON.stringify(actualReadback) !== JSON.stringify(storedReadback)) {
    throw new Error('READBACK_DRIFT');
  }
  console.log(`G-28 game-mechanics YMM4 diagnostic probe OK: classification=${actualReadback.classification}, items=${actualReadback.totals.item_count}`);
}

main();

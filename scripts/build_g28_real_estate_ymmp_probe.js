// G-28 real_estate_information_gap YMM4-compatible diagnostic probe.
// Builds a self-contained ShapeItem/TextItem-only .ymmp from the accepted
// Lecture Diagram Carrier diagnostic variant.
// No external images, URLs, source footage, audio, render, or production approval.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  sourceJson: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.json',
  sourceReadback: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_readback.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp',
  readbackJson: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json',
  reportMd: 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md',
};

const FRAME = { width: 1920, height: 1080 };
const DURATION_FRAMES = 600;
const shapeSizeMode = 'WidthHeight';
const expectedVariantId = 'g28_ldc_real_estate_information_gap';
const expectedSourceArtifactId = 'g28_lecture_diagram_carrier_real_estate_information_gap_v1';
const probeArtifactId = 'g28_lecture_diagram_carrier_real_estate_information_gap_ymmp_probe_v1';
const diagnosticTextBudget = {
  max_visible_text_items: 8,
  max_visible_chars: 60,
  production_text_budget_claimed: false,
};
const polishRevision = {
  revision_id: 'g28_real_estate_information_gap_ymmp_polish_v1',
  source_human_decision: 'revise_probe',
  classification: 'pass_probe_polished',
  bounded_scope: [
    'yellow connector alignment',
    'rectangle text centering',
    'callout spacing',
    'small visual offsets',
  ],
  boundary_note: 'Diagnostic-only polish revision; no production approval, render, slot-fill, image, URL, audio, TTS, or source footage.',
};
const polishedShapeRects = {
  G28_LDC_Connector_Left: { x: 490, y: 394, width: 70, height: 12 },
  G28_LDC_Connector_Right: { x: 1360, y: 394, width: 70, height: 12 },
  G28_LDC_CalloutSlot_1: { x: 375, y: 642, width: 330, height: 90 },
  G28_LDC_CalloutSlot_2: { x: 795, y: 642, width: 330, height: 90 },
  G28_LDC_CalloutSlot_3: { x: 1215, y: 642, width: 330, height: 90 },
};
const textVisualOffsets = {
  G28_LDC_Title_Text: { x: 0, y: -2 },
  G28_LDC_Node_Left_Label: { x: 0, y: -4 },
  G28_LDC_Node_Center_Label: { x: 0, y: -4 },
  G28_LDC_Node_Right_Label: { x: 0, y: -4 },
  G28_LDC_CalloutSlot_1_Label: { x: 0, y: -3 },
  G28_LDC_CalloutSlot_2_Label: { x: 0, y: -3 },
  G28_LDC_CalloutSlot_3_Label: { x: 0, y: -3 },
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
  return {
    x: rect.x + rect.width / 2,
    y: rect.y + rect.height / 2,
  };
}
function polishedRectFor(item) {
  return polishedShapeRects[item.id] || item.rect;
}
function screenRectToYmm4Center(rect) {
  const center = rectCenter(rect);
  return {
    x: center.x - FRAME.width / 2,
    y: center.y - FRAME.height / 2,
  };
}
function screenTopLeftToYmm4(topLeft) {
  return {
    x: topLeft.x - FRAME.width / 2,
    y: topLeft.y - FRAME.height / 2,
  };
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
  const rect = polishedRectFor(item);
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
    stroke_thickness: rect.height,
    description: `G-28 source carrier primitive ${item.id}`,
  };
}

function centeredTextPrimitive(displayName, groupId, role, layer, centerScreen, fontSize, content, color, description) {
  const bboxWidth = estimateTextWidth(content, fontSize);
  const bboxHeight = fontSize;
  const visualOffset = textVisualOffsets[displayName] || { x: 0, y: 0 };
  const adjustedCenter = {
    x: centerScreen.x + visualOffset.x,
    y: centerScreen.y + visualOffset.y,
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
    intent_screen_cx: adjustedCenter.x,
    intent_screen_cy: adjustedCenter.y,
    source_intent_screen_cx: centerScreen.x,
    source_intent_screen_cy: centerScreen.y,
    visual_offset_px: visualOffset,
    bbox_width: bboxWidth,
    bbox_height: bboxHeight,
    font_size: fontSize,
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
  const focalChain = sourceReadback.variant_readback.focal_chain;
  const callouts = sourceReadback.variant_readback.callouts;
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
      rectCenter(polishedRectFor(title)),
      52,
      titleText,
      labelColor,
      'short title label from accepted diagnostic variant',
    ),
  ];

  const leftNode = byId.get('G28_LDC_Node_Left');
  const focalCore = byId.get('G28_LDC_Focal_Core');
  const rightNode = byId.get('G28_LDC_Node_Right');
  const focalLabelTargets = [
    { item: leftNode, label: focalChain[0].label, displayName: 'G28_LDC_Node_Left_Label' },
    { item: focalCore, label: focalChain[1].label, displayName: 'G28_LDC_Node_Center_Label' },
    { item: rightNode, label: focalChain[2].label, displayName: 'G28_LDC_Node_Right_Label' },
  ];
  for (const target of focalLabelTargets) {
    textPrimitives.push(centeredTextPrimitive(
      target.displayName,
      'G28_LDC_FocalGroup',
      'focal_chain_label',
      7,
      rectCenter(polishedRectFor(target.item)),
      42,
      target.label,
      nodeColor,
      'visible node label for YMM4 GUI diagnostic probe',
    ));
  }

  for (const callout of callouts) {
    const slot = byId.get(callout.slot);
    textPrimitives.push(centeredTextPrimitive(
      `${callout.slot}_Label`,
      'G28_LDC_CalloutSlots',
      'callout_label',
      9,
      rectCenter(polishedRectFor(slot)),
      30,
      callout.label,
      calloutColor,
      'visible callout label for YMM4 GUI diagnostic probe',
    ));
  }

  return {
    source_artifact_id: source.artifact_id,
    variant_id: source.variant_id,
    source_theme_variant: source.theme_variant,
    frame_contract: source.frame_contract,
    scs_mapping: source.scs_mapping,
    polish_revision: polishRevision,
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
  const screenRect = (() => {
    if (isShape) {
      return {
        x: x + FRAME.width / 2 - width / 2,
        y: y + FRAME.height / 2 - height / 2,
        width,
        height,
      };
    }
    return {
      x: x + FRAME.width / 2,
      y: y + FRAME.height / 2,
      width,
      height,
    };
  })();
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
    stroke_thickness: isShape ? shapeParameterValue(item, 'StrokeThickness') ?? null : null,
    round: isShape ? shapeParameterValue(item, 'Round') ?? null : null,
    opacity: animationValue(item, 'Opacity') ?? null,
    fill_color: isShape ? item.ShapeParameter?.Brush?.Parameter?.Color || null : null,
    text: isText ? item.Text : null,
    text_color: isText ? item.FontColor : null,
    font_size: isText ? item.FontSize?.Values?.[0]?.Value ?? null : null,
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

function layerStats(items, filterFn) {
  const layers = items.filter(filterFn).map((item) => item.layer);
  if (!layers.length) return null;
  return { min: Math.min(...layers), max: Math.max(...layers), layers };
}

function readbackProbe(ymmp, primitivePlan, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const primitivesByName = new Map(primitivePlan.primitives.map((primitive) => [primitive.display_name, primitive]));
  const items = timelineItems.map((item) => readbackItem(item, primitivesByName.get(String(item.Remark || ''))));
  const missing = primitivePlan.primitives
    .filter((primitive) => !items.find((item) => item.display_name === primitive.display_name))
    .map((primitive) => primitive.display_name);
  const itemTypes = items.map((item) => item.item_type);
  const textItems = items.filter((item) => item.item_type === 'TextItem');
  const shapeItems = items.filter((item) => item.item_type === 'ShapeItem');
  const serialized = JSON.stringify(ymmp);
  const sourceVariant = primitivePlan.source_theme_variant;
  const frameContract = primitivePlan.frame_contract;
  const captionReserve = frameContract.caption_reserve;
  const mainCanvas = frameContract.main_canvas;
  const captionOverlaps = items.filter((item) => (
    item.display_name !== 'G28_LDC_BG_Stage' &&
    item.screen_rect &&
    overlaps(item.screen_rect, captionReserve)
  ));
  const focalCore = items.find((item) => item.display_name === 'G28_LDC_Focal_Core');
  const hosts = items.filter((item) => item.display_name.startsWith('G28_LDC_Host_'));
  const calloutShapes = items.filter((item) => /^G28_LDC_CalloutSlot_\d$/.test(item.display_name));
  const calloutLabels = items.filter((item) => /^G28_LDC_CalloutSlot_\d_Label$/.test(item.display_name));
  const focalLabels = items.filter((item) => item.role === 'focal_chain_label');
  const visibleTextChars = textItems.reduce((sum, item) => sum + [...String(item.text || '')].length, 0);
  const stageLayers = layerStats(items, (item) => item.display_name === 'G28_LDC_BG_Stage');
  const titleLayers = layerStats(items, (item) => item.group_id === 'G28_LDC_TitleBand');
  const focalSurfaceLayers = layerStats(items, (item) => ['G28_LDC_Focal_Core', 'G28_LDC_Node_Left', 'G28_LDC_Node_Right'].includes(item.display_name));
  const connectorLayers = layerStats(items, (item) => item.role === 'connector');
  const focalLabelLayers = layerStats(items, (item) => item.role === 'focal_chain_label');
  const calloutLayers = layerStats(items, (item) => item.group_id === 'G28_LDC_CalloutSlots');
  const hostLayers = layerStats(items, (item) => item.group_id === 'G28_LDC_Hosts');
  const layerOrderMatches = Boolean(
    stageLayers && titleLayers && focalSurfaceLayers && connectorLayers && focalLabelLayers && calloutLayers && hostLayers &&
    stageLayers.max < titleLayers.min &&
    titleLayers.max < focalSurfaceLayers.min &&
    focalSurfaceLayers.max < connectorLayers.min &&
    connectorLayers.max < focalLabelLayers.min &&
    focalLabelLayers.max < calloutLayers.min &&
    calloutLayers.max < hostLayers.min
  );
  const textBudgetPass = textItems.length <= diagnosticTextBudget.max_visible_text_items &&
    visibleTextChars <= diagnosticTextBudget.max_visible_chars;
  const externalImageCount = itemTypes.filter((type) => type === 'ImageItem').length + countMatches(serialized, imageReferencePattern());
  const externalUrlCount = countMatches(serialized, /https?:\/\//gi);
  const sourceFootageCount = itemTypes.filter((type) => ['VideoItem'].includes(type)).length;
  const audioItemCount = itemTypes.filter((type) => ['AudioItem'].includes(type)).length;
  const ttsOrVoiceItemCount = itemTypes.filter((type) => ['VoiceItem'].includes(type)).length;
  const tokenLikePatternCount = countMatches(serialized, tokenLikePattern());
  const checks = {
    diagnostic_only: true,
    production_candidate_false: true,
    source_artifact_id_expected: primitivePlan.source_artifact_id === expectedSourceArtifactId,
    variant_id_expected: primitivePlan.variant_id === expectedVariantId,
    self_contained_ymmp_probe_created: itemTypes.every((type) => ['ShapeItem', 'TextItem'].includes(type)),
    frame_16_9_1920_1080: frameContract.width === 1920 && frameContract.height === 1080 && frameContract.aspect_ratio === '16:9',
    caption_reserve_bottom_20pct: captionReserve.y === 810 && captionReserve.height === 216,
    caption_reserve_clear: captionOverlaps.length === 0,
    focal_area_in_main_canvas: Boolean(focalCore?.screen_rect && inRegion(focalCore.screen_rect, mainCanvas)),
    focal_chain_nodes_3: focalLabels.length === 3,
    focal_chain_labels_expected: ['元付情報', 'ポータル掲載', '借主判断'].every((label) => focalLabels.some((item) => item.text === label)),
    callout_count_3: calloutShapes.length === 3 && calloutLabels.length === 3,
    callout_labels_expected: ['情報遅延', '掲載粒度の欠落', '仲介インセンティブ'].every((label) => calloutLabels.some((item) => item.text === label)),
    host_role_non_focal: hosts.length === 2 && hosts.every((item) => item.role === 'decoration' && rectBottom(item.screen_rect) <= captionReserve.y),
    layer_order_matches_contract: layerOrderMatches,
    diagnostic_text_budget_bounded: textBudgetPass,
    dense_table_false: true,
    indexed_whiteboard_false: true,
    external_image_count_zero: externalImageCount === 0,
    external_url_count_zero: externalUrlCount === 0,
    source_footage_count_zero: sourceFootageCount === 0,
    audio_item_count_zero: audioItemCount === 0,
    tts_or_voice_item_count_zero: ttsOrVoiceItemCount === 0,
    render_output_false: true,
    creative_final_acceptance_false: true,
    production_approval_false: true,
    token_like_pattern_count_zero: tokenLikePatternCount === 0,
    carrier_not_modified_in_place: carrierHashBefore === carrierHashAfter,
    polish_revision_bounded: primitivePlan.polish_revision.source_human_decision === 'revise_probe' &&
      primitivePlan.polish_revision.classification === 'pass_probe_polished',
  };
  const failures = Object.entries(checks)
    .filter(([, ok]) => ok !== true)
    .map(([name]) => name);
  return {
    artifact_type: 'g28_real_estate_information_gap_ymmp_diagnostic_probe_readback',
    probe_artifact_id: probeArtifactId,
    source_artifact_id: primitivePlan.source_artifact_id,
    variant_id: primitivePlan.variant_id,
    status: failures.length === 0 && missing.length === 0 ? 'passed' : 'failed',
    classification: failures.length === 0 && missing.length === 0 ? primitivePlan.polish_revision.classification : 'fail_ymmp_probe_readback',
    generated_files: {
      ymmp: paths.outputYmmp,
      readback_json: paths.readbackJson,
      report_md: paths.reportMd,
    },
    boundary: {
      diagnostic_only: true,
      production_candidate: false,
      self_contained_ymmp_probe: true,
      production_render: false,
      render_output: false,
      creative_final_acceptance: false,
      production_carrier_approval: false,
      slot_fill: false,
      source_footage_intake: false,
      audio_or_tts: false,
      image_or_url_or_raw_reference: false,
      g27_revival: false,
      rss_or_notebooklm_work: false,
    },
    polish_revision: primitivePlan.polish_revision,
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
      visible_text_chars: visibleTextChars,
      missing_item_count: missing.length,
      callout_count: calloutShapes.length,
      callout_label_count: calloutLabels.length,
      focal_chain_label_count: focalLabels.length,
    },
    checks,
    failures,
    missing_items: missing,
    caption_reserve_readback: {
      rect: captionReserve,
      bottom_percent: 20,
      clear: captionOverlaps.length === 0,
      overlaps: captionOverlaps.map((item) => item.display_name),
    },
    focal_area_readback: {
      composition_type: sourceVariant.composition_type,
      focal_core_rect: focalCore?.screen_rect || null,
      focal_core_in_main_canvas: Boolean(focalCore?.screen_rect && inRegion(focalCore.screen_rect, mainCanvas)),
      focal_chain: sourceVariant.focal_chain,
      visible_node_labels: focalLabels.map((item) => ({
        id: item.display_name,
        text: item.text,
        rect: item.screen_rect,
      })),
    },
    callout_readback: {
      count: calloutShapes.length,
      labels: calloutLabels.map((item) => ({
        id: item.display_name,
        text: item.text,
        rect: item.screen_rect,
      })),
      allowed_min: 2,
      allowed_max: 3,
    },
    host_role_readback: {
      role: 'non_focal_lower_corner_decoration_emotional_anchor',
      hosts: hosts.map((item) => ({
        id: item.display_name,
        rect: item.screen_rect,
        below_focal: item.screen_rect.y > focalCore.screen_rect.y,
        above_caption_reserve: rectBottom(item.screen_rect) <= captionReserve.y,
      })),
    },
    text_budget_readback: {
      visible_text_item_count: textItems.length,
      visible_text_chars: visibleTextChars,
      max_visible_text_items: diagnosticTextBudget.max_visible_text_items,
      max_visible_chars: diagnosticTextBudget.max_visible_chars,
      dense: false,
      production_text_budget_claimed: false,
      note: 'Diagnostic probe labels are visible for YMM4 GUI review only and do not approve a production in-frame text budget.',
      visible_text_items: textItems.map((item) => ({
        id: item.display_name,
        text: item.text,
        role: item.role,
      })),
    },
    layer_order_readback: {
      contract: [
        'stage',
        'title',
        'focal surfaces',
        'connectors',
        'focal labels',
        'callouts',
        'hosts',
      ],
      matches_contract: layerOrderMatches,
      phases: {
        stage: stageLayers,
        title: titleLayers,
        focal_surfaces: focalSurfaceLayers,
        connectors: connectorLayers,
        focal_labels: focalLabelLayers,
        callouts: calloutLayers,
        hosts: hostLayers,
      },
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
    ymm4_mapping: {
      note: 'YMM4 Group remains 0; logical groups are recorded in readback and item Remarks for a simple static diagnostic probe.',
      groups: [
        { group_id: 'G28_LDC_Stage', ymm4_items: items.filter((item) => item.group_id === 'G28_LDC_Stage').map((item) => item.display_name) },
        { group_id: 'G28_LDC_TitleBand', ymm4_items: items.filter((item) => item.group_id === 'G28_LDC_TitleBand').map((item) => item.display_name) },
        { group_id: 'G28_LDC_FocalGroup', ymm4_items: items.filter((item) => item.group_id === 'G28_LDC_FocalGroup').map((item) => item.display_name) },
        { group_id: 'G28_LDC_CalloutSlots', ymm4_items: items.filter((item) => item.group_id === 'G28_LDC_CalloutSlots').map((item) => item.display_name) },
        { group_id: 'G28_LDC_Hosts', ymm4_items: items.filter((item) => item.group_id === 'G28_LDC_Hosts').map((item) => item.display_name) },
      ],
    },
    source_integrity: {
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    items,
    limitations: [
      'This is a self-contained diagnostic probe, not production carrier approval.',
      'This revision addresses bounded human-review polish only after revise_probe; it does not change the diagnostic-only boundary.',
      'It uses visible node/callout labels for GUI review; this does not approve production text density.',
      'No render, video, audio, source footage, external image, URL, raw reference, rights automation, or slot-fill is included.',
    ],
  };
}

function renderReport(readback) {
  const lines = [];
  lines.push('# G-28 Real Estate Information Gap YMM4 Diagnostic Probe');
  lines.push('');
  lines.push(`Probe artifact: \`${readback.probe_artifact_id}\``);
  lines.push(`Source artifact: \`${readback.source_artifact_id}\``);
  lines.push(`Variant id: \`${readback.variant_id}\``);
  lines.push('');
  lines.push('This is a self-contained YMM4-compatible diagnostic probe. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, or slot-fill.');
  lines.push('');
  lines.push('## Polish Revision');
  lines.push('');
  lines.push(`- revision id: \`${readback.polish_revision.revision_id}\``);
  lines.push(`- source human decision: \`${readback.polish_revision.source_human_decision}\``);
  lines.push(`- bounded scope: ${readback.polish_revision.bounded_scope.map((item) => `\`${item}\``).join(', ')}`);
  lines.push(`- boundary note: ${readback.polish_revision.boundary_note}`);
  lines.push('');
  lines.push('## Generated Files');
  lines.push('');
  lines.push(`- YMM4 probe: \`${readback.generated_files.ymmp}\``);
  lines.push(`- readback JSON: \`${readback.generated_files.readback_json}\``);
  lines.push(`- report: \`${readback.generated_files.report_md}\``);
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
  lines.push(`- frame: ${readback.frame_contract.width}x${readback.frame_contract.height} / ${readback.frame_contract.aspect_ratio}`);
  lines.push(`- caption reserve: y=${readback.caption_reserve_readback.rect.y}, h=${readback.caption_reserve_readback.rect.height}, clear=\`${readback.caption_reserve_readback.clear}\``);
  lines.push(`- focal chain labels: ${readback.focal_area_readback.visible_node_labels.map((item) => item.text).join(' -> ')}`);
  lines.push(`- callout labels: ${readback.callout_readback.labels.map((item) => item.text).join(' / ')}`);
  lines.push(`- host role: \`${readback.host_role_readback.role}\``);
  lines.push(`- visible text: ${readback.text_budget_readback.visible_text_item_count} items / ${readback.text_budget_readback.visible_text_chars} chars`);
  lines.push('');
  lines.push('## Checks');
  lines.push('');
  for (const [key, value] of Object.entries(readback.checks)) {
    lines.push(`- \`${key}\`: \`${value}\``);
  }
  lines.push('');
  lines.push('## YMM4 Mapping');
  lines.push('');
  for (const group of readback.ymm4_mapping.groups) {
    lines.push(`- \`${group.group_id}\`: ${group.ymm4_items.map((item) => `\`${item}\``).join(', ')}`);
  }
  lines.push('');
  lines.push('## Human GUI Check');
  lines.push('');
  lines.push('- Open the probe in YMM4 and confirm the project opens without error.');
  lines.push('- Confirm the focal chain reads as `元付情報 -> ポータル掲載 -> 借主判断`.');
  lines.push('- Confirm the bottom caption reserve remains visually clear.');
  lines.push('- Confirm the three callouts are readable without becoming a table.');
  lines.push('- Confirm the hosts stay lower-corner, non-focal, and non-evidence-like.');
  lines.push('- Confirm the surface does not imply a real listing, real portal, real property, render approval, rights approval, or production use.');
  lines.push('');
  lines.push('## Limitations');
  lines.push('');
  for (const limitation of readback.limitations) {
    lines.push(`- ${limitation}`);
  }
  lines.push('');
  return `${lines.join('\n')}`;
}

function assertReadback(readback) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.boundary.diagnostic_only !== true) failures.push('diagnostic_only is not true');
  if (readback.boundary.production_candidate !== false) failures.push('production_candidate is not false');
  if (readback.boundary.production_render !== false) failures.push('production_render is not false');
  if (readback.boundary.creative_final_acceptance !== false) failures.push('creative_final_acceptance is not false');
  if (readback.totals.missing_item_count !== 0) failures.push(`missing items: ${readback.missing_items.join(', ')}`);
  if (readback.failures.length) failures.push(`failed checks: ${readback.failures.join(', ')}`);
  if (failures.length) throw new Error(`G28_YMMP_PROBE_READBACK_FAILED: ${failures.join('; ')}`);
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
    console.log(`G-28 real-estate YMM4 diagnostic probe written: ${paths.outputYmmp}`);
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
  console.log(`G-28 real-estate YMM4 diagnostic probe OK: classification=${actualReadback.classification}, items=${actualReadback.totals.item_count}`);
}

main();

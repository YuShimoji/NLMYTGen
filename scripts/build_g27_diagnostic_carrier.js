const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const fps = 60;

const paths = {
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_readback.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_report.md',
};

const shapeSizeMode = 'WidthHeight';
const maxDisplayNameLength = 32;
const maxRemarkLength = 80;
const hexColorPattern = /^#[0-9A-Fa-f]{8}$/;

const sceneFrame = {
  frame: 0,
  duration_frames: 600,
  canvas: { width: 1920, height: 1080 },
  tonal_system: 'light-stage',
  background_color: '#FFF0F4F8',
};

// SCS §1 Composition Grid: 1920x1080
//   outer safe band 5%       : top y=0-54, bottom y=1026-1080, left x=0-96, right x=1824-1920
//   title band 8-12%         : y=54-140
//   main canvas 60-65%       : y=140-842
//   caption safe area 18-22% : y=842-1026
//
// YMM4 uses center-origin coordinates: cx = px_x - 960, cy = px_y - 540
//   title band      : cy = -486..-400 (use cy=-455 / height=86)
//   main canvas     : cy = -400..302
//   caption safe    : cy = 302..486 (no items here)
//
// SCS §2.1 split:
//   left panel x=96-826      -> center cx=-499, width=730
//   boundary  x=826-1094     -> center cx=0,    width=268
//   right panel x=1094-1824  -> center cx=499,  width=730
const grid = {
  title_band: { cy: -443, height: 86 },
  main_canvas: { cy_top: -400, cy_bottom: 302, height: 702 },
  caption_safe_area: { cy_top: 302, cy_bottom: 486 },
  outer_safe_band_px: 96,
  left_panel: { cx: -499, width: 730 },
  center_boundary: { cx: 0, width: 268 },
  right_panel: { cx: 499, width: 730 },
};

// Item set follows G27_PublicVsBrokerDB carrier checklist required item_names.
// Visual role assignment follows SCS §3 vocabulary.
// All ShapeItems use SizeMode=WidthHeight (SCS §5.1).
// All colors are #AARRGGBB strings (SCS §5.1, fixed in G-27 minimal probe).
//
// SCS strict reading violations are intentionally recorded as
// composition_violations rather than silently normalized:
//   - supporting count = 5 (SCS §3 strict limit: <=3 per frame; split needs per-focal limit)
//   - label count = 3   (SCS §4.3 strict limit: <=2 per frame; split needs global + per-panel)
// These ambiguities are recorded as SCS v0.1 spec gaps for v0.2 refinement.
const sceneItems = [
  // decoration: full-screen light-stage background
  shape('G27PBD_BG', 'decoration', 5, 0, 0, 1920, 1080, '#FFF0F4F8', 100, 0, 1080, true, false, 'full-screen light-stage background'),

  // label: global title (title band) — upper concept distinct from panel titles
  text('G27PBD_Title', 'label', 9, 0, grid.title_band.cy, 64, '情報の非対称性', '#FF1A2B3C', false, null, 'global title; upper concept above panel titles (no lexical overlap with 公開ポータル / 業者DB)'),

  // focal_anchor: left public panel (filled blue rect)
  shape('G27PBD_PublicPanel', 'focal_anchor', 8, grid.left_panel.cx, -49, grid.left_panel.width, 620, '#FF2563EB', 100, 16, 620, true, false, 'left focal anchor: public portal panel'),

  // label: public panel title (inside panel)
  text('G27PBD_PublicTitle', 'label', 10, grid.left_panel.cx, -310, 48, '公開ポータル', '#FFFFFFFF', true, 'G27PBD_PublicPanel', 'public panel title'),

  // supporting: public side cards (2 fixed, visible)
  shape('G27PBD_PublicCard1', 'supporting', 11, grid.left_panel.cx, -150, 600, 130, '#FFE0EBFE', 100, 12, 130, true, false, 'public card 1: visible listing'),
  shape('G27PBD_PublicCard2', 'supporting', 11, grid.left_panel.cx, 30, 600, 130, '#FFE0EBFE', 100, 12, 130, true, false, 'public card 2: visible listing'),

  // boundary: center gate = 2 thin vertical pillars (left + right) forming
  // a closed double-pillar barrier. Each pillar 30x400 (aspect 1:13), round=4,
  // placed symmetrically at cx=-20 and cx=+20 with a 10px gap. The pair
  // reads as a gate / double-pillar wall, never as a human silhouette
  // (no oval head, no torso-like single mass). No TextItem added.
  // Naming follows carrier checklist derivation rule (G27PBD_Lock_<part>).
  shape('G27PBD_Lock', 'boundary', 12, -20, -49, 30, 400, '#FFE5A800', 100, 4, 400, true, false, 'center gate left pillar'),
  shape('G27PBD_Lock_Right', 'boundary', 12, 20, -49, 30, 400, '#FFE5A800', 100, 4, 400, true, false, 'center gate right pillar'),

  // focal_anchor: right broker / private DB panel
  shape('G27PBD_BrokerPanel', 'focal_anchor', 8, grid.right_panel.cx, -49, grid.right_panel.width, 620, '#FF7C3AED', 100, 16, 620, true, false, 'right focal anchor: broker / private DB panel'),

  // label: broker panel title (inside panel)
  text('G27PBD_BrokerTitle', 'label', 10, grid.right_panel.cx, -310, 48, '業者DB', '#FFFFFFFF', true, 'G27PBD_BrokerPanel', 'broker panel title'),

  // supporting: broker side cards (3 fixed)
  shape('G27PBD_BrokerCard1', 'supporting', 11, grid.right_panel.cx, -190, 600, 110, '#FFEDE9FE', 100, 12, 110, true, false, 'broker card 1: hidden listing'),
  shape('G27PBD_BrokerCard2', 'supporting', 11, grid.right_panel.cx, -49, 600, 110, '#FFEDE9FE', 100, 12, 110, true, false, 'broker card 2: hidden listing'),
  shape('G27PBD_BrokerCard3', 'supporting', 11, grid.right_panel.cx, 92, 600, 110, '#FFEDE9FE', 100, 12, 110, true, false, 'broker card 3: hidden listing'),

  // connector (hidden in initial state): arrow placeholder
  shape('G27PBD_Arrow', 'connector', 13, 0, 200, 120, 60, '#FFE5A800', 100, 8, 60, true, true, 'optional arrow placeholder (kept hidden)'),
];

function shape(displayName, role, layer, x, y, width, height, color, opacity, round, strokeThickness, visibleBorderExpected, isHidden, description) {
  return {
    kind: 'ShapeItem',
    display_name: displayName,
    role,
    layer,
    x,
    y,
    width,
    height,
    color,
    opacity,
    round,
    stroke_thickness: strokeThickness,
    visible_border_expected: visibleBorderExpected,
    is_hidden: Boolean(isHidden),
    intended_inside_panel: false,
    description,
  };
}

function text(displayName, role, layer, x, y, fontSize, content, color, intendedInsidePanel, panelName, description) {
  return {
    kind: 'TextItem',
    display_name: displayName,
    role,
    layer,
    x,
    y,
    font_size: fontSize,
    content,
    color,
    opacity: 100,
    is_hidden: false,
    intended_inside_panel: intendedInsidePanel,
    expected_panel: panelName,
    description,
  };
}

function abs(relPath) {
  return path.join(root, relPath);
}

function readText(relPath) {
  return fs.readFileSync(abs(relPath), 'utf8').replace(/^﻿/, '');
}

function readJson(relPath) {
  return JSON.parse(readText(relPath));
}

function writeJson(relPath, payload) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function writeMarkdown(relPath, markdown) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), markdown, 'utf8');
}

function writeYmmp(relPath, payload) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), `﻿${JSON.stringify(payload, null, 2)}`, 'utf8');
}

function sha256(relPath) {
  return crypto.createHash('sha256').update(fs.readFileSync(abs(relPath))).digest('hex');
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
  if (!brush || typeof brush !== 'object' || !brush.Parameter || typeof brush.Parameter !== 'object') {
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
  item.Frame = sceneFrame.frame;
  item.Length = sceneFrame.duration_frames;
  item.Layer = primitive.layer;
  item.Group = 0;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Remark = primitive.display_name;
  item.IsLocked = false;
  item.IsHidden = Boolean(primitive.is_hidden);
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
    Frame: sceneFrame.frame,
    Layer: primitive.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: sceneFrame.duration_frames,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: primitive.display_name,
    IsLocked: false,
    IsHidden: Boolean(primitive.is_hidden),
  };
}

function validateSceneDesign() {
  const errors = [];
  if (sceneItems.length < 8 || sceneItems.length > 14) {
    errors.push(`SCS §3 element count out of range [8,14]: ${sceneItems.length}`);
  }
  if (sceneFrame.tonal_system !== 'light-stage') errors.push('tonal system must be light-stage (single stage policy)');
  for (const item of sceneItems) {
    if (!['ShapeItem', 'TextItem'].includes(item.kind)) errors.push(`${item.display_name} unsupported item kind ${item.kind}`);
    if (item.display_name.length > maxDisplayNameLength) errors.push(`${item.display_name} display name too long`);
    if (!String(item.display_name).startsWith('G27PBD_')) errors.push(`${item.display_name} item name must start with G27PBD_`);
    if (item.kind === 'ShapeItem') {
      if (item.width <= 0 || item.height <= 0) errors.push(`${item.display_name} invalid geometry`);
      if (!hexColorPattern.test(item.color)) errors.push(`${item.display_name} color is not #AARRGGBB`);
    }
    if (item.kind === 'TextItem') {
      if (item.font_size < 30) errors.push(`${item.display_name} font size too small`);
      if (!hexColorPattern.test(item.color)) errors.push(`${item.display_name} text color is not #AARRGGBB`);
    }
  }
  const focalCount = sceneItems.filter((i) => i.role === 'focal_anchor').length;
  if (focalCount !== 2) errors.push(`SCS §2.1 split requires exactly 2 focal_anchor, got ${focalCount}`);
  const boundaryCount = sceneItems.filter((i) => i.role === 'boundary').length;
  if (boundaryCount < 1) errors.push(`SCS §2.1 split requires at least 1 boundary, got ${boundaryCount}`);
  // boundary >= 2 is allowed when a single boundary concept (e.g. key = body + shackle)
  // is composed from multiple ShapeItems following the carrier checklist derivation rule.
  if (errors.length) throw new Error(`DIAGNOSTIC_CARRIER_DESIGN_INVALID: ${errors.join('; ')}`);
}

function buildProbeProject(carrierYmmp, shapeTemplateYmmp) {
  validateSceneDesign();
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) {
    throw new Error(`SHAPE_TEMPLATE_MISSING: ${paths.shapeTemplateYmmp}`);
  }
  const project = clone(carrierYmmp);
  const timeline = project.Timelines?.[0];
  if (!timeline || !Array.isArray(project.Timelines)) {
    throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  }
  const items = sceneItems.map((primitive) => {
    if (primitive.kind === 'ShapeItem') return makeShapeItem(shapeTemplate, primitive);
    if (primitive.kind === 'TextItem') return makeTextItem(primitive);
    throw new Error(`UNSUPPORTED_PRIMITIVE_KIND: ${primitive.kind}`);
  });
  timeline.Items = items;
  timeline.CurrentFrame = 0;
  timeline.Length = sceneFrame.duration_frames;
  timeline.MaxLayer = Math.max(...items.map((item) => item.Layer), 0);
  if (!timeline.LayerSettings || Array.isArray(timeline.LayerSettings)) {
    timeline.LayerSettings = { Items: Array.isArray(timeline.LayerSettings) ? timeline.LayerSettings : [] };
  }
  project.FilePath = abs(paths.outputYmmp);
  return project;
}

function animationValue(item, key) {
  return item?.[key]?.Values?.[0]?.Value;
}

function shapeParameterValue(item, key) {
  return item?.ShapeParameter?.[key]?.Values?.[0]?.Value;
}

// SCS §1 grid in YMM4 center-origin (cx, cy) ranges
const safeBands = {
  outer_left:   { cx_min: -960, cx_max: -864 },
  outer_right:  { cx_min: 864,  cx_max: 960  },
  outer_top:    { cy_min: -540, cy_max: -486 },
  outer_bottom: { cy_min: 486,  cy_max: 540  },
  caption:      { cy_min: 302,  cy_max: 486  },
};

function rectIntersects(item, region) {
  const left = item.x - item.width / 2;
  const right = item.x + item.width / 2;
  const top = item.y - item.height / 2;
  const bottom = item.y + item.height / 2;
  if (region.cx_min !== undefined) {
    if (right < region.cx_min || left > region.cx_max) return false;
    if (region.cy_min !== undefined) {
      if (bottom < region.cy_min || top > region.cy_max) return false;
    }
    return true;
  }
  return bottom >= region.cy_min && top <= region.cy_max;
}

function safeAreaCheckForItem(primitive) {
  if (primitive.role === 'decoration') {
    return { check: 'pass', note: 'background covers full canvas by design' };
  }
  const widthGuess = primitive.kind === 'ShapeItem' ? primitive.width : primitive.content.length * primitive.font_size * 0.62;
  const heightGuess = primitive.kind === 'ShapeItem' ? primitive.height : primitive.font_size * 1.3;
  const box = { x: primitive.x, y: primitive.y, width: widthGuess, height: heightGuess };
  const left = box.x - box.width / 2;
  const right = box.x + box.width / 2;
  const top = box.y - box.height / 2;
  const bottom = box.y + box.height / 2;
  const issues = [];
  if (left < -864) issues.push('intrudes into left outer safe band');
  if (right > 864) issues.push('intrudes into right outer safe band');
  if (top < -486) issues.push('intrudes into top outer safe band');
  if (bottom > 486) issues.push('intrudes into bottom outer safe band');
  return { check: issues.length === 0 ? 'pass' : 'warn', issues };
}

function subtitleClearanceForItem(primitive) {
  if (primitive.role === 'decoration') {
    return { check: 'pass', note: 'background is allowed across caption safe area' };
  }
  const widthGuess = primitive.kind === 'ShapeItem' ? primitive.width : primitive.content.length * primitive.font_size * 0.62;
  const heightGuess = primitive.kind === 'ShapeItem' ? primitive.height : primitive.font_size * 1.3;
  const box = { x: primitive.x, y: primitive.y, width: widthGuess, height: heightGuess };
  const bottom = box.y + box.height / 2;
  const top = box.y - box.height / 2;
  if (bottom < safeBands.caption.cy_min) return { check: 'pass' };
  if (top > safeBands.caption.cy_max) return { check: 'pass' };
  return { check: 'fail', note: 'crosses caption safe area (cy 302..486)' };
}

function deriveReadbackItem(item, primitive) {
  const displayName = String(item.Remark || '');
  const type = itemType(item);
  const isShape = type === 'ShapeItem';
  const isText = type === 'TextItem';
  return {
    index: 0,
    display_name: displayName,
    item_name: displayName,
    item_name_source: 'YMM4 Remark field; short G27PBD_ name, no long provenance on authoring surface',
    item_type: type,
    role: primitive?.role || null,
    layer: item.Layer,
    frame: item.Frame,
    duration_frames: item.Length,
    is_hidden: Boolean(item.IsHidden),
    x: animationValue(item, 'X') ?? null,
    y: animationValue(item, 'Y') ?? null,
    width: isShape ? shapeParameterValue(item, 'Width') ?? null : null,
    height: isShape ? shapeParameterValue(item, 'Height') ?? null : null,
    shape_size_mode: isShape ? item.ShapeParameter?.SizeMode || null : null,
    shape_size: isShape ? shapeParameterValue(item, 'Size') ?? null : null,
    shape_aspect_rate: isShape ? shapeParameterValue(item, 'AspectRate') ?? null : null,
    stroke_thickness: isShape ? shapeParameterValue(item, 'StrokeThickness') ?? null : null,
    opacity: animationValue(item, 'Opacity') ?? null,
    fill_color: isShape ? item.ShapeParameter?.Brush?.Parameter?.Color || null : null,
    text_color: isText ? item.FontColor : null,
    text: isText ? item.Text : null,
    font_size: isText ? item.FontSize?.Values?.[0]?.Value ?? null : null,
    display_name_length: displayName.length,
    item_name_length_check: displayName.length <= maxDisplayNameLength ? 'pass' : 'fail',
    remark: item.Remark || '',
    remark_length: String(item.Remark || '').length,
    remark_length_check: String(item.Remark || '').length <= maxRemarkLength ? 'pass' : 'fail',
    detailed_provenance: {
      generator: paths.outputYmmp,
      design_description: primitive?.description || null,
      composition_type: 'split',
      composition_role: primitive?.role || null,
      source: 'G-27 diagnostic carrier for SCS §2.1 split adoption (not creative acceptance)',
      not_video_scene: true,
      render_performed: false,
    },
  };
}

function buildScsComplianceFields(items) {
  const groupedByRole = {
    focal_anchor: [],
    supporting: [],
    boundary: [],
    connector: [],
    risk_marker: [],
    decoration: [],
    label: [],
  };
  for (const it of items) {
    const role = it.role || 'decoration';
    if (groupedByRole[role]) groupedByRole[role].push(it.item_name);
    else groupedByRole[role] = [it.item_name];
  }
  // SCS §4 reading order for split: left focal -> boundary -> right focal
  const readingOrder = ['G27PBD_PublicPanel', 'G27PBD_Lock', 'G27PBD_BrokerPanel'];

  const violations = [];

  // SCS §3 element count check (8-14 inclusive, all items including hidden Arrow)
  const elementCount = items.length;
  if (elementCount < 8 || elementCount > 14) {
    violations.push({
      rule: 'SCS_3_element_count_range',
      actual: elementCount,
      allowed_range: [8, 14],
      severity: 'fail',
    });
  }

  // SCS §3 supporting per-frame strict limit (<=3). split needs per-focal interpretation.
  if (groupedByRole.supporting.length > 3) {
    violations.push({
      rule: 'SCS_3_supporting_per_frame_strict',
      actual: groupedByRole.supporting.length,
      max_strict: 3,
      severity: 'spec_ambiguity',
      note: 'split composition with 2 focal anchors needs per-focal supporting count limit. SCS v0.1 ambiguity recorded for v0.2 refinement.',
      per_focal_distribution: {
        public: groupedByRole.supporting.filter((n) => n.startsWith('G27PBD_Public')).length,
        broker: groupedByRole.supporting.filter((n) => n.startsWith('G27PBD_Broker')).length,
      },
    });
  }

  // SCS §4.3 label budget (<=2 per frame). split needs global + per-panel.
  if (groupedByRole.label.length > 2) {
    violations.push({
      rule: 'SCS_4_3_label_budget_strict',
      actual_labels: groupedByRole.label.length,
      max_strict: 2,
      severity: 'spec_ambiguity',
      note: 'split composition needs global title + per-panel title (3 labels). SCS v0.1 ambiguity recorded for v0.2 refinement.',
    });
  }

  // SCS §5.1 ShapeItem SizeMode = WidthHeight
  const shapeItems = items.filter((it) => it.item_type === 'ShapeItem');
  const wrongSizeMode = shapeItems.filter((it) => it.shape_size_mode !== shapeSizeMode);
  const shapeSizeModeCheck = wrongSizeMode.length === 0 ? 'pass' : 'fail';
  if (wrongSizeMode.length > 0) {
    violations.push({
      rule: 'SCS_5_1_shape_size_mode',
      offenders: wrongSizeMode.map((it) => it.display_name),
      expected: shapeSizeMode,
      severity: 'fail',
    });
  }

  // SCS §5.1 color string format
  const shapeColorViolations = shapeItems.filter((it) => !(typeof it.fill_color === 'string' && hexColorPattern.test(it.fill_color)));
  const textColorViolations = items.filter((it) => it.item_type === 'TextItem' && !(typeof it.text_color === 'string' && hexColorPattern.test(it.text_color)));
  const colorFormatCheck = (shapeColorViolations.length + textColorViolations.length) === 0 ? 'pass' : 'fail';
  if (shapeColorViolations.length + textColorViolations.length > 0) {
    violations.push({
      rule: 'SCS_5_1_color_format',
      shape_offenders: shapeColorViolations.map((it) => it.display_name),
      text_offenders: textColorViolations.map((it) => it.display_name),
      expected: '#AARRGGBB string',
      severity: 'fail',
    });
  }

  // SCS §1 safe area + caption clearance: aggregate from per-item checks
  let safeAreaPass = true;
  let subtitleClearancePass = true;
  for (const primitive of sceneItems) {
    const sa = safeAreaCheckForItem(primitive);
    const sc = subtitleClearanceForItem(primitive);
    if (sa.check === 'warn' || sa.check === 'fail') safeAreaPass = false;
    if (sc.check === 'fail') subtitleClearancePass = false;
  }

  if (!safeAreaPass) {
    violations.push({ rule: 'SCS_1_outer_safe_band', severity: 'warn', note: 'one or more items intrude into outer 5% safe band' });
  }
  if (!subtitleClearancePass) {
    violations.push({ rule: 'SCS_1_caption_safe_area', severity: 'fail', note: 'one or more items cross caption safe area cy 302..486' });
  }

  // SCS §6 Beat -> composition type mapping
  const beatMapping = {
    narration_logical_form: 'A is not B (公開ポータル vs 業者DB の情報非対称性)',
    selected_composition_type: 'split',
    rationale: '対比 / 二項の主張 -> SCS §2.1 split composition type',
  };

  // Typography hierarchy check
  const titleFont = items.find((it) => it.display_name === 'G27PBD_Title')?.font_size ?? 0;
  const panelTitleFonts = items.filter((it) => it.display_name === 'G27PBD_PublicTitle' || it.display_name === 'G27PBD_BrokerTitle').map((it) => it.font_size ?? 0);
  const typographyHierarchyCheck = (titleFont >= 48 && titleFont <= 96 && panelTitleFonts.every((s) => s >= 32 && s <= 64)) ? 'pass' : 'warn';

  // In-frame text budget
  const inFrameLabels = groupedByRole.label;
  const inFrameTextChars = items.filter((it) => inFrameLabels.includes(it.item_name) && it.text).reduce((acc, it) => acc + String(it.text).length, 0);
  const inFrameTextBudgetCheck = inFrameTextChars <= 30 ? 'pass' : 'warn';

  return {
    composition_type: 'split',
    composition_type_check: 'pass',
    beat_to_composition_mapping: beatMapping,
    visual_roles: groupedByRole,
    element_count: elementCount,
    element_count_check: (elementCount >= 8 && elementCount <= 14) ? 'pass' : 'fail',
    reading_order: readingOrder,
    typography_hierarchy_check: typographyHierarchyCheck,
    in_frame_text_budget: { labels: inFrameLabels.length, chars: inFrameTextChars },
    in_frame_text_budget_check: inFrameTextBudgetCheck,
    safe_area_check: safeAreaPass ? 'pass' : 'warn',
    subtitle_clearance_check: subtitleClearancePass ? 'pass' : 'fail',
    shape_size_mode_check: shapeSizeModeCheck,
    color_format_check: colorFormatCheck,
    composition_violations: violations,
  };
}

function readbackProbe(ymmp, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const items = timelineItems.map((item, index) => {
    const displayName = String(item.Remark || '');
    const primitive = sceneItems.find((entry) => entry.display_name === displayName);
    const built = deriveReadbackItem(item, primitive);
    built.index = index;
    return built;
  });

  const missingItems = sceneItems
    .filter((expected) => !items.find((item) => item.display_name === expected.display_name))
    .map((expected) => ({ display_name: expected.display_name, reason: 'expected scene item not found in output' }));

  const malformedItems = [];
  for (const expected of sceneItems) {
    const found = items.find((item) => item.display_name === expected.display_name);
    if (!found) continue;
    const mismatches = [];
    if (found.item_type !== expected.kind) mismatches.push({ field: 'item_type', expected: expected.kind, actual: found.item_type });
    if (found.layer !== expected.layer) mismatches.push({ field: 'layer', expected: expected.layer, actual: found.layer });
    if (found.frame !== sceneFrame.frame) mismatches.push({ field: 'frame', expected: sceneFrame.frame, actual: found.frame });
    if (found.duration_frames !== sceneFrame.duration_frames) {
      mismatches.push({ field: 'duration_frames', expected: sceneFrame.duration_frames, actual: found.duration_frames });
    }
    if (found.x !== expected.x || found.y !== expected.y) {
      mismatches.push({ field: 'position', expected: { x: expected.x, y: expected.y }, actual: { x: found.x, y: found.y } });
    }
    if (Boolean(found.is_hidden) !== Boolean(expected.is_hidden)) {
      mismatches.push({ field: 'is_hidden', expected: Boolean(expected.is_hidden), actual: Boolean(found.is_hidden) });
    }
    if (expected.kind === 'ShapeItem') {
      if (found.shape_size_mode !== shapeSizeMode) mismatches.push({ field: 'shape_size_mode', expected: shapeSizeMode, actual: found.shape_size_mode });
      if (found.width !== expected.width || found.height !== expected.height) {
        mismatches.push({ field: 'width_height', expected: { width: expected.width, height: expected.height }, actual: { width: found.width, height: found.height } });
      }
      if (found.fill_color !== expected.color) mismatches.push({ field: 'fill_color', expected: expected.color, actual: found.fill_color });
    }
    if (expected.kind === 'TextItem') {
      if (found.text !== expected.content) mismatches.push({ field: 'text', expected: expected.content, actual: found.text });
      if (found.text_color !== expected.color) mismatches.push({ field: 'text_color', expected: expected.color, actual: found.text_color });
    }
    if (mismatches.length) malformedItems.push({ display_name: expected.display_name, mismatches });
  }

  const scs = buildScsComplianceFields(items);

  const hardFailures = scs.composition_violations.filter((v) => v.severity === 'fail');
  const status = missingItems.length === 0 && malformedItems.length === 0 && hardFailures.length === 0 ? 'passed' : 'failed';

  return {
    artifact_type: 'g27_diagnostic_carrier_readback',
    status,
    source: {
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_diagnostic_carrier_ymmp: paths.outputYmmp,
    },
    boundary: {
      diagnostic_only: true,
      not_video_scene: true,
      existing_micro_scene_probe_modified: false,
      existing_primitive_visibility_probe_modified: false,
      shape_item_text_item_only: true,
      tonal_system: sceneFrame.tonal_system,
      black_white_background_mix: false,
      external_assets_used: false,
      tts_performed: false,
      url_fetch_performed: false,
      publishing_performed: false,
      render_performed: false,
      timing_adjusted: false,
      creative_acceptance_performed: false,
      production_readiness_claimed: false,
      production_carrier_replaced: false,
      next_user_action: 'user-authored carrier .ymmp is still required for production slot-fill',
    },
    scene: {
      frame: sceneFrame.frame,
      duration_frames: sceneFrame.duration_frames,
      duration_sec: sceneFrame.duration_frames / fps,
      canvas: sceneFrame.canvas,
      background_color: sceneFrame.background_color,
      composition_type: 'split',
      composition_grid: grid,
      scs_spec: 'docs/SCENE_COMPOSITION_SCHEMA.md (v0.1)',
      carrier_checklist_ref: 'docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md',
    },
    scs_compliance: scs,
    source_integrity: {
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    totals: {
      item_count: items.length,
      expected_item_count: sceneItems.length,
      shape_item_count: items.filter((item) => item.item_type === 'ShapeItem').length,
      text_item_count: items.filter((item) => item.item_type === 'TextItem').length,
      hidden_item_count: items.filter((item) => item.is_hidden).length,
      missing_item_count: missingItems.length,
      malformed_item_count: malformedItems.length,
      item_name_length_failures: items.filter((item) => item.item_name_length_check !== 'pass').length,
      remark_length_failures: items.filter((item) => item.remark_length_check !== 'pass').length,
      composition_violation_count: scs.composition_violations.length,
      composition_hard_failure_count: hardFailures.length,
    },
    items,
    missing_items: missingItems,
    malformed_items: malformedItems,
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Diagnostic Carrier (SCS §2.1 split)');
  lines.push('');
  lines.push(`Diagnostic carrier: \`${readback.source.generated_diagnostic_carrier_ymmp}\``);
  lines.push('');
  lines.push('Diagnostic only. Not a production carrier. Render / creative acceptance / timing adjustment were not performed.');
  lines.push('');
  lines.push('## 1. Composition');
  lines.push('');
  lines.push(`- composition_type: \`${readback.scs_compliance.composition_type}\``);
  lines.push(`- beat -> composition mapping: \`${readback.scs_compliance.beat_to_composition_mapping.selected_composition_type}\` from \`${readback.scs_compliance.beat_to_composition_mapping.narration_logical_form}\``);
  lines.push(`- scs spec ref: \`${readback.scene.scs_spec}\``);
  lines.push(`- carrier checklist ref: \`${readback.scene.carrier_checklist_ref}\``);
  lines.push('');
  lines.push('## 2. Visual Roles (SCS §3)');
  lines.push('');
  for (const [role, names] of Object.entries(readback.scs_compliance.visual_roles)) {
    lines.push(`- \`${role}\`: ${names.length} item(s) — ${names.map((n) => `\`${n}\``).join(', ') || '(none)'}`);
  }
  lines.push('');
  lines.push('## 3. SCS Compliance Rollup');
  lines.push('');
  lines.push(`- element_count: \`${readback.scs_compliance.element_count}\` (\`${readback.scs_compliance.element_count_check}\`)`);
  lines.push(`- reading_order: ${readback.scs_compliance.reading_order.map((n) => `\`${n}\``).join(' -> ')}`);
  lines.push(`- shape_size_mode_check: \`${readback.scs_compliance.shape_size_mode_check}\``);
  lines.push(`- color_format_check: \`${readback.scs_compliance.color_format_check}\``);
  lines.push(`- safe_area_check: \`${readback.scs_compliance.safe_area_check}\``);
  lines.push(`- subtitle_clearance_check: \`${readback.scs_compliance.subtitle_clearance_check}\``);
  lines.push(`- typography_hierarchy_check: \`${readback.scs_compliance.typography_hierarchy_check}\``);
  lines.push(`- in_frame_text_budget_check: \`${readback.scs_compliance.in_frame_text_budget_check}\` (labels=${readback.scs_compliance.in_frame_text_budget.labels}, chars=${readback.scs_compliance.in_frame_text_budget.chars})`);
  lines.push('');
  lines.push('## 4. Composition Violations');
  lines.push('');
  if (readback.scs_compliance.composition_violations.length === 0) {
    lines.push('- (none)');
  } else {
    for (const v of readback.scs_compliance.composition_violations) {
      lines.push(`- \`${v.rule}\` (\`${v.severity}\`): ${v.note || JSON.stringify(v).slice(0, 200)}`);
    }
  }
  lines.push('');
  lines.push('## 5. Item Table');
  lines.push('');
  lines.push('| item_name | role | type | layer | hidden | x,y | width x height (or font) | color |');
  lines.push('| --- | --- | --- | --- | --- | --- | --- | --- |');
  for (const item of readback.items) {
    const geom = item.item_type === 'ShapeItem' ? `${item.width}x${item.height}` : `font=${item.font_size}`;
    const color = item.item_type === 'ShapeItem' ? item.fill_color : item.text_color;
    lines.push(`| \`${item.item_name}\` | \`${item.role}\` | \`${item.item_type}\` | \`${item.layer}\` | \`${item.is_hidden}\` | \`${item.x}, ${item.y}\` | \`${geom}\` | \`${color}\` |`);
  }
  lines.push('');
  lines.push('## 6. Status');
  lines.push('');
  lines.push(`- readback status: \`${readback.status}\``);
  lines.push(`- carrier modified in place: \`${readback.source_integrity.carrier_modified_in_place}\``);
  lines.push(`- composition hard failures: \`${readback.totals.composition_hard_failure_count}\``);
  lines.push(`- composition violation count (all severities): \`${readback.totals.composition_violation_count}\``);
  lines.push('');
  lines.push('## 7. Boundary');
  lines.push('');
  for (const [key, val] of Object.entries(readback.boundary)) {
    lines.push(`- \`${key}\`: \`${JSON.stringify(val)}\``);
  }
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (!readback.boundary.diagnostic_only || !readback.boundary.not_video_scene) failures.push('boundary is not diagnostic-only');
  if (!readback.boundary.shape_item_text_item_only) failures.push('item boundary is not ShapeItem/TextItem only');
  if (readback.boundary.render_performed) failures.push('render performed');
  if (readback.boundary.timing_adjusted) failures.push('timing adjusted');
  if (readback.boundary.creative_acceptance_performed) failures.push('creative acceptance performed');
  if (readback.totals.item_count !== readback.totals.expected_item_count) failures.push('item count mismatch');
  if (readback.totals.missing_item_count !== 0) failures.push('missing items present');
  if (readback.totals.malformed_item_count !== 0) failures.push(`malformed items present: ${JSON.stringify(readback.malformed_items.slice(0, 3))}`);
  if (readback.totals.composition_hard_failure_count !== 0) failures.push(`SCS hard failures present: ${JSON.stringify(readback.scs_compliance.composition_violations.filter((v) => v.severity === 'fail'))}`);
  if (readback.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  if (readback.scs_compliance.composition_type !== 'split') failures.push('composition_type is not split');
  if (readback.scs_compliance.shape_size_mode_check !== 'pass') failures.push('shape_size_mode_check failed');
  if (readback.scs_compliance.color_format_check !== 'pass') failures.push('color_format_check failed');
  if (readback.scs_compliance.element_count_check !== 'pass') failures.push('element_count out of SCS §3 range');
  if (failures.length) throw new Error(`G27_DIAGNOSTIC_CARRIER_FAILED: ${failures.join('; ')}`);
}

function main() {
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplateYmmp = readJson(paths.shapeTemplateYmmp);
  const generatedProject = buildProbeProject(carrierYmmp, shapeTemplateYmmp);
  const generatedReadback = readbackProbe(generatedProject, carrierHashBefore, sha256(paths.carrierYmmp));
  const generatedReport = renderMarkdown(generatedReadback);
  assertReadback(generatedReadback);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generatedProject);
    const writtenProject = readJson(paths.outputYmmp);
    const writtenReadback = readbackProbe(writtenProject, carrierHashBefore, sha256(paths.carrierYmmp));
    const writtenReport = renderMarkdown(writtenReadback);
    assertReadback(writtenReadback);
    writeJson(paths.readbackJson, writtenReadback);
    writeMarkdown(paths.reportMd, writtenReport);
    console.log(`G-27 diagnostic carrier written: ${paths.outputYmmp}`);
    console.log(`Readback: ${paths.readbackJson}`);
    console.log(`Report: ${paths.reportMd}`);
    console.log(`SCS compliance: status=${writtenReadback.status}, violations=${writtenReadback.totals.composition_violation_count} (hard_fail=${writtenReadback.totals.composition_hard_failure_count})`);
  } else {
    if (!fs.existsSync(abs(paths.outputYmmp))) {
      throw new Error(`OUTPUT_YMMP_MISSING: run with --write first (${paths.outputYmmp})`);
    }
    const existingProject = readJson(paths.outputYmmp);
    const existingReadback = readJson(paths.readbackJson);
    const actualReadback = readbackProbe(existingProject, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(actualReadback);
    assertReadback(existingReadback);
    if (JSON.stringify(actualReadback) !== JSON.stringify(existingReadback)) {
      throw new Error('READBACK_DRIFT: existing diagnostic carrier readback JSON does not match probe .ymmp');
    }
    console.log(`G-27 diagnostic carrier OK (no-write check): item_count=${actualReadback.totals.item_count}, hard_fail=${actualReadback.totals.composition_hard_failure_count}`);
  }
}

main();

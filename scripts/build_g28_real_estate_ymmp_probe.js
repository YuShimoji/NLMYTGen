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
const layoutContractRevision = {
  revision_id: 'g28_real_estate_information_gap_layout_contract_v1',
  source_audit: 'docs/verification/G28-REAL-ESTATE-YMMP-PROBE-LAYOUT-CONTRACT-AUDIT-2026-06-07.md',
  classification: 'pass_layout_contract_implemented',
  next_decision: 'ready_for_human_gui_recheck_before_review_console_ingest',
};
const rightNodeAlignmentRevision = {
  revision_id: 'g28_real_estate_information_gap_right_node_alignment_v1',
  source_human_decision: 'revise_probe_again_narrow_right_node_text_alignment',
  classification: 'pass_right_node_alignment_fixed',
  target_label: 'G28_LDC_Node_Right_Label',
  observed_issue: 'Human GUI recheck saw only the right node label as visually off-center inside its rectangle.',
  cause_classification: 'right_node_registered_optical_offset_needed',
  formula_change: 'No common text-centering formula change; the right node label gets a bounded x-axis optical offset.',
  boundary_note: 'Diagnostic-only right-node alignment fix; no render, production approval, slot-fill, image, URL, audio, TTS, or source footage.',
};
const calloutLabelAlignmentRevision = {
  revision_id: 'g28_real_estate_information_gap_callout_label_alignment_v1',
  source_human_decision: 'revise_probe_again_narrow_callout_label_alignment',
  classification: 'pass_callout_label_alignment_fixed',
  target_label: 'G28_LDC_CalloutSlot_3_Label',
  observed_issue: 'Human GUI correction identified the lower-right callout label as the actual off-center target, not the right node label.',
  target_correction: 'Previous right-node alignment fix is retained; the corrected target is the third callout label.',
  cause_classification: 'callout_label_registered_optical_offset_needed',
  formula_change: 'No common callout formula change; the third callout label gets a bounded x-axis optical offset.',
  boundary_note: 'Diagnostic-only callout label alignment fix; no render, production approval, slot-fill, image, URL, audio, TTS, or source footage.',
};
const layoutThresholds = {
  text_center_error_px: 1,
  registered_optical_offset_px: 6,
  connector_alignment_error_px: 2,
  caption_reserve_overlap_px: 0,
  callout_density_width_ratio: 0.85,
  callout_density_height_ratio: 0.45,
  host_area_ratio: 0.03,
};
const connectorLayoutRule = {
  thickness: 12,
  left: {
    from: 'G28_LDC_Node_Left',
    to: 'G28_LDC_Focal_Core',
    from_edge: 'right',
    to_edge: 'left',
    y_reference: 'from_center',
  },
  right: {
    from: 'G28_LDC_Focal_Core',
    to: 'G28_LDC_Node_Right',
    from_edge: 'right',
    to_edge: 'left',
    y_reference: 'to_center',
  },
};
const calloutSlotLayoutRule = {
  supported_counts: [2, 3],
  active_count: 3,
  start_x: 375,
  row_y: 642,
  width: 330,
  height: 90,
  gap: 90,
  text_offset: { x: 0, y: -3 },
  four_callout_risk: 'Four callouts at this slot width and gap would consume too much host-side breathing room; split or reduce text instead.',
};
const manualOffsetRegistry = {
  G28_LDC_Title_Text: {
    target: 'title text',
    value: { x: 0, y: -2 },
    reason: 'Optical centering correction for YMM4 TextItem top-left placement inside the source title rect.',
    allowed_range: { x_abs_max: 4, y_abs_max: 4 },
    reuse_risk: 'medium',
  },
  G28_LDC_Node_Left_Label: {
    target: 'focal node label',
    value: { x: 0, y: -4 },
    reason: 'Optical centering correction for Japanese node labels.',
    allowed_range: { x_abs_max: 4, y_abs_max: 6 },
    reuse_risk: 'medium',
  },
  G28_LDC_Node_Center_Label: {
    target: 'focal node label',
    value: { x: 0, y: -4 },
    reason: 'Optical centering correction for Japanese node labels.',
    allowed_range: { x_abs_max: 4, y_abs_max: 6 },
    reuse_risk: 'medium',
  },
  G28_LDC_Node_Right_Label: {
    target: 'focal node label',
    value: { x: 4, y: -4 },
    reason: 'Right-node-only optical centering correction after human GUI recheck; readback placement metrics did not capture the rendered glyph-center perception.',
    allowed_range: { x_abs_max: 4, y_abs_max: 6 },
    reuse_risk: 'medium_right_node_specific',
  },
  G28_LDC_CalloutSlot_1_Label: {
    target: 'callout label',
    value: calloutSlotLayoutRule.text_offset,
    reason: 'Optical centering correction inside compact callout slot.',
    allowed_range: { x_abs_max: 4, y_abs_max: 5 },
    reuse_risk: 'medium',
  },
  G28_LDC_CalloutSlot_2_Label: {
    target: 'callout label',
    value: calloutSlotLayoutRule.text_offset,
    reason: 'Optical centering correction inside compact callout slot.',
    allowed_range: { x_abs_max: 4, y_abs_max: 5 },
    reuse_risk: 'medium',
  },
  G28_LDC_CalloutSlot_3_Label: {
    target: 'callout label',
    value: { x: 4, y: -3 },
    reason: 'Lower-right callout-only optical centering correction after human GUI target correction; readback placement metrics did not capture the rendered glyph-center perception.',
    allowed_range: { x_abs_max: 4, y_abs_max: 5 },
    reuse_risk: 'medium_callout_specific',
  },
  G28_LDC_Connector_Left: {
    target: 'left connector',
    value: connectorLayoutRule.left,
    reason: 'Derived edge-to-edge bar from left node right edge to focal core left edge.',
    allowed_range: { endpoint_gap_abs_max: 2, y_error_abs_max: 2 },
    reuse_risk: 'low_after_derivation',
  },
  G28_LDC_Connector_Right: {
    target: 'right connector',
    value: connectorLayoutRule.right,
    reason: 'Derived edge-to-edge bar from focal core right edge to right node left edge.',
    allowed_range: { endpoint_gap_abs_max: 2, y_error_abs_max: 2 },
    reuse_risk: 'low_after_derivation',
  },
  G28_LDC_CalloutSlots: {
    target: 'three-callout row',
    value: calloutSlotLayoutRule,
    reason: 'Bounded 3-callout row that preserves host-side breathing room and caption clearance.',
    allowed_range: { max_width_ratio: 0.85, max_height_ratio: 0.45, caption_gap_min: 60 },
    reuse_risk: 'medium_high_for_four_callouts',
  },
  G28_LDC_Hosts: {
    target: 'lower-corner hosts',
    value: 'source rectangles retained',
    reason: 'Hosts remain non-focal emotional anchors and are not part of layout-system polish.',
    allowed_range: { area_ratio_max_each: 0.03, caption_overlap_px: 0 },
    reuse_risk: 'medium_across_themes',
  },
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
function rectForId(byId, id) {
  const item = byId.get(id);
  if (!item) throw new Error(`LAYOUT_SOURCE_ITEM_MISSING: ${id}`);
  return layoutRectFor(item, byId);
}
function edgeValue(rect, edge) {
  if (edge === 'left') return rect.x;
  if (edge === 'right') return rectRight(rect);
  if (edge === 'top') return rect.y;
  if (edge === 'bottom') return rectBottom(rect);
  throw new Error(`UNSUPPORTED_EDGE: ${edge}`);
}
function connectorRectFor(item, byId) {
  const side = item.id === 'G28_LDC_Connector_Left' ? 'left' :
    item.id === 'G28_LDC_Connector_Right' ? 'right' : null;
  if (!side) return null;
  const rule = connectorLayoutRule[side];
  const fromRect = rectForId(byId, rule.from);
  const toRect = rectForId(byId, rule.to);
  const startX = edgeValue(fromRect, rule.from_edge);
  const endX = edgeValue(toRect, rule.to_edge);
  const yReferenceRect = rule.y_reference === 'to_center' ? toRect : fromRect;
  const thickness = connectorLayoutRule.thickness;
  return {
    x: startX,
    y: rectCenter(yReferenceRect).y - thickness / 2,
    width: endX - startX,
    height: thickness,
  };
}
function calloutSlotRectFor(item) {
  const match = /^G28_LDC_CalloutSlot_(\d)$/.exec(item.id);
  if (!match) return null;
  const index = Number(match[1]) - 1;
  if (index < 0 || index >= calloutSlotLayoutRule.active_count) {
    throw new Error(`CALLOUT_SLOT_INDEX_OUT_OF_CONTRACT: ${item.id}`);
  }
  return {
    x: calloutSlotLayoutRule.start_x + index * (calloutSlotLayoutRule.width + calloutSlotLayoutRule.gap),
    y: calloutSlotLayoutRule.row_y,
    width: calloutSlotLayoutRule.width,
    height: calloutSlotLayoutRule.height,
  };
}
function layoutRectFor(item, byId) {
  return connectorRectFor(item, byId) || calloutSlotRectFor(item) || item.rect;
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

function shapePrimitive(item, byId) {
  const rect = layoutRectFor(item, byId);
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
    layout_contract: {
      rect_source: item.rect === rect ? 'source_rect' : 'derived_layout_contract',
      source_rect: item.rect,
      derived_rect: rect,
      manual_registry_entry: manualOffsetRegistry[item.id] || null,
    },
    description: `G-28 source carrier primitive ${item.id}`,
  };
}

function centeredTextPrimitive(displayName, groupId, role, layer, targetBox, fontSize, content, color, description) {
  const bboxWidth = estimateTextWidth(content, fontSize);
  const bboxHeight = fontSize;
  const registryEntry = manualOffsetRegistry[displayName] || null;
  const visualOffset = registryEntry?.value || { x: 0, y: 0 };
  const centerScreen = rectCenter(targetBox.rect);
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
    layout_contract: {
      target_box_id: targetBox.id,
      target_box_rect: targetBox.rect,
      estimated_text_width: bboxWidth,
      estimated_text_height: bboxHeight,
      box_center_x: centerScreen.x,
      box_center_y: centerScreen.y,
      baseline_adjust: visualOffset.y,
      visual_offset_x: visualOffset.x,
      visual_offset_y: visualOffset.y,
      text_center_error_px: 0,
      manual_registry_entry: registryEntry,
    },
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
    .map((item) => shapePrimitive(item, byId));

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
      { id: 'G28_LDC_Title_Text_SourceRect', rect: layoutRectFor(title, byId) },
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
      { id: target.item.id, rect: layoutRectFor(target.item, byId) },
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
      { id: slot.id, rect: layoutRectFor(slot, byId) },
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
    layout_contract_revision: layoutContractRevision,
    right_node_alignment_revision: rightNodeAlignmentRevision,
    callout_label_alignment_revision: calloutLabelAlignmentRevision,
    layout_contract_rules: {
      connector_layout_rule: connectorLayoutRule,
      callout_slot_layout_rule: calloutSlotLayoutRule,
      manual_offset_registry: manualOffsetRegistry,
      thresholds: layoutThresholds,
    },
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

function layerStats(items, filterFn) {
  const layers = items.filter(filterFn).map((item) => item.layer);
  if (!layers.length) return null;
  return { min: Math.min(...layers), max: Math.max(...layers), layers };
}
function roundMetric(value) {
  return Math.round(value * 1000) / 1000;
}
function distance(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}
function rectArea(rect) {
  return rect.width * rect.height;
}
function intersectionRect(a, b) {
  const x1 = Math.max(a.x, b.x);
  const y1 = Math.max(a.y, b.y);
  const x2 = Math.min(rectRight(a), rectRight(b));
  const y2 = Math.min(rectBottom(a), rectBottom(b));
  if (x2 <= x1 || y2 <= y1) return { x: x1, y: y1, width: 0, height: 0 };
  return { x: x1, y: y1, width: x2 - x1, height: y2 - y1 };
}
function maxOf(values) {
  return values.length ? Math.max(...values) : 0;
}
function textCenteringMetrics(textItems) {
  const items = textItems
    .filter((item) => item.layout_contract?.target_box_rect)
    .map((item) => {
      const boxCenter = rectCenter(item.layout_contract.target_box_rect);
      const expectedCenter = {
        x: boxCenter.x + item.layout_contract.visual_offset_x,
        y: boxCenter.y + item.layout_contract.visual_offset_y,
      };
      const actualCenter = rectCenter(item.screen_rect);
      const implementationError = distance(actualCenter, expectedCenter);
      const registeredOffset = distance(boxCenter, expectedCenter);
      return {
        id: item.display_name,
        text: item.text,
        target_box_id: item.layout_contract.target_box_id,
        font_size: item.font_size,
        estimated_text_width: item.layout_contract.estimated_text_width,
        estimated_text_height: item.layout_contract.estimated_text_height,
        box_center_x: item.layout_contract.box_center_x,
        box_center_y: item.layout_contract.box_center_y,
        baseline_adjust: item.layout_contract.baseline_adjust,
        visual_offset_x: item.layout_contract.visual_offset_x,
        visual_offset_y: item.layout_contract.visual_offset_y,
        implementation_error_px: roundMetric(implementationError),
        registered_optical_offset_px: roundMetric(registeredOffset),
        pass: implementationError <= layoutThresholds.text_center_error_px &&
          registeredOffset <= layoutThresholds.registered_optical_offset_px,
      };
    });
  return {
    formula: 'top_left = center(target_box) + registered_visual_offset - estimated_text_bbox / 2',
    metric_scope: 'Measures implementation placement against the registered offset and estimated text box; it is not a rendered YMM4 glyph optical-center measurement.',
    character_width_model: 'Japanese full-width ranges count as 1.0em; other characters count as 0.55em; height is font_size.',
    threshold_px: layoutThresholds.text_center_error_px,
    registered_optical_offset_threshold_px: layoutThresholds.registered_optical_offset_px,
    text_center_error_px: roundMetric(maxOf(items.map((item) => item.implementation_error_px))),
    registered_optical_offset_max_px: roundMetric(maxOf(items.map((item) => item.registered_optical_offset_px))),
    pass: items.every((item) => item.pass),
    items,
  };
}
function rightNodeAlignmentMetrics(textItems) {
  const item = textItems.find((candidate) => candidate.display_name === rightNodeAlignmentRevision.target_label);
  if (!item) {
    return {
      ...rightNodeAlignmentRevision,
      pass: false,
      failure: 'target_label_missing',
    };
  }
  const entry = manualOffsetRegistry[rightNodeAlignmentRevision.target_label];
  return {
    ...rightNodeAlignmentRevision,
    target_text: item.text,
    target_box_id: item.layout_contract?.target_box_id || null,
    manual_offset_registry_update: entry,
    applied_visual_offset_px: {
      x: item.layout_contract?.visual_offset_x ?? null,
      y: item.layout_contract?.visual_offset_y ?? null,
    },
    screen_rect: item.screen_rect,
    readback_metric_caveat: 'text_center_error_px=0 means the label was placed exactly at the registered offset; the human GUI recheck is the authority for rendered optical centering.',
    previous_registered_offset_px: { x: 0, y: -4 },
    pass: Boolean(entry &&
      item.layout_contract?.visual_offset_x === entry.value.x &&
      item.layout_contract?.visual_offset_y === entry.value.y &&
      Math.abs(entry.value.x) <= entry.allowed_range.x_abs_max &&
      Math.abs(entry.value.y) <= entry.allowed_range.y_abs_max),
  };
}
function calloutLabelAlignmentMetrics(textItems) {
  const item = textItems.find((candidate) => candidate.display_name === calloutLabelAlignmentRevision.target_label);
  if (!item) {
    return {
      ...calloutLabelAlignmentRevision,
      previous_right_node_fix: rightNodeAlignmentRevision,
      pass: false,
      failure: 'target_label_missing',
    };
  }
  const entry = manualOffsetRegistry[calloutLabelAlignmentRevision.target_label];
  return {
    ...calloutLabelAlignmentRevision,
    target_text: item.text,
    target_box_id: item.layout_contract?.target_box_id || null,
    manual_offset_registry_update: entry,
    applied_visual_offset_px: {
      x: item.layout_contract?.visual_offset_x ?? null,
      y: item.layout_contract?.visual_offset_y ?? null,
    },
    screen_rect: item.screen_rect,
    readback_metric_caveat: 'text_center_error_px=0 means the callout label was placed exactly at the registered offset; the human GUI correction is the authority for rendered optical centering.',
    previous_registered_offset_px: { x: 0, y: -3 },
    previous_right_node_fix: {
      revision_id: rightNodeAlignmentRevision.revision_id,
      retained: true,
      note: 'The prior right-node offset is not rolled back because the target correction did not report an adverse side effect.',
    },
    pass: Boolean(entry &&
      item.layout_contract?.visual_offset_x === entry.value.x &&
      item.layout_contract?.visual_offset_y === entry.value.y &&
      Math.abs(entry.value.x) <= entry.allowed_range.x_abs_max &&
      Math.abs(entry.value.y) <= entry.allowed_range.y_abs_max),
  };
}
function connectorAlignmentMetrics(items) {
  const byName = new Map(items.map((item) => [item.display_name, item]));
  const leftNode = byName.get('G28_LDC_Node_Left')?.screen_rect;
  const focalCore = byName.get('G28_LDC_Focal_Core')?.screen_rect;
  const rightNode = byName.get('G28_LDC_Node_Right')?.screen_rect;
  const leftConnector = byName.get('G28_LDC_Connector_Left')?.screen_rect;
  const rightConnector = byName.get('G28_LDC_Connector_Right')?.screen_rect;
  const metrics = [];
  if (leftNode && focalCore && leftConnector) {
    metrics.push({
      id: 'G28_LDC_Connector_Left',
      start_gap_px: roundMetric(leftConnector.x - rectRight(leftNode)),
      end_gap_px: roundMetric(focalCore.x - rectRight(leftConnector)),
      y_center_error_px: roundMetric(rectCenter(leftConnector).y - rectCenter(leftNode).y),
    });
  }
  if (focalCore && rightNode && rightConnector) {
    metrics.push({
      id: 'G28_LDC_Connector_Right',
      start_gap_px: roundMetric(rightConnector.x - rectRight(focalCore)),
      end_gap_px: roundMetric(rightNode.x - rectRight(rightConnector)),
      y_center_error_px: roundMetric(rectCenter(rightConnector).y - rectCenter(rightNode).y),
    });
  }
  const maxError = maxOf(metrics.flatMap((item) => [
    Math.abs(item.start_gap_px),
    Math.abs(item.end_gap_px),
    Math.abs(item.y_center_error_px),
  ]));
  return {
    formula: 'connector spans from source edge to target edge, with y centered on the adjacent side node and fixed thickness.',
    threshold_px: layoutThresholds.connector_alignment_error_px,
    connector_alignment_error_px: roundMetric(maxError),
    pass: maxError <= layoutThresholds.connector_alignment_error_px,
    items: metrics,
  };
}
function captionReserveOverlapMetric(items, captionReserve) {
  const overlapsReadback = items
    .filter((item) => item.display_name !== 'G28_LDC_BG_Stage' && item.screen_rect)
    .map((item) => ({ item, intersection: intersectionRect(item.screen_rect, captionReserve) }))
    .filter(({ intersection }) => intersection.width > 0 && intersection.height > 0)
    .map(({ item, intersection }) => ({
      id: item.display_name,
      overlap_area_px: roundMetric(rectArea(intersection)),
      overlap_height_px: roundMetric(intersection.height),
    }));
  return {
    threshold_px: layoutThresholds.caption_reserve_overlap_px,
    caption_reserve_overlap_px: roundMetric(maxOf(overlapsReadback.map((item) => item.overlap_height_px))),
    overlap_area_px: roundMetric(overlapsReadback.reduce((sum, item) => sum + item.overlap_area_px, 0)),
    pass: overlapsReadback.length === 0,
    items: overlapsReadback,
  };
}
function calloutDensityMetrics(calloutShapes, calloutLabels) {
  const labelsBySlot = new Map(calloutLabels.map((item) => [item.display_name.replace('_Label', ''), item]));
  const items = calloutShapes.map((slot) => {
    const label = labelsBySlot.get(slot.display_name);
    const widthRatio = label ? label.screen_rect.width / slot.screen_rect.width : 0;
    const heightRatio = label ? label.screen_rect.height / slot.screen_rect.height : 0;
    return {
      slot: slot.display_name,
      label: label?.display_name || null,
      text: label?.text || null,
      width_ratio: roundMetric(widthRatio),
      height_ratio: roundMetric(heightRatio),
      pass: widthRatio <= layoutThresholds.callout_density_width_ratio &&
        heightRatio <= layoutThresholds.callout_density_height_ratio,
    };
  });
  return {
    supported_counts: calloutSlotLayoutRule.supported_counts,
    active_count: calloutSlotLayoutRule.active_count,
    four_callout_risk: calloutSlotLayoutRule.four_callout_risk,
    width_ratio_threshold: layoutThresholds.callout_density_width_ratio,
    height_ratio_threshold: layoutThresholds.callout_density_height_ratio,
    max_width_ratio: roundMetric(maxOf(items.map((item) => item.width_ratio))),
    max_height_ratio: roundMetric(maxOf(items.map((item) => item.height_ratio))),
    pass: items.every((item) => item.pass),
    items,
  };
}
function hostFocalityRiskMetrics(hosts, focalCore, captionReserve) {
  const frameArea = FRAME.width * FRAME.height;
  const items = hosts.map((host) => {
    const areaRatio = rectArea(host.screen_rect) / frameArea;
    const belowFocal = focalCore ? host.screen_rect.y > focalCore.screen_rect.y : false;
    const aboveCaption = rectBottom(host.screen_rect) <= captionReserve.y;
    const lowRisk = host.role === 'decoration' &&
      areaRatio <= layoutThresholds.host_area_ratio &&
      belowFocal &&
      aboveCaption &&
      !host.text;
    return {
      id: host.display_name,
      area_ratio: roundMetric(areaRatio),
      role: host.role,
      below_focal: belowFocal,
      above_caption_reserve: aboveCaption,
      risk: lowRisk ? 'low' : 'review',
    };
  });
  return {
    area_ratio_threshold_each: layoutThresholds.host_area_ratio,
    host_focality_risk: items.every((item) => item.risk === 'low') ? 'low' : 'review',
    pass: items.every((item) => item.risk === 'low'),
    items,
  };
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
  const textCenteringReadback = textCenteringMetrics(textItems);
  const rightNodeAlignmentReadback = rightNodeAlignmentMetrics(textItems);
  const calloutLabelAlignmentReadback = calloutLabelAlignmentMetrics(textItems);
  const connectorAlignmentReadback = connectorAlignmentMetrics(items);
  const captionReserveOverlapReadback = captionReserveOverlapMetric(items, captionReserve);
  const calloutDensityReadback = calloutDensityMetrics(calloutShapes, calloutLabels);
  const hostFocalityRiskReadback = hostFocalityRiskMetrics(hosts, focalCore, captionReserve);
  const layoutContractReadback = {
    revision: primitivePlan.layout_contract_revision,
    rules: primitivePlan.layout_contract_rules,
    next_decision: primitivePlan.layout_contract_revision.next_decision,
    rectangle_text_centering: textCenteringReadback,
    right_node_alignment: rightNodeAlignmentReadback,
    callout_label_alignment: calloutLabelAlignmentReadback,
    connector_positioning: connectorAlignmentReadback,
    callout_slot_layout: calloutDensityReadback,
    manual_offset_registry: primitivePlan.layout_contract_rules.manual_offset_registry,
    tolerance_metrics: {
      text_center_error_px: textCenteringReadback.text_center_error_px,
      registered_optical_offset_max_px: textCenteringReadback.registered_optical_offset_max_px,
      connector_alignment_error_px: connectorAlignmentReadback.connector_alignment_error_px,
      caption_reserve_overlap_px: captionReserveOverlapReadback.caption_reserve_overlap_px,
      callout_density: {
        max_width_ratio: calloutDensityReadback.max_width_ratio,
        max_height_ratio: calloutDensityReadback.max_height_ratio,
      },
      host_focality_risk: hostFocalityRiskReadback.host_focality_risk,
    },
    caption_reserve_overlap: captionReserveOverlapReadback,
    host_focality_risk: hostFocalityRiskReadback,
    limitations: [
      'Text width remains an approximation and should not be treated as font-engine proof.',
      'Manual optical offsets are now registered and bounded, not removed.',
      'Right-node rendered optical centering still requires human GUI review; readback verifies the registered correction, not YMM4 glyph pixels.',
      'Callout-label rendered optical centering still requires human GUI review; readback verifies the registered correction, not YMM4 glyph pixels.',
      'Callout row formula is intended for 2-3 callouts; 4 callouts should fail fast or use another layout.',
    ],
  };
  const layoutContractPass = textCenteringReadback.pass &&
    rightNodeAlignmentReadback.pass &&
    calloutLabelAlignmentReadback.pass &&
    connectorAlignmentReadback.pass &&
    captionReserveOverlapReadback.pass &&
    calloutDensityReadback.pass &&
    hostFocalityRiskReadback.pass;
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
    layout_contract_metrics_present: true,
    layout_contract_tolerances_pass: layoutContractPass,
    right_node_alignment_fix_recorded: rightNodeAlignmentReadback.pass,
    callout_label_alignment_fix_recorded: calloutLabelAlignmentReadback.pass,
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
    classification: failures.length === 0 && missing.length === 0 ? primitivePlan.callout_label_alignment_revision.classification : 'fail_ymmp_probe_readback',
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
    layout_contract_revision: primitivePlan.layout_contract_revision,
    right_node_alignment_revision: primitivePlan.right_node_alignment_revision,
    callout_label_alignment_revision: primitivePlan.callout_label_alignment_revision,
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
    layout_contract_readback: layoutContractReadback,
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
  lines.push('## Layout Contract Revision');
  lines.push('');
  lines.push(`- revision id: \`${readback.layout_contract_revision.revision_id}\``);
  lines.push(`- classification: \`${readback.layout_contract_revision.classification}\``);
  lines.push(`- next decision: \`${readback.layout_contract_revision.next_decision}\``);
  lines.push('- scope: derived connector geometry, registered text offsets, callout row rule, and tolerance readback metrics.');
  lines.push('- boundary: diagnostic-only implementation improvement; not production approval, render approval, rights approval, creative final acceptance, or slot-fill.');
  lines.push('');
  lines.push('## Right Node Alignment Revision');
  lines.push('');
  lines.push(`- revision id: \`${readback.right_node_alignment_revision.revision_id}\``);
  lines.push(`- source human decision: \`${readback.right_node_alignment_revision.source_human_decision}\``);
  lines.push(`- classification: \`${readback.right_node_alignment_revision.classification}\``);
  lines.push(`- target label: \`${readback.right_node_alignment_revision.target_label}\``);
  lines.push(`- observed issue: ${readback.right_node_alignment_revision.observed_issue}`);
  lines.push(`- cause classification: \`${readback.right_node_alignment_revision.cause_classification}\``);
  lines.push(`- formula change: ${readback.right_node_alignment_revision.formula_change}`);
  lines.push(`- boundary note: ${readback.right_node_alignment_revision.boundary_note}`);
  lines.push('');
  lines.push('## Callout Label Alignment Revision');
  lines.push('');
  lines.push(`- revision id: \`${readback.callout_label_alignment_revision.revision_id}\``);
  lines.push(`- source human decision: \`${readback.callout_label_alignment_revision.source_human_decision}\``);
  lines.push(`- classification: \`${readback.callout_label_alignment_revision.classification}\``);
  lines.push(`- target label: \`${readback.callout_label_alignment_revision.target_label}\``);
  lines.push(`- observed issue: ${readback.callout_label_alignment_revision.observed_issue}`);
  lines.push(`- target correction: ${readback.callout_label_alignment_revision.target_correction}`);
  lines.push(`- cause classification: \`${readback.callout_label_alignment_revision.cause_classification}\``);
  lines.push(`- formula change: ${readback.callout_label_alignment_revision.formula_change}`);
  lines.push(`- boundary note: ${readback.callout_label_alignment_revision.boundary_note}`);
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
  lines.push('## Layout Contract Readback');
  lines.push('');
  lines.push(`- text_center_error_px: ${readback.layout_contract_readback.tolerance_metrics.text_center_error_px} (threshold ${readback.layout_contract_readback.rectangle_text_centering.threshold_px})`);
  lines.push(`- registered_optical_offset_max_px: ${readback.layout_contract_readback.tolerance_metrics.registered_optical_offset_max_px} (threshold ${readback.layout_contract_readback.rectangle_text_centering.registered_optical_offset_threshold_px})`);
  lines.push(`- connector_alignment_error_px: ${readback.layout_contract_readback.tolerance_metrics.connector_alignment_error_px} (threshold ${readback.layout_contract_readback.connector_positioning.threshold_px})`);
  lines.push(`- caption_reserve_overlap_px: ${readback.layout_contract_readback.tolerance_metrics.caption_reserve_overlap_px}`);
  lines.push(`- callout_density: width=${readback.layout_contract_readback.tolerance_metrics.callout_density.max_width_ratio}, height=${readback.layout_contract_readback.tolerance_metrics.callout_density.max_height_ratio}`);
  lines.push(`- host_focality_risk: \`${readback.layout_contract_readback.tolerance_metrics.host_focality_risk}\``);
  lines.push(`- formula: ${readback.layout_contract_readback.rectangle_text_centering.formula}`);
  lines.push(`- metric scope: ${readback.layout_contract_readback.rectangle_text_centering.metric_scope}`);
  lines.push(`- right node applied offset: x=${readback.layout_contract_readback.right_node_alignment.applied_visual_offset_px.x}, y=${readback.layout_contract_readback.right_node_alignment.applied_visual_offset_px.y}`);
  lines.push(`- right node caveat: ${readback.layout_contract_readback.right_node_alignment.readback_metric_caveat}`);
  lines.push(`- callout label applied offset: x=${readback.layout_contract_readback.callout_label_alignment.applied_visual_offset_px.x}, y=${readback.layout_contract_readback.callout_label_alignment.applied_visual_offset_px.y}`);
  lines.push(`- callout label caveat: ${readback.layout_contract_readback.callout_label_alignment.readback_metric_caveat}`);
  lines.push(`- connector rule: ${readback.layout_contract_readback.connector_positioning.formula}`);
  lines.push(`- callout supported counts: ${readback.layout_contract_readback.callout_slot_layout.supported_counts.join(', ')}`);
  lines.push('- 4-callout handling: fail fast or change layout; do not squeeze into the current 3-slot row.');
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

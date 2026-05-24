const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const fps = 60;

const paths = {
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_report.md',
};

const shapeSizeMode = 'WidthHeight';
const maxDisplayNameLength = 24;
const maxRemarkLength = 80;
const hexColorPattern = /^#[0-9A-Fa-f]{8}$/;

const assumptionsUnderTest = [
  'YMM4 ShapeItem rectangles need WidthHeight plus non-zero StrokeThickness to become material panels.',
  'X/Y coordinates are expected to behave as center-origin placement in the 1920x1080 preview canvas.',
  'Panel-contained TextItems should be legible when positioned inside a large panel, not as independent floating labels.',
  'A single light-stage tonal system should keep panel, text, markers, and connector readable without black/white background toggles.',
  'Human-readable short Remarks should keep the YMM4 authoring surface manageable while detailed provenance stays in readback/report.',
];

const calibrationFrame = {
  frame: 0,
  duration_frames: 900,
  canvas: { width: 1920, height: 1080 },
  tonal_system: 'light-stage',
  background_color: '#FFF4F7FB',
  panel: {
    name: 'Main Panel',
    x: 0,
    y: 0,
    width: 920,
    height: 560,
    color: '#FF155EA8',
    opacity: 100,
  },
};

const calibrationItems = [
  shape('BG', 'background', 5, 0, 0, 1920, 1080, '#FFF4F7FB', 100, 0, 1080, true, 'full-screen light-stage background'),
  shape('Main Panel', 'panel', 8, 0, 0, 920, 560, '#FF155EA8', 100, 24, 560, true, 'central filled panel'),
  text('Panel Title', 'panel_title', 9, 0, -145, 68, 'PANEL TITLE', '#FFFFFFFF', true, 'Main Panel', 'large title inside panel'),
  text('Panel Body', 'panel_body', 9, 0, -60, 38, 'Body text stays inside this panel.', '#FFFFFFFF', true, 'Main Panel', 'body line inside panel'),
  shape('Center Marker', 'center_marker', 10, 0, 0, 56, 56, '#FFFF3B30', 100, 6, 56, true, 'center-origin marker'),
  text('Center Label', 'center_label', 11, 0, 74, 34, 'CENTER', '#FFFFFFFF', true, 'Main Panel', 'label for center marker'),
  shape('TL Marker', 'top_left_marker', 10, -460, -280, 56, 56, '#FF16A34A', 100, 4, 56, true, 'expected panel top-left marker'),
  text('TL Label', 'top_left_label', 11, -350, -246, 32, 'TOP LEFT', '#FFFFFFFF', true, 'Main Panel', 'label for top-left marker'),
  shape('BR Marker', 'bottom_right_marker', 10, 460, 280, 56, 56, '#FFFF9500', 100, 4, 56, true, 'expected panel bottom-right marker'),
  text('BR Label', 'bottom_right_label', 11, 345, 246, 32, 'BOTTOM RIGHT', '#FFFFFFFF', true, 'Main Panel', 'label for bottom-right marker'),
  shape('Connector', 'connector', 10, 245, 140, 420, 42, '#FFFFD43B', 100, 6, 42, true, 'thick relation primitive from center toward lower-right'),
];

function shape(displayName, role, layer, x, y, width, height, color, opacity, round, strokeThickness, visibleBorderExpected, description) {
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
    intended_inside_panel: role !== 'background',
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
    intended_inside_panel: intendedInsidePanel,
    expected_panel: panelName,
    description,
  };
}

function abs(relPath) {
  return path.join(root, relPath);
}

function readText(relPath) {
  return fs.readFileSync(abs(relPath), 'utf8').replace(/^\uFEFF/, '');
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
  fs.writeFileSync(abs(relPath), `\uFEFF${JSON.stringify(payload, null, 2)}`, 'utf8');
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
  item.Frame = calibrationFrame.frame;
  item.Length = calibrationFrame.duration_frames;
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
    Frame: calibrationFrame.frame,
    Layer: primitive.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: calibrationFrame.duration_frames,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: primitive.display_name,
    IsLocked: false,
    IsHidden: false,
  };
}

function validateCalibrationDesign() {
  const errors = [];
  if (calibrationItems.length > 12) errors.push(`too many calibration items: ${calibrationItems.length}`);
  if (calibrationFrame.tonal_system !== 'light-stage') errors.push('tonal system must be light-stage');
  const panel = calibrationItems.find((item) => item.display_name === 'Main Panel');
  if (!panel) errors.push('Main Panel missing');
  if (panel && (panel.width < 800 || panel.width > 1000 || panel.height < 450 || panel.height > 650)) {
    errors.push(`Main Panel geometry outside required range: ${panel.width}x${panel.height}`);
  }
  for (const item of calibrationItems) {
    if (!['ShapeItem', 'TextItem'].includes(item.kind)) errors.push(`${item.display_name} unsupported item type ${item.kind}`);
    if (item.display_name.length > maxDisplayNameLength) errors.push(`${item.display_name} display name too long`);
    if (item.display_name.length > maxRemarkLength) errors.push(`${item.display_name} remark too long`);
    if (item.opacity < 90) errors.push(`${item.display_name} opacity below 90`);
    if (item.kind === 'ShapeItem') {
      if (item.width <= 0 || item.height <= 0) errors.push(`${item.display_name} invalid geometry`);
      if (item.visible_border_expected && item.stroke_thickness <= 0) errors.push(`${item.display_name} expected visible border/fill but stroke is zero`);
      if (item.role === 'panel' && item.stroke_thickness < item.height * 0.8) {
        errors.push(`${item.display_name} stroke thickness is too low for filled-panel calibration`);
      }
    }
    if (item.kind === 'TextItem' && item.font_size < 30) errors.push(`${item.display_name} font size too small`);
  }
  if (errors.length) throw new Error(`CALIBRATION_DESIGN_INVALID: ${errors.join('; ')}`);
}

function buildProbeProject(carrierYmmp, shapeTemplateYmmp) {
  validateCalibrationDesign();
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) {
    throw new Error(`SHAPE_TEMPLATE_MISSING: ${paths.shapeTemplateYmmp}`);
  }
  const project = clone(carrierYmmp);
  const timeline = project.Timelines?.[0];
  if (!timeline || !Array.isArray(project.Timelines)) {
    throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  }
  const items = calibrationItems.map((primitive) => {
    if (primitive.kind === 'ShapeItem') return makeShapeItem(shapeTemplate, primitive);
    if (primitive.kind === 'TextItem') return makeTextItem(primitive);
    throw new Error(`UNSUPPORTED_PRIMITIVE_KIND: ${primitive.kind}`);
  });
  timeline.Items = items;
  timeline.CurrentFrame = 0;
  timeline.Length = calibrationFrame.duration_frames;
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

function parseAarrggbb(color) {
  if (!(typeof color === 'string' && hexColorPattern.test(color))) return null;
  return {
    a: parseInt(color.slice(1, 3), 16),
    r: parseInt(color.slice(3, 5), 16),
    g: parseInt(color.slice(5, 7), 16),
    b: parseInt(color.slice(7, 9), 16),
  };
}

function srgbToLinear(channel) {
  const normalized = channel / 255;
  return normalized <= 0.03928 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
}

function relativeLuminance(color) {
  const parsed = parseAarrggbb(color);
  if (!parsed) return null;
  return 0.2126 * srgbToLinear(parsed.r) + 0.7152 * srgbToLinear(parsed.g) + 0.0722 * srgbToLinear(parsed.b);
}

function contrastRatio(foreground, background) {
  const fg = relativeLuminance(foreground);
  const bg = relativeLuminance(background);
  if (fg === null || bg === null) return null;
  const lighter = Math.max(fg, bg);
  const darker = Math.min(fg, bg);
  return Number(((lighter + 0.05) / (darker + 0.05)).toFixed(2));
}

function expectedBounds(primitive) {
  if (primitive.kind !== 'ShapeItem') return null;
  return {
    left: primitive.x - primitive.width / 2,
    top: primitive.y - primitive.height / 2,
    right: primitive.x + primitive.width / 2,
    bottom: primitive.y + primitive.height / 2,
  };
}

function pointInside(bounds, x, y) {
  return Boolean(bounds && x >= bounds.left && x <= bounds.right && y >= bounds.top && y <= bounds.bottom);
}

function roughTextBounds(primitive) {
  if (primitive.kind !== 'TextItem') return null;
  const roughWidth = primitive.content.length * primitive.font_size * 0.62;
  const roughHeight = primitive.font_size * 1.3;
  return {
    left: Number((primitive.x - roughWidth / 2).toFixed(1)),
    top: Number((primitive.y - roughHeight / 2).toFixed(1)),
    right: Number((primitive.x + roughWidth / 2).toFixed(1)),
    bottom: Number((primitive.y + roughHeight / 2).toFixed(1)),
    rough_width: Number(roughWidth.toFixed(1)),
    rough_height: Number(roughHeight.toFixed(1)),
  };
}

function boundsInside(outer, inner) {
  return Boolean(outer && inner && inner.left >= outer.left && inner.right <= outer.right && inner.top >= outer.top && inner.bottom <= outer.bottom);
}

function expectedPanelRelationship(primitive) {
  const panel = calibrationItems.find((item) => item.display_name === 'Main Panel');
  const panelBounds = expectedBounds(panel);
  if (!primitive.intended_inside_panel) {
    return {
      intended_inside_panel: false,
      expected_panel: null,
      expected_panel_bounds: null,
      expected_center_inside_panel: false,
      rough_text_bounds_inside_panel: null,
    };
  }
  const textBounds = roughTextBounds(primitive);
  return {
    intended_inside_panel: true,
    expected_panel: primitive.expected_panel || 'Main Panel',
    expected_panel_bounds: panelBounds,
    expected_center_inside_panel: pointInside(panelBounds, primitive.x, primitive.y),
    rough_text_bounds: textBounds,
    rough_text_bounds_inside_panel: textBounds ? boundsInside(panelBounds, textBounds) : null,
    coordinate_assumption: 'X/Y values are intended as center-origin coordinates',
  };
}

function suspiciousDefaultNotes(readbackItem) {
  const notes = [];
  if (readbackItem.opacity < 90) notes.push('opacity below 90');
  if (readbackItem.item_type === 'ShapeItem') {
    if (readbackItem.shape_size_mode !== shapeSizeMode) notes.push(`shape size mode is ${readbackItem.shape_size_mode}`);
    if (readbackItem.shape_aspect_rate === 0) notes.push('aspect ratio is zero');
    if (readbackItem.role !== 'center_marker' && readbackItem.role !== 'top_left_marker' && readbackItem.role !== 'bottom_right_marker' && readbackItem.role !== 'connector') {
      if (Math.max(readbackItem.width || 0, readbackItem.height || 0) <= 100) notes.push('large visible shape uses tiny dimensions');
    }
    if (readbackItem.visible_border_expected && readbackItem.stroke_thickness <= 0) notes.push('visible border/fill expected but stroke thickness is zero');
  }
  if (readbackItem.item_type === 'TextItem') {
    if (readbackItem.font_size < 30) notes.push('text font size below 30');
    if (!(typeof readbackItem.text_color === 'string' && hexColorPattern.test(readbackItem.text_color))) notes.push('text color is not #AARRGGBB');
  }
  if (readbackItem.display_name_length > maxDisplayNameLength) notes.push('display name too long');
  if (readbackItem.remark_length > maxRemarkLength) notes.push('remark too long');
  return notes;
}

function readbackProbe(ymmp, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const items = timelineItems.map((item, index) => {
    const displayName = String(item.Remark || '');
    const expected = calibrationItems.find((entry) => entry.display_name === displayName);
    const type = itemType(item);
    const isShape = type === 'ShapeItem';
    const isText = type === 'TextItem';
    const textColor = isText ? item.FontColor : null;
    const fillColor = isShape ? item.ShapeParameter?.Brush?.Parameter?.Color || null : null;
    const expectedRelationship = expected ? expectedPanelRelationship(expected) : null;
    const textContrastAgainstPanel = isText ? contrastRatio(textColor, calibrationFrame.panel.color) : null;
    const textContrastAgainstStage = isText ? contrastRatio(textColor, calibrationFrame.background_color) : null;
    const readbackItem = {
      index,
      display_name: displayName,
      item_name: displayName,
      item_name_source: 'YMM4 Remark field; no long provenance is stored on the authoring surface',
      item_type: type,
      role: expected?.role || null,
      layer: item.Layer,
      frame: item.Frame,
      duration_frames: item.Length,
      x: animationValue(item, 'X') ?? null,
      y: animationValue(item, 'Y') ?? null,
      width: isShape ? shapeParameterValue(item, 'Width') ?? null : null,
      height: isShape ? shapeParameterValue(item, 'Height') ?? null : null,
      shape_size_mode: isShape ? item.ShapeParameter?.SizeMode || null : null,
      shape_size: isShape ? shapeParameterValue(item, 'Size') ?? null : null,
      shape_aspect_rate: isShape ? shapeParameterValue(item, 'AspectRate') ?? null : null,
      stroke_thickness: isShape ? shapeParameterValue(item, 'StrokeThickness') ?? null : null,
      opacity: animationValue(item, 'Opacity') ?? null,
      fill_color: fillColor,
      text_color: textColor,
      text: isText ? item.Text : null,
      font_size: isText ? shapeParameterValue(item, 'FontSize') ?? item.FontSize?.Values?.[0]?.Value ?? null : null,
      intended_inside_panel: expected?.intended_inside_panel || false,
      expected_panel_relationship: expectedRelationship,
      display_name_length: displayName.length,
      item_name_length_check: displayName.length <= maxDisplayNameLength ? 'pass' : 'fail',
      remark: item.Remark || '',
      remark_length: String(item.Remark || '').length,
      remark_length_check: String(item.Remark || '').length <= maxRemarkLength ? 'pass' : 'fail',
      visible_border_expected: expected?.visible_border_expected || false,
      color_contrast_notes: isText
        ? {
            against_main_panel: textContrastAgainstPanel,
            against_stage_background: textContrastAgainstStage,
            intended_background: expected?.intended_inside_panel ? 'Main Panel' : 'stage background',
            pass_for_intended_background: expected?.intended_inside_panel
              ? textContrastAgainstPanel !== null && textContrastAgainstPanel >= 4.5
              : textContrastAgainstStage !== null && textContrastAgainstStage >= 4.5,
          }
        : {
            fill_against_stage_background: fillColor ? contrastRatio(fillColor, calibrationFrame.background_color) : null,
            fill_against_main_panel: fillColor ? contrastRatio(fillColor, calibrationFrame.panel.color) : null,
            intended_background: expected?.intended_inside_panel ? 'Main Panel' : 'stage background',
          },
      detailed_provenance: {
        generator: paths.outputYmmp,
        calibration_item_description: expected?.description || null,
        source: 'G-27 user GUI reset; primitive visibility/geometry calibration only',
        not_video_scene: true,
        render_performed: false,
      },
    };
    readbackItem.suspicious_default_notes = suspiciousDefaultNotes(readbackItem);
    return readbackItem;
  });

  const missingItems = calibrationItems
    .filter((expected) => !items.find((item) => item.display_name === expected.display_name))
    .map((expected) => ({ display_name: expected.display_name, reason: 'expected calibration item not found' }));
  const malformedItems = [];
  for (const expected of calibrationItems) {
    const found = items.find((item) => item.display_name === expected.display_name);
    if (!found) continue;
    const mismatches = [];
    if (found.item_type !== expected.kind) mismatches.push({ field: 'item_type', expected: expected.kind, actual: found.item_type });
    if (found.layer !== expected.layer) mismatches.push({ field: 'layer', expected: expected.layer, actual: found.layer });
    if (found.frame !== calibrationFrame.frame) mismatches.push({ field: 'frame', expected: calibrationFrame.frame, actual: found.frame });
    if (found.duration_frames !== calibrationFrame.duration_frames) {
      mismatches.push({ field: 'duration_frames', expected: calibrationFrame.duration_frames, actual: found.duration_frames });
    }
    if (found.x !== expected.x || found.y !== expected.y) {
      mismatches.push({ field: 'position', expected: { x: expected.x, y: expected.y }, actual: { x: found.x, y: found.y } });
    }
    if (expected.kind === 'ShapeItem') {
      if (found.shape_size_mode !== shapeSizeMode) mismatches.push({ field: 'shape_size_mode', expected: shapeSizeMode, actual: found.shape_size_mode });
      if (found.width !== expected.width || found.height !== expected.height) {
        mismatches.push({ field: 'width_height', expected: { width: expected.width, height: expected.height }, actual: { width: found.width, height: found.height } });
      }
      if (found.stroke_thickness !== expected.stroke_thickness) {
        mismatches.push({ field: 'stroke_thickness', expected: expected.stroke_thickness, actual: found.stroke_thickness });
      }
      if (found.shape_aspect_rate === 0) mismatches.push({ field: 'shape_aspect_rate', expected: 'non-zero', actual: found.shape_aspect_rate });
    }
    if (expected.kind === 'TextItem') {
      if (found.text !== expected.content) mismatches.push({ field: 'text', expected: expected.content, actual: found.text });
      if (found.text_color !== expected.color) mismatches.push({ field: 'text_color', expected: expected.color, actual: found.text_color });
      if (found.color_contrast_notes && !found.color_contrast_notes.pass_for_intended_background) {
        mismatches.push({ field: 'contrast', expected: '>=4.5 against intended background', actual: found.color_contrast_notes });
      }
    }
    if (found.suspicious_default_notes.length > 0) mismatches.push({ field: 'suspicious_defaults', expected: [], actual: found.suspicious_default_notes });
    if (mismatches.length) malformedItems.push({ display_name: expected.display_name, mismatches });
  }

  const status = missingItems.length === 0 && malformedItems.length === 0 ? 'passed' : 'failed';

  return {
    artifact_type: 'g27_primitive_visibility_calibration_probe_readback',
    status,
    source: {
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_probe_ymmp: paths.outputYmmp,
    },
    boundary: {
      calibration_only: true,
      not_video_scene: true,
      existing_micro_scene_probe_modified: false,
      shape_item_text_item_only: true,
      tonal_system: calibrationFrame.tonal_system,
      black_white_background_mix: false,
      external_assets_used: false,
      tts_performed: false,
      url_fetch_performed: false,
      publishing_performed: false,
      render_performed: false,
      creative_acceptance_performed: false,
      production_readiness_claimed: false,
      minimal_render_smoke_recommendation: 'not_ready_until_calibration_gui_review_passes',
    },
    calibration: {
      frame: calibrationFrame.frame,
      duration_frames: calibrationFrame.duration_frames,
      duration_sec: calibrationFrame.duration_frames / fps,
      canvas: calibrationFrame.canvas,
      background_color: calibrationFrame.background_color,
      main_panel: calibrationFrame.panel,
      assumptions_under_test: assumptionsUnderTest,
      coordinate_anchor_origin_tested: true,
      panel_contained_text_tested: true,
      high_contrast_visibility_tested: true,
      authoring_surface_hygiene_tested: true,
    },
    source_integrity: {
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    totals: {
      item_count: items.length,
      expected_item_count: calibrationItems.length,
      shape_item_count: items.filter((item) => item.item_type === 'ShapeItem').length,
      text_item_count: items.filter((item) => item.item_type === 'TextItem').length,
      missing_item_count: missingItems.length,
      malformed_item_count: malformedItems.length,
      item_name_length_failures: items.filter((item) => item.item_name_length_check !== 'pass').length,
      remark_length_failures: items.filter((item) => item.remark_length_check !== 'pass').length,
      suspicious_default_item_count: items.filter((item) => item.suspicious_default_notes.length > 0).length,
    },
    items,
    missing_items: missingItems,
    malformed_items: malformedItems,
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Primitive Visibility Calibration Probe');
  lines.push('');
  lines.push(`Probe: \`${readback.source.generated_probe_ymmp}\``);
  lines.push('');
  lines.push('This is not a video scene. It is a bounded drawing-semantics calibration probe for YMM4 ShapeItem/TextItem visibility, geometry, and authoring-surface hygiene.');
  lines.push('');
  lines.push('## 1. What exactly is being calibrated?');
  lines.push('');
  lines.push('- ShapeItem position, WidthHeight geometry, non-zero StrokeThickness visibility, opacity, color contrast, TextItem containment, connector visibility, and short YMM4 authoring labels.');
  lines.push('');
  lines.push('## 2. Which assumptions from the failed micro scene are being tested?');
  lines.push('');
  readback.calibration.assumptions_under_test.forEach((assumption) => {
    lines.push(`- ${assumption}`);
  });
  lines.push('');
  lines.push('## 3. Does the probe intentionally test coordinate / anchor behavior?');
  lines.push('');
  lines.push('- Yes. `Center Marker` is placed at `(0, 0)`, `TL Marker` at the expected top-left corner of the 920x560 panel, and `BR Marker` at the expected bottom-right corner. If these markers do not align with panel geometry in YMM4, the X/Y anchor assumption is wrong or incomplete.');
  lines.push('');
  lines.push('## 4. Does the probe intentionally test panel-contained text?');
  lines.push('');
  lines.push('- Yes. `Panel Title`, `Panel Body`, and marker labels are positioned inside `Main Panel`; readback records expected panel relationships and rough text bounds.');
  lines.push('');
  lines.push('## 5. Does the probe intentionally test high-contrast visibility?');
  lines.push('');
  lines.push('- Yes. It uses one light-stage tonal system, a dark blue central panel, white panel text, high-contrast markers, and an amber connector. Primary opacity is 100%.');
  lines.push('');
  lines.push('## 6. Does the probe keep provenance out of YMM4 item names / Remarks?');
  lines.push('');
  lines.push('- Yes. YMM4 Remarks are short display names only. Detailed provenance is kept in the readback JSON and this report.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Readback status: \`${readback.status}\``);
  lines.push(`- Items: \`${readback.totals.item_count}\` (ShapeItem=\`${readback.totals.shape_item_count}\`, TextItem=\`${readback.totals.text_item_count}\`)`);
  lines.push(`- Tonal system: \`${readback.boundary.tonal_system}\``);
  lines.push(`- Item name length failures: \`${readback.totals.item_name_length_failures}\``);
  lines.push(`- Remark length failures: \`${readback.totals.remark_length_failures}\``);
  lines.push(`- Suspicious default item count: \`${readback.totals.suspicious_default_item_count}\``);
  lines.push(`- Carrier modified in place: \`${readback.source_integrity.carrier_modified_in_place}\``);
  lines.push('');
  lines.push('## Item Table');
  lines.push('');
  lines.push('| item | type | layer | x/y | geometry | opacity | color | intended panel relation | suspicious defaults |');
  lines.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- |');
  readback.items.forEach((item) => {
    const geometry = item.item_type === 'ShapeItem'
      ? `${item.width}x${item.height}, stroke=${item.stroke_thickness}`
      : `font=${item.font_size}`;
    const color = item.item_type === 'ShapeItem' ? item.fill_color : item.text_color;
    const relation = item.expected_panel_relationship?.intended_inside_panel
      ? `inside ${item.expected_panel_relationship.expected_panel}; center=${item.expected_panel_relationship.expected_center_inside_panel}`
      : 'none';
    const suspicious = item.suspicious_default_notes.length ? item.suspicious_default_notes.join('; ') : 'none';
    lines.push(`| \`${item.display_name}\` | \`${item.item_type}\` | \`${item.layer}\` | \`${item.x}, ${item.y}\` | \`${geometry}\` | \`${item.opacity}\` | \`${color}\` | ${relation} | ${suspicious} |`);
  });
  lines.push('');
  lines.push('## 7. What should the user inspect in YMM4?');
  lines.push('');
  lines.push('- Open the probe and check whether the light-stage background, large blue panel, panel title/body, three anchor markers, and connector are visible without toggling backgrounds.');
  lines.push('- Confirm whether title/body text visually belongs to the panel rather than floating independently.');
  lines.push('- Confirm whether `Center Marker`, `TL Marker`, and `BR Marker` align with the intended panel center/corners.');
  lines.push('- Confirm whether timeline item labels are manageable: `BG`, `Main Panel`, `Panel Title`, `Panel Body`, `Center Marker`, `TL Marker`, `BR Marker`, `Connector`.');
  lines.push('');
  lines.push('## 8. What screenshot angles or selected item properties should the user return?');
  lines.push('');
  lines.push('- Preview screenshot of the full calibration frame.');
  lines.push('- Screenshot of one selected panel item property, preferably `Main Panel`, including X/Y, opacity, Width/Height, StrokeThickness, and color.');
  lines.push('- Screenshot of one selected text item property, preferably `Panel Title`, including X/Y, font size, opacity, and color.');
  lines.push('- If a marker is off, include a screenshot with the relevant marker selected so coordinate/anchor behavior can be inferred.');
  lines.push('');
  lines.push('## Completion Position');
  lines.push('');
  lines.push('- Calibration probe is ready for user-side GUI inspection only.');
  lines.push('- Existing micro scene work is not advanced in this slice.');
  lines.push('- Minimal render smoke remains blocked until this calibration passes in YMM4 GUI review.');
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback, markdown = null) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (!readback.boundary.calibration_only || !readback.boundary.not_video_scene) failures.push('boundary is not calibration-only');
  if (!readback.boundary.shape_item_text_item_only) failures.push('item boundary is not ShapeItem/TextItem only');
  if (readback.boundary.black_white_background_mix) failures.push('mixed background tonal logic detected');
  if (readback.boundary.render_performed) failures.push('render performed');
  if (readback.totals.item_count !== readback.totals.expected_item_count) failures.push('item count mismatch');
  if (readback.totals.item_count > 12) failures.push('item count too high for minimal calibration');
  if (readback.totals.missing_item_count !== 0) failures.push('missing items present');
  if (readback.totals.malformed_item_count !== 0) failures.push(`malformed items present: ${JSON.stringify(readback.malformed_items.slice(0, 3))}`);
  if (readback.totals.item_name_length_failures !== 0) failures.push('item name length failures present');
  if (readback.totals.remark_length_failures !== 0) failures.push('remark length failures present');
  if (readback.totals.suspicious_default_item_count !== 0) failures.push('suspicious defaults present');
  if (readback.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  const panel = readback.items.find((item) => item.display_name === 'Main Panel');
  if (!panel) failures.push('Main Panel missing from readback');
  if (panel && (panel.width < 800 || panel.width > 1000 || panel.height < 450 || panel.height > 650)) {
    failures.push('Main Panel geometry outside required range');
  }
  for (const textItem of readback.items.filter((item) => item.item_type === 'TextItem')) {
    if (textItem.intended_inside_panel && !textItem.expected_panel_relationship?.expected_center_inside_panel) {
      failures.push(`${textItem.display_name} center is not expected inside panel`);
    }
    if (textItem.color_contrast_notes && !textItem.color_contrast_notes.pass_for_intended_background) {
      failures.push(`${textItem.display_name} contrast failed`);
    }
  }
  if (markdown) {
    const requiredHeadings = [
      '## 1. What exactly is being calibrated?',
      '## 2. Which assumptions from the failed micro scene are being tested?',
      '## 3. Does the probe intentionally test coordinate / anchor behavior?',
      '## 4. Does the probe intentionally test panel-contained text?',
      '## 5. Does the probe intentionally test high-contrast visibility?',
      '## 6. Does the probe keep provenance out of YMM4 item names / Remarks?',
      '## 7. What should the user inspect in YMM4?',
      '## 8. What screenshot angles or selected item properties should the user return?',
    ];
    for (const heading of requiredHeadings) {
      if (!markdown.includes(heading)) failures.push(`report missing heading: ${heading}`);
    }
  }
  if (failures.length) throw new Error(`G27_PRIMITIVE_VISIBILITY_CALIBRATION_FAILED: ${failures.join('; ')}`);
}

function main() {
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplateYmmp = readJson(paths.shapeTemplateYmmp);
  const generatedProject = buildProbeProject(carrierYmmp, shapeTemplateYmmp);
  const generatedReadback = readbackProbe(generatedProject, carrierHashBefore, sha256(paths.carrierYmmp));
  const generatedReport = renderMarkdown(generatedReadback);
  assertReadback(generatedReadback, generatedReport);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generatedProject);
    const writtenProject = readJson(paths.outputYmmp);
    const writtenReadback = readbackProbe(writtenProject, carrierHashBefore, sha256(paths.carrierYmmp));
    const writtenReport = renderMarkdown(writtenReadback);
    assertReadback(writtenReadback, writtenReport);
    writeJson(paths.readbackJson, writtenReadback);
    writeMarkdown(paths.reportMd, writtenReport);
  } else {
    if (!fs.existsSync(abs(paths.outputYmmp))) {
      throw new Error(`OUTPUT_YMMP_MISSING: run with --write first (${paths.outputYmmp})`);
    }
    const existingProject = readJson(paths.outputYmmp);
    const existingReadback = readJson(paths.readbackJson);
    const actualReadback = readbackProbe(existingProject, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(actualReadback);
    assertReadback(existingReadback, fs.existsSync(abs(paths.reportMd)) ? readText(paths.reportMd) : null);
    if (JSON.stringify(actualReadback) !== JSON.stringify(existingReadback)) {
      throw new Error('READBACK_DRIFT: existing calibration readback JSON does not match probe .ymmp');
    }
  }

  console.log('G-27 primitive visibility calibration probe OK: 11 items, ShapeItem/TextItem only, no render');
}

main();

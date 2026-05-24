// Layout Instruction Compliance Proof — verify that a natural-language layout
// instruction set ("16:9, 上部タイトル帯, 中央 2x2 grid, 左右下キャラ bust placeholder,
// 下部 20% caption safe area, 最小限の領域ラベル") converts to a stable YMM4 layout.
// This is NOT a scene; it is a slot/region proof. ShapeItem + TextItem only.
// No external assets, no render, no creative acceptance.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const fps = 60;

const paths = {
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/layout_instruction_proof.ymmp',
  readbackJson: 'samples/_probe/g24/layout_instruction_proof_readback.json',
  reportMd: 'samples/_probe/g24/layout_instruction_proof_report.md',
};

const shapeSizeMode = 'WidthHeight';
const hexColorPattern = /^#[0-9A-Fa-f]{8}$/;
const maxDisplayNameLength = 48;
const maxRemarkLength = 80;

// =====================================================================
// SPEC — fixed by user instruction
// =====================================================================
const SPEC = {
  canvas: { width: 1920, height: 1080 },
  outer_safe_margin_pct: 5,
  title_band: {
    cy: -443,
    height: 86,
    cx: 0,
    max_chars_assumption: 18,
    font_size: 64,
  },
  grid_2x2: {
    overall_cx: 0,
    overall_cy: -200,
    overall_width: 1728,
    overall_height: 400,
    rows: 2,
    cols: 2,
    gap_px: 16,
  },
  caption_safe_area: {
    height_pct: 20,
    height_px: 216,
    cy_top: 324,
    cy_bottom: 540,
  },
  character_a: {
    side: 'left',
    cx: -700,
    head: { cy: 70, w: 140, h: 160, round: 70 },
    shoulders: { cy: 210, w: 280, h: 100, round: 20 },
    color: '#FF5B7A99',
  },
  character_b: {
    side: 'right',
    cx: 700,
    head: { cy: 70, w: 140, h: 160, round: 70 },
    shoulders: { cy: 210, w: 280, h: 100, round: 20 },
    color: '#FF99765B',
  },
};

// =====================================================================
// Derived layout
// =====================================================================
function computeGridCells() {
  const g = SPEC.grid_2x2;
  const cell_w = (g.overall_width - g.gap_px * (g.cols - 1)) / g.cols;
  const cell_h = (g.overall_height - g.gap_px * (g.rows - 1)) / g.rows;
  const left_edge = g.overall_cx - g.overall_width / 2;
  const top_edge = g.overall_cy - g.overall_height / 2;
  const cells = [];
  for (let r = 0; r < g.rows; r += 1) {
    for (let c = 0; c < g.cols; c += 1) {
      const cx = left_edge + cell_w / 2 + c * (cell_w + g.gap_px);
      const cy = top_edge + cell_h / 2 + r * (cell_h + g.gap_px);
      cells.push({ row: r, col: c, cx, cy, w: cell_w, h: cell_h });
    }
  }
  return cells;
}
const GRID_CELLS = computeGridCells();

// Cell fill colors alternate so the 2x2 boundary is visible without strokes.
const CELL_COLORS = ['#FFE7ECF1', '#FFCFD8E0', '#FFCFD8E0', '#FFE7ECF1'];

// Title text — chosen short, but slot width must accommodate max 18 chars.
const TITLE_TEXT = 'レイアウト指示遵守の検証';
const TITLE_TEXT_LENGTH = [...TITLE_TEXT].length; // 12 codepoints
// Slot width design: 18 chars * font 64 * 0.62 ≈ 715 px
const TITLE_SLOT_WIDTH_DESIGN = Math.ceil(SPEC.title_band.max_chars_assumption * SPEC.title_band.font_size * 0.62);

// =====================================================================
// Layout items
// =====================================================================
const layoutItems = [
  // 1. BG
  shape('LIP_BG', 'background', 1, 0, 0, 1920, 1080, '#FFF5F7FA', 100, 0, 1080, false, 'full-screen light-stage background'),

  // 2. Title band background
  shape('LIP_TitleBandBG', 'title_band', 2, SPEC.title_band.cx, SPEC.title_band.cy, 1728, SPEC.title_band.height, '#FFE0E7EF', 100, 8, SPEC.title_band.height, false, 'title band background strip'),

  // 3. Title text (slot designed for 18 chars max)
  text('LIP_Title', 'title_text', 3, SPEC.title_band.cx, SPEC.title_band.cy, SPEC.title_band.font_size, TITLE_TEXT, '#FF1A2B3C', false, `title text (current ${TITLE_TEXT_LENGTH} chars; slot designed for ${SPEC.title_band.max_chars_assumption} chars / ${TITLE_SLOT_WIDTH_DESIGN}px wide)`),

  // 4-7. 2x2 grid cells
  ...GRID_CELLS.map((cell, idx) => shape(
    `LIP_GridCell_${cell.row}_${cell.col}`,
    'grid_cell',
    4,
    cell.cx,
    cell.cy,
    cell.w,
    cell.h,
    CELL_COLORS[idx],
    100,
    8,
    cell.h,
    false,
    `grid cell row=${cell.row} col=${cell.col} (boundary visible via gap=${SPEC.grid_2x2.gap_px}px + alternating fill)`,
  )),

  // 8. Character A head (ellipse via large round)
  shape('LIP_CharA_Head', 'character_bust', 5, SPEC.character_a.cx, SPEC.character_a.head.cy, SPEC.character_a.head.w, SPEC.character_a.head.h, SPEC.character_a.color, 100, SPEC.character_a.head.round, SPEC.character_a.head.h, false, 'character A head (left-bottom bust placeholder)'),

  // 9. Character A shoulders (rounded rect, bust-up)
  shape('LIP_CharA_Shoulders', 'character_bust', 5, SPEC.character_a.cx, SPEC.character_a.shoulders.cy, SPEC.character_a.shoulders.w, SPEC.character_a.shoulders.h, SPEC.character_a.color, 100, SPEC.character_a.shoulders.round, SPEC.character_a.shoulders.h, false, 'character A shoulders (bust cut at shoulder line)'),

  // 10. Character B head
  shape('LIP_CharB_Head', 'character_bust', 5, SPEC.character_b.cx, SPEC.character_b.head.cy, SPEC.character_b.head.w, SPEC.character_b.head.h, SPEC.character_b.color, 100, SPEC.character_b.head.round, SPEC.character_b.head.h, false, 'character B head (right-bottom bust placeholder)'),

  // 11. Character B shoulders
  shape('LIP_CharB_Shoulders', 'character_bust', 5, SPEC.character_b.cx, SPEC.character_b.shoulders.cy, SPEC.character_b.shoulders.w, SPEC.character_b.shoulders.h, SPEC.character_b.color, 100, SPEC.character_b.shoulders.round, SPEC.character_b.shoulders.h, false, 'character B shoulders (bust cut at shoulder line)'),

  // 12. Caption safe area indicator (thin line at top edge of caption safe area)
  shape('LIP_CaptionSafeIndicator', 'caption_safe_indicator', 6, 0, SPEC.caption_safe_area.cy_top, 1728, 4, '#FFAAB3BD', 100, 2, 4, false, 'thin line marking the top edge of the bottom 20% caption safe area (area itself is empty)'),

  // 13-17. Minimal region labels
  text('LIP_Label_Title', 'region_label', 7, -800, -480, 22, '[title band]', '#FF6B7280', false, 'region label: title band'),
  text('LIP_Label_Grid', 'region_label', 7, -800, -400, 22, '[grid 2x2]', '#FF6B7280', false, 'region label: 2x2 grid'),
  text('LIP_Label_CharA', 'region_label', 7, -800, -20, 22, '[character A bust]', '#FF6B7280', false, 'region label: character A area'),
  text('LIP_Label_CharB', 'region_label', 7, 800, -20, 22, '[character B bust]', '#FF6B7280', false, 'region label: character B area'),
  text('LIP_Label_Caption', 'region_label', 7, 0, 310, 22, '[caption safe area / empty]', '#FF6B7280', false, 'region label: caption safe area top edge'),
];

// =====================================================================
// Item builders
// =====================================================================
function shape(displayName, role, layer, x, y, width, height, color, opacity, round, strokeThickness, isHidden, description) {
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
    is_hidden: Boolean(isHidden),
    description,
  };
}

function text(displayName, role, layer, x, y, fontSize, content, color, isHidden, description) {
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
    is_hidden: Boolean(isHidden),
    description,
  };
}

// =====================================================================
// File helpers
// =====================================================================
function abs(rel) { return path.join(root, rel); }
function readText(rel) { return fs.readFileSync(abs(rel), 'utf8').replace(/^﻿/, ''); }
function readJson(rel) { return JSON.parse(readText(rel)); }
function writeJson(rel, payload) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}
function writeMarkdown(rel, md) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), md, 'utf8');
}
function writeYmmp(rel, payload) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), `﻿${JSON.stringify(payload, null, 2)}`, 'utf8');
}
function sha256(rel) { return crypto.createHash('sha256').update(fs.readFileSync(abs(rel))).digest('hex'); }
function clone(v) { return JSON.parse(JSON.stringify(v)); }

// =====================================================================
// YMM4 item construction (copy of patterns proven in build_g27_diagnostic_carrier.js)
// =====================================================================
function animation(value) {
  return {
    Values: [{ Value: value }],
    Span: 0,
    AnimationType: 'なし',
    Bezier: {
      Points: [
        { Point: { X: 0, Y: 0 }, ControlPoint1: { X: -0.3, Y: -0.3 }, ControlPoint2: { X: 0.3, Y: 0.3 } },
        { Point: { X: 1, Y: 1 }, ControlPoint1: { X: -0.3, Y: -0.3 }, ControlPoint2: { X: 0.3, Y: 0.3 } },
      ],
      IsQuadratic: false,
    },
  };
}
function itemType(item) { return String(item?.$type || '').split(',')[0].split('.').pop(); }
function findFirstItemByType(ymmp, typeName) {
  const timelines = Array.isArray(ymmp.Timelines) ? ymmp.Timelines : [];
  for (const tl of timelines) {
    const items = Array.isArray(tl.Items) ? tl.Items : [];
    const found = items.find((it) => itemType(it) === typeName);
    if (found) return found;
  }
  return null;
}
function setAnimatedValue(item, key, value) {
  if (!item[key] || typeof item[key] !== 'object') { item[key] = animation(value); return; }
  if (!Array.isArray(item[key].Values) || item[key].Values.length === 0) { item[key].Values = [{ Value: value }]; return; }
  item[key].Values[0].Value = value;
}
function setShapeParameterValue(shapeItem, key, value) {
  if (!shapeItem.ShapeParameter || typeof shapeItem.ShapeParameter !== 'object') shapeItem.ShapeParameter = {};
  const t = shapeItem.ShapeParameter[key];
  if (!t || typeof t !== 'object') { shapeItem.ShapeParameter[key] = animation(value); return; }
  if (!Array.isArray(t.Values) || t.Values.length === 0) { t.Values = [{ Value: value }]; return; }
  t.Values[0].Value = value;
}
function setShapeBrushColor(shapeItem, color) {
  const brush = shapeItem.ShapeParameter?.Brush;
  if (!brush?.Parameter || typeof brush.Parameter !== 'object') throw new Error('SHAPE_BRUSH_PARAMETER_MISSING');
  brush.Parameter.Color = color;
}
function setShapeGeometry(shapeItem, p) {
  shapeItem.ShapeParameter.SizeMode = shapeSizeMode;
  setShapeParameterValue(shapeItem, 'Size', Math.max(p.width, p.height));
  setShapeParameterValue(shapeItem, 'AspectRate', p.width / p.height);
  setShapeParameterValue(shapeItem, 'Width', p.width);
  setShapeParameterValue(shapeItem, 'Height', p.height);
  setShapeParameterValue(shapeItem, 'Round', p.round);
  setShapeParameterValue(shapeItem, 'StrokeThickness', p.stroke_thickness);
}
const DURATION_FRAMES = 600;
function makeShapeItem(template, p) {
  const it = clone(template);
  it.Frame = 0;
  it.Length = DURATION_FRAMES;
  it.Layer = p.layer;
  it.Group = 0;
  it.KeyFrames = { Frames: [], Count: 0 };
  it.Remark = p.display_name;
  it.IsLocked = false;
  it.IsHidden = Boolean(p.is_hidden);
  setAnimatedValue(it, 'X', p.x);
  setAnimatedValue(it, 'Y', p.y);
  setAnimatedValue(it, 'Z', 0);
  setAnimatedValue(it, 'Opacity', p.opacity);
  setAnimatedValue(it, 'Zoom', 100);
  setAnimatedValue(it, 'Rotation', 0);
  setShapeGeometry(it, p);
  setShapeBrushColor(it, p.color);
  return it;
}
function makeTextItem(p) {
  return {
    $type: 'YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker',
    Text: p.content,
    Font: 'Yu Gothic UI',
    FontSize: animation(p.font_size),
    FontColor: p.color,
    Style: 'Normal',
    X: animation(p.x),
    Y: animation(p.y),
    Z: animation(0),
    Opacity: animation(p.opacity),
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
    Layer: p.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: DURATION_FRAMES,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: p.display_name,
    IsLocked: false,
    IsHidden: Boolean(p.is_hidden),
  };
}

// =====================================================================
// Build project
// =====================================================================
function validateLayoutDesign() {
  const errors = [];
  for (const it of layoutItems) {
    if (!['ShapeItem', 'TextItem'].includes(it.kind)) errors.push(`${it.display_name} unsupported kind`);
    if (it.display_name.length > maxDisplayNameLength) errors.push(`${it.display_name} display name too long`);
    if (!String(it.display_name).startsWith('LIP_')) errors.push(`${it.display_name} must start with LIP_`);
    if (it.kind === 'ShapeItem') {
      if (it.width <= 0 || it.height <= 0) errors.push(`${it.display_name} invalid geometry`);
      if (!hexColorPattern.test(it.color)) errors.push(`${it.display_name} color is not #AARRGGBB`);
    }
    if (it.kind === 'TextItem') {
      if (it.font_size < 18) errors.push(`${it.display_name} font size too small`);
      if (!hexColorPattern.test(it.color)) errors.push(`${it.display_name} text color is not #AARRGGBB`);
    }
  }
  // 4 grid cells expected
  const gridCount = layoutItems.filter((it) => it.role === 'grid_cell').length;
  if (gridCount !== 4) errors.push(`expected 4 grid cells, got ${gridCount}`);
  // 2 character bust placeholders, each with head+shoulders => 4 items
  const bustCount = layoutItems.filter((it) => it.role === 'character_bust').length;
  if (bustCount !== 4) errors.push(`expected 4 character bust items (2 chars × head+shoulders), got ${bustCount}`);
  if (errors.length) throw new Error(`LAYOUT_DESIGN_INVALID: ${errors.join('; ')}`);
}

function buildProject(carrierYmmp, shapeTemplateYmmp) {
  validateLayoutDesign();
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) throw new Error(`SHAPE_TEMPLATE_MISSING: ${paths.shapeTemplateYmmp}`);
  const project = clone(carrierYmmp);
  const timeline = project.Timelines?.[0];
  if (!timeline || !Array.isArray(project.Timelines)) throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  const items = layoutItems.map((p) => {
    if (p.kind === 'ShapeItem') return makeShapeItem(shapeTemplate, p);
    if (p.kind === 'TextItem') return makeTextItem(p);
    throw new Error(`UNSUPPORTED_KIND: ${p.kind}`);
  });
  timeline.Items = items;
  timeline.CurrentFrame = 0;
  timeline.Length = DURATION_FRAMES;
  timeline.MaxLayer = Math.max(...items.map((it) => it.Layer), 0);
  if (!timeline.LayerSettings || Array.isArray(timeline.LayerSettings)) {
    timeline.LayerSettings = { Items: Array.isArray(timeline.LayerSettings) ? timeline.LayerSettings : [] };
  }
  project.FilePath = abs(paths.outputYmmp);
  return project;
}

// =====================================================================
// Readback
// =====================================================================
function animationValue(item, key) { return item?.[key]?.Values?.[0]?.Value; }
function shapeParameterValue(item, key) { return item?.ShapeParameter?.[key]?.Values?.[0]?.Value; }

function readbackItem(item, primitive) {
  const displayName = String(item.Remark || '');
  const type = itemType(item);
  const isShape = type === 'ShapeItem';
  const isText = type === 'TextItem';
  return {
    display_name: displayName,
    role: primitive?.role || null,
    item_type: type,
    layer: item.Layer,
    is_hidden: Boolean(item.IsHidden),
    x: animationValue(item, 'X') ?? null,
    y: animationValue(item, 'Y') ?? null,
    width: isShape ? shapeParameterValue(item, 'Width') ?? null : null,
    height: isShape ? shapeParameterValue(item, 'Height') ?? null : null,
    shape_size_mode: isShape ? item.ShapeParameter?.SizeMode || null : null,
    stroke_thickness: isShape ? shapeParameterValue(item, 'StrokeThickness') ?? null : null,
    round: isShape ? shapeParameterValue(item, 'Round') ?? null : null,
    opacity: animationValue(item, 'Opacity') ?? null,
    fill_color: isShape ? item.ShapeParameter?.Brush?.Parameter?.Color || null : null,
    text_color: isText ? item.FontColor : null,
    text: isText ? item.Text : null,
    font_size: isText ? item.FontSize?.Values?.[0]?.Value ?? null : null,
    description: primitive?.description || null,
  };
}

function complianceFromItems(items) {
  const violations = [];

  const titleText = items.find((it) => it.display_name === 'LIP_Title');
  const titleBand = items.find((it) => it.display_name === 'LIP_TitleBandBG');
  const gridCells = items.filter((it) => it.role === 'grid_cell');
  const charAItems = items.filter((it) => it.display_name.startsWith('LIP_CharA_'));
  const charBItems = items.filter((it) => it.display_name.startsWith('LIP_CharB_'));
  const captionIndicator = items.find((it) => it.role === 'caption_safe_indicator');
  const regionLabels = items.filter((it) => it.role === 'region_label');

  // 16:9 / 1920x1080 — implicit, verified by canvas constants in SPEC
  const canvas_check = (SPEC.canvas.width === 1920 && SPEC.canvas.height === 1080) ? 'pass' : 'fail';

  // Title band check: located in upper area (cy < -350)
  const title_band_check = (titleBand && titleBand.y < -350) ? 'pass' : 'fail';
  if (title_band_check !== 'pass') violations.push({ rule: 'TITLE_BAND_POSITION', severity: 'fail' });

  // Title max-chars assumption
  const title_slot_width_required = Math.ceil(SPEC.title_band.max_chars_assumption * SPEC.title_band.font_size * 0.62);
  const title_band_width = titleBand?.width ?? 0;
  const title_slot_width_ok = title_band_width >= title_slot_width_required;
  if (!title_slot_width_ok) violations.push({ rule: 'TITLE_SLOT_WIDTH_INSUFFICIENT_FOR_MAX_CHARS', severity: 'fail', required_px: title_slot_width_required, actual_px: title_band_width });

  // Grid 2x2 check: 4 cells with boundary visible (alternate fill colors or gap)
  const grid_2x2_check = gridCells.length === 4 ? 'pass' : 'fail';
  if (grid_2x2_check !== 'pass') violations.push({ rule: 'GRID_2X2_CELL_COUNT', severity: 'fail', actual: gridCells.length });
  const cell_fills = gridCells.map((c) => c.fill_color);
  const grid_boundary_visible = (() => {
    if (gridCells.length !== 4) return false;
    // adjacent cells must differ in color (gap_px also provides separation)
    const byRC = (r, c) => gridCells.find((x) => x.display_name === `LIP_GridCell_${r}_${c}`);
    const a = byRC(0, 0); const b = byRC(0, 1); const c = byRC(1, 0); const d = byRC(1, 1);
    if (!a || !b || !c || !d) return false;
    return a.fill_color !== b.fill_color && a.fill_color !== c.fill_color && d.fill_color !== b.fill_color && d.fill_color !== c.fill_color;
  })();
  if (!grid_boundary_visible) violations.push({ rule: 'GRID_BOUNDARY_NOT_VISIBLE', severity: 'fail' });

  // Character A & B bust check: each has head + shoulders, located in lower-left / lower-right
  const charA_bust_check = (charAItems.length === 2 && charAItems.every((it) => it.x < -300)) ? 'pass' : 'fail';
  const charB_bust_check = (charBItems.length === 2 && charBItems.every((it) => it.x > 300)) ? 'pass' : 'fail';
  if (charA_bust_check !== 'pass') violations.push({ rule: 'CHAR_A_BUST_PLACEMENT', severity: 'fail' });
  if (charB_bust_check !== 'pass') violations.push({ rule: 'CHAR_B_BUST_PLACEMENT', severity: 'fail' });

  // Bust-up (shoulders-up): no items extend below cy=300 inside the character region (other than caption indicator)
  const max_char_bottom_a = Math.max(...charAItems.map((it) => (it.y ?? 0) + (it.height ?? 0) / 2));
  const max_char_bottom_b = Math.max(...charBItems.map((it) => (it.y ?? 0) + (it.height ?? 0) / 2));
  const bust_up_check = (max_char_bottom_a <= SPEC.caption_safe_area.cy_top && max_char_bottom_b <= SPEC.caption_safe_area.cy_top) ? 'pass' : 'fail';
  if (bust_up_check !== 'pass') violations.push({ rule: 'CHAR_INTRUDES_CAPTION_SAFE_AREA', severity: 'fail', max_char_bottom_a, max_char_bottom_b, caption_top: SPEC.caption_safe_area.cy_top });

  // Caption safe area check: no major item (role != region_label && role != caption_safe_indicator) crosses cy=324..540
  const major_items = items.filter((it) => !['region_label', 'caption_safe_indicator', 'background'].includes(it.role));
  const safe_area_violators = major_items.filter((it) => {
    const bottom = (it.y ?? 0) + (it.height || (it.font_size ? it.font_size * 1.3 : 0)) / 2;
    const top = (it.y ?? 0) - (it.height || (it.font_size ? it.font_size * 1.3 : 0)) / 2;
    return bottom > SPEC.caption_safe_area.cy_top && top < SPEC.caption_safe_area.cy_bottom;
  });
  const caption_safe_area_check = safe_area_violators.length === 0 ? 'pass' : 'fail';
  if (caption_safe_area_check !== 'pass') violations.push({ rule: 'MAJOR_ITEM_IN_CAPTION_SAFE_AREA', severity: 'fail', offenders: safe_area_violators.map((it) => it.display_name) });

  // Region labels: at least 4 (title, grid, character_a or character_b, caption)
  const region_label_check = regionLabels.length >= 4 ? 'pass' : 'fail';
  if (region_label_check !== 'pass') violations.push({ rule: 'INSUFFICIENT_REGION_LABELS', severity: 'fail', actual: regionLabels.length });

  // Caption indicator present
  const caption_indicator_check = captionIndicator ? 'pass' : 'fail';
  if (caption_indicator_check !== 'pass') violations.push({ rule: 'CAPTION_INDICATOR_MISSING', severity: 'fail' });

  // ShapeItem SizeMode
  const shape_size_mode_violators = items.filter((it) => it.item_type === 'ShapeItem' && it.shape_size_mode !== shapeSizeMode);
  const shape_size_mode_check = shape_size_mode_violators.length === 0 ? 'pass' : 'fail';
  if (shape_size_mode_check !== 'pass') violations.push({ rule: 'SHAPE_SIZE_MODE_NOT_WIDTHHEIGHT', severity: 'fail', offenders: shape_size_mode_violators.map((it) => it.display_name) });

  // Color format
  const color_violators = items.filter((it) => {
    if (it.item_type === 'ShapeItem') return !hexColorPattern.test(it.fill_color || '');
    if (it.item_type === 'TextItem') return !hexColorPattern.test(it.text_color || '');
    return false;
  });
  const color_format_check = color_violators.length === 0 ? 'pass' : 'fail';
  if (color_format_check !== 'pass') violations.push({ rule: 'COLOR_FORMAT_NOT_AARRGGBB', severity: 'fail', offenders: color_violators.map((it) => it.display_name) });

  // 16:9 canvas (constant, but report)
  if (canvas_check !== 'pass') violations.push({ rule: 'CANVAS_NOT_16_9_1920_1080', severity: 'fail' });

  return {
    instruction_compliance: {
      canvas_16_9_1920_1080: canvas_check,
      title_band_top: title_band_check,
      title_slot_width_for_18_chars: title_slot_width_ok ? 'pass' : 'fail',
      grid_2x2_cells: grid_2x2_check,
      grid_boundary_visible: grid_boundary_visible ? 'pass' : 'fail',
      char_a_bust_left_bottom: charA_bust_check,
      char_b_bust_right_bottom: charB_bust_check,
      bust_up_no_intrusion_into_caption_safe: bust_up_check,
      caption_safe_area_empty_of_major_items: caption_safe_area_check,
      region_labels_present: region_label_check,
      caption_indicator_present: caption_indicator_check,
      shape_size_mode_widthheight: shape_size_mode_check,
      color_format_aarrggbb: color_format_check,
    },
    title_slot: {
      cx: SPEC.title_band.cx,
      cy: SPEC.title_band.cy,
      band_width: titleBand?.width ?? null,
      band_height: titleBand?.height ?? null,
      font_size: titleText?.font_size ?? null,
      current_text: titleText?.text ?? null,
      current_chars: titleText?.text ? [...titleText.text].length : 0,
      max_chars_assumption: SPEC.title_band.max_chars_assumption,
      slot_width_required_for_max_chars_px: title_slot_width_required,
    },
    grid_2x2_slots: gridCells.map((c) => ({
      id: c.display_name,
      role: c.role,
      row: Number(c.display_name.split('_')[2]),
      col: Number(c.display_name.split('_')[3]),
      cx: c.x,
      cy: c.y,
      width: c.width,
      height: c.height,
      fill_color: c.fill_color,
    })),
    character_slots: {
      A: {
        side: SPEC.character_a.side,
        cx: SPEC.character_a.cx,
        head: charAItems.find((it) => it.display_name.endsWith('_Head')) ? {
          cx: charAItems.find((it) => it.display_name.endsWith('_Head')).x,
          cy: charAItems.find((it) => it.display_name.endsWith('_Head')).y,
          w: charAItems.find((it) => it.display_name.endsWith('_Head')).width,
          h: charAItems.find((it) => it.display_name.endsWith('_Head')).height,
        } : null,
        shoulders: charAItems.find((it) => it.display_name.endsWith('_Shoulders')) ? {
          cx: charAItems.find((it) => it.display_name.endsWith('_Shoulders')).x,
          cy: charAItems.find((it) => it.display_name.endsWith('_Shoulders')).y,
          w: charAItems.find((it) => it.display_name.endsWith('_Shoulders')).width,
          h: charAItems.find((it) => it.display_name.endsWith('_Shoulders')).height,
        } : null,
      },
      B: {
        side: SPEC.character_b.side,
        cx: SPEC.character_b.cx,
        head: charBItems.find((it) => it.display_name.endsWith('_Head')) ? {
          cx: charBItems.find((it) => it.display_name.endsWith('_Head')).x,
          cy: charBItems.find((it) => it.display_name.endsWith('_Head')).y,
          w: charBItems.find((it) => it.display_name.endsWith('_Head')).width,
          h: charBItems.find((it) => it.display_name.endsWith('_Head')).height,
        } : null,
        shoulders: charBItems.find((it) => it.display_name.endsWith('_Shoulders')) ? {
          cx: charBItems.find((it) => it.display_name.endsWith('_Shoulders')).x,
          cy: charBItems.find((it) => it.display_name.endsWith('_Shoulders')).y,
          w: charBItems.find((it) => it.display_name.endsWith('_Shoulders')).width,
          h: charBItems.find((it) => it.display_name.endsWith('_Shoulders')).height,
        } : null,
      },
    },
    caption_safe_area: {
      cy_top: SPEC.caption_safe_area.cy_top,
      cy_bottom: SPEC.caption_safe_area.cy_bottom,
      height_px: SPEC.caption_safe_area.height_px,
      height_pct: SPEC.caption_safe_area.height_pct,
      indicator_present: caption_indicator_check === 'pass',
    },
    region_labels: regionLabels.map((it) => ({ name: it.display_name, text: it.text, cx: it.x, cy: it.y })),
    violations,
  };
}

function readbackProbe(ymmp, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const items = timelineItems.map((it) => {
    const displayName = String(it.Remark || '');
    const p = layoutItems.find((x) => x.display_name === displayName);
    return readbackItem(it, p);
  });
  const missing = layoutItems.filter((p) => !items.find((it) => it.display_name === p.display_name)).map((p) => p.display_name);

  const compliance = complianceFromItems(items);
  const hardFails = compliance.violations.filter((v) => v.severity === 'fail');
  const status = missing.length === 0 && hardFails.length === 0 ? 'passed' : 'failed';

  return {
    artifact_type: 'g27_layout_instruction_proof_readback',
    status,
    source: {
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_proof_ymmp: paths.outputYmmp,
    },
    boundary: {
      diagnostic_only: true,
      layout_proof_only: true,
      scene_composition: false,
      external_assets_used: false,
      render_performed: false,
      creative_acceptance_performed: false,
      production_readiness_claimed: false,
    },
    spec: SPEC,
    totals: {
      item_count: items.length,
      expected_item_count: layoutItems.length,
      shape_item_count: items.filter((it) => it.item_type === 'ShapeItem').length,
      text_item_count: items.filter((it) => it.item_type === 'TextItem').length,
      missing_item_count: missing.length,
      hard_failure_count: hardFails.length,
      violation_count: compliance.violations.length,
    },
    layout_compliance: compliance,
    source_integrity: {
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    items,
    missing_items: missing,
  };
}

// =====================================================================
// Report
// =====================================================================
function renderReport(rb) {
  const c = rb.layout_compliance;
  const lines = [];
  lines.push('# G-27 Layout Instruction Compliance Proof');
  lines.push('');
  lines.push(`Artifact: \`${rb.source.generated_proof_ymmp}\``);
  lines.push('');
  lines.push('Diagnostic-only layout proof. Not a scene composition, not a render, not creative acceptance.');
  lines.push('');
  lines.push('## Instruction Compliance Rollup');
  lines.push('');
  for (const [k, v] of Object.entries(c.instruction_compliance)) {
    lines.push(`- \`${k}\`: \`${v}\``);
  }
  lines.push('');
  lines.push('## Title Slot');
  lines.push('');
  const t = c.title_slot;
  lines.push(`- center: cx=${t.cx}, cy=${t.cy}`);
  lines.push(`- band size: ${t.band_width}x${t.band_height}`);
  lines.push(`- font size: ${t.font_size}`);
  lines.push(`- current text: "${t.current_text}" (${t.current_chars} chars)`);
  lines.push(`- max chars assumption: ${t.max_chars_assumption}`);
  lines.push(`- slot width required for ${t.max_chars_assumption} chars: ${t.slot_width_required_for_max_chars_px}px`);
  lines.push('');
  lines.push('## Grid 2x2 Slots');
  lines.push('');
  lines.push('| id | row | col | cx | cy | width | height | fill |');
  lines.push('| --- | --- | --- | --- | --- | --- | --- | --- |');
  for (const s of c.grid_2x2_slots) {
    lines.push(`| \`${s.id}\` | ${s.row} | ${s.col} | ${s.cx} | ${s.cy} | ${s.width} | ${s.height} | \`${s.fill_color}\` |`);
  }
  lines.push('');
  lines.push('## Character Placeholder Slots');
  lines.push('');
  for (const key of ['A', 'B']) {
    const ch = c.character_slots[key];
    lines.push(`### Character ${key} (${ch.side})`);
    lines.push('');
    lines.push(`- cx (center): ${ch.cx}`);
    if (ch.head) lines.push(`- head: cx=${ch.head.cx}, cy=${ch.head.cy}, w=${ch.head.w}, h=${ch.head.h}`);
    if (ch.shoulders) lines.push(`- shoulders: cx=${ch.shoulders.cx}, cy=${ch.shoulders.cy}, w=${ch.shoulders.w}, h=${ch.shoulders.h}`);
    lines.push('');
  }
  lines.push('## Caption Safe Area');
  lines.push('');
  const cs = c.caption_safe_area;
  lines.push(`- cy range: ${cs.cy_top}..${cs.cy_bottom}`);
  lines.push(`- height: ${cs.height_px}px (${cs.height_pct}% of 1080)`);
  lines.push(`- indicator present: ${cs.indicator_present}`);
  lines.push('');
  lines.push('## Region Labels');
  lines.push('');
  for (const l of c.region_labels) {
    lines.push(`- \`${l.name}\`: "${l.text}" at cx=${l.cx}, cy=${l.cy}`);
  }
  lines.push('');
  lines.push('## Violations');
  lines.push('');
  if (c.violations.length === 0) {
    lines.push('- (none)');
  } else {
    for (const v of c.violations) {
      lines.push(`- \`${v.rule}\` (\`${v.severity}\`): ${JSON.stringify(v).slice(0, 200)}`);
    }
  }
  lines.push('');
  lines.push('## Status');
  lines.push('');
  lines.push(`- readback status: \`${rb.status}\``);
  lines.push(`- item count: ${rb.totals.item_count} (Shape=${rb.totals.shape_item_count}, Text=${rb.totals.text_item_count})`);
  lines.push(`- carrier modified in place: \`${rb.source_integrity.carrier_modified_in_place}\``);
  return `${lines.join('\n')}\n`;
}

function assertReadback(rb) {
  const failures = [];
  if (rb.status !== 'passed') failures.push(`status=${rb.status}`);
  if (!rb.boundary.diagnostic_only || !rb.boundary.layout_proof_only) failures.push('boundary is not layout-proof-only');
  if (rb.boundary.render_performed) failures.push('render performed');
  if (rb.boundary.creative_acceptance_performed) failures.push('creative acceptance performed');
  if (rb.totals.item_count !== rb.totals.expected_item_count) failures.push('item count mismatch');
  if (rb.totals.missing_item_count !== 0) failures.push('missing items present');
  if (rb.totals.hard_failure_count !== 0) failures.push(`hard failures: ${JSON.stringify(rb.layout_compliance.violations.filter((v) => v.severity === 'fail'))}`);
  if (rb.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  if (failures.length) throw new Error(`LAYOUT_INSTRUCTION_PROOF_FAILED: ${failures.join('; ')}`);
}

function main() {
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplate = readJson(paths.shapeTemplateYmmp);
  const generated = buildProject(carrierYmmp, shapeTemplate);
  const generatedReadback = readbackProbe(generated, carrierHashBefore, sha256(paths.carrierYmmp));
  const generatedReport = renderReport(generatedReadback);
  assertReadback(generatedReadback);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generated);
    const written = readJson(paths.outputYmmp);
    const writtenReadback = readbackProbe(written, carrierHashBefore, sha256(paths.carrierYmmp));
    const writtenReport = renderReport(writtenReadback);
    assertReadback(writtenReadback);
    writeJson(paths.readbackJson, writtenReadback);
    writeMarkdown(paths.reportMd, writtenReport);
    console.log(`Layout proof written: ${paths.outputYmmp}`);
    console.log(`Readback: ${paths.readbackJson}`);
    console.log(`Report: ${paths.reportMd}`);
    console.log(`status=${writtenReadback.status}, items=${writtenReadback.totals.item_count}, hard_fail=${writtenReadback.totals.hard_failure_count}`);
  } else {
    if (!fs.existsSync(abs(paths.outputYmmp))) throw new Error(`OUTPUT_YMMP_MISSING: run with --write first (${paths.outputYmmp})`);
    const existing = readJson(paths.outputYmmp);
    const existingReadback = readJson(paths.readbackJson);
    const actualReadback = readbackProbe(existing, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(actualReadback);
    assertReadback(existingReadback);
    if (JSON.stringify(actualReadback) !== JSON.stringify(existingReadback)) throw new Error('READBACK_DRIFT');
    console.log(`Layout proof OK (no-write check): items=${actualReadback.totals.item_count}, hard_fail=${actualReadback.totals.hard_failure_count}`);
  }
}

main();

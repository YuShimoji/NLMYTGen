const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  compactReview: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/real_estate_dx_visual_proxy_v21_probe.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_visual_proxy_v21_probe_readback.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_visual_proxy_v21_probe_report.md',
};

const expectedCandidateIds = [
  'RE-02-beginning',
  'RE-02-development',
  'RE-06-beginning',
  'RE-06-development',
  'RE-06-turn',
  'RE-07D-beginning',
  'RE-07D-development',
];

const textColor = '#FFF8FAFF';
const mutedTextColor = '#FFD8E0EE';
const warningTextColor = '#FFFFF2D0';
const colorLikeTerms = ['color', 'brush', 'background', 'border', 'fill', 'stroke', 'shadow', 'foreground'];
const hexColorPattern = /^#[0-9A-Fa-f]{8}$/;

const visualSpecs = {
  'RE-02-beginning': {
    visual_intent: 'search/database contrast with one central access split',
    proxy_v21_status: 'pass',
    rationale: 'The frame is dominated by a single access-split composition: public portal on the left, private database depth on the right, and a locked threshold between them.',
    primitives: [
      shape('scene_backplate', 7, 0, -70, 1040, 410, '#FF102030', 96, 18),
      shape('public_portal_main', 8, -315, -75, 420, 300, '#FFEAF7FF', 100, 18),
      shape('public_search_bar', 8, -315, -185, 350, 44, '#FFFFFFFF', 100, 12),
      shape('public_result_card_1', 8, -395, -95, 260, 48, '#FFCBE6FF', 100, 8),
      shape('public_result_card_2', 8, -395, -35, 210, 42, '#FFCBE6FF', 72, 8),
      shape('private_db_depth', 8, 300, -75, 420, 300, '#FF182A48', 100, 18),
      shape('private_db_inner', 8, 330, -74, 330, 220, '#FF2B4770', 90, 12),
      shape('private_db_rows', 8, 330, -112, 270, 28, '#FF82A8D8', 80, 5),
      shape('private_db_rows_2', 8, 330, -55, 270, 28, '#FF82A8D8', 62, 5),
      shape('threshold_bar', 8, 0, -75, 70, 330, '#FF060B12', 100, 10),
      shape('lock_body', 8, 0, -20, 92, 86, '#FFFFC857', 100, 14),
      shape('lock_shackle', 8, 0, -88, 72, 42, '#FFFFD98A', 100, 18),
      text('public_word', 9, -315, -235, 28, 'PUBLIC', '#FF14304A'),
      text('private_word', 9, 300, -235, 28, 'PRIVATE DB', textColor),
      text('lock_word', 9, 0, -36, 30, 'LOCK', '#FF2A1E00'),
      text('scene_caption', 9, 0, 268, 32, '公開検索では見えない情報層がある', textColor),
    ],
  },
  'RE-02-development': {
    visual_intent: 'database-to-public extraction pipeline',
    proxy_v21_status: 'pass',
    rationale: 'The frame uses a left-to-right pipeline: large private database stack, narrow extraction funnel, and a small public portal output.',
    primitives: [
      shape('pipeline_backplate', 7, 0, -70, 1040, 410, '#FF102030', 96, 18),
      shape('db_stack_base', 8, -390, -70, 390, 310, '#FF183857', 100, 18),
      shape('db_stack_layer_1', 8, -390, -160, 310, 54, '#FF5B91C6', 96, 10),
      shape('db_stack_layer_2', 8, -390, -75, 310, 54, '#FF5B91C6', 78, 10),
      shape('db_stack_layer_3', 8, -390, 10, 310, 54, '#FF5B91C6', 60, 10),
      shape('funnel_top', 8, -45, -105, 190, 76, '#FF8EE0A1', 100, 14),
      shape('funnel_neck', 8, 20, -25, 70, 150, '#FF8EE0A1', 95, 10),
      shape('portal_output', 8, 370, -70, 360, 260, '#FFEAF7FF', 100, 18),
      shape('portal_card_small', 8, 370, -105, 260, 70, '#FFFFFFFF', 100, 10),
      shape('portal_card_smaller', 8, 370, 0, 210, 56, '#FFFFFFFF', 72, 10),
      text('db_label', 9, -390, -235, 28, '業者DB', textColor),
      text('funnel_label', 9, -14, -95, 28, '抽出', '#FF122818'),
      text('portal_label', 9, 370, -205, 28, '公開ポータル', '#FF14304A'),
      text('scene_caption', 9, 0, 268, 32, '多い内部情報 → 少ない公開情報', textColor),
    ],
  },
  'RE-06-beginning': {
    visual_intent: 'property comparison board with overload pressure',
    proxy_v21_status: 'pass',
    rationale: 'A single comparison board owns the frame while excess candidate cards crowd its edges, so it reads as property comparison rather than sticky notes.',
    primitives: [
      shape('comparison_backplate', 7, 0, -70, 1040, 410, '#FF17202D', 96, 18),
      shape('main_compare_panel', 8, 0, -75, 650, 315, '#FFFFFEF4', 100, 18),
      shape('axis_price', 8, 0, -170, 560, 26, '#FF5A89C8', 100, 6),
      shape('axis_station', 8, 0, -78, 560, 26, '#FF5A89C8', 82, 6),
      shape('axis_risk', 8, 0, 14, 560, 26, '#FFFFB14A', 90, 6),
      shape('overflow_card_left_1', 8, -455, -150, 180, 84, '#FFFFFFFF', 76, 10),
      shape('overflow_card_left_2', 8, -455, -35, 180, 84, '#FFFFFFFF', 56, 10),
      shape('overflow_card_right_1', 8, 455, -150, 180, 84, '#FFFFFFFF', 76, 10),
      shape('overflow_card_right_2', 8, 455, -35, 180, 84, '#FFFFFFFF', 56, 10),
      shape('overload_zone', 8, 0, 100, 450, 62, '#FFFF5B5B', 96, 16),
      text('board_label', 9, 0, -232, 30, '比較軸で整理', '#FF1B2A3C'),
      text('axis_labels', 9, -250, -121, 24, '価格\n駅距離\nリスク', '#FF1B2A3C'),
      text('overload_label', 9, 0, 85, 30, '候補が多すぎる', warningTextColor),
      text('scene_caption', 9, 0, 268, 32, '物件カードを比較軸へ押し込む', textColor),
    ],
  },
  'RE-06-development': {
    visual_intent: 'selected property with rejected cards and drawback callout',
    proxy_v21_status: 'pass',
    rationale: 'The layout has one selected property sheet in focus, rejected cards pushed aside, and a large drawback callout attached to the selected sheet.',
    primitives: [
      shape('recommend_backplate', 7, 0, -70, 1040, 410, '#FF17202D', 96, 18),
      shape('rejected_left', 8, -430, -95, 250, 120, '#FF445064', 45, 12),
      shape('rejected_right', 8, 430, -95, 250, 120, '#FF445064', 45, 12),
      shape('selected_sheet', 8, 0, -90, 570, 330, '#FFFFFEF4', 100, 18),
      shape('selected_header', 8, 0, -215, 520, 54, '#FF5A89C8', 100, 12),
      shape('score_column', 8, -175, -55, 210, 180, '#FFEAF3FF', 100, 12),
      shape('drawback_callout', 8, 245, 25, 250, 120, '#FFFFB14A', 100, 18),
      shape('selection_glow', 8, 0, -90, 625, 380, '#3370FFB0', 55, 18),
      text('selected_label', 9, 0, -228, 29, 'SELECTED PROPERTY', textColor),
      text('score_text', 9, -175, -98, 24, '条件 ✓\n価格 ✓\n駅距離 ✓', '#FF1B2A3C'),
      text('drawback_text', 9, 245, -4, 29, '注意点\nあり', '#FF2A1E00'),
      text('reject_text', 9, -430, -112, 25, 'REJECT', mutedTextColor),
      text('scene_caption', 9, 0, 268, 32, '選ぶ理由と弱点を同時に見せる', textColor),
    ],
  },
  'RE-06-turn': {
    visual_intent: 'document-backed recommendation decision',
    proxy_v21_status: 'pass',
    rationale: 'A document comparison table leads into one green recommendation decision, making the scene feel like a recommendation derived from evidence.',
    primitives: [
      shape('document_backplate', 7, 0, -70, 1040, 410, '#FF17202D', 96, 18),
      shape('evidence_table', 8, -155, -90, 650, 315, '#FFFFFBED', 100, 18),
      shape('table_header', 8, -155, -215, 590, 48, '#FF5A89C8', 100, 12),
      shape('row_a', 8, -155, -125, 560, 34, '#FFDDE8F5', 100, 6),
      shape('row_b', 8, -155, -65, 560, 34, '#FFDDE8F5', 82, 6),
      shape('row_c', 8, -155, -5, 560, 34, '#FFFFE2A8', 95, 6),
      shape('decision_panel', 8, 350, 70, 320, 130, '#FF5FD08D', 100, 18),
      shape('decision_arrow_body', 8, 155, 65, 250, 30, '#FF5FD08D', 100, 6),
      shape('decision_arrow_head', 8, 285, 65, 70, 70, '#FF5FD08D', 100, 10),
      text('table_label', 9, -155, -229, 28, '書類比較', textColor),
      text('row_labels', 9, -385, -126, 22, '価格\n条件\n弱点', '#FF1B2A3C'),
      text('decision_text', 9, 350, 43, 31, '推薦\nA案', '#FF0E2A17'),
      text('scene_caption', 9, 0, 268, 32, '比較から推薦へつなげる', textColor),
    ],
  },
  'RE-07D-beginning': {
    visual_intent: 'AI recommendation system focused on one matched card',
    proxy_v21_status: 'pass',
    rationale: 'The AI panel is a dark system block with scan bars pointing to one highlighted property card, reducing whiteboard feel and avoiding product branding.',
    primitives: [
      shape('ai_scene_backplate', 7, 0, -70, 1040, 410, '#FF091224', 98, 18),
      shape('ai_core_panel', 8, -300, -80, 500, 320, '#FF14243E', 100, 18),
      shape('ai_scan_line_1', 8, -300, -150, 390, 24, '#FF6BFFB5', 100, 6),
      shape('ai_scan_line_2', 8, -300, -95, 330, 24, '#FF6BFFB5', 80, 6),
      shape('ai_scan_line_3', 8, -300, -40, 270, 24, '#FF6BFFB5', 60, 6),
      shape('matched_property_focus', 8, 330, -80, 410, 300, '#FFFFFEF4', 100, 18),
      shape('match_ring', 8, 330, -80, 470, 360, '#3370FFB0', 58, 18),
      shape('confidence_badge', 8, 330, 75, 250, 78, '#FF63D48A', 100, 16),
      shape('arrow_to_card', 8, 10, -80, 310, 34, '#FF6BFFB5', 95, 8),
      text('ai_word', 9, -300, -228, 30, 'AI MATCH', textColor),
      text('card_word', 9, 330, -198, 28, 'PROPERTY', '#FF1B2A3C'),
      text('confidence_word', 9, 330, 58, 30, '高一致', '#FF0E2A17'),
      text('scene_caption', 9, 0, 268, 32, 'AIが一つの物件を強く推薦する', textColor),
    ],
  },
  'RE-07D-development': {
    visual_intent: 'AI recommendation interrupted by risk warning zones',
    proxy_v21_status: 'pass',
    rationale: 'Risk zones are layered over the recommendation as warning bands, so it reads as AI/risk tension rather than a list of notes.',
    primitives: [
      shape('risk_scene_backplate', 7, 0, -70, 1040, 410, '#FF140B12', 98, 18),
      shape('property_under_risk', 8, 0, -75, 520, 300, '#FFFFFEF4', 92, 18),
      shape('ai_recommendation_bar', 8, 0, -205, 520, 54, '#FF6BFFB5', 96, 12),
      shape('risk_zone_boundary', 8, -340, -88, 300, 108, '#FFFF5B5B', 98, 18),
      shape('risk_zone_inheritance', 8, 0, 30, 300, 108, '#FFFFB14A', 98, 18),
      shape('risk_zone_neighborhood', 8, 340, -88, 300, 108, '#FFFF5B5B', 98, 18),
      shape('black_warning_strip', 8, 0, 132, 650, 64, '#FF080C14', 100, 12),
      text('ai_ok_text', 9, 0, -219, 28, 'AI: 推薦', '#FF0E2A17'),
      text('boundary_text', 9, -340, -110, 28, '! 境界', warningTextColor),
      text('inheritance_text', 9, 0, 8, 28, '! 相続', '#FF2A1E00'),
      text('neighborhood_text', 9, 340, -110, 28, '! 周辺', warningTextColor),
      text('warning_strip_text', 9, 0, 116, 30, '見えないリスクで推薦を止める', textColor),
      text('scene_caption', 9, 0, 268, 32, 'AI推薦にリスク警告が割り込む', textColor),
    ],
  },
};

function shape(itemId, layer, x, y, width, height, color, opacity = 100, round = 10) {
  return { kind: 'ShapeItem', item_id: itemId, layer, x, y, width, height, color, opacity, round };
}

function text(itemId, layer, x, y, fontSize, content, color = textColor) {
  return { kind: 'TextItem', item_id: itemId, layer, x, y, fontSize, content, color };
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

function validateCompactReview(compactReview) {
  const candidates = compactReview.candidates || [];
  const errors = [];
  if (candidates.length !== expectedCandidateIds.length) {
    errors.push(`expected 7 candidates, got ${candidates.length}`);
  }
  const candidateIds = candidates.map((candidate) => candidate.candidate_id);
  for (const candidateId of expectedCandidateIds) {
    if (!candidateIds.includes(candidateId)) errors.push(`missing ${candidateId}`);
    if (!visualSpecs[candidateId]) errors.push(`missing visual spec ${candidateId}`);
  }
  for (const candidate of candidates) {
    if (candidate.actual_ymmp_patch_output_readiness !== 'ready') {
      errors.push(`${candidate.candidate_id} is not ready`);
    }
  }
  if (errors.length) {
    throw new Error(`COMPACT_REVIEW_INVALID: ${errors.join('; ')}`);
  }
}

function sourceLineText(candidate) {
  const lines = candidate.source_reference?.source_line_range;
  return lines ? `${lines.line_start}-${lines.line_end}` : 'unknown';
}

function buildRemark(candidate, primitive) {
  return [
    'g27_visual_proxy_v21_probe',
    `candidate_id=${candidate.candidate_id}`,
    `item_id=${scopedItemId(candidate, primitive)}`,
    `source=${paths.compactReview}`,
    `source_beat=${candidate.source_reference?.visual_treatment_beat_id || candidate.candidate_id}`,
    `source_lines=${sourceLineText(candidate)}`,
    'shape_text_only',
    'not_creative_acceptance',
    'no_render',
  ].join(' ');
}

function scopedItemId(candidate, primitive) {
  return `${candidate.candidate_id}__${primitive.item_id}`;
}

function makeShapeItem(template, candidate, primitive) {
  const item = clone(template);
  item.Frame = candidate.approximate_start_frame;
  item.Length = candidate.approximate_duration_frames;
  item.Layer = primitive.layer;
  item.Group = 0;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Remark = buildRemark(candidate, primitive);
  item.IsLocked = false;
  item.IsHidden = false;
  setAnimatedValue(item, 'X', primitive.x);
  setAnimatedValue(item, 'Y', primitive.y);
  setAnimatedValue(item, 'Z', 0);
  setAnimatedValue(item, 'Opacity', primitive.opacity);
  setAnimatedValue(item, 'Zoom', 100);
  setAnimatedValue(item, 'Rotation', 0);
  setShapeParameterValue(item, 'Width', primitive.width);
  setShapeParameterValue(item, 'Height', primitive.height);
  setShapeParameterValue(item, 'Round', primitive.round);
  setShapeParameterValue(item, 'StrokeThickness', 0);
  setShapeBrushColor(item, primitive.color);
  return item;
}

function makeTextItem(candidate, primitive) {
  return {
    $type: 'YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker',
    Text: primitive.content,
    Font: 'Yu Gothic UI',
    FontSize: animation(primitive.fontSize),
    FontColor: primitive.color,
    Style: 'Normal',
    X: animation(primitive.x),
    Y: animation(primitive.y),
    Z: animation(0),
    Opacity: animation(100),
    Zoom: animation(100),
    Rotation: animation(0),
    FadeIn: 0,
    FadeOut: 0,
    Blend: 'Normal',
    IsAlwaysOnTop: false,
    IsZOrderEnabled: false,
    VideoEffects: [],
    Group: 0,
    Frame: candidate.approximate_start_frame,
    Layer: primitive.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: candidate.approximate_duration_frames,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: buildRemark(candidate, primitive),
    IsLocked: false,
    IsHidden: false,
  };
}

function buildProbeProject(compactReview, carrierYmmp, shapeTemplateYmmp) {
  validateCompactReview(compactReview);
  const shapeTemplate = findFirstItemByType(shapeTemplateYmmp, 'ShapeItem');
  if (!shapeTemplate) {
    throw new Error(`SHAPE_TEMPLATE_MISSING: ${paths.shapeTemplateYmmp}`);
  }
  const project = clone(carrierYmmp);
  const timeline = project.Timelines?.[0];
  if (!timeline || !Array.isArray(project.Timelines)) {
    throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  }
  const items = [];
  for (const candidate of compactReview.candidates) {
    const spec = visualSpecs[candidate.candidate_id];
    for (const primitive of spec.primitives) {
      if (primitive.kind === 'ShapeItem') {
        items.push(makeShapeItem(shapeTemplate, candidate, primitive));
      } else if (primitive.kind === 'TextItem') {
        items.push(makeTextItem(candidate, primitive));
      } else {
        throw new Error(`UNSUPPORTED_PRIMITIVE_KIND: ${primitive.kind}`);
      }
    }
  }
  timeline.Items = items;
  timeline.CurrentFrame = 0;
  timeline.Length = Math.max(...items.map((item) => item.Frame + item.Length), 0);
  timeline.MaxLayer = Math.max(...items.map((item) => item.Layer), 0);
  if (!timeline.LayerSettings || Array.isArray(timeline.LayerSettings)) {
    timeline.LayerSettings = { Items: Array.isArray(timeline.LayerSettings) ? timeline.LayerSettings : [] };
  }
  project.FilePath = abs(paths.outputYmmp);
  return project;
}

function parseRemark(remark) {
  const result = {};
  String(remark || '').split(/\s+/).forEach((part) => {
    const separatorIndex = part.indexOf('=');
    if (separatorIndex > 0) {
      result[part.slice(0, separatorIndex)] = part.slice(separatorIndex + 1);
    }
  });
  return result;
}

function expectedItems(compactReview) {
  return compactReview.candidates.flatMap((candidate) =>
    visualSpecs[candidate.candidate_id].primitives.map((primitive) => ({
      candidate_id: candidate.candidate_id,
      item_id: scopedItemId(candidate, primitive),
      item_type: primitive.kind,
      layer: primitive.layer,
      start_frame: candidate.approximate_start_frame,
      duration_frames: candidate.approximate_duration_frames,
      source: paths.compactReview,
    })),
  );
}

function valueType(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  return typeof value === 'object' ? 'object' : typeof value;
}

function isAnimationObject(value) {
  return Boolean(value && typeof value === 'object' && Array.isArray(value.Values) && Object.hasOwn(value, 'AnimationType'));
}

function colorPatternFor(key, value) {
  const loweredKey = key.toLowerCase();
  if (loweredKey.includes('color')) {
    return typeof value === 'string' && hexColorPattern.test(value)
      ? { status: 'pass', pattern: '#AARRGGBB string' }
      : { status: 'fail', pattern: 'Color-like key is not #AARRGGBB string' };
  }
  if (loweredKey.includes('brush')) {
    const color = value?.Parameter?.Color;
    return value && typeof value === 'object' && typeof value.Type === 'string' && typeof color === 'string' && hexColorPattern.test(color)
      ? { status: 'pass', pattern: 'YMM4 brush plugin object with nested #AARRGGBB Color' }
      : { status: 'fail', pattern: 'Brush-like key is not recognized YMM4 brush plugin object' };
  }
  if (isAnimationObject(value)) {
    return { status: 'pass', pattern: 'YMM4 animation object, not a color scalar' };
  }
  return { status: 'review', pattern: `visual-style key value type ${valueType(value)}` };
}

function scanColorLikeFields(items) {
  const occurrences = [];
  const failures = [];
  function walk(value, jsonPath) {
    if (Array.isArray(value)) {
      value.forEach((entry, index) => walk(entry, `${jsonPath}[${index}]`));
      return;
    }
    if (!value || typeof value !== 'object') return;
    for (const [key, childValue] of Object.entries(value)) {
      const childPath = `${jsonPath}.${key}`;
      if (colorLikeTerms.some((term) => key.toLowerCase().includes(term))) {
        const pattern = colorPatternFor(key, childValue);
        const occurrence = {
          json_path: childPath,
          value_type: valueType(childValue),
          observed_compatible_pattern: pattern.pattern,
          status: pattern.status,
        };
        occurrences.push(occurrence);
        if (pattern.status === 'fail') {
          failures.push(occurrence);
        }
      }
      walk(childValue, childPath);
    }
  }
  items.forEach((item, index) => walk(item, `$.Timelines[0].Items[${index}]`));
  return { occurrences, failures };
}

function readbackProbe(compactReview, ymmp, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const probeItems = timelineItems
    .map((item, index) => {
      const remark = parseRemark(item.Remark);
      return {
        index,
        item_type: itemType(item),
        candidate_id: remark.candidate_id || null,
        item_id: remark.item_id || null,
        layer: item.Layer,
        start_frame: item.Frame,
        duration_frames: item.Length,
        text: item.Text || null,
        font_color: item.FontColor || null,
        remark: item.Remark || '',
        source_reference_found: {
          candidate_id: Boolean(remark.candidate_id),
          item_id: Boolean(remark.item_id),
          source: remark.source === paths.compactReview,
          source_lines: Boolean(remark.source_lines),
        },
      };
    })
    .filter((item) => item.remark.includes('g27_visual_proxy_v21_probe'));

  const expected = expectedItems(compactReview);
  const missingItems = [];
  const malformedItems = [];
  for (const expectedItem of expected) {
    const found = probeItems.find((item) => item.item_id === expectedItem.item_id);
    if (!found) {
      missingItems.push({ ...expectedItem, reason: 'expected v2.1 primitive item not found' });
      continue;
    }
    const mismatches = [];
    for (const field of ['candidate_id', 'item_type', 'layer', 'start_frame', 'duration_frames']) {
      if (found[field] !== expectedItem[field]) {
        mismatches.push({ field, expected: expectedItem[field], actual: found[field] });
      }
    }
    if (!found.source_reference_found.source || !found.source_reference_found.source_lines) {
      mismatches.push({ field: 'source_reference', expected: 'compact review source and source_lines', actual: found.source_reference_found });
    }
    if (!['ShapeItem', 'TextItem'].includes(found.item_type)) {
      mismatches.push({ field: 'item_type_allowed', expected: 'ShapeItem/TextItem only', actual: found.item_type });
    }
    if (![7, 8, 9].includes(found.layer)) {
      mismatches.push({ field: 'safe_layer', expected: '7/8/9', actual: found.layer });
    }
    if (found.item_type === 'TextItem' && !(typeof found.font_color === 'string' && hexColorPattern.test(found.font_color))) {
      mismatches.push({ field: 'FontColor', expected: '#AARRGGBB string', actual: found.font_color });
    }
    if (mismatches.length) {
      malformedItems.push({ item_id: expectedItem.item_id, candidate_id: expectedItem.candidate_id, mismatches });
    }
  }

  const colorScan = scanColorLikeFields(timelineItems);
  const candidateSummaries = expectedCandidateIds.map((candidateId) => {
    const spec = visualSpecs[candidateId];
    const items = probeItems.filter((item) => item.candidate_id === candidateId);
    const shapeCount = items.filter((item) => item.item_type === 'ShapeItem').length;
    const textCount = items.filter((item) => item.item_type === 'TextItem').length;
    const missing = missingItems.filter((item) => item.candidate_id === candidateId);
    const malformed = malformedItems.filter((item) => item.candidate_id === candidateId);
    return {
      candidate_id: candidateId,
      visual_intent: spec.visual_intent,
      proxy_v21_status: missing.length || malformed.length ? 'fix required' : spec.proxy_v21_status,
      shape_item_count: shapeCount,
      text_item_count: textCount,
      source_line_range: compactReview.candidates.find((candidate) => candidate.candidate_id === candidateId)?.source_reference?.source_line_range || null,
      semantic_readability_basis: spec.rationale,
      missing_item_count: missing.length,
      malformed_item_count: malformed.length,
    };
  });

  const foundCandidateIds = [...new Set(probeItems.map((item) => item.candidate_id).filter(Boolean))];
  const insertedShapeItemCount = probeItems.filter((item) => item.item_type === 'ShapeItem').length;
  const insertedTextItemCount = probeItems.filter((item) => item.item_type === 'TextItem').length;
  const status =
    missingItems.length === 0 &&
    malformedItems.length === 0 &&
    colorScan.failures.length === 0 &&
    expectedCandidateIds.every((candidateId) => foundCandidateIds.includes(candidateId))
      ? 'passed'
      : 'failed';

  return {
    artifact_type: 'g27_visual_proxy_v21_probe_readback',
    status,
    source: {
      compact_patch_review: paths.compactReview,
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_probe_ymmp: paths.outputYmmp,
    },
    boundary: {
      visual_proxy_v21_probe_only: true,
      shape_item_text_item_only: true,
      external_assets_used: false,
      tts_performed: false,
      url_fetch_performed: false,
      publishing_performed: false,
      render_performed: false,
      creative_acceptance_performed: false,
      production_or_source_ymmp_modified_in_place: false,
      excluded_RE_02_turn: 'blocked_outside_output',
      excluded_RE_07D_turn: 'deferred_outside_output',
    },
    source_integrity: {
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    totals: {
      expected_candidate_count: expectedCandidateIds.length,
      expected_item_count: expected.length,
      inserted_probe_item_count: probeItems.length,
      inserted_shape_item_count: insertedShapeItemCount,
      inserted_text_item_count: insertedTextItemCount,
      missing_item_count: missingItems.length,
      malformed_item_count: malformedItems.length,
      color_like_occurrence_count: colorScan.occurrences.length,
      color_like_failure_count: colorScan.failures.length,
    },
    candidate_ids_found: foundCandidateIds,
    candidate_summaries: candidateSummaries,
    items: probeItems,
    color_like_scan: colorScan,
    missing_items: missingItems,
    malformed_items: malformedItems,
    pass_fix_defer_table: candidateSummaries.map((summary) => ({
      candidate_id: summary.candidate_id,
      classification: summary.proxy_v21_status,
      reason: summary.semantic_readability_basis,
    })),
    next_slice_note:
      status === 'passed'
        ? 'Open the visual proxy v2.1 .ymmp in YMM4 for GUI readback only; do not render or treat this as creative acceptance.'
        : 'Fix v2.1 primitive/readback failures before any GUI readback retry.',
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Visual Proxy v2.1 Probe');
  lines.push('');
  lines.push(`Probe: \`${readback.source.generated_probe_ymmp}\``);
  lines.push(`Source compact review: \`${readback.source.compact_patch_review}\``);
  lines.push('');
  lines.push('This is a bounded G-27 visual proxy v2.1 probe. It reduces indexed whiteboard / sticky-note feel by using one focal panel per candidate, stronger hierarchy, and distinct layout grammar for RE-02 / RE-06 / RE-07D. It is not a render, not creative acceptance, and not production readiness.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Readback status: \`${readback.status}\``);
  lines.push(`- Inserted items: \`${readback.totals.inserted_probe_item_count}\` (` +
    `ShapeItem=\`${readback.totals.inserted_shape_item_count}\`, TextItem=\`${readback.totals.inserted_text_item_count}\`)`);
  lines.push(`- Color-like scan failures: \`${readback.totals.color_like_failure_count}\``);
  lines.push(`- Carrier modified in place: \`${readback.source_integrity.carrier_modified_in_place}\``);
  lines.push('');
  lines.push('## Pass / Fix / Defer Table');
  lines.push('');
  lines.push('| candidate | classification | visual intent | basis |');
  lines.push('| --- | --- | --- | --- |');
  readback.candidate_summaries.forEach((summary) => {
    lines.push(`| \`${summary.candidate_id}\` | \`${summary.proxy_v21_status}\` | ${summary.visual_intent} | ${summary.semantic_readability_basis} |`);
  });
  lines.push('');
  lines.push('## Candidate Counts');
  lines.push('');
  lines.push('| candidate | ShapeItems | TextItems | source lines |');
  lines.push('| --- | ---: | ---: | --- |');
  readback.candidate_summaries.forEach((summary) => {
    const lineRange = summary.source_line_range
      ? `${summary.source_line_range.line_start}-${summary.source_line_range.line_end}`
      : 'unknown';
    lines.push(`| \`${summary.candidate_id}\` | ${summary.shape_item_count} | ${summary.text_item_count} | ${lineRange} |`);
  });
  lines.push('');
  lines.push('## Boundaries');
  lines.push('');
  lines.push('- Technical openability: the prior minimal probe and v2 opened in YMM4; this v2.1 readback keeps project-canvas structure and ShapeItem/TextItem-only output.');
  lines.push('- Visual semantic adequacy: locally improved from indexed whiteboard toward focal scene proxies with split-screen, pipeline, comparison board, document decision, AI match, and warning-zone grammar. GUI visual judgment is still required.');
  lines.push('- Production readiness: not ready. No render, production timing, creative acceptance, external assets, TTS, URL fetch, or publishing.');
  lines.push('- Remaining distance to minimal render: if this v2.1 GUI readback passes as meaningful video proxy, the next slice may be minimal render smoke; otherwise keep local fixes in v2.1.');
  lines.push('- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.');
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback, markdown = null) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.totals.expected_candidate_count !== 7) failures.push('candidate count mismatch');
  if (readback.totals.inserted_probe_item_count !== readback.totals.expected_item_count) failures.push('item count mismatch');
  if (readback.totals.missing_item_count !== 0) failures.push('missing items present');
  if (readback.totals.malformed_item_count !== 0) {
    failures.push(`malformed items present: ${JSON.stringify(readback.malformed_items.slice(0, 3))}`);
  }
  if (readback.totals.color_like_failure_count !== 0) failures.push('color-like scan failures present');
  if (readback.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  if (!readback.candidate_summaries.every((summary) => summary.proxy_v21_status === 'pass')) {
    failures.push('not all candidates pass v2.1 proxy construction readback');
  }
  if (markdown) {
    if (!markdown.includes('## Pass / Fix / Defer Table')) failures.push('report missing pass/fix/defer table');
    if (!markdown.includes('Remaining distance to minimal render')) failures.push('report missing minimal render distance');
  }
  if (failures.length) {
    throw new Error(`G27_VISUAL_PROXY_V21_READBACK_FAILED: ${failures.join('; ')}`);
  }
}

function main() {
  const compactReview = readJson(paths.compactReview);
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const carrierYmmp = readJson(paths.carrierYmmp);
  const shapeTemplateYmmp = readJson(paths.shapeTemplateYmmp);
  const generatedProject = buildProbeProject(compactReview, carrierYmmp, shapeTemplateYmmp);
  const generatedReadback = readbackProbe(compactReview, generatedProject, carrierHashBefore, sha256(paths.carrierYmmp));
  const generatedReport = renderMarkdown(generatedReadback);
  assertReadback(generatedReadback, generatedReport);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generatedProject);
    const writtenProject = readJson(paths.outputYmmp);
    const writtenReadback = readbackProbe(compactReview, writtenProject, carrierHashBefore, sha256(paths.carrierYmmp));
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
    const actualReadback = readbackProbe(compactReview, existingProject, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(actualReadback);
    assertReadback(existingReadback, fs.existsSync(abs(paths.reportMd)) ? readText(paths.reportMd) : null);
    if (JSON.stringify(actualReadback) !== JSON.stringify(existingReadback)) {
      throw new Error('READBACK_DRIFT: existing v2.1 readback JSON does not match probe .ymmp');
    }
  }

  console.log('G-27 visual proxy v2.1 probe OK: 7 candidates, ShapeItem/TextItem only, color-like failures=0');
}

main();

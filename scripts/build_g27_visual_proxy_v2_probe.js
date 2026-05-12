const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const paths = {
  compactReview: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/real_estate_dx_visual_proxy_v2_probe.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_visual_proxy_v2_probe_readback.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_visual_proxy_v2_probe_report.md',
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
    visual_intent: 'public search UI vs broker/private database contrast',
    proxy_v2_status: 'pass',
    rationale: 'Public/private contrast is readable through two labeled panels and a restricted-access badge.',
    primitives: [
      shape('private_db_panel', 7, 270, -95, 700, 330, '#FF16233C', 92, 18),
      shape('private_db_header', 8, 270, -220, 650, 48, '#FF2F4B78', 96, 12),
      shape('private_db_row_1', 8, 270, -145, 580, 36, '#FF405C86', 75, 8),
      shape('private_db_row_2', 8, 270, -90, 580, 36, '#FF405C86', 65, 8),
      shape('private_db_row_3', 8, 270, -35, 580, 36, '#FF405C86', 55, 8),
      shape('public_search_card', 8, -385, -90, 560, 300, '#FFEAF5FF', 94, 18),
      shape('public_search_bar', 8, -385, -205, 500, 44, '#FFFFFFFF', 100, 14),
      shape('limited_badge_bg', 8, -125, 70, 190, 64, '#FFFFC857', 100, 14),
      text('public_label', 9, -385, -214, 30, '公開検索', textColor),
      text('private_label', 9, 270, -225, 30, '業者DB / 非公開', textColor),
      text('restricted_badge', 9, -125, 61, 26, '一部だけ見える', '#FF2A1E00'),
      text('contrast_arrow', 9, -10, -20, 44, '公開  →  内部DB', textColor),
      text('title', 9, 0, 278, 34, 'RE-02: 公開情報と業者DBの差', textColor),
    ],
  },
  'RE-02-development': {
    visual_intent: 'broker DB panel, public portal card, and property-card flow',
    proxy_v2_status: 'pass',
    rationale: 'Information volume and extraction are represented by many private cards flowing into a small public portal.',
    primitives: [
      shape('broker_db_panel', 7, -380, -80, 600, 340, '#FF173552', 94, 18),
      shape('public_portal_panel', 7, 405, -80, 470, 300, '#FFE7F3FF', 94, 18),
      shape('db_card_a', 8, -520, -155, 120, 62, '#FF6CA6D9', 92, 8),
      shape('db_card_b', 8, -375, -155, 120, 62, '#FF6CA6D9', 82, 8),
      shape('db_card_c', 8, -230, -155, 120, 62, '#FF6CA6D9', 72, 8),
      shape('db_card_d', 8, -520, -65, 120, 62, '#FF6CA6D9', 72, 8),
      shape('db_card_e', 8, -375, -65, 120, 62, '#FF6CA6D9', 62, 8),
      shape('portal_card_a', 8, 335, -105, 150, 76, '#FFFFFFFF', 100, 10),
      shape('portal_card_b', 8, 505, -105, 150, 76, '#FFFFFFFF', 88, 10),
      shape('flow_badge_bg', 8, 20, -80, 160, 56, '#FF8EE0A1', 100, 12),
      text('broker_db_label', 9, -380, -238, 30, '業者DB: 多い', textColor),
      text('portal_label', 9, 405, -220, 30, '公開ポータル: 少ない', '#FF153044'),
      text('flow_arrow', 9, 20, -104, 48, '抽出 →', '#FF122818'),
      text('title', 9, 0, 278, 34, 'RE-02: 情報量の差が流れで読める', textColor),
    ],
  },
  'RE-06-beginning': {
    visual_intent: 'property card overload cluster',
    proxy_v2_status: 'pass',
    rationale: 'Too many property choices are represented by crowded cards plus an overload warning badge.',
    primitives: [
      shape('card_cluster_back', 7, 0, -70, 900, 330, '#FF213047', 78, 18),
      shape('property_card_1', 8, -390, -165, 220, 94, '#FFFFFFFF', 100, 10),
      shape('property_card_2', 8, -135, -175, 220, 94, '#FFFFFFFF', 95, 10),
      shape('property_card_3', 8, 120, -160, 220, 94, '#FFFFFFFF', 90, 10),
      shape('property_card_4', 8, 375, -175, 220, 94, '#FFFFFFFF', 86, 10),
      shape('property_card_5', 8, -260, -30, 220, 94, '#FFFFFFFF', 82, 10),
      shape('property_card_6', 8, 5, -20, 220, 94, '#FFFFFFFF', 78, 10),
      shape('warning_badge_bg', 8, 315, 74, 270, 76, '#FFFF5B5B', 100, 16),
      text('card_text_1', 9, -390, -179, 20, '物件A', '#FF1B2A3C'),
      text('card_text_2', 9, -135, -189, 20, '物件B', '#FF1B2A3C'),
      text('card_text_3', 9, 120, -174, 20, '物件C', '#FF1B2A3C'),
      text('warning_label', 9, 315, 59, 32, '候補が多すぎる', warningTextColor),
      text('title', 9, 0, 278, 34, 'RE-06: 物件カード過多 / 選択疲れ', textColor),
    ],
  },
  'RE-06-development': {
    visual_intent: 'selected property sheet with drawback marker',
    proxy_v2_status: 'pass',
    rationale: 'A selected sheet, checklist, and drawback badge turn noisy cards into a readable curation proxy.',
    primitives: [
      shape('faded_noise_left', 7, -450, -120, 240, 110, '#FF536274', 38, 10),
      shape('faded_noise_right', 7, 450, -115, 240, 110, '#FF536274', 38, 10),
      shape('selected_property_sheet', 8, -120, -70, 560, 330, '#FFFFFEF4', 100, 18),
      shape('sheet_header', 8, -120, -210, 500, 50, '#FF5A89C8', 100, 12),
      shape('checklist_box', 8, -215, -55, 270, 180, '#FFEAF3FF', 100, 10),
      shape('drawback_badge_bg', 8, 250, 55, 250, 86, '#FFFFB14A', 100, 16),
      shape('selection_frame', 8, -120, -70, 620, 380, '#3370FFB0', 42, 18),
      text('header_label', 9, -120, -222, 28, '選定物件シート', textColor),
      text('checklist', 9, -215, -94, 23, '✓ 条件\n✓ 価格\n✓ 駅距離', '#FF1B2A3C'),
      text('drawback', 9, 250, 38, 30, 'デメリットも表示', '#FF2A1E00'),
      text('title', 9, 0, 278, 34, 'RE-06: ノイズ排除 + 注意点提示', textColor),
    ],
  },
  'RE-06-turn': {
    visual_intent: 'property document editorial comparison',
    proxy_v2_status: 'pass',
    rationale: 'Two document panels and a recommendation ribbon make the proxy feel document-backed rather than a generic strategy diagram.',
    primitives: [
      shape('document_left', 7, -265, -75, 420, 335, '#FFFFFBED', 100, 12),
      shape('document_right', 7, 265, -75, 420, 335, '#FFFFFBED', 100, 12),
      shape('doc_line_l1', 8, -265, -170, 320, 24, '#FFB8C6D8', 100, 5),
      shape('doc_line_l2', 8, -265, -110, 320, 24, '#FFB8C6D8', 90, 5),
      shape('doc_line_r1', 8, 265, -170, 320, 24, '#FFB8C6D8', 100, 5),
      shape('doc_line_r2', 8, 265, -110, 320, 24, '#FFB8C6D8', 90, 5),
      shape('recommend_ribbon', 8, 0, 88, 360, 72, '#FF5FD08D', 100, 16),
      text('left_doc_label', 9, -265, -237, 27, '物件書類 A', '#FF1B2A3C'),
      text('right_doc_label', 9, 265, -237, 27, '物件書類 B', '#FF1B2A3C'),
      text('compare_arrow', 9, 0, -75, 48, '比較 → 推奨', textColor),
      text('recommend_label', 9, 0, 72, 30, '納得できる推薦', '#FF0E2A17'),
      text('title', 9, 0, 278, 34, 'RE-06: 書類ベースの比較とキュレーション', textColor),
    ],
  },
  'RE-07D-beginning': {
    visual_intent: 'AI panel plus matched property card',
    proxy_v2_status: 'pass',
    rationale: 'An abstract AI panel, confidence bars, and matched property card are visible without real product branding.',
    primitives: [
      shape('ai_panel', 7, -310, -80, 520, 330, '#FF14243E', 96, 18),
      shape('ai_header', 8, -310, -210, 470, 52, '#FF7A7BFF', 100, 14),
      shape('confidence_bar_1', 8, -390, -120, 300, 26, '#FF6BFFB5', 100, 8),
      shape('confidence_bar_2', 8, -390, -70, 250, 26, '#FF6BFFB5', 88, 8),
      shape('matched_card', 8, 340, -70, 430, 300, '#FFFFFEF4', 100, 18),
      shape('match_badge_bg', 8, 340, 83, 250, 70, '#FF63D48A', 100, 16),
      text('ai_header_text', 9, -310, -223, 29, 'AI 推薦パネル', textColor),
      text('score_text', 9, -390, -18, 34, 'MATCH 100%?', '#FFBFFFE2'),
      text('property_text', 9, 340, -188, 29, '物件カード', '#FF1B2A3C'),
      text('match_badge', 9, 340, 68, 30, 'あなた向け', '#FF0E2A17'),
      text('title', 9, 0, 278, 34, 'RE-07D: AI推薦 + 物件カード', textColor),
    ],
  },
  'RE-07D-development': {
    visual_intent: 'AI-adjacent risk marker and warning state proxy',
    proxy_v2_status: 'pass',
    rationale: 'Boundary, inheritance, and neighborhood risks are separated into visible warning markers around a property context card.',
    primitives: [
      shape('property_context_card', 7, 0, -90, 500, 310, '#FFFFFEF4', 96, 18),
      shape('risk_panel', 7, 0, -90, 850, 360, '#FF2D1D28', 55, 18),
      shape('boundary_marker', 8, -360, -150, 250, 74, '#FFFF6B6B', 100, 16),
      shape('inheritance_marker', 8, 0, -180, 250, 74, '#FFFFB14A', 100, 16),
      shape('neighborhood_marker', 8, 360, -150, 250, 74, '#FFFF6B6B', 100, 16),
      shape('warning_state_bar', 8, 0, 80, 530, 70, '#FF101A2A', 96, 14),
      text('property_context', 9, 0, -70, 28, '物件カードの裏側', '#FF1B2A3C'),
      text('boundary_text', 9, -360, -165, 25, '! 境界', warningTextColor),
      text('inheritance_text', 9, 0, -195, 25, '! 相続', '#FF2A1E00'),
      text('neighborhood_text', 9, 360, -165, 25, '! 周辺', warningTextColor),
      text('warning_state', 9, 0, 64, 31, 'データだけでは見えないリスク', textColor),
      text('title', 9, 0, 278, 34, 'RE-07D: AI推薦にリスク警告を重ねる', textColor),
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
    'g27_visual_proxy_v2_probe',
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
    .filter((item) => item.remark.includes('g27_visual_proxy_v2_probe'));

  const expected = expectedItems(compactReview);
  const missingItems = [];
  const malformedItems = [];
  for (const expectedItem of expected) {
    const found = probeItems.find((item) => item.item_id === expectedItem.item_id);
    if (!found) {
      missingItems.push({ ...expectedItem, reason: 'expected v2 primitive item not found' });
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
      proxy_v2_status: missing.length || malformed.length ? 'fix required' : spec.proxy_v2_status,
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
    artifact_type: 'g27_visual_proxy_v2_probe_readback',
    status,
    source: {
      compact_patch_review: paths.compactReview,
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_probe_ymmp: paths.outputYmmp,
    },
    boundary: {
      visual_proxy_v2_probe_only: true,
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
      classification: summary.proxy_v2_status,
      reason: summary.semantic_readability_basis,
    })),
    next_slice_note:
      status === 'passed'
        ? 'Open the visual proxy v2 .ymmp in YMM4 for GUI readback only; do not render or treat this as creative acceptance.'
        : 'Fix v2 primitive/readback failures before any GUI readback retry.',
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Visual Proxy v2 Probe');
  lines.push('');
  lines.push(`Probe: \`${readback.source.generated_probe_ymmp}\``);
  lines.push(`Source compact review: \`${readback.source.compact_patch_review}\``);
  lines.push('');
  lines.push('This is a bounded G-27 visual proxy probe. It improves marker-level rectangles into ShapeItem/TextItem primitive compositions for the same 7 ready candidates. It is not a render, not creative acceptance, and not production readiness.');
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
    lines.push(`| \`${summary.candidate_id}\` | \`${summary.proxy_v2_status}\` | ${summary.visual_intent} | ${summary.semantic_readability_basis} |`);
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
  lines.push('- Technical openability: the prior minimal probe opened in YMM4; this v2 readback keeps project-canvas structure and ShapeItem/TextItem-only output.');
  lines.push('- Visual semantic adequacy: improved to a proxy-readback target with panels, cards, badges, arrows, checklists, and warning markers, but still needs GUI visual judgment.');
  lines.push('- Production readiness: not ready. No render, production timing, creative acceptance, external assets, TTS, URL fetch, or publishing.');
  lines.push('- Remaining distance to minimal render: one GUI readback of this v2 probe must confirm the compositions are legible enough before any later minimal render probe can be considered.');
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
  if (!readback.candidate_summaries.every((summary) => summary.proxy_v2_status === 'pass')) {
    failures.push('not all candidates pass v2 proxy construction readback');
  }
  if (markdown) {
    if (!markdown.includes('## Pass / Fix / Defer Table')) failures.push('report missing pass/fix/defer table');
    if (!markdown.includes('Remaining distance to minimal render')) failures.push('report missing minimal render distance');
  }
  if (failures.length) {
    throw new Error(`G27_VISUAL_PROXY_V2_READBACK_FAILED: ${failures.join('; ')}`);
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
      throw new Error('READBACK_DRIFT: existing v2 readback JSON does not match probe .ymmp');
    }
  }

  console.log('G-27 visual proxy v2 probe OK: 7 candidates, ShapeItem/TextItem only, color-like failures=0');
}

main();

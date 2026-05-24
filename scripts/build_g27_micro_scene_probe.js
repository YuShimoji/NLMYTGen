const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const fps = 60;

const paths = {
  compactReview: 'samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json',
  carrierYmmp: 'samples/canonical.ymmp',
  shapeTemplateYmmp: 'samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp',
  outputYmmp: 'samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe_readback.json',
  reportMd: 'samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe_report.md',
};

const selectedCandidateIds = [
  'RE-02-development',
  'RE-06-development',
  'RE-07D-beginning',
  'RE-07D-development',
];

const notSelectedCandidateIds = [
  'RE-02-beginning',
  'RE-06-beginning',
  'RE-06-turn',
];

const textColor = '#FFFFFFFF';
const darkTextColor = '#FF111827';
const warningTextColor = '#FFFFF7D6';
const colorLikeTerms = ['color', 'brush', 'background', 'border', 'fill', 'stroke', 'shadow', 'foreground'];
const hexColorPattern = /^#[0-9A-Fa-f]{8}$/;
const shapeSizeMode = 'WidthHeight';

const sceneBeats = [
  {
    beat_id: 'micro-01-access-contrast',
    candidate_id: 'RE-02-development',
    start_frame: 0,
    duration_frames: 900,
    narrative_intent: 'Viewer understands that the same market has a public entrance and a deeper professional database, so visible information is structurally limited.',
    visual_composition: 'A large dark broker database slides into dominance behind a smaller public portal; a lock threshold appears between them and only a thin output card escapes.',
    on_screen_copy: ['公開入口', '業者DB', 'LOCK'],
    why_avoids_whiteboard: 'The beat is staged as a door/threshold event with one focal split-screen system, not as separate note cards explaining the concept.',
    minimal_render_readiness_basis: 'access contrast reads through lock and depth relation',
    primitives: [
      shape('backplate', 7, 0, 0, 1500, 780, '#FF12233C', 100, 0, 900, 24),
      shape('public_panel', 8, -450, -50, 590, 500, '#FFEAF7FF', 100, 0, 900, 24),
      shape('public_search_bar', 8, -450, -190, 485, 74, '#FFFFFFFF', 100, 60, 840, 14),
      shape('public_result_stack', 8, -450, 30, 420, 190, '#FFB8D9F2', 100, 120, 780, 18),
      shape('private_panel', 8, 360, -50, 760, 560, '#FF1F4B7D', 100, 150, 750, 24),
      shape('private_depth_1', 8, 360, -210, 600, 62, '#FF76A7E8', 100, 220, 680, 10),
      shape('private_depth_2', 8, 360, -90, 600, 62, '#FF4F83C8', 100, 280, 620, 10),
      shape('private_depth_3', 8, 360, 30, 600, 62, '#FF2F659F', 100, 340, 560, 10),
      shape('access_arrow_body', 8, -210, 190, 420, 44, '#FF64D4FF', 100, 420, 480, 10),
      shape('lock_boundary', 8, -40, -40, 125, 610, '#FFFFC857', 100, 450, 450, 14),
      shape('lock_body', 8, -40, -40, 155, 132, '#FFFFD77A', 100, 500, 400, 18),
      shape('output_card', 8, 135, 208, 410, 118, '#FF7BE28F', 100, 600, 300, 18),
      text('public_label', 9, -450, -285, 42, '公開入口', darkTextColor, 30, 870),
      text('db_label', 9, 360, -310, 42, '業者DB', textColor, 170, 730),
      text('lock_label', 9, -40, -62, 36, 'LOCK', '#FF3A2800', 520, 380),
    ],
  },
  {
    beat_id: 'micro-02-selection',
    candidate_id: 'RE-06-development',
    start_frame: 900,
    duration_frames: 900,
    narrative_intent: 'Viewer understands that the service narrows many options into one recommended property while keeping the drawback visible.',
    visual_composition: 'Rejected cards slide to the edges, one property sheet remains center stage, and a warning callout attaches to the selected sheet.',
    on_screen_copy: ['一つに絞る', '選定', '注意点'],
    why_avoids_whiteboard: 'The screen is a selection event: cards are spatially rejected, one sheet is framed, and the drawback is attached to the chosen object.',
    minimal_render_readiness_basis: 'selection and drawback relation are event-like and focal',
    primitives: [
      shape('backplate', 7, 0, 0, 1500, 780, '#FF182235', 100, 0, 900, 24),
      shape('candidate_left', 8, -545, -70, 360, 260, '#FF748095', 92, 0, 540, 18),
      shape('candidate_right', 8, 545, -70, 360, 260, '#FF748095', 92, 0, 540, 18),
      shape('selected_sheet', 8, 0, -30, 850, 560, '#FFFFFEF4', 100, 120, 780, 24),
      shape('sheet_header', 8, 0, -270, 780, 82, '#FF3977C4', 100, 180, 720, 14),
      shape('condition_axis_1', 8, -70, -145, 620, 44, '#FFE0EAF8', 100, 260, 640, 8),
      shape('condition_axis_2', 8, -70, -45, 620, 44, '#FFCEDCF0', 100, 320, 580, 8),
      shape('condition_axis_3', 8, -70, 55, 620, 44, '#FFBFD0E8', 100, 380, 520, 8),
      shape('funnel_left', 8, -270, 175, 500, 46, '#FF63D48A', 100, 480, 420, 10),
      shape('funnel_right', 8, 270, 175, 500, 46, '#FF63D48A', 100, 480, 420, 10),
      shape('drawback_callout', 8, 360, 150, 380, 180, '#FFFFB14A', 100, 540, 360, 22),
      shape('selection_overlay', 8, 0, -30, 920, 620, '#2270FFB0', 100, 600, 300, 24),
      text('headline', 9, 0, 318, 46, '一つに絞る', textColor, 0, 900),
      text('selected_label', 9, 0, -286, 40, '選定', textColor, 220, 680),
      text('drawback_label', 9, 360, 120, 38, '注意点', '#FF302000', 560, 340),
    ],
  },
  {
    beat_id: 'micro-03-ai-match',
    candidate_id: 'RE-07D-beginning',
    start_frame: 1800,
    duration_frames: 900,
    narrative_intent: 'Viewer understands that an AI-like system can confidently highlight one property as the best match.',
    visual_composition: 'A dark AI system panel scans, a match arrow fires, and a single property card becomes the focal target with a confidence badge.',
    on_screen_copy: ['照合して選ぶ', '推奨物件', '高一致'],
    why_avoids_whiteboard: 'The beat is a scanning and targeting event with one highlighted card, not a board of explanatory labels.',
    minimal_render_readiness_basis: 'AI targeting relation reads visually through scan bars, arrow, and match badge',
    primitives: [
      shape('backplate', 7, 0, 0, 1500, 780, '#FF07172A', 100, 0, 900, 24),
      shape('ai_panel', 8, -440, -35, 640, 540, '#FF17304F', 100, 0, 900, 24),
      shape('scan_bar_1', 8, -440, -205, 520, 48, '#FF6BFFB5', 100, 110, 580, 8),
      shape('scan_bar_2', 8, -440, -85, 470, 48, '#FF54DCA0', 100, 230, 560, 8),
      shape('scan_bar_3', 8, -440, 35, 410, 48, '#FF42B786', 100, 350, 540, 8),
      shape('match_line', 8, 0, 30, 560, 52, '#FF6BFFB5', 100, 450, 450, 12),
      shape('match_arrow_head', 8, 245, 30, 110, 110, '#FF6BFFB5', 100, 450, 450, 14),
      shape('property_card', 8, 395, -35, 660, 510, '#FFFFFEF4', 100, 520, 380, 24),
      shape('property_image_block', 8, 395, -135, 560, 190, '#FFCBD7E6', 100, 560, 340, 18),
      shape('match_overlay', 8, 395, -35, 735, 585, '#2270FFB0', 100, 600, 300, 24),
      shape('confidence_badge', 8, 395, 150, 300, 92, '#FF63D48A', 100, 660, 240, 18),
      text('headline', 9, 0, 318, 46, '照合して選ぶ', textColor, 0, 900),
      text('property_label', 9, 395, -286, 40, '推奨物件', darkTextColor, 540, 360),
      text('confidence_label', 9, 395, 126, 38, '高一致', '#FF082614', 670, 230),
    ],
  },
  {
    beat_id: 'micro-04-conditional',
    candidate_id: 'RE-07D-development',
    start_frame: 2700,
    duration_frames: 900,
    narrative_intent: 'Viewer understands that the AI recommendation is not final because hidden real-estate risks interrupt it and make the choice conditional.',
    visual_composition: 'The matched property remains in the center, then red/yellow risk zones cover it and a dark conditional strip overrides the previous recommendation.',
    on_screen_copy: ['条件つき推薦', '境界', '相続', '周辺'],
    why_avoids_whiteboard: 'The beat uses interruption and occlusion: risk zones physically cover the recommendation instead of listing risk notes beside it.',
    minimal_render_readiness_basis: 'conditional recommendation reads as visual interruption, but needs GUI judgment before render smoke',
    primitives: [
      shape('backplate', 7, 0, 0, 1500, 780, '#FF1B0C14', 100, 0, 900, 24),
      shape('property_card', 8, 0, -55, 800, 520, '#FFFFFEF4', 100, 0, 900, 24),
      shape('ai_ok_bar', 8, 0, -285, 740, 82, '#FF6BFFB5', 100, 0, 420, 14),
      shape('warning_band', 8, 0, -15, 1120, 170, '#FFFFD36A', 100, 300, 600, 24),
      shape('risk_boundary', 8, -380, -60, 430, 190, '#FFFF5B5B', 100, 330, 570, 22),
      shape('risk_inheritance', 8, 0, 75, 430, 190, '#FFFFB14A', 100, 430, 470, 22),
      shape('risk_neighborhood', 8, 380, -60, 430, 190, '#FFFF5B5B', 100, 530, 370, 22),
      shape('interruption_overlay', 8, 0, -55, 920, 590, '#88210015', 100, 600, 300, 24),
      shape('conditional_strip', 8, 0, 255, 980, 102, '#FF070A12', 100, 660, 240, 14),
      text('headline', 9, 0, 318, 46, '条件つき推薦', textColor, 0, 900),
      text('boundary_label', 9, -380, -92, 38, '境界', warningTextColor, 340, 560),
      text('inheritance_label', 9, 0, 43, 38, '相続', '#FF302000', 460, 440),
      text('neighborhood_label', 9, 380, -92, 38, '周辺', warningTextColor, 580, 320),
    ],
  },
];

function shape(itemId, layer, x, y, width, height, color, opacity, offset, duration, round = 10) {
  return { kind: 'ShapeItem', item_id: itemId, layer, x, y, width, height, color, opacity, offset, duration, round };
}

function text(itemId, layer, x, y, fontSize, content, color, offset, duration) {
  return { kind: 'TextItem', item_id: itemId, layer, x, y, fontSize, content, color, offset, duration };
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

function setShapeSize(shapeItem, primitive) {
  shapeItem.ShapeParameter.SizeMode = shapeSizeMode;
  setShapeParameterValue(shapeItem, 'Size', Math.max(primitive.width, primitive.height));
  setShapeParameterValue(shapeItem, 'AspectRate', primitive.width / primitive.height);
  setShapeParameterValue(shapeItem, 'Width', primitive.width);
  setShapeParameterValue(shapeItem, 'Height', primitive.height);
  setShapeParameterValue(shapeItem, 'Round', primitive.round);
  setShapeParameterValue(shapeItem, 'StrokeThickness', 0);
}

function validateInputs(compactReview) {
  const candidates = compactReview.candidates || [];
  const candidateIds = new Set(candidates.map((candidate) => candidate.candidate_id));
  const errors = [];
  for (const candidateId of selectedCandidateIds) {
    if (!candidateIds.has(candidateId)) errors.push(`missing selected candidate ${candidateId}`);
  }
  if (sceneBeats.length < 3 || sceneBeats.length > 4) {
    errors.push(`scene beat count must be 3-4, got ${sceneBeats.length}`);
  }
  const totalDuration = sceneBeats.reduce((maxFrame, beat) => Math.max(maxFrame, beat.start_frame + beat.duration_frames), 0) / fps;
  if (totalDuration < 60 || totalDuration > 90) {
    errors.push(`scene duration must be 60-90 seconds, got ${totalDuration}`);
  }
  for (const beat of sceneBeats) {
    const textItems = beat.primitives.filter((primitive) => primitive.kind === 'TextItem');
    if (textItems.length > 4) {
      errors.push(`${beat.beat_id} has too many on-screen copy items: ${textItems.length}`);
    }
    if (beat.on_screen_copy.length > 4) {
      errors.push(`${beat.beat_id} on_screen_copy exceeds one headline plus three labels`);
    }
    const candidate = candidates.find((item) => item.candidate_id === beat.candidate_id);
    if (!candidate || candidate.actual_ymmp_patch_output_readiness !== 'ready') {
      errors.push(`${beat.candidate_id} is not ready`);
    }
    for (const primitive of beat.primitives) {
      if (![7, 8, 9].includes(primitive.layer)) {
        errors.push(`${beat.beat_id}/${primitive.item_id} uses unsafe layer ${primitive.layer}`);
      }
      if (primitive.offset < 0 || primitive.offset >= beat.duration_frames) {
        errors.push(`${beat.beat_id}/${primitive.item_id} invalid offset ${primitive.offset}`);
      }
      if (primitive.duration <= 0 || primitive.offset + primitive.duration > beat.duration_frames) {
        errors.push(`${beat.beat_id}/${primitive.item_id} invalid duration ${primitive.duration}`);
      }
    }
  }
  if (errors.length) {
    throw new Error(`MICRO_SCENE_INPUT_INVALID: ${errors.join('; ')}`);
  }
}

function sourceLineText(candidate) {
  const lines = candidate.source_reference?.source_line_range;
  return lines ? `${lines.line_start}-${lines.line_end}` : 'unknown';
}

function scopedItemId(beat, primitive) {
  const beatNumber = String(sceneBeats.indexOf(beat) + 1).padStart(2, '0');
  return `b${beatNumber}_${primitive.item_id}`;
}

function buildRemark(candidate, beat, primitive) {
  const beatNumber = String(sceneBeats.indexOf(beat) + 1).padStart(2, '0');
  return [
    'g27vis',
    `beat=${beatNumber}`,
    `candidate=${beat.candidate_id}`,
    `item_id=${scopedItemId(beat, primitive)}`,
    `lines=${sourceLineText(candidate)}`,
  ].join(' ');
}

function shapeRole(itemId) {
  if (itemId === 'backplate') return 'background';
  if (/(public_panel|private_panel|selected_sheet|ai_panel|property_card)/.test(itemId)) return 'focal_panel';
  if (/(arrow|lock|funnel|match|warning|risk|conditional|interruption|output_card|drawback)/.test(itemId)) return 'relation';
  return 'support';
}

function makeShapeItem(template, candidate, beat, primitive) {
  const item = clone(template);
  item.Frame = beat.start_frame + primitive.offset;
  item.Length = primitive.duration;
  item.Layer = primitive.layer;
  item.Group = 0;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Remark = buildRemark(candidate, beat, primitive);
  item.IsLocked = false;
  item.IsHidden = false;
  setAnimatedValue(item, 'X', primitive.x);
  setAnimatedValue(item, 'Y', primitive.y);
  setAnimatedValue(item, 'Z', 0);
  setAnimatedValue(item, 'Opacity', primitive.opacity);
  setAnimatedValue(item, 'Zoom', 100);
  setAnimatedValue(item, 'Rotation', 0);
  setShapeSize(item, primitive);
  setShapeBrushColor(item, primitive.color);
  return item;
}

function makeTextItem(candidate, beat, primitive) {
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
    Frame: beat.start_frame + primitive.offset,
    Layer: primitive.layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: primitive.duration,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: buildRemark(candidate, beat, primitive),
    IsLocked: false,
    IsHidden: false,
  };
}

function buildProbeProject(compactReview, carrierYmmp, shapeTemplateYmmp) {
  validateInputs(compactReview);
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
  for (const beat of sceneBeats) {
    const candidate = compactReview.candidates.find((item) => item.candidate_id === beat.candidate_id);
    for (const primitive of beat.primitives) {
      if (primitive.kind === 'ShapeItem') {
        items.push(makeShapeItem(shapeTemplate, candidate, beat, primitive));
      } else if (primitive.kind === 'TextItem') {
        items.push(makeTextItem(candidate, beat, primitive));
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
    const index = part.indexOf('=');
    if (index > 0) result[part.slice(0, index)] = part.slice(index + 1);
  });
  return result;
}

function animationValue(item, key) {
  return item?.[key]?.Values?.[0]?.Value;
}

function shapeParameterValue(item, key) {
  return item?.ShapeParameter?.[key]?.Values?.[0]?.Value;
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
  const lowered = key.toLowerCase();
  if (lowered.includes('color')) {
    return typeof value === 'string' && hexColorPattern.test(value)
      ? { status: 'pass', pattern: '#AARRGGBB string' }
      : { status: 'fail', pattern: 'Color-like key is not #AARRGGBB string' };
  }
  if (lowered.includes('brush')) {
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
    for (const [key, child] of Object.entries(value)) {
      const childPath = `${jsonPath}.${key}`;
      if (colorLikeTerms.some((term) => key.toLowerCase().includes(term))) {
        const pattern = colorPatternFor(key, child);
        const occurrence = {
          json_path: childPath,
          value_type: valueType(child),
          observed_compatible_pattern: pattern.pattern,
          status: pattern.status,
        };
        occurrences.push(occurrence);
        if (pattern.status === 'fail') failures.push(occurrence);
      }
      walk(child, childPath);
    }
  }
  items.forEach((item, index) => walk(item, `$.Timelines[0].Items[${index}]`));
  return { occurrences, failures };
}

function expectedItems() {
  return sceneBeats.flatMap((beat) =>
    beat.primitives.map((primitive) => ({
      beat_id: beat.beat_id,
      candidate_id: beat.candidate_id,
      item_id: scopedItemId(beat, primitive),
      item_type: primitive.kind,
      layer: primitive.layer,
      start_frame: beat.start_frame + primitive.offset,
      duration_frames: primitive.duration,
      primitive_id: primitive.item_id,
      role: primitive.kind === 'ShapeItem' ? shapeRole(primitive.item_id) : 'copy',
      x: primitive.x,
      y: primitive.y,
      opacity: primitive.opacity ?? 100,
      width: primitive.width ?? null,
      height: primitive.height ?? null,
      font_size: primitive.fontSize ?? null,
    })),
  );
}

function readbackProbe(compactReview, ymmp, carrierHashBefore, carrierHashAfter) {
  const timelineItems = Array.isArray(ymmp.Timelines?.[0]?.Items) ? ymmp.Timelines[0].Items : [];
  const probeItems = timelineItems
    .map((item, index) => {
      const remark = parseRemark(item.Remark);
      const itemId = remark.item_id || null;
      const primitiveId = itemId ? itemId.replace(/^b\d+_/, '') : null;
      const role = itemType(item) === 'ShapeItem' && primitiveId ? shapeRole(primitiveId) : 'copy';
      const candidateId = remark.candidate || remark.candidate_id || null;
      const beatNumber = remark.beat || null;
      const beat = beatNumber ? sceneBeats[Number(beatNumber) - 1] : null;
      const candidate = compactReview.candidates.find((entry) => entry.candidate_id === candidateId);
      return {
        index,
        item_type: itemType(item),
        beat_id: beat?.beat_id || remark.beat_id || null,
        candidate_id: candidateId,
        item_id: itemId,
        primitive_id: primitiveId,
        role,
        layer: item.Layer,
        start_frame: item.Frame,
        duration_frames: item.Length,
        x: animationValue(item, 'X') ?? null,
        y: animationValue(item, 'Y') ?? null,
        opacity: animationValue(item, 'Opacity') ?? null,
        zoom: animationValue(item, 'Zoom') ?? null,
        text: item.Text || null,
        font_color: item.FontColor || null,
        shape_size_mode: item.ShapeParameter?.SizeMode || null,
        shape_size: shapeParameterValue(item, 'Size') ?? null,
        shape_aspect_rate: shapeParameterValue(item, 'AspectRate') ?? null,
        shape_width: shapeParameterValue(item, 'Width') ?? null,
        shape_height: shapeParameterValue(item, 'Height') ?? null,
        shape_brush_color: item.ShapeParameter?.Brush?.Parameter?.Color || null,
        remark: item.Remark || '',
        source_reference_found: {
          probe_marker: String(item.Remark || '').includes('g27vis'),
          source_lines: Boolean(remark.lines || remark.source_lines),
        },
        detailed_provenance: {
          compact_patch_review: paths.compactReview,
          source_beat: candidate?.source_reference?.visual_treatment_beat_id || candidateId,
          source_line_range: candidate?.source_reference?.source_line_range || null,
          not_creative_acceptance: true,
          render_performed: false,
        },
      };
    })
    .filter((item) => item.remark.includes('g27vis'));

  const missingItems = [];
  const malformedItems = [];
  for (const expected of expectedItems()) {
    const found = probeItems.find((item) => item.item_id === expected.item_id);
    if (!found) {
      missingItems.push({ ...expected, reason: 'expected micro scene primitive item not found' });
      continue;
    }
    const mismatches = [];
    for (const field of ['beat_id', 'candidate_id', 'item_type', 'layer', 'start_frame', 'duration_frames']) {
      if (found[field] !== expected[field]) mismatches.push({ field, expected: expected[field], actual: found[field] });
    }
    if (!found.source_reference_found.probe_marker || !found.source_reference_found.source_lines) {
      mismatches.push({ field: 'source_reference', expected: 'compact review source and line range', actual: found.source_reference_found });
    }
    if (!['ShapeItem', 'TextItem'].includes(found.item_type)) {
      mismatches.push({ field: 'item_type_allowed', expected: 'ShapeItem/TextItem only', actual: found.item_type });
    }
    if (found.item_type === 'ShapeItem') {
      if (found.shape_size_mode !== shapeSizeMode) {
        mismatches.push({ field: 'ShapeParameter.SizeMode', expected: shapeSizeMode, actual: found.shape_size_mode });
      }
      if (found.shape_width !== expected.width || found.shape_height !== expected.height) {
        mismatches.push({
          field: 'ShapeParameter.WidthHeight',
          expected: { width: expected.width, height: expected.height },
          actual: { width: found.shape_width, height: found.shape_height },
        });
      }
      if (found.shape_aspect_rate === 0 || found.shape_size === 100) {
        mismatches.push({
          field: 'ShapeParameter.SizeAspectFallback',
          expected: 'Size/AspectRate should not be the old 100px square fallback',
          actual: { size: found.shape_size, aspect_rate: found.shape_aspect_rate },
        });
      }
      if (expected.role !== 'background' && found.opacity < 90) {
        mismatches.push({ field: 'Opacity', expected: '>=90 for visible scene elements', actual: found.opacity });
      }
    }
    if (found.item_type === 'TextItem' && !(typeof found.font_color === 'string' && hexColorPattern.test(found.font_color))) {
      mismatches.push({ field: 'FontColor', expected: '#AARRGGBB string', actual: found.font_color });
    }
    if (mismatches.length) malformedItems.push({ item_id: expected.item_id, candidate_id: expected.candidate_id, mismatches });
  }

  const colorScan = scanColorLikeFields(timelineItems);
  const beatSummaries = sceneBeats.map((beat) => {
    const items = probeItems.filter((item) => item.beat_id === beat.beat_id);
    const candidate = compactReview.candidates.find((item) => item.candidate_id === beat.candidate_id);
    const shapeCount = items.filter((item) => item.item_type === 'ShapeItem').length;
    const textCount = items.filter((item) => item.item_type === 'TextItem').length;
    const focalPanelCount = items.filter((item) => item.role === 'focal_panel').length;
    const relationElementCount = items.filter((item) => item.role === 'relation').length;
    const largestPanelArea = Math.max(
      0,
      ...items
        .filter((item) => item.role === 'focal_panel')
        .map((item) => (item.shape_width || 0) * (item.shape_height || 0)),
    );
    const missing = missingItems.filter((item) => item.beat_id === beat.beat_id);
    const malformed = malformedItems.filter((item) => item.beat_id === beat.beat_id);
    const visibilityIssues = [];
    if (focalPanelCount < 1) visibilityIssues.push('missing focal panel');
    if (relationElementCount < 2) visibilityIssues.push('insufficient relation elements');
    if (largestPanelArea < 250000) visibilityIssues.push(`largest focal panel area too small: ${largestPanelArea}`);
    return {
      beat_id: beat.beat_id,
      candidate_id: beat.candidate_id,
      classification: missing.length || malformed.length || visibilityIssues.length ? 'fix required' : 'pass',
      narrative_intent: beat.narrative_intent,
      visual_composition: beat.visual_composition,
      on_screen_copy: beat.on_screen_copy,
      why_avoids_slideshow_whiteboard_effect: beat.why_avoids_whiteboard,
      source_line_range: candidate?.source_reference?.source_line_range || null,
      start_frame: beat.start_frame,
      duration_frames: beat.duration_frames,
      shape_item_count: shapeCount,
      text_item_count: textCount,
      focal_panel_count: focalPanelCount,
      relation_element_count: relationElementCount,
      largest_focal_panel_area: largestPanelArea,
      visibility_issues: visibilityIssues,
      missing_item_count: missing.length,
      malformed_item_count: malformed.length,
    };
  });

  const status =
    missingItems.length === 0 &&
    malformedItems.length === 0 &&
    colorScan.failures.length === 0 &&
    beatSummaries.every((beat) => beat.classification === 'pass')
      ? 'passed'
      : 'failed';

  return {
    artifact_type: 'g27_micro_scene_visibility_probe_readback',
    status,
    source: {
      compact_patch_review: paths.compactReview,
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_probe_ymmp: paths.outputYmmp,
    },
    boundary: {
      micro_scene_visibility_fix_only: true,
      previous_gui_review_result: {
        openability: 'pass',
        timeline_placement: 'pass',
        scene_visibility: 'fail',
        minimal_render_readiness: 'no',
      },
      selected_candidate_ids: selectedCandidateIds,
      not_selected_candidate_ids: notSelectedCandidateIds,
      shape_item_text_item_only: true,
      same_4_beats_as_previous_micro_scene: true,
      same_source_references: true,
      shape_size_mode: shapeSizeMode,
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
    timeline: {
      fps,
      beat_count: sceneBeats.length,
      duration_frames: Math.max(...timelineItems.map((item) => item.Frame + item.Length), 0),
      duration_sec: Math.max(...timelineItems.map((item) => item.Frame + item.Length), 0) / fps,
    },
    totals: {
      expected_item_count: expectedItems().length,
      inserted_probe_item_count: probeItems.length,
      inserted_shape_item_count: probeItems.filter((item) => item.item_type === 'ShapeItem').length,
      inserted_text_item_count: probeItems.filter((item) => item.item_type === 'TextItem').length,
      missing_item_count: missingItems.length,
      malformed_item_count: malformedItems.length,
      color_like_occurrence_count: colorScan.occurrences.length,
      color_like_failure_count: colorScan.failures.length,
    },
    beat_summaries: beatSummaries,
    items: probeItems,
    color_like_scan: colorScan,
    missing_items: missingItems,
    malformed_items: malformedItems,
    minimal_render_smoke_recommendation:
      'not_ready_until_user_gui_review_confirms_visibility_fix',
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Micro Scene Visibility Probe');
  lines.push('');
  lines.push(`Probe: \`${readback.source.generated_probe_ymmp}\``);
  lines.push(`Source compact review: \`${readback.source.compact_patch_review}\``);
  lines.push('');
  lines.push('This bounded probe fixes the GUI visibility failure from the previous micro scene without changing the 4 beats, source references, 60-second structure, or ShapeItem/TextItem-only boundary. It is not rendered, not creative acceptance, and not production-ready.');
  lines.push('');
  lines.push('Root cause addressed: the previous ShapeItems inherited `SizeMode=SizeAspect`, `Size=100`, and `AspectRate=0`, so large Width/Height values were not materially visible in YMM4 preview. This revision writes `SizeMode=WidthHeight`, large focal panels, high opacity, and explicit relation elements.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Readback status: \`${readback.status}\``);
  lines.push(`- Timeline duration: \`${readback.timeline.duration_sec}\` sec`);
  lines.push(`- Inserted items: \`${readback.totals.inserted_probe_item_count}\` (` +
    `ShapeItem=\`${readback.totals.inserted_shape_item_count}\`, TextItem=\`${readback.totals.inserted_text_item_count}\`)`);
  lines.push(`- Shape size mode: \`${readback.boundary.shape_size_mode}\``);
  lines.push(`- Color-like scan failures: \`${readback.totals.color_like_failure_count}\``);
  lines.push(`- Carrier modified in place: \`${readback.source_integrity.carrier_modified_in_place}\``);
  lines.push('');
  lines.push('## Beat Table');
  lines.push('');
  lines.push('| beat | candidate | focal / relation readback | narrative intent | visual composition | on-screen copy | why it avoids slideshow / whiteboard effect |');
  lines.push('| --- | --- | --- | --- | --- | --- | --- |');
  readback.beat_summaries.forEach((beat) => {
    lines.push(`| \`${beat.beat_id}\` | \`${beat.candidate_id}\` | focal=\`${beat.focal_panel_count}\`, relation=\`${beat.relation_element_count}\`, max_area=\`${beat.largest_focal_panel_area}\` | ${beat.narrative_intent} | ${beat.visual_composition} | ${beat.on_screen_copy.join(' / ')} | ${beat.why_avoids_slideshow_whiteboard_effect} |`);
  });
  lines.push('');
  lines.push('## Candidate Selection');
  lines.push('');
  lines.push(`- Selected candidates: \`${readback.boundary.selected_candidate_ids.join(', ')}\``);
  lines.push(`- Not selected in this micro scene: \`${readback.boundary.not_selected_candidate_ids.join(', ')}\``);
  lines.push('- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.');
  lines.push('');
  lines.push('## Completion Position');
  lines.push('');
  lines.push('- Technical openability: machine structure is ready for another user-side YMM4 GUI readback.');
  lines.push('- Semantic proxy: local readback keeps narrative intent, visual composition, and minimal on-screen copy separate.');
  lines.push('- Video adequacy: not proven until GUI review confirms each beat has one visible focal composition and reads as screen events.');
  lines.push('- Production readiness: no. No render, production timing, creative acceptance, external assets, URL fetch, TTS, or publishing.');
  lines.push(`- Minimal render smoke recommendation: \`${readback.minimal_render_smoke_recommendation}\`.`);
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback, markdown = null) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.timeline.duration_sec < 60 || readback.timeline.duration_sec > 90) failures.push('duration outside 60-90 sec');
  if (readback.boundary.selected_candidate_ids.length !== 4) failures.push('selected candidate count mismatch');
  if (readback.totals.inserted_probe_item_count !== readback.totals.expected_item_count) failures.push('item count mismatch');
  if (readback.totals.missing_item_count !== 0) failures.push('missing items present');
  if (readback.totals.malformed_item_count !== 0) failures.push(`malformed items present: ${JSON.stringify(readback.malformed_items.slice(0, 3))}`);
  if (readback.totals.color_like_failure_count !== 0) failures.push('color-like scan failures present');
  if (readback.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  for (const beat of readback.beat_summaries) {
    if (beat.on_screen_copy.length > 4) failures.push(`${beat.beat_id} has too much on-screen copy`);
    if (beat.text_item_count > 4) failures.push(`${beat.beat_id} has too many TextItems`);
    if (beat.focal_panel_count < 1) failures.push(`${beat.beat_id} lacks focal panel`);
    if (beat.relation_element_count < 2) failures.push(`${beat.beat_id} lacks relation elements`);
    if (beat.largest_focal_panel_area < 250000) failures.push(`${beat.beat_id} focal panel area too small`);
    if (beat.classification !== 'pass') failures.push(`${beat.beat_id} classification=${beat.classification}`);
  }
  if (markdown) {
    if (!markdown.includes('## Beat Table')) failures.push('report missing beat table');
    if (!markdown.includes('narrative intent')) failures.push('report missing narrative intent column');
    if (!markdown.includes('visual composition')) failures.push('report missing visual composition column');
    if (!markdown.includes('on-screen copy')) failures.push('report missing on-screen copy column');
  }
  if (failures.length) throw new Error(`G27_MICRO_SCENE_PROBE_READBACK_FAILED: ${failures.join('; ')}`);
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
      throw new Error('READBACK_DRIFT: existing micro scene readback JSON does not match probe .ymmp');
    }
  }

  console.log('G-27 micro scene visibility probe OK: 4 beats, 60 sec, ShapeItem/TextItem only, no render');
}

main();

// G-28 Map / Evidence Carrier diagnostic skeleton.
// Generates self-contained JSON/HTML/readback/MD artifacts only.
// No external images, URLs, render, creative acceptance, or production slot-fill.

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');

const OUT = {
  skeletonJson: 'samples/_probe/g28/map_evidence_carrier_skeleton.json',
  readbackJson: 'samples/_probe/g28/map_evidence_carrier_skeleton_readback.json',
  html: 'samples/_probe/g28/map_evidence_carrier_skeleton.html',
  reportMd: 'samples/_probe/g28/map_evidence_carrier_skeleton_report.md',
};

const FRAME = { width: 1920, height: 1080 };
const REGIONS = {
  outer_safe: { x: 96, y: 54, width: 1728, height: 972 },
  title_area: { x: 96, y: 54, width: 1728, height: 96 },
  main_canvas: { x: 96, y: 150, width: 1728, height: 660 },
  caption_reserve: { x: 0, y: 810, width: 1920, height: 216 },
  bottom_outer_safe: { x: 0, y: 1026, width: 1920, height: 54 },
};

const SKELETON = {
  artifact_id: 'g28_map_evidence_carrier_skeleton_v1',
  artifact_type: 'diagnostic_carrier_skeleton',
  archetype: 'Map / Evidence Carrier',
  diagnostic_only: true,
  production_candidate: false,
  creative_final_acceptance: false,
  production_render: false,
  slot_fill: false,
  ymmp_generation: 'not_generated_boundary',
  external_assets: {
    image_binary: false,
    image_path: false,
    image_url: false,
    raw_reference: false,
  },
  frame_contract: {
    aspect_ratio: '16:9',
    width: FRAME.width,
    height: FRAME.height,
    outer_safe_margin_pct: 5,
    caption_reserve_pct: 20,
    title_area: REGIONS.title_area,
    main_canvas: REGIONS.main_canvas,
    caption_reserve: REGIONS.caption_reserve,
  },
  scs_mapping: {
    archetype: 'Map / Evidence Carrier',
    composition_type: 'center-focal',
    composition_rationale: 'A single map/evidence surface is the focal argument surface; annotation slots support it without becoming equal-weight cards.',
    visual_roles: {
      focal_anchor: ['G28_MEC_EvidenceSurface'],
      supporting: [
        'G28_MEC_AnnotationSlot_1',
        'G28_MEC_AnnotationSlot_2',
        'G28_MEC_AnnotationSlot_3',
        'G28_MEC_SourceNote',
      ],
      boundary: [],
      connector: ['G28_MEC_LabelAnchor_1', 'G28_MEC_LabelAnchor_2', 'G28_MEC_LeaderLine_1'],
      risk_marker: [],
      decoration: ['G28_MEC_Stage', 'G28_MEC_Host_Left', 'G28_MEC_Host_Right'],
      label: ['G28_MEC_Title_Text', 'G28_MEC_SourceNote_Text'],
    },
    reading_order: [
      'G28_MEC_Title_Text',
      'G28_MEC_EvidenceSurface',
      'G28_MEC_LabelAnchor_1',
      'G28_MEC_LabelAnchor_2',
      'G28_MEC_AnnotationSlot_1',
      'G28_MEC_AnnotationSlot_2',
      'G28_MEC_AnnotationSlot_3',
      'G28_MEC_SourceNote_Text',
    ],
    in_frame_text_budget: {
      labels: 2,
      chars: 16,
      active_text_items: ['G28_MEC_Title_Text', 'G28_MEC_SourceNote_Text'],
      annotation_slots_are_empty_until_slot_fill: true,
    },
    expected_anti_patterns: [
      'map_label_overload',
      'source_note_overload',
      'indexed_whiteboard',
      'tiny_text',
      'subtitle_collision',
      'decorative_map_without_argument',
    ],
  },
  groups: [
    group('G28_MEC_Stage', 'decoration', 1, 'dark low-salience stage and safe frame'),
    group('G28_MEC_TitleBand', 'label', 2, 'one-line map/evidence claim area'),
    group('G28_MEC_EvidenceSurface', 'focal_anchor', 3, 'abstract map/evidence surface, not an image asset'),
    group('G28_MEC_Annotations', 'supporting', 4, 'three bounded annotation slots and label anchors'),
    group('G28_MEC_SourceNote', 'supporting', 5, 'short bounded source note area'),
    group('G28_MEC_Hosts', 'decoration', 6, 'lower-corner host placeholders, not focal'),
  ],
  semantic_elements: [
    'G28_MEC_Stage',
    'G28_MEC_Title_Text',
    'G28_MEC_EvidenceSurface',
    'G28_MEC_LabelAnchor_1',
    'G28_MEC_LabelAnchor_2',
    'G28_MEC_AnnotationSlot_1',
    'G28_MEC_AnnotationSlot_2',
    'G28_MEC_AnnotationSlot_3',
    'G28_MEC_SourceNote',
    'G28_MEC_Host_Left',
    'G28_MEC_Host_Right',
  ],
  items: [
    item('G28_MEC_BG_Stage', 'ShapeItem', 'G28_MEC_Stage', 'decoration', 1, rect(0, 0, 1920, 1080), { fill: '#FF0F172A', stroke: '#FF0F172A' }),
    item('G28_MEC_TitleBand_BG', 'ShapeItem', 'G28_MEC_TitleBand', 'label', 2, rect(96, 54, 1728, 96), { fill: '#FF1F2937', stroke: '#FF64748B' }),
    item('G28_MEC_Title_Text', 'TextItem', 'G28_MEC_TitleBand', 'label', 3, rect(706, 78, 508, 56), { text: '地域差を証拠で見る', font_size: 56, fill: '#FFF8FAFC' }),

    item('G28_MEC_EvidenceSurface', 'ShapeItem', 'G28_MEC_EvidenceSurface', 'focal_anchor', 4, rect(240, 180, 1440, 500), { fill: '#FF12263A', stroke: '#FF7DD3FC' }),
    item('G28_MEC_LabelAnchor_1', 'ShapeItem', 'G28_MEC_Annotations', 'connector', 5, rect(620, 350, 24, 24), { fill: '#FFFACC15', stroke: '#FFFEF08A' }),
    item('G28_MEC_LabelAnchor_2', 'ShapeItem', 'G28_MEC_Annotations', 'connector', 5, rect(1210, 430, 24, 24), { fill: '#FFFACC15', stroke: '#FFFEF08A' }),
    item('G28_MEC_LeaderLine_1', 'ShapeItem', 'G28_MEC_Annotations', 'connector', 6, rect(645, 360, 320, 8), { fill: '#FFFEF08A', stroke: '#FFFEF08A' }),

    item('G28_MEC_AnnotationSlot_1', 'ShapeItem', 'G28_MEC_Annotations', 'supporting', 7, rect(270, 710, 300, 72), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),
    item('G28_MEC_AnnotationSlot_2', 'ShapeItem', 'G28_MEC_Annotations', 'supporting', 7, rect(610, 710, 300, 72), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),
    item('G28_MEC_AnnotationSlot_3', 'ShapeItem', 'G28_MEC_Annotations', 'supporting', 7, rect(950, 710, 300, 72), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),

    item('G28_MEC_SourceNote_BG', 'ShapeItem', 'G28_MEC_SourceNote', 'supporting', 8, rect(1290, 718, 300, 56), { fill: '#FF111827', stroke: '#FF94A3B8' }),
    item('G28_MEC_SourceNote_Text', 'TextItem', 'G28_MEC_SourceNote', 'label', 9, rect(1334, 732, 212, 36), { text: '出典確認済み', font_size: 32, fill: '#FFE2E8F0' }),

    item('G28_MEC_Host_Left', 'ShapeItem', 'G28_MEC_Hosts', 'decoration', 10, rect(112, 655, 204, 145), { fill: '#FF4B5563', stroke: '#FFD1D5DB' }),
    item('G28_MEC_Host_Right', 'ShapeItem', 'G28_MEC_Hosts', 'decoration', 10, rect(1604, 655, 204, 145), { fill: '#FF4B5563', stroke: '#FFD1D5DB' }),
  ],
  reserved_areas: [
    {
      id: 'G28_MEC_CaptionReserve',
      role: 'caption_reserve',
      rect: REGIONS.caption_reserve,
      patch_forbidden: true,
      note: 'Bottom 20% reserved for YMM4 captions / thesis band. Main items must not overlap.',
    },
  ],
  diagnostic_semantics: {
    primary_uses: ['map', 'statistics', 'industrial_location', 'company_distribution', 'population_market_regional_difference', 'source_backed_argument'],
    annotation_slot_count_min: 2,
    annotation_slot_count_max: 4,
    source_note_area_exists: true,
    source_note_policy: 'short bounded provenance note only; not a source body or URL field',
    dense_table: false,
    indexed_whiteboard: false,
    tiny_text: false,
    decorative_map_without_argument: false,
    external_image_count: 0,
    external_url_count: 0,
    token_like_pattern_count: 0,
  },
  patch_boundary: {
    allowed_in_diagnostic_next_slice: [
      'review annotation slot semantics',
      'toggle annotation slot visibility',
      'fill at most two in-frame text slots after text-budget validation',
    ],
    forbidden_until_production_carrier: [
      'add real map or satellite image assets',
      'record image paths or URLs',
      'change caption reserve',
      'claim creative final acceptance',
      'render production output',
      'generate a YMM4 project file',
      'promote G-27 diagnostic evidence into G-28',
    ],
  },
};

function group(id, role, layer, note) {
  return { id, role, layer, note };
}

function rect(x, y, width, height) {
  return { x, y, width, height };
}

function item(id, itemType, groupId, role, layer, rectValue, style) {
  const center = {
    x: rectValue.x + rectValue.width / 2 - FRAME.width / 2,
    y: rectValue.y + rectValue.height / 2 - FRAME.height / 2,
  };
  return {
    id,
    item_type: itemType,
    group_id: groupId,
    semantic_role: role,
    layer,
    rect: rectValue,
    ymm4_center_origin: center,
    size_mode: itemType === 'ShapeItem' ? 'WidthHeight' : undefined,
    style,
  };
}

function abs(rel) {
  return path.join(root, rel);
}

function writeText(rel, text) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), text, 'utf8');
}

function writeJson(rel, payload) {
  writeText(rel, `${JSON.stringify(payload, null, 2)}\n`);
}

function rectBottom(r) {
  return r.y + r.height;
}

function rectRight(r) {
  return r.x + r.width;
}

function overlaps(a, b) {
  return !(rectRight(a) <= b.x || rectRight(b) <= a.x || rectBottom(a) <= b.y || rectBottom(b) <= a.y);
}

function inRegion(r, region) {
  return r.x >= region.x && r.y >= region.y && rectRight(r) <= rectRight(region) && rectBottom(r) <= rectBottom(region);
}

function countMatches(text, pattern) {
  const matches = text.match(pattern);
  return matches ? matches.length : 0;
}

function externalImageReferencePattern() {
  const drivePath = '[A-Za-z]' + ':\\\\';
  const imageExts = ['pn' + 'g', 'jp' + 'e?g', 'we' + 'bp', 'gi' + 'f', 'bm' + 'p']
    .map((ext) => `\\.${ext}\\b`)
    .join('|');
  return new RegExp(`(?:${drivePath}|${imageExts})`, 'gi');
}

function tokenLikePattern() {
  const secretPrefix = 's' + 'k-';
  const bearerWord = 'Bear' + 'er';
  const privateKey = 'PRIVATE ' + 'KEY';
  return new RegExp(`\\b(?:${secretPrefix}[A-Za-z0-9_-]{8,}|${bearerWord}\\s+[A-Za-z0-9._-]{8,}|BEGIN [A-Z ]*${privateKey})\\b`, 'g');
}

function validate() {
  const items = SKELETON.items;
  const semanticGroups = new Set(items.map((entry) => entry.group_id));
  const annotationSlots = items.filter((entry) => entry.id.startsWith('G28_MEC_AnnotationSlot_'));
  const sourceNoteItems = items.filter((entry) => entry.group_id === 'G28_MEC_SourceNote');
  const captionOverlaps = items.filter((entry) => (
    entry.id !== 'G28_MEC_BG_Stage' &&
    overlaps(entry.rect, REGIONS.caption_reserve)
  ));
  const mainContentItems = items.filter((entry) => !entry.id.includes('BG_Stage') && !entry.id.includes('Title'));
  const outsideMain = mainContentItems.filter((entry) => (
    !entry.id.startsWith('G28_MEC_Host_') &&
    !inRegion(entry.rect, REGIONS.main_canvas)
  ));
  const shapeItems = items.filter((entry) => entry.item_type === 'ShapeItem');
  const textItems = items.filter((entry) => entry.item_type === 'TextItem');
  const sourceNoteText = items.find((entry) => entry.id === 'G28_MEC_SourceNote_Text');
  const textChars = textItems.reduce((sum, entry) => sum + [...(entry.style.text || '')].length, 0);
  const smallestTextSize = Math.min(...textItems.map((entry) => entry.style.font_size || 0));
  const serializedArtifact = JSON.stringify(SKELETON);
  const externalUrlCount = countMatches(serializedArtifact, /https?:\/\//gi);
  const externalImageCount = countMatches(serializedArtifact, externalImageReferencePattern());
  const tokenLikePatternCount = countMatches(serializedArtifact, tokenLikePattern());
  const evidenceSurface = items.find((entry) => entry.id === 'G28_MEC_EvidenceSurface');
  const checks = {
    diagnostic_only: SKELETON.diagnostic_only === true,
    production_candidate_false: SKELETON.production_candidate === false,
    no_external_image_or_url: Object.values(SKELETON.external_assets).every((v) => v === false),
    ymmp_not_generated: SKELETON.ymmp_generation === 'not_generated_boundary',
    frame_16_9_1920_1080: FRAME.width === 1920 && FRAME.height === 1080,
    caption_reserve_bottom_20pct: REGIONS.caption_reserve.height === 216 && REGIONS.caption_reserve.y === 810,
    caption_reserve_clear: captionOverlaps.length === 0,
    evidence_area_in_main_canvas: inRegion(evidenceSurface.rect, REGIONS.main_canvas),
    annotation_slot_count_2_to_4: annotationSlots.length >= 2 && annotationSlots.length <= 4,
    source_note_area_exists: sourceNoteItems.length >= 2 && sourceNoteText?.item_type === 'TextItem',
    source_note_text_budget_bounded: sourceNoteText && [...sourceNoteText.style.text].length <= 12 && sourceNoteText.style.font_size >= 28,
    host_role_non_focal: !SKELETON.scs_mapping.visual_roles.focal_anchor.some((id) => id.includes('Host')),
    dense_table_false: SKELETON.diagnostic_semantics.dense_table === false,
    indexed_whiteboard_false: SKELETON.diagnostic_semantics.indexed_whiteboard === false,
    tiny_text_false_or_bounded: SKELETON.diagnostic_semantics.tiny_text === false && smallestTextSize >= 28,
    decorative_map_without_argument_false: SKELETON.diagnostic_semantics.decorative_map_without_argument === false,
    primitive_item_count_bounded: items.length <= 14,
    semantic_element_count_bounded: SKELETON.semantic_elements.length <= 14,
    shape_size_mode_widthheight: shapeItems.every((entry) => entry.size_mode === 'WidthHeight'),
    in_frame_text_budget: textItems.length === 2 && textChars <= 30,
    no_main_content_outside_main_canvas_except_hosts: outsideMain.length === 0,
    external_image_count_zero: externalImageCount === 0 && SKELETON.diagnostic_semantics.external_image_count === 0,
    external_url_count_zero: externalUrlCount === 0 && SKELETON.diagnostic_semantics.external_url_count === 0,
    token_like_pattern_count_zero: tokenLikePatternCount === 0 && SKELETON.diagnostic_semantics.token_like_pattern_count === 0,
    image_path_false: SKELETON.external_assets.image_path === false,
    image_url_false: SKELETON.external_assets.image_url === false,
    raw_reference_false: SKELETON.external_assets.raw_reference === false,
  };
  const failed = Object.entries(checks).filter(([, ok]) => !ok).map(([name]) => name);
  return {
    artifact_id: SKELETON.artifact_id,
    status: failed.length === 0 ? 'passed' : 'failed',
    diagnostic_only: SKELETON.diagnostic_only,
    production_candidate: SKELETON.production_candidate,
    generated_files: OUT,
    totals: {
      primitive_item_count: items.length,
      shape_item_count: shapeItems.length,
      text_item_count: textItems.length,
      semantic_group_count: semanticGroups.size,
      semantic_element_count: SKELETON.semantic_elements.length,
      annotation_slot_count: annotationSlots.length,
      caption_overlap_count: captionOverlaps.length,
      text_chars: textChars,
      smallest_text_size: smallestTextSize,
    },
    checks,
    failures: failed,
    scs_readback: {
      archetype: SKELETON.scs_mapping.archetype,
      composition_type: SKELETON.scs_mapping.composition_type,
      composition_rationale: SKELETON.scs_mapping.composition_rationale,
      visual_roles: SKELETON.scs_mapping.visual_roles,
      reading_order: SKELETON.scs_mapping.reading_order,
    },
    layer_order: items.slice().sort((a, b) => a.layer - b.layer).map((entry) => ({
      layer: entry.layer,
      id: entry.id,
      item_type: entry.item_type,
      group_id: entry.group_id,
      semantic_role: entry.semantic_role,
    })),
    caption_reserve_readback: {
      rect: REGIONS.caption_reserve,
      clear: captionOverlaps.length === 0,
      overlaps: captionOverlaps.map((entry) => entry.id),
    },
    focal_evidence_area_readback: {
      id: 'G28_MEC_EvidenceSurface',
      composition_type: SKELETON.scs_mapping.composition_type,
      rect: evidenceSurface.rect,
      in_main_canvas: checks.evidence_area_in_main_canvas,
    },
    annotation_readback: {
      count: annotationSlots.length,
      allowed_min: SKELETON.diagnostic_semantics.annotation_slot_count_min,
      allowed_max: SKELETON.diagnostic_semantics.annotation_slot_count_max,
      ids: annotationSlots.map((entry) => entry.id),
    },
    source_note_readback: {
      exists: checks.source_note_area_exists,
      text: sourceNoteText?.style.text || '',
      chars: sourceNoteText ? [...sourceNoteText.style.text].length : 0,
      font_size: sourceNoteText?.style.font_size || 0,
      bounded: checks.source_note_text_budget_bounded,
    },
    host_role_readback: {
      left: items.find((entry) => entry.id === 'G28_MEC_Host_Left').rect,
      right: items.find((entry) => entry.id === 'G28_MEC_Host_Right').rect,
      role: 'lower-corner decoration / emotional anchor, not focal',
      above_caption_reserve: ['G28_MEC_Host_Left', 'G28_MEC_Host_Right'].every((id) => rectBottom(items.find((entry) => entry.id === id).rect) <= REGIONS.caption_reserve.y),
    },
    safety_readback: {
      external_image_count: externalImageCount,
      external_url_count: externalUrlCount,
      token_like_pattern_count: tokenLikePatternCount,
      image_binary: SKELETON.external_assets.image_binary,
      image_path: SKELETON.external_assets.image_path,
      image_url: SKELETON.external_assets.image_url,
      raw_reference: SKELETON.external_assets.raw_reference,
    },
    text_budget_readback: {
      labels: textItems.length,
      chars: textChars,
      dense: false,
      tiny_text: SKELETON.diagnostic_semantics.tiny_text,
      smallest_text_size: smallestTextSize,
      visible_text_items: textItems.map((entry) => ({
        id: entry.id,
        text: entry.style.text,
        font_size: entry.style.font_size,
      })),
    },
    failure_modes: SKELETON.scs_mapping.expected_anti_patterns,
    limitations: [
      'No real map, satellite image, image path, or URL is used in this diagnostic skeleton.',
      'HTML is visualization-only and not a render or creative final acceptance.',
      'Annotation slots are empty placeholders until a later scoped slot-fill slice exists.',
      'No YMM4 .ymmp file is generated in this slice.',
    ],
  };
}

function cssColor(argb) {
  if (!/^#[0-9A-Fa-f]{8}$/.test(argb || '')) return '#000000';
  return `#${argb.slice(3)}`;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderHtml(readback) {
  const itemSvg = SKELETON.items
    .slice()
    .sort((a, b) => a.layer - b.layer)
    .map((entry) => {
      const r = entry.rect;
      if (entry.item_type === 'TextItem') {
        return `    <text data-id="${entry.id}" x="${r.x}" y="${r.y}" font-size="${entry.style.font_size}" fill="${cssColor(entry.style.fill)}" font-family="'Yu Gothic UI','Noto Sans CJK JP',sans-serif" font-weight="700" dominant-baseline="hanging">${escapeHtml(entry.style.text)}</text>`;
      }
      const rx = entry.id.includes('LabelAnchor') ? 12 : 12;
      return `    <rect data-id="${entry.id}" data-role="${entry.semantic_role}" x="${r.x}" y="${r.y}" width="${r.width}" height="${r.height}" rx="${rx}" fill="${cssColor(entry.style.fill)}" stroke="${cssColor(entry.style.stroke)}" stroke-width="4" />`;
    })
    .join('\n');
  const guides = [
    guideRect('outer-safe', REGIONS.outer_safe, '#E5E7EB', '8 8'),
    guideRect('title-area', REGIONS.title_area, '#FBBF24', '5 5'),
    guideRect('main-canvas', REGIONS.main_canvas, '#38BDF8', '5 5'),
    guideRect('caption-reserve', REGIONS.caption_reserve, '#F87171', '5 5', 'rgba(248,113,113,0.08)'),
  ].join('\n');
  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>G-28 Map / Evidence Carrier Skeleton</title>
  <style>
    body { margin: 0; background: #0b1120; color: #e5e7eb; font-family: 'Yu Gothic UI', sans-serif; }
    .meta { padding: 12px 20px; background: #111827; border-bottom: 1px solid #374151; font-size: 14px; line-height: 1.5; }
    svg { display: block; width: 1920px; height: 1080px; }
    code { color: #fbbf24; }
  </style>
</head>
<body>
  <div class="meta">
    <div><strong>G-28 Map / Evidence Carrier Skeleton</strong> / diagnostic_only=${readback.diagnostic_only} / production_candidate=${readback.production_candidate} / status=${readback.status}</div>
    <div>Visualization-only. No map image, no satellite image, no image path, no URL, no render, no creative final acceptance.</div>
    <div>Checks failed: <code>${readback.failures.length ? readback.failures.join(', ') : 'none'}</code></div>
    <div>Composition: <code>${readback.scs_readback.composition_type}</code> / annotations: <code>${readback.annotation_readback.count}</code> / source note bounded: <code>${readback.source_note_readback.bounded}</code></div>
  </div>
  <svg viewBox="0 0 1920 1080" aria-label="G-28 Map Evidence Carrier diagnostic skeleton">
${itemSvg}
${guides}
  </svg>
</body>
</html>`;
}

function guideRect(id, r, stroke, dash, fill = 'none') {
  return `    <rect data-guide="${id}" x="${r.x}" y="${r.y}" width="${r.width}" height="${r.height}" fill="${fill}" stroke="${stroke}" stroke-width="2" stroke-dasharray="${dash}" />`;
}

function renderReport(readback) {
  return `# G-28 Map / Evidence Carrier Skeleton Report

- artifact: ${SKELETON.artifact_id}
- status: ${readback.status}
- diagnostic_only: ${readback.diagnostic_only}
- production_candidate: ${readback.production_candidate}
- ymmp_generation: ${SKELETON.ymmp_generation}
- composition_type: ${readback.scs_readback.composition_type}
- primitive_item_count: ${readback.totals.primitive_item_count}
- semantic_group_count: ${readback.totals.semantic_group_count}
- semantic_element_count: ${readback.totals.semantic_element_count}
- annotation_slot_count: ${readback.totals.annotation_slot_count}
- source_note_exists: ${readback.source_note_readback.exists}
- source_note_bounded: ${readback.source_note_readback.bounded}
- caption_reserve_clear: ${readback.caption_reserve_readback.clear}
- dense_table: ${SKELETON.diagnostic_semantics.dense_table}
- indexed_whiteboard: ${SKELETON.diagnostic_semantics.indexed_whiteboard}
- tiny_text: ${SKELETON.diagnostic_semantics.tiny_text}
- external_image_count: ${readback.safety_readback.external_image_count}
- external_url_count: ${readback.safety_readback.external_url_count}
- token_like_pattern_count: ${readback.safety_readback.token_like_pattern_count}
- failures: ${readback.failures.length ? readback.failures.join(', ') : 'none'}

## Boundary

This is a diagnostic skeleton/readback artifact, not a production carrier. It
does not use a real map, satellite image, image asset, image path, URL, raw
reference, YMM4 project generation, render, production timing, or creative final
acceptance.

## SCS Mapping

- archetype: ${readback.scs_readback.archetype}
- composition_type: ${readback.scs_readback.composition_type}
- rationale: ${readback.scs_readback.composition_rationale}
- reading_order: ${readback.scs_readback.reading_order.join(' -> ')}

## Layer Order

${readback.layer_order.map((entry) => `- L${entry.layer}: ${entry.id} (${entry.item_type}, ${entry.semantic_role}, group=${entry.group_id})`).join('\n')}

## Readback

- evidence area: ${JSON.stringify(readback.focal_evidence_area_readback.rect)}, in_main_canvas=${readback.focal_evidence_area_readback.in_main_canvas}
- annotation slots: ${readback.annotation_readback.ids.join(', ')}
- source note: text=${readback.source_note_readback.text}, chars=${readback.source_note_readback.chars}, font_size=${readback.source_note_readback.font_size}
- host role: ${readback.host_role_readback.role}
- caption reserve: y=${REGIONS.caption_reserve.y}, h=${REGIONS.caption_reserve.height}, clear=${readback.caption_reserve_readback.clear}
- failure modes: ${readback.failure_modes.join(', ')}

## Limitations

${readback.limitations.map((entry) => `- ${entry}`).join('\n')}
`;
}

function main() {
  const readback = validate();
  if (writeOutputs) {
    writeJson(OUT.skeletonJson, SKELETON);
    writeJson(OUT.readbackJson, readback);
    writeText(OUT.html, renderHtml(readback));
    writeText(OUT.reportMd, renderReport(readback));
  }
  console.log(`artifact=${SKELETON.artifact_id}`);
  console.log(`status=${readback.status}`);
  console.log(`diagnostic_only=${readback.diagnostic_only}`);
  console.log(`production_candidate=${readback.production_candidate}`);
  console.log(`composition_type=${readback.scs_readback.composition_type}`);
  console.log(`primitive_item_count=${readback.totals.primitive_item_count}`);
  console.log(`semantic_group_count=${readback.totals.semantic_group_count}`);
  console.log(`semantic_element_count=${readback.totals.semantic_element_count}`);
  console.log(`annotation_slot_count=${readback.totals.annotation_slot_count}`);
  console.log(`source_note_bounded=${readback.source_note_readback.bounded}`);
  console.log(`caption_reserve_clear=${readback.caption_reserve_readback.clear}`);
  console.log(`external_image_count=${readback.safety_readback.external_image_count}`);
  console.log(`external_url_count=${readback.safety_readback.external_url_count}`);
  console.log(`token_like_pattern_count=${readback.safety_readback.token_like_pattern_count}`);
  if (readback.failures.length) {
    console.error(`failures=${readback.failures.join(',')}`);
    process.exitCode = 1;
  }
}

main();

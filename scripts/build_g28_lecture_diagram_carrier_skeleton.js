// G-28 Lecture Diagram Carrier diagnostic skeleton.
// Generates self-contained JSON/HTML/readback/MD artifacts only.
// No external images, URLs, render, creative acceptance, or production slot-fill.

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const writeOutputs = process.argv.includes('--write');
const SUPPORTED_VARIANTS = new Set(['real_estate_information_gap']);
const selectedVariant = parseVariantArg(process.argv);

const OUT = {
  skeletonJson: selectedVariant
    ? 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.json'
    : 'samples/_probe/g28/lecture_diagram_carrier_skeleton.json',
  readbackJson: selectedVariant
    ? 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_readback.json'
    : 'samples/_probe/g28/lecture_diagram_carrier_skeleton_readback.json',
  html: selectedVariant
    ? 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.html'
    : 'samples/_probe/g28/lecture_diagram_carrier_skeleton.html',
  reportMd: selectedVariant
    ? 'samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_report.md'
    : 'samples/_probe/g28/lecture_diagram_carrier_skeleton_report.md',
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
  artifact_id: 'g28_lecture_diagram_carrier_skeleton_v1',
  artifact_type: 'diagnostic_carrier_skeleton',
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
    archetype: 'Lecture Diagram Carrier',
    composition_type: 'center-focal',
    visual_roles: {
      focal_anchor: ['G28_LDC_FocalGroup'],
      supporting: [
        'G28_LDC_CalloutSlot_1',
        'G28_LDC_CalloutSlot_2',
        'G28_LDC_CalloutSlot_3',
      ],
      boundary: [],
      connector: ['G28_LDC_Connector_Left', 'G28_LDC_Connector_Right'],
      risk_marker: [],
      decoration: ['G28_LDC_Stage', 'G28_LDC_Host_Left', 'G28_LDC_Host_Right'],
      label: ['G28_LDC_Title_Text', 'G28_LDC_Focal_Label'],
    },
    reading_order: [
      'G28_LDC_Title_Text',
      'G28_LDC_Node_Left',
      'G28_LDC_Focal_Core',
      'G28_LDC_Node_Right',
      'G28_LDC_CalloutSlot_1',
      'G28_LDC_CalloutSlot_2',
      'G28_LDC_CalloutSlot_3',
    ],
    in_frame_text_budget: {
      labels: 2,
      chars: 12,
      active_text_items: ['G28_LDC_Title_Text', 'G28_LDC_Focal_Label'],
      callout_slots_are_empty_until_slot_fill: true,
    },
    expected_anti_patterns: [
      'indexed_whiteboard',
      'grid_overload',
      'information_overload',
      'host_as_focal',
      'subtitle_collision',
      'source_over_decoration',
    ],
  },
  groups: [
    group('G28_LDC_Stage', 'decoration', 1, 'dark low-salience stage and safe frame'),
    group('G28_LDC_TitleBand', 'label', 2, 'one-line chapter/title area'),
    group('G28_LDC_FocalGroup', 'focal_anchor', 3, 'central mechanism diagram and two internal nodes'),
    group('G28_LDC_CalloutSlots', 'supporting', 4, 'three optional callout slots, empty in diagnostic skeleton'),
    group('G28_LDC_Hosts', 'decoration', 5, 'lower-corner host placeholders, not focal'),
  ],
  semantic_elements: [
    'G28_LDC_Stage',
    'G28_LDC_Title_Text',
    'G28_LDC_FocalGroup',
    'G28_LDC_CalloutSlot_1',
    'G28_LDC_CalloutSlot_2',
    'G28_LDC_CalloutSlot_3',
    'G28_LDC_Host_Left',
    'G28_LDC_Host_Right',
  ],
  items: [
    item('G28_LDC_BG_Stage', 'ShapeItem', 'G28_LDC_Stage', 'decoration', 1, rect(0, 0, 1920, 1080), { fill: '#FF111827', stroke: '#FF111827' }),
    item('G28_LDC_TitleBand_BG', 'ShapeItem', 'G28_LDC_TitleBand', 'label', 2, rect(96, 54, 1728, 96), { fill: '#FF1F2937', stroke: '#FF6B7280' }),
    item('G28_LDC_Title_Text', 'TextItem', 'G28_LDC_TitleBand', 'label', 3, rect(706, 78, 508, 56), { text: '仕組みを一枚で見る', font_size: 56, fill: '#FFF9FAFB' }),

    item('G28_LDC_Focal_Core', 'ShapeItem', 'G28_LDC_FocalGroup', 'focal_anchor', 4, rect(560, 240, 800, 360), { fill: '#FF22324A', stroke: '#FF93C5FD' }),
    item('G28_LDC_Focal_Label', 'TextItem', 'G28_LDC_FocalGroup', 'label', 5, rect(820, 382, 280, 56), { text: '核心メカニズム', font_size: 56, fill: '#FFE0F2FE' }),
    item('G28_LDC_Node_Left', 'ShapeItem', 'G28_LDC_FocalGroup', 'internal_node', 6, rect(230, 330, 260, 140), { fill: '#FF374151', stroke: '#FFFBBF24' }),
    item('G28_LDC_Node_Right', 'ShapeItem', 'G28_LDC_FocalGroup', 'internal_node', 6, rect(1430, 330, 260, 140), { fill: '#FF374151', stroke: '#FFFBBF24' }),
    item('G28_LDC_Connector_Left', 'ShapeItem', 'G28_LDC_FocalGroup', 'connector', 7, rect(500, 395, 90, 10), { fill: '#FFFBBF24', stroke: '#FFFBBF24' }),
    item('G28_LDC_Connector_Right', 'ShapeItem', 'G28_LDC_FocalGroup', 'connector', 7, rect(1330, 395, 90, 10), { fill: '#FFFBBF24', stroke: '#FFFBBF24' }),

    item('G28_LDC_CalloutSlot_1', 'ShapeItem', 'G28_LDC_CalloutSlots', 'supporting', 8, rect(395, 650, 300, 86), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),
    item('G28_LDC_CalloutSlot_2', 'ShapeItem', 'G28_LDC_CalloutSlots', 'supporting', 8, rect(810, 650, 300, 86), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),
    item('G28_LDC_CalloutSlot_3', 'ShapeItem', 'G28_LDC_CalloutSlots', 'supporting', 8, rect(1225, 650, 300, 86), { fill: '#FF1E3A5F', stroke: '#FF60A5FA' }),

    item('G28_LDC_Host_Left', 'ShapeItem', 'G28_LDC_Hosts', 'decoration', 9, rect(112, 655, 204, 145), { fill: '#FF4B5563', stroke: '#FFD1D5DB' }),
    item('G28_LDC_Host_Right', 'ShapeItem', 'G28_LDC_Hosts', 'decoration', 9, rect(1604, 655, 204, 145), { fill: '#FF4B5563', stroke: '#FFD1D5DB' }),
  ],
  reserved_areas: [
    {
      id: 'G28_LDC_CaptionReserve',
      role: 'caption_reserve',
      rect: REGIONS.caption_reserve,
      patch_forbidden: true,
      note: 'Bottom 20% reserved for YMM4 captions / thesis band. Main items must not overlap.',
    },
  ],
  patch_boundary: {
    allowed_in_diagnostic_next_slice: [
      'toggle callout slot visibility',
      'fill callout text after text-budget validation',
      'produce theme variant JSON from this skeleton',
    ],
    forbidden_until_production_carrier: [
      'change frame grid',
      'move focal geometry',
      'move caption reserve',
      'add external image assets',
      'claim creative final acceptance',
      'render production output',
    ],
  },
};

if (selectedVariant === 'real_estate_information_gap') {
  applyRealEstateInformationGapVariant(SKELETON);
}

function parseVariantArg(argv) {
  const variantIndex = argv.indexOf('--variant');
  if (variantIndex < 0) return null;

  const value = argv[variantIndex + 1];
  if (!value || value.startsWith('--')) {
    console.error('Missing value for --variant. Supported: real_estate_information_gap');
    process.exit(1);
  }
  if (!SUPPORTED_VARIANTS.has(value)) {
    console.error(`Unsupported --variant value: ${value}`);
    console.error(`Supported variants: ${Array.from(SUPPORTED_VARIANTS).join(', ')}`);
    process.exit(1);
  }
  return value;
}

function applyRealEstateInformationGapVariant(artifact) {
  artifact.artifact_id = 'g28_lecture_diagram_carrier_real_estate_information_gap_v1';
  artifact.artifact_type = 'diagnostic_carrier_theme_variant';
  artifact.variant_id = 'g28_ldc_real_estate_information_gap';
  artifact.source_skeleton_artifact_id = 'g28_lecture_diagram_carrier_skeleton_v1';
  artifact.theme_variant = {
    id: 'g28_ldc_real_estate_information_gap',
    theme: 'real_estate_information_gap',
    diagnostic_only: true,
    production_candidate: false,
    slot_fill: false,
    production_render: false,
    creative_final_acceptance: false,
    composition_type: 'center-focal',
    focal_chain: [
      { id: 'G28_LDC_Node_Left', label: '元付情報', role: 'source' },
      { id: 'G28_LDC_Focal_Core', label: 'ポータル掲載', role: 'publication_surface' },
      { id: 'G28_LDC_Node_Right', label: '借主判断', role: 'viewer_decision' },
    ],
    callouts: [
      { slot: 'G28_LDC_CalloutSlot_1', label: '情報遅延' },
      { slot: 'G28_LDC_CalloutSlot_2', label: '掲載粒度の欠落' },
      { slot: 'G28_LDC_CalloutSlot_3', label: '仲介インセンティブ' },
    ],
    callout_text_policy: 'semantic labels only; slots are not text-filled in this diagnostic variant',
    dense_table: false,
    indexed_whiteboard: false,
    external_image_count: 0,
    external_url_count: 0,
    token_like_pattern_count: 0,
    forbidden_scope: [
      'G-27 carrier promotion',
      'production render',
      'creative final acceptance',
      'YMM4 project generation',
      'source footage intake',
      'external image or URL use',
      'RSS or NotebookLM source-pack work',
    ],
  };

  artifact.scs_mapping.composition_type = 'center-focal';
  artifact.scs_mapping.reading_order = [
    'G28_LDC_Title_Text',
    'G28_LDC_Node_Left',
    'G28_LDC_Focal_Core',
    'G28_LDC_Node_Right',
    'G28_LDC_CalloutSlot_1',
    'G28_LDC_CalloutSlot_2',
    'G28_LDC_CalloutSlot_3',
  ];
  artifact.scs_mapping.in_frame_text_budget.chars = 15;
  artifact.scs_mapping.in_frame_text_budget.theme_semantic_labels_are_not_slot_fill = true;

  const title = artifact.items.find((entry) => entry.id === 'G28_LDC_Title_Text');
  const focalLabel = artifact.items.find((entry) => entry.id === 'G28_LDC_Focal_Label');
  title.style.text = '情報非対称の流れ';
  focalLabel.style.text = '判断までの遅れ';

  artifact.patch_boundary.allowed_in_diagnostic_next_slice = [
    'review semantic labels against narration beat',
    'toggle callout slot visibility',
    'fill at most two in-frame text slots after text-budget validation',
  ];
  artifact.patch_boundary.forbidden_until_production_carrier.push(
    'treat this theme variant as a production carrier',
    'promote G-27 diagnostic evidence into G-28'
  );
}

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
  const activeCalloutSlots = items.filter((entry) => entry.id.startsWith('G28_LDC_CalloutSlot_'));
  const captionOverlaps = items.filter((entry) => (
    entry.id !== 'G28_LDC_BG_Stage' &&
    overlaps(entry.rect, REGIONS.caption_reserve)
  ));
  const mainContentItems = items.filter((entry) => !entry.id.includes('BG_Stage') && !entry.id.includes('Title'));
  const outsideMain = mainContentItems.filter((entry) => (
    !entry.id.startsWith('G28_LDC_Host_') &&
    !inRegion(entry.rect, REGIONS.main_canvas)
  ));
  const shapeItems = items.filter((entry) => entry.item_type === 'ShapeItem');
  const textItems = items.filter((entry) => entry.item_type === 'TextItem');
  const textChars = textItems.reduce((sum, entry) => sum + [...(entry.style.text || '')].length, 0);
  const groupCount = semanticGroups.size;
  const semanticElementCount = SKELETON.semantic_elements.length;
  const serializedArtifact = JSON.stringify(SKELETON);
  const externalUrlCount = countMatches(serializedArtifact, /https?:\/\//gi);
  const externalImageCount = countMatches(serializedArtifact, externalImageReferencePattern());
  const tokenLikePatternCount = countMatches(serializedArtifact, tokenLikePattern());
  const checks = {
    diagnostic_only: SKELETON.diagnostic_only === true,
    production_candidate_false: SKELETON.production_candidate === false,
    no_external_image_or_url: Object.values(SKELETON.external_assets).every((v) => v === false),
    ymmp_not_generated: SKELETON.ymmp_generation === 'not_generated_boundary',
    frame_16_9_1920_1080: FRAME.width === 1920 && FRAME.height === 1080,
    title_area_top_short: REGIONS.title_area.y >= 54 && rectBottom(REGIONS.title_area) <= 160,
    caption_reserve_bottom_20pct: REGIONS.caption_reserve.height === 216 && REGIONS.caption_reserve.y === 810,
    caption_reserve_clear: captionOverlaps.length === 0,
    focal_area_in_main_canvas: inRegion(SKELETON.items.find((entry) => entry.id === 'G28_LDC_Focal_Core').rect, REGIONS.main_canvas),
    host_placeholders_above_caption: ['G28_LDC_Host_Left', 'G28_LDC_Host_Right'].every((id) => rectBottom(items.find((entry) => entry.id === id).rect) <= REGIONS.caption_reserve.y),
    active_callout_slot_count_2_to_3: activeCalloutSlots.length >= 2 && activeCalloutSlots.length <= 3,
    semantic_element_count_8_to_14: semanticElementCount >= 8 && semanticElementCount <= 14,
    primitive_item_count_bounded: items.length <= 14,
    shape_size_mode_widthheight: shapeItems.every((entry) => entry.size_mode === 'WidthHeight'),
    in_frame_text_budget: textItems.length === 2 && textChars <= 30,
    no_indexed_whiteboard: activeCalloutSlots.length <= 3 && groupCount <= 14,
    no_main_content_outside_main_canvas_except_hosts: outsideMain.length === 0,
  };
  const variant = SKELETON.theme_variant;
  if (selectedVariant) {
    const focalChainLabels = (variant?.focal_chain || []).map((entry) => entry.label);
    const calloutLabels = (variant?.callouts || []).map((entry) => entry.label);
    Object.assign(checks, {
      variant_id_g28_ldc_real_estate_information_gap: SKELETON.variant_id === 'g28_ldc_real_estate_information_gap',
      variant_diagnostic_only: variant?.diagnostic_only === true,
      variant_production_candidate_false: variant?.production_candidate === false,
      variant_production_render_false: variant?.production_render === false,
      variant_slot_fill_false: variant?.slot_fill === false,
      variant_composition_center_focal: variant?.composition_type === 'center-focal' && SKELETON.scs_mapping.composition_type === 'center-focal',
      focal_chain_node_count_3: focalChainLabels.length === 3,
      focal_chain_labels_expected: ['元付情報', 'ポータル掲載', '借主判断'].every((label) => focalChainLabels.includes(label)),
      callout_count_2_to_3: calloutLabels.length >= 2 && calloutLabels.length <= 3,
      callout_labels_expected: ['情報遅延', '掲載粒度の欠落', '仲介インセンティブ'].every((label) => calloutLabels.includes(label)),
      host_role_non_focal: !SKELETON.scs_mapping.visual_roles.focal_anchor.some((id) => id.includes('Host')),
      dense_table_false: variant?.dense_table === false,
      indexed_whiteboard_false: variant?.indexed_whiteboard === false,
      external_image_count_zero: externalImageCount === 0 && variant?.external_image_count === 0,
      external_url_count_zero: externalUrlCount === 0 && variant?.external_url_count === 0,
      token_like_pattern_count_zero: tokenLikePatternCount === 0 && variant?.token_like_pattern_count === 0,
      text_budget_not_dense: textItems.length === 2 && textChars <= 30 && variant?.dense_table === false,
    });
  }
  const failed = Object.entries(checks).filter(([, ok]) => !ok).map(([name]) => name);
  const readback = {
    artifact_id: SKELETON.artifact_id,
    status: failed.length === 0 ? 'passed' : 'failed',
    diagnostic_only: SKELETON.diagnostic_only,
    production_candidate: SKELETON.production_candidate,
    generated_files: OUT,
    totals: {
      primitive_item_count: items.length,
      shape_item_count: shapeItems.length,
      text_item_count: textItems.length,
      semantic_group_count: groupCount,
      semantic_element_count: semanticElementCount,
      active_callout_slot_count: activeCalloutSlots.length,
      caption_overlap_count: captionOverlaps.length,
      text_item_count: textItems.length,
      text_chars: textChars,
    },
    checks,
    failures: failed,
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
    focal_area_readback: {
      id: 'G28_LDC_FocalGroup',
      composition_type: SKELETON.scs_mapping.composition_type,
      focal_core_rect: items.find((entry) => entry.id === 'G28_LDC_Focal_Core').rect,
      focal_core_in_main_canvas: checks.focal_area_in_main_canvas,
    },
    host_role_readback: {
      left: items.find((entry) => entry.id === 'G28_LDC_Host_Left').rect,
      right: items.find((entry) => entry.id === 'G28_LDC_Host_Right').rect,
      role: 'lower-corner decoration / emotional anchor, not focal',
      above_caption_reserve: checks.host_placeholders_above_caption,
    },
    callout_count_readback: {
      count: activeCalloutSlots.length,
      allowed_min: 2,
      allowed_max: 3,
      ids: activeCalloutSlots.map((entry) => entry.id),
    },
    limitations: [
      'No YMM4 .ymmp file generated in this slice because G-28 v0.1 still excludes zero-generation.',
      'HTML is visualization-only and not a render or creative final acceptance.',
      'Callout slots are empty placeholders until a theme-specific slot-fill slice exists.',
    ],
  };
  if (selectedVariant) {
    readback.variant_readback = {
      variant_id: SKELETON.variant_id,
      source_skeleton_artifact_id: SKELETON.source_skeleton_artifact_id,
      composition_type: SKELETON.scs_mapping.composition_type,
      focal_chain: variant.focal_chain,
      focal_chain_node_count: variant.focal_chain.length,
      callouts: variant.callouts,
      callout_count: variant.callouts.length,
      host_role: 'non-focal lower-corner decoration',
      dense_table: variant.dense_table,
      indexed_whiteboard: variant.indexed_whiteboard,
      semantic_labels_are_not_slot_fill: true,
    };
    readback.safety_readback = {
      external_image_count: externalImageCount,
      external_url_count: externalUrlCount,
      token_like_pattern_count: tokenLikePatternCount,
      image_binary: SKELETON.external_assets.image_binary,
      image_path: SKELETON.external_assets.image_path,
      image_url: SKELETON.external_assets.image_url,
      raw_reference: SKELETON.external_assets.raw_reference,
    };
    readback.text_budget_readback = {
      labels: textItems.length,
      chars: textChars,
      dense: false,
      dense_table: variant.dense_table,
      visible_text_items: textItems.map((entry) => ({
        id: entry.id,
        text: entry.style.text,
      })),
    };
    readback.layer_order_intent = [
      'low-salience stage',
      'title band boundary',
      'short title',
      'focal core',
      'focal label',
      'left/right internal nodes',
      'connectors',
      'three semantic callout slots',
      'non-focal lower-corner hosts',
    ];
  }
  return readback;
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
  const artifactLabel = selectedVariant
    ? 'G-28 Lecture Diagram Carrier Real Estate Information Gap Variant'
    : 'G-28 Lecture Diagram Carrier Skeleton';
  const ariaLabel = selectedVariant
    ? 'G-28 Lecture Diagram Carrier real estate information gap diagnostic variant'
    : 'G-28 Lecture Diagram Carrier diagnostic skeleton';
  const variantMeta = selectedVariant
    ? `
    <div>Variant: <code>${escapeHtml(readback.variant_readback.variant_id)}</code> / focal chain: <code>${escapeHtml(readback.variant_readback.focal_chain.map((entry) => entry.label).join(' -> '))}</code></div>
    <div>Callouts: <code>${escapeHtml(readback.variant_readback.callouts.map((entry) => entry.label).join(' / '))}</code> / semantic labels only, no slot-fill.</div>`
    : '';
  const itemSvg = SKELETON.items
    .slice()
    .sort((a, b) => a.layer - b.layer)
    .map((entry) => {
      const r = entry.rect;
      if (entry.item_type === 'TextItem') {
        return `    <text data-id="${entry.id}" x="${r.x}" y="${r.y}" font-size="${entry.style.font_size}" fill="${cssColor(entry.style.fill)}" font-family="'Yu Gothic UI','Noto Sans CJK JP',sans-serif" font-weight="700" dominant-baseline="hanging">${escapeHtml(entry.style.text)}</text>`;
      }
      return `    <rect data-id="${entry.id}" data-role="${entry.semantic_role}" x="${r.x}" y="${r.y}" width="${r.width}" height="${r.height}" rx="14" fill="${cssColor(entry.style.fill)}" stroke="${cssColor(entry.style.stroke)}" stroke-width="4" />`;
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
  <title>${artifactLabel}</title>
  <style>
    body { margin: 0; background: #0b1120; color: #e5e7eb; font-family: 'Yu Gothic UI', sans-serif; }
    .meta { padding: 12px 20px; background: #111827; border-bottom: 1px solid #374151; font-size: 14px; line-height: 1.5; }
    svg { display: block; width: 1920px; height: 1080px; }
    code { color: #fbbf24; }
  </style>
</head>
<body>
  <div class="meta">
    <div><strong>${artifactLabel}</strong> / diagnostic_only=${readback.diagnostic_only} / production_candidate=${readback.production_candidate} / status=${readback.status}</div>
    <div>Visualization-only. No image assets, no URL, no render, no creative final acceptance, no slot-fill.</div>
    <div>Checks failed: <code>${readback.failures.length ? readback.failures.join(', ') : 'none'}</code></div>${variantMeta}
  </div>
  <svg viewBox="0 0 1920 1080" aria-label="${ariaLabel}">
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
  const reportTitle = selectedVariant
    ? '# G-28 Lecture Diagram Carrier Real Estate Information Gap Variant Report'
    : '# G-28 Lecture Diagram Carrier Skeleton Report';
  const variantSection = selectedVariant
    ? `

## Variant Semantics

- variant_id: ${readback.variant_readback.variant_id}
- composition_type: ${readback.variant_readback.composition_type}
- focal_chain: ${readback.variant_readback.focal_chain.map((entry) => entry.label).join(' -> ')}
- callouts: ${readback.variant_readback.callouts.map((entry) => entry.label).join(', ')}
- host_role: ${readback.variant_readback.host_role}
- dense_table: ${readback.variant_readback.dense_table}
- indexed_whiteboard: ${readback.variant_readback.indexed_whiteboard}
- external_image_count: ${readback.safety_readback.external_image_count}
- external_url_count: ${readback.safety_readback.external_url_count}
- token_like_pattern_count: ${readback.safety_readback.token_like_pattern_count}
- text_budget_dense: ${readback.text_budget_readback.dense}

`
    : '\n\n';
  return `${reportTitle}

- artifact: ${SKELETON.artifact_id}
- status: ${readback.status}
- diagnostic_only: ${readback.diagnostic_only}
- production_candidate: ${readback.production_candidate}
- ymmp_generation: ${SKELETON.ymmp_generation}
- primitive_item_count: ${readback.totals.primitive_item_count}
- semantic_group_count: ${readback.totals.semantic_group_count}
- semantic_element_count: ${readback.totals.semantic_element_count}
- callout_slot_count: ${readback.totals.active_callout_slot_count}
- caption_reserve_clear: ${readback.caption_reserve_readback.clear}
- failures: ${readback.failures.length ? readback.failures.join(', ') : 'none'}

## Boundary

This is a diagnostic skeleton/readback artifact, not a production carrier. It
does not copy or transform reference images, does not use external image assets,
does not record image paths or URLs, does not generate a YMM4 project file, does
not render, and does not claim creative final acceptance.

## Layer Order

${readback.layer_order.map((entry) => `- L${entry.layer}: ${entry.id} (${entry.item_type}, ${entry.semantic_role}, group=${entry.group_id})`).join('\n')}

## Readback

- caption reserve: y=${REGIONS.caption_reserve.y}, h=${REGIONS.caption_reserve.height}, clear=${readback.caption_reserve_readback.clear}
- focal area: ${JSON.stringify(readback.focal_area_readback.focal_core_rect)}
- host role: ${readback.host_role_readback.role}
- callout slots: ${readback.callout_count_readback.ids.join(', ')}${variantSection}## Limitations

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
  console.log(`primitive_item_count=${readback.totals.primitive_item_count}`);
  console.log(`semantic_group_count=${readback.totals.semantic_group_count}`);
  console.log(`semantic_element_count=${readback.totals.semantic_element_count}`);
  console.log(`callout_slot_count=${readback.totals.active_callout_slot_count}`);
  console.log(`caption_reserve_clear=${readback.caption_reserve_readback.clear}`);
  if (selectedVariant) {
    console.log(`variant_id=${readback.variant_readback.variant_id}`);
    console.log(`focal_chain_node_count=${readback.variant_readback.focal_chain_node_count}`);
    console.log(`theme_callout_count=${readback.variant_readback.callout_count}`);
    console.log(`external_image_count=${readback.safety_readback.external_image_count}`);
    console.log(`external_url_count=${readback.safety_readback.external_url_count}`);
    console.log(`token_like_pattern_count=${readback.safety_readback.token_like_pattern_count}`);
  }
  if (readback.failures.length) {
    console.error(`failures=${readback.failures.join(',')}`);
    process.exitCode = 1;
  }
}

main();

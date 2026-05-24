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
  outputYmmp: 'samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp',
  readbackJson: 'samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.json',
  readbackMd: 'samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.md',
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
const textFontColor = '#FFF5F8FF';

function abs(relPath) {
  return path.join(root, relPath);
}

function readText(relPath) {
  return fs.readFileSync(abs(relPath), 'utf8').replace(/^\uFEFF/, '');
}

function readJson(relPath) {
  return JSON.parse(readText(relPath));
}

function readYmmp(relPath) {
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

function itemType(item) {
  return String(item?.$type || '').split(',')[0].split('.').pop();
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
    return;
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

function findFirstItemByType(ymmp, typeName) {
  const timelines = Array.isArray(ymmp.Timelines) ? ymmp.Timelines : [];
  for (const timeline of timelines) {
    const items = Array.isArray(timeline.Items) ? timeline.Items : [];
    const found = items.find((item) => itemType(item) === typeName);
    if (found) {
      return found;
    }
  }
  return null;
}

function validateCompactReview(compactReview) {
  const candidates = compactReview.candidates || [];
  const candidateIds = candidates.map((candidate) => candidate.candidate_id);
  const errors = [];
  if (candidates.length !== expectedCandidateIds.length) {
    errors.push(`expected 7 compact candidates, got ${candidates.length}`);
  }
  for (const id of expectedCandidateIds) {
    if (!candidateIds.includes(id)) {
      errors.push(`missing compact candidate ${id}`);
    }
  }
  for (const candidate of candidates) {
    if (candidate.actual_ymmp_patch_output_readiness !== 'ready') {
      errors.push(`${candidate.candidate_id} is not ready`);
    }
    const plannedItems = candidate.planned_items || [];
    const shapeCount = plannedItems.filter((item) => item.item_type === 'ShapeItem').length;
    const textCount = plannedItems.filter((item) => item.item_type === 'TextItem').length;
    if (shapeCount !== 2 || textCount !== 1) {
      errors.push(`${candidate.candidate_id} expected 2 ShapeItem + 1 TextItem, got ${shapeCount} + ${textCount}`);
    }
  }
  if (errors.length) {
    throw new Error(`COMPACT_REVIEW_INVALID: ${errors.join('; ')}`);
  }
}

function buildRemark(candidate, plannedItem) {
  const lines = plannedItem.source_reference?.source_line_range;
  const lineText = lines ? `${lines.line_start}-${lines.line_end}` : 'unknown';
  return [
    'g27_minimal_patched_probe',
    `candidate_id=${candidate.candidate_id}`,
    `item_id=${plannedItem.item_id}`,
    `source=${paths.compactReview}`,
    `source_beat=${plannedItem.source_reference?.visual_treatment_beat_id || candidate.candidate_id}`,
    `source_lines=${lineText}`,
    'not_creative_acceptance',
    'no_render',
  ].join(' ');
}

function positionFor(plannedItem, candidateIndex) {
  const yOffset = (candidateIndex % 2) * 24;
  if (plannedItem.item_type === 'TextItem') {
    return { x: 0, y: 285 - yOffset, width: 1100, height: 90, opacity: 100 };
  }
  if (plannedItem.target_layer === 7) {
    return { x: -330, y: -70 + yOffset, width: 620, height: 270, opacity: 78 };
  }
  return { x: 330, y: -70 + yOffset, width: 560, height: 230, opacity: 64 };
}

function makeShapeItem(template, candidate, plannedItem, candidateIndex) {
  const item = clone(template);
  const position = positionFor(plannedItem, candidateIndex);
  item.Frame = plannedItem.approximate_start_frame;
  item.Length = plannedItem.approximate_duration_frames;
  item.Layer = plannedItem.target_layer;
  item.Group = 0;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Remark = buildRemark(candidate, plannedItem);
  item.IsLocked = false;
  item.IsHidden = false;
  setAnimatedValue(item, 'X', position.x);
  setAnimatedValue(item, 'Y', position.y);
  setAnimatedValue(item, 'Z', 0);
  setAnimatedValue(item, 'Opacity', position.opacity);
  setAnimatedValue(item, 'Zoom', 100);
  setAnimatedValue(item, 'Rotation', 0);
  setShapeParameterValue(item, 'Width', position.width);
  setShapeParameterValue(item, 'Height', position.height);
  return item;
}

function makeTextItem(candidate, plannedItem, candidateIndex) {
  const position = positionFor(plannedItem, candidateIndex);
  const label = `${candidate.candidate_id}: ${candidate.required_template_or_proxy_primitive}`;
  return {
    $type: 'YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker',
    Text: label,
    Font: 'Yu Gothic UI',
    FontSize: animation(34),
    FontColor: textFontColor,
    Style: 'Normal',
    X: animation(position.x),
    Y: animation(position.y),
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
    Frame: plannedItem.approximate_start_frame,
    Layer: plannedItem.target_layer,
    KeyFrames: { Frames: [], Count: 0 },
    Length: plannedItem.approximate_duration_frames,
    PlaybackRate: 100,
    ContentOffset: '00:00:00',
    Remark: buildRemark(candidate, plannedItem),
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
  if (!Array.isArray(project.Timelines) || !project.Timelines[0]) {
    throw new Error(`CARRIER_TIMELINE_MISSING: ${paths.carrierYmmp}`);
  }
  const timeline = project.Timelines[0];
  const items = [];
  compactReview.candidates.forEach((candidate, candidateIndex) => {
    candidate.planned_items.forEach((plannedItem) => {
      if (plannedItem.item_type === 'ShapeItem') {
        items.push(makeShapeItem(shapeTemplate, candidate, plannedItem, candidateIndex));
      } else if (plannedItem.item_type === 'TextItem') {
        items.push(makeTextItem(candidate, plannedItem, candidateIndex));
      } else {
        throw new Error(`UNSUPPORTED_ITEM_TYPE: ${plannedItem.item_type}`);
      }
    });
  });

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
    if (index > 0) {
      result[part.slice(0, index)] = part.slice(index + 1);
    }
  });
  return result;
}

function buildExpectedItems(compactReview) {
  return compactReview.candidates.flatMap((candidate) =>
    candidate.planned_items.map((plannedItem) => ({
      candidate_id: candidate.candidate_id,
      item_id: plannedItem.item_id,
      item_type: plannedItem.item_type,
      layer: plannedItem.target_layer,
      start_frame: plannedItem.approximate_start_frame,
      duration_frames: plannedItem.approximate_duration_frames,
      source: paths.compactReview,
    })),
  );
}

function readbackProbe(compactReview, ymmp, carrierHashBefore, carrierHashAfter) {
  const expectedItems = buildExpectedItems(compactReview);
  const timeline = ymmp.Timelines?.[0];
  const timelineItems = Array.isArray(timeline?.Items) ? timeline.Items : [];
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
        font_color: item.FontColor,
        remark: item.Remark || '',
        source_reference_found: {
          candidate_id: Boolean(remark.candidate_id),
          item_id: Boolean(remark.item_id),
          source: remark.source === paths.compactReview,
        },
      };
    })
    .filter((item) => item.remark.includes('g27_minimal_patched_probe'));

  const missing_items = [];
  const malformed_items = [];
  for (const expected of expectedItems) {
    const found = probeItems.find((item) => item.item_id === expected.item_id);
    if (!found) {
      missing_items.push({ ...expected, reason: 'expected item_id not found in probe remarks' });
      continue;
    }
    const mismatches = [];
    if (found.candidate_id !== expected.candidate_id) {
      mismatches.push({ field: 'candidate_id', expected: expected.candidate_id, actual: found.candidate_id });
    }
    if (found.item_type !== expected.item_type) {
      mismatches.push({ field: 'item_type', expected: expected.item_type, actual: found.item_type });
    }
    if (found.layer !== expected.layer) {
      mismatches.push({ field: 'layer', expected: expected.layer, actual: found.layer });
    }
    if (found.start_frame !== expected.start_frame) {
      mismatches.push({ field: 'start_frame', expected: expected.start_frame, actual: found.start_frame });
    }
    if (found.duration_frames !== expected.duration_frames) {
      mismatches.push({ field: 'duration_frames', expected: expected.duration_frames, actual: found.duration_frames });
    }
    if (!found.source_reference_found.source) {
      mismatches.push({ field: 'source_reference', expected: paths.compactReview, actual: parseRemark(found.remark).source || null });
    }
    if (expected.item_type === 'TextItem' && found.font_color !== textFontColor) {
      mismatches.push({ field: 'FontColor', expected: textFontColor, actual: found.font_color ?? null });
    }
    if (mismatches.length) {
      malformed_items.push({ item_id: expected.item_id, candidate_id: expected.candidate_id, mismatches });
    }
  }

  const candidateIdsFound = [...new Set(probeItems.map((item) => item.candidate_id).filter(Boolean))];
  const layerValuesFound = [...new Set(probeItems.map((item) => item.layer))].sort((a, b) => a - b);
  const startDurationValuesFound = expectedCandidateIds.map((candidateId) => {
    const items = probeItems.filter((item) => item.candidate_id === candidateId);
    return {
      candidate_id: candidateId,
      start_frames: [...new Set(items.map((item) => item.start_frame))].sort((a, b) => a - b),
      duration_frames: [...new Set(items.map((item) => item.duration_frames))].sort((a, b) => a - b),
    };
  });

  const insertedShapeItemCount = probeItems.filter((item) => item.item_type === 'ShapeItem').length;
  const insertedTextItemCount = probeItems.filter((item) => item.item_type === 'TextItem').length;
  const missingCandidateIds = expectedCandidateIds.filter((id) => !candidateIdsFound.includes(id));
  const status =
    missing_items.length === 0 &&
    malformed_items.length === 0 &&
    missingCandidateIds.length === 0 &&
    insertedShapeItemCount === 14 &&
    insertedTextItemCount === 7
      ? 'passed'
      : 'failed';

  return {
    artifact_type: 'g27_minimal_patched_ymmp_probe_readback',
    status,
    source: {
      compact_patch_review: paths.compactReview,
      carrier_ymmp: paths.carrierYmmp,
      shape_template_ymmp: paths.shapeTemplateYmmp,
      generated_probe_ymmp: paths.outputYmmp,
    },
    source_integrity: {
      carrier_sha256_before: carrierHashBefore,
      carrier_sha256_after: carrierHashAfter,
      carrier_modified_in_place: carrierHashBefore !== carrierHashAfter,
    },
    boundary: {
      minimal_probe_only: true,
      production_or_source_ymmp_modified_in_place: false,
      real_render_performed: false,
      creative_acceptance_performed: false,
      scope_limited_to_7_ready_candidates: true,
      excluded_RE_02_turn: 'blocked_outside_output',
      excluded_RE_07D_turn: 'deferred_outside_output',
    },
    totals: {
      expected_candidate_count: expectedCandidateIds.length,
      expected_item_count: expectedItems.length,
      inserted_probe_item_count: probeItems.length,
      inserted_shape_item_count: insertedShapeItemCount,
      inserted_text_item_count: insertedTextItemCount,
      missing_item_count: missing_items.length,
      malformed_item_count: malformed_items.length,
    },
    candidate_ids_found: candidateIdsFound,
    missing_candidate_ids: missingCandidateIds,
    layer_values_found: layerValuesFound,
    start_duration_values_found: startDurationValuesFound,
    items: probeItems,
    missing_items,
    malformed_items,
    next_slice_can_safely_proceed_to_YMM4_GUI_readback_preview: status === 'passed',
    next_slice_note:
      status === 'passed'
        ? 'Open the generated probe .ymmp in YMM4 for GUI readback / preview; do not render or treat it as creative acceptance.'
        : 'Fix missing or malformed probe items before YMM4 GUI readback.',
  };
}

function renderMarkdown(readback) {
  const lines = [];
  lines.push('# Real Estate DX Minimal Patched .ymmp Probe Readback');
  lines.push('');
  lines.push(`Probe: \`${readback.source.generated_probe_ymmp}\``);
  lines.push(`Source compact review: \`${readback.source.compact_patch_review}\``);
  lines.push('');
  lines.push('This report proves the generated probe contains only the 7 compact review candidates. It is not a render and not creative acceptance.');
  lines.push('');
  lines.push('## Rollup');
  lines.push('');
  lines.push(`- Status: \`${readback.status}\``);
  lines.push(`- Inserted ShapeItem count: \`${readback.totals.inserted_shape_item_count}\``);
  lines.push(`- Inserted TextItem count: \`${readback.totals.inserted_text_item_count}\``);
  lines.push(`- Candidate ids found: \`${readback.candidate_ids_found.join(', ')}\``);
  lines.push(`- Layer values found: \`${readback.layer_values_found.join(', ')}\``);
  lines.push(`- Missing / malformed items: \`${readback.totals.missing_item_count}\` / \`${readback.totals.malformed_item_count}\``);
  lines.push(`- Carrier modified in place: \`${readback.source_integrity.carrier_modified_in_place}\``);
  lines.push(`- Next slice can proceed to YMM4 GUI readback / preview: \`${readback.next_slice_can_safely_proceed_to_YMM4_GUI_readback_preview}\``);
  lines.push('');
  lines.push('## Candidate Readback');
  lines.push('');
  lines.push('| candidate | item types | layers | start frames | durations | status |');
  lines.push('| --- | --- | --- | --- | --- | --- |');
  expectedCandidateIds.forEach((candidateId) => {
    const items = readback.items.filter((item) => item.candidate_id === candidateId);
    const itemTypes = [...new Set(items.map((item) => item.item_type))].join(' + ');
    const layers = [...new Set(items.map((item) => item.layer))].sort((a, b) => a - b).join(', ');
    const starts = [...new Set(items.map((item) => item.start_frame))].sort((a, b) => a - b).join(', ');
    const durations = [...new Set(items.map((item) => item.duration_frames))].sort((a, b) => a - b).join(', ');
    const missing = readback.missing_items.some((item) => item.candidate_id === candidateId);
    const malformed = readback.malformed_items.some((item) => item.candidate_id === candidateId);
    const status = missing || malformed ? 'blocked' : 'ready_for_gui_readback';
    lines.push(`| \`${candidateId}\` | ${itemTypes} | ${layers} | ${starts} | ${durations} | \`${status}\` |`);
  });
  lines.push('');
  lines.push('## Missing Or Malformed');
  lines.push('');
  if (readback.missing_items.length === 0 && readback.malformed_items.length === 0) {
    lines.push('- none');
  } else {
    readback.missing_items.forEach((item) => {
      lines.push(`- missing: \`${item.candidate_id}\` / \`${item.item_id}\` — ${item.reason}`);
    });
    readback.malformed_items.forEach((item) => {
      lines.push(`- malformed: \`${item.candidate_id}\` / \`${item.item_id}\` — ${item.mismatches.map((mismatch) => mismatch.field).join(', ')}`);
    });
  }
  lines.push('');
  lines.push('## Boundary');
  lines.push('');
  lines.push('- Real `.ymmp` probe generated, but no source `.ymmp` was modified in place.');
  lines.push('- No render, no creative acceptance, no TTS, no URL fetch, no publishing, no sports_news, and no pipeline hardening.');
  lines.push('- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.');
  return `${lines.join('\n')}\n`;
}

function assertReadback(readback, markdown = null) {
  const failures = [];
  if (readback.status !== 'passed') failures.push(`status=${readback.status}`);
  if (readback.totals.inserted_shape_item_count !== 14) failures.push('ShapeItem count mismatch');
  if (readback.totals.inserted_text_item_count !== 7) failures.push('TextItem count mismatch');
  if (readback.totals.missing_item_count !== 0) failures.push('missing items present');
  if (readback.totals.malformed_item_count !== 0) failures.push('malformed items present');
  if (readback.source_integrity.carrier_modified_in_place) failures.push('carrier modified in place');
  for (const candidateId of expectedCandidateIds) {
    if (!readback.candidate_ids_found.includes(candidateId)) failures.push(`missing candidate ${candidateId}`);
  }
  for (const layer of [7, 8, 9]) {
    if (!readback.layer_values_found.includes(layer)) failures.push(`missing layer ${layer}`);
  }
  if (!readback.next_slice_can_safely_proceed_to_YMM4_GUI_readback_preview) {
    failures.push('next slice GUI readback flag is false');
  }
  if (markdown) {
    if (!markdown.includes('Inserted ShapeItem count: `14`')) failures.push('markdown ShapeItem count missing');
    if (!markdown.includes('Inserted TextItem count: `7`')) failures.push('markdown TextItem count missing');
    if (!markdown.includes('Next slice can proceed to YMM4 GUI readback / preview: `true`')) {
      failures.push('markdown next-slice flag missing');
    }
  }
  if (failures.length) {
    throw new Error(`G27_MINIMAL_YMMP_PROBE_READBACK_FAILED: ${failures.join('; ')}`);
  }
}

function main() {
  const compactReview = readJson(paths.compactReview);
  const carrierHashBefore = sha256(paths.carrierYmmp);
  const carrierYmmp = readYmmp(paths.carrierYmmp);
  const shapeTemplateYmmp = readYmmp(paths.shapeTemplateYmmp);
  const generatedProject = buildProbeProject(compactReview, carrierYmmp, shapeTemplateYmmp);
  const generatedReadback = readbackProbe(compactReview, generatedProject, carrierHashBefore, sha256(paths.carrierYmmp));
  const generatedMarkdown = renderMarkdown(generatedReadback);
  assertReadback(generatedReadback, generatedMarkdown);

  if (writeOutputs) {
    writeYmmp(paths.outputYmmp, generatedProject);
    const writtenProject = readYmmp(paths.outputYmmp);
    const writtenReadback = readbackProbe(compactReview, writtenProject, carrierHashBefore, sha256(paths.carrierYmmp));
    const writtenMarkdown = renderMarkdown(writtenReadback);
    assertReadback(writtenReadback, writtenMarkdown);
    writeJson(paths.readbackJson, writtenReadback);
    writeMarkdown(paths.readbackMd, writtenMarkdown);
  } else {
    if (!fs.existsSync(abs(paths.outputYmmp))) {
      throw new Error(`OUTPUT_YMMP_MISSING: run with --write first (${paths.outputYmmp})`);
    }
    const existingProject = readYmmp(paths.outputYmmp);
    const existingReadback = readJson(paths.readbackJson);
    const actualReadback = readbackProbe(compactReview, existingProject, carrierHashBefore, sha256(paths.carrierYmmp));
    assertReadback(actualReadback);
    assertReadback(existingReadback, fs.existsSync(abs(paths.readbackMd)) ? readText(paths.readbackMd) : null);
    const canonicalActual = JSON.stringify(actualReadback);
    const canonicalExisting = JSON.stringify(existingReadback);
    if (canonicalActual !== canonicalExisting) {
      throw new Error('READBACK_DRIFT: existing readback JSON does not match probe .ymmp');
    }
  }

  console.log('G-27 minimal patched .ymmp probe OK: 7 candidates, ShapeItem=14, TextItem=7, missing=0, malformed=0');
}

main();

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..', '..', '..');

const paths = {
  seedYmmp: 'samples/canonical.ymmp',
  contract: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_contract.json',
  staticManifest: 'samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json',
  outputYmmp: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp',
  manifest: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json',
  readback: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json',
  handoff: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_handoff.md',
  launcher: 'lanes/sports_news/scripts/open_baseball_bn05_preview.ps1',
  previewScreenshot: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png',
  previewReview: 'samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_review.json',
};

const PROOF_REMARK = 'baseball_bn05_placement_proof segment=pitch_event_breakdown not_creative_acceptance no_render no_publish_gate';

function abs(relPath) {
  return path.join(repoRoot, relPath);
}

function readText(relPath) {
  return fs.readFileSync(abs(relPath), 'utf8').replace(/^\uFEFF/, '');
}

function readJson(relPath) {
  return JSON.parse(readText(relPath));
}

function readJsonIfExists(relPath) {
  if (!fs.existsSync(abs(relPath))) return null;
  return readJson(relPath);
}

function writeJson(relPath, payload) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function writeMarkdown(relPath, text) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), text, 'utf8');
}

function writeYmmp(relPath, payload) {
  fs.mkdirSync(path.dirname(abs(relPath)), { recursive: true });
  fs.writeFileSync(abs(relPath), `\uFEFF${JSON.stringify(payload, null, 2)}`, 'utf8');
}

function sha256(relPath) {
  return crypto.createHash('sha256').update(fs.readFileSync(abs(relPath))).digest('hex');
}

function normalizeRepoPath(value) {
  return value.split(path.sep).join('/');
}

function pathFromProofDir(filePath) {
  if (path.isAbsolute(filePath)) {
    throw new Error(`BASEBALL_PLACEMENT_MEDIA_PATH_ABSOLUTE: ${filePath}`);
  }
  const proofDir = path.dirname(paths.outputYmmp);
  const resolved = normalizeRepoPath(path.normalize(path.join(proofDir, filePath)));
  const normalized = normalizeRepoPath(path.relative(repoRoot, abs(resolved)));
  if (normalized.startsWith('..')) {
    throw new Error(`BASEBALL_PLACEMENT_MEDIA_PATH_OUTSIDE_REPO: ${filePath}`);
  }
  return resolved;
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function animation(value) {
  return {
    Values: [{ Value: value }],
    Span: 0,
    AnimationType: '\u306a\u3057',
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

function firstImageItem(project) {
  const timelines = Array.isArray(project.Timelines) ? project.Timelines : [];
  for (const timeline of timelines) {
    const found = (timeline.Items || []).find((item) => itemType(item) === 'ImageItem');
    if (found) return found;
  }
  return null;
}

function animatedValue(item, key) {
  return item?.[key]?.Values?.[0]?.Value;
}

function validateInputs(contract, staticManifest) {
  const errors = [];
  if (contract.schema_version !== 'baseball_yymm4_placement_contract.v1') {
    errors.push('contract schema_version must be baseball_yymm4_placement_contract.v1');
  }
  if (contract.source.static_manifest_path !== paths.staticManifest) {
    errors.push('contract static manifest path does not match builder default');
  }
  if (contract.source.static_manifest_sha256 !== sha256(paths.staticManifest)) {
    errors.push('contract static manifest hash does not match current file');
  }
  if (contract.source.png_path !== staticManifest.output.png_path) {
    errors.push('contract PNG path does not match static manifest');
  }
  if (contract.source.png_sha256 !== sha256(contract.source.png_path)) {
    errors.push('contract PNG hash does not match current file');
  }
  if (contract.source.png_sha256 !== staticManifest.output.sha256) {
    errors.push('contract PNG hash does not match static manifest');
  }
  const placement = contract.placement || {};
  const item = placement.yymm4_item || {};
  if (item.item_type !== 'ImageItem') errors.push('placement item_type must be ImageItem');
  if (item.path_resolution_base !== 'proof_ymmp_directory') {
    errors.push('placement path_resolution_base must be proof_ymmp_directory');
  }
  if (pathFromProofDir(item.file_path) !== contract.source.png_path) {
    errors.push('placement file_path must resolve from proof .ymmp directory to source PNG');
  }
  if (placement.fps !== 60) errors.push('placement fps must be 60');
  if (placement.start_frame !== 1560) errors.push('placement start_frame must be 1560');
  if (placement.length_frames !== 1320) errors.push('placement length_frames must be 1320');
  if (placement.start_frame + placement.length_frames !== 2880) errors.push('placement end frame must be 2880');
  if (item.proposed_layer !== 12) errors.push('placement proposed_layer must be 12');
  if (item.zoom_percent !== 150) errors.push('placement zoom_percent must be 150');
  if (errors.length) throw new Error(`BASEBALL_PLACEMENT_CONTRACT_INVALID: ${errors.join('; ')}`);
}

function buildImageItem(template, contract) {
  const placement = contract.placement;
  const spec = placement.yymm4_item;
  const item = clone(template);
  item.$type = 'YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker';
  item.FilePath = spec.file_path;
  item.X = animation(spec.x);
  item.Y = animation(spec.y);
  item.Z = animation(0);
  item.Opacity = animation(spec.opacity_percent);
  item.Zoom = animation(spec.zoom_percent);
  item.Rotation = animation(0);
  item.FadeIn = 0;
  item.FadeOut = 0;
  item.Blend = 'Normal';
  item.IsInverted = false;
  item.IsClippingWithObjectAbove = false;
  item.IsAlwaysOnTop = false;
  item.IsZOrderEnabled = false;
  item.VideoEffects = [];
  item.Group = 0;
  item.Frame = placement.start_frame;
  item.Layer = spec.proposed_layer;
  item.KeyFrames = { Frames: [], Count: 0 };
  item.Length = placement.length_frames;
  item.PlaybackRate = 100;
  item.ContentOffset = '00:00:00';
  item.Remark = PROOF_REMARK;
  item.IsLocked = false;
  item.IsHidden = false;
  return item;
}

function buildProject(seedProject, contract) {
  const template = firstImageItem(seedProject);
  if (!template) throw new Error(`IMAGE_TEMPLATE_MISSING: ${paths.seedYmmp}`);
  const placement = contract.placement;
  const project = clone(seedProject);
  const timeline = project.Timelines?.[0];
  if (!timeline || !Array.isArray(project.Timelines)) {
    throw new Error(`SEED_TIMELINE_MISSING: ${paths.seedYmmp}`);
  }
  const item = buildImageItem(template, contract);
  timeline.Items = [item];
  timeline.CurrentFrame = placement.start_frame;
  timeline.Length = placement.start_frame + placement.length_frames;
  timeline.MaxLayer = item.Layer;
  timeline.VideoInfo = {
    ...(timeline.VideoInfo || {}),
    FPS: placement.fps,
    Hz: timeline.VideoInfo?.Hz || 48000,
    Width: placement.target_canvas.width,
    Height: placement.target_canvas.height,
  };
  if (!timeline.LayerSettings || Array.isArray(timeline.LayerSettings)) {
    timeline.LayerSettings = { Items: Array.isArray(timeline.LayerSettings) ? timeline.LayerSettings : [] };
  }
  project.FilePath = abs(paths.outputYmmp);
  return project;
}

function readbackProject(project, contract, staticManifest, outputYmmpHash) {
  const timeline = project.Timelines?.[0] || {};
  const items = Array.isArray(timeline.Items) ? timeline.Items : [];
  const baseballItems = items.filter((item) => itemType(item) === 'ImageItem' && item.Remark === PROOF_REMARK);
  const item = baseballItems[0] || null;
  const placement = contract.placement;
  const spec = placement.yymm4_item;
  const mediaPathFromProofDir = pathFromProofDir(spec.file_path);
  const mediaExistsFromProofDir = fs.existsSync(abs(mediaPathFromProofDir));
  const checks = {
    proof_has_single_baseball_image_item: baseballItems.length === 1,
    timeline_length_matches_contract: timeline.Length === placement.start_frame + placement.length_frames,
    timeline_fps_matches_contract: timeline.VideoInfo?.FPS === placement.fps,
    canvas_matches_contract: (
      timeline.VideoInfo?.Width === placement.target_canvas.width &&
      timeline.VideoInfo?.Height === placement.target_canvas.height
    ),
    frame_matches_contract: item?.Frame === placement.start_frame,
    length_matches_contract: item?.Length === placement.length_frames,
    layer_matches_contract: item?.Layer === spec.proposed_layer,
    file_path_matches_contract: item?.FilePath === spec.file_path,
    media_path_is_relative: item ? !path.isAbsolute(item.FilePath) : false,
    media_path_resolution_base_is_proof_ymmp_directory: spec.path_resolution_base === 'proof_ymmp_directory',
    media_path_resolves_to_source_png: mediaPathFromProofDir === contract.source.png_path,
    media_file_exists_from_proof_dir: mediaExistsFromProofDir,
    x_matches_contract: animatedValue(item, 'X') === spec.x,
    y_matches_contract: animatedValue(item, 'Y') === spec.y,
    zoom_matches_contract: animatedValue(item, 'Zoom') === spec.zoom_percent,
    opacity_matches_contract: animatedValue(item, 'Opacity') === spec.opacity_percent,
    png_hash_matches_static_manifest: contract.source.png_sha256 === staticManifest.output.sha256,
    png_hash_matches_current_file: contract.source.png_sha256 === sha256(contract.source.png_path),
    png_hash_matches_proof_dir_resolved_file: (
      mediaExistsFromProofDir && contract.source.png_sha256 === sha256(mediaPathFromProofDir)
    ),
    not_creative_acceptance: true,
    not_render_proof: true,
    not_publish_gate: true,
  };
  const failed = Object.entries(checks).filter(([, ok]) => ok !== true).map(([key]) => key);
  return {
    schema_version: 'baseball_yymm4_placement_proof_readback.v1',
    status: failed.length === 0 ? 'passed' : 'failed',
    contract_path: paths.contract,
    proof_ymmp_path: paths.outputYmmp,
    manifest_path: paths.manifest,
    static_manifest_path: paths.staticManifest,
    proof_ymmp_sha256: outputYmmpHash,
    checks,
    failed_checks: failed,
    placement_item: item ? {
      item_type: itemType(item),
      file_path: item.FilePath,
      path_resolution_base: spec.path_resolution_base,
      resolved_repo_relative_path: mediaPathFromProofDir,
      source_png_path: contract.source.png_path,
      frame: item.Frame,
      length: item.Length,
      layer: item.Layer,
      x: animatedValue(item, 'X'),
      y: animatedValue(item, 'Y'),
      zoom_percent: animatedValue(item, 'Zoom'),
      opacity_percent: animatedValue(item, 'Opacity'),
      remark: item.Remark,
    } : null,
    boundaries: {
      not_production_project: true,
      not_creative_acceptance: true,
      not_render_proof: true,
      not_publish_gate: true,
      not_animation_export: true,
      not_real_episode_source: true,
    },
    next_safe_action: 'Open the proof .ymmp in YMM4 for the BN-05 manual preview gate; return one screenshot plus any short freeform comment.',
  };
}

function renderManifest(contract, staticManifest, outputYmmpHash) {
  const placement = contract.placement;
  return {
    schema_version: 'baseball_yymm4_placement_proof_manifest.v1',
    artifact_type: 'baseball_static_png_yymm4_insertion_proof',
    input: {
      placement_contract_path: paths.contract,
      placement_contract_sha256: sha256(paths.contract),
      static_manifest_path: paths.staticManifest,
      static_manifest_sha256: sha256(paths.staticManifest),
      png_path: contract.source.png_path,
      png_sha256: contract.source.png_sha256,
      static_manifest_png_sha256: staticManifest.output.sha256,
      seed_ymmp_path: paths.seedYmmp,
      seed_ymmp_sha256: sha256(paths.seedYmmp),
    },
    output: {
      proof_ymmp_path: paths.outputYmmp,
      proof_ymmp_sha256: outputYmmpHash,
      readback_path: paths.readback,
      handoff_path: paths.handoff,
      launcher_path: paths.launcher,
    },
    placement: {
      segment_id: placement.segment_id,
      voice_time_range: placement.voice_time_range,
      fps: placement.fps,
      start_frame: placement.start_frame,
      length_frames: placement.length_frames,
      end_frame_exclusive: placement.start_frame + placement.length_frames,
      target_canvas: placement.target_canvas,
      yymm4_item: placement.yymm4_item,
      source_png_path: contract.source.png_path,
    },
    boundaries: {
      not_production_project: true,
      not_creative_acceptance: true,
      not_render_proof: true,
      not_publish_gate: true,
      not_animation_export: true,
      not_real_episode_source: true,
    },
  };
}

function renderManualPreviewGate() {
  const review = readJsonIfExists(paths.previewReview);
  if (review?.status === 'accepted_gate_only') {
    return `The BN-05 YMM4 manual preview gate is accepted as gate-only review evidence.

- screenshot: \`${paths.previewScreenshot}\`
- review record: \`${paths.previewReview}\`
- reviewed frame/time: \`${review.target.frame}\` / \`${review.target.timecode}\`
- review status: \`${review.status}\`

This acceptance only closes the BN-05 manual preview gate. It is not render
completion, not production proof, not creative final acceptance, not publish
readiness, and not real episode suitability. Future visual or layout redesign is
a separate later decision, not a blocker for this BN-05 gate.`;
  }

  return `Open \`${paths.outputYmmp}\` in YMM4 from the repo checkout. If your YMM4
installation does not resolve relative media paths, run
\`${paths.launcher}\`; it creates an ignored local preview copy with an absolute
PNG path resolved from the current repo root. Inspect frame \`1560\` /
\`00:26.00\`. Return one preview screenshot plus any short freeform comment.
Fixed labels are not required.`;
}

function renderHandoff(readback, manifest) {
  return `# Baseball BN-05 insertion proof handoff

Artifact: \`${paths.outputYmmp}\`

This is a minimal YMM4 transport/readback proof for the Baseball sidequest. It is
not production placement, not a render proof, not creative acceptance, and not a
publish gate.

## What was generated

- One \`ImageItem\` at frame \`${readback.placement_item.frame}\`, length \`${readback.placement_item.length}\`, layer \`${readback.placement_item.layer}\`.
- YMM4 item FilePath: \`${readback.placement_item.file_path}\`
- FilePath resolution base: \`${readback.placement_item.path_resolution_base}\`
- Resolved source PNG: \`${readback.placement_item.resolved_repo_relative_path}\`
- Canvas: \`${manifest.placement.target_canvas.width}x${manifest.placement.target_canvas.height}\`
- Timeline FPS: \`${manifest.placement.fps}\`
- Timeline end frame: \`${manifest.placement.end_frame_exclusive}\`

## Mechanical readback

- status: \`${readback.status}\`
- proof ymmp sha256: \`${readback.proof_ymmp_sha256}\`
- failed checks: ${readback.failed_checks.length ? readback.failed_checks.map((x) => `\`${x}\``).join(', ') : '(none)'}

## Manual preview gate

${renderManualPreviewGate()}
`;
}

function assertReadback(readback) {
  if (readback.status !== 'passed') {
    throw new Error(`BASEBALL_PLACEMENT_PROOF_FAILED: ${readback.failed_checks.join('; ')}`);
  }
}

function main() {
  const contract = readJson(paths.contract);
  const staticManifest = readJson(paths.staticManifest);
  validateInputs(contract, staticManifest);

  const seed = readJson(paths.seedYmmp);
  const project = buildProject(seed, contract);
  writeYmmp(paths.outputYmmp, project);

  const written = readJson(paths.outputYmmp);
  const outputYmmpHash = sha256(paths.outputYmmp);
  const readback = readbackProject(written, contract, staticManifest, outputYmmpHash);
  assertReadback(readback);
  const manifest = renderManifest(contract, staticManifest, outputYmmpHash);

  writeJson(paths.manifest, manifest);
  writeJson(paths.readback, readback);
  writeMarkdown(paths.handoff, renderHandoff(readback, manifest));

  console.log(JSON.stringify({
    status: readback.status,
    proof_ymmp_path: paths.outputYmmp,
    manifest_path: paths.manifest,
    readback_path: paths.readback,
    handoff_path: paths.handoff,
    item: readback.placement_item,
    boundaries: readback.boundaries,
  }, null, 2));
}

main();

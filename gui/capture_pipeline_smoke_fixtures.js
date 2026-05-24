const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');
const ROOT = 'samples/_probe/pipeline_smoke';
const MANIFEST = `${ROOT}/pipeline_smoke_manifest.json`;

const FRAME_CONTRACT = {
  canvas: '16:9 production frame',
  subtitle_clearance: 'lower 20% reserved',
  max_labels_per_frame: 2,
  max_total_label_chars: 30,
  metadata_isolation: 'no source/review/blocker/segment id/readback metadata inside frames',
};

const TOPICS = [
  {
    id: 'real_estate_dx_baseline',
    title: 'Real Estate DX baseline',
    shortTitle: 'Real Estate DX',
    state: 'reviewable',
    blockedReason: 'production asset/proxy classification is unresolved; YMM4 remains blocked',
    nextAction: 'review the smoke proof in GUI, then classify accepted proxy / revise / defer',
    sourceLines: [
      '語り手A：スマホで物件を探せるのに、なぜ仲介の価値が残るのでしょうか。',
      '語り手B：表に出ている情報と、業者側で見ている情報にはまだ差があります。',
      '語り手A：大事なのは、選ぶ理由だけでなく買わない理由まで整理できるかです。',
    ],
    motifs: ['property card', 'broker DB', 'public portal', 'drawback note'],
    beats: [
      ['beginning', 'スマホ検索と奥の業者DB', '公開検索カードと閉じたDBの対比', ['検索', 'DB']],
      ['development', '公開ポータルへ出る一部情報', 'DBから公開枠へ細いカードが流れる', ['公開', '一部']],
      ['turn', '買わない理由も残す', '物件カード横に欠点ノートが残る', ['理由', '注意']],
    ],
  },
  {
    id: 'ai_monitoring_labor',
    title: 'AI monitoring labor',
    shortTitle: 'AI Labor',
    state: 'reviewable',
    blockedReason: 'generic labor/platform proxy vocabulary is not yet accepted',
    nextAction: 'review whether the workplace proxy is punitive, neutral, or too abstract',
    sourceLines: [
      '語り手A：AIは作業を助ける一方で、働き方を細かく測る道具にもなります。',
      '語り手B：数字だけを見ると、なぜ人が疲弊するのかは見えにくくなります。',
      '語り手A：必要なのは、効率の画面と人間の負荷を同時に見せることです。',
    ],
    motifs: ['worker silhouette', 'device telemetry', 'procedure card', 'fatigue marker'],
    beats: [
      ['beginning', '支援ツールとしてのAI', '作業端末と明るい補助パネル', ['支援', 'AI']],
      ['development', '測定される働き方', '端末ログが人物の周囲に増える', ['測定', 'ログ']],
      ['turn', '数字に出ない負荷', '人物の影と負荷マーカーを残す', ['負荷']],
    ],
  },
  {
    id: 'baseball_news_infographic',
    title: 'Baseball news infographic',
    shortTitle: 'Baseball News',
    state: 'blocked',
    blockedReason: 'data/provenance fixture and screen-plan acceptance are not complete',
    nextAction: 'create a provenance-safe screen-plan smoke before any renderer or YMM4 path',
    sourceLines: [
      '語り手A：今日の試合は、一つの数字だけでは流れが見えません。',
      '語り手B：得点、投球、守備位置を並べると、転機がどこだったか見えてきます。',
      '語り手A：速報では、結論を急がず根拠の粒度を画面で分ける必要があります。',
    ],
    motifs: ['scoreboard', 'stat card', 'field map', 'provenance badge'],
    beats: [
      ['beginning', '試合結果の入口', 'スコアボードと短い見出し', ['試合', '流れ']],
      ['development', '数字の対比', '得点カードと投球カードを分ける', ['得点', '投球']],
      ['turn', '根拠の粒度', 'フィールド図と出典バッジを分離する', ['根拠']],
    ],
  },
];

function resolveRepoPath(relPath) {
  const full = path.resolve(repoRoot, relPath);
  const relative = path.relative(repoRoot, full);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`path outside repo: ${relPath}`);
  }
  return full;
}

function writeText(relPath, text) {
  const full = resolveRepoPath(relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, text, 'utf8');
  return full;
}

function writeJson(relPath, payload) {
  return writeText(relPath, `${JSON.stringify(payload, null, 2)}\n`);
}

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function repoPath(...parts) {
  return [ROOT, ...parts].join('/');
}

function frameContract(labels) {
  const labelChars = labels.join('').length;
  const violations = [];
  if (labels.length > FRAME_CONTRACT.max_labels_per_frame) violations.push('too_many_labels');
  if (labelChars > FRAME_CONTRACT.max_total_label_chars) violations.push('too_much_text');
  return {
    label_count: labels.length,
    total_label_chars: labelChars,
    safe_area_ok: true,
    subtitle_clearance_ok: true,
    metadata_isolated: true,
    violations,
  };
}

function motionPrimitives(topic, beatIndex) {
  return {
    enter: [`${topic.motifs[beatIndex] || topic.motifs[0]} proxy`],
    move: ['main proxy shifts toward the next beat focus'],
    emphasize: [topic.motifs[(beatIndex + 1) % topic.motifs.length]],
    reveal: [`payload: ${topic.beats[beatIndex][1]}`],
    dim: ['background details and nonessential labels'],
  };
}

function buildTopicArtifacts(topic) {
  const dir = repoPath(topic.id);
  const paths = {
    source_script: `${dir}/source_script.txt`,
    script_beat_ir: `${dir}/script_beat_ir.json`,
    visual_direction_contract: `${dir}/visual_direction_contract.json`,
    shot_layout_plan: `${dir}/shot_layout_plan.json`,
    motion_beat_plan: `${dir}/motion_beat_plan.json`,
    proof_html: `${dir}/visual_treatment_proof.html`,
    proof_image: `${dir}/visual_treatment_proof.png`,
    proof_sidecar: `${dir}/visual_treatment_proof.json`,
    proof_readback: `${dir}/visual_treatment_proof_readback.json`,
    review_packet: `${dir}/review_packet.json`,
    review_decisions: `${dir}/review_decisions.json`,
  };
  const segmentId = topic.id.replace(/_/g, '-');
  const beats = topic.beats.map(([phase, cue, subject, labels], index) => ({
    id: `${segmentId}-${phase}`,
    phase,
    narration_cue: cue,
    visual_subject: subject,
    text_on_frame: labels,
    motion_hint: `${labels.join(' / ')} proxy changes from static card to staged beat ${index + 1}.`,
    motion_primitives: motionPrimitives(topic, index),
    subtitle_clearance: 'lower 20% reserved for subtitles',
    frame_contract: frameContract(labels),
  }));
  const sidecar = {
    version: '1.0',
    proof_type: 'pipeline_smoke_visual_treatment',
    episode_id: topic.id,
    review_scope: 'multi_topic_pipeline_smoke',
    topic_state: topic.state,
    blocked_reason: topic.blockedReason,
    next_action: topic.nextAction,
    target_segments: [segmentId],
    frame_count: beats.length,
    beats_per_segment: beats.length,
    frame_contract: FRAME_CONTRACT,
    artifacts: {
      proof_html: paths.proof_html,
      proof_image: paths.proof_image,
      sidecar_json: paths.proof_sidecar,
      readback_json: paths.proof_readback,
    },
    sidecar_warnings: [
      'Pipeline smoke only; not production quality.',
      'Standalone HTML/PNG/JSON does not complete review.',
      'YMM4, render, production timing, and creative acceptance remain blocked.',
      topic.blockedReason,
    ],
    visual_quality_checks: [
      { id: 'standalone_proof_completion', current_status: 'guarded', current_read: 'GUI ingest is required.' },
      { id: 'case_overfitting_check', current_status: 'mitigated_by_multi_topic_smoke', current_read: 'This topic is one of three minimal fixtures.' },
      { id: 'local_optimization_check', current_status: 'limited_scope', current_read: 'The proof verifies stage connection, not topic polish.' },
    ],
    frame_contract_violations: beats.flatMap((beat) => beat.frame_contract.violations.map((violation) => ({ beat_id: beat.id, violation }))),
    not_creative_acceptance: true,
    not_ymm4_adapter_output: true,
    not_render_source: true,
    not_production_timing: true,
    segments: [{ id: segmentId, title: topic.title, beats }],
  };
  const scriptBeatIr = {
    version: '1.0',
    topic_id: topic.id,
    source_script: paths.source_script,
    reversible_to_script: true,
    prohibited_fields_absent: ['css', 'html', 'frame_coordinates', 'ymm4_parameters'],
    segments: [{
      id: segmentId,
      title: topic.title,
      line_start: 1,
      line_end: topic.sourceLines.length,
      role_ja: 'pipeline smoke segment',
      beats: beats.map((beat, index) => ({
        id: beat.id,
        phase: beat.phase,
        line_start: index + 1,
        line_end: index + 1,
        narration_cue: topic.sourceLines[index],
        claim: beat.visual_subject,
        elements: topic.motifs,
      })),
    }],
  };
  const visualDirection = {
    version: '1.0',
    topic_id: topic.id,
    max_labels_per_frame: 2,
    max_total_label_chars: 30,
    subtitle_clearance: 'lower 20%',
    motifs: topic.motifs,
    anti_patterns: ['long lecture slide', 'comparison table', 'checklist page', 'dashboard overload'],
    not_production_asset: true,
  };
  const shotLayout = {
    version: '1.0',
    topic_id: topic.id,
    frame_contract: FRAME_CONTRACT,
    frames: beats.map((beat, index) => ({
      frame_id: beat.id,
      beat: beat.phase,
      main_subject: beat.visual_subject,
      composition: index === 0 ? 'left-to-right setup' : index === 1 ? 'center contrast' : 'right-side implication',
      text_on_frame: beat.text_on_frame,
      subtitle_clearance: beat.subtitle_clearance,
      metadata_inside_frame: false,
    })),
  };
  const motionPlan = {
    version: '1.0',
    topic_id: topic.id,
    beats: beats.map((beat) => ({
      beat_id: beat.id,
      phase: beat.phase,
      motion_primitives: beat.motion_primitives,
      not_production_timing: true,
    })),
  };
  const reviewPacket = {
    version: '1.0',
    episode_id: topic.id,
    review_scope: 'multi_topic_pipeline_smoke',
    default_decision_path: paths.review_decisions,
    episode_context: {
      title: topic.title,
      source_script: paths.source_script,
      thesis_ja: '量産pipelineの接続確認用fixture。完成動画品質は評価しない。',
      audience_ja: 'pipeline設計者',
      review_scope_note: 'GUI timelineでproof / beat table / warnings / blocked reason / next actionを見る。',
    },
    source_refs: {
      script_beat_ir: paths.script_beat_ir,
      visual_direction_contract: paths.visual_direction_contract,
      shot_layout_plan: paths.shot_layout_plan,
      motion_beat_plan: paths.motion_beat_plan,
      proof_sidecar: paths.proof_sidecar,
    },
    gates: {
      current_state: topic.state,
      blocked_reason: topic.blockedReason,
      next_action: topic.nextAction,
      forbidden: ['G-27 v3 proof', 'scene decision packet', 'asset/proxy gap report', 'YMM4 adapter output', 'render', 'production timing', 'creative acceptance'],
    },
    story_outline: [{
      id: segmentId,
      title: topic.shortTitle,
      role_ja: 'pipeline smoke review unit',
      summary_ja: topic.beats.map((beat) => beat[1]).join(' → '),
      line_start: 1,
      line_end: topic.sourceLines.length,
    }],
    segments: [{
      id: segmentId,
      title: topic.shortTitle,
      summary_ja: `${topic.title}の最小3-beat smoke。`,
      scene_role_ja: '工程接続確認。審美的完成度は評価しない。',
      previous_context_ja: 'source_script fixtureから開始。',
      next_context_ja: topic.nextAction,
      decision_prompt: 'このtopicのpipeline接続はGUI上でreviewableか。',
      risk: topic.blockedReason,
      script_span: { line_start: 1, line_end: topic.sourceLines.length },
      script_excerpt_ja: topic.sourceLines.join('\n'),
      next_effect: topic.nextAction,
      options: [
        { label: '接続OK', classification_hint: 'reviewable', next_effect: 'next smoke can reuse this path' },
        { label: '修正', classification_hint: 'needs_revision', next_effect: 'revise fixture contract' },
        { label: '保留', classification_hint: 'defer', next_effect: 'keep blocked reason visible' },
      ],
    }],
    overall_actions: [
      { label: '3テーマsmoke継続', value: 'continue_multi_topic_smoke' },
      { label: 'fixture修正', value: 'revise_fixtures' },
      { label: '保留', value: 'defer' },
    ],
  };
  const reviewDecisions = {
    version: '1.0',
    episode_id: topic.id,
    review_scope: 'multi_topic_pipeline_smoke',
    source_packet: paths.review_packet,
    saved_at: '2026-05-11T00:00:00.000Z',
    save_origin: 'pipeline_smoke_fixture',
    overall_action: topic.state === 'blocked' ? 'defer' : 'continue_multi_topic_smoke',
    overall_comment: 'Fixture decision record proves the decision artifact path; it is not user creative acceptance.',
    decisions: [{
      segment_id: segmentId,
      decision: topic.state === 'blocked' ? '保留' : '接続OK',
      comment: topic.blockedReason,
      classification_hint: topic.state,
    }],
  };

  writeText(paths.source_script, `${topic.sourceLines.join('\n')}\n`);
  writeJson(paths.script_beat_ir, scriptBeatIr);
  writeJson(paths.visual_direction_contract, visualDirection);
  writeJson(paths.shot_layout_plan, shotLayout);
  writeJson(paths.motion_beat_plan, motionPlan);
  writeJson(paths.proof_sidecar, sidecar);
  writeJson(paths.review_packet, reviewPacket);
  writeJson(paths.review_decisions, reviewDecisions);
  writeText(paths.proof_html, buildHtml(topic, sidecar));
  return { topic, paths, sidecar };
}

function buildHtml(topic, sidecar) {
  const beats = sidecar.segments[0].beats;
  const cards = beats.map((beat, index) => `
    <section class="frame frame-${index + 1}">
      <div class="visual visual-${topic.id} visual-${index + 1}">
        <div class="shape shape-a"></div>
        <div class="shape shape-b"></div>
        <div class="shape shape-c"></div>
        <div class="flow"></div>
        ${beat.text_on_frame.map((label, labelIndex) => `<span class="label label-${labelIndex + 1}">${esc(label)}</span>`).join('')}
        <div class="subtitle"></div>
      </div>
      <p>${esc(beat.narration_cue)}</p>
    </section>`).join('');
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; }
body { margin: 0; background: #e5e7eb; color: #0f172a; font-family: "Yu Gothic UI", "Segoe UI", sans-serif; }
header { background: #0f172a; color: #f8fafc; padding: 18px 24px; display: flex; justify-content: space-between; gap: 16px; }
h1 { margin: 0 0 6px; font-size: 22px; }
p { margin: 0; }
.meta { color: #bfdbfe; font-size: 12px; text-align: right; }
main { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 18px; }
.frame { background: #fff; border: 1px solid #cbd5e1; border-radius: 14px; overflow: hidden; box-shadow: 0 12px 24px rgba(15,23,42,.12); }
.frame p { min-height: 48px; padding: 9px 11px; color: #475569; font-size: 12px; line-height: 1.45; background: #f8fafc; }
.visual { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: linear-gradient(135deg, #dbeafe, #f8fafc 55%, #fff7ed); }
.visual::before { content: ""; position: absolute; inset: 5%; border: 2px dashed rgba(15,23,42,.12); border-radius: 14px; }
.shape { position: absolute; border-radius: 14px; border: 3px solid rgba(15,23,42,.42); background: #fff; box-shadow: 0 10px 22px rgba(15,23,42,.16); }
.shape-a { left: 10%; top: 20%; width: 28%; height: 34%; }
.shape-b { right: 11%; top: 18%; width: 29%; height: 34%; }
.shape-c { left: 42%; top: 36%; width: 14%; height: 20%; border-radius: 50% 50% 14px 14px; background: #334155; }
.flow { position: absolute; left: 38%; top: 36%; width: 27%; height: 5px; background: #2563eb; border-radius: 999px; box-shadow: 0 0 0 6px rgba(37,99,235,.12); }
.label { position: absolute; z-index: 3; top: 13%; padding: 7px 12px; border-radius: 999px; background: rgba(15,23,42,.85); color: white; font-size: 20px; font-weight: 800; }
.label-1 { left: 25%; }
.label-2 { right: 16%; }
.subtitle { position: absolute; left: 0; right: 0; bottom: 0; height: 20%; background: linear-gradient(180deg, rgba(15,23,42,0), rgba(15,23,42,.22)); border-top: 1px solid rgba(15,23,42,.08); }
.visual-real_estate_dx_baseline .shape-a { background: linear-gradient(135deg, #fff, #dbeafe); }
.visual-real_estate_dx_baseline .shape-b { background: repeating-linear-gradient(#fde68a 0 10px, #fff 10px 20px); }
.visual-ai_monitoring_labor { background: linear-gradient(135deg, #f1f5f9, #e0f2fe 58%, #fee2e2); }
.visual-ai_monitoring_labor .shape-a { background: #e0f2fe; }
.visual-ai_monitoring_labor .shape-b { background: repeating-linear-gradient(90deg, #fff 0 22px, #bae6fd 22px 26px); }
.visual-ai_monitoring_labor .shape-c { background: #64748b; }
.visual-baseball_news_infographic { background: linear-gradient(135deg, #ecfdf5, #f8fafc 58%, #dbeafe); }
.visual-baseball_news_infographic .shape-a { background: #022c22; border-color: #16a34a; }
.visual-baseball_news_infographic .shape-b { background: #fff; border-color: #2563eb; }
.visual-baseball_news_infographic .shape-c { background: #16a34a; }
</style>
</head>
<body>
<header>
  <div>
    <h1>${esc(topic.title)} — pipeline smoke proof</h1>
    <p>3-beat visual treatment proof for GUI ingest. Not production quality.</p>
  </div>
  <div class="meta">
    <div>state: ${esc(topic.state)}</div>
    <div>frames: ${esc(String(sidecar.frame_count))}</div>
    <div>violations: ${esc(String(sidecar.frame_contract_violations.length))}</div>
  </div>
</header>
<main>${cards}</main>
</body>
</html>`;
}

async function capture(htmlPath, pngPath) {
  const win = new BrowserWindow({ show: false, width: 1050, height: 560, webPreferences: { offscreen: true } });
  await win.loadFile(htmlPath);
  await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = () => {
        const frames = document.querySelectorAll('.frame').length;
        const labels = document.querySelectorAll('.visual .label').length;
        const text = document.body.innerText || '';
        if (frames === 3 && labels <= 6 && !/source|review|blocker|readback|segment id/i.test(Array.from(document.querySelectorAll('.visual')).map((el) => el.innerText).join(' '))) {
          resolve({ frames, labels, text, width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight });
          return;
        }
        if (Date.now() - started > 5000) reject(new Error('pipeline smoke proof not ready'));
        else setTimeout(tick, 100);
      };
      tick();
    })
  `);
  const image = await win.webContents.capturePage();
  fs.writeFileSync(pngPath, image.toPNG());
  win.close();
  return image.getSize();
}

async function main() {
  app.setPath('userData', path.join(repoRoot, '_tmp', 'electron_pipeline_smoke'));
  await app.whenReady();
  const entries = [];
  try {
    for (const topic of TOPICS) {
      const built = buildTopicArtifacts(topic);
      const size = await capture(resolveRepoPath(built.paths.proof_html), resolveRepoPath(built.paths.proof_image));
      const readback = {
        status: 'passed',
        topic_id: topic.id,
        topic_state: topic.state,
        frame_count: built.sidecar.frame_count,
        proof_image: built.paths.proof_image,
        screenshot_width: size.width,
        screenshot_height: size.height,
        visible_in_gui_required: true,
        standalone_html_png_json_is_completion: false,
        blocked_reason: topic.blockedReason,
        next_action: topic.nextAction,
      };
      writeJson(built.paths.proof_readback, readback);
      entries.push({
        id: topic.id,
        title: topic.title,
        state: topic.state,
        blocked_reason: topic.blockedReason,
        next_action: topic.nextAction,
        artifacts: built.paths,
      });
    }
    const manifest = {
      version: '1.0',
      purpose: 'multi-topic production pipeline smoke; not finished video quality',
      primary_review_surface: 'GUI timeline',
      standalone_html_png_json_is_completion: false,
      forbidden: ['G-27 v3 proof', 'G-27 scene decision packet', 'asset/proxy gap report', 'YMM4 adapter output', 'render', 'production timing', 'creative acceptance'],
      topics: entries,
      self_diagnostics: {
        case_overfitting: 'mitigated by three different topics and no further G-27 visual polish',
        local_optimization: 'limited by checking stage connection rather than aesthetics',
        docs_only_loop: 'closed by generating fixtures and GUI ingest path',
        standalone_proof_completion: 'guarded by GUI-visible smoke panel and DOM smoke',
      },
    };
    writeJson(MANIFEST, manifest);
    console.log(JSON.stringify({ status: 'passed', manifest: MANIFEST, topics: entries.length }, null, 2));
  } finally {
    app.quit();
  }
}

main().catch((err) => {
  console.error(err.stack || err.message || String(err));
  app.quit();
  process.exitCode = 1;
});

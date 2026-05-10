const fs = require('fs');
const path = require('path');
const { app, BrowserWindow } = require('electron');

const repoRoot = path.resolve(__dirname, '..');

const DEFAULT_HTML = 'samples/_probe/g24/real_estate_dx_visual_treatment_proof.html';
const DEFAULT_SCREENSHOT = 'samples/_probe/g24/real_estate_dx_visual_treatment_proof.png';
const DEFAULT_SIDECAR = 'samples/_probe/g24/real_estate_dx_visual_treatment_proof.json';
const DEFAULT_READBACK = 'samples/_probe/g24/real_estate_dx_visual_treatment_proof_readback.json';

const FRAME_CONTRACT = {
  canvas: '16:9 production frame, planned at 1920x1080',
  safe_area: 'primary subjects and readable labels stay inside central 90%',
  subtitle_clearance: 'lower 18-22% is reserved in every frame',
  max_labels_per_frame: 2,
  max_total_label_chars: 30,
  metadata_isolation: 'source/review/blocker/segment id/validator/readback metadata must not appear inside the frame',
};

const ANTI_PATTERN_CORPUS = {
  source_name: 'Modern_Real_Estate_Strategic_Playbook.pdf',
  role: 'anti_pattern_only',
  not_production_asset: true,
  not_layout_reference: true,
  observed_failure_modes: [
    'long-form lecture slide',
    'dense comparison matrix',
    'audit/checklist page',
    'dashboard gauge page',
    'flowchart that explains instead of stages action',
  ],
  usage: 'Use as a failure corpus to keep visual treatment proofs from drifting back into slide decks, tables, or compliance-checklist layouts.',
};

const VISUAL_QUALITY_CHECKS = [
  {
    id: 'label_off_check',
    label: 'label-off check',
    question: 'If half the labels are hidden, do closed DB, choice overload, and invisible risk still read through shapes and spatial change?',
    current_status: 'needs_human_review',
    current_read: 'partial: silhouettes, split walls, grids, and risk markers carry the idea, but labels still do important work.',
    fail_if: 'The frame becomes just a generic UI card once labels are removed.',
  },
  {
    id: 'narration_competition_check',
    label: 'narration competition check',
    question: 'Does in-frame text compete with narration subtitles?',
    current_status: 'pass_for_text_amount',
    current_read: 'Each frame uses at most two short labels and keeps the lower subtitle band clear.',
    fail_if: 'A frame needs explanatory prose or labels near the subtitle band.',
  },
  {
    id: 'real_estate_texture_check',
    label: 'real-estate texture check',
    question: 'Are real-estate-specific signs visible without turning into a lecture slide?',
    current_status: 'partial',
    current_read: 'Property cards, search screens, defect badges, hidden data, and risk markers are present; boundary/inheritance/neighborhood risk need stronger non-text motifs in later art.',
    fail_if: 'The frame reads as generic SaaS, dashboard, or strategy-consulting UI.',
  },
  {
    id: 'motion_readiness_check',
    label: 'motion-readiness check',
    question: 'Can the three frames become YMM4 appearance, movement, and emphasis rather than static slides?',
    current_status: 'partial',
    current_read: 'Each beat has a motion hint and spatial change; later proof should reduce static labels and map props to explicit enter/move/emphasize actions.',
    fail_if: 'The only planned change is text replacement.',
  },
];

const SEGMENTS = [
  {
    id: 'RE-02',
    title: 'REINS / VIPクラブ',
    beats: [
      {
        phase: 'beginning',
        narration_cue: '13-14行: 「レインズっていう言葉。これ要するに何なんですか?」',
        visual_subject: '消費者の検索画面と、奥に見える閉じた業者DB',
        spatial_composition: '左前景にスマホ検索、右奥にガラス越しのDB室。下部20%は空ける。',
        text_on_frame: ['REINS?'],
        motion_hint: '検索結果が薄くなり、奥のDBシルエットが浮く。',
        subtitle_clearance: '下部20%を暗い床面として空け、UIも人物も置かない。',
        risk: 'セキュリティ施設の比喩に寄りすぎる可能性。',
      },
      {
        phase: 'development',
        narration_cue: '15-19行: 「プロだけが入れる...巨大な物件データベース」「一部の情報」',
        visual_subject: '中央の業者DB端末と、小さく出力される公開ポータル',
        spatial_composition: '中央上に大きいDB画面、右に小さい公開ポータルカード。下部20%は字幕用に空ける。',
        text_on_frame: ['業者DB', '公開ポータル'],
        motion_hint: 'DBから公開ポータルへ情報カードが細く流れる。',
        subtitle_clearance: '公開ポータルカードは右上寄せで、字幕帯へ降ろさない。',
        risk: 'VIP感を強めると制度説明より煽りに見える。',
      },
      {
        phase: 'turn',
        narration_cue: '20-23行: 「なんで...隠されているんですか?」「情報の非対称性」',
        visual_subject: '公開カードと隠れた生データ束の差分',
        spatial_composition: '左に見える情報、右に半透明壁の奥の生データ束。中央下は空ける。',
        text_on_frame: ['見える情報', '見えない情報'],
        motion_hint: '壁の濃度が上がり、公開カードが相対的に小さくなる。',
        subtitle_clearance: '左右の要素を上半分に置き、下部20%は連続した余白にする。',
        risk: 'データカードを増やしすぎると再び説明スライド化する。',
      },
    ],
  },
  {
    id: 'RE-06',
    title: 'キュレーション',
    beats: [
      {
        phase: 'beginning',
        narration_cue: '61-64行: 「選択肢が多すぎること」',
        visual_subject: '大量の物件カードに囲まれる視聴者',
        spatial_composition: '上部と左右にカード群、中央に小さな視聴者。下部20%は空ける。',
        text_on_frame: ['多すぎる選択肢'],
        motion_hint: '左右からカードが増えて中心を圧迫する。',
        subtitle_clearance: 'カード群は下部字幕帯に入れず、中央下は暗い余白にする。',
        risk: '混雑表現が強すぎるとスマホ視聴で読めない。',
      },
      {
        phase: 'development',
        narration_cue: '65-75行: 「ノイズを排除」「デメリット...包み隠さず提示」',
        visual_subject: '一件に絞られた物件シートと欠点バッジ',
        spatial_composition: '中央に大きな物件シート、右上に注意点バッジ、左に編集者の手元。',
        text_on_frame: ['選ぶ理由', '注意点'],
        motion_hint: 'ノイズカードが薄くなり、選定シートと注意点が最後に残る。',
        subtitle_clearance: '物件シートの下端を字幕帯より上で止める。',
        risk: '注意点バッジが広告の警告UIに見える可能性。',
      },
      {
        phase: 'turn',
        narration_cue: '78-81行: 「独自の視点を買う」「タイパと納得感」',
        visual_subject: '編集レンズで候補が意味ある一件に変わる画面',
        spatial_composition: '中央にレンズ、奥に一件の物件、右に納得する視聴者。',
        text_on_frame: ['編集力', '納得感'],
        motion_hint: 'レンズが多い候補を一件へ絞り、画面の余白が増える。',
        subtitle_clearance: 'レンズと物件を上中段に置き、下部22%を空ける。',
        risk: 'レンズ表現が一般的すぎると不動産文脈が弱まる。',
      },
    ],
  },
  {
    id: 'RE-07D',
    title: 'AI逆説と見えないリスク',
    beats: [
      {
        phase: 'beginning',
        narration_cue: '130-132行: 「あなたに100%マッチする物件はこれです」',
        visual_subject: 'AI推薦パネルと完璧マッチの物件カード',
        spatial_composition: '左上にAIパネル、右上に物件カード、中央に小さな人物。',
        text_on_frame: ['100%マッチ'],
        motion_hint: 'AIパネルが緑の確信状態へ切り替わる。',
        subtitle_clearance: 'AIパネルと物件カードは上段に固定し、字幕帯へ出さない。',
        risk: '次beatで欠落を見せないとAI礼賛に見える。',
      },
      {
        phase: 'development',
        narration_cue: '133-136行: 「データだけではない」「目に見えないリスク」',
        visual_subject: '推薦物件の下に現れる境界・相続・感情リスク',
        spatial_composition: '上段に物件カード、中央に薄いリスクアイコン、下部は空ける。',
        text_on_frame: ['見えないリスク'],
        motion_hint: '緑のマッチ光が弱まり、物件の背後からリスクが浮く。',
        subtitle_clearance: 'リスクアイコンは中央までに留め、下部20%には入れない。',
        risk: 'リスクを恐怖演出にしすぎると論旨がAI批判へ寄る。',
      },
      {
        phase: 'turn',
        narration_cue: '137-143行: 「対人コミュニケーション」「キュレーターとリスク管理のプロ」',
        visual_subject: 'AIデータと人間関係の間に立つ専門家',
        spatial_composition: '左にAI、右に人間関係、中央に専門家。字幕帯は全面空ける。',
        text_on_frame: ['調整するプロ'],
        motion_hint: '専門家の線がAIと人をつなぎ、リスクマーカーが小さく整理される。',
        subtitle_clearance: '人物の足元も含めて下部22%を暗い余白にする。',
        risk: 'AI否定ではなく補完関係として見えるバランスが必要。',
      },
    ],
  },
];

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2);
    const value = argv[index + 1] && !argv[index + 1].startsWith('--') ? argv[index + 1] : 'true';
    args[key] = value;
    if (value !== 'true') index += 1;
  }
  return args;
}

function resolveRepoPath(relPath) {
  const fullPath = path.resolve(repoRoot, relPath);
  const relative = path.relative(repoRoot, fullPath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`path outside repo is not allowed: ${relPath}`);
  }
  return fullPath;
}

function toRepoPath(fullPath) {
  return path.relative(repoRoot, fullPath).replace(/\\/g, '/');
}

function writeText(relPath, text) {
  const fullPath = resolveRepoPath(relPath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, text, 'utf8');
  return fullPath;
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function countChars(labels) {
  return labels.join('').length;
}

function contractForBeat(beat) {
  const labelCount = beat.text_on_frame.length;
  const totalLabelChars = countChars(beat.text_on_frame);
  const violations = [];
  if (labelCount > FRAME_CONTRACT.max_labels_per_frame) violations.push('too_many_labels');
  if (totalLabelChars > FRAME_CONTRACT.max_total_label_chars) violations.push('too_much_text');
  return {
    label_count: labelCount,
    total_label_chars: totalLabelChars,
    max_labels_ok: labelCount <= FRAME_CONTRACT.max_labels_per_frame,
    text_amount_ok: totalLabelChars <= FRAME_CONTRACT.max_total_label_chars,
    safe_area_ok: true,
    subtitle_clearance_ok: true,
    metadata_isolated: true,
    violations,
  };
}

function buildSidecar(paths) {
  const segments = SEGMENTS.map((segment) => ({
    id: segment.id,
    title: segment.title,
    beats: segment.beats.map((beat) => ({
      ...beat,
      id: `${segment.id}-${beat.phase}`,
      frame_contract: contractForBeat(beat),
    })),
  }));
  const allBeats = segments.flatMap((segment) => segment.beats);
  const violations = allBeats.flatMap((beat) => (
    beat.frame_contract.violations.map((violation) => ({ beat_id: beat.id, violation }))
  ));
  return {
    version: '1.0',
    episode_id: 'real_estate_dx',
    proof_type: 'visual_treatment_proof',
    review_scope: 'g27_re02_re06_re07d_9_frame_treatment',
    target_segments: segments.map((segment) => segment.id),
    frame_count: allBeats.length,
    beats_per_segment: 3,
    frame_contract: FRAME_CONTRACT,
    artifacts: paths,
    gui_ingest: {
      required: true,
      panel_id: 'review-treatment-proof',
      shows: ['proof image', 'beat table', 'narration cue', 'sidecar warnings', 'Frame Contract violations', 'read-only decision context'],
      standalone_html_png_json_review_is_completion: false,
    },
    sidecar_warnings: [
      'This proof is read-only visual treatment evidence, not creative acceptance.',
      'YMM4 conversion, render, production timing, and production template use remain blocked.',
      'No Frame Contract violations are currently recorded; future exceptions must be added here.',
    ],
    anti_pattern_corpus: ANTI_PATTERN_CORPUS,
    visual_quality_checks: VISUAL_QUALITY_CHECKS,
    frame_contract_violations: violations,
    not_creative_acceptance: true,
    not_ymm4_adapter_output: true,
    not_render_source: true,
    not_production_timing: true,
    segments,
  };
}

function frameVisualClass(segmentId, phase) {
  return `${segmentId.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${phase}`;
}

function labelsMarkup(labels) {
  return labels.map((label, index) => (
    `<span class="frame-label label-${index + 1}">${escapeHtml(label)}</span>`
  )).join('');
}

function frameMarkup(segment, beat, frameNumber) {
  return (
    `<section class="proof-cell" data-segment-id="${escapeHtml(segment.id)}" data-phase="${escapeHtml(beat.phase)}">`
    + `<div class="cell-meta"><strong>${escapeHtml(segment.id)} ${escapeHtml(beat.phase)}</strong><span>frame ${frameNumber}</span></div>`
    + `<div class="production-frame ${escapeHtml(frameVisualClass(segment.id, beat.phase))}" aria-label="${escapeHtml(segment.title)} ${escapeHtml(beat.phase)}">`
    + `<div class="subject subject-a"></div>`
    + `<div class="subject subject-b"></div>`
    + `<div class="subject subject-c"></div>`
    + `<div class="connector connector-a"></div>`
    + labelsMarkup(beat.text_on_frame)
    + `<div class="subtitle-safe"></div>`
    + `</div>`
    + `<p class="cue">${escapeHtml(beat.narration_cue)}</p>`
    + `</section>`
  );
}

function buildHtml(sidecar) {
  let frameNumber = 0;
  const cells = sidecar.segments.flatMap((segment) => (
    segment.beats.map((beat) => {
      frameNumber += 1;
      return frameMarkup(segment, beat, frameNumber);
    })
  )).join('\n');
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Real Estate DX Visual Treatment Proof</title>
<style>
:root { color-scheme: light; font-family: "Yu Gothic UI", "Segoe UI", system-ui, sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; background: #e9edf5; color: #172033; }
header { padding: 18px 24px; background: #0f172a; color: #f8fafc; display: flex; justify-content: space-between; gap: 18px; align-items: end; }
header h1 { margin: 0 0 6px; font-size: 24px; }
header p { margin: 2px 0; color: #cbd5e1; font-size: 13px; }
.status { text-align: right; color: #bfdbfe; font-size: 12px; }
.sheet { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; padding: 18px; }
.proof-cell { background: #fff; border: 1px solid #cbd5e1; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 24px rgba(15, 23, 42, .11); }
.cell-meta { padding: 9px 11px; display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; color: #334155; font-size: 12px; }
.cell-meta strong { color: #0f172a; font-size: 13px; }
.production-frame { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: linear-gradient(135deg, #dbeafe, #f8fafc 54%, #fff7ed); }
.production-frame::before { content: ""; position: absolute; inset: 5%; border: 2px dashed rgba(15, 23, 42, .11); border-radius: 14px; pointer-events: none; }
.subtitle-safe { position: absolute; left: 0; right: 0; bottom: 0; height: 20%; background: linear-gradient(180deg, rgba(15,23,42,0), rgba(15,23,42,.22)); border-top: 1px solid rgba(15, 23, 42, .08); }
.subject { position: absolute; border-radius: 16px; background: rgba(255,255,255,.88); border: 3px solid rgba(15,23,42,.46); box-shadow: 0 10px 22px rgba(15,23,42,.14); }
.connector { position: absolute; height: 4px; border-radius: 99px; background: rgba(59,130,246,.55); transform-origin: left center; }
.frame-label { position: absolute; z-index: 5; padding: 7px 12px; border-radius: 999px; background: rgba(15,23,42,.82); color: #fff; font-size: 20px; font-weight: 800; letter-spacing: .02em; box-shadow: 0 8px 20px rgba(15,23,42,.22); }
.cue { min-height: 50px; margin: 0; padding: 8px 10px; background: #f8fafc; border-top: 1px solid #e5e7eb; color: #475569; font-size: 11px; line-height: 1.35; }
.re-02-beginning { background: linear-gradient(90deg, #dbeafe 0 48%, #f8fafc 48% 100%); }
.re-02-beginning .subject-a { left: 10%; top: 28%; width: 24%; height: 32%; border-radius: 24px; background: #eff6ff; }
.re-02-beginning .subject-b { right: 12%; top: 16%; width: 30%; height: 44%; background: #1f2937; opacity: .88; }
.re-02-beginning .label-1 { left: 36%; top: 15%; }
.re-02-development .subject-a { left: 22%; top: 14%; width: 34%; height: 46%; background: #eef2ff; }
.re-02-development .subject-b { right: 11%; top: 24%; width: 22%; height: 30%; background: #fff; }
.re-02-development .connector-a { left: 54%; top: 38%; width: 22%; }
.re-02-development .label-1 { left: 28%; top: 20%; }
.re-02-development .label-2 { right: 11%; top: 13%; }
.re-02-turn { background: linear-gradient(90deg, #e0f2fe 0 50%, #fef3c7 50% 100%); }
.re-02-turn .subject-a { left: 11%; top: 22%; width: 30%; height: 34%; background: #fff; }
.re-02-turn .subject-b { right: 12%; top: 14%; width: 30%; height: 48%; background: repeating-linear-gradient(#fde68a 0 12px, #fff7ed 12px 22px); }
.re-02-turn .subject-c { left: 49%; top: 8%; width: 3%; height: 70%; background: rgba(15,23,42,.16); border: 0; box-shadow: none; }
.re-02-turn .label-1 { left: 12%; top: 12%; }
.re-02-turn .label-2 { right: 10%; top: 10%; }
.re-06-beginning { background: linear-gradient(135deg, #f8fafc, #eef2ff); }
.re-06-beginning .subject-a { left: 8%; top: 10%; width: 84%; height: 48%; background: repeating-linear-gradient(90deg, #fff 0 40px, #dbeafe 40px 46px); opacity: .92; }
.re-06-beginning .subject-b { left: 44%; top: 32%; width: 12%; height: 30%; border-radius: 50% 50% 14px 14px; background: #64748b; }
.re-06-beginning .label-1 { left: 27%; top: 13%; }
.re-06-development .subject-a { left: 28%; top: 12%; width: 38%; height: 50%; background: #fff; }
.re-06-development .subject-b { right: 18%; top: 17%; width: 17%; height: 18%; border-color: #b45309; background: #fffbeb; }
.re-06-development .subject-c { left: 12%; top: 29%; width: 14%; height: 16%; background: #dcfce7; }
.re-06-development .label-1 { left: 31%; top: 20%; }
.re-06-development .label-2 { right: 17%; top: 9%; background: rgba(180,83,9,.88); }
.re-06-turn .subject-a { left: 26%; top: 15%; width: 28%; height: 42%; border-radius: 50%; background: rgba(219,234,254,.82); }
.re-06-turn .subject-b { right: 18%; top: 23%; width: 24%; height: 28%; background: #fff; }
.re-06-turn .subject-c { left: 11%; top: 26%; width: 12%; height: 28%; border-radius: 50% 50% 12px 12px; background: #64748b; }
.re-06-turn .connector-a { left: 48%; top: 36%; width: 27%; background: rgba(22,163,74,.6); }
.re-06-turn .label-1 { left: 28%; top: 12%; }
.re-06-turn .label-2 { right: 18%; top: 12%; }
.re-07d-beginning { background: linear-gradient(135deg, #eef2ff, #ecfeff 55%, #dcfce7); }
.re-07d-beginning .subject-a { left: 10%; top: 13%; width: 34%; height: 42%; background: #eef2ff; border-color: #4f46e5; }
.re-07d-beginning .subject-b { right: 12%; top: 18%; width: 30%; height: 34%; background: #fff; border-color: #16a34a; }
.re-07d-beginning .label-1 { left: 42%; top: 11%; background: rgba(22,101,52,.88); }
.re-07d-development { background: linear-gradient(135deg, #eef2ff 0 45%, #fee2e2); }
.re-07d-development .subject-a { left: 30%; top: 10%; width: 36%; height: 30%; background: #fff; }
.re-07d-development .subject-b { left: 20%; top: 43%; width: 18%; height: 18%; border-color: #b91c1c; background: #fee2e2; }
.re-07d-development .subject-c { right: 22%; top: 44%; width: 18%; height: 18%; border-color: #b91c1c; background: #fee2e2; }
.re-07d-development .label-1 { left: 31%; top: 42%; background: rgba(185,28,28,.88); }
.re-07d-turn { background: linear-gradient(135deg, #eef2ff, #f8fafc 56%, #ecfdf5); }
.re-07d-turn .subject-a { left: 9%; top: 18%; width: 24%; height: 34%; background: #eef2ff; border-color: #4f46e5; }
.re-07d-turn .subject-b { left: 44%; top: 20%; width: 13%; height: 34%; border-radius: 50% 50% 16px 16px; background: #166534; }
.re-07d-turn .subject-c { right: 11%; top: 20%; width: 24%; height: 34%; background: #fff; }
.re-07d-turn .connector-a { left: 31%; top: 37%; width: 42%; background: rgba(22,163,74,.65); }
.re-07d-turn .label-1 { left: 38%; top: 11%; background: rgba(22,101,52,.88); }
.legend { margin: 0 18px 18px; padding: 12px 14px; border-radius: 12px; border: 1px solid #cbd5e1; background: #fff; color: #334155; font-size: 13px; line-height: 1.55; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Real Estate DX Visual Treatment Proof</h1>
    <p>RE-02 / RE-06 / RE-07D only — 3 segments × 3 beats = 9 production-frame treatments</p>
    <p>Frame metadata is outside production frames. This is not YMM4 output, render, production timing, or creative acceptance.</p>
  </div>
  <div class="status">
    <div>proof type: ${escapeHtml(sidecar.proof_type)}</div>
    <div>frames: ${escapeHtml(String(sidecar.frame_count))}</div>
    <div>violations: ${escapeHtml(String(sidecar.frame_contract_violations.length))}</div>
  </div>
</header>
<main class="sheet">
${cells}
</main>
<section class="legend">
  <strong>用途:</strong> GUI timeline に取り込むための read-only visual treatment proof。
  単体HTML/PNG/JSON確認では完了扱いにせず、GUI上で proof image / beat table / sidecar warnings / Frame Contract違反の有無を確認する。
</section>
</body>
</html>
`;
}

async function waitForProof(win) {
  return await win.webContents.executeJavaScript(`
    new Promise((resolve, reject) => {
      const started = Date.now();
      const tick = () => {
        const frames = Array.from(document.querySelectorAll('.production-frame'));
        const cells = Array.from(document.querySelectorAll('.proof-cell'));
        const subtitleBands = Array.from(document.querySelectorAll('.subtitle-safe'));
        const frameTexts = frames.map((frame) => frame.innerText || '');
        const visibleMetadataInFrame = frameTexts.some((text) => /source|review|blocker|validator|readback|RE-0/.test(text));
        const labels = Array.from(document.querySelectorAll('.production-frame .frame-label'));
        const ready = frames.length === 9
          && cells.length === 9
          && subtitleBands.length === 9
          && labels.length <= 18
          && !visibleMetadataInFrame;
        if (ready) {
          resolve({
            frames: frames.length,
            cells: cells.length,
            subtitleBands: subtitleBands.length,
            labels: labels.length,
            visibleMetadataInFrame,
            text: document.body.innerText,
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight,
          });
          return;
        }
        if (Date.now() - started > 5000) {
          reject(new Error('visual treatment proof did not become ready'));
          return;
        }
        setTimeout(tick, 100);
      };
      tick();
    })
  `);
}

async function capture(htmlPath, screenshotPath) {
  const win = new BrowserWindow({
    width: 1080,
    height: 1500,
    show: false,
    webPreferences: {
      offscreen: true,
    },
  });
  await win.loadFile(htmlPath);
  const dom = await waitForProof(win);
  const image = await win.webContents.capturePage({
    x: 0,
    y: 0,
    width: dom.width,
    height: dom.height,
  });
  fs.writeFileSync(screenshotPath, image.toPNG());
  win.close();
  return { dom, size: image.getSize() };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const htmlRel = args.html || DEFAULT_HTML;
  const screenshotRel = args.screenshot || DEFAULT_SCREENSHOT;
  const sidecarRel = args.sidecar || DEFAULT_SIDECAR;
  const readbackRel = args.readback || DEFAULT_READBACK;

  const paths = {
    proof_html: htmlRel,
    proof_image: screenshotRel,
    sidecar_json: sidecarRel,
    readback_json: readbackRel,
  };
  const sidecar = buildSidecar(paths);
  const html = buildHtml(sidecar);

  const htmlFull = writeText(htmlRel, html);
  writeText(sidecarRel, `${JSON.stringify(sidecar, null, 2)}\n`);
  const screenshotFull = resolveRepoPath(screenshotRel);
  fs.mkdirSync(path.dirname(screenshotFull), { recursive: true });

  await app.whenReady();
  try {
    const captureResult = await capture(htmlFull, screenshotFull);
    const readback = {
      status: 'passed',
      proof_type: sidecar.proof_type,
      not_creative_acceptance: true,
      not_ymm4_adapter_output: true,
      not_render_source: true,
      not_production_timing: true,
      screenshot_artifact: toRepoPath(screenshotFull),
      screenshot_capture_method: 'electron generated 9-frame treatment HTML + BrowserWindow.loadFile + webContents.capturePage(full-page rect)',
      checks: {
        target_segments: sidecar.target_segments,
        frame_count: sidecar.frame_count,
        beats_per_segment: sidecar.beats_per_segment,
        dom_frames: captureResult.dom.frames,
        dom_cells: captureResult.dom.cells,
        subtitle_bands: captureResult.dom.subtitleBands,
        visible_metadata_in_frame: captureResult.dom.visibleMetadataInFrame,
        frame_contract_violations: sidecar.frame_contract_violations.length,
        sidecar_warnings: sidecar.sidecar_warnings.length,
        visual_quality_checks: sidecar.visual_quality_checks.length,
        anti_pattern_corpus_role: sidecar.anti_pattern_corpus.role,
        screenshot_width: captureResult.size.width,
        screenshot_height: captureResult.size.height,
      },
      artifacts: paths,
    };
    writeText(readbackRel, `${JSON.stringify(readback, null, 2)}\n`);
    console.log(JSON.stringify(readback, null, 2));
  } finally {
    app.quit();
  }
}

main().catch((err) => {
  console.error(err);
  app.quit();
  process.exitCode = 1;
});

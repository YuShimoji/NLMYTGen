// StrikeZone — リアルゾーン + 球軌跡 + 際どい球のズーム演出
// Real proportions: ホームベース幅 ≈ 43cm、ボール直径 ≈ 7.4cm → 比率 1:5.8
// よってボール半径 = ゾーン幅(2)の 1/11.6 ≈ 0.085(従来0.105を縮小)
//
// props:
//   pitches: [{ num, type, typeJa, kmh, x, y, result, startX?, startY? }]
//   currentPitchIdx: 表示中の球数
//   teamColor, batterSide, showHeatmap, width, height, animateLatest
//   zoomMode: 'auto' | 'always' | 'off' — 際どい球(ボーダー±0.18以内)で自動ズーム
//   showStadiumBackground: false にすると背景SVGを描かず透明に(画像スロット重ね用)
//   showBatterSilhouette: シルエットを描くか
//   variant: 'minimal' | 'standard' | 'detailed'

const TRAJECTORY_CURVE = {
  FF: { dx: 0,    dy: -0.05 },
  FT: { dx: 0.1,  dy: -0.05 },
  SL: { dx: 0.35, dy: 0.05 },
  CB: { dx: 0,    dy: 0.45 },
  CH: { dx: 0.05, dy: 0.25 },
  SP: { dx: 0,    dy: 0.55 },
  CT: { dx: -0.2, dy: 0 },
};

const PITCH_COLORS = {
  FF: '#EF4444',
  FT: '#F87171',
  SL: '#FBBF24',
  CB: '#3B82F6',
  CH: '#10B981',
  SP: '#A855F7',
  CT: '#F97316',
};

const RESULT_STYLE = {
  CalledStrike: { fill: '#EF4444', label: '見逃' },
  SwingingStrike: { fill: '#DC2626', label: '空振' },
  Foul: { fill: '#FACC15', label: 'ファウル' },
  Ball: { fill: '#3B82F6', label: 'ボール' },
  InPlay: { fill: '#10B981', label: '打球' },
  HitByPitch: { fill: '#8B5CF6', label: '死球' },
};

// 実物比率: ストライクゾーン幅(2) ≈ ホームベース幅43cm
// ボール直径7.4cm → ボール半径 ≈ (2/43)*(7.4/2) ≈ 0.086
const BALL_RADIUS = 0.086;

function StrikeZone({
  pitches = [],
  currentPitchIdx = -1,
  teamColor = '#F97316',
  variant = 'standard',
  batterSide = 'L',
  showHeatmap = false,
  width = 320,
  height = 380,
  animateLatest = true,
  zoomMode = 'off',
  showStadiumBackground = true,
  showBatterSilhouette = true,
}) {
  const padX = 0.6, padY = 0.55;
  const zoneL = -1, zoneR = 1, zoneT = -1, zoneB = 1;
  const viewL = zoneL - padX, viewR = zoneR + padX;
  const viewT = zoneT - padY, viewB = zoneB + padY;
  const vw = viewR - viewL;
  const vh = viewB - viewT;

  const mirrorX = (x) => batterSide === 'L' ? -x : x;

  const visiblePitches = currentPitchIdx >= 0
    ? pitches.slice(0, currentPitchIdx + 1)
    : pitches;
  const latestIdx = visiblePitches.length - 1;
  const latestPitch = visiblePitches[latestIdx];

  // 際どい球ズーム判定: ボーダー±0.18以内、または直近の判定球
  const isCloseCall = latestPitch && (
    Math.abs(Math.abs(latestPitch.x) - 1) < 0.18 ||
    Math.abs(Math.abs(latestPitch.y) - 1) < 0.18
  );
  const shouldZoom = zoomMode === 'always' || (zoomMode === 'auto' && isCloseCall);

  // ズーム時のviewBox(ゾーン中心+終端中心の重み付き)
  const zoomCx = latestPitch ? mirrorX(latestPitch.x) * 0.4 : 0;
  const zoomCy = latestPitch ? latestPitch.y * 0.4 : 0;
  const zoomSize = 1.65; // 表示する横幅(縦も同じスケール)
  const aspect = vh / vw;

  const gridLines = [-1/3, 1/3];

  // viewBoxアニメーション用のkey(球が変わるたびにアニメ再開)
  const animKey = `${latestIdx}-${currentPitchIdx}`;
  const fromVb = `${viewL} ${viewT} ${vw} ${vh}`;
  const toVb = `${zoomCx - zoomSize/2} ${zoomCy - (zoomSize*aspect)/2} ${zoomSize} ${zoomSize*aspect}`;

  return (
    <svg viewBox={fromVb} width={width} height={height}
         preserveAspectRatio="xMidYMid meet"
         style={{ display: 'block', overflow: 'visible' }}>
      {shouldZoom && animateLatest && (
        <animate key={animKey} attributeName="viewBox"
                 values={`${fromVb}; ${fromVb}; ${toVb}; ${toVb}; ${fromVb}`}
                 keyTimes="0; 0.3; 0.55; 0.85; 1"
                 dur="3s" fill="freeze" begin="0.7s" />
      )}
      <defs>
        <linearGradient id="zone-bg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(255,255,255,0.04)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.08)" />
        </linearGradient>
        <filter id="pitch-glow">
          <feGaussianBlur stdDeviation="0.04" />
        </filter>
        <linearGradient id="sky-bg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#1a2438" />
          <stop offset="55%" stopColor="#2a3550" />
          <stop offset="100%" stopColor="#1a1812" />
        </linearGradient>
        <linearGradient id="dirt-grad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#5a3a22" />
          <stop offset="100%" stopColor="#3d2614" />
        </linearGradient>
        <linearGradient id="grass-grad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#2d5530" />
          <stop offset="100%" stopColor="#1f3a22" />
        </linearGradient>
        <linearGradient id="zone-front" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(255,255,255,0.08)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.02)" />
        </linearGradient>
      </defs>

      {/* スタジアム背景 — 画像スロット利用時はOFF */}
      {showStadiumBackground && (
        <>
          <rect x={viewL} y={viewT} width={vw} height={vh * 0.55} fill="url(#sky-bg)" opacity="0.85" />
          <path d={`M ${viewL} ${viewT + vh * 0.55}
                     L ${viewR} ${viewT + vh * 0.55}
                     L ${viewR} ${viewT + vh * 0.72}
                     L ${viewL} ${viewT + vh * 0.72} Z`}
                fill="url(#grass-grad)" opacity="0.75" />
          <path d={`M ${viewL} ${viewT + vh * 0.72}
                     L ${viewR} ${viewT + vh * 0.72}
                     L ${viewR + 0.3} ${viewB}
                     L ${viewL - 0.3} ${viewB} Z`}
                fill="url(#dirt-grad)" opacity="0.9" />

          <line x1={0} y1={zoneB + 0.42}
                x2={viewL - 0.15} y2={viewT + vh * 0.72}
                stroke="rgba(255,255,255,0.55)" strokeWidth="0.018" />
          <line x1={0} y1={zoneB + 0.42}
                x2={viewR + 0.15} y2={viewT + vh * 0.72}
                stroke="rgba(255,255,255,0.55)" strokeWidth="0.018" />

          {[-1, 1].map((s) => {
            const inner = 0.42 * s, outer = 0.95 * s;
            const top = zoneB + 0.22, bot = zoneB + 0.58;
            return (
              <path key={s}
                    d={`M ${inner} ${top} L ${outer} ${top}
                        L ${outer + 0.08 * s} ${bot} L ${inner + 0.04 * s} ${bot} Z`}
                    fill="rgba(255,255,255,0.04)"
                    stroke="rgba(255,255,255,0.5)"
                    strokeWidth="0.014" />
            );
          })}

          <path
            d={`M -0.18 ${zoneB + 0.36} L 0.18 ${zoneB + 0.36}
                 L 0.20 ${zoneB + 0.46} L 0 ${zoneB + 0.54} L -0.20 ${zoneB + 0.46} Z`}
            fill="rgba(255,255,255,0.92)"
            stroke="rgba(0,0,0,0.4)"
            strokeWidth="0.008"
          />

          {showBatterSilhouette && variant !== 'minimal' && (
            <g opacity="0.32">
              <ellipse cx={batterSide === 'L' ? -1.0 : 1.0} cy={-0.05}
                       rx={0.13} ry={0.18} fill="#0a0a0a" />
              <path d={batterSide === 'L'
                ? `M -1.15 0.1 L -0.85 0.1 L -0.78 1.1 L -1.22 1.1 Z`
                : `M 0.85 0.1 L 1.15 0.1 L 1.22 1.1 L 0.78 1.1 Z`}
                    fill="#0a0a0a" />
              <line x1={batterSide === 'L' ? -0.85 : 0.85} y1={0.15}
                    x2={batterSide === 'L' ? -0.4 : 0.4} y2={-0.7}
                    stroke="#3a2818" strokeWidth="0.045" strokeLinecap="round" />
            </g>
          )}
        </>
      )}

      {/* ストライクゾーン本体 */}
      <path d={`M ${zoneL} ${zoneB} L ${zoneR} ${zoneB}
                 L ${zoneR + 0.08} ${zoneB + 0.06} L ${zoneL - 0.08} ${zoneB + 0.06} Z`}
            fill="rgba(0,0,0,0.4)" />
      <rect x={zoneL} y={zoneT} width={2} height={2}
            fill="url(#zone-front)"
            stroke="rgba(255,255,255,0.85)"
            strokeWidth="0.022" />
      <line x1={zoneL} y1={zoneT} x2={zoneR} y2={zoneT}
            stroke="rgba(255,255,255,0.95)" strokeWidth="0.012" />

      {variant !== 'minimal' && gridLines.map((g, i) => (
        <g key={i}>
          <line x1={g} y1={zoneT} x2={g} y2={zoneB}
                stroke="rgba(255,255,255,0.18)" strokeWidth="0.01" strokeDasharray="0.04 0.04" />
          <line x1={zoneL} y1={g} x2={zoneR} y2={g}
                stroke="rgba(255,255,255,0.18)" strokeWidth="0.01" strokeDasharray="0.04 0.04" />
        </g>
      ))}

      {showHeatmap && variant === 'detailed' && (
        <g opacity="0.5">
          {[[-2/3, -2/3, 0.4], [0, -2/3, 0.6], [2/3, -2/3, 0.3],
            [-2/3, 0, 0.7], [0, 0, 0.85], [2/3, 0, 0.5],
            [-2/3, 2/3, 0.2], [0, 2/3, 0.4], [2/3, 2/3, 0.3]].map(([cx, cy, intensity], i) => (
            <rect key={i} x={cx - 1/3} y={cy - 1/3} width={2/3} height={2/3}
                  fill={teamColor} opacity={intensity * 0.6} />
          ))}
        </g>
      )}

      <defs>
        {visiblePitches.map((p, i) => {
          const color = PITCH_COLORS[p.type] || teamColor;
          return (
            <linearGradient key={`tg-${i}`} id={`trail-${i}`} gradientUnits="userSpaceOnUse"
                            x1={mirrorX(p.startX !== undefined ? p.startX : (p.x * 0.15))}
                            y1={p.startY !== undefined ? p.startY : -1.5}
                            x2={mirrorX(p.x)} y2={p.y}>
              <stop offset="0%" stopColor={color} stopOpacity="0" />
              <stop offset="55%" stopColor={color} stopOpacity="0.15" />
              <stop offset="100%" stopColor={color} stopOpacity="0.95" />
            </linearGradient>
          );
        })}
      </defs>

      {visiblePitches.map((p, i) => {
        const isLatest = i === latestIdx;
        const color = PITCH_COLORS[p.type] || teamColor;
        const result = RESULT_STYLE[p.result] || { fill: color };
        const cx = mirrorX(p.x);
        const cy = p.y;
        const startX = mirrorX(p.startX !== undefined ? p.startX : (p.x * 0.15));
        const startY = p.startY !== undefined ? p.startY : -1.5;
        const curveOffsets = TRAJECTORY_CURVE[p.type] || { dx: 0, dy: 0 };
        const ctrlX = startX * 0.35 + cx * 0.65 + (batterSide === 'L' ? -curveOffsets.dx : curveOffsets.dx);
        const ctrlY = startY * 0.35 + cy * 0.65 + curveOffsets.dy;
        const path = `M ${startX} ${startY} Q ${ctrlX} ${ctrlY} ${cx} ${cy}`;
        const animDur = animateLatest && isLatest ? 0.7 : 0;
        return (
          <g key={i} opacity={isLatest ? 1 : 0.4}>
            {isLatest && (
              <circle cx={startX} cy={startY} r={0.022}
                      fill={color} opacity="0.5" />
            )}
            {isLatest && animateLatest && (
              <path d={path} fill="none" stroke={`url(#trail-${i})`}
                    strokeWidth="0.038" strokeLinecap="round"
                    strokeDasharray="3" strokeDashoffset="3">
                <animate attributeName="stroke-dashoffset" from="3" to="0"
                         dur={`${animDur}s`} fill="freeze" />
              </path>
            )}
            {!isLatest && (
              <path d={path} fill="none" stroke={`url(#trail-${i})`}
                    strokeWidth="0.018" strokeLinecap="round" opacity="0.5" />
            )}
            {isLatest && animateLatest && (
              <circle cx={cx} cy={cy} r={0.18} fill={result.fill} opacity="0"
                      filter="url(#pitch-glow)">
                <animate attributeName="opacity" values="0;0;0.5;0.2"
                         keyTimes={`0;${animDur/(animDur+0.6)};${(animDur+0.05)/(animDur+0.6)};1`}
                         dur={`${animDur+0.6}s`} fill="freeze" />
              </circle>
            )}
            {isLatest && animateLatest ? (
              <g>
                <circle r={BALL_RADIUS} fill={result.fill}
                        stroke="#fff" strokeWidth="0.018">
                  <animateMotion dur={`${animDur}s`} fill="freeze" path={path} rotate="auto" />
                </circle>
                <circle cx={cx} cy={cy} r={BALL_RADIUS} fill="none"
                        stroke={result.fill} strokeWidth="0.018" opacity="0">
                  <animate attributeName="opacity" from="0" to="0.8"
                           begin={`${animDur}s`} dur="0.05s" fill="freeze" />
                  <animate attributeName="r" from={BALL_RADIUS} to={BALL_RADIUS * 4}
                           begin={`${animDur}s`} dur="1.2s" repeatCount="indefinite" />
                </circle>
              </g>
            ) : (
              <circle cx={cx} cy={cy} r={BALL_RADIUS}
                      fill={result.fill}
                      stroke="#fff" strokeWidth="0.012" />
            )}
            {/* 球番号は球の外側に小さく表示 */}
            {(!isLatest || !animateLatest) && (
              <text x={cx + BALL_RADIUS + 0.04} y={cy + 0.04} textAnchor="start"
                    fontSize="0.1" fontWeight="700" fontFamily="Geist Mono, monospace"
                    fill="rgba(255,255,255,0.65)">
                {p.num}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

window.StrikeZone = StrikeZone;
window.PITCH_COLORS = PITCH_COLORS;
window.RESULT_STYLE = RESULT_STYLE;
window.BALL_RADIUS = BALL_RADIUS;

// Diamond — ベース図 + アウト + カウント
// props: bases {first, second, third}, outs (0-3), balls (0-4), strikes (0-3)

function Diamond({ bases = {}, outs = 0, balls = 0, strikes = 0,
                   teamColor = '#F97316', size = 100, showCount = true,
                   variant = 'standard' }) {
  const cx = size / 2;
  const cy = size / 2 + size * 0.05;
  const r = size * 0.28;

  const baseStyle = (active) => ({
    fill: active ? teamColor : 'rgba(255,255,255,0.1)',
    stroke: active ? teamColor : 'rgba(255,255,255,0.4)',
    strokeWidth: 1.5,
  });

  return (
    <svg width={size} height={showCount ? size + 30 : size} viewBox={`0 0 ${size} ${showCount ? size + 30 : size}`}>
      {/* ベース */}
      <g>
        {/* 二塁 */}
        <rect x={cx - r * 0.18} y={cy - r - r * 0.18}
              width={r * 0.36} height={r * 0.36}
              transform={`rotate(45 ${cx} ${cy - r})`}
              {...baseStyle(bases.second)} />
        {/* 三塁 */}
        <rect x={cx - r - r * 0.18} y={cy - r * 0.18}
              width={r * 0.36} height={r * 0.36}
              transform={`rotate(45 ${cx - r} ${cy})`}
              {...baseStyle(bases.third)} />
        {/* 一塁 */}
        <rect x={cx + r - r * 0.18} y={cy - r * 0.18}
              width={r * 0.36} height={r * 0.36}
              transform={`rotate(45 ${cx + r} ${cy})`}
              {...baseStyle(bases.first)} />
        {/* ホーム */}
        <path d={`M ${cx - r * 0.18} ${cy + r}
                  L ${cx + r * 0.18} ${cy + r}
                  L ${cx + r * 0.2} ${cy + r + r * 0.12}
                  L ${cx} ${cy + r + r * 0.22}
                  L ${cx - r * 0.2} ${cy + r + r * 0.12} Z`}
              fill="rgba(255,255,255,0.18)"
              stroke="rgba(255,255,255,0.5)" strokeWidth={1} />
      </g>

      {/* B/S/O カウント */}
      {showCount && (
        <g transform={`translate(0, ${size + 4})`}>
          {/* B */}
          <text x={cx - size * 0.32} y={size * 0.12} fontSize={size * 0.1}
                fontFamily="Geist Mono, monospace" fontWeight="600"
                fill="rgba(255,255,255,0.6)" textAnchor="middle">B</text>
          {[0, 1, 2, 3].map(i => (
            <circle key={i} cx={cx - size * 0.18 + i * size * 0.08}
                    cy={size * 0.085} r={size * 0.025}
                    fill={i < balls ? '#3B82F6' : 'rgba(255,255,255,0.15)'} />
          ))}
          {/* S */}
          <text x={cx + size * 0.13} y={size * 0.12} fontSize={size * 0.1}
                fontFamily="Geist Mono, monospace" fontWeight="600"
                fill="rgba(255,255,255,0.6)" textAnchor="middle">S</text>
          {[0, 1, 2].map(i => (
            <circle key={i} cx={cx + size * 0.22 + i * size * 0.08}
                    cy={size * 0.085} r={size * 0.025}
                    fill={i < strikes ? '#FACC15' : 'rgba(255,255,255,0.15)'} />
          ))}
          {/* O */}
          {variant !== 'minimal' && (
            <>
              <text x={cx - size * 0.18} y={size * 0.27} fontSize={size * 0.1}
                    fontFamily="Geist Mono, monospace" fontWeight="600"
                    fill="rgba(255,255,255,0.6)" textAnchor="middle">O</text>
              {[0, 1, 2].map(i => (
                <circle key={i} cx={cx - size * 0.04 + i * size * 0.08}
                        cy={size * 0.245} r={size * 0.025}
                        fill={i < outs ? '#EF4444' : 'rgba(255,255,255,0.15)'} />
              ))}
            </>
          )}
        </g>
      )}
    </svg>
  );
}

window.Diamond = Diamond;

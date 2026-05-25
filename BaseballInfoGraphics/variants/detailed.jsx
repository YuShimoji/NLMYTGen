function DetailedVariant({ data, currentPitchIdx, teamColor, density, showRomaji = false, statMode = 'simple', animateLatest = true }) {
  const { teams, score, atBat, visual = {} } = data;
  const pitches = atBat.pitches || [];
  const safePitchIdx = Math.max(0, Math.min(pitches.length - 1, currentPitchIdx));
  const currentPitch = pitches[safePitchIdx] || pitches[0] || {};
  const previousPitch = safePitchIdx > 0 ? pitches[safePitchIdx - 1] : null;
  const visiblePitches = pitches.slice(0, safePitchIdx + 1);
  const compact = density === 'compact';
  const activeClaim = currentPitch.claim || visual.claim || 'この一球の意味を、スコアとカウントから読む';

  return (
    <div style={frameStyle(compact)}>
      <BroadcastHeader
        teams={teams}
        score={score}
        visual={visual}
        teamColor={teamColor}
      />

      <div style={bodyGridStyle(compact)}>
        <div style={sideStackStyle}>
          <PlayerPanel
            role="pitcher"
            player={atBat.pitcher}
            teamColor={teams.home.primary}
            showRomaji={showRomaji}
            statMode={statMode}
          />
          <CountStatus score={score} teamColor={teamColor} />
        </div>

        <main style={mainStageStyle}>
          <ClaimBand
            claim={activeClaim}
            eventLabel={visual.eventLabel}
            teamColor={teamColor}
          />
          <PitchStage
            pitches={pitches}
            currentPitch={currentPitch}
            previousPitch={previousPitch}
            currentPitchIdx={safePitchIdx}
            teamColor={teamColor}
            compact={compact}
            ambientBackdrop={visual.ambientBackdrop}
          />
        </main>

        <div style={sideStackStyle}>
          <PitchHistoryPanel
            pitches={visiblePitches}
            currentPitchIdx={safePitchIdx}
            teamColor={teamColor}
          />
          <PlayerPanel
            role="batter"
            player={atBat.batter}
            teamColor={teams.away.primary}
            showRomaji={showRomaji}
            statMode={statMode}
          />
        </div>
      </div>

      <FooterRibbon
        sourceLabel={visual.sourceLabel}
        watchPoint={visual.watchPoint}
      />
    </div>
  );
}

const palette = {
  bg: '#070b13',
  panel: 'rgba(10,16,29,0.92)',
  panelSoft: 'rgba(15,23,42,0.72)',
  border: 'rgba(148,163,184,0.22)',
  text: '#f8fafc',
  muted: 'rgba(226,232,240,0.62)',
  faint: 'rgba(226,232,240,0.36)',
  amber: '#FACC15',
  blue: '#38BDF8',
  red: '#F43F5E',
};

function frameStyle(compact) {
  return {
    width: '100%',
    height: '100%',
    position: 'relative',
    overflow: 'hidden',
    color: palette.text,
    background: [
      'radial-gradient(circle at 74% 28%, rgba(56,189,248,0.18), transparent 27%)',
      'radial-gradient(circle at 24% 18%, rgba(250,204,21,0.12), transparent 24%)',
      'linear-gradient(135deg, #050711 0%, #0b1220 45%, #020617 100%)',
    ].join(','),
    padding: compact ? 18 : 22,
    fontFamily: '"Noto Sans JP", system-ui, sans-serif',
  };
}

function bodyGridStyle(compact) {
  return {
    display: 'grid',
    gridTemplateColumns: compact ? '230px 1fr 250px' : '250px 1fr 270px',
    gap: compact ? 14 : 18,
    height: compact ? 548 : 538,
    marginTop: compact ? 12 : 16,
  };
}

const sideStackStyle = {
  minHeight: 0,
  display: 'flex',
  flexDirection: 'column',
  gap: 14,
};

const mainStageStyle = {
  minWidth: 0,
  minHeight: 0,
  display: 'grid',
  gridTemplateRows: '118px 1fr',
  gap: 14,
};

function BroadcastHeader({ teams, score, visual, teamColor }) {
  const halfLabel = score.half === 'top' ? '表' : '裏';
  return (
    <header style={headerStyle}>
      <div style={scoreBlockStyle}>
        <TeamCode code={teams.away.code} color={teams.away.primary} />
        <div style={scoreNumberStyle}>{score.away}</div>
        <div style={dashStyle}>-</div>
        <div style={scoreNumberStyle}>{score.home}</div>
        <TeamCode code={teams.home.code} color={teams.home.primary} />
      </div>
      <div style={headerMetaStyle}>
        <div style={{ ...labelStyle, color: teamColor }}>{visual.eventLabel || 'PITCH EVENT'}</div>
        <div style={inningStyle}>{score.inning}回{halfLabel} · {score.outs} OUT · B{score.balls}-S{score.strikes}</div>
      </div>
    </header>
  );
}

function TeamCode({ code, color }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      minWidth: 92,
      justifyContent: 'center',
    }}>
      <span style={{ width: 9, height: 9, borderRadius: 999, background: color, boxShadow: `0 0 18px ${color}` }} />
      <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 22, fontWeight: 800, letterSpacing: '0.08em' }}>{code}</span>
    </div>
  );
}

const headerStyle = {
  height: 88,
  display: 'grid',
  gridTemplateColumns: '1fr 360px',
  alignItems: 'stretch',
  border: `1px solid ${palette.border}`,
  background: 'linear-gradient(90deg, rgba(15,23,42,0.96), rgba(15,23,42,0.7))',
  boxShadow: '0 18px 50px rgba(0,0,0,0.28)',
};

const scoreBlockStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 18,
};

const scoreNumberStyle = {
  fontFamily: '"Bebas Neue", sans-serif',
  fontSize: 68,
  lineHeight: 0.9,
  fontVariantNumeric: 'tabular-nums',
};

const dashStyle = {
  color: palette.faint,
  fontSize: 28,
  fontFamily: '"Geist Mono", monospace',
};

const headerMetaStyle = {
  borderLeft: `1px solid ${palette.border}`,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  gap: 8,
  padding: '0 24px',
};

const labelStyle = {
  fontFamily: '"Geist Mono", monospace',
  fontSize: 10,
  fontWeight: 800,
  letterSpacing: '0.22em',
  color: palette.muted,
};

const inningStyle = {
  fontSize: 24,
  fontWeight: 900,
  letterSpacing: '0.03em',
};

function ClaimBand({ claim, eventLabel, teamColor }) {
  return (
    <section style={claimBandStyle}>
      <div style={{ ...labelStyle, color: teamColor }}>{eventLabel || 'ONE SCREEN · ONE CLAIM'}</div>
      <div style={claimTextStyle}>{claim}</div>
    </section>
  );
}

const claimBandStyle = {
  border: `1px solid ${palette.border}`,
  background: 'linear-gradient(135deg, rgba(15,23,42,0.96), rgba(2,6,23,0.88))',
  padding: '18px 22px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  gap: 10,
  boxShadow: '0 18px 44px rgba(0,0,0,0.25)',
};

const claimTextStyle = {
  fontSize: 29,
  lineHeight: 1.18,
  fontWeight: 900,
  letterSpacing: '-0.03em',
};

function PitchStage({ pitches, currentPitch, previousPitch, currentPitchIdx, teamColor, compact, ambientBackdrop, animateLatest = true }) {
  const backdrop = ambientBackdrop || {};
  return (
    <section style={pitchStageStyle}>
      <div
        style={ambientBackdropLayerStyle(backdrop)}
        data-ambient-backdrop-kind={backdrop.kind || 'css_grid'}
        data-ambient-backdrop-provenance={backdrop.provenance || 'none'}
        data-ambient-backdrop-usage-stage={backdrop.usageStage || 'design_preview'}
        aria-hidden="true"
      />
      <div style={pitchSummaryStyle}>
        <PitchSummary currentPitch={currentPitch} previousPitch={previousPitch} teamColor={teamColor} />
      </div>
      <div style={zoneShellStyle(compact)}>
        <StrikeZone
          pitches={pitches}
          currentPitchIdx={currentPitchIdx}
          teamColor={teamColor}
          variant="detailed"
          width={compact ? 480 : 520}
          height={compact ? 330 : 360}
          animateLatest={animateLatest}
          showHeatmap={false}
          showBatterSilhouette={false}
        />
      </div>
    </section>
  );
}

const pitchStageStyle = {
  minHeight: 0,
  position: 'relative',
  border: `1px solid ${palette.border}`,
  background: '#020617',
  overflow: 'hidden',
};

function ambientBackdropLayerStyle(ambientBackdrop) {
  const imageUrl = typeof ambientBackdrop.imageUrl === 'string' ? ambientBackdrop.imageUrl.trim() : '';
  const safeUrl = imageUrl.replace(/"/g, '\\"');
  const imageLayers = [
    'linear-gradient(180deg, rgba(2,6,23,0.18), rgba(2,6,23,0.84))',
    'radial-gradient(circle at 64% 38%, rgba(34,197,94,0.18), transparent 34%)',
    `url("${safeUrl}")`,
  ];
  const gridLayers = [
    'linear-gradient(rgba(148,163,184,0.055) 1px, transparent 1px)',
    'linear-gradient(90deg, rgba(148,163,184,0.055) 1px, transparent 1px)',
    'radial-gradient(circle at 50% 78%, rgba(34,197,94,0.18), transparent 34%)',
    'linear-gradient(180deg, rgba(15,23,42,0.62), rgba(2,6,23,0.86))',
  ];
  return {
    position: 'absolute',
    inset: 0,
    zIndex: 0,
    pointerEvents: 'none',
    background: (imageUrl ? imageLayers : gridLayers).join(','),
    backgroundSize: imageUrl ? 'auto, auto, cover' : '42px 42px, 42px 42px, auto, auto',
    backgroundPosition: 'center',
    opacity: imageUrl ? 0.92 : 1,
    filter: imageUrl ? 'saturate(0.9) contrast(1.05)' : 'none',
  };
}

const pitchSummaryStyle = {
  position: 'absolute',
  top: 18,
  left: 18,
  right: 18,
  zIndex: 3,
};

function zoneShellStyle(compact) {
  return {
    position: 'absolute',
    left: '50%',
    top: compact ? 82 : 92,
    transform: 'translateX(-50%)',
    zIndex: 2,
    filter: 'drop-shadow(0 20px 36px rgba(0,0,0,0.42))',
  };
}

function PitchSummary({ currentPitch, previousPitch, teamColor }) {
  const velocityDelta = previousPitch && currentPitch.kmh != null && previousPitch.kmh != null
    ? currentPitch.kmh - previousPitch.kmh
    : null;
  const deltaText = velocityDelta == null
    ? 'OPENING PITCH'
    : `${velocityDelta > 0 ? '+' : ''}${velocityDelta} km/h vs prev`;

  return (
    <div style={pitchCardStyle}>
      <div>
        <div style={labelStyle}>CURRENT PITCH</div>
        <div style={pitchNameStyle}>
          <span style={{ color: teamColor }}>P{String(currentPitch.num || 0).padStart(2, '0')}</span>
          <span>{currentPitch.typeJa || currentPitch.type || '—'}</span>
          <span style={pitchTypeStyle}>{currentPitch.type || ''}</span>
        </div>
        <div style={resultStyle}>{currentPitch.resultJa || currentPitch.result || '—'} · {deltaText}</div>
      </div>
      <div style={velocityStyle}>
        <span>{currentPitch.kmh ?? '—'}</span>
        <small>km/h</small>
      </div>
    </div>
  );
}

const pitchCardStyle = {
  display: 'grid',
  gridTemplateColumns: '1fr 138px',
  alignItems: 'center',
  minHeight: 86,
  background: 'linear-gradient(90deg, rgba(2,6,23,0.94), rgba(15,23,42,0.74))',
  border: `1px solid ${palette.border}`,
  borderLeft: `4px solid ${palette.amber}`,
  padding: '14px 18px',
};

const pitchNameStyle = {
  display: 'flex',
  alignItems: 'baseline',
  gap: 12,
  marginTop: 8,
  fontSize: 24,
  lineHeight: 1,
  fontWeight: 900,
};

const pitchTypeStyle = {
  fontFamily: '"Geist Mono", monospace',
  fontSize: 11,
  color: palette.faint,
};

const resultStyle = {
  marginTop: 8,
  fontSize: 12,
  color: palette.muted,
  fontFamily: '"Geist Mono", monospace',
  letterSpacing: '0.02em',
};

const velocityStyle = {
  textAlign: 'right',
  fontFamily: '"Bebas Neue", sans-serif',
  lineHeight: 0.85,
};

function PlayerPanel({ role, player, teamColor, showRomaji, statMode }) {
  const isPitcher = role === 'pitcher';
  const stats = isPitcher
    ? [
        { label: 'THROWS', value: player.throws || '—' },
        { label: 'ERA', value: player.season?.era ?? '—' },
        { label: 'PC', value: player.today?.pc ?? '—' },
        { label: 'K', value: player.today?.k ?? '—' },
        { label: 'IP', value: player.today?.ip ?? '—' },
      ]
    : [
        { label: 'BATS', value: player.bats || '—' },
        { label: 'AVG', value: formatAverage(player.season?.avg) },
        { label: 'OPS', value: formatAverage(player.season?.ops) },
        { label: 'TODAY', value: `${player.today?.h ?? 0}-${player.today?.ab ?? 0}` },
        { label: 'vsP', value: `${player.vsP?.h ?? 0}-${player.vsP?.ab ?? 0}` },
      ];
  const panelTitle = isPitcher ? 'PITCHER' : 'BATTER';
  const handLabel = isPitcher ? `${player.throws || '—'}投` : `${player.bats || '—'}打`;

  return (
    <section style={panelStyle}>
      <div style={{ ...panelAccentStyle, background: teamColor }} />
      <div style={panelHeadStyle}>
        <div>
          <div style={labelStyle}>{panelTitle}</div>
          <div style={playerNameStyle}>
            <span style={{ color: teamColor }}>#{player.number ?? '—'}</span>
            <span>{player.name}</span>
          </div>
          {showRomaji && <div style={romajiStyle}>{player.nameEn}</div>}
        </div>
        <div style={handBadgeStyle}>{handLabel}</div>
      </div>
      <MajorStatGrid stats={stats} />
      {statMode === 'detailed' && (
        <div style={detailLineStyle}>
          {isPitcher
            ? `H ${player.today?.h ?? '—'} · BB ${player.today?.bb ?? '—'} · ER ${player.today?.er ?? '—'}`
            : `HR ${player.season?.hr ?? '—'} · RBI ${player.season?.rbi ?? '—'} · K ${player.today?.k ?? '—'}`}
        </div>
      )}
    </section>
  );
}

const panelStyle = {
  position: 'relative',
  overflow: 'hidden',
  minHeight: 172,
  border: `1px solid ${palette.border}`,
  background: palette.panel,
  padding: '18px 16px 16px 20px',
};

const panelAccentStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  width: 4,
  height: '100%',
};

const panelHeadStyle = {
  display: 'grid',
  gridTemplateColumns: '1fr auto',
  gap: 10,
  alignItems: 'start',
};

const playerNameStyle = {
  display: 'flex',
  gap: 8,
  alignItems: 'baseline',
  marginTop: 8,
  fontSize: 20,
  lineHeight: 1.1,
  fontWeight: 900,
  whiteSpace: 'nowrap',
  overflow: 'hidden',
  textOverflow: 'ellipsis',
};

const romajiStyle = {
  marginTop: 5,
  fontSize: 10,
  color: palette.faint,
  fontFamily: '"Geist Mono", monospace',
};

const handBadgeStyle = {
  minWidth: 42,
  padding: '6px 8px',
  textAlign: 'center',
  border: `1px solid ${palette.border}`,
  color: palette.muted,
  fontSize: 11,
  fontWeight: 800,
};

function MajorStatGrid({ stats }) {
  return (
    <div style={statGridStyle}>
      {stats.slice(0, 5).map((stat) => (
        <div key={stat.label} style={statBoxStyle}>
          <div style={statLabelStyle}>{stat.label}</div>
          <div style={statValueStyle}>{stat.value}</div>
        </div>
      ))}
    </div>
  );
}

const statGridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(5, 1fr)',
  gap: 7,
  marginTop: 18,
};

const statBoxStyle = {
  minWidth: 0,
  padding: '8px 5px',
  border: `1px solid ${palette.border}`,
  background: 'rgba(15,23,42,0.68)',
  textAlign: 'center',
};

const statLabelStyle = {
  fontSize: 8,
  color: palette.faint,
  fontFamily: '"Geist Mono", monospace',
};

const statValueStyle = {
  marginTop: 5,
  fontFamily: '"Bebas Neue", sans-serif',
  fontSize: 22,
  lineHeight: 0.9,
  fontVariantNumeric: 'tabular-nums',
};

const detailLineStyle = {
  marginTop: 12,
  color: palette.muted,
  fontSize: 11,
  fontFamily: '"Geist Mono", monospace',
};

function CountStatus({ score, teamColor }) {
  return (
    <section style={countPanelStyle}>
      <div style={{ ...labelStyle, color: teamColor }}>COUNT / RUNNERS</div>
      <div style={countBodyStyle}>
        <div style={{ width: 104 }}>
          <Diamond
            bases={score.bases}
            outs={score.outs}
            balls={score.balls}
            strikes={score.strikes}
            teamColor={teamColor}
            size={96}
            showCount={false}
            variant="standard"
          />
        </div>
        <div style={countRowsStyle}>
          <CountRow label="B" value={score.balls} max={4} color={palette.blue} />
          <CountRow label="S" value={score.strikes} max={3} color={palette.amber} />
          <CountRow label="O" value={score.outs} max={3} color={palette.red} />
        </div>
      </div>
    </section>
  );
}

const countPanelStyle = {
  flex: 1,
  border: `1px solid ${palette.border}`,
  background: palette.panelSoft,
  padding: 16,
  minHeight: 0,
};

const countBodyStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 14,
  marginTop: 12,
};

const countRowsStyle = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  gap: 10,
};

function CountRow({ label, value, max, color }) {
  return (
    <div style={countRowStyle}>
      <span style={countLabelStyle}>{label}</span>
      {Array.from({ length: max }).map((_, index) => (
        <span
          key={index}
          style={{
            width: 13,
            height: 13,
            borderRadius: 999,
            background: index < value ? color : 'rgba(148,163,184,0.18)',
            boxShadow: index < value ? `0 0 14px ${color}` : 'none',
          }}
        />
      ))}
    </div>
  );
}

const countRowStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
};

const countLabelStyle = {
  width: 18,
  color: palette.muted,
  fontFamily: '"Geist Mono", monospace',
  fontWeight: 800,
};

function PitchHistoryPanel({ pitches, currentPitchIdx, teamColor }) {
  return (
    <section style={historyPanelStyle}>
      <div style={{ ...labelStyle, color: teamColor }}>PITCH LOG</div>
      <div style={historyListStyle}>
        {pitches.map((pitch, index) => {
          const active = index === currentPitchIdx;
          return (
            <div key={pitch.num} style={historyItemStyle(active, teamColor)}>
              <div style={historyNumberStyle(active, teamColor)}>{pitch.num}</div>
              <div style={{ minWidth: 0 }}>
                <div style={historyPitchStyle}>{pitch.typeJa || pitch.type}</div>
                <div style={historyResultStyle}>{pitch.resultJa || pitch.result}</div>
              </div>
              <div style={historyVelocityStyle}>{pitch.kmh}</div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

const historyPanelStyle = {
  minHeight: 226,
  border: `1px solid ${palette.border}`,
  background: palette.panelSoft,
  padding: 16,
  overflow: 'hidden',
};

const historyListStyle = {
  marginTop: 12,
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
};

function historyItemStyle(active, teamColor) {
  return {
    display: 'grid',
    gridTemplateColumns: '30px 1fr 44px',
    alignItems: 'center',
    gap: 9,
    padding: '8px 9px',
    border: `1px solid ${active ? teamColor : palette.border}`,
    background: active ? 'rgba(56,189,248,0.13)' : 'rgba(15,23,42,0.5)',
  };
}

function historyNumberStyle(active, teamColor) {
  return {
    width: 26,
    height: 26,
    borderRadius: 999,
    display: 'grid',
    placeItems: 'center',
    background: active ? teamColor : 'rgba(148,163,184,0.22)',
    color: active ? '#020617' : palette.text,
    fontFamily: '"Geist Mono", monospace',
    fontWeight: 900,
    fontSize: 12,
  };
}

const historyPitchStyle = {
  fontSize: 13,
  fontWeight: 900,
  whiteSpace: 'nowrap',
  overflow: 'hidden',
  textOverflow: 'ellipsis',
};

const historyResultStyle = {
  marginTop: 2,
  color: palette.muted,
  fontSize: 10,
};

const historyVelocityStyle = {
  textAlign: 'right',
  fontFamily: '"Bebas Neue", sans-serif',
  fontSize: 22,
  fontVariantNumeric: 'tabular-nums',
};

function FooterRibbon({ sourceLabel, watchPoint }) {
  return (
    <footer style={footerStyle}>
      <span>{sourceLabel || 'ORIGINAL INFOGRAPHIC · PROVENANCE-GATED VISUALS'}</span>
      <strong>{watchPoint || '次に見るべきポイントをここに固定'}</strong>
    </footer>
  );
}

const footerStyle = {
  position: 'absolute',
  left: 22,
  right: 22,
  bottom: 18,
  height: 32,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: 18,
  color: palette.muted,
  fontSize: 11,
  fontFamily: '"Geist Mono", monospace',
  letterSpacing: '0.04em',
  borderTop: `1px solid ${palette.border}`,
  paddingTop: 10,
};

function formatAverage(value) {
  if (typeof value !== 'number') return '—';
  return value.toFixed(3).replace(/^0/, '');
}

window.DetailedVariant = DetailedVariant;

// Variant 3: DETAILED
// レイアウト:
//  ┌──────────────────────────────────────────┐
//  │  TOP: スコアボード(バックスクリーン位置)        │
//  ├──────┬─────────────────────────┬────────┤
//  │ 投手  │  メインビジュアル              │ 投球履歴│
//  │      │  - 球種(固定幅) + B/S/O        │ (縦並び)│
//  │ 打者  │  - ストライクゾーン            │        │
//  │      │                             │        │
//  └──────┴─────────────────────────┴────────┘

function DetailedVariant({ data, currentPitchIdx, teamColor, density, showRomaji = false, statMode = 'simple' }) {
  const { score, atBat, teams } = data;
  const currentPitch = atBat.pitches[Math.max(0, currentPitchIdx)];
  const visiblePitches = atBat.pitches.slice(0, currentPitchIdx + 1);

  return (
    <div style={{
      width: '100%', height: '100%',
      background: '#0a0d18',
      backgroundImage: 'linear-gradient(180deg, #0d1120 0%, #060810 100%)',
      color: '#fff',
      fontFamily: '"Noto Sans JP", system-ui, sans-serif',
      display: 'grid',
      gridTemplateColumns: '240px 1fr 220px',
      gridTemplateRows: 'auto 1fr',
      gap: 10, padding: 12,
      position: 'relative', overflow: 'hidden',
    }}>
      {/* ============= TOP — MLB風スコアボード(上部) ============= */}
      <div style={{ gridColumn: '1 / -1' }}>
        <MLBScoreboard data={data} teamColor={teamColor} currentPitch={currentPitch} />
      </div>

      {/* ============= LEFT — 投手 ============= */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minHeight: 0, overflow: 'hidden' }}>
        <PlayerCardCompact role="pitcher" teamColor={teamColor} showRomaji={showRomaji} statMode={statMode} player={atBat.pitcher} />
      </div>

      {/* ============= MAIN ============= */}
      <div style={{
        position: 'relative', minHeight: 0, overflow: 'hidden',
        background: 'linear-gradient(180deg, #1a2438 0%, #2a3550 55%, #1a1812 100%)',
        border: '1px solid rgba(255,255,255,0.12)', borderRadius: 2,
      }}>
        <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
          <image-slot id="stadium-bg" placeholder="球場/バッターボックス画像をドロップ" shape="rect"
            style={{ width: '100%', height: '100%', '--is-bg': 'rgba(0,0,0,0.2)' }}></image-slot>
        </div>
        <div style={{
          position: 'absolute', inset: 0, zIndex: 1, pointerEvents: 'none',
          background: 'linear-gradient(180deg, rgba(0,0,0,0.4) 0%, transparent 35%, rgba(0,0,0,0.5) 100%)',
        }} />
        {/* TOP-LEFT: 球種(固定幅) + B/S/O */}
        <div style={{
          position: 'absolute', top: 14, left: 16, zIndex: 3,
          display: 'flex', alignItems: 'stretch', gap: 8,
        }}>
          <PitchHero currentPitch={currentPitch} teamColor={teamColor} />
          <CountPills score={score} />
        </div>
        {/* RIGHT: 投球履歴(上揃え) */}
        <div style={{
          position: 'absolute', right: 14, top: 76, zIndex: 3,
          width: 150, maxHeight: 'calc(100% - 220px)', display: 'flex',
        }}>
          <PitchHistoryVertical pitches={visiblePitches} currentPitchIdx={currentPitchIdx} teamColor={teamColor} />
        </div>
        {/* BOTTOM-RIGHT — 塁上表示(下揃え) */}
        <div style={{ position: 'absolute', right: 14, bottom: 14, zIndex: 3,
          width: 150,
          background: 'rgba(0,0,0,0.55)', border: '1px solid rgba(255,255,255,0.12)',
          borderRadius: 2, padding: '10px 8px',
          display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
        }}>
          <BigDiamond bases={score.bases} teamColor={teamColor} size={88} />
        </div>
        <div style={{
          position: 'absolute', inset: 0, zIndex: 2,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <StrikeZone pitches={atBat.pitches} currentPitchIdx={currentPitchIdx}
            teamColor={teamColor} variant="standard" batterSide={atBat.batter.bats}
            showHeatmap={false} showStadiumBackground={false} showBatterSilhouette={true}
            zoomMode="auto" width={520} height={520} />
        </div>
      </div>

      {/* ============= RIGHT — 打者 ============= */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minHeight: 0, overflow: 'hidden' }}>
        <PlayerCardCompact role="batter" teamColor={teamColor} showRomaji={showRomaji} statMode={statMode} player={atBat.batter} />
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// 球種表示 — 固定幅。長い球種名でもズレない
// ─────────────────────────────────────────────────────────────
function PitchHero({ currentPitch, teamColor }) {
  if (!currentPitch) return null;
  const pitchColor = PITCH_COLORS[currentPitch.type] || teamColor;
  return (
    <div style={{
      width: 240, // 固定幅
      background: 'rgba(0,0,0,0.65)',
      backdropFilter: 'blur(8px)',
      border: '1px solid rgba(255,255,255,0.12)',
      borderLeft: `3px solid ${pitchColor}`,
      borderRadius: 2,
      padding: '8px 14px',
      display: 'grid',
      gridTemplateColumns: '1fr 88px',
      alignItems: 'center', gap: 10,
      boxSizing: 'border-box',
    }}>
      {/* 左: ピッチ番号 + 球種 */}
      <div style={{ minWidth: 0, overflow: 'hidden' }}>
        <div style={{ fontSize: 9, letterSpacing: '0.25em', color: 'rgba(255,255,255,0.55)' }}>
          PITCH {String(currentPitch.num).padStart(2, '0')}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 2, whiteSpace: 'nowrap' }}>
          <span style={{
            display: 'inline-block', width: 8, height: 8, borderRadius: 4,
            background: pitchColor, boxShadow: `0 0 8px ${pitchColor}80`, flexShrink: 0,
          }} />
          <span style={{
            fontSize: 14, fontWeight: 700,
            overflow: 'hidden', textOverflow: 'ellipsis',
          }}>{currentPitch.typeJa}</span>
          <span style={{ fontSize: 9, color: 'rgba(255,255,255,0.45)', fontFamily: 'Geist Mono, monospace', marginLeft: 'auto' }}>
            {currentPitch.type}
          </span>
        </div>
      </div>
      {/* 右: 球速(固定幅で揃える) */}
      <div style={{
        display: 'flex', alignItems: 'baseline', gap: 4,
        justifyContent: 'flex-end',
      }}>
        <span style={{
          fontSize: 36, fontFamily: '"Bebas Neue", sans-serif',
          lineHeight: 0.85, fontVariantNumeric: 'tabular-nums',
        }}>
          {currentPitch.kmh}
        </span>
        <span style={{ fontSize: 10, color: 'rgba(255,255,255,0.5)', fontFamily: 'Geist Mono, monospace' }}>km/h</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// B/S/O カウント — 球種表示の右に並べる
// ─────────────────────────────────────────────────────────────
function CountPills({ score }) {
  return (
    <div style={{
      background: 'rgba(0,0,0,0.65)',
      backdropFilter: 'blur(8px)',
      border: '1px solid rgba(255,255,255,0.12)',
      borderRadius: 2,
      padding: '8px 12px',
      display: 'flex', flexDirection: 'column', gap: 5,
      justifyContent: 'center',
    }}>
      <CountRow label="B" value={score.balls} max={4} color="#3B82F6" />
      <CountRow label="S" value={score.strikes} max={3} color="#FACC15" />
      <CountRow label="O" value={score.outs} max={3} color="#EF4444" />
    </div>
  );
}

function CountRow({ label, value, max, color }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
      <span style={{
        fontSize: 11, color: '#fff', fontWeight: 800,
        minWidth: 10, fontFamily: '"Bebas Neue", sans-serif',
      }}>{label}</span>
      <div style={{ display: 'flex', gap: 3 }}>
        {Array.from({ length: max }).map((_, i) => (
          <div key={i} style={{
            width: 10, height: 10, borderRadius: 5,
            background: i < value ? color : 'transparent',
            border: `1.3px solid ${i < value ? color : 'rgba(255,255,255,0.3)'}`,
            transition: 'all 0.2s',
            boxShadow: i < value ? `0 0 6px ${color}80` : 'none',
          }} />
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// MLB風スコアボード — 打者情報 + 投手 + チームスコア + ベース + カウント
// ─────────────────────────────────────────────────────────────
function MLBScoreboard({ data, teamColor, currentPitch }) {
  const { score, atBat, teams } = data;
  const battingTeam = score.half === 'bottom' ? teams.home : teams.away;
  const batter = atBat.batter;
  const pitcher = atBat.pitcher;
  const battingOrder = atBat.battingOrder || score.battingOrder || 3;
  const battingTeamScore = score.half === 'bottom' ? score.home : score.away;
  const fieldingTeamScore = score.half === 'bottom' ? score.away : score.home;
  const fieldingTeam = score.half === 'bottom' ? teams.away : teams.home;

  const runners = [];
  if (score.bases.first) runners.push('1');
  if (score.bases.second) runners.push('2');
  if (score.bases.third) runners.push('3');

  return (
    <div style={{
      background: '#0d1018',
      border: '1px solid rgba(255,255,255,0.18)',
      borderRadius: 2, overflow: 'hidden',
      fontFamily: '"Bebas Neue", "Noto Sans JP", sans-serif',
      boxShadow: '0 4px 14px rgba(0,0,0,0.5)',
    }}>
      {/* ROW 3: チームスコア + イニング */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr auto',
        alignItems: 'stretch',
      }}>
        {/* スコア(2行: away/home) */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <TeamScoreRow team={teams.away} runs={score.away}
            isBatting={score.half === 'top'} teamColor={teamColor} runners={[]} />
          <TeamScoreRow team={teams.home} runs={score.home}
            isBatting={score.half === 'bottom'} teamColor={teamColor} runners={[]} />
        </div>
        {/* イニングのみ */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          padding: '0 18px',
          borderLeft: '1px solid rgba(255,255,255,0.12)',
          background: 'rgba(0,0,0,0.4)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ fontSize: 28, color: '#fff', lineHeight: 0.9, fontVariantNumeric: 'tabular-nums' }}>
              {score.inning}
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <div style={{
                width: 0, height: 0,
                borderLeft: '4px solid transparent', borderRight: '4px solid transparent',
                borderBottom: `5px solid ${score.half === 'top' ? teamColor : 'rgba(255,255,255,0.2)'}`,
              }} />
              <div style={{
                width: 0, height: 0,
                borderLeft: '4px solid transparent', borderRight: '4px solid transparent',
                borderTop: `5px solid ${score.half === 'bottom' ? teamColor : 'rgba(255,255,255,0.2)'}`,
              }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatChip({ label, value, small }) {
  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
      <span style={{
        fontSize: small ? 14 : 17, color: '#fff', fontWeight: 700,
        fontVariantNumeric: 'tabular-nums', lineHeight: 1,
      }}>{value}</span>
      <span style={{
        fontSize: 9, color: 'rgba(255,255,255,0.55)',
        letterSpacing: '0.1em', fontFamily: 'Geist Mono, monospace',
      }}>{label}</span>
    </div>
  );
}

function TeamScoreRow({ team, runs, isBatting, teamColor, runners }) {
  return (
    <div style={{
      display: 'grid', gridTemplateColumns: '52px 28px 1fr auto',
      height: 32, alignItems: 'center',
      background: isBatting ? `linear-gradient(90deg, ${teamColor}25 0%, transparent 100%)` : 'transparent',
      borderBottom: '1px solid rgba(255,255,255,0.06)',
    }}>
      <div style={{
        height: '100%',
        background: team.primary, color: team.secondary,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: 13, fontWeight: 800, letterSpacing: '0.05em',
      }}>{team.code}</div>
      <div style={{
        textAlign: 'center', fontSize: 18, color: '#fff',
        fontVariantNumeric: 'tabular-nums', fontWeight: 700,
      }}>{runs}</div>
      <div />
      <div style={{ paddingRight: 12 }}>
        {isBatting && (
          <span style={{ fontSize: 10, color: teamColor, fontWeight: 700, letterSpacing: '0.15em' }}>● 攻撃</span>
        )}
      </div>
    </div>
  );
}

// 旧スコアボード(未使用、後方互換)
function BroadcastScoreboard({ data, teamColor }) {
  const { score, teams } = data;
  const innings = Array.from({ length: 9 }, (_, i) => i + 1);

  const Row = ({ team, lineScore, totals, isBatting }) => (
    <tr>
      <td style={{
        padding: '0 10px', height: 38,
        background: team.primary, color: team.secondary,
        fontWeight: 800, fontSize: 13, fontFamily: '"Bebas Neue", sans-serif',
        letterSpacing: '0.05em', width: 56, minWidth: 56, textAlign: 'center',
        borderRight: '2px solid rgba(0,0,0,0.3)',
      }}>{team.code}</td>
      {innings.map((inning, i) => {
        const v = lineScore[i];
        const isCurrent = inning === score.inning && (
          (isBatting && score.half === 'bottom') || (!isBatting && score.half === 'top')
        );
        return (
          <td key={i} style={{
            width: 32, textAlign: 'center',
            fontFamily: '"Bebas Neue", sans-serif',
            fontSize: 16, fontWeight: 700,
            color: isCurrent ? teamColor : '#fff',
            background: isCurrent ? 'rgba(255,255,255,0.08)' : 'transparent',
            borderRight: '1px solid rgba(255,255,255,0.08)',
            fontVariantNumeric: 'tabular-nums',
          }}>{v ?? '·'}</td>
        );
      })}
      <td style={{
        width: 38, textAlign: 'center',
        background: 'rgba(255,255,255,0.1)',
        fontFamily: '"Bebas Neue", sans-serif',
        fontSize: 19, fontWeight: 800, color: '#fff',
        fontVariantNumeric: 'tabular-nums',
        borderLeft: '2px solid rgba(255,255,255,0.15)',
      }}>{totals.r}</td>
      <td style={{
        width: 32, textAlign: 'center',
        fontFamily: '"Bebas Neue", sans-serif',
        fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.85)',
        fontVariantNumeric: 'tabular-nums',
        borderLeft: '1px solid rgba(255,255,255,0.08)',
      }}>{totals.h}</td>
      <td style={{
        width: 32, textAlign: 'center',
        fontFamily: '"Bebas Neue", sans-serif',
        fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.65)',
        fontVariantNumeric: 'tabular-nums',
        borderLeft: '1px solid rgba(255,255,255,0.08)',
      }}>{totals.e}</td>
    </tr>
  );

  return (
    <div style={{
      background: 'rgba(0,0,0,0.7)',
      border: '1px solid rgba(255,255,255,0.15)',
      borderRadius: 2, overflow: 'hidden',
      display: 'grid', gridTemplateColumns: '1fr auto',
    }}>
      <table style={{ borderCollapse: 'collapse', tableLayout: 'fixed' }}>
        <thead>
          <tr style={{ background: 'rgba(255,255,255,0.04)' }}>
            <th style={{ ...headStyle(), width: 56 }}></th>
            {innings.map((i) => (
              <th key={i} style={{
                ...headStyle(), width: 32,
                color: i === score.inning ? teamColor : 'rgba(255,255,255,0.6)',
              }}>{i}</th>
            ))}
            <th style={{ ...headStyle(), width: 38, background: 'rgba(255,255,255,0.06)' }}>R</th>
            <th style={{ ...headStyle(), width: 32 }}>H</th>
            <th style={{ ...headStyle(), width: 32 }}>E</th>
          </tr>
        </thead>
        <tbody>
          <Row team={teams.away} lineScore={score.lineScore.away} totals={score.lineScore.awayTotal} isBatting={false} />
          <Row team={teams.home} lineScore={score.lineScore.home} totals={score.lineScore.homeTotal} isBatting={true} />
        </tbody>
      </table>
      {/* 右端: イニング + ベース図 */}
      <div style={{
        display: 'flex', alignItems: 'center',
        borderLeft: '1px solid rgba(255,255,255,0.15)',
        padding: '0 14px', gap: 14,
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ fontSize: 28, fontFamily: '"Bebas Neue", sans-serif', lineHeight: 0.85, fontVariantNumeric: 'tabular-nums' }}>
              {score.inning}
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <div style={{
                width: 0, height: 0,
                borderLeft: '4px solid transparent', borderRight: '4px solid transparent',
                borderBottom: `6px solid ${score.half === 'top' ? teamColor : 'rgba(255,255,255,0.18)'}`,
              }} />
              <div style={{
                width: 0, height: 0,
                borderLeft: '4px solid transparent', borderRight: '4px solid transparent',
                borderTop: `6px solid ${score.half === 'bottom' ? teamColor : 'rgba(255,255,255,0.18)'}`,
              }} />
            </div>
          </div>
          <div style={{ fontSize: 8, letterSpacing: '0.2em', color: teamColor, marginTop: 2, fontWeight: 700 }}>
            {score.half === 'top' ? '表 TOP' : '裏 BOT'}
          </div>
        </div>
        <BigDiamond bases={score.bases} teamColor={teamColor} size={56} />
      </div>
    </div>
  );
}

function headStyle() {
  return {
    padding: '4px 0', height: 22,
    fontSize: 10, fontWeight: 700, letterSpacing: '0.1em',
    color: 'rgba(255,255,255,0.6)',
    fontFamily: 'Geist Mono, monospace',
    borderBottom: '1px solid rgba(255,255,255,0.12)',
  };
}

// ─────────────────────────────────────────────────────────────
// 投球履歴 — 縦並び。画面右(=左打席のバッターボックス位置)
// ─────────────────────────────────────────────────────────────
function PitchHistoryVertical({ pitches, currentPitchIdx, teamColor }) {
  return (
    <div style={{
      background: 'rgba(255,255,255,0.04)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: 2,
      padding: '12px 12px',
      display: 'flex', flexDirection: 'column', gap: 8,
      minHeight: 0, overflow: 'hidden',
    }}>
      <div style={{ fontSize: 9, letterSpacing: '0.25em', color: 'rgba(255,255,255,0.6)', flexShrink: 0 }}>
        投球履歴 PITCH LOG
      </div>
      <div style={{
        display: 'flex', flexDirection: 'column', gap: 5,
        overflow: 'auto', minHeight: 0,
      }}>
        {pitches.length === 0 && (
          <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.3)' }}>—</div>
        )}
        {pitches.map((p, i) => {
          const result = RESULT_STYLE[p.result] || {};
          const isCurrent = i === currentPitchIdx;
          const pitchColor = PITCH_COLORS[p.type] || teamColor;
          return (
            <div key={i} style={{
              display: 'grid',
              gridTemplateColumns: '22px 1fr auto',
              alignItems: 'center', gap: 8,
              padding: '6px 8px',
              background: isCurrent ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.02)',
              border: isCurrent ? `1.5px solid ${teamColor}` : '1px solid rgba(255,255,255,0.08)',
              borderRadius: 2,
              transition: 'all 0.2s',
            }}>
              {/* 番号 */}
              <div style={{
                width: 22, height: 22, borderRadius: 11,
                background: result.fill || '#888',
                color: '#fff', fontSize: 11, fontWeight: 800,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: 'Geist Mono, monospace',
              }}>{p.num}</div>
              {/* 球種 + 結果ラベル */}
              <div style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                  <span style={{
                    width: 6, height: 6, borderRadius: 3, background: pitchColor, flexShrink: 0,
                  }} />
                  <span style={{ fontSize: 11, fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {p.typeJa}
                  </span>
                </div>
                <div style={{
                  fontSize: 9, color: result.fill || 'rgba(255,255,255,0.55)',
                  fontWeight: 700, letterSpacing: '0.05em', marginTop: 1,
                }}>
                  {result.label || '—'}
                </div>
              </div>
              {/* 球速 */}
              <div style={{
                fontSize: 16, fontFamily: '"Bebas Neue", sans-serif',
                fontVariantNumeric: 'tabular-nums', lineHeight: 1,
                color: isCurrent ? '#fff' : 'rgba(255,255,255,0.85)',
              }}>{p.kmh}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// 選手カード(コンパクト)
// ─────────────────────────────────────────────────────────────
function PlayerCardCompact({ role, player, teamColor, showRomaji, statMode }) {
  const isPitcher = role === 'pitcher';
  const handLabel = isPitcher
    ? `${player.throws === 'R' ? '右' : '左'}投`
    : `${player.bats === 'L' ? '左' : '右'}打`;

  const stats = isPitcher
    ? [
        { label: 'ERA', value: player.season.era.toFixed(2) },
        { label: 'W-L', value: `${player.season.w}-${player.season.l}` },
        { label: 'K', value: player.season.k },
      ]
    : [
        { label: 'AVG', value: `.${String(Math.round(player.season.avg * 1000)).padStart(3, '0')}` },
        { label: 'HR', value: player.season.hr },
        { label: 'OPS', value: player.season.ops.toFixed(3) },
      ];

  const today = isPitcher
    ? `${player.today.ip}回 ${player.today.k}K ${player.today.pc}球`
    : `${player.today.ab}-${player.today.h} ${player.today.k}三振`;

  return (
    <div style={{
      background: 'rgba(255,255,255,0.04)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: 2,
      position: 'relative',
      padding: '10px 12px 10px 16px',
      flexShrink: 0,
    }}>
      <div style={{ position: 'absolute', top: 0, left: 0, width: 3, height: '100%', background: teamColor }} />
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
        <div style={{ fontSize: 9, letterSpacing: '0.25em', color: 'rgba(255,255,255,0.55)' }}>
          {isPitcher ? '投手 PITCHER' : '打者 BATTER'}
        </div>
        <div style={{ fontSize: 9, color: 'rgba(255,255,255,0.45)', fontFamily: 'Geist Mono, monospace', letterSpacing: '0.08em' }}>
          {handLabel}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, whiteSpace: 'nowrap', overflow: 'hidden' }}>
        <span style={{ fontSize: 22, fontFamily: '"Bebas Neue", sans-serif', color: teamColor, lineHeight: 1, flexShrink: 0 }}>
          #{player.number}
        </span>
        <span style={{ fontSize: 16, fontWeight: 700, lineHeight: 1.1, overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {player.name}
        </span>
      </div>
      {showRomaji && (
        <div style={{ fontSize: 9, color: 'rgba(255,255,255,0.4)', fontFamily: 'Geist Mono, monospace', marginTop: 3, letterSpacing: '0.05em' }}>
          {player.nameEn}
        </div>
      )}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 6,
        marginTop: 8, paddingTop: 8, borderTop: '1px solid rgba(255,255,255,0.08)',
      }}>
        {stats.map((s) => (
          <div key={s.label}>
            <div style={{ fontSize: 8, letterSpacing: '0.15em', color: 'rgba(255,255,255,0.5)' }}>{s.label}</div>
            <div style={{
              fontSize: 16, fontFamily: '"Bebas Neue", sans-serif', lineHeight: 1,
              fontVariantNumeric: 'tabular-nums', marginTop: 2,
            }}>{s.value}</div>
          </div>
        ))}
      </div>
      {statMode === 'detailed' && (
        <div style={{
          marginTop: 6, paddingTop: 6, borderTop: '1px solid rgba(255,255,255,0.06)',
          fontSize: 10, color: 'rgba(255,255,255,0.7)', fontFamily: 'Geist Mono, monospace',
        }}>
          <span style={{ color: 'rgba(255,255,255,0.4)', marginRight: 6 }}>本日</span>{today}
        </div>
      )}
    </div>
  );
}

function BigDiamond({ bases, teamColor, size = 56 }) {
  const cx = size / 2, cy = size / 2;
  const r = size * 0.34;
  const baseSize = size * 0.18;
  const baseStyle = (active) => ({
    fill: active ? teamColor : 'transparent',
    stroke: active ? teamColor : 'rgba(255,255,255,0.55)',
    strokeWidth: 1.4,
  });
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <rect x={-baseSize / 2} y={-baseSize / 2} width={baseSize} height={baseSize}
            transform={`translate(${cx} ${cy - r}) rotate(45)`} {...baseStyle(bases.second)} />
      <rect x={-baseSize / 2} y={-baseSize / 2} width={baseSize} height={baseSize}
            transform={`translate(${cx - r} ${cy}) rotate(45)`} {...baseStyle(bases.third)} />
      <rect x={-baseSize / 2} y={-baseSize / 2} width={baseSize} height={baseSize}
            transform={`translate(${cx + r} ${cy}) rotate(45)`} {...baseStyle(bases.first)} />
      <path d={`M ${cx - baseSize * 0.5} ${cy + r}
                L ${cx + baseSize * 0.5} ${cy + r}
                L ${cx + baseSize * 0.6} ${cy + r + baseSize * 0.35}
                L ${cx} ${cy + r + baseSize * 0.65}
                L ${cx - baseSize * 0.6} ${cy + r + baseSize * 0.35} Z`}
            fill="rgba(255,255,255,0.15)"
            stroke="rgba(255,255,255,0.6)" strokeWidth={1.1} />
    </svg>
  );
}

window.DetailedVariant = DetailedVariant;

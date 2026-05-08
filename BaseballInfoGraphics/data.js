// 架空のサンプルデータ — 実際の配信ではAPIから流し込む想定
// MLB / NPB両方を想定した汎用構造

window.GAME_DATA = {
  // 試合メタ
  meta: {
    league: 'NPB',
    venue: '東京ドーム',
    date: '2026.05.06',
    weather: '屋内',
    attendance: '42,318',
  },

  // 両チーム（チームカラーが動的に反映される）
  teams: {
    home: {
      code: 'YOM',
      name: '読売ジャイアンツ',
      shortName: '巨人',
      primary: '#F97316',  // オレンジ
      secondary: '#1E1B4B',
      logo: 'G',
    },
    away: {
      code: 'HAN',
      name: '阪神タイガース',
      shortName: '阪神',
      primary: '#FACC15',  // イエロー
      secondary: '#000000',
      logo: 'T',
    },
  },

  // スコア
  score: {
    home: 4,
    away: 3,
    inning: 7,
    half: 'top',  // 'top' | 'bottom'
    outs: 1,
    balls: 2,
    strikes: 2,
    bases: { first: true, second: false, third: true },  // 走者
    lineScore: {
      // 1-9回 + R H E
      away: [0, 1, 0, 0, 2, 0, 0, null, null],
      home: [0, 0, 2, 0, 0, 2, null, null, null],
      awayTotal: { r: 3, h: 7, e: 0 },
      homeTotal: { r: 4, h: 6, e: 1 },
    },
  },

  // 現在の打席
  atBat: {
    pitcher: {
      id: 'p001',
      name: '山本 由伸',
      nameEn: 'Yoshinobu Yamamoto',
      number: 18,
      throws: 'R',
      season: { era: 1.82, w: 6, l: 1, k: 84, ip: '64.1' },
      today: { ip: '6.1', h: 4, r: 3, er: 3, bb: 2, k: 8, pc: 98 },
    },
    batter: {
      id: 'b001',
      name: '佐藤 輝明',
      nameEn: 'Teruaki Sato',
      number: 8,
      bats: 'L',
      season: { avg: 0.298, hr: 12, rbi: 38, ops: 0.912 },
      today: { ab: 3, h: 1, hr: 0, rbi: 1, k: 1, bb: 0 },
      vsP: { ab: 8, h: 2, hr: 1, k: 3 },  // この投手との対戦成績
      // 本日の打席履歴(最新が末尾)
      todayAtBats: [
        { inning: '1回表', vs: '山本', pitches: 4, result: 'K', resultJa: '空振三振', detail: '4球三振' },
        { inning: '3回表', vs: '山本', pitches: 6, result: '1B', resultJa: 'ヒット', detail: 'センター前' },
        { inning: '5回表', vs: '山本', pitches: 5, result: 'GO', resultJa: 'ゴロ', detail: 'セカンドゴロ' },
        { inning: '7回表', vs: '山本', pitches: 5, result: '—', resultJa: '対戦中', detail: '5球目', current: true },
      ],
    },
    onDeck: { name: '大山 悠輔', number: 3, avg: 0.276 },
    inHole: { name: '近本 光司', number: 5, avg: 0.312 },
    // 今打席の投球履歴
    pitches: [
      { num: 1, type: 'FF', typeJa: '直球', mph: 96.4, kmh: 155, x: 0.15, y: -0.4, result: 'CalledStrike', resultJa: '見逃しS' },
      { num: 2, type: 'SL', typeJa: 'スライダー', mph: 87.2, kmh: 140, x: -0.55, y: 0.3, result: 'Ball', resultJa: 'ボール' },
      { num: 3, type: 'FF', typeJa: '直球', mph: 95.8, kmh: 154, x: 0.6, y: -0.2, result: 'Foul', resultJa: 'ファウル' },
      { num: 4, type: 'SP', typeJa: 'スプリット', mph: 89.1, kmh: 143, x: -0.2, y: 0.95, result: 'Ball', resultJa: 'ボール' },
      { num: 5, type: 'CB', typeJa: 'カーブ', mph: 78.5, kmh: 126, x: 0.4, y: -0.7, result: 'SwingingStrike', resultJa: '空振りS' },
    ],
    // 次の球（リアルタイム想定）
    upcoming: { num: 6, type: 'FF', typeJa: '直球', mph: 97.3, kmh: 157, x: -0.1, y: 0.0, result: 'InPlay', resultJa: '打球' },
  },

  // ストライクゾーン定義（バッターの身長に基づく相対座標 -1.0〜1.0）
  zone: {
    // 0,0 が中央。x: 左右、y: 上下（負=高め、正=低め）
    halfWidth: 0.83,   // ホームベースの幅（フィート） / 1.42
    top: -1.0,         // ストライクゾーン上端
    bottom: 1.0,       // ストライクゾーン下端
  },

  // スコアリングプレイ（簡易版）
  scoringPlays: [
    { inning: '5回表', team: 'away', desc: '近本 光司のタイムリー二塁打', score: '0-2' },
    { inning: '3回裏', team: 'home', desc: '岡本 和真の2点本塁打', score: '2-1' },
    { inning: '6回裏', team: 'home', desc: '坂本 勇人の犠牲フライ', score: '4-2' },
    { inning: '7回表', team: 'away', desc: 'ノイジーのソロ本塁打', score: '4-3' },
  ],

  // ライバル打順（簡易）
  lineup: {
    away: [
      { order: 1, num: 5, name: '近本 光司', pos: 'CF', avg: 0.312 },
      { order: 2, num: 0, name: '中野 拓夢', pos: '2B', avg: 0.281 },
      { order: 3, num: 1, name: '森下 翔太', pos: 'RF', avg: 0.265 },
      { order: 4, num: 8, name: '佐藤 輝明', pos: '3B', avg: 0.298, current: true },
      { order: 5, num: 3, name: '大山 悠輔', pos: '1B', avg: 0.276 },
    ],
  },
};

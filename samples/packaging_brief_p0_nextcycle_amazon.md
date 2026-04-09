# Packaging Orchestrator Brief

- brief_version: 0.1
- video_id: p0_nextcycle_amazon_2026_04_10_a
- topic_label: Amazon配送ネットワークにおけるAI監視と労働負荷の構造
- target_viewer: テック企業の業務最適化が労働現場へ与える影響を具体的に知りたい視聴者
- audience_hook: 「便利な配送体験」の裏で、どこに無理が集中しているのかを数値で把握したい
- title_promise: Amazon配送現場でのAI監視が、速度・安全・メンタルに与える圧力を制度名と統計で理解できる
- thumbnail_promise: 監視強度と企業の投資規模のギャップを、具体数値で瞬時に伝える

## novelty_basis
- 抽象的な労働批判ではなく、監視指標と制度名を先に提示する
- 企業PRと現場の身体負荷を同一動画内で比較し、論点を分離せずに示す

## required_evidence
- kind: number
  value: 71.4%
  why_it_matters: 監視の強度を一目で伝える主要指標
  must_surface_in: thumbnail, opening, body
  status: confirmed

- kind: number
  value: 19億ドル
  why_it_matters: 企業の建前と実装投資のスケール差を示せる
  must_surface_in: thumbnail, body
  status: confirmed

- kind: named_entity
  value: タイム・オフ・タスク
  why_it_matters: 抽象論ではなく制度としての拘束を示せる
  must_surface_in: body
  status: confirmed

- kind: number
  value: 気温+1度でスピード違反9%増
  why_it_matters: アルゴリズム最適化が安全余白を侵食する証拠になる
  must_surface_in: body
  status: confirmed

- kind: number
  value: 66%
  why_it_matters: 精神的健康への影響規模を定量で示せる
  must_surface_in: body
  status: confirmed

- kind: anecdote
  value: 喘息の吸入器を取ろうとして脇見運転フラグが立った証言
  why_it_matters: 導入で視聴者の理解を抽象論ではなく体感に接続できる
  must_surface_in: opening
  status: confirmed

## missing_or_weak_evidence
- 中盤以降で個人エピソードの追撃が弱く、制度的冷たさの実感が薄まりやすい

## forbidden_overclaim
- 台本や出典にない違法断定をしない
- 陰謀論方向へ誇張しない
- 「Amazonが全面的に悪である」と単純化しない
- 台本にない数値や因果関係を追加しない

## thumbnail_controls
- prefer_specificity: true
- preferred_specifics: 71.4%, 19億ドル, 気温+1度で9%増
- banned_copy_patterns: 衝撃の真実, 知らないと損, ヤバすぎる, 閲覧注意
- rotation_axes:
  - layout_family: number_left_character_right
  - emotion_family: confused_vs_angry
  - color_family: dark_blue_red_alert
  - copy_family: number_fact

## script_opening_commitment
- 導入ブロックで「吸入器エピソード」または「71.4%」を先に出し、一般論から入らない

## must_payoff_by_section
- S1 までに吸入器エピソードか監視強度（71.4%）を提示
- S2 までに 71.4% とタイム・オフ・タスクを回収
- S3 までに気温+1度で9%増とインセンティブ設計を接続
- S4 までに 19億ドル規模のPR/投資文脈を提示
- S5 で視聴者への問題提起（便利さと負荷のトレードオフ）を明示

## alignment_check
- thumbnail promise を支える具体根拠（71.4%、19億ドル）が opening か body 前半に存在するか
- title promise が forbidden_overclaim を踏み越えていないか
- 台本が title を先に決めるのではなく、brief の promise を本文で回収しているか
- サムネコピーが banned_copy_patterns に該当しないか
- 導入が script_opening_commitment を守っているか

## consumer_hints
- for_c07: 71.4% とタイム・オフ・タスクは B パターン（情報埋め込み）優先。吸入器エピソードは A パターン（茶番劇）で導入。19億ドルは D パターン（黒板型）で対比し、overclaim を避ける
- for_c08: 数値先頭のコピー案を優先（71.4%、19億ドル、9%増）。抽象煽り語は除外し、困惑と怒りの感情対比で訴求
- for_e02: 説明文でも 71.4% とタイム・オフ・タスクを必ず保持し、タグは Amazon, AI監視, 労働 を軸にする
- for_h04: 中盤以降の anecdote 希薄を warning 扱い。数値根拠の回収不足を重点監視
- for_h03: 数値可視化ブロックを 3 箇所以上確保し、同一背景の長時間停滞を避ける

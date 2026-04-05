# Packaging Orchestrator Brief

- brief_version: 0.1
- video_id: amazon_ai_monitoring
- topic_label: Amazon配送現場でのAI監視と労働負荷
- target_viewer: 社会問題とテックの裏側に関心がある視聴者
- audience_hook: 便利な配送の裏で、どこまで人間が削られているのか知りたい
- title_promise: Amazon配送現場でAI監視が労働者の余裕をどう奪ったかを、具体データと制度名で理解できる
- thumbnail_promise: 監視の強度と企業の建前のギャップを、割合や金額を使って一目で掴ませる

## novelty_basis
- 抽象的な労働批判ではなく具体数値から入る
- 企業PRと現場実態のギャップを同時に見せる

## required_evidence
- kind: number
  value: 71.4%
  why_it_matters: 監視強度を即座に伝えられる
  must_surface_in: thumbnail, opening, body
  status: confirmed

- kind: number
  value: 19億ドル
  why_it_matters: 企業の建前と投資規模のギャップを示せる
  must_surface_in: thumbnail, body
  status: confirmed

- kind: named_entity
  value: タイム・オフ・タスク
  why_it_matters: 抽象論ではなく制度名として刺さる
  must_surface_in: body
  status: confirmed

- kind: number
  value: 気温+1度でスピード違反9%増
  why_it_matters: アルゴリズムが生理的限界を無視する証拠
  must_surface_in: body
  status: confirmed

- kind: number
  value: 66%
  why_it_matters: 精神的健康への悪影響の規模
  must_surface_in: body
  status: confirmed

- kind: anecdote
  value: 喘息の吸入器を取ろうとして脇見運転フラグ
  why_it_matters: 導入の掴み。個人のエピソードで共感を作る
  must_surface_in: opening
  status: confirmed

## missing_or_weak_evidence
- 個人エピソードが導入以降は薄く、中盤以降の anecdote が弱い

## forbidden_overclaim
- 台本にない違法断定をしない
- 陰謀論方向へ盛らない
- 「Amazonが全て悪い」という単純化をしない
- 台本にない数値を盛らない

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
- 導入ブロックで喘息エピソードと71.4%のどちらかを早めに出し、抽象論から入らない

## must_payoff_by_section
- S1 までに監視強度の個人エピソード (吸入器)
- S2 までに 71.4% とタイム・オフ・タスク
- S3 までに気温+1度→9%増とインセンティブの構造
- S4 までに 19億ドル PR戦略と労組の反応
- S5 で問題提起 (思考実験)

## alignment_check
- thumbnail promise を支える具体根拠 (71.4%, 19億ドル) が opening か body 前半に存在するか
- title promise が forbidden overclaim を踏み越えていないか
- 台本が title を決めるのではなく、brief の promise を本文で回収しているか
- サムネコピーが banned_copy_patterns に該当しないか
- 導入が script_opening_commitment を守っているか

## consumer_hints
- for_c07: 71.4% とタイム・オフ・タスクは B パターン (情報埋め込み) で可視化。吸入器エピソードは A パターン (茶番劇)。19億ドル PR は D パターン (黒板型) でデータ対比。forbidden_overclaim に反する強い演出を避ける
- for_c08: 数値先頭の copy family を優先 (71.4%, 19億ドル, 9%増)。抽象煽りを避け、banned_copy_patterns を除外。表情は困惑 vs 怒りの組み合わせ
- for_e02: 説明文でも 71.4% と制度名 (タイム・オフ・タスク) を落とさない。タグに Amazon, AI監視, 労働
- for_h04: anecdote が導入以降弱い点を warning 扱い。数値根拠は充足
- for_h03: 数値表示ブロック (B パターン) が 3 箇所以上あるか。同一背景 60 秒超を避ける

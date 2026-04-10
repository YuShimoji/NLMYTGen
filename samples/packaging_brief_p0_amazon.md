# Packaging Orchestrator Brief

- brief_version: 0.1
- video_id: p0_phase1_amazon
- topic_label: Amazon の物流・配送におけるアルゴリズム監視とパノプティコン構造（倉庫〜路上〜PR対立まで）
- target_viewer: プラットフォーム労働・監視テック・社会問題の裏側に関心がある視聴者
- audience_hook: 「便利な配送」の裏で、スキャナー・カメラ・インセンティブが肉体と精神に何をしているか知りたい
- title_promise: Amazon を軸に、倉庫の実数値監視、路上配送の客観データ、2025〜2026 の PR と労組の対立までを一本でつなげて理解できる
- thumbnail_promise: 監視の強さ（割合）と、企業の投資・建前とのギャップを数値で一目で示す

## novelty_basis
- パノプティコン概念で倉庫ネットワークを読み替え、単なる「きつい現場」話にしない
- 主観アンケートではなくドローン＋GPS の運動学データで路上リスクを説明する
- 消費のワンタップが街のリスク配分に変換されるメタ構造まで持ち上げる

## required_evidence
- kind: anecdote
  value: 喘息の吸入器を取ろうとして脇見運転フラグ（車内 AI カメラ）
  why_it_matters: 人間の切実な事情がアルゴリズムではノイズになる具体例
  must_surface_in: opening, body
  status: confirmed

- kind: number
  value: 71.4%
  why_it_matters: 倉庫労働者がスキャナーで秒単位追跡されていると答えた割合
  must_surface_in: thumbnail, opening, body
  status: confirmed

- kind: named_entity
  value: タイム・オフ・タスク（タスク離脱タイマー）
  why_it_matters: 監視のメカニズムを制度名レベルで固定できる
  must_surface_in: opening, body
  status: confirmed

- kind: number
  value: 66%（精神的健康悪影響）／54%（身体的影響）
  why_it_matters: メンタル負荷が身体より大きいという規模感
  must_surface_in: body
  status: confirmed

- kind: number
  value: インセンティブ時は上位85%の速度が平均+約2km/h、60km/h超での速度違反確率が1.61倍
  why_it_matters: 「ボーナス」の裏の客観的リスク上昇
  must_surface_in: body
  status: confirmed

- kind: number
  value: 気温+1℃ごとに速度違反確率+9%
  why_it_matters: 気候×アルゴリズムの合わせ技を数値で示す
  must_surface_in: thumbnail, body
  status: confirmed

- kind: number
  value: 19億ドル（DSP 等への投資の規模として言及）
  why_it_matters: 企業の安全・対遇アピールと労組の「PR スタント」批判の対比軸
  must_surface_in: thumbnail, body
  status: confirmed

- kind: named_entity
  value: チームスターズ／ALU 等の 2025年10月声明（10億ドル PR スタントとの批判）
  why_it_matters: 対立の最新イベントを固有名で固定
  must_surface_in: body
  status: confirmed

## missing_or_weak_evidence
- 台本冒頭の誤変換・聞き取りノイズが多く、セリフの厳密引用は人間確認が望ましい

## forbidden_overclaim
- 台本にない違法断定をしない
- 陰謀論・単純な「Amazon 悪」一辺倒にしない
- 台本にない数値・固有名を盛らない
- 研究・報告書の帰属をねじ曲げない

## thumbnail_controls
- prefer_specificity: true
- preferred_specifics: 71.4%, 19億ドル, 9%（気温1度あたり）, 1.61倍
- banned_copy_patterns: 衝撃の真実, 知らないと損, ヤバすぎる, 閲覧注意
- rotation_axes:
  - layout_family: number_left_character_right
  - emotion_family: dread_vs_outrage
  - color_family: cold_blue_warning_red
  - copy_family: number_fact

## script_opening_commitment
- 導入で吸入器エピソードまたは 71.4% のいずれかを早めに出し、抽象論だけで始めない

## must_payoff_by_section
- 冒頭〜倉庫パートで 71.4% とタイム・オフ・タスク、人間無視のメカニズム
- 中盤で路上パート（ドローン研究・インセンティブ・気温相関）
- 後半で 19億ドル PR と労組声明の対比
- 締めで思考実験（最適化の先の人間排除か）

## alignment_check
- thumbnail promise を支える具体根拠（71.4%, 9%増, 19億ドル 等）が opening か body 前半に存在するか
- title promise が forbidden overclaim を踏み越えていないか
- 台本がタイトルに引っ張られすぎず、brief の promise を本文で回収しているか
- サムネコピーが banned_copy_patterns に該当しないか
- 導入が script_opening_commitment を守っているか

## consumer_hints
- for_c07: 吸入器シーンは人間ドラマ（A）、71.4%／タイムオフタスクは情報パネル（B）、PR対比は黒板・対比（D）を想定。required_evidence の must_surface_in を見落とさない
- for_c08: 数値先頭の copy family を優先。抽象煽りと banned pattern を避ける。Panopticon はサブコピーに回すか抑える（読みやすさ優先）
- for_e02: Amazon, 監視, 労働, 配送, 気候 をタグ候補に。具体数値は説明にも残す
- for_h04: 逸話は導入強いが中盤以降は数値線が主という不均衡に注意
- for_h03: 同一トーンの数値パネルが続く箇所は視覚密度の散らしを検討

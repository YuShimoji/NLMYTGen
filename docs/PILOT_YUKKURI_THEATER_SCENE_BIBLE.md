# Pilot Yukkuri Theater Scene Bible

この文書は `pilot_yukkuri_theater_v1` の背景茶番劇を、IR / YMM4 placement より前に固定するための正本である。目的は motion label の列ではなく、背景側の無言劇として「誰が、どこで、何を巡って、どの比率で変化するか」を先に決めること。

## Non-Negotiables

- 背景茶番劇は語り手への合いの手ではない。語り手・ゆっくり立ち絵と並行する別レイヤーの無言劇である。
- `pilot_yukkuri_theater_v1_patched.ymmp` は transport/readback proof のみ。creative acceptance / production acceptance の証跡ではない。
- IR / YMM4 placement へ進める前に、`scene bible / time budget / cast continuity / screen placement / props / 休ませる区間 / proof path` を揃える。
- `delivery_v1_templates.ymmp` は不動産業者そのものとして使わない。使えるのは、仮の案内人・移動役としての transport proof、または再スキン前提の template candidate まで。
- 既存 template を流用するときは、誰を何の比喩として演じるかを scene bible 内で決める。決められない場合は missing template として扱う。

## Cast Continuity

| role | fixed identity | story function | screen continuity | template stance |
|---|---|---|---|---|
| 消費者 | スマホで探す本人。後半では選ぶ主体になる | 情報民主化の受け手であり、最後にプロを選ぶ判断者 | 原則は画面左〜中央。混乱時はカード群に埋もれ、透明化後は中央へ出る | 既存配達員 template では代替しない。新規 body / face 候補 |
| ゲートキーパー業者 | REINS/VIPクラブの扉・PC・商談中札を管理する対立役 | 情報を抱え込み、消費者・売主の視界を狭める | 画面右奥または扉の内側。囲い込みでは中央に割り込む | `delivery_v1_templates.ymmp` の literal reuse 禁止。再スキン candidate |
| キュレーター/リスク管理プロ | 後半で残る専門家 | 情報を独占せず、選択肢を編集し、見えないリスクを止める | 画面中央〜右。ゲートキーパーと入れ替わり、消費者の横へ移動する | 新規 template candidate。案内人 proxy は transport proof 限定 |
| データ/AI/プラットフォーム | カード群、QR、ステータス盤、AI推薦の非人物要素 | 可視化された情報量と自動提案を表す | 背景全面または上部 overlay 的に扱う | YMM4 native item / overlay candidate |
| 配達員 | 配達短編だけの主役 | 誤配に気づき訂正する一本の小話を担う | 玄関左から入り、ドア/受取人/部屋番号を確認し、荷物を持って退場 | 既存 `delivery_v1_templates.ymmp` の主用途 |

## Real Estate DX Scene Bible

### 1. 自力検索

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 1-12
- `time budget %`: 10
- `background story beat`: 消費者がベッドでスマホをスワイプし、物件カードが増殖する。鍵の比喩は「スマホを持つ手」として見せ、業者はまだ遠くに小さく置く。
- `cast continuity`: 消費者を初登場させる。ゲートキーパー業者は影または扉の奥に留め、対立をまだ前面化しない。
- `screen placement`: 消費者は左下〜中央左、スマホ画面と物件カードは中央、遠景右に閉じた扉。
- `props`: スマホ、物件カード群、薄い鍵アイコン、ベッド/枕、閉じた扉。
- `休ませる区間`: lines 9-12 は情報量を増やしすぎず、カード群を静止/低速スクロールにして語りの論点提示を邪魔しない。
- `proof path`: scene bible → asset gap → consumer/search UI template → compact review。既存 patched `.ymmp` はここでは acceptance proof にしない。

### 2. REINS-VIPクラブ

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 13-24
- `time budget %`: 12
- `background story beat`: ゲートキーパー業者がVIPクラブの内側でPC/業務DBを見る。消費者はスマホを持っているが、扉の外で「生データ」には届かない。
- `cast continuity`: ゲートキーパー業者を明確に登場させる。消費者は左側に残し、情報アクセスの非対称性を人物間距離で見せる。
- `screen placement`: 右奥にVIPクラブ扉とPC机、中央に半透明の境界線、左手前に消費者。
- `props`: REINS風DB画面、会員証/鍵、VIPクラブ扉、一般向けポータルカード、プリントアウト紙。
- `休ませる区間`: lines 16-21 の問い返しは人物を動かさず、扉内/扉外の構図を保持して理解を優先する。
- `proof path`: VIP扉/PC/境界 props の有無を asset matrix で確認してから IR 化。配達員 template は不動産業者として使わない。

### 3. 保護理由

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 25-36
- `time budget %`: 12
- `background story beat`: 業者が「プライバシー」「リスク調査」「市場秩序」の3枚の盾を並べる。盾は一部正当だが、背後に利益の影が見え始める。
- `cast continuity`: ゲートキーパー業者は対立役のままだが、単純な悪役にはしない。消費者は盾の前で一度立ち止まる。
- `screen placement`: 画面中央に3枚の盾カード、右奥に業者、左に消費者。影は盾の背後へ薄く出す。
- `props`: プライバシー封筒、境界線/違反警告カード、冷やかし禁止札、影付き手数料袋。
- `休ませる区間`: lines 27-33 は盾カードを順に出すだけにし、line 35 の「闇」は飛び上がりではなく背後の影を濃くする。
- `proof path`: 盾/影 props が無い場合は overlay candidate。motion label で驚きを代替しない。

### 4. 囲い込み

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 37-48
- `time budget %`: 14
- `background story beat`: ゲートキーパー業者が売主カードと買主カードの間へ割り込み、他社ルートに「商談中」札を置く。利益相反を人物の遮断で見せる。
- `cast continuity`: ゲートキーパー業者の対立性が最大化する。消費者は買主側、売主カードは右奥、業者が中央を塞ぐ。
- `screen placement`: 中央に業者、左に買主/消費者、右に売主カード、奥に閉じた他社ルート。
- `props`: 売主カード、買主カード、両手仲介の二方向矢印、商談中札、閉じたゲート、手数料袋。
- `休ませる区間`: lines 44-48 は遮断構図を保持し、動きは札の固定だけにする。怒り/驚きのリアクションを足さない。
- `proof path`: 商談中札・二方向矢印・遮断ゲートが必須。既存 motion cue の `deny` 的揺れだけでは scene proof 不足。

### 5. QR透明化

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 49-60
- `time budget %`: 10
- `background story beat`: 売主/消費者がQRを読み、ステータス盤が点灯する。閉じていた扉が半分開き、嘘が可視化される。
- `cast continuity`: ゲートキーパー業者は中央から後退する。消費者はスマホを持ったまま一歩前へ出る。
- `screen placement`: 中央にQR/ステータス盤、左に消費者、右奥に開き始めるVIP扉、業者は扉脇へ退く。
- `props`: QRコード、スマホ、REINS登録証明書、公開/商談中ステータス盤、開く扉。
- `休ませる区間`: lines 55-60 は透明化の盤面を静止で見せ、次の価値転換へ画面を整理する。
- `proof path`: QR/ステータス盤 props がない場合は新規 overlay。既存 template は「歩いて近づく」transport proof に限る。

### 6. キュレーション

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 61-82
- `time budget %`: 17
- `background story beat`: 大量の物件カードをキュレーターがテーマ別に整理し、欠点カードも隠さず添える。消費者は「少ないが意味のある候補」を受け取る。
- `cast continuity`: キュレーター/リスク管理プロが初めて主役級に出る。ゲートキーパー業者は背景へ退き、消費者の横に専門家が並ぶ。
- `screen placement`: 左に消費者、中央に整理テーブル、右にキュレーター。不要カードは奥へ流し、選抜カードは手前へ置く。
- `props`: 物件カード束、テーマ札、欠点カード、ミシュラン/学芸員風の展示台、タイパ/納得感メーター。
- `休ませる区間`: lines 70-77 は欠点カードを一枚見せた後、カード整理の手を止めて「誠実さ」を読ませる。
- `proof path`: キュレーター body / card sorting template / 欠点カード overlay を asset gap 化。配達員 template の再スキンは候補止まり。

### 7. AI後の人間価値

- `script line range`: `samples/不動産DX_魔法の鍵とキュレーション.txt` lines 83-152
- `time budget %`: 25
- `background story beat`: SNSで映える候補とAI推薦が並ぶが、最後にキュレーター/リスク管理プロが「買ってはいけない理由」カードで止める。最後の問いかけまで、価値は情報アクセスではなく、リスクと感情の調整に移る。
- `cast continuity`: 消費者は選ぶ主体として中央に立つ。ゲートキーパー業者は退場または影のみ。キュレーター/リスク管理プロが消費者の横で最終判断を支える。
- `screen placement`: 前半はSNS/推しスペース/AI候補を背景全面に流し、後半は中央の消費者と右の専門家へ収束させる。
- `props`: SNSカード、推しスペース部屋カード、免許/倫理チェック札、空き家/ハザード/相続カード、AI推薦画面、買ってはいけない理由カード。
- `休ませる区間`: lines 83-122 は小道具を多く出しすぎず、SNS信頼と専門性リスクを2枚の対比カードで保持する。lines 130-152 は最終カードの提示と締めの問いかけを主動作に絞る。
- `proof path`: SNS/AI/リスク cards は overlay candidate。最終停止の演技は motion label ではなく、専門家が消費者の前にカードを差し出す blocking で検証する。

## Delivery Mini Scene Bible

配達台本は不動産DXとは別枠の短編である。ここで既存 template が使える理由は、motion label の順番があるからではなく、配達員・ドア/受取人・荷物・部屋番号による一本の連続行動が読めるからである。

### Delivery Setup

- `script line range`: 配達台本の冒頭〜配達員が玄関へ入る範囲
- `time budget %`: 25
- `background story beat`: 配達員が荷物を持ってドア前へ到着し、部屋番号を見ながら呼びかける。
- `cast continuity`: 配達員を主役に固定。受取人/ドアは相手役として右側に置く。
- `screen placement`: 左から配達員、右にドア/受取人、中央に荷物。
- `props`: 荷物、伝票、部屋番号札、ドア。
- `休ませる区間`: 呼びかけ中は歩き続けず、ドア前で止める。
- `proof path`: `delivery_enter_from_left_v1` は transport proof として有効。荷物/部屋番号 props の有無を別確認する。

### Delivery Complication

- `script line range`: 受取人が違和感を示し、伝票/部屋番号確認へ移る範囲
- `time budget %`: 25
- `background story beat`: 受取人が受け取りを保留し、配達員が伝票と部屋番号を照合する。
- `cast continuity`: 配達員は同一人物のまま、ドア/受取人との距離を詰めすぎない。
- `screen placement`: 中央に伝票、右に部屋番号、左に配達員。
- `props`: 伝票、部屋番号札、荷物ラベル。
- `休ませる区間`: 照合中は大きな驚きではなく、視線/荷物向きの確認を主にする。
- `proof path`: `delivery_nod_v1` は同意ではなく確認動作として使う。

### Delivery Reaction

- `script line range`: 誤配に気づく範囲
- `time budget %`: 25
- `background story beat`: 配達員が伝票と部屋番号の不一致を発見し、一拍だけ驚く。
- `cast continuity`: 驚きは配達員の行動結果であり、語り手の発話への反応ではない。
- `screen placement`: 配達員を中央へ少し寄せ、伝票/部屋番号の対比を画面内に残す。
- `props`: 間違った部屋番号、正しい部屋番号メモ、荷物。
- `休ませる区間`: 驚きはワンショットで終え、すぐ訂正行動へ戻す。
- `proof path`: `delivery_surprise_oneshot_v1` は原因が画面上の誤配として見える場合だけ使う。

### Delivery Resolution

- `script line range`: 訂正して退出する範囲
- `time budget %`: 25
- `background story beat`: 配達員が荷物の向き/行き先を直し、正しい部屋へ向かって退場する。
- `cast continuity`: 配達員は責任を持って処理を戻す。受取人/ドアは場面収束の相手役。
- `screen placement`: 右にドア/受取人、中央に荷物、左へ退場導線。
- `props`: 荷物、訂正済み伝票、部屋番号札。
- `休ませる区間`: 退場直前は荷物を持ち直す静止を入れ、解決を読ませる。
- `proof path`: `delivery_deny_oneshot_v1` は誤配否定/制止、`delivery_exit_left_v1` は退出として使う。motion label の並びだけで acceptance としない。

## Asset / Proof Matrix

| item | current availability | owner | allowed use | missing / next |
|---|---|---|---|---|
| `samples/templates/skit_group/delivery_v1_templates.ymmp` | repo tracked | assistant | 配達短編の main proof。不動産DXでは仮案内人/移動 proxy または再スキン candidate | 不動産業者としての literal reuse は不可 |
| 消費者 body / face | missing | user-owned authoring after assistant gap report | 不動産DXの主役 | assistant が必要 pose / size / placement を gap report 化 |
| ゲートキーパー業者 body / face | missing | user-owned authoring after assistant gap report | 対立役 | PC/扉/商談中札と一体で template candidate 化 |
| キュレーター/リスク管理プロ body / face | missing | user-owned authoring after assistant gap report | 後半の専門家 | 欠点カード/停止カードを持つ pose が必要 |
| PC / REINS風DB / VIP扉 | missing | assistant-owned design, user-owned asset if native art required | REINS-VIPクラブ、囲い込み | overlay / YMM4 item / template のどれで出すかを後続分類 |
| 物件カード / 売主買主カード / QR / SNS / AI / リスクカード | missing | assistant-owned layout; user-owned final art if needed | 7ブロックの props | 低解像度 placeholder 可否を後続判断 |
| proof artifacts | partial | assistant | patched `.ymmp` は transport/readback proof only。`samples/_probe/g24/real_estate_dx_background_skit_blueprint.json` は source-backed blueprint、`samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json` は `blocked` 証跡、`samples/_probe/g24/real_estate_dx_background_skit_gap_report.json` は RE-07 小節分割と template/proxy 分類、`samples/_probe/g24/real_estate_dx_row_time_map.json` は行→CSV→VoiceItem時刻、`samples/_probe/g24/real_estate_dx_script_maturity_diagnostic.json` は脚本成熟度、`samples/_probe/g24/real_estate_dx_overlay_card_placeholder_map.json` は overlay/card placeholder map | overlay-only compact review → production timing artifact |

## Response Contract

今後この pilot の茶番劇認識を説明する返答は、最低限次を含める。

1. `認識`: 合いの手禁止、並行する独立背景小場面、transport/readback proof と creative acceptance の分離。
2. `不動産DX scene bible`: 7ブロックの script line range / time budget / cast continuity / screen placement / props / 休ませる区間 / block proof path。
3. `配達 mini bible`: setup → complication → reaction → resolution の連続行動。
4. `asset / proof matrix`: 既存 template、missing template、user-owned / assistant-owned、proof path。
5. `next action`: assistant が scene bible に基づく gap report と template/proxy 分類を作る。IR / YMM4 placement / creative acceptance にはまだ進めない。

## Anti-Overclaim Rules

- `scene bible` は IR ではない。IR / 演出指定へ進めるには [BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md](BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md) の `script_diagnostic` / `duration_model` / `quantitative_timetable` / `density_thresholds` / `density_audit` / `asset_control_matrix` を通す。
- `time budget %` は構成比であり、タイムライン時刻表ではない。総尺、`mm:ss` の開始/終了、演出秒数、意図的休止、スカスカ判定を実数値で埋めない限り、production timing へ進めない。`総尺 / mm:ss / 演出秒数が必要` という項目名列挙は未完である。
- 脚本が未成熟な場合、演出で補うのではなく `script_diagnostic` と `ideal-script delta` を作る。理想台本に必要な thesis / causality / visual anchor / evidence / payoff を明示する。
- 「このまま IR / YMM4 確認に接続できる」と書かない。正しくは、`scene bible → asset/proof gap report → template/proxy 分類 → revised skit_group IR案 → compact review → creative acceptance → production timing` の順である。
- 返答内で `script line range` を省くと、設計図ではなく概略である。7ブロック表には必ず台本行範囲を入れる。
- `proof path` は末尾の総論だけでなく、各 block が何を満たせば次へ進めるかとして書く。例: `QR/ステータス盤 props を確認してから IR 化`、`専門家 body と停止カード template を gap report 化`。
- `script line range` は任意の番号ではない。`script_source` / `line_count` / `range_basis` / readback evidence なしに `lines 1-12` を置くと、設計図ではなく arbitrary estimate である。
- `舞台監督の香り` のような雰囲気語で closeout しない。values / blockers / deltas / source-backed gaps を出す。
- `intent` と `template_name` を混同しない。IRで使う intent は `enter_from_left` / `nod` / `surprise_oneshot` / `deny_oneshot` / `exit_left`。`delivery_enter_from_left_v1` などは template 名であり、`intent` 欄に入れない。
- Python / adapter の役割を「既存GroupItemを配置するだけ」と過小化しない。素材アートは生成しないが、IR validation、registry解決、template source解析、`.ymmp` patch、readback、gap report 生成を担う。
- 不動産DXでは `delivery_v1_templates.ymmp` の直流用をしない。使う場合は `仮案内人 proxy` / `移動 proxy` / `再スキン candidate` のいずれかとして明示し、消費者・ゲートキーパー業者・キュレーターの literal cast にはしない。

## Intent / Template Boundary

| semantic action | IR intent | template_name | allowed story use |
|---|---|---|---|
| 配達員が入る | `enter_from_left` | `delivery_enter_from_left_v1` | 配達短編の到着。非配達では proxy 理由を明記 |
| 伝票や部屋番号を確認する | `nod` | `delivery_nod_v1` | 同意ではなく確認動作 |
| 誤配に気づく | `surprise_oneshot` | `delivery_surprise_oneshot_v1` | 画面内に誤配原因が見える時だけ |
| その場で制止/否定する | `deny_oneshot` | `delivery_deny_oneshot_v1` | 誤配訂正や踏みとどまり |
| 訂正後に退場する | `exit_left` | `delivery_exit_left_v1` | 解決後の退出 |

`surprise_jump` / `deny_shake` は production-like label fallback であり、返答では正規 intent と template 名を分けて説明する。`panic_shake` は通常 IR 語彙ではなく、新規 template candidate か自然文 gap に落とす。

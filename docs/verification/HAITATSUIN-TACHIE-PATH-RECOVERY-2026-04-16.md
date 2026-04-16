# haitatsuin 立ち絵パス復旧 (2026-04-16)

**ブロック**: 復旧 B (user 報告「立ち絵が表示されない」の対応)
**対象**: [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)

## 症状

user が YMM4 で haitatsuin_2026-04-12.ymmp を開くと立ち絵が表示されない。

## 原因

2026-04-13 commit `17339dd` で立ち絵パーツ参照を `D:\MovieCreationWorkspace\...` → `migrated_tachie/...` に書き換えた migration が実行されたが、`samples/characterAnimSample/migrated_tachie/` 配下の全ファイルが **`reimu_easy.png` の複製プレースホルダ**だった([TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §2.1 に既往記載)。

検証:
- `migrated_tachie/新まりさ/目/00.png` md5 = `2b73fdfae08cd760da552b4c8f9b0928`
- `reimu_easy.png` md5 = 同じ = **placeholder clone 確定**

YMM4 が「目パーツ」として reimu 全身画像を、「口パーツ」として同じ reimu 全身を… と重ねようとして立ち絵合成が破綻。

## 復旧 B 対応

`samples/Mat/` には 2026-04-14 commit `e22bf75` で**実パーツがコミット済**([samples/Mat/新まりさ/](../../samples/Mat/新まりさ/) / [samples/Mat/新れいむ/](../../samples/Mat/新れいむ/))。
haitatsuin ymmp のパス参照を `migrated_tachie\` → `..\Mat\` (相対 from characterAnimSample/) に書き換えた。

## 実施

1. **書き換えスクリプト**: [samples/characterAnimSample/_repoint_to_samples_mat.py](../../samples/characterAnimSample/_repoint_to_samples_mat.py) を新規作成
2. **backup**: 元 ymmp を [samples/_probe/b2/haitatsuin_backup_before_repoint.ymmp](../../samples/_probe/b2/haitatsuin_backup_before_repoint.ymmp) に保存
3. **実行**: `uv run python samples/characterAnimSample/_repoint_to_samples_mat.py` → "migrated_tachie refs left: 0"
4. **検証**: [samples/_probe/b2/verify_paths.py](../../samples/_probe/b2/verify_paths.py) で 15 パーツパス全て `samples/Mat/` 配下に解決、Missing 0

## 変更パス一覧 (15 件)

| 旧 | 新 |
|---|---|
| `migrated_tachie\新まりさ\他\00b.png` | `..\Mat\新まりさ\他\00b.png` |
| `migrated_tachie\新まりさ\他\00o.png` | `..\Mat\新まりさ\他\00o.png` |
| `migrated_tachie\新まりさ\体\01.png` | `..\Mat\新まりさ\体\01.png` |
| `migrated_tachie\新まりさ\口\00.png` | `..\Mat\新まりさ\口\00.png` |
| `migrated_tachie\新まりさ\目\00.png` | `..\Mat\新まりさ\目\00.png` |
| `migrated_tachie\新まりさ\眉\06c.png` | `..\Mat\新まりさ\眉\06c.png` |
| `migrated_tachie\新まりさ\髪\00o.png` | `..\Mat\新まりさ\髪\00o.png` |
| `migrated_tachie\新れいむ\他\00a.png` | `..\Mat\新れいむ\他\00a.png` |
| `migrated_tachie\新れいむ\他\00o.png` | `..\Mat\新れいむ\他\00o.png` |
| `migrated_tachie\新れいむ\体\00.png` | `..\Mat\新れいむ\体\00.png` |
| `migrated_tachie\新れいむ\口\00.png` | `..\Mat\新れいむ\口\00.png` |
| `migrated_tachie\新れいむ\後\00o.png` | `..\Mat\新れいむ\後\00o.png` |
| `migrated_tachie\新れいむ\目\00.png` | `..\Mat\新れいむ\目\00.png` |
| `migrated_tachie\新れいむ\眉\05c.png` | `..\Mat\新れいむ\眉\05c.png` |
| `migrated_tachie\新れいむ\髪\00o.png` | `..\Mat\新れいむ\髪\00o.png` |

## user 視覚確認依頼

YMM4 で haitatsuin_2026-04-12.ymmp を開き、立ち絵(ゆっくり魔理沙 + ゆっくり霊夢)が正常に表示されるかを確認してください。

- OK → B-2 次ステップ (face_map / overlay_map / IR / dry-run) に進む
- NG → パス解決の追加 failure class を特定

## 副次対応

- `migrated_tachie/` 配下は placeholder のため、将来的にディレクトリ削除 or archived 化を検討 (本ブロック非対象)
- B-3 や X-2a など他の proof で参照されていないことは確認済み (grep で migrated_tachie 参照は haitatsuin 関連のみ)

## 2026-04-17 追記 — NG 報告と原因切り分け

**user 視覚確認結果 (2026-04-17)**: NG。
user 報告原文: 「立ち絵全体が表示されていません。これは新規追加しても表示されなくなっています。参照フォルダは migrated tachie になっているようです。フォルダを参照して開いても立ち絵フォルダで何も表示されません。」

### 追加診断

1. **ymmp 本体の状態**: 正常。`samples/_probe/b2/verify_paths.py` 再実行 → 15/15 パーツが `samples/characterAnimSample/..\Mat\...` 配下で resolve OK、Missing 0。`migrated_tachie` 文字列は ymmp 内に**0件**残留 (Grep 確認)。
2. **したがって原因は ymmp の外側**: user 報告の「新規追加しても表示されない」「参照フォルダが migrated_tachie」は、YMM4 の**キャラクター登録側**(AnimationTachie プラグインの character settings / `CharacterItem` の TachieParameter) が `migrated_tachie/` を指している強い示唆。
3. **migrated_tachie/ の中身**: placeholder clone (reimu_easy.png の複製) であり、どのキャラクターも migrated_tachie 基点で開けば空または破綻した立ち絵になる。

### 責務境界

YMM4 のキャラクター登録・立ち絵プラグイン設定は YMM4 アプリ側の設定で管理される。NLMYTGen (Python) からは直接編集しない (INVARIANTS: 「YMM4 を開くのは 2 つのタイミングだけ」「`.ymmp` 直接編集や画面効果の自動注入は高リスク」)。

### User 次アクション案 (実施は user)

選択肢:
- **(案 A)** YMM4 を開き、キャラクター登録 (新れいむ / 新まりさ) の立ち絵参照フォルダを `samples/Mat/新れいむ/` / `samples/Mat/新まりさ/` の **絶対パス**に変更。ymmp を開き直して立ち絵表示を再確認。
- **(案 B)** `samples/Mat/新れいむ/` 配下を `samples/characterAnimSample/migrated_tachie/新れいむ/` に**上書きコピー**し、placeholder を実パーツで差し替える。YMM4 側設定は触らず、参照先の中身だけ入れ替える方式。
- **(案 C)** 上記のハイブリッド: コピーで即復旧 + 登録を samples/Mat/ に切替で恒久化。

assistant は案 B の実施補助 (コピースクリプト) は可能。案 A は user 作業。いずれを選ぶかは user 判断。

### 本ブロックの対応

B-2 haitatsuin の Phase A (face_map / overlay_map / IR / dry-run) は tachie 視覚確認が取れるまで**待機**。本セッションでは Phase B (視覚効果 slice Step 3 の docs 先回り) を先行する。

## 2026-04-17 2 次追記 — user 再設定後の残留症状と原因切り分け

user 報告 (2026-04-17 第 2 報): 「立ち絵のパスがおかしくなっていたので再設定して samples/Mat 以下の立ち絵に設定しました。レイヤー00の台詞オブジェクトの空白の立ち絵が優先されるのか、喋っている間は立ち絵が表示されません。」

### 追加診断 (`samples/_probe/b2/inspect_layers.py`)

| 項目 | 値 |
|------|-----|
| VoiceItem 件数 (layer 0) | 365 |
| VoiceItem `CharacterName` (多数派) | **`ゆっくり魔理沙黄縁`** (184) / **`ゆっくり霊夢赤縁`** (181) |
| TachieItem (layer 5/6) の `CharacterName` | 同じ (`ゆっくり魔理沙黄縁` / `ゆっくり霊夢赤縁`) |
| VoiceItem 内 `TachieFaceParameter` のパーツパス | **全件 `..\Mat\新れいむ\...` / `..\Mat\新まりさ\...` で実在 OK** |

### 原因特定

ymmp の中で参照されるキャラクター名は 2 つ固定: **`ゆっくり魔理沙黄縁`** と **`ゆっくり霊夢赤縁`**。パーツフォルダ名 (`新れいむ` / `新まりさ`) とは**別物**。

YMM4 の立ち絵描画モデル (推定):
- **待機中 (VoiceItem 非アクティブ)**: レイヤー 5/6 の `TachieItem` が描画される。`TachieItem` は **キャラクター登録 (AnimationTachie プラグインの設定)** からパーツフォルダを引いて描画。user が `新れいむ` / `新まりさ` という新規キャラクター**別名**で登録 + パーツフォルダを `samples/Mat/` に指定した場合、`TachieItem` の `CharacterName` = `ゆっくり霊夢赤縁` とマッチしない可能性あり。もしマッチして待機中は表示されるなら、user が **同じ名前 (`ゆっくり霊夢赤縁`)** でキャラクター登録を修正した結果。
- **発話中 (VoiceItem アクティブ)**: YMM4 は VoiceItem の `CharacterName` (= `ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁`) に対応する**キャラクター登録**の立ち絵をオーバーレイする。user の再設定がこの**既存キャラクター名**に対して行われていない場合 (別名で新規登録しただけの場合)、旧設定 (空 or `migrated_tachie/`) が読まれて空白立ち絵になる。

VoiceItem 内の `TachieFaceParameter` に埋め込まれたパーツパスは「表情選択時のスナップショット」であり、発話中の描画には**直接使われない** (スナップショット経由ではなくキャラクター登録経由で解決する) と推定される。これが「パスは実在するのに発話中は消える」現象の説明。

### 2 次対処案 (user 判断を仰ぐ)

ymmp 内の名前 (`ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁`) と、user が YMM4 で登録したキャラクターの名前のどちらを正本にするかで分岐:

#### 案 1: **YMM4 側を ymmp 内名前に合わせる** (ymmp 不変)

- user が YMM4 のキャラクター登録画面で、`ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁` **そのままの名前**で 2 キャラクターを登録 (or 既存登録を修正) し、それぞれのパーツフォルダを `samples/Mat/新れいむ/` / `samples/Mat/新まりさ/` の絶対パスに指定。
- 既に別名 (`新れいむ` / `新まりさ` 等) で登録しているなら、YMM4 側で**名前だけ** `ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁` にリネーム (不可能なら別途新規登録)。
- ymmp は触らない。**汎用性高** (この 2 名前を使う他案件でも再利用できる)。

#### 案 2: **ymmp 内名前を YMM4 側の名前に合わせる** (assistant スクリプト実行)

- user が YMM4 で新規登録したキャラクター名 (例: `新れいむ` / `新まりさ`) を assistant に教える。
- assistant がスクリプトで ymmp 内の全 VoiceItem / TachieItem の `CharacterName` を一括置換:
  - `ゆっくり霊夢赤縁` → user 指定名 (霊夢側)
  - `ゆっくり魔理沙黄縁` → user 指定名 (魔理沙側)
- backup 取得 + 差分検証後、ymmp を上書き保存。
- **作業量**: 365 件の書き換え。backup + verify パイプラインは `_repoint_to_samples_mat.py` と同方式で実装可能。

#### 案 3: 併用 (推奨しない)

既存登録と新規登録を両方残す方式。保守コスト増。

### 推奨判断

**案 1 を第一候補** — ymmp を変更せず YMM4 設定で収束、キャラクター名 (`ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁`) を今後の案件にも共通利用できる。

案 2 は user がすでに多数の別名登録ワークフローを確立している場合の次善策。

### 確認してほしいこと (user)

- 現在 YMM4 のキャラクター登録画面にあるキャラクター名と数 (`ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁` が**残っているか**、あるいは別名だけになっているか)
- 別名登録している場合の正確な名前 (案 2 を採る場合に必要)
- 「待機中 (発話していない時) は立ち絵が見えているか」 — 案 1 の成立条件 (ymmp 内名前がキャラクター登録にある) の追確認

## 2026-04-17 3 次追記 — 案 1 成立条件確認済みでも残る症状

user 回答 (2026-04-17 第 3 報):

- 待機中: **立ち絵が表示されている**
- YMM4 キャラクター登録: `ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁` の名前で**存在する** (この名前で登録した)

### 2 次追記 §案 1 の成立条件は満たされている

- ymmp 内名前 (`ゆっくり霊夢赤縁` / `ゆっくり魔理沙黄縁`) = YMM4 登録名。両者一致。
- キャラクター登録のパーツフォルダは `samples/Mat/新れいむ/` / `samples/Mat/新まりさ/` を指していると推定 (待機中描画成立から逆算)。

**それでも発話中だけ消える**。ymmp 外 (キャラ登録) の責任ではなく、**ymmp 内 VoiceItem の描画パス解決**に問題がある可能性が高い。

### 3 次仮説 — VoiceItem の埋め込みパスと解決基準の不整合

YMM4 AnimationTachie プラグインにおける立ち絵描画の 2 経路 (推定):

| 経路 | アクティブ時 | パーツパスのソース | 解決基準 |
|------|-------------|------------------|----------|
| **TachieItem (layer 5/6)** | 待機中 | キャラクター登録 | ymmp or キャラ登録ルート (待機中 OK なので matched) |
| **VoiceItem + TachieFaceParameter** | 発話中 | **VoiceItem 内に埋め込まれたスナップショット** | キャラクター登録ルート相対?ymmp 相対? |

ymmp 内 VoiceItem の `TachieFaceParameter.Eye` は `..\Mat\新れいむ\目\00.png` (ymmp 相対)。
- ymmp 相対で解決 → `samples/Mat/新れいむ/目/00.png` (実在、verify_paths.py 確認済)
- キャラ登録ルート (`samples/Mat/新れいむ/`) 相対で解決 → `samples/Mat/新れいむ/..\Mat\新れいむ\目\00.png` = `samples/Mat/Mat/新れいむ/目/00.png` (**不存在**)

後者で解釈されていると発話中は毎回解決失敗 → 空描画。この仮説は YMM4 の 2 経路の解決ルールが**異なる**という前提。

### 3 次対処案 — まず 1 件で実機検証

ymmp を一括書き換える前に、**VoiceItem 1 件を GUI で再選択**して挙動変化を観察:

1. YMM4 で haitatsuin ymmp を開く
2. 任意の VoiceItem (layer 0 の発話ブロック 1 個) を**タイムラインで選択**
3. プロパティパネルの `TachieFaceParameter` セクションを開く
4. `Eye` (目) を現在の表情のまま**同じ表情に選び直す** (GUI ドロップダウンで一度別表情 → 元に戻す)
5. プレビューでその発話区間を再生し、**立ち絵が表示されるようになるか**を確認

結果の解釈:

- **表示される**: VoiceItem の埋め込みパスが GUI 再選択で書き換わり、YMM4 の期待フォーマットに揃った → assistant スクリプトで 365 件の TachieFaceParameter を**ルート相対**に一括書き換え可能 (案 A)
- **表示されない**: パス解決ではなく別の原因 (例: VoiceItem 側の `SomeOtherTachieReference` / YMM4 バージョン不整合 / 描画レイヤーの z-order) → さらなる切り分けが必要 (案 B: TachieFaceParameter を GUI で**全選択削除** → YMM4 がキャラ登録のデフォルト表情にフォールバックするかを確認)

### 3 次対処案 A (実装準備済) — ルート相対一括書き換え (assistant)

上記 1 件検証で「表示される」なら、assistant が `samples/_probe/b2/repoint_voice_tachie_faceparameter.py` を新規作成し:

- 365 件の VoiceItem を走査
- 各 `TachieFaceParameter` の Eye / Mouth / Eyebrow / Hair / Body / Back1 / Etc1 / Etc2 等のパス文字列を `..\Mat\新れいむ\X` → `X` のような**キャラ登録ルート相対**に変換
- ymmp backup を取得
- 上書き保存して再度 YMM4 で視覚確認

### 3 次対処案 B (実装準備済) — 埋め込みパス削除 (assistant or GUI)

TachieFaceParameter を最小化 (Eye/Mouth 等を `null` に設定) し、YMM4 がキャラクター登録側の**既定表情**を使うように促す。YMM4 の挙動仕様不明なので検証必要。

### 3 次追加診断情報

`samples/_probe/b2/inspect_layers.py` の出力 (文字化けなし版) は `samples/_probe/b2/inspect_out.txt`。CharacterName と TachieFaceParameter の全パーツパスがここに記録されている。

## 2026-04-17 4 次追記 — パス完全一致検査 + 真因仮説の確定

### パス完全一致検査 (`samples/_probe/b2/compare_tachie_paths.py`)

TachieItem (layer 5/6) の `TachieItemParameter` と、対応する CharacterName の全 VoiceItem (365 件) の `TachieFaceParameter` のパーツパスをバイト単位比較:

| キャラ | 件数 | 全パーツキー (Eyebrow/Eye/Mouth/Hair/Body/Back1/Etc1/Etc2/...) |
|------|------|----|
| `ゆっくり魔理沙黄縁` | TI 1 件 vs VI 184 件 | **全パーツ・全 VoiceItem でパス文字列完全一致** |
| `ゆっくり霊夢赤縁` | TI 1 件 vs VI 181 件 | **全パーツ・全 VoiceItem でパス文字列完全一致** |

つまり **TachieItem と VoiceItem が保持するパス値に差はない**。にもかかわらず描画結果が異なる。

### 真因仮説 (確定寄り)

YMM4 の AnimationTachie プラグインにおけるパス解決:

- **TachieItem の `TachieItemParameter`**: パス文字列をそのまま ymmp 相対で読み、ImageItem と同様に描画 (= **パス参照モード**)。
- **VoiceItem の `TachieFaceParameter`**: YMM4 の**キャラクター登録側に定義された表情プリセット**を名前参照するのが本来の姿 (= **プリセット参照モデル**)。パス文字列が埋まっていても YMM4 は「プリセット名」として扱い、キャラクター登録の**プリセット辞書**に該当名が**存在しない**ため解決失敗 → 空描画。

user 報告の挙動 (「全セリフに立ち絵自体が設定されていない」「パーツを変えるとそのパーツのみ表示される」「全パーツが設定されたプリセットに変更する必要」) は、**プリセット参照モデル**で説明がつく:

- YMM4 GUI は **キャラクター登録の表情プリセット**から選ぶ UI。選ぶとプリセットがアクティブになる。
- パーツ個別に変えた場合、YMM4 はその 1 パーツだけ pathに書き換えて描画。他パーツはプリセット未設定のまま空。
- 「全パーツ設定済みのプリセット」を 1 つ選べば全パーツ揃って表示される。

### 結論

**データ書き換えでこの問題は直らない** (パス値は既に正しい)。YMM4 のキャラクター登録側で**全パーツを持つ表情プリセットを定義**し、ymmp の VoiceItem に**そのプリセット名を参照させる**必要がある。ただし現在の VoiceItem の TachieFaceParameter にはプリセット名を格納する専用フィールドが確認できない (`EyeAnimation: 'Default'`, `MouthAnimation: 'Default'` の 2 つのみで、これは瞬き/リップシンクのアニメーション方式指定)。

### 未検証の仮説 (実機で 1 件検証後に確認)

user が YMM4 GUI で 1 件の VoiceItem に「全パーツ設定済みのプリセット」を適用した後の ymmp を開くと、TachieFaceParameter に**新規フィールド** (例: `FaceName`, `PresetName`, `FacePreset` 等) が追加されているはず。もし追加されていれば、そのフィールドを 365 件一括で埋めるスクリプトで解決可能。

### 現実的な次の道

#### 道 1: **実機で 1 件 GUI 設定 → ymmp 差分観察 → 一括スクリプト化** (最も直接的)

1. user が YMM4 で 1 件の VoiceItem に「全パーツ設定済みの表情プリセット」を適用し、ymmp を保存
2. assistant が修正前/後の ymmp を diff してフィールド差異を特定
3. assistant が 365 件一括適用スクリプトを作成
4. user が保存後の ymmp で視覚確認

前提: user 側で YMM4 キャラクター登録に**全パーツを含む表情プリセット** (例: 「通常」「笑顔」等) が定義されていること。定義がなければ定義が先。

#### 道 2: **VoiceItem の TachieFaceParameter を null リセット + TachieItem に委譲** (assistant スクリプト、リバーシブル)

- VoiceItem の `TachieFaceParameter` のパーツキー (Eyebrow/Eye/Mouth/... 9 キー) を全て `null` にするスクリプトを実行
- 結果: 発話中も TachieItem (layer 5/6) の表情 (=待機中と同じ) が描画される想定
- デメリット: 発話ごとの表情変化は失われる (常時固定表情)
- 利点: 即効性・backup あり・reversible

#### 道 3: **立ち絵問題と独立して Phase A (B-2 dry-run proof) を先に進める**

立ち絵視覚表示は YMM4 GUI 仕様の話で、CLI の `apply-production --dry-run` とは**独立**。dry-run proof は face_map / overlay_map の整合と apply-production の exit code / 変更件数のみ検証する。視覚確認は P02 昇格の最終段で必要だが、1 次 dry-run は視覚なしで通せる。

**推奨**: Phase A (B-2 dry-run) を道 3 として先に進め、立ち絵視覚問題は道 1 の実機 1 件検証を並行で進める。立ち絵表示は最終視覚 proof までに直せれば十分。

## 2026-04-17 5 次追記 — 立ち絵発話中非表示は **user 先行解決済み**と判明

### 実施

user が [samples/_probe/b2/haitatsuin_1utt_preset_2026-04-17.ymmp](../../samples/_probe/b2/haitatsuin_1utt_preset_2026-04-17.ymmp) に 1 件 VoiceItem へ「全パーツ設定済みプリセット」を適用し保存。

### diff 結果 ([samples/_probe/b2/diff_voice_items.py](../../samples/_probe/b2/diff_voice_items.py))

元 ymmp と編集後 ymmp の全 diff:

| path | 種類 | 内容 |
|------|------|------|
| `.LayoutXml` | VALUE_CHANGE | YMM4 UI レイアウトの更新 (ウィンドウ配置) |
| `.FilePath` | VALUE_CHANGE | ファイル保存パスが変更 |
| `.Timelines[0].CurrentFrame` | VALUE_CHANGE | タイムラインカーソル 5772 → 0 |

**Items (VoiceItem / TachieItem) 内の diff: ゼロ**。

### 真因 (user 発言で判明)

> user (2026-04-17): 「既に修正した 4/12 をそのままコピーしたため差分はゼロです。立ち絵アイテム自体を修正後に台本再読み込みで全てのセリフに修正後の正常に表示される立ち絵が適用されています。」

つまり:

1. user は**本ブロック着手前の別セッション**で既に `haitatsuin_2026-04-12.ymmp` を修正済み
2. 修正手順は **「立ち絵アイテム (TachieItem) の設定を修正」 + 「台本再読み込み (YMM4 の CSV import)」** により全 VoiceItem の TachieFaceParameter を再構築する方式
3. 今回 assistant が観測した `haitatsuin_2026-04-12.ymmp` は**既にこの修正が適用済みの正常状態**
4. 発話中の立ち絵描画は**既に成立している**
5. assistant が「差分ゼロで道 1 成立せず」と結論づけたのは、修正前の状態と比較対象にすべきところ、**既に修正後のファイルを基準にしていたため** (そもそも道 1 の前提が不要だった)

### 立ち絵問題の解決手順 (今後の運用メモ)

user が別セッションで実施した手順 (今後同系の問題が出た時の参考):

1. YMM4 で haitatsuin ymmp を開く
2. レイヤー 5/6 の **TachieItem** の設定 (キャラクター登録参照先) を正しい状態 (`samples/Mat/新れいむ/` / `samples/Mat/新まりさ/`) に修正
3. **台本を再読み込み** (YMM4 の CSV import 機能、または該当メニュー) を実行 → 全 VoiceItem の TachieFaceParameter が新しい TachieItem 設定から再構築される
4. これで発話中も含めて全 VoiceItem に正常な立ち絵が適用される

### 結論

- **立ち絵発話中非表示問題**: **解決済み** (user 先行対応、2026-04-17)
- **B-2 CLI dry-run proof (`b2_haitatsuin_dryrun_2026-04-17`)**: PASS ([B2-haitatsuin-dryrun-proof-2026-04-17.md](B2-haitatsuin-dryrun-proof-2026-04-17.md))
- 道 2 / 道 2' / 道 E は**実施不要**。データ書き換えスクリプトは保留のまま (もしも将来の類似問題で必要になれば参照)
- 次段: 本適用 (`apply-production -o`) + YMM4 視覚確認で B-2 視覚 proof を取る、または B-2 を現状で閉じる判断は user 次第

### 先行修正済み ymmp との整合

assistant が本ブロックで観測した全診断結果 (`verify_paths.py` 15/15 OK / パス文字列 TachieItem == VoiceItem / `face_changes: 18` で dry-run 成功) は**すべて user 先行修正後の状態**に対する観測で、追加修正なしで整合する。

## 関連

- 事前調査: [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §2.1
- 原因 commit: `17339dd` (2026-04-13)
- 復旧後の commit: `HEAD` (2026-04-16)

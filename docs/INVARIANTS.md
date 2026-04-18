# Invariants
# 破ってはいけない条件・責務境界・UX不変量を保持する正本。

## Systemic Diagnosis
- この repo の失敗は「未承認実装」そのものより、status 語彙の崩れと value path 不在が静かに混入することにある。
- 「テンプレートを作る」「GUI を作る」といった命題先行は、実ワークフローの bottleneck を見失わせやすい。

## UX / Algorithmic Invariants
- **制作工程は全て GUI で完結させる。** 制作のために CLI を使う必要がある状態は設計の不備であり、GUI 側を改善する対象とする。CLI は開発・デバッグ用。
- **YMM4 を開くのは 2 つのタイミングだけ**: (1) テンプレ用素材の登録時、(2) 全素材を集め終わって配置・書き出すとき。増分の中間確認で繰り返し開かない。
- **品質ゲートは開発速度を優先して柔軟に運用する。** テストや proof が開発のブロッカーにならないようにする。
- **具体的な現実の日時をドキュメントの方針・ルール記述に含めない。** 日付固定の宣言（「2026-xx-xx 固定」等）は使わない。
- NotebookLM が主台本品質の源泉であり、Python/LLM は主台本を生成しない。
- ただし、NotebookLM 由来の既存台本を前提にした constrained rewrite（2本の台本の接続、聞き手/解説役の整合性調整、再編集指示の自動化）は検討対象に含めてよい。ゼロからの主台本生成とは区別する。
- `build-csv` の既定動作は後方互換を保つ。表示幅ベース分割は opt-in で有効化する。
- 優先度と status は分離する。項目を「先に見る」ことは implementation approval を意味しない。
- canonical rules が repo 内にある場合は、`docs/ai/*.md` を tool-specific helper docs や prompt より先に読む。

## Responsibility Boundaries
- Python の責務はテキスト変換のみ。CSV とテキストメタデータ文字列までに限定する。
- 音声合成・字幕配置・演出指定・レンダリング・サムネイル最終判断は YMM4 または人間の責務。
- `.ymmp` を直接編集しても音声合成は成立しない。音声合成は YMM4 の台本読込経由でのみ行う。
- YMM4 / `.ymmp` の直接編集や画面効果の自動注入は高リスクなため、LLM や Automation を使う場合も、まずはテキスト補助・コピペ用メモ・プリセット候補提示に留める。direct edit は workflow proof なしに採用しない。
- GUI/API/SDK 追加は、value path と境界違反の有無を確認し、必要なら ADR を通してから扱う。
- YMM4 自動化の主経路は「演出 IR 定義 → テンプレート資産蓄積 → 接続方式判断」の段階的アプローチ。特定の外部ツールを主軸にしない。
- 新しい自動化経路を提案する際は、現行ロードマップ (YMM4-AUTOMATION-RESEARCH.md セクション4) の段階構成との整合を示すこと。根拠なしに経路を増やさない。
- YMovieHelper は参照実装 (設計思想の観察対象)。「YMovieHelper を使う」「YMovieHelper に接続する」とは書かない。
- 演出 IR (PRODUCTION_IR_SPEC.md) が視覚配置の中心課題。C-07 系 (演出判断支援) が主系統であり、D-02 (素材取得) は従属的補助論点。D-02 を主軸として扱わない。
- 再開時に「CSV 変換専用ツール」という旧理解に引き戻されないよう、README / CLAUDE.md / WORKFLOW / AUTOMATION_BOUNDARY は演出 IR の役割を反映した状態を維持する。
- patch-ymmp (G-06) は成熟段階モデルで評価する。「研究か実用か」の二択で早期に裁定しない。.ymmp のゼロからの生成 (不可能) と、台本読込後の限定的な後段適用 (patch-ymmp) は明確に区別する。成熟段階: Level 0 構造把握 / Level 1 限定変換器 (face+bg) / Level 2 演出IR適用エンジン / Level 3a face+bg 限定 E2E / Level 3b slot+motion 含む拡張 E2E / Level 4 制作標準装備。現在は Level 1 到達済み、Level 2 形成中。
- IR 語彙に定義済みだが ymmp 適用が未実装のフィールド (motion/transition/overlay/slot/bg_anim) は「境界外」ではなく「正式スコープ内の未実装 frontier」。「未実装」と「境界外」を混同しない。
- 演出パイプラインは Writer 工程 (LLM による IR 生成) と Editor 工程 (テンプレート解決 + ymmp 適用) に分離する。proof の際限なき拡張を防ぐため、Writer の品質はフィードバック駆動で scope を区切り、Editor の設計品質で吸収する。
- 演出パイプラインは三層構造: 第1層 Writer IR (高水準の意味ラベル) / 第2層 Template Registry (素材・プリセット辞書 + YMM4 ネイティブテンプレート名参照) / 第3層 YMM4 Adapter (IR + Registry → ymmp の接着層)。詳細は PRODUCTION_IR_SPEC.md セクション6 を参照。
- YMM4 ネイティブに解決できるもの (エフェクト、アニメーション、場面テンプレート) は YMM4 のアイテムテンプレート機能に委ね、Adapter (patch-ymmp) は face/bg/slot 等の JSON キー置換レベルの差し替えに集中する。YMM4 の既存機能を再発明しない。
- **外部素材ベースの茶番劇演者**（配達員・消防員等の body/顔合成）は、`speaker_tachie` と混同しない。`motion` / `face` / `idle_face` / `slot` は **ゆっくり立ち絵 (`TachieItem`)** の語彙として扱い、茶番劇演者の body 骨格は **GroupItem テンプレート資産**として扱う。正本: `SKIT_GROUP_TEMPLATE_SPEC.md`
- **`TachieItem` は解説役のゆっくり立ち絵専用。** 外部茶番劇演者 (配達員・消防員・アイドル等) の GroupItem 配下には `TachieItem` を含めない。配下構成は **body `ImageItem` + 顔 `ImageItem` + (任意で装飾 `ImageItem`)** の重ね合わせに固定する。理由: 連番アニメ `TachieItem` の新規セットアップ (AnimationTachie プラグイン設定・パーツ分解・表情マッピング) は運用コストが過大で、既に非採用決定済。
- **解説役のゆっくり立ち絵は新規セットアップしない。** 既存の「ゆっくり霊夢」「ゆっくり魔理沙」等の `TachieItem` を流用する。新キャラの連番アニメ立ち絵を増設しない。
- **外部演者の顔感情差し替えは `ImageItem.Source` パス置換で行う。** `TachieFaceParameter` / 連番アニメパーツ分解は外部演者には適用しない。
- **`skit_group` の主経路は canonical template である。** library (tachie_motion_map) / motion_target 直書き / group_motion は補助経路であり、茶番劇固有の所作の主体にはしない。根拠: SKIT_GROUP_TEMPLATE_SPEC §3.1-3.3
- IR は逐次属性の全指定ではなく、scene_preset による高水準バンドル参照 + optional override を基本とする。LLM にはプリセット一覧を渡し、個別フィールドの組み立てを強いない。
- タイトル / サムネイル / 台本の約束 (promise) は central brief で統制し、台本単体が動画タイトルを越権決定しない。最終 owner は人間であり、assistant は判断材料と候補整理を支援する。
- visual density score / evidence richness score は creative final judgement の代替ではなく、gate / diagnostic として使う。スコア最大化自体を目的化しない。

## Prohibited Interpretations / Shortcuts
- rejected を「その工程は不要」と解釈しない。代替の手動導線は WORKFLOW に残す。
- 汚染バッチ由来の候補を、未再審査のまま normal backlog として扱わない。
- `approved` を「有望そう」「今はこれが一番まし」といった意味で使わない。
- ユーザー未指定の固有名詞、音声エンジン、GUI 技術、素材サイト、API 互換先を勝手に採用しない。
- サムネイルの重要性を軽視して、Python 生成や定型化で代替しようとしない。
- テンプレート素材の「完全自動生成」に踏み込まない。NLMYTGen の責務は提案と仮組立まで。素材の作成・収集は人間の責務。
- サムネイル訴求を「衝撃の真実」「知らないと損」のような抽象煽りテンプレの反復で代替しない。年数・人数・割合・金額・固有名詞など、本文根拠のある具体性を優先する。
- 同一構図 / 同一コピー型 / 同一配色の固定テンプレ連打をしない。variation / rotation を設計対象として持つ。
- YMM4 プラグイン開発 (G-01/G-03) に時間を使う前に、演出 IR 定義 (G-02 done) + IR 出力プロンプト (G-05) を進めること。見通しのない .NET 環境構築を先行しない。
- ymmp のゼロからの生成は禁止。台本読込後の限定的な後段適用 (patch-ymmp による face/bg 差し替え) は Level 1 変換器として許容済み。ただし適用範囲の拡張は成熟段階を上げる判断として扱い、無制限な ymmp 編集には進まない。デッドファイル蓄積を避ける。
- テストスイートの拡張を目的化しない。テストは実装の検証手段であり、テスト設計が開発の主活動にならないこと。
- route contract / readback / unit test は **production value path の代替ではない**。テンプレート資産の不足や運用前提のズレを、テスト通過だけで「自動化できた」と扱わない。
- **テストはコードを変更したときだけ実行する。** ドキュメントのみの変更、設定変更、GUI テキスト変更でテストを回さない。テスト実行を作業完了の儀式にしない。
- proof は出力レビューで完了とする。実動画制作や定量計測 (N% 以上が一致等) を proof 要件にしない。
- 手動時間計測を開発目的にしない。効果測定は時間差ではなく、接続成立・failure class・差分証跡を優先する。
- 研究 (ymmp 解析等) と開発 (build-ymh 等) を混同しない。研究に2ブロック以上費やす場合は一度止まって開発に戻る。

## 運用ルール
- ユーザーが一度説明した非交渉条件は、同一ブロック内でここへ固定する。
- `project-context.md` の DECISION LOG には理由を短く残し、ここには条件そのものを残す。

### 意思決定注記 (根拠注記) の最小仕様
対象: 新方針採用 / 方針撤回 / 主軸・slice・next_action 変更 / FEATURE status 遷移 / 台帳新規追記。
対象外: 文言微修正 / typo / 内部 refactor。
形式: `根拠: <源1> [+ <源2>]`
許容源: canonical docs 参照 (例 `INVARIANTS §Responsibility Boundaries`) / 台帳エントリ (例 `USER_REQUEST_LEDGER 2026-04-18`) / DECISION LOG 行 / workflow proof ファイル / FEATURE_REGISTRY ID。
禁止源: 「経験的に」「一般に」「安全上」など verifiable でない抽象文言。

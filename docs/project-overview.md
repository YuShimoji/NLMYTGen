# Project Overview

このページは 2026-06-17 に作られた文書地図です。現在地は
[PROJECT_COCKPIT.md](PROJECT_COCKPIT.md) を先に読み、内部詳細が必要な場合だけ
`runtime-state.md` へ進みます。このページ内の G-27/G-28 例は履歴説明であり、
current next action ではありません。

## まず見る場所

| 知りたいこと | 見る文書 | 読み方 |
| --- | --- | --- |
| GitHub 上で現在地と次の分岐を知る | [PROJECT_COCKPIT.md](PROJECT_COCKPIT.md) | runtime capsule と同じ State ID を持つ current mirror。まずここだけ読む。 |
| これまで実装された機能と、今後候補の状態 | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) | A-H の機能 ID、`done / approved / proposed / hold / rejected` を見る。機能追加や再開可否の正本。 |
| いま進めてよい作業、止めている作業 | [runtime-state.md](runtime-state.md) | 160 行以内の current capsule 全体を見る。履歴はこの文書に置かない。 |
| なぜその判断になったか | [project-context.md](project-context.md) | decision log / handoff の該当範囲を見る。過去ロードマップを正本に戻さないための履歴置き場。 |
| 文書群の正しい入り口 | [NAV.md](NAV.md) | 作業タイプ別に追加で読む文書を決める。迷ったときの地図。 |
| 開発・レビューのサイクル | [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md) | plan / review surface / machine proof / human signal / close gate の流れを確認する。 |

## 機能実装は項目別に見えるか

項目別の実装状況は [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) にまとまっています。大枠は次の読み方です。

| 領域 | 代表 ID | 見えること |
| --- | --- | --- |
| 台本取得・変換 | A / B | NotebookLM 入力、CSV 変換、字幕 reflow、診断 CLI の実装済み範囲 |
| YMM4・演出補助 | C / G | Production IR、patch、motion、overlay、SE、skit group、G-27/G-28 系の状態 |
| 素材・投稿・GUI | D / E / F | Python 側でやらないこと、YouTube 周辺の hold、GUI 補助機能 |
| packaging / 評価 | H | brief、thumbnail、visual density、evidence richness、session manifest 系 |

ただし、FEATURE_REGISTRY は台帳なので、文章としての「現在の見通し」は [runtime-state.md](runtime-state.md) と [project-context.md](project-context.md) を併読します。実装詳細やコマンドは [docs/dev/CLI_REFERENCE.md](dev/CLI_REFERENCE.md)、構造は [ARCHITECTURE.md](ARCHITECTURE.md)、IR と対応範囲は [PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) / [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) に分かれています。

## 進捗を即確認できる画面証跡

スクリーンショットや proof image は散在しています。すぐ見る入口として [Visual Proof Index](visual-proof-index.md) を追加しました。

| 種類 | 主な配置 | 状態 |
| --- | --- | --- |
| G-27 Real Estate DX proof / screenshot | `samples/_probe/g24/` | PNG / HTML / readback が存在。G-27 は診断証跡として保持され、active production blocker としては G-28 へ学びを渡している。 |
| G-28 layout prototype | `samples/_probe/g28/reference_layout_prototypes/` | HTML prototype pack が存在する履歴証跡。現在のレビュー入口ではない。 |
| pipeline smoke proof | `samples/_probe/pipeline_smoke/` | GUI screenshot と visual treatment proof が存在。 |
| thumbnail proof | `samples/*thumb*.png` など | YMM4/user 書き出しによるサムネ proof。Python 画像生成ではない。 |

## 履歴上の turn map

2026-06-17 時点の補助計画は [Turn-Based Development Map](turn-based-development-map.md) に残っています。これは current plan ではなく、当時の G-28 / common-foundation 判断経路を読む履歴資料です。

現在の分岐は `PROJECT_COCKPIT.md` を使います。turn map を更新して current を二重管理しません。

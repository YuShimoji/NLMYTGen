# CLAUDE.md — NLMYTGen プロジェクト方針
# このファイルはプロジェクトの方針・技術スタック・成功定義を定める。
# 運用ルールの正本は docs/REPO_LOCAL_RULES.md。Claude Code 入口は .claude/CLAUDE.md（ポインタ）。全体の入口は AGENTS.md。

## プロジェクト概要
NotebookLM の台本を YMM4 用 CSV に変換し、さらに演出 IR (中間表現) を定義して S-6 (背景・演出設定) の半自動化を目指すパイプライン。音声・字幕投入は YMM4 台本読込が不動の主経路。視覚配置 (背景・立ち絵・素材) の効率化が現在の中心課題。

## 技術スタック
- Python (stdlib のみ、外部ライブラリなし)
- uv（パッケージ管理・タスクランナー）
- pytest（テスト。既定はユニット中心で高速、`NLMYTGEN_PYTEST_FULL=1` で CLI 統合まで全件）
- YMM4（音声合成・動画レンダリング — 外部ツール、Python では操作しない）

## 成功定義（Phase 1: 全達成 2026-03-29）
1. ✅ 任意の NLM transcript を入力し、YMM4 が読み込める CSV を出力できる
2. ✅ その CSV を YMM4 に読み込ませ、動画をレンダリングできる
3. ✅ 複数の NLM transcript で再現性がある

## 絶対的な制約
- **Python で動画をレンダリングしない** (ADR-0003)
- **Voicevox / 外部 TTS は使用しない** — 音声合成は YMM4 内蔵機能を使う
- **動画生成・合成は YMM4 上で完結する**
- **NotebookLM が台本品質の源泉** (ADR-0002) — LLM で主台本を生成しない
- **他プロジェクトを参照しない** (AGENTS.md 境界ルール)

## 機能追加のルール
- **docs/FEATURE_REGISTRY.md が全件把握の唯一のソース**
- FEATURE_REGISTRY に登録されていない機能は追加しない
- `proposed` ステータスの機能はユーザー承認後に `approved` へ昇格してから実装する
- 自動化の境界は docs/AUTOMATION_BOUNDARY.md に従う

## 動画制作ワークフロー（全体像）

ゆっくり解説動画の標準的な制作フロー。NLMYTGen は S-3 (CSV変換) と S-6 支援 (演出 IR + LLM プロンプト) を担当する。

```
[準備]    S-0  YMM4 テンプレート構築 (初回のみ)
[台本]    S-1  NotebookLM → S-2  台本取得 → S-3  NLMYTGen CSV変換
[演出IR]  S-3b 演出 IR 生成 (LLM プロンプト経由、Python 変更なし)
[YMM4]    S-4  台本読込 → S-5  読み上げ確認 → S-6  背景・演出 → S-7  レンダリング
[公開]    S-8  サムネイル制作 → S-9  YouTube 投稿
```

- S-3 (Python) の出力は CSV。S-3b は LLM (Custom GPT) が演出 IR を出力し、人間が S-6 で参照する
- 音声・字幕投入は YMM4 台本読込が不動の主経路。ymmp 直接編集では音声合成されない
- 視覚配置 (背景・立ち絵・素材) の効率化は演出 IR + テンプレート定義で段階的に進める
- 詳細: docs/WORKFLOW.md, docs/AUTOMATION_BOUNDARY.md

## ドキュメント構成

| ファイル | 責務 |
|---------|------|
| CLAUDE.md (ルート) | プロジェクト方針・技術スタック・成功定義・本書の「絶対的な制約」。日々の運用 Hard Rules の正本は `docs/REPO_LOCAL_RULES.md`（`.claude/CLAUDE.md` は入口ポインタ）、非交渉境界の正本は `docs/INVARIANTS.md` |
| AGENTS.md | 入口・境界ルール・再アンカリング手順・read order 関係の正本 |
| docs/ai/CORE_RULESET.md | AI 運用の canonical rules |
| docs/ai/DECISION_GATES.md | 進路判断・gate・read-only ルール |
| docs/ai/STATUS_AND_HANDOFF.md | status 語彙と handoff 要件 |
| docs/ai/WORKFLOWS_AND_PHASES.md | 再開時 read order・phase ルール |
| docs/INVARIANTS.md | 非交渉条件・境界・禁止ショートカット |
| docs/USER_REQUEST_LEDGER.md | ユーザー継続要求・是正要求・backlog delta |
| docs/OPERATOR_WORKFLOW.md | 実運用フロー・pain・品質目標 |
| docs/INTERACTION_NOTES.md | 報告・質問形式に関する project memory |
| docs/FEATURE_REGISTRY.md | **機能一覧（全件把握）** |
| docs/AUTOMATION_BOUNDARY.md | YMM4内部/外部の自動化境界 |
| docs/ARCHITECTURE.md | モジュール構成・データフロー |
| docs/PIPELINE_SPEC.md | パイプラインの入出力仕様 |
| docs/WORKFLOW.md | 動画制作の操作手順 |
| docs/REPO_LOCAL_RULES.md | repo-local 運用（Hard Rules・Read Order・Checklist）の正本 |
| docs/verification/README.md | 検証ディレクトリの索引・正本チェーン・読み方 |
| docs/PROJECT_CHARTER.md | v2 の設立経緯・再発防止原則 |
| docs/project-context.md | DECISION LOG・IDEA POOL・HANDOFF |
| docs/runtime-state.md | 現在位置・カウンター |

## 再開時の正本順序

再開時は `AGENTS.md` の read order を優先する。
要点だけ書くと、入口 → repo-local rules → `docs/ai/*.md` → project-local canonical docs → runtime/context/registry/boundary の順で読む。
resume prompt や外部メモより、repo 内 docs を常に優先する。

## スコープ外（現時点）
- ブラウザ向け Web UI / API サーバー（デスクトップ Electron GUI は `gui/` でスコープ内）
- 他プロジェクト（HoloSync / NLMandSlideVideoGenerator 等）との連携

# CLAUDE.md — NLMYTGen プロジェクト方針
# このファイルはプロジェクトの方針・技術スタック・成功定義を定める。
# 運用ルールは .claude/CLAUDE.md を参照。入口は AGENTS.md を参照。

## プロジェクト概要
NotebookLM の台本を YMM4 用 CSV に変換し、YMM4 での動画制作を効率化するパイプライン。

## 技術スタック
- Python (stdlib のみ、外部ライブラリなし)
- uv（パッケージ管理・タスクランナー）
- pytest（テスト）
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

```
L1 入力取得    L2 変換         L3 YMM4内部      L4 配信
NotebookLM → NLMYTGen CLI → YMM4            → YouTube
             (Python)        音声合成
                             字幕配置
                             動画レンダリング
```

- L2 (Python) の出力は CSV / メタデータ / テンプレートファイルまで
- L3 (YMM4) が音声合成・動画レンダリングを担う
- 詳細: docs/AUTOMATION_BOUNDARY.md

## ドキュメント構成

| ファイル | 責務 |
|---------|------|
| CLAUDE.md | プロジェクト方針・制約・ルール |
| AGENTS.md | 入口・境界ルール・再アンカリング手順 |
| docs/FEATURE_REGISTRY.md | **機能一覧（全件把握）** |
| docs/AUTOMATION_BOUNDARY.md | YMM4内部/外部の自動化境界 |
| docs/ARCHITECTURE.md | モジュール構成・データフロー |
| docs/PIPELINE_SPEC.md | パイプラインの入出力仕様 |
| docs/WORKFLOW.md | 動画制作の操作手順 |
| docs/PROJECT_CHARTER.md | v2 の設立経緯・再発防止原則 |
| docs/project-context.md | DECISION LOG・IDEA POOL・HANDOFF |
| docs/runtime-state.md | 現在位置・カウンター |

## スコープ外（現時点）
- Web UI / API サーバー
- 他プロジェクト（HoloSync / NLMandSlideVideoGenerator 等）との連携

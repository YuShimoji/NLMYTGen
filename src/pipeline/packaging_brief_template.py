"""H-01 Packaging Orchestrator brief の空テンプレート（PACKAGING_ORCHESTRATOR_SPEC v0.1 §5 と同期すること）。"""

from __future__ import annotations

import json

# 正本: docs/PACKAGING_ORCHESTRATOR_SPEC.md の「5. 推奨フォーマット」コードブロック
H01_MARKDOWN_BLANK = """# Packaging Orchestrator Brief

- brief_version: 0.1
- video_id:
- topic_label:
- target_viewer:
- audience_hook:
- title_promise:
- thumbnail_promise:

## novelty_basis
- ...

## required_evidence
- kind:
  value:
  why_it_matters:
  must_surface_in:
  status:

## missing_or_weak_evidence
- ...

## forbidden_overclaim
- ...

## thumbnail_controls
- prefer_specificity:
- preferred_specifics:
- banned_copy_patterns:
- rotation_axes:
  - layout_family:
  - emotion_family:
  - color_family:
  - copy_family:

## script_opening_commitment
- ...

## must_payoff_by_section
- ...

## alignment_check
- ...

## consumer_hints
- for_c07:
- for_c08:
- for_e02:
- for_h04:
- for_h03:
"""


def minimal_json_brief() -> dict:
    """スコア CLI が解釈できる最小構造（中身はプレースホルダ）。"""
    return {
        "brief_version": "0.1",
        "video_id": "replace_me",
        "topic_label": "",
        "target_viewer": "",
        "audience_hook": "",
        "title_promise": "",
        "thumbnail_promise": "",
        "novelty_basis": [],
        "required_evidence": [],
        "missing_or_weak_evidence": [],
        "forbidden_overclaim": [],
        "thumbnail_controls": {
            "prefer_specificity": True,
            "preferred_specifics": [],
            "banned_copy_patterns": [],
            "rotation_axes": {
                "layout_family": "",
                "emotion_family": "",
                "color_family": "",
                "copy_family": "",
            },
        },
        "script_opening_commitment": "",
        "must_payoff_by_section": [],
        "alignment_check": [],
        "consumer_hints": {},
    }


def emit_markdown() -> str:
    return H01_MARKDOWN_BLANK


def emit_json_text() -> str:
    return json.dumps(minimal_json_brief(), ensure_ascii=False, indent=2) + "\n"

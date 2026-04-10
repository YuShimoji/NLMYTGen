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

REQUIRED_JSON_KEYS = (
    "brief_version",
    "video_id",
    "topic_label",
    "target_viewer",
    "audience_hook",
    "title_promise",
    "thumbnail_promise",
    "novelty_basis",
    "required_evidence",
    "missing_or_weak_evidence",
    "forbidden_overclaim",
    "thumbnail_controls",
    "script_opening_commitment",
    "must_payoff_by_section",
    "alignment_check",
    "consumer_hints",
)

REQUIRED_ROTATION_AXES_KEYS = (
    "layout_family",
    "emotion_family",
    "color_family",
    "copy_family",
)

REQUIRED_CONSUMER_HINT_KEYS = (
    "for_c07",
    "for_c08",
    "for_e02",
    "for_h04",
    "for_h03",
)

REQUIRED_MARKDOWN_SECTIONS = (
    "# Packaging Orchestrator Brief",
    "## novelty_basis",
    "## required_evidence",
    "## missing_or_weak_evidence",
    "## forbidden_overclaim",
    "## thumbnail_controls",
    "## script_opening_commitment",
    "## must_payoff_by_section",
    "## alignment_check",
    "## consumer_hints",
)


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
        "consumer_hints": {
            "for_c07": "",
            "for_c08": "",
            "for_e02": "",
            "for_h04": "",
            "for_h03": "",
        },
    }


def _validate_json_brief_schema(data: dict) -> None:
    """最低限の schema drift を検出する."""
    missing = [key for key in REQUIRED_JSON_KEYS if key not in data]
    if missing:
        raise ValueError(f"H-01 JSON template missing required keys: {', '.join(missing)}")

    if not isinstance(data["required_evidence"], list):
        raise ValueError("H-01 JSON template invalid type: required_evidence must be a list")
    if not isinstance(data["alignment_check"], list):
        raise ValueError("H-01 JSON template invalid type: alignment_check must be a list")
    if not isinstance(data["thumbnail_controls"], dict):
        raise ValueError("H-01 JSON template invalid type: thumbnail_controls must be an object")
    if not isinstance(data["consumer_hints"], dict):
        raise ValueError("H-01 JSON template invalid type: consumer_hints must be an object")

    rotation_axes = data["thumbnail_controls"].get("rotation_axes")
    if not isinstance(rotation_axes, dict):
        raise ValueError("H-01 JSON template invalid type: thumbnail_controls.rotation_axes must be an object")
    missing_rotation_axes = [key for key in REQUIRED_ROTATION_AXES_KEYS if key not in rotation_axes]
    if missing_rotation_axes:
        raise ValueError(
            "H-01 JSON template missing required thumbnail_controls.rotation_axes keys: "
            + ", ".join(missing_rotation_axes)
        )

    missing_consumer_hints = [key for key in REQUIRED_CONSUMER_HINT_KEYS if key not in data["consumer_hints"]]
    if missing_consumer_hints:
        raise ValueError(
            "H-01 JSON template missing required consumer_hints keys: "
            + ", ".join(missing_consumer_hints)
        )


def _validate_markdown_template(text: str) -> None:
    """spec §5 との最低限の同期を確認する."""
    missing = [marker for marker in REQUIRED_MARKDOWN_SECTIONS if marker not in text]
    if missing:
        raise ValueError(f"H-01 Markdown template missing sections: {', '.join(missing)}")


def emit_markdown() -> str:
    _validate_markdown_template(H01_MARKDOWN_BLANK)
    return H01_MARKDOWN_BLANK if H01_MARKDOWN_BLANK.endswith("\n") else H01_MARKDOWN_BLANK + "\n"


def emit_json_text() -> str:
    payload = minimal_json_brief()
    _validate_json_brief_schema(payload)
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

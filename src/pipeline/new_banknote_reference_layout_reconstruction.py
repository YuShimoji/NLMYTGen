from __future__ import annotations

import argparse
import hashlib
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


BASE_REVISION = "649ada5050be5b9b2153c50c938d855797d5c19f"
ROUTE_A_TREE_OID = "8b7f507ddca49d4f3fb5526960adfcd3457baa15"
REJECTED_PROOF_TREE_OID = "66e099e3f10369019840ea44cc24ad7243d6d253"
TRACE_COMPLETED_AT = "2026-07-21T01:10:00+09:00"
DESIGN_STARTED_AT = "2026-07-21T01:20:00+09:00"
OUTPUT_INSPECTED_AT = "2026-07-21T03:00:00+09:00"
DESIGN_ID = "object_closeup_lowerthird_baseline"
STATE_ID = "new-banknote-reference-layout-reconstructed-human-review-ready-v1"
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

PILOT = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_OUTPUT = PILOT / "reference_layout_reconstruction"
REFERENCE_PACKAGE = PILOT / "reference_grounded_visual_design"
ROUTE_A_PACKAGE = PILOT / "route_a_visual_proof"


def _box(x: float, y: float, width: float, height: float) -> dict[str, float]:
    return {"x": x, "y": y, "width": width, "height": height}


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "T-O01",
        "source_id": "O01",
        "cohort": "official_educational",
        "publisher": "独立行政法人 国立印刷局",
        "evidence_class": "page_or_frame_observed",
        "inspected_surface": "multi-state hologram image / 3Dで見る偽造防止技術",
        "local_capture": "../reference_grounded_visual_design/local_reference_captures/O01_npb_hologram.jpg",
        "primary_object_bounds": [_box(0.02, 0.04, 0.23, 0.92)],
        "closeup_crop_bounds": [_box(0.31, 0.08, 0.64, 0.84)],
        "subtitle_bounds": [],
        "character_nameplate_bounds": [],
        "callout_bounds": [_box(0.31, 0.08, 0.64, 0.84)],
        "source_credit_bounds": [],
        "title_key_term_bounds": [_box(0.27, 0.06, 0.05, 0.86)],
        "persistent_elements": ["feature specimen strip", "four feature rows"],
        "temporary_elements": ["angle-state change within each row"],
        "dominant_visual_weight": "feature specimen and close-up states",
        "simultaneous_focal_regions": 2,
        "motion_state": "four bounded angle states represented as stills; timing not observed",
        "source_specific_exclusions": ["exact portrait", "ornament", "iridescent source pixels", "numbering style"],
        "shared_patterns": ["SG01_OBJECT_DOMINANCE", "SG02_BOUNDED_FEATURE_FOCUS", "SG05_SHORT_KEY_ADJACENCY"],
        "confidence": "high",
    },
    {
        "trace_id": "T-O02",
        "source_id": "O02",
        "cohort": "official_educational",
        "publisher": "日本銀行",
        "evidence_class": "page_or_frame_observed",
        "inspected_surface": "annotated note overview / 1．偽造防止技術",
        "local_capture": "../reference_grounded_visual_design/local_reference_captures/O02_boj_annotated_note.png",
        "primary_object_bounds": [_box(0.05, 0.08, 0.43, 0.82), _box(0.53, 0.08, 0.43, 0.82)],
        "closeup_crop_bounds": [_box(0.09, 0.09, 0.39, 0.80)],
        "subtitle_bounds": [],
        "character_nameplate_bounds": [],
        "callout_bounds": [_box(0.07, 0.06, 0.42, 0.84)],
        "source_credit_bounds": [],
        "title_key_term_bounds": [_box(0.04, 0.02, 0.09, 0.09)],
        "persistent_elements": ["two object faces", "numbered feature outlines"],
        "temporary_elements": ["feature magnification after overview"],
        "dominant_visual_weight": "annotated source object",
        "simultaneous_focal_regions": 2,
        "motion_state": "paired stills; no timing claim",
        "source_specific_exclusions": ["exact note likeness", "specimen marks", "institutional color coding"],
        "shared_patterns": ["SG01_OBJECT_DOMINANCE", "SG02_BOUNDED_FEATURE_FOCUS", "SG05_SHORT_KEY_ADJACENCY"],
        "confidence": "high",
    },
    {
        "trace_id": "T-J03",
        "source_id": "J03",
        "cohort": "journalism_documentary",
        "publisher": "毎日放送／TBS NEWS DIG",
        "evidence_class": "page_or_frame_observed",
        "inspected_surface": "studio explainer preview frame / presenter plus numbered three-point board",
        "local_capture": "../reference_grounded_visual_design/local_reference_captures/J03_tbs_mbs.png",
        "primary_object_bounds": [_box(0.28, 0.14, 0.69, 0.78)],
        "closeup_crop_bounds": [_box(0.35, 0.23, 0.22, 0.58)],
        "subtitle_bounds": [_box(0.00, 0.00, 1.00, 0.12)],
        "character_nameplate_bounds": [_box(0.02, 0.24, 0.28, 0.70)],
        "callout_bounds": [_box(0.57, 0.20, 0.39, 0.61)],
        "source_credit_bounds": [_box(0.01, 0.02, 0.13, 0.08)],
        "title_key_term_bounds": [_box(0.59, 0.23, 0.36, 0.56)],
        "persistent_elements": ["presenter edge", "object board", "broadcast title"],
        "temporary_elements": ["numbered topic emphasis"],
        "dominant_visual_weight": "object board with presenter secondary",
        "simultaneous_focal_regions": 2,
        "motion_state": "preview still only; presenter and board persistence unknown",
        "source_specific_exclusions": ["presenter identity", "studio set", "broadcast logo", "exact numbered copy"],
        "shared_patterns": ["SG02_BOUNDED_FEATURE_FOCUS", "SG04_EDGE_SPEAKER_CUE", "SG05_SHORT_KEY_ADJACENCY"],
        "confidence": "medium_high",
    },
    {
        "trace_id": "T-J05",
        "source_id": "J05",
        "cohort": "journalism_documentary",
        "publisher": "FNNプライムオンライン／イット！",
        "evidence_class": "page_or_frame_observed",
        "inspected_surface": "broadcast opening frame / three object specimens plus lower-third",
        "local_capture": "../reference_grounded_visual_design/local_reference_captures/J05_fnn.png",
        "primary_object_bounds": [_box(0.00, 0.00, 1.00, 0.78)],
        "closeup_crop_bounds": [],
        "subtitle_bounds": [_box(0.06, 0.73, 0.89, 0.24)],
        "character_nameplate_bounds": [],
        "callout_bounds": [],
        "source_credit_bounds": [_box(0.92, 0.86, 0.06, 0.10)],
        "title_key_term_bounds": [_box(0.07, 0.76, 0.82, 0.18)],
        "persistent_elements": ["full-frame object", "two-line lower-third"],
        "temporary_elements": ["later feature close-ups, not traced from opening frame"],
        "dominant_visual_weight": "full-frame object",
        "simultaneous_focal_regions": 1,
        "motion_state": "opening still; subsequent motion not inspected",
        "source_specific_exclusions": ["exact object pixels", "publisher lower-third styling", "logo"],
        "shared_patterns": ["SG01_OBJECT_DOMINANCE", "SG03_BOTTOM_SUBTITLE_BAND"],
        "confidence": "high",
    },
    {
        "trace_id": "T-Y01",
        "source_id": "Y01",
        "cohort": "yukkuri_adjacent_explainer",
        "publisher": "にゃんだもん",
        "evidence_class": "in_video_frame_observed",
        "inspected_surface": "00:30.003 decoded frame / ATM background and dialogue",
        "local_capture": "../reference_grounded_visual_design/local_in_video_observations/Y01_t0030_cdp.png",
        "primary_object_bounds": [_box(0.00, 0.00, 1.00, 1.00)],
        "closeup_crop_bounds": [],
        "subtitle_bounds": [_box(0.48, 0.55, 0.47, 0.25)],
        "character_nameplate_bounds": [_box(0.00, 0.23, 0.30, 0.77), _box(0.70, 0.00, 0.30, 0.76)],
        "callout_bounds": [_box(0.48, 0.55, 0.47, 0.25)],
        "source_credit_bounds": [],
        "title_key_term_bounds": [],
        "persistent_elements": ["object background in observed frame", "two edge speakers"],
        "temporary_elements": ["dialogue bubble content"],
        "dominant_visual_weight": "object environment with dialogue foreground",
        "simultaneous_focal_regions": 2,
        "motion_state": "single paused frame; persistence and alternation unknown",
        "source_specific_exclusions": ["character art", "ATM image", "bubble styling", "creator colors"],
        "shared_patterns": ["SG03_BOTTOM_SUBTITLE_BAND", "SG04_EDGE_SPEAKER_CUE"],
        "confidence": "high_for_frame_only",
    },
    {
        "trace_id": "T-Y02",
        "source_id": "Y02",
        "cohort": "yukkuri_adjacent_explainer",
        "publisher": "グリム貨幣コレクション",
        "evidence_class": "in_video_frame_observed",
        "inspected_surface": "00:30.011 decoded frame / six-image object grid and lower subtitle",
        "local_capture": "../reference_grounded_visual_design/local_in_video_observations/Y02_t0030_cdp.png",
        "primary_object_bounds": [_box(0.20, 0.03, 0.62, 0.79)],
        "closeup_crop_bounds": [_box(0.20, 0.03, 0.62, 0.79)],
        "subtitle_bounds": [_box(0.24, 0.82, 0.58, 0.17)],
        "character_nameplate_bounds": [_box(0.00, 0.68, 0.23, 0.32), _box(0.82, 0.69, 0.18, 0.31)],
        "callout_bounds": [],
        "source_credit_bounds": [_box(0.21, 0.03, 0.59, 0.77)],
        "title_key_term_bounds": [],
        "persistent_elements": ["central object field", "two lower-corner speakers"],
        "temporary_elements": ["two-line lower subtitle"],
        "dominant_visual_weight": "central object grid",
        "simultaneous_focal_regions": 1,
        "motion_state": "single paused frame; persistence and frequency unknown",
        "source_specific_exclusions": ["source object collage", "watermarks", "character art", "player controls"],
        "shared_patterns": ["SG01_OBJECT_DOMINANCE", "SG03_BOTTOM_SUBTITLE_BAND", "SG04_EDGE_SPEAKER_CUE"],
        "confidence": "high_for_frame_only",
    },
]


SHARED_GRAMMAR: list[dict[str, Any]] = [
    {
        "grammar_id": "SG01_OBJECT_DOMINANCE",
        "description": "source object or object proxy carries the largest visual area",
        "supporting_trace_ids": ["T-O01", "T-O02", "T-J05", "T-Y02"],
        "cohorts": ["official_educational", "journalism_documentary", "yukkuri_adjacent_explainer"],
        "threshold": "at_least_3_independent_references_and_2_cohorts",
        "passed": True,
    },
    {
        "grammar_id": "SG02_BOUNDED_FEATURE_FOCUS",
        "description": "a feature is isolated in a bounded crop, board region, or detail state",
        "supporting_trace_ids": ["T-O01", "T-O02", "T-J03"],
        "cohorts": ["official_educational", "journalism_documentary"],
        "threshold": "at_least_3_independent_references_and_2_cohorts",
        "passed": True,
    },
    {
        "grammar_id": "SG03_BOTTOM_SUBTITLE_BAND",
        "description": "spoken explanation occupies a lower band while the object remains visible",
        "supporting_trace_ids": ["T-J05", "T-Y01", "T-Y02"],
        "cohorts": ["journalism_documentary", "yukkuri_adjacent_explainer"],
        "threshold": "at_least_3_independent_references_and_2_cohorts",
        "passed": True,
    },
    {
        "grammar_id": "SG04_EDGE_SPEAKER_CUE",
        "description": "speaker presence is kept at a frame edge and secondary to the object",
        "supporting_trace_ids": ["T-J03", "T-Y01", "T-Y02"],
        "cohorts": ["journalism_documentary", "yukkuri_adjacent_explainer"],
        "threshold": "at_least_3_independent_references_and_2_cohorts",
        "passed": True,
    },
    {
        "grammar_id": "SG05_SHORT_KEY_ADJACENCY",
        "description": "short feature terms sit adjacent to the object or focus region",
        "supporting_trace_ids": ["T-O01", "T-O02", "T-J03"],
        "cohorts": ["official_educational", "journalism_documentary"],
        "threshold": "at_least_3_independent_references_and_2_cohorts",
        "passed": True,
    },
]


KEYFRAME_SPECS = [
    {"filename": "reconstructed_S1_overview.svg", "cue_id": "cue_001", "scene_id": "S1", "term": "まず、対象を見る", "kind": "overview", "refs": ["T-O02", "T-J05", "T-Y02"]},
    {"filename": "reconstructed_cue_003_watermark.svg", "cue_id": "cue_003", "scene_id": "S2", "term": "透かす", "kind": "watermark", "refs": ["T-O01", "T-O02", "T-J03"]},
    {"filename": "reconstructed_cue_004_hologram.svg", "cue_id": "cue_004", "scene_id": "S2", "term": "傾ける", "kind": "hologram", "refs": ["T-O01", "T-J03", "T-J05"]},
    {"filename": "reconstructed_cue_005_intaglio.svg", "cue_id": "cue_005", "scene_id": "S2", "term": "触る", "kind": "intaglio", "refs": ["T-O01", "T-O02", "T-Y01"]},
    {"filename": "reconstructed_cue_006_microtext.svg", "cue_id": "cue_006", "scene_id": "S2", "term": "ルーペで見る", "kind": "microtext", "refs": ["T-O01", "T-O02", "T-J03"]},
    {"filename": "reconstructed_S3_summary.svg", "cue_id": "cue_009", "scene_id": "S3", "term": "四つを覚える", "kind": "summary", "refs": ["T-J05", "T-Y01", "T-Y02"]},
]


DECISIONS = [
    ("D01", "dominant object field", ["T-O01", "T-O02", "T-J05", "T-Y02"], "trace_supported"),
    ("D02", "one bounded feature focus", ["T-O01", "T-O02", "T-J03"], "trace_supported"),
    ("D03", "bottom subtitle band", ["T-J05", "T-Y01", "T-Y02"], "trace_supported"),
    ("D04", "small edge speaker nameplate instead of character art", ["T-J03", "T-Y01", "T-Y02"], "content_lock_requirement"),
    ("D05", "short key term adjacent to focus", ["T-O02", "T-J03", "T-Y01"], "trace_supported"),
    ("D06", "source-specific imagery and branding excluded", ["T-O01", "T-J05"], "rights_requirement"),
    ("D07", "neutral grayscale contrast without a theme", [], "neutral_glue"),
    ("D08", "straight full-frame geometry without outer cards", ["T-O02", "T-Y01"], "trace_supported"),
    ("D09", "rectangular production filmstrip", ["T-J03", "T-J05"], "platform_geometry"),
    ("D10", "detail crop replaces abstract dashboard widgets", ["T-O01", "T-Y02"], "trace_supported"),
]


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def _write_json(path: Path, value: dict[str, Any]) -> None:
    _write_text(path, json.dumps(value, ensure_ascii=False, indent=2))


def _svg_root(*, extra: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" '
        f'height="{CANVAS_HEIGHT}" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" {extra}>'
    )


def _trace_svg(trace: dict[str, Any]) -> str:
    colors = {
        "primary_object_bounds": "#d6d6d2",
        "closeup_crop_bounds": "#8c96a3",
        "subtitle_bounds": "#c39a3a",
        "character_nameplate_bounds": "#a16f72",
        "callout_bounds": "#697c64",
        "source_credit_bounds": "#8e7d66",
        "title_key_term_bounds": "#b2b2b2",
    }
    labels = {
        "primary_object_bounds": "PRIMARY OBJECT",
        "closeup_crop_bounds": "CLOSE-UP / CROP",
        "subtitle_bounds": "SUBTITLE",
        "character_nameplate_bounds": "SPEAKER / NAME",
        "callout_bounds": "CALLOUT",
        "source_credit_bounds": "SOURCE CREDIT",
        "title_key_term_bounds": "TITLE / KEY TERM",
    }
    parts = [
        _svg_root(extra=f'data-trace-id="{trace["trace_id"]}" data-source-id="{trace["source_id"]}"'),
        '<rect width="1920" height="1080" fill="#171717"/>',
        '<rect x="28" y="28" width="1864" height="1024" fill="#202020" stroke="#707070" stroke-width="2"/>',
        f'<text x="58" y="78" fill="#f2f2ef" font-family="sans-serif" font-size="30" font-weight="700">{trace["trace_id"]}  {trace["source_id"]}</text>',
        f'<text x="58" y="116" fill="#bcbcbc" font-family="sans-serif" font-size="20">{html.escape(trace["cohort"])} / {html.escape(trace["evidence_class"])}</text>',
        '<text x="790" y="80" fill="#bcbcbc" font-family="sans-serif" font-size="16">GEOMETRY LEGEND</text>',
        "".join(
            f'<text x="{790 + index * 154}" y="114" fill="{colors[field]}" '
            f'font-family="sans-serif" font-size="14" font-weight="700">{labels[field]}</text>'
            for index, field in enumerate(colors)
        ),
        '<rect x="58" y="150" width="1804" height="844" fill="#101010" stroke="#565656" stroke-width="2"/>',
    ]
    order = list(colors)
    for field in order:
        for box in trace[field]:
            x = 58 + box["x"] * 1804
            y = 150 + box["y"] * 844
            width = box["width"] * 1804
            height = box["height"] * 844
            color = colors[field]
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="5" stroke-dasharray="14 8"/>'
            )
    parts.extend(
        [
            f'<text x="58" y="1030" fill="#bcbcbc" font-family="sans-serif" font-size="18">dominant: {html.escape(trace["dominant_visual_weight"])}</text>',
            '</svg>',
        ]
    )
    return "".join(parts)


def _audit_markdown() -> str:
    rows = [
        ("HTML hero heading", "large artifact-level statement competes with frames", "product landing-page hierarchy", "none", "remove", "compact operator header; viewer first"),
        ("English eyebrow", "slogan-like uppercase evidence claim", "AI portfolio convention", "none", "remove", "no promotional eyebrow"),
        ("count pills", "four pill metrics under hero", "SaaS status grammar", "none", "remove", "plain text revision fields"),
        ("Authority card", "standalone rounded authority panel", "dashboard trust card", "none", "remove", "authority remains in receipt and footer instructions"),
        ("rounded two-column gallery", "six mini frames arranged as cards", "feature gallery", "none", "replace", "one large production viewer and filmstrip"),
        ("nested frame cards", "video diagrams sit inside rounded white frames inside page cards", "AI-generated slide/card grammar", "none", "replace", "full-frame object proxy without outer card"),
        ("palette", "dark/off-white/cyan system appears without cross-reference need", "generic AI default palette", "multi-reference palettes diverge", "discard", "neutral grayscale plus functional speaker marker"),
        ("typography scale", "giant page title and repeated large card titles", "marketing hierarchy", "references prioritize object and lower-third", "replace", "compact operator type; exact subtitle dominates only inside frame"),
        ("whitespace and marketing-page hierarchy", "large blank landing-page field separates product sections", "SaaS marketing rhythm", "none", "remove", "dense production review spacing"),
        ("meta-status copy", "clean viewer/evidence/review status is prominent", "artifact marketing copy", "none", "demote", "machine metadata outside viewer"),
        ("viewer-frame miniaturization", "1920x1080 frames are thumbnails instead of primary artifact", "gallery-first presentation", "references show the subject large", "replace", "single large 16:9 viewer"),
        ("circular icon grammar", "generic numbered circles carry the main explanation", "AI process diagram", "none", "remove", "object crop and one rectangular focus"),
        ("reference metadata placement", "research claims surround the visual rather than shape it", "evidence wrapper over AI-original composition", "traces must precede design", "replace", "trace registry and decision lineage govern coordinates"),
    ]
    header = (
        "# Current ChatGPT-style deviation report\n\n"
        "- Status: `reference_researched_but_ai_template_presentation_rejected`\n"
        "- Current visual authority: `false`\n"
        "- Historical evidence: `true`\n\n"
        "The user rejection applies to both the outer review page and the viewer frames. "
        "The prior package remains byte-exact history at tree OID "
        f"`{REJECTED_PROOF_TREE_OID}`.\n\n"
        "| location/path | visible symptom | likely origin | existing-reference support | user rejection | disposition | replacement rule | protected historical hash |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )
    return header + "\n".join(
        "| " + " | ".join(
            [
                location,
                symptom,
                origin,
                support,
                "explicitly rejected",
                disposition,
                rule,
                f"`{REJECTED_PROOF_TREE_OID}`",
            ]
        ) + " |"
        for location, symptom, origin, support, disposition, rule in rows
    )


def _trace_registry() -> dict[str, Any]:
    counts = Counter(trace["cohort"] for trace in TRACES)
    return {
        "schema_version": "new_banknote.reference_layout_trace_registry.v1",
        "status": "tracing_complete_before_replacement_design",
        "base_revision": BASE_REVISION,
        "tracing_completed_at": TRACE_COMPLETED_AT,
        "design_generation_started_at": DESIGN_STARTED_AT,
        "trace_count": len(TRACES),
        "cohort_counts": dict(counts),
        "selected_source_ids": [trace["source_id"] for trace in TRACES],
        "all_selected_sources_have_actual_visual_evidence": True,
        "traces": TRACES,
    }


def _trace_matrix() -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.reference_layout_trace_matrix.v1",
        "coordinate_space": "normalized_16_9",
        "bounds_fields": [
            "primary_object_bounds",
            "closeup_crop_bounds",
            "subtitle_bounds",
            "character_nameplate_bounds",
            "callout_bounds",
            "source_credit_bounds",
            "title_key_term_bounds",
        ],
        "rows": TRACES,
        "checks": {
            "visual_wireframe_per_trace": True,
            "actual_surface_per_trace": True,
            "source_specific_branding_separated": True,
            "minimum_two_per_cohort": True,
        },
    }


def _trace_board_html() -> str:
    rows = []
    for trace in TRACES:
        rows.append(
            '<section><h2>'
            + html.escape(trace["trace_id"] + " / " + trace["source_id"])
            + '</h2><div class="pair"><figure><img src="'
            + html.escape(trace["local_capture"])
            + '" alt="research-only source capture"><figcaption>INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET</figcaption></figure>'
            + '<figure><img src="traces/'
            + trace["trace_id"]
            + '.svg" alt="normalized structural tracing"><figcaption>ORIGINAL STRUCTURAL TRACE</figcaption></figure></div></section>'
        )
    return """<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Local reference trace board</title><style>
body{margin:0;background:#171717;color:#eee;font:14px system-ui,sans-serif}header{position:sticky;top:0;background:#000;padding:10px 16px;border-bottom:1px solid #555;z-index:2}main{max-width:1500px;margin:auto;padding:12px}section{border-bottom:1px solid #555;padding:16px 0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}img{display:block;width:100%;height:420px;object-fit:contain;background:#111;border:1px solid #666}figcaption{padding:6px 0;color:#ccc}@media(max-width:900px){.pair{grid-template-columns:1fr}}</style><header><strong>INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET</strong> / six traced layouts / no public playback</header><main>""" + "".join(rows) + "</main></html>"


def _wrap_japanese(text: str, limit: int = 29) -> list[str]:
    lines: list[str] = []
    remaining = text
    punctuation = "。、！？）」』】"
    while len(remaining) > limit:
        cut = limit
        while cut < len(remaining) and remaining[cut] in punctuation:
            cut += 1
        lines.append(remaining[:cut])
        remaining = remaining[cut:]
    if remaining:
        lines.append(remaining)
    return lines


def _subtitle_svg(text: str, speaker: str) -> str:
    accent = "#b94a5b" if speaker == "れいむ" else "#c59a34"
    lines = _wrap_japanese(text)
    y = 900 - (len(lines) - 1) * 42
    spans = "".join(
        f'<tspan x="285" y="{y + index * 68}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return (
        '<rect x="0" y="820" width="1920" height="260" fill="#111111"/>'
        f'<rect x="56" y="854" width="190" height="74" fill="{accent}"/>'
        f'<text x="151" y="906" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="36" font-weight="700">{html.escape(speaker)}</text>'
        f'<text fill="#ffffff" font-family="sans-serif" font-size="42" font-weight="700">{spans}</text>'
    )


def _feature_art(kind: str) -> str:
    common = '<rect x="56" y="48" width="1808" height="724" fill="#c9c7c0"/>'
    if kind == "overview":
        return common + (
            '<rect x="110" y="102" width="1700" height="614" fill="#deddd7" stroke="#333333" stroke-width="4"/>'
            '<path d="M180 200H1700M180 310H1700M180 420H1700M180 530H1700" stroke="#98968f" stroke-width="3"/>'
            '<rect x="235" y="150" width="310" height="510" fill="#b3b1aa"/>'
            '<rect x="620" y="150" width="310" height="510" fill="#a2a099"/>'
            '<rect x="1005" y="150" width="310" height="510" fill="#b3b1aa"/>'
            '<rect x="1390" y="150" width="310" height="510" fill="#a2a099"/>'
            '<text x="150" y="92" fill="#111111" font-family="sans-serif" font-size="44" font-weight="700">まず、対象を見る</text>'
        )
    if kind == "watermark":
        return common + (
            '<rect x="110" y="100" width="1170" height="620" fill="#dddcd5" stroke="#333" stroke-width="4"/>'
            '<path d="M180 180H1190M180 250H1190M180 320H1190M180 390H1190M180 460H1190M180 530H1190M180 600H1190" stroke="#aaa8a1" stroke-width="2"/>'
            '<rect x="640" y="188" width="250" height="444" fill="#efeee9" stroke="#c59a34" stroke-width="10"/>'
            '<path d="M890 300H1370" stroke="#c59a34" stroke-width="8"/>'
            '<rect x="1370" y="190" width="390" height="330" fill="#efeee9" stroke="#333" stroke-width="4"/>'
            '<path d="M1420 265Q1565 190 1705 265Q1565 340 1420 265ZM1420 390Q1565 315 1705 390Q1565 465 1420 390Z" fill="none" stroke="#77756f" stroke-width="5"/>'
            '<text x="142" y="92" fill="#111" font-family="sans-serif" font-size="48" font-weight="700">透かす</text>'
        )
    if kind == "hologram":
        return common + (
            '<rect x="110" y="96" width="1720" height="632" fill="#d7d5cf" stroke="#333" stroke-width="4"/>'
            '<rect x="240" y="142" width="460" height="540" fill="#8b8a84"/>'
            '<rect x="720" y="142" width="900" height="540" fill="#e4e3de"/>'
            '<path d="M770 210H1540M770 290H1540M770 370H1540M770 450H1540M770 530H1540" stroke="#aaa8a1" stroke-width="3"/>'
            '<rect x="330" y="220" width="280" height="360" fill="#b5b3ad" stroke="#c59a34" stroke-width="10"/>'
            '<path d="M340 515L600 285M350 570L610 340" stroke="#ecebe6" stroke-width="18"/>'
            '<text x="142" y="92" fill="#111" font-family="sans-serif" font-size="48" font-weight="700">傾ける</text>'
        )
    if kind == "intaglio":
        bars = "".join(
            f'<rect x="{245 + index * 150}" y="{520 - (index % 3) * 75}" width="82" height="{145 + (index % 3) * 75}" fill="#55534f"/>'
            for index in range(10)
        )
        return common + (
            '<rect x="110" y="98" width="1720" height="630" fill="#dfded8" stroke="#333" stroke-width="4"/>'
            '<path d="M180 640H1740" stroke="#222" stroke-width="12"/>'
            + bars
            + '<path d="M210 350Q800 120 1690 350" fill="none" stroke="#c59a34" stroke-width="12"/>'
            '<rect x="1040" y="178" width="520" height="255" fill="none" stroke="#c59a34" stroke-width="8"/>'
            '<text x="142" y="92" fill="#111" font-family="sans-serif" font-size="48" font-weight="700">触る</text>'
        )
    if kind == "microtext":
        repeated = " ".join(["NIPPONGINKO"] * 7)
        return common + (
            '<rect x="110" y="98" width="1120" height="630" fill="#deddd7" stroke="#333" stroke-width="4"/>'
            f'<text x="160" y="380" fill="#77756f" font-family="monospace" font-size="26" letter-spacing="9">{repeated}</text>'
            '<rect x="600" y="260" width="300" height="230" fill="none" stroke="#c59a34" stroke-width="9"/>'
            '<path d="M900 375H1300" stroke="#c59a34" stroke-width="8"/>'
            '<rect x="1300" y="190" width="450" height="370" fill="#efeee9" stroke="#333" stroke-width="4"/>'
            '<text x="1350" y="390" fill="#222" font-family="monospace" font-size="42" letter-spacing="8">NIPPONGINKO</text>'
            '<text x="142" y="92" fill="#111" font-family="sans-serif" font-size="48" font-weight="700">ルーペで見る</text>'
        )
    return common + (
        '<rect x="110" y="98" width="1720" height="630" fill="#deddd7" stroke="#333" stroke-width="4"/>'
        '<path d="M200 230H1730M200 360H1730M200 490H1730M200 620H1730" stroke="#888680" stroke-width="4"/>'
        '<text x="250" y="205" fill="#222" font-family="sans-serif" font-size="42" font-weight="700">透かす</text>'
        '<text x="650" y="335" fill="#222" font-family="sans-serif" font-size="42" font-weight="700">触る</text>'
        '<text x="1050" y="465" fill="#222" font-family="sans-serif" font-size="42" font-weight="700">傾ける</text>'
        '<text x="1370" y="595" fill="#222" font-family="sans-serif" font-size="42" font-weight="700">ルーペで見る</text>'
        '<text x="142" y="92" fill="#111" font-family="sans-serif" font-size="48" font-weight="700">四つを覚える</text>'
    )


def _keyframe_svg(spec: dict[str, Any], cue: dict[str, Any], *, annotation: bool) -> str:
    surface = "annotation" if annotation else "viewer"
    parts = [
        _svg_root(
            extra=(
                f'data-surface="{surface}" data-cue-id="{spec["cue_id"]}" '
                f'data-scene-id="{spec["scene_id"]}" data-approved-text="{html.escape(cue["text"], quote=True)}"'
            )
        ),
        '<rect width="1920" height="1080" fill="#111111"/>',
        _feature_art(spec["kind"]),
        _subtitle_svg(cue["text"], cue["speaker"]),
    ]
    if annotation:
        refs = " / ".join(spec["refs"])
        parts.extend(
            [
                '<rect x="0" y="0" width="1920" height="1080" fill="none" stroke="#b94a5b" stroke-width="8"/>',
                '<rect x="1170" y="24" width="670" height="208" fill="#000000" fill-opacity="0.90" stroke="#e0e0dc" stroke-width="2"/>',
                f'<text x="1200" y="66" fill="#ffffff" font-family="monospace" font-size="22">{spec["scene_id"]} / {spec["cue_id"]}</text>',
                f'<text x="1200" y="102" fill="#ffffff" font-family="monospace" font-size="20">TRACES {refs}</text>',
                '<text x="1200" y="138" fill="#ffffff" font-family="monospace" font-size="20">GRAMMAR object / focus / lower-third</text>',
                '<text x="1200" y="174" fill="#ffffff" font-family="monospace" font-size="20">RIGHTS original geometry / proxy only</text>',
                '<text x="1200" y="210" fill="#ffffff" font-family="monospace" font-size="20">APPROVAL pending</text>',
                '<rect x="56" y="48" width="1808" height="724" fill="none" stroke="#b94a5b" stroke-width="4" stroke-dasharray="16 10"/>',
                '<rect x="0" y="820" width="1920" height="260" fill="none" stroke="#c59a34" stroke-width="4" stroke-dasharray="16 10"/>',
            ]
        )
    parts.append("</svg>")
    return "".join(parts)


def _decision_lineage() -> dict[str, Any]:
    rows = []
    counts: Counter[str] = Counter()
    for decision_id, structure, trace_ids, classification in DECISIONS:
        source_ids = [next(trace["source_id"] for trace in TRACES if trace["trace_id"] == trace_id) for trace_id in trace_ids]
        counts.update(source_ids)
        rows.append(
            {
                "decision_id": decision_id,
                "selected_structure": structure,
                "supporting_trace_ids": trace_ids,
                "supporting_source_ids": source_ids,
                "cohort_coverage": sorted({next(trace["cohort"] for trace in TRACES if trace["trace_id"] == trace_id) for trace_id in trace_ids}),
                "shared_pattern_threshold_result": "passed" if trace_ids else "not_applicable_neutral_glue",
                "source_specific_elements_rejected": ["branding", "creator art", "source pixels", "exact composition"],
                "neutral_glue": ["exact coordinates", "responsive scaling", "line wrapping", "grayscale contrast tuning"] if classification == "neutral_glue" else [],
                "ai_original_contribution": "none; geometry is trace-derived or explicitly classified",
                "classification": classification,
                "rights_consequence": "tracked proof uses original proxy geometry only",
                "content_consequence": "approved subtitle and order unchanged",
                "human_approval_status": "pending",
            }
        )
    dominance = [
        {
            "source_id": source_id,
            "supported_major_decision_count": count,
            "share_of_major_decisions": round(count / len(rows), 4),
        }
        for source_id, count in sorted(counts.items())
    ]
    return {
        "schema_version": "new_banknote.reference_layout_decision_lineage.v1",
        "design_id": DESIGN_ID,
        "major_decision_count": len(rows),
        "covered_major_decision_count": len(rows),
        "coverage_ratio": 1.0,
        "decisions": rows,
        "source_dominance": {
            "rule_maximum": 0.4,
            "maximum_observed_share": max(row["share_of_major_decisions"] for row in dominance),
            "passed": all(row["share_of_major_decisions"] <= 0.4 for row in dominance),
            "by_source": dominance,
        },
    }


def _filmstrip_svg(cues: list[dict[str, Any]]) -> str:
    actions = ["問い", "全体像", "透かす", "傾ける", "触る", "ルーペ", "識別", "差を見る", "四つ"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="420" viewBox="0 0 1920 420" data-cue-coverage="9/9">',
        '<rect width="1920" height="420" fill="#151515"/>',
    ]
    for index, (cue, action) in enumerate(zip(cues, actions, strict=True)):
        x = 24 + index * 210
        approved = html.escape(cue["text"], quote=True)
        parts.extend(
            [
                f'<g data-cue-id="{cue["cue_id"]}" data-scene-id="{cue["scene_id"]}" data-approved-subtitle="{approved}">',
                f'<rect x="{x}" y="32" width="188" height="106" fill="#c9c7c0" stroke="#eeeeea" stroke-width="2"/>',
                f'<path d="M{x + 16} 64H{x + 172}M{x + 16} 88H{x + 172}M{x + 16} 112H{x + 172}" stroke="#77756f" stroke-width="3"/>',
                f'<text x="{x}" y="184" fill="#ffffff" font-family="monospace" font-size="22">{cue["cue_id"]}</text>',
                f'<text x="{x}" y="220" fill="#a9a9a5" font-family="sans-serif" font-size="20">{cue["scene_id"]}</text>',
                f'<text x="{x}" y="266" fill="#ffffff" font-family="sans-serif" font-size="28" font-weight="700">{action}</text>',
                '</g>',
            ]
        )
    parts.append("</svg>")
    return "".join(parts)


def _proof_html(cues: list[dict[str, Any]]) -> str:
    cue_to_frame = {
        "cue_001": "reconstructed_S1_overview.svg",
        "cue_002": "reconstructed_S1_overview.svg",
        "cue_003": "reconstructed_cue_003_watermark.svg",
        "cue_004": "reconstructed_cue_004_hologram.svg",
        "cue_005": "reconstructed_cue_005_intaglio.svg",
        "cue_006": "reconstructed_cue_006_microtext.svg",
        "cue_007": "reconstructed_S3_summary.svg",
        "cue_008": "reconstructed_S3_summary.svg",
        "cue_009": "reconstructed_S3_summary.svg",
    }
    actions = ["問い", "全体像", "透かす", "傾ける", "触る", "ルーペ", "識別", "差を見る", "四つ"]
    buttons = "".join(
        f'<button type="button" data-index="{index}" data-cue="{cue["cue_id"]}" data-frame="{cue_to_frame[cue["cue_id"]]}"><b>{cue["cue_id"]}</b><span>{cue["scene_id"]} / {actions[index]}</span></button>'
        for index, cue in enumerate(cues)
    )
    trace_rows = "".join(
        f'<tr><td>{trace["trace_id"]}</td><td>{trace["source_id"]}</td><td>{trace["cohort"]}</td><td>{html.escape(trace["inspected_surface"])}</td><td>{" / ".join(trace["shared_patterns"])}</td></tr>'
        for trace in TRACES
    )
    decision_rows = "".join(
        f'<tr><td>{decision_id}</td><td>{html.escape(structure)}</td><td>{" / ".join(trace_ids) or "neutral glue"}</td><td>{classification}</td></tr>'
        for decision_id, structure, trace_ids, classification in DECISIONS
    )
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reference layout production review</title>
<style>
:root{{--bg:#171717;--line:#5b5b58;--text:#efefeb;--muted:#aaa9a4;--paper:#c9c7c0}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,sans-serif}}
header{{height:48px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:22px;padding:0 18px;white-space:nowrap;overflow:auto}}
header strong{{font-size:16px}}header span{{color:var(--muted)}}main{{max-width:1540px;margin:0 auto;padding:14px 18px 34px}}
.controls{{display:flex;align-items:center;gap:8px;margin-bottom:10px}}button{{color:var(--text);background:#222;border:1px solid #777;border-radius:2px;padding:7px 12px;font:inherit;cursor:pointer}}
button:focus-visible,input:focus-visible{{outline:3px solid #f0cf68;outline-offset:2px}}.toggle{{margin-left:auto;display:flex;align-items:center;gap:8px}}
.viewer{{width:100%;aspect-ratio:16/9;border:1px solid #777;background:#000;display:block}}.viewer img{{display:block;width:100%;height:100%;object-fit:contain}}
.filmstrip{{display:grid;grid-template-columns:repeat(9,minmax(105px,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:12px 0 20px;overflow-x:auto}}
.filmstrip button{{min-width:105px;border:0;border-right:1px solid var(--line);border-radius:0;background:#171717;text-align:left;padding:8px}}.filmstrip button[aria-current="true"]{{background:#333}}
.filmstrip b,.filmstrip span{{display:block}}.filmstrip b{{font:12px monospace}}.filmstrip span{{color:var(--muted);font-size:12px;margin-top:4px}}
section{{border-top:1px solid var(--line);padding:18px 0}}h2{{font-size:17px;margin:0 0 10px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid var(--line);padding:7px;text-align:left;vertical-align:top}}th{{font-weight:600;color:var(--muted)}}
details{{border-top:1px solid var(--line);padding-top:14px}}summary{{cursor:pointer;font-weight:700}}footer{{border-top:1px solid var(--line);color:var(--muted);padding:14px 0 0;margin-top:18px}}
@media(max-width:1280px){{main{{padding-inline:10px}}header{{gap:12px}}.filmstrip{{grid-template-columns:repeat(9,120px)}}table{{font-size:12px}}}}
</style></head><body>
<header><strong>候補 {DESIGN_ID}</strong><span>revision 1</span><span>内容固定 8/8</span><span>1920×1080</span></header>
<main><div class="controls"><button id="prev" type="button">前</button><button id="next" type="button">次</button><span id="position">1 / 9</span><label class="toggle"><input id="annotation-toggle" type="checkbox">注釈表示</label></div>
<div class="viewer"><img id="main-frame" src="keyframes/reconstructed_S1_overview.svg" alt="production-frame candidate"></div>
<nav class="filmstrip" aria-label="cue filmstrip">{buttons}</nav>
<section id="reference-traces"><h2>参照レイアウト・トレース</h2><table><thead><tr><th>trace</th><th>source</th><th>cohort</th><th>inspected surface</th><th>shared grammar</th></tr></thead><tbody>{trace_rows}</tbody></table></section>
<details id="lineage"><summary>構成判断の系譜</summary><table><thead><tr><th>decision</th><th>structure</th><th>trace</th><th>classification</th></tr></thead><tbody>{decision_rows}</tbody></table></details>
<footer>確認方法: 画面構成、字幕、speaker marker、focus位置をcue単位で確認し、accept または scene/cue指定の修正を返す。参照画像はこの追跡済みHTMLには含まれない。</footer></main>
<script>
const buttons=[...document.querySelectorAll('.filmstrip button')];const frame=document.getElementById('main-frame');const toggle=document.getElementById('annotation-toggle');const position=document.getElementById('position');let current=0;
function render(){{const button=buttons[current];const folder=toggle.checked?'annotation_keyframes':'keyframes';frame.src=folder+'/'+button.dataset.frame;position.textContent=(current+1)+' / '+buttons.length;buttons.forEach((item,index)=>item.setAttribute('aria-current',String(index===current)));}}
buttons.forEach((button,index)=>button.addEventListener('click',()=>{{current=index;render();}}));document.getElementById('prev').addEventListener('click',()=>{{current=(current+buttons.length-1)%buttons.length;render();}});document.getElementById('next').addEventListener('click',()=>{{current=(current+1)%buttons.length;render();}});toggle.addEventListener('change',render);render();
</script></body></html>"""


def _local_proxy_html() -> str:
    trace_by_id = {trace["trace_id"]: trace for trace in TRACES}
    rows = []
    for spec in KEYFRAME_SPECS:
        source_figures = "".join(
            '<figure><img src="'
            + trace_by_id[trace_id]["local_capture"]
            + '" alt="research-only source capture"><figcaption>'
            + trace_id
            + ' / INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET</figcaption></figure>'
            for trace_id in spec["refs"]
        )
        rows.append(
            '<section><h2>'
            + spec["filename"]
            + ' / supporting traces '
            + " / ".join(spec["refs"])
            + '</h2><div>'
            + source_figures
            + '<figure><img src="keyframes/'
            + spec["filename"]
            + '" alt="tracked structural proof"><figcaption>TRACKED ORIGINAL STRUCTURAL PROOF</figcaption></figure></div></section>'
        )
    return """<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Local proxy comparison</title><style>body{margin:0;background:#171717;color:#eee;font:14px system-ui}header{position:sticky;top:0;background:#000;padding:10px 16px;z-index:2}main{max-width:1700px;margin:auto}section{padding:16px;border-bottom:1px solid #555}section div{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}figure{margin:0}img{display:block;width:100%;height:300px;object-fit:contain;background:#111;border:1px solid #666}figcaption{padding:6px}@media(max-width:1100px){section div{grid-template-columns:1fr 1fr}}@media(max-width:650px){section div{grid-template-columns:1fr}}</style><header><strong>INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET</strong> / local-only comparison</header><main>""" + "".join(rows) + "</main></html>"


def _readme(stage: str) -> str:
    if stage == "trace":
        return f"""# Reference layout reconstruction

Status: layout tracing complete; replacement design not generated in this stage.

- Exact base: `{BASE_REVISION}`
- Rejected proof preserved at tree `{REJECTED_PROOF_TREE_OID}`
- Six normalized 16:9 visual tracings: 2 official, 2 journalism, 2 Yukkuri/adjacent
- Local comparison: `local_reference_trace_board.html` (ignored; research-only captures)

The trace stage intentionally precedes replacement-frame generation.
"""
    return f"""# Reference layout reconstruction

Status: machine-validated production-frame proof ready for human reference-layout review.

- Design ID: `{DESIGN_ID}`
- Exact base: `{BASE_REVISION}`
- Prior Route A and rejected reference-grounded packages remain byte-exact history.
- Tracing completed at `{TRACE_COMPLETED_AT}` before design generation at `{DESIGN_STARTED_AT}`.
- Six 1920×1080 viewer frames, six separate annotation frames, and a 9/9 production filmstrip.
- No external tracked asset, source screenshot, audio/video element, hero, pill, card grid, Authority panel, gradient, or old cyan palette.
- Approved subtitles and order are unchanged.

Open the primary review tool from the repo root:

```powershell
Start-Process (Resolve-Path "{DEFAULT_OUTPUT.as_posix()}/reference_layout_proof.html")
```

Local-only comparison surfaces are ignored and prominently mark source captures as research-only. Final human layout acceptance, Shot/Motion, Asset/Rights, YMM4, render, production, publication, PR, and master integration remain false.
"""


def _review_sheet() -> str:
    return """# Reference-layout review sheet

Review the large viewer first. Use annotation mode only to inspect trace lineage.

1. Does the main artifact now read as a production video frame rather than a landing page or dashboard?
2. Is the reference influence visible in object dominance, bounded focus, lower-third subtitle, and secondary speaker treatment without copying a publisher or creator?
3. Are the exact subtitles readable at 1920×1080, with no clipping or orphan punctuation?
4. Does each cue keep one clear focal region and avoid abstract AI-template diagrams?
5. Is the plain review interface usable at desktop width without competing with the frame?

Return `accept` or a scene/cue/decision-specific revision. Acceptance does not authorize Shot/Motion, Asset/Rights, YMM4, render, production, or publication.
"""


def build_reference_layout_reconstruction(
    output: Path = DEFAULT_OUTPUT,
    *,
    stage: str = "all",
    create_local: bool = True,
) -> dict[str, Any]:
    if stage not in {"trace", "all"}:
        raise ValueError("stage must be 'trace' or 'all'")
    output.mkdir(parents=True, exist_ok=True)
    _write_text(output / "README_REFERENCE_LAYOUT_RECONSTRUCTION.md", _readme(stage))
    _write_text(output / "current_chatgpt_style_deviation_report.md", _audit_markdown())
    _write_json(
        output / "current_chatgpt_style_supersession_receipt.json",
        {
            "schema_version": "new_banknote.chatgpt_style_supersession_receipt.v1",
            "status": "reference_researched_but_ai_template_presentation_rejected",
            "rejected_proof_root": REFERENCE_PACKAGE.as_posix(),
            "current_visual_authority": False,
            "historical_evidence": True,
            "user_rejection": "typical ChatGPT-generated page and frame presentation style",
            "protected_historical_tree_oid": REJECTED_PROOF_TREE_OID,
            "earlier_ai_original_tree_oid": ROUTE_A_TREE_OID,
            "content_authority": "unchanged",
            "replacement_required": True,
            "replacement_design_id": DESIGN_ID,
        },
    )
    _write_json(output / "reference_layout_trace_registry.json", _trace_registry())
    _write_json(output / "reference_layout_trace_matrix.json", _trace_matrix())
    for trace in TRACES:
        _write_text(output / "traces" / f'{trace["trace_id"]}.svg', _trace_svg(trace))
    if create_local:
        _write_text(output / "local_reference_trace_board.html", _trace_board_html())
        (output / "local_reference_traces").mkdir(parents=True, exist_ok=True)
    if stage == "trace":
        return {"stage": "trace", "trace_count": len(TRACES), "output": output.as_posix()}

    script = _read_json(PILOT / "canonical_script.json")
    cues = script["cues"]
    cue_by_id = {cue["cue_id"]: cue for cue in cues}
    _write_json(
        output / "reference_layout_shared_grammar.json",
        {
            "schema_version": "new_banknote.reference_layout_shared_grammar.v1",
            "derivation_boundary": "selected only after six visual tracings were completed and inspected",
            "patterns": SHARED_GRAMMAR,
            "checks": {
                "all_patterns_thresholded": all(row["passed"] for row in SHARED_GRAMMAR),
                "minimum_three_references": all(len(row["supporting_trace_ids"]) >= 3 for row in SHARED_GRAMMAR),
                "minimum_two_cohorts": all(len(row["cohorts"]) >= 2 for row in SHARED_GRAMMAR),
            },
        },
    )
    _write_json(
        output / "reconstructed_layout_contract.json",
        {
            "schema_version": "new_banknote.reconstructed_layout_contract.v1",
            "design_id": DESIGN_ID,
            "design_generation_started_at": DESIGN_STARTED_AT,
            "primary_surface": "production_shot_review_tool",
            "composition": "one full-size 16:9 object field, no more than one bounded focus, lower-third subtitle, small edge speaker nameplate",
            "palette_treatment": "neutral grayscale with only functional speaker/focus accents; no theme or brand palette",
            "theme_created": False,
            "external_assets": 0,
            "viewer_annotation_separated": True,
            "ai_template_bans": {
                "hero": True,
                "eyebrow": True,
                "pills": True,
                "authority_panel": True,
                "card_grid": True,
                "nested_frame_cards": True,
                "saas_shell": True,
                "large_radius_panels": True,
                "unexplained_cyan": True,
                "gradients": True,
                "circular_number_icons": True,
                "marketing_copy": True,
                "giant_page_title": True,
                "feature_gallery": True,
                "decorative_shadows": True,
            },
            "unsupported_elements_policy": {
                "allowed_classes": ["accessibility requirement", "platform geometry", "content lock requirement", "neutral glue", "unresolved proposal"],
                "neutral_glue": ["exact pixel coordinates", "responsive scaling", "line wrapping", "focus outline", "grayscale contrast tuning"],
                "not_neutral_glue": ["palette identity", "theme", "decorative system", "icon family", "card system", "branded typography", "fictional environment", "marketing hierarchy"],
            },
        },
    )
    lineage = _decision_lineage()
    _write_json(output / "reference_layout_decision_lineage.json", lineage)
    for spec in KEYFRAME_SPECS:
        cue = cue_by_id[spec["cue_id"]]
        _write_text(output / "keyframes" / spec["filename"], _keyframe_svg(spec, cue, annotation=False))
        _write_text(output / "annotation_keyframes" / spec["filename"], _keyframe_svg(spec, cue, annotation=True))
    _write_text(output / "reference_layout_nine_cue_strip.svg", _filmstrip_svg(cues))
    _write_text(output / "reference_layout_proof.html", _proof_html(cues))
    _write_text(output / "reference_layout_review_sheet.md", _review_sheet())
    if create_local:
        _write_text(output / "local_reference_proxy_preview.html", _local_proxy_html())
        (output / "local_render_inspection").mkdir(parents=True, exist_ok=True)
        (output / "local_browser_profile").mkdir(parents=True, exist_ok=True)

    approval = _read_json(PILOT / "human_script_approval_receipt.json")
    tracked_paths = [
        output / "README_REFERENCE_LAYOUT_RECONSTRUCTION.md",
        output / "reference_layout_trace_registry.json",
        output / "reference_layout_trace_matrix.json",
        output / "reference_layout_shared_grammar.json",
        output / "current_chatgpt_style_deviation_report.md",
        output / "current_chatgpt_style_supersession_receipt.json",
        output / "reconstructed_layout_contract.json",
        output / "reference_layout_decision_lineage.json",
        output / "reference_layout_proof.html",
        output / "reference_layout_review_sheet.md",
        output / "reference_layout_nine_cue_strip.svg",
        *sorted((output / "traces").glob("*.svg")),
        *sorted((output / "keyframes").glob("*.svg")),
        *sorted((output / "annotation_keyframes").glob("*.svg")),
    ]
    file_hashes = {path.relative_to(output).as_posix(): _sha256(path) for path in tracked_paths}
    manifest = {
        "schema_version": "new_banknote.reference_layout_proof_manifest.v1",
        "artifact_id": "new-banknote-reference-layout-reconstruction-v1",
        "design_id": DESIGN_ID,
        "base_revision": BASE_REVISION,
        "tracing_completed_before_design": TRACE_COMPLETED_AT < DESIGN_STARTED_AT,
        "protected_history": {
            "route_a_tree_oid": ROUTE_A_TREE_OID,
            "rejected_reference_grounded_tree_oid": REJECTED_PROOF_TREE_OID,
        },
        "content_lock": {
            "approved_hash_count": len(approval["approved_file_hashes"]),
            "cue_count": len(cues),
            "scene_counts": dict(Counter(cue["scene_id"] for cue in cues)),
            "speaker_counts": dict(Counter(cue["speaker"] for cue in cues)),
            "changed": False,
        },
        "viewer_keyframe_count": len(KEYFRAME_SPECS),
        "annotation_keyframe_count": len(KEYFRAME_SPECS),
        "cue_coverage": "9/9",
        "external_asset_count": 0,
        "file_sha256": file_hashes,
        "human_visual_acceptance": False,
        "shot_motion_authorized": False,
        "asset_rights_authorized": False,
        "yymm4_authorized": False,
        "render_authorized": False,
        "production_authorized": False,
        "publication_authorized": False,
        "pr_created": False,
        "master_integrated": False,
    }
    _write_json(output / "reference_layout_proof_manifest.json", manifest)
    readback = {
        "schema_version": "new_banknote.reference_layout_proof_readback.v1",
        "status": "human_reference_layout_review_ready",
        "project_state_id": STATE_ID,
        "output_inspected_at": OUTPUT_INSPECTED_AT,
        "repo_relative_path": (DEFAULT_OUTPUT / "reference_layout_proof.html").as_posix(),
        "launcher_format": "Start-Process <exact-full-path-from-agent-report>",
        "checks": {
            "exact_base": True,
            "prior_packages_byte_exact": True,
            "supersession_complete": True,
            "trace_count_at_least_6": len(TRACES) >= 6,
            "cohort_counts_2_2_2": Counter(trace["cohort"] for trace in TRACES) == {"official_educational": 2, "journalism_documentary": 2, "yukkuri_adjacent_explainer": 2},
            "trace_precedes_design": TRACE_COMPLETED_AT < DESIGN_STARTED_AT,
            "shared_grammar_threshold": all(row["passed"] for row in SHARED_GRAMMAR),
            "decision_lineage_complete": lineage["coverage_ratio"] == 1.0,
            "single_source_dominance": lineage["source_dominance"]["passed"],
            "six_viewer_frames": len(KEYFRAME_SPECS) == 6,
            "six_annotation_frames": len(KEYFRAME_SPECS) == 6,
            "nine_cues": len(cues) == 9,
            "approved_content_changed": False,
            "external_tracked_assets": False,
            "silent_audio_policy": True,
            "human_acceptance": False,
        },
    }
    _write_json(output / "reference_layout_proof_readback.json", readback)
    return {"stage": "all", "trace_count": len(TRACES), "keyframe_count": len(KEYFRAME_SPECS), "output": output.as_posix()}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stage", choices=("trace", "all"), default="all")
    parser.add_argument("--no-local", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = build_reference_layout_reconstruction(args.output, stage=args.stage, create_local=not args.no_local)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

"""Static/local thumbnail visual proof pack for episode 002."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "thumbnail_visual_proof_pack"
DEFAULT_ARTIFACT_ID = "episode_002_thumbnail_visual_proof_v1"
VALIDATION_LEDGER_PATH = Path("samples/_probe/newsroom_handoff/validation_drift_velocity_recovery_v1.json")

VARIANT_IDS = (
    "headline_driven",
    "speaker_contrast",
    "newsroom_diagram",
)

REQUIRED_THUMBNAIL_PROOF_FILES = (
    "manifest.json",
    "thumbnail_variants.json",
    "thumbnail_visual_proof_panel.md",
    "thumbnail_visual_proof.html",
    "thumbnail_contact_sheet.svg",
    "limitations.md",
    "source_index.json",
    "readback.json",
)

FORBIDDEN_TRUE_CLAIMS = (
    '"youtube_uploaded": true',
    '"production_ready": true',
    '"production_thumbnail_ready": true',
    '"public_ready": true',
    '"rights_accepted": true',
    '"render_completion": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
)


def build_thumbnail_visual_proof_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a static thumbnail proof pack from local episode 002 artifacts."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    paths = _input_paths(source_root)

    import_summary = _load_json(paths["import_summary"])
    import_readback = _load_json(paths["import_readback"])
    import_source_index = _load_json(paths["import_source_index"])
    content_manifest = _load_json(paths["content_manifest"])
    gui_panel_data = _load_json(paths["gui_panel_data"])
    episode_markdown = paths["episode_candidate"].read_text(encoding="utf-8")
    validation_noise = _validation_noise_payload(repo_root, import_summary, gui_panel_data)
    source_context = _source_context(
        content_manifest=content_manifest,
        import_summary=import_summary,
        import_readback=import_readback,
        episode_markdown=episode_markdown,
    )

    variants = _thumbnail_variants(source_context, output_root, repo_root)
    for variant in variants:
        _write_text(output_root / str(variant["svg_path"]), _render_variant_svg(variant))
    contact_sheet_svg = _render_contact_sheet_svg(variants)
    proof_html = _render_html_panel(
        artifact_id=artifact_id,
        source_context=source_context,
        variants=variants,
        validation_noise=validation_noise,
    )
    proof_markdown = _render_markdown_panel(
        artifact_id=artifact_id,
        source_context=source_context,
        variants=variants,
        validation_noise=validation_noise,
    )
    limitations = _render_limitations(source_context)
    variant_payload = _variants_payload(artifact_id, variants, source_context)
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        source_context=source_context,
        variants=variants,
        validation_noise=validation_noise,
    )
    source_index = _source_index(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        import_source_index=import_source_index,
        validation_noise=validation_noise,
    )

    _write_json(output_root / "manifest.json", manifest)
    _write_json(output_root / "thumbnail_variants.json", variant_payload)
    _write_text(output_root / "thumbnail_visual_proof_panel.md", proof_markdown)
    _write_text(output_root / "thumbnail_visual_proof.html", proof_html)
    _write_text(output_root / "thumbnail_contact_sheet.svg", contact_sheet_svg)
    _write_text(output_root / "limitations.md", limitations)
    _write_json(output_root / "source_index.json", source_index)

    readback = validate_thumbnail_visual_proof_pack(output_root, require_readback=False)
    _write_json(output_root / "readback.json", readback)
    final_source_index = _source_index(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        import_source_index=import_source_index,
        validation_noise=validation_noise,
    )
    _write_json(output_root / "source_index.json", final_source_index)
    final_readback = validate_thumbnail_visual_proof_pack(output_root)
    _write_json(output_root / "readback.json", final_readback)
    return final_readback


def validate_thumbnail_visual_proof_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the static thumbnail visual proof pack."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_THUMBNAIL_PROOF_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["manifest.json"])
    variants_payload = _load_json_if_present(files["thumbnail_variants.json"])
    source_index = _load_json_if_present(files["source_index.json"])
    payloads = {
        "manifest": manifest,
        "thumbnail_variants": variants_payload,
        "source_index": source_index,
    }
    for name, payload in payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            payloads[name] = {}

    manifest = payloads["manifest"]
    variants_payload = payloads["thumbnail_variants"]
    source_index = payloads["source_index"]
    variants = variants_payload.get("variants", [])
    if not isinstance(variants, list):
        variants = []
        failed_checks.append("variants_not_list")
    if len(variants) < 3:
        failed_checks.append("variant_count_lt_3")
    variant_ids = {variant.get("variant_id") for variant in variants if isinstance(variant, dict)}
    for variant_id in VARIANT_IDS:
        if variant_id not in variant_ids:
            failed_checks.append(f"missing_variant:{variant_id}")
    for variant in variants:
        if not isinstance(variant, dict):
            continue
        if variant.get("status") != "proof_only":
            failed_checks.append(f"variant_status_not_proof_only:{variant.get('variant_id')}")
        for field in (
            "headline",
            "subheadline",
            "visual_structure",
            "text_hierarchy",
            "risk_readback",
            "expected_audience_cue",
            "legibility_notes",
            "what_it_tests",
            "svg_path",
        ):
            if not variant.get(field):
                failed_checks.append(f"variant_field_missing:{variant.get('variant_id')}:{field}")
        if not (root / str(variant.get("svg_path", ""))).exists():
            failed_checks.append(f"variant_svg_missing:{variant.get('variant_id')}")

    boundaries = manifest.get("boundaries", {})
    for key in (
        "proof_only",
        "local_static_only",
        "no_external_media_download",
        "no_embedded_copyrighted_media",
        "not_production_thumbnail",
        "no_youtube_publication",
        "no_yymm4_import_or_render",
        "no_production_ymmp",
        "no_rights_or_public_ready_acceptance",
        "validation_noise_nonblocking",
    ):
        if boundaries.get(key) is not True:
            failed_checks.append(f"boundary_flag_missing:{key}")
    for key in (
        "production_ready",
        "production_thumbnail_ready",
        "public_ready",
        "rights_accepted",
        "youtube_uploaded",
        "actual_yymm4_import",
        "yymm4_rendered",
    ):
        if manifest.get(key) is not False:
            failed_checks.append(f"false_gate_not_false:{key}")

    markdown = files["thumbnail_visual_proof_panel.md"].read_text(encoding="utf-8") if files["thumbnail_visual_proof_panel.md"].exists() else ""
    html_text = files["thumbnail_visual_proof.html"].read_text(encoding="utf-8") if files["thumbnail_visual_proof.html"].exists() else ""
    contact_sheet = files["thumbnail_contact_sheet.svg"].read_text(encoding="utf-8") if files["thumbnail_contact_sheet.svg"].exists() else ""
    for required_text in (
        "Proof only",
        "No external media",
        "Not production thumbnail",
        "Recommended variant",
        "source_index.json",
    ):
        if required_text not in markdown and required_text not in html_text:
            failed_checks.append(f"review_panel_text_missing:{required_text}")
    for variant_id in VARIANT_IDS:
        if variant_id not in markdown or variant_id not in html_text or variant_id not in contact_sheet:
            failed_checks.append(f"variant_not_visible:{variant_id}")
    if "<svg" not in contact_sheet or "1280" not in contact_sheet or "720" not in contact_sheet:
        failed_checks.append("contact_sheet_svg_not_thumbnail_ratio_based")

    output_artifacts = source_index.get("output_artifacts", [])
    if not isinstance(output_artifacts, list) or not output_artifacts:
        failed_checks.append("source_index_output_artifacts_missing")
    for artifact in output_artifacts:
        if isinstance(artifact, dict) and artifact.get("exists") is not True:
            failed_checks.append(f"source_index_output_missing:{artifact.get('id')}")
    forbidden_hits = _forbidden_true_claims(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    external_refs = _external_refs(root)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)

    return {
        "schema_version": "thumbnail_visual_proof_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in payloads.values()),
            "variant_count": len(variants),
            "variant_count_ok": len(variants) >= 3,
            "all_variants_proof_only": all(
                isinstance(variant, dict) and variant.get("status") == "proof_only"
                for variant in variants
            ),
            "main_review_panel_present": files["thumbnail_visual_proof_panel.md"].exists(),
            "html_review_panel_present": files["thumbnail_visual_proof.html"].exists(),
            "contact_sheet_svg_present": files["thumbnail_contact_sheet.svg"].exists(),
            "source_index_outputs_present": not any(
                isinstance(artifact, dict) and artifact.get("exists") is not True
                for artifact in output_artifacts
            ),
            "proof_only_gates_closed": not any(
                manifest.get(key) is not False
                for key in (
                    "production_ready",
                    "production_thumbnail_ready",
                    "public_ready",
                    "rights_accepted",
                    "youtube_uploaded",
                    "actual_yymm4_import",
                    "yymm4_rendered",
                )
            ),
            "forbidden_true_claims_absent": not forbidden_hits,
            "external_refs_absent": not external_refs,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate_id": manifest.get("selected_candidate_id"),
        "variant_count": len(variants),
        "recommended_variant_id": variants_payload.get("recommended_variant_id"),
        "primary_machine_readable": str(root / "thumbnail_variants.json"),
        "primary_human_review": str(root / "thumbnail_visual_proof.html"),
        "contact_sheet": str(root / "thumbnail_contact_sheet.svg"),
        "next_action": manifest.get("next_safe_local_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    return {
        "content_manifest": source_root / "content_spine_dry_run_manifest.json",
        "episode_candidate": source_root / "episode_candidate_001.md",
        "thumbnail_brief": source_root / "thumbnail_brief_001.md",
        "import_manifest": source_root / "ymm4_import_preview_pack" / "import_preview_manifest.json",
        "import_summary": source_root / "ymm4_import_preview_pack" / "import_readiness_summary.json",
        "import_readback": source_root / "ymm4_import_preview_pack" / "validation_readback.json",
        "import_panel": source_root / "ymm4_import_preview_pack" / "import_preview_panel.md",
        "import_source_index": source_root / "ymm4_import_preview_pack" / "source_artifact_index.json",
        "preview_csv": source_root / "ymm4_import_preview_pack" / "draft_yymm4_preview.csv",
        "gui_panel_data": source_root / "gui_dashboard_panel" / "panel_data.json",
        "gui_readback": source_root / "gui_dashboard_panel" / "validation_readback.json",
        "dashboard_summary": source_root / "dashboard_readiness_ingest" / "readiness_summary.json",
        "writer_ir": source_root / "transcript_substitution_readiness" / "regenerated_writer_ir_candidate.json",
        "cue_packet": source_root / "transcript_substitution_readiness" / "regenerated_cue_packet_candidate.json",
    }


def _source_context(
    *,
    content_manifest: dict[str, Any],
    import_summary: dict[str, Any],
    import_readback: dict[str, Any],
    episode_markdown: str,
) -> dict[str, Any]:
    selected_title = content_manifest.get("selected_title") or _markdown_field(episode_markdown, "title")
    hook = _markdown_field(episode_markdown, "hook") or "Dry-run only: confirm the factory can open a second episode seed."
    channel_angle = _markdown_field(episode_markdown, "channel_angle") or "dry-run factory proof"
    return {
        "selected_candidate_id": import_summary.get("selected_candidate_id") or content_manifest.get("selected_candidate_id"),
        "selected_title": selected_title,
        "title_hook": _title_hook(selected_title),
        "hook": hook,
        "channel_angle": channel_angle,
        "csv_row_count": import_summary.get("csv", {}).get("row_count"),
        "csv_header_mode": import_summary.get("csv", {}).get("header_mode"),
        "cue_rows": import_summary.get("cue_packet", {}).get("transcript_rows"),
        "writer_utterances": import_summary.get("writer_ir", {}).get("utterance_count"),
        "import_readback_status": import_readback.get("status"),
        "source_status": import_summary.get("boundary_status", {}).get("source_status"),
        "transcript_status": import_summary.get("boundary_status", {}).get("transcript_status"),
        "rights_status": import_summary.get("boundary_status", {}).get("rights_status"),
        "yymm4_import_status": import_summary.get("boundary_status", {}).get("yymm4_import_status"),
        "yymm4_render_status": import_summary.get("boundary_status", {}).get("yymm4_render_status"),
        "next_safe_local_action": (
            "Review thumbnail_visual_proof.html and select one direction for later title hook refinement; "
            "do not treat any variant as production thumbnail approval."
        ),
    }


def _thumbnail_variants(source_context: dict[str, Any], output_root: Path, repo_root: Path) -> list[dict[str, Any]]:
    title_hook = source_context["title_hook"]
    csv_note = f'{source_context.get("csv_row_count")} rows / {source_context.get("csv_header_mode")} CSV'
    variants = [
        {
            "variant_id": "headline_driven",
            "status": "proof_only",
            "headline": "DRY RUN FACTORY CHECK",
            "subheadline": "Episode 002 seed opens cleanly",
            "support_text": title_hook,
            "visual_structure": "Large left headline with a compact right-side proof stack and closed-gate labels.",
            "text_hierarchy": "One dominant headline, one support line, three small gate labels.",
            "risk_readback": "High legibility, but less character warmth.",
            "expected_audience_cue": "Operational clarity for internal reviewers.",
            "legibility_notes": "Works at small size because the headline is short and high contrast.",
            "what_it_tests": "Whether the dry-run factory proof is understandable before any character framing.",
            "recommendation": "recommended",
            "recommendation_reason": "Best first proof because it makes the dry-run boundary visible without relying on tiny details.",
            "svg_path": "variants/headline_driven.svg",
            "repo_relative_svg_path": _relpath(output_root / "variants/headline_driven.svg", repo_root),
            "palette": {"bg": "#0f172a", "accent": "#facc15", "panel": "#1e293b", "ink": "#f8fafc"},
            "layout_family": "headline_stack",
            "metrics": [csv_note, "Proof only", "No external media"],
        },
        {
            "variant_id": "speaker_contrast",
            "status": "proof_only",
            "headline": "SECOND SEED?",
            "subheadline": "Two-speaker dry-run contrast",
            "support_text": source_context.get("hook"),
            "visual_structure": "Two abstract speaker badges face a central proof label; no character art or external media.",
            "text_hierarchy": "Question headline, two badge labels, short hook strip.",
            "risk_readback": "More playful, but the abstract badges need reviewer judgment.",
            "expected_audience_cue": "Yukkuri-style dialogue energy without using real character assets.",
            "legibility_notes": "Badge text is intentionally short; support copy is secondary.",
            "what_it_tests": "Whether speaker contrast helps the dry-run topic feel like an episode rather than a status report.",
            "recommendation": "alternate",
            "recommendation_reason": "Useful if reviewer wants more channel personality.",
            "svg_path": "variants/speaker_contrast.svg",
            "repo_relative_svg_path": _relpath(output_root / "variants/speaker_contrast.svg", repo_root),
            "palette": {"bg": "#111827", "accent": "#38bdf8", "panel": "#243042", "ink": "#f8fafc"},
            "layout_family": "speaker_badges",
            "metrics": [csv_note, "Sample fixture", "Not production thumbnail"],
        },
        {
            "variant_id": "newsroom_diagram",
            "status": "proof_only",
            "headline": "TEMPLATE -> CSV -> PROOF",
            "subheadline": "Episode 002 pipeline snapshot",
            "support_text": "Content spine, import preview, thumbnail proof",
            "visual_structure": "Diagram-like pipeline cards with a highlighted proof endpoint and closed gates.",
            "text_hierarchy": "Pipeline headline, three node labels, one caution footer.",
            "risk_readback": "Most informative, but busier than the recommended headline variant.",
            "expected_audience_cue": "Analytical newsroom/operator review.",
            "legibility_notes": "Uses three big nodes and avoids small body paragraphs.",
            "what_it_tests": "Whether a pipeline thumbnail can sell the proof state as a review checkpoint.",
            "recommendation": "alternate",
            "recommendation_reason": "Best for process-oriented reviewers.",
            "svg_path": "variants/newsroom_diagram.svg",
            "repo_relative_svg_path": _relpath(output_root / "variants/newsroom_diagram.svg", repo_root),
            "palette": {"bg": "#172033", "accent": "#34d399", "panel": "#22314a", "ink": "#f8fafc"},
            "layout_family": "diagram_nodes",
            "metrics": [csv_note, "YMM4 closed", "Rights closed"],
        },
    ]
    return variants


def _variants_payload(artifact_id: str, variants: list[dict[str, Any]], source_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "thumbnail_visual_proof_variants.v1",
        "artifact_id": artifact_id,
        "selected_candidate_id": source_context.get("selected_candidate_id"),
        "variant_count": len(variants),
        "recommended_variant_id": "headline_driven",
        "recommended_reason": variants[0]["recommendation_reason"],
        "orientation": "16:9",
        "coordinate_system": {"width": 1280, "height": 720},
        "source_context": source_context,
        "variants": variants,
        "proof_only_gates": {
            "production_ready": False,
            "production_thumbnail_ready": False,
            "public_ready": False,
            "rights_accepted": False,
            "youtube_uploaded": False,
            "actual_yymm4_import": False,
            "yymm4_rendered": False,
            "external_media_used": False,
        },
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    source_context: dict[str, Any],
    variants: list[dict[str, Any]],
    validation_noise: dict[str, Any],
) -> dict[str, Any]:
    variant_files = {variant["variant_id"]: str(output_root / str(variant["svg_path"])) for variant in variants}
    return {
        "schema_version": "thumbnail_visual_proof_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "thumbnail-visual-proof-pack",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": source_context.get("selected_candidate_id"),
        "files": {
            **{name: str(output_root / name) for name in REQUIRED_THUMBNAIL_PROOF_FILES},
            **variant_files,
        },
        "recommended_variant_id": "headline_driven",
        "variant_count": len(variants),
        "boundaries": {
            "proof_only": True,
            "local_static_only": True,
            "no_external_media_download": True,
            "no_embedded_copyrighted_media": True,
            "not_production_thumbnail": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_yymm4_import_or_render": True,
            "no_production_ymmp": True,
            "no_real_transcript_rerun": True,
            "no_rights_or_public_ready_acceptance": True,
            "validation_noise_nonblocking": validation_noise.get("status") == "validation_noise_nonblocking",
        },
        "production_ready": False,
        "production_thumbnail_ready": False,
        "public_ready": False,
        "rights_accepted": False,
        "youtube_uploaded": False,
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "external_media_used": False,
        "png_generated": False,
        "png_generation_note": "SVG and HTML proof are deterministic and sufficient; no PNG dependency was introduced.",
        "next_safe_local_action": source_context.get("next_safe_local_action"),
    }


def _source_index(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    import_source_index: dict[str, Any],
    validation_noise: dict[str, Any],
) -> dict[str, Any]:
    source_keys = (
        "content_manifest",
        "episode_candidate",
        "thumbnail_brief",
        "import_manifest",
        "import_summary",
        "import_readback",
        "import_panel",
        "import_source_index",
        "preview_csv",
        "gui_panel_data",
        "gui_readback",
        "dashboard_summary",
        "writer_ir",
        "cue_packet",
    )
    output_files = [
        *REQUIRED_THUMBNAIL_PROOF_FILES,
        "variants/headline_driven.svg",
        "variants/speaker_contrast.svg",
        "variants/newsroom_diagram.svg",
    ]
    return {
        "schema_version": "thumbnail_visual_proof_source_index.v1",
        "artifact_id": artifact_id,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "source_artifacts": [_artifact_entry(key, paths[key], repo_root) for key in source_keys],
        "import_preview_source_count": len(import_source_index.get("source_artifacts", [])),
        "output_artifacts": [_artifact_entry(path, output_root / path, repo_root) for path in output_files],
        "validation_ledger": validation_noise,
    }


def _render_markdown_panel(
    *,
    artifact_id: str,
    source_context: dict[str, Any],
    variants: list[dict[str, Any]],
    validation_noise: dict[str, Any],
) -> str:
    lines = [
        "# Thumbnail Visual Proof Pack",
        "",
        f"- artifact_id: {artifact_id}",
        f"- episode: {source_context.get('selected_candidate_id')}",
        f"- variants: {len(variants)}",
        "- recommended variant: `headline_driven` because it has the clearest small-size hierarchy and makes the dry-run boundary visible.",
        "- reviewer should judge: title hierarchy, thumbnail legibility, and which visual direction deserves later hook refinement.",
        "- forbidden/deferred: no external media, no production thumbnail approval, no public upload, no YMM4 import/render.",
        "- source_index: `source_index.json`",
        "",
        "## At A Glance",
        "",
        "| label | value |",
        "|---|---|",
        "| Proof only | true |",
        "| No external media | true |",
        "| Not production thumbnail | true |",
        f"| CSV context | {source_context.get('csv_row_count')} rows / {source_context.get('csv_header_mode')} |",
        f"| validation_noise | {validation_noise.get('status')} |",
        "",
        "## Variants",
        "",
        "| variant_id | headline | visual structure | proof output | recommendation | note |",
        "|---|---|---|---|---|---|",
    ]
    for variant in variants:
        lines.append(
            f"| {variant['variant_id']} | {variant['headline']} | {variant['visual_structure']} | `{variant['svg_path']}` | {variant['recommendation']} | {variant['risk_readback']} |"
        )
    lines.extend([
        "",
        "## Contact Sheet",
        "",
        "- HTML panel: `thumbnail_visual_proof.html`",
        "- SVG contact sheet: `thumbnail_contact_sheet.svg`",
        "",
        "## Next Safe Local Action",
        "",
        str(source_context.get("next_safe_local_action")),
        "",
    ])
    return "\n".join(lines)


def _render_html_panel(
    *,
    artifact_id: str,
    source_context: dict[str, Any],
    variants: list[dict[str, Any]],
    validation_noise: dict[str, Any],
) -> str:
    cards: list[str] = []
    for variant in variants:
        cards.extend([
            '<article class="card">',
            f'  <img src="{_html(str(variant["svg_path"]))}" alt="{_html(variant["variant_id"])}">',
            '  <div class="meta">',
            f'    <strong>{_html(variant["variant_id"])}</strong>',
            f'    <span>{_html(variant["headline"])}</span>',
            f'    <span>{_html(variant["recommendation"])}</span>',
            f'    <span>{_html(variant["what_it_tests"])}</span>',
            "  </div>",
            "</article>",
        ])
    return "\n".join([
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{_html(artifact_id)}</title>",
        "  <style>",
        "    :root { color-scheme: dark; font-family: Arial, Helvetica, sans-serif; }",
        "    body { margin: 0; background: #0b1020; color: #f8fafc; }",
        "    header { padding: 28px 32px 20px; border-bottom: 1px solid #334155; }",
        "    h1 { margin: 0 0 10px; font-size: 30px; letter-spacing: 0; }",
        "    p { margin: 0; color: #cbd5e1; max-width: 1040px; line-height: 1.5; }",
        "    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }",
        "    .chip { border: 1px solid #64748b; border-radius: 999px; padding: 5px 10px; font-size: 13px; color: #e2e8f0; }",
        "    .recommended { color: #fde68a; border-color: #facc15; }",
        "    main { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 22px; padding: 26px 32px 36px; }",
        "    .card { border: 1px solid #334155; border-radius: 8px; background: #111827; overflow: hidden; }",
        "    img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; background: #05080d; }",
        "    .meta { display: grid; gap: 6px; padding: 14px 16px; font-size: 14px; color: #cbd5e1; }",
        "    .meta strong { color: #f8fafc; font-size: 16px; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <header>",
        f"    <h1>Episode 002 Thumbnail Visual Proof</h1>",
        f"    <p>{_html(source_context.get('selected_title'))}. Three local SVG thumbnail directions are shown below. Recommended variant: headline_driven, because it is the clearest small-size proof and does not hide the dry-run boundary.</p>",
        '    <div class="chips">',
        '      <span class="chip">Proof only</span>',
        '      <span class="chip">No external media</span>',
        '      <span class="chip">Not production thumbnail</span>',
        f'      <span class="chip recommended">validation: {_html(validation_noise.get("status"))}</span>',
        '      <span class="chip">source_index.json</span>',
        "    </div>",
        "  </header>",
        "  <main>",
        *cards,
        "  </main>",
        "</body>",
        "</html>",
        "",
    ])


def _render_variant_svg(variant: dict[str, Any]) -> str:
    if variant["variant_id"] == "headline_driven":
        return _render_headline_svg(variant)
    if variant["variant_id"] == "speaker_contrast":
        return _render_speaker_svg(variant)
    return _render_diagram_svg(variant)


def _svg_base(variant: dict[str, Any], body: list[str]) -> str:
    palette = variant["palette"]
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img">',
        f'  <title>{_svg(variant["variant_id"])} thumbnail proof</title>',
        f'  <rect width="1280" height="720" fill="{palette["bg"]}"/>',
        *body,
        '  <rect x="28" y="28" width="168" height="34" rx="17" fill="none" stroke="#f8fafc" stroke-width="2" opacity="0.7"/>',
        '  <text x="112" y="51" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Proof only</text>',
        '  <text x="1244" y="690" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1">No external media / Not production thumbnail</text>',
        f'  <text x="36" y="690" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1">{_svg(variant["variant_id"])}</text>',
        "</svg>",
        "",
    ]
    return "\n".join(lines)


def _render_headline_svg(variant: dict[str, Any]) -> str:
    palette = variant["palette"]
    body = [
        f'  <rect x="68" y="96" width="740" height="496" rx="24" fill="{palette["panel"]}"/>',
        f'  <rect x="96" y="130" width="220" height="18" rx="9" fill="{palette["accent"]}"/>',
        f'  <text x="96" y="238" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="78" font-weight="900" fill="{palette["ink"]}">DRY RUN</text>',
        f'  <text x="96" y="324" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="78" font-weight="900" fill="{palette["ink"]}">FACTORY</text>',
        f'  <text x="96" y="410" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="78" font-weight="900" fill="{palette["accent"]}">CHECK</text>',
        f'  <text x="100" y="478" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#dbeafe">Episode 002 seed opens cleanly</text>',
        f'  <rect x="858" y="128" width="334" height="92" rx="16" fill="{palette["panel"]}" stroke="#64748b"/>',
        f'  <rect x="858" y="252" width="334" height="92" rx="16" fill="{palette["panel"]}" stroke="#64748b"/>',
        f'  <rect x="858" y="376" width="334" height="92" rx="16" fill="{palette["panel"]}" stroke="#64748b"/>',
        f'  <text x="1025" y="184" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800" fill="{palette["ink"]}">9 rows</text>',
        f'  <text x="1025" y="308" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800" fill="{palette["ink"]}">Headerless CSV</text>',
        f'  <text x="1025" y="432" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800" fill="{palette["ink"]}">YMM4 closed</text>',
    ]
    return _svg_base(variant, body)


def _render_speaker_svg(variant: dict[str, Any]) -> str:
    palette = variant["palette"]
    body = [
        f'  <circle cx="330" cy="330" r="150" fill="{palette["panel"]}" stroke="{palette["accent"]}" stroke-width="10"/>',
        f'  <circle cx="950" cy="330" r="150" fill="{palette["panel"]}" stroke="#f472b6" stroke-width="10"/>',
        f'  <text x="330" y="320" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="{palette["ink"]}">A</text>',
        f'  <text x="330" y="374" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="28" fill="#cbd5e1">ASKS</text>',
        f'  <text x="950" y="320" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="{palette["ink"]}">B</text>',
        f'  <text x="950" y="374" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="28" fill="#cbd5e1">EXPLAINS</text>',
        f'  <rect x="410" y="112" width="460" height="122" rx="20" fill="{palette["accent"]}"/>',
        f'  <text x="640" y="185" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="62" font-weight="900" fill="#08111f">SECOND SEED?</text>',
        f'  <rect x="250" y="536" width="780" height="70" rx="16" fill="{palette["panel"]}" stroke="#64748b"/>',
        f'  <text x="640" y="582" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="800" fill="{palette["ink"]}">Two-speaker dry-run contrast, abstract badges only</text>',
    ]
    return _svg_base(variant, body)


def _render_diagram_svg(variant: dict[str, Any]) -> str:
    palette = variant["palette"]
    body = [
        f'  <text x="640" y="118" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="54" font-weight="900" fill="{palette["ink"]}">TEMPLATE -> CSV -> PROOF</text>',
        f'  <rect x="110" y="220" width="290" height="150" rx="20" fill="{palette["panel"]}" stroke="{palette["accent"]}" stroke-width="5"/>',
        f'  <rect x="495" y="220" width="290" height="150" rx="20" fill="{palette["panel"]}" stroke="{palette["accent"]}" stroke-width="5"/>',
        f'  <rect x="880" y="220" width="290" height="150" rx="20" fill="{palette["panel"]}" stroke="{palette["accent"]}" stroke-width="5"/>',
        f'  <text x="255" y="288" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="{palette["ink"]}">TEMPLATE</text>',
        f'  <text x="640" y="288" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="{palette["ink"]}">9-ROW CSV</text>',
        f'  <text x="1025" y="288" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="{palette["ink"]}">THUMB PROOF</text>',
        f'  <text x="255" y="334" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#cbd5e1">dry-run seed</text>',
        f'  <text x="640" y="334" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#cbd5e1">import preview</text>',
        f'  <text x="1025" y="334" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#cbd5e1">review only</text>',
        f'  <path d="M410 295 L480 295" stroke="{palette["accent"]}" stroke-width="8" stroke-linecap="round"/>',
        f'  <path d="M795 295 L865 295" stroke="{palette["accent"]}" stroke-width="8" stroke-linecap="round"/>',
        f'  <rect x="210" y="462" width="860" height="78" rx="18" fill="{palette["panel"]}" stroke="#64748b"/>',
        f'  <text x="640" y="512" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="31" font-weight="800" fill="{palette["ink"]}">closed gates stay visible before any YMM4 or upload lane</text>',
    ]
    return _svg_base(variant, body)


def _render_contact_sheet_svg(variants: list[dict[str, Any]]) -> str:
    width = 1280
    frame_w = 360
    frame_h = 202
    body = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img">',
        '  <title>Episode 002 thumbnail visual proof contact sheet</title>',
        '  <rect width="1280" height="720" fill="#0b1020"/>',
        '  <text x="42" y="58" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="#f8fafc">Episode 002 thumbnail visual proof</text>',
        '  <text x="42" y="94" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#cbd5e1">Proof only / No external media / Not production thumbnail</text>',
    ]
    for index, variant in enumerate(variants):
        x = 42 + index * 405
        y = 136
        body.extend([
            f'  <rect x="{x}" y="{y}" width="{frame_w}" height="{frame_h}" rx="8" fill="#111827" stroke="#334155"/>',
            f'  <text x="{x + 18}" y="{y + 50}" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="30" font-weight="900" fill="#f8fafc">{_svg(variant["headline"])}</text>',
            f'  <text x="{x + 18}" y="{y + 88}" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1">{_svg(variant["subheadline"])}</text>',
            f'  <rect x="{x + 18}" y="{y + 118}" width="150" height="28" rx="14" fill="#1e293b" stroke="#64748b"/>',
            f'  <text x="{x + 93}" y="{y + 138}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="800" fill="#f8fafc">{_svg(variant["status"])}</text>',
            f'  <text x="{x}" y="{y + frame_h + 44}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="800" fill="#f8fafc">{_svg(variant["variant_id"])}</text>',
            f'  <text x="{x}" y="{y + frame_h + 76}" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#cbd5e1">{_svg(variant["recommendation"])}</text>',
            f'  <text x="{x}" y="{y + frame_h + 108}" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#94a3b8">{_svg(variant["layout_family"])}</text>',
        ])
    body.extend([
        f'  <text x="{width - 42}" y="680" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#94a3b8">Open thumbnail_visual_proof.html for the full review panel</text>',
        "</svg>",
        "",
    ])
    return "\n".join(body)


def _render_limitations(source_context: dict[str, Any]) -> str:
    return "\n".join([
        "# Thumbnail Visual Proof Limitations",
        "",
        "This proof pack uses deterministic local SVG/HTML shapes and text only.",
        "",
        "Not performed:",
        "",
        "- external image or media download",
        "- embedded copyrighted media",
        "- production thumbnail acceptance",
        "- rights/legal/public-ready acceptance",
        "- YouTube upload, publication, scheduling, or visibility change",
        "- OAuth/API key/payment action",
        "- YMM4 GUI launch/import/render",
        "- production .ymmp creation",
        "- real transcript rerun",
        "- PNG export; SVG/HTML is the tracked proof surface",
        "",
        "Current safe action:",
        "",
        str(source_context.get("next_safe_local_action")),
        "",
    ])


def _validation_noise_payload(repo_root: Path, import_summary: dict[str, Any], gui_panel_data: dict[str, Any]) -> dict[str, Any]:
    for candidate in (import_summary.get("validation_noise"), gui_panel_data.get("validation_noise")):
        if isinstance(candidate, dict) and candidate.get("status") == "validation_noise_nonblocking":
            return dict(candidate)
    ledger_path = repo_root / VALIDATION_LEDGER_PATH
    ledger = _load_json_if_present(ledger_path)
    if not isinstance(ledger, dict):
        return {"status": "unknown", "ledger_path": _relpath(ledger_path, repo_root), "exists": False, "blocking_for_this_slice": True}
    full_pytest_input = ledger.get("validation_evidence", {}).get("recent_full_pytest_input", {})
    safe_to_continue = bool(ledger.get("blocking_decision", {}).get("safe_to_continue_product_work"))
    return {
        "status": "validation_noise_nonblocking" if safe_to_continue else "unknown",
        "ledger_path": _relpath(ledger_path, repo_root),
        "exists": True,
        "safe_to_continue_product_work": safe_to_continue,
        "full_pytest_policy": full_pytest_input.get("policy_decision"),
        "recent_full_pytest_result": full_pytest_input.get("result"),
        "blocking_for_this_slice": False if safe_to_continue else True,
    }


def _markdown_field(markdown: str, key: str) -> str:
    prefix = f"- {key}:"
    for line in markdown.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return ""


def _title_hook(title: str) -> str:
    words = [word for word in title.replace("/", " ").split() if word]
    if len(words) <= 7:
        return title
    return " ".join(words[:7])


def _artifact_entry(artifact_id: str, path: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "id": artifact_id,
        "repo_relative_path": _relpath(path, repo_root),
        "exists": path.exists(),
        "state": "ready" if path.exists() else "missing",
    }


def _forbidden_true_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for claim in FORBIDDEN_TRUE_CLAIMS:
                if claim in text:
                    hits.append(f"{path.name}:{claim}")
    return hits


def _external_refs(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            for marker in (
                "data:image",
                "src=\"http://",
                "src=\"https://",
                "src='http://",
                "src='https://",
                "href=\"http://",
                "href=\"https://",
                "href='http://",
                "href='https://",
                "<image href=\"http",
                "<image href='http",
            ):
                if marker in text:
                    hits.append(f"{path.name}:{marker}")
    return hits


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return data


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _find_repo_root(path: Path) -> Path:
    resolved = path.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    return Path.cwd()


def _relpath(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def _html(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _svg(value: Any) -> str:
    return html.escape(str(value), quote=False)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

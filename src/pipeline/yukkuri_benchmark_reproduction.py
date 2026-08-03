from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any, Mapping


REGISTRY_SCHEMA = "nlmytgen.yukkuri_benchmark_registry.v1"
PACK_SCHEMA = "nlmytgen.yukkuri_benchmark_pack.v1"
READBACK_SCHEMA = "nlmytgen.yukkuri_benchmark_readback.v1"
ALLOWED_DIMENSION_STATES = {"measured", "partial", "missing"}
REQUIRED_COMPLETION_GATES = (
    "rights_cleared_replacements",
    "yymm4_readback_passed",
    "render_comparison_passed",
    "human_creative_acceptance",
)
DEFAULT_REGISTRY = Path(
    "production_pilots/yukkuri_benchmark_six_v1/benchmark_registry.json"
)
DEFAULT_OUTPUT = Path(
    "production_pilots/yukkuri_benchmark_six_v1/reproduction_pack"
)


DIMENSION_REQUIREMENTS: dict[str, str] = {
    "identity": "channel, video, title, publication date, and immutable source locator",
    "script": "complete dialogue text, speaker assignment, line order, and approved rewrite boundary",
    "timeline": "full duration, chapters, every visual state interval, and transition anchors",
    "composition": "canvas, safe areas, object bounds, text bounds, and visual hierarchy per state",
    "subtitles": "font family, size, stroke, color, line count, wrapping, position, and timing",
    "characters": "speaker assets, scale, placement, expression state, persistence, and alternation",
    "assets": "every image, diagram, background, source credit, replacement, and content hash",
    "motion": "entrance, exit, zoom, pan, emphasis, transition, frequency, easing, and reset policy",
    "audio": "voice, BGM, SE, silence, level, timing, and a separately authorized observation record",
    "yymm4_mapping": "existing YMM4 template source, registry labels, IR mapping, and post-import patch plan",
    "rights": "approved reusable or replacement assets plus attribution and prohibited-copy decisions",
    "render_comparison": "machine readback, frame-level comparison, duration match, and human creative acceptance",
}


class BenchmarkRegistryError(ValueError):
    """Raised when the six-target benchmark contract is incomplete or unsafe."""


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise BenchmarkRegistryError(f"Expected JSON object: {path}")
    return value


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_benchmark_registry(path: str | Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    registry = _read_json(Path(path))
    validate_benchmark_registry(registry)
    return registry


def validate_benchmark_registry(registry: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if registry.get("schema_version") != REGISTRY_SCHEMA:
        errors.append("REGISTRY_SCHEMA_INVALID")
    if registry.get("strategy") != "reverse_engineering_quick_win":
        errors.append("STRATEGY_NOT_REVERSE_ENGINEERING")
    if registry.get("audio_policy") != "silent":
        errors.append("AUDIO_POLICY_NOT_SILENT")
    for field in (
        "media_foreground_allowed",
        "media_playback_allowed",
        "automatic_media_download_allowed",
    ):
        if registry.get(field) is not False:
            errors.append(f"{field.upper()}_MUST_BE_FALSE")

    required_dimensions = registry.get("required_dimensions")
    if required_dimensions != list(DIMENSION_REQUIREMENTS):
        errors.append("REQUIRED_DIMENSIONS_NOT_EXACT")

    targets = registry.get("targets")
    if not isinstance(targets, list) or len(targets) != 6:
        errors.append("TARGET_COUNT_NOT_SIX")
        targets = targets if isinstance(targets, list) else []

    unique_fields = {
        "benchmark_id": [],
        "archetype_id": [],
        "channel_name": [],
        "video_id": [],
    }
    quick_win_priorities: list[int] = []
    for index, target in enumerate(targets, start=1):
        prefix = f"TARGET_{index:02d}"
        if not isinstance(target, Mapping):
            errors.append(f"{prefix}_NOT_OBJECT")
            continue
        expected_id = f"B{index:02d}"
        if target.get("benchmark_id") != expected_id:
            errors.append(f"{prefix}_ID_NOT_SEQUENTIAL")
        for field, values in unique_fields.items():
            value = target.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}_{field.upper()}_MISSING")
            else:
                values.append(value)
        for field in ("title", "canonical_url", "published", "selected_reason"):
            if not isinstance(target.get(field), str) or not target[field].strip():
                errors.append(f"{prefix}_{field.upper()}_MISSING")
        priority = target.get("quick_win_priority")
        if not isinstance(priority, int) or isinstance(priority, bool):
            errors.append(f"{prefix}_QUICK_WIN_PRIORITY_INVALID")
        else:
            quick_win_priorities.append(priority)
        evidence_locators = target.get("evidence_locators")
        if (
            not isinstance(evidence_locators, list)
            or not evidence_locators
            or any(not isinstance(value, str) or not value.strip() for value in evidence_locators)
        ):
            errors.append(f"{prefix}_EVIDENCE_LOCATORS_INVALID")
        video_id = target.get("video_id")
        expected_url = f"https://www.youtube.com/watch?v={video_id}"
        if target.get("canonical_url") != expected_url:
            errors.append(f"{prefix}_CANONICAL_URL_MISMATCH")

        observation = target.get("observation")
        if not isinstance(observation, Mapping):
            errors.append(f"{prefix}_OBSERVATION_MISSING")
        else:
            if not isinstance(observation.get("observed_surfaces"), list):
                errors.append(f"{prefix}_OBSERVED_SURFACES_INVALID")
            if not isinstance(observation.get("static_signature"), Mapping):
                errors.append(f"{prefix}_STATIC_SIGNATURE_INVALID")

        statuses = target.get("dimension_status")
        if not isinstance(statuses, Mapping) or set(statuses) != set(DIMENSION_REQUIREMENTS):
            errors.append(f"{prefix}_DIMENSION_SET_INVALID")
        else:
            for dimension, state in statuses.items():
                if state not in ALLOWED_DIMENSION_STATES:
                    errors.append(f"{prefix}_{dimension.upper()}_STATE_INVALID")

        gates = target.get("completion_gates")
        if not isinstance(gates, Mapping) or set(gates) != set(REQUIRED_COMPLETION_GATES):
            errors.append(f"{prefix}_COMPLETION_GATES_INVALID")
        elif any(not isinstance(gates[name], bool) for name in REQUIRED_COMPLETION_GATES):
            errors.append(f"{prefix}_COMPLETION_GATE_NOT_BOOLEAN")

    for field, values in unique_fields.items():
        if len(values) != len(set(values)):
            errors.append(f"{field.upper()}_NOT_UNIQUE")
    if sorted(quick_win_priorities) != list(range(1, 7)):
        errors.append("QUICK_WIN_PRIORITIES_NOT_EXACT")

    result = {
        "schema_version": REGISTRY_SCHEMA,
        "status": "passed" if not errors else "failed",
        "target_count": len(targets),
        "dimension_count": len(DIMENSION_REQUIREMENTS),
        "errors": errors,
    }
    if errors:
        raise BenchmarkRegistryError("; ".join(errors))
    return result


def _target_blueprint(target: Mapping[str, Any], dimensions: list[str]) -> dict[str, Any]:
    states = dict(target["dimension_status"])
    measured = [name for name in dimensions if states[name] == "measured"]
    incomplete = [name for name in dimensions if states[name] != "measured"]
    gates = dict(target["completion_gates"])
    gates_passed = all(gates[name] for name in REQUIRED_COMPLETION_GATES)
    ready = not incomplete and gates_passed
    return {
        "schema_version": "nlmytgen.yukkuri_reproduction_blueprint.v1",
        "benchmark_id": target["benchmark_id"],
        "archetype_id": target["archetype_id"],
        "quick_win_priority": target["quick_win_priority"],
        "channel_name": target["channel_name"],
        "source_video": {
            "video_id": target["video_id"],
            "title": target["title"],
            "canonical_url": target["canonical_url"],
            "published": target["published"],
        },
        "selected_reason": target["selected_reason"],
        "evidence_locators": list(target["evidence_locators"]),
        "observation": target["observation"],
        "dimension_status": states,
        "dimension_requirements": {
            name: DIMENSION_REQUIREMENTS[name] for name in dimensions
        },
        "measured_dimensions": measured,
        "incomplete_dimensions": incomplete,
        "measured_count": len(measured),
        "required_count": len(dimensions),
        "completion_gates": gates,
        "reproduction_ready": ready,
        "status": "reproduction_ready" if ready else "blocked_by_missing_evidence",
        "next_static_action": (
            "record or import evidence for " + incomplete[0]
            if incomplete
            else "await completion gate evidence"
        ),
        "boundaries": {
            "static_review_only": True,
            "foreground_media": False,
            "audible_output": False,
            "automatic_download": False,
            "python_video_render": False,
            "ymmp_zero_generation": False,
            "source_expression_copy_authorized": False,
        },
    }


def _review_card_html(blueprint: Mapping[str, Any]) -> str:
    rows = "".join(
        f"<tr><th>{html.escape(name)}</th><td class='{html.escape(state)}'>{html.escape(state)}</td>"
        f"<td>{html.escape(DIMENSION_REQUIREMENTS[name])}</td></tr>"
        for name, state in blueprint["dimension_status"].items()
    )
    source = blueprint["source_video"]
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(blueprint['benchmark_id'])} static benchmark card</title>
<style>body{{font-family:system-ui,sans-serif;background:#111827;color:#e5e7eb;margin:0;padding:32px}}main{{max-width:1100px;margin:auto}}.card{{background:#1f2937;border:1px solid #475569;border-radius:16px;padding:28px}}.eyebrow{{color:#67e8f9}}h1{{margin:.25rem 0}}.blocked,.missing{{color:#fca5a5}}.partial{{color:#fde68a}}.measured{{color:#86efac}}table{{width:100%;border-collapse:collapse;margin-top:20px}}th,td{{text-align:left;border-top:1px solid #475569;padding:10px;vertical-align:top}}th{{width:15%}}code{{color:#a5f3fc}}.notice{{background:#0f172a;border-left:4px solid #f59e0b;padding:12px 16px}}</style></head>
<body><main><section class="card"><div class="eyebrow">STATIC / SILENT / REVERSE BENCHMARK</div>
<h1>{html.escape(blueprint['benchmark_id'])} · {html.escape(blueprint['channel_name'])}</h1>
<p>{html.escape(source['title'])}</p><p>Archetype: <code>{html.escape(blueprint['archetype_id'])}</code></p>
<p class="notice">Status: <strong class="blocked">{html.escape(blueprint['status'])}</strong>. This page embeds no player, audio, iframe, or remote asset.</p>
<p>Measured: {blueprint['measured_count']} / {blueprint['required_count']} required dimensions</p>
<table><thead><tr><th>Dimension</th><th>State</th><th>Completion evidence</th></tr></thead><tbody>{rows}</tbody></table>
</section></main></body></html>
"""


def _blueprint_markdown(blueprint: Mapping[str, Any]) -> str:
    source = blueprint["source_video"]
    missing = ", ".join(blueprint["incomplete_dimensions"])
    return f"""# {blueprint['benchmark_id']} — {blueprint['channel_name']}

This is a static, silent reverse-engineering blueprint for one fixed benchmark video.

- Archetype: `{blueprint['archetype_id']}`
- Source identity: `{source['video_id']}` / {source['title']}
- Current result: `{blueprint['status']}`
- Measured dimensions: `{blueprint['measured_count']}/{blueprint['required_count']}`
- Incomplete dimensions: {missing or 'none'}
- Next static action: {blueprint['next_static_action']}

`reproduction_ready` stays false until every required dimension is measured and all
rights, YMM4 readback, render comparison, and human acceptance gates pass. This pack
does not launch or embed media, download source assets, render video, generate a new
`.ymmp`, or authorize copying source expression.
"""


def _index_html(blueprints: list[dict[str, Any]]) -> str:
    cards = "".join(
        f"<article><div class='id'>{html.escape(row['benchmark_id'])} · {html.escape(row['archetype_id'])}</div>"
        f"<h2>{html.escape(row['channel_name'])}</h2><p>{html.escape(row['source_video']['title'])}</p>"
        f"<p><strong>{row['measured_count']}/{row['required_count']}</strong> dimensions measured</p>"
        f"<p class='blocked'>{html.escape(row['status'])}</p>"
        f"<a href='{html.escape(row['benchmark_id'])}/static_review_card.html'>Open static card</a></article>"
        for row in blueprints
    )
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Six-channel reverse benchmark</title><style>body{{font-family:system-ui,sans-serif;background:#07111f;color:#e5e7eb;margin:0;padding:32px}}main{{max-width:1300px;margin:auto}}header{{margin-bottom:28px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}}article{{background:#111c2e;border:1px solid #334155;border-radius:14px;padding:20px}}.id{{color:#67e8f9}}.blocked{{color:#fca5a5}}a{{color:#93c5fd}}.notice{{background:#172033;border-left:4px solid #f59e0b;padding:14px}}</style></head>
<body><main><header><div>STATIC / SILENT / QUICK-WIN</div><h1>6-channel Yukkuri reverse benchmark</h1>
<p class="notice">One controlled topic, six distinct editing archetypes. No player, audio, iframe, remote asset, download, render, or YMM4 launch is used by this review surface.</p></header>
<section class="grid">{cards}</section></main></body></html>
"""


def build_yukkuri_benchmark_pack(
    registry_path: str | Path = DEFAULT_REGISTRY,
    output_dir: str | Path = DEFAULT_OUTPUT,
    *,
    artifact_id: str | None = None,
) -> dict[str, Any]:
    registry_path = Path(registry_path)
    output_dir = Path(output_dir)
    registry = load_benchmark_registry(registry_path)
    dimensions = list(registry["required_dimensions"])
    blueprints = [_target_blueprint(target, dimensions) for target in registry["targets"]]

    generated: list[Path] = []
    for blueprint in blueprints:
        target_dir = output_dir / blueprint["benchmark_id"]
        json_path = target_dir / "reproduction_blueprint.json"
        markdown_path = target_dir / "README.md"
        html_path = target_dir / "static_review_card.html"
        _write_json(json_path, blueprint)
        _write_text(markdown_path, _blueprint_markdown(blueprint))
        _write_text(html_path, _review_card_html(blueprint))
        generated.extend((json_path, markdown_path, html_path))

    gap_matrix = {
        "schema_version": "nlmytgen.yukkuri_benchmark_gap_matrix.v1",
        "required_dimensions": dimensions,
        "targets": [
            {
                "benchmark_id": row["benchmark_id"],
                "channel_name": row["channel_name"],
                "archetype_id": row["archetype_id"],
                "quick_win_priority": row["quick_win_priority"],
                "measured_count": row["measured_count"],
                "required_count": row["required_count"],
                "incomplete_dimensions": row["incomplete_dimensions"],
                "completion_gates": row["completion_gates"],
                "reproduction_ready": row["reproduction_ready"],
            }
            for row in blueprints
        ],
    }
    gap_path = output_dir / "gap_matrix.json"
    index_path = output_dir / "index.html"
    _write_json(gap_path, gap_matrix)
    _write_text(index_path, _index_html(blueprints))
    generated.extend((gap_path, index_path))

    execution_queue = {
        "schema_version": "nlmytgen.yukkuri_benchmark_execution_queue.v1",
        "strategy": "lowest_complexity_first_without_media_playback",
        "next_benchmark_id": min(
            blueprints, key=lambda row: row["quick_win_priority"]
        )["benchmark_id"],
        "targets": [
            {
                "quick_win_priority": row["quick_win_priority"],
                "benchmark_id": row["benchmark_id"],
                "archetype_id": row["archetype_id"],
                "status": row["status"],
                "next_static_action": row["next_static_action"],
            }
            for row in sorted(
                blueprints, key=lambda row: row["quick_win_priority"]
            )
        ],
        "automatic_execution": False,
        "requires_authorized_evidence_before_promotion": True,
    }
    execution_queue_path = output_dir / "execution_queue.json"
    _write_json(execution_queue_path, execution_queue)
    generated.append(execution_queue_path)

    html_text = "\n".join(path.read_text(encoding="utf-8") for path in generated if path.suffix == ".html")
    forbidden_tags = [tag for tag in ("video", "audio", "iframe", "source") if f"<{tag}" in html_text.lower()]
    ready_count = sum(bool(row["reproduction_ready"]) for row in blueprints)
    readback = {
        "schema_version": READBACK_SCHEMA,
        "status": "passed" if not forbidden_tags and len(blueprints) == 6 else "failed",
        "target_count": len(blueprints),
        "archetype_count": len({row["archetype_id"] for row in blueprints}),
        "channel_count": len({row["channel_name"] for row in blueprints}),
        "video_count": len({row["source_video"]["video_id"] for row in blueprints}),
        "required_dimension_count": len(dimensions),
        "reproduction_ready_count": ready_count,
        "blocked_count": len(blueprints) - ready_count,
        "checks": {
            "exactly_six_targets": len(blueprints) == 6,
            "six_unique_archetypes": len({row["archetype_id"] for row in blueprints}) == 6,
            "six_unique_channels": len({row["channel_name"] for row in blueprints}) == 6,
            "six_unique_videos": len({row["source_video"]["video_id"] for row in blueprints}) == 6,
            "quick_win_priorities_are_one_through_six": sorted(
                row["quick_win_priority"] for row in blueprints
            ) == list(range(1, 7)),
            "quick_win_starts_with_compact_profile": execution_queue[
                "next_benchmark_id"
            ] == "B05",
            "static_html_has_no_media_or_iframe_tags": not forbidden_tags,
            "silent_policy_preserved": registry["audio_policy"] == "silent",
            "foreground_media_disabled": registry["media_foreground_allowed"] is False,
            "automatic_download_disabled": registry["automatic_media_download_allowed"] is False,
            "no_false_ready_claims": all(
                row["reproduction_ready"]
                == (not row["incomplete_dimensions"] and all(row["completion_gates"].values()))
                for row in blueprints
            ),
        },
        "forbidden_tags_found": forbidden_tags,
    }
    readback["checks"]["all_passed"] = all(readback["checks"].values())
    readback["status"] = "passed" if readback["checks"]["all_passed"] else "failed"
    readback_path = output_dir / "readback.json"
    _write_json(readback_path, readback)
    generated.append(readback_path)

    manifest = {
        "schema_version": PACK_SCHEMA,
        "artifact_id": artifact_id or registry["artifact_id"],
        "strategy": registry["strategy"],
        "registry": registry_path.as_posix(),
        "target_ids": [row["benchmark_id"] for row in blueprints],
        "reproduction_ready_count": ready_count,
        "blocked_count": len(blueprints) - ready_count,
        "audio_policy": registry["audio_policy"],
        "static_only": True,
        "file_sha256": {
            path.relative_to(output_dir).as_posix(): _sha256(path)
            for path in sorted(generated)
        },
    }
    manifest_path = output_dir / "manifest.json"
    _write_json(manifest_path, manifest)

    return {
        "status": readback["status"],
        "artifact_id": manifest["artifact_id"],
        "output_dir": output_dir.as_posix(),
        "target_count": len(blueprints),
        "reproduction_ready_count": ready_count,
        "blocked_count": len(blueprints) - ready_count,
        "readback": readback,
        "manifest": manifest_path.as_posix(),
        "index": index_path.as_posix(),
    }


def render_benchmark_pack_text(result: Mapping[str, Any]) -> str:
    return (
        f"Six-channel reverse benchmark: {result['status']}\n"
        f"Targets: {result['target_count']}\n"
        f"Reproduction ready: {result['reproduction_ready_count']}\n"
        f"Blocked by missing evidence: {result['blocked_count']}\n"
        f"Static index: {result['index']}\n"
    )

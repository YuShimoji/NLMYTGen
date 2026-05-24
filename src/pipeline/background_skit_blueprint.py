"""Background skit blueprint validator.

This gate turns background-skit planning from prose into a source-backed
artifact. It cannot prove semantic understanding, but it can reject fabricated
numbers, arbitrary line ranges, missing asset/control bindings, and unverified
handoffs before IR/YMM4 production timing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any


TOP_LEVEL_REQUIRED = (
    "source_lock",
    "script_diagnostic",
    "duration_model",
    "blocks",
    "asset_control_matrix",
    "density_thresholds",
    "blockers",
)

SOURCE_LOCK_REQUIRED = (
    "script_source",
    "script_sha256",
    "line_count",
    "ymmp_source",
    "fps",
    "total_duration_formula",
    "duration_source",
)

ASSET_REQUIRED = (
    "availability",
    "owner",
    "control_needed",
    "control_route",
    "readback_check",
)

DENSITY_THRESHOLDS_REQUIRED = (
    "minimum_active_visual_coverage_pct",
    "maximum_unexplained_gap_sec",
    "visual_states_per_min_range",
    "maximum_repeated_motion_ratio",
)

TIMING_BLOCKER_CODES = {
    "TIMETABLE_BLOCKED_TIMING_SOURCE_MISSING",
    "DURATION_BLOCKED",
    "TIMING_SOURCE_MISSING",
}

SCRIPT_BLOCKER_RE07_TOO_BROAD = "SCRIPT_BLOCKED_RE07_TOO_BROAD"

NEXT_ACTIONS = (
    "overlay_only_compact_review",
    "cast_motion_ir",
    "ymm4_creative_acceptance",
    "production_timing",
)


@dataclass
class BackgroundSkitBlueprintValidationResult:
    status: str = "passed"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    allowed_next_actions: list[str] = field(default_factory=list)
    forbidden_next_actions: list[str] = field(default_factory=list)
    derived_metrics: dict[str, Any] = field(default_factory=dict)

    def finalize(self) -> "BackgroundSkitBlueprintValidationResult":
        if self.errors:
            self.status = "failed"
        elif self.blockers:
            self.status = "blocked"
        else:
            self.status = "passed"
        _assign_next_actions(self)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "blockers": self.blockers,
            "allowed_next_actions": self.allowed_next_actions,
            "forbidden_next_actions": self.forbidden_next_actions,
            "derived_metrics": self.derived_metrics,
        }


def validate_background_skit_blueprint(
    blueprint: dict[str, Any],
    *,
    script_path: str | Path,
    ymmp_path: str | Path | None = None,
    fps: float = 60.0,
    tolerance_sec: float = 0.05,
) -> BackgroundSkitBlueprintValidationResult:
    result = BackgroundSkitBlueprintValidationResult()
    script_path = Path(script_path)
    ymmp_path = Path(ymmp_path) if ymmp_path is not None else None

    for key in TOP_LEVEL_REQUIRED:
        if key not in blueprint:
            result.errors.append(f"BLUEPRINT_FIELD_MISSING: {key}")
    if result.errors:
        return result.finalize()

    source_lock = _as_dict(blueprint.get("source_lock"))
    for key in SOURCE_LOCK_REQUIRED:
        if key not in source_lock:
            result.errors.append(f"SOURCE_LOCK_FIELD_MISSING: {key}")

    declared_blockers = _as_string_list(blueprint.get("blockers"))
    result.blockers.extend(declared_blockers)
    timing_blocked = _has_timing_blocker(declared_blockers)

    script_bytes = script_path.read_bytes()
    script_text = script_bytes.decode("utf-8-sig")
    script_line_count = len(script_text.splitlines())
    script_sha256 = hashlib.sha256(script_bytes).hexdigest()
    result.derived_metrics["script"] = {
        "path": str(script_path),
        "line_count": script_line_count,
        "sha256": script_sha256,
    }

    if source_lock.get("line_count") != script_line_count:
        result.errors.append(
            "SCRIPT_SOURCE_MISMATCH: "
            f"line_count declared={source_lock.get('line_count')} actual={script_line_count}"
        )
    if source_lock.get("script_sha256") != script_sha256:
        result.errors.append("SCRIPT_SHA256_MISMATCH: script_sha256 does not match source script")
    if _to_float(source_lock.get("fps")) != float(fps):
        result.errors.append(
            f"FPS_MISMATCH: source_lock fps={source_lock.get('fps')} cli fps={fps:g}"
        )

    if ymmp_path is None or not ymmp_path.exists():
        blocker = "TIMETABLE_BLOCKED_TIMING_SOURCE_MISSING"
        if not any(str(item).startswith(blocker) for item in result.blockers):
            result.blockers.append(
                f"{blocker}: ymmp source not found: {ymmp_path}"
            )
        timing_blocked = True
    else:
        duration_sec = _load_ymmp_total_duration_sec(ymmp_path, fps)
        result.derived_metrics["duration"] = {
            "ymmp_path": str(ymmp_path),
            "fps": fps,
            "total_duration_sec": duration_sec,
            "formula": "max(Frame + Length) / fps",
        }

    _validate_script_diagnostic(blueprint, result)
    assets = _validate_asset_control_matrix(blueprint, result)
    blocks = _as_list(blueprint.get("blocks"))

    if timing_blocked:
        return result.finalize()

    duration_model = _as_dict(blueprint.get("duration_model"))
    declared_duration = _to_float(duration_model.get("total_duration_sec"))
    actual_duration = result.derived_metrics.get("duration", {}).get("total_duration_sec")
    if declared_duration is None:
        result.errors.append("DURATION_MODEL_MISSING_TOTAL: total_duration_sec is required")
    elif actual_duration is not None and abs(declared_duration - actual_duration) > tolerance_sec:
        result.errors.append(
            "DURATION_MISMATCH: "
            f"declared={declared_duration:.3f} actual={actual_duration:.3f}"
        )

    if not blocks:
        result.errors.append("BLOCKS_MISSING: blocks must not be empty when timing source exists")
        return result.finalize()

    block_metrics = _validate_blocks(
        blocks,
        line_count=script_line_count,
        total_duration_sec=declared_duration,
        assets=assets,
        blueprint=blueprint,
        result=result,
        tolerance_sec=tolerance_sec,
    )
    _resolve_script_blockers_from_subbeats(
        blueprint,
        blocks,
        result,
        tolerance_sec=tolerance_sec,
    )
    result.derived_metrics["blocks"] = block_metrics

    density = _compute_density_metrics(blocks, declared_duration or 0.0)
    result.derived_metrics["density"] = density
    _validate_density_thresholds(blueprint, density, result)
    _validate_declared_density(blueprint, density, result, tolerance_sec=tolerance_sec)

    return result.finalize()


def load_background_skit_blueprint(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("BACKGROUND_SKIT_BLUEPRINT_INVALID: root must be an object")
    return data


def render_background_skit_blueprint_text(
    result: BackgroundSkitBlueprintValidationResult,
) -> str:
    lines = [f"Background Skit Blueprint: {result.status}"]
    if result.errors:
        lines.append("\nErrors:")
        lines.extend(f"- {item}" for item in result.errors)
    if result.blockers:
        lines.append("\nBlockers:")
        lines.extend(f"- {item}" for item in result.blockers)
    if result.allowed_next_actions:
        lines.append("\nAllowed next actions:")
        lines.extend(f"- {item}" for item in result.allowed_next_actions)
    if result.forbidden_next_actions:
        lines.append("\nForbidden next actions:")
        lines.extend(f"- {item}" for item in result.forbidden_next_actions)
    if result.warnings:
        lines.append("\nWarnings:")
        lines.extend(f"- {item}" for item in result.warnings)
    if result.derived_metrics:
        lines.append("\nDerived metrics:")
        lines.append(json.dumps(result.derived_metrics, ensure_ascii=False, indent=2))
    return "\n".join(lines) + "\n"


def _validate_script_diagnostic(
    blueprint: dict[str, Any],
    result: BackgroundSkitBlueprintValidationResult,
) -> None:
    diagnostic = _as_dict(blueprint.get("script_diagnostic"))
    if not diagnostic:
        result.errors.append("SCRIPT_DIAGNOSTIC_MISSING: script_diagnostic must be an object")
        return
    if not diagnostic.get("ideal_script_delta"):
        result.errors.append("SCRIPT_DIAGNOSTIC_MISSING_IDEAL_DELTA: ideal_script_delta is required")
    if not diagnostic.get("source_line_citations"):
        result.errors.append(
            "SCRIPT_DIAGNOSTIC_MISSING_SOURCE_LINES: source_line_citations is required"
        )


def _validate_asset_control_matrix(
    blueprint: dict[str, Any],
    result: BackgroundSkitBlueprintValidationResult,
) -> dict[str, dict[str, Any]]:
    raw_matrix = blueprint.get("asset_control_matrix")
    assets: dict[str, dict[str, Any]] = {}
    if isinstance(raw_matrix, dict):
        for key, value in raw_matrix.items():
            if isinstance(value, dict):
                assets[str(key)] = value
            else:
                result.errors.append(f"ASSET_CONTROL_INVALID: {key} must be an object")
    elif isinstance(raw_matrix, list):
        for index, value in enumerate(raw_matrix):
            if not isinstance(value, dict):
                result.errors.append(f"ASSET_CONTROL_INVALID: item#{index} must be an object")
                continue
            asset_id = value.get("id")
            if not asset_id:
                result.errors.append(f"ASSET_CONTROL_ID_MISSING: item#{index}")
                continue
            assets[str(asset_id)] = value
    else:
        result.errors.append("ASSET_CONTROL_MATRIX_INVALID: must be object or list")
        return assets

    for asset_id, item in assets.items():
        for field_name in ASSET_REQUIRED:
            if not _has_value(item.get(field_name)):
                result.errors.append(f"ASSET_CONTROL_FIELD_MISSING: {asset_id}.{field_name}")
        template_name = str(item.get("template_name", ""))
        if template_name.startswith("delivery_"):
            if not _has_value(item.get("symbolic_role")) or not _has_value(
                item.get("proxy_limitation")
            ):
                result.errors.append(
                    "TEMPLATE_REUSE_UNGROUNDED: "
                    f"{asset_id} uses {template_name} without symbolic_role and proxy_limitation"
                )
    return assets


def _validate_blocks(
    blocks: list[Any],
    *,
    line_count: int,
    total_duration_sec: float | None,
    assets: dict[str, dict[str, Any]],
    blueprint: dict[str, Any],
    result: BackgroundSkitBlueprintValidationResult,
    tolerance_sec: float,
) -> dict[str, Any]:
    line_ranges: list[tuple[int, int, str]] = []
    timeline_ranges: list[tuple[float, float, str]] = []
    all_active_windows: list[tuple[float, float]] = []
    all_rest_windows: list[tuple[float, float]] = []
    intents: list[str] = []

    for index, raw_block in enumerate(blocks):
        if not isinstance(raw_block, dict):
            result.errors.append(f"BLOCK_INVALID: block#{index} must be an object")
            continue
        block_id = str(raw_block.get("block_id") or f"block#{index}")
        line_start = _to_int(raw_block.get("line_start"))
        line_end = _to_int(raw_block.get("line_end"))
        if line_start is None or line_end is None:
            result.errors.append(f"LINE_RANGE_MISSING: {block_id}")
        elif line_start < 1 or line_end > line_count or line_start > line_end:
            result.errors.append(
                f"LINE_RANGE_OUT_OF_BOUNDS: {block_id} lines {line_start}-{line_end}"
            )
        else:
            line_ranges.append((line_start, line_end, block_id))

        if not _has_value(raw_block.get("range_basis")):
            result.errors.append(f"RANGE_BASIS_MISSING: {block_id}")
        if not _has_value(raw_block.get("negative_rationale")):
            result.errors.append(f"NEGATIVE_RATIONALE_MISSING: {block_id}")
        if not _has_value(raw_block.get("proof_path")):
            result.errors.append(f"BLOCK_PROOF_PATH_MISSING: {block_id}")

        block_start = _to_float(raw_block.get("block_start_sec"))
        block_end = _to_float(raw_block.get("block_end_sec"))
        if block_start is None or block_end is None or block_start >= block_end:
            result.errors.append(f"BLOCK_TIME_INVALID: {block_id}")
            continue
        timeline_ranges.append((block_start, block_end, block_id))

        for asset_id in _as_string_list(raw_block.get("cast")) + _as_string_list(
            raw_block.get("props")
        ):
            if asset_id not in assets:
                result.errors.append(f"ASSET_CONTROL_UNBOUND: {block_id}.{asset_id}")

        template_name = str(raw_block.get("template_name", ""))
        if template_name.startswith("delivery_"):
            if not _has_value(raw_block.get("symbolic_role")) or not _has_value(
                raw_block.get("proxy_limitation")
            ):
                result.errors.append(
                    f"TEMPLATE_REUSE_UNGROUNDED: {block_id} uses {template_name}"
                )
        intent = raw_block.get("intent")
        if isinstance(intent, str) and intent:
            intents.append(intent)

        for window in _as_list(raw_block.get("skit_active_windows")):
            parsed = _parse_window(window)
            if parsed is None:
                result.errors.append(f"ACTIVE_WINDOW_INVALID: {block_id}")
                continue
            start, end = parsed
            if start < block_start - tolerance_sec or end > block_end + tolerance_sec:
                result.errors.append(f"ACTIVE_WINDOW_OUT_OF_BLOCK: {block_id} {start:g}-{end:g}")
            all_active_windows.append((start, end))

        for window in _as_list(raw_block.get("rest_windows")):
            parsed = _parse_window(window)
            if parsed is None:
                result.errors.append(f"REST_WINDOW_INVALID: {block_id}")
                continue
            start, end = parsed
            if start < block_start - tolerance_sec or end > block_end + tolerance_sec:
                result.errors.append(f"REST_WINDOW_OUT_OF_BLOCK: {block_id} {start:g}-{end:g}")
            all_rest_windows.append((start, end))

    _validate_line_coverage(line_ranges, line_count, blueprint, result)
    _validate_timeline_coverage(timeline_ranges, total_duration_sec, result, tolerance_sec)

    return {
        "block_count": len([b for b in blocks if isinstance(b, dict)]),
        "line_ranges": [
            {"start": start, "end": end, "block_id": block_id}
            for start, end, block_id in line_ranges
        ],
        "active_window_count": len(all_active_windows),
        "rest_window_count": len(all_rest_windows),
        "intent_count": len(intents),
    }


def _resolve_script_blockers_from_subbeats(
    blueprint: dict[str, Any],
    blocks: list[Any],
    result: BackgroundSkitBlueprintValidationResult,
    *,
    tolerance_sec: float,
) -> None:
    if not any(blocker.startswith(SCRIPT_BLOCKER_RE07_TOO_BROAD) for blocker in result.blockers):
        return
    check = _validate_re07_subbeat_authority(
        blueprint,
        blocks,
        tolerance_sec=tolerance_sec,
    )
    if not check["valid"]:
        if check["reason"]:
            result.warnings.append(f"RE07_SUBBEAT_AUTHORITY_MISSING: {check['reason']}")
        return

    result.blockers = [
        blocker
        for blocker in result.blockers
        if not blocker.startswith(SCRIPT_BLOCKER_RE07_TOO_BROAD)
    ]
    result.derived_metrics["resolved_blockers"] = (
        result.derived_metrics.get("resolved_blockers", [])
        + [SCRIPT_BLOCKER_RE07_TOO_BROAD]
    )
    result.derived_metrics["subbeats"] = {
        "re07_authority": check["source"],
        "recognized": check["recognized"],
    }


def _validate_re07_subbeat_authority(
    blueprint: dict[str, Any],
    blocks: list[Any],
    *,
    tolerance_sec: float,
) -> dict[str, Any]:
    parent = _find_block(blocks, "RE-07")
    if parent is None:
        return {"valid": False, "reason": "RE-07 parent block not found", "source": None, "recognized": []}

    parent_line_start = _to_int(parent.get("line_start"))
    parent_line_end = _to_int(parent.get("line_end"))
    parent_start = _to_float(parent.get("block_start_sec"))
    parent_end = _to_float(parent.get("block_end_sec"))
    if (
        parent_line_start is None
        or parent_line_end is None
        or parent_start is None
        or parent_end is None
    ):
        return {"valid": False, "reason": "RE-07 parent range/time incomplete", "source": None, "recognized": []}

    invalid_reason = ""
    for source_name, candidates in _collect_re07_subbeat_candidates(blueprint, parent):
        normalized: list[dict[str, Any]] = []
        for raw in candidates:
            item = _normalize_subbeat(raw)
            if item is None:
                invalid_reason = "subbeat item missing line/time/csv/voice range"
                continue
            if not (parent_line_start <= item["line_start"] <= item["line_end"] <= parent_line_end):
                invalid_reason = "subbeat line range outside RE-07 parent"
                continue
            if item["start_sec"] < parent_start - tolerance_sec or item["end_sec"] > parent_end + tolerance_sec:
                invalid_reason = "subbeat time range outside RE-07 parent"
                continue
            normalized.append(item)

        if not normalized:
            continue
        normalized.sort(key=lambda item: (item["line_start"], item["line_end"]))
        line_ok, line_reason = _covers_range_exactly(
            [(item["line_start"], item["line_end"]) for item in normalized],
            parent_line_start,
            parent_line_end,
        )
        if not line_ok:
            invalid_reason = line_reason
            continue

        time_ok, time_reason = _covers_timeline_exactly(
            [(item["start_sec"], item["end_sec"]) for item in normalized],
            parent_start,
            parent_end,
            tolerance_sec,
        )
        if not time_ok:
            invalid_reason = time_reason
            continue

        return {
            "valid": True,
            "reason": "",
            "source": source_name,
            "recognized": normalized,
        }

    return {
        "valid": False,
        "reason": invalid_reason or "no official RE-07 subbeats in blueprint or row_time_map",
        "source": None,
        "recognized": [],
    }


def _find_block(blocks: list[Any], block_id: str) -> dict[str, Any] | None:
    for raw in blocks:
        if isinstance(raw, dict) and str(raw.get("block_id")) == block_id:
            return raw
    return None


def _collect_re07_subbeat_candidates(
    blueprint: dict[str, Any],
    parent: dict[str, Any],
) -> list[tuple[str, list[Any]]]:
    candidates: list[tuple[str, list[Any]]] = []
    parent_subbeats = _as_list(parent.get("subbeats"))
    if parent_subbeats:
        candidates.append(("blueprint.blocks.RE-07.subbeats", parent_subbeats))

    top_level_subbeats = [
        item
        for item in _as_list(blueprint.get("subbeats"))
        if isinstance(item, dict) and str(item.get("parent_block_id") or item.get("block_id")) == "RE-07"
    ]
    if top_level_subbeats:
        candidates.append(("blueprint.subbeats", top_level_subbeats))

    row_time_map = _load_row_time_map(blueprint)
    if row_time_map:
        subbeats = _as_list(row_time_map.get("re07_subbeat_time_map"))
        if subbeats:
            candidates.append(("row_time_map.re07_subbeat_time_map", subbeats))
    return candidates


def _load_row_time_map(blueprint: dict[str, Any]) -> dict[str, Any]:
    raw = blueprint.get("row_time_map")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        path = Path(raw)
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                return {}
            return data if isinstance(data, dict) else {}
    return {}


def _normalize_subbeat(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    line_start = _to_int(raw.get("line_start"))
    line_end = _to_int(raw.get("line_end"))
    start_sec = _to_float(raw.get("start_sec", raw.get("block_start_sec")))
    end_sec = _to_float(raw.get("end_sec", raw.get("block_end_sec")))
    csv_row_start = _to_int(raw.get("csv_row_start"))
    csv_row_end = _to_int(raw.get("csv_row_end"))
    voice_index_start = _to_int(raw.get("voice_index_start"))
    voice_index_end = _to_int(raw.get("voice_index_end"))
    if None in (
        line_start,
        line_end,
        start_sec,
        end_sec,
        csv_row_start,
        csv_row_end,
        voice_index_start,
        voice_index_end,
    ):
        return None
    if (
        line_start > line_end
        or start_sec >= end_sec
        or csv_row_start > csv_row_end
        or voice_index_start > voice_index_end
    ):
        return None
    return {
        "id": str(raw.get("id") or raw.get("subbeat_id") or f"lines-{line_start}-{line_end}"),
        "line_start": line_start,
        "line_end": line_end,
        "csv_row_start": csv_row_start,
        "csv_row_end": csv_row_end,
        "voice_index_start": voice_index_start,
        "voice_index_end": voice_index_end,
        "start_sec": round(start_sec, 6),
        "end_sec": round(end_sec, 6),
        "duration_sec": round(end_sec - start_sec, 6),
    }


def _covers_range_exactly(
    ranges: list[tuple[int, int]],
    expected_start: int,
    expected_end: int,
) -> tuple[bool, str]:
    cursor = expected_start
    for start, end in sorted(ranges):
        if start != cursor:
            return False, f"subbeat line coverage gap before {cursor}: got {start}"
        cursor = end + 1
    if cursor != expected_end + 1:
        return False, f"subbeat line coverage ends at {cursor - 1}, expected {expected_end}"
    return True, ""


def _covers_timeline_exactly(
    ranges: list[tuple[float, float]],
    expected_start: float,
    expected_end: float,
    tolerance_sec: float,
) -> tuple[bool, str]:
    ranges = sorted(ranges)
    if not ranges:
        return False, "subbeat time coverage missing"
    if abs(ranges[0][0] - expected_start) > tolerance_sec:
        return False, f"subbeat time starts at {ranges[0][0]:.3f}, expected {expected_start:.3f}"
    previous_end = ranges[0][1]
    for start, end in ranges[1:]:
        if abs(start - previous_end) > tolerance_sec:
            return False, f"subbeat time gap/overlap {previous_end:.3f}-{start:.3f}"
        previous_end = end
    if abs(previous_end - expected_end) > tolerance_sec:
        return False, f"subbeat time ends at {previous_end:.3f}, expected {expected_end:.3f}"
    return True, ""


def _validate_line_coverage(
    line_ranges: list[tuple[int, int, str]],
    line_count: int,
    blueprint: dict[str, Any],
    result: BackgroundSkitBlueprintValidationResult,
) -> None:
    covered: set[int] = set()
    for start, end, block_id in line_ranges:
        for line_no in range(start, end + 1):
            if line_no in covered:
                result.errors.append(f"LINE_RANGE_OVERLAP: line {line_no} in {block_id}")
            covered.add(line_no)

    explained = _explained_line_gaps(blueprint)
    unexplained = [
        line_no
        for line_no in range(1, line_count + 1)
        if line_no not in covered and line_no not in explained
    ]
    if unexplained:
        result.errors.append(
            "SCRIPT_LINE_GAP_UNEXPLAINED: "
            f"{_compact_line_ranges(unexplained)}"
        )


def _validate_timeline_coverage(
    ranges: list[tuple[float, float, str]],
    total_duration_sec: float | None,
    result: BackgroundSkitBlueprintValidationResult,
    tolerance_sec: float,
) -> None:
    if not ranges or total_duration_sec is None:
        return
    ranges = sorted(ranges)
    if abs(ranges[0][0]) > tolerance_sec:
        result.errors.append(f"BLOCK_TIMELINE_GAP: starts at {ranges[0][0]:.3f} sec")
    previous_end = ranges[0][1]
    for start, end, block_id in ranges[1:]:
        if start < previous_end - tolerance_sec:
            result.errors.append(f"BLOCK_TIMELINE_OVERLAP: {block_id}")
        elif start > previous_end + tolerance_sec:
            result.errors.append(
                f"BLOCK_TIMELINE_GAP: {previous_end:.3f}-{start:.3f} sec before {block_id}"
            )
        previous_end = max(previous_end, end)
    if abs(previous_end - total_duration_sec) > tolerance_sec:
        result.errors.append(
            "TOTAL_DURATION_COVERAGE_MISMATCH: "
            f"last_block_end={previous_end:.3f} total={total_duration_sec:.3f}"
        )


def _validate_density_thresholds(
    blueprint: dict[str, Any],
    density: dict[str, float],
    result: BackgroundSkitBlueprintValidationResult,
) -> None:
    thresholds = _as_dict(blueprint.get("density_thresholds"))
    for field_name in DENSITY_THRESHOLDS_REQUIRED:
        if field_name not in thresholds:
            result.errors.append(f"DENSITY_THRESHOLD_MISSING: {field_name}")

    minimum_coverage = _to_float(thresholds.get("minimum_active_visual_coverage_pct"))
    if minimum_coverage is not None and density["active_visual_coverage_pct"] < minimum_coverage:
        result.errors.append(
            "DENSITY_THRESHOLD_FAILED: "
            f"active_visual_coverage_pct {density['active_visual_coverage_pct']:.3f}"
            f" < {minimum_coverage:g}"
        )
    max_gap = _to_float(thresholds.get("maximum_unexplained_gap_sec"))
    if max_gap is not None and density["longest_unexplained_gap_sec"] > max_gap:
        result.errors.append(
            "DENSITY_THRESHOLD_FAILED: "
            f"longest_unexplained_gap_sec {density['longest_unexplained_gap_sec']:.3f}"
            f" > {max_gap:g}"
        )
    max_repeat = _to_float(thresholds.get("maximum_repeated_motion_ratio"))
    if max_repeat is not None and density["repeated_motion_ratio"] > max_repeat:
        result.errors.append(
            "DENSITY_THRESHOLD_FAILED: "
            f"repeated_motion_ratio {density['repeated_motion_ratio']:.3f} > {max_repeat:g}"
        )
    states_range = thresholds.get("visual_states_per_min_range")
    if isinstance(states_range, list) and len(states_range) == 2:
        lower = _to_float(states_range[0])
        upper = _to_float(states_range[1])
        if lower is not None and density["visual_states_per_min"] < lower:
            result.errors.append(
                "DENSITY_THRESHOLD_FAILED: "
                f"visual_states_per_min {density['visual_states_per_min']:.3f} < {lower:g}"
            )
        if upper is not None and density["visual_states_per_min"] > upper:
            result.errors.append(
                "DENSITY_THRESHOLD_FAILED: "
                f"visual_states_per_min {density['visual_states_per_min']:.3f} > {upper:g}"
            )


def _validate_declared_density(
    blueprint: dict[str, Any],
    density: dict[str, float],
    result: BackgroundSkitBlueprintValidationResult,
    *,
    tolerance_sec: float,
) -> None:
    audit = _as_dict(blueprint.get("density_audit"))
    if not audit:
        return
    mappings = {
        "active_visual_coverage_pct": 0.01,
        "unexplained_empty_duration_sec": tolerance_sec,
        "longest_unexplained_gap_sec": tolerance_sec,
        "visual_states_per_min": 0.01,
    }
    for field_name, tolerance in mappings.items():
        declared = _to_float(audit.get(field_name))
        if declared is None:
            continue
        actual = density[field_name]
        if abs(declared - actual) > tolerance:
            result.errors.append(
                "DENSITY_AUDIT_MISMATCH: "
                f"{field_name} declared={declared:.3f} actual={actual:.3f}"
            )


def _compute_density_metrics(blocks: list[Any], total_duration_sec: float) -> dict[str, float]:
    active_windows: list[tuple[float, float]] = []
    rest_windows: list[tuple[float, float]] = []
    block_ranges: list[tuple[float, float]] = []
    intents: list[str] = []
    visual_states: list[str] = []
    for raw_block in blocks:
        if not isinstance(raw_block, dict):
            continue
        block_start = _to_float(raw_block.get("block_start_sec"))
        block_end = _to_float(raw_block.get("block_end_sec"))
        if block_start is not None and block_end is not None and block_start < block_end:
            block_ranges.append((block_start, block_end))
        if isinstance(raw_block.get("intent"), str) and raw_block.get("intent"):
            intents.append(raw_block["intent"])
        if isinstance(raw_block.get("visual_state"), str) and raw_block.get("visual_state"):
            visual_states.append(raw_block["visual_state"])
        for window in _as_list(raw_block.get("skit_active_windows")):
            parsed = _parse_window(window)
            if parsed:
                active_windows.append(parsed)
        for window in _as_list(raw_block.get("rest_windows")):
            parsed = _parse_window(window)
            if parsed:
                rest_windows.append(parsed)

    active_duration = _interval_duration(_merge_intervals(active_windows))
    rest_duration = _interval_duration(_merge_intervals(rest_windows))
    unexplained_intervals = _unexplained_intervals(block_ranges, active_windows + rest_windows)
    unexplained_duration = _interval_duration(unexplained_intervals)
    longest_gap = max((end - start for start, end in unexplained_intervals), default=0.0)
    if intents:
        max_repeat = max(intents.count(intent) for intent in set(intents))
        repeated_ratio = max_repeat / len(intents)
    else:
        repeated_ratio = 0.0
    visual_states_per_min = len(visual_states) / (total_duration_sec / 60.0) if total_duration_sec else 0.0
    coverage = (active_duration / total_duration_sec * 100.0) if total_duration_sec else 0.0
    return {
        "active_visual_duration_sec": round(active_duration, 6),
        "active_visual_coverage_pct": round(coverage, 6),
        "intentional_rest_duration_sec": round(rest_duration, 6),
        "unexplained_empty_duration_sec": round(unexplained_duration, 6),
        "longest_unexplained_gap_sec": round(longest_gap, 6),
        "visual_states_per_min": round(visual_states_per_min, 6),
        "repeated_motion_ratio": round(repeated_ratio, 6),
    }


def _load_ymmp_total_duration_sec(path: Path, fps: float) -> float:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ends: list[float] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            frame = _to_float(value.get("Frame", value.get("StartFrame")))
            length = _to_float(value.get("Length"))
            end_frame = _to_float(value.get("EndFrame"))
            if frame is not None and length is not None:
                ends.append(frame + length)
            elif end_frame is not None:
                ends.append(end_frame)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    if not ends:
        raise ValueError("YMM4_TIMING_EMPTY: no Frame/Length or EndFrame values found")
    return max(ends) / fps


def _explained_line_gaps(blueprint: dict[str, Any]) -> set[int]:
    diagnostic = _as_dict(blueprint.get("script_diagnostic"))
    explained: set[int] = set()
    for gap in _as_list(diagnostic.get("explained_line_gaps")):
        if not isinstance(gap, dict) or not _has_value(gap.get("reason")):
            continue
        start = _to_int(gap.get("line_start"))
        end = _to_int(gap.get("line_end"))
        if start is None or end is None:
            continue
        explained.update(range(start, end + 1))
    return explained


def _compact_line_ranges(lines: list[int]) -> str:
    ranges: list[str] = []
    start = previous = lines[0]
    for line_no in lines[1:]:
        if line_no == previous + 1:
            previous = line_no
            continue
        ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
        start = previous = line_no
    ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
    return ", ".join(ranges)


def _unexplained_intervals(
    block_ranges: list[tuple[float, float]],
    explained_windows: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    explained = _merge_intervals(explained_windows)
    unexplained: list[tuple[float, float]] = []
    for block_start, block_end in _merge_intervals(block_ranges):
        cursor = block_start
        for start, end in explained:
            if end <= block_start or start >= block_end:
                continue
            clipped_start = max(start, block_start)
            clipped_end = min(end, block_end)
            if clipped_start > cursor:
                unexplained.append((cursor, clipped_start))
            cursor = max(cursor, clipped_end)
        if cursor < block_end:
            unexplained.append((cursor, block_end))
    return unexplained


def _merge_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    cleaned = sorted((start, end) for start, end in intervals if start < end)
    if not cleaned:
        return []
    merged = [cleaned[0]]
    for start, end in cleaned[1:]:
        previous_start, previous_end = merged[-1]
        if start <= previous_end:
            merged[-1] = (previous_start, max(previous_end, end))
        else:
            merged.append((start, end))
    return merged


def _interval_duration(intervals: list[tuple[float, float]]) -> float:
    return sum(end - start for start, end in intervals)


def _parse_window(raw: Any) -> tuple[float, float] | None:
    if not isinstance(raw, dict):
        return None
    start = _to_float(raw.get("start_sec"))
    end = _to_float(raw.get("end_sec"))
    if start is None or end is None or start >= end:
        return None
    return start, end


def _has_timing_blocker(blockers: list[str]) -> bool:
    for blocker in blockers:
        if any(blocker.startswith(code) for code in TIMING_BLOCKER_CODES):
            return True
    return False


def _assign_next_actions(result: BackgroundSkitBlueprintValidationResult) -> None:
    if result.errors:
        result.allowed_next_actions = []
        result.forbidden_next_actions = list(NEXT_ACTIONS)
        return

    if not result.blockers:
        result.allowed_next_actions = [
            "overlay_only_compact_review",
            "cast_motion_ir",
        ]
        result.forbidden_next_actions = [
            "ymm4_creative_acceptance",
            "production_timing",
        ]
        return

    has_script_or_timing_blocker = any(
        blocker.startswith("SCRIPT_BLOCKED")
        or blocker.startswith("SCRIPT_SOURCE")
        or any(blocker.startswith(code) for code in TIMING_BLOCKER_CODES)
        for blocker in result.blockers
    )
    has_asset_or_cast_blocker = any(
        blocker.startswith("ASSET_BLOCKED")
        or blocker.startswith("CAST_BLOCKED")
        or "CAST_TEMPLATES_MISSING" in blocker
        or "PROPS_MISSING" in blocker
        for blocker in result.blockers
    )

    if has_asset_or_cast_blocker and not has_script_or_timing_blocker:
        result.allowed_next_actions = ["overlay_only_compact_review"]
        result.forbidden_next_actions = [
            "cast_motion_ir",
            "ymm4_creative_acceptance",
            "production_timing",
        ]
        return

    result.allowed_next_actions = []
    result.forbidden_next_actions = list(NEXT_ACTIONS)


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, (str, int, float))]
    if isinstance(value, str) and value:
        return [value]
    return []


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _to_float(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _to_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None

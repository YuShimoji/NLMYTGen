#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_PATH = REPO_ROOT / ".agent" / "state.json"


class GateInputError(RuntimeError):
    pass


def resolve_repo_path(path_value: str | Path, *, must_exist: bool = False) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    resolved = path.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise GateInputError(f"path is outside this repo: {path_value}") from exc
    if must_exist and not resolved.exists():
        raise GateInputError(f"path does not exist: {path_value}")
    return resolved


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise GateInputError(f"JSON root must be an object: {path}")
    return data


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _schema_path_from_state(state: dict[str, Any]) -> Path:
    schema_path = state.get("worker_report_schema", ".agent/schemas/worker_report.schema.json")
    if not isinstance(schema_path, str):
        raise GateInputError("worker_report_schema must be a string")
    return resolve_repo_path(schema_path, must_exist=True)


def _validate_schema_document(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("type") != "object":
        errors.append("schema root type must be object")
    if not isinstance(schema.get("required"), list):
        errors.append("schema required must be an array")
    if not isinstance(schema.get("properties"), dict):
        errors.append("schema properties must be an object")
    return errors


def _json_type_matches(value: Any, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return (isinstance(value, int | float)) and not isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def _validate_schema_value(field: str, value: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not _json_type_matches(value, expected_type):
        errors.append(f"{field} must be {expected_type}")
        return errors

    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and value not in enum_values:
        enum_text = ", ".join(str(item) for item in enum_values)
        errors.append(f"{field} must be one of: {enum_text}")

    if expected_type == "array":
        item_schema = schema.get("items", {})
        if not isinstance(item_schema, dict):
            item_schema = {}
        for index, item in enumerate(value):
            errors.extend(_validate_schema_value(f"{field}[{index}]", item, item_schema))

    return errors


def validate_report_against_schema(report: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_errors = _validate_schema_document(schema)
    if schema_errors:
        raise GateInputError("; ".join(schema_errors))

    required = _string_list(schema.get("required"))
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}

    for field in required:
        if field not in report:
            errors.append(f"missing required field: {field}")

    if schema.get("additionalProperties") is False:
        for field in sorted(set(report) - set(properties)):
            errors.append(f"additional property is not allowed: {field}")

    for field, value in report.items():
        field_schema = properties.get(field)
        if isinstance(field_schema, dict):
            errors.extend(_validate_schema_value(field, value, field_schema))

    return errors


def _normalize_report_path(path_value: str) -> str | None:
    text = str(path_value).strip().replace("\\", "/")
    if not text:
        return None
    if re.match(r"^[A-Za-z]:", text) or text.startswith("/"):
        return None
    parts: list[str] = []
    for part in text.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            return None
        parts.append(part)
    if not parts:
        return None
    return "/".join(parts)


def _normalize_allowed_prefix(prefix: str) -> str | None:
    normalized = _normalize_report_path(prefix)
    if normalized is None:
        return None
    if str(prefix).replace("\\", "/").endswith("/"):
        return f"{normalized}/"
    return normalized


def _path_is_allowed(path_value: str, allowed_prefixes: list[str]) -> bool:
    normalized = _normalize_report_path(path_value)
    if normalized is None:
        return False

    for raw_prefix in allowed_prefixes:
        prefix = _normalize_allowed_prefix(raw_prefix)
        if prefix is None:
            continue
        if prefix.endswith("/"):
            if normalized.startswith(prefix):
                return True
        elif normalized == prefix or normalized.startswith(f"{prefix}/"):
            return True
    return False


def _load_gate_policy(state: dict[str, Any]) -> dict[str, list[str]]:
    policy = state.get("gate_policy", {})
    if not isinstance(policy, dict):
        policy = {}
    return {
        "allowed_changed_path_prefixes": _string_list(
            policy.get("allowed_changed_path_prefixes", state.get("allowed_changed_path_prefixes", []))
        ),
        "blocked_changed_path_prefixes": _string_list(policy.get("blocked_changed_path_prefixes", [])),
        "blocked_changed_path_patterns": _string_list(policy.get("blocked_changed_path_patterns", [])),
        "risk_keywords": _string_list(policy.get("risk_keywords", state.get("risk_keywords", []))),
    }


def _blocked_path_reasons(path_value: str, policy: dict[str, list[str]]) -> list[str]:
    normalized = _normalize_report_path(path_value)
    if normalized is None:
        return [f"changed_file_invalid_or_external:{path_value}"]

    reasons: list[str] = []
    for raw_prefix in policy["blocked_changed_path_prefixes"]:
        prefix = _normalize_allowed_prefix(raw_prefix)
        if prefix is None:
            continue
        if prefix.endswith("/") and normalized.startswith(prefix):
            reasons.append(f"changed_file_blocked_prefix:{raw_prefix}:{path_value}")
        elif normalized == prefix or normalized.startswith(f"{prefix}/"):
            reasons.append(f"changed_file_blocked_prefix:{raw_prefix}:{path_value}")

    for pattern in policy["blocked_changed_path_patterns"]:
        try:
            if re.search(pattern, normalized, flags=re.IGNORECASE):
                reasons.append(f"changed_file_blocked_pattern:{pattern}:{path_value}")
        except re.error as exc:
            reasons.append(f"policy_invalid_blocked_pattern:{pattern}:{exc}")

    if not _path_is_allowed(normalized, policy["allowed_changed_path_prefixes"]):
        reasons.append(f"changed_file_out_of_scope:{path_value}")
    return reasons


def evaluate_report(report_path: str | Path, state_path: str | Path = DEFAULT_STATE_PATH) -> dict[str, Any]:
    resolved_report_path = resolve_repo_path(report_path, must_exist=True)
    resolved_state_path = resolve_repo_path(state_path, must_exist=True)
    report = load_json(resolved_report_path)
    state = load_json(resolved_state_path)
    schema_path = _schema_path_from_state(state)
    schema = load_json(schema_path)
    policy = _load_gate_policy(state)

    reasons: list[str] = []
    validation_errors = validate_report_against_schema(report, schema)
    reasons.extend(f"invalid_report:{error}" for error in validation_errors)

    severity = report.get("severity")
    if severity in {"P1", "P0"}:
        reasons.append(f"severity:{severity}")

    status = report.get("status")
    if status in {"needs_human", "blocked"}:
        reasons.append(f"status:{status}")

    tests_status = report.get("tests_status")
    if tests_status == "failed":
        reasons.append("tests_status:failed")

    lowered_keywords = [keyword.lower() for keyword in policy["risk_keywords"]]
    for risk in report.get("risks", []) if isinstance(report.get("risks"), list) else []:
        lowered_risk = risk.lower()
        for keyword in lowered_keywords:
            if keyword and keyword in lowered_risk:
                reasons.append(f"risk_keyword:{keyword}")

    for changed_file in report.get("changed_files", []) if isinstance(report.get("changed_files"), list) else []:
        reasons.extend(_blocked_path_reasons(changed_file, policy))

    needs_human = bool(reasons)
    try:
        display_report_path = resolved_report_path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        display_report_path = str(resolved_report_path)

    return {
        "decision": "needs_human" if needs_human else str(status or "pass"),
        "needs_human": needs_human,
        "reasons": reasons,
        "report_path": display_report_path,
        "schema_path": schema_path.relative_to(REPO_ROOT).as_posix(),
        "lane": report.get("lane", ""),
        "status": report.get("status", ""),
        "severity": report.get("severity", ""),
        "tests_status": report.get("tests_status", ""),
        "summary": report.get("summary", ""),
        "next_recommended_worker": report.get("next_recommended_worker", ""),
        "human_question": report.get("human_question", ""),
        "copyable_next_prompt": report.get("copyable_next_prompt", ""),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an NLMYTGen worker report.")
    parser.add_argument("report", help="Worker report JSON path inside this repo.")
    parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE_PATH.relative_to(REPO_ROOT)),
        help="Agent state JSON path inside this repo.",
    )
    args = parser.parse_args(argv)

    try:
        result = evaluate_report(args.report, args.state)
    except (GateInputError, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "error", "needs_human": True, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

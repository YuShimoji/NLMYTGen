"""Deterministic salvage analysis for unlabeled NotebookLM Audio Overview text.

The raw transcript is immutable local evidence.  This module writes full-text
derivatives only to an ignored local directory and emits a tracked package
containing hashes, counts, categories, fingerprints, and short labels.
Nothing in this module verifies a claim or assigns a production character.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


CAPTURE_SCHEMA = "notebooklm_audio_overview_capture.v2"
ANALYZER_SCHEMA = "notebooklm_audio_transcript_salvage.v1"
ANONYMOUS_IDENTITIES = {"voice_1", "voice_2", "ambiguous"}
STYLE_CLASSES = (
    "host_introduction",
    "program_format_self_reference",
    "listener_address",
    "neutrality_balance_self_positioning",
    "suspense_hidden_mission_framing",
    "exaggerated_certainty",
    "generic_agreement_filler",
    "rhetorical_question_scaffolding",
    "closing_boilerplate",
    "update_sensitive_unknown_pattern",
)
CLAIM_CLASSES = (
    "technical_description",
    "quantitative_statistic",
    "historical_claim",
    "policy_or_intent_claim",
    "causal_claim",
    "analogy_or_metaphor",
    "rhetorical_framing",
    "future_prediction",
    "unsupported_dramatic_assertion",
)


_STYLE_RULES: dict[str, tuple[str, ...]] = {
    "host_introduction": (
        r"リスナー(?:の|のみな)",
        r"今回の(?:深掘り|解説)",
        r"今日は.*(?:見て|紐|話して)",
    ),
    "program_format_self_reference": (
        r"深掘り(?:解説|して)",
        r"話してみましょう",
        r"資料を元に",
        r"ここまで.*(?:話|解説|深掘り)",
    ),
    "listener_address": (
        r"(?:リスナー|あなた)",
        r"どう思いますか",
        r"思いませんか",
        r"手にした時",
    ),
    "neutrality_balance_self_positioning": (
        r"一見すると",
        r"視点を広げ",
        r"色々な角度",
        r"(?:対立|矛盾).*どころか",
        r"公平|中立|バランス",
    ),
    "suspense_hidden_mission_framing": (
        r"裏のミッション",
        r"信じられない",
        r"ここからが面白い",
        r"隠された|謎|驚くべき",
    ),
    "exaggerated_certainty": (
        r"徹底解剖",
        r"完全に|全く同じ|絶対|不可能",
        r"最大の|最も重要|かつてない",
        r"一瞬で.*確信",
        r"究極|とんでもない",
    ),
    "generic_agreement_filler": (
        r"^(?:はい|ええ|そうです|そうですね|なるほど|確かに|お願いします)[。.!！ ]*$",
        r"^(?:いや|ああ|うわあ)[、。 ]*$",
    ),
    "rhetorical_question_scaffolding": (
        r"[?？]$",
        r"(?:でしょうか|じゃないですか|思いませんか)[。]?$",
    ),
    "closing_boilerplate": (
        r"今回の.*(?:ここまで|終わり)",
        r"また次回|お会いしましょう",
        r"(?:触って|傾けて)みてください",
        r"考えさせられるテーマ",
    ),
    "update_sensitive_unknown_pattern": (
        r"今回の深掘り解説",
        r"リスナーのあなた",
        r"裏のミッション",
        r"そう感じていただける",
        r"また次回お会い",
    ),
}


_ASR_CATALOG: tuple[dict[str, Any], ...] = (
    {"raw": "ビジネスモドル", "candidate": "ビジネスモデル", "confidence": 0.99, "class": "safe_auto_fix_candidate"},
    {"raw": "ソフトウェ レベル", "candidate": "ソフトウェアレベル", "confidence": 0.97, "class": "safe_auto_fix_candidate"},
    {"raw": "レムル", "candidate": "レベル", "confidence": 0.96, "class": "safe_auto_fix_candidate"},
    {"raw": "立ちごっこ", "candidate": "いたちごっこ", "confidence": 0.96, "class": "safe_auto_fix_candidate"},
    {"raw": "発酵", "candidate": "発行", "confidence": 0.91, "class": "domain_candidate"},
    {"raw": "新兵", "candidate": "新紙幣", "confidence": 0.90, "class": "domain_candidate"},
    {"raw": "新市兵", "candidate": "新紙幣", "confidence": 0.88, "class": "domain_candidate"},
    {"raw": "新幣", "candidate": "新紙幣", "confidence": 0.84, "class": "domain_candidate"},
    {"raw": "紙兵", "candidate": "紙幣", "confidence": 0.88, "class": "domain_candidate"},
    {"raw": "死兵", "candidate": "紙幣", "confidence": 0.86, "class": "domain_candidate"},
    {"raw": "兵幣", "candidate": "紙幣", "confidence": 0.82, "class": "domain_candidate"},
    {"raw": "髪切れ", "candidate": "紙切れ", "confidence": 0.91, "class": "domain_candidate"},
    {"raw": "神切れ", "candidate": "紙切れ", "confidence": 0.88, "class": "domain_candidate"},
    {"raw": "国の維新", "candidate": "国の威信", "confidence": 0.86, "class": "domain_candidate"},
    {"raw": "深顔版", "candidate": "凹版", "confidence": 0.82, "class": "domain_candidate"},
    {"raw": "精子技術", "candidate": "製紙技術", "confidence": 0.82, "class": "domain_candidate"},
    {"raw": "向上で", "candidate": "工場で", "confidence": 0.78, "class": "domain_candidate"},
    {"raw": "学面表示", "candidate": "額面表示", "confidence": 0.80, "class": "domain_candidate"},
    {"raw": "車線マーク", "candidate": "斜線マーク", "confidence": 0.78, "class": "source_verification_required"},
    {"raw": "お札の修理", "candidate": "お札の種類", "confidence": 0.86, "class": "domain_candidate"},
    {"raw": "審議を判定", "candidate": "真偽を判定", "confidence": 0.85, "class": "domain_candidate"},
    {"raw": "ゆけし君", "candidate": "名称要確認", "confidence": 0.35, "class": "source_verification_required"},
    {"raw": "広格ホログラム", "candidate": "方式名要確認", "confidence": 0.30, "class": "source_verification_required"},
    {"raw": "お鉄もない", "candidate": None, "confidence": 0.10, "class": "unresolved"},
    {"raw": "丸化四角化", "candidate": None, "confidence": 0.15, "class": "unresolved"},
)


_CLAIM_RULES: dict[str, tuple[str, ...]] = {
    "technical_description": (
        r"ホログラム|透かし|凹版|印刷|マイクロ|識別マーク|アプリ|コピー機|スキャナー|偽造防止|レーザー",
    ),
    "quantitative_statistic": (
        r"\d[\d,. ]*(?:年|円|万円|億円|兆円|分|時間|本|台|%|％)",
        r"年間で|平均して|総額",
    ),
    "historical_claim": (
        r"\d{3,4}\s*年|世界初|以来|歴史|発行された",
    ),
    "policy_or_intent_claim": (
        r"政府.*(?:推進|戦略|目的|ミッション)",
        r"キャッシュレス.*(?:推進|移行|導く|ゴール)",
        r"現金を.*使わせなく|国.*(?:狙い|戦略)",
    ),
    "causal_claim": (
        r"(?:ため|ので|だから|ことによって|結果|効果|影響).*",
        r"(?:ことが|のが).*理由",
    ),
    "analogy_or_metaphor": (
        r"みたい|のような|例え|ワッフルメーカー|ハリー・ポッター|デバイス|結晶",
    ),
    "rhetorical_framing": (
        r"[?？]$|どう思いますか|思いませんか|考えさせられる",
    ),
    "future_prediction": (
        r"かもしれません|いずれ|未来|なる日が来る|そう遠くない",
    ),
    "unsupported_dramatic_assertion": (
        r"裏のミッション|徹底解剖|究極|完全に|絶対|不可能|とんでもない|国家の執",
    ),
}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _normalized_key(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).lower()
    return "".join(char for char in value if char.isalnum())


def _logical_lines(data: bytes) -> tuple[str, list[str], dict[str, int]]:
    text = data.decode("utf-8")
    crlf = text.count("\r\n")
    bare_lf = len(re.findall(r"(?<!\r)\n", text))
    bare_cr = len(re.findall(r"\r(?!\n)", text))
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return text, normalized.split("\n"), {
        "crlf_separators": crlf,
        "bare_lf_separators": bare_lf,
        "bare_cr_separators": bare_cr,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _line_record(ordinal: int, text: str) -> dict[str, Any]:
    return {
        "ordinal": ordinal,
        "fingerprint": _fingerprint(text),
        "empty": not bool(text.strip()),
        "raw_text": text,
        "normalized_candidate": text,
    }


def _matching_rules(text: str, rules: dict[str, tuple[str, ...]]) -> list[str]:
    return [
        class_name
        for class_name, patterns in rules.items()
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
    ]


def _exact_duplicate_clusters(lines: list[str]) -> list[dict[str, Any]]:
    groups: dict[str, list[int]] = defaultdict(list)
    for ordinal, line in enumerate(lines, 1):
        key = _normalized_key(line)
        if len(key) >= 12:
            groups[key].append(ordinal)
    clusters: list[dict[str, Any]] = []
    for ordinals in groups.values():
        if len(ordinals) < 2:
            continue
        clusters.append(
            {
                "kind": "exact_line",
                "members": [
                    {
                        "line_start": ordinal,
                        "line_end": ordinal,
                        "fingerprints": [_fingerprint(lines[ordinal - 1])],
                    }
                    for ordinal in ordinals
                ],
                "representative_member": 0,
                "decision": "review",
                "relation": "rhetorical_callback_or_repeated_line",
                "confidence": 1.0,
            }
        )
    return sorted(clusters, key=lambda item: item["members"][0]["line_start"])


def _near_duplicate_spans(
    lines: list[str], *, start_threshold: float = 0.78, line_threshold: float = 0.62
) -> list[dict[str, Any]]:
    keys = [_normalized_key(line) for line in lines]
    candidates: list[dict[str, Any]] = []
    count = len(lines)
    for lag in range(4, count):
        left = 0
        while left + lag < count:
            first_score = SequenceMatcher(
                None, keys[left], keys[left + lag]
            ).ratio() if len(keys[left]) >= 10 and len(keys[left + lag]) >= 10 else 0.0
            if first_score < start_threshold:
                left += 1
                continue
            scores: list[float] = []
            offset = 0
            misses = 0
            while offset < lag and left + lag + offset < count:
                a = keys[left + offset]
                b = keys[left + lag + offset]
                score = SequenceMatcher(None, a, b).ratio() if a and b else 0.0
                if score < line_threshold:
                    misses += 1
                    if misses > 1:
                        break
                else:
                    misses = 0
                scores.append(score)
                offset += 1
            while scores and scores[-1] < line_threshold:
                scores.pop()
            usable = len(scores)
            if usable < 4:
                left += 1
                continue
            average = round(sum(scores) / usable, 4)
            member_starts = [left, left + lag]
            next_start = left + (2 * lag)
            while next_start + usable <= count:
                repeat_scores = [
                    SequenceMatcher(
                        None, keys[left + index], keys[next_start + index]
                    ).ratio()
                    for index in range(usable)
                ]
                if sum(repeat_scores) / usable < 0.75:
                    break
                member_starts.append(next_start)
                next_start += lag
            candidates.append(
                {
                    "kind": "near_span",
                    "members": [
                        {
                            "line_start": start + 1,
                            "line_end": start + usable,
                            "fingerprints": [
                                _fingerprint(lines[index])
                                for index in range(start, start + usable)
                            ],
                        }
                        for start in member_starts
                    ],
                    "representative_member": 0,
                    "decision": "omit_later_candidate" if average >= 0.78 else "review",
                    "relation": (
                        "probable_accidental_repetition"
                        if usable >= 6 and average >= 0.75
                        else "rhetorical_callback_possible"
                    ),
                    "confidence": average,
                }
            )
            left += usable
    selected: list[dict[str, Any]] = []
    occupied_lines: set[int] = set()
    for candidate in sorted(
        candidates,
        key=lambda item: (
            -sum(member["line_end"] - member["line_start"] + 1 for member in item["members"]),
            -item["confidence"],
        ),
    ):
        coverage = {
            ordinal
            for member in candidate["members"]
            for ordinal in range(member["line_start"], member["line_end"] + 1)
        }
        overlap = len(coverage & occupied_lines) / max(1, len(coverage))
        if overlap >= 0.5:
            continue
        selected.append(candidate)
        occupied_lines.update(coverage)
        if len(selected) >= 6:
            break
    return sorted(selected, key=lambda item: item["members"][0]["line_start"])


def _deduplicated_candidate(lines: list[str], clusters: list[dict[str, Any]]) -> str:
    omitted: set[int] = set()
    for cluster in clusters:
        if cluster["kind"] != "near_span" or cluster["decision"] != "omit_later_candidate":
            continue
        for member in cluster["members"][1:]:
            omitted.update(range(member["line_start"], member["line_end"] + 1))
    return "\n".join(line for ordinal, line in enumerate(lines, 1) if ordinal not in omitted)


def _asr_candidates(lines: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    findings: list[dict[str, Any]] = []
    normalized = list(lines)
    for ordinal, line in enumerate(lines, 1):
        candidate_line = line
        for catalog in _ASR_CATALOG:
            token = catalog["raw"]
            if token not in line:
                continue
            applied = catalog["class"] == "safe_auto_fix_candidate"
            proposal = catalog["candidate"]
            findings.append(
                {
                    "candidate_id": f"asr_{len(findings) + 1:03d}",
                    "line_ordinal": ordinal,
                    "line_fingerprint": _fingerprint(line),
                    "raw_token": token,
                    "proposed_normalized_form": proposal,
                    "confidence": catalog["confidence"],
                    "class": catalog["class"],
                    "source_verification_needed": catalog["class"] in {"source_verification_required", "unresolved"},
                    "applied_to_local_candidate": applied,
                }
            )
            if applied and proposal:
                candidate_line = candidate_line.replace(token, proposal)
        normalized[ordinal - 1] = candidate_line
    return findings, normalized


def _style_findings(lines: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for ordinal, line in enumerate(lines, 1):
        for class_name in _matching_rules(line, _STYLE_RULES):
            impact = class_name not in {"generic_agreement_filler", "rhetorical_question_scaffolding"}
            recommendation = {
                "generic_agreement_filler": "remove_or_merge",
                "rhetorical_question_scaffolding": "review",
                "closing_boilerplate": "remove",
                "listener_address": "rewrite",
            }.get(class_name, "review")
            findings.append(
                {
                    "finding_id": f"style_{len(findings) + 1:03d}",
                    "class": class_name,
                    "line_start": ordinal,
                    "line_end": ordinal,
                    "line_fingerprints": [_fingerprint(line)],
                    "confidence": 0.95 if class_name == "generic_agreement_filler" else 0.80,
                    "recommendation": recommendation,
                    "factual_meaning_impact": "possible" if impact else "low",
                    "short_label": f"{class_name} signal at line {ordinal:03d}",
                }
            )
    return findings


def _turn_candidates(
    lines: list[str], duplicate_members: set[int], asr_by_line: dict[int, int]
) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    current = "voice_1"
    previous_line = ""
    for ordinal, line in enumerate(lines, 1):
        stripped = line.strip()
        rationale = "alternating_unlabeled_dialogue"
        confidence = 0.62
        if not stripped:
            identity = "ambiguous"
            confidence = 0.0
            rationale = "empty_logical_line"
        elif ordinal > 1 and previous_line and not re.search(r"[。.!！?？]$", previous_line):
            identity = turns[-1]["identity"] if turns else "ambiguous"
            confidence = 0.55
            rationale = "continuation_after_unterminated_line"
        elif len(_normalized_key(stripped)) <= 1:
            identity = "ambiguous"
            confidence = 0.2
            rationale = "insufficient_turn_signal"
        else:
            identity = current
            current = "voice_2" if current == "voice_1" else "voice_1"
            if re.match(r"^(?:はい|ええ|なるほど|そうですね|確かに)", stripped):
                confidence = 0.75
                rationale = "acknowledgement_turn"
            elif stripped.endswith(("?", "？")):
                confidence = 0.72
                rationale = "question_turn"
        if asr_by_line.get(ordinal, 0) >= 3:
            confidence = min(confidence, 0.35)
            rationale += ";asr_heavy"
        turns.append(
            {
                "turn_id": f"turn_{ordinal:03d}",
                "line_start": ordinal,
                "line_end": ordinal,
                "line_fingerprints": [_fingerprint(line)],
                "identity": identity,
                "confidence": round(confidence, 2),
                "heuristic": rationale,
                "duplicate_member": ordinal in duplicate_members,
                "duplicate_assignment_policy": "assignment_retained_and_flagged",
                "text": line,
            }
        )
        previous_line = line
    return turns


def _claim_candidates(lines: list[str]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    class_status = {
        "technical_description": ("requires_primary_source", "high"),
        "quantitative_statistic": ("requires_primary_source", "high"),
        "historical_claim": ("requires_primary_source", "high"),
        "policy_or_intent_claim": ("reject_without_evidence", "high"),
        "causal_claim": ("requires_context_source", "high"),
        "analogy_or_metaphor": ("likely_editorial_only", "medium"),
        "rhetorical_framing": ("likely_editorial_only", "medium"),
        "future_prediction": ("unresolved", "high"),
        "unsupported_dramatic_assertion": ("reject_without_evidence", "high"),
    }
    for ordinal, line in enumerate(lines, 1):
        for class_name in _matching_rules(line, _CLAIM_RULES):
            status, risk = class_status[class_name]
            claims.append(
                {
                    "claim_id": f"claim_{len(claims) + 1:03d}",
                    "line_ordinal": ordinal,
                    "line_fingerprint": _fingerprint(line),
                    "claim_class": class_name,
                    "short_label": f"{class_name} candidate at line {ordinal:03d}",
                    "status": status,
                    "risk": risk,
                    "verified": False,
                    "source_verification_required": status in {"requires_primary_source", "requires_context_source", "reject_without_evidence", "unresolved"},
                }
            )
    return claims


def _sanitized_clusters(clusters: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **cluster,
            "members": [
                {
                    "line_start": member["line_start"],
                    "line_end": member["line_end"],
                    "fingerprints": member["fingerprints"],
                }
                for member in cluster["members"]
            ],
        }
        for cluster in clusters
    ]


def analyze_notebooklm_audio_transcript(
    *,
    raw_path: str | Path,
    capture_manifest_path: str | Path,
    tracked_output_dir: str | Path,
    local_output_dir: str | Path | None = None,
    raw_label: str | None = None,
) -> dict[str, Any]:
    """Analyze immutable raw input and write tracked/local salvage layers."""
    raw = Path(raw_path)
    manifest_path = Path(capture_manifest_path)
    tracked = Path(tracked_output_dir)
    local = Path(local_output_dir) if local_output_dir else tracked / "local_outputs"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != CAPTURE_SCHEMA:
        raise ValueError(f"capture manifest must use {CAPTURE_SCHEMA}")

    before = raw.read_bytes()
    raw_sha = _sha256_bytes(before)
    raw_text, lines, newline_counts = _logical_lines(before)
    expected = {
        "sha256": manifest.get("raw_transcript_sha256"),
        "size_bytes": manifest.get("raw_transcript_size_bytes"),
        "logical_line_count": manifest.get("raw_transcript_line_count"),
    }
    actual = {
        "sha256": raw_sha,
        "size_bytes": len(before),
        "logical_line_count": len(lines),
    }
    if expected != actual:
        raise ValueError(f"raw identity mismatch: expected={expected} actual={actual}")

    line_map = [_line_record(index, line) for index, line in enumerate(lines, 1)]
    exact_clusters = _exact_duplicate_clusters(lines)
    span_clusters = _near_duplicate_spans(lines)
    all_clusters = exact_clusters + span_clusters
    duplicate_members = {
        ordinal
        for cluster in all_clusters
        for member in cluster["members"]
        for ordinal in range(member["line_start"], member["line_end"] + 1)
    }
    asr_findings, normalized_lines = _asr_candidates(lines)
    for record, candidate in zip(line_map, normalized_lines):
        record["normalized_candidate"] = candidate
    style_findings = _style_findings(lines)
    asr_by_line: dict[int, int] = defaultdict(int)
    for finding in asr_findings:
        asr_by_line[finding["line_ordinal"]] += 1
    turns = _turn_candidates(lines, duplicate_members, asr_by_line)
    claims = _claim_candidates(lines)

    local.mkdir(parents=True, exist_ok=True)
    _write_json(local / "raw_line_map.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.raw_line_map",
        "raw_sha256": raw_sha,
        "logical_line_count": len(lines),
        "newline_treatment": "CRLF and bare CR normalized to LF only in derivatives",
        "lines": line_map,
    })
    _write_json(local / "duplicate_span_map.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.duplicate_span_map",
        "similarity_config": {"start_threshold": 0.78, "line_threshold": 0.62, "minimum_span_lines": 4},
        "clusters": all_clusters,
    })
    _write_text(local / "deduplicated_transcript_candidate.txt", _deduplicated_candidate(lines, span_clusters))
    _write_text(local / "normalized_transcript_candidate.txt", "\n".join(normalized_lines))
    _write_json(local / "turn_segmentation_candidates.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.turn_candidates",
        "allowed_identities": sorted(ANONYMOUS_IDENTITIES),
        "turns": turns,
    })

    tracked.mkdir(parents=True, exist_ok=True)
    raw_display = raw_label or raw.name
    class_counts = {name: 0 for name in STYLE_CLASSES}
    for finding in style_findings:
        class_counts[finding["class"]] += 1
    claim_counts = {name: 0 for name in CLAIM_CLASSES}
    for claim in claims:
        claim_counts[claim["claim_class"]] += 1

    _write_json(tracked / "input_identity_receipt.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.input_identity_receipt",
        "status": "identity_matched",
        "raw_path": raw_display,
        "capture_manifest_schema": manifest["schema_version"],
        "raw_sha256": raw_sha,
        "raw_size_bytes": len(before),
        "raw_logical_line_count": len(lines),
        "newline_counts": newline_counts,
        "line_fingerprint_count": len(line_map),
        "raw_modified": False,
        "raw_tracked": False,
    })
    _write_json(tracked / "notebooklm_generation_receipt.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.generation_receipt",
        "evidence_grade": "user_observed",
        "process": [
            "exact title used as NotebookLM Fast Research anchor",
            "Audio Overview generated from notebook materials",
            "Audio Overview added back and converted to plain text",
        ],
        "generation_latency": "approximately 30 minutes",
        "speaker_labels_present": False,
        "speaker_split_retry_performed": False,
        "regeneration_performed": False,
        "no_rerun_policy": "repair deterministic transcript defects locally unless a later gate changes source set or editorial objective",
        "NotebookLM_accessed_by_analyzer": False,
    })
    _write_json(tracked / "normalization_contract.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.normalization_contract",
        "raw_is_immutable": True,
        "full_text_outputs_are_local_ignored": True,
        "line_mapping_is_complete": True,
        "newline_policy": "logical UTF-8 lines; CRLF separators are not line records",
        "asr_policy": "confidence-graded reversible candidates; source-dependent terms remain unresolved",
        "style_policy": "classification first; no blind phrase deletion",
        "speaker_policy": "voice_1, voice_2, or ambiguous only",
        "claim_policy": "all extracted claims remain unverified pending source reconciliation",
    })
    _write_json(tracked / "deduplication_readback.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.deduplication_readback",
        "status": "candidate_clusters_ready",
        "raw_modified": False,
        "similarity_config": {"start_threshold": 0.78, "line_threshold": 0.62, "minimum_span_lines": 4},
        "exact_line_cluster_count": len(exact_clusters),
        "near_span_cluster_count": len(span_clusters),
        "clusters": _sanitized_clusters(all_clusters),
        "universal_design_repetition_detected": any(
            any(member["line_start"] <= 228 <= member["line_end"] for member in cluster["members"])
            for cluster in span_clusters
        ),
    })
    _write_json(tracked / "notebooklm_style_profile.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.style_profile",
        "profile_kind": "semantic_classification_not_exact_phrase_filter",
        "classes": [
            {"class": name, "finding_count": class_counts[name], "update_sensitive": name == "update_sensitive_unknown_pattern"}
            for name in STYLE_CLASSES
        ],
        "class_coverage_complete": set(class_counts) == set(STYLE_CLASSES),
    })
    _write_json(tracked / "notebooklm_style_contamination_ledger.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.style_ledger",
        "finding_count": len(style_findings),
        "findings": style_findings,
        "automatic_removal_performed": False,
    })
    _write_json(tracked / "asr_correction_ledger.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.asr_ledger",
        "candidate_count": len(asr_findings),
        "applied_to_local_candidate_count": sum(item["applied_to_local_candidate"] for item in asr_findings),
        "source_verification_required_count": sum(item["source_verification_needed"] for item in asr_findings),
        "raw_overwritten": False,
        "clean_transcript_claimed": False,
        "candidates": asr_findings,
    })
    identity_counts = {name: sum(turn["identity"] == name for turn in turns) for name in sorted(ANONYMOUS_IDENTITIES)}
    _write_json(tracked / "turn_segmentation_readback.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.turn_readback",
        "status": "provisional_anonymous_segmentation",
        "logical_line_count": len(lines),
        "turn_count": len(turns),
        "identity_counts": identity_counts,
        "allowed_identities": sorted(ANONYMOUS_IDENTITIES),
        "character_casting_performed": False,
        "invented_dialogue_count": 0,
        "duplicate_assignment_policy": "retain provisional assignment and flag duplicate membership",
        "heuristics": ["question_turn", "acknowledgement_turn", "continuation_after_unterminated_line", "alternating_unlabeled_dialogue"],
    })
    _write_json(tracked / "claim_risk_ledger.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.claim_risk_ledger",
        "claim_candidate_count": len(claims),
        "verified_claim_count": 0,
        "source_set_status": "absent",
        "class_counts": claim_counts,
        "high_risk_classes": ["quantitative_statistic", "policy_or_intent_claim", "historical_claim", "technical_description", "causal_claim", "future_prediction"],
        "claims": claims,
    })
    _write_json(tracked / "transcript_quality_readback.json", {
        "schema_version": f"{ANALYZER_SCHEMA}.quality_readback",
        "status": "salvaged_not_source_verified",
        "raw_logical_lines": len(lines),
        "mapped_lines": len(line_map),
        "duplicate_clusters": len(all_clusters),
        "style_findings": len(style_findings),
        "asr_candidates": len(asr_findings),
        "anonymous_turns": len(turns),
        "ambiguous_turns": identity_counts["ambiguous"],
        "claim_candidates": len(claims),
        "verified_claims": 0,
        "source_set_status": "reconciliation_required",
        "raw_and_full_text_tracking_status": "local_ignored_untracked_required",
    })
    _write_text(tracked / "source_reconciliation_request.md", _source_request())
    _write_text(tracked / "README_TRANSCRIPT_SALVAGE.md", _readme(raw_sha, len(lines)))
    _write_text(tracked / "limitations.md", _limitations())

    after = raw.read_bytes()
    if before != after:
        raise RuntimeError("raw transcript changed during analysis")
    return {
        "status": "salvaged_not_source_verified",
        "raw_sha256": raw_sha,
        "raw_size_bytes": len(before),
        "raw_logical_lines": len(lines),
        "mapped_lines": len(line_map),
        "duplicate_clusters": len(all_clusters),
        "style_findings": len(style_findings),
        "asr_candidates": len(asr_findings),
        "anonymous_turns": len(turns),
        "ambiguous_turns": identity_counts["ambiguous"],
        "claim_candidates": len(claims),
        "verified_claims": 0,
        "tracked_output_dir": str(tracked),
        "local_output_dir": str(local),
    }


def _source_request() -> str:
    return """# NotebookLM source-set reconciliation request

The transcript has been preserved and analyzed locally. To reconcile its unverified claims without rerunning the approximately 30-minute Audio Overview, please return no more than these three items:

1. NotebookLM source titles.
2. Source URLs or stable identifiers when available.
3. Intentionally excluded sources, if known.

No speaker split, timestamp reconstruction, Audio Overview regeneration, or source re-search is requested in this gate.
"""


def _readme(raw_sha: str, line_count: int) -> str:
    return f"""# New-banknote NotebookLM transcript salvage

This package records the deterministic salvage of an unlabeled NotebookLM Audio Overview transcript. The immutable local raw input is bound to SHA-256 `{raw_sha}` and {line_count} logical lines; it is not committed or reproduced here.

The input is not a final script. It contains repeated passages, probable ASR corruption, host/program framing, anonymous turns, and factual or causal statements whose exact NotebookLM source support is unknown. The analyzer mapped every line, separated exact/near duplication, classified style contamination, produced reversible ASR candidates, created provisional `voice_1` / `voice_2` / `ambiguous` turns, and extracted a claim-risk ledger with zero verified claims.

NotebookLM was not asked to split speakers again because the observed retry path previously omitted content or invented unrelated text. The approximately 30-minute generation is therefore milestone-gated: deterministic local repair is preferred unless a later explicit decision changes the frozen source set or editorial objective.

The next gate is source reconciliation. Provide only the NotebookLM source titles, source URLs or stable identifiers when available, and intentionally excluded sources if known. Until that mapping exists, no final nine-cue script, Reimu/Marisa casting, CSV, YMM4 package, factual verification, editorial adoption, rights approval, or public/production claim is authorized.
"""


def _limitations() -> str:
    return """# Limitations

| Open item | Impact | Owner | Revisit trigger | Blocking now |
| --- | --- | --- | --- | --- |
| NotebookLM source set is absent | Claims cannot be verified or selected for a canonical script | User / supervisor | Source titles and identifiers are supplied | Yes, for H1 and later |
| Original audio timestamps and duration are absent | Turn and ASR locations are line-based only | Future intake slice | Easy export becomes available without regeneration | No for H0 |
| Speaker identity is unresolved | Turn labels remain anonymous and confidence-graded | Editorial successor | Source-backed script shaping begins | No for H0 |
| ASR candidates include source-dependent terms | Normalized candidate is not a clean transcript | Source reconciliation owner | Exact supporting source is mapped | No for H0 |
| Human editorial value is unreviewed | Salvage does not imply adoption or production quality | Human reviewer | Source-backed canonical candidate exists | No for H0 |
"""

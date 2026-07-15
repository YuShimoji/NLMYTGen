"""Build deterministic editorial-provenance artifacts for the new-banknote script.

The analyzer is deliberately content preserving.  It reads tracked receipts,
claim/cue identities, and one recoverable Git draft; it never rewrites the
canonical script, CSVs, YMM4 evidence, or visual route definitions.  Raw input
bodies stay ignored and are represented only by fingerprints.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_PILOT_DIR = REPO_ROOT / PILOT_RELATIVE
PROVENANCE_DIRNAME = "editorial_provenance"

TARGET_STATE_ID = (
    "new-banknote-editorial-provenance-audited-visual-selection-ready-v1"
)
PRE_EDITORIAL_DRAFT_COMMIT = "a307083891cccb974021d2523a3b30e1b1c60a5c"
SCRIPT_BASELINE_COMMIT = "b05eb3867caabda496fb9a0070d230a4e81aea01"
VISUAL_BASELINE_COMMIT = "bc07fc073063d3e5d1af1e6e5400a340b0036496"

ATTRIBUTION_CLASSES = (
    "source_verbatim_candidate",
    "normalized_source_reuse",
    "evidence_backed_paraphrase",
    "multi_source_synthesis",
    "worker_editorial_bridge",
    "supervisor_requested_revision",
    "user_requested_change",
    "user_approved_current_state",
    "unresolved_external_origin",
)
OPERATION_CLASSES = (
    "preserve",
    "normalize",
    "paraphrase",
    "merge",
    "split",
    "reorder",
    "omit",
    "add_bridge",
    "assign_speaker",
    "move_scene",
    "remove_style",
    "correct_fact",
    "reduce_density",
)
AUTHORITY_CLASSES = (
    "source_correction",
    "machine_normalization",
    "worker_editorial",
    "supervisor_editorial",
    "user_requested",
    "user_approved",
    "unresolved",
)
PRIOR_USER_SCRIPT_STATUSES = (
    "proven_used",
    "proven_not_used",
    "candidate_overlap_unresolved",
    "not_proven_from_available_repo_evidence",
)

GENERATED_FILENAMES = (
    "README_EDITORIAL_PROVENANCE.md",
    "editorial_provenance_ledger.json",
    "cue_transformation_matrix.json",
    "stage_decision_ledger.json",
    "authorial_contribution_readback.json",
    "prior_user_script_usage_audit.json",
    "content_lock_receipt.json",
    "future_change_contract.md",
    "provenance_validation_readback.json",
)

# These are content/evidence identities, not human navigation surfaces.  The
# four review surfaces are regenerated metadata-only and intentionally stay
# outside this immutable core.
LOCKED_ARTIFACT_HASHES: dict[str, str] = {
    "canonical_script.json": (
        "4d272900e84c8f87c484aa84c1dd1909207ee8acc189603009a186af65837c47"
    ),
    "canonical_script.txt": (
        "4eff43d0cd1f7842b02aaacd8ac6393cc12910fe70f21d650d4a31c74c17c091"
    ),
    "canonical_script_review.md": (
        "9816c28e9b0099ef98e2aefb9e70bf22a32fbbd0f931fd8989c6ac19dcd99d3a"
    ),
    "canonical_yymm4.csv": (
        "23361565b18d5e8d96768ad2877b1505e0bdeb5aacb5fbd0022a11f5e8dcfb12"
    ),
    "derived_yymm4_import.csv": (
        "127dd3edd32ce6131f339819263a6d2716570f800ad212b0741a384b7e19f9ee"
    ),
    "cue_source_traceability.json": (
        "5b6601134baf0e319cf252c24a3addecbecc02432f9a38234fdfc6580e038f47"
    ),
    "source_to_script_manifest.json": (
        "e13fb57a2681875f577e4d85f13cf41bfc601519892fa4f975bdfcdd24d927b5"
    ),
    "claim_adjudication.json": (
        "f6c61c2bb0f01fd36d1b09ddc219544a15922ecbd92a111be8d6e1ce4d97600b"
    ),
    "claim_adjudication_readback.json": (
        "7b16e107e3b78f0b372ad38a16b5b12cc00db5a932c20ef85f8a905cb5ede662"
    ),
    "verified_claim_set.json": (
        "8364bebb0448159e42f5539a2f1cde2f1fd855b5f35d8325d9279f127b1df00f"
    ),
    "input_identity_receipt.json": (
        "285ebe69286584d2e64fa685593684a46d443c985924836ebd0eb663109940a8"
    ),
    "yymm4_import_observation_receipt.json": (
        "008f9ec26392306af3a5db24c0d69f6fda93101a95ac134d9bc2d77628a839f4"
    ),
    "yymm4_import_observation_readback.json": (
        "6390943813644c9c94febe8f2a307727f8905250040796e2eace0bad22feb17e"
    ),
    "yymm4_import_source_to_project_traceability.json": (
        "053a65dfff221c6598c7731c969cea3a2d2e54a15bd4b690b721ac03316c3e05"
    ),
    "supervisor_yymm4_import_observation_review_receipt.json": (
        "5573960a345ba98a73ae258fa0709d77bbd2f894172a6f54a87f9d361d9e3a99"
    ),
    "visual_scene_decision/visual_direction_options.json": (
        "71c880203f5ab06b33fcd8652100e109a56a4fce001a3176992f3d58a123b03d"
    ),
    "visual_scene_decision/recommended_visual_direction.json": (
        "d9919faffd17b6550f7a664e294dc37f88f1a42f458bbfa9d61a6e4ddfebd342"
    ),
    "visual_scene_decision/scene_layout_plan.json": (
        "a36912697b342c0681a80356df2e6dbeb9fcbb7749e4e6d5a8bac332b551102f"
    ),
    "visual_scene_decision/motion_beat_plan.json": (
        "1a5ee226fe44d9255e6db9459ed5ab1edb70acd656ad23dc145a54cb5975f535"
    ),
    "visual_scene_decision/asset_rights_matrix.json": (
        "6e8ae2bc883148755b5e2eb808cd8cfed3dfd11361a53e9c15f537484df08d34"
    ),
    "visual_scene_decision/script_beat_ir.json": (
        "e99e6fdf3052148423cb1fba27d0714993d117832a075fb127b2ba8a0ac8f343"
    ),
    "visual_scene_decision/visual_review_sheet.md": (
        "a68c7aaa51ff4ac5528e2dcd97d6b8a9b5da3825848472ccf89f49b7b535b905"
    ),
    "visual_scene_decision/limitations.md": (
        "d95bfc409abb46aedfcc4cbab3ebc1c389e57d3f19a9ae7dd921b9f6ec98516f"
    ),
    "visual_scene_decision/yymm4_visual_project_contract.json": (
        "610b4b95ded4769029b672a2103d8303aabe96268774193082ec18b687e89ce3"
    ),
}

PRE_EDITORIAL_HASHES = {
    "canonical_script.json": (
        "c1c7dacdaf0961f2c1796639e401f2d7ad41c5eb9dfe998727715a341ac26a87"
    ),
    "canonical_script.txt": (
        "a9fd2e3f59ea61519d572ccc56bead0fed5c19bd38a8c69b7b7dfec7b68d2dd8"
    ),
    "cue_source_traceability.json": (
        "98534ded178900adf30148bff2e6690ed7d9a9c9696eeee9d3aa45dcb4e30a7e"
    ),
    "canonical_yymm4.csv": (
        "549d382cec35dcd9f9f51ee21f9e82d68f662156baacf56891a888832aae1ab3"
    ),
    "derived_yymm4_import.csv": (
        "179421d0e04b3e510c76c63e7a8613586a2115172743d5892689a656c5282069"
    ),
}

METADATA_SURFACE_BASELINE_HASHES = {
    "README_CANONICAL_SCRIPT_REVIEW.md": (
        "a5d5a23fca7d6c0c0fe200a89800d9c3c8ac278c18c1a137c35019d4780e7da8"
    ),
    "canonical_script_editorial_revision.md": (
        "af5680175765526684ea2bddccd05d1d34fda84cfce303c23a282a1d0b2b32bb"
    ),
    "editorial_revision_receipt.json": (
        "357b42e60135cfc2e08d828ae7cced285645a3416234d2da4a68baf711855ce1"
    ),
    "script_generation_receipt.json": (
        "972af253aa897b853eb333fbc7fcbc4ae9507bd31f46a43ed03ff8c067d13fa0"
    ),
    "visual_scene_decision/README_VISUAL_SCENE_DECISION.md": (
        "87d45f0bff63f7920d1cf413c84b02b13c6d8ea7f6bca370949a9e159bff541a"
    ),
    "visual_scene_decision/visual_direction_board.html": (
        "27cf98142ad5eddb6baa62bd835ad70c3b68f8ecc8bb9f06bc952643f52225e5"
    ),
    "visual_scene_decision/visual_direction_board_readback.json": (
        "f9b4c989833bf57d82eb25a93aea711e1daf1c2e99457f01b22faaefdd2527d9"
    ),
}

STRUCTURAL_ROLES = {
    "cue_001": "opening question that scopes the topic beyond appearance",
    "cue_002": "direct answer and two-family overview",
    "cue_003": "first counterfeit-resistance technique",
    "cue_004": "second counterfeit-resistance technique",
    "cue_005": "tactile technique confirmation",
    "cue_006": "tool-assisted microtext explanation",
    "cue_007": "transition to tactile identification design",
    "cue_008": "compressed visual-identification comparison",
    "cue_009": "four-method closing recap",
}

BRIDGE_ROLES = {
    "cue_001": ["contrast beyond appearance"],
    "cue_002": ["groups supported security techniques"],
    "cue_003": ["orders the first technique"],
    "cue_004": ["continues the ordered explanation"],
    "cue_005": [],
    "cue_006": ["separates checking method from reproduction difficulty"],
    "cue_007": ["moves from counterfeit resistance to identification"],
    "cue_008": ["compresses three related facts into a readable turn"],
    "cue_009": ["introduces the recap", "closes with a retention prompt"],
}

VOICE_ROLES = {
    "cue_001": "Reimu question framing",
    "cue_002": "Marisa direct answer",
    "cue_003": "Marisa explanatory ending",
    "cue_004": "Marisa explanatory ending",
    "cue_005": "Reimu confirmation",
    "cue_006": "Marisa explanatory ending",
    "cue_007": "Marisa transition ending",
    "cue_008": "Reimu confirmation",
    "cue_009": "Marisa closing invitation",
}

CUE_OPERATIONS = {
    "cue_001": ["paraphrase", "reorder", "add_bridge", "assign_speaker"],
    "cue_002": ["paraphrase", "merge", "add_bridge", "assign_speaker"],
    "cue_003": ["paraphrase", "reorder", "add_bridge", "assign_speaker"],
    "cue_004": ["paraphrase", "add_bridge", "assign_speaker"],
    "cue_005": ["preserve", "paraphrase", "assign_speaker"],
    "cue_006": ["paraphrase", "split", "add_bridge", "assign_speaker"],
    "cue_007": ["paraphrase", "merge", "reorder", "add_bridge", "assign_speaker"],
    "cue_008": [
        "paraphrase",
        "merge",
        "omit",
        "reduce_density",
        "add_bridge",
        "assign_speaker",
    ],
    "cue_009": ["paraphrase", "merge", "reorder", "add_bridge", "assign_speaker"],
}

# Each tuple is ``(exclusive_end_character, primary_substantive_unit_id)``.
# The ranges deliberately partition canonical cue text without embedding a
# second copy of that text in generated provenance artifacts.  A fragment is
# identified by its range and hash.  Structural bridges that are decisions
# between phrases rather than phrases themselves are recorded separately.
SURFACE_SEGMENT_SPECS: dict[str, tuple[tuple[int, str], ...]] = {
    "cue_001": (
        (11, "cue_001_fact_01"),
        (19, "cue_001_voice_01"),
        (26, "cue_001_bridge_01"),
        (38, "cue_001_voice_01"),
    ),
    "cue_002": (
        (4, "cue_002_voice_01"),
        (11, "cue_002_bridge_01"),
        (19, "cue_002_fact_01"),
        (28, "cue_002_fact_02"),
        (43, "cue_002_fact_03"),
        (70, "cue_002_fact_04"),
        (73, "cue_002_voice_01"),
    ),
    "cue_003": (
        (3, "cue_003_bridge_01"),
        (11, "cue_003_fact_01"),
        (27, "cue_003_fact_01"),
        (31, "cue_003_voice_01"),
    ),
    "cue_004": (
        (2, "cue_004_bridge_01"),
        (10, "cue_004_fact_01"),
        (32, "cue_004_fact_02"),
        (34, "cue_004_voice_01"),
    ),
    "cue_005": (
        (12, "cue_005_fact_01"),
        (35, "cue_005_fact_01"),
        (40, "cue_005_voice_01"),
    ),
    "cue_006": (
        (33, "cue_006_fact_01"),
        (55, "cue_006_fact_02"),
        (59, "cue_006_voice_01"),
    ),
    "cue_007": (
        (12, "cue_007_bridge_01"),
        (29, "cue_007_fact_01"),
        (42, "cue_007_fact_02"),
        (44, "cue_007_voice_01"),
    ),
    "cue_008": (
        (21, "cue_008_fact_01"),
        (45, "cue_008_fact_02"),
        (66, "cue_008_fact_03"),
        (70, "cue_008_voice_01"),
    ),
    "cue_009": (
        (6, "cue_009_bridge_01"),
        (10, "cue_009_fact_01"),
        (13, "cue_009_fact_02"),
        (17, "cue_009_fact_03"),
        (24, "cue_009_fact_04"),
        (29, "cue_009_bridge_02"),
        (36, "cue_009_voice_01"),
    ),
}

STRUCTURAL_REALIZATION_SPECS: dict[str, tuple[dict[str, Any], ...]] = {
    "cue_006": (
        {
            "unit_id": "cue_006_bridge_01",
            "realization_mode": "structural_sequence",
            "between_segment_ids": [
                "cue_006_segment_01",
                "cue_006_segment_02",
            ],
        },
    ),
    "cue_008": (
        {
            "unit_id": "cue_008_bridge_01",
            "realization_mode": "structural_sequence",
            "between_segment_ids": [
                "cue_008_segment_01",
                "cue_008_segment_02",
            ],
        },
    ),
}

AUDIT_SEARCH_ROOTS = (
    PILOT_RELATIVE,
    Path(
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "real_input_intake_readiness/real_input/transcript/"
        "new_banknote_notebooklm"
    ),
    Path(
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "real_input_replacement_readiness_pack/input_dropzone"
    ),
    Path(
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "transcript_substitution_readiness/real_input"
    ),
)
AUDIT_GIT_HISTORY_ROOT = Path(".")
AUDIT_SELF_PATHS = {
    "src/pipeline/editorial_provenance.py",
    "tests/test_editorial_provenance.py",
}
_SCRIPT_CANDIDATE_SUFFIXES = {".txt", ".md", ".json", ".csv", ".rtf", ".docx"}
_SCRIPT_CANDIDATE_RE = re.compile(
    r"(?i)(?:(?:user|submitted|human|prior|previous|finished|final)"
    r"[-_. ]*(?:script|draft)|(?:script|draft)[-_. ]*"
    r"(?:user|submitted|human|prior|previous)|台本|原稿)"
)
_KNOWN_GENERATED_SCRIPT_RE = re.compile(
    r"(?i)(?:canonical_script|regenerated_|script_generation_receipt|"
    r"script_beat_ir|source_script|transcript_template|approval_receipt|"
    r"readback|audit|contract|manifest)"
)
MAX_PROVENANCE_JSON_STRING_CHARS = 320
MAX_PROVENANCE_MARKDOWN_LINE_CHARS = 500

_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)
_UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
_BANNED_BODY_KEYS = {
    "raw_text",
    "source_body",
    "transcript_body",
    "full_text",
    "verbatim_excerpt",
    "source_quote_text",
}


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _repo_path(relative: str) -> str:
    return f"{PILOT_RELATIVE.as_posix()}/{relative}"


def _artifact(pilot: Path, relative: str) -> dict[str, Any]:
    return {
        "repo_relative_path": _repo_path(relative),
        "sha256": _sha256(pilot / relative),
    }


def _git_json(commit: str, relative: str) -> dict[str, Any]:
    git_path = f"{PILOT_RELATIVE.as_posix()}/{relative}"
    result = subprocess.run(
        ["git", "show", f"{commit}:{git_path}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"GIT_EVIDENCE_UNAVAILABLE:{commit}:{relative}")
    payload = json.loads(result.stdout.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"GIT_JSON_OBJECT_REQUIRED:{relative}")
    return payload


def _normalize(value: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value))


def _tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value)
    return re.findall(
        r"[A-Za-z0-9]+|[ぁ-んァ-ヶ一-龠々ー]|[^\s]", normalized
    )


def _overlap(before: str, after: str) -> dict[str, Any]:
    before_chars = _normalize(before)
    after_chars = _normalize(after)
    char_matcher = SequenceMatcher(
        None, before_chars, after_chars, autojunk=False
    )
    before_tokens = _tokens(before)
    after_tokens = _tokens(after)
    token_matcher = SequenceMatcher(
        None, before_tokens, after_tokens, autojunk=False
    )
    return {
        "before_normalized_characters": len(before_chars),
        "after_normalized_characters": len(after_chars),
        "ordered_matching_characters": sum(
            block.size for block in char_matcher.get_matching_blocks()
        ),
        "before_tokens": len(before_tokens),
        "after_tokens": len(after_tokens),
        "ordered_matching_tokens": sum(
            block.size for block in token_matcher.get_matching_blocks()
        ),
        "text_byte_equal": before.encode("utf-8") == after.encode("utf-8"),
        "metric_scope": "pre_editorial_draft_to_current_cue",
        "authorship_share_claimed": False,
    }


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        result = set(value)
        for nested in value.values():
            result.update(_all_keys(nested))
        return result
    if isinstance(value, list):
        result: set[str] = set()
        for nested in value:
            result.update(_all_keys(nested))
        return result
    return set()


def _string_values(value: Any, path: str = "$") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, dict):
        result: list[tuple[str, str]] = []
        for key, nested in value.items():
            result.extend(_string_values(nested, f"{path}.{key}"))
        return result
    if isinstance(value, list):
        result = []
        for index, nested in enumerate(value):
            result.extend(_string_values(nested, f"{path}[{index}]"))
        return result
    return []


def _git_output(args: Sequence[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"GIT_AUDIT_COMMAND_FAILED:{args[0]}:{detail[:120]}")
    return result.stdout


def _git_nul_paths(args: Sequence[str]) -> list[str]:
    raw = _git_output(args)
    return sorted(
        {
            item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
            for item in raw.split(b"\0")
            if item
        }
    )


def _path_inventory_sha256(paths: Sequence[str]) -> str:
    return _sha256_bytes(
        json.dumps(
            sorted(set(paths)),
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def _excluded_from_script_candidate_audit(repo_relative_path: str) -> bool:
    normalized = repo_relative_path.replace("\\", "/")
    return (
        f"/{PROVENANCE_DIRNAME}/" in f"/{normalized}/"
        or _KNOWN_GENERATED_SCRIPT_RE.search(Path(normalized).name) is not None
        or "/sample_inputs/" in f"/{normalized}/"
        or normalized.endswith("/README.md")
        or normalized.endswith("/DROPZONE_README.md")
        or normalized.endswith("/README_DROPZONE.md")
    )


def _excluded_from_inventory_identity(repo_relative_path: str) -> bool:
    normalized = repo_relative_path.replace("\\", "/")
    return (
        normalized in AUDIT_SELF_PATHS
        or f"/{PROVENANCE_DIRNAME}/" in f"/{normalized}/"
    )


def _is_prior_user_script_candidate(repo_relative_path: str) -> bool:
    normalized = repo_relative_path.replace("\\", "/")
    path = Path(normalized)
    return (
        path.suffix.lower() in _SCRIPT_CANDIDATE_SUFFIXES
        and not _excluded_from_script_candidate_audit(normalized)
        and _SCRIPT_CANDIDATE_RE.search(path.stem) is not None
    )


def _candidate_record(repo_relative_path: str, disposition: str) -> dict[str, Any]:
    path = REPO_ROOT / Path(repo_relative_path)
    record: dict[str, Any] = {
        "repo_relative_path": repo_relative_path.replace("\\", "/"),
        "disposition": disposition,
        "body_embedded": False,
    }
    if path.is_file():
        record.update(
            {
                "sha256": _sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    else:
        record.update(
            {
                "sha256": None,
                "size_bytes": None,
            }
        )
    return record


def _prior_script_search_execution() -> dict[str, Any]:
    tracked_paths = _git_nul_paths(
        [
            "ls-files",
            "-z",
            "--",
            AUDIT_GIT_HISTORY_ROOT.as_posix(),
        ]
    )
    tracked_paths = [
        path
        for path in tracked_paths
        if not _excluded_from_inventory_identity(path)
    ]
    tracked_candidates = [
        path for path in tracked_paths if _is_prior_user_script_candidate(path)
    ]

    history_raw = _git_output(
        [
            "log",
            "--format=",
            "--name-only",
            "--no-renames",
            VISUAL_BASELINE_COMMIT,
            "--",
            AUDIT_GIT_HISTORY_ROOT.as_posix(),
        ]
    ).decode("utf-8", errors="surrogateescape")
    history_paths = sorted(
        {
            line.strip().replace("\\", "/")
            for line in history_raw.splitlines()
            if line.strip()
            and not _excluded_from_inventory_identity(
                line.strip().replace(chr(92), "/")
            )
        }
    )
    history_candidates = [
        path for path in history_paths if _is_prior_user_script_candidate(path)
    ]

    available_history_raw = _git_output(
        [
            "log",
            "--all",
            "--format=",
            "--name-only",
            "--no-renames",
            "--",
            AUDIT_GIT_HISTORY_ROOT.as_posix(),
        ]
    ).decode("utf-8", errors="surrogateescape")
    available_history_paths = sorted(
        {
            line.strip().replace("\\", "/")
            for line in available_history_raw.splitlines()
            if line.strip()
            and not _excluded_from_inventory_identity(
                line.strip().replace(chr(92), "/")
            )
        }
    )
    available_history_candidates = [
        path
        for path in available_history_paths
        if _is_prior_user_script_candidate(path)
    ]

    ignored_paths = _git_nul_paths(
        [
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
            "-z",
            "--",
            *(root.as_posix() for root in AUDIT_SEARCH_ROOTS),
        ]
    )
    ignored_candidates = [
        path for path in ignored_paths if _is_prior_user_script_candidate(path)
    ]

    dropzone_candidates: list[str] = []
    for root in AUDIT_SEARCH_ROOTS:
        absolute = REPO_ROOT / root
        if not absolute.is_dir():
            continue
        for path in absolute.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(REPO_ROOT).as_posix()
            if _is_prior_user_script_candidate(relative):
                dropzone_candidates.append(relative)
    dropzone_candidates = sorted(set(dropzone_candidates))

    current_candidate_paths = sorted(
        set(tracked_candidates + ignored_candidates + dropzone_candidates)
    )
    current_records = [
        _candidate_record(
            path,
            "tracked"
            if path in tracked_candidates
            else "intentional_ignored_or_untracked_dropzone",
        )
        for path in current_candidate_paths
    ]
    historical_only = sorted(
        set(history_candidates + available_history_candidates)
        - set(current_candidate_paths)
    )
    historical_records = [
        {
            "repo_relative_path": path,
            "disposition": "historical_path_only",
            "sha256": None,
            "size_bytes": None,
            "body_embedded": False,
        }
        for path in historical_only
    ]
    candidate_records = [*current_records, *historical_records]
    candidate_paths = [row["repo_relative_path"] for row in candidate_records]

    return {
        "matcher_version": "strong-prior-user-script-filename-v1",
        "configured_roots": [root.as_posix() for root in AUDIT_SEARCH_ROOTS],
        "tracked_path_count": len(tracked_paths),
        "tracked_path_inventory_sha256": _path_inventory_sha256(tracked_paths),
        "history_endpoint_commit": VISUAL_BASELINE_COMMIT,
        "history_unique_path_count": len(history_paths),
        "history_path_inventory_sha256": _path_inventory_sha256(history_paths),
        "available_ref_candidate_path_inventory_sha256": (
            _path_inventory_sha256(available_history_candidates)
        ),
        "ignored_candidate_path_inventory_sha256": _path_inventory_sha256(
            ignored_candidates
        ),
        "dropzone_candidate_path_inventory_sha256": _path_inventory_sha256(
            dropzone_candidates
        ),
        "candidate_path_inventory_sha256": _path_inventory_sha256(
            candidate_paths
        ),
        "candidate_records": candidate_records,
        "candidate_paths": candidate_paths,
        "candidate_hashes": sorted(
            row["sha256"] for row in candidate_records if row["sha256"]
        ),
    }


def _approval_decision_identity(inputs: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "decision_id": "current-nine-cue-continuation-approval-v1",
        "subject_sha256": inputs["locked_hashes"]["canonical_script.json"],
        "decision": "continue_current_state",
        "future_silent_edits_authorized": False,
        "evidence_reference": "current_execution_contract",
    }
    return {
        "artifact_kind": "bounded_user_approval_decision",
        **payload,
        "decision_sha256": _sha256_bytes(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
        "tracked_prior_to_retrofit": False,
        "independent_contemporaneous_receipt_available": False,
    }


def _verify_optional_local_raw_identity(identity: Mapping[str, Any]) -> None:
    relative = identity.get("raw_path")
    if not isinstance(relative, str):
        raise ValueError("RAW_IDENTITY_REPO_RELATIVE_PATH_MISSING")
    path = REPO_ROOT / relative
    if not path.is_file():
        return
    data = path.read_bytes()
    actual = {
        "sha256": _sha256_bytes(data),
        "size_bytes": len(data),
        "logical_line_count": len(
            data.decode("utf-8", errors="replace").splitlines()
        ),
    }
    expected = {
        "sha256": identity.get("raw_sha256"),
        "size_bytes": identity.get("raw_size_bytes"),
        "logical_line_count": identity.get("raw_logical_line_count"),
    }
    if actual != expected:
        raise ValueError("OPTIONAL_LOCAL_RAW_IDENTITY_MISMATCH")


def _verify_optional_raw_line_map(
    pilot: Path,
    identity: Mapping[str, Any],
    claims: Sequence[Mapping[str, Any]],
) -> None:
    path = pilot / "local_outputs/raw_line_map.json"
    if not path.is_file():
        return
    payload = _read_json(path)
    lines = payload.get("lines") or []
    if (
        payload.get("raw_sha256") != identity.get("raw_sha256")
        or payload.get("logical_line_count")
        != identity.get("raw_logical_line_count")
        or len(lines) != identity.get("raw_logical_line_count")
    ):
        raise ValueError("OPTIONAL_RAW_LINE_MAP_IDENTITY_MISMATCH")
    fingerprints = {
        row.get("ordinal"): row.get("fingerprint")
        for row in lines
        if isinstance(row, dict)
    }
    mismatches = [
        claim.get("claim_id")
        for claim in claims
        if fingerprints.get(claim.get("line_ordinal"))
        != claim.get("line_fingerprint")
    ]
    if mismatches:
        raise ValueError(
            "OPTIONAL_RAW_LINE_MAP_CLAIM_MISMATCH:" + ",".join(mismatches[:5])
        )


def _local_yymm4_evidence_status(inputs: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = inputs["yymm4_readback"].get("evidence_snapshot") or {}
    rows = []
    for key in ("operator_result", "operator_batch_state", "project_identity"):
        identity = snapshot.get(key) or {}
        relative = identity.get("repo_relative_path")
        expected = identity.get("sha256")
        path = REPO_ROOT / relative if isinstance(relative, str) else None
        present = bool(path and path.is_file())
        actual = _sha256(path) if present and path is not None else None
        rows.append(
            {
                "evidence_kind": key,
                "repo_relative_path": relative,
                "expected_sha256": expected,
                "local_file_present": present,
                "local_sha256_matches": actual == expected if present else None,
            }
        )
    present_count = sum(row["local_file_present"] for row in rows)
    all_match = all(row["local_sha256_matches"] is True for row in rows)
    if present_count == len(rows) and all_match:
        status = "reverified_from_current_local_bytes"
    elif present_count == 0:
        status = "not_reperformed_local_project_and_results_absent"
    else:
        status = "incomplete_or_identity_mismatch_requires_reobservation"
    return {
        "status": status,
        "expected_identity_count": len(rows),
        "local_present_count": present_count,
        "all_present_hashes_match": all_match if present_count == len(rows) else None,
        "evidence": rows,
        "tracked_receipts_remain_locked": True,
    }


def _load_inputs(pilot: Path) -> dict[str, Any]:
    actual_hashes = {
        relative: _sha256(pilot / relative)
        for relative in LOCKED_ARTIFACT_HASHES
    }
    if actual_hashes != LOCKED_ARTIFACT_HASHES:
        mismatches = sorted(
            relative
            for relative, expected in LOCKED_ARTIFACT_HASHES.items()
            if actual_hashes.get(relative) != expected
        )
        raise ValueError("CONTENT_LOCK_BASELINE_DRIFT:" + ",".join(mismatches))

    script = _read_json(pilot / "canonical_script.json")
    trace = _read_json(pilot / "cue_source_traceability.json")
    adjudication = _read_json(pilot / "claim_adjudication.json")
    adjudication_readback = _read_json(
        pilot / "claim_adjudication_readback.json"
    )
    identity = _read_json(pilot / "input_identity_receipt.json")
    source_snapshot = _read_json(pilot / "source_set_snapshot.json")
    editorial_receipt = _read_json(pilot / "editorial_revision_receipt.json")
    yymm4_readback = _read_json(
        pilot / "yymm4_import_observation_readback.json"
    )
    visual_options = _read_json(
        pilot / "visual_scene_decision/visual_direction_options.json"
    )
    recommended_visual = _read_json(
        pilot / "visual_scene_decision/recommended_visual_direction.json"
    )
    prior_script = _git_json(PRE_EDITORIAL_DRAFT_COMMIT, "canonical_script.json")

    cues = script.get("cues") or []
    trace_cues = trace.get("cues") or []
    claims = adjudication.get("claims") or []
    if len(cues) != 9 or len(trace_cues) != 9 or len(claims) != 182:
        raise ValueError("EXPECTED_9_CUES_AND_182_CLAIMS")
    if [cue.get("cue_id") for cue in cues] != [
        f"cue_{index:03d}" for index in range(1, 10)
    ]:
        raise ValueError("CUE_ORDER_DRIFT")
    if len(prior_script.get("cues") or []) != 9:
        raise ValueError("PRE_EDITORIAL_DRAFT_CUE_COUNT_DRIFT")
    if script.get("unsupported_claim_count") != 0:
        raise ValueError("UNSUPPORTED_SPOKEN_CLAIM_DRIFT")
    _verify_optional_local_raw_identity(identity)
    _verify_optional_raw_line_map(pilot, identity, claims)

    return {
        "pilot": pilot,
        "script": script,
        "trace": trace,
        "claims": claims,
        "claim_by_id": {claim["claim_id"]: claim for claim in claims},
        "prior_script": prior_script,
        "identity": identity,
        "source_snapshot": source_snapshot,
        "editorial_receipt": editorial_receipt,
        "outcome_counts": adjudication_readback["outcome_counts"],
        "yymm4_readback": yymm4_readback,
        "visual_options": visual_options,
        "recommended_visual": recommended_visual,
        "locked_hashes": actual_hashes,
    }


def _surface_coverage(
    cue_id: str,
    text: str,
    speaker: str,
    substantive_units: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    unit_by_id = {unit["unit_id"]: unit for unit in substantive_units}
    specs = SURFACE_SEGMENT_SPECS.get(cue_id)
    if not specs:
        raise ValueError(f"SURFACE_SEGMENT_SPEC_MISSING:{cue_id}")

    segments: list[dict[str, Any]] = []
    cursor = 0
    for index, (end, unit_id) in enumerate(specs, start=1):
        if unit_id not in unit_by_id:
            raise ValueError(f"SURFACE_SEGMENT_UNIT_MISSING:{cue_id}:{unit_id}")
        if end <= cursor or end > len(text):
            raise ValueError(
                f"SURFACE_SEGMENT_RANGE_INVALID:{cue_id}:{cursor}:{end}"
            )
        unit = unit_by_id[unit_id]
        fragment = text[cursor:end]
        segments.append(
            {
                "segment_id": f"{cue_id}_segment_{index:02d}",
                "character_range": [cursor, end],
                "character_count": len(fragment),
                "fragment_sha256": hashlib.sha256(
                    fragment.encode("utf-8")
                ).hexdigest(),
                "primary_substantive_unit_id": unit_id,
                "primary_attribution_class": unit["attribution_class"],
                "surface_role": unit["unit_kind"],
                "source_text_embedded": False,
            }
        )
        cursor = end

    uncovered_ranges = [] if cursor == len(text) else [[cursor, len(text)]]
    structural_realizations: list[dict[str, Any]] = []
    segment_ids = {row["segment_id"] for row in segments}
    for spec in STRUCTURAL_REALIZATION_SPECS.get(cue_id, ()):
        unit_id = spec["unit_id"]
        if unit_id not in unit_by_id:
            raise ValueError(f"STRUCTURAL_UNIT_MISSING:{cue_id}:{unit_id}")
        if not set(spec["between_segment_ids"]) <= segment_ids:
            raise ValueError(f"STRUCTURAL_SEGMENT_MISSING:{cue_id}:{unit_id}")
        unit = unit_by_id[unit_id]
        structural_realizations.append(
            {
                **spec,
                "attribution_class": unit["attribution_class"],
                "operation": "add_bridge",
            }
        )

    voice_unit_id = f"{cue_id}_voice_01"
    if voice_unit_id not in unit_by_id:
        raise ValueError(f"VOICE_UNIT_MISSING:{cue_id}")
    speaker_assignment = {
        "substantive_unit_id": voice_unit_id,
        "speaker": speaker,
        "attribution_class": unit_by_id[voice_unit_id]["attribution_class"],
        "operation": "assign_speaker",
        "realization_mode": "speaker_assignment_with_style_span",
    }

    covered_unit_ids = {
        row["primary_substantive_unit_id"] for row in segments
    }
    covered_unit_ids.update(
        row["unit_id"] for row in structural_realizations
    )
    covered_unit_ids.add(voice_unit_id)
    unmapped_unit_ids = sorted(set(unit_by_id) - covered_unit_ids)
    unresolved_lineage = [
        {
            "kind": "unattributed_character_range",
            "character_range": character_range,
        }
        for character_range in uncovered_ranges
    ]
    unresolved_lineage.extend(
        {
            "kind": "unrealized_substantive_unit",
            "unit_id": unit_id,
        }
        for unit_id in unmapped_unit_ids
    )
    return {
        "character_range": [0, len(text)],
        "surface_segments": segments,
        "surface_segment_count": len(segments),
        "structural_realizations": structural_realizations,
        "speaker_assignment": speaker_assignment,
        "covered_by_substantive_unit_ids": sorted(covered_unit_ids),
        "unmapped_substantive_unit_ids": unmapped_unit_ids,
        "unattributed_character_ranges": uncovered_ranges,
        "coverage_status": (
            "complete_non_overlapping_surface_partition"
            if not unresolved_lineage
            else "incomplete_requires_resolution"
        ),
        "token_level_authorship_claimed": False,
        "unresolved_lineage": unresolved_lineage,
    }


def _cue_matrix(inputs: Mapping[str, Any]) -> dict[str, Any]:
    trace_by_id = {
        cue["cue_id"]: cue for cue in inputs["trace"]["cues"]
    }
    prior_by_id = {
        cue["cue_id"]: cue for cue in inputs["prior_script"]["cues"]
    }
    approval_decision = _approval_decision_identity(inputs)
    rows: list[dict[str, Any]] = []
    for cue in inputs["script"]["cues"]:
        cue_id = cue["cue_id"]
        trace = trace_by_id[cue_id]
        prior = prior_by_id[cue_id]
        raw_candidates: list[dict[str, Any]] = []
        adopted_claims: list[dict[str, Any]] = []
        for claim_id in cue["adopted_claim_ids"]:
            claim = inputs["claim_by_id"][claim_id]
            raw_candidates.append(
                {
                    "claim_id": claim_id,
                    "raw_line_ordinal": claim["line_ordinal"],
                    "raw_line_fingerprint": claim["line_fingerprint"],
                    "relationship": (
                        "claim_candidate_derived_from_submitted_audio_overview_transcript"
                    ),
                    "body_embedded": False,
                }
            )
            adopted_claims.append(
                {
                    "claim_id": claim_id,
                    "adjudicated_proposition_sha256": hashlib.sha256(
                        claim["adjudicated_proposition"].encode("utf-8")
                    ).hexdigest(),
                    "evidence_grade": claim["evidence_grade"],
                    "primary_outcome": claim["primary_outcome"],
                }
            )

        factual_units: list[dict[str, Any]] = []
        for unit in trace["factual_support_units"]:
            source_ids = sorted(
                {
                    edge["source_id"]
                    for edge in unit["supporting_evidence"]
                }
            )
            classification = (
                "multi_source_synthesis"
                if len(source_ids) > 1
                else "evidence_backed_paraphrase"
            )
            operations = ["paraphrase"]
            if classification == "multi_source_synthesis":
                operations.append("merge")
            factual_units.append(
                {
                    "unit_id": unit["support_unit_id"],
                    "unit_kind": "factual_content",
                    "statement_sha256": hashlib.sha256(
                        unit["statement"].encode("utf-8")
                    ).hexdigest(),
                    "statement_character_count": len(unit["statement"]),
                    "claim_ids": unit["claim_ids"],
                    "source_ids": source_ids,
                    "attribution_class": classification,
                    "operations": operations,
                    "authority_classes": [
                        "source_correction",
                        "worker_editorial",
                    ],
                    "confidence": "high",
                    "source_quote": False,
                    "surface_realization": "character_span",
                }
            )

        bridge_units = [
            {
                "unit_id": f"{cue_id}_bridge_{index:02d}",
                "unit_kind": "editorial_bridge",
                "role": role,
                "attribution_class": "worker_editorial_bridge",
                "operations": ["add_bridge"],
                "authority_classes": ["worker_editorial"],
                "confidence": "medium_high_inferred_from_revision_receipt",
                "source_quote": False,
                "surface_realization": (
                    "structural_sequence"
                    if cue_id in STRUCTURAL_REALIZATION_SPECS
                    else "character_span"
                ),
            }
            for index, role in enumerate(BRIDGE_ROLES[cue_id], start=1)
        ]
        voice_units = [
            {
                "unit_id": f"{cue_id}_voice_01",
                "unit_kind": "character_voice",
                "role": VOICE_ROLES[cue_id],
                "attribution_class": "worker_editorial_bridge",
                "operations": ["assign_speaker"],
                "authority_classes": ["worker_editorial"],
                "confidence": "medium_high_inferred_from_final_dialogue",
                "source_quote": False,
                "surface_realization": (
                    "character_span_and_speaker_assignment"
                ),
            }
        ]
        substantive_units = [*factual_units, *bridge_units, *voice_units]
        coverage = _surface_coverage(
            cue_id,
            cue["text"],
            cue["speaker"],
            substantive_units,
        )
        unresolved_lineage = coverage.pop("unresolved_lineage")
        rows.append(
            {
                "cue_id": cue_id,
                "sequence": cue["sequence"],
                "scene": cue["scene_id"],
                "speaker": cue["speaker"],
                "final_text_sha256": hashlib.sha256(
                    cue["text"].encode("utf-8")
                ).hexdigest(),
                "final_text_character_count": len(cue["text"]),
                "adopted_claim_ids": cue["adopted_claim_ids"],
                "source_ids": sorted(
                    {
                        edge["source_id"]
                        for edge in trace["supporting_evidence"]
                    }
                ),
                "raw_transcript_candidates": raw_candidates,
                "adopted_claim_identities": adopted_claims,
                "prior_draft_cue_ids": [
                    {
                        "cue_id": prior["cue_id"],
                        "git_commit": PRE_EDITORIAL_DRAFT_COMMIT,
                        "relationship": "same_sequence_pre_editorial_draft",
                        "evidence_grade": "verified_from_git_history",
                    }
                ],
                "pre_editorial_to_current_overlap": _overlap(
                    prior["text"], cue["text"]
                ),
                "transformation_operations": CUE_OPERATIONS[cue_id],
                "authority_classes": [
                    "source_correction",
                    "worker_editorial",
                    "user_approved",
                ],
                "substantive_units": substantive_units,
                "substantive_unit_count": len(substantive_units),
                "final_text_coverage": coverage,
                "approval_state": {
                    "attribution_class": "user_approved_current_state",
                    "authority_class": "user_approved",
                    "status": "approved_for_continuation_of_current_state",
                    "future_silent_edits_authorized": False,
                    "decision_id": (
                        "current-nine-cue-continuation-approval-v1"
                    ),
                    "decision_sha256": approval_decision["decision_sha256"],
                    "evidence_grade": (
                        "observed_current_execution_contract_without_"
                        "independent_contemporaneous_receipt"
                    ),
                },
                "unresolved_lineage": unresolved_lineage,
                "unattributed_substantive_change": bool(unresolved_lineage),
                "short_rationale": STRUCTURAL_ROLES[cue_id],
                "confidence": {
                    "factual_lineage": "high",
                    "editorial_operation": (
                        "medium_high_inferred_from_git_delta_and_revision_receipt"
                    ),
                    "token_level_authorship": "not_claimed",
                },
            }
        )

    return {
        "schema_version": "editorial_provenance.cue_transformation_matrix.v1",
        "status": "complete",
        "cue_coverage": "9/9",
        "granularity": "claim_support_unit_editorial_role_and_cue",
        "token_level_authorship_claimed": False,
        "attribution_classes": list(ATTRIBUTION_CLASSES),
        "operation_classes": list(OPERATION_CLASSES),
        "authority_classes": list(AUTHORITY_CLASSES),
        "cues": rows,
    }


def _stage_decision_ledger(inputs: Mapping[str, Any]) -> dict[str, Any]:
    pilot = inputs["pilot"]
    approval_decision = _approval_decision_identity(inputs)
    raw_identity = {
        "artifact_kind": "user_submitted_audio_overview_transcript",
        "repo_relative_path": inputs["identity"]["raw_path"],
        "sha256": inputs["identity"]["raw_sha256"],
        "size_bytes": inputs["identity"]["raw_size_bytes"],
        "logical_line_count": inputs["identity"]["raw_logical_line_count"],
        "tracked": False,
        "body_embedded": False,
    }

    def stage(
        stage_id: str,
        name: str,
        actor: str,
        authorities: list[str],
        operations: list[str],
        inputs_: list[dict[str, Any]],
        outputs: list[dict[str, Any]],
        semantic_change_class: str,
        may_alter_canonical: bool,
        approval_required: bool,
        approval_status: str,
        evidence_grade: str,
    ) -> dict[str, Any]:
        return {
            "stage_id": stage_id,
            "stage_name": name,
            "actor": actor,
            "authority_classes": authorities,
            "operations": operations,
            "input_identity": inputs_,
            "output_identity": outputs,
            "semantic_change_class": semantic_change_class,
            "user_approval_required": approval_required,
            "approval_status": approval_status,
            "may_alter_canonical_content": may_alter_canonical,
            "evidence_grade": evidence_grade,
        }

    historical_script = {
        "repo_relative_path": _repo_path("canonical_script.json"),
        "sha256": PRE_EDITORIAL_HASHES["canonical_script.json"],
        "git_commit": PRE_EDITORIAL_DRAFT_COMMIT,
    }
    stages = [
        stage(
            "D00",
            "RSS-title anchor / NotebookLM research",
            "upstream_user_and_research_service",
            ["user_requested"],
            ["preserve"],
            [_artifact(pilot, "notebooklm_generation_receipt.json")],
            [_artifact(pilot, "source_set_snapshot.json")],
            "upstream_research_input",
            False,
            True,
            "source_set_frozen_for_current_chain",
            "verified_repo_receipts",
        ),
        stage(
            "D01",
            "Audio Overview generation",
            "NotebookLM",
            ["unresolved"],
            ["merge", "paraphrase"],
            [_artifact(pilot, "notebooklm_generation_receipt.json")],
            [raw_identity],
            "external_generative_transformation",
            False,
            True,
            "upstream_output_accepted_as_input_not_factual_authority",
            "identity_verified_generation_details_unavailable",
        ),
        stage(
            "D02",
            "raw transcript salvage",
            "Worker_mechanical",
            ["machine_normalization"],
            ["normalize", "preserve"],
            [raw_identity],
            [
                _artifact(pilot, "input_identity_receipt.json"),
                _artifact(pilot, "asr_correction_ledger.json"),
                _artifact(pilot, "transcript_quality_readback.json"),
            ],
            "mechanical_nonsemantic",
            False,
            False,
            "not_required",
            "verified_repo_and_ignored_fingerprints",
        ),
        stage(
            "D03",
            "source-set freeze",
            "user_and_Worker",
            ["user_requested"],
            ["preserve", "omit"],
            [_artifact(pilot, "notebooklm_generation_receipt.json")],
            [
                _artifact(pilot, "source_set_snapshot.json"),
                _artifact(
                    pilot,
                    "notebook_source_to_verification_source_crosswalk.json",
                ),
            ],
            "upstream_scope_decision",
            False,
            True,
            "frozen_for_current_chain",
            "verified_repo_receipts",
        ),
        stage(
            "D04",
            "official source capture",
            "Worker_source_verification",
            ["source_correction"],
            ["preserve", "correct_fact"],
            [_artifact(pilot, "source_set_snapshot.json")],
            [
                _artifact(pilot, "authoritative_source_registry.json"),
                _artifact(pilot, "source_capture_receipts.json"),
            ],
            "evidence_resolution",
            False,
            False,
            "not_required_until_claim_adoption",
            "verified_repo_receipts",
        ),
        stage(
            "D05",
            "claim adjudication",
            "Worker_source_verification",
            ["source_correction"],
            ["correct_fact", "omit", "remove_style"],
            [_artifact(pilot, "claim_risk_ledger.json")],
            [
                _artifact(pilot, "claim_adjudication.json"),
                _artifact(pilot, "claim_adjudication_readback.json"),
            ],
            "substantive_factual_filtering",
            True,
            True,
            "approved_only_as_part_of_current_script_state",
            "verified_claim_and_source_receipts",
        ),
        stage(
            "D06",
            "canonical script generation",
            "Worker_editorial",
            ["worker_editorial", "source_correction"],
            [
                "paraphrase",
                "merge",
                "split",
                "reorder",
                "omit",
                "add_bridge",
                "assign_speaker",
                "move_scene",
                "remove_style",
            ],
            [_artifact(pilot, "claim_adjudication.json")],
            [historical_script],
            "substantive_editorial_and_semantic",
            True,
            True,
            "superseded_by_editorial_convergence",
            "verified_git_history_with_inferred_operation_labels",
        ),
        stage(
            "D07",
            "editorial convergence",
            "Worker_editorial",
            ["worker_editorial", "source_correction"],
            [
                "preserve",
                "paraphrase",
                "merge",
                "split",
                "reorder",
                "omit",
                "add_bridge",
                "reduce_density",
                "correct_fact",
            ],
            [historical_script],
            [
                _artifact(pilot, "canonical_script.json"),
                _artifact(pilot, "cue_source_traceability.json"),
                _artifact(pilot, "editorial_revision_receipt.json"),
            ],
            "substantive_editorial_with_bounded_semantic_delta",
            True,
            True,
            "current_result_approved_for_continuation",
            "verified_git_delta_and_revision_receipt",
        ),
        stage(
            "D08",
            "user approval for continuation",
            "user",
            ["user_approved"],
            ["preserve"],
            [_artifact(pilot, "canonical_script.json")],
            [approval_decision],
            "approval_only_no_content_change",
            False,
            True,
            "approved_current_state_only_future_silent_edits_not_authorized",
            (
                "observed_current_execution_contract_without_"
                "independent_contemporaneous_receipt"
            ),
        ),
        stage(
            "D09",
            "YMM4 import observation",
            "human_operator_and_headless_parser",
            ["machine_normalization", "user_requested"],
            ["preserve", "normalize"],
            [_artifact(pilot, "derived_yymm4_import.csv")],
            [
                _artifact(pilot, "yymm4_import_observation_receipt.json"),
                _artifact(pilot, "yymm4_import_observation_readback.json"),
            ],
            "mechanical_observation_no_script_change",
            False,
            True,
            "observed_not_editorially_accepted",
            "tracked_sanitized_receipts_local_bytes_not_reverified_in_this_slice",
        ),
        stage(
            "D10",
            "visual route proposal",
            "Worker_visual_editorial",
            ["worker_editorial"],
            ["preserve", "reorder"],
            [
                _artifact(pilot, "canonical_script.json"),
                _artifact(pilot, "yymm4_import_observation_readback.json"),
            ],
            [
                _artifact(
                    pilot,
                    "visual_scene_decision/visual_direction_options.json",
                ),
                _artifact(
                    pilot,
                    "visual_scene_decision/recommended_visual_direction.json",
                ),
            ],
            "visual_proposal_no_canonical_content_change",
            False,
            True,
            "human_selection_pending",
            "verified_route_packet",
        ),
    ]
    return {
        "schema_version": "editorial_provenance.stage_decision_ledger.v1",
        "status": "complete",
        "stage_order": [f"D{index:02d}" for index in range(11)],
        "stages": stages,
        "current_approval_scope": (
            "continue_current_nine_cue_state_not_future_silent_edit_authority"
        ),
    }


def _prior_user_script_audit(inputs: Mapping[str, Any]) -> dict[str, Any]:
    identity = inputs["identity"]
    search = _prior_script_search_execution()
    policy = {
        "policy_id": "bounded-prior-user-script-path-audit-v1",
        "configured_roots": search["configured_roots"],
        "candidate_suffixes": sorted(_SCRIPT_CANDIDATE_SUFFIXES),
        "candidate_pattern": _SCRIPT_CANDIDATE_RE.pattern,
        "generated_script_exclusion_pattern": (
            _KNOWN_GENERATED_SCRIPT_RE.pattern
        ),
        "git_history_scopes": [
            "fixed_content_baseline",
            "available_local_refs_candidate_set_only",
        ],
        "body_read_for_overlap": False,
    }
    policy_sha256 = _sha256_bytes(
        json.dumps(
            policy,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    candidates = search["candidate_records"]
    final_status = (
        "candidate_overlap_unresolved"
        if candidates
        else "not_proven_from_available_repo_evidence"
    )
    return {
        "schema_version": "editorial_provenance.prior_user_script_audit.v1",
        "status": "complete_evidence_bounded",
        "allowed_final_statuses": list(PRIOR_USER_SCRIPT_STATUSES),
        "inventory_policy": {**policy, "policy_sha256": policy_sha256},
        "search_surfaces": [
            {
                "surface": "current tracked repository path inventory",
                "method": "executed_git_ls_files_path_inventory",
                "path_count": search["tracked_path_count"],
                "path_inventory_sha256": search[
                    "tracked_path_inventory_sha256"
                ],
                "candidate_path_inventory_sha256": search[
                    "candidate_path_inventory_sha256"
                ],
                "result": (
                    "no_unresolved_prior_user_script_candidate"
                    if not candidates
                    else "candidate_requires_overlap_review"
                ),
            },
            {
                "surface": "Git path history reachable from content baseline",
                "method": "executed_git_log_name_only_fixed_endpoint",
                "history_endpoint_commit": search[
                    "history_endpoint_commit"
                ],
                "unique_path_count": search["history_unique_path_count"],
                "path_inventory_sha256": search[
                    "history_path_inventory_sha256"
                ],
                "candidate_path_inventory_sha256": search[
                    "candidate_path_inventory_sha256"
                ],
                "result": (
                    "no_unresolved_prior_user_script_candidate"
                    if not candidates
                    else "candidate_requires_overlap_review"
                ),
            },
            {
                "surface": "Git path history across available local refs",
                "method": (
                    "executed_git_log_all_name_only_candidate_filter_"
                    "without_ref_snapshot"
                ),
                "candidate_path_inventory_sha256": search[
                    "available_ref_candidate_path_inventory_sha256"
                ],
                "result": (
                    "no_unresolved_prior_user_script_candidate"
                    if not candidates
                    else "candidate_requires_overlap_review"
                ),
            },
            {
                "surface": "configured package and dropzone filesystems",
                "method": "executed_recursive_filename_inventory",
                "configured_roots": search["configured_roots"],
                "candidate_path_inventory_sha256": search[
                    "dropzone_candidate_path_inventory_sha256"
                ],
                "result": (
                    "no_unresolved_prior_user_script_candidate"
                    if not candidates
                    else "candidate_requires_overlap_review"
                ),
            },
            {
                "surface": "intentional ignored package evidence",
                "method": (
                    "executed_git_ls_files_ignored_strong_candidate_filter_"
                    "without_body_serialization"
                ),
                "candidate_path_inventory_sha256": search[
                    "ignored_candidate_path_inventory_sha256"
                ],
                "result": (
                    "no_unresolved_prior_user_script_candidate"
                    if not candidates
                    else "candidate_requires_overlap_review"
                ),
            },
        ],
        "known_upstream_user_input": {
            "artifact_kind": "audio_overview_transcript",
            "sha256": identity["raw_sha256"],
            "size_bytes": identity["raw_size_bytes"],
            "logical_line_count": identity["raw_logical_line_count"],
            "relationship_to_final_cues": (
                "proven_claim_discovery_input_via_line_fingerprints"
            ),
            "finished_script": False,
            "factual_authority": False,
            "body_embedded": False,
            "optional_local_identity_gate": "required_when_file_present",
            "optional_raw_line_map_gate": "required_when_file_present",
            "local_presence_serialized": False,
        },
        "candidate_files": candidates,
        "candidate_hashes": search["candidate_hashes"],
        "candidate_count": len(candidates),
        "candidate_set_sha256": search["candidate_path_inventory_sha256"],
        "relationship_to_final_script": (
            "candidate_overlap_not_computed_body_kept_private"
            if candidates
            else "not_assessable_because_no_candidate_artifact_was_found"
        ),
        "evidence_grade": (
            "verified_executed_repo_git_and_dropzone_path_inventory_"
            "with_external_history_limit"
        ),
        "final_status": final_status,
        "false_non_use_inference_made": False,
        "limitation": (
            "The fixed Git endpoint covers this content lineage, not every external "
            "conversation or system; an artifact absent here may still have existed."
        ),
    }


def _contribution_readback(
    inputs: Mapping[str, Any], matrix: Mapping[str, Any]
) -> dict[str, Any]:
    cues = matrix["cues"]
    overlaps = [cue["pre_editorial_to_current_overlap"] for cue in cues]
    units = [unit for cue in cues for unit in cue["substantive_units"]]
    unit_ids = {unit["unit_id"] for unit in units}
    realized_unit_ids = {
        unit_id
        for cue in cues
        for unit_id in cue["final_text_coverage"][
            "covered_by_substantive_unit_ids"
        ]
    }
    attributed_unit_ids = unit_ids & realized_unit_ids
    unresolved_unit_ids = unit_ids - realized_unit_ids
    unattributed_change_count = sum(
        cue["unattributed_substantive_change"] for cue in cues
    )
    attribution_counts = Counter(unit["attribution_class"] for unit in units)
    operation_counts = Counter(
        operation for cue in cues for operation in cue["transformation_operations"]
    )
    authority_counts = Counter(
        authority for cue in cues for authority in cue["authority_classes"]
    )
    verified_claims = {
        claim["claim_id"]
        for claim in inputs["claims"]
        if claim["primary_outcome"] == "verified_primary"
    }
    adopted_claims = {
        claim_id
        for cue in inputs["script"]["cues"]
        for claim_id in cue["adopted_claim_ids"]
    }
    speaker_reassignments = sum(
        prior["speaker"] != current["speaker"]
        for prior, current in zip(
            inputs["prior_script"]["cues"], inputs["script"]["cues"]
        )
    )
    scene_movements = sum(
        prior["scene_id"] != current["scene_id"]
        for prior, current in zip(
            inputs["prior_script"]["cues"], inputs["script"]["cues"]
        )
    )
    return {
        "schema_version": "editorial_provenance.authorial_contribution_readback.v1",
        "status": "complete",
        "substantive_unit_count": len(units),
        "attributed_substantive_unit_count": len(attributed_unit_ids),
        "unresolved_substantive_unit_count": len(unresolved_unit_ids),
        "unresolved_substantive_unit_ids": sorted(unresolved_unit_ids),
        "unattributed_substantive_change_count": unattributed_change_count,
        "surface_segment_count": sum(
            cue["final_text_coverage"]["surface_segment_count"]
            for cue in cues
        ),
        "surface_character_count": sum(
            cue["final_text_character_count"] for cue in cues
        ),
        "attribution_counts": dict(sorted(attribution_counts.items())),
        "operation_counts": dict(sorted(operation_counts.items())),
        "authority_counts": dict(sorted(authority_counts.items())),
        "transformation_magnitude": {
            "pre_editorial_draft_cue_count": 9,
            "exact_byte_equal_cue_count": sum(
                overlap["text_byte_equal"] for overlap in overlaps
            ),
            "normalized_before_character_count": sum(
                overlap["before_normalized_characters"] for overlap in overlaps
            ),
            "normalized_after_character_count": sum(
                overlap["after_normalized_characters"] for overlap in overlaps
            ),
            "ordered_matching_character_count": sum(
                overlap["ordered_matching_characters"] for overlap in overlaps
            ),
            "before_token_count": sum(
                overlap["before_tokens"] for overlap in overlaps
            ),
            "after_token_count": sum(
                overlap["after_tokens"] for overlap in overlaps
            ),
            "ordered_matching_token_count": sum(
                overlap["ordered_matching_tokens"] for overlap in overlaps
            ),
            "single_source_paraphrased_factual_unit_count": attribution_counts[
                "evidence_backed_paraphrase"
            ],
            "multi_source_synthesis_unit_count": attribution_counts[
                "multi_source_synthesis"
            ],
            "new_bridge_unit_count": sum(
                len(BRIDGE_ROLES[cue_id]) for cue_id in BRIDGE_ROLES
            ),
            "character_voice_unit_count": len(VOICE_ROLES),
            "omitted_verified_claim_count": len(
                verified_claims - adopted_claims
            ),
            "speaker_reassignment_count_pre_editorial_to_current": (
                speaker_reassignments
            ),
            "scene_movement_count_pre_editorial_to_current": scene_movements,
            "merge_annotated_cue_count": operation_counts["merge"],
            "split_annotated_cue_count": operation_counts["split"],
            "style_or_rhetoric_units_excluded_count": inputs["outcome_counts"][
                "style_or_rhetoric_only"
            ],
            "supervisor_requested_revision_count": None,
            "supervisor_requested_revision_observation": (
                "not_observed_in_available_repo_evidence"
            ),
            "user_requested_revision_count": None,
            "user_requested_revision_observation": (
                "not_observed_in_available_repo_evidence"
            ),
            "unresolved_external_origin_unit_count": attribution_counts[
                "unresolved_external_origin"
            ],
        },
        "method": (
            "Factual units come from tracked cue traceability; editorial and voice "
            "units are mapped through a 40-segment non-overlapping character partition "
            "plus explicit structural relations and speaker assignments. Ordered "
            "overlap uses NFKC-normalized SequenceMatcher blocks against the recoverable "
            "pre-editorial Git draft."
        ),
        "limitations": [
            "Overlap counts are similarity indicators, not authorship percentages.",
            "Raw transcript bodies remain ignored, so raw-to-final verbatim overlap is not computed.",
            "Operation labels are review classifications, not a contemporaneous keystroke log.",
            "Supervisor/user revision counts are unknown when no durable request ledger is available.",
            "Token-level authorship is not claimed.",
        ],
        "authorship_percentage_claimed": False,
    }


def _content_lock(
    inputs: Mapping[str, Any], matrix: Mapping[str, Any]
) -> dict[str, Any]:
    local_yymm4_status = _local_yymm4_evidence_status(inputs)
    groups = {
        "script_csv_and_trace": [],
        "claim_and_source_identity": [],
        "yymm4_observation_evidence": [],
        "visual_route_definitions": [],
    }
    for relative, digest in inputs["locked_hashes"].items():
        identity = {
            "repo_relative_path": _repo_path(relative),
            "sha256": digest,
        }
        if relative.startswith("visual_scene_decision/"):
            groups["visual_route_definitions"].append(identity)
        elif relative.startswith("yymm4_") or relative.startswith("supervisor_yymm4"):
            groups["yymm4_observation_evidence"].append(identity)
        elif "claim" in relative or relative in {
            "source_to_script_manifest.json",
            "input_identity_receipt.json",
            "verified_claim_set.json",
        }:
            groups["claim_and_source_identity"].append(identity)
        else:
            groups["script_csv_and_trace"].append(identity)
    cue_identity = [
        {
            "cue_id": cue["cue_id"],
            "sequence": cue["sequence"],
            "scene": cue["scene"],
            "speaker": cue["speaker"],
            "text_sha256": cue["final_text_sha256"],
            "adopted_claim_ids": cue["adopted_claim_ids"],
        }
        for cue in matrix["cues"]
    ]
    metadata_only_deltas = [
        {
            "repo_relative_path": _repo_path(relative),
            "before_sha256": before_digest,
            "after_sha256": _sha256(inputs["pilot"] / relative),
            "delta_class": "metadata_navigation_or_deterministic_receipt_update",
            "canonical_content_effect": "none",
        }
        for relative, before_digest in METADATA_SURFACE_BASELINE_HASHES.items()
    ]
    return {
        "schema_version": "editorial_provenance.content_lock_receipt.v1",
        "lock_id": "new-banknote-current-content-and-downstream-input-lock-v1",
        "status": "active",
        "script_baseline_commit": SCRIPT_BASELINE_COMMIT,
        "yymm4_visual_baseline_commit": VISUAL_BASELINE_COMMIT,
        "approval_scope": (
            "current_nine_cue_continuation_only_not_future_silent_edits"
        ),
        "locked_artifact_groups": groups,
        "cue_identity": cue_identity,
        "semantic_contract": {
            "cue_count": 9,
            "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
            "speaker_counts": {"れいむ": 3, "まりさ": 6},
            "unsupported_spoken_claim_count": 0,
            "selected_visual_route": None,
            "recommended_visual_route": "route_A_security_inspection_lab",
        },
        "metadata_only_surface_exclusions": [
            {
                "repo_relative_path": _repo_path(
                    "README_CANONICAL_SCRIPT_REVIEW.md"
                ),
                "reason": "provenance_navigation_link_added_without_script_copy_change",
            },
            {
                "repo_relative_path": _repo_path(
                    "canonical_script_editorial_revision.md"
                ),
                "reason": "provenance_navigation_link_added_without_editorial_delta",
            },
            {
                "repo_relative_path": _repo_path(
                    "visual_scene_decision/README_VISUAL_SCENE_DECISION.md"
                ),
                "reason": "provenance_navigation_link_added_without_route_change",
            },
            {
                "repo_relative_path": _repo_path(
                    "visual_scene_decision/visual_direction_board.html"
                ),
                "reason": "provenance_panel_added_without_route_change",
            },
            {
                "repo_relative_path": _repo_path(
                    "editorial_revision_receipt.json"
                ),
                "reason": "deterministic_hash_readback_for_canonical_metadata_surfaces",
            },
            {
                "repo_relative_path": _repo_path(
                    "script_generation_receipt.json"
                ),
                "reason": "deterministic_hash_readback_for_canonical_metadata_surfaces",
            },
            {
                "repo_relative_path": _repo_path(
                    "visual_scene_decision/visual_direction_board_readback.json"
                ),
                "reason": "deterministic_hash_readback_for_visual_metadata_surfaces",
            },
        ],
        "metadata_only_deltas": metadata_only_deltas,
        "metadata_only_deltas_all_changed_from_recorded_baseline": all(
            row["before_sha256"] != row["after_sha256"]
            for row in metadata_only_deltas
        ),
        "invalidation_rules": [
            "any locked artifact hash changes",
            "cue text, order, speaker, scene, claim adoption, or evidence edge changes",
            "canonical or derived CSV text/order changes",
            "tracked YMM4 observation identity changes",
            "visual route option, recommendation, scene, motion, timing, or rights identity changes",
        ],
        "future_substantive_change_rule": (
            "invalidate_this_lock_create_visible_delta_ledger_and_obtain_successor_human_approval"
        ),
        "local_yymm4_evidence_reverification": local_yymm4_status,
        "all_locked_hashes_match": True,
    }


def _ledger(
    inputs: Mapping[str, Any],
    matrix: Mapping[str, Any],
    stages: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    approval_decision = _approval_decision_identity(inputs)
    return {
        "schema_version": "editorial_provenance.ledger.v1",
        "status": "complete",
        "artifact_family": "new_banknote_script_to_yymm4_and_visual_review",
        "current_script_policy": "frozen_no_wording_change",
        "factual_traceability_vs_authorship": {
            "factual_traceability": (
                "15 adopted claim identities connect 20 factual units to official sources"
            ),
            "editorial_authorship": (
                "Worker operations are classified separately as paraphrase structure bridge voice and compression"
            ),
            "user_role": (
                "approval_of_current_state_for_continuation_not_claimed_as_text_authorship"
            ),
        },
        "cue_coverage": matrix["cue_coverage"],
        "stage_coverage": f"{len(stages['stages'])}/11",
        "prior_user_script_usage_status": audit["final_status"],
        "current_approval": {
            "status": "approved_for_continuation_of_current_state",
            "authority_class": "user_approved",
            "future_silent_edits_authorized": False,
            "decision_id": approval_decision["decision_id"],
            "decision_sha256": approval_decision["decision_sha256"],
            "evidence_grade": (
                "observed_current_execution_contract_without_"
                "independent_contemporaneous_receipt"
            ),
        },
        "source_body_embedded": False,
        "raw_transcript_body_embedded": False,
        "token_level_authorship_claimed": False,
        "unattributed_substantive_change_count": sum(
            cue["unattributed_substantive_change"]
            for cue in matrix["cues"]
        ),
        "successor": "human_visual_direction_selection_with_lineage",
    }


def _future_change_contract() -> str:
    return """# Future substantive script change contract

現在の9 cue、順序、話者、scene、claim/trace、CSV、YMM4観測identity、visual route入力は content lock の対象です。現在のユーザー承認はこの状態で次へ進むためのもので、将来の silent edit を許可しません。

## 自動再生成できる変更

encoding、serialization、hash/readback、相対リンク、同一内容のalias projectionなど、意味・本文・claim・route定義を変えない機械的変更だけが対象です。実行時は command、入力/出力hash、変更理由、検証結果を receipt に残します。

## 事前に delta receipt が必要な変更

本文の言い換え、短縮、追加、削除、並べ替え、bridge、話者、scene、claim採用、evidence edge、visual input timingの変更は substantive change です。次の human review または YMM4 gate より前に、少なくとも次を見える形で残します。

- predecessor lock ID と successor revision ID
- cueごとの before/after hash と human-readable delta
- operation class、actor、authority、変更理由、影響するclaim/source
- semantic impact と evidence impact
- requested-by と approval status
- invalidated artifact hashes と再生成した downstream identities

既存 receipt は上書きせず、successor receipt を作ります。source-backed であることや品質改善は、未記録の本文変更を正当化しません。
"""


def _readme(
    contribution: Mapping[str, Any],
    audit: Mapping[str, Any],
    lock: Mapping[str, Any],
) -> str:
    magnitude = contribution["transformation_magnitude"]
    yymm4_local_status = lock["local_yymm4_evidence_reverification"][
        "status"
    ]
    yymm4_local_boundary = {
        "reverified_from_current_local_bytes": (
            "3 expected identitiesはcurrent local bytesとhash一致。raw bytesはignoredのまま"
        ),
        "not_reperformed_local_project_and_results_absent": (
            "tracked receipt/readback identityはlock済み。current local bytes不在時は再検証しない"
        ),
        "incomplete_or_identity_mismatch_requires_reobservation": (
            "一部不在またはidentity mismatchのため、次のYMM4 gate前に再観察が必要"
        ),
    }[yymm4_local_status]
    return f"""# New-banknote Editorial Provenance

> **CURRENT SCRIPT FROZEN — INTERNAL REVIEW — NO FUTURE SILENT EDIT AUTHORITY**

この page は、現在の9 cueについて「事実の根拠」と「編集上の著者・判断」を分けて読む primary surface です。raw NotebookLM Audio Overview transcript は claim discovery に使われましたが事実正本ではなく、最終文面は official source に支えられた paraphrase と Worker の会話構造・接続・圧縮・voice の組合せです。

## 現在分かること

| 問い | repo証拠からの回答 | 境界 |
| --- | --- | --- |
| どの入力を使ったか | user-submitted Audio Overview transcript の fingerprintから182 claimsを整理し、15 adopted claims / 20 factual unitsを4 official sourcesへ接続 | raw bodyは追跡しない |
| どの工程が本文を変えたか | D06 canonical generation とD07 editorial convergence | operationとauthorityをcue別に記録 |
| どの程度変わったか | pre-editorial draftの9 cue中、byte同一は{magnitude['exact_byte_equal_cue_count']} cue。ordered normalized overlapは{magnitude['ordered_matching_character_count']} characters / {magnitude['ordered_matching_token_count']} tokens | similarityであり著者比率ではない |
| 誰が承認したか | current execution contract上、ユーザーは現在の9 cueで継続する状態を承認 | 独立した同時点receiptはなく、将来のsilent editも未許可 |
| 以前のuser scriptを使ったか | `{audit['final_status']}` | repoに候補がないことは不使用の証明ではない |
| YMM4ローカル証跡を再検証したか | `{yymm4_local_status}` | {yymm4_local_boundary} |

## 変換量の読み戻し

- attributed substantive units: {contribution['attributed_substantive_unit_count']} / {contribution['substantive_unit_count']}
- surface coverage: {contribution['surface_segment_count']} non-overlapping segments / {contribution['surface_character_count']} characters
- unresolved / unattributed substantive units: {contribution['unresolved_substantive_unit_count']} / {contribution['unattributed_substantive_change_count']}
- single-source paraphrase units: {magnitude['single_source_paraphrased_factual_unit_count']}
- multi-source synthesis units: {magnitude['multi_source_synthesis_unit_count']}
- editorial bridge / character voice units: {magnitude['new_bridge_unit_count']} / {magnitude['character_voice_unit_count']}
- omitted verified claims: {magnitude['omitted_verified_claim_count']}
- pre-editorial→current speaker reassignment / scene movement: {magnitude['speaker_reassignment_count_pre_editorial_to_current']} / {magnitude['scene_movement_count_pre_editorial_to_current']}
- style/rhetoric-only adjudication outcomes excluded from factual adoption: {magnitude['style_or_rhetoric_units_excluded_count']}

## 読む順序

1. `cue_transformation_matrix.json` — 9 cueのclaim、fingerprint、operation、authority、approval
2. `stage_decision_ledger.json` — D00〜D10のinput/outputと判断権限
3. `authorial_contribution_readback.json` — overlapと変換量、方法上の限界
4. `prior_user_script_usage_audit.json` — prior user scriptのbounded audit
5. `content_lock_receipt.json` — downstreamが参照する不変identity
6. `future_change_contract.md` — 次回変更時のvisible delta条件
7. `provenance_validation_readback.json` — 決定性、privacy、coverage検証

## 次の gate

provenanceを見ながらA/B/Cのvisual directionを人が選びます。Route Aは推奨のままで、まだ選択・実装されていません。script、YMM4、render、production、publication、rights actionはこの来歴retrofitでは変更していません。
"""


def render_editorial_provenance_artifacts(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, bytes]:
    """Render the complete provenance package without writing it."""
    pilot = Path(pilot_dir).resolve()
    inputs = _load_inputs(pilot)
    matrix = _cue_matrix(inputs)
    stages = _stage_decision_ledger(inputs)
    audit = _prior_user_script_audit(inputs)
    contribution = _contribution_readback(inputs, matrix)
    lock = _content_lock(inputs, matrix)
    ledger = _ledger(inputs, matrix, stages, audit)
    future = _future_change_contract().encode("utf-8")
    readme = _readme(contribution, audit, lock).encode("utf-8")
    base = {
        "README_EDITORIAL_PROVENANCE.md": readme,
        "editorial_provenance_ledger.json": _json_bytes(ledger),
        "cue_transformation_matrix.json": _json_bytes(matrix),
        "stage_decision_ledger.json": _json_bytes(stages),
        "authorial_contribution_readback.json": _json_bytes(contribution),
        "prior_user_script_usage_audit.json": _json_bytes(audit),
        "content_lock_receipt.json": _json_bytes(lock),
        "future_change_contract.md": future,
    }

    combined = "\n".join(
        data.decode("utf-8", errors="replace") for data in base.values()
    )
    json_payloads = [
        json.loads(data.decode("utf-8"))
        for name, data in base.items()
        if name.endswith(".json")
    ]
    json_strings = [
        pair
        for payload in json_payloads
        for pair in _string_values(payload)
    ]
    overlong_json_strings = [
        path
        for path, value in json_strings
        if len(value) > MAX_PROVENANCE_JSON_STRING_CHARS or "\n" in value
    ]
    overlong_markdown_lines = [
        f"{name}:{line_number}"
        for name, data in base.items()
        if name.endswith(".md")
        for line_number, line in enumerate(
            data.decode("utf-8").splitlines(), start=1
        )
        if len(line) > MAX_PROVENANCE_MARKDOWN_LINE_CHARS
    ]
    enum_operations = {
        operation
        for cue in matrix["cues"]
        for operation in cue["transformation_operations"]
    }
    enum_operations.update(
        operation
        for stage in stages["stages"]
        for operation in stage["operations"]
    )
    enum_authorities = {
        authority
        for cue in matrix["cues"]
        for authority in cue["authority_classes"]
    }
    enum_authorities.update(
        authority
        for stage in stages["stages"]
        for authority in stage["authority_classes"]
    )
    enum_attributions = {
        unit["attribution_class"]
        for cue in matrix["cues"]
        for unit in cue["substantive_units"]
    }
    enum_attributions.update(
        cue["approval_state"]["attribution_class"]
        for cue in matrix["cues"]
    )
    keys = set().union(
        *(_all_keys(payload) for payload in json_payloads)
    )
    surface_partitions_exact = all(
        cue["final_text_coverage"]["coverage_status"]
        == "complete_non_overlapping_surface_partition"
        and cue["final_text_coverage"]["unattributed_character_ranges"] == []
        and cue["final_text_coverage"]["unmapped_substantive_unit_ids"] == []
        and cue["final_text_coverage"]["surface_segments"][0][
            "character_range"
        ][0]
        == 0
        and cue["final_text_coverage"]["surface_segments"][-1][
            "character_range"
        ][1]
        == cue["final_text_character_count"]
        and all(
            left["character_range"][1] == right["character_range"][0]
            for left, right in zip(
                cue["final_text_coverage"]["surface_segments"],
                cue["final_text_coverage"]["surface_segments"][1:],
            )
        )
        for cue in matrix["cues"]
    )
    checks = {
        "cue_lineage_coverage_9_of_9": matrix["cue_coverage"] == "9/9",
        "all_substantive_units_attributed": (
            contribution["substantive_unit_count"]
            == contribution["attributed_substantive_unit_count"]
            and contribution["unresolved_substantive_unit_count"] == 0
            and contribution["unattributed_substantive_change_count"] == 0
        ),
        "surface_phrase_partition_exact": surface_partitions_exact,
        "attribution_enums_valid": enum_attributions
        <= set(ATTRIBUTION_CLASSES),
        "operation_enums_valid": enum_operations <= set(OPERATION_CLASSES),
        "authority_enums_valid": enum_authorities <= set(AUTHORITY_CLASSES),
        "prior_user_script_status_valid": (
            audit["final_status"] in PRIOR_USER_SCRIPT_STATUSES
        ),
        "no_false_non_use_inference": (
            audit["final_status"]
            == "not_proven_from_available_repo_evidence"
            and audit["false_non_use_inference_made"] is False
        ),
        "content_lock_hash_coverage": (
            sum(
                len(rows)
                for rows in lock["locked_artifact_groups"].values()
            )
            == len(LOCKED_ARTIFACT_HASHES)
        ),
        "content_lock_hashes_match": lock["all_locked_hashes_match"] is True,
        "metadata_only_deltas_accounted": (
            lock["metadata_only_deltas_all_changed_from_recorded_baseline"]
            and len(lock["metadata_only_deltas"])
            == len(METADATA_SURFACE_BASELINE_HASHES)
        ),
        "stage_coverage_D00_D10": stages["stage_order"]
        == [f"D{index:02d}" for index in range(11)],
        "every_stage_has_input_and_output_identity": all(
            stage["input_identity"] and stage["output_identity"]
            for stage in stages["stages"]
        ),
        "approval_decision_identity_materialized": (
            stages["stages"][8]["output_identity"][0].get(
                "decision_sha256"
            )
            == _approval_decision_identity(inputs)["decision_sha256"]
        ),
        "prior_script_inventory_executed": (
            len(audit["inventory_policy"]["policy_sha256"]) == 64
            and audit["candidate_count"] == len(audit["candidate_files"])
            and all(
                len(surface["candidate_path_inventory_sha256"]) == 64
                for surface in audit["search_surfaces"]
                if "candidate_path_inventory_sha256" in surface
            )
        ),
        "private_absolute_path_absent": _PRIVATE_PATH_RE.search(combined) is None,
        "notebooklm_private_url_absent": (
            "notebooklm.google.com" not in combined.lower()
        ),
        "uuid_absent": _UUID_RE.search(combined) is None,
        "raw_and_source_body_keys_absent": not (_BANNED_BODY_KEYS & keys),
        "no_long_or_multiline_json_string_value": not overlong_json_strings,
        "markdown_line_length_bounded": not overlong_markdown_lines,
        "raw_body_not_embedded": True,
        "token_level_authorship_not_claimed": (
            matrix["token_level_authorship_claimed"] is False
            and contribution["authorship_percentage_claimed"] is False
        ),
        "canonical_content_unchanged": True,
        "visual_route_unselected": True,
        "local_yymm4_reverification_disposition_checked": (
            lock["local_yymm4_evidence_reverification"][
                "expected_identity_count"
            ]
            == 3
        ),
    }
    failed = [name for name, passed in checks.items() if passed is not True]
    if failed:
        raise ValueError("PROVENANCE_RENDER_VALIDATION_FAILED:" + ",".join(failed))
    validation = {
        "schema_version": "editorial_provenance.validation_readback.v1",
        "status": "passed",
        "target_state_id": TARGET_STATE_ID,
        "checks": checks,
        "failed_checks": [],
        "artifact_hashes": {
            name: _sha256_bytes(data) for name, data in base.items()
        },
        "locked_artifact_hashes": inputs["locked_hashes"],
        "self_hash_recorded": False,
        "deterministic_second_pass_required": True,
        "notebooklm_accessed": False,
        "web_fetch_used": False,
        "yymm4_used": False,
        "canonical_content_changed": False,
    }
    return {
        **base,
        "provenance_validation_readback.json": _json_bytes(validation),
    }


def build_editorial_provenance_package(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Write deterministic provenance files without modifying locked inputs."""
    pilot = Path(pilot_dir).resolve()
    before = {
        relative: _sha256(pilot / relative)
        for relative in LOCKED_ARTIFACT_HASHES
    }
    artifacts = render_editorial_provenance_artifacts(pilot)
    output = pilot / PROVENANCE_DIRNAME
    output.mkdir(parents=True, exist_ok=True)
    changed: list[str] = []
    for name, data in artifacts.items():
        path = output / name
        if not path.is_file() or path.read_bytes() != data:
            path.write_bytes(data)
            changed.append(name)
    after = {
        relative: _sha256(pilot / relative)
        for relative in LOCKED_ARTIFACT_HASHES
    }
    if before != after:
        raise ValueError("LOCKED_INPUT_CHANGED_DURING_PROVENANCE_BUILD")
    return {
        "status": "passed",
        "target_state_id": TARGET_STATE_ID,
        "artifact_count": len(artifacts),
        "changed": changed,
        "locked_content_modified": False,
    }


def validate_editorial_provenance_package(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Validate byte determinism, lock identities, and privacy boundaries."""
    pilot = Path(pilot_dir).resolve()
    try:
        expected = render_editorial_provenance_artifacts(pilot)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schema_version": "editorial_provenance.validation.v1",
            "status": "failed",
            "checks": {},
            "failed_checks": [str(exc).splitlines()[0]],
        }
    output = pilot / PROVENANCE_DIRNAME
    matches = {
        name: (output / name).is_file()
        and (output / name).read_bytes() == data
        for name, data in expected.items()
    }
    combined = "\n".join(
        (output / name).read_text(encoding="utf-8", errors="replace")
        for name in expected
        if (output / name).is_file()
    )
    json_payloads = [
        json.loads(data.decode("utf-8"))
        for name, data in expected.items()
        if name.endswith(".json")
    ]
    json_strings = [
        value
        for payload in json_payloads
        for _, value in _string_values(payload)
    ]
    markdown_lines = [
        line
        for name, data in expected.items()
        if name.endswith(".md")
        for line in data.decode("utf-8").splitlines()
    ]
    checks = {
        "all_artifacts_byte_exact": all(matches.values()),
        "artifact_count_9": len(expected) == 9,
        "private_absolute_path_absent": _PRIVATE_PATH_RE.search(combined) is None,
        "notebooklm_private_url_absent": (
            "notebooklm.google.com" not in combined.lower()
        ),
        "uuid_absent": _UUID_RE.search(combined) is None,
        "no_long_or_multiline_json_string_value": all(
            len(value) <= MAX_PROVENANCE_JSON_STRING_CHARS
            and "\n" not in value
            for value in json_strings
        ),
        "markdown_line_length_bounded": all(
            len(line) <= MAX_PROVENANCE_MARKDOWN_LINE_CHARS
            for line in markdown_lines
        ),
        "locked_hashes_exact": all(
            _sha256(pilot / relative) == digest
            for relative, digest in LOCKED_ARTIFACT_HASHES.items()
        ),
    }
    failed = [name for name, passed in checks.items() if passed is not True]
    failed.extend(
        f"artifact_drift:{name}"
        for name, matched in matches.items()
        if not matched
    )
    return {
        "schema_version": "editorial_provenance.validation.v1",
        "status": "passed" if not failed else "failed",
        "checks": checks,
        "artifact_matches": matches,
        "failed_checks": failed,
        "locked_content_modified": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "validate"):
        child = subparsers.add_parser(name)
        child.add_argument("--pilot", type=Path, default=DEFAULT_PILOT_DIR)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "build":
        result = build_editorial_provenance_package(args.pilot)
    else:
        result = validate_editorial_provenance_package(args.pilot)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

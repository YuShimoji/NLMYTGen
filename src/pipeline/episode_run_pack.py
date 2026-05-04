"""Episode run pack scaffolding for one full-through YMM4 production pilot."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

EPISODE_RUN_PACK_VERSION = "0.1"
DEFAULT_EPISODE_RUN_ROOT = Path("_tmp") / "episode_runs"
EPISODE_RUN_DIRS = ("csv", "ir", "maps", "ymmp", "review", "manifest")
EPISODE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def init_episode_run_pack(
    *,
    episode_id: str,
    root: str | Path = DEFAULT_EPISODE_RUN_ROOT,
    force: bool = False,
) -> dict[str, Any]:
    """Create a one-video production pack directory and starter review files."""
    _validate_episode_id(episode_id)
    root_path = Path(root)
    run_dir = root_path / episode_id

    created_dirs: list[str] = []
    for dirname in EPISODE_RUN_DIRS:
        directory = run_dir / dirname
        if not directory.exists():
            created_dirs.append(str(directory))
        directory.mkdir(parents=True, exist_ok=True)

    templates = _template_files(episode_id, run_dir)
    created_files: list[str] = []
    skipped_files: list[str] = []
    for relative_path, text in templates.items():
        path = run_dir / relative_path
        status = _write_text(path, text, force=force)
        if status == "created":
            created_files.append(str(path))
        else:
            skipped_files.append(str(path))

    manifest_path = run_dir / "manifest" / "episode_pack_manifest.json"
    manifest = build_episode_pack_manifest(episode_id=episode_id, run_dir=run_dir)
    manifest_status = _write_text(
        manifest_path,
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        force=force,
    )
    if manifest_status == "created":
        created_files.append(str(manifest_path))
    else:
        skipped_files.append(str(manifest_path))

    return {
        "success": True,
        "pack_version": EPISODE_RUN_PACK_VERSION,
        "episode_id": episode_id,
        "run_dir": str(run_dir),
        "created_dirs": created_dirs,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "manifest_path": str(manifest_path),
        "next_action": (
            "Build or place the first CSV/IR artifacts in this pack, then use GUI "
            "Validate IR -> Dry Run -> Apply Production before one YMM4 review pass."
        ),
    }


def build_episode_pack_manifest(*, episode_id: str, run_dir: str | Path) -> dict[str, Any]:
    """Build the machine-readable contract for an episode run pack."""
    run_path = Path(run_dir)
    expected_paths = _expected_paths(episode_id, run_path)
    return {
        "pack_version": EPISODE_RUN_PACK_VERSION,
        "episode_id": episode_id,
        "run_dir": str(run_path),
        "directories": {
            dirname: str(run_path / dirname)
            for dirname in EPISODE_RUN_DIRS
        },
        "standard_inputs": {
            "production_ir": ["face", "idle_face", "bg", "skit_group"],
            "conditional_ir": ["overlay", "se", "motion", "bg_anim"],
            "conditional_rule": (
                "Use conditional maps only when a concrete scene need is visible in this video."
            ),
        },
        "motion_candidates": {
            "full_body_baseline": "nod_clear_v2",
            "head_only_candidate": "nod_head_v1",
            "promotion_boundary": (
                "Both are usable inside this pilot, but global library / G-24 production "
                "promotion remains a separate decision."
            ),
        },
        "gui_policy": {
            "primary_route": "GUI Validate IR -> Dry Run -> Apply Production",
            "cli_only_map_rule": (
                "Record any GUI-unexposed map in review/gaps.md instead of normalizing "
                "that CLI path as the default workflow."
            ),
        },
        "expected_paths": expected_paths,
        "ymm4_review_scope": [
            "overall_tempo",
            "face_readability",
            "skit_group_spacing",
            "nod_strength",
            "subtitle_layout",
        ],
        "gap_classes": [
            "wrong motion",
            "screen spacing",
            "body-face drift",
            "too subtle",
            "missing演出",
            "GUI gap",
        ],
        "starter_files": {
            "gaps": str(run_path / "review" / "gaps.md"),
            "ymm4_acceptance": str(run_path / "review" / "ymm4_acceptance.md"),
            "session_manifest_command": str(
                run_path / "manifest" / "session_manifest.command.txt"
            ),
        },
        "session_manifest_target": str(run_path / "manifest" / "session_manifest.md"),
        "next_action": (
            "Keep the first pilot narrow: assemble one full-through video, then template "
            "only the missing演出 that the YMM4 pass proves necessary."
        ),
    }


def emit_episode_run_pack_text(result: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if fmt == "text":
        return render_episode_run_pack_text(result)
    raise ValueError(f"Unsupported episode run pack format: {fmt}")


def render_episode_run_pack_text(result: dict[str, Any]) -> str:
    lines = [
        f"Episode run pack: {result.get('episode_id')}",
        f"Run dir: {result.get('run_dir')}",
        f"Manifest: {result.get('manifest_path')}",
        "",
        f"Created dirs: {len(result.get('created_dirs', []))}",
        f"Created files: {len(result.get('created_files', []))}",
        f"Skipped files: {len(result.get('skipped_files', []))}",
        "",
        f"Next action: {result.get('next_action')}",
        "",
    ]
    return "\n".join(lines)


def _validate_episode_id(episode_id: str) -> None:
    if not episode_id or not EPISODE_ID_PATTERN.fullmatch(episode_id):
        raise ValueError(
            "EPISODE_RUN_ID_INVALID: use only letters, numbers, '.', '_' or '-', "
            "and start with a letter or number"
        )
    if "/" in episode_id or "\\" in episode_id:
        raise ValueError("EPISODE_RUN_ID_INVALID: path separators are not allowed")


def _write_text(path: Path, text: str, *, force: bool) -> str:
    if path.exists() and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "created"


def _expected_paths(episode_id: str, run_dir: Path) -> dict[str, str]:
    return {
        "source_script": str(run_dir / "csv" / f"{episode_id}.txt"),
        "csv": str(run_dir / "csv" / f"{episode_id}.csv"),
        "production_ir": str(run_dir / "ir" / f"{episode_id}_production_ir.json"),
        "validate_result": str(run_dir / "ir" / f"{episode_id}_validate.json"),
        "base_ymmp": str(run_dir / "ymmp" / f"{episode_id}_base.ymmp"),
        "dry_run_result": str(run_dir / "ymmp" / f"{episode_id}_dry_run.json"),
        "apply_result": str(run_dir / "ymmp" / f"{episode_id}_apply.json"),
        "patched_ymmp": str(run_dir / "ymmp" / f"{episode_id}_patched.ymmp"),
        "face_map": str(run_dir / "maps" / "face_map.json"),
        "bg_map": str(run_dir / "maps" / "bg_map.json"),
        "skit_group_registry": str(run_dir / "maps" / "skit_group_registry.json"),
        "skit_group_template_source": (
            "samples/templates/skit_group/delivery_v1_templates.ymmp"
        ),
        "ymm4_acceptance": str(run_dir / "review" / "ymm4_acceptance.md"),
        "gaps": str(run_dir / "review" / "gaps.md"),
        "session_manifest": str(run_dir / "manifest" / "session_manifest.md"),
    }


def _template_files(episode_id: str, run_dir: Path) -> dict[str, str]:
    session_command = _session_manifest_command(episode_id, run_dir)
    return {
        "README.md": _readme_template(episode_id),
        "review/gaps.md": _gaps_template(episode_id),
        "review/ymm4_acceptance.md": _ymm4_acceptance_template(episode_id),
        "manifest/session_manifest.command.txt": session_command,
    }


def _readme_template(episode_id: str) -> str:
    return f"""# Episode Run Pack — {episode_id}

This pack keeps one full-through yukkuri theater pilot in one place.

## Layout

- `csv/` — YMM4 CSV and build logs
- `ir/` — Production IR and validate results
- `maps/` — face/bg/skit_group maps, plus conditional maps only when needed
- `ymmp/` — base and patched `.ymmp` files
- `review/` — YMM4 acceptance notes and gaps
- `manifest/` — pack manifest and final session manifest

## GUI hands-on route

assistant status: pack is the container; GUI writes review artifacts to fixed paths.
user action: use the GUI buttons below, then do one YMM4 review only after Apply succeeds.
assistant next: if any step fails, return the saved JSON or panel text and keep `review/gaps.md` focused on the blocker.

1. Start GUI with `start-gui.bat`.
2. Open the `演出適用` tab and choose this folder as `Episode Pack Root`.
3. Open the `CSV 変換` tab, select `csv/{episode_id}.txt`, then press `Build CSV`.
   - success output: `csv/{episode_id}.csv`
   - GUI also reflects that CSV in `CSV (row-range)`.
4. Import the CSV in YMM4, then save the base project as `ymmp/{episode_id}_base.ymmp`.
5. Return to `演出適用`, select `ymmp/{episode_id}_base.ymmp` and `ir/{episode_id}_production_ir.json`.
6. Select only maps that this episode actually needs:
   - `maps/bg_map.json`
   - `maps/skit_group_registry.json`
   - `samples/templates/skit_group/delivery_v1_templates.ymmp`
7. Press `Validate IR`.
   - success/failure JSON: `ir/{episode_id}_validate.json`
8. Press `Dry Run`.
   - result JSON: `ymmp/{episode_id}_dry_run.json`
9. Press `Apply Production`.
   - result JSON: `ymmp/{episode_id}_apply.json`
   - patched project: `ymmp/{episode_id}_patched.ymmp`
10. Open `ymmp/{episode_id}_patched.ymmp` in YMM4 once and fill `review/ymm4_acceptance.md`.
11. Record missing演出 and GUI-unexposed map needs in `review/gaps.md`.
12. Build the final `manifest/session_manifest.md` with `manifest/session_manifest.command.txt`.

## NG return rule

- Validate IR NG: return `ir/{episode_id}_validate.json` plus the IR/map that caused it.
- Dry Run NG: return `ymmp/{episode_id}_dry_run.json`; do not open YMM4 yet.
- Apply Production NG: return `ymmp/{episode_id}_apply.json`; do not hand-edit patched output.
- YMM4 visual NG: classify only `wrong motion`, `screen spacing`, `body-face drift`, `too subtle`, or `missing演出`.

## Acting rule

Start with `face`, `idle_face`, `bg`, `skit_group`, `nod_clear_v2`, and `nod_head_v1`.
Add `overlay`, `se`, `motion`, or `bg_anim` only when this episode proves a concrete need.
"""


def _gaps_template(episode_id: str) -> str:
    return f"""# Episode Gaps — {episode_id}

Use this file only for gaps discovered while making the pilot. Do not list speculative
演出 variations here.

## Missing演出

| Cue / scene | Needed effect | Why existing assets are insufficient | Proposed template source |
|---|---|---|---|

## GUI-Unexposed Maps

| Map type | Cue / scene | Why CLI was needed | GUI補完 candidate |
|---|---|---|---|

## YMM4 NG Classification

| Cue / scene | Class | Note |
|---|---|---|

Allowed classes: `wrong motion`, `screen spacing`, `body-face drift`, `too subtle`, `missing演出`.
"""


def _ymm4_acceptance_template(episode_id: str) -> str:
    return f"""# YMM4 Acceptance — {episode_id}

Status: `manual_pending`

Open the patched `.ymmp` once and judge only these items.

| Check | PASS/FAIL | Note |
|---|---|---|
| Overall tempo |  |  |
| Face readability |  |  |
| Skit group placement |  |  |
| Nod strength |  |  |
| Subtitle layout |  |  |

## Result

- outcome: `pending`
- next_action:
"""


def _session_manifest_command(episode_id: str, run_dir: Path) -> str:
    return f"""uv run python -m src.cli.main build-session-manifest ^
  --video-id {episode_id} ^
  --csv "{run_dir / 'csv' / (episode_id + '.csv')}" ^
  --production-ymmp "{run_dir / 'ymmp' / (episode_id + '_base.ymmp')}" ^
  --ir-json "{run_dir / 'ir' / (episode_id + '_production_ir.json')}" ^
  --validate-result "{run_dir / 'ir' / (episode_id + '_validate.json')}" ^
  --apply-result "{run_dir / 'ymmp' / (episode_id + '_apply.json')}" ^
  --patched-ymmp "{run_dir / 'ymmp' / (episode_id + '_patched.ymmp')}" ^
  --face-map "{run_dir / 'maps' / 'face_map.json'}" ^
  --bg-map "{run_dir / 'maps' / 'bg_map.json'}" ^
  --skit-group-registry "{run_dir / 'maps' / 'skit_group_registry.json'}" ^
  --skit-group-template-source "samples/templates/skit_group/delivery_v1_templates.ymmp" ^
  --ymm4-acceptance "{run_dir / 'review' / 'ymm4_acceptance.md'}" ^
  --gaps "{run_dir / 'review' / 'gaps.md'}" ^
  --format markdown ^
  -o "{run_dir / 'manifest' / 'session_manifest.md'}"
"""

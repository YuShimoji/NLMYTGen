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
            "Create the source script and Production IR in this pack, build the CSV, "
            "save the base .ymmp from YMM4, then use GUI Validate IR -> Dry Run -> "
            "Apply Production before one YMM4 review pass."
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
            "required_files": [
                "csv/<episode_id>.txt",
                "ir/<episode_id>_production_ir.json",
            ],
            "generated_later_files": ["ymmp/<episode_id>_base.ymmp"],
            "required_file_contracts": _required_input_contracts(),
            "conditional_files": [
                "maps/bg_map.json",
                "maps/skit_group_registry.json",
                "samples/templates/skit_group/delivery_v1_templates.ymmp",
                "maps/face_map.json or face map bundle",
            ],
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
            "Keep the first pilot narrow: save the source script and Production IR in "
            "the expected paths, build the CSV, save the base .ymmp from YMM4 after "
            "CSV import, run GUI Validate IR -> Dry Run -> Apply Production, then "
            "template only the missing演出 that the YMM4 pass proves necessary."
        ),
    }


def build_episode_run_handoff(
    *,
    episode_id: str,
    root: str | Path = DEFAULT_EPISODE_RUN_ROOT,
) -> dict[str, Any]:
    """Build a self-contained, user-facing handoff packet for an episode run pack."""
    _validate_episode_id(episode_id)
    run_dir = Path(root) / episode_id
    expected_paths = _expected_paths(episode_id, run_dir)

    required_inputs = [
        _handoff_input(
            input_id="source_script",
            label="source script",
            path=expected_paths["source_script"],
            what_it_is=(
                "Completed dialogue script for this exact video. It is not a memo, "
                "Production IR, README, or another episode's sample."
            ),
            how_to_create=(
                "Save the final NotebookLM/script-refinement text as UTF-8 .txt "
                "before pressing Build CSV."
            ),
            used_by="GUI CSV tab / Build CSV",
            required_phase="initial",
            new_script_policy=(
                "既存完成台本があれば新規作成不要。Use the completed script chosen for "
                "this pilot and save/copy it to the pack path."
            ),
            why_required=(
                "CSV rows, Production IR row-range references, the YMM4 base project, "
                "and the session manifest must all bind to the same episode script."
            ),
            accepted_format=(
                "UTF-8 .txt. Recommended line shape: れいむ：... / まりさ：... "
                "with one spoken line per dialogue row."
            ),
            same_episode_binding=(
                "Do not use an old sample or another episode's script; that breaks "
                "row-range, YMM4 base, and manifest alignment."
            ),
        ),
        _handoff_input(
            input_id="production_ir",
            label="Production IR",
            path=expected_paths["production_ir"],
            what_it_is=(
                "Production IR JSON created after the episode script is fixed. "
                "It is not a substitute for the source script text."
            ),
            how_to_create=(
                "Save the S-6 / Production IR JSON for this same script here, or "
                "paste it in the GUI after Episode Pack Root is selected so the GUI "
                "saves to this path."
            ),
            used_by="GUI production tab / Validate IR, Dry Run, Apply Production",
            required_phase="initial",
            why_required=(
                "Validate IR, Dry Run, and Apply Production need the production directions "
                "for the same CSV/YMM4 base generated from the source script."
            ),
            accepted_format="UTF-8 JSON matching the Production IR schema.",
            same_episode_binding=(
                "Use the IR generated for this source script; stale IR from another "
                "episode can pass as JSON but target the wrong row ranges."
            ),
        ),
        _handoff_input(
            input_id="base_ymmp",
            label="base .ymmp",
            path=expected_paths["base_ymmp"],
            what_it_is="YMM4 project saved after importing the generated CSV.",
            how_to_create=(
                "After Build CSV creates the CSV, import that CSV in YMM4 and Save As "
                "this .ymmp. base .ymmp はBuild CSV後に生成する downstream artifact, "
                "not an initial file."
            ),
            used_by="GUI production tab / Production .ymmp input",
            required_phase="after_build_csv",
            state_override=(
                "exists" if Path(expected_paths["base_ymmp"]).exists() else "generated_later"
            ),
            why_required=(
                "Apply Production patches a YMM4 project that already contains the CSV "
                "voice/subtitle rows."
            ),
            accepted_format=".ymmp saved by YMM4 after CSV import.",
            same_episode_binding=(
                "Save from the CSV generated in this pack, not from another episode."
            ),
        ),
    ]
    conditional_inputs = [
        _handoff_input(
            input_id="bg_map",
            label="BG map",
            path=expected_paths["bg_map"],
            what_it_is="JSON label map for IR bg/background labels.",
            how_to_create="Prepare only if this episode's IR uses bg labels.",
            used_by="GUI production tab / BG map input",
            required=False,
            required_phase="conditional",
        ),
        _handoff_input(
            input_id="skit_group_registry",
            label="skit_group registry",
            path=expected_paths["skit_group_registry"],
            what_it_is="JSON registry resolving skit_group intents to templates.",
            how_to_create=(
                "Use the pack-local copy when skit_group appears in the IR; assistant "
                "can prepare it from the repo template."
            ),
            used_by="GUI production tab / Skit Group Registry input",
            required=False,
            required_phase="conditional",
        ),
        _handoff_input(
            input_id="skit_group_template_source",
            label="skit_group template source",
            path=expected_paths["skit_group_template_source"],
            what_it_is="Repo-tracked YMM4 template source for skit_group placement.",
            how_to_create="Already repo-owned; select it in GUI when skit_group is enabled.",
            used_by="GUI production tab / Skit Group Template Source input",
            required=False,
            required_phase="conditional",
        ),
    ]
    missing_initial_inputs = [
        item["id"]
        for item in required_inputs
        if item["required_phase"] == "initial" and item["state"] == "missing"
    ]
    pending_generated = [
        item["id"] for item in required_inputs if item["state"] == "generated_later"
    ]
    phase, assistant_status = _episode_handoff_phase(
        expected_paths=expected_paths,
        missing_initial_inputs=missing_initial_inputs,
        pending_generated=pending_generated,
    )
    return {
        "success": True,
        "pack_version": EPISODE_RUN_PACK_VERSION,
        "episode_id": episode_id,
        "run_dir": str(run_dir),
        "pack_exists": run_dir.exists(),
        "phase": phase,
        "assistant_status": assistant_status,
        "missing_required": missing_initial_inputs,
        "missing_initial_inputs": missing_initial_inputs,
        "pending_generated": pending_generated,
        "required_inputs": required_inputs,
        "conditional_inputs": conditional_inputs,
        "operation_order": [
            f"Save the refined script to {expected_paths['source_script']}.",
            f"Save or GUI-paste the Production IR to {expected_paths['production_ir']}.",
            "Start GUI with start-gui.bat and select this folder as Episode Pack Root.",
            (
                f"Build CSV from {expected_paths['source_script']}; success output is "
                f"{expected_paths['csv']}."
            ),
            (
                f"Import {expected_paths['csv']} in YMM4, then Save As "
                f"{expected_paths['base_ymmp']}."
            ),
            "Run Validate IR, Dry Run, then Apply Production in the GUI.",
        ],
        "success_outputs": {
            "csv": expected_paths["csv"],
            "validate_result": expected_paths["validate_result"],
            "dry_run_result": expected_paths["dry_run_result"],
            "apply_result": expected_paths["apply_result"],
            "patched_ymmp": expected_paths["patched_ymmp"],
        },
        "ng_returns": {
            "validate_ng": expected_paths["validate_result"],
            "dry_run_ng": expected_paths["dry_run_result"],
            "apply_ng": expected_paths["apply_result"],
        },
        "do_not": [
            (
                "Do not collapse these entries into bare 'put/place this path' bullets; "
                "include what each file is and how it is created."
            ),
            (
                "Do not describe the base .ymmp as an initial placement unless it already "
                "exists; the normal route creates it after Build CSV and YMM4 CSV import."
            ),
            (
                "Do not ask for a new script when an existing completed script is available; "
                "copy/save the selected episode script to the pack path instead."
            ),
            "Do not hand-edit patched .ymmp outputs after Apply Production NG.",
        ],
        "assistant_next": (
            "After the user returns saved JSON/readback or panel text, classify the "
            "blocker and patch IR/map/GUI gaps as needed."
        ),
    }


def emit_episode_run_pack_text(result: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if fmt == "text":
        return render_episode_run_pack_text(result)
    raise ValueError(f"Unsupported episode run pack format: {fmt}")


def emit_episode_run_handoff_text(result: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if fmt == "text":
        return render_episode_run_handoff_text(result)
    raise ValueError(f"Unsupported episode run handoff format: {fmt}")


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


def render_episode_run_handoff_text(result: dict[str, Any]) -> str:
    lines = [
        f"Episode run handoff: {result.get('episode_id')}",
        f"Pack root: {result.get('run_dir')}",
        f"Phase: {result.get('phase')}",
        f"Assistant status: {result.get('assistant_status')}",
        "",
        "Required inputs and generated-later artifacts:",
    ]
    for item in result.get("required_inputs", []):
        lines.extend(_render_handoff_item(item))
    lines.extend(["", "Conditional inputs:"])
    for item in result.get("conditional_inputs", []):
        lines.extend(_render_handoff_item(item))
    lines.extend(["", "Operation order:"])
    for index, step in enumerate(result.get("operation_order", []), start=1):
        lines.append(f"{index}. {step}")
    lines.extend(["", "Success outputs:"])
    for key, path in result.get("success_outputs", {}).items():
        lines.append(f"- {key}: {path}")
    lines.extend(["", "NG returns:"])
    for key, path in result.get("ng_returns", {}).items():
        lines.append(f"- {key}: {path}")
    lines.extend(["", "Do not:"])
    for entry in result.get("do_not", []):
        lines.append(f"- {entry}")
    lines.extend(["", f"Assistant next: {result.get('assistant_next')}", ""])
    return "\n".join(lines)


def _validate_episode_id(episode_id: str) -> None:
    if not episode_id or not EPISODE_ID_PATTERN.fullmatch(episode_id):
        raise ValueError(
            "EPISODE_RUN_ID_INVALID: use only letters, numbers, '.', '_' or '-', "
            "and start with a letter or number"
        )
    if "/" in episode_id or "\\" in episode_id:
        raise ValueError("EPISODE_RUN_ID_INVALID: path separators are not allowed")


def _required_input_contracts() -> list[dict[str, str]]:
    return [
        {
            "id": "source_script",
            "path": "csv/<episode_id>.txt",
            "file_kind": "UTF-8 plain text source script",
            "created_by": "user / script refinement",
            "required_phase": "initial",
            "creation_route": (
                "Save the selected completed episode script before Build CSV. "
                "A new script is not required if a completed one already exists."
            ),
            "used_by": "Build CSV",
            "new_script_policy": (
                "既存完成台本があれば新規作成不要; save/copy the selected pilot script."
            ),
            "why_required": (
                "CSV rows, Production IR row-range, YMM4 base, and manifest must bind "
                "to the same episode script."
            ),
            "accepted_format": "UTF-8 .txt; recommended speaker lines like れいむ：... / まりさ：...",
            "same_episode_binding": "Do not use old samples or another episode's script.",
        },
        {
            "id": "production_ir",
            "path": "ir/<episode_id>_production_ir.json",
            "file_kind": "Production IR JSON",
            "created_by": "S-6 Production IR output or GUI paste-save",
            "required_phase": "initial",
            "creation_route": "Save valid JSON before Validate IR.",
            "used_by": "Validate IR / Dry Run / Apply Production",
            "why_required": "IR must target the same script/CSV/base .ymmp.",
            "accepted_format": "UTF-8 JSON matching the Production IR schema.",
            "same_episode_binding": "Do not use stale IR from another episode.",
        },
        {
            "id": "base_ymmp",
            "path": "ymmp/<episode_id>_base.ymmp",
            "file_kind": "YMM4 base project after CSV import",
            "created_by": "YMM4 Save As after Build CSV",
            "required_phase": "after_build_csv",
            "creation_route": "Build CSV, import the CSV in YMM4, then save this .ymmp.",
            "used_by": "Production .ymmp input",
            "why_required": "Apply Production patches the YMM4 project containing the CSV rows.",
            "accepted_format": ".ymmp saved by YMM4 after CSV import.",
            "same_episode_binding": "Save from this pack's generated CSV.",
        },
    ]


def _handoff_input(
    *,
    input_id: str,
    label: str,
    path: str,
    what_it_is: str,
    how_to_create: str,
    used_by: str,
    required: bool = True,
    required_phase: str = "initial",
    state_override: str | None = None,
    new_script_policy: str | None = None,
    why_required: str | None = None,
    accepted_format: str | None = None,
    same_episode_binding: str | None = None,
) -> dict[str, Any]:
    item = {
        "id": input_id,
        "label": label,
        "path": path,
        "state": state_override or ("exists" if Path(path).exists() else "missing"),
        "required": required,
        "required_phase": required_phase,
        "what_it_is": what_it_is,
        "how_to_create": how_to_create,
        "used_by": used_by,
    }
    if new_script_policy:
        item["new_script_policy"] = new_script_policy
    if why_required:
        item["why_required"] = why_required
    if accepted_format:
        item["accepted_format"] = accepted_format
    if same_episode_binding:
        item["same_episode_binding"] = same_episode_binding
    return item


def _render_handoff_item(item: dict[str, Any]) -> list[str]:
    lines = [
        f"- {item['label']}: {item['path']}",
        f"  state: {item['state']}",
        f"  phase: {item['required_phase']}",
        f"  what: {item['what_it_is']}",
        f"  create: {item['how_to_create']}",
        f"  used by: {item['used_by']}",
    ]
    if item.get("new_script_policy"):
        lines.append(f"  new script?: {item['new_script_policy']}")
    if item.get("why_required"):
        lines.append(f"  why: {item['why_required']}")
    if item.get("accepted_format"):
        lines.append(f"  format: {item['accepted_format']}")
    if item.get("same_episode_binding"):
        lines.append(f"  same episode: {item['same_episode_binding']}")
    return lines


def _episode_handoff_phase(
    *,
    expected_paths: dict[str, str],
    missing_initial_inputs: list[str],
    pending_generated: list[str],
) -> tuple[str, str]:
    if missing_initial_inputs:
        return "initial_inputs", "blocked_on_initial_user_inputs"
    if not Path(expected_paths["csv"]).exists():
        return "build_csv", "ready_for_build_csv"
    if "base_ymmp" in pending_generated:
        return "ymm4_base_save", "waiting_for_ymm4_base_generation"
    return "apply_production", "ready_for_validate_ir_dry_run_apply"


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

assistant status: blocked only on the user-owned pack inputs listed below; GUI writes review artifacts to fixed paths.
user action: create or select the required files at the exact paths, use the GUI buttons below, then do one YMM4 review only after Apply succeeds.
assistant next: if any step fails, return the saved JSON or panel text; assistant will inspect that artifact and keep `review/gaps.md` focused on the blocker.
assistant system aid: `episode-run-handoff --episode-id {episode_id}` prints the current exists/missing state plus what/create/used-by details for this pack.

## Initial input packet

Required before the GUI route can complete:

| File | Purpose | Created by / when |
|---|---|---|
| `csv/{episode_id}.txt` | completed dialogue script for this exact video; not a memo, IR, README, or old sample | save/copy the selected completed script here as UTF-8 `.txt`; a new script is not required if a completed one already exists |
| `ir/{episode_id}_production_ir.json` | Production IR for this same script; not a substitute for the script text | save the S-6 IR here, or save pasted IR through GUI after the script is fixed |
| `ymmp/{episode_id}_base.ymmp` | generated later: YMM4 base project after CSV import | after `csv/{episode_id}.csv` is built, import it in YMM4 and Save As this file |

Why the same script matters: CSV rows, Production IR row-range references,
the YMM4 base project, and the session manifest must all describe the same
episode. Using an old sample or another video's script can make JSON valid
while still patching the wrong rows.

Conditional files:

| File | Use only when |
|---|---|
| `maps/bg_map.json` | IR uses background labels / `bg` changes |
| `maps/skit_group_registry.json` | IR uses `skit_group` intents |
| `samples/templates/skit_group/delivery_v1_templates.ymmp` | `skit_group` placement is enabled; select this repo template source in GUI |
| `maps/face_map.json` or face map bundle | face / idle_face labels need an explicit character-scoped map |

1. Start GUI with `start-gui.bat`.
2. Open the `演出適用` tab and choose this folder as `Episode Pack Root`.
3. Confirm `csv/{episode_id}.txt` and `ir/{episode_id}_production_ir.json` exist in this pack.
4. Open the `CSV 変換` tab, select `csv/{episode_id}.txt`, then press `Build CSV`.
   - success output: `csv/{episode_id}.csv`
   - GUI also reflects that CSV in `CSV (row-range)`.
5. Import the CSV in YMM4, then save the base project as `ymmp/{episode_id}_base.ymmp`.
6. Return to `演出適用`, select `ymmp/{episode_id}_base.ymmp` and `ir/{episode_id}_production_ir.json`.
7. Select only maps that this episode actually needs:
   - `maps/bg_map.json`
   - `maps/skit_group_registry.json`
   - `samples/templates/skit_group/delivery_v1_templates.ymmp`
8. Press `Validate IR`.
   - success/failure JSON: `ir/{episode_id}_validate.json`
9. Press `Dry Run`.
   - result JSON: `ymmp/{episode_id}_dry_run.json`
10. Press `Apply Production`.
   - result JSON: `ymmp/{episode_id}_apply.json`
   - patched project: `ymmp/{episode_id}_patched.ymmp`
11. Open `ymmp/{episode_id}_patched.ymmp` in YMM4 once and fill `review/ymm4_acceptance.md`.
12. Record missing演出 and GUI-unexposed map needs in `review/gaps.md`.
13. Build the final `manifest/session_manifest.md` with `manifest/session_manifest.command.txt`.

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

from __future__ import annotations

import argparse
import shutil
import sys
from collections import defaultdict
from pathlib import Path


EXCLUDED_PARTS = {
    ".git",
    ".claude",
    ".mkdocs-docs",
    ".mkdocs-site",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site",
    "venv",
}

SPEC_KEYWORDS = (
    "ARCHITECTURE",
    "ATLAS",
    "BOUNDARY",
    "CHECKLIST",
    "CONTRACT",
    "GUIDE",
    "MATRIX",
    "PIPELINE",
    "PRESET",
    "SCHEMA",
    "SPEC",
    "STRATEGY",
    "WORKFLOW",
)

RUNTIME_FILES = {
    "docs/runtime-state.md",
    "docs/project-context.md",
    "docs/FEATURE_REGISTRY.md",
    "docs/USER_REQUEST_LEDGER.md",
    "docs/INTERACTION_NOTES.md",
    "docs/MIGRATION_LEDGER.md",
    "docs/OPERATOR_WORKFLOW.md",
}

OVERVIEW_ORDER = [
    "index.md",
    "docs/index.md",
    "docs/PROJECT_OVERVIEW.md",
    "docs/BRANCH_THREAD_SUPERVISION.md",
    "docs/BASEBALL_SUPERVISOR_REVIEW_PROMPT.md",
    "docs/PROGRESS_SCREENSHOT_INDEX.md",
    "docs/TURN_BASED_DEVELOPMENT_PLAN.md",
    "docs/GLOSSARY.md",
    "README.md",
    "AGENTS.md",
    "docs/REPO_LOCAL_RULES.md",
    "docs/runtime-state.md",
    "docs/NAV.md",
    "docs/FEATURE_REGISTRY.md",
]

CATEGORY_ORDER = [
    "Overview",
    "Specs",
    "Runtime State",
    "Development Notes",
    "Artifacts",
    "Misc",
]

ASSET_SUFFIXES = {
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".webp",
}

PROGRESS_ASSET_PREFIXES = (
    "samples/_probe/baseball/",
    "samples/_probe/g24/",
    "samples/_probe/pipeline_smoke/",
)

SUBGROUP_ORDER = {
    "Development Notes": [
        "AI Rules",
        "ADR",
        "Prompts",
        "Developer Reference",
        "Agent Adapters",
        "Other",
    ],
    "Artifacts": [
        "Verification Evidence",
        "Samples",
        "Sports News Lane",
        "Baseball Info Graphics",
        "Other",
    ],
}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDED_PARTS:
        return True
    return any(part.startswith("_tmp") for part in path.parts)


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def view_rel(rel: str) -> str:
    if rel == "README.md":
        return "_root/README.md"
    if rel.startswith(".agent/"):
        return "_hidden/agent/" + rel.removeprefix(".agent/")
    if rel.startswith(".claude/"):
        return "_hidden/claude/" + rel.removeprefix(".claude/")
    return rel


def first_heading(path: Path) -> str | None:
    try:
        for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:80]:
            line = raw_line.strip()
            if line.startswith("# "):
                text = line[2:].strip()
                return text or None
    except OSError:
        return None
    return None


def fallback_label(rel: str) -> str:
    path = Path(rel)
    if path.name.lower() == "readme.md":
        if len(path.parts) == 1:
            return "Project README"
        return f"{path.parent.as_posix()} README"
    return path.stem.replace("_", " ").replace("-", " ")


def label_for(path: Path, root: Path) -> str:
    rel = rel_posix(path, root)
    heading = first_heading(path)
    if heading and len(heading) <= 90:
        return heading.replace(":", " -")
    return fallback_label(rel)


def classify(rel: str) -> tuple[str, str | None]:
    if rel in OVERVIEW_ORDER:
        return "Overview", None
    if rel in RUNTIME_FILES:
        return "Runtime State", None
    if rel.startswith("docs/verification/"):
        return "Artifacts", "Verification Evidence"
    if rel.startswith("samples/"):
        return "Artifacts", "Samples"
    if rel.startswith("lanes/sports_news/"):
        return "Artifacts", "Sports News Lane"
    if rel.startswith("BaseballInfoGraphics/"):
        return "Artifacts", "Baseball Info Graphics"
    if rel.startswith("docs/ai/"):
        return "Development Notes", "AI Rules"
    if rel.startswith("docs/ADR/"):
        return "Development Notes", "ADR"
    if rel.startswith("docs/prompts/"):
        return "Development Notes", "Prompts"
    if rel.startswith("docs/dev/"):
        return "Development Notes", "Developer Reference"
    if rel.startswith(".agent/") or rel.startswith(".claude/"):
        return "Development Notes", "Agent Adapters"
    if rel.startswith("docs/AGENT_") or rel.startswith("docs/gui-"):
        return "Development Notes", "Agent Adapters"
    if rel.startswith("docs/"):
        name = Path(rel).name.upper()
        if any(keyword in name for keyword in SPEC_KEYWORDS):
            return "Specs", None
        return "Development Notes", "Other"
    return "Misc", None


def markdown_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*.md"):
        if not path.is_file() or is_excluded(path.relative_to(root)):
            continue
        files.append(path)
    return sorted(files, key=lambda p: rel_posix(p, root).lower())


def should_copy_progress_asset(rel: str) -> bool:
    path = Path(rel)
    if path.suffix.lower() not in ASSET_SUFFIXES:
        return False
    if any(rel.startswith(prefix) for prefix in PROGRESS_ASSET_PREFIXES):
        return True
    return rel.startswith("samples/") and "thumb" in path.name.lower()


def progress_asset_files(root: Path) -> list[Path]:
    files = []
    for suffix in ASSET_SUFFIXES:
        for path in root.rglob(f"*{suffix}"):
            if not path.is_file() or is_excluded(path.relative_to(root)):
                continue
            rel = rel_posix(path, root)
            if should_copy_progress_asset(rel):
                files.append(path)
    return sorted(set(files), key=lambda p: rel_posix(p, root).lower())


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def emit_nav(root: Path) -> str:
    by_category: dict[str, dict[str | None, list[Path]]] = defaultdict(lambda: defaultdict(list))
    for path in markdown_files(root):
        rel = rel_posix(path, root)
        category, subgroup = classify(rel)
        by_category[category][subgroup].append(path)

    lines = ["nav:"]
    for category in CATEGORY_ORDER:
        groups = by_category.get(category)
        if not groups:
            continue
        lines.append(f"  - {yaml_quote(category)}:")
        if category == "Overview":
            paths_by_rel = {rel_posix(path, root): path for path in groups.get(None, [])}
            ordered = [paths_by_rel.pop(rel) for rel in OVERVIEW_ORDER if rel in paths_by_rel]
            ordered.extend(sorted(paths_by_rel.values(), key=lambda p: rel_posix(p, root).lower()))
            emit_path_list(lines, ordered, root, 4, sort_paths=False)
            continue
        if None in groups:
            emit_path_list(lines, groups[None], root, 4)
        subgroup_names = SUBGROUP_ORDER.get(category, [])
        remaining = [name for name in groups if name is not None and name not in subgroup_names]
        for subgroup in subgroup_names + sorted(remaining):
            paths = groups.get(subgroup)
            if not paths:
                continue
            lines.append(f"    - {yaml_quote(str(subgroup))}:")
            emit_path_list(lines, paths, root, 6)
    return "\n".join(lines) + "\n"


def emit_path_list(
    lines: list[str], paths: list[Path], root: Path, indent: int, *, sort_paths: bool = True
) -> None:
    seen: set[str] = set()
    prefix = " " * indent
    ordered_paths = sorted(paths, key=lambda p: rel_posix(p, root).lower()) if sort_paths else paths
    for path in ordered_paths:
        rel = rel_posix(path, root)
        label = label_for(path, root)
        if label in seen:
            label = f"{label} ({rel})"
        seen.add(label)
        lines.append(f"{prefix}- {yaml_quote(label)}: {yaml_quote(view_rel(rel))}")


def emit_config(root: Path) -> str:
    return (
        "site_name: NLMYTGen Local Docs\n"
        "site_description: Local browser view for repository Markdown audit and temporary page translation.\n"
        "docs_dir: .mkdocs-docs\n"
        "site_dir: .mkdocs-site\n"
        "use_directory_urls: true\n"
        "theme:\n"
        "  name: material\n"
        "  language: ja\n"
        "  features:\n"
        "    - navigation.sections\n"
        "    - navigation.top\n"
        "    - navigation.tracking\n"
        "    - search.highlight\n"
        "    - search.suggest\n"
        "    - content.code.copy\n"
        "plugins:\n"
        "  - search\n"
        "markdown_extensions:\n"
        "  - admonition\n"
        "  - fenced_code\n"
        "  - tables\n"
        "  - toc:\n"
        "      permalink: true\n"
        "exclude_docs: |\n"
        "  .git/\n"
        "  .mkdocs-docs/\n"
        "  .mkdocs-site/\n"
        "  .mypy_cache/\n"
        "  .pytest_cache/\n"
        "  .venv/\n"
        "  __pycache__/\n"
        "  build/\n"
        "  dist/\n"
        "  gui/node_modules/\n"
        "  node_modules/\n"
        "  site/\n"
        "  venv/\n"
        "  _tmp/\n"
        "  **/__pycache__/\n"
        "  **/*.pyc\n"
        "  **/*.pyo\n"
        "  **/*.ymmp\n"
        "  **/*.csv\n"
        "  **/*.opml\n"
        "  **/*.opml.xml\n"
        "\n"
        + emit_nav(root)
    )


def prepare_docs_dir(root: Path, target: Path) -> None:
    target = target.resolve()
    if target == root or root not in target.parents:
        raise ValueError(f"prepare target must be inside the repository and not the root: {target}")

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    for source in markdown_files(root):
        rel = Path(view_rel(source.relative_to(root).as_posix()))
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for source in progress_asset_files(root):
        rel = Path(view_rel(source.relative_to(root).as_posix()))
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Generate a MkDocs navigation candidate from repository Markdown files."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument(
        "--prepare-docs-dir",
        type=Path,
        help="Optional ignored MkDocs docs_dir to refresh with exact Markdown copies.",
    )
    parser.add_argument(
        "--format",
        choices=("nav", "mkdocs"),
        default="nav",
        help="Print only the nav block or a complete mkdocs.yml candidate.",
    )
    parser.add_argument("--write", type=Path, help="Optional output path. Defaults to stdout.")
    parser.add_argument("--force", action="store_true", help="Overwrite --write output if it exists.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if args.prepare_docs_dir:
        prepare_docs_dir(root, root / args.prepare_docs_dir)

    text = emit_config(root) if args.format == "mkdocs" else emit_nav(root)

    if args.write:
        target = args.write
        if target.exists() and not args.force:
            parser.error(f"{target} already exists; pass --force to overwrite it")
        target.write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

"""Keep the generated local MkDocs source focused on Markdown and media."""

from pathlib import PurePosixPath

from mkdocs.structure.files import Files


EXCLUDED_PARTS = {
    ".agent",
    ".claude",
    ".codex",
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "_local",
    "_tmp",
    "build",
    "dist",
    "node_modules",
    "nlmytgen.egg-info",
    "venv",
}

ALLOWED_SUFFIXES = {
    ".gif",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".png",
    ".svg",
    ".webp",
}


def _is_allowed(src_uri: str) -> bool:
    path = PurePosixPath(src_uri)
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in ALLOWED_SUFFIXES


def on_files(files, config):
    return Files([file for file in files if _is_allowed(file.src_uri)])

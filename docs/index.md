# Local Document View Note

This file exists only as a local documentation-view entry. It does not replace,
translate, summarize, or weaken the existing canonical Markdown files.

Run the local site from the repository root:

```powershell
python -m pip install mkdocs-material
python tools\generate-doc-nav.py --format mkdocs --prepare-docs-dir .mkdocs-docs --write mkdocs.yml --force
python -m mkdocs serve
```

Then open <http://127.0.0.1:8000/> and use the left navigation tree. If port
8000 is already in use, run `python -m mkdocs serve --dev-addr
127.0.0.1:8006` and open <http://127.0.0.1:8006/> instead. For
Japanese-to-English review, use Chrome, Edge, or a DeepL browser extension page
translation on the rendered page. Do not create permanent translated copies in
the repository.

Useful first checks:

- [AGENTS.md](../AGENTS.md)
- [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md)
- [runtime-state.md](runtime-state.md)
- [NAV.md](NAV.md)
- [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md)

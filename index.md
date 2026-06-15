# NLMYTGen Local Document View

This page is a local browsing entry for the repository Markdown files. It is not
a replacement for the canonical documents, and it does not translate, summarize,
or reorganize their meaning.

Use this view to inspect the existing Markdown tree with a browser side
navigation pane, then use Chrome, Edge, or a DeepL browser extension as a
temporary page-translation aid.

```powershell
python -m pip install mkdocs-material
python tools\generate-doc-nav.py --format mkdocs --prepare-docs-dir .mkdocs-docs --write mkdocs.yml --force
python -m mkdocs serve
```

Open <http://127.0.0.1:8000/> after the server starts.
If port 8000 is already in use, choose another local port:

```powershell
python -m mkdocs serve --dev-addr 127.0.0.1:8006
```

Primary starting points:

- [Repository rules](docs/REPO_LOCAL_RULES.md)
- [Project overview](docs/PROJECT_OVERVIEW.md)
- [Baseball foundation rebaseline](docs/baseball/FOUNDATION_REBASELINE_2026-06-15.md)
- [Progress screenshot index](docs/PROGRESS_SCREENSHOT_INDEX.md)
- [Turn-based development plan](docs/TURN_BASED_DEVELOPMENT_PLAN.md)
- [Runtime state](docs/runtime-state.md)
- [Document map](docs/NAV.md)
- [Feature registry](docs/FEATURE_REGISTRY.md)
- [Local view note](docs/index.md)

The Markdown files themselves remain the source of truth. Browser translation is
only a temporary reading aid and should not be committed as translated files.

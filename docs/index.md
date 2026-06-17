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
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- [Baseball foundation rebaseline](baseball/FOUNDATION_REBASELINE_2026-06-15.md)
- [Baseball BN-05 manual preview gate handoff](../lanes/sports_news/docs/baseball_bn05_manual_preview_gate_handoff_2026-06-17.md)
- [BRANCH_THREAD_SUPERVISION.md](BRANCH_THREAD_SUPERVISION.md)
- [BASEBALL_SUPERVISOR_REVIEW_PROMPT.md](BASEBALL_SUPERVISOR_REVIEW_PROMPT.md)
- [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md)
- [TURN_BASED_DEVELOPMENT_PLAN.md](TURN_BASED_DEVELOPMENT_PLAN.md)
- [runtime-state.md](runtime-state.md)
- [NAV.md](NAV.md)
- [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md)

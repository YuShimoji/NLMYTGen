# NLMYTGen Local Document View

This page is a local-only MkDocs home for browsing repository Markdown in a
browser tree pane. It is not a canonical spec, translation, or replacement for
the existing Markdown sources.

Start from the [viewing guide](docs/index.md) or the
[Markdown inventory](docs/markdown-inventory.md). Serve the site locally and
open `http://127.0.0.1:8000/`, then use Chrome, Edge, or a DeepL browser
extension for temporary page translation while reviewing the original docs.

Quick PowerShell options:

```powershell
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format source
uvx --from mkdocs-material mkdocs serve --dev-addr 127.0.0.1:8000
```

or:

```powershell
python -m pip install mkdocs-material
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format source
mkdocs serve --dev-addr 127.0.0.1:8000
```

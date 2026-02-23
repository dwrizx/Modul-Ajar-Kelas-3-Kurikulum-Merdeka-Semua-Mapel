# Repository Guidelines

## Start Here (Read First)
When opening this file, agent must immediately review changelog context first:
- Read latest entries in `changelog/` (at least 3 most recent files when available).
- Follow `skill/SKILL.md` as source of truth for changelog workflow.
- Do not start implementation before pre-work log review is done.

Quick commands:

```bash
ls -1 changelog | sort | tail -n 10
```

```bash
sed -n '1,220p' skill/SKILL.md
```

## Project Structure
Core logic lives in `webdl/`:
- `crawler.py`: page traversal and internal link discovery.
- `extractor.py`: HTML parsing and link classification.
- `downloader.py`: filename resolution and file download flow (including Google Drive confirmation handling).
- `cli.py`: CLI entrypoints for `analyze`, `download`, and `download-classes`.
- `models.py`: shared dataclass models.

Tests live in `tests/`:
- `test_extractor.py`
- `test_downloader.py`
- `test_cli.py`
- `conftest.py` for shared fixtures/utilities.

Project metadata:
- `pyproject.toml`
- `uv.lock`

Common generated artifacts:
- `analysis-kelas*.json` (analysis outputs)
- `downloads/` (download outputs)

## Development Commands
Use `uv` for environment + execution.

```bash
uv sync
uv run pytest -q
uv run python -m webdl.cli analyze "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --output analysis-kelas3.json
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --out downloads
uv run python -m webdl.cli download-classes --classes "1-6" --max-pages 30 --out downloads
```

If default cache is not writable, prefix with:

```bash
UV_CACHE_DIR=.uv-cache
```

## Coding Style
- Python 3.14+, 4-space indentation, UTF-8.
- Keep explicit type hints and explicit return types where already used.
- Naming:
  - `snake_case` for variables/functions.
  - `PascalCase` for dataclasses/classes.
- Keep modules cohesive and focused (crawl/extract/download/cli separation).
- Prefer small, testable units and avoid hidden side effects.

## Testing Rules
- Framework: `pytest`.
- File naming: `tests/test_*.py`.
- Test naming: `test_<behavior>`.
- Update/add tests for every behavior change in:
  - extraction/classification
  - crawl traversal logic
  - download handling and filename resolution
  - CLI behavior/flags/output.
- Run before PR:

```bash
uv run pytest -q
```

## Output & Folder Conventions
- Keep downloaded data under `downloads/`.
- Prefer predictable structure for grouped runs, for example:
  - `downloads/kelas-6/genjil/<subject>/`
  - `downloads/kelas-6/genap/<subject>/`
  - `downloads/kelas-6/mendalam/<subject>/`
- Keep run artifacts lightweight and reproducible:
  - optional per-run logs: `_download.log`
  - optional summary file: `_summary.tsv`

## Commit & PR Guidelines
Commit style (preferred):
- `feat: ...`
- `fix: ...`
- `test: ...`
- `docs: ...`

Examples:
- `feat: add Google Drive confirmation token fallback`
- `fix: handle empty href in extractor`
- `test: cover direct file detection edge case`

PR description should include:
- what changed
- why it changed
- test evidence (commands + result)
- sample CLI output when behavior changes
- issue/context link (if available)

## Mandatory Changelog Policy
This repository follows the `maintainable_feature_change` workflow in `skill/SKILL.md`.

For every feature/behavior/API/CLI/config/UI/performance change that impacts users or developers, agent **must**:
- Do pre-work review before coding:
  - read recent files in `changelog/`
  - check recent `git log` for touched area
  - confirm current behavior contract from docs/code
- Create or update one changelog file in `changelog/` using pattern:
  - `changelog/YYYY-MM-DD-<short-topic>.md`
- Ensure changelog includes at minimum:
  - what changed
  - why it changed
  - impact/risk
  - testing evidence (automated or manual steps)
- Update related docs (README/docs/examples) when behavior or usage changes.

Completion gate:
- Work is **not complete** until changelog entry is written for qualifying changes.
- If change is non-functional (pure refactor/chore/no behavior impact), agent must explicitly state reason when skipping changelog.

Recommended files:
- Changelog guide: `changelog/README.md`
- Changelog template: `changelog/_template.md`

## Agent Working Notes
- Do not commit generated downloads unless explicitly requested.
- Avoid unrelated refactors in the same change.
- For network-dependent commands, report failures clearly (DNS, timeout, rate limit, permission).
- If a URL list contains missing links, document assumptions used (for example inferred URL patterns).

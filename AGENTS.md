# Repository Guidelines

## Project Structure & Module Organization

This is a Python YouTube downloader core built around `yt-dlp`. Source code lives in `src/`:

- `src/main.py` contains the runnable example flow and segment callback.
- `src/core/` contains downloader logic, playlist dispatching, options, and segment writing.
- `src/tools/` contains shared helpers such as URL parsing, logging, and run ID utilities.
- `src/config.py` centralizes runtime configuration.
- `src/benchmark/` contains benchmarking helpers.
- `tests/` is configured in `pyproject.toml` but not currently present; add new tests there.

Keep runtime artifacts, such as temporary JSONL segment files, under ignored directories such as `temp/`.

## Build, Test, and Development Commands

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run the example flow:

```bash
python src/main.py
```

Run tests:

```bash
pytest
```

Run quality checks:

```bash
black src tests
flake8 src tests
mypy src
```

Build and run Docker:

```bash
docker build -t pydc .
docker run -d --name pydc-container -p 8000:8000 pydc
```

## Coding Style & Naming Conventions

Target Python `3.14` syntax and keep compatibility with `requires-python ==3.14.5`. Use Black formatting with an 88-character line length. Prefer explicit type hints on public functions and shared data structures.

Use `snake_case` for modules, functions, variables, and file names. Use `PascalCase` for dataclasses and classes. Keep downloader-specific logic in `src/core/`; place generic helpers in `src/tools/`.

## Testing Guidelines

Pytest is the configured test framework. Add tests under `tests/` with names matching `test_*.py` or `*_test.py`, for example `tests/core/test_yt.py`.

For code that calls YouTube or `yt-dlp`, prefer mocks or small fixtures over live network calls. Cover playlist ranges, errors, and callback behavior before changing dispatcher or extraction code.

## Commit & Pull Request Guidelines

Recent commit history uses short, direct messages such as `minor change to pyproject toml` and `use python api for get_playlist_count`. Keep commits focused and describe the behavioral change.

Pull requests should include a concise summary, test results, and relevant issue links. For downloader behavior changes, note the URL type tested, such as single video or playlist. Do not commit downloaded media or generated temp files.

## Security & Configuration Tips

Do not commit credentials, cookies, downloaded media, or large generated outputs. Treat external URLs as untrusted input and avoid logging private query parameters or local paths.

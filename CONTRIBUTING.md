# Contributing

Thanks for the interest.

## Setup

    git clone https://github.com/sswivell/mock-relay.git
    cd mock-relay
    python -m venv .venv
    .venv\Scripts\activate
    pip install -e .
    pip install pytest ruff

## Run tests

    pytest -q

## Lint

    ruff check .

## Style

- Python 3.10+
- No comments in code
- Functions and classes use numbered names (_01, _02, ...)
- Docstrings at the top of each module

## Adding a feature

1. Open an issue first if the change is non-trivial.
2. Add tests under tests/.
3. Keep the CLI surface documented in docs/cli.md.
4. Update README.md if user-facing behavior changes.

## Commit messages

Prefix with one of: feat:, fix:, docs:, chore:, refactor:, test:.

## Pull requests

- One logical change per PR
- CI must be green
- Include a short description and, if UI-facing, a screenshot

# Contributing

Thanks for the interest.

## Find something to work on

Start with the issues labelled
[`good first issue`](https://github.com/sswivell/mock-relay/labels/good%20first%20issue).
Each one is scoped so that it can be finished in a single sitting, and
several are commented with the exact change we have in mind. If you pick one
up, comment on the issue so nobody duplicates the work.

Nothing appeals? [ROADMAP.md](ROADMAP.md) lists the themes we are working on.

## Setup

    git clone https://github.com/sswivell/mock-relay.git
    cd mock-relay
    python -m venv .venv
    .venv\Scripts\activate
    pip install -e .
    pip install pytest ruff

## Run tests

    pytest -q

To run one test:

    pytest tests/test_match_strategies.py -k priority

## Lint

    ruff check .

## Style

- Python 3.10+
- No comments in code
- Functions and classes use numbered names (_01, _02, ...)
- Docstrings at the top of each module

## Code layout

Modules and functions are numbered rather than named, so this table is the
map. `_09.py` is the matcher and is the module you will edit most often.

| Module | Responsibility |
|---|---|
| `_01.py` | Default settings and theme constants |
| `_02.py` | Brand key encode/decode |
| `_03.py` | Colour palettes and terminal capability detection |
| `_04.py` | Terminal rendering: header, section, table, spinner, box |
| `_05.py` | `Config`: loading, validation, scoped setting resolution |
| `_06.py` | Data classes: `MatchSpec`, `Request`, `Response`, `Fixture` |
| `_07.py` | Redaction of headers and secret-shaped strings |
| `_08.py` | JSON body normalisation |
| `_09.py` | The matcher: strategies, ranking, match diagnostics |
| `_10.py` | `Store`: fixture identity, paths, and persistence |
| `_11.py` | `Metrics`: request counters and recent-request ring |
| `_12.py` | Outbound HTTP to the upstream, and response decoding |
| `_13.py` | Proxy request handler and server |
| `_14.py` | Admin API server |
| `_15.py` | CLI entry point (`argparse`) |
| `_16.py` | Terminal UI facade, re-exporting from `_01` and `_04` |
| `_17.py` | Fixture counts per upstream |

Numbering is load-bearing across modules, because modules import each other
under aliases:

    from ._09 import _22 as _11

That means `_11` inside one module is not `_11` in another. When you add a
symbol, give it the next free number in its own module and check what the
existing numbers are used for first.

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
- Reference the issue it closes, for example `Closes #12`


# Architecture

## Request flow

    client -> proxy -> handler -> mode dispatch -> upstream or fixture
                                |
                                +-> metrics
                                +-> recorder (if mode=record/hybrid)

## Modules

| File | Role |
|---|---|
| _01.py | settings store |
| _02.py | brand blob encode/decode |
| _03.py | themes and color |
| _04.py | swivel ui helpers |
| _05.py | config loader + route overrides |
| _06.py | dataclasses: MatchSpec, Fixture, Request, Response |
| _07.py | header/body redaction |
| _08.py | JSON-path normalization |
| _09.py | fixture matching |
| _10.py | on-disk fixture store |
| _11.py | metrics counters |
| _12.py | upstream HTTP client |
| _13.py | proxy HTTP server |
| _14.py | admin HTTP server |
| _15.py | CLI |
| _16.py | public exports |
| _17.py | stats and clean helpers |

## Storage

Fixtures are plain JSON files under `fixtures/<upstream>/`. Atomic writes via
temp file + rename. No database.

## Concurrency

The proxy uses ThreadingHTTPServer. Each request is handled on its own
thread. The fixture store is read on every request so edits on disk are
picked up live.

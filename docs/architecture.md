# Architecture

## Request flow

    client -> proxy -> handler -> mode dispatch -> upstream or fixture

## Modules

| File | Role |
|---|---|
| _01.py | settings store |
| _02.py | brand blob |
| _03.py | themes |
| _04.py | swivel ui |
| _05.py | config loader |
| _06.py | dataclasses |
| _07.py | redaction |
| _08.py | normalization |
| _09.py | smart matcher |
| _10.py | store |
| _11.py | metrics |
| _12.py | upstream client |
| _13.py | proxy server |
| _14.py | admin server |
| _15.py | CLI |
| _16.py | exports |
| _17.py | stats helpers |

## Matching

The matcher resolves options, then scores candidates rather than filtering
them, so the most specific fixture wins.

    config -> _05._12  -> MatchOptions
    MatchSpec          -> _09._23  -> MatchOptions (fixture overrides base)
    fixtures + request -> _09._22  -> ranked results

`_22` is the entry point used by replay, `/api/match`, and `mockrelay match`.
It delegates to `_21` per fixture, which returns a per-check breakdown for
diagnostics, then sorts by matched, score, and ID.

See [Smart matching](matching.md).

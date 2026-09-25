# MockRelay

<p align="center">
  <img src="https://files.catbox.moe/v9x6sc.png" alt="MockRelay preview">
</p>

<p align="center">
  <a href="https://github.com/sswivell/mock-relay/actions"><img src="https://img.shields.io/github/actions/workflow/status/sswivell/mock-relay/ci.yml?branch=main&label=ci" alt="CI"></a>
  <a href="https://github.com/sswivell/mock-relay/stargazers"><img src="https://img.shields.io/github/stars/sswivell/mock-relay" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e" alt="License"></a>
</p>

<p align="center">
  <b>Record real HTTP traffic. Replay it forever.</b>
</p>

## Install

```bash
git clone https://github.com/sswivell/mock-relay.git
cd mock-relay
pip install -e .
```

## Quickstart

```bash
mockrelay init
mockrelay serve
```

Point your app at the proxy:

| Real | Local |
|---|---|
| `https://api.stripe.com` | `http://localhost:8080/stripe` |
| `https://api.github.com` | `http://localhost:8080/gh` |

## Modes

| Mode | Behavior |
|---|---|
| `record` | Forward, save each request/response as a fixture |
| `replay` | Serve from fixtures only |
| `passthrough` | Forward only, no recording |
| `hybrid` | Fixtures if matched, else live + record |

## Smart matching

Fixtures are ranked, not just filtered, so the most specific one wins.

| Strategy | Pattern | Matches |
|---|---|---|
| exact | `/users/7` | that path only |
| wildcard | `wildcard:/users/*` | one segment |
| regex | `re:^/orders/\d+$` | pattern match |
| fuzzy | `fuzzy:/custommer/prof` | close enough, above the threshold |

`match_mode: auto` infers the strategy from the prefix, and never
fuzzy-matches a bare path, so a typo cannot silently hit the wrong fixture.
Bodies match on the keys you care about, with operators and JSONPath-style
keys:

```json
"body_contains": {
  "status": "paid",
  "total": { "$gt": 100 },
  "$.items[*].sku": "wildcard:A*"
}
```

Candidates are ranked, not just filtered. `match_priority` reorders the
criteria, so you can put a query match ahead of the path when that is what
identifies the request:

```yaml
match_priority: [query, path, body, literal]   # default is [path, body, query, literal]
```

A fixture can also set an integer `priority` to jump the queue entirely:

```json
"match": { "method": "GET", "path": "wildcard:/files/**", "priority": 10 }
```

Check a request against the stored fixtures without starting a server:

```bash
mockrelay match /users/7
mockrelay match /orders -m POST -b '{"total":500}'
```

Full reference: [docs/matching.md](docs/matching.md).

## CLI

```bash
mockrelay serve
mockrelay serve --mode replay
mockrelay record
mockrelay replay --latency 150
mockrelay list
mockrelay match /users/7
mockrelay stats
```

## Docs

https://sswivell.github.io/mock-relay/

## Contributing

New here? Start with the issues labelled
[good first issue](https://github.com/sswivell/mock-relay/labels/good%20first%20issue).

- [CONTRIBUTING.md](CONTRIBUTING.md) - setup, tests, and a map of the codebase
- [ROADMAP.md](ROADMAP.md) - what is being worked on
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

MIT - see [LICENSE](LICENSE).

# MockRelay

<p align="center">
  <img src="https://files.catbox.moe/v9x6sc.png" alt="MockRelay preview">
</p>

<p align="center">
  <a href="https://github.com/sswivell/mock-relay/actions"><img src="https://img.shields.io/github/actions/workflow/status/sswivell/mock-relay/ci.yml?branch=main&label=ci" alt="CI"></a>
  <a href="https://pypi.org/project/mockrelay/"><img src="https://img.shields.io/pypi/v/mockrelay" alt="PyPI"></a>
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

## CLI

```bash
mockrelay serve
mockrelay serve --mode replay
mockrelay record
mockrelay replay --latency 150
mockrelay list
mockrelay stats
```

## Docs

https://sswivell.github.io/mock-relay/

## License

MIT - see [LICENSE](LICENSE).

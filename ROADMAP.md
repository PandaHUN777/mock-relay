# Roadmap

MockRelay is pre-1.0. `0.x` means the shape of things may still change, so
tell us early if something does not fit your use case.

Where work actually lives:

| Label | Meaning |
|---|---|
| [`good first issue`](https://github.com/sswivell/mock-relay/labels/good%20first%20issue) | Small and self-contained. A good first PR. |
| [`help wanted`](https://github.com/sswivell/mock-relay/labels/help%20wanted) | Real work, but larger or needs design input first. |
| [`bug`](https://github.com/sswivell/mock-relay/labels/bug) | Does not behave as documented. |
| [`enhancement`](https://github.com/sswivell/mock-relay/labels/enhancement) | New capability. |
| [`documentation`](https://github.com/sswivell/mock-relay/labels/documentation) | Docs and examples. |
| [`tests`](https://github.com/sswivell/mock-relay/labels/tests) | Coverage. |
| [`ci`](https://github.com/sswivell/mock-relay/labels/ci) | Workflows and packaging. |

The full label set is in [`.github/labels.yml`](.github/labels.yml).

## Themes we are working on

**Diagnostics.** Matching is ranked, so the interesting question is always
"why did that fixture win?". `mockrelay match` and `GET /api/match` answer
this, and the remaining work is making the output easier to read, and
covering more match fields in it.

**Packaging and reach.** MockRelay depends only on PyYAML and targets
Python 3.10+, but it is not on PyPI yet. Publishing, and keeping a
`Dockerfile` current, are tracked under `ci`.

**Docs and examples.** The [docs](docs/) cover the feature set, and
[examples](examples/) has runnable configurations. Both would benefit from
more of them, especially for the recording and hybrid paths.

## Themes we are not pursuing

- A hosted service or dashboard. MockRelay is a local tool.
- A plugin system. The matching engine is deliberately small and explicit.

## Suggesting something

Open a feature request, and say in the issue if you would like to implement
it. See [CONTRIBUTING.md](CONTRIBUTING.md).

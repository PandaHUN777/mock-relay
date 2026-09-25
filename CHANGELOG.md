# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added

- Smart matching: exact, wildcard, regex, and fuzzy path strategies with syntax-driven `auto` mode
- Strategy prefixes: `exact:`/`==`, `wildcard:`/`glob:`, `re:`/`regex:`/`~/`, `fuzzy:`/`~=`
- JSON-aware `body_contains` with `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$exists`, `$regex`, `$contains` operators
- JSONPath-style body keys (`$.items[*].id`, recursive `..id`), wildcard keys, and wildcard values
- Smart query-subset matching so a fixture may constrain only the query keys it cares about
- Match diagnostics on every replay response: `X-MockRelay-Match`, `X-MockRelay-Fixture`, `X-MockRelay-Score`
- Replay misses now report the active `match_mode` and the nearest fixture IDs
- `GET /api/match` admin endpoint for previewing how a request would match
- `mockrelay match [path]` CLI command with `--method`, `--query`, `--body`, and `--upstream`
- Config keys `match_mode`, `fuzzy_threshold`, `ignore_case`, `fuzzy_enabled`, and `smart_record_paths`, settable globally, per upstream, and per route
- `match_mode`, `fuzzy_threshold`, and `ignore_case` fields on fixtures and `MatchSpec`, with backward-compatible loading of older fixtures

### Changed

- Fixture selection now ranks candidates by match specificity (exact > wildcard > regex > fuzzy) and then by constraint count, instead of first-match-wins

### Fixed

- The query string is no longer treated as part of the request path, so recorded and replayed paths are clean and glob patterns behave
- A bare `?` in a path is no longer read as a single-character wildcard, which could make unrelated paths match; use `wildcard:` for that
- CLI output no longer crashes on Windows consoles that cannot encode the status glyphs

## [0.2.0] - 2026-09-23

### Added

- Record, replay, passthrough, and hybrid modes
- Per-upstream and per-route overrides
- On-disk JSON fixture store
- Header and body redaction
- JSON-path normalization
- Sequential fixture replay
- Prometheus metrics endpoint
- Admin HTTP API
- CLI: serve, record, replay, list, stats, clean, init, config
- Health and readiness endpoints
- Per-request mode override via X-MockRelay-Mode

# Changelog

All notable changes to this project are documented here.

The format is based on Keep a Changelog and this project adheres to Semantic
Versioning.

## [Unreleased]

## [0.2.0] - 2026-09-23

### Added

- Record, replay, passthrough, and hybrid modes
- Per-upstream and per-route overrides for mode, latency, error injection
- On-disk JSON fixture store with atomic writes
- Header and body redaction with configurable rules
- JSON-path normalization for volatile fields
- Sequential fixture replay
- Prometheus metrics endpoint
- Admin HTTP API for state, fixtures, mode, and latency
- CLI commands: serve, record, replay, list, stats, clean, init, config
- Health and readiness endpoints
- Per-request mode override via X-MockRelay-Mode header

[Unreleased]: https://github.com/sswivell/mock-relay/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/sswivell/mock-relay/releases/tag/v0.2.0

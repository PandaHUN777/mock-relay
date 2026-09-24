# Security policy

## Reporting

Report security issues privately by opening a draft advisory at
https://github.com/sswivell/mock-relay/security/advisories/new
or emailing the maintainer listed in the repo.

Do not open a public issue for anything exploitable.

## Scope

MockRelay is a development tool. It is not designed to be exposed to the
public internet. Run it on a loopback address or a trusted dev network.

In scope:

- Secrets leaking from fixtures despite redaction rules
- Path traversal in the fixture store
- Malformed YAML or fixture files causing code execution
- Admin API reachable beyond the configured bind address

Out of scope:

- Anyone with shell access to the host running MockRelay
- Upstream misconfiguration
- Fixtures committed with secrets from before redaction was enabled

## Redaction caveats

Redaction covers headers listed under redact_headers and body patterns for
Bearer, sk_live_*, sk_test_*, ghp_*. Other secrets may slip through. Review
fixtures before committing them to a public repo.

## Supported versions

Only the latest release is supported.

# Getting started

## Install

    git clone https://github.com/sswivell/mock-relay.git
    cd mock-relay
    pip install -e .

Requires Python 3.10+ and pyyaml.

## First run

    mockrelay init

This writes a starter mockrelay.yaml. It ships with three example upstreams
(stripe, gh, local) that you can keep, edit, or delete.

Open mockrelay.yaml and confirm the upstreams block. Each key becomes a URL
prefix on the proxy:

    upstreams:
      gh:
        base_url: "https://api.github.com"
        mode: record

The key gh means http://localhost:8080/gh/... forwards to
https://api.github.com/...

Then start the proxy:

    mockrelay serve

You will see the routing table, fixture counts, and the admin UI URL.

Open http://localhost:8081 for the admin UI.

## First record

Point any client at the proxy:

    curl http://localhost:8080/gh/users/octocat

You now have a fixture under `fixtures/gh/`.

## First replay

Stop the server (Ctrl-C), then:

    mockrelay serve --mode replay --latency 150

Same curl. Served from the fixture. No internet.

## Local demo (no internet)

Terminal A:

    python examples/demo_upstream.py

Terminal B:

    mockrelay serve --config examples/mockrelay.demo.yaml

Terminal C:

    curl http://localhost:8080/local/v1/users

Then replay:

    mockrelay serve --mode replay --latency 150 --config examples/mockrelay.demo.yaml

## Next

- `docs/modes.md` for record/replay/passthrough/hybrid
- `docs/fixtures.md` for the fixture format
- `docs/recipes.md` for real workflows


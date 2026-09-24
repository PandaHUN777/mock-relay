# Getting started

## Install

    git clone https://github.com/sswivell/mock-relay.git
    cd mock-relay
    pip install -e .

Requires Python 3.10+ and pyyaml.

## First run

    mockrelay init
    mockrelay serve

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

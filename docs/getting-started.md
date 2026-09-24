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

    curl http://localhost:8080/gh/users/octocat

You now have a fixture under fixtures/gh/.

## First replay

    mockrelay serve --mode replay --latency 150

Same curl. Served from the fixture. No internet.

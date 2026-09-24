# CLI reference

## serve

    mockrelay serve
    mockrelay serve --mode replay
    mockrelay serve --latency 200
    mockrelay serve --config path/to/mockrelay.yaml
    mockrelay serve --strict

## record

    mockrelay record
    mockrelay record --latency 0
    mockrelay record --config path/to/mockrelay.yaml

## replay

    mockrelay replay
    mockrelay replay --latency 150
    mockrelay replay --config path/to/mockrelay.yaml

## list

Lists recorded fixtures, one per row. Columns: upstream, method, path,
status, id.

    mockrelay list
    mockrelay list --upstream gh
    mockrelay list --config path/to/mockrelay.yaml

Example output:

      upstream  method  path                  status  id
      ------------------------------------------------------------
      gh        GET     /users/octocat        200     gh-get-9ab7c12d3e4f
      gh        GET     /repos/cli/cli        200     gh-get-4f2c81e0a1b2
      stripe    POST    /v1/charges           200     stripe-post-7d8e9f0a1c2d
      local     GET     /v1/users             200     local-get-3a4b5c6d7e8f

Flags:

| Flag | Effect |
|---|---|
| --upstream NAME | only show fixtures for one upstream |
| --config PATH | use a different mockrelay.yaml |

If no fixtures match, prints a warning and exits. If the fixtures
directory does not exist, prints an empty table with a warning.

## stats

    mockrelay stats
    mockrelay stats --config path/to/mockrelay.yaml

## clean

    mockrelay clean --older-than 30
    mockrelay clean --older-than 30 --yes
    mockrelay clean --config path/to/mockrelay.yaml --older-than 7 --yes

## init

    mockrelay init
    mockrelay init path/to/mockrelay.yaml

## config

    mockrelay config

Prints effective settings and the decoded brand string.


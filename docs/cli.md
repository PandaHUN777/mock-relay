# CLI reference

## serve

    mockrelay serve
    mockrelay serve --mode replay
    mockrelay serve --latency 200

## record

    mockrelay record

## replay

    mockrelay replay --latency 150

## list

    mockrelay list
    mockrelay list --upstream gh

## stats

    mockrelay stats

## clean

    mockrelay clean --older-than 30 --yes

## init

    mockrelay init

## config

    mockrelay config

## match

Preview how a request would be matched against the stored fixtures, without
starting a server. Every candidate is listed with a per-check breakdown of
method, path, query, and body.

    mockrelay match /v1/users
    mockrelay match /orders -m POST -b '{"total":500}'
    mockrelay match /users -q page=2 -q sort=asc
    mockrelay match /users -u gh

| Flag | Default | Purpose |
|---|---|---|
| `--config` | `mockrelay.yaml` | config file to read |
| `-m`, `--method` | `GET` | request method |
| `-u`, `--upstream` | all | limit to one upstream |
| `-q`, `--query` | none | repeatable `key=value` |
| `-b`, `--body` | none | JSON body, or a literal string |

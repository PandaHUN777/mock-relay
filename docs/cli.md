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

    mockrelay list
    mockrelay list --upstream gh
    mockrelay list --config path/to/mockrelay.yaml

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

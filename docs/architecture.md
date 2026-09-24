# Architecture

## Request flow

    client -> proxy -> handler -> mode dispatch -> upstream or fixture

## Modules

| File | Role |
|---|---|
| _01.py | settings store |
| _02.py | brand blob |
| _03.py | themes |
| _04.py | swivel ui |
| _05.py | config loader |
| _06.py | dataclasses |
| _07.py | redaction |
| _08.py | normalization |
| _09.py | matcher |
| _10.py | store |
| _11.py | metrics |
| _12.py | upstream client |
| _13.py | proxy server |
| _14.py | admin server |
| _15.py | CLI |
| _16.py | exports |
| _17.py | stats helpers |

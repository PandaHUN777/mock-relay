---
name: Bug report
about: Something is broken
title: ""
labels: bug
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the report. `mockrelay match <path>` shows exactly which
        check failed, so please paste its output if the request matches a
        fixture.

  - type: textarea
    id: happened
    attributes:
      label: What happened
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: What you expected
    validations:
      required: true

  - type: textarea
    id: reproduce
    attributes:
      label: Steps to reproduce
      value: |
        1.
        2.
        3.
      render: text
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: MockRelay version
      description: Output of `mockrelay --version`
    validations:
      required: true

  - type: input
    id: python
    attributes:
      label: Python version
      placeholder: 3.11.4
    validations:
      required: true

  - type: input
    id: os
    attributes:
      label: OS
      placeholder: Windows 11
    validations:
      required: false

  - type: textarea
    id: config
    attributes:
      label: Config
      description: The relevant part of mockrelay.yaml
      render: yaml

  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: Terminal output, including any `mockrelay match` table
      render: shell

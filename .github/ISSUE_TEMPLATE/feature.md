---
name: Feature request
about: Suggest an idea
title: ""
labels: enhancement
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the idea. Open a discussion or an issue if you would like
        to work on it, and say so below.

  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What are you trying to do that MockRelay makes hard?
      placeholder: I want to ...
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: What should change, and roughly how?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Workarounds you have used, and why they do not fit.

  - type: dropdown
    id: area
    attributes:
      label: Area
      multiple: true
      options:
        - Matching
        - Recording
        - Replay
        - Admin API
        - CLI
        - Documentation
        - CI / packaging
    validations:
      required: false

  - type: checkboxes
    id: willing
    attributes:
      label: Would you like to work on this?
      options:
        - label: I would like to implement this
        - label: I am interested, but would need guidance

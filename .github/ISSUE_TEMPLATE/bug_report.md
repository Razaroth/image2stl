name: Bug Report
description: Report a bug to help us improve
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill out the form below to help us fix it.
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the bug
      placeholder: What happened?
    validations:
      required: true
  
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the bug
      placeholder: |
        1. Use GUI/CLI with...
        2. Set parameters...
        3. Click/Run...
    validations:
      required: true
  
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should have happened?
      placeholder: The model should be created...
    validations:
      required: true
  
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened?
      placeholder: Instead, I got an error...
    validations:
      required: true
  
  - type: input
    id: environment
    attributes:
      label: Environment
      description: Python version, OS, etc.
      placeholder: "Python 3.10, Windows 11"
    validations:
      required: true
  
  - type: textarea
    id: error
    attributes:
      label: Error Message or Screenshot
      description: Full error message or screenshot
      placeholder: Paste error or attach screenshot
  
  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I've checked existing issues
          required: true
        - label: I've tried updating dependencies
          required: false
        - label: I'm using the latest version
          required: true

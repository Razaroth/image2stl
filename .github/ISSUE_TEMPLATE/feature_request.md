name: Feature Request
description: Suggest a new feature
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Great! Thanks for suggesting a feature. Let's discuss it!
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the feature
      placeholder: I would like to...
    validations:
      required: true
  
  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why is this feature needed?
      placeholder: This would help because...
    validations:
      required: true
  
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How do you envision this working?
      placeholder: I think it could work like...
  
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Other approaches you've considered
      placeholder: Other options include...
  
  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I've checked existing feature requests
          required: true
        - label: This is for GUI or CLI or both?
          required: false
        - label: I'm willing to help implement this
          required: false

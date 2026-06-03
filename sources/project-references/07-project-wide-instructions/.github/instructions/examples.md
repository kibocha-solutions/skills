---
title: Examples Instructions
description: Instructions for working with documentation examples
applies_to:
  - "02-examples/**/*"
---

# Working with Documentation Examples

These are **working examples** demonstrating correct implementation of documentation canons.

## When Creating Examples

### Purpose

Examples illustrate **how** to apply a canon, not just **what** the canon says.

### Requirements

1. **Complete:** Show entire file structure, not snippets
2. **Realistic:** Use believable project data (Tax Management System)
3. **Correct:** Follow the canon exactly
4. **Minimal:** Smallest example that demonstrates the pattern
5. **Documented:** Include README explaining what it demonstrates

### Structure

```
02-examples/{type}-example/
├── README.md              # What this example demonstrates
├── {main-files}           # Actual documentation files
└── {supporting-files}     # Diagrams, configs, etc.
```

### Writing Style

Follow canon rules:
- NO emojis
- NO emdashes
- Active voice
- Specific, realistic content

## Example README Format

```markdown
# {Type} Documentation Example

## Purpose

This example demonstrates [specific canon] for [use case].

## What's Included

- File A: Purpose
- File B: Purpose
- Directory C: Purpose

## How to Use

1. Review the canon: [link to canon]
2. See implementation in [file]
3. Note [specific patterns]

## Compliance

Follows:
- [Canon name]
- Core canon writing rules
- Access level: [Level X]
```

## Validation

Test examples match their canons:
1. Run validation scripts
2. Build Sphinx docs (if reST)
3. Validate API specs (if OpenAPI/GraphQL/Proto)
4. Check no emojis/emdashes

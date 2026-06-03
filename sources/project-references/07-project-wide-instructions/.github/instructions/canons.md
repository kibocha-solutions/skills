---
title: Documentation Canons Instructions
description: Instructions for working with documentation type canons
applies_to:
  - "01-documentation-canons/**/*.md"
  - "00-core-canons/**/*.md"
---

# Working with Documentation Canons

These are **canon files** that define rules for generating specific documentation types.

## When Editing Canons

### Structure Requirements

Every canon MUST include:
- Purpose section
- Scope (what it applies to, what it doesn't)
- Access Level Classification
- When to Generate
- Files to Generate (complete list)
- Directory Structure
- Generation Rules
- Content Guidelines (with examples)
- Validation section
- Agent Checklist

### Writing Style

Follow `00-core-canons/_core_canon.md`:
- NO emojis
- NO emdashes (—)
- Active voice
- Specific examples
- Vary sentence structure
- No AI clichés

### Format

Use Markdown with clear headings.

### Validation

After editing a canon:
1. Ensure structure is complete
2. Check for emojis/emdashes
3. Verify examples are correct
4. Test validation commands work

## When Creating New Canons

1. Copy `00-core-canons/_template.md` structure
2. Read existing canons for consistency
3. Include complete file structure
4. Provide working examples
5. Specify validation steps
6. Include access level classification

## Key References

- Core canon: `00-core-canons/_core_canon.md`
- Docs canon: `00-core-canons/_docs-canon.md`
- reST syntax: `03-reference/rest-syntax.md`

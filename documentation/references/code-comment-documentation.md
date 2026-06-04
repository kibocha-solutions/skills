# Code Comment Documentation

Use this reference when creating or revising comments, docstrings, API comment
blocks, or inline implementation notes.

## Goal

Comments preserve intent that code cannot express clearly by itself. They help
future maintainers understand public contracts, local invariants, trade-offs,
hazards, and non-obvious choices.

Do not use comments to narrate obvious syntax.

## Contents

- General Rules
- Package Level
- Module Level
- File Level
- Class Level
- Function and Method Level
- Line and Block Level
- Comment Freshness
- Documentation Comment Content
- Official and Primary References

## General Rules

- Match the language and repository convention first.
- Update comments in the same change that updates behavior.
- Prefer names and structure over comments when clearer code can remove the
  need for explanation.
- Use comments to explain why, when, constraints, side effects, and operational
  risks.
- Avoid repeating the function name, class name, type signature, or line of code
  in prose.
- Keep generated docs useful in IDE hover, API references, and source review.
- Remove stale, speculative, or aspirational comments.
- Mark temporary work with the repo's task convention and an owner or issue
  reference when available.

## Package Level

Package-level documentation explains why the package exists and how it fits into
the system.

Include:

- package responsibility and boundary
- primary public entry points
- important dependencies or integrations
- lifecycle or initialization requirements
- security, concurrency, or performance assumptions that affect all modules
- common usage pattern when package consumers need orientation

Avoid:

- listing every file
- repeating README content
- implementation details that belong in modules
- marketing language

## Module Level

Module-level documentation explains the module's purpose and safe use.

Include:

- module responsibility
- exported functions, classes, constants, or exceptions when the language
  convention expects them
- external systems touched by the module
- state, cache, environment, or configuration assumptions
- invariants that multiple functions rely on
- examples only when they prevent misuse

Avoid:

- describing imports
- restating all function signatures
- documenting private helper flow better handled by function comments

## File Level

File-level comments are useful when a file is not naturally represented as a
module, or when the file contains generated code, migrations, scripts,
configuration, or mixed declarations.

Include:

- why the file exists
- whether it is generated or hand-maintained
- how it is regenerated
- ordering constraints
- ownership or source of truth
- operational risk if edited incorrectly

Avoid file headers that only repeat the filename, copyright boilerplate already
handled elsewhere, or generic project slogans.

## Class Level

Class-level documentation describes the abstraction and its contract.

Include:

- what the class represents
- when to use it and when not to use it
- construction requirements
- ownership of resources
- lifecycle rules
- thread-safety, mutability, caching, or persistence behavior
- important collaborators
- exceptions or failure modes that shape normal use

Avoid:

- listing every method
- repeating property names without adding behavior
- saying only that the class "manages" or "handles" something

## Function and Method Level

Function and method documentation must help a caller use the API correctly.

Include when relevant:

- effect or returned value
- parameters whose valid values, units, defaults, or constraints are not obvious
- side effects
- errors, exceptions, or rejected states
- idempotency, ordering, concurrency, or transaction behavior
- security or authorization assumptions
- performance costs
- examples for tricky usage

Omit the comment when the function is private, small, and obvious, unless it
encodes a non-obvious invariant or risk.

For overrides, document only changed behavior, strengthened or weakened
preconditions, and important side effects.

## Line and Block Level

Line-level and block comments explain local intent.

Use them for:

- non-obvious algorithms
- business rules that look arbitrary in code
- workarounds for platform, compiler, dependency, or data issues
- security-sensitive checks
- concurrency and locking assumptions
- performance trade-offs
- validation that protects a later operation

Avoid inline comments that repeat the operation:

```python
count += 1  # Increment count
```

Prefer a useful reason:

```python
count += 1  # Account for the sentinel row appended by the importer.
```

Keep inline comments short. Move longer explanations above the block.

## Comment Freshness

Before keeping a comment, check:

- Does the code still do what the comment says?
- Does the comment describe current behavior instead of desired behavior?
- Would a rename, extraction, or clearer condition remove the need for it?
- Does the comment point to a real issue, decision record, or source of truth?
- Does it create maintenance work without helping the reader?

Delete comments that fail these checks.

## Documentation Comment Content

For public API comments, include descriptions for public classes, constants,
methods, parameters, return values, and exceptions when the language ecosystem
expects them.

Use present tense and direct verbs. Parameter descriptions should state purpose,
valid values, defaults, units, and boolean behavior where relevant. Return
descriptions should state what information the caller receives, not repeat the
return type.

## Official and Primary References

- Google API reference code comments:
  https://developers.google.com/style/api-reference-comments
- PEP 8 comments and documentation strings:
  https://peps.python.org/pep-0008/
- PEP 257 docstring conventions:
  https://peps.python.org/pep-0257/
- JetBrains WebStorm JSDoc comments:
  https://www.jetbrains.com/help/webstorm/creating-jsdoc-comments.html
- JSDoc ES module guidance:
  https://jsdoc.app/howto-es2015-modules

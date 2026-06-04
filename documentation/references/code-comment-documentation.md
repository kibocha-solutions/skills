# Code Comment Documentation

Use this reference when creating or revising language-native documentation
comments, docstrings, API comment blocks, or inline implementation notes.

## Goal

Comments preserve intent that code cannot express clearly by itself. They help
future maintainers understand public contracts, local invariants, trade-offs,
hazards, and non-obvious choices.

Do not use comments to narrate obvious syntax.

## Contents

- General Rules
- Documentation Comments and Implementation Comments
- Supported Documentation Levels
- Language Forms and Tag Sets
- Freshness and Missing-Level Audit
- Package Level
- Module Level
- File Level
- Class Level
- Constructor and Initializer Level
- Property, Field, and Attribute Level
- Function and Method Level
- Implementation Line and Block Level
- Comment Freshness
- Documentation Comment Content
- Bundled Examples
- Official and Primary References

## General Rules

- Match the language and repository convention first.
- Check the bundled examples when a comment level or language convention is
  unclear.
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

## Freshness and Missing-Level Audit

When changing source code or source-level documentation, check whether the
expected documentation levels are present and current:

- package or module overview
- file-level generated, migration, script, configuration, or ownership note
- class or type contract
- constructor or initializer contract
- public property, field, or attribute meaning
- public function or method contract
- implementation note for non-obvious local reasoning

Add missing or stale documentation directly when the code, tests, nearby docs,
or established project patterns make the contract clear. This is safe when the
change only adds or refreshes accurate documentation without altering behavior
or removing useful existing text.

Ask the user before changing documentation when:

- existing docs conflict with the code and the intended source of truth is
  unclear
- a public contract, lifecycle, side effect, error condition, or performance
  guarantee cannot be verified from local context
- replacing or deleting existing comments could remove useful history or
  stakeholder intent
- package, module, or file-level documentation is missing but the boundary or
  ownership model is not clear

After adding non-destructive documentation, tell the user which levels were
filled or refreshed.

## Documentation Comments and Implementation Comments

Keep generated API documentation separate from ordinary implementation notes.

Use language-native documentation comments for public or package-level API
contracts:

- Kotlin: KDoc `/** ... */` with tags such as `@param`, `@property`,
  `@constructor`, `@return`, and `@throws`.
- Python: module, class, function, and method docstrings.
- JavaScript and TypeScript: JSDoc `/** ... */` with tags such as `@param`,
  `@returns`, `@throws`, `@template`, and `@property`.
- Go: doc comments immediately preceding packages, exported types, functions,
  methods, constants, and variables.

Use ordinary line or block comments for local implementation notes that should
not become generated API documentation:

- `//` or `/* ... */` in Kotlin, JavaScript, TypeScript, Go, Java, C-like
  languages
- `#` comments in Python

Do not use ordinary block comments as a substitute for KDoc, JSDoc, Go doc
comments, or Python docstrings when documenting public API contracts.

## Supported Documentation Levels

Treat these as documentation targets. Not every language supports every target
with the same syntax.

- Package level: documents a package or library namespace. It explains the
  package responsibility, boundaries, entry points, and package-wide
  assumptions.
- Module level: documents a source module or JavaScript module. It explains the
  exported surface and required caller context.
- File level: documents generated files, migrations, scripts, configuration, or
  mixed-declaration files whose safety depends on file-wide rules.
- Class or type level: documents the abstraction represented by a class, data
  type, interface, enum, or struct.
- Constructor or initializer level: documents construction requirements,
  required dependencies, initialized state, and construction failures.
- Property, field, or attribute level: documents public data members whose
  meaning, units, defaults, lifecycle, or mutability are not obvious from the
  name and type.
- Function or method level: documents caller-visible behavior, inputs, outputs,
  errors, side effects, ordering, concurrency, performance, and examples.
- Implementation line or block level: documents local reasoning inside a body.
  It is not generated API documentation.

## Language Forms and Tag Sets

Use the repository's language convention first. When no convention exists, use
these defaults.

### Kotlin

- Package and module: use Dokka include Markdown with headings such as
  `# Module name` and `# Package com.example.name`.
- Class, constructor, property, function, and method: use KDoc `/** ... */`.
- Generic and value parameters: `@param name` or `@param[name]`.
- Primary-constructor properties: `@property name`.
- Constructor summary: `@constructor`.
- Return value: `@return`.
- Extension receiver: `@receiver`.
- Exceptions worth caller attention: `@throws Type` or `@exception Type`.
- Runnable or compiled sample reference: `@sample qualified.name`.
- Related API: `@see qualified.name`.
- Since/version note: `@since`.
- Suppress generated docs for externally visible non-API elements: `@suppress`.
- Deprecation: use the Kotlin `@Deprecated` annotation, not a KDoc
  `@deprecated` tag.

### Python

- Package: use the module docstring in the package's `__init__.py`.
- Module, class, function, and method: use triple double-quoted docstrings as
  the first statement of the object.
- Public methods, including `__init__`, should have docstrings when they are
  part of the public API.
- Public attributes may use attribute docstrings when tooling supports them.
- PEP 257 defines placement and prose conventions, but not a single field
  syntax for parameters and returns.
- When Sphinx-style fields are the project convention, use `:param name:`,
  `:type name:`, `:return:`, `:rtype:`, `:raises Type:`, `:ivar name:`,
  `:cvar name:`, `:var name:`, and related aliases.
- When Google-style docstrings are the project convention, use sections such as
  `Args:`, `Returns:`, `Yields:`, `Raises:`, and `Examples:`.
- Do not repeat obvious type hints. Document constraints, units, defaults,
  accepted ranges, side effects, errors, and non-obvious return meanings.

### JavaScript and TypeScript

- Module: use `@module` when the file should appear as a module in generated
  docs.
- Function and method: use JSDoc `/** ... */` with `@param`, `@returns` or
  `@return`, and `@throws` when relevant.
- Optional parameters: use `[name]`, `[name=default]`, or the project-supported
  Closure-style optional syntax.
- Rest parameters: use a repeatable type such as `@param {...number} values`.
- Object or typedef properties: use `@typedef` with `@property`.
- Generic type parameters: use `@template`.
- Constructor functions: use `@constructor` when a function is intended to be
  called with `new`.
- Classes may also use `@class`, `@extends`, and `@implements` when the
  repository convention or tooling needs those tags.
- Use `@type`, `@const`, and `@readonly` for exported values when the type or
  mutability is not clear from code or TypeScript declarations.

### Go

- Package, exported const, func, type, and var declarations use ordinary Go
  doc comments immediately before the declaration with no blank line.
- Every exported name should have a doc comment.
- Package comments start with `Package name ...`.
- Exported symbol comments normally start with the symbol name.
- Type comments explain what an instance represents or provides, plus
  concurrency and zero-value behavior when those matter.
- Function and method comments explain what the operation does or returns and
  any caller-visible special cases.
- Explain exported struct fields in the type comment or with per-field
  comments.
- Use a `Deprecated:` paragraph in the doc comment for deprecated exported
  identifiers.
- Do not document implementation algorithms in Go doc comments unless a
  caller-visible complexity bound matters.

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

## Constructor and Initializer Level

Constructor and initializer documentation explains how an object becomes valid.

Include:

- required dependencies or collaborators
- validation performed during construction
- default values and optional parameters
- initialized resource ownership
- construction side effects
- errors raised or thrown during construction
- lifecycle rules that begin at construction

Avoid:

- repeating every constructor parameter without adding constraints or purpose
- documenting private wiring that callers cannot observe
- claiming an object is ready for use when later initialization is required

## Property, Field, and Attribute Level

Property, field, and attribute documentation explains public data members.

Include:

- meaning, unit, format, or allowed values
- default value when not obvious
- mutability and lifecycle
- ownership or aliasing rules
- whether callers may persist, compare, or expose the value
- relationship to constructor parameters or serialized fields

Avoid:

- repeating the property name in sentence form
- documenting private storage only to satisfy a comment quota
- duplicating type annotations unless generated documentation cannot display
  the type

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

## Implementation Line and Block Level

Line-level and block comments explain local implementation intent. They are not
API documentation blocks.

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

Keep inline comments short. Move longer explanations above the relevant block,
but keep them as ordinary implementation comments unless the text documents a
public API contract.

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

## Bundled Examples

When examples would help calibrate the right level of detail, review
`../examples/code-comments/` before drafting or revising comments. Use the
examples to copy the shape of a compliant comment, not the domain wording.

The bundled examples cover:

- Kotlin Dokka package include Markdown, KDoc class, constructor-property,
  function, extension-function, and local implementation comments
- Python module, class, function, method, implementation, and freshness examples
- JavaScript JSDoc for modules, classes, typedefs, functions, and local
  implementation comments
- Go package, generated-file, exported type, function, method, and local
  implementation comments

## Official and Primary References

- Kotlin KDoc:
  https://kotlinlang.org/docs/kotlin-doc.html
- Kotlin Dokka module and package documentation:
  https://kotlinlang.org/docs/dokka-module-and-package-docs.html
- PEP 257 docstring conventions:
  https://peps.python.org/pep-0257/
- Sphinx Python domain info field lists:
  https://www.sphinx-doc.org/en/master/usage/domains/python.html
- Google API reference code comments:
  https://developers.google.com/style/api-reference-comments
- PEP 8 comments and documentation strings:
  https://peps.python.org/pep-0008/
- JetBrains WebStorm JSDoc comments:
  https://www.jetbrains.com/help/webstorm/creating-jsdoc-comments.html
- JSDoc ES module guidance:
  https://jsdoc.app/howto-es2015-modules
- JSDoc type and tag syntax:
  https://jsdoc.app/tags-type
- TypeScript-supported JSDoc reference:
  https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html
- Go doc comments:
  https://go.dev/doc/comment
- Godoc documentation conventions:
  https://go.dev/blog/godoc

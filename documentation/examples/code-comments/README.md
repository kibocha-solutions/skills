# Code Comment Examples

Use these examples when applying `references/code-comment-documentation.md`.
They show language-native documentation comments and docstrings at the levels
the reference defines: package, module, file, class or type, constructor or
initializer, property or field, function, method, and local implementation
notes.

## Examples

- `kotlin-comments.md`: Dokka package include Markdown, KDoc for classes,
  generic parameters, constructor properties, functions, and local
  implementation notes.
- `python-comments.md`: module, class, function, and method docstrings plus
  package and local implementation notes.
- `javascript-comments.md`: JSDoc for modules, classes, constructors,
  typedefs, functions, parameters, return values, thrown errors, and local
  implementation notes.
- `go-comments.md`: Go doc comments for packages, exported types, functions,
  methods, fields, deprecation, and local implementation notes.

## Review Use

When writing or revising comments:

1. Choose the example closest to the language and documentation level.
2. Keep only facts the code or repository context supports.
3. Adapt the structure, not the domain wording.
4. Use ordinary line or block comments only for implementation notes that should
   not become generated API documentation.

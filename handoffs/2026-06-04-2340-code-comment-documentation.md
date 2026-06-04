# Handoff: code comment documentation

## Datetime

2026-06-04 23:40 EAT

## Current objective

Refine the `documentation` skill so agents produce and maintain language-native
source documentation comments, docstrings, and implementation comments at the
right level.

## State of the repo

Current branch: `feat/docs`.

The documentation skill has uncommitted updates for source-level documentation
guidance. The work now distinguishes generated/API documentation comments from
ordinary implementation comments, adds supported documentation levels, adds
language-specific forms and tag sets, and introduces examples for Kotlin,
Python, JavaScript, and Go.

Separate pre-existing staged work remains present:

- `.gitmodules`
- `sources/anthropic-skills`

Those staged items were not edited as part of the documentation-comment work.

## Decisions made

- Treat language-native documentation comments and docstrings as the primary
  form for public API documentation.
- Keep ordinary `//`, `/* ... */`, and `#` comments for narrow implementation
  notes only.
- Support eight documentation targets: package, module, file, class/type,
  constructor/initializer, property/field/attribute, function/method, and
  implementation line/block.
- Kotlin package and module documentation should use Dokka include Markdown;
  KDoc is for classes, functions, constructor parameters, properties, receivers,
  returns, throws, samples, and related API references.
- Python examples include both Google-style and Sphinx-style function
  docstrings because PEP 257 defines placement and prose, not one parameter
  field syntax.
- Go examples follow Go doc comment conventions: package comments start with
  `Package`, exported symbol comments start with the symbol name, and
  deprecation uses a `Deprecated:` paragraph.
- Agents must audit whether expected source-documentation levels are present
  and current. They should add safe non-destructive documentation from local
  evidence, then report what was added. They should ask before replacing
  existing docs, deleting disputed comments, or inventing unverifiable contracts.

## Files changed

- `AGENTS.md`: routes documentation comments through the `documentation` skill,
  points to examples, and adds the missing/stale documentation audit rule.
- `documentation/SKILL.md`: adds documentation freshness and missing-level
  audit steps to the default workflow.
- `documentation/references/code-comment-documentation.md`: expands the
  reference with documentation levels, language forms and tags, freshness audit
  rules, constructor/property guidance, official references, and example
  routing.
- `documentation/examples/code-comments/README.md`: explains how to use bundled
  examples.
- `documentation/examples/code-comments/kotlin-comments.md`: adds Dokka package
  include and KDoc examples.
- `documentation/examples/code-comments/python-comments.md`: adds package,
  module, class, Google-style function, Sphinx-style function, method, and
  implementation-note examples.
- `documentation/examples/code-comments/javascript-comments.md`: adds JSDoc
  module, typedef, class, constructor, function, optional/rest/generic parameter,
  return, throws, and implementation-note examples.
- `documentation/examples/code-comments/go-comments.md`: adds Go package,
  generated-file, exported type, field, function, method, deprecated identifier,
  and implementation-note examples.

## Open questions

- Should the code-comment examples be split further by language convention, for
  example Python Google style versus Sphinx style in separate files?
- Should the repository add a validation script later to flag stale placeholders,
  missing example references, or unsupported documentation tags?
- Should similar examples be added for Java/Javadoc, Rust/Rustdoc, and
  TypeScript-specific declarations?

## Next entry point

1. Review the uncommitted documentation-comment changes and examples.
2. Decide whether to commit the documentation-comment work separately from the
   staged submodule work.
3. If continuing the documentation skill, consider adding examples for Java,
   Rust, and TypeScript-specific documentation forms.
4. Keep future edits aligned with the source-material rule: distill guidance,
   do not copy source material wholesale.

## Constraints

- Do not delete `sources/` or handoff documents unless the user explicitly
  requests it.
- Treat `sources/` as source material, not active skill guidance.
- Ignore the reports directory for this handoff context.
- Keep `SKILL.md` concise and procedural; keep detailed source-documentation
  guidance in `documentation/references/`.
- Add documentation automatically only when local evidence makes it safe and
  non-destructive.
- Ask before replacing existing docs, deleting disputed comments, or inventing
  contracts that cannot be verified from code and nearby docs.

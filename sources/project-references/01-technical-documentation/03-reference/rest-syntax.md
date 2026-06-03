# reStructuredText (reST) Quick Reference

## Overview

reStructuredText (reST) is the primary markup language for all narrative technical documentation in this framework. It provides semantic structure, powerful cross-referencing, and extensibility.

**Official Docs:** https://docutils.sourceforge.io/rst.html  
**Sphinx Guide:** https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

---

## Why reST Over Markdown

**reST Advantages:**
- Semantic structure (define custom directives)
- Built-in cross-referencing
- Math support
- Tables with column spanning
- Warnings, notes, code-blocks with language
- Extensible via Sphinx extensions

**When to Use Markdown:**
- README files (widely supported on GitHub)
- CHANGELOG files (Keep a Changelog standard)
- ADRs (Architecture Decision Records)

---

## Headings

```rst
Document Title
==============

Section
-------

Subsection
~~~~~~~~~~

Subsubsection
^^^^^^^^^^^^^
```

**Rules:**
- Underline must be at least as long as text
- Hierarchy determined by order of appearance (not character choice)
- Most common convention: `=` `-` `~` `^`

---

## Paragraphs

Paragraphs separated by blank line:

```rst
This is a paragraph with normal text.

This is another paragraph after a blank line.
```

**Line Breaks:**

```rst
This is a long sentence that spans
multiple lines but renders as one paragraph.

| This is a line.
| This is another line.
| Line breaks preserved.
```

---

## Inline Markup

```rst
*italic text*
**bold text**
``code or literal text``
```

**Rendered:**
- *italic text* - Emphasis
- **bold text** - Strong emphasis
- `code or literal text` - Monospace font

---

## Lists

### Bullet Lists

```rst
- First item
- Second item

  - Nested item
  - Another nested item

- Third item
```

### Numbered Lists

```rst
1. First item
2. Second item
3. Third item

   a. Nested item
   b. Another nested item

4. Fourth item
```

### Auto-Numbered

```rst
#. First item
#. Second item
#. Third item (numbering automatic)
```

### Definition Lists

```rst
Term
    Definition of term

Another Term
    Definition of another term
```

---

## Code Blocks

### Simple Code Block

```rst
::

    def calculate_tax(salary):
        return salary * 0.15
```

### With Language Highlighting

```rst
.. code-block:: python

   def calculate_tax(salary):
       return salary * 0.15
```

### Inline Code

```rst
Use the ``calculate_tax()`` function to compute taxes.
```

---

## Links

### External Links

```rst
Visit `Python <https://python.org>`_ for more information.

Or use anonymous reference:
Visit Python_ for more information.

.. _Python: https://python.org
```

### Internal Cross-References

```rst
See :doc:`architecture` for system design.

See :doc:`/architecture/overview` for absolute path.

See :ref:`calculating-taxes` for tax calculations.

.. _calculating-taxes:

Tax Calculations
================

Content here...
```

---

## Images and Figures

### Basic Image

```rst
.. image:: path/to/image.png
   :alt: Alternative text
   :width: 600px
```

### Figure with Caption

```rst
.. figure:: path/to/image.png
   :alt: System architecture
   :width: 800px
   :align: center
   
   Figure 1: High-level system architecture showing all components.
```

---

## Tables

### Simple Table

```rst
=====  =====  ======
A      B      Result
=====  =====  ======
1      2      3
4      5      9
=====  =====  ======
```

### List Table (Easier to Write)

```rst
.. list-table:: Tax Brackets 2025
   :header-rows: 1
   :widths: 30 30 40

   * - Income Range
     - Tax Rate
     - Example
   * - 0 - 24,000
     - 10%
     - KES 2,400
   * - 24,001 - 32,333
     - 25%
     - KES 8,333
```

---

## Admonitions (Warnings, Notes, Tips)

```rst
.. note::
   This is a note providing additional information.

.. warning::
   This is a warning about potential issues.

.. danger::
   This is a danger notice for critical warnings.

.. tip::
   This is a helpful tip for users.

.. important::
   This highlights important information.

.. caution::
   This advises caution.
```

---

## Table of Contents

### Document TOC

```rst
.. contents::
   :local:
   :depth: 2
```

### Sphinx Toctree

```rst
.. toctree::
   :maxdepth: 2

   introduction
   getting-started
   api-reference
```

---

## Comments

```rst
.. This is a comment and won't appear in output

..
   This is a multi-line comment.
   Also hidden from output.
```

---

## Line Blocks (Poetry, Addresses)

```rst
| Line 1
| Line 2
| Line 3
```

---

## Field Lists (Metadata)

```rst
:Author: John Doe
:Version: 1.0
:Date: 2025-12-29
:Email: john@example.com
```

---

## Substitutions

```rst
.. |name| replace:: Tax Management System
.. |version| replace:: 2.5.0

Welcome to the |name| version |version|.
```

---

## Raw HTML (Use Sparingly)

```rst
.. raw:: html

   <div class="custom-class">
   Custom HTML content
   </div>
```

---

## Common Sphinx Directives

### Version Added/Changed

```rst
.. versionadded:: 2.5.0
   Multi-currency support added.

.. versionchanged:: 2.4.0
   Tax calculation formula updated for 2025 rates.

.. deprecated:: 2.3.0
   Use new API endpoint instead.
```

### Index Entries

```rst
.. index::
   single: tax calculation
   pair: API; authentication
```

---

## Best Practices

### Heading Consistency

Use consistent underline characters throughout project:

```rst
# Document level (==)
# Section level (-)
# Subsection level (~)
# Subsubsection level (^)
```

### Cross-Referencing

Always use explicit labels for important sections:

```rst
.. _installation:

Installation
============

To install, run: pip install package

Later, reference it:
See :ref:`installation` for setup instructions.
```

### File Naming

Use consistent naming:
- `00-index.rst` - Index/overview
- `01-getting-started.rst` - Numbered for ordering
- `feature-name.rst` - Descriptive names (lowercase-with-hyphens)

### TOC Depth

Limit depth to avoid overwhelming users:

```rst
.. toctree::
   :maxdepth: 2  # Show 2 levels only
```

---

## Validation

### Check Syntax

```bash
# Install rstcheck
pip install rstcheck

# Validate file
rstcheck document.rst

# Validate directory
rstcheck docs/source/*.rst
```

### Build with Sphinx

```bash
# Build HTML
sphinx-build -b html docs/source docs/build

# Build with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

---

## Common Errors

### Error: "Unexpected indentation"

**Cause:** Incorrect indentation in directive

**Fix:** Ensure content indented 3 spaces:

```rst
.. code-block:: python

   def function():  # 3 spaces indent
       pass
```

### Error: "Unknown directive type"

**Cause:** Missing Sphinx extension

**Fix:** Add extension to `conf.py`:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
]
```

### Error: "Duplicate explicit target name"

**Cause:** Two sections with same label

**Fix:** Use unique labels:

```rst
.. _intro-overview:

Overview (Introduction)
=======================

.. _api-overview:

Overview (API Reference)
========================
```

---

## Quick Comparison: reST vs Markdown

| Feature | reST | Markdown |
|---------|------|----------|
| Headers | Underline with `=` `-` | `#` `##` `###` |
| Bold | `**text**` | `**text**` |
| Italic | `*text*` | `*text*` |
| Code | `` `text` `` | `` `text` `` |
| Links | `` `label <url>`_ `` | `[label](url)` |
| Images | `.. image::` | `![alt](url)` |
| Tables | List-table directive | Pipe tables |
| Admonitions | `.. note::` | Blockquotes |
| TOC | `.. contents::` | Manual |
| Cross-refs | `:doc:` `:ref:` | Manual links |

---

## Resources

- **reST Primer:** https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- **Docutils Spec:** https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
- **Sphinx Directives:** https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
- **reST Cheat Sheet:** https://github.com/ralsina/rst-cheatsheet

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial reStructuredText quick reference
- Covers essential syntax for technical documentation

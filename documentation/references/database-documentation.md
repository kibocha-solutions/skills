# Database Documentation

Use this reference for database schema, migrations, data dictionary, entity
relationships, backup, and recovery documentation.

## Required Sources

- Migrations, schema files, ORM models, serializers, seed data, fixtures,
  queries, indexes, backup scripts, and database tests.

## Default Paths

- `docs/domain/entity-relationship-model.md`
- `docs/data/object-document-model.md`
- `docs/data/database-schema.md`
- `docs/data/data-dictionary.md`
- `docs/data/backup-recovery.md`
- diagrams in `docs/diagrams/entity-relationship.drawio` and `.svg`

## Required Content

- Database technology and source of truth.
- Tables, collections, documents, entities, relationships, and ownership.
- Primary keys, foreign keys, unique constraints, indexes, and important
  constraints.
- Field meanings, units, allowed values, nullability, defaults, and sensitivity.
- Migration rules, rollback constraints, and compatibility concerns.
- Backup, restore, and integrity verification for hosted data.

## Table Documentation Shape

When a database table has its own source file, migration, model, or accepted
design draft, document it on its own page by default. Do not merge multiple
tables into one table-design page when each table has separate columns,
constraints, relationships, lifecycle rules, or boundary decisions.

Each table page should be complete enough for a careful intern or new
contributor to understand and review the table without relying on another page
for basic meaning. Include the relevant parts of this structure:

- title using the table name
- overview of what the table stores, who creates rows, and what the table does
  not own
- function or responsibility, including source-of-truth boundaries
- local relationship diagram showing the table, direct dependencies, and direct
  dependents
- table design summary: primary key, natural key, normal form target,
  cardinality, ownership, lifecycle state, and durable source basis when that
  source can be named without exposing hidden planning paths
- complete column table with data type, requiredness or value rule, default,
  relationship, sensitivity, and notes
- keys, constraints, indexes, and important partial-index rules
- inbound and outbound relationships, including ownership and tenant behavior
  when known
- lifecycle, workflow, migration, and deletion or archive behavior
- source-backed examples
- boundary rules and common mistakes
- FAQ when real design ambiguity or implementation confusion exists

Use Writerside semantic markup where it improves the page. FAQ sections should
use `<deflist collapsible="true">`. Use plain paragraphs for boundary notes,
lifecycle guidance, and validation guidance unless a table or definition list
gives the reader a clearer reference.

Official table documentation must not cite temporary planning paths such as
agent brain folders, hidden scratch files, or chat-only design notes. When a
temporary design draft is the source used during documentation work, publish
the accepted facts in the table page and cite only durable documentation,
schema, migration, model, or generated assets that are expected to remain
available to documentation readers.

Scope overview pages are useful for groups such as users, organizations,
permissions, storage, or shared infrastructure. Keep those pages focused on
navigation, all-table relationship diagrams, ownership summaries, and links to
the table pages. Do not use a scope overview as a substitute for the one-page
table design.

For table-level ERDs, show the current table, the tables it references, and the
tables that reference it. Neighbor tables can appear as named boxes with
relationship labels. Do not list every neighbor column in the diagram when the
table page already defines the documented table's columns in tabular form.

## Workflow

1. Separate domain ER documentation from physical schema when both exist.
2. Generate or refresh ER diagrams through `technical-diagrams`.
3. Treat data classification as Restricted when PII, auth, finance, donor,
   beneficiary, or regulated data exists.
4. Do not document speculative future tables as current schema.
5. Link schema docs to migrations or model files.

## Validation

- Every documented field exists in code, schema, or a stated design draft.
- Relationships and constraints match the source of truth.
- Sensitive fields have classification and handling notes.
- Restore procedures include verification.

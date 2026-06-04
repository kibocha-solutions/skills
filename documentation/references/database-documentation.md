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

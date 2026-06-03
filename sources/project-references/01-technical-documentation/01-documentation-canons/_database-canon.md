# Canon: Database Documentation

## Purpose

Database documentation provides complete reference for database schema, data models, migration procedures, backup strategies, and performance optimization. It enables developers to understand data structures, database administrators to maintain systems, and ensures data integrity and recovery capabilities.

---

## Scope

**This canon applies to:**
- Relational databases (PostgreSQL, MySQL, SQL Server, Oracle)
- NoSQL databases (MongoDB, Cassandra, DynamoDB) 
- Database schema and data models
- Migration procedures
- Backup and recovery procedures
- Performance tuning and indexing strategies

**This canon does NOT apply to:**
- Application data models (document in code)
- Caching strategies (use architecture documentation)
- ORM configurations (document in service README)

---

## Access Level Classification

**Database Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Database administrators, backend developers, DevOps team
- **Storage:** Private repository with authentication
- **Review:** Database team review, security clearance for sensitive schemas
- **Rationale:** Contains data structure details, business logic exposed through schema, potential security vulnerabilities

**Exception:** Sample schema or ERDs may be Public (Level 1) for open-source projects (with sensitive data removed)

---

## When to Generate

### Initial Creation
- **Database Design Phase:** Before implementation (schema design)
- **Migration Planning:** Document migration strategy before execution
- **Performance Baseline:** After initial data load

### Updates
- After schema changes (new tables, columns, constraints)
- After index additions or removals
- After major performance optimizations
- Monthly for backup procedure verification

### Frequency
- **Initial:** During database design phase
- **Schema Changes:** Every migration
- **Performance Tuning:** Quarterly review
- **Backup Verification:** Monthly testing

---

## Files to Generate

Agent must create the following files when documenting databases:

### 1. Database Documentation Index
**File:** `/docs/source/database/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Database documentation entry point

### 2. Schema Overview
**File:** `/docs/source/database/01-schema-overview.rst`  
**Format:** reStructuredText  
**Purpose:** High-level schema design and entity relationships

### 3. Table Definitions
**File:** `/docs/source/database/02-tables.rst`  
**Format:** reStructuredText  
**Purpose:** Detailed table, column, and constraint documentation

### 4. Indexes and Performance
**File:** `/docs/source/database/03-indexes.rst`  
**Format:** reStructuredText  
**Purpose:** Index strategy, query optimization, performance tuning

### 5. Migrations
**File:** `/docs/source/database/04-migrations.rst`  
**Format:** reStructuredText  
**Purpose:** Migration procedures, versioning, rollback strategies

### 6. Backup and Recovery
**File:** `/docs/source/database/05-backup-restore.rst`  
**Format:** reStructuredText  
**Purpose:** Backup procedures, recovery testing, disaster recovery

### 7. Entity Relationship Diagram (ERD)
**File:** `/docs/source/database/diagrams/erd.drawio` and `.png`  
**Format:** diagrams.net (exported PNG for docs)  
**Purpose:** Visual representation of database schema

---

## Directory Structure

```
docs/source/database/
├── 00-index.rst                    # Database documentation entry point
├── 01-schema-overview.rst          # High-level schema design
├── 02-tables.rst                   # Table and column definitions
├── 03-indexes.rst                  # Index strategy and performance
├── 04-migrations.rst               # Migration procedures
├── 05-backup-restore.rst           # Backup and recovery procedures
└── diagrams/
    ├── erd.drawio                  # Entity Relationship Diagram (editable)
    └── erd.png                     # ERD exported for documentation
```

---

## Generation Rules

### Schema Documentation

**For each table, document:**
1. **Purpose** - What the table stores
2. **Columns** - Name, type, constraints, default values
3. **Primary Key** - Unique identifier
4. **Foreign Keys** - Relationships to other tables
5. **Indexes** - Performance optimization
6. **Business Rules** - Constraints and validation

### Column Documentation Format

```rst
**Column Name**
- Type: ``VARCHAR(255)``
- Nullable: No
- Default: None
- Description: Brief explanation
- Constraints: ``UNIQUE``, ``CHECK (value > 0)``
```

### Migration Documentation

Document migrations in chronological order:
- Migration number/version
- Purpose and changes
- SQL statements
- Rollback procedure
- Data migration notes

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice
- Specific over vague (exact data types, sizes, constraints)
- Vary sentence structure
- **Tables are appropriate** for listing columns and constraints

---

## Content Guidelines

### Database Index (`/docs/source/database/00-index.rst`)

```rst
Database Documentation
======================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains sensitive database schema details.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

The Tax Management System uses PostgreSQL 15 as the primary database.

**Database Host**: tms-postgres.internal (production)  
**Database Name**: ``tms_production``  
**Schema Version**: ``v2.5.0`` (as of Dec 2025)  
**Total Tables**: 18  
**Total Indexes**: 45  
**Database Size**: 15 GB

Schema Design Principles
------------------------

**Normalization**: Third Normal Form (3NF) for transactional data  
**Denormalization**: Reporting tables use materialized views for performance  
**Partitioning**: Tax calculations table partitioned by year  
**Constraints**: Foreign keys enforced for referential integrity

Quick Links
-----------

- **Schema Overview**: :doc:`01-schema-overview`
- **Table Reference**: :doc:`02-tables`
- **Performance Tuning**: :doc:`03-indexes`
- **Migration Guide**: :doc:`04-migrations`
- **Backup Procedures**: :doc:`05-backup-restore`

.. toctree::
   :maxdepth: 2

   01-schema-overview
   02-tables
   03-indexes
   04-migrations
   05-backup-restore

Entity Relationship Diagram
---------------------------

.. figure:: diagrams/erd.png
   :alt: Entity Relationship Diagram
   :width: 100%
   
   Database schema showing all tables and relationships.
```

### Schema Overview (`/docs/source/database/01-schema-overview.rst`)

```rst
Schema Overview
===============

High-level overview of database design and entity relationships.

Core Entities
-------------

**Users**
- Stores user accounts and authentication data
- Primary table: ``users``
- Related tables: ``user_sessions``, ``user_roles``

**Tax Calculations**
- Stores tax calculation requests and results
- Primary table: ``tax_calculations``
- Related tables: ``tax_brackets``, ``calculation_history``
- Partitioned by year for performance

**Receipts**
- Stores receipt metadata (files stored in S3)
- Primary table: ``receipts``
- Related tables: ``receipt_items``

**Integrations**
- Tracks external system integrations
- Primary table: ``integration_logs``
- Related tables: ``kra_submissions``, ``mpesa_transactions``

Schema Diagram
--------------

.. figure:: diagrams/erd.png
   :alt: Entity Relationship Diagram
   :width: 100%
   
   Complete entity relationship diagram.

Key Relationships
-----------------

**Users → Tax Calculations**
- One-to-many relationship
- Foreign key: ``tax_calculations.user_id`` → ``users.id``
- Cascading delete: Disabled (preserve audit trail)

**Tax Calculations → Receipts**
- One-to-many relationship
- Foreign key: ``receipts.calculation_id`` → ``tax_calculations.id``
- Cascading delete: Enabled

**Tax Calculations → Tax Brackets**
- Many-to-many relationship
- Join table: ``calculation_brackets``

Data Volumes
------------

**Current (Dec 2025):**
- Users: 50,000 records
- Tax Calculations: 2,500,000 records (partitioned by year)
- Receipts: 3,000,000 records
- Integration Logs: 10,000,000 records (rotated monthly)

**Growth Rate:**
- Tax Calculations: +200,000/month
- Receipts: +250,000/month
```

### Table Definitions (`/docs/source/database/02-tables.rst`)

```rst
Table Definitions
=================

Detailed reference for all database tables.

users
-----

Stores user account information.

**Purpose**: User authentication and profile data

**Columns:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 10 45

   * - Column
     - Type
     - Nullable
     - Default
     - Description
   * - ``id``
     - UUID
     - No
     - ``gen_random_uuid()``
     - Primary key, unique user identifier
   * - ``email``
     - VARCHAR(255)
     - No
     - 
     - User email address (unique)
   * - ``password_hash``
     - VARCHAR(255)
     - No
     - 
     - Bcrypt hashed password
   * - ``name``
     - VARCHAR(100)
     - No
     - 
     - User's display name
   * - ``role``
     - VARCHAR(50)
     - No
     - ``'user'``
     - User role (user, admin, system_admin)
   * - ``created_at``
     - TIMESTAMPTZ
     - No
     - ``CURRENT_TIMESTAMP``
     - Account creation timestamp
   * - ``updated_at``
     - TIMESTAMPTZ
     - No
     - ``CURRENT_TIMESTAMP``
     - Last update timestamp
   * - ``last_login_at``
     - TIMESTAMPTZ
     - Yes
     - NULL
     - Last successful login timestamp

**Constraints:**

.. code-block:: sql

   PRIMARY KEY (id)
   UNIQUE (email)
   CHECK (role IN ('user', 'admin', 'system_admin'))
   CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')

**Indexes:**

.. code-block:: sql

   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_users_created_at ON users(created_at);

**Sample Data:**

.. code-block:: sql

   INSERT INTO users (email, password_hash, name, role) VALUES
   ('admin@example.com', '$2a$10$...', 'Admin User', 'admin'),
   ('user@example.com', '$2a$10$...', 'Regular User', 'user');

tax_calculations
----------------

Stores tax calculation requests and results.

**Purpose**: PAYE tax calculations with KRA compliance

**Partitioning**: Partitioned by year (``created_at``)

**Columns:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 10 45

   * - Column
     - Type
     - Nullable
     - Default
     - Description
   * - ``id``
     - UUID
     - No
     - ``gen_random_uuid()``
     - Primary key
   * - ``user_id``
     - UUID
     - No
     - 
     - Foreign key to users.id
   * - ``gross_salary``
     - NUMERIC(12,2)
     - No
     - 
     - Gross monthly salary in KES
   * - ``tax_amount``
     - NUMERIC(12,2)
     - No
     - 
     - Calculated PAYE tax in KES
   * - ``effective_rate``
     - NUMERIC(5,2)
     - No
     - 
     - Effective tax rate percentage
   * - ``relief_amount``
     - NUMERIC(12,2)
     - No
     - ``2400.00``
     - Personal relief in KES
   * - ``created_at``
     - TIMESTAMPTZ
     - No
     - ``CURRENT_TIMESTAMP``
     - Calculation timestamp

**Constraints:**

.. code-block:: sql

   PRIMARY KEY (id, created_at)  -- Composite key for partitioning
   FOREIGN KEY (user_id) REFERENCES users(id)
   CHECK (gross_salary >= 0)
   CHECK (tax_amount >= 0)
   CHECK (effective_rate >= 0 AND effective_rate <= 100)

**Partitions:**

.. code-block:: sql

   -- Partition for 2024
   CREATE TABLE tax_calculations_2024 PARTITION OF tax_calculations
   FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

   -- Partition for 2025
   CREATE TABLE tax_calculations_2025 PARTITION OF tax_calculations
   FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

**Indexes:**

.. code-block:: sql

   CREATE INDEX idx_tax_calc_user_id ON tax_calculations(user_id);
   CREATE INDEX idx_tax_calc_created_at ON tax_calculations(created_at);
```

### Indexes (`/docs/source/database/03-indexes.rst`)

```rst
Indexes and Performance
=======================

Index strategy and query optimization.

Index Strategy
--------------

**Primary Indexes:**
- All primary keys have automatic B-tree indexes
- Composite primary keys for partitioned tables

**Foreign Key Indexes:**
- All foreign keys indexed for join performance
- Example: ``tax_calculations.user_id``

**Query-Specific Indexes:**
- Created based on actual query patterns
- Reviewed quarterly, unused indexes removed

Index Types
-----------

**B-Tree Indexes** (default)
- Used for equality and range queries
- Example: ``CREATE INDEX idx_users_email ON users(email);``

**Partial Indexes**
- Index only subset of rows
- Example:

.. code-block:: sql

   CREATE INDEX idx_active_users ON users(id) WHERE deleted_at IS NULL;

**Composite Indexes**
- Multiple columns in single index
- Example:

.. code-block:: sql

   CREATE INDEX idx_calc_user_created ON tax_calculations(user_id, created_at DESC);

Query Optimization
------------------

**Slow Query Example:**

.. code-block:: sql

   -- SLOW: No index on created_at filter
   SELECT * FROM tax_calculations
   WHERE created_at > '2025-01-01'
   ORDER BY created_at DESC
   LIMIT 100;

**Optimized with Index:**

.. code-block:: sql

   CREATE INDEX idx_calc_created_desc ON tax_calculations(created_at DESC);

   -- Now fast with index
   EXPLAIN ANALYZE SELECT * FROM tax_calculations
   WHERE created_at > '2025-01-01'
   ORDER BY created_at DESC
   LIMIT 100;

Performance Metrics
-------------------

**Target Query Performance:**
- Simple SELECT by ID: < 1ms
- Filtered queries with indexes: < 10ms
- Complex joins: < 50ms
- Aggregation queries: < 100ms

**Index Maintenance:**
- VACUUM: Automatic (autovacuum enabled)
- ANALYZE: Weekly via cron job
- REINDEX: Quarterly for heavily updated tables
```

### Migrations (`/docs/source/database/04-migrations.rst`)

```rst
Database Migrations
===================

Migration procedures and version control.

Migration Strategy
------------------

**Tools**: Flyway (Java-based migration tool)  
**Versioning**: ``V{version}__{description}.sql``  
**Direction**: Forward-only (no rollback in production)

Migration Files
---------------

Location: ``/db/migrations/``

Naming convention:

.. code-block:: text

   V001__initial_schema.sql
   V002__add_users_table.sql
   V003__add_tax_calculations_table.sql
   V004__add_receipts_table.sql

Running Migrations
------------------

**Development:**

.. code-block:: bash

   # Run all pending migrations
   flyway migrate

**Staging:**

.. code-block:: bash

   # Test migration on staging first
   flyway -url=jdbc:postgresql://staging-db/tms migrate

**Production:**

.. code-block:: bash

   # Require manual confirmation
   flyway -url=jdbc:postgresql://prod-db/tms migrate

Migration Example
-----------------

**File**: ``V005__add_user_role_column.sql``

.. code-block:: sql

   -- Add role column to users table
   ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user' NOT NULL;

   -- Add constraint
   ALTER TABLE users ADD CONSTRAINT check_user_role 
     CHECK (role IN ('user', 'admin', 'system_admin'));

   -- Create index
   CREATE INDEX idx_users_role ON users(role);

   -- Backfill existing users
   UPDATE users SET role = 'user' WHERE role IS NULL;

Rolling Back Migrations
-----------------------

Production migrations are forward-only. To rollback:

**Option 1: Create compensating migration**

.. code-block:: sql

   -- V006__remove_user_role_column.sql
   ALTER TABLE users DROP COLUMN role;

**Option 2: Restore from backup**

See :doc:`05-backup-restore` for backup restoration procedures.

Migration Checklist
-------------------

Before running production migration:

1. [ ] Migration tested on development
2. [ ] Migration tested on staging
3. [ ] Migration is backwards-compatible (if possible)
4. [ ] Data migration tested with production-like volume
5. [ ] Rollback plan documented
6. [ ] Database backup completed within last 24 hours
7. [ ] Maintenance window scheduled
8. [ ] DBA notified and available
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all database reST files
rstcheck docs/source/database/*.rst
```

**Expected output:** No errors

### SQL Syntax Validation

```bash
# Validate SQL in code blocks (if linter available)
sqlfluff lint docs/source/database/*.rst --dialect postgres
```

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

---

## Examples Reference

See working example: `02-examples/database-example/` (to be created)

**Example includes:**
- Complete database documentation
- ERD diagram
- Table definitions
- Migration examples

---

## Access Level Warning

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains sensitive database schema details.
   Do not share with external parties.
```

---

## Agent Checklist

Before marking database documentation complete, verify:

- [ ] Database index created
- [ ] Schema overview with ERD diagram
- [ ] All tables documented with columns and constraints
- [ ] Index strategy documented
- [ ] Migration procedures documented
- [ ] Backup and recovery procedures documented
- [ ] ERD diagram created in diagrams.net
- [ ] ERD exported as PNG and embedded
- [ ] All SQL syntax validated
- [ ] Access level warnings included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Tables used appropriately for column definitions

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial database documentation canon
- Based on PostgreSQL best practices
- Follows `_docs-canon.md` v4 specifications

# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reported that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys.

That parity gap is now closed in current pg-delta. The refreshed pg-delta tree
extracts temporal constraint metadata, compares it in table diffs, and has
PostgreSQL 18 integration coverage for temporal primary keys and foreign keys.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#182](https://github.com/supabase/pg-toolbelt/issues/182) is closed, and
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213) is merged.

## Reproduction SQL

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE SCHEMA test_schema;

CREATE TABLE test_schema.contacts (
    id uuid NOT NULL,
    name text NOT NULL,
    valid_period tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)'),
    PRIMARY KEY (id, valid_period)
);

CREATE TABLE test_schema.conversations (
    id uuid NOT NULL,
    contact_id uuid NOT NULL,
    valid_period tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)'),
    PRIMARY KEY (id, valid_period),
    FOREIGN KEY (contact_id, valid_period)
      REFERENCES test_schema.contacts (id, valid_period)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.contacts
  DROP CONSTRAINT contacts_pkey;
ALTER TABLE test_schema.contacts
  ADD CONSTRAINT contacts_pkey
  PRIMARY KEY (id, valid_period WITHOUT OVERLAPS);

ALTER TABLE test_schema.conversations
  DROP CONSTRAINT conversations_contact_id_valid_period_fkey;
ALTER TABLE test_schema.conversations
  ADD CONSTRAINT conversations_contact_id_valid_period_fkey
  FOREIGN KEY (contact_id, PERIOD valid_period)
  REFERENCES test_schema.contacts (id, PERIOD valid_period);
```

## How pgschema handled it

pgschema PR #365 extracted the temporal flag from `pg_constraint`, preserved it
in the constraint representation, and re-emitted `WITHOUT OVERLAPS` and
`PERIOD` in generated DDL.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ current table model extracts `is_temporal` |
| Table diff treats temporal vs non-temporal constraints as changes | ✅ `src/core/objects/table/table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 temporal PK coverage | ✅ `tests/integration/constraint-operations.test.ts` |
| PostgreSQL 18 temporal FK coverage | ✅ `tests/integration/constraint-operations.test.ts` |
| Catalog-model coverage for temporal constraint definitions | ✅ `tests/integration/catalog-model.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed, PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped temporal constraint syntax | Same parity gap existed originally |
| **Current fix** | Extract and preserve the temporal flag | Extract `is_temporal`, diff it, and preserve temporal constraint definitions |
| **Regression coverage** | PG18 fixtures upstream | PG18 integration and catalog-model coverage in pg-delta |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed pg-delta
snapshot.

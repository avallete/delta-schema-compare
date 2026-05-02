# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reported that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys in generated plan and dump
output.

That gap is now also fixed in pg-delta. The current pg-delta tree extracts a
temporal flag from `pg_constraint`, compares it in table-constraint diffs, and
ships PostgreSQL 18 integration coverage for temporal primary-key and
foreign-key scenarios.

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

pgschema PR #365 added temporal constraint support by extracting
`conperiod` from `pg_constraint` through `to_jsonb(c) ->> 'conperiod'`, which
keeps the catalog query backward-compatible on PostgreSQL 14-17 where the
column does not exist. The value is mapped to a constraint-level temporal flag
and then used by the diff and plan layers to emit `WITHOUT OVERLAPS` for
primary/unique constraints and `PERIOD` for foreign keys.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ `table.model.ts` now records `is_temporal` via `to_jsonb(c) ->> 'conperiod'` |
| Temporal flag in table constraint schema | ✅ Present in `tableConstraintPropsSchema` |
| Diff detects regular ↔ temporal constraint transition | ✅ `table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 included in test matrix | ✅ `tests/constants.ts` includes PG 18 |
| Integration test for temporal PK/FK scenarios | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

Current integration coverage includes:

- `convert primary key to temporal primary key`
- `add temporal foreign key constraint`
- `convert related PK and FK to temporal together`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads temporal metadata from `pg_constraint.conperiod` safely across PG versions | Now does the same via `to_jsonb(c) ->> 'conperiod'` |
| **Internal representation** | Tracks a temporal constraint flag in IR | Tracks `is_temporal` in table constraints |
| **Diff behavior** | Compares temporal vs non-temporal constraints explicitly | Now compares the temporal flag and recreates constraints when needed |
| **Coverage** | Has PG18 regression fixtures for temporal PK/FK creation | Has PG18 roundtrip integration coverage for temporal PK/FK transitions |

## Resolution in pg-delta

This benchmark gap is solved in current pg-delta.

Evidence in the refreshed submodule:

- `src/core/objects/table/table.model.ts`
- `src/core/objects/table/table.diff.ts`
- `tests/constants.ts`
- `tests/integration/constraint-operations.test.ts`

The benchmark entry is retained as historical context only.

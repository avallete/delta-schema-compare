# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reported that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys in generated plan and dump
output.

That gap is now closed in current pg-delta. The table constraint model extracts
an `is_temporal` flag from `pg_constraint`, the table diff compares it, the
constraint serializer reuses `pg_get_constraintdef(...)`, and the integration
suite exercises temporal primary-key and foreign-key roundtrips on PostgreSQL
18.

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
`conperiod` from `pg_constraint` through `to_jsonb(c) ->> 'conperiod'`,
propagating the value through its constraint IR, and re-emitting
`WITHOUT OVERLAPS` / `PERIOD` during diff and plan generation.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ Present in `src/core/objects/table/table.model.ts` as `is_temporal` |
| Temporal flag in table constraint schema | ✅ Present |
| Diff detects regular ↔ temporal constraint transition | ✅ `table.diff.ts` compares `is_temporal` |
| Add-constraint serialization preserves temporal definition | ✅ `AlterTableAddConstraint` reuses `constraint.definition` |
| PostgreSQL 18 included in test matrix | ✅ `tests/constants.ts` includes PG18 in the alpine matrix |
| Integration test for temporal PK/FK scenarios | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#182](https://github.com/supabase/pg-toolbelt/issues/182) / [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

**Current source / test evidence:**

- `src/core/objects/table/table.model.ts` extracts
  `is_temporal: coalesce((to_jsonb(c)->>'conperiod')::boolean, false)`
- `src/core/objects/table/table.diff.ts` includes
  `mainC.is_temporal !== branchC.is_temporal` in constraint change detection
- `tests/integration/constraint-operations.test.ts` contains:
  - `convert primary key to temporal primary key`
  - `add temporal foreign key constraint`
  - `convert related PK and FK to temporal together`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads `conperiod` safely across PG versions | Uses the same `to_jsonb(c)->>'conperiod'` pattern |
| **Internal representation** | Tracks a temporal constraint flag | Tracks `is_temporal` on table constraints |
| **Diff behavior** | Treats temporal vs non-temporal constraints as a semantic change | Same |
| **Coverage** | Merged regression fixtures | Merged PG18 integration coverage |

## Latest refresh note (2026-05-01)

This benchmark entry is now solved in current pg-delta at
`repos/pg-toolbelt@c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`, via
[pg-toolbelt#182](https://github.com/supabase/pg-toolbelt/issues/182) and
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213).

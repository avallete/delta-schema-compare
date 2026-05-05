# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reports that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys in generated plan and dump
output. That changes the constraint semantics even though the emitted DDL still
looks superficially valid.

pgschema fixed this in PR #365 by reading `pg_constraint.conperiod`,
propagating a temporal flag through its constraint IR, and re-emitting
`WITHOUT OVERLAPS` / `PERIOD` in its diff and plan paths.

This benchmark entry is historical now: current pg-delta implements and tests
the same temporal-constraint behavior. The related pg-toolbelt issue
[#182](https://github.com/supabase/pg-toolbelt/issues/182) is closed, and
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213) merged the
necessary PG18 model/diff support plus integration coverage.

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

The merged PR also added concrete regression coverage in
`repos/pgschema/testdata/diff/create_table/add_pk/` and
`repos/pgschema/testdata/diff/create_table/add_fk/`, including
`PRIMARY KEY (id, valid_period WITHOUT OVERLAPS)` and
`FOREIGN KEY (product_id, PERIOD adjustment_period) ...`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ `src/core/objects/table/table.model.ts` stores `is_temporal` via `coalesce((to_jsonb(c)->>'conperiod')::boolean, false)` |
| Diff detects regular ↔ temporal transitions | ✅ `src/core/objects/table/table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 included in the integration matrix | ✅ `tests/constants.ts` includes PostgreSQL 18 |
| Temporal primary key regression | ✅ `tests/integration/constraint-operations.test.ts` has `"convert primary key to temporal primary key"` |
| Temporal foreign key regression | ✅ Same file has `"add temporal foreign key constraint"` |
| Coupled PK/FK transition regression | ✅ Same file has `"convert related PK and FK to temporal together"` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Missing temporal metadata in diff / dump output | Same historical gap |
| **Current catalog model** | Tracks temporal constraint state | Tracks `is_temporal` in table constraints |
| **Current regression coverage** | Fixture coverage in pgschema | PG18 integration coverage for PK, FK, and combined transitions |

## Resolution in pg-delta

This benchmark entry is retained as historical context, but the parity gap is
now solved in the current pg-delta snapshot.

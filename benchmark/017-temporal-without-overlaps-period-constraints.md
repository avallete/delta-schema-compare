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

pg-delta now matches that behavior in the current upstream snapshot. The table
constraint catalog model exposes `is_temporal`, the diff logic compares it, and
the integration test suite now includes PostgreSQL 18 temporal primary-key and
foreign-key roundtrips. The original pg-toolbelt tracker
[#182](https://github.com/supabase/pg-toolbelt/issues/182) is closed and the
fix landed in merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213).

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
  DROP CONSTRAINT conversations_pkey;

ALTER TABLE test_schema.conversations
  ADD CONSTRAINT conversations_pkey
  PRIMARY KEY (id, valid_period WITHOUT OVERLAPS);

ALTER TABLE test_schema.conversations
  DROP CONSTRAINT conversations_contact_id_valid_period_fkey;

ALTER TABLE test_schema.conversations
  ADD CONSTRAINT conversations_contact_id_valid_period_fkey
  FOREIGN KEY (contact_id, PERIOD valid_period)
  REFERENCES test_schema.contacts (id, PERIOD valid_period);
```

**Expected:** pg-delta detects that the PK and FK definitions changed and emits
the necessary drop/recreate DDL preserving `WITHOUT OVERLAPS` and `PERIOD`.

**Current pg-delta behavior:** the refreshed upstream snapshot does exactly
that. Temporal metadata is extracted from `pg_constraint`, preserved in the
table-constraint model, compared in diffing, and validated end-to-end in the
PG18 integration suite.

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
| Temporal flag extracted from `pg_constraint` | ✅ `src/core/objects/table/table.model.ts` exposes `is_temporal` |
| Temporal flag in table constraint schema | ✅ `tableConstraintPropsSchema` includes `is_temporal` |
| Diff detects regular ↔ temporal constraint transition | ✅ `src/core/objects/table/table.diff.ts` compares `is_temporal` |
| Add-constraint serialization can preserve PG catalog definition | ✅ `definition` is captured from `pg_get_constraintdef(c.oid, true)` |
| PostgreSQL 18 included in test matrix | ✅ `tests/constants.ts` includes PostgreSQL 18 |
| Integration test for temporal PK/FK scenarios | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ Fixed by issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) / PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads temporal metadata from `pg_constraint.conperiod` safely across PG versions | Reads temporal metadata via `to_jsonb(c)->>'conperiod'` in the table extractor |
| **Internal representation** | Tracks a temporal constraint flag in IR | Tracks `is_temporal` in the table constraint model |
| **Diff behavior** | Compares temporal vs non-temporal constraints explicitly | Compares temporal vs non-temporal constraints explicitly in `table.diff.ts` |
| **Coverage** | Has PG18 regression fixtures for temporal PK/FK creation | Has PG18 integration regressions in `constraint-operations.test.ts` |

## Resolution in pg-delta

pg-delta now preserves temporal constraint semantics end-to-end:

1. `src/core/objects/table/table.model.ts` extracts `is_temporal` from
   `pg_constraint`.
2. `src/core/objects/table/table.diff.ts` treats temporal vs non-temporal
   constraints as a drop/recreate change.
3. `tests/constants.ts` includes PostgreSQL 18 in the integration matrix.
4. `tests/integration/constraint-operations.test.ts` covers:
   - converting a regular primary key to a temporal primary key,
   - adding a temporal foreign key, and
   - converting related PK/FK constraints to temporal forms together.

This benchmark entry is therefore retained as historical context, but the parity
gap is now solved in the current pg-delta snapshot.

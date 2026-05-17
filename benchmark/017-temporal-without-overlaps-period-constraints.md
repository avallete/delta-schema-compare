# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reports that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys in generated plan and dump
output.

Those clauses are semantic, not decorative. Dropping them weakens temporal
uniqueness and containment guarantees even though the emitted DDL still looks
plausible.

Refresh note (2026-05-16): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#182](https://github.com/supabase/pg-toolbelt/issues/182)
is closed, and
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213) added the
temporal constraint model changes plus PG18 integration coverage.

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

## How pgschema handled it

pgschema PR #365 added temporal constraint support by extracting `conperiod`
through a version-safe `to_jsonb(c) ->> 'conperiod'` pattern, carrying the flag
through the constraint IR, and re-emitting `WITHOUT OVERLAPS` / `PERIOD` in
diff and plan output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ Present in `src/core/objects/table/table.model.ts` as `is_temporal` |
| Temporal flag preserved in table constraint schema | ✅ Present |
| Diff detects regular ↔ temporal constraint transition | ✅ `table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 temporal scenarios covered in integration tests | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

Current local pg-delta now includes PG18-specific integration cases that assert
the exact clauses which used to be missing:

- `PRIMARY KEY (... WITHOUT OVERLAPS)`
- `FOREIGN KEY (..., PERIOD ...) REFERENCES ... (..., PERIOD ...)`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Temporal metadata not carried through diff / plan layers | Same class of missing temporal metadata and diff comparison |
| **Current fix** | Read `conperiod`, propagate a temporal flag, re-emit temporal syntax | Store `is_temporal` on table constraints and treat temporal changes as semantic diffs |
| **Regression coverage** | PG18 fixtures for temporal PK/FK cases | PG18 integration coverage in the constraint suite |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the current pg-delta
snapshot. The benchmark now serves as historical context for why temporal
constraint metadata is modeled explicitly instead of inferred from the rendered
definition.

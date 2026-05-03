# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reports that PostgreSQL 18 temporal constraints were
being silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal
primary keys and `PERIOD` was dropped from temporal foreign keys.

pg-delta used to lack the temporal constraint metadata and regression
coverage required to prove parity here, so this benchmark tracked the gap
through pg-toolbelt issue
[#182](https://github.com/supabase/pg-toolbelt/issues/182).

Refresh note (2026-05-03): pg-delta now models temporal constraints,
includes PostgreSQL 18 in its default integration matrix, and has focused
regression coverage. Issue
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

## How pgschema handled it

pgschema PR #365 reads temporal metadata from `pg_constraint.conperiod`,
propagates it through the constraint IR, and re-emits `WITHOUT OVERLAPS`
/ `PERIOD` during diff and plan generation.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ `src/core/objects/table/table.model.ts` reads `coalesce((to_jsonb(c)->>'conperiod')::boolean, false)` into `is_temporal` |
| Table constraint diff treats regular <-> temporal as a change | ✅ `src/core/objects/table/table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 in the default integration matrix | ✅ `tests/constants.ts` includes `18` in `POSTGRES_VERSIONS` |
| Integration regression coverage | ✅ `tests/integration/constraint-operations.test.ts` covers temporal PK/FK creation and conversion; `tests/integration/catalog-model.test.ts` asserts extraction |
| Existing pg-toolbelt issue / PR | ✅ [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed, [#213](https://github.com/supabase/pg-toolbelt/pull/213) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Temporal metadata was not preserved through diff / plan | Same parity question originally existed |
| **Current fix** | Extracts `conperiod` safely and carries it through IR | Extracts `is_temporal`, compares it in table diffing, and tests PG18 temporal constraint roundtrips |
| **Regression coverage** | PG18 fixtures upstream | PG18 integration coverage in pg-delta |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta preserves
`WITHOUT OVERLAPS` and `PERIOD`, includes PostgreSQL 18 in the default test
matrix, and exercises temporal constraint roundtrips in integration tests.

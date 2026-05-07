# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed),
> fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reports that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` disappeared from temporal primary keys
and `PERIOD` disappeared from temporal foreign keys.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#182](https://github.com/supabase/pg-toolbelt/issues/182)
is closed, and
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213) merged the
required extractor, diff, and integration coverage. Current pg-delta now
includes PostgreSQL 18 in its default integration matrix and exercises both
temporal constraint extraction and temporal roundtrips.

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

pgschema fixed the issue by extracting the temporal bit from `pg_constraint`,
propagating it through its constraint IR, and re-emitting `WITHOUT OVERLAPS` /
`PERIOD` during diff and plan output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ✅ `table.model.ts` now exposes `is_temporal` |
| Diff detects regular ↔ temporal constraint transitions | ✅ `table.diff.ts` compares `is_temporal` |
| PostgreSQL 18 present in the default integration matrix | ✅ `tests/constants.ts` now includes PG18 |
| Integration coverage for temporal PK/FK scenarios | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Catalog extraction coverage for temporal constraints | ✅ Present in `tests/integration/catalog-model.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

Current integration coverage includes:

- `convert primary key to temporal primary key`
- `add temporal foreign key constraint`
- `convert related PK and FK to temporal together`
- `extract temporal table constraints`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped temporal modifiers from extracted constraints | Same class of missing temporal metadata/diffing |
| **Current fix** | Extracts and propagates temporal constraint state | Extracts `is_temporal`, compares it in the table diff, and tests PG18 roundtrips end-to-end |
| **Coverage** | Fixed upstream | PG18 extraction + integration coverage on current `main` |

## Resolution in pg-delta

The current pg-delta snapshot now handles the temporal constraint scenarios that
motivated pgschema #364. This benchmark entry remains as historical context and
is no longer an active parity gap.

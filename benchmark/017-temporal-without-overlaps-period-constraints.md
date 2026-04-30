# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

PostgreSQL 18 temporal constraints are not decorative syntax. `WITHOUT
OVERLAPS` on a primary / unique key and `PERIOD` on a foreign key change
actual integrity semantics for time-ranged data.

pgschema issue #364 covered those clauses being silently dropped. pg-delta
used to miss the same distinction, but it is now fixed by
[pg-toolbelt#213](https://github.com/supabase/pg-toolbelt/pull/213), which
resolved [pg-toolbelt#182](https://github.com/supabase/pg-toolbelt/issues/182).

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

pgschema fixed the issue by extracting the temporal flag from
`pg_constraint.conperiod`, carrying it through its IR, and re-emitting the
temporal clauses in dump / diff output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | Yes - `src/core/objects/table/table.model.ts` uses `coalesce((to_jsonb(c)->>'conperiod')::boolean, false)` |
| Temporal flag stored in the table-constraint schema | Yes - `tableConstraintPropsSchema` includes `is_temporal` |
| Diff detects regular -> temporal transitions | Yes - `src/core/objects/table/table.diff.ts` compares `mainC.is_temporal` and `branchC.is_temporal` |
| Unit coverage for the metadata-driven diff | Yes - `altered temporal constraint metadata triggers drop+add` in `table.diff.test.ts` |
| PostgreSQL 18 included in the integration matrix | Yes - `tests/constants.ts` lists 18 |
| Integration tests for temporal PK / FK scenarios | Yes - `tests/integration/constraint-operations.test.ts` includes `convert primary key to temporal primary key`, `add temporal foreign key constraint`, and `convert related PK and FK to temporal together` |
| Existing pg-toolbelt issue / PR | Yes - issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Temporal metadata was not preserved through diff / plan output | Same |
| Current upstream state | Fixed in merged PR #365 | Fixed in merged PR #213 |
| Regression coverage | PG18 regression fixtures | PG18 unit + integration coverage for temporal PK / FK transitions |

## Resolution in pg-delta

pg-delta now tracks temporal constraint metadata explicitly and exercises
the PostgreSQL 18 benchmark scenarios end-to-end. This benchmark entry is
solved in the refreshed snapshot.

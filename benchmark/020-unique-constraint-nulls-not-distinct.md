# `UNIQUE NULLS NOT DISTINCT` on Table Constraints

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being silently downgraded to plain `UNIQUE (...)` during
dump and diff output. That changes constraint semantics: with `NULLS NOT
DISTINCT`, multiple rows whose constrained columns are all `NULL` should
conflict rather than being treated as distinct.

This benchmark originally tracked the table-constraint slice separately from
the already-solved standalone-index slice in
[016](016-unique-index-nulls-not-distinct.md). The key question was whether
pg-delta would detect a change from an existing plain `UNIQUE (a, b)` table
constraint to `UNIQUE NULLS NOT DISTINCT (a, b)` and emit the required
drop + recreate.

## Refresh note (2026-08-11)

This refresh advanced checked-in/live `pg-delta` from
`2929e83981fee139772cc1c60255f1b2592a6f3a` to
`2247de05849455b358fae71bbe514273cae4faba` after the clean-room rewrite
from [pg-toolbelt#299](https://github.com/supabase/pg-toolbelt/pull/299)
landed on `main`; checked-in/live `pgschema` remained
`0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`.

A focused 2026-08-11 pg17 proof probe now emits the exact corrective plan:

```sql
ALTER TABLE "test_schema"."pgschema_repro_nulls"
  DROP CONSTRAINT "pgschema_repro_nulls_uniq";

ALTER TABLE "test_schema"."pgschema_repro_nulls"
  ADD CONSTRAINT "pgschema_repro_nulls_uniq"
  UNIQUE NULLS NOT DISTINCT (a, b);
```

The plan proved cleanly with zero drift, so benchmark 020 now moves to
**Solved in pg-delta**. No exact pg-toolbelt issue or PR was needed for the
fix because the behavior arrived through the new default-branch engine.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
    a integer,
    b integer,
    CONSTRAINT pgschema_repro_nulls_uniq
      UNIQUE (a, b)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  DROP CONSTRAINT pgschema_repro_nulls_uniq;

ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta plans a drop + recreate for the changed table
constraint definition so the roundtrip converges on
`UNIQUE NULLS NOT DISTINCT (a, b)`.

**Actual on current pg-delta:** the exact scenario now converges. The
focused 2026-08-11 probe emitted the two statements above and proved with
zero drift.

## How pgschema handled it

pgschema fixed the issue in PR #413 by preserving
`UNIQUE NULLS NOT DISTINCT` for table constraints in both dump and diff
paths. The merged change added dump and diff regression fixtures under
`repos/pgschema/testdata/` and read the necessary PostgreSQL metadata from
the backing constraint/index state.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint extraction preserves the rendered definition | Yes - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` captures `pg_get_constraintdef(con.oid)` as the constraint `def` |
| Diff distinguishes plain `UNIQUE` from `UNIQUE NULLS NOT DISTINCT` table constraints | Yes - the focused 2026-08-11 probe emitted a drop + recreate for the exact toggle scenario |
| Focused proof on the exact benchmark SQL | Yes - pg17 proof succeeded with zero drift |
| Existing exact pg-toolbelt issue / PR | No exact tracker needed |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog / IR representation** | Preserves the table-constraint modifier after the resolved fix | Current engine preserves enough of the rendered constraint definition to detect the change |
| **Plan / SQL emission** | Emits the modifier in dump + diff output | Current engine now emits the required drop + recreate with `UNIQUE NULLS NOT DISTINCT` |
| **Current parity state** | Fixed | Covered |

## Plan to handle it in pg-delta

1. No additional engine change is currently required for the exact table-
   constraint toggle scenario.
2. A focused committed regression under `packages/pg-delta/tests/` would
   still be valuable to lock this exact behavior in place across future
   planner refactors.

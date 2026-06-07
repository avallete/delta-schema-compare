# `UNIQUE NULLS NOT DISTINCT` on Table Constraints

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being silently downgraded to plain `UNIQUE (...)` during dump
output. That changes constraint semantics: with `NULLS NOT DISTINCT`, multiple
rows whose constrained columns are all `NULL` should conflict rather than being
treated as distinct.

Current pg-delta already supports `NULLS NOT DISTINCT` for standalone unique
indexes, and benchmark [016](016-unique-index-nulls-not-distinct.md) tracks that
now-solved parity path. The table-constraint path is separate, though: it uses
the table constraint model and `ALTER TABLE ... ADD CONSTRAINT ...` DDL, not
the standalone index model. During this refresh, there is still no exact
pg-delta coverage for the table-constraint form from pgschema #412.

This matters because the downgrade is silent. A migration plan that emits
`UNIQUE (a, b)` instead of `UNIQUE NULLS NOT DISTINCT (a, b)` looks plausible,
but it weakens uniqueness semantics for nullable columns.

## Refresh note (2026-06-07)

pg-delta advanced from `b9b8b157c23e08e9d8a9c7573718edcc06f603c3` to
`f95e0a8b773539dfb60ebf541131ab9feba4a525` during this refresh. The new
upstream work includes policy dependency fixes, but it does not change this
benchmark's parity state.

A focused unit-level diff probe against the current table-constraint path still
reported zero planned changes when only the definition changed from
`UNIQUE (a, b)` to `UNIQUE NULLS NOT DISTINCT (a, b)`, confirming that the
modifier is still ignored in the table-constraint diff logic.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
    a integer,
    b integer
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta emits
`ALTER TABLE ... ADD CONSTRAINT ... UNIQUE NULLS NOT DISTINCT (a, b)` and the
roundtrip converges.

**Actual:** current pg-delta has explicit coverage only for the standalone
unique-index form. The table-constraint model does not expose a dedicated
`nulls_not_distinct` field, `table.diff.ts` does not compare the full rendered
constraint definition, and `constraint-operations.test.ts` has no regression
for this exact scenario.

## How pgschema handled it

pgschema fixed the issue in PR #413 by preserving
`UNIQUE NULLS NOT DISTINCT` for table constraints in both dump and diff paths.
The merged change added:

- dump regression coverage in
  `repos/pgschema/testdata/dump/issue_412_unique_nulls_not_distinct/`
- diff regression coverage in
  `repos/pgschema/testdata/diff/create_table/add_unique_constraint_nulls_not_distinct/`
- constraint inspection logic that safely reads the PostgreSQL 15+
  `indnullsnotdistinct` metadata through a version-safe `to_jsonb(...)` path

## Current pg-delta status

| Aspect | Status |
|---|---|
| Standalone unique index `NULLS NOT DISTINCT` support | Yes - covered in `src/core/objects/index/` and `tests/integration/index-operations.test.ts` |
| Table constraint extraction exposes `nulls_not_distinct` | No - the table constraint JSON in `src/core/objects/table/table.model.ts` does not include it |
| Constraint diff compares `NULLS NOT DISTINCT` on table constraints | No - `src/core/objects/table/table.diff.ts` compares structured fields but not the full rendered definition |
| Constraint `definition` is captured from the catalog | Yes - `pg_get_constraintdef(c.oid, true)` is stored on the table constraint model |
| Integration regression for `UNIQUE NULLS NOT DISTINCT` table constraints | No - `tests/integration/constraint-operations.test.ts` only covers plain `UNIQUE (...)` |
| Existing pg-toolbelt issue / PR for this exact scenario | No - none found during the 2026-06-05 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads `NULLS NOT DISTINCT` for table constraints | Reads it for standalone indexes only |
| **Internal representation** | Tracks the modifier through constraint inspection | Table constraint model does not expose the modifier |
| **Coverage** | Dump + diff fixtures for the table-constraint scenario | Integration tests only for the standalone index scenario |
| **Current parity state** | Fixed | Not covered |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so table constraints expose whether the backing constraint is
   `NULLS NOT DISTINCT`, likely by reading the backing index metadata from
   `c.conindid` in a PostgreSQL-version-safe way.
2. Add the new field to `tableConstraintPropsSchema` and preserve it through
   the table object model.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so a plain `UNIQUE` and `UNIQUE NULLS NOT DISTINCT` are treated as different
   constraints that require drop/recreate.
4. Ensure `ALTER TABLE ... ADD CONSTRAINT` serialization preserves the modifier
   when creating the branch-side constraint.
5. Add a PostgreSQL 15+ roundtrip regression to
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for the exact table-constraint scenario above.

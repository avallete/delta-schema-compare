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

## Refresh note (2026-08-04)

This refresh kept the checked-in `pg-delta` baseline at
`a974b83fc044788caa4ca538d112b62d1873843b` while live
`pg-toolbelt/main` advanced to `2929e83981fee139772cc1c60255f1b2592a6f3a`;
`pgschema` remained at `325dac205047a7850a52ee9f9ff35ec18c145dcc`.

The new live pg-delta delta is the alpha.5 `pg-topo` byte-offset parser fix
from [pg-toolbelt#372](https://github.com/supabase/pg-toolbelt/pull/372),
released by [pg-toolbelt#374](https://github.com/supabase/pg-toolbelt/pull/374).
A focused live pg17 plan probe for this exact benchmark still produced **zero
planned changes** when toggling an existing plain `UNIQUE` table constraint to
`UNIQUE NULLS NOT DISTINCT`, so the table-constraint diff gap remains
unresolved. Direct duplicate searches still found no exact pg-toolbelt issue or
PR for this scenario, so benchmark 020 remains **Not covered**.

## Refresh note (2026-07-18)

This refresh advanced the checked-in `pg-delta` baseline from
`ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` to
`c0decd173d191bc470bf7b8c8dd3e862f08ae398`, while `pgschema` remained at
`e18d9ede7973537919c02f25eced5c97271af1dc`.

The new pg-delta delta is the alpha.32 non-superuser extraction fix
(`pg_user_mappings`, redacted `subconninfo`, and related tests), so it does
not touch the table-constraint extraction or diff path behind this benchmark.
Targeted duplicate searches still found no exact pg-toolbelt issue or PR for
this scenario, so benchmark 020 remains **Not covered**.

## Refresh note (2026-07-08)

This refresh advanced both checked-in submodules:

- `pg-delta` from `9284412d71635308ebb0c1537e0b0183d2cfa4da` to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `pgschema` from `62d09975eaac726f055aa62a5baa2961ef7e5a83` to
  `e18d9ede7973537919c02f25eced5c97271af1dc`

The newer upstream pgschema head adds merged fixes for issues #505, #506, #508,
and #509, but none of those change this exact table-constraint scenario.

During this refresh, a focused local diff probe against the new pg-delta head
showed the same asymmetric behavior more clearly:

- creating a brand-new `UNIQUE NULLS NOT DISTINCT` table constraint still works
- toggling an existing plain `UNIQUE (a, b)` constraint to
  `UNIQUE NULLS NOT DISTINCT (a, b)` still produces **zero planned changes**

That means the active parity gap is specifically the **alter / replacement**
path for table constraints, not initial creation. There is still no exact
pg-toolbelt issue or PR for this table-constraint toggle scenario, so benchmark
020 remains active alongside benchmarks 021, 022, and the newly promoted
[023](023-fk-before-standalone-unique-index.md).

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

**Actual:** current pg-delta treats the existing plain `UNIQUE` and the target
`UNIQUE NULLS NOT DISTINCT` constraint as equivalent and emits **no changes**.
The initial-create path is fine, but the diff path still ignores the modifier
when the constraint already exists.

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
| Create a brand-new `UNIQUE NULLS NOT DISTINCT` table constraint | Yes - `AlterTableAddConstraint.serialize()` preserves the modifier when the branch-side constraint already has it |
| Table constraint extraction exposes `nulls_not_distinct` | No - the table constraint JSON in `src/core/objects/table/table.model.ts` does not include it |
| Constraint diff compares `NULLS NOT DISTINCT` on table constraints | No - `src/core/objects/table/table.diff.ts` compares structured fields but not the full rendered definition |
| Constraint `definition` is captured from the catalog | Yes - `pg_get_constraintdef(c.oid, true)` is stored on the table constraint model |
| Integration regression for `UNIQUE NULLS NOT DISTINCT` table constraints | No - `tests/integration/constraint-operations.test.ts` only covers plain `UNIQUE (...)` |
| Existing pg-toolbelt issue / PR for this exact scenario | No - none found through the 2026-07-18 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads `NULLS NOT DISTINCT` for table constraints | Reads it for standalone indexes only |
| **Internal representation** | Tracks the modifier through constraint inspection | Table constraint model does not expose the modifier |
| **Coverage** | Dump + diff fixtures for the table-constraint scenario | Initial create path works, but there is still no regression for the existing-constraint toggle |
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

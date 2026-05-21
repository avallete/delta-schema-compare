# Table constraint `UNIQUE NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were dumped as plain `UNIQUE (...)`, silently dropping the
PostgreSQL 15+ modifier that makes `NULL` values conflict for uniqueness
purposes.

pgschema fixed that in PR #413 by reading the PG15+ metadata from the backing
unique index and preserving the clause in dump and diff output.

Current pg-delta already solves the **index** variant of this feature
(benchmark [016](016-unique-index-nulls-not-distinct.md)), but the
**table-constraint** path still does not model the modifier. The table
constraint extractor in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
captures `definition`, `deferrable`, `no_inherit`, `is_temporal`, key columns,
and other fields, but there is no table-constraint `nulls_not_distinct` flag.
`table.diff.ts` compares those scalar fields and column lists, yet it never
compares the full rendered constraint definition. That means a same-name
constraint changing from `UNIQUE (a, b)` to
`UNIQUE NULLS NOT DISTINCT (a, b)` can be treated as unchanged.

This matters because the modifier changes data semantics, not formatting. A
plain UNIQUE constraint allows multiple rows that differ only by `NULL`
placement; `UNIQUE NULLS NOT DISTINCT` rejects them.

## Reproduction SQL

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.repro_nulls (
    a integer,
    b integer,
    CONSTRAINT repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.repro_nulls
  DROP CONSTRAINT repro_nulls_uniq;

ALTER TABLE test_schema.repro_nulls
  ADD CONSTRAINT repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the semantic change and emits a drop / recreate
that preserves `NULLS NOT DISTINCT`.

**Actual:** current pg-delta can preserve the clause on a pure add-constraint
path because `AlterTableAddConstraint` reuses `constraint.definition`, but it
does not model the modifier as a first-class table-constraint property. A
same-name constraint toggle can therefore be diffed as unchanged.

## How pgschema handled it

pgschema PR #413 uses a PostgreSQL-version-safe `to_jsonb(...)` extraction to
read `indnullsnotdistinct` from the backing unique index, maps that into the
constraint representation, and re-emits `NULLS NOT DISTINCT` during dump / diff
output.

The upstream fix is backed by explicit regression artifacts:

- `repos/pgschema/testdata/dump/issue_412_unique_nulls_not_distinct/raw.sql`
- `repos/pgschema/testdata/diff/create_table/add_unique_constraint_nulls_not_distinct/`

Those fixtures preserve:

```sql
ALTER TABLE pgschema_repro_nulls
ADD CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b);
```

## Current pg-delta status

| Aspect | Status |
|---|---|
| Index variant (`CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`) | ✅ Solved separately in benchmark [016](016-unique-index-nulls-not-distinct.md) |
| Table-constraint model exposes `nulls_not_distinct` | ❌ Missing from `src/core/objects/table/table.model.ts` |
| Table diff compares `NULLS NOT DISTINCT` state | ❌ `src/core/objects/table/table.diff.ts` does not compare this modifier or the full rendered definition |
| Add-constraint serializer can emit the clause when present | ⚠️ Partial — `AlterTableAddConstraint` reuses `constraint.definition` |
| Integration coverage for table-level `UNIQUE NULLS NOT DISTINCT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found in the live sweep for this refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Dump / diff lost the PG15+ modifier on table constraints | Table-constraint model never records the modifier, so semantic toggles are invisible |
| **Fix approach** | Read backing-index metadata and re-emit the clause | Add a modeled flag for table constraints and compare it during diff |
| **Regression coverage** | Dedicated dump and diff fixtures | Index-only coverage today; no table-constraint regression |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   to read the PG15+ `indnullsnotdistinct` flag from the backing unique index
   (`c.conindid`) using a PostgreSQL-version-safe `to_jsonb(...)` expression.
2. Add the new field to `tableConstraintPropsSchema` and preserve it through the
   table object model.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so plain `UNIQUE` vs `UNIQUE NULLS NOT DISTINCT` becomes a semantic
   drop/recreate change.
4. Add integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for both create-only and toggle cases.

# Table-level `UNIQUE NULLS NOT DISTINCT` constraints

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being dumped without the `NULLS NOT DISTINCT` modifier. That
silently weakens uniqueness semantics for rows containing `NULL` values.

pg-delta already has explicit coverage for the related standalone-index case
(benchmark item 016), but the table-constraint path is different. Table
constraints are diffed in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`,
and the current change-detection logic does not compare either the full
constraint `definition` or a dedicated `nulls_not_distinct` flag for table
constraints.

That means a live schema with:

```sql
CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
```

and a desired schema with:

```sql
CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b)
```

can look unchanged to pg-delta if the constraint name and key columns stay the
same. The add-constraint serializer already reuses the catalog definition
verbatim, so create-from-scratch flows are likely fine; the unresolved parity
gap is detecting modifier-only changes on existing named table constraints.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
    a integer,
    b integer,
    CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
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

**Expected:** pg-delta detects the modifier change and emits a drop/recreate
for the named constraint so the target database preserves `NULLS NOT DISTINCT`.

**Actual:** current table-constraint diffing does not compare the modifier, so
the regular unique constraint and the `NULLS NOT DISTINCT` variant can appear
equivalent when the key columns are unchanged.

## How pgschema handled it

pgschema fixed the issue in PR #413 and added both diff and dump regressions:

- `repos/pgschema/testdata/diff/create_table/add_unique_constraint_nulls_not_distinct/`
- `repos/pgschema/testdata/dump/issue_412_unique_nulls_not_distinct/`

The fix preserves the modifier in emitted DDL:

```sql
ADD CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b);
```

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint definition extracted from catalog | ✅ `src/core/objects/table/table.model.ts` stores `definition` via `pg_get_constraintdef(c.oid, true)` |
| Add-constraint serializer preserves captured definition | ✅ `src/core/objects/table/changes/table.alter.ts` emits `ADD CONSTRAINT ... ${this.constraint.definition}` |
| Diff detects `UNIQUE` ↔ `UNIQUE NULLS NOT DISTINCT` transitions on same key columns | ❌ `src/core/objects/table/table.diff.ts` does not compare `definition` or a dedicated `nulls_not_distinct` field |
| Integration regression for table-level `UNIQUE NULLS NOT DISTINCT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during the 2026-05-05 refresh |

The relevant diff check currently compares structured fields such as
`constraint_type`, `deferrable`, `initially_deferred`, `no_inherit`,
`is_temporal`, and `key_columns`, but not the full rendered constraint
definition. A modifier-only change on the same named UNIQUE constraint therefore
falls through.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped `NULLS NOT DISTINCT` from table-level UNIQUE constraints | Does not currently diff the modifier for existing named table constraints |
| **Current model** | Explicitly preserves the modifier in dump and diff fixtures | Preserves raw `definition` text for adds, but not in change detection |
| **Regression coverage** | Dedicated diff + dump regressions | Index path covered; table-constraint path still uncovered |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so named table constraints treat `UNIQUE` vs
   `UNIQUE NULLS NOT DISTINCT` as a drop/recreate change.
   - Either compare `definition` for relevant constraint types, or
   - Add an explicit `nulls_not_distinct` field to the table-constraint model.
2. Add PostgreSQL 15+ integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - adding a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling an existing named constraint from plain `UNIQUE` to
     `UNIQUE NULLS NOT DISTINCT`.
3. Keep `AlterTableAddConstraint.serialize()` definition-based so the emitted
   DDL preserves the exact modifier text once the diff detects the change.

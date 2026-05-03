# Table-constraint `UNIQUE NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being dumped without the `NULLS NOT DISTINCT` modifier:

```sql
CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b)
```

was degraded to:

```sql
CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
```

This is distinct from pgschema issue #355 / benchmark 016, which covered
standalone `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`. The index variant
is solved in pg-delta; the table-constraint variant is not yet covered with
the same confidence.

## Reproduction SQL

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
    a integer,
    b integer,
    CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  DROP CONSTRAINT pgschema_repro_nulls_uniq;

ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects that the constraint definition changed and
emits a drop / recreate flow that preserves `NULLS NOT DISTINCT`.

**Actual:** pg-delta stores the rendered constraint definition, but current
table-constraint diffing does not compare `definition` or a dedicated
`nulls_not_distinct` field. A same-named plain unique -> `UNIQUE NULLS NOT
DISTINCT` transition can therefore be treated as unchanged.

## How pgschema handled it

pgschema PR #413 added explicit support for the constraint variant and
backed it with both dump and diff fixtures:

- `repos/pgschema/testdata/dump/issue_412_unique_nulls_not_distinct/`
- `repos/pgschema/testdata/diff/create_table/add_unique_constraint_nulls_not_distinct/`

The fix keeps `NULLS NOT DISTINCT` on table constraints just as pgschema
already did for standalone unique indexes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint extraction stores the rendered definition | ✅ `src/core/objects/table/table.model.ts` captures `pg_get_constraintdef(c.oid, true)` |
| Add-constraint serialization can preserve the clause for brand-new constraints | ✅ `AlterTableAddConstraint` reuses `constraint.definition` |
| Diff detects plain unique -> `UNIQUE NULLS NOT DISTINCT` on the same named constraint | ❌ `src/core/objects/table/table.diff.ts` does not compare `definition` or a constraint-level `nulls_not_distinct` field |
| Index diff can rescue constraint-backed unique indexes | ❌ `src/core/objects/index/index.diff.ts` explicitly skips `is_owned_by_constraint` indexes |
| Integration regression coverage for table-level `UNIQUE NULLS NOT DISTINCT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ❌ None found during the 2026-05-03 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Coverage shape** | Explicitly models the table-constraint modifier and tests both dump + diff | Models the standalone index variant directly, but not the table-constraint variant |
| **Diff semantics** | Preserves `NULLS NOT DISTINCT` on the constraint itself | Constraint diff ignores the rendered definition while index diff skips constraint-owned indexes |
| **Current risk** | Addressed upstream | Potential silent semantic drift when only the constraint modifier changes |

## Plan to handle it in pg-delta

1. Extend `src/core/objects/table/table.diff.ts` so table constraints detect
   `UNIQUE` vs `UNIQUE NULLS NOT DISTINCT` changes. The cleanest options are:
   - add an explicit constraint-level `nulls_not_distinct` field, or
   - compare the canonical `definition` for unique constraints.
2. Add PG15+ integration coverage in
   `tests/integration/constraint-operations.test.ts` for:
   - creating a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling an existing same-named constraint between plain unique and
     `NULLS NOT DISTINCT`.
3. Add focused unit coverage proving the table-constraint path owns this
   semantic diff, because `index.diff.ts` intentionally skips
   constraint-owned indexes.

# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` -> custom enum), PostgreSQL
requires a `USING` clause when no implicit cast exists. If the column also has
an incompatible default, the default must be dropped before the type change
and re-applied afterward.

pgschema originally emitted `ALTER COLUMN ... TYPE ...` without that
default-safe flow. pg-delta used to have the same gap, and this benchmark
originally tracked pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130)
and draft PR [#146](https://github.com/supabase/pg-toolbelt/pull/146).

Refresh note (2026-05-03): pg-delta now covers this scenario. pg-toolbelt
issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) is closed,
the earlier draft PR [#146](https://github.com/supabase/pg-toolbelt/pull/146)
was closed unmerged, and the effective fix landed in merged PR
[#231](https://github.com/supabase/pg-toolbelt/pull/231).

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TYPE test_schema.status AS ENUM ('active', 'inactive', 'archived');

CREATE TABLE test_schema.items (
    id serial PRIMARY KEY,
    state text NOT NULL DEFAULT 'active'
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.items
  ALTER COLUMN state DROP DEFAULT;
ALTER TABLE test_schema.items
  ALTER COLUMN state TYPE test_schema.status USING state::test_schema.status;
ALTER TABLE test_schema.items
  ALTER COLUMN state SET DEFAULT 'active'::test_schema.status;
```

## How pgschema handled it

pgschema added explicit `USING` clause generation for non-implicit casts and
paired it with the default drop / type change / default reapply flow.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | ✅ Present |
| `USING` clause emitted when the type really changes | ✅ `src/core/objects/table/changes/table.alter.ts` appends `USING column::new_type` when `previousColumn.data_type_str` differs |
| Default-safe sequencing around type change | ✅ `src/core/objects/table/table.diff.ts` emits drop-default -> type-with-using -> set-default |
| Integration regression coverage | ✅ `tests/integration/alter-table-operations.test.ts` covers `change column type to enum with default` and a `varchar -> integer` cast path |
| Existing pg-toolbelt issue / PR | ✅ [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed, [#231](https://github.com/supabase/pg-toolbelt/pull/231) merged (`#146` closed unmerged) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Missing `USING` and missing default-safe sequencing | Same |
| **Current fix** | Emits explicit cast flow when needed | Emits the same cast flow and folds default handling into the type-change plan |
| **Regression coverage** | Fixture-backed in the Go repo | Integration coverage in `alter-table-operations.test.ts` |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta emits the
default-safe `ALTER COLUMN TYPE ... USING ...` flow and has end-to-end
regression coverage for the scenario that originally motivated pgschema
issue #190.

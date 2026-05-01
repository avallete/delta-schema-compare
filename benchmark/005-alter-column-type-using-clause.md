# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` to a custom enum),
PostgreSQL may require both a `USING` clause and a default-safe sequence:
drop an incompatible default, perform the cast, then restore the default in the
new type. pgschema previously missed that flow.

This benchmark used to be an active parity gap for pg-delta as well. That is no
longer true in the current upstream state: pg-delta now emits cast-aware
`ALTER COLUMN ... TYPE ... USING ...` SQL and wraps type changes with
default-safe `DROP DEFAULT` / `SET DEFAULT` operations when needed.

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

pgschema fixed the issue by emitting a `USING` cast for non-implicit type
changes and preserving the safe default drop/re-set flow around the cast.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` serializer can add `USING` | ✅ `src/core/objects/table/changes/table.alter.ts` appends `USING column::new_type` when the previous and next types differ |
| Table diff emits default-safe flow around type changes | ✅ `src/core/objects/table/table.diff.ts` emits `DROP DEFAULT` before the type change and `SET DEFAULT` after it when needed |
| Integration test for `text -> enum` with default | ✅ `tests/integration/alter-table-operations.test.ts` has `change column type to enum with default` |
| Integration test for explicit cast to integer | ✅ The same file has `change varchar column type to integer with using cast` |
| Existing pg-toolbelt issue / PR | ✅ [#130](https://github.com/supabase/pg-toolbelt/issues/130) was closed by merged PR [#231](https://github.com/supabase/pg-toolbelt/pull/231) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing cast-aware ALTER flow | Same historical gap |
| **Current state** | Fixed upstream | Fixed upstream |
| **Regression coverage** | Covered by resolved upstream issue | Covered by focused integration tests in `alter-table-operations.test.ts` |

## Plan to handle it in pg-delta

No new parity work is required for this benchmark item. The remaining work is
just to keep the existing regression coverage in place as nearby ALTER COLUMN
logic evolves.

## Latest refresh note (2026-05-01)

This benchmark item moved from "tracked" to "solved" in the 2026-05-01 refresh.
The previous draft PR path was superseded by the merged upstream fix in
[pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231), and the
current submodule revision `c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f` contains
both the serializer fix and the regression tests.

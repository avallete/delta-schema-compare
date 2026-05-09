# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` to a custom enum), PostgreSQL
often requires a `USING` clause. If the column also has a default that no longer
type-checks, the default must be dropped before the type change and then
re-applied afterwards.

pgschema originally missed both pieces of behavior. That parity gap is now
closed in current pg-delta as well: the refreshed `table.alter.ts` serializer
can emit `USING column::new_type`, and `table.diff.ts` wraps type changes in a
default-safe flow when the original column had a default.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#130](https://github.com/supabase/pg-toolbelt/issues/130) is now closed, and
the current pg-delta tree at
`repos/pg-toolbelt@102ef99ae5aabb29510d48b39fbb8ecee34f5458` has both source
support and end-to-end coverage for the pgschema #190 scenario.

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

pgschema fixed the bug by generating the cast expression needed for
non-implicit type changes and by preserving the required drop-default /
re-set-default sequence around the type rewrite.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` emits `USING` when the type actually changes | ✅ `src/core/objects/table/changes/table.alter.ts` |
| Default-safe type-change flow (`DROP DEFAULT` → `TYPE` → `SET DEFAULT`) | ✅ `src/core/objects/table/table.diff.ts` |
| Integration test: `text -> enum` with default | ✅ `tests/integration/alter-table-operations.test.ts` (`"change column type to enum with default"`) |
| Integration test: explicit cast such as `varchar -> integer` | ✅ `tests/integration/alter-table-operations.test.ts` (`"change varchar column type to integer with using cast"`) |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed, original PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) closed |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Missing `USING` and default-safe sequencing | Same parity gap existed originally |
| **Current fix path** | Emit safe cast DDL plus default handling | Emit `USING` from `AlterTableAlterColumnType` and surround with default-safe ALTERs |
| **Regression coverage** | Covered by the upstream fix | Covered by focused integration tests for enum and explicit-cast transitions |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed
pg-delta tree. The benchmark file is retained as historical context, but the
current implementation now matches the behavior pgschema added for issue #190.

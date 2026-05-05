# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` to a custom enum),
PostgreSQL may require a `USING` clause if the cast is not implicit. If the
column also has a default that is incompatible with the new type, the default
must be dropped first and re-set after the type change.

pgschema originally emitted `ALTER COLUMN ... TYPE ...` without the required
`USING` clause and without the default-safe sequencing. That behavior is now
fixed upstream.

This benchmark entry is historical now: current pg-delta covers the same flow.
Notably, the old pg-toolbelt issue
[#130](https://github.com/supabase/pg-toolbelt/issues/130) is closed, and even
though the original implementation PR
[#146](https://github.com/supabase/pg-toolbelt/pull/146) was closed without
merge, the current pg-delta source and integration tests already implement the
required behavior.

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

pgschema added `USING` clause generation for type changes involving custom
types and preserved the default-safe drop / re-set sequence around the cast.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` supports `USING` | ✅ `src/core/objects/table/changes/table.alter.ts` appends `USING column::new_type` when `previousColumn.data_type_str` differs |
| Type-diff logic passes previous column metadata | ✅ `src/core/objects/table/table.diff.ts` constructs `AlterTableAlterColumnType` with `previousColumn: mainCol` |
| `text -> enum` with default regression | ✅ `tests/integration/alter-table-operations.test.ts` has `"change column type to enum with default"` |
| Casted scalar type regression | ✅ Same file has `"change varchar column type to integer with using cast"` |
| Reverse enum -> text with default regression | ✅ Same file has `"change column type from enum to text preserves default"` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) is closed; PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) is closed unmerged, but current behavior is present in source/tests |

The current serializer path now includes:

```typescript
if (hasTypeChangedWithPreviousDefinition) {
  parts.push("USING", `${this.column.name}::${this.column.data_type_str}`);
}
```

That behavior is exercised end-to-end by the integration cases above, including
the default-aware enum casts that originally motivated the benchmark item.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical bug** | Missing `USING` and default-safe sequencing | Same historical gap |
| **Current implementation** | Fixed upstream | Fixed in current source and integration suite |
| **Evidence** | Resolved pgschema issue | Direct source evidence plus multiple roundtrip tests |

## Resolution in pg-delta

This benchmark entry is retained as historical context, but the parity gap is
now solved in the current pg-delta snapshot.

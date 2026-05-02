# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed),
> fixed in pgschema by [#209](https://github.com/pgplex/pgschema/pull/209)

## Context

When changing a column's type, PostgreSQL often needs an explicit `USING`
expression. A simple `ALTER COLUMN ... TYPE new_type` fails for cases like
`text -> enum`, and a pre-existing default may also need to be dropped before
the type change and restored afterward.

This used to be a genuine parity gap: pgschema originally omitted the `USING`
clause and default-safe flow, and pg-delta had the same problem. That gap is
now closed in current pg-delta.

The pg-delta fix landed in
[pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231), which
closed the tracking issue
[pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130).

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

pgschema fixed the issue by generating a `USING` clause for type changes that
need an explicit cast and by handling the default drop/re-set flow around the
ALTER.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | ✅ Present |
| `USING` clause emitted for true type changes | ✅ `table.alter.ts` now appends `USING column::new_type` when the previous type differs |
| Default-safe flow around type changes | ✅ `table.diff.ts` drops and re-sets defaults around the type change when needed |
| Integration regression for `text -> enum` with default | ✅ Present in `tests/integration/alter-table-operations.test.ts` |
| Integration regression for `varchar -> integer` with `USING` | ✅ Present in `tests/integration/alter-table-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed by [#231](https://github.com/supabase/pg-toolbelt/pull/231) |

Current source evidence from
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.alter.ts`:

```typescript
if (hasTypeChangedWithPreviousDefinition) {
  parts.push("USING", `${this.column.name}::${this.column.data_type_str}`);
}
```

Current integration evidence from
`repos/pg-toolbelt/packages/pg-delta/tests/integration/alter-table-operations.test.ts`:

- `change column type to enum with default`
- `change varchar column type to integer with using cast`
- `widen column type preserves pre-existing default`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical bug** | Omitted `USING` / default-safe flow | Same |
| **Current state** | Fixed | Fixed |
| **Regression coverage** | Merged issue fix in pgschema | Merged source fix plus roundtrip integration coverage |

## Resolution in pg-delta

pg-delta now handles this scenario correctly:

1. `table.diff.ts` emits a safe sequence around the type change when a default
   must be temporarily removed.
2. `AlterTableAlterColumnType.serialize()` appends a `USING` cast when the
   previous and next type definitions differ.
3. Integration coverage exercises both enum and numeric/integer casting flows.

This benchmark entry is therefore retained as historical context only. The
parity gap is solved in the current pg-delta snapshot
(`repos/pg-toolbelt@c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`).

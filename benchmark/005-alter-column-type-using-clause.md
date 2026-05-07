# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` → custom enum), PostgreSQL
requires a `USING` clause if the cast is not implicit. If the existing default
cannot be cast automatically, the default must also be dropped before the type
change and re-applied afterward.

pgschema originally generated `ALTER COLUMN ... TYPE enum_type` without the
`USING` clause and without the default-safe sequencing. That behavior is what
issue #190 fixed upstream.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130)
is closed, and although the original PR
[pg-toolbelt#146](https://github.com/supabase/pg-toolbelt/pull/146) closed
without merging, equivalent logic is present in current `main`: the type-change
serializer now emits `USING column::new_type` when the previous column shape is
known, and integration tests cover both the enum/default flow and a plain cast
flow.

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

pgschema fixed the issue by generating `USING` for non-implicit casts and by
sequencing default drop/reapply around the type change.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | ✅ Present |
| USING clause in `serialize()` | ✅ Current `table.alter.ts` appends `USING <column>::<new_type>` when a real type change is detected via `previousColumn` |
| Default drop/re-set around type change | ✅ Current diff planning uses a default-safe type-change flow |
| Integration regression for `text -> enum` with default | ✅ Covered in `tests/integration/alter-table-operations.test.ts` |
| Integration regression for plain cast path (`varchar -> integer`) | ✅ Covered in `tests/integration/alter-table-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) is closed; PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) is closed after equivalent logic reached `main` |

**Current source evidence** (`table.alter.ts` on
`repos/pg-toolbelt@102ef99ae5aabb29510d48b39fbb8ecee34f5458`):

```typescript
if (hasTypeChangedWithPreviousDefinition) {
  parts.push("USING", `${this.column.name}::${this.column.data_type_str}`);
}
```

The two key integration cases now live in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/alter-table-operations.test.ts`:

- `change column type to enum with default`
- `change varchar column type to integer with using cast`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Missing `USING` and default-safe sequencing | Same |
| **Current fix** | Emits `USING` and sequences default handling safely | Emits `USING` from `AlterTableAlterColumnType` and plans the type/default flow together |
| **Regression coverage** | Fixed in upstream issue/fixture flow | Integration coverage for enum/default and generic cast paths |

## Resolution in pg-delta

pg-delta now handles the same class of type-change migrations that motivated
pgschema #190. The benchmark entry is retained as historical context, but it is
no longer an active parity gap in the current pg-delta snapshot.

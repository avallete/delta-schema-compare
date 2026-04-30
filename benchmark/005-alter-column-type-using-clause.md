# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed), fixed by [pgschema#209](https://github.com/pgplex/pgschema/pull/209)

## Context

When changing a column's type (for example `text` to a custom enum),
PostgreSQL may require an explicit `USING` clause. If the column also has
an incompatible default, that default must be dropped before the type
change and re-applied afterward.

pgschema issue #190 covered exactly that failure mode: a text column with a
default was converted to an enum, but the emitted migration omitted both
the cast expression and the default-safe sequencing.

pg-delta used to have the same gap. That parity issue is now fixed in
pg-delta by [pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231),
which closed [pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130).
The earlier draft attempt in
[pg-toolbelt#146](https://github.com/supabase/pg-toolbelt/pull/146) was
later closed once the merged fix landed.

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

**Expected:** pg-delta generates the same default-safe sequence with an
explicit `USING state::test_schema.status` cast.

## How pgschema handled it

pgschema fixed the issue by emitting a `USING` clause for the cast and by
preserving the required `DROP DEFAULT` / `SET DEFAULT` sequencing around
the type change.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` serializer emits `USING` for real type changes | Yes - `src/core/objects/table/changes/table.alter.ts` appends `USING column::new_type` when `previousColumn.data_type_str` differs |
| Default drop / re-set sequencing around type changes | Yes |
| Integration regression for `text -> enum` with default | Yes - `tests/integration/alter-table-operations.test.ts` includes `change column type to enum with default` |
| Integration regression for casted `varchar -> integer` changes | Yes - the same file includes `change varchar column type to integer with using cast` |
| Existing pg-toolbelt issue / PR | Yes - issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed by merged PR [#231](https://github.com/supabase/pg-toolbelt/pull/231) |

**Source evidence** (`src/core/objects/table/changes/table.alter.ts`):

```typescript
if (hasTypeChangedWithPreviousDefinition) {
  parts.push("USING", `${this.column.name}::${this.column.data_type_str}`);
}
```

A separate reverse-direction cleanup scenario (`enum -> text` followed by
`DROP TYPE`) is still skipped in the integration suite, but that is an
adjacent dependency-ordering problem rather than the original #190
forward cast/default case.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Missing `USING` and default-safe sequencing | Same |
| Current upstream state | Fixed in merged PR #209 | Fixed in merged PR #231 |
| Regression coverage | Reproduction locked into pgschema fixtures | End-to-end roundtrip coverage for both enum/default and explicit-cast cases |

## Resolution in pg-delta

pg-delta now treats this benchmark scenario as solved. The serializer emits
`USING` when a real type change is detected, and the integration suite
exercises the exact text-to-enum-with-default flow from pgschema #190.

This benchmark entry is therefore retained as historical context only.

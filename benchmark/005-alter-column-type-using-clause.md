# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` to a custom enum),
PostgreSQL requires a `USING` clause if the cast is not implicit. If the column
also has a default that is invalid for the new type, the default must be
dropped before the type change and re-applied afterward.

That was the original gap behind pgschema issue #190, and pg-delta used to have
the same failure mode. In the current pg-delta mainline snapshot, that parity
gap is now resolved: the table alter serializer emits a `USING` cast when it is
given the previous column definition, and the diff logic plans the
default-drop/type-change/default-reapply sequence safely.

The original pg-toolbelt tracker for this work was
[pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130), with the
implementation first proposed in
[pg-toolbelt#146](https://github.com/supabase/pg-toolbelt/pull/146). Both are
now closed, and equivalent behavior is present in the refreshed `main` snapshot
used by this benchmark.

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

pgschema fixed the issue by generating `USING` clauses for non-implicit casts
and by handling the default drop/re-set workflow around the type change.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | ✅ Present |
| `USING` clause generation | ✅ `table.alter.ts` appends `USING <column>::<type>` when the previous type differs |
| Default drop/re-set around type change | ✅ Planned in the current table diff flow |
| Integration regression for `text -> enum` with default | ✅ Present in `tests/integration/alter-table-operations.test.ts` |
| Integration regression for `varchar -> integer` with cast | ✅ Present in `tests/integration/alter-table-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed; PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) closed |

**Source evidence** (`src/core/objects/table/changes/table.alter.ts`):

```typescript
const hasTypeChangedWithPreviousDefinition =
  this.previousColumn?.data_type_str !== undefined &&
  this.previousColumn.data_type_str !== this.column.data_type_str;

// ...

if (hasTypeChangedWithPreviousDefinition) {
  parts.push("USING", `${this.column.name}::${this.column.data_type_str}`);
}
```

And the refreshed integration suite now includes both:

- `change column type to enum with default`
- `change varchar column type to integer with using cast`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing `USING` and default-safe sequencing | Same historical gap |
| **Current upstream state** | Fixed | Fixed in the current `main` snapshot |
| **Regression coverage** | Issue-specific fix landed upstream | End-to-end integration coverage now exists for both enum and casted scalar changes |
| **Benchmark status** | Historical context only | Solved |

## Resolution in pg-delta

pg-delta now handles this scenario end to end:

1. it detects a real type change,
2. emits `USING <column>::<new_type>` when needed,
3. preserves default safety by sequencing drop/reapply correctly, and
4. proves the behavior with focused integration coverage.

This benchmark entry is therefore retained as historical context, but the parity
gap itself is solved in the current pg-delta snapshot.

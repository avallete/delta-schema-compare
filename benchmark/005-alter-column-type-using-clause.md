# Column Type Change Missing USING Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (e.g. `text` → custom enum), PostgreSQL requires
a `USING` clause if the implicit cast doesn't exist. Without it the ALTER fails
with `ERROR: column "x" cannot be cast automatically to type "y"`. Additionally,
if the column has a default value that is incompatible with the new type, the
default must be dropped first and re-set after the ALTER.

pgschema was generating `ALTER COLUMN ... TYPE enum_type` without the `USING`
clause and without handling existing defaults.

pg-delta's `AlterTableAlterColumnType.serialize()` (in
`src/core/objects/table/changes/table.alter.ts`) generates the ALTER statement
**without a USING clause** — the code only emits TYPE and optional COLLATE.

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

pgschema added USING clause generation for type changes involving custom types.
It also handles the default drop/re-set workflow.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | ✅ Exists |
| USING clause in serialize() | ❌ **Not generated** |
| Default drop/re-set around type change | ❌ Not handled |
| Integration test for type change with USING | ❌ None |

**Source evidence** (`table.alter.ts` lines 605–618):
```typescript
serialize(): string {
  const parts: string[] = [
    "ALTER TABLE", `${this.table.schema}.${this.table.name}`,
    "ALTER COLUMN", this.column.name,
    "TYPE", this.column.data_type_str,
  ];
  if (this.column.collation) {
    parts.push("COLLATE", this.column.collation);
  }
  return parts.join(" ");
}
```

No `USING` clause is appended.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing USING in ALTER DDL output | Same — no USING in `serialize()` |
| **Fix scope** | IR ALTER serialiser | `AlterTableAlterColumnType` + diff logic |
| **Complexity** | Medium — needs to decide when USING is required | Medium — same analysis needed |

## Plan to handle it in pg-delta

1. **Modify `AlterTableAlterColumnType`** in `src/core/objects/table/changes/table.alter.ts`:
   - Add logic to detect when old type → new type requires a USING clause
   - Generate `USING column_name::new_type` as a safe default
   - Consider allowing explicit USING expressions in the future
2. **Handle default drop/re-set**: when a column's type changes and it has a
   default, emit `ALTER COLUMN ... DROP DEFAULT` before the type change, then
   `ALTER COLUMN ... SET DEFAULT ...` after.
3. **Add integration tests** in `tests/integration/alter-table-operations.test.ts`:
   - `text` → `enum` type change
   - `varchar` → `integer` type change
   - Type change on column with existing default
4. **Edge case**: columns with `NOT NULL` and data — the USING must produce
   non-null values.

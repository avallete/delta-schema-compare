# Composite FK Referenced Column Order Incorrect

> pgschema issue [#266](https://github.com/pgplex/pgschema/issues/266) (closed)

## Context

When a composite foreign key's column order differs from the referenced table's
column definition order (attnum), the referenced columns may be emitted in the
wrong order. This generates invalid DDL that references the wrong columns.

For example, `FOREIGN KEY (b, a) REFERENCES parent (y, x)` could be emitted as
`FOREIGN KEY (b, a) REFERENCES parent (x, y)` if the serialiser sorts by
attnum rather than FK column position.

pg-delta has FK constraint tests (including ordering tests in
`fk-constraint-ordering.test.ts`) but **no test for multi-column FK where the
column order matters**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parent (
    x int NOT NULL,
    y int NOT NULL,
    UNIQUE (y, x)  -- note: y before x
);

CREATE TABLE test_schema.child (
    b int NOT NULL,
    a int NOT NULL,
    CONSTRAINT fk_child_parent
      FOREIGN KEY (b, a) REFERENCES test_schema.parent (y, x)
);
```

**Change to diff:**

```sql
-- Modify the FK to add ON DELETE CASCADE
ALTER TABLE test_schema.child
  DROP CONSTRAINT fk_child_parent;
ALTER TABLE test_schema.child
  ADD CONSTRAINT fk_child_parent
    FOREIGN KEY (b, a) REFERENCES test_schema.parent (y, x)
    ON DELETE CASCADE;
```

## How pgschema handled it

pgschema fixed its FK serialiser to maintain the column mapping order as stored
in `pg_constraint.conkey` / `confkey` arrays, rather than sorting by attnum.

## Current pg-delta status

| Aspect | Status |
|---|---|
| FK constraint model | ✅ Present |
| Single-column FK tests | ✅ Covered |
| Multi-column (composite) FK tests | ❌ None |
| FK column order preservation | ❓ Untested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Sorting referenced columns by attnum | Unknown — likely uses catalog order |
| **Fix scope** | FK serialiser column ordering | Verify catalog query + add test |
| **Risk** | High — broken FK semantics | Medium — may already work correctly |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/constraint-operations.test.ts`:
   - Create a composite FK where FK column order differs from parent attnum
   - Diff and verify the DDL preserves the correct column mapping
   - Test modifying the FK (e.g. adding `ON DELETE CASCADE`)
2. **Verify catalog query** — check that the constraint query in pg-delta
   preserves `conkey`/`confkey` ordering from `pg_constraint`.
3. **Test edge case**: composite FK referencing columns in reverse order of
   their definition in the parent table.

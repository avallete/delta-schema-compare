# View Column Expansion with SELECT * and Table Changes

> pgschema issue [#308](https://github.com/pgplex/pgschema/issues/308) (closed)

## Context

When a table gains a new column and a dependent view uses `SELECT t.*`,
PostgreSQL cannot use `CREATE OR REPLACE VIEW` because it would require
renaming existing view columns or changing their types. Instead, the view
must be dropped and recreated.

pgschema was emitting `CREATE OR REPLACE VIEW` which fails with
`ERROR: cannot change name of view column`.

pg-delta reads view definitions from the catalog, where `SELECT *` is expanded
to explicit column lists. So pg-delta would see the view definition as unchanged
(still listing the old columns). When the user modifies the view in the branch
database to include the new column, pg-delta should detect the change. However,
the **DDL ordering** (add column to table before recreating view) and the
**need to DROP+CREATE** (rather than CREATE OR REPLACE when view column list
changes) have not been tested.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.items (
    id serial PRIMARY KEY,
    title text NOT NULL,
    status text DEFAULT 'active'
);

CREATE VIEW test_schema.item_details AS
    SELECT i.* FROM test_schema.items i;
```

**Change to diff (add a column to the table):**

```sql
ALTER TABLE test_schema.items ADD COLUMN priority int DEFAULT 0;

-- View must be recreated to pick up the new column
DROP VIEW test_schema.item_details;
CREATE VIEW test_schema.item_details AS
    SELECT i.* FROM test_schema.items i;
```

## How pgschema handled it

pgschema detects when a view's column list would change and emits DROP + CREATE
instead of CREATE OR REPLACE.

## Current pg-delta status

| Aspect | Status |
|---|---|
| View create/drop/replace | ✅ Tests exist |
| View with SELECT * | ✅ SELECT * appears in view tests |
| View column list change detection | ❓ Untested |
| DROP + CREATE vs CREATE OR REPLACE for column changes | ❓ Unknown |
| Table column addition with dependent view | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | CREATE OR REPLACE can't change columns | Same PostgreSQL limitation |
| **Fix scope** | View diff to detect column list changes | View diff + DDL choice |
| **pg-delta advantage** | N/A | Already uses catalog-expanded column lists |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/view-operations.test.ts`:
   - Create a table and a view using `SELECT *`
   - In branch, add a column to the table and recreate the view
   - Verify pg-delta generates correct DDL (DROP VIEW, ALTER TABLE, CREATE VIEW)
2. **Verify** that the view diff detects column list changes (not just
   definition text changes) and chooses DROP + CREATE when columns differ.
3. **Test ordering**: the table alteration must happen before the view is
   recreated in the DDL output.

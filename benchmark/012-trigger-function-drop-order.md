# Trigger Function Drop Ordering

> pgschema issue [#148](https://github.com/pgplex/pgschema/issues/148) (closed)

## Context

When removing both a trigger and its trigger function, the trigger must be
dropped **before** the function. pgschema was generating the DDL in the wrong
order — dropping the function first, which fails because the trigger still
references it.

pg-delta has trigger tests and function tests, but **no integration test for
the specific scenario of dropping a trigger and its function together**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.foo (id int PRIMARY KEY);

CREATE FUNCTION test_schema.bar()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RETURN NULL;
END;
$$;

CREATE TRIGGER foo_insert
    BEFORE INSERT ON test_schema.foo
    EXECUTE FUNCTION test_schema.bar();
```

**Change to diff (remove trigger and function):**

```sql
-- Just the table remains
CREATE TABLE test_schema.foo (id int PRIMARY KEY);
```

**Expected DDL order:**

```sql
DROP TRIGGER foo_insert ON test_schema.foo;
DROP FUNCTION test_schema.bar();
```

**Wrong order (fails):**

```sql
DROP FUNCTION test_schema.bar();
-- ERROR: cannot drop function bar() because trigger foo_insert depends on it
```

## How pgschema handled it

pgschema fixed the dependency ordering to ensure triggers are dropped before
their functions.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger create/drop | ✅ Tests exist |
| Function create/drop | ✅ Tests exist |
| Drop trigger + function together | ❌ Not tested |
| Dependency: trigger → function for drops | ❓ May work via `pg_depend` |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing reverse dependency edge for drops | Should work if `pg_depend` is used for drop ordering |
| **Fix scope** | Dependency graph | Verify sort module handles drop dependencies |
| **pg-delta advantage** | N/A | Dependency graph infrastructure already exists |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/trigger-operations.test.ts`:
   - Create a table, trigger function, and trigger
   - Remove both trigger and function in the branch
   - Verify the DDL drops the trigger before the function
2. **Verify** that the topological sort in `src/core/sort/` correctly inverts
   dependencies for drop operations (i.e. if create order is function → trigger,
   then drop order is trigger → function).
3. **Test edge case**: trigger function used by multiple triggers — all triggers
   must be dropped before the function.

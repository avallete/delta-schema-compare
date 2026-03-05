# Domain CHECK Constraint with Function Reference Ordering

> pgschema issue [#254](https://github.com/pgplex/pgschema/issues/254) (closed)

## Context

When a `CREATE DOMAIN` statement has a CHECK constraint that references a
function (e.g. `CHECK (typeid_check_prefix(VALUE, 'user'))`), the function
must be created before the domain. pgschema was ordering statements
incorrectly, creating the domain before the function it references.

pg-delta has domain type support and tests for basic CHECK constraints on
domains, but **no test for domain CHECK constraints that reference
user-defined functions**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

-- Function used in domain CHECK
CREATE OR REPLACE FUNCTION test_schema.check_prefix(val text, prefix text)
RETURNS boolean LANGUAGE plpgsql IMMUTABLE AS $$
BEGIN
  RETURN starts_with(val, prefix);
END;
$$;

-- Domain with CHECK referencing the function
CREATE DOMAIN test_schema.user_id AS text
  CHECK (test_schema.check_prefix(VALUE, 'user_'));
```

**Change to diff:**

```sql
-- Add a new domain referencing the same function
CREATE DOMAIN test_schema.org_id AS text
  CHECK (test_schema.check_prefix(VALUE, 'org_'));
```

## How pgschema handled it

pgschema added dependency tracking for function references within domain CHECK
constraint expressions, ensuring the function is created before the domain.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Domain type support | ✅ Module in `src/core/objects/domain/` |
| Domain CHECK constraint | ✅ Basic tests exist |
| Domain CHECK referencing a function | ❌ Not tested |
| Dependency edge: domain → function | ❓ Unknown |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing dependency: domain CHECK → function | Unknown — may rely on `pg_depend` which should track this |
| **Fix scope** | Dependency graph edge | Verify `pg_depend` captures it, add test |
| **pg-delta advantage** | N/A | `pg_depend` should capture domain → function deps |

**Key insight**: Unlike plpgsql function body references (issue #256),
domain CHECK constraints ARE tracked by `pg_depend`. So pg-delta's
`pg_depend`-based ordering should handle this correctly, but it has never
been verified with a test.

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/type-operations.test.ts`:
   - Create a function and a domain whose CHECK references it
   - Verify pg-delta creates the function before the domain
   - Modify the domain CHECK expression
   - Test dropping the function (should fail or cascade)
2. **Verify** that pg-delta's dependency extraction from `pg_depend` includes
   domain → function edges.
3. **Test edge case**: circular dependency where a function uses a domain type
   as a parameter, and the domain CHECK references a different function.

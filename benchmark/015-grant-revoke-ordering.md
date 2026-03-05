# Grant/Revoke Ordering (Column vs Table Level)

> pgschema issue [#324](https://github.com/pgplex/pgschema/issues/324) (closed)

## Context

When migrating from a table-level GRANT to a column-level GRANT, the order of
operations matters. If the REVOKE happens before the new GRANT, the user
temporarily loses all permissions. If the column-level GRANT happens first,
the subsequent table-level REVOKE also removes the column-level grant.

The correct order is:
1. REVOKE the old table-level grant
2. GRANT the new column-level grant

pgschema was generating them in the wrong order (GRANT before REVOKE), which
effectively left the user with no permissions.

pg-delta has privilege operation tests, but **no test for the specific
interaction between table-level and column-level privilege transitions**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.data (
    id serial PRIMARY KEY,
    public_info text,
    secret_info text
);

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_user') THEN
    CREATE ROLE app_user;
  END IF;
END $$;

-- Current state: full table UPDATE
GRANT UPDATE ON test_schema.data TO app_user;
```

**Change to diff (restrict to column-level):**

```sql
-- Desired state: only column-level UPDATE
GRANT UPDATE (public_info) ON test_schema.data TO app_user;
```

**Expected DDL (correct order):**

```sql
REVOKE UPDATE ON TABLE test_schema.data FROM app_user;
GRANT UPDATE (public_info) ON TABLE test_schema.data TO app_user;
```

**Buggy order (user loses access):**

```sql
GRANT UPDATE (public_info) ON TABLE test_schema.data TO app_user;
REVOKE UPDATE ON TABLE test_schema.data FROM app_user;
-- Now app_user has NO update permission at all!
```

## How pgschema handled it

pgschema fixed the privilege ordering to ensure REVOKE of the broader
permission happens before GRANT of the narrower one.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table-level GRANT/REVOKE | ✅ Tests exist |
| Column-level GRANT/REVOKE | ✅ Tests exist |
| Table → column privilege transition | ❌ Not tested |
| REVOKE-before-GRANT ordering | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Wrong statement ordering | Untested — may have same bug |
| **Fix scope** | Privilege planner ordering | Privilege diff + sort module |
| **Risk** | 🔴 Data access violation | 🔴 Same — silent permission loss |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/privilege-operations.test.ts`:
   - Start with table-level GRANT UPDATE
   - Transition to column-level GRANT UPDATE (public_info)
   - Verify DDL order: REVOKE table-level first, then GRANT column-level
   - Verify the role has the correct permissions after migration
2. **Check privilege diff logic** in `src/core/objects/privilege/` to ensure
   the ordering rule (REVOKE broad → GRANT narrow) is implemented.
3. **Test reverse transition**: column-level → table-level (should REVOKE
   column-level first, then GRANT table-level).

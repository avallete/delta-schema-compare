# Default Privileges + Selective REVOKE Convergence

> pgschema issue [#253](https://github.com/pgplex/pgschema/issues/253) (closed)

## Context

When a schema uses `ALTER DEFAULT PRIVILEGES` to auto-grant access on new
tables, combined with explicit `REVOKE` statements for specific tables, the
migration may require two apply cycles to converge. The REVOKE is not included
in the same apply as the `CREATE TABLE` because the default privilege grant
happens asynchronously during table creation.

pgschema required two `plan` + `apply` cycles to reach steady state.

pg-delta has default privileges tests (including edge cases) but **no test for
the interaction between default privileges and selective REVOKE on individual
tables** within a single migration.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

-- Setup: default privileges grant SELECT to a role
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'reader') THEN
    CREATE ROLE reader;
  END IF;
END $$;

ALTER DEFAULT PRIVILEGES IN SCHEMA test_schema
  GRANT SELECT ON TABLES TO reader;

CREATE TABLE test_schema.public_data (
    id serial PRIMARY KEY,
    info text
);

-- This table should NOT be readable by 'reader' despite default privileges
CREATE TABLE test_schema.secret_data (
    id serial PRIMARY KEY,
    secret text
);

REVOKE SELECT ON test_schema.secret_data FROM reader;
```

**Expected single-pass behavior:**

```sql
CREATE TABLE test_schema.secret_data (...);
-- Default privileges auto-grant SELECT to reader
REVOKE SELECT ON test_schema.secret_data FROM reader;
```

## How pgschema handled it

pgschema addressed this by ensuring REVOKE statements are generated in the same
plan as the CREATE TABLE, even when the grant comes from default privileges.
This was not fully resolved — it remains an area of complexity.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `ALTER DEFAULT PRIVILEGES` support | ✅ Tests exist |
| Default privileges edge cases | ✅ `default-privileges-edge-case.test.ts` |
| Default priv + selective REVOKE interaction | ❌ Not tested |
| Single-pass convergence verification | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Default grants happen at CREATE TABLE time, REVOKE comes later | Same issue could occur |
| **Fix complexity** | High — requires awareness of default privilege effects | High — same analysis needed |
| **Convergence model** | Eventually converges in 2 passes | Unknown — untested |

## Plan to handle it in pg-delta

1. **Add integration test** in
   `tests/integration/default-privileges-edge-case.test.ts`:
   - Setup default privileges granting SELECT to a role
   - Create a table that should have the grant revoked
   - Verify the generated DDL includes both CREATE TABLE and REVOKE in proper order
   - Verify a second diff produces no changes (single-pass convergence)
2. **Investigate** whether pg-delta's privilege diff logic accounts for
   grants that originate from default privileges when determining what to
   REVOKE.
3. **Edge case**: test with multiple roles and mixed default privileges
   (GRANT on some object types, REVOKE on others).

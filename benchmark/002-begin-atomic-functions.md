# BEGIN ATOMIC Function Bodies Not Supported

> pgschema issue [#241](https://github.com/pgplex/pgschema/issues/241) (closed)

## Context

PostgreSQL 14+ supports SQL-standard function bodies using `BEGIN ATOMIC ...
END` syntax as an alternative to dollar-quoted string bodies. These functions
have their body stored in `pg_proc.prosqlbody` as a parsed node tree rather
than as a text string in `prosrc`.

pgschema was producing a syntax error when dumping these functions because its
serialiser only handled `AS $$...$$` bodies.

pg-delta has **no test coverage** for `BEGIN ATOMIC` functions.  The procedure
model captures the server-generated `pg_get_functiondef()` output (which
includes `BEGIN ATOMIC`), but correctness is unverified.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.accounts (
    user_id int PRIMARY KEY,
    balance int NOT NULL DEFAULT 0
);

CREATE OR REPLACE FUNCTION test_schema.transfer_funds(
    sender_id int, receiver_id int, amount numeric
)
RETURNS void
LANGUAGE SQL
BEGIN ATOMIC
    UPDATE test_schema.accounts
      SET balance = balance - amount WHERE user_id = sender_id;
    UPDATE test_schema.accounts
      SET balance = balance + amount WHERE user_id = receiver_id;
END;
```

**Change to diff:**

```sql
CREATE OR REPLACE FUNCTION test_schema.transfer_funds(
    sender_id int, receiver_id int, amount numeric
)
RETURNS void
LANGUAGE SQL
BEGIN ATOMIC
    UPDATE test_schema.accounts
      SET balance = balance - amount WHERE user_id = sender_id;
    UPDATE test_schema.accounts
      SET balance = balance + amount WHERE user_id = receiver_id;
    INSERT INTO test_schema.accounts (user_id, balance)
      VALUES (receiver_id, amount)
      ON CONFLICT (user_id) DO NOTHING;
END;
```

## How pgschema handled it

pgschema added support for the `prosqlbody` column and serialises the body
with `BEGIN ATOMIC ... END` when the function uses SQL-standard syntax.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Catalog query captures `definition` via `pg_get_functiondef()` | ✅ |
| `sql_body` field in procedure model | ✅ Present |
| Integration test for BEGIN ATOMIC | ❌ None |
| Diff logic handles `sql_body` changes | ❓ Untested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Dump serialiser only knew `AS $$` syntax | Model likely captures it via `pg_get_functiondef()` but untested |
| **Fix scope** | IR body serialiser + prosqlbody column | Add integration test, verify round-trip |
| **Complexity** | Medium — new serialiser branch | Low — likely already works, just needs test |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/function-operations.test.ts`:
   - Create a function with `BEGIN ATOMIC` body
   - Modify the body
   - Verify diff detects the change and round-trips correctly
2. **Verify** that the procedure diff treats `sql_body` changes the same as
   `source_code` changes (both are in `NON_ALTERABLE_FIELDS`).
3. **Test with PostgreSQL 14+** since BEGIN ATOMIC is unavailable on older
   versions — guard with version check.

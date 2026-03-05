# INSTEAD OF Triggers on Views Missing

> pgschema issue [#287](https://github.com/pgplex/pgschema/issues/287) (closed)

## Context

`INSTEAD OF` triggers are used on views to intercept INSERT/UPDATE/DELETE
operations and redirect them to underlying tables. pgschema was not dumping
these triggers at all.

pg-delta's trigger model captures trigger definitions via `pg_get_triggerdef()`
which does include `INSTEAD OF` timing, and the trigger type bitmask encodes
it (bit 8). However, there are **no integration tests** for `INSTEAD OF`
triggers — all existing trigger tests use `BEFORE` or `AFTER` timing on
tables, never on views.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
    id serial PRIMARY KEY,
    email text NOT NULL
);

CREATE VIEW test_schema.user_emails AS
  SELECT id, email FROM test_schema.users;

CREATE OR REPLACE FUNCTION test_schema.insert_user_email()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO test_schema.users (email) VALUES (NEW.email);
    RETURN NEW;
END;
$$;

CREATE TRIGGER user_emails_insert
    INSTEAD OF INSERT ON test_schema.user_emails
    FOR EACH ROW
    EXECUTE FUNCTION test_schema.insert_user_email();
```

**Change to diff:**

```sql
-- Add an INSTEAD OF UPDATE trigger
CREATE OR REPLACE FUNCTION test_schema.update_user_email()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    UPDATE test_schema.users SET email = NEW.email WHERE id = OLD.id;
    RETURN NEW;
END;
$$;

CREATE TRIGGER user_emails_update
    INSTEAD OF UPDATE ON test_schema.user_emails
    FOR EACH ROW
    EXECUTE FUNCTION test_schema.update_user_email();
```

## How pgschema handled it

pgschema fixed its trigger inspector to include triggers with `tgtype` bit 8
set (INSTEAD OF), which were previously filtered out.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger type bitmask supports INSTEAD OF (bit 8) | ✅ Catalog query captures it |
| `pg_get_triggerdef()` includes INSTEAD OF text | ✅ |
| Integration test for INSTEAD OF triggers | ❌ None |
| Trigger on views (not tables) | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Inspector query filtered out INSTEAD OF triggers | No filter, but zero test coverage |
| **Fix scope** | Query filter removal | Add integration tests |
| **Risk** | Low | Low — mechanism likely works, needs verification |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/trigger-operations.test.ts`:
   - Create a view with an `INSTEAD OF INSERT` trigger
   - Add an `INSTEAD OF UPDATE` trigger
   - Verify both triggers appear in diff and DDL is correct
2. **Verify** that the trigger catalog query does not filter on `tgtype` in a
   way that excludes INSTEAD OF triggers.
3. **Test view dependency** — the trigger depends on the view, which depends
   on the table. Verify the DDL ordering is correct.

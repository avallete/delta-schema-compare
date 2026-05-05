# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with `UPDATE OF <column_list>`
were dumped or planned as plain `UPDATE`, dropping the column list and making
the trigger fire for unrelated updates.

That is a real semantic downgrade. A trigger meant to run only when `email`
changes can become a trigger that runs on any update, which can be observable
at the application level.

This benchmark entry is historical now: current pg-delta explicitly covers the
same scenario. The corresponding pg-toolbelt issue
[#140](https://github.com/supabase/pg-toolbelt/issues/140) is closed and
[pg-toolbelt#200](https://github.com/supabase/pg-toolbelt/pull/200) added
focused integration coverage for `UPDATE OF` trigger column lists.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.user_account (
    id bigint generated always as identity primary key,
    email text not null,
    verified boolean not null default false
);

CREATE OR REPLACE FUNCTION test_schema.user_account_encrypt_secret_email()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    NEW.email := 'enc:' || NEW.email;
    RETURN NEW;
END;
$$;
```

**Change to diff:**

```sql
CREATE OR REPLACE TRIGGER user_account_encrypt_secret_trigger_email
    BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
    FOR EACH ROW
    EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email();
```

## How pgschema handled it

pgschema fixed the issue by preserving `UPDATE OF ...` trigger metadata through
introspection and DDL emission.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger model captures update-column metadata | ✅ `src/core/objects/trigger/trigger.model.ts` stores `column_numbers` from `pg_trigger.tgattr` |
| Trigger create SQL preserves catalog trigger definition | ✅ Create / replace flows reuse the captured `definition` |
| Integration test for `UPDATE OF <columns>` | ✅ `tests/integration/trigger-operations.test.ts` includes `"multi-event trigger preserves UPDATE OF column list"` |
| Column-number diff regression | ✅ `tests/integration/trigger-update-of-column-numbers.test.ts` covers `tgattr`-driven replacement behavior |
| Existing pg-toolbelt issue / PR | ✅ Issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

The integration suite now asserts that generated SQL contains:

```sql
CREATE TRIGGER user_account_encrypt_secret_trigger_email
BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
FOR EACH ROW EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email();
```

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical bug** | Dropped `UPDATE OF` column filters | Same parity gap existed historically |
| **Current implementation** | Fixed upstream | Fixed with dedicated integration regressions |
| **Evidence** | Resolved issue + merged PR | Trigger model support plus two focused integration suites |

## Resolution in pg-delta

This benchmark entry is retained as historical context, but the parity gap is
now solved in the current pg-delta snapshot.

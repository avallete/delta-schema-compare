# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with `UPDATE OF <column_list>`
were dumped and planned as plain `UPDATE`, dropping the column filter and
changing trigger semantics.

That behavior is correctness-sensitive: a trigger meant to fire only when
`email` changes can become a trigger that fires on any update.

Refresh note (2026-05-16): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#140](https://github.com/supabase/pg-toolbelt/issues/140)
is closed, and
[pg-toolbelt#200](https://github.com/supabase/pg-toolbelt/pull/200) added the
focused roundtrip coverage that was previously missing.

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

pgschema fixed the issue by preserving `UPDATE OF ...` column lists in trigger
introspection and by re-emitting them during dump / plan output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger create/replace support | ✅ Present |
| Trigger model captures update-column metadata | ✅ `column_numbers` and full `definition` are extracted in `trigger.model.ts` |
| Diff treats `UPDATE OF` column names as semantic trigger state | ✅ Trigger comparison now relies on `definition` so named column lists are preserved |
| Dedicated `UPDATE OF <columns>` roundtrip test | ✅ `"multi-event trigger preserves UPDATE OF column list"` in `tests/integration/trigger-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

The current integration test asserts the exact SQL that used to be a blind spot:

```sql
CREATE TRIGGER user_account_encrypt_secret_trigger_email
BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
FOR EACH ROW
EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email();
```

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Dropped trigger column filter during dump / plan | Had implementation support, but lacked a focused regression case |
| **Current fix** | Preserve `UPDATE OF ...` in emitted trigger DDL | Keep trigger definitions verbatim and verify them with dedicated integration coverage |
| **Regression coverage** | Upstream issue-specific fix | Explicit roundtrip test for multi-event triggers with `UPDATE OF` lists |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the current pg-delta
snapshot. The important follow-up from the old review was the missing regression
test, and that test now exists in the integration suite.

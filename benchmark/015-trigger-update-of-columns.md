# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reported that triggers declared with `UPDATE OF <column_list>`
were being downgraded to plain `UPDATE`, which broadens trigger firing to
unrelated column updates.

That parity gap is now closed in current pg-delta as well. The refreshed
pg-delta tree keeps the column list in trigger definitions and has dedicated
integration coverage for a multi-event trigger that includes `UPDATE OF email`.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#140](https://github.com/supabase/pg-toolbelt/issues/140) is closed, and
[pg-toolbelt#200](https://github.com/supabase/pg-toolbelt/pull/200) is merged.

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

pgschema fixed the bug by preserving the `UPDATE OF ...` column list during
trigger introspection and plan emission, rather than collapsing the event list
to plain `UPDATE`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger model captures update-column metadata | ✅ `src/core/objects/trigger/trigger.model.ts` |
| Trigger SQL preserves captured trigger definition | ✅ current trigger create path reuses the catalog definition |
| Dedicated integration test for `UPDATE OF <columns>` | ✅ `tests/integration/trigger-operations.test.ts` (`"multi-event trigger preserves UPDATE OF column list"`) |
| Generated SQL asserts the column filter is retained | ✅ test asserts `UPDATE OF email` is present in emitted SQL |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed, PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped the trigger's column filter | Same parity risk existed originally |
| **Current fix** | Preserve `UPDATE OF ...` on dump and plan output | Preserve the trigger definition and assert the column filter in integration tests |
| **Regression coverage** | Upstream fix coverage | Dedicated roundtrip coverage for the exact trigger shape |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed pg-delta
snapshot. The issue stays documented here as historical context for a now-fixed
behavioral mismatch.

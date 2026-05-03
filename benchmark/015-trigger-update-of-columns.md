# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with
`UPDATE OF <column_list>` were dumped and planned as plain `UPDATE`,
dropping the column list and broadening when the trigger fires.

pg-delta used to lack a focused regression proving that the `UPDATE OF`
column list survived roundtrip diffing, so this benchmark tracked the gap
through pg-toolbelt issue
[#140](https://github.com/supabase/pg-toolbelt/issues/140).

Refresh note (2026-05-03): pg-delta now has both implementation support and
focused integration coverage. Issue
[#140](https://github.com/supabase/pg-toolbelt/issues/140) is closed and the
fix landed in merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200).

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

pgschema PR #344 added explicit handling for `UPDATE OF` trigger column
lists during introspection and output generation.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger model captures `UPDATE OF` columns | ✅ `src/core/objects/trigger/trigger.model.ts` records `column_numbers` from `tgattr` |
| Create SQL preserves the exact trigger definition | ✅ Trigger creation reuses `pg_get_triggerdef()` output |
| Focused integration regression coverage | ✅ `tests/integration/trigger-operations.test.ts` covers `multi-event trigger preserves UPDATE OF column list` |
| Additional diff-loop coverage | ✅ `tests/integration/trigger-update-of-column-numbers.test.ts` exercises repeated `UPDATE OF a, b, d` roundtrips |
| Existing pg-toolbelt issue / PR | ✅ [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed, [#200](https://github.com/supabase/pg-toolbelt/pull/200) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Dropped the `UPDATE OF` column list during schema rendering | Missing focused parity coverage for the exact trigger form |
| **Current fix** | Preserves the filtered event list | Preserves trigger definition and validates it with focused integration tests |
| **Regression coverage** | Upstream regression fixture | Two dedicated integration suites |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta preserves
`UPDATE OF <columns>` trigger definitions and exercises the scenario with
focused roundtrip tests.

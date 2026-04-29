# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with `UPDATE OF <column_list>`
were dumped/planned as plain `UPDATE`, dropping the column list and making the
trigger fire for unrelated updates.

This can produce application-level corruption (for example, re-encrypting a
field on any update). pgschema fixed this in PR #344 by explicitly tracking and
emitting the `UPDATE OF ...` column list.

pg-delta now has both source-level support and dedicated regression coverage for
this case. The trigger model captures `tgattr` as `column_numbers`, trigger
serialization reuses `pg_get_triggerdef()` via the captured `definition`, and
the integration suite now includes focused tests for `UPDATE OF <columns>`
preservation and for the related attnum-mismatch diff loop.

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

**Expected:** generated DDL preserves `UPDATE OF email`.

**Risky behavior if not preserved:** generated DDL uses `BEFORE INSERT OR UPDATE`
without the column filter, causing the trigger to run on updates that do not
modify `email`.

## How pgschema handled it

pgschema added explicit handling for `UPDATE OF` columns in trigger
introspection and output generation (PR #344), preventing loss of trigger event
specificity.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger create/replace support | ✅ Present |
| Trigger integration tests (general) | ✅ Present |
| Integration test for `UPDATE OF <columns>` | ✅ Present in `tests/integration/trigger-operations.test.ts` |
| Trigger model captures update-column metadata | ✅ `column_numbers` extracted in `src/core/objects/trigger/trigger.model.ts` |
| Create SQL preserves captured trigger definition | ✅ `definition` from `pg_get_triggerdef()` is reused |
| Diff regression for attnum-mismatch / `tgattr` stability | ✅ Present in `tests/integration/trigger-update-of-column-numbers.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ Fixed by issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) / PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Issue handling** | Fixed in merged PR #344 | Fixed in pg-delta with dedicated integration coverage |
| **Evidence level** | Verified by issue + merged tests | Verified by roundtrip coverage and a focused diff-loop regression |
| **Risk** | Addressed | Addressed in the current pg-delta snapshot |

## Resolution in pg-delta

pg-delta now has explicit roundtrip coverage for a multi-event trigger declared
as `BEFORE INSERT OR UPDATE OF email`, and the inline snapshot asserts that the
generated SQL retains the column list instead of broadening to plain `UPDATE`.
The current tree also includes a second focused regression for
`Trigger.column_numbers` / `tgattr` stability across tables with different
physical attnums, ensuring the `UPDATE OF` trigger does not get stuck in a
phantom replace loop.

This benchmark entry is therefore retained as historical context, but the parity
gap is solved in the current pg-delta snapshot.

# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with `UPDATE OF <column_list>`
were dumped/planned as plain `UPDATE`, dropping the column list and making the
trigger fire for unrelated updates.

This can produce application-level corruption (for example, re-encrypting a
field on any update). pgschema fixed this in PR #344 by explicitly tracking and
emitting the `UPDATE OF ...` column list.

In pg-delta, trigger support exists and there is broad trigger integration
coverage in `tests/integration/trigger-operations.test.ts`. The trigger model
already captures `tgattr` as `column_numbers`, and trigger creation reuses
`pg_get_triggerdef()` output via the captured `definition`, so the column list
appears to be preserved by the current implementation. The remaining gap is
that there is still no dedicated integration scenario proving roundtrip
fidelity for `UPDATE OF <columns>`.

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
| Integration test for `UPDATE OF <columns>` | ❌ Missing |
| Trigger model captures update-column metadata | ✅ `column_numbers` extracted in `src/core/objects/trigger/trigger.model.ts` |
| Create SQL preserves captured trigger definition | ✅ `definition` from `pg_get_triggerdef()` is reused |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Issue handling** | Fixed in merged PR #344 | Implementation likely preserves `UPDATE OF`, but there is no dedicated parity test |
| **Evidence level** | Verified by issue + merged tests | Source-level support exists, but roundtrip behavior is unproven by integration test |
| **Risk** | Addressed | Medium regression blind spot until a focused test exists |

## Plan to handle it in pg-delta

1. Add an integration test in `tests/integration/trigger-operations.test.ts`
   covering creation and replacement of a trigger with `UPDATE OF email`.
2. Assert generated SQL includes the column list (`UPDATE OF email`) and does
   not broaden to plain `UPDATE`.
3. Optionally add an assertion against extracted trigger metadata in
   `src/core/objects/trigger/trigger.model.ts` so the test validates both the
   catalog model and serialized SQL output.

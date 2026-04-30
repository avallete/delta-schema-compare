# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed), fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

Triggers declared as `UPDATE OF <column_list>` should only fire for
updates that touch the listed columns. If the column list is dropped and
the trigger becomes a plain `UPDATE` trigger, the trigger can start firing
for unrelated updates and change application behavior.

pgschema issue #342 covered exactly that loss of specificity. pg-delta now
handles the same scenario correctly; the gap was closed by
[pg-toolbelt#200](https://github.com/supabase/pg-toolbelt/pull/200), which
resolved [pg-toolbelt#140](https://github.com/supabase/pg-toolbelt/issues/140).

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.user_account (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email text NOT NULL,
    verified boolean NOT NULL DEFAULT false
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

## How pgschema handled it

pgschema fixed the trigger introspection / output path so `UPDATE OF ...`
column lists are preserved rather than broadened to a plain `UPDATE`
trigger.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger create / replace support | Yes |
| Trigger model captures update-column metadata | Yes - `src/core/objects/trigger/trigger.model.ts` extracts `tgattr` as `column_numbers` |
| Trigger diff compares the stable trigger definition | Yes - `src/core/objects/trigger/trigger.diff.ts` compares `definition` instead of raw attnums |
| Integration test for `UPDATE OF <columns>` | Yes - `multi-event trigger preserves UPDATE OF column list` in `tests/integration/trigger-operations.test.ts` |
| Existing pg-toolbelt issue / PR | Yes - issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

The focused regression asserts that pg-delta emits:

```sql
CREATE TRIGGER user_account_encrypt_secret_trigger_email
  BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
  FOR EACH ROW EXECUTE FUNCTION ...
```

and explicitly checks that the broader `BEFORE INSERT OR UPDATE` form is
not emitted.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Dropped the `UPDATE OF` column list | Same parity risk |
| Current upstream state | Fixed in merged PR #344 | Fixed in merged PR #200 |
| Regression coverage | Upstream issue fix tests | Focused roundtrip regression on the exact trigger form |

## Resolution in pg-delta

pg-delta now preserves `UPDATE OF` trigger column lists and has focused
integration coverage for the benchmark scenario. This benchmark entry is
solved in the current snapshot.

# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed),
> fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with
`UPDATE OF <column_list>` were dumped and planned as plain `UPDATE`, dropping
the column filter and broadening when the trigger fires.

pg-delta previously had only source-level confidence for this case because
trigger definitions are captured via `pg_get_triggerdef(...)`, but there was no
focused roundtrip regression proving that the `UPDATE OF` list survives
diff/apply. That parity gap is now closed.

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

pgschema PR #344 added explicit handling for `UPDATE OF` columns in trigger
introspection and output generation, preventing loss of trigger event
specificity.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger model captures update-column metadata | ✅ `column_numbers` extracted in `src/core/objects/trigger/trigger.model.ts` |
| Create SQL preserves captured trigger definition | ✅ `definition` from `pg_get_triggerdef()` is reused |
| Focused integration regression for `UPDATE OF <columns>` | ✅ Present in `tests/integration/trigger-operations.test.ts` |
| Supporting pg-toolbelt tracking | ✅ issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

The refreshed integration suite now includes
`"multi-event trigger preserves UPDATE OF column list"`, which asserts the
planned SQL contains:

```sql
CREATE TRIGGER user_account_encrypt_secret_trigger_email
BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
FOR EACH ROW EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email()
```

and explicitly rejects the broadened `BEFORE INSERT OR UPDATE` form without the
column list.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical bug** | Dropped the `UPDATE OF` column filter | Needed focused regression coverage to prove fidelity |
| **Current implementation** | Tracks and re-emits `UPDATE OF` columns | Reuses `pg_get_triggerdef()` and now has roundtrip regression coverage |
| **Current status** | Fixed | Solved in current pg-delta snapshot |

## Resolution in pg-delta

pg-delta now has direct end-to-end coverage for the pgschema #342 scenario.
The historical parity gap is solved and this benchmark entry is retained only
as a record of the previously missing case.

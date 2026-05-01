# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed),
> fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reported that triggers declared with `UPDATE OF <column_list>`
were dumped and planned as plain `UPDATE`, dropping the column filter and making
the trigger fire for unrelated updates. pgschema fixed this in PR #344 by
tracking the column list explicitly through introspection and re-emitting it in
generated DDL.

Current pg-delta is aligned with the fixed pgschema behavior. Trigger creation
reuses `pg_get_triggerdef(...)` via the extracted trigger `definition`, and the
integration suite now contains a direct regression for a multi-event trigger
that must preserve `UPDATE OF email`.

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

pgschema PR #344 added explicit handling for `UPDATE OF` trigger column lists in
its trigger model and serializer so the column filter survives dump / diff /
apply intact.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger create/replace support | ✅ Present |
| Trigger model captures update-column metadata | ✅ `column_numbers` extracted in `src/core/objects/trigger/trigger.model.ts` |
| Create SQL preserves captured trigger definition | ✅ `definition` from `pg_get_triggerdef()` is reused |
| Integration test for `UPDATE OF <columns>` | ✅ Present in `tests/integration/trigger-operations.test.ts` |
| Additional regression around `tgattr` attnum churn | ✅ Present in `tests/integration/trigger-update-of-column-numbers.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

**Evidence from current pg-delta tests**

`tests/integration/trigger-operations.test.ts` contains:

```typescript
test(
  "multi-event trigger preserves UPDATE OF column list",
  withDb(pgVersion, async (db) => {
    await roundtripFidelityTest({
      ...
      testSql: dedent`
        CREATE OR REPLACE TRIGGER user_account_encrypt_secret_trigger_email
          BEFORE INSERT OR UPDATE OF email ON test_schema.user_account
          FOR EACH ROW
          EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email();
      `,
      assertSqlStatements: (statements) => {
        expect(statements).toMatchInlineSnapshot(`
          [
            "CREATE TRIGGER user_account_encrypt_secret_trigger_email BEFORE INSERT OR UPDATE OF email ON test_schema.user_account FOR EACH ROW EXECUTE FUNCTION test_schema.user_account_encrypt_secret_email()",
          ]
        `);
      },
    });
  }),
);
```

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Issue handling** | Fixed in merged PR #344 | Fixed in merged PR #200 |
| **Serialization strategy** | Tracks trigger column list explicitly | Reuses `pg_get_triggerdef(...)` and keeps `UPDATE OF` in trigger definition |
| **Regression coverage** | Verified by upstream fixture | Verified by direct integration test + `tgattr` regression coverage |

## Latest refresh note (2026-05-01)

This benchmark item remains historically interesting, but it is now solved in
current pg-delta (`repos/pg-toolbelt@c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`).

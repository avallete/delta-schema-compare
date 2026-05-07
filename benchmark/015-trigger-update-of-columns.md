# Trigger `UPDATE OF` Column Lists

> pgschema issue [#342](https://github.com/pgplex/pgschema/issues/342) (closed),
> fixed by [pgschema#344](https://github.com/pgplex/pgschema/pull/344)

## Context

pgschema issue #342 reports that triggers declared with `UPDATE OF <column_list>`
were dumped/planned as plain `UPDATE`, dropping the column list and widening the
trigger so it fired on unrelated updates.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#140](https://github.com/supabase/pg-toolbelt/issues/140)
is closed, and
[pg-toolbelt#200](https://github.com/supabase/pg-toolbelt/pull/200) added
focused integration coverage. Current pg-delta also carries a second regression
test that exercises the underlying `tgattr` / column-number diff loop for
`UPDATE OF` triggers created on different table shapes.

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

pgschema PR #344 added explicit handling for `UPDATE OF` trigger columns during
introspection and DDL emission.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Trigger model preserves update-column metadata | ✅ `Trigger.column_numbers` tracks the raw `tgattr` data |
| Create SQL preserves `UPDATE OF <columns>` | ✅ Covered in `tests/integration/trigger-operations.test.ts` |
| Regression for column-number diff loop / convergence | ✅ Covered in `tests/integration/trigger-update-of-column-numbers.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) |

Current integration coverage includes:

- `multi-event trigger preserves UPDATE OF column list`
- `trigger UPDATE OF column-number diff loop`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped the `UPDATE OF` column filter | Needed dedicated regression coverage for the same trigger shape |
| **Current fix** | Tracks and re-emits the filtered column list | Preserves the `UPDATE OF` list and tests both SQL output and convergence behavior |
| **Coverage** | Fixed upstream | Dedicated integration coverage on current `main` |

## Resolution in pg-delta

The current pg-delta snapshot preserves `UPDATE OF` trigger column lists and
has targeted regressions protecting both SQL output and the internal
column-number diff path. This benchmark entry is therefore historical context,
not an active parity gap.

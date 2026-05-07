# Parity issue drafts (2026-05-07)

This document records the draft-only pg-toolbelt issue text prepared during the
2026-05-07 parity refresh.

Only one unresolved scenario warranted a fresh draft in this refresh:

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level
  `UNIQUE NULLS NOT DISTINCT` constraints

## Duplicate-check summary (pg-toolbelt)

Before drafting, the refresh checked current pg-toolbelt issues and PRs for
relevant terms such as:

- `nulls not distinct`
- `unique nulls not distinct`
- `unique constraint nulls not distinct`
- `table constraint nulls not distinct`

Result:

- The related unique-index gap is already solved by
  [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183) and
  [pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185).
- No open pg-toolbelt issue or PR was found for the **table-constraint**
  variant, so the draft below is intentionally kept distinct from the index
  issue.

## Draft 1 — pgschema #412 (table constraint `UNIQUE NULLS NOT DISTINCT`)

Relates to pgschema issue #412:
https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 describes a historical gap where table-level `UNIQUE`
constraints declared with `NULLS NOT DISTINCT` were dumped without that
modifier. That weakens the constraint semantics on PostgreSQL 15+: rows whose
NULL-bearing keys should conflict become insertable again.

Current pg-delta already handles the **index-shaped** form of this feature, but
table constraints flow through a different model and diff path. Table
constraints are extracted in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
and compared in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`.
Current pg-delta stores the rendered constraint `definition`, but it does not
surface a dedicated `nulls_not_distinct` flag for table constraints and does
not compare the rendered definition when deciding whether a named `UNIQUE`
constraint changed. As a result, a transition between `UNIQUE (...)` and
`UNIQUE NULLS NOT DISTINCT (...)` on the same named constraint can remain
invisible.

This should be tracked separately from the already-closed index issue so future
triage does not treat pg-toolbelt #183 / #185 as a duplicate fix.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.accounts (
  a integer,
  b integer,
  CONSTRAINT accounts_ab_key UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.accounts DROP CONSTRAINT accounts_ab_key;
ALTER TABLE test_schema.accounts
  ADD CONSTRAINT accounts_ab_key
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the semantic change and emits the required
drop/recreate flow preserving `NULLS NOT DISTINCT`.

**Actual:** current table-constraint diff compares structured fields such as
`constraint_type`, `key_columns`, `deferrable`, `initially_deferred`,
`validated`, `no_inherit`, and `is_temporal`, but it has no dedicated
table-constraint `nulls_not_distinct` property and it does not compare the
rendered `definition`. A named `UNIQUE` constraint with the same key columns
can therefore be treated as unchanged even though its NULL semantics differ.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so table constraints expose a first-class `nulls_not_distinct` signal (or an
   equally explicit representation) in addition to the rendered definition.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` are treated as a
   drop/recreate change when the same named constraint exists on both sides.
3. Add focused integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for both:
   - creating a table constraint with `NULLS NOT DISTINCT`, and
   - converting an existing named `UNIQUE` constraint to `NULLS NOT DISTINCT`.

## Not drafted in this refresh

- pgschema [#414](https://github.com/pgplex/pgschema/issues/414) remains a
  watch item instead of a pg-toolbelt issue draft because upstream fix PR
  [#417](https://github.com/pgplex/pgschema/pull/417) is still open.

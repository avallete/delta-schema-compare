# Parity issue drafts (2026-05-01)

This document records the draft issue text produced during the 2026-05-01
pgschema ↔ pg-delta parity refresh.

Unlike the 2026-04-22 refresh, only one scenario remained genuinely
unduplicated after reviewing current pg-toolbelt issues, PRs, benchmark files,
and upstream pg-delta source/tests:

- pgschema #412 (`UNIQUE NULLS NOT DISTINCT` on table constraints)

Open pgschema issues #404 and #366 remain tracked by existing pg-toolbelt
issues:

- pgschema #404 → [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema #366 → [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

## Duplicate-check summary (pg-toolbelt)

Before drafting, we checked for existing pg-toolbelt issues and PRs using
searches around these topics:

- `NULLS NOT DISTINCT`
- `deferrable unique`
- `enum privilege`
- `unlogged`
- `materialized view`
- `aggregate`

Result at draft time:

- standalone unique-index `NULLS NOT DISTINCT` coverage already existed via
  [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183) /
  [#185](https://github.com/supabase/pg-toolbelt/pull/185)
- no existing pg-toolbelt issue or PR was found for the table-constraint form
  of `UNIQUE NULLS NOT DISTINCT`

---

## Draft 1 — pgschema #412 (table-level `UNIQUE NULLS NOT DISTINCT`)

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 describes a gap where table-level `UNIQUE NULLS NOT
DISTINCT (...)` constraints are dumped as plain `UNIQUE (...)`, silently
weakening uniqueness semantics for rows containing `NULL`.

In pg-delta, standalone indexes already support `NULLS NOT DISTINCT` via
`src/core/objects/index/index.model.ts`, `index.diff.ts`, and integration
coverage in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/index-operations.test.ts`.
However, table constraints are modeled separately in
`src/core/objects/table/table.model.ts`, and the current table-constraint
schema/diff path does not store or compare any `nulls_not_distinct` property.
Because `table.diff.ts` compares only structured fields such as
`constraint_type`, `deferrable`, `initially_deferred`, `no_inherit`,
`is_temporal`, column lists, FK metadata, and `check_expression`, a change from
plain `UNIQUE` to `UNIQUE NULLS NOT DISTINCT` is currently invisible to the
table-constraint diff.

This matters for users migrating schemas because PostgreSQL 15 introduced
`NULLS NOT DISTINCT` specifically to make `NULL` values participate in
uniqueness checks. Dropping the modifier is not cosmetic; it changes data
integrity behavior.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
  a integer,
  b integer,
  CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  DROP CONSTRAINT pgschema_repro_nulls_uniq;

ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the constraint definition change and emits the
drop/recreate DDL preserving `NULLS NOT DISTINCT`.

**Actual:** pg-delta has no table-constraint field or integration coverage for
this modifier, so the transition is currently untracked on the table-constraint
path.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   to persist a table-constraint-level `nulls_not_distinct` flag (or otherwise
   preserve enough structured metadata to detect the modifier).
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so a plain `UNIQUE` ↔ `UNIQUE NULLS NOT DISTINCT` change triggers
   drop/recreate.
3. Keep using `pg_get_constraintdef(c.oid, true)` in
   `src/core/objects/table/changes/table.alter.ts` so the add-constraint path
   serializes the exact PostgreSQL definition once the diff detects the change.
4. Add integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating a table constraint with `UNIQUE NULLS NOT DISTINCT`
   - toggling an existing table constraint between plain `UNIQUE` and
     `UNIQUE NULLS NOT DISTINCT`

# Parity issue drafts (2026-05-09)

This document records draft follow-up text prepared during the 2026-05-09
manual pgschema ↔ pg-delta parity refresh.

## Duplicate-check summary (pg-toolbelt)

Before drafting new follow-up text, the refresh checked current pg-toolbelt
issues and PRs for the relevant pgschema scenarios.

- pgschema #404 already maps to
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema #366 already maps to
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- No matching pg-toolbelt issue or PR was found for pgschema #412

The remaining text below is draft-only material. No new pg-toolbelt issue was
opened during this refresh.

---

## Draft 1 — pgschema #412 (table-level `UNIQUE NULLS NOT DISTINCT`)

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 describes a gap where table-level
`UNIQUE NULLS NOT DISTINCT (...)` constraints were dumped without the
`NULLS NOT DISTINCT` clause. Current pg-delta already covers the **index** form
of this feature (see benchmark item 016), but the **table-constraint** form is
still not explicitly covered.

The current pg-delta table extractor captures the full constraint definition via
`pg_get_constraintdef(c.oid, true)`, but `table.diff.ts` does not compare the
rendered `definition` for same-name constraints. If a constraint keeps the same
name and key columns while changing from plain `UNIQUE` to
`UNIQUE NULLS NOT DISTINCT`, the diff can miss the semantic change.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;
CREATE TABLE test_schema.accounts (
  id integer PRIMARY KEY,
  email text,
  CONSTRAINT accounts_email_key UNIQUE (email)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.accounts
  DROP CONSTRAINT accounts_email_key;

ALTER TABLE test_schema.accounts
  ADD CONSTRAINT accounts_email_key
  UNIQUE NULLS NOT DISTINCT (email);
```

**Expected:** pg-delta emits migration SQL that recreates the named table
constraint with `NULLS NOT DISTINCT` preserved.

**Actual:** current parity evidence shows no dedicated integration test for the
table-constraint form, and the same-name constraint diff path does not compare
the full `definition`.

### Suggested Fix

1. Add an integration test in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   covering `UNIQUE NULLS NOT DISTINCT` on a named table constraint.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so same-name constraint definition changes are treated as drop-and-recreate
   changes.
3. Keep this scenario distinct from the already-solved index-level coverage in
   `tests/integration/index-operations.test.ts`.

# Parity issue drafts (2026-07-04)

This document records draft-only text from the 2026-07-04 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. These drafts are saved so
the findings can be reviewed in a PR first and then promoted to real
pg-toolbelt issues only if they still look correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing exact parity trackers already cover:
  - pgschema #404 ->
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 ->
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Exact in-flight work already exists for:
  - pgschema PR #479 trigger enabled / disabled state ->
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
- The now-closed partition-child override gap from pgschema #499 is no longer
  draft-only in this refresh; it is benchmarked as
  [`benchmark/021-partition-child-column-overrides.md`](../benchmark/021-partition-child-column-overrides.md)
- Related but not duplicate work:
  - open [pg-toolbelt#307](https://github.com/supabase/pg-toolbelt/pull/307)
    remains adjacent `pg-delta-next` work rather than an exact tracker for
    PostgreSQL 18 `VIRTUAL` generated columns

No exact open or closed pg-toolbelt issue / PR was found for pgschema #501.

---

## Draft 1 - pgschema #501 (PostgreSQL 18 `VIRTUAL` generated columns)

Relates to pgschema issue #501:
https://github.com/pgplex/pgschema/issues/501

### Context

pgschema issue #501 reports that PostgreSQL 18 `VIRTUAL` generated columns are
silently rewritten as ordinary `DEFAULT` expressions in pgschema's plan output,
producing invalid DDL. pg-delta does not use the same desired-state SQL rewrite
path, so this is not the same bug mechanism. However, the user-visible parity
gap still appears to exist: current pg-delta does not distinguish `VIRTUAL`
from `STORED` generated columns in its extract/diff/serialize pipeline.

Current pg-delta evidence for that gap:

- `table.model.ts` collapses `pg_attribute.attgenerated` to
  `is_generated: boolean`
- `table.create.ts` and `table.alter.ts` serialize non-identity generated
  columns as `GENERATED ALWAYS AS (...) STORED`
- no integration regression currently exercises PostgreSQL 18 `VIRTUAL`
  generated columns

That means even though pg-delta avoids pgschema's exact SQL rewrite bug, it
still does not appear able to preserve the `VIRTUAL` generated-column kind.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
  first_name text,
  last_name text
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.users
  ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL;
```

**Expected:** pg-delta preserves the PostgreSQL 18 `VIRTUAL` generated-column
kind when diffing and serializing the migration plan.

**Actual:** current pg-delta models generated columns only as a boolean
`is_generated` flag and serializes generated expressions as `... STORED`, so
`VIRTUAL` is not represented in the current table model or create/alter SQL
output.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/base.model.ts` and
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so generated columns preserve the actual `attgenerated` kind instead of only
   a boolean.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `VIRTUAL` vs `STORED` is treated as a meaningful change rather than being
   collapsed into a single generated/not-generated state.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.create.ts`
   and
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.alter.ts`
   so generated-column SQL preserves the correct PostgreSQL 18 keyword.
4. Add a focused regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/alter-table-operations.test.ts`
   for PostgreSQL 18 `VIRTUAL` generated columns.

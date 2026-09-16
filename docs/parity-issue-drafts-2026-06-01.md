# Parity issue drafts (2026-06-01)

This document records draft-only text from the 2026-06-01 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. These drafts are saved so
the findings can be reviewed in a PR first and then promoted to real
pg-toolbelt issues only if they still look correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing parity trackers already cover:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Related but not duplicate work:
  - [pg-toolbelt#139](https://github.com/supabase/pg-toolbelt/issues/139) /
    [#155](https://github.com/supabase/pg-toolbelt/pull/155) cover
    `SELECT *` view recreation when projected columns change after `ADD COLUMN`
  - [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263)
    covers dependency-chain failures for `ALTER COLUMN TYPE` and `DROP FUNCTION`
    with policy/view dependents, not `DROP COLUMN` with a dependent view
- No matching pg-toolbelt issue or PR was found for:
  - pgschema #444

---

## Draft 1 - pgschema #444 (`DROP COLUMN` before dependent view drop)

Relates to pgschema issue #444: https://github.com/pgplex/pgschema/issues/444

### Context

pgschema issue #444 reports a destructive ordering failure: when a column is
dropped and a view that depends on that column is recreated in the same plan,
the plan emits `ALTER TABLE ... DROP COLUMN` before the `DROP VIEW`. PostgreSQL
rejects the column drop with `SQLSTATE 2BP01` because the live view still
depends on the column.

Current pg-delta has adjacent coverage for view replacement when an `ADD COLUMN`
changes a `SELECT *` projection (`tests/integration/view-operations.test.ts`)
and related dependency-chain work is being discussed in
[pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263). However,
there is still no exact integration regression or dedicated tracker for the
`DROP COLUMN` + dependent-view ordering case from pgschema #444, so parity for
this scenario remains unverified.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.foo (
  id bigint PRIMARY KEY,
  keep_me text,
  drop_me text
);

CREATE VIEW test_schema.foo_v AS
SELECT id, keep_me, drop_me
FROM test_schema.foo;
```

**Change to diff (branch only):**

```sql
DROP VIEW test_schema.foo_v;

ALTER TABLE test_schema.foo
  DROP COLUMN drop_me;

CREATE VIEW test_schema.foo_v AS
SELECT id, keep_me
FROM test_schema.foo;
```

**Expected:** pg-delta emits a dependency-safe plan in this order:

1. `DROP VIEW test_schema.foo_v`
2. `ALTER TABLE test_schema.foo DROP COLUMN drop_me`
3. `CREATE VIEW test_schema.foo_v AS ...`

**Actual (current parity evidence):** pg-delta has analogous coverage for the
`ADD COLUMN` case, but there is no exact `DROP COLUMN` + dependent-view
regression in the current integration suite and no dedicated pg-toolbelt issue
or PR for this case, so the scenario is still not covered by parity evidence.

### Suggested Fix

1. Add an integration regression in:
   - `repos/pg-toolbelt/packages/pg-delta/tests/integration/view-operations.test.ts`
   - or `mixed-objects.test.ts` if that better matches the final implementation
2. Reproduce the exact sequence from pgschema #444 and assert the generated plan
   orders statements as:
   - `DROP VIEW`
   - `ALTER TABLE ... DROP COLUMN`
   - `CREATE VIEW`
3. If the test fails, inspect and update:
   - `src/core/depend.ts`
   - `src/core/objects/view/view.diff.ts`
   - `src/core/sort/expand-replace-dependencies.ts`
   - any sort-phase logic that should promote view teardown ahead of the table
     alteration
4. If implementation lands through the broader dependency-chain work in
   [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263), link
   that issue in the final fix PR and keep the new test as dedicated regression
   coverage for the `DROP COLUMN` variant.

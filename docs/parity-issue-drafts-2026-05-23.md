# Parity issue drafts (2026-05-23)

This document records draft-only text from the 2026-05-23 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. These drafts are saved so
the findings can be reviewed in a PR first and then promoted to real
pg-toolbelt issues only if they still look correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the drafts below, I checked the current open pg-toolbelt issues
and PRs for overlapping work:

- Existing trackers already cover:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Upstream pgschema fix work is now in progress for:
  - pgschema #427 -> [pgschema#428](https://github.com/pgplex/pgschema/pull/428)
- No matching pg-toolbelt issue or PR was found for:
  - pgschema #427
  - pgschema #439

---

## Draft 1 - pgschema #427 (schema-qualified functions in RLS policy expressions)

Relates to pgschema issue #427: https://github.com/pgplex/pgschema/issues/427

Upstream pgschema now also has open fix PR
[#428](https://github.com/pgplex/pgschema/pull/428), so this remains saved as a
draft-only pg-delta parity candidate rather than a duplicate live issue.

### Context

pgschema issue #427 reports that schema-qualified function calls inside RLS
policy expressions, such as `auth.uid()` and `auth.role()`, are dumped and
planned as unqualified `uid()` / `role()` calls. That breaks Supabase-style RLS
policies whose semantics depend on the explicit `auth.` schema qualification.
The new pgschema PR #428 confirms upstream considers this a real bug and is
already carrying a targeted fix for it.

pg-delta's RLS policy extraction currently reads policy expressions using
`pg_get_expr(p.polqual, p.polrelid)` in
`src/core/objects/rls-policy/rls-policy.model.ts`, and the integration tests in
`tests/integration/rls-operations.test.ts` do not cover schema-qualified
external functions in policy expressions. That means the exact parity scenario
is still unverified by regression tests and remains a plausible pg-delta gap.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE ROLE authenticated;

CREATE SCHEMA auth;
CREATE FUNCTION auth.uid()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$ SELECT '00000000-0000-0000-0000-000000000001'::uuid; $$;

CREATE SCHEMA test_schema;
CREATE TABLE test_schema.items (
  id bigint PRIMARY KEY,
  owner_id uuid NOT NULL,
  name text NOT NULL
);

ALTER TABLE test_schema.items ENABLE ROW LEVEL SECURITY;
```

**Change to diff (branch only):**

```sql
CREATE POLICY items_select_own
ON test_schema.items
FOR SELECT
TO authenticated
USING (owner_id = (SELECT auth.uid()));
```

**Expected:** pg-delta emits migration SQL that preserves `auth.uid()` in the
policy expression and roundtrip converges.

**Actual (current parity evidence):** there is no dedicated pg-delta
integration test for schema-qualified external functions in policy expressions,
and the extractor reuses `pg_get_expr(...)` output directly, so qualification
stability is currently unverified.

### Suggested Fix

1. Add a roundtrip regression to
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/rls-operations.test.ts`
   (or `policy-dependencies.test.ts`) covering a policy that calls
   `auth.uid()` or `auth.role()`.
2. Assert that emitted SQL preserves the schema-qualified function call rather
   than normalizing it to an unqualified bare function.
3. If the test fails, adjust RLS policy extraction/serialization in:
   - `src/core/objects/rls-policy/rls-policy.model.ts`
   - `src/core/objects/rls-policy/changes/rls-policy.create.ts`
4. Add a regression assertion ensuring no temporary schema names or lost schema
   qualifiers leak into policy SQL.

---

## Draft 2 - pgschema #439 (constraint replacement with dependents)

Relates to pgschema issue #439: https://github.com/pgplex/pgschema/issues/439

### Context

pgschema issue #439 describes a migration that replaces a `UNIQUE` constraint
with a `PRIMARY KEY` while other objects still depend on the old uniqueness
guarantee. PostgreSQL rejects a plain `DROP CONSTRAINT` in that situation with
`SQLSTATE 2BP01` unless the dependents are removed first or the drop is done
with `CASCADE`.

pg-delta's `AlterTableDropConstraint.serialize()` currently emits
`ALTER TABLE ... DROP CONSTRAINT <name>` without `CASCADE`, and there is no
dedicated integration test that exercises a dependent-constraint teardown /
rebuild flow for `UNIQUE -> PRIMARY KEY` replacement. That makes this a likely
runtime parity gap rather than just a missing coverage hole.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parents (
  code text NOT NULL,
  CONSTRAINT parents_code_key UNIQUE (code)
);

CREATE TABLE test_schema.children (
  id bigint PRIMARY KEY,
  parent_code text NOT NULL,
  CONSTRAINT children_parent_code_fkey
    FOREIGN KEY (parent_code) REFERENCES test_schema.parents (code)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.children
  DROP CONSTRAINT children_parent_code_fkey;

ALTER TABLE test_schema.parents
  DROP CONSTRAINT parents_code_key;

ALTER TABLE test_schema.parents
  ADD CONSTRAINT parents_pkey PRIMARY KEY (code);

ALTER TABLE test_schema.children
  ADD CONSTRAINT children_parent_code_fkey
  FOREIGN KEY (parent_code) REFERENCES test_schema.parents (code);
```

**Expected:** pg-delta plans a dependency-safe teardown and rebuild sequence for
the dependent foreign key around the parent constraint replacement.

**Actual (current parity evidence):** `AlterTableDropConstraint` emits a plain
drop without `CASCADE`, and there is no dedicated integration coverage for this
replacement flow, so the scenario is currently unverified and likely to hit the
same `2BP01` dependency failure.

### Suggested Fix

1. Add an integration test in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   or `dependencies-cycles.test.ts` for `UNIQUE -> PRIMARY KEY` replacement
   when a foreign key depends on the old constraint.
2. Extend dependency expansion / replacement handling so dependent foreign keys
   are explicitly dropped and recreated around the parent constraint change.
3. Inspect and, if needed, update:
   - `src/core/objects/table/table.diff.ts`
   - `src/core/objects/table/changes/table.alter.ts`
   - `src/core/expand-replace-dependencies.ts`
4. Only fall back to `CASCADE` if explicit dependent-object rebuilds are not
   sufficient, because explicit teardown/recreate preserves a more predictable
   migration plan.

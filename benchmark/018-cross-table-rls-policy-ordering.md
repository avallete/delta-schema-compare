# Cross-table RLS policy ordering

> pgschema issue [#373](https://github.com/pgplex/pgschema/issues/373) (closed), fixed by [pgschema#374](https://github.com/pgplex/pgschema/pull/374)

Relates to pgschema issue #373: https://github.com/pgplex/pgschema/issues/373

## Context

pgschema issue #373 reports a migration-ordering bug for row-level security
policies: when a policy on one newly created table references another newly
created table, pgschema used to emit `CREATE POLICY` immediately after the
policy's own table, before the referenced table existed. That causes plan/apply
failures on empty databases for otherwise valid schemas.

pgschema fixed this in PR #374 by adding a targeted deferral path for policies
whose `USING` / `WITH CHECK` expressions reference other newly created tables.
The merged PR also added a regression fixture,
`repos/pgschema/testdata/diff/dependency/issue_373_policy_references_other_table/`,
that exercises the exact failing scenario.

In pg-delta, the closest coverage is
`repos/pg-toolbelt/packages/pg-delta/tests/integration/policy-dependencies.test.ts`,
but those tests only cover policies on their own table and creating a table plus
its policy together. There is no integration case for a policy whose predicate
references a second new table, so the latest cross-table ordering behavior is
not covered.

## Reproduction SQL

```sql
CREATE SCHEMA public;

CREATE TABLE manager (
    id serial PRIMARY KEY,
    user_id uuid NOT NULL
);

ALTER TABLE manager ENABLE ROW LEVEL SECURITY;

CREATE TABLE project_manager (
    id serial PRIMARY KEY,
    project_id integer NOT NULL,
    manager_id integer NOT NULL,
    is_deleted boolean NOT NULL DEFAULT false
);

CREATE POLICY employee_manager_select
ON manager
FOR SELECT
TO PUBLIC
USING (
    id IN (
        SELECT pam.manager_id
        FROM project_manager pam
        WHERE pam.project_id IN (
            SELECT unnest(ARRAY[1, 2, 3])
        )
        AND pam.is_deleted = false
    )
);
```

**Expected:** pg-delta emits migration SQL in an order where `project_manager`
exists before `employee_manager_select` is created.

**Actual:** the exact scenario is not covered by pg-delta integration tests, and
the sort/dependency code does not include an explicit guard for cross-table
references inside policy expressions.

## How pgschema handled it

pgschema PR #374 introduced a policy-specific deferral step: policies that
reference other newly added tables are emitted only after all tables have been
created. The fix relies on inspecting policy expressions and preserving inline
creation only for policies that reference their own table or pre-existing
objects.

The regression fixture added in
`repos/pgschema/testdata/diff/dependency/issue_373_policy_references_other_table/`
demonstrates the exact before/after ordering and locks the behavior in place.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Integration test for policy depending on another new table | ❌ Missing from `tests/integration/policy-dependencies.test.ts` |
| Existing policy dependency tests | ⚠️ Only cover self-table policies and create-table-plus-policy cases |
| RLS policy model stores policy expressions | ✅ `src/core/objects/rls-policy/rls-policy.model.ts` captures `using_expression` / `with_check_expression` |
| Explicit cross-table policy ordering rule | ❌ No dedicated handling found in `src/core/depend.ts` or `src/core/sort/logical-sort.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during review |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Ordering strategy** | Defers only cross-table policies after all tables exist | Groups `rls_policy` with table-adjacent objects and relies on generic dependency ordering |
| **Scenario coverage** | Has a dedicated regression fixture for issue #373 | No integration test for a policy referencing another new table |
| **Policy expression handling** | Uses policy expression inspection to detect new-table references | Stores expressions, but no explicit cross-table ordering check is covered |

## Plan to handle it in pg-delta

1. Add an integration regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/policy-dependencies.test.ts`
   that creates two new tables and a policy on one table that references the
   other.
2. Extend dependency extraction or policy planning in
   `repos/pg-toolbelt/packages/pg-delta/src/core/depend.ts` so policies can
   depend on referenced newly created tables, not only on their owning table.
3. If dependency extraction cannot express the relationship directly, add a
   targeted policy deferral step before final plan ordering, similar in spirit
   to pgschema's issue #373 fix.
4. Re-run the policy dependency integration suite to verify that self-table
   policy ordering remains unchanged while the cross-table case is emitted
   safely.

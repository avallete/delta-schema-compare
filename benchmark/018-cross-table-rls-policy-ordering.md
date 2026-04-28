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

This gap was fixed in pg-delta by
[pg-toolbelt#187](https://github.com/supabase/pg-toolbelt/pull/187), which
teaches `CreateRlsPolicy.requires` to include table references found in policy
expressions. The same PR also added focused regression coverage in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/policy-dependencies.test.ts`
for policies whose `USING` expression references another newly created table.

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

**Current pg-delta behavior:** the referenced table is now ordered before the
policy create statement, and the end-to-end regression test asserts that order.

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
| Integration test for policy depending on another new table | ✅ Present in `tests/integration/policy-dependencies.test.ts` |
| Existing policy dependency tests | ✅ Cover self-table cases and cross-table references |
| RLS policy model stores policy expressions | ✅ `src/core/objects/rls-policy/rls-policy.model.ts` captures `using_expression` / `with_check_expression` |
| Explicit cross-table policy ordering rule | ✅ `CreateRlsPolicy.requires` now tracks referenced relations from policy expressions |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ Fixed by issue [#184](https://github.com/supabase/pg-toolbelt/issues/184) / PR [#187](https://github.com/supabase/pg-toolbelt/pull/187) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Ordering strategy** | Defers only cross-table policies after all tables exist | Adds the missing dependency edge directly to policy creation requirements |
| **Scenario coverage** | Has a dedicated regression fixture for issue #373 | Has dedicated integration regressions for `EXISTS` and multi-table `IN (SELECT ...)` policy references |
| **Policy expression handling** | Uses policy expression inspection to detect new-table references | Parses policy expressions and converts referenced relations into ordering dependencies |

## Resolution in pg-delta

pg-delta now treats referenced relations inside policy expressions as explicit
dependencies. The merged fix in `pg-toolbelt#187` adds regression coverage for
cross-table policy references and verifies the planner emits `CREATE POLICY`
only after referenced new tables exist.

This benchmark entry is therefore retained as historical context, but the parity
gap is now solved in the current pg-delta snapshot.

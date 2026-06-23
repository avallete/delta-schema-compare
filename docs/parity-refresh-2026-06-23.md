# Parity refresh report - 2026-06-23

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `d6b89c26535938291a0512da59e3619aa6f2759f`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-22 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
  - the 2026-06-23 focused diff probe still reports:

    ```json
    {
      "changeCount": 0,
      "sql": []
    }
    ```

  - that still confirms current pg-delta ignores the definition-only change
    from `UNIQUE (a, b)` to `UNIQUE NULLS NOT DISTINCT (a, b)`

## 2) Open-issue screening refresh

No newly-filed open pgschema issues landed after the 2026-06-22 refresh.

### Still-open pgschema issues

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49):
  explicit rename / refactor workflow proposal
  - **not parity work** for pg-delta
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450):
  missing role blocks plan/apply
  - **not parity work** for pg-delta
- pgschema [#471](https://github.com/pgplex/pgschema/issues/471):
  `ENABLE ROW LEVEL SECURITY` on partitioned tables
  - **covered** in current pg-delta
  - the extractor already reads `relrowsecurity` for `relkind in ('r', 'p')`
    and the table diff path already emits `ENABLE/DISABLE ROW LEVEL SECURITY`
  - there is still no dedicated partitioned-parent RLS integration regression,
    but the current live path already converges the scenario
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473):
  partial-index predicate normalization (`IN (...)` vs `= ANY(ARRAY[...])`)
  - **not parity work** for pg-delta

### Newly-closed upstream issues from the recent open-screening set

- pgschema [#472](https://github.com/pgplex/pgschema/issues/472):
  partition-clone child triggers with `.pgschemaignore`
  - now **closed upstream**
  - **not parity work** for pg-delta
- pgschema [#477](https://github.com/pgplex/pgschema/issues/477):
  `CREATE POLICY ... AS RESTRICTIVE`
  - now **closed upstream**
  - **covered** in current pg-delta
- pgschema [#480](https://github.com/pgplex/pgschema/issues/480):
  view / function dependency ordering
  - now **closed upstream**
  - **covered** in current pg-delta
  - the exact `RETURNS vw_users` composite-rowtype case now has focused live
    plan evidence in pg-delta:

    ```json
    {
      "changeCount": 6,
      "sql": [
        "SET check_function_bodies = false",
        "DROP FUNCTION public.fn_create_user(email text)",
        "DROP VIEW public.vw_users",
        "ALTER TABLE public.tb_users ADD COLUMN role text DEFAULT 'member'::text NOT NULL",
        "CREATE VIEW public.vw_users AS SELECT id,\n    email,\n    role,\n    created_at\n   FROM tb_users\n  WHERE (is_deleted = false)",
        "CREATE FUNCTION public.fn_create_user(email text, role text DEFAULT 'member'::text)\n RETURNS vw_users\n LANGUAGE plpgsql\n SECURITY DEFINER\nAS $function$\n    DECLARE\n        v_result vw_users;\n        v_new_id UUID;\n    BEGIN\n        INSERT INTO tb_users (email, role) VALUES (email, role) RETURNING id INTO v_new_id;\n        SELECT id, email, role, created_at INTO v_result FROM vw_users WHERE id = v_new_id;\n        RETURN v_result;\n    END;\n    $function$"
      ]
    }
    ```

  - because the live plan drops the old function and view, rewrites the table,
    recreates the view, and only then recreates the function, no duplicate
    pg-toolbelt issue was drafted
- pgschema [#481](https://github.com/pgplex/pgschema/issues/481):
  repeat-plan drift for trigger `WHEN` expressions with same-schema enum casts
  - now **closed upstream**
  - **not parity work** for pg-delta

## 3) Existing tracked and draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - still resolved upstream
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - still closed upstream as `not_planned`
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still closed upstream
  - still no exact pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - still closed upstream
  - related but non-exact pg-toolbelt work still exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - there is still no exact tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 4) Recent upstream PR closure refresh

- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - now **closed upstream**
  - current pg-delta looks **covered** for the saved MRE
  - the 2026-06-23 focused plan probe produced:

    ```json
    {
      "changeCount": 3,
      "sql": [
        "ALTER TABLE test_schema.child_links DROP CONSTRAINT child_links_parent_variant_fkey",
        "ALTER TABLE test_schema.parent_variants ADD CONSTRAINT parent_variants_parent_entity_id_id_key UNIQUE (parent_entity_id, id)",
        "ALTER TABLE test_schema.child_links ADD CONSTRAINT child_links_parent_variant_fkey FOREIGN KEY (parent_entity_id, parent_variant_id) REFERENCES test_schema.parent_variants(parent_entity_id, id) ON DELETE CASCADE"
      ]
    }
    ```

  - that matches the required order, so the older draft in
    [`docs/parity-issue-drafts-2026-06-17.md`](./parity-issue-drafts-2026-06-17.md)
    is now historical only rather than an active candidate
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478):
  `feat: add support for index storage parameters (reloptions)`
  - now **closed upstream**
  - **covered** in current pg-delta
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  `feat: add support for trigger comments, trigger enabled/disabled state, and
  sequence comments`
  - now **closed upstream**
  - **partially covered** in current pg-delta
  - trigger comments and sequence comments already have coverage, but trigger
    enabled / disabled state still lacks an exact pg-delta tracker
  - the 2026-06-23 focused diff probe still reports:

    ```json
    {
      "changeCount": 1,
      "sql": [
        "CREATE OR REPLACE TRIGGER audit_log_touch_trigger BEFORE INSERT OR UPDATE ON test_schema.audit_log FOR EACH ROW EXECUTE FUNCTION test_schema.audit_log_touch()"
      ]
    }
    ```

  - that remains insufficient because there is still no
    `ALTER TABLE ... DISABLE TRIGGER ...` follow-up
  - the draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)

Existing exact parity trackers remain unchanged:

- pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

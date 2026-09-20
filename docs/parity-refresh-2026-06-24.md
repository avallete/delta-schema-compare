# Parity refresh report - 2026-06-24

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c0e697343afc6116a393df68f14e9a4aee773365`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-23 refresh.

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
  - the 2026-06-24 focused diff probe still reports:

    ```json
    {
      "changeCount": 0,
      "sql": []
    }
    ```

  - that still confirms current pg-delta ignores the definition-only change
    from `UNIQUE (a, b)` to `UNIQUE NULLS NOT DISTINCT (a, b)`

## 2) Open-issue screening refresh

No newly-filed open pgschema issues landed after the 2026-06-23 refresh.

### Still-open reviewed pgschema issues

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49):
  explicit rename / refactor workflow proposal
  - **not parity work** for pg-delta
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450):
  missing role blocks plan/apply
  - **not parity work** for pg-delta

### Newly-closed upstream issues from the recent open-screening set

- pgschema [#471](https://github.com/pgplex/pgschema/issues/471):
  `ENABLE ROW LEVEL SECURITY` on partitioned tables
  - now **closed upstream**
  - **covered** in current pg-delta
  - this reviewed item moved from `benchmark/review-memory.json` `open` to
    `resolved` in this refresh
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473):
  partial-index predicate normalization (`IN (...)` vs `= ANY(ARRAY[...])`)
  - now **closed upstream**
  - **not parity work** for pg-delta
  - this reviewed item moved from `benchmark/review-memory.json` `open` to
    `resolved` in this refresh

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
- duplicate checks for the active unresolved scenarios stayed unchanged:
  - pg-toolbelt issue search for `NULLS NOT DISTINCT` returned no exact tracker
    for benchmark 020
  - pg-toolbelt issue search for trigger enabled / disabled state returned no
    exact tracker for the draft-only pgschema PR #479 slice
  - PR search still only surfaced adjacent dependency work such as
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291)

## 4) Code-head and probe refresh

- `pgschema` advanced to `c0e697343afc6116a393df68f14e9a4aee773365`
  - this includes the upstream fixes that closed pgschema issues #471 and #473
- `pg-delta` advanced to `9284412d71635308ebb0c1537e0b0183d2cfa4da`
  - this head adds trigger quoted-name formatter coverage and a matching
    integration regression
  - it does **not** change the active parity verdicts below

### Rechecked covered cases

- pgschema [#480](https://github.com/pgplex/pgschema/issues/480):
  view / function dependency ordering
  - still **covered** in current pg-delta
  - the 2026-06-24 focused plan probe produced:

    ```json
    {
      "changeCount": 6,
      "sql": [
        "SET check_function_bodies = false",
        "DROP FUNCTION public.fn_create_user(email text)",
        "DROP VIEW public.vw_users",
        "ALTER TABLE public.tb_users ADD COLUMN role text DEFAULT 'member'::text NOT NULL",
        "CREATE VIEW public.vw_users AS SELECT id,\n    email,\n    role,\n    created_at\n   FROM tb_users\n  WHERE (is_deleted = false)",
        "CREATE FUNCTION public.fn_create_user(email text, role text DEFAULT 'member'::text)\n RETURNS vw_users\n LANGUAGE plpgsql\n SECURITY DEFINER\nAS $function$\nDECLARE\n    v_result vw_users;\n    v_new_id UUID;\nBEGIN\n    INSERT INTO tb_users (email, role) VALUES (email, role) RETURNING id INTO v_new_id;\n    SELECT id, email, role, created_at INTO v_result FROM vw_users WHERE id = v_new_id;\n    RETURN v_result;\nEND;\n$function$"
      ]
    }
    ```

  - because the live plan still drops the old function and view, rewrites the
    table, recreates the view, and only then recreates the function, no
    duplicate pg-toolbelt issue was drafted
- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - still **covered** in current pg-delta for the saved MRE
  - the 2026-06-24 focused plan probe produced:

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

### Still-partial draft-only case

- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  `feat: add support for trigger comments, trigger enabled/disabled state, and
  sequence comments`
  - still **partially covered** in current pg-delta
  - trigger comments and sequence comments remain covered
  - trigger enabled / disabled state still lacks an exact pg-delta tracker
  - the 2026-06-24 focused diff probe still reports:

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

## 5) Validation notes

- `bun test packages/pg-delta/src/core/objects/index/index.diff.test.ts packages/pg-delta/src/core/objects/rls-policy/changes/rls-policy.alter.test.ts packages/pg-delta/src/core/objects/trigger/changes/trigger.alter.test.ts packages/pg-delta/src/core/objects/table/table.diff.test.ts packages/pg-delta/src/core/plan/sql-format/format-trigger-quoted-name.test.ts`
  passed (`41 pass`, `0 fail`)
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  passed (`9` tests)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` succeeded
- focused 2026-06-24 pg-delta parity probes against live Postgres containers
  produced:

  ```json
  {
    "nulls_not_distinct": {
      "changeCount": 0,
      "sql": []
    },
    "trigger_enabled_state": {
      "changeCount": 1,
      "sql": [
        "CREATE OR REPLACE TRIGGER audit_log_touch_trigger BEFORE INSERT OR UPDATE ON test_schema.audit_log FOR EACH ROW EXECUTE FUNCTION test_schema.audit_log_touch()"
      ]
    },
    "view_function_recreate": {
      "changeCount": 6,
      "sql": [
        "SET check_function_bodies = false",
        "DROP FUNCTION public.fn_create_user(email text)",
        "DROP VIEW public.vw_users",
        "ALTER TABLE public.tb_users ADD COLUMN role text DEFAULT 'member'::text NOT NULL",
        "CREATE VIEW public.vw_users AS SELECT id,\n    email,\n    role,\n    created_at\n   FROM tb_users\n  WHERE (is_deleted = false)",
        "CREATE FUNCTION public.fn_create_user(email text, role text DEFAULT 'member'::text)\n RETURNS vw_users\n LANGUAGE plpgsql\n SECURITY DEFINER\nAS $function$\nDECLARE\n    v_result vw_users;\n    v_new_id UUID;\nBEGIN\n    INSERT INTO tb_users (email, role) VALUES (email, role) RETURNING id INTO v_new_id;\n    SELECT id, email, role, created_at INTO v_result FROM vw_users WHERE id = v_new_id;\n    RETURN v_result;\nEND;\n$function$"
      ]
    },
    "fk_to_new_unique": {
      "changeCount": 3,
      "sql": [
        "ALTER TABLE test_schema.child_links DROP CONSTRAINT child_links_parent_variant_fkey",
        "ALTER TABLE test_schema.parent_variants ADD CONSTRAINT parent_variants_parent_entity_id_id_key UNIQUE (parent_entity_id, id)",
        "ALTER TABLE test_schema.child_links ADD CONSTRAINT child_links_parent_variant_fkey FOREIGN KEY (parent_entity_id, parent_variant_id) REFERENCES test_schema.parent_variants(parent_entity_id, id) ON DELETE CASCADE"
      ]
    }
  }
  ```

- `DRY_RUN=true python3 scripts/compare_issues.py` returned zero items
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned zero items
- both dry-run scripts still filter on upstream `Bug` / `Feature` labels, so the
  manual unlabeled-issue sweep remains necessary for this repository

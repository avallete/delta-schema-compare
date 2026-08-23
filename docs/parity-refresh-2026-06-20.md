# Parity refresh report - 2026-06-20

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-19 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR found during this refresh
  - a focused diff probe against the current `table.diff.ts` path still reports:

    ```json
    {
      "changeCount": 0,
      "sql": []
    }
    ```

  - that confirms current pg-delta still ignores the definition-only change
    from `UNIQUE (a, b)` to `UNIQUE NULLS NOT DISTINCT (a, b)`

## 2) Existing tracked / draft-only closures remain unchanged

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - still closed upstream as `completed`
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
    [#263](https://github.com/supabase/pg-toolbelt/issues/263),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291)
  - there is still no exact tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 3) Open-issue screening

No new open pgschema issues were filed after the 2026-06-19 refresh.

- pgschema [#477](https://github.com/pgplex/pgschema/issues/477):
  `CREATE POLICY ... AS RESTRICTIVE`
  - **covered** in current pg-delta
  - `rls-policy.model.ts` extracts `pg_policy.polpermissive`
  - `rls-policy.alter.test.ts` covers the drop + create path when permissive
    changes
  - `rls-operations.test.ts` already roundtrips a `CREATE POLICY ...
    AS RESTRICTIVE ...` integration case
- pgschema [#480](https://github.com/pgplex/pgschema/issues/480):
  view / function dependency ordering
  - **likely covered** in current pg-delta; no duplicate tracker drafted in this
    refresh
  - `depend.ts` extracts both view rewrite relation edges and view rewrite
    procedure edges
  - `table-function-dependency-ordering.test.ts` covers `RETURNS SETOF` table
    ordering
  - `function-operations.test.ts` covers function / view ordering and signature
    change cascades through dependent views
  - `view-operations.test.ts` covers drop / recreate ordering when a view's
    shape changes

## 4) Open upstream PR screening

No new upstream PR activity landed after the 2026-06-19 refresh.

- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - still an open upstream PR
  - still no exact pg-toolbelt issue or PR duplicate found
  - existing draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-17.md`](./parity-issue-drafts-2026-06-17.md)
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478):
  `feat: add support for index storage parameters (reloptions)`
  - **covered** in current pg-delta
  - `index.model.ts` reads `reloptions` into `storage_params`
  - `index.diff.ts` emits `ALTER INDEX ... SET/RESET (...)`
  - `index.diff.test.ts` covers storage-parameter diffs
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  `feat: add support for trigger comments, trigger enabled/disabled state, and sequence comments`
  - **partially covered** in current pg-delta
  - trigger comments and sequence comments already have integration coverage
  - trigger enabled / disabled state still lacks an exact pg-delta tracker
  - the current trigger replacement path still serializes:

    ```json
    {
      "changeCount": 1,
      "sql": [
        "CREATE OR REPLACE TRIGGER audit_log_touch_trigger BEFORE INSERT OR UPDATE ON test_schema.audit_log EXECUTE FUNCTION test_schema.audit_log_touch()"
      ]
    }
    ```

    when the only semantic change is `enabled: "O"` -> `enabled: "D"`
  - the existing draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)

## 5) Validation notes

- `bun test packages/pg-delta/src/core/objects/index/index.diff.test.ts packages/pg-delta/src/core/objects/rls-policy/changes/rls-policy.alter.test.ts packages/pg-delta/src/core/objects/trigger/changes/trigger.alter.test.ts packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  passed (`39 pass`, `0 fail`)
- a focused one-off Bun probe against the current source printed:

  ```json
  {
    "nulls_not_distinct": {
      "changeCount": 0,
      "sql": []
    },
    "trigger_enabled_state": {
      "changeCount": 1,
      "sql": [
        "CREATE OR REPLACE TRIGGER audit_log_touch_trigger BEFORE INSERT OR UPDATE ON test_schema.audit_log EXECUTE FUNCTION test_schema.audit_log_touch()"
      ]
    }
  }
  ```

- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  passed
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` succeeded
- `DRY_RUN=true python3 scripts/compare_issues.py` and
  `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  both returned zero items, which remains expected because the scripts still
  filter on upstream `Bug` / `Feature` labels while the newest pgschema items
  are unlabeled

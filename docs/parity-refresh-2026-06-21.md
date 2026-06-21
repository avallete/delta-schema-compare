# Parity refresh report - 2026-06-21

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-20 refresh.

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
  - the June 20 focused diff probe remains the latest runtime evidence because
    the checked-in upstream SHAs are unchanged in this refresh:

    ```json
    {
      "changeCount": 0,
      "sql": []
    }
    ```

  - that still confirms current pg-delta ignores the definition-only change
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
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - there is still no exact tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 3) Open-issue screening

No new open pgschema issues were filed after the 2026-06-20 refresh.

- pgschema [#471](https://github.com/pgplex/pgschema/issues/471):
  `ENABLE ROW LEVEL SECURITY` on partitioned tables
  - **covered** in current pg-delta
- pgschema [#472](https://github.com/pgplex/pgschema/issues/472):
  partition-clone child triggers with `.pgschemaignore`
  - **not parity work** for pg-delta
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473):
  partial-index predicate normalization (`IN (...)` vs `= ANY(ARRAY[...])`)
  - **not parity work** for pg-delta
- pgschema [#477](https://github.com/pgplex/pgschema/issues/477):
  `CREATE POLICY ... AS RESTRICTIVE`
  - **covered** in current pg-delta
- pgschema [#480](https://github.com/pgplex/pgschema/issues/480):
  view / function dependency ordering
  - **likely covered** in current pg-delta; no duplicate tracker drafted in
    this refresh

## 4) Duplicate-check / pg-toolbelt watch

No new exact pg-toolbelt issue or PR duplicates landed after the 2026-06-20
refresh.

- Existing exact parity trackers remain:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Newer pg-toolbelt issues
  [#286](https://github.com/supabase/pg-toolbelt/issues/286) and
  [#301](https://github.com/supabase/pg-toolbelt/issues/301) were checked
  during this refresh. They are adjacent dependency/materialized-view work, but
  neither is an exact duplicate of benchmark 020 or the saved draft-only gaps.
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479) still remains a
  **draft-only pg-delta parity candidate** for trigger enabled / disabled
  state. The saved issue body remains in
  [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)
- pg-toolbelt [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains
  an open draft rewrite and should not be used to change the current benchmark
  status yet

## 5) Validation posture

- The checked-in submodules did not move between the 2026-06-20 and 2026-06-21
  refreshes, so the June 20 runtime evidence for benchmark 020 and the draft-
  only trigger enabled-state gap remains directly applicable in this refresh.
- This refresh therefore focuses on live issue / PR state and duplicate
  detection rather than introducing a new benchmark-status change.

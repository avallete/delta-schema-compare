# Parity refresh report - 2026-06-22

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-21 refresh.

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
  - the 2026-06-22 focused diff probe still reports:

    ```json
    {
      "changeCount": 0,
      "sql": []
    }
    ```

  - that still confirms current pg-delta ignores the definition-only change
    from `UNIQUE (a, b)` to `UNIQUE NULLS NOT DISTINCT (a, b)`

## 2) Open-issue screening bookkeeping

No newly-filed open pgschema issues landed after the 2026-06-21 refresh.

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
  - **likely covered** in current pg-delta
  - no duplicate tracker was drafted because the current evidence is
    architectural + adjacent-test coverage rather than an exact integration
    repro of the `RETURNS vw_users` composite-rowtype case

### Newly-closed upstream issues carried forward from prior open screening

- the following items are now **closed upstream and covered** in current
  pg-delta: **#362**, **#401**, **#414**, **#415**, **#416**, **#420**,
  **#427**, and **#436**
- the following items are now **closed upstream and still not parity work** for
  pg-delta: **#407**, **#409**, **#418**, **#419**, **#421**, **#422**,
  **#429**, **#447**, and **#449**

## 3) Existing tracked / draft-only closures remain unchanged

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

## 4) Open upstream PR watch / duplicate check

No new parity-relevant upstream PR activity landed after the 2026-06-21
refresh.

- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - still an open upstream PR
  - still no exact pg-toolbelt issue or PR duplicate found
  - existing draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-17.md`](./parity-issue-drafts-2026-06-17.md)
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478):
  `feat: add support for index storage parameters (reloptions)`
  - **covered** in current pg-delta
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  `feat: add support for trigger comments, trigger enabled/disabled state, and
  sequence comments`
  - **partially covered** in current pg-delta
  - trigger comments and sequence comments already have integration coverage
  - trigger enabled / disabled state still lacks an exact pg-delta tracker
  - the existing draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)

Existing exact parity trackers remain unchanged:

- pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

No exact pg-toolbelt issue or PR was found for benchmark **020**, pgschema
issue **#480**, or the trigger enabled-state slice of pgschema PR **#479**.

## 5) Validation notes

Validation results are recorded in the follow-up validation commit for this
refresh.

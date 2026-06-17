# Parity refresh report - 2026-06-17

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-07 refresh.

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
  - current pg-delta still ignores this definition-only difference in the table
    constraint path

## 2) Upstream issue-state delta since 2026-06-07

### Closed upstream, still tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - closed upstream on 2026-06-09
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - closed upstream on 2026-06-09
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Closed upstream, still uncovered, still unduplicated

- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - closed upstream on 2026-06-10 via pgschema PR
    [#470](https://github.com/pgplex/pgschema/pull/470)
  - still no exact pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - closed upstream on 2026-06-10 via pgschema PR
    [#466](https://github.com/pgplex/pgschema/pull/466)
  - related but non-exact pg-toolbelt work exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291)
  - there is still no exact tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 3) New open-item screening

- pgschema [#471](https://github.com/pgplex/pgschema/issues/471):
  partitioned-table `ENABLE ROW LEVEL SECURITY`
  - **covered** in current pg-delta's table extraction / diff path
  - `table.model.ts` reads `relrowsecurity` for both regular and partitioned
    tables, `table.diff.ts` emits `ENABLE / DISABLE ROW LEVEL SECURITY`, and
    the generic RLS roundtrip path remains covered by `rls-operations.test.ts`
- pgschema [#472](https://github.com/pgplex/pgschema/issues/472):
  ignored child-trigger dumping with `.pgschemaignore`
  - **not parity work for pg-delta**
  - this is specific to pgschema's ignore-file filtering and partition-clone
    dump behavior
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473):
  partial-index predicate normalization (`IN (...)` vs `= ANY (ARRAY[...])`)
  - **not parity work for pg-delta**
  - pg-delta compares live catalog predicates through `pg_get_expr(i.indpred,
    i.indrelid)` instead of comparing rendered dump text

## 4) Open upstream PR watch / draft-only candidate

- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - open upstream PR created on 2026-06-12
  - no exact pg-toolbelt issue or PR duplicate found
  - a draft-only pg-delta issue body is saved in
    [`docs/parity-issue-drafts-2026-06-17.md`](./parity-issue-drafts-2026-06-17.md)

## 5) Validation notes

Validation details are added after local checks run on this branch.

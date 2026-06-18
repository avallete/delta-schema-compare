# Parity refresh report - 2026-06-18

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-17 refresh.

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

## 2) Carry-over state still true on 2026-06-18

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

### Still-open issues previously screened

- pgschema [#471](https://github.com/pgplex/pgschema/issues/471):
  partitioned-table `ENABLE ROW LEVEL SECURITY`
  - **covered** in current pg-delta's table extraction / diff path
- pgschema [#472](https://github.com/pgplex/pgschema/issues/472):
  ignored child-trigger dumping with `.pgschemaignore`
  - **not parity work for pg-delta**
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473):
  partial-index predicate normalization (`IN (...)` vs `= ANY (ARRAY[...])`)
  - **not parity work for pg-delta**

## 3) Newly screened open issues on 2026-06-18

- pgschema [#477](https://github.com/pgplex/pgschema/issues/477):
  `AS RESTRICTIVE` on `CREATE POLICY`
  - **covered** in current pg-delta
  - policy extraction preserves `polpermissive`, `CREATE POLICY` serialization
    emits `AS RESTRICTIVE`, and `rls-operations.test.ts` already roundtrips the
    exact clause
- pgschema [#480](https://github.com/pgplex/pgschema/issues/480):
  dependency ordering on table -> view -> function chains
  - **overlapping active pg-toolbelt dependency-replacement work**
  - current open work in [#263](https://github.com/supabase/pg-toolbelt/issues/263),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) overlaps the
    reported drop / recreate ordering path
  - there is still no exact dedicated regression for the view-returning-
    function chain, so no new duplicate draft was added yet

## 4) Open upstream PR watch list refresh

- pgschema [#474](https://github.com/pgplex/pgschema/pull/474):
  `fix: avoid substring matches in policy table dependency detection`
  - **covered** in current pg-delta
  - policy dependencies come from live `pg_depend` extraction rather than
    substring scanning, and `policy-dependencies.test.ts` already covers
    multi-table, function, and view dependency ordering
- pgschema [#475](https://github.com/pgplex/pgschema/pull/475):
  `fix: order modified foreign keys after added unique constraints`
  - still an **uncovered draft-only pg-delta parity candidate**
  - no exact pg-toolbelt issue or PR duplicate found
  - candidate issue body remains in
    [`docs/parity-issue-drafts-2026-06-17.md`](./parity-issue-drafts-2026-06-17.md)
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478):
  `feat: add support for index storage parameters (reloptions)`
  - **covered** in current pg-delta's index path
  - `index.model.ts` reads `reloptions` into `storage_params`,
    `index.diff.ts` emits `AlterIndexSetStorageParams`, and `index.alter.ts`
    serializes `ALTER INDEX ... SET/RESET (...)`
  - no duplicate tracker or draft was added
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  `feat: add support for trigger comments, trigger enabled/disabled state, and sequence comments`
  - **partially covered** in current pg-delta
  - trigger comments and sequence comments already roundtrip in pg-delta
  - trigger enabled / disabled state is still missing an apply path because
    `tgenabled` drift triggers replacement while the generated SQL never emits
    `ALTER TABLE ... ENABLE/DISABLE TRIGGER`
  - a new draft-only issue body for that remaining gap is saved in
    [`docs/parity-issue-drafts-2026-06-18.md`](./parity-issue-drafts-2026-06-18.md)

## 5) Validation notes

Validation commands and results were added after the post-edit verification
step.

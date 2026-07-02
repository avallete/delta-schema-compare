# Parity refresh report - 2026-07-02

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-07-01 refresh.

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
  - benchmark 020 remains the only active resolved-issue gap

## 2) Upstream delta on 2026-07-02

There is no upstream code-head delta versus the 2026-07-01 refresh:

- `git submodule update --remote --merge` kept `pgschema` at
  `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads for updates after `2026-07-01T07:35:00Z` again found no
newer pgschema issue or PR activity.

On the pg-toolbelt side, newer open PR activity now includes:

- [#285](https://github.com/supabase/pg-toolbelt/pull/285), updated
  `2026-07-02T06:57:21Z`
- [#288](https://github.com/supabase/pg-toolbelt/pull/288), updated
  `2026-07-02T04:50:15Z`
- [#291](https://github.com/supabase/pg-toolbelt/pull/291), updated
  `2026-07-01T14:00:00Z`
- [#307](https://github.com/supabase/pg-toolbelt/pull/307), updated
  `2026-07-01T14:52:38Z`
- [#316](https://github.com/supabase/pg-toolbelt/pull/316), updated
  `2026-07-01T12:45:58Z`

None of those PRs changes the parity verdict set:

- **#285** remains the exact in-flight tracker for the trigger enabled /
  disabled-state slice from pgschema PR #479
- **#288** (range-type creation dependencies), **#291** (procedure expression
  dependents), **#307** (`pg-delta-next` work), and **#316** (leading enum
  additions) remain adjacent rather than exact duplicates of benchmark 020 or
  the current draft-only parity items

## 3) Existing tracked and draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - latest check: still `OPEN`, last updated `2026-06-18T20:04:11Z`
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - latest check: still `OPEN`, last updated `2026-04-22T17:38:52Z`
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
  - related pg-toolbelt work exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - current pg-delta coverage is still only exact for the
    `ALTER COLUMN TYPE` + dependent-view ordering case, not this destructive
    `DROP COLUMN` ordering case
  - there is still no exact tracker, so the saved draft remains active context
    in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  trigger comments, trigger enabled/disabled state, and sequence comments
  - still **partially covered** in current pg-delta
  - trigger comments and sequence comments remain covered on current `main`
  - the remaining trigger enabled / disabled state slice is still **tracked
    in-flight** by open
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
  - latest check: PR #285 is still `OPEN`, `mergeable_state=blocked`, updated
    `2026-07-02T06:57:21Z`
  - no new pg-toolbelt tracker should be drafted while #285 remains open

## 4) What changed in this refresh

This is a latest-state reconciliation pass rather than a parity-state change:

- advance `benchmark/README.md` to the 2026-07-02 snapshot date
- refresh the July note in
  `benchmark/020-unique-constraint-nulls-not-distinct.md`
- refresh `reviewed_at` for the active `benchmark/review-memory.json` entries:
  `#49`, `#52`, `#84`, `#450`, `#493`, `#366`, `#404`, `#412`, `#439`, `#444`
- add this dated report

No benchmark verdicts changed in this refresh.

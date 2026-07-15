# Parity refresh report - 2026-07-15

This report records the 2026-07-15 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)
- live `pg-toolbelt` `main` (`d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`), which still differs from the checked-in baseline only in CI / repo-meta files

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-14.md`](./parity-refresh-2026-07-14.md).

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Active resolved-issue benchmark gaps

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#499](https://github.com/pgplex/pgschema/issues/499):
  child-specific column overrides in `PARTITION OF` create path
  - benchmark file:
    [`benchmark/021-partition-child-column-overrides.md`](../benchmark/021-partition-child-column-overrides.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501):
  PostgreSQL 18 `VIRTUAL` generated columns
  - benchmark file:
    [`benchmark/022-virtual-generated-columns.md`](../benchmark/022-virtual-generated-columns.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#506](https://github.com/pgplex/pgschema/issues/506):
  new-table FK ordered before a standalone unique index on the referenced table
  - benchmark file:
    [`benchmark/023-fk-before-standalone-unique-index.md`](../benchmark/023-fk-before-standalone-unique-index.md)
  - no matching pg-toolbelt issue or PR was found through this refresh

## 2) Upstream delta on 2026-07-15

This refresh found **no new pgschema issue movement** after the 2026-07-14
sweep and **no pg-delta engine delta** relative to the checked-in benchmark
baseline:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- the current open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493)
- the latest closed parity-relevant pgschema issues are still
  [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501),
  [#505](https://github.com/pgplex/pgschema/issues/505),
  [#506](https://github.com/pgplex/pgschema/issues/506),
  [#508](https://github.com/pgplex/pgschema/issues/508), and
  [#509](https://github.com/pgplex/pgschema/issues/509)
- direct issue-page checks confirm the older tracked and draft-only resolved
  items keep the same parity state:
  - [#366](https://github.com/pgplex/pgschema/issues/366) remains closed as
    `not_planned` and is still tracked by
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - [#404](https://github.com/pgplex/pgschema/issues/404) remains closed as
    completed and is still tracked by
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - [#412](https://github.com/pgplex/pgschema/issues/412),
    [#439](https://github.com/pgplex/pgschema/issues/439), and
    [#444](https://github.com/pgplex/pgschema/issues/444) remain resolved
    upstream with no exact pg-toolbelt issue or PR
- checked-in `pg-delta` remains
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`, while live `pg-toolbelt` `main`
  remains `d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`
- the diff between those two pg-toolbelt SHAs is still limited to CI /
  repo-meta files:
  - `.github/MAINTAINERS.md`
  - `.github/scripts/contribution-gate.test.ts`
  - `.github/scripts/contribution-gate.ts`
  - `.github/workflows/contribution-gate.yml`
- no `packages/pg-delta/**` source files or pg-delta integration tests changed,
  so benchmarks **020**, **021**, **022**, and **023** keep the same
  `Not covered` verdicts
- exact open pg-toolbelt trackers still exist only for
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- the latest pg-toolbelt tracker state is still non-duplicative and unresolved:
  - [#218](https://github.com/supabase/pg-toolbelt/issues/218) remains
    issue-only with no PR
  - [#219](https://github.com/supabase/pg-toolbelt/issues/219) remains open
    with no exact matching PR
  - adjacent function-privilege work in
    [#308](https://github.com/supabase/pg-toolbelt/issues/308) /
    [#310](https://github.com/supabase/pg-toolbelt/pull/310) still targets
    `REVOKE EXECUTE ... FROM PUBLIC`, not the enum-argument signature parity gap
- no new exact pg-toolbelt issue or PR was found for benchmarks **020**, **021**,
  **022**, or **023**, nor for the older draft-only resolved items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- the only adjacent pg-toolbelt state change versus the 2026-07-14 sweep is
  that [#329](https://github.com/supabase/pg-toolbelt/pull/329) is now
  **closed**. Its scope remains non-superuser Supabase profile apply behavior
  rather than any active or draft-only pgschema parity gap
- currently open adjacent pg-toolbelt work therefore remains non-duplicative:
  - [#263](https://github.com/supabase/pg-toolbelt/issues/263) is still an
    open issue for a different dependency-chain scenario
  - [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains the open
    `pg-delta-next` promotion PR

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix and checked-in submodule pointers unchanged and records the
result as another dated no-delta report:

- add this report as the 2026-07-15 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up and records that the 2026-07-15 sweep again found no benchmark or
  upstream parity delta
- refresh the reviewed timestamps in `benchmark/review-memory.json` for the
  rechecked open, tracked, active-gap, and draft-only items

## 4) Validation notes

Validation results are appended after the targeted checks complete.

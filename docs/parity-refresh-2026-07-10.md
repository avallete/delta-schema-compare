# Parity refresh report - 2026-07-10

This report records the 2026-07-10 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)
- live `pg-toolbelt` `main` (`d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`), which is one CI-only commit ahead of the checked-in baseline

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-09.md`](./parity-refresh-2026-07-09.md).

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

## 2) Upstream delta on 2026-07-10

This refresh found **no parity-relevant upstream movement** after the
2026-07-09 sweep:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`, which
  is identical to the checked-in benchmark snapshot
- checked-in `pg-delta` remains
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`, while live `pg-toolbelt` `main`
  advanced to `d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`
- the diff between those two pg-toolbelt SHAs touches only CI / repo-meta files:
  - `.github/MAINTAINERS.md`
  - `.github/scripts/contribution-gate.test.ts`
  - `.github/scripts/contribution-gate.ts`
  - `.github/workflows/contribution-gate.yml`
- no `packages/pg-delta/**` source files or pg-delta integration tests changed,
  so benchmarks **020**, **021**, **022**, and **023** keep the same
  `Not covered` verdicts
- the highest live pgschema issue number remains **#509**, while **#513** and
  **#514** still return `404`
- pgschema [#404](https://github.com/pgplex/pgschema/issues/404),
  [#412](https://github.com/pgplex/pgschema/issues/412),
  [#439](https://github.com/pgplex/pgschema/issues/439),
  [#444](https://github.com/pgplex/pgschema/issues/444),
  [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501), and
  [#506](https://github.com/pgplex/pgschema/issues/506) remain closed with no
  new parity-state change
- exact open pg-toolbelt trackers still exist only for
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- no new exact pg-toolbelt issue or PR was found for benchmarks **020**, **021**,
  **022**, or **023**, nor for the older draft-only resolved items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix, review-memory cache, and checked-in submodule pointers
unchanged and records the result as a dated no-delta report:

- add this report as the 2026-07-10 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up
- intentionally leave `benchmark/review-memory.json` untouched because the only
  upstream code movement since 2026-07-09 is a CI-only pg-toolbelt commit
  outside `packages/pg-delta`

## 4) Validation notes

This refresh was validated with:

- live upstream SHA checks showing `pgschema` unchanged and `pg-toolbelt` ahead
  only by a CI-only `.github/**` diff
- targeted live GitHub issue-state checks for pgschema **#404**, **#412**,
  **#439**, **#444**, **#499**, **#501**, **#506**, and **#509**, plus
  pg-toolbelt **#218** and **#219**
- direct confirmation that pgschema **#513** and **#514** still do not exist
- repository maintenance checks (`benchmark/review-memory.json` JSON parsing,
  targeted repository tests, and dry-run compare scripts)

The unlabeled-issue caveat still applies: the parity-relevant pgschema issues
remain mostly unlabeled, so `compare_issues.py` and `compare_resolved.py` can
still return zero candidates even when the manual latest-state sweep finds
useful parity updates.

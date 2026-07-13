# Parity refresh report - 2026-07-13

This report records the 2026-07-13 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)
- live `pg-toolbelt` `main` (`d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`), which is still the same CI-only commit ahead already seen on 2026-07-10, 2026-07-11, and 2026-07-12

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-12.md`](./parity-refresh-2026-07-12.md).

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

## 2) Upstream delta on 2026-07-13

This refresh found **no new upstream parity movement** after the 2026-07-12
sweep:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- the highest live pgschema issue remains **#509**; higher visible numbers
  **#510**, **#511**, and **#512** are PRs rather than issues, and **#513+**
  still do not exist
- rechecked pgschema [#404](https://github.com/pgplex/pgschema/issues/404),
  [#412](https://github.com/pgplex/pgschema/issues/412),
  [#439](https://github.com/pgplex/pgschema/issues/439),
  [#444](https://github.com/pgplex/pgschema/issues/444),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501),
  [#505](https://github.com/pgplex/pgschema/issues/505),
  [#506](https://github.com/pgplex/pgschema/issues/506),
  [#508](https://github.com/pgplex/pgschema/issues/508), and
  [#509](https://github.com/pgplex/pgschema/issues/509): each retains the same
  state and `updatedAt` value recorded on 2026-07-12
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
- no new exact pg-toolbelt issue or PR was found for benchmarks **020**, **021**,
  **022**, or **023**, nor for the older draft-only resolved items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- currently open adjacent pg-toolbelt work remains non-duplicative:
  - [#263](https://github.com/supabase/pg-toolbelt/issues/263) is still an
    exact issue for a different dependency-chain scenario
  - [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains an open
    `pg-delta-next` promotion PR
  - [#329](https://github.com/supabase/pg-toolbelt/pull/329) remains open, but
    its scope is non-superuser Supabase profile apply behavior rather than any
    active pgschema parity gap

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix and checked-in submodule pointers unchanged and records the
result as another dated no-delta report:

- add this report as the 2026-07-13 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up and records that the 2026-07-13 sweep again found no benchmark or
  upstream parity delta after 2026-07-12
- refresh the reviewed timestamps in `benchmark/review-memory.json` for the
  rechecked open, tracked, active-gap, and draft-only items

## 4) Validation notes

This refresh was validated with:

- live GitHub issue / PR checks for pgschema **#404**, **#412**, **#439**,
  **#444**, **#450**, **#493**, **#499**, **#501**, **#505**, **#506**,
  **#508**, and **#509**
- live GitHub issue / PR checks for pg-toolbelt **#218**, **#219**, **#263**,
  **#299**, and **#329**
- direct git diff of live pg-toolbelt `main` versus the checked-in baseline,
  confirming the same CI-only `.github/**` delta as the 2026-07-12 sweep
- targeted pg-delta unit tests:
  - `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  - `bun test packages/pg-delta/src/core/objects/table/changes/table.create.test.ts`
  - `bun test packages/pg-delta/src/core/sort/sort-changes.test.ts`
  - `bun test packages/pg-delta/src/core/objects/index/index.diff.test.ts`
  - result: **37 pass / 0 fail**
- repository maintenance checks:
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `git diff --check`
  - results:
    - `benchmark/review-memory.json` parsed successfully
    - Python tests: **9 pass / 0 fail**
    - `compare_issues.py`: **0** open issues processed
    - `compare_resolved.py`: **0** resolved issues processed
    - working tree remained clean after validation

The unlabeled-issue caveat still applies: the parity-relevant pgschema issues
remain mostly unlabeled, so `compare_issues.py` and `compare_resolved.py` can
still return zero candidates even when the manual latest-state sweep finds
useful parity updates.

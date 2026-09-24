# Parity refresh report - 2026-07-09

This report records the 2026-07-09 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-08.md`](./parity-refresh-2026-07-08.md).

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

## 2) Upstream delta on 2026-07-09

This refresh found **no code-head delta** in either submodule versus the
2026-07-08 snapshot:

- `pg-delta` remains `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `pgschema` remains `e18d9ede7973537919c02f25eced5c97271af1dc`

Targeted upstream reads also found **no new parity-relevant pgschema movement**
after the prior refresh:

- the highest live pgschema issue number remains **#509**
- the highest merged pgschema parity-relevant PR remains **#512**
- the current open-issue screening set remains unchanged: **#49**, **#52**,
  **#84**, **#450**, and **#493** are still open and remain **not parity work
  for pg-delta**
- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) and
  [#366](https://github.com/pgplex/pgschema/issues/366) remain **closed
  upstream**, while their exact pg-toolbelt trackers remain open:
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- resolved pgschema [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444) still have **no exact
  pg-toolbelt tracker**

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix and review-memory cache unchanged and records the result as a
dated no-delta report:

- add this report as the 2026-07-09 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  no-change follow-up
- intentionally leave `benchmark/review-memory.json` untouched because both the
  reviewed verdicts and the checked-in submodule SHAs are unchanged from the
  2026-07-08 refresh

## 4) Validation notes

This refresh was validated with:

- live upstream issue / PR checks to confirm there is no new parity-relevant
  pgschema movement after 2026-07-08
- repository-local verification that the checked-in submodule SHAs still match
  the 2026-07-08 snapshot
- repo maintenance checks (`benchmark/review-memory.json` JSON parsing, targeted
  repository tests, and dry-run compare scripts)

The unlabeled-issue caveat still applies: the parity-relevant pgschema issues
remain mostly unlabeled, so `compare_issues.py` and `compare_resolved.py` can
still return zero candidates even when the manual latest-state sweep finds
useful parity updates.

# Parity refresh report - 2026-07-23

This report records the 2026-07-23 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-22.md`](./parity-refresh-2026-07-22.md).

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

## 2) Upstream delta on 2026-07-23

This refresh found **no pg-delta code-head delta** relative to the
2026-07-22 sweep, but it did find a small **pgschema code-head** delta and a
small **pg-toolbelt PR-state** delta:

- `pgschema` `main` advanced from
  `5f2b37bae6d51068b3a3b05fec3185c4219f8968` to
  `a0acf0b9590a6bd7b3455d795f7e547490aa9699` via merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514)
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still matches it exactly
- pgschema [#493](https://github.com/pgplex/pgschema/issues/493) remains
  **open**, but merged pgschema PR #514 only extends dump-side
  `--qualify-schema` handling for same-schema type references. The remaining
  function / procedure parameter and return-type slices are still outstanding
  upstream, and the issue still remains **not parity work** for pg-delta
  because it does not change live-catalog diff or planner behavior
- the current open pgschema issue set still remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493)
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pg-toolbelt [#356](https://github.com/supabase/pg-toolbelt/pull/356) is now
  **merged** while [#355](https://github.com/supabase/pg-toolbelt/pull/355)
  remains **open**
- direct issue / PR rechecks confirm
  [#286](https://github.com/supabase/pg-toolbelt/issues/286),
  [#344](https://github.com/supabase/pg-toolbelt/issues/344),
  [#346](https://github.com/supabase/pg-toolbelt/issues/346),
  [#355](https://github.com/supabase/pg-toolbelt/pull/355), and
  [#356](https://github.com/supabase/pg-toolbelt/pull/356) are still adjacent
  rather than exact duplicates for benchmarks **020** through **023** or the
  older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The real 2026-07-23 delta is state
reconciliation around the latest upstream merges:

- advance the checked-in `repos/pgschema` submodule from
  `5f2b37bae6d51068b3a3b05fec3185c4219f8968` to
  `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- add this report as the 2026-07-23 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth matrix records merged
  pgschema PR #514, merged pg-toolbelt PR #356, and the current
  non-overlapping duplicate-check state
- refresh the review-memory fingerprints / reviewed timestamps for the
  rechecked open, tracked, active-gap, and older draft-only items

## 4) Validation notes

- Repo-local validation results will be recorded after the focused branch
  checks run for this refresh.

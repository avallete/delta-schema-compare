# Parity refresh report - 2026-07-24

This report records the 2026-07-24 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-23.md`](./parity-refresh-2026-07-23.md).

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

## 2) Upstream delta on 2026-07-24

This refresh found **no code-head delta in either upstream repo** relative to
the 2026-07-23 sweep:

- `pgschema` `main` still remains `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still matches it exactly
- the current open pgschema issue set is unchanged at
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493)
- pgschema [#493](https://github.com/pgplex/pgschema/issues/493) remains
  **open** and still **not parity work** for pg-delta. Merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514) remains the most
  recent upstream code change here, but it only extends dump-side
  `--qualify-schema` handling for same-schema type references; the remaining
  function / procedure parameter and return-type slices are still outstanding
  upstream and still do not change current pg-delta parity classification
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pg-toolbelt [#355](https://github.com/supabase/pg-toolbelt/pull/355) and
  [#358](https://github.com/supabase/pg-toolbelt/pull/358) are now **merged**,
  while [#357](https://github.com/supabase/pg-toolbelt/pull/357) is **open**
  and issue [#308](https://github.com/supabase/pg-toolbelt/issues/308) was
  updated
- direct issue / PR rechecks confirm
  [#286](https://github.com/supabase/pg-toolbelt/issues/286),
  [#308](https://github.com/supabase/pg-toolbelt/issues/308),
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#333](https://github.com/supabase/pg-toolbelt/issues/333),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#340](https://github.com/supabase/pg-toolbelt/issues/340),
  [#344](https://github.com/supabase/pg-toolbelt/issues/344),
  [#346](https://github.com/supabase/pg-toolbelt/issues/346),
  [#310](https://github.com/supabase/pg-toolbelt/pull/310),
  [#357](https://github.com/supabase/pg-toolbelt/pull/357), and
  [#358](https://github.com/supabase/pg-toolbelt/pull/358) remain adjacent
  rather than exact duplicates for benchmarks **020** through **023** or the
  older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The real 2026-07-24 delta is
state-reconciliation around the latest pg-toolbelt issue / PR churn:

- add this report as the 2026-07-24 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged upstream code heads, the unchanged open pgschema issue set, and the
  latest adjacent pg-toolbelt issue / PR states
- leave `benchmark/review-memory.json` unchanged because none of the reviewed
  pgschema issue fingerprints moved: `issue_updated_at`, checked-in `pg-delta`
  SHA, and checked-in `pgschema` SHA are all unchanged versus the 2026-07-23
  sweep

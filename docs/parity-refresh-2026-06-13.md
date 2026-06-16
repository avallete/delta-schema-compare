# Parity refresh report - 2026-06-13

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-12 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no exact pg-toolbelt issue or PR found during this refresh
  - current pg-delta still ignores the definition-only difference in the table
    constraint path (see validation note below)

## 2) Upstream movement since 2026-06-12

`pgschema` did not move beyond `8b7a248c...` during this refresh window.
`pg-toolbelt` advanced by six commits from `436b3d19...` to `c06f0812...`, but
the changes were not on the tracked parity surfaces:

- [pg-toolbelt#289](https://github.com/supabase/pg-toolbelt/pull/289) -
  pg-topo `ALTER PUBLICATION` / `ALTER SUBSCRIPTION`
- [pg-toolbelt#293](https://github.com/supabase/pg-toolbelt/pull/293) -
  execution-aware migration units
- [pg-toolbelt#294](https://github.com/supabase/pg-toolbelt/pull/294) -
  `COMMENT ON RULE` dependencies
- [pg-toolbelt#295](https://github.com/supabase/pg-toolbelt/pull/295) -
  publication FK-chain cycle handling

Those changes do not alter the current parity verdicts for benchmark 020, the
open parity trackers, or the historical draft-only gaps.

## 3) Open pgschema issue refresh

The issue-level screening set is unchanged from 2026-06-12:

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49): explicit rename
  / refactor workflow proposal - **not parity** for pg-delta
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450): missing role
  blocks plan/apply - **not parity** for pg-delta
- pgschema [#471](https://github.com/pgplex/pgschema/issues/471): partitioned
  table RLS enablement - **covered** in current pg-delta's generic table RLS
  extraction and diff path
- pgschema [#472](https://github.com/pgplex/pgschema/issues/472): partition
  clone triggers with ignored child tables - **not parity** for pg-delta
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473): partial-index
  predicate normalization (`IN (...)` vs `= ANY(ARRAY)`) - **not parity** for
  pg-delta

No new parity-relevant pgschema issues appeared after #473. Two new upstream
pull requests are worth noting, but neither changes the issue-level verdict:

- [pgschema#474](https://github.com/pgplex/pgschema/pull/474) addresses
  temp-schema dependency false positives around RLS policy parsing - **not
  parity** for pg-delta
- [pgschema#475](https://github.com/pgplex/pgschema/pull/475) is adjacent to
  the historical [#439](https://github.com/pgplex/pgschema/issues/439)
  dependency-replacement scenario, but pg-delta still has no exact tracker for
  that gap

### Historical gaps still tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) is closed
  upstream via [pgschema#458](https://github.com/pgplex/pgschema/pull/458), but
  the matching pg-delta parity tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218) remains
  open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) is closed
  upstream after the temp-schema signature fix landed via
  [pgschema#379](https://github.com/pgplex/pgschema/pull/379), but the matching
  pg-delta parity tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219) remains
  open

### Historical draft-only gaps with no exact pg-toolbelt tracker

- pgschema [#439](https://github.com/pgplex/pgschema/issues/439): replacing
  `UNIQUE` with `PRIMARY KEY` when dependents still point at the old constraint
  - still no exact pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  before dropping a dependent view in the same plan group
  - still no exact pg-toolbelt issue or PR found
  - related but non-duplicate work remains in
    [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263),
    merged PR [#273](https://github.com/supabase/pg-toolbelt/pull/273), and
    merged PR [#275](https://github.com/supabase/pg-toolbelt/pull/275)
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 4) Validation notes

- `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  passed on current `pg-delta@c06f081208c067e9aab5a4f9b109cd2f5546bbc1`
- a focused one-off Bun probe constructed two otherwise-identical table
  constraints whose only difference was `UNIQUE (a, b)` versus
  `UNIQUE NULLS NOT DISTINCT (a, b)`. The current diff code still returned:

  ```json
  {
    "changeCount": 0,
    "sql": []
  }
  ```

  That reproduces the unresolved benchmark 020 behavior on the current
  `pg-delta` head without needing a Docker-backed integration environment.
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  passed
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` passed
- `DRY_RUN=true python3 scripts/compare_issues.py` and
  `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  both returned zero items once authenticated, which remains expected because
  most current pgschema issues are unlabeled and those scripts still filter on
  the `Bug` / `Feature` labels

## 5) Metadata refresh note

This refresh is still mostly about upstream state tracking rather than a
pg-delta code change. `benchmark/review-memory.json` now refreshes the active
tracked entries to `pgschema@8b7a248ce08f155b43b31cdee9ea38751aff6d5d` /
`pg-delta@c06f081208c067e9aab5a4f9b109cd2f5546bbc1`, specifically:

- open-screening entries #49, #450, #471, #472, and #473
- tracked historical parity items #366 and #404
- unresolved historical gaps #412, #439, and #444

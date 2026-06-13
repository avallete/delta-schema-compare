# Parity refresh report - 2026-06-08

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `592c19c95b06830255b45bc4d80eeacd62e7e727`)
- `pg-delta` (`repos/pg-toolbelt` @ `f95e0a8b773539dfb60ebf541131ab9feba4a525`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-07 refresh.

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
    constraint path (see validation note below)

## 2) Existing open pgschema issue refresh

There is no open-issue parity-state delta versus the 2026-06-07 refresh.

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Draft-only uncovered open candidates

- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - pg-delta still has related but not identical dependency-ordering work in
    [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263),
    open PR [#273](https://github.com/supabase/pg-toolbelt/pull/273), and open
    PR [#275](https://github.com/supabase/pg-toolbelt/pull/275)
  - there is still no exact `DROP COLUMN` + dependent-view regression or
    dedicated tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

### Covered / not-parity open items with upstream movement

- pgschema [#420](https://github.com/pgplex/pgschema/issues/420) remains
  **covered** in pg-delta even though upstream fix PR
  [#438](https://github.com/pgplex/pgschema/pull/438) is merged
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427) remains
  **covered** in pg-delta while upstream fix PR
  [#428](https://github.com/pgplex/pgschema/pull/428) is still open
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421) /
  [#422](https://github.com/pgplex/pgschema/issues/422) remain **not parity**
  work for pg-delta; new upstream PR
  [#451](https://github.com/pgplex/pgschema/pull/451) overlaps the mixed-case
  trigger / FK quoting surface but does not change the pg-delta verdict
- pgschema [#449](https://github.com/pgplex/pgschema/issues/449) and
  [#450](https://github.com/pgplex/pgschema/issues/450) remain **not parity**
  work for pg-delta

No newer parity-relevant open pgschema issues appeared since the 2026-06-07
refresh.

## 3) Recently closed issue screening

No new parity-relevant pgschema closed issues or merged fix PRs changed the
benchmark since the 2026-06-07 refresh. The screened closed-item state remains
unchanged:

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406): indexes in
  `.pgschemaignore` remain not parity work for pg-delta
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output remain covered in current pg-delta
- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): `name` typed
  columns remain covered in current pg-delta
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints remains not covered
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables remain covered in current pg-delta
- pgschema [#426](https://github.com/pgplex/pgschema/issues/426): Docker Hub
  image lag remains not parity work for pg-delta
- pgschema [#445](https://github.com/pgplex/pgschema/issues/445): same-schema
  CHECK constraint qualifier drift remains not parity work for pg-delta
- pgschema [#446](https://github.com/pgplex/pgschema/issues/446): explicit
  `UNIQUE` constraints on `PRIMARY KEY` columns remain covered in current
  pg-delta

## 4) Validation notes

- `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  passed on current `pg-delta@f95e0a8b773539dfb60ebf541131ab9feba4a525`
- a focused one-off Bun probe constructed two otherwise-identical table
  constraints whose only difference was `UNIQUE (a, b)` versus
  `UNIQUE NULLS NOT DISTINCT (a, b)`. The current diff code returned:

  ```json
  {
    "changeCount": 0,
    "sql": []
  }
  ```

  That reproduces the unresolved benchmark 020 behavior on the current
  `pg-delta` head without needing a Docker-backed integration environment.
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  succeeded
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` succeeded
- `DRY_RUN=true python3 scripts/compare_issues.py` and
  `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  both returned zero items, which remains expected because most current
  pgschema issues are unlabeled and those scripts still filter on the
  `Bug` / `Feature` labels

## 5) Repo metadata refresh note

The upstream parity verdicts are unchanged, but this refresh still updates the
local benchmark metadata: `benchmark/review-memory.json` now uses the current
`pg-delta@f95e0a8b773539dfb60ebf541131ab9feba4a525` fingerprint and fresh
`reviewed_at` timestamps for the actively screened issues so the cache matches
the benchmark snapshot documented in `benchmark/README.md`.

# Parity refresh report - 2026-06-12

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`)
- `pg-delta` (`repos/pg-toolbelt` @ `436b3d19b1330970ccf158c4bb8ed6e59b7cef01`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-10 refresh.

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

## 2) Open pgschema issue refresh

Compared with the 2026-06-10 refresh, the live open-screening set changed shape:
previously open issues #436, #439, #445, and #449 are now closed upstream,
while new open issues #471, #472, and #473 need screening.

Current open-screening outcomes:

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49): explicit rename
  / refactor workflow proposal - **not parity** for pg-delta
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450): missing role
  blocks plan/apply - **not parity** for pg-delta
- pgschema [#471](https://github.com/pgplex/pgschema/issues/471): partitioned
  table RLS enablement - **covered** in current pg-delta's generic table RLS
  extraction and diff path
- pgschema [#472](https://github.com/pgplex/pgschema/issues/472): partition
  clone triggers with ignored child tables - **not parity** for pg-delta; the
  remaining mismatch is `.pgschemaignore` semantics, and current pg-delta
  already skips partition-clone triggers
- pgschema [#473](https://github.com/pgplex/pgschema/issues/473): partial-index
  predicate normalization (`IN (...)` vs `= ANY(ARRAY)`) - **not parity** for
  pg-delta because it compares canonical live-catalog predicates via
  `pg_get_expr(i.indpred, i.indrelid)` rather than dumped SQL text

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
  - now closed upstream, and current `pgschema` carries regression fixtures at
    `repos/pgschema/testdata/diff/dependency/issue_439_unique_to_pk_fk_dependent/`
  - still no exact pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  before dropping a dependent view in the same plan group
  - fixed upstream via
    [pgschema#466](https://github.com/pgplex/pgschema/pull/466) and already
    closed before this refresh
  - still no exact pg-toolbelt issue or PR found
  - related but non-duplicate work remains in
    [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263),
    merged PR [#273](https://github.com/supabase/pg-toolbelt/pull/273), and
    merged PR [#275](https://github.com/supabase/pg-toolbelt/pull/275)
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 3) Recently closed issue screening

Newly closed upstream since the 2026-06-10 refresh, with unchanged pg-delta
verdicts:

- pgschema [#436](https://github.com/pgplex/pgschema/issues/436): required
  extensions in dump output - **covered**
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439): `UNIQUE` to
  `PRIMARY KEY` replacement with dependents - **not covered** and still
  draft-only
- pgschema [#445](https://github.com/pgplex/pgschema/issues/445): same-schema
  CHECK constraint qualifier drift - **not parity**
- pgschema [#449](https://github.com/pgplex/pgschema/issues/449): repeated
  same-schema policy / CHECK drift after apply - **not parity**

## 4) Validation notes

- `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  passed on current `pg-delta@436b3d19b1330970ccf158c4bb8ed6e59b7cef01`
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
  passed
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` passed
- `DRY_RUN=true python3 scripts/compare_issues.py` and
  `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  both returned zero items once authenticated, which remains expected because
  most current pgschema issues are unlabeled and those scripts still filter on
  the `Bug` / `Feature` labels

## 5) Metadata refresh note

This refresh is still mostly about upstream state tracking rather than a
pg-delta code change. `benchmark/review-memory.json` now:

- moves #436, #439, #445, and #449 out of the `open` bucket and into
  `resolved`
- keeps #404 / #366 marked `tracked`
- keeps #412 / #439 / #444 marked `not_covered`
- keeps #49 / #450 marked `not_parity`
- adds pgschema [#471](https://github.com/pgplex/pgschema/issues/471) as
  `covered`, and [#472](https://github.com/pgplex/pgschema/issues/472) /
  [#473](https://github.com/pgplex/pgschema/issues/473) as `not_parity`
- refreshes active-entry fingerprints to
  `pgschema@8b7a248ce08f155b43b31cdee9ea38751aff6d5d` /
  `pg-delta@436b3d19b1330970ccf158c4bb8ed6e59b7cef01`

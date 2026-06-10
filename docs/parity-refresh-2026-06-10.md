# Parity refresh report - 2026-06-10

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `b0d7efafe297eaf2985981e9521c75bd9f02bc3b`)
- `pg-delta` (`repos/pg-toolbelt` @ `f95e0a8b773539dfb60ebf541131ab9feba4a525`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-08 refresh.

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

## 2) Open pgschema issue refresh

Compared with the 2026-06-08 refresh, the live open-screening set is much
smaller because pgschema closed a broad batch of previously screened issues on
2026-06-09 and 2026-06-10. The remaining parity-relevant open items are:

- pgschema [#436](https://github.com/pgplex/pgschema/issues/436): required
  extensions missing from dump output — **covered** in current pg-delta
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439): replacing
  `UNIQUE` with `PRIMARY KEY` when dependents still point at the old constraint
  — **not covered** and still draft-only in
  [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#445](https://github.com/pgplex/pgschema/issues/445): same-schema
  CHECK constraint qualifier drift — **not parity** for pg-delta
- pgschema [#449](https://github.com/pgplex/pgschema/issues/449) and
  [#450](https://github.com/pgplex/pgschema/issues/450) — **not parity** for
  pg-delta
- pgschema [#49](https://github.com/pgplex/pgschema/issues/49): explicit rename
  / refactor workflow proposal — **not parity** for pg-delta

No newer parity-relevant open pgschema issues appeared after #450 during this
refresh.

### Historical gaps still tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) is now closed
  upstream via [pgschema#458](https://github.com/pgplex/pgschema/pull/458), but
  the matching pg-delta parity tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218) remains
  open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) is now closed
  upstream after the temp-schema signature fix landed via
  [pgschema#379](https://github.com/pgplex/pgschema/pull/379), but the matching
  pg-delta parity tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219) remains
  open

### Historical draft-only gap with no exact pg-toolbelt tracker

- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  before dropping a dependent view in the same plan group
  - fixed upstream via
    [pgschema#466](https://github.com/pgplex/pgschema/pull/466) and now closed
  - still no exact pg-toolbelt issue or PR found
  - related but non-duplicate work remains in
    [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263),
    open PR [#273](https://github.com/supabase/pg-toolbelt/pull/273), and open
    PR [#275](https://github.com/supabase/pg-toolbelt/pull/275)
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

## 3) Recently closed issue screening

Newly closed upstream since the 2026-06-08 refresh, with unchanged pg-delta
verdicts:

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric
  precision changes — **covered**
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): enum-arg
  function privilege signatures — **tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401):
  `RETURNS SETOF <table>` dependency ordering — **covered**
- pgschema [#404](https://github.com/pgplex/pgschema/issues/404): deferrable
  unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#407](https://github.com/pgplex/pgschema/issues/407),
  [#409](https://github.com/pgplex/pgschema/issues/409),
  [#429](https://github.com/pgplex/pgschema/issues/429), and
  [#447](https://github.com/pgplex/pgschema/issues/447): `.pgschemaignore`
  follow-ups — **not parity**
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414): views created
  after `ADD COLUMN` changes — **covered**
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415):
  materialized-view refactors — **covered**
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416): custom
  aggregates missing from dump output — **covered**
- pgschema [#418](https://github.com/pgplex/pgschema/issues/418):
  `CREATE INDEX CONCURRENTLY` on partitioned parents — **not parity**
- pgschema [#419](https://github.com/pgplex/pgschema/issues/419):
  `.pgschemaignore` behavior differs by GitHub Actions install path —
  **not parity**
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation — **covered**; upstream fix
  [#438](https://github.com/pgplex/pgschema/pull/438) is now merged and closed
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421) and
  [#422](https://github.com/pgplex/pgschema/issues/422): quoted-name dump edge
  cases — **not parity**; merged upstream PR
  [#451](https://github.com/pgplex/pgschema/pull/451) overlaps the quoting
  surface but does not change the pg-delta verdict
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions — **covered**; upstream
  fix [#465](https://github.com/pgplex/pgschema/pull/465) is now merged and
  closed
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  with a dependent view — **not covered** and still draft-only

Older closed-item verdicts remain unchanged:

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406): indexes in
  `.pgschemaignore` — **not parity**
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output — **covered**
- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): `name` typed
  columns — **covered**
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints — **not covered**
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables — **covered**
- pgschema [#426](https://github.com/pgplex/pgschema/issues/426): Docker Hub
  image lag — **not parity**
- pgschema [#446](https://github.com/pgplex/pgschema/issues/446): explicit
  `UNIQUE` constraints on `PRIMARY KEY` columns — **covered**

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
  passed after the review-memory rebucketing and snapshot updates
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` passed
- `DRY_RUN=true python3 scripts/compare_issues.py` and
  `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  are still expected to return zero items because most current pgschema issues
  remain unlabeled and those scripts still filter on the `Bug` / `Feature`
  labels

## 5) Metadata refresh note

This refresh is mostly about upstream state tracking rather than a pg-delta code
change. `benchmark/review-memory.json` now:

- move newly closed issues out of the `open` bucket and into `resolved`
- keep #404 / #366 marked `tracked` even though pgschema closed them upstream
- keep #444 marked `not_covered` as a historical draft-only gap
- move pgschema [#445](https://github.com/pgplex/pgschema/issues/445) back into
  the `open` bucket, since it remains open upstream and is still `not_parity`
- refresh fingerprints to the current `pgschema@b0d7efafe297eaf2985981e9521c75bd9f02bc3b`
  / `pg-delta@f95e0a8b773539dfb60ebf541131ab9feba4a525` snapshot for the actively
  screened entries

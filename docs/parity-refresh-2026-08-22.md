# Parity refresh report - 2026-08-22

This report records the 2026-08-22 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9a09fe5861575ccfc71c7387ce3524b502992a97`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `d19314ac6586bfaabfaa7c2408038e44fdc7bb6a`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-21.md`](./parity-refresh-2026-08-21.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
    relation columns with `a.attislocal`, so child-local overrides on inherited
    partition columns never become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child-element
    list
  - the focused 2026-08-14 runtime probe remains representative because the new
    `pg-delta` work since 2026-08-21 did not touch the relevant extract or
    render paths
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
  - the focused 2026-08-14 runtime probe remains representative because the new
    `pg-delta` work since 2026-08-21 did not touch the relevant generated-
    column extract or render paths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, and `pgschema#444` returned no dedicated pg-toolbelt issue or
  PR
- keyword searches still surface open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332); the
  broad `PARTITION OF` term additionally hits generic closed backlog issue
  [#333](https://github.com/supabase/pg-toolbelt/issues/333), but not a better
  exact tracker

## 2) Upstream delta on 2026-08-22

Both code heads moved again today:

- checked-in/live `pg-delta` advanced from
  `18562f9a2eb01f181f1412dfeac1c1cea17ec579` to
  `d19314ac6586bfaabfaa7c2408038e44fdc7bb6a`
  (`@supabase/pg-delta@1.0.0-alpha.46`)
- the intervening merged pg-toolbelt work came from
  [#445](https://github.com/supabase/pg-toolbelt/pull/445),
  [#447](https://github.com/supabase/pg-toolbelt/pull/447), and release PR
  [#448](https://github.com/supabase/pg-toolbelt/pull/448); it touched
  load-assist, SQL-file ordering, extraction frontends, and CLI/export
  frontends, but did not touch the active benchmark codepaths in
  `src/extract/relations.ts`, `src/plan/rules/tables.ts`, or
  `src/plan/rules/helpers.ts`
- checked-in/live `pgschema` advanced from
  `9c81d465d76c20588d670ede188c6939febdf3ac` to
  `9a09fe5861575ccfc71c7387ce3524b502992a97`
- `pgschema` merged
  [pgschema#556](https://github.com/pgplex/pgschema/pull/556), which closes
  [#553](https://github.com/pgplex/pgschema/issues/553) by stubbing temporary
  role membership for `ALTER DEFAULT PRIVILEGES` in the external plan database

The current open pgschema issue set is now:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)

### Open-issue findings rechecked on current heads

- [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#450](https://github.com/pgplex/pgschema/issues/450) remain **not parity
  work for pg-delta**

### Newly closed parity-adjacent issue today

- [#553](https://github.com/pgplex/pgschema/issues/553) closed by
  [pgschema#556](https://github.com/pgplex/pgschema/pull/556) and remains
  **not parity work for pg-delta**; the merged fix is specific to pgschema's
  external plan database setup, while current pg-delta already exercises
  default-privilege planning in Supabase-style contexts

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest tracker context for active benchmarks **021** / **022**
- there are currently **no open pgschema PRs in parity-adjacent scope**
- current open pg-toolbelt PRs
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
  context, but none is an exact duplicate of the active benchmarks or the
  draft-only gaps
- direct issue/PR searches for `pgschema#499`, `pgschema#501`, `pgschema#439`,
  and `pgschema#444` all returned no matches

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` and `repos/pgschema` submodule
  pointers to current upstream heads
- refresh `benchmark/README.md` to the 2026-08-22 latest-state snapshot
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with the new-head
  recheck notes
- refresh `benchmark/review-memory.json` for the watch-list transition:
  - remove now-closed former-open issue **#553** from the `open` cache
  - add resolved entry **#553**
  - refresh active benchmark entries **#499** / **#501** plus still-open
    watch-list entries **#49**, **#52**, **#84**, and **#450** on the new
    heads
- add this report as the 2026-08-22 latest-state sweep
- no new draft-only pg-toolbelt issue markdown was needed because this refresh
  still found no dedicated exact duplicate beyond the existing umbrella issue
  context

## 4) Validation notes

This refresh was validated with:

- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `DRY_RUN=true python3 scripts/compare_issues.py` (**0** labeled open issues)
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  (**0** labeled resolved issues)
- `git diff --check`

Those dry-run script runs are still expected to return **0** parity items
because the current manually tracked open pgschema issues
**#49**, **#52**, **#84**, and **#450** do not carry the upstream `Bug` /
`Feature` labels the automation filters on.

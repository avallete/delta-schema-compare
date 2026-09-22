# Parity refresh report - 2026-08-25

This report records the 2026-08-25 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9a09fe5861575ccfc71c7387ce3524b502992a97`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `d19314ac6586bfaabfaa7c2408038e44fdc7bb6a`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-24.md`](./parity-refresh-2026-08-24.md):

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
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
- there was no fresh targeted runtime probe today; the 2026-08-14 runtime
  probes remain the latest direct runtime evidence, and today's same-head source
  recheck does not change them
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, and `pgschema#444` returned no dedicated pg-toolbelt issue or
  PR
- keyword searches for `VIRTUAL generated` and `PARTITION OF` still surface
  open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332); the
  broad `PARTITION OF` term additionally hits generic closed backlog issue
  [#333](https://github.com/supabase/pg-toolbelt/issues/333), but not a better
  exact tracker

## 2) Upstream delta on 2026-08-25

- there was **no code-head movement** since 2026-08-24; checked-in/live
  `pg-delta` remains at `d19314ac6586bfaabfaa7c2408038e44fdc7bb6a`
  (`@supabase/pg-delta@1.0.0-alpha.46`) and `pgschema` remains at
  `9a09fe5861575ccfc71c7387ce3524b502992a97` (`v1.12.4`)
- the current open pgschema issue set is now:
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#557](https://github.com/pgplex/pgschema/issues/557)
- new open unlabeled issue
  [#557](https://github.com/pgplex/pgschema/issues/557) ("Lock timeout and
  retries") is currently **not parity work for the benchmark**:
  - current pg-delta already exposes per-segment `lockTimeoutMs` on target
    `apply()` via
    `repos/pg-toolbelt/packages/pg-delta/src/apply/apply.ts` and
    `src/apply/apply-preamble.ts`
  - current pg-delta also has bounded retry behavior in the shadow SQL-file
    loader via
    `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - but there is still no live-target apply retry loop matching the pgschema
    request, and exact pg-toolbelt tracker searches for `pgschema#557` and
    `"lock timeout"` returned nothing
- no additional parity-adjacent pgschema issues closed or reopened between
  2026-08-24 and 2026-08-25
- there are still no open or newly merged parity-adjacent pgschema PRs
- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest pg-toolbelt tracker context for active benchmarks **021** / **022**
- current open pg-toolbelt PRs
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
  context, but none is an exact duplicate of the active benchmarks, the
  older draft-only gaps, or issue
  [#557](https://github.com/pgplex/pgschema/issues/557)

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-25 latest-state snapshot
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with same-head recheck
  notes
- refresh `benchmark/review-memory.json` reviewed timestamps for still-open
  watch-list issues **#49**, **#52**, **#84**, and **#450**, refresh active
  benchmarked issues **#499** and **#501**, and add new open issue **#557**
  as reviewed non-parity work
- add this report as the 2026-08-25 latest-state sweep
- no benchmark status rows changed, no new benchmark files were added, and no
  new draft-only pg-toolbelt issue markdown was needed

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues/PRs and pg-toolbelt
  issues/PRs, plus exact duplicate searches for `pgschema#499`,
  `pgschema#501`, `pgschema#439`, `pgschema#444`, `pgschema#557`,
  `VIRTUAL generated`, `PARTITION OF`, and `"lock timeout"`
- direct source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/apply/apply.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/apply/apply-preamble.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN=... DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN=... DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

Those dry-run script runs still return **0** parity items because the manually
tracked current open pgschema issues **#49**, **#52**, **#84**, **#450**, and
**#557** do not carry the upstream `Bug` / `Feature` labels the automation
filters on.

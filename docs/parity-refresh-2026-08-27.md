# Parity refresh report - 2026-08-27

This report records the 2026-08-27 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9a09fe5861575ccfc71c7387ce3524b502992a97`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `6f480e6ed707133e13bd76c5ff3a8df6102806ee`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-26.md`](./parity-refresh-2026-08-26.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- checked-in/live `pgschema` and `pg-delta` heads are unchanged from
  2026-08-26, so the active structural-gap evidence still stands
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
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both active benchmarks, and today's unchanged heads do not alter
  those specific codepaths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#557`, and `pgschema#559` returned
  no dedicated pg-toolbelt issue or PR
- keyword searches for `VIRTUAL generated` and `PARTITION OF` still only
  surface open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
- keyword searches for `lock timeout`, `config data`, and event-trigger RLS
  terms surfaced no exact pg-toolbelt duplicate for the newly changed pgschema
  watch-list context

## 2) Upstream delta on 2026-08-27

- checked-in/live `pg-delta` remains at
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
  (`@supabase/pg-delta@1.0.0-alpha.47`)
- checked-in/live `pgschema` remains at
  `9a09fe5861575ccfc71c7387ce3524b502992a97`
- the current open pgschema issue set now includes new issue
  [#559](https://github.com/pgplex/pgschema/issues/559) ("config data")
- issue [#559](https://github.com/pgplex/pgschema/issues/559) remains **not
  parity work for pg-delta**: the request is about declarative reference-data
  diffs, while pg-delta's SQL-file loader explicitly treats row-level
  comparison as out of scope (`packages/pg-delta/tests/load-sql-files.test.ts`
  notes that the loader "deliberately never compares data")
- pgschema now has an open PR on the existing watch list:
  [#558](https://github.com/pgplex/pgschema/pull/558) for issue
  [#557](https://github.com/pgplex/pgschema/issues/557)
- PR [#558](https://github.com/pgplex/pgschema/pull/558) adds
  `--lock-timeout-retries` and `--lock-timeout-retry-wait` for `pgschema apply`;
  this remains **not parity work for pg-delta today** because it is operational
  apply ergonomics rather than a schema-diff fidelity change, although current
  pg-delta does already expose `lockTimeoutMs` through
  `src/apply/apply-preamble.ts` and `src/cli/commands/schema.ts`
- open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) is useful new
  upstream context on the pg-delta side, but it does not correspond to a
  current open pgschema issue or an active benchmark scenario in this repo
- current open pg-toolbelt PRs remain
  [#449](https://github.com/supabase/pg-toolbelt/pull/449),
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288); none is an exact
  duplicate of the active benchmarks, the older draft-only gaps, or the new
  pgschema watch-list items

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-27 latest-state snapshot
- refresh `benchmark/review-memory.json` reviewed timestamps for the open watch
  list issues **#49**, **#52**, **#84**, **#450**, and **#557**
- add new open-issue cache entry for
  [#559](https://github.com/pgplex/pgschema/issues/559) with a `not_parity`
  verdict
- refresh the reviewed timestamps for the rechecked known gaps
  **#439**, **#444**, **#499**, and **#501**
- add this report as the 2026-08-27 latest-state sweep
- no benchmark status rows changed, no benchmark gap files changed, no new
  draft-only pg-toolbelt issue markdown was needed, and no submodule pointers
  moved today

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues/PRs and pg-toolbelt
  issues/PRs
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#439`,
  `pgschema#444`, `pgschema#557`, and `pgschema#559`
- keyword duplicate searches for `VIRTUAL generated`, `PARTITION OF`,
  `lock timeout`, `config data`, `event trigger RLS`, `enable row level
  security`, and `force row level security`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/apply/apply-preamble.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/cli/commands/schema.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run script runs are still expected to return **0** parity items because
the manually tracked current open pgschema issues **#49**, **#52**, **#84**,
**#450**, **#557**, and **#559** do not carry the upstream `Bug` / `Feature`
labels the automation filters on.

Bun is not installed in this pod, so no fresh pg-delta test run was available
locally today. Because the checked-in/live pg-delta head is unchanged from
2026-08-26, today's verdict rests on the GitHub state checks above plus the
existing unchanged active-gap codepath evidence.

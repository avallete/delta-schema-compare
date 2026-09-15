# Parity refresh report - 2026-08-29

This report records the 2026-08-29 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `00db700e74b2b255e1e570495ae59fda6af38ed7`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `013c2a2f00cf5f24259ed0344cf4b057e48cfc86`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-28.md`](./parity-refresh-2026-08-28.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- checked-in/live `pg-delta` advances to
  `013c2a2f00cf5f24259ed0344cf4b057e48cfc86`, but the diff from
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee` only touches
  `packages/pg-delta/README.md` and `packages/pg-delta/COVERAGE.md`
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
  evidence for both active benchmarks, and today's docs-only pg-delta head
  advance does not alter those specific codepaths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#559`, `pgschema#561`, and
  `pgschema#563` returned no dedicated pg-toolbelt issue or PR
- keyword searches for `VIRTUAL generated` and `PARTITION OF` still only
  surface open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332)
- keyword searches for `config data`, `existing data`, `lock timeout`, and
  `NULLS LAST` surfaced no exact pg-toolbelt duplicate for the current
  pgschema watch-list or recent resolved-issue context

## 2) Upstream delta on 2026-08-29

- checked-in/live `pg-delta` advances to
  `013c2a2f00cf5f24259ed0344cf4b057e48cfc86`
  (`@supabase/pg-delta@1.0.0-alpha.47-1-g013c2a2f`) via docs-only changes in
  `packages/pg-delta/README.md` and `packages/pg-delta/COVERAGE.md`
- checked-in/live `pgschema` remains at
  `00db700e74b2b255e1e570495ae59fda6af38ed7`; there were no new merged
  pgschema PRs after [#562](https://github.com/pgplex/pgschema/pull/562)
- new open issue [#563](https://github.com/pgplex/pgschema/issues/563)
  ("Dealing with migrations that impact existing data") remains **not parity
  work for pg-delta**: the issue is about workflow hooks for manual data
  migrations, while current pg-delta only diffs schema and explicitly documents
  in `src/frontends/load-sql-files.ts` plus
  `packages/pg-delta/tests/load-sql-files.test.ts` that the loader
  "deliberately never compares data"
- open issue [#559](https://github.com/pgplex/pgschema/issues/559) remains
  **not parity work for pg-delta** for the same schema-only reason
- there were no new closed pgschema issues after
  [#557](https://github.com/pgplex/pgschema/issues/557) /
  [#561](https://github.com/pgplex/pgschema/issues/561), so the 2026-08-28
  closed-issue conclusions still stand unchanged
- open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) remains useful
  current context on the pg-delta side, but it does not correspond to a current
  open pgschema issue or an active benchmark scenario in this repo
- current open pg-toolbelt PRs are
  [#453](https://github.com/supabase/pg-toolbelt/pull/453),
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288); none is an exact
  duplicate of the active benchmarks, the older draft-only gaps, or the new
  workflow/data watch-list issue [#563](https://github.com/pgplex/pgschema/issues/563)
- new pg-toolbelt PR [#453](https://github.com/supabase/pg-toolbelt/pull/453)
  is about Supabase-managed policy surfaces and `COMMENT ON POLICY`, which is
  adjacent upstream context rather than an exact tracker for the current
  partition-child or virtual-generated-column parity gaps

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-29 latest-state snapshot
- refresh `benchmark/review-memory.json` reviewed timestamps / fingerprints for
  the open watch-list issues **#49**, **#52**, **#84**, **#450**, **#559**, and
  new issue **#563**
- refresh the reviewed timestamps / fingerprints for the rechecked known gaps
  **#439**, **#444**, **#499**, and **#501**
- refresh the reviewed timestamps / fingerprints for recent resolved issues
  **#557** and **#561**
- refresh benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) to the current checked-in
  pg-delta head
- add this report as the 2026-08-29 latest-state sweep
- advance checked-in/live `pg-delta` to
  `013c2a2f00cf5f24259ed0344cf4b057e48cfc86`; checked-in/live `pgschema`
  remains `00db700e74b2b255e1e570495ae59fda6af38ed7`
- no benchmark status rows changed, no solved/active benchmark verdict changed,
  and no new draft-only pg-toolbelt issue markdown was needed

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues/PRs and pg-toolbelt
  issues/PRs
- `git -C repos/pg-toolbelt diff --stat 6f480e6ed707133e13bd76c5ff3a8df6102806ee 013c2a2f00cf5f24259ed0344cf4b057e48cfc86 -- packages/pg-delta`
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#439`,
  `pgschema#444`, `pgschema#559`, `pgschema#561`, and `pgschema#563`
- keyword duplicate searches for `VIRTUAL generated`, `PARTITION OF`,
  `config data`, `existing data`, `lock timeout`, and `NULLS LAST`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/indexes.ts`
- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run script runs are still expected to return **0** parity items because
the manually tracked current open pgschema issues **#49**, **#52**, **#84**,
**#450**, **#559**, and **#563** do not carry the upstream `Bug` / `Feature`
labels that the automation currently filters on.

No fresh pg-delta runtime test run was needed today because the only local
`packages/pg-delta` delta since 2026-08-28 is documentation. Behavioral
conclusions therefore rest on the unchanged source codepaths above plus the
focused 2026-08-14 runtime probes already recorded in the active benchmark
files.

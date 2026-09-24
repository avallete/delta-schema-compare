# Parity refresh report - 2026-08-30

This report records the 2026-08-30 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `00db700e74b2b255e1e570495ae59fda6af38ed7`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `107ac3df4b889c527215d1f6a37df64b33154c16`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-29.md`](./parity-refresh-2026-08-29.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- checked-in/live `pg-delta` advances to
  `107ac3df4b889c527215d1f6a37df64b33154c16`
  (`@supabase/pg-delta@1.0.0-alpha.48`) through merged PR
  [#453](https://github.com/supabase/pg-toolbelt/pull/453) plus release
  [#454](https://github.com/supabase/pg-toolbelt/pull/454)
- the diff from `013c2a2f00cf5f24259ed0344cf4b057e48cfc86` to
  `107ac3df4b889c527215d1f6a37df64b33154c16` only touches role/policy surfaces,
  related tests/fixtures, and package metadata; it does **not** touch the
  active benchmark codepaths in `src/extract/relations.ts`,
  `src/plan/rules/tables.ts`, or `src/plan/rules/helpers.ts`
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
  evidence for both active benchmarks, and today's role/policy pg-delta
  advance does not alter those specific codepaths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#559`, `pgschema#561`, and
  `pgschema#563` returned no dedicated pg-toolbelt issue or PR
- keyword searches for `VIRTUAL generated` still only surface open umbrella
  issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
- keyword searches for `PARTITION OF` now surface umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus open issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451), but #451 is about
  identical-SQL RLS drift rather than partition-child column overrides
- keyword searches for `config data`, `existing data`, `lock timeout`, and
  `NULLS LAST` surfaced no exact pg-toolbelt duplicate for the current
  pgschema watch-list or recent resolved-issue context

## 2) Upstream delta on 2026-08-30

- checked-in/live `pg-delta` advances from
  `013c2a2f00cf5f24259ed0344cf4b057e48cfc86`
  (`@supabase/pg-delta@1.0.0-alpha.47-1-g013c2a2f`) to
  `107ac3df4b889c527215d1f6a37df64b33154c16`
  (`@supabase/pg-delta@1.0.0-alpha.48`)
- the new pg-delta code arrived via merged PR
  [#453](https://github.com/supabase/pg-toolbelt/pull/453)
  (`feat(pg-delta): manage user RLS policies + policy comments on
  storage/realtime/auth`) and release
  [#454](https://github.com/supabase/pg-toolbelt/pull/454)
- previously open pg-toolbelt PR
  [#444](https://github.com/supabase/pg-toolbelt/pull/444)
  closed without merge on 2026-08-29 and is no longer in the active PR set
- current open pg-toolbelt PRs are now
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288); none is an exact
  duplicate of the active benchmarks, the older draft-only gaps, or the
  workflow/data watch-list issue
  [#563](https://github.com/pgplex/pgschema/issues/563)
- open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) remains useful
  current pg-delta context, but it does not correspond to a current open
  pgschema issue or an active benchmark scenario in this repo
- checked-in/live `pgschema` remains at
  `00db700e74b2b255e1e570495ae59fda6af38ed7`; the current open pgschema watch
  list is still
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#563](https://github.com/pgplex/pgschema/issues/563)
- there were no new merged pgschema PRs after
  [#562](https://github.com/pgplex/pgschema/pull/562) /
  [#560](https://github.com/pgplex/pgschema/pull/560), and no new closed
  pgschema issues after [#561](https://github.com/pgplex/pgschema/issues/561) /
  [#557](https://github.com/pgplex/pgschema/issues/557)
- open issues [#559](https://github.com/pgplex/pgschema/issues/559) and
  [#563](https://github.com/pgplex/pgschema/issues/563) remain **not parity
  work for pg-delta** because current pg-delta still explicitly documents in
  `src/frontends/load-sql-files.ts` and
  `packages/pg-delta/tests/load-sql-files.test.ts` that the loader
  "deliberately never compares data"

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-30 latest-state snapshot
- refresh `benchmark/review-memory.json` reviewed timestamps / fingerprints for
  the open watch-list issues **#49**, **#52**, **#84**, **#450**, **#559**,
  and **#563**
- refresh the reviewed timestamps / fingerprints for the rechecked known gaps
  **#439**, **#444**, **#499**, **#501**, **#557**, and **#561**
- refresh benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) to the current checked-in
  pg-delta head
- add this report as the 2026-08-30 latest-state sweep
- advance checked-in/live `pg-delta` to
  `107ac3df4b889c527215d1f6a37df64b33154c16`; checked-in/live `pgschema`
  remains `00db700e74b2b255e1e570495ae59fda6af38ed7`
- no benchmark status rows changed, no solved/active benchmark verdict changed,
  and no new draft-only pg-toolbelt issue markdown was needed

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues/PRs and pg-toolbelt
  issues/PRs
- `git -C repos/pg-toolbelt diff --stat 013c2a2f00cf5f24259ed0344cf4b057e48cfc86 107ac3df4b889c527215d1f6a37df64b33154c16 -- packages/pg-delta`
- `git -C repos/pg-toolbelt diff --name-only 013c2a2f00cf5f24259ed0344cf4b057e48cfc86 107ac3df4b889c527215d1f6a37df64b33154c16 -- packages/pg-delta`
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

No fresh pg-delta runtime test run was needed today because the pg-delta delta
since 2026-08-29 is confined to role/policy surfaces, related fixtures/tests,
and package metadata rather than the active 021/022 codepaths. Behavioral
conclusions therefore continue to rest on the unchanged source codepaths above
plus the focused 2026-08-14 runtime probes already recorded in the active
benchmark files.

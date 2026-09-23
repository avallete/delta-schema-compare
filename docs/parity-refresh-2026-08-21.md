# Parity refresh report - 2026-08-21

This report records the 2026-08-21 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9c81d465d76c20588d670ede188c6939febdf3ac`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `18562f9a2eb01f181f1412dfeac1c1cea17ec579`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-20.md`](./parity-refresh-2026-08-20.md):

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
  - the focused 2026-08-14 runtime probe remains representative: the latest head
    still did not touch the relevant extract or render paths
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
  - the focused 2026-08-14 runtime probe remains representative: the latest head
    still did not touch the relevant generated-column extract or render paths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, and `pgschema#444` returned no dedicated pg-toolbelt issue or
  PR
- keyword searches still surface open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332); the
  broad `PARTITION OF` term additionally hits generic closed backlog issue
  [#333](https://github.com/supabase/pg-toolbelt/issues/333), but not a better
  exact tracker

## 2) Upstream delta on 2026-08-21

Unlike the 2026-08-20 refresh, **both** code heads moved today:

- checked-in/live `pg-delta` advanced from
  `47bf101558f0c1e42cf59b272ac943537b5af483` to
  `18562f9a2eb01f181f1412dfeac1c1cea17ec579` (`@supabase/pg-delta@1.0.0-alpha.43`)
  via release PR [#441](https://github.com/supabase/pg-toolbelt/pull/441)
- the intervening merged pg-toolbelt work covered statement-fallback loading,
  serial `OWNED BY`, Supabase ACL policy shaping, extension relocation, vault
  presence, and vector fidelity, but did not touch the active benchmark
  codepaths in `src/extract/relations.ts`, `src/plan/rules/tables.ts`, or
  `src/plan/rules/helpers.ts`
- checked-in/live `pgschema` advanced from
  `91e45a1da95c4a36043ff520c8617bd7e7cc75ed` to
  `9c81d465d76c20588d670ede188c6939febdf3ac`
- `pgschema` merged:
  - [pgschema#554](https://github.com/pgplex/pgschema/pull/554), which closes
    [#551](https://github.com/pgplex/pgschema/issues/551) by recreating the
    policy when an explicit `WITH CHECK` clause is removed
  - [pgschema#555](https://github.com/pgplex/pgschema/pull/555), which closes
    [#552](https://github.com/pgplex/pgschema/issues/552) by stubbing cross-
    schema partition parents in the external plan database
- `pgschema` also now has open PR
  [#556](https://github.com/pgplex/pgschema/pull/556) for
  [#553](https://github.com/pgplex/pgschema/issues/553)

The current open pgschema issue set is now:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)
- [#553](https://github.com/pgplex/pgschema/issues/553)

### Open-issue findings rechecked on current heads

- [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#450](https://github.com/pgplex/pgschema/issues/450) remain **not parity
  work for pg-delta**
- [#553](https://github.com/pgplex/pgschema/issues/553) remains **not parity
  work for pg-delta**; upstream PR
  [pgschema#556](https://github.com/pgplex/pgschema/pull/556) adds role stubs
  for external-plan `ALTER DEFAULT PRIVILEGES`, while current pg-delta already
  exercises default-privilege planning in Supabase-style contexts through
  `src/plan/rules/default-privilege.test.ts` and
  `src/policy/supabase-default-privileges.test.ts`

### Newly closed parity-adjacent issues today

- [#493](https://github.com/pgplex/pgschema/issues/493) closed on 2026-08-21
  and remains **not parity work for pg-delta**; it is still a pgschema
  `--qualify-schema` render/IR follow-up rather than a pg-delta live-catalog
  diff gap
- [#551](https://github.com/pgplex/pgschema/issues/551) closed by
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554) and remains
  **covered** in current pg-delta; `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/policies.ts`
  still rebuilds policies when `usingExpr` / `checkExpr` changes, and
  `src/plan/policy-clause-removal.test.ts` still pins the clause-removal path
- [#552](https://github.com/pgplex/pgschema/issues/552) closed by
  [pgschema#555](https://github.com/pgplex/pgschema/pull/555) and remains
  **not parity work for pg-delta**; the merged upstream fix adds cross-schema
  partition-parent stubs in `repos/pgschema/cmd/plan/partition_stubs.go`,
  while pg-delta still diffs live catalogs directly and the active partition
  gap remains benchmark **021**

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest tracker context for active benchmarks **021** / **022**
- current open pg-toolbelt PRs
  [#442](https://github.com/supabase/pg-toolbelt/pull/442),
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
- refresh `benchmark/README.md` to the 2026-08-21 latest-state snapshot
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with the new-head
  recheck notes
- refresh `benchmark/review-memory.json` for the watch-list transition:
  - remove closed former-open issues **#493**, **#551**, and **#552** from the
    `open` cache
  - add/update resolved entries for **#493**, **#551**, and **#552**
  - refresh active benchmark entries **#499** / **#501** plus still-open
    watch-list entries **#49**, **#52**, **#84**, **#450**, and **#553** on the
    new heads
- add this report as the 2026-08-21 latest-state sweep
- no new draft-only pg-toolbelt issue markdown was needed because this refresh
  still found no dedicated exact duplicate beyond the existing umbrella issue
  context

## 4) Validation notes

This refresh was validated with:

- direct GitHub issue / PR checks for:
  - the current open pgschema issue set
    [#49](https://github.com/pgplex/pgschema/issues/49),
    [#52](https://github.com/pgplex/pgschema/issues/52),
    [#84](https://github.com/pgplex/pgschema/issues/84),
    [#450](https://github.com/pgplex/pgschema/issues/450), and
    [#553](https://github.com/pgplex/pgschema/issues/553)
  - newly closed parity-adjacent issues
    [#493](https://github.com/pgplex/pgschema/issues/493),
    [#551](https://github.com/pgplex/pgschema/issues/551), and
    [#552](https://github.com/pgplex/pgschema/issues/552)
  - the relevant pgschema PRs
    [#554](https://github.com/pgplex/pgschema/pull/554),
    [#555](https://github.com/pgplex/pgschema/pull/555), and
    [#556](https://github.com/pgplex/pgschema/pull/556)
  - the current pg-toolbelt issue / PR context including
    [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    [#442](https://github.com/supabase/pg-toolbelt/pull/442),
    [#432](https://github.com/supabase/pg-toolbelt/pull/432),
    [#303](https://github.com/supabase/pg-toolbelt/pull/303),
    [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
    [#288](https://github.com/supabase/pg-toolbelt/pull/288)
- source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/policies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/policy-clause-removal.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/default-privilege.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/supabase-default-privileges.test.ts`
  - `repos/pgschema/cmd/plan/partition_stubs.go`
  - `repos/pgschema/cmd/plan/partition_stubs_test.go`
- duplicate-search queries covering `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `PARTITION OF`, and `VIRTUAL generated`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `python3 -m pip install -r requirements.txt` (needed in this VM because the
  `openai` dependency was not preinstalled)
- `DRY_RUN=true python3 scripts/compare_issues.py` (**0** labeled open issues)
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  (**0** labeled resolved issues)
- `git diff --check`
- those dry-run script runs are still expected to return **0** parity items
  because the current manual-watch-list issues
  **#49**, **#52**, **#84**, **#450**, and **#553** do not carry the upstream
  `Bug` / `Feature` labels the automation filters on

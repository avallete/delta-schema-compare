# Parity refresh report - 2026-08-19

This report records the 2026-08-19 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `47bf101558f0c1e42cf59b272ac943537b5af483`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-18.md`](./parity-refresh-2026-08-18.md):

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
  - the last focused runtime probe (2026-08-14) remains representative: it
    emitted only the bare `PARTITION OF ... FOR VALUES ...` statement and the
    proof loop stayed blind to the missing overrides
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
  - the last focused runtime probe (2026-08-14) remains representative: a PG18
    `VIRTUAL` generated column still serialized as `... STORED`, and the proof
    loop stayed blind to the mismatch
- keyword duplicate searches still surface only umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332); the
  relevant context still lives in issue comments rather than the original issue
  body, and there is still no dedicated exact issue or PR for benchmark **021**
  or **022**

## 2) Upstream delta on 2026-08-19

The important upstream change since the 2026-08-18 refresh is one-sided:

- checked-in/live `pg-delta` is unchanged at
  `47bf101558f0c1e42cf59b272ac943537b5af483`
- checked-in/live `pgschema` advanced from
  `843aac05eac082b3f9e486504a5d72f0c7983d7f` to
  `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`

Current open pgschema issue set relevant to this repo is now:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)
- [#493](https://github.com/pgplex/pgschema/issues/493)
- [#551](https://github.com/pgplex/pgschema/issues/551)
- [#552](https://github.com/pgplex/pgschema/issues/552)
- [#553](https://github.com/pgplex/pgschema/issues/553)

### Open-issue findings rechecked on the new heads

- [#49](https://github.com/pgplex/pgschema/issues/49) remains **not parity work
  for pg-delta**
- [#52](https://github.com/pgplex/pgschema/issues/52) remains **not parity work
  for pg-delta**
- [#84](https://github.com/pgplex/pgschema/issues/84) remains **not parity work
  for pg-delta**
- [#450](https://github.com/pgplex/pgschema/issues/450) remains **not parity
  work for pg-delta**
- [#493](https://github.com/pgplex/pgschema/issues/493) remains **not parity
  work for pg-delta**
- [#551](https://github.com/pgplex/pgschema/issues/551) is **covered** in
  current pg-delta; policy clause removal rebuilds the policy instead of
  emitting invalid `ALTER POLICY ... WITH CHECK ;`
- [#552](https://github.com/pgplex/pgschema/issues/552) is **not parity work
  for pg-delta**; the failure is specific to pgschema's external-plan /
  temporary-schema construction path, while pg-delta diffs live catalogs
  directly and already preserves fully qualified parent-table schema data for
  partition children
- [#553](https://github.com/pgplex/pgschema/issues/553) is **not parity work
  for pg-delta**; the failure is another external-plan permission/setup issue,
  while current pg-delta already exercises default-privilege planning in
  Supabase-style contexts

### Recently closed upstream issues screened in this refresh

- [#548](https://github.com/pgplex/pgschema/issues/548) closed by
  [pgschema#549](https://github.com/pgplex/pgschema/pull/549) and remains
  **not parity work for pg-delta**

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest tracker context for active benchmarks **021** / **022**, but the
  relevant notes still live in issue comments rather than the issue body
- current open pg-toolbelt PRs
  [#433](https://github.com/supabase/pg-toolbelt/pull/433),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022** or the newly screened pgschema issues **#551** / **#552** / **#553**
- direct duplicate searches still find no dedicated exact open pg-toolbelt
  issue or PR for benchmark **021**, benchmark **022**, or the draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The 2026-08-19 delta is:

- advance the checked-in `pgschema` submodule pointer to
  `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`
- refresh `benchmark/README.md` to:
  - record the new checked-in/live heads
  - replace open issue **#548** with open issues **#551**, **#552**, and
    **#553**
  - move **#548** into the closed-issue notes
  - record that **#551** is already covered in current pg-delta while **#552**
    and **#553** are not parity work
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with the current head
  SHAs
- refresh `benchmark/review-memory.json` for:
  - the current open pgschema watch-list issue set
  - resolved issue **#548**
  - benchmark **021** / pgschema **#499** -> still `tracked`
  - benchmark **022** / pgschema **#501** -> still `tracked`
- add this report as the 2026-08-19 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#551](https://github.com/pgplex/pgschema/issues/551),
    [#552](https://github.com/pgplex/pgschema/issues/552), and
    [#553](https://github.com/pgplex/pgschema/issues/553)
  - the newly closed pgschema issue
    [#548](https://github.com/pgplex/pgschema/issues/548) and merged fix PR
    [#549](https://github.com/pgplex/pgschema/pull/549)
  - the current pg-toolbelt issue / PR context including
    [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    [#433](https://github.com/supabase/pg-toolbelt/pull/433),
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
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/supabase-default-privileges.test.ts`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `DRY_RUN=true python3 scripts/compare_issues.py` (**0** labeled open issues)
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  (**0** labeled resolved issues)
- those dry-run script runs are still expected to return **0** parity items
  because the current manual-watch-list issues
  **#49**, **#52**, **#84**, **#450**, **#493**, **#551**, **#552**, and
  **#553** do not carry the upstream `Bug` / `Feature` labels the automation
  filters on
- an attempted focused `bun test` recheck for the pg-delta policy-only unit
  tests could not run in this VM because Bun is not installed on `PATH`, so the
  #551 / #553 classifications rely on the current checked-in source and test
  corpus rather than an extra local Bun execution in this environment

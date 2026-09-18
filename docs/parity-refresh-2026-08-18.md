# Parity refresh report - 2026-08-18

This report records the 2026-08-18 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `843aac05eac082b3f9e486504a5d72f0c7983d7f`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `47bf101558f0c1e42cf59b272ac943537b5af483`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-14.md`](./parity-refresh-2026-08-14.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the new heads

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
  relevant context now lives in issue comments rather than the original issue
  body, and there is still no dedicated exact issue or PR for benchmark **021**
  or **022**

## 2) Upstream delta on 2026-08-18

The important upstream changes since the 2026-08-14 refresh land on both sides:

- checked-in/live `pg-delta` advanced from
  `551e88b42977db673a7a9d74f7b7876c2a5e5377` to
  `47bf101558f0c1e42cf59b272ac943537b5af483`
- checked-in/live `pgschema` advanced from
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e` to
  `843aac05eac082b3f9e486504a5d72f0c7983d7f`

Current open pgschema issue set relevant to this repo is now:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)
- [#493](https://github.com/pgplex/pgschema/issues/493)
- [#548](https://github.com/pgplex/pgschema/issues/548)

### Open-issue findings rechecked on the new heads

- [#49](https://github.com/pgplex/pgschema/issues/49) remains **not parity
  work for pg-delta**
- [#52](https://github.com/pgplex/pgschema/issues/52) remains **not parity
  work for pg-delta**
- [#84](https://github.com/pgplex/pgschema/issues/84) remains **not parity
  work for pg-delta**
- [#450](https://github.com/pgplex/pgschema/issues/450) remains **not parity
  work for pg-delta**
- [#493](https://github.com/pgplex/pgschema/issues/493) remains **not parity
  work for pg-delta**
- [#548](https://github.com/pgplex/pgschema/issues/548) is **not parity work
  for pg-delta**; it is a pgschema desired-state dump-scope problem for
  cross-schema FKs to `auth.users`, and open pgschema PR
  [#549](https://github.com/pgplex/pgschema/pull/549) is the upstream fix path

### Recently closed upstream issues screened in this refresh

- [#518](https://github.com/pgplex/pgschema/issues/518) closed by
  [pgschema#544](https://github.com/pgplex/pgschema/pull/544) and remains
  **not parity work for pg-delta**
- [#519](https://github.com/pgplex/pgschema/issues/519) closed by
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520) and remains
  **not parity work for pg-delta**
- [#534](https://github.com/pgplex/pgschema/issues/534) closed by
  [pgschema#540](https://github.com/pgplex/pgschema/pull/540) and remains
  **covered** in current pg-delta
- [#535](https://github.com/pgplex/pgschema/issues/535) closed by
  [pgschema#539](https://github.com/pgplex/pgschema/pull/539) and remains
  **covered** in current pg-delta
- [#536](https://github.com/pgplex/pgschema/issues/536) closed upstream and
  remains **covered** in current pg-delta
- [#537](https://github.com/pgplex/pgschema/issues/537) closed by
  [pgschema#541](https://github.com/pgplex/pgschema/pull/541), remains
  **covered** in current pg-delta, and still maps cleanly to solved benchmark
  family [005](../benchmark/005-alter-column-type-using-clause.md)
- [#538](https://github.com/pgplex/pgschema/issues/538) closed upstream; current
  pg-delta already has trigger-drop-before-function-drop coverage (historical
  tracker [pg-toolbelt#137](https://github.com/supabase/pg-toolbelt/issues/137)
  plus the `trigger-operations--trigger-drop-before-function-drop` corpus
  scenario)
- [#545](https://github.com/pgplex/pgschema/issues/545) closed by
  [pgschema#546](https://github.com/pgplex/pgschema/pull/546); current
  pg-delta already resolves routine signature dependencies on relation row
  types through `pg_depend` in
  `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`, so no new
  benchmark file or duplicate tracker is needed

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest tracker context for active benchmarks **021** / **022**, but the
  relevant notes now live in issue comments rather than the issue body
- current open pg-toolbelt PRs
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022** or open pgschema issue **#548**
- direct duplicate searches still find no dedicated exact open pg-toolbelt
  issue or PR for benchmark **021**, benchmark **022**, or the draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The 2026-08-18 delta is:

- advance the checked-in `pg-delta` submodule pointer to
  `47bf101558f0c1e42cf59b272ac943537b5af483`
- advance the checked-in `pgschema` submodule pointer to
  `843aac05eac082b3f9e486504a5d72f0c7983d7f`
- refresh `benchmark/README.md` to:
  - record the new checked-in/live heads
  - shrink the open watch list to the current six open pgschema issues
  - move newly closed issues into the closed-issue notes
  - clarify that issue-thread comments on
    [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332), not
    its original body, carry the active-gap context
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with the current
  extractor/planner evidence on the new heads
- refresh `benchmark/review-memory.json` for:
  - the current open pgschema watch-list issue set
  - newly closed screened issues **#518**, **#519**, **#534**, **#535**,
    **#536**, **#537**, **#538**, and **#545**
  - benchmark **021** / pgschema **#499** -> still `tracked`
  - benchmark **022** / pgschema **#501** -> still `tracked`
- add this report as the 2026-08-18 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#548](https://github.com/pgplex/pgschema/issues/548)
  - recently closed pgschema issues
    [#518](https://github.com/pgplex/pgschema/issues/518),
    [#519](https://github.com/pgplex/pgschema/issues/519),
    [#534](https://github.com/pgplex/pgschema/issues/534),
    [#535](https://github.com/pgplex/pgschema/issues/535),
    [#536](https://github.com/pgplex/pgschema/issues/536),
    [#537](https://github.com/pgplex/pgschema/issues/537),
    [#538](https://github.com/pgplex/pgschema/issues/538), and
    [#545](https://github.com/pgplex/pgschema/issues/545)
  - relevant recent pgschema PRs
    [#540](https://github.com/pgplex/pgschema/pull/540),
    [#541](https://github.com/pgplex/pgschema/pull/541),
    [#544](https://github.com/pgplex/pgschema/pull/544),
    [#546](https://github.com/pgplex/pgschema/pull/546), and
    [#549](https://github.com/pgplex/pgschema/pull/549)
  - the current pg-toolbelt issue / PR context including
    [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    [#432](https://github.com/supabase/pg-toolbelt/pull/432),
    [#303](https://github.com/supabase/pg-toolbelt/pull/303),
    [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
    [#288](https://github.com/supabase/pg-toolbelt/pull/288)
- duplicate-search review against the current open pg-toolbelt issue / PR lists
- source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/triggers.ts`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs are still expected to return **0** parity items
  because the current open pgschema watch-list issues
  **#49**, **#52**, **#84**, **#450**, **#493**, and **#548** do not carry the
  upstream `Bug` / `Feature` labels the automation filters on
- `git diff --check`

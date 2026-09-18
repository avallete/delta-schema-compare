# Parity refresh report - 2026-08-20

This report records the 2026-08-20 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `47bf101558f0c1e42cf59b272ac943537b5af483`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-19.md`](./parity-refresh-2026-08-19.md):

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
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
- direct duplicate searches still find no dedicated exact open pg-toolbelt
  issue or PR for benchmark **021**, benchmark **022**, or the draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 2) Upstream delta on 2026-08-20

Unlike the 2026-08-19 refresh, the code heads did not move today:

- checked-in/live `pg-delta` remains at
  `47bf101558f0c1e42cf59b272ac943537b5af483`
- checked-in/live `pgschema` remains at
  `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`
- there were no newly closed parity-scope pgschema issues since the
  2026-08-19 refresh

The current open pgschema issue set remains:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)
- [#493](https://github.com/pgplex/pgschema/issues/493)
- [#551](https://github.com/pgplex/pgschema/issues/551)
- [#552](https://github.com/pgplex/pgschema/issues/552)
- [#553](https://github.com/pgplex/pgschema/issues/553)

### Open-issue findings rechecked on the same heads

- [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493) remain **not parity
  work for pg-delta**
- [#551](https://github.com/pgplex/pgschema/issues/551) remains **covered** in
  current pg-delta; upstream now has open fix PR
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554), but it follows
  the same drop-and-recreate policy direction pg-delta already implements
- [#552](https://github.com/pgplex/pgschema/issues/552) was updated on
  2026-08-20 and remains **not parity work for pg-delta**; the failure is
  specific to pgschema's external-plan / temporary-schema construction path,
  while pg-delta diffs live catalogs directly and already preserves parent-table
  schema identity in partition facts
- [#553](https://github.com/pgplex/pgschema/issues/553) was updated on
  2026-08-20 and remains **not parity work for pg-delta**; the failure is
  another external-plan permission/setup issue, while current pg-delta already
  exercises default-privilege planning in Supabase-style contexts

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest tracker context for active benchmarks **021** / **022**, but the
  relevant notes still live in issue comments rather than the issue body
- current open pg-toolbelt PRs
  [#434](https://github.com/supabase/pg-toolbelt/pull/434),
  [#433](https://github.com/supabase/pg-toolbelt/pull/433),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022**, the updated open pgschema issues **#552** / **#553**, or the
  draft-only gaps **#439** / **#444**
- direct search queries for `pgschema#499`, `pgschema#501`, `pgschema#439`,
  `pgschema#444`, `PARTITION OF`, `VIRTUAL generated column`, `WITH CHECK`, and
  `ALTER DEFAULT PRIVILEGES` found no better exact duplicate than the existing
  umbrella thread

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-20 latest-state snapshot
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with a same-head
  2026-08-20 recheck note
- refresh `benchmark/review-memory.json` for the re-screened open watch-list
  issues and active benchmark entries, including the new `updated_at`
  fingerprints for open issues **#552** / **#553**
- no new draft-only pg-toolbelt issue markdown was needed because this refresh
  found no new exact uncovered pg-toolbelt duplicate/tracker candidate beyond
  the existing umbrella issue context
- add this report as the 2026-08-20 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- direct GitHub issue / PR checks for:
  - the current open pgschema issue set
    [#49](https://github.com/pgplex/pgschema/issues/49),
    [#52](https://github.com/pgplex/pgschema/issues/52),
    [#84](https://github.com/pgplex/pgschema/issues/84),
    [#450](https://github.com/pgplex/pgschema/issues/450),
    [#493](https://github.com/pgplex/pgschema/issues/493),
    [#551](https://github.com/pgplex/pgschema/issues/551),
    [#552](https://github.com/pgplex/pgschema/issues/552), and
    [#553](https://github.com/pgplex/pgschema/issues/553)
  - the new parity-adjacent open pgschema PR
    [#554](https://github.com/pgplex/pgschema/pull/554)
  - the current pg-toolbelt issue / PR context including
    [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    [#434](https://github.com/supabase/pg-toolbelt/pull/434),
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
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/default-privilege.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/supabase-default-privileges.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/policy.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/policy.test.ts`
- GitHub search queries covering `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `PARTITION OF`, `VIRTUAL generated column`,
  `WITH CHECK`, and `ALTER DEFAULT PRIVILEGES`
- `python3 -m pip install -r requirements.txt` (needed in this VM because the
  `openai` dependency was missing before the dry-run script checks)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `DRY_RUN=true python3 scripts/compare_issues.py` (**0** labeled open issues)
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  (**0** labeled resolved issues)
- `git diff --check`
- those dry-run script runs are still expected to return **0** parity items
  because the current manual-watch-list issues
  **#49**, **#52**, **#84**, **#450**, **#493**, **#551**, **#552**, and
  **#553** do not carry the upstream `Bug` / `Feature` labels the automation
  filters on

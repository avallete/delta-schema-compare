# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-08-20)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `47bf101558f0c1e42cf59b272ac943537b5af483`
- checked-in/live `repos/pgschema` @ `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`

> The 2026-08-20 refresh finds **no behavioral benchmark-matrix delta** versus
> the 2026-08-19 snapshot.
>
> - the active benchmarked gap set remains **021** and **022**
> - checked-in/live `repos/pg-toolbelt` remains
>   `47bf101558f0c1e42cf59b272ac943537b5af483`
> - checked-in/live `repos/pgschema` remains
>   `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`
> - source inspection on the current `pg-delta` head still shows the same
>   structural gaps:
>   - `src/extract/relations.ts` still filters relation columns with
>     `a.attislocal`, so inherited partition-child local overrides never become
>     diff-visible facts
>   - `src/plan/rules/tables.ts` still hard-codes bare
>     `CREATE TABLE ... PARTITION OF ... ${bound}` rendering with no typed child
>     column-element list
>   - `src/extract/relations.ts` still stores only `generatedExpr` from
>     `attgenerated`
>   - `src/plan/rules/helpers.ts` still hard-codes
>     `GENERATED ALWAYS AS (...) STORED`
> - the open pgschema issue set is unchanged, but
>   [#551](https://github.com/pgplex/pgschema/issues/551),
>   [#552](https://github.com/pgplex/pgschema/issues/552), and
>   [#553](https://github.com/pgplex/pgschema/issues/553) were rechecked on the
>   same heads: **#551 is still covered** in current pg-delta, while **#552**
>   and **#553** remain **not parity work for pg-delta**. Upstream now also has
>   open fix PR [pgschema#554](https://github.com/pgplex/pgschema/pull/554) for
>   **#551**, but that does not change pg-delta parity state.
> - keyword duplicate searches on pg-toolbelt still surface only umbrella
>   fidelity issue [#332](https://github.com/supabase/pg-toolbelt/issues/332);
>   comments on that issue thread (not the original issue body) now carry both
>   the inherited-column local-override note and the PG17/18 virtual-generated-
>   column note
> - there were no new parity-scope closed pgschema issues since the 2026-08-19
>   refresh
> - current open pg-toolbelt PRs
>   [#434](https://github.com/supabase/pg-toolbelt/pull/434),
>   [#433](https://github.com/supabase/pg-toolbelt/pull/433),
>   [#432](https://github.com/supabase/pg-toolbelt/pull/432),
>   [#303](https://github.com/supabase/pg-toolbelt/pull/303),
>   [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
>   [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
>   context, but direct duplicate searches still find **no dedicated exact
>   pg-toolbelt issue or PR** for the active benchmarks **021** / **022** or the
>   older draft-only gaps
>   [#439](https://github.com/pgplex/pgschema/issues/439) /
>   [#444](https://github.com/pgplex/pgschema/issues/444)

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed), replacement [#231](https://github.com/supabase/pg-toolbelt/pull/231) (merged) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [UNIQUE constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | none found | none found | **Solved in pg-delta** |
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Two resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** - PostgreSQL 18 `VIRTUAL` generated columns

Source inspection on 2026-08-19 current heads still shows:

- benchmark **021** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  child-inherited columns with `a.attislocal`, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
  only a bare `CREATE TABLE ... PARTITION OF ... FOR VALUES ...` form with no
  child-local column-element list
- benchmark **022** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still collapses
  `attgenerated` to `generatedExpr`, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still renders
  generated columns as `... STORED`
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both scenarios; nothing in the 2026-08-19 state changes those
  specific codepaths
- comments on the umbrella tracker
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  now carry both fidelity-gap notes, but there is still no dedicated exact
  issue or PR for either benchmark

## Open pgschema issue screening (current state)

The current open pgschema issue set is:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#450](https://github.com/pgplex/pgschema/issues/450),
[#493](https://github.com/pgplex/pgschema/issues/493),
[#551](https://github.com/pgplex/pgschema/issues/551),
[#552](https://github.com/pgplex/pgschema/issues/552), and
[#553](https://github.com/pgplex/pgschema/issues/553).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity
  work for pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work
  for pg-delta**
- **#450** missing role blocks plan/apply - **not parity work for
  pg-delta**; this remains specific to pgschema's desired-state temp
  schema workflow, while pg-delta diffs live catalogs directly
- **#493** `--qualify-schema` type-reference follow-up work - **not parity
  work for pg-delta**
- **#551** removing an explicit RLS `WITH CHECK` clause - **covered** in
  current pg-delta; `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/policies.ts`
  rebuilds policies when `usingExpr` / `checkExpr` changes,
  `src/plan/policy-clause-removal.test.ts` pins the clause-removal path, and
  upstream now has open fix PR
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554) carrying the same
  drop-and-recreate direction
- **#552** cross-schema partition child planning with an external plan database
  - **not parity work for pg-delta**; the issue was updated on 2026-08-20 but
  remains a pgschema temporary-plan-schema construction failure, while pg-delta
  diffs live catalogs directly and its partition facts / render path already
  preserve fully qualified parent-table schema information
- **#553** external plan database rejects `ALTER DEFAULT PRIVILEGES` in
  Supabase-style plans - **not parity work for pg-delta**; the issue was
  updated on 2026-08-20 but remains a pgschema external-plan
  permission/setup problem, while current pg-delta already exercises default-
  privilege planning in Supabase-style contexts
  (`src/plan/rules/default-privilege.test.ts`,
  `src/policy/supabase-default-privileges.test.ts`)

There is currently **no dedicated exact open pg-toolbelt parity tracker** for
the active benchmarks above or for the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444). The remaining active
benchmarks **021** / **022** are only adjacently tracked under the open
umbrella fidelity issue
[pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332):
keyword duplicate searches still surface that issue, and comments on the issue
thread carry both gap notes, but there is still no dedicated issue or PR for
either benchmark.

## Recent closed-issue / tracker updates

- **#404** deferrable unique constraints - **covered** in current
  pg-delta; exact tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#366** enum-arg function privilege signatures - **covered** in
  current pg-delta; exact tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#412** `UNIQUE NULLS NOT DISTINCT` on table constraints - now
  **covered** in current pg-delta; benchmark [020](020-unique-constraint-nulls-not-distinct.md)
  is retained as a historical record
- **#518** extension-owned type schema mismatch - closed by
  [pgschema#544](https://github.com/pgplex/pgschema/pull/544) and still
  **not parity work for pg-delta**
- **#519** view normalization through the temporary plan schema - closed by
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520) and still
  **not parity work for pg-delta**
- **#534** self-referencing FK to a non-PK standalone unique index on the same
  table - closed by [pgschema#540](https://github.com/pgplex/pgschema/pull/540)
  and remains **covered** in current pg-delta
- **#535** domain created over a table row type - closed by
  [pgschema#539](https://github.com/pgplex/pgschema/pull/539) and remains
  **covered** in current pg-delta
- **#536** dropping a foreign-keyed table/column in the wrong order - closed
  upstream and remains **covered** in current pg-delta
- **#537** built-in `ALTER COLUMN TYPE` without a `USING` clause - closed by
  [pgschema#541](https://github.com/pgplex/pgschema/pull/541), remains
  **covered** in current pg-delta, and matches the solved benchmark family in
  [005](005-alter-column-type-using-clause.md)
- **#538** dropping a table with a trigger - closed upstream; current pg-delta
  already has trigger-drop-before-function-drop coverage (historical tracker
  [pg-toolbelt#137](https://github.com/supabase/pg-toolbelt/issues/137) plus
  the `trigger-operations--trigger-drop-before-function-drop` corpus scenario)
- **#545** function signature depends on a deferred table row type - closed by
  [pgschema#546](https://github.com/pgplex/pgschema/pull/546); current
  pg-delta already resolves routine signature dependencies on relation row
  types through `pg_depend` in
  `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`, so no new
  benchmark file or duplicate tracker is needed
- **#548** cross-schema FK to `auth.users` when the `auth` schema is
  intentionally excluded from a pgschema dump - closed by
  [pgschema#549](https://github.com/pgplex/pgschema/pull/549) and remains
  **not parity work for pg-delta**; pg-delta diffs live catalogs directly and
  already carries `auth`-schema fixtures, so no benchmark or duplicate tracker
  change is needed
- **#499** child-specific column elements on `PARTITION OF` create -
  still **not covered in current behavior**, with only umbrella-thread context
  from [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [021](021-partition-child-column-overrides.md)
- **#501** PostgreSQL 18 `VIRTUAL` generated columns - still **not covered in
  current behavior**, with only umbrella-thread context from
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [022](022-virtual-generated-columns.md)
- **#506** new-table FK before standalone unique index - **covered** in
  current pg-delta; benchmark [023](023-fk-before-standalone-unique-index.md)
  is retained as a historical record
- draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444) still have no
  exact pg-toolbelt issue or PR

## Upstream watch list

- there is currently **one open pgschema PR in parity-adjacent scope**:
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554) for issue
  [#551](https://github.com/pgplex/pgschema/issues/551). It carries the same
  policy-rebuild direction current pg-delta already covers, so it does not
  change the active benchmark gap set
- checked-in/live `pg-toolbelt` remains at
  `47bf101558f0c1e42cf59b272ac943537b5af483`
- checked-in/live `pgschema` remains at
  `91e45a1da95c4a36043ff520c8617bd7e7cc75ed`
- comments on open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remain the
  closest tracker context for benchmarks **021** / **022**
- current open pg-toolbelt PRs
  [#434](https://github.com/supabase/pg-toolbelt/pull/434),
  [#433](https://github.com/supabase/pg-toolbelt/pull/433),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022**, the newly updated open pgschema issues **#552** / **#553**, or the
  draft-only gaps **#439** / **#444**

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by
  the automation scripts.
